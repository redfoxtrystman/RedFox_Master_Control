#include "Game.h"

namespace falloutcraft
{
    namespace
    {
        std::mutex g_hookLock;
        HWND g_hwnd = nullptr;
        WNDPROC g_originalWndProc = nullptr;
        std::atomic<bool> g_installed{ false };
        std::atomic<bool> g_playerControlsHooked{ false };
        long long g_virtualX = 0;
        long long g_virtualY = 0;
        bool g_lastScreenOpen = false;
        int g_fallbackX = 0;
        int g_fallbackY = 0;
        bool g_haveFallback = false;
        std::uint64_t g_lastRawMouseMs = 0;

        std::uint16_t VkToSdl(WPARAM a_vk, LPARAM a_lParam)
        {
            const auto vk = static_cast<unsigned>(a_vk);
            if (vk >= 'A' && vk <= 'Z') return static_cast<std::uint16_t>(4 + vk - 'A');
            if (vk >= '1' && vk <= '9') return static_cast<std::uint16_t>(30 + vk - '1');
            if (vk == '0') return 39;
            switch (vk) {
            case VK_RETURN: return (a_lParam & (1ll << 24)) ? 88 : 40;
            case VK_ESCAPE: return 41;
            case VK_BACK: return 42;
            case VK_TAB: return 43;
            case VK_SPACE: return 44;
            case VK_OEM_MINUS: return 45;
            case VK_OEM_PLUS: return 46;
            case VK_OEM_4: return 47;
            case VK_OEM_6: return 48;
            case VK_OEM_5: return 49;
            case VK_OEM_1: return 51;
            case VK_OEM_7: return 52;
            case VK_OEM_3: return 53;
            case VK_OEM_COMMA: return 54;
            case VK_OEM_PERIOD: return 55;
            case VK_OEM_2: return 56;
            case VK_CAPITAL: return 57;
            case VK_F1: return 58;
            case VK_F2: return 59;
            case VK_F3: return 60;
            case VK_F4: return 61;
            case VK_F5: return 62;
            case VK_F6: return 63;
            case VK_F7: return 64;
            case VK_F8: return 65;
            case VK_F9: return 66;
            case VK_F10: return 67;
            case VK_F11: return 68;
            case VK_F12: return 69;
            case VK_SNAPSHOT: return 70;
            case VK_SCROLL: return 71;
            case VK_PAUSE: return 72;
            case VK_INSERT: return 73;
            case VK_HOME: return 74;
            case VK_PRIOR: return 75;
            case VK_DELETE: return 76;
            case VK_END: return 77;
            case VK_NEXT: return 78;
            case VK_RIGHT: return 79;
            case VK_LEFT: return 80;
            case VK_DOWN: return 81;
            case VK_UP: return 82;
            case VK_NUMLOCK: return 83;
            case VK_DIVIDE: return 84;
            case VK_MULTIPLY: return 85;
            case VK_SUBTRACT: return 86;
            case VK_ADD: return 87;
            case VK_NUMPAD1: return 89;
            case VK_NUMPAD2: return 90;
            case VK_NUMPAD3: return 91;
            case VK_NUMPAD4: return 92;
            case VK_NUMPAD5: return 93;
            case VK_NUMPAD6: return 94;
            case VK_NUMPAD7: return 95;
            case VK_NUMPAD8: return 96;
            case VK_NUMPAD9: return 97;
            case VK_NUMPAD0: return 98;
            case VK_DECIMAL: return 99;
            case VK_LCONTROL: return 224;
            case VK_LSHIFT: return 225;
            case VK_LMENU: return 226;
            case VK_LWIN: return 227;
            case VK_RCONTROL: return 228;
            case VK_RSHIFT: return 229;
            case VK_RMENU: return 230;
            case VK_RWIN: return 231;
            case VK_CONTROL:
                return (a_lParam & (1ll << 24)) ? 228 : 224;
            case VK_SHIFT:
                return (MapVirtualKeyW((a_lParam >> 16) & 0xFF, MAPVK_VSC_TO_VK_EX) == VK_RSHIFT) ? 229 : 225;
            case VK_MENU:
                return (a_lParam & (1ll << 24)) ? 230 : 226;
            default:
                return 0;
            }
        }

        bool RoutesToMinecraft()
        {
            const auto& st = State();
            return st.minecraftOwnsPlayer.load() && !st.falloutMenuOpen.load();
        }

        void RouteMouseDelta(int a_dx, int a_dy)
        {
            if (!RoutesToMinecraft() || (a_dx == 0 && a_dy == 0)) {
                return;
            }

            auto& st = State();
            const bool screenOpen = st.mcScreenOpen.load();
            if (screenOpen != g_lastScreenOpen) {
                g_lastScreenOpen = screenOpen;
                if (screenOpen) {
                    g_virtualX = std::max(1, st.viewportW.load()) / 2;
                    g_virtualY = std::max(1, st.viewportH.load()) / 2;
                    st.cursorX = static_cast<int>(g_virtualX);
                    st.cursorY = static_cast<int>(g_virtualY);
                } else {
                    g_virtualX = 0;
                    g_virtualY = 0;
                }
            }

            if (screenOpen) {
                const int w = std::max(1, st.viewportW.load());
                const int h = std::max(1, st.viewportH.load());
                g_virtualX = std::clamp<long long>(g_virtualX + a_dx, 0, w - 1);
                g_virtualY = std::clamp<long long>(g_virtualY + a_dy, 0, h - 1);
                st.cursorX = static_cast<int>(g_virtualX);
                st.cursorY = static_cast<int>(g_virtualY);
                // c=0: absolute cursor coordinates for Minecraft GUI screens.
                Link::Get().PushInput(proto::kInCursor, 0,
                    static_cast<std::int32_t>(g_virtualX),
                    static_cast<std::int32_t>(g_virtualY), 0);
            } else {
                // c=1: RELATIVE look delta. v0.5.2 accumulated these into a fake absolute cursor
                // starting at 960,540; Minecraft's first event therefore looked like a gigantic
                // 960x540 mouse swipe. Send the actual raw delta instead.
                Link::Get().PushInput(proto::kInCursor, 0, a_dx, a_dy, 1);
            }
        }

        void RouteButton(std::uint16_t a_button, bool a_down)
        {
            if (RoutesToMinecraft()) {
                Link::Get().PushInput(proto::kInMouseButton, a_button, a_down ? 1 : 0);
            }
        }

        LRESULT CALLBACK FalloutCraftWndProc(HWND a_hwnd, UINT a_msg, WPARAM a_wParam, LPARAM a_lParam)
        {
            switch (a_msg) {
            case WM_INPUT:
                if (RoutesToMinecraft()) {
                    UINT bytes = 0;
                    if (GetRawInputData(reinterpret_cast<HRAWINPUT>(a_lParam), RID_INPUT, nullptr, &bytes, sizeof(RAWINPUTHEADER)) == 0 && bytes) {
                        std::vector<std::uint8_t> storage(bytes);
                        if (GetRawInputData(reinterpret_cast<HRAWINPUT>(a_lParam), RID_INPUT, storage.data(), &bytes, sizeof(RAWINPUTHEADER)) == bytes) {
                            const auto* raw = reinterpret_cast<const RAWINPUT*>(storage.data());
                            if (raw->header.dwType == RIM_TYPEMOUSE &&
                                (raw->data.mouse.usFlags & MOUSE_MOVE_ABSOLUTE) == 0) {
                                RouteMouseDelta(raw->data.mouse.lLastX, raw->data.mouse.lLastY);
                                g_lastRawMouseMs = GetTickCount64();
                            }
                        }
                    }
                }
                break;
            case WM_MOUSEMOVE:
                if (RoutesToMinecraft() && GetTickCount64() - g_lastRawMouseMs > 100) {
                    const int x = static_cast<short>(LOWORD(a_lParam));
                    const int y = static_cast<short>(HIWORD(a_lParam));
                    if (g_haveFallback) {
                        RouteMouseDelta(x - g_fallbackX, y - g_fallbackY);
                    }
                    g_fallbackX = x;
                    g_fallbackY = y;
                    g_haveFallback = true;
                }
                break;
            case WM_LBUTTONDOWN: RouteButton(1, true); break;
            case WM_LBUTTONUP: RouteButton(1, false); break;
            case WM_RBUTTONDOWN: RouteButton(3, true); break;
            case WM_RBUTTONUP: RouteButton(3, false); break;
            case WM_MBUTTONDOWN: RouteButton(2, true); break;
            case WM_MBUTTONUP: RouteButton(2, false); break;
            case WM_XBUTTONDOWN:
                RouteButton(HIWORD(a_wParam) == XBUTTON1 ? 4 : 5, true);
                break;
            case WM_XBUTTONUP:
                RouteButton(HIWORD(a_wParam) == XBUTTON1 ? 4 : 5, false);
                break;
            case WM_MOUSEWHEEL:
                if (RoutesToMinecraft()) {
                    Link::Get().PushInput(proto::kInScroll, 0, GET_WHEEL_DELTA_WPARAM(a_wParam));
                }
                break;
            case WM_KEYDOWN:
            case WM_SYSKEYDOWN:
            case WM_KEYUP:
            case WM_SYSKEYUP:
                if (RoutesToMinecraft()) {
                    if (const auto sc = VkToSdl(a_wParam, a_lParam); sc != 0) {
                        const bool down = a_msg == WM_KEYDOWN || a_msg == WM_SYSKEYDOWN;
                        Link::Get().PushInput(proto::kInKey, sc, down ? 1 : 0);
                    }
                }
                break;
            case WM_KILLFOCUS:
                Input::ReleaseAll();
                break;
            default:
                break;
            }
            return g_originalWndProc ? CallWindowProcW(g_originalWndProc, a_hwnd, a_msg, a_wParam, a_lParam)
                                     : DefWindowProcW(a_hwnd, a_msg, a_wParam, a_lParam);
        }
    }

        // Fallout's raw Windows messages still need to reach menus and the rest of the game,
        // but its gameplay PlayerControls must not turn the same mouse/keyboard input into a
        // second camera/movement stream while Minecraft owns the player.
        struct PlayerControlsInputHook
        {
            static void thunk(RE::PlayerControls* a_this, const RE::InputEvent* a_queueHead)
            {
                if (State().minecraftOwnsPlayer.load() && !State().falloutMenuOpen.load()) {
                    return;
                }
                func(a_this, a_queueHead);
            }
            static inline REL::Relocation<decltype(thunk)> func;
        };

    namespace Input
    {
        void Install()
        {
            bool expectedControls = false;
            if (g_playerControlsHooked.compare_exchange_strong(expectedControls, true)) {
                REL::Relocation<std::uintptr_t> controlsVtbl{ RE::PlayerControls::VTABLE[0] };
                PlayerControlsInputHook::func =
                    controlsVtbl.write_vfunc(0x00, PlayerControlsInputHook::thunk);
                logger::info("FalloutCraft: Fallout PlayerControls gameplay input suppressed while Minecraft owns player");
            }

            auto* rw = RE::BSGraphics::GetCurrentRendererWindow();
            HWND hwnd = rw ? reinterpret_cast<HWND>(rw->hwnd) : nullptr;
            if (!hwnd) {
                return;
            }

            std::lock_guard lock(g_hookLock);
            if (g_hwnd == hwnd && g_originalWndProc) {
                return;
            }

            if (g_hwnd && g_originalWndProc) {
                SetWindowLongPtrW(g_hwnd, GWLP_WNDPROC, reinterpret_cast<LONG_PTR>(g_originalWndProc));
            }

            g_hwnd = hwnd;
            g_originalWndProc = reinterpret_cast<WNDPROC>(
                SetWindowLongPtrW(hwnd, GWLP_WNDPROC, reinterpret_cast<LONG_PTR>(FalloutCraftWndProc)));
            if (g_originalWndProc) {
                g_installed = true;
                logger::info("FalloutCraft: Fallout window input bridge installed");
            } else {
                logger::warn("FalloutCraft: could not subclass Fallout window ({})", GetLastError());
            }
        }

        void ConsumeLook(float& a_dx, float& a_dy)
        {
            // Mouse deltas are delivered directly to Minecraft through the input ring.
            a_dx = 0.0f;
            a_dy = 0.0f;
        }

        void ReleaseAll()
        {
            Link::Get().PushInput(proto::kInReleaseAll, 0);
        }

        void SetActivatePromptKey(bool) {}
    }
}
