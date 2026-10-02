#include <Windows.h>
#include <d3d11.h>
#include <d3dcompiler.h>
#include <dxgi.h>

#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <cstring>
#include <memory>
#include <vector>

#include <spdlog/sinks/basic_file_sink.h>

#include "F4SE/F4SE.h"
#include "RE/Fallout.h"
#include "REL/Relocation.h"

namespace logger = F4SE::log;

namespace
{
    constexpr wchar_t kMappingName[] = L"Local\\FalloutCraft_v1";
    constexpr std::size_t kHeaderBase = 0x340;
    constexpr std::size_t kHeaderStride = 0x40;
    constexpr std::size_t kPixelsBase = 0x2020000;
    constexpr std::size_t kPixelStride = 0x1FA4000;
    constexpr std::uint32_t kMaxW = 3840;
    constexpr std::uint32_t kMaxH = 2160;

    struct Slot
    {
        std::uint32_t width{};
        std::uint32_t height{};
        std::uint32_t flags{};
        std::uint64_t frameId{};
        int index{-1};
    };

    struct Params
    {
        float flipY{};
        float pad[3]{};
    };

    HANDLE g_mapping = nullptr;
    const std::uint8_t* g_shared = nullptr;
    std::uint64_t g_lastFrame = 0;

    ID3D11Device* g_device = nullptr;
    ID3D11DeviceContext* g_context = nullptr;
    ID3D11Texture2D* g_texture = nullptr;
    ID3D11ShaderResourceView* g_srv = nullptr;
    ID3D11VertexShader* g_vs = nullptr;
    ID3D11PixelShader* g_ps = nullptr;
    ID3D11SamplerState* g_sampler = nullptr;
    ID3D11BlendState* g_blend = nullptr;
    ID3D11DepthStencilState* g_depth = nullptr;
    ID3D11RasterizerState* g_raster = nullptr;
    ID3D11Buffer* g_params = nullptr;
    std::uint32_t g_texW = 0, g_texH = 0;
    bool g_flipY = true;
    bool g_rendererReady = false;
    bool g_rendererFailed = false;

    using PresentFn = HRESULT(__stdcall*)(IDXGISwapChain*, UINT, UINT);
    PresentFn g_originalPresent = nullptr;

    using CreateFn = HRESULT(WINAPI*)(
        IDXGIAdapter*, D3D_DRIVER_TYPE, HMODULE, UINT,
        const D3D_FEATURE_LEVEL*, UINT, UINT,
        const DXGI_SWAP_CHAIN_DESC*, IDXGISwapChain**,
        ID3D11Device**, D3D_FEATURE_LEVEL*, ID3D11DeviceContext**);
    CreateFn g_originalCreate = nullptr;

    template <class T>
    void Release(T*& p)
    {
        if (p) {
            p->Release();
            p = nullptr;
        }
    }

    void SetupLog()
    {
        auto dir = F4SE::log::log_directory();
        if (!dir) {
            return;
        }
        auto sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(
            (*dir / "FalloutCraftDX11Overlay.log").string(), true);
        auto log = std::make_shared<spdlog::logger>("FalloutCraftDX11Overlay", std::move(sink));
        spdlog::set_default_logger(std::move(log));
        spdlog::set_level(spdlog::level::info);
        spdlog::flush_on(spdlog::level::info);
    }

    bool EnsureMapping()
    {
        if (g_shared) {
            return true;
        }
        if (!g_mapping) {
            g_mapping = ::OpenFileMappingW(FILE_MAP_READ, FALSE, kMappingName);
            if (!g_mapping) {
                return false;
            }
        }
        g_shared = static_cast<const std::uint8_t*>(
            ::MapViewOfFile(g_mapping, FILE_MAP_READ, 0, 0, 0));
        if (!g_shared) {
            ::CloseHandle(g_mapping);
            g_mapping = nullptr;
            return false;
        }
        logger::info("attached to Local\\\\FalloutCraft_v1");
        return true;
    }

    bool ReadStableSlot(int index, Slot& out)
    {
        const auto* h = g_shared + kHeaderBase + static_cast<std::size_t>(index) * kHeaderStride;
        const auto id1 = *reinterpret_cast<const volatile std::uint64_t*>(h + 0x10);
        MemoryBarrier();
        const auto w = *reinterpret_cast<const volatile std::uint32_t*>(h + 0x00);
        const auto ht = *reinterpret_cast<const volatile std::uint32_t*>(h + 0x04);
        const auto flags = *reinterpret_cast<const volatile std::uint32_t*>(h + 0x08);
        MemoryBarrier();
        const auto id2 = *reinterpret_cast<const volatile std::uint64_t*>(h + 0x10);
        if (id1 == 0 || id1 != id2 || w == 0 || ht == 0 || w > kMaxW || ht > kMaxH) {
            return false;
        }
        out = { w, ht, flags, id1, index };
        return true;
    }

    bool NewestSlot(Slot& out)
    {
        Slot best{};
        bool found = false;
        for (int i = 0; i < 3; ++i) {
            Slot s{};
            if (ReadStableSlot(i, s) && (!found || s.frameId > best.frameId)) {
                best = s;
                found = true;
            }
        }
        if (!found) {
            return false;
        }
        out = best;
        return true;
    }

    constexpr const char* kShader = R"(
cbuffer Params : register(b0) { float flipY; float3 pad; };
Texture2D overlayTex : register(t0);
SamplerState overlaySamp : register(s0);

struct VSOut {
    float4 pos : SV_Position;
    float2 uv : TEXCOORD0;
};

VSOut VSMain(uint id : SV_VertexID) {
    VSOut o;
    float2 uv = float2((id << 1) & 2, id & 2);
    o.pos = float4(uv * float2(2, -2) + float2(-1, 1), 0, 1);
    o.uv = uv;
    return o;
}

float4 PSMain(VSOut i) : SV_Target {
    float2 uv = i.uv;
    if (flipY > 0.5) uv.y = 1.0 - uv.y;
    return overlayTex.Sample(overlaySamp, uv);
}
)";

    bool Compile(const char* entry, const char* target, ID3DBlob** out)
    {
        ID3DBlob* errors = nullptr;
        const auto hr = D3DCompile(
            kShader, std::strlen(kShader), "falloutcraft_dx11_overlay",
            nullptr, nullptr, entry, target, D3DCOMPILE_OPTIMIZATION_LEVEL3, 0,
            out, &errors);
        if (FAILED(hr)) {
            logger::error("shader {} failed: {}", entry,
                errors ? static_cast<const char*>(errors->GetBufferPointer()) : "unknown");
            Release(errors);
            return false;
        }
        Release(errors);
        return true;
    }

    bool InitRenderer(IDXGISwapChain* swap)
    {
        if (g_rendererReady) return true;
        if (g_rendererFailed) return false;

        if (!g_device) {
            if (FAILED(swap->GetDevice(__uuidof(ID3D11Device), reinterpret_cast<void**>(&g_device))) || !g_device) {
                g_rendererFailed = true;
                return false;
            }
        }
        if (!g_context) g_device->GetImmediateContext(&g_context);

        ID3DBlob* vsb = nullptr;
        ID3DBlob* psb = nullptr;
        if (!Compile("VSMain", "vs_5_0", &vsb) || !Compile("PSMain", "ps_5_0", &psb)) {
            Release(vsb);
            Release(psb);
            g_rendererFailed = true;
            return false;
        }
        g_device->CreateVertexShader(vsb->GetBufferPointer(), vsb->GetBufferSize(), nullptr, &g_vs);
        g_device->CreatePixelShader(psb->GetBufferPointer(), psb->GetBufferSize(), nullptr, &g_ps);
        Release(vsb);
        Release(psb);

        D3D11_SAMPLER_DESC sd{};
        sd.Filter = D3D11_FILTER_MIN_MAG_MIP_POINT;
        sd.AddressU = sd.AddressV = sd.AddressW = D3D11_TEXTURE_ADDRESS_CLAMP;
        sd.MaxLOD = D3D11_FLOAT32_MAX;
        g_device->CreateSamplerState(&sd, &g_sampler);

        D3D11_BLEND_DESC blend{};
        blend.RenderTarget[0].BlendEnable = TRUE;
        blend.RenderTarget[0].SrcBlend = D3D11_BLEND_ONE;
        blend.RenderTarget[0].DestBlend = D3D11_BLEND_INV_SRC_ALPHA;
        blend.RenderTarget[0].BlendOp = D3D11_BLEND_OP_ADD;
        blend.RenderTarget[0].SrcBlendAlpha = D3D11_BLEND_ONE;
        blend.RenderTarget[0].DestBlendAlpha = D3D11_BLEND_INV_SRC_ALPHA;
        blend.RenderTarget[0].BlendOpAlpha = D3D11_BLEND_OP_ADD;
        blend.RenderTarget[0].RenderTargetWriteMask = D3D11_COLOR_WRITE_ENABLE_ALL;
        g_device->CreateBlendState(&blend, &g_blend);

        D3D11_DEPTH_STENCIL_DESC dd{};
        dd.DepthEnable = FALSE;
        dd.StencilEnable = FALSE;
        g_device->CreateDepthStencilState(&dd, &g_depth);

        D3D11_RASTERIZER_DESC rd{};
        rd.FillMode = D3D11_FILL_SOLID;
        rd.CullMode = D3D11_CULL_NONE;
        rd.DepthClipEnable = TRUE;
        g_device->CreateRasterizerState(&rd, &g_raster);

        D3D11_BUFFER_DESC cbd{};
        cbd.ByteWidth = sizeof(Params);
        cbd.Usage = D3D11_USAGE_DYNAMIC;
        cbd.BindFlags = D3D11_BIND_CONSTANT_BUFFER;
        cbd.CPUAccessFlags = D3D11_CPU_ACCESS_WRITE;
        g_device->CreateBuffer(&cbd, nullptr, &g_params);

        g_rendererReady = g_vs && g_ps && g_sampler && g_blend && g_depth && g_raster && g_params;
        g_rendererFailed = !g_rendererReady;
        logger::info("DX11 overlay renderer {}", g_rendererReady ? "ready" : "failed");
        return g_rendererReady;
    }

    bool EnsureTexture(std::uint32_t w, std::uint32_t h)
    {
        if (g_texture && w == g_texW && h == g_texH) return true;
        Release(g_srv);
        Release(g_texture);

        D3D11_TEXTURE2D_DESC td{};
        td.Width = w;
        td.Height = h;
        td.MipLevels = 1;
        td.ArraySize = 1;
        td.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
        td.SampleDesc.Count = 1;
        td.Usage = D3D11_USAGE_DYNAMIC;
        td.BindFlags = D3D11_BIND_SHADER_RESOURCE;
        td.CPUAccessFlags = D3D11_CPU_ACCESS_WRITE;
        if (FAILED(g_device->CreateTexture2D(&td, nullptr, &g_texture)) ||
            FAILED(g_device->CreateShaderResourceView(g_texture, nullptr, &g_srv))) {
            Release(g_srv);
            Release(g_texture);
            return false;
        }
        g_texW = w;
        g_texH = h;
        logger::info("overlay texture {}x{}", w, h);
        return true;
    }

    bool UploadNewest()
    {
        if (!EnsureMapping()) return false;

        Slot slot{};
        if (!NewestSlot(slot) || slot.frameId == g_lastFrame) return g_srv != nullptr;

        const std::size_t rowBytes = static_cast<std::size_t>(slot.width) * 4;
        const std::size_t bytes = rowBytes * slot.height;
        const auto* src = g_shared + kPixelsBase + static_cast<std::size_t>(slot.index) * kPixelStride;

        std::vector<std::uint8_t> copy(bytes);
        std::memcpy(copy.data(), src, bytes);
        MemoryBarrier();

        Slot verify{};
        if (!ReadStableSlot(slot.index, verify) || verify.frameId != slot.frameId) {
            return g_srv != nullptr;
        }
        if (!EnsureTexture(slot.width, slot.height)) return g_srv != nullptr;

        D3D11_MAPPED_SUBRESOURCE mapped{};
        if (FAILED(g_context->Map(g_texture, 0, D3D11_MAP_WRITE_DISCARD, 0, &mapped))) {
            return g_srv != nullptr;
        }
        auto* dst = static_cast<std::uint8_t*>(mapped.pData);
        if (mapped.RowPitch == rowBytes) {
            std::memcpy(dst, copy.data(), bytes);
        } else {
            for (std::uint32_t y = 0; y < slot.height; ++y) {
                std::memcpy(dst + static_cast<std::size_t>(y) * mapped.RowPitch,
                    copy.data() + static_cast<std::size_t>(y) * rowBytes, rowBytes);
            }
        }
        g_context->Unmap(g_texture, 0);
        g_flipY = (slot.flags & 1u) != 0;
        g_lastFrame = slot.frameId;

        static bool once = false;
        if (!once) {
            once = true;
            logger::info("first Minecraft HUD/hand frame uploaded from shared memory");
        }
        return true;
    }

    void DrawOverlay(IDXGISwapChain* swap)
    {
        if (!InitRenderer(swap) || !UploadNewest() || !g_srv) return;

        ID3D11Texture2D* back = nullptr;
        if (FAILED(swap->GetBuffer(0, __uuidof(ID3D11Texture2D), reinterpret_cast<void**>(&back))) || !back) return;
        D3D11_TEXTURE2D_DESC bb{};
        back->GetDesc(&bb);

        ID3D11RenderTargetView* rtv = nullptr;
        const auto hr = g_device->CreateRenderTargetView(back, nullptr, &rtv);
        Release(back);
        if (FAILED(hr) || !rtv) return;

        ID3D11RenderTargetView* oldRtv[D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT]{};
        ID3D11DepthStencilView* oldDsv = nullptr;
        ID3D11BlendState* oldBlend = nullptr;
        FLOAT oldFactor[4]{};
        UINT oldMask = 0;
        ID3D11DepthStencilState* oldDepth = nullptr;
        UINT oldStencil = 0;
        ID3D11RasterizerState* oldRaster = nullptr;
        D3D11_VIEWPORT oldVp[D3D11_VIEWPORT_AND_SCISSORRECT_OBJECT_COUNT_PER_PIPELINE]{};
        UINT oldVpCount = D3D11_VIEWPORT_AND_SCISSORRECT_OBJECT_COUNT_PER_PIPELINE;
        D3D11_PRIMITIVE_TOPOLOGY oldTopo{};
        ID3D11InputLayout* oldLayout = nullptr;
        ID3D11VertexShader* oldVs = nullptr;
        ID3D11PixelShader* oldPs = nullptr;
        ID3D11ShaderResourceView* oldSrv = nullptr;
        ID3D11SamplerState* oldSampler = nullptr;
        ID3D11Buffer* oldCb = nullptr;

        g_context->OMGetRenderTargets(D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT, oldRtv, &oldDsv);
        g_context->OMGetBlendState(&oldBlend, oldFactor, &oldMask);
        g_context->OMGetDepthStencilState(&oldDepth, &oldStencil);
        g_context->RSGetState(&oldRaster);
        g_context->RSGetViewports(&oldVpCount, oldVp);
        g_context->IAGetPrimitiveTopology(&oldTopo);
        g_context->IAGetInputLayout(&oldLayout);
        g_context->VSGetShader(&oldVs, nullptr, nullptr);
        g_context->PSGetShader(&oldPs, nullptr, nullptr);
        g_context->PSGetShaderResources(0, 1, &oldSrv);
        g_context->PSGetSamplers(0, 1, &oldSampler);
        g_context->PSGetConstantBuffers(0, 1, &oldCb);

        D3D11_MAPPED_SUBRESOURCE cb{};
        if (SUCCEEDED(g_context->Map(g_params, 0, D3D11_MAP_WRITE_DISCARD, 0, &cb))) {
            *static_cast<Params*>(cb.pData) = Params{ g_flipY ? 1.0f : 0.0f, {} };
            g_context->Unmap(g_params, 0);
        }

        D3D11_VIEWPORT vp{ 0.0f, 0.0f, static_cast<float>(bb.Width), static_cast<float>(bb.Height), 0.0f, 1.0f };
        FLOAT factor[4]{};
        g_context->OMSetRenderTargets(1, &rtv, nullptr);
        g_context->OMSetBlendState(g_blend, factor, 0xFFFFFFFF);
        g_context->OMSetDepthStencilState(g_depth, 0);
        g_context->RSSetState(g_raster);
        g_context->RSSetViewports(1, &vp);
        g_context->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
        g_context->IASetInputLayout(nullptr);
        g_context->VSSetShader(g_vs, nullptr, 0);
        g_context->PSSetShader(g_ps, nullptr, 0);
        g_context->PSSetShaderResources(0, 1, &g_srv);
        g_context->PSSetSamplers(0, 1, &g_sampler);
        g_context->PSSetConstantBuffers(0, 1, &g_params);
        g_context->Draw(3, 0);

        g_context->OMSetRenderTargets(D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT, oldRtv, oldDsv);
        g_context->OMSetBlendState(oldBlend, oldFactor, oldMask);
        g_context->OMSetDepthStencilState(oldDepth, oldStencil);
        g_context->RSSetState(oldRaster);
        g_context->RSSetViewports(oldVpCount, oldVp);
        g_context->IASetPrimitiveTopology(oldTopo);
        g_context->IASetInputLayout(oldLayout);
        g_context->VSSetShader(oldVs, nullptr, 0);
        g_context->PSSetShader(oldPs, nullptr, 0);
        g_context->PSSetShaderResources(0, 1, &oldSrv);
        g_context->PSSetSamplers(0, 1, &oldSampler);
        g_context->PSSetConstantBuffers(0, 1, &oldCb);

        for (auto*& p : oldRtv) Release(p);
        Release(oldDsv);
        Release(oldBlend);
        Release(oldDepth);
        Release(oldRaster);
        Release(oldLayout);
        Release(oldVs);
        Release(oldPs);
        Release(oldSrv);
        Release(oldSampler);
        Release(oldCb);
        Release(rtv);
    }

    HRESULT __stdcall PresentHook(IDXGISwapChain* swap, UINT sync, UINT flags)
    {
        try {
            DrawOverlay(swap);
        } catch (...) {
        }
        return g_originalPresent ? g_originalPresent(swap, sync, flags) : S_OK;
    }

    HRESULT WINAPI CreateDeviceHook(
        IDXGIAdapter* adapter, D3D_DRIVER_TYPE driverType, HMODULE software, UINT flags,
        const D3D_FEATURE_LEVEL* levels, UINT levelCount, UINT sdk,
        const DXGI_SWAP_CHAIN_DESC* desc, IDXGISwapChain** swap,
        ID3D11Device** device, D3D_FEATURE_LEVEL* outLevel, ID3D11DeviceContext** context)
    {
        const auto hr = g_originalCreate(
            adapter, driverType, software, flags, levels, levelCount, sdk,
            desc, swap, device, outLevel, context);
        if (FAILED(hr) || !swap || !*swap) return hr;

        if (device && *device && !g_device) {
            g_device = *device;
            g_device->AddRef();
        }
        if (context && *context && !g_context) {
            g_context = *context;
            g_context->AddRef();
        }

        auto** vtbl = *reinterpret_cast<void***>(*swap);
        DWORD oldProtect = 0;
        if (::VirtualProtect(&vtbl[8], sizeof(void*), PAGE_EXECUTE_READWRITE, &oldProtect)) {
            g_originalPresent = reinterpret_cast<PresentFn>(vtbl[8]);
            vtbl[8] = reinterpret_cast<void*>(&PresentHook);
            ::VirtualProtect(&vtbl[8], sizeof(void*), oldProtect, &oldProtect);
            logger::info("hooked Fallout 4 real IDXGISwapChain::Present");
        } else {
            logger::error("failed to patch swap-chain Present");
        }
        return hr;
    }

    void InstallHooks()
    {
        REL::Relocation<std::uintptr_t> callSite{ REL::ID(224250), 0x419 };
        auto& trampoline = F4SE::GetTrampoline();
        g_originalCreate = reinterpret_cast<CreateFn>(
            trampoline.write_call<5>(callSite.address(), &CreateDeviceHook));
        logger::info("hooked Fallout 4 D3D11CreateDeviceAndSwapChain call site");
    }
}

extern "C" __declspec(dllexport) bool F4SEAPI F4SEPlugin_Query(
    const F4SE::QueryInterface* f4se, F4SE::PluginInfo* info)
{
    info->infoVersion = F4SE::PluginInfo::kVersion;
    info->name = "FalloutCraftDX11Overlay";
    info->version = 1;
    return !f4se->IsEditor();
}

extern "C" __declspec(dllexport) bool F4SEAPI F4SEPlugin_Load(
    const F4SE::LoadInterface* f4se)
{
    F4SE::Init(f4se);
    SetupLog();
    logger::info("FalloutCraft DX11 overlay loading");
    F4SE::AllocTrampoline(128);
    InstallHooks();
    logger::info("FalloutCraft DX11 overlay loaded; no GDI window will be created");
    return true;
}
