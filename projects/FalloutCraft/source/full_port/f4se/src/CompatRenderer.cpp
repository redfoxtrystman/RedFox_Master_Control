#include "Game.h"

#include <d3dcompiler.h>

namespace falloutcraft
{
    namespace
    {
        struct GpuTexture
        {
            ID3D11Texture2D* texture{ nullptr };
            ID3D11ShaderResourceView* srv{ nullptr };
            std::uint32_t width{ 0 };
            std::uint32_t height{ 0 };
        };

        struct Section
        {
            int sx{}, sy{}, sz{};
            std::vector<proto::RenVertex> vertices;
        };

        struct AvatarCache
        {
            std::vector<proto::RenBatch> batches;
            std::vector<proto::RenVertex> vertices;
        };

        struct SceneCache
        {
            double ox{}, oy{}, oz{};
            std::vector<proto::RenBatch> batches;
            std::vector<proto::RenVertex> vertices;
        };

        struct ScreenVertex
        {
            float x, y, z, w;
            float u, v;
            std::uint32_t color;
        };

        std::mutex g_renderLock;
        std::unordered_map<std::uint32_t, GpuTexture> g_textures;
        std::unordered_map<std::uint64_t, Section> g_sections;
        AvatarCache g_avatar;
        SceneCache g_scene;
        GpuTexture g_overlay;
        GpuTexture g_cursor;

        ID3D11Device* g_device = nullptr;
        ID3D11DeviceContext* g_context = nullptr;
        ID3D11VertexShader* g_vs = nullptr;
        ID3D11PixelShader* g_ps = nullptr;
        ID3D11InputLayout* g_layout = nullptr;
        ID3D11SamplerState* g_sampler = nullptr;
        ID3D11BlendState* g_worldBlend = nullptr;
        ID3D11BlendState* g_overlayBlend = nullptr;
        ID3D11DepthStencilState* g_noDepth = nullptr;
        ID3D11DepthStencilState* g_depthWrite = nullptr;
        ID3D11DepthStencilState* g_depthWriteRev = nullptr;
        ID3D11Texture2D* g_worldDepth = nullptr;
        ID3D11DepthStencilView* g_worldDsv = nullptr;
        std::uint32_t g_worldDepthW = 0;
        std::uint32_t g_worldDepthH = 0;
        UINT g_worldDepthSamples = 0;
        UINT g_worldDepthQuality = 0;
        ID3D11RasterizerState* g_raster = nullptr;
        ID3D11Buffer* g_vb = nullptr;
        std::size_t g_vbCapacity = 0;
        bool g_gpuReady = false;

        using PresentFn = HRESULT(__stdcall*)(IDXGISwapChain*, UINT, UINT);
        PresentFn g_originalPresent = nullptr;
        IDXGISwapChain* g_hookedSwap = nullptr;
        std::mutex g_hookLock;

        std::uint64_t SectionKey(int x, int y, int z)
        {
            constexpr std::uint64_t mask = (1ull << 21) - 1;
            return (std::uint64_t(std::uint32_t(x)) & mask) |
                   ((std::uint64_t(std::uint32_t(y)) & mask) << 21) |
                   ((std::uint64_t(std::uint32_t(z)) & mask) << 42);
        }

        template <class T>
        void Release(T*& p)
        {
            if (p) {
                p->Release();
                p = nullptr;
            }
        }

        void FreeTexture(GpuTexture& t)
        {
            Release(t.srv);
            Release(t.texture);
            t.width = t.height = 0;
        }

        bool CompileShader(const char* source, const char* entry, const char* profile, ID3DBlob** blob)
        {
            ID3DBlob* errors = nullptr;
            const auto hr = D3DCompile(source, std::strlen(source), "FalloutCraft", nullptr, nullptr,
                entry, profile, D3DCOMPILE_OPTIMIZATION_LEVEL3, 0, blob, &errors);
            if (FAILED(hr)) {
                logger::error("FalloutCraft shader {} failed: {}", entry,
                    errors ? static_cast<const char*>(errors->GetBufferPointer()) : "unknown");
                Release(errors);
                return false;
            }
            Release(errors);
            return true;
        }

        bool InitGpu(IDXGISwapChain* swap)
        {
            if (g_gpuReady) {
                return true;
            }
            if (!swap) {
                return false;
            }

            if (FAILED(swap->GetDevice(__uuidof(ID3D11Device), reinterpret_cast<void**>(&g_device))) || !g_device) {
                return false;
            }
            g_device->GetImmediateContext(&g_context);
            if (!g_context) {
                return false;
            }

            static constexpr char shader[] = R"(
struct VSIn {
    float4 pos : POSITION;
    float2 uv : TEXCOORD0;
    float4 color : COLOR0;
};
struct PSIn {
    float4 pos : SV_Position;
    float2 uv : TEXCOORD0;
    float4 color : COLOR0;
};
PSIn VSMain(VSIn i) {
    PSIn o;
    o.pos = i.pos;
    o.uv = i.uv;
    o.color = i.color;
    return o;
}
Texture2D tex0 : register(t0);
SamplerState samp0 : register(s0);
float4 PSMain(PSIn i) : SV_Target {
    return tex0.Sample(samp0, i.uv) * i.color;
}
)";

            ID3DBlob* vs = nullptr;
            ID3DBlob* ps = nullptr;
            if (!CompileShader(shader, "VSMain", "vs_5_0", &vs) ||
                !CompileShader(shader, "PSMain", "ps_5_0", &ps)) {
                Release(vs);
                Release(ps);
                return false;
            }

            HRESULT hr = g_device->CreateVertexShader(vs->GetBufferPointer(), vs->GetBufferSize(), nullptr, &g_vs);
            hr |= g_device->CreatePixelShader(ps->GetBufferPointer(), ps->GetBufferSize(), nullptr, &g_ps);
            D3D11_INPUT_ELEMENT_DESC elems[] = {
                { "POSITION", 0, DXGI_FORMAT_R32G32B32A32_FLOAT, 0, 0, D3D11_INPUT_PER_VERTEX_DATA, 0 },
                { "TEXCOORD", 0, DXGI_FORMAT_R32G32_FLOAT, 0, 16, D3D11_INPUT_PER_VERTEX_DATA, 0 },
                { "COLOR", 0, DXGI_FORMAT_R8G8B8A8_UNORM, 0, 24, D3D11_INPUT_PER_VERTEX_DATA, 0 },
            };
            hr |= g_device->CreateInputLayout(elems, static_cast<UINT>(std::size(elems)),
                vs->GetBufferPointer(), vs->GetBufferSize(), &g_layout);
            Release(vs);
            Release(ps);

            D3D11_SAMPLER_DESC sd{};
            sd.Filter = D3D11_FILTER_MIN_MAG_MIP_POINT;
            sd.AddressU = sd.AddressV = sd.AddressW = D3D11_TEXTURE_ADDRESS_CLAMP;
            sd.MaxLOD = D3D11_FLOAT32_MAX;
            hr |= g_device->CreateSamplerState(&sd, &g_sampler);

            D3D11_BLEND_DESC wb{};
            wb.RenderTarget[0].BlendEnable = TRUE;
            wb.RenderTarget[0].SrcBlend = D3D11_BLEND_SRC_ALPHA;
            wb.RenderTarget[0].DestBlend = D3D11_BLEND_INV_SRC_ALPHA;
            wb.RenderTarget[0].BlendOp = D3D11_BLEND_OP_ADD;
            wb.RenderTarget[0].SrcBlendAlpha = D3D11_BLEND_ONE;
            wb.RenderTarget[0].DestBlendAlpha = D3D11_BLEND_INV_SRC_ALPHA;
            wb.RenderTarget[0].BlendOpAlpha = D3D11_BLEND_OP_ADD;
            wb.RenderTarget[0].RenderTargetWriteMask = D3D11_COLOR_WRITE_ENABLE_ALL;
            hr |= g_device->CreateBlendState(&wb, &g_worldBlend);

            D3D11_BLEND_DESC ob = wb;
            ob.RenderTarget[0].SrcBlend = D3D11_BLEND_ONE;
            hr |= g_device->CreateBlendState(&ob, &g_overlayBlend);

            D3D11_DEPTH_STENCIL_DESC dd{};
            dd.DepthEnable = FALSE;
            dd.StencilEnable = FALSE;
            hr |= g_device->CreateDepthStencilState(&dd, &g_noDepth);

            dd.DepthEnable = TRUE;
            dd.DepthWriteMask = D3D11_DEPTH_WRITE_MASK_ALL;
            dd.DepthFunc = D3D11_COMPARISON_LESS_EQUAL;
            hr |= g_device->CreateDepthStencilState(&dd, &g_depthWrite);
            dd.DepthFunc = D3D11_COMPARISON_GREATER_EQUAL;
            hr |= g_device->CreateDepthStencilState(&dd, &g_depthWriteRev);

            D3D11_RASTERIZER_DESC rd{};
            rd.FillMode = D3D11_FILL_SOLID;
            rd.CullMode = D3D11_CULL_NONE;
            rd.DepthClipEnable = TRUE;
            hr |= g_device->CreateRasterizerState(&rd, &g_raster);

            g_gpuReady = SUCCEEDED(hr) && g_vs && g_ps && g_layout && g_sampler &&
                         g_worldBlend && g_overlayBlend && g_noDepth && g_depthWrite &&
                         g_depthWriteRev && g_raster;
            logger::info("FalloutCraft: D3D11 full-port renderer {}", g_gpuReady ? "ready" : "failed");
            return g_gpuReady;
        }

        bool SetTexture(std::uint32_t id, std::uint32_t w, std::uint32_t h, const std::uint8_t* rgba)
        {
            if (!g_device || !rgba || w == 0 || h == 0 || w > 8192 || h > 8192) {
                return false;
            }
            auto& t = g_textures[id];
            FreeTexture(t);

            D3D11_TEXTURE2D_DESC td{};
            td.Width = w;
            td.Height = h;
            td.MipLevels = 1;
            td.ArraySize = 1;
            td.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
            td.SampleDesc.Count = 1;
            td.Usage = D3D11_USAGE_DEFAULT;
            td.BindFlags = D3D11_BIND_SHADER_RESOURCE;

            D3D11_SUBRESOURCE_DATA init{};
            init.pSysMem = rgba;
            init.SysMemPitch = w * 4;
            if (FAILED(g_device->CreateTexture2D(&td, &init, &t.texture)) ||
                FAILED(g_device->CreateShaderResourceView(t.texture, nullptr, &t.srv))) {
                FreeTexture(t);
                return false;
            }
            t.width = w;
            t.height = h;
            return true;
        }

        bool EnsureOverlayTexture(std::uint32_t w, std::uint32_t h)
        {
            if (g_overlay.texture && g_overlay.width == w && g_overlay.height == h) {
                return true;
            }
            FreeTexture(g_overlay);

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
            if (FAILED(g_device->CreateTexture2D(&td, nullptr, &g_overlay.texture)) ||
                FAILED(g_device->CreateShaderResourceView(g_overlay.texture, nullptr, &g_overlay.srv))) {
                FreeTexture(g_overlay);
                return false;
            }
            g_overlay.width = w;
            g_overlay.height = h;
            return true;
        }

        bool EnsureCursorTexture()
        {
            if (g_cursor.srv) {
                return true;
            }
            if (!g_device) {
                return false;
            }

            const std::uint32_t pixel = 0xFFFFFFFFu;
            D3D11_TEXTURE2D_DESC td{};
            td.Width = 1;
            td.Height = 1;
            td.MipLevels = 1;
            td.ArraySize = 1;
            td.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
            td.SampleDesc.Count = 1;
            td.Usage = D3D11_USAGE_DEFAULT;
            td.BindFlags = D3D11_BIND_SHADER_RESOURCE;

            D3D11_SUBRESOURCE_DATA init{};
            init.pSysMem = &pixel;
            init.SysMemPitch = sizeof(pixel);
            if (FAILED(g_device->CreateTexture2D(&td, &init, &g_cursor.texture)) ||
                FAILED(g_device->CreateShaderResourceView(g_cursor.texture, nullptr, &g_cursor.srv))) {
                FreeTexture(g_cursor);
                return false;
            }
            g_cursor.width = g_cursor.height = 1;
            return true;
        }

        void HandleRenderMessage(std::uint32_t type, const std::uint8_t* data, std::uint32_t bytes)
        {
            switch (type) {
            case proto::kRenAtlas:
                if (bytes >= sizeof(proto::RenAtlas)) {
                    const auto* h = reinterpret_cast<const proto::RenAtlas*>(data);
                    const auto need = sizeof(*h) + std::uint64_t(h->width) * h->height * 4;
                    if (need <= bytes) {
                        SetTexture(0, h->width, h->height, data + sizeof(*h));
                        logger::info("FalloutCraft: Minecraft atlas {}x{} received", h->width, h->height);
                    }
                }
                break;
            case proto::kRenTexture:
                if (bytes >= sizeof(proto::RenTexture)) {
                    const auto* h = reinterpret_cast<const proto::RenTexture*>(data);
                    const auto need = sizeof(*h) + std::uint64_t(h->width) * h->height * 4;
                    if (need <= bytes) {
                        SetTexture(h->id, h->width, h->height, data + sizeof(*h));
                    }
                }
                break;
            case proto::kRenAtlasRegion:
                if (bytes >= sizeof(proto::RenAtlasRegion)) {
                    const auto* h = reinterpret_cast<const proto::RenAtlasRegion*>(data);
                    auto it = g_textures.find(0);
                    const auto need = sizeof(*h) + std::uint64_t(h->width) * h->height * 4;
                    if (it != g_textures.end() && it->second.texture && need <= bytes) {
                        D3D11_BOX box{ h->x, h->y, 0, h->x + h->width, h->y + h->height, 1 };
                        g_context->UpdateSubresource(it->second.texture, 0, &box,
                            data + sizeof(*h), h->width * 4, 0);
                    }
                }
                break;
            case proto::kRenSection:
                if (bytes >= sizeof(proto::RenSection)) {
                    const auto* h = reinterpret_cast<const proto::RenSection*>(data);
                    const auto need = sizeof(*h) + std::uint64_t(h->vertexCount) * sizeof(proto::RenVertex);
                    const auto key = SectionKey(h->sx, h->sy, h->sz);
                    if (h->vertexCount == 0) {
                        g_sections.erase(key);
                    } else if (need <= bytes) {
                        Section s;
                        s.sx = h->sx; s.sy = h->sy; s.sz = h->sz;
                        const auto* v = reinterpret_cast<const proto::RenVertex*>(data + sizeof(*h));
                        s.vertices.assign(v, v + h->vertexCount);
                        g_sections[key] = std::move(s);
                    }
                }
                break;
            case proto::kRenClearAll:
                g_sections.clear();
                g_avatar = {};
                g_scene = {};
                NpcBlocks::Clear();
                BlockLights::Clear();
                break;
            case proto::kRenAvatar:
            case proto::kRenRagdoll:
                if (bytes >= sizeof(proto::RenAvatar)) {
                    const auto* h = reinterpret_cast<const proto::RenAvatar*>(data);
                    const auto batchBytes = std::uint64_t(h->batchCount) * sizeof(proto::RenBatch);
                    const auto vertBytes = std::uint64_t(h->vertexCount) * sizeof(proto::RenVertex);
                    if (sizeof(*h) + batchBytes + vertBytes <= bytes && type == proto::kRenAvatar) {
                        const auto* b = reinterpret_cast<const proto::RenBatch*>(data + sizeof(*h));
                        const auto* v = reinterpret_cast<const proto::RenVertex*>(data + sizeof(*h) + batchBytes);
                        g_avatar.batches.assign(b, b + h->batchCount);
                        g_avatar.vertices.assign(v, v + h->vertexCount);
                    }
                }
                break;
            case proto::kRenScene:
                if (bytes >= sizeof(proto::RenScene)) {
                    const auto* h = reinterpret_cast<const proto::RenScene*>(data);
                    const auto batchBytes = std::uint64_t(h->batchCount) * sizeof(proto::RenBatch);
                    const auto vertBytes = std::uint64_t(h->vertexCount) * sizeof(proto::RenVertex);
                    if (sizeof(*h) + batchBytes + vertBytes <= bytes) {
                        const auto* b = reinterpret_cast<const proto::RenBatch*>(data + sizeof(*h));
                        const auto* v = reinterpret_cast<const proto::RenVertex*>(data + sizeof(*h) + batchBytes);
                        g_scene.ox = h->originX; g_scene.oy = h->originY; g_scene.oz = h->originZ;
                        g_scene.batches.assign(b, b + h->batchCount);
                        g_scene.vertices.assign(v, v + h->vertexCount);
                    }
                }
                break;
            case proto::kRenLights:
                BlockLights::OnLights(data, bytes);
                break;
            case proto::kRenSolids:
                NpcBlocks::OnSolids(data, bytes);
                break;
            case proto::kRenDug:
                // Digging protocol is retained. Fallout-side mesh surgery is brought online after
                // the first full-system runtime pass.
                break;
            default:
                break;
            }
        }

        bool EnsureVertexBuffer(std::size_t count)
        {
            if (count == 0) {
                return false;
            }
            if (g_vb && g_vbCapacity >= count) {
                return true;
            }
            Release(g_vb);
            g_vbCapacity = std::max<std::size_t>(count, g_vbCapacity ? g_vbCapacity * 2 : 8192);

            D3D11_BUFFER_DESC bd{};
            bd.ByteWidth = static_cast<UINT>(std::min<std::size_t>(
                g_vbCapacity * sizeof(ScreenVertex), std::numeric_limits<UINT>::max()));
            bd.Usage = D3D11_USAGE_DYNAMIC;
            bd.BindFlags = D3D11_BIND_VERTEX_BUFFER;
            bd.CPUAccessFlags = D3D11_CPU_ACCESS_WRITE;
            return SUCCEEDED(g_device->CreateBuffer(&bd, nullptr, &g_vb));
        }

        std::uint32_t EnvironmentLitColor(const proto::RenVertex& v)
        {
            const std::uint32_t rgba = v.color ? v.color : 0xFFFFFFFFu;
            auto* sky = RE::Sky::GetSingleton();
            if (!sky) {
                return rgba;
            }

            // WorldExporter intentionally removes Minecraft's hard-coded face brightness. Like
            // SkyCraft, the host now supplies directional environment lighting instead. Fallout's
            // live Sky singleton already contains the blended six-direction ambient cube for the
            // current interior/weather/time of day.
            RE::NiColor ambient{};
            const int face = static_cast<int>((v.flags >> 4) & 7u);
            auto pick = [&](int axis, int sign) {
                return sky->directionalAmbientColorsA[axis][sign];
            };
            switch (face) {
            case 1: ambient = pick(2, 1); break;  // MC down  -> Fallout -Z
            case 2: ambient = pick(2, 0); break;  // MC up    -> Fallout +Z
            case 3: ambient = pick(1, 0); break;  // MC north -> Fallout +Y
            case 4: ambient = pick(1, 1); break;  // MC south -> Fallout -Y
            case 5: ambient = pick(0, 1); break;  // MC west  -> Fallout -X
            case 6: ambient = pick(0, 0); break;  // MC east  -> Fallout +X
            default:
                for (int axis = 0; axis < 3; ++axis) {
                    for (int sign = 0; sign < 2; ++sign) {
                        const auto a = pick(axis, sign);
                        ambient.r += a.r / 6.0f;
                        ambient.g += a.g / 6.0f;
                        ambient.b += a.b / 6.0f;
                    }
                }
                break;
            }

            // A not-yet-initialized ambient cube is safer as neutral light than black. Minecraft
            // block light remains authoritative for torches/glowstone while Fallout supplies the
            // environmental component.
            const float energy = ambient.r + ambient.g + ambient.b;
            float lr = 1.0f, lg = 1.0f, lb = 1.0f;
            if (std::isfinite(energy) && energy > 0.015f) {
                lr = std::clamp(0.12f + ambient.r * 1.45f, 0.12f, 1.20f);
                lg = std::clamp(0.12f + ambient.g * 1.45f, 0.12f, 1.20f);
                lb = std::clamp(0.12f + ambient.b * 1.45f, 0.12f, 1.20f);
            }
            const float block = std::clamp(float(v.light & 0xFFu) / 15.0f, 0.0f, 1.0f);
            const float emitted = 0.28f + 0.72f * block;
            lr = std::max(lr, emitted * block);
            lg = std::max(lg, emitted * block);
            lb = std::max(lb, emitted * block);

            const auto mul = [](std::uint32_t channel, float light) {
                return static_cast<std::uint32_t>(std::clamp(
                    std::lround(float(channel) * light), 0l, 255l));
            };
            const std::uint32_t r = mul(rgba & 0xFFu, lr);
            const std::uint32_t g = mul((rgba >> 8) & 0xFFu, lg);
            const std::uint32_t b = mul((rgba >> 16) & 0xFFu, lb);
            return (rgba & 0xFF000000u) | (b << 16) | (g << 8) | r;
        }

        bool ProjectVertex(RE::NiCamera* camera, const proto::RenVertex& v,
            double ox, double oy, double oz, ScreenVertex& out)
        {
            if (!camera) {
                return false;
            }

            // Preserve Fallout's real homogeneous clip coordinates, but do the multiply in
            // camera-relative space. Fallout world coordinates are large enough that multiplying
            // absolute positions here loses the low bits that distinguish nearby Minecraft
            // vertices. The result is the giant/flattened/warped block faces seen in v0.5.5.
            //
            // This is the same re-basing used by SkyCraft's mature renderer: fold the camera
            // position into the matrix translation once, then multiply a small relative vector.
            // It is algebraically identical to M * world, but dramatically more stable in float.
            const auto world = McToSky(ox + v.x, oy + v.y, oz + v.z);
            const auto cam = camera->world.translate;
            const RE::NiPoint3 rel{ world.x - cam.x, world.y - cam.y, world.z - cam.z };
            const auto& m = camera->worldToCam;
            float clip[4]{};
            for (int r = 0; r < 4; ++r) {
                const double rebasedT = double(m[r][3]) +
                    double(m[r][0]) * cam.x +
                    double(m[r][1]) * cam.y +
                    double(m[r][2]) * cam.z;
                clip[r] = static_cast<float>(
                    double(m[r][0]) * rel.x +
                    double(m[r][1]) * rel.y +
                    double(m[r][2]) * rel.z +
                    rebasedT);
            }
            if (!std::isfinite(clip[0]) || !std::isfinite(clip[1]) ||
                !std::isfinite(clip[2]) || !std::isfinite(clip[3]) ||
                std::abs(clip[3]) < 1e-5f) {
                return false;
            }

            out.x = clip[0];
            out.y = clip[1];
            out.z = clip[2];
            out.w = clip[3];
            out.u = v.u;
            out.v = v.v;
            out.color = EnvironmentLitColor(v);
            return true;
        }

        bool EnsureWorldDepth(std::uint32_t w, std::uint32_t h, UINT samples, UINT quality)
        {
            samples = std::max<UINT>(1, samples);
            if (g_worldDepth && g_worldDepthW == w && g_worldDepthH == h &&
                g_worldDepthSamples == samples && g_worldDepthQuality == quality) {
                return true;
            }
            Release(g_worldDsv);
            Release(g_worldDepth);
            g_worldDepthW = g_worldDepthH = 0;

            D3D11_TEXTURE2D_DESC td{};
            td.Width = w;
            td.Height = h;
            td.MipLevels = 1;
            td.ArraySize = 1;
            td.Format = DXGI_FORMAT_D32_FLOAT;
            td.SampleDesc.Count = samples;
            td.SampleDesc.Quality = quality;
            td.Usage = D3D11_USAGE_DEFAULT;
            td.BindFlags = D3D11_BIND_DEPTH_STENCIL;
            if (FAILED(g_device->CreateTexture2D(&td, nullptr, &g_worldDepth)) ||
                FAILED(g_device->CreateDepthStencilView(g_worldDepth, nullptr, &g_worldDsv))) {
                Release(g_worldDsv);
                Release(g_worldDepth);
                return false;
            }
            g_worldDepthW = w;
            g_worldDepthH = h;
            g_worldDepthSamples = samples;
            g_worldDepthQuality = quality;
            return true;
        }

        bool CameraUsesReversedDepth(RE::NiCamera* camera)
        {
            // Fallout's depth convention does not change when the player turns or changes FOV.
            // Cache the first valid comparison instead of re-deciding every frame from floats;
            // the old per-frame test could flip on borderline matrices and make overlapping block
            // faces alternate between two visibly different depth orders.
            static int cached = -1;
            if (cached >= 0) {
                return cached != 0;
            }
            if (!camera) {
                return false;
            }

            const auto& m = camera->worldToCam;
            const auto& R = camera->world.rotate;
            const RE::NiPoint3 fwd{ R.entry[1][0], R.entry[1][1], R.entry[1][2] };
            const auto cam = camera->world.translate;
            auto depthAt = [&](float d) {
                const auto p = cam + fwd * d;
                const double z = double(m[2][0]) * p.x + double(m[2][1]) * p.y +
                                 double(m[2][2]) * p.z + double(m[2][3]);
                const double wv = double(m[3][0]) * p.x + double(m[3][1]) * p.y +
                                  double(m[3][2]) * p.z + double(m[3][3]);
                return std::abs(wv) > 1e-7 ? z / wv : std::numeric_limits<double>::quiet_NaN();
            };
            const double nearZ = depthAt(100.0f);
            const double farZ = depthAt(10000.0f);
            if (std::isfinite(nearZ) && std::isfinite(farZ) && std::abs(nearZ - farZ) > 1e-7) {
                cached = nearZ > farZ ? 1 : 0;
                logger::info("FalloutCraft: locked Minecraft world depth convention to {}",
                    cached ? "reversed-Z" : "standard-Z");
            }
            return cached > 0;
        }

        void BindCommon(ID3D11RenderTargetView* rtv, std::uint32_t width, std::uint32_t height,
            ID3D11BlendState* blend)
        {
            D3D11_VIEWPORT vp{};
            vp.Width = static_cast<float>(width);
            vp.Height = static_cast<float>(height);
            vp.MaxDepth = 1.0f;
            FLOAT factor[4]{};
            g_context->OMSetRenderTargets(1, &rtv, nullptr);
            g_context->OMSetBlendState(blend, factor, 0xFFFFFFFF);
            g_context->OMSetDepthStencilState(g_noDepth, 0);
            g_context->RSSetState(g_raster);
            g_context->RSSetViewports(1, &vp);
            g_context->IASetInputLayout(g_layout);
            g_context->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
            g_context->VSSetShader(g_vs, nullptr, 0);
            g_context->PSSetShader(g_ps, nullptr, 0);
            g_context->PSSetSamplers(0, 1, &g_sampler);
        }

        void DrawScreenVertices(const std::vector<ScreenVertex>& verts, ID3D11ShaderResourceView* srv)
        {
            if (verts.empty() || !srv || !EnsureVertexBuffer(verts.size())) {
                return;
            }
            D3D11_MAPPED_SUBRESOURCE mapped{};
            if (FAILED(g_context->Map(g_vb, 0, D3D11_MAP_WRITE_DISCARD, 0, &mapped))) {
                return;
            }
            std::memcpy(mapped.pData, verts.data(), verts.size() * sizeof(ScreenVertex));
            g_context->Unmap(g_vb, 0);

            UINT stride = sizeof(ScreenVertex), offset = 0;
            g_context->IASetVertexBuffers(0, 1, &g_vb, &stride, &offset);
            g_context->PSSetShaderResources(0, 1, &srv);
            g_context->Draw(static_cast<UINT>(verts.size()), 0);
            ID3D11ShaderResourceView* none = nullptr;
            g_context->PSSetShaderResources(0, 1, &none);
        }

        void DrawProjected(RE::NiCamera* camera, const proto::RenVertex* vertices,
            std::size_t first, std::size_t count, double ox, double oy, double oz,
            std::uint32_t texture)
        {
            if (!camera || !vertices || count < 3) {
                return;
            }
            const auto it = g_textures.find(texture);
            if (it == g_textures.end() || !it->second.srv) {
                return;
            }

            constexpr std::size_t kMaxProjected = 600000;
            std::vector<ScreenVertex> out;
            out.reserve(std::min<std::size_t>(count, kMaxProjected));
            const std::size_t end = std::min(first + count, first + kMaxProjected);
            for (std::size_t i = first; i + 2 < end; i += 3) {
                ScreenVertex tri[3];
                if (ProjectVertex(camera, vertices[i], ox, oy, oz, tri[0]) &&
                    ProjectVertex(camera, vertices[i + 1], ox, oy, oz, tri[1]) &&
                    ProjectVertex(camera, vertices[i + 2], ox, oy, oz, tri[2])) {
                    // Let D3D clip triangles crossing the near plane, but never submit a triangle
                    // that is wholly behind the camera. Keeping those was another source of
                    // screen-filling wedges when the player turned through nearby blocks.
                    if (!(tri[0].w <= 1e-5f && tri[1].w <= 1e-5f && tri[2].w <= 1e-5f)) {
                        out.insert(out.end(), std::begin(tri), std::end(tri));
                    }
                }
            }
            DrawScreenVertices(out, it->second.srv);
        }

        void DrawWorld(ID3D11RenderTargetView* rtv, std::uint32_t w, std::uint32_t h, UINT samples, UINT quality)
        {
            if (!State().puppeting.load()) {
                return;
            }
            auto* camera = RE::Main::WorldRootCamera();
            if (!camera || g_textures.find(0) == g_textures.end()) {
                return;
            }

            BindCommon(rtv, w, h, g_worldBlend);
            if (EnsureWorldDepth(w, h, samples, quality)) {
                const bool reversed = CameraUsesReversedDepth(camera);
                g_context->OMSetRenderTargets(1, &rtv, g_worldDsv);
                g_context->OMSetDepthStencilState(reversed ? g_depthWriteRev : g_depthWrite, 0);
                g_context->ClearDepthStencilView(g_worldDsv, D3D11_CLEAR_DEPTH, reversed ? 0.0f : 1.0f, 0);
            }

            for (const auto& [key, section] : g_sections) {
                (void)key;
                DrawProjected(camera, section.vertices.data(), 0, section.vertices.size(),
                    double(section.sx) * 16.0, double(section.sy) * 16.0, double(section.sz) * 16.0, 0);
            }

            if (!g_scene.vertices.empty()) {
                for (const auto& batch : g_scene.batches) {
                    if (std::uint64_t(batch.first) + batch.count <= g_scene.vertices.size()) {
                        DrawProjected(camera, g_scene.vertices.data(), batch.first, batch.count,
                            g_scene.ox, g_scene.oy, g_scene.oz, batch.texture);
                    }
                }
            }

            if (State().feetValid && !g_avatar.vertices.empty()) {
                for (const auto& batch : g_avatar.batches) {
                    if (std::uint64_t(batch.first) + batch.count <= g_avatar.vertices.size()) {
                        DrawProjected(camera, g_avatar.vertices.data(), batch.first, batch.count,
                            State().feetX, State().feetY, State().feetZ, batch.texture);
                    }
                }
            }
        }

        void UploadOverlay()
        {
            auto& link = Link::Get();
            if (!link.AcquireOverlayFrame()) {
                return;
            }
            const auto* h = link.FrontHeader();
            const auto* pixels = link.FrontPixels();
            if (!h || !pixels || h->width == 0 || h->height == 0 ||
                h->width > proto::kMaxOverlayW || h->height > proto::kMaxOverlayH) {
                return;
            }
            if (!EnsureOverlayTexture(h->width, h->height)) {
                return;
            }

            D3D11_MAPPED_SUBRESOURCE mapped{};
            if (FAILED(g_context->Map(g_overlay.texture, 0, D3D11_MAP_WRITE_DISCARD, 0, &mapped))) {
                return;
            }
            const std::size_t row = std::size_t(h->width) * 4;
            for (std::uint32_t y = 0; y < h->height; ++y) {
                std::memcpy(static_cast<std::uint8_t*>(mapped.pData) + std::size_t(y) * mapped.RowPitch,
                    pixels + std::size_t(y) * row, row);
            }
            g_context->Unmap(g_overlay.texture, 0);

            static bool once = false;
            if (!once) {
                once = true;
                logger::info("FalloutCraft: first Minecraft HUD/hand frame uploaded through D3D11");
            }
        }

        void DrawOverlay(ID3D11RenderTargetView* rtv, std::uint32_t w, std::uint32_t h)
        {
            UploadOverlay();
            if (!g_overlay.srv || !State().mcInWorld.load()) {
                return;
            }

            BindCommon(rtv, w, h, g_overlayBlend);
            bool flip = false;
            if (const auto* hdr = Link::Get().FrontHeader()) {
                flip = (hdr->flags & 1u) != 0;
            }
            const float v0 = flip ? 1.0f : 0.0f;
            const float v1 = flip ? 0.0f : 1.0f;
            const std::uint32_t white = 0xFFFFFFFFu;
            std::vector<ScreenVertex> q{
                { -1,-1,0,1, 0,v1,white }, { -1,1,0,1, 0,v0,white }, { 1,1,0,1, 1,v0,white },
                { -1,-1,0,1, 0,v1,white }, { 1,1,0,1, 1,v0,white }, { 1,-1,0,1, 1,v1,white }
            };
            DrawScreenVertices(q, g_overlay.srv);
        }

        void DrawCursor(ID3D11RenderTargetView* rtv, std::uint32_t w, std::uint32_t h)
        {
            auto& st = State();
            if (!st.mcScreenOpen.load() || w == 0 || h == 0 || !EnsureCursorTexture()) {
                return;
            }

            BindCommon(rtv, w, h, g_overlayBlend);

            const float x = static_cast<float>(std::clamp(st.cursorX.load(), 0, static_cast<int>(w) - 1));
            const float y = static_cast<float>(std::clamp(st.cursorY.load(), 0, static_cast<int>(h) - 1));
            auto ndcX = [w](float px) { return px / static_cast<float>(w) * 2.0f - 1.0f; };
            auto ndcY = [h](float py) { return 1.0f - py / static_cast<float>(h) * 2.0f; };

            auto tri = [&](float x0, float y0, float x1, float y1, float x2, float y2, std::uint32_t color) {
                std::vector<ScreenVertex> v{
                    { ndcX(x0), ndcY(y0), 0, 1, 0, 0, color },
                    { ndcX(x1), ndcY(y1), 0, 1, 0, 0, color },
                    { ndcX(x2), ndcY(y2), 0, 1, 0, 0, color },
                };
                DrawScreenVertices(v, g_cursor.srv);
            };

            // Minecraft's hidden window has no OS cursor, so reproduce SkyCraft's virtual
            // pointer in the Fallout backbuffer. Black outline first, white inset second.
            tri(x, y, x + 13.0f, y + 20.0f, x + 5.0f, y + 16.0f, 0xFF000000u);
            tri(x + 2.0f, y + 2.0f, x + 10.0f, y + 17.0f, x + 5.0f, y + 14.0f, 0xFFFFFFFFu);
        }

        void RenderPresent(IDXGISwapChain* swap)
        {
            if (!InitGpu(swap)) {
                return;
            }

            Link::Get().Heartbeat();
            Input::Install();

            {
                std::lock_guard lock(g_renderLock);
                Link::Get().DrainRender([](std::uint32_t type, const std::uint8_t* data, std::uint32_t bytes) {
                    HandleRenderMessage(type, data, bytes);
                }, 24ull << 20);
            }

            ID3D11Texture2D* back = nullptr;
            if (FAILED(swap->GetBuffer(0, __uuidof(ID3D11Texture2D), reinterpret_cast<void**>(&back))) || !back) {
                return;
            }
            D3D11_TEXTURE2D_DESC desc{};
            back->GetDesc(&desc);
            ID3D11RenderTargetView* rtv = nullptr;
            const auto hr = g_device->CreateRenderTargetView(back, nullptr, &rtv);
            Release(back);
            if (FAILED(hr) || !rtv) {
                return;
            }

            // Draw Minecraft's world-space streams first and its normal GUI last. This alpha uses
            // Fallout's finished backbuffer; the imported in-frame/depth path remains in-tree and
            // will replace this post-scene pass as the Fallout render-target indices are validated.
            DrawWorld(rtv, desc.Width, desc.Height, desc.SampleDesc.Count, desc.SampleDesc.Quality);
            DrawOverlay(rtv, desc.Width, desc.Height);
            DrawCursor(rtv, desc.Width, desc.Height);
            Release(rtv);
        }

        HRESULT __stdcall PresentHook(IDXGISwapChain* swap, UINT sync, UINT flags)
        {
            try {
                RenderPresent(swap);
            } catch (const std::exception& e) {
                logger::error("FalloutCraft Present exception: {}", e.what());
            } catch (...) {
                logger::error("FalloutCraft Present exception: unknown");
            }
            return g_originalPresent ? g_originalPresent(swap, sync, flags) : S_OK;
        }

        bool EnsurePresentHook()
        {
            std::lock_guard lock(g_hookLock);
            auto* rw = RE::BSGraphics::GetCurrentRendererWindow();
            auto* swap = rw ? reinterpret_cast<IDXGISwapChain*>(rw->swapChain) : nullptr;
            if (!swap) {
                return false;
            }
            if (g_hookedSwap == swap && g_originalPresent) {
                return true;
            }

            auto** vtbl = *reinterpret_cast<void***>(swap);
            if (!vtbl) {
                return false;
            }
            if (vtbl[8] == reinterpret_cast<void*>(&PresentHook)) {
                g_hookedSwap = swap;
                return true;
            }

            DWORD oldProtect = 0;
            if (!VirtualProtect(&vtbl[8], sizeof(void*), PAGE_EXECUTE_READWRITE, &oldProtect)) {
                return false;
            }
            g_originalPresent = reinterpret_cast<PresentFn>(vtbl[8]);
            vtbl[8] = reinterpret_cast<void*>(&PresentHook);
            VirtualProtect(&vtbl[8], sizeof(void*), oldProtect, &oldProtect);
            FlushInstructionCache(GetCurrentProcess(), &vtbl[8], sizeof(void*));
            g_hookedSwap = swap;
            logger::info("FalloutCraft: hooked Fallout 4 IDXGISwapChain::Present (no GDI)");
            return true;
        }
    }

    namespace Overlay
    {
        void Install()
        {
            EnsurePresentHook();
        }
    }

    namespace WorldRender
    {
        void Install()
        {
            EnsurePresentHook();
        }

        void Draw(ID3D11Device*, ID3D11DeviceContext*, IDXGISwapChain* swap)
        {
            if (swap) {
                RenderPresent(swap);
            }
        }

        void CaptureIfRequested(ID3D11DeviceContext*, IDXGISwapChain*) {}

        void StickArrow(RE::FormID, float, float, float, float, float) {}

        void UpdateRagdoll(RE::PlayerCharacter*, bool) {}
    }
}
