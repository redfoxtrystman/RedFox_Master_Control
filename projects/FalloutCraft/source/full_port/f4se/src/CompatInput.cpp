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


        // Fallout's native ButtonEvent keyboard IDs are DirectInput scan codes, not Win32
        // virtual-key values. Feeding them through VkToSdl remapped keys such as E/F5 to the
        // wrong Minecraft keys and made the bridge appear to repeat/toggle unpredictably.
        // This is the same DIK -> SDL/USB-HID table used by SkyCraft's proven input path.
        constexpr auto kDikToSdl = [] {
            std::array<std::uint16_t, 256> t{};
            t[0x01] = 41;  // Esc
            for (int i = 0; i < 9; ++i) t[0x02 + i] = static_cast<std::uint16_t>(30 + i);  // 1-9
            t[0x0B] = 39;  // 0
            t[0x0C] = 45; t[0x0D] = 46; t[0x0E] = 42; t[0x0F] = 43;  // - = Backspace Tab
            t[0x10] = 20; t[0x11] = 26; t[0x12] = 8; t[0x13] = 21; t[0x14] = 23;  // Q W E R T
            t[0x15] = 28; t[0x16] = 24; t[0x17] = 12; t[0x18] = 18; t[0x19] = 19;  // Y U I O P
            t[0x1A] = 47; t[0x1B] = 48; t[0x1C] = 40; t[0x1D] = 224;               // [ ] Enter LCtrl
            t[0x1E] = 4; t[0x1F] = 22; t[0x20] = 7; t[0x21] = 9; t[0x22] = 10;     // A S D F G
            t[0x23] = 11; t[0x24] = 13; t[0x25] = 14; t[0x26] = 15;                // H J K L
            t[0x27] = 51; t[0x28] = 52; t[0x29] = 53; t[0x2A] = 225; t[0x2B] = 49; // ; ' ` LShift \
            t[0x2C] = 29; t[0x2D] = 27; t[0x2E] = 6; t[0x2F] = 25; t[0x30] = 5;    // Z X C V B
            t[0x31] = 17; t[0x32] = 16; t[0x33] = 54; t[0x34] = 55; t[0x35] = 56;  // N M , . /
            t[0x36] = 229; t[0x37] = 85; t[0x38] = 226; t[0x39] = 44; t[0x3A] = 57; // RShift KP* LAlt Space Caps
            for (int i = 0; i < 10; ++i) t[0x3B + i] = static_cast<std::uint16_t>(58 + i);  // F1-F10
            t[0x45] = 83; t[0x46] = 71;                                             // NumLock ScrollLock
            t[0x47] = 95; t[0x48] = 96; t[0x49] = 97; t[0x4A] = 86;                 // KP7 KP8 KP9 KP-
            t[0x4B] = 92; t[0x4C] = 93; t[0x4D] = 94; t[0x4E] = 87;                 // KP4 KP5 KP6 KP+
            t[0x4F] = 89; t[0x50] = 90; t[0x51] = 91; t[0x52] = 98; t[0x53] = 99;   // KP1 KP2 KP3 KP0 KP.
            t[0x56] = 100; t[0x57] = 68; t[0x58] = 69;                              // OEM102 F11 F12
            t[0x9C] = 88; t[0x9D] = 228; t[0xB5] = 84; t[0xB7] = 70; t[0xB8] = 230; // KPEnter RCtrl KP/ PrtSc RAlt
            t[0xC5] = 72; t[0xC7] = 74; t[0xC8] = 82; t[0xC9] = 75; t[0xCB] = 80;    // Pause Home Up PgUp Left
            t[0xCD] = 79; t[0xCF] = 77; t[0xD0] = 81; t[0xD1] = 78; t[0xD2] = 73;    // Right End Down PgDn Insert
            t[0xD3] = 76; t[0xDB] = 227; t[0xDC] = 231; t[0xDD] = 101;               // Delete LWin RWin Menu
            return t;
        }();

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

                const bool pressed = a_event->QJustPressed();
                const bool released = a_event->QReleased();

                if (a_event->device == RE::INPUT_DEVICE::kKeyboard) {
                    // Native Fallout keyboard events use DirectInput scan codes (QIDCode).
                    // Only forward real edges; held events are consumed but never replayed as
                    // Minecraft key presses. This fixes E/F5 and other one-shot keys firing
                    // repeatedly while still preserving normal held movement.
                    const auto dik = a_event->QIDCode();
                    if ((pressed || released) && dik < kDikToSdl.size()) {
                        if (const auto sc = kDikToSdl[dik]; sc != 0) {
                            RouteKey(sc, pressed);
                        }
                    }
                    const_cast<RE::ButtonEvent*>(a_event)->handled = RE::InputEvent::HANDLED_RESULT::kStop;
                    return;
                }

                if (a_event->device == RE::INPUT_DEVICE::kMouse) {
                    const auto code = static_cast<std::uint32_t>(a_event->GetBSButtonCode());
                    if (code == static_cast<std::uint32_t>(RE::BS_BUTTON_CODE::kWheelUp)) {
                        if (pressed) Link::Get().PushInput(proto::kInScroll, 0, 120);
                    } else if (code == static_cast<std::uint32_t>(RE::BS_BUTTON_CODE::kWheelDown)) {
                        if (pressed) Link::Get().PushInput(proto::kInScroll, 0, -120);
                    } else if (pressed || released) {
                        static constexpr std::uint16_t buttons[8]{ 1, 3, 2, 4, 5, 0, 0, 0 };
                        const auto id = a_event->QIDCode();
                        if (id < std::size(buttons) && buttons[id] != 0) {
                            RouteButton(buttons[id], pressed);
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
