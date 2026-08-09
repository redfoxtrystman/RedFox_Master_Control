using System;
using System.Collections.Generic;
using BepInEx.Unity.IL2CPP.Configuration;
using UnityEngine;

namespace BepInEx.Configuration
{
    /// <summary>
    /// BepInEx 5 namespace-compatible keyboard shortcut backed by the BepInEx 6 IL2CPP implementation.
    /// </summary>
    public struct KeyboardShortcut
    {
        private BepInEx.Unity.IL2CPP.Configuration.KeyboardShortcut _inner;

        static KeyboardShortcut()
        {
            TomlTypeConverter.AddConverter(typeof(KeyboardShortcut), new TypeConverter
            {
                ConvertToString = (o, type) => ((KeyboardShortcut)o).Serialize(),
                ConvertToObject = (s, type) => Deserialize(s)
            });
        }

        public static readonly KeyboardShortcut Empty =
            new KeyboardShortcut(BepInEx.Unity.IL2CPP.Configuration.KeyboardShortcut.Empty);

        public KeyboardShortcut(KeyCode mainKey, params KeyCode[] modifiers)
        {
            _inner = new BepInEx.Unity.IL2CPP.Configuration.KeyboardShortcut(mainKey, modifiers);
        }

        private KeyboardShortcut(BepInEx.Unity.IL2CPP.Configuration.KeyboardShortcut inner)
        {
            _inner = inner;
        }

        public KeyCode MainKey => _inner.MainKey;
        public IEnumerable<KeyCode> Modifiers => _inner.Modifiers;

        public static KeyboardShortcut Deserialize(string str) =>
            new KeyboardShortcut(BepInEx.Unity.IL2CPP.Configuration.KeyboardShortcut.Deserialize(str));

        public string Serialize() => _inner.Serialize();
        public bool IsDown() => _inner.IsDown();
        public bool IsPressed() => _inner.IsPressed();
        public bool IsUp() => _inner.IsUp();
        public override string ToString() => _inner.ToString();

        public override bool Equals(object obj) =>
            obj is KeyboardShortcut other && _inner.Equals(other._inner);

        public override int GetHashCode() => _inner.GetHashCode();
    }
}
