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
        std::atomic<bool> g_nativeInputInstalled{ false };
        float g_lookDx = 0.0f;
        float g_lookDy = 0.0f;
        std::mutex g_lookLock;
        std::array<bool, 256> g_keyDown{};
        std::array<bool, 8> g_mouseDown{};
        std::mutex g_buttonLock;

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
            if (st.mcScreenOpen.load()) {
                const int w = std::max(1, st.viewportW.load());
                const int h = std::max(1, st.viewportH.load());
                const int x = std::clamp(st.cursorX.load() + a_dx, 0, w - 1);
                const int y = std::clamp(st.cursorY.load() + a_dy, 0, h - 1);
                st.cursorX = x;
                st.cursorY = y;
                Link::Get().PushInput(proto::kInCursor, 0, x, y);
            } else {
                // Match SkyCraft's proven design: raw host mouse input drives the host-side
                // zero-latency look accumulator. Minecraft receives the resulting yaw/pitch
                // through HostState instead of independently integrating the same delta.
                std::lock_guard lock(g_lookLock);
                g_lookDx += static_cast<float>(a_dx);
                g_lookDy += static_cast<float>(a_dy);
            }
        }

        void RouteKey(std::uint16_t a_scancode, bool a_down)
        {
            if (!RoutesToMinecraft() || a_scancode >= g_keyDown.size()) {
                return;
            }
            std::lock_guard lock(g_buttonLock);
            if (g_keyDown[a_scancode] == a_down) {
                return;  // Fallout emits held button events every frame; Minecraft wants edges.
            }
            g_keyDown[a_scancode] = a_down;
            Link::Get().PushInput(proto::kInKey, a_scancode, a_down ? 1 : 0);
        }

        void RouteButton(std::uint16_t a_button, bool a_down)
        {
            if (!RoutesToMinecraft() || a_button >= g_mouseDown.size()) {
                return;
            }
            std::lock_guard lock(g_buttonLock);
            if (g_mouseDown[a_button] == a_down) {
                return;
            }
            g_mouseDown[a_button] = a_down;
            Link::Get().PushInput(proto::kInMouseButton, a_button, a_down ? 1 : 0);
        }

        void ClearBridgeButtonState()
        {
            std::lock_guard lock(g_buttonLock);
            g_keyDown.fill(false);
            g_mouseDown.fill(false);
        }

        LRESULT CALLBACK FalloutCraftWndProc(HWND a_hwnd, UINT a_msg, WPARAM a_wParam, LPARAM a_lParam)
        {
            switch (a_msg) {
            case WM_INPUT:
                // FO4's MouseMoveEvent can be cursor-bounded/scaled. Use true raw relative
                // WM_INPUT for Minecraft look/cursor so pitch can traverse the full +/-90 range.
                // The native BSInputEventUser still consumes Fallout's own mouse event below.
                if (RoutesToMinecraft()) {
                    UINT bytes = 0;
                    if (GetRawInputData(reinterpret_cast<HRAWINPUT>(a_lParam), RID_INPUT, nullptr, &bytes, sizeof(RAWINPUTHEADER)) == 0 && bytes) {
                        std::vector<std::uint8_t> storage(bytes);
                        if (GetRawInputData(reinterpret_cast<HRAWINPUT>(a_lParam), RID_INPUT, storage.data(), &bytes, sizeof(RAWINPUTHEADER)) == bytes) {
                            const auto* raw = reinterpret_cast<const RAWINPUT*>(storage.data());
                            if (raw->header.dwType == RIM_TYPEMOUSE &&
                                (raw->data.mouse.usFlags & MOUSE_MOVE_ABSOLUTE) == 0) {
                                RouteMouseDelta(raw->data.mouse.lLastX, raw->data.mouse.lLastY);
                            }
                        }
                    }
                }
                break;
            case WM_LBUTTONDOWN: if (!g_nativeInputInstalled.load()) RouteButton(1, true); break;
            case WM_LBUTTONUP: if (!g_nativeInputInstalled.load()) RouteButton(1, false); break;
            case WM_RBUTTONDOWN: if (!g_nativeInputInstalled.load()) RouteButton(3, true); break;
            case WM_RBUTTONUP: if (!g_nativeInputInstalled.load()) RouteButton(3, false); break;
            case WM_MBUTTONDOWN: if (!g_nativeInputInstalled.load()) RouteButton(2, true); break;
            case WM_MBUTTONUP: if (!g_nativeInputInstalled.load()) RouteButton(2, false); break;
            case WM_XBUTTONDOWN:
                if (!g_nativeInputInstalled.load()) RouteButton(HIWORD(a_wParam) == XBUTTON1 ? 4 : 5, true);
                break;
            case WM_XBUTTONUP:
                if (!g_nativeInputInstalled.load()) RouteButton(HIWORD(a_wParam) == XBUTTON1 ? 4 : 5, false);
                break;
            case WM_MOUSEWHEEL:
                if (!g_nativeInputInstalled.load() && RoutesToMinecraft()) {
                    Link::Get().PushInput(proto::kInScroll, 0, GET_WHEEL_DELTA_WPARAM(a_wParam));
                }
                break;
            case WM_KEYDOWN:
            case WM_SYSKEYDOWN:
            case WM_KEYUP:
            case WM_SYSKEYUP:
                if (!g_nativeInputInstalled.load() && RoutesToMinecraft()) {
                    if (const auto sc = VkToSdl(a_wParam, a_lParam); sc != 0) {
                        const bool down = a_msg == WM_KEYDOWN || a_msg == WM_SYSKEYDOWN;
                        RouteKey(sc, down);
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

        class FalloutCraftInputUser final : public RE::BSInputEventUser
        {
        public:
            static FalloutCraftInputUser* GetSingleton()
            {
                static FalloutCraftInputUser sink;
                return &sink;
            }

            bool ShouldHandleEvent(const RE::InputEvent* a_event) override
            {
                if (!a_event || !RoutesToMinecraft()) {
                    return false;
                }
                const auto type = a_event->eventType.get();
                return type == RE::INPUT_EVENT_TYPE::kButton ||
                       type == RE::INPUT_EVENT_TYPE::kMouseMove ||
                       type == RE::INPUT_EVENT_TYPE::kChar;
            }

            void OnMouseMoveEvent(const RE::MouseMoveEvent* a_event) override
            {
                if (!a_event || !RoutesToMinecraft()) {
                    return;
                }
                // Actual relative motion comes from WM_INPUT. Consuming this native event keeps
                // Fallout's camera from also reacting without integrating the same motion twice.
                const_cast<RE::MouseMoveEvent*>(a_event)->handled = RE::InputEvent::HANDLED_RESULT::kStop;
            }

            void OnCharacterEvent(const RE::CharacterEvent* a_event) override
            {
                if (!a_event || !RoutesToMinecraft() || !State().mcScreenOpen.load()) {
                    return;
                }
                Link::Get().PushInput(proto::kInText, 0, static_cast<std::int32_t>(a_event->charCode));
                const_cast<RE::CharacterEvent*>(a_event)->handled = RE::InputEvent::HANDLED_RESULT::kStop;
            }

            void OnButtonEvent(const RE::ButtonEvent* a_event) override
            {
                if (!a_event || !RoutesToMinecraft()) {
                    return;
                }

                const bool down = a_event->QAnalogValue() != 0.0f;
                if (a_event->device == RE::INPUT_DEVICE::kKeyboard) {
                    const auto vk = static_cast<WPARAM>(static_cast<std::uint32_t>(a_event->GetBSButtonCode()));
                    if (const auto sc = VkToSdl(vk, 0); sc != 0) {
                        RouteKey(sc, down);
                    }
                    const_cast<RE::ButtonEvent*>(a_event)->handled = RE::InputEvent::HANDLED_RESULT::kStop;
                    return;
                }

                if (a_event->device == RE::INPUT_DEVICE::kMouse) {
                    const auto code = static_cast<std::uint32_t>(a_event->GetBSButtonCode());
                    if (code == static_cast<std::uint32_t>(RE::BS_BUTTON_CODE::kWheelUp)) {
                        if (a_event->QJustPressed()) Link::Get().PushInput(proto::kInScroll, 0, 120);
                    } else if (code == static_cast<std::uint32_t>(RE::BS_BUTTON_CODE::kWheelDown)) {
                        if (a_event->QJustPressed()) Link::Get().PushInput(proto::kInScroll, 0, -120);
                    } else {
                        static constexpr std::uint16_t buttons[8]{ 1, 3, 2, 4, 5, 0, 0, 0 };
                        const auto id = a_event->QIDCode();
                        if (id < std::size(buttons) && buttons[id] != 0) {
                            RouteButton(buttons[id], down);
                        }
                    }
                    const_cast<RE::ButtonEvent*>(a_event)->handled = RE::InputEvent::HANDLED_RESULT::kStop;
                }
            }
        };

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
            if (auto* menuControls = RE::MenuControls::GetSingleton()) {
                auto* sink = FalloutCraftInputUser::GetSingleton();
                auto& handlers = menuControls->handlers;
                if (std::find(handlers.begin(), handlers.end(), sink) == handlers.end()) {
                    handlers.insert(handlers.begin(), sink);
                    logger::info("FalloutCraft: native Fallout input bridge installed first in MenuControls");
                }
                g_nativeInputInstalled = true;
            }

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
            std::lock_guard lock(g_lookLock);
            a_dx = g_lookDx;
            a_dy = g_lookDy;
            g_lookDx = 0.0f;
            g_lookDy = 0.0f;
        }

        void ReleaseAll()
        {
            ClearBridgeButtonState();
            {
                std::lock_guard lock(g_lookLock);
                g_lookDx = 0.0f;
                g_lookDy = 0.0f;
            }
            Link::Get().PushInput(proto::kInReleaseAll, 0);
        }

        void SetActivatePromptKey(bool) {}
    }
}
