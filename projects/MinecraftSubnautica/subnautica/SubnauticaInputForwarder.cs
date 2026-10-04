using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Sends the host's keyboard/mouse state into SkyCraft's existing SDL-scancode input ring.
    ///
    /// This deliberately starts with keyboard/mouse. Controller-to-Minecraft action translation
    /// comes after the first end-to-end water slice is proven.
    /// </summary>
    public sealed class SubnauticaInputForwarder
    {
        // SDL3/USB HID scancodes expected by the current SkyCraft InputBridge.
        private static readonly KeyMap[] Keys =
        {
            new KeyMap(Key.W, 26),
            new KeyMap(Key.A, 4),
            new KeyMap(Key.S, 22),
            new KeyMap(Key.D, 7),
            new KeyMap(Key.Space, 44),
            new KeyMap(Key.LeftShift, 225),
            new KeyMap(Key.RightShift, 229),
            new KeyMap(Key.LeftCtrl, 224),
            new KeyMap(Key.RightCtrl, 228),
            new KeyMap(Key.E, 8),
            new KeyMap(Key.Q, 20),
            new KeyMap(Key.F, 9),
            new KeyMap(Key.R, 21),
            new KeyMap(Key.T, 23),
            new KeyMap(Key.Tab, 43),
            new KeyMap(Key.Escape, 41),
            new KeyMap(Key.Digit1, 30),
            new KeyMap(Key.Digit2, 31),
            new KeyMap(Key.Digit3, 32),
            new KeyMap(Key.Digit4, 33),
            new KeyMap(Key.Digit5, 34),
            new KeyMap(Key.Digit6, 35),
            new KeyMap(Key.Digit7, 36),
            new KeyMap(Key.Digit8, 37),
            new KeyMap(Key.Digit9, 38)
        };

        private readonly Dictionary<Key, bool> _keyState = new Dictionary<Key, bool>();
        private readonly bool[] _mouseState = new bool[4];
        private bool _active;
        private Vector2 _lastCursor;
        private bool _haveCursor;

        public void SetActive(bool active, BridgeRuntime runtime)
        {
            if (_active == active)
                return;

            _active = active;

            if (!active)
            {
                runtime.ReleaseAllInput();
                _keyState.Clear();
                Array.Clear(_mouseState, 0, _mouseState.Length);
                _haveCursor = false;
            }
        }

        public void Tick(BridgeRuntime runtime)
        {
            if (!_active)
                return;

            Keyboard keyboard = Keyboard.current;
            if (keyboard != null)
            {
                for (int i = 0; i < Keys.Length; i++)
                {
                    KeyMap map = Keys[i];
                    bool down = keyboard[map.Key].isPressed;
                    bool old = _keyState.TryGetValue(map.Key, out bool previous) && previous;

                    if (down != old && runtime.PushKey(map.Scancode, down))
                        _keyState[map.Key] = down;
                }
            }

            Mouse mouse = Mouse.current;
            if (mouse == null)
                return;

            ForwardMouseButton(runtime, 1, 1, mouse.leftButton.isPressed);
            ForwardMouseButton(runtime, 3, 2, mouse.rightButton.isPressed);
            ForwardMouseButton(runtime, 2, 3, mouse.middleButton.isPressed);

            Vector2 cursor = mouse.position.ReadValue();
            // Unity screen coordinates are bottom-left based; SDL window coordinates are top-left.
            Vector2 sdlCursor = new Vector2(cursor.x, Screen.height - cursor.y);
            if (!_haveCursor || (sdlCursor - _lastCursor).sqrMagnitude >= 0.25f)
            {
                if (runtime.PushCursor(
                    Mathf.RoundToInt(sdlCursor.x),
                    Mathf.RoundToInt(sdlCursor.y)))
                {
                    _lastCursor = sdlCursor;
                    _haveCursor = true;
                }
            }

            float scrollY = mouse.scroll.ReadValue().y;
            if (Mathf.Abs(scrollY) > 0.01f)
            {
                // Windows usually reports 120 per notch; normalize devices that report +/-1.
                int wheelUnits = Mathf.Abs(scrollY) < 10.0f
                    ? Mathf.RoundToInt(scrollY * 120.0f)
                    : Mathf.RoundToInt(scrollY);

                runtime.PushScroll(wheelUnits);
            }
        }

        private void ForwardMouseButton(BridgeRuntime runtime, ushort sdlButton, int stateSlot, bool down)
        {
            bool old = _mouseState[stateSlot];
            if (down == old)
                return;

            if (runtime.PushMouseButton(sdlButton, down))
                _mouseState[stateSlot] = down;
        }

        private readonly struct KeyMap
        {
            public readonly Key Key;
            public readonly ushort Scancode;

            public KeyMap(Key key, ushort scancode)
            {
                Key = key;
                Scancode = scancode;
            }
        }
    }
}
