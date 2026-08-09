using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Unity.IL2CPP;
using HarmonyLib;
using UnityEngine;
using KeyboardShortcut = BepInEx.Unity.IL2CPP.Configuration.KeyboardShortcut;

namespace RedFox.DeathBeacon.GamePass.IL2CPP;

[BepInPlugin(GUID, NAME, VERSION)]
public sealed class Plugin : BasePlugin
{
    public const string GUID = "redfox.planetcrafter.gamepass.deathbeacon";
    public const string NAME = "Death Beacon - Game Pass IL2CPP Port";
    public const string VERSION = "1.4.0-gp.1";

    internal static Plugin Instance = null!;
    internal static ConfigEntry<KeyboardShortcut> DismissKey = null!;
    internal static Vector3? PendingDeathPosition;
    private Harmony? _harmony;

    public override void Load()
    {
        Instance = this;
        DismissKey = Config.Bind(
            "General",
            "DismissKey",
            new KeyboardShortcut(KeyCode.X, KeyCode.LeftShift),
            "Key combo to dismiss (clear) all death chest markers. Default: Shift+X");

        AddComponent<DeathBeaconHost>();
        _harmony = new Harmony(GUID);

        var playerStatus = ReflectionUtil.FindType("SpaceCraft.PlayerStatus");
        if (playerStatus == null)
        {
            Log.LogError("SpaceCraft.PlayerStatus was not found. This Game Pass build is not compatible with this port yet.");
            return;
        }

        var die = ReflectionUtil.FindMethod(playerStatus, "DieAndRespawn");
        var consequence = ReflectionUtil.FindMethod(playerStatus, "HandleDyingConsequencesNotification");

        if (die != null)
            _harmony.Patch(die, prefix: new HarmonyMethod(typeof(DeathBeaconHooks), nameof(DeathBeaconHooks.DieAndRespawnPrefix)));
        else
            Log.LogError("PlayerStatus.DieAndRespawn was not found.");

        if (consequence != null)
            _harmony.Patch(consequence, postfix: new HarmonyMethod(typeof(DeathBeaconHooks), nameof(DeathBeaconHooks.HandleDyingConsequencesNotificationPostfix)));
        else
            Log.LogError("PlayerStatus.HandleDyingConsequencesNotification was not found.");

        Log.LogMessage("DEATH BEACON IL2CPP PORT ACTIVE - Game Pass test build.");
    }

    public override bool Unload()
    {
        _harmony?.UnpatchSelf();
        return true;
    }
}

internal static class DeathBeaconHooks
{
    public static void DieAndRespawnPrefix(object __instance, object[] __args)
    {
        try
        {
            var isOwner = ReflectionUtil.GetBool(__instance, "IsOwner", true);
            if (!isOwner) return;

            var handle = __args.Length > 0 ? ReflectionUtil.AsBool(__args[^1], true) : true;
            if (!handle) return;

            if (__instance is Component c)
            {
                Plugin.PendingDeathPosition = c.transform.position;
                Plugin.Instance.Log.LogInfo($"Death position recorded: {Plugin.PendingDeathPosition}");
            }
        }
        catch (Exception ex)
        {
            Plugin.Instance.Log.LogWarning("Death position hook failed: " + ex.Message);
        }
    }

    public static void HandleDyingConsequencesNotificationPostfix(object __instance, object[] __args)
    {
        try
        {
            if (__args.Length == 0 || ReflectionUtil.AsInt(__args[0], -1) != 1) return;
            if (!Plugin.PendingDeathPosition.HasValue) return;

            var deathPos = Plugin.PendingDeathPosition.Value;
            Plugin.PendingDeathPosition = null;

            var groupData = ReflectionUtil.Get(__instance, "canisterGroup");
            var groupId = ReflectionUtil.Get(groupData, "id")?.ToString();
            if (string.IsNullOrWhiteSpace(groupId))
            {
                Plugin.Instance.Log.LogWarning("Death drop confirmed, but canisterGroup.id could not be read.");
                return;
            }

            var groupsHandler = ReflectionUtil.FindType("SpaceCraft.GroupsHandler");
            var getGroup = groupsHandler?.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static)
                .FirstOrDefault(m => m.Name == "GetGroupViaId" && m.GetParameters().Length == 1);
            var group = getGroup?.Invoke(null, new object?[] { groupId });
            if (group == null)
            {
                Plugin.Instance.Log.LogWarning($"Could not resolve death canister group '{groupId}'.");
                return;
            }

            var hash = ReflectionUtil.AsInt(ReflectionUtil.Get(group, "stableHashCode"), int.MinValue);
            if (hash == int.MinValue)
                hash = ReflectionUtil.AsInt(ReflectionUtil.Invoke(group, "get_stableHashCode"), int.MinValue);

            Plugin.Instance.Log.LogInfo($"Death drop confirmed. Scanning for canister near {deathPos} (group={groupId}, hash={hash})...");
            DeathBeaconHost.BeginScan(deathPos, hash);
        }
        catch (Exception ex)
        {
            Plugin.Instance.Log.LogWarning("Death drop hook failed: " + ex);
        }
    }
}

public sealed class DeathBeaconHost : MonoBehaviour
{
    private sealed class ScanRequest
    {
        public Vector3 DeathPos;
        public int TargetHash;
        public float Elapsed;
        public float NextScan;
    }

    private static readonly List<ScanRequest> Scans = new();
    private static readonly List<Transform> Markers = new();
    private static Type? _groupNetworkBaseType;
    private static Camera? _mainCam;
    private static GUIStyle? _textStyle;
    private static GUIStyle? _shadowStyle;
    private static GUIStyle? _arrowStyle;
    private static GUIStyle? _arrowShadowStyle;
    private static Font? _font;
    private static Texture2D? _bgTex;

    public DeathBeaconHost(IntPtr ptr) : base(ptr) { }

    internal static void BeginScan(Vector3 position, int targetHash)
    {
        Scans.Add(new ScanRequest { DeathPos = position, TargetHash = targetHash, Elapsed = 0f, NextScan = 0f });
    }

    private void Update()
    {
        if (Plugin.DismissKey != null && Plugin.DismissKey.Value.IsDown())
        {
            var count = Markers.Count;
            Markers.Clear();
            Scans.Clear();
            Plugin.Instance.Log.LogInfo($"Dismissed {count} death chest marker(s).");
        }

        for (var i = Markers.Count - 1; i >= 0; i--)
            if (Markers[i] == null) Markers.RemoveAt(i);

        var dt = Time.unscaledDeltaTime;
        for (var i = Scans.Count - 1; i >= 0; i--)
        {
            var scan = Scans[i];
            scan.Elapsed += dt;
            scan.NextScan -= dt;
            if (scan.NextScan > 0f) continue;
            scan.NextScan = 0.25f;

            if (TryFindCanister(scan.DeathPos, scan.TargetHash, out var target))
            {
                if (target != null && !Markers.Any(x => x == target)) Markers.Add(target);
                Plugin.Instance.Log.LogInfo($"Found death canister at {target?.position}. Attaching HUD marker.");
                Scans.RemoveAt(i);
                continue;
            }

            if (scan.Elapsed >= 10f)
            {
                Plugin.Instance.Log.LogWarning("Could not locate death canister within timeout. Marker not placed.");
                Scans.RemoveAt(i);
            }
        }
    }

    private void OnGUI()
    {
        if (_mainCam == null || !_mainCam.isActiveAndEnabled) _mainCam = Camera.main;
        if (_mainCam == null || Markers.Count == 0) return;
        if (_textStyle == null) InitStyles();
        if (_textStyle == null) return;

        foreach (var marker in Markers.ToArray())
        {
            if (marker == null) continue;
            DrawMarker(marker);
        }
    }

    private static bool TryFindCanister(Vector3 deathPos, int targetHash, out Transform? target)
    {
        target = null;
        try
        {
            _groupNetworkBaseType ??= ReflectionUtil.FindType("SpaceCraft.GroupNetworkBase");
            if (_groupNetworkBaseType == null) return false;

            var method = typeof(Resources).GetMethods(BindingFlags.Public | BindingFlags.Static)
                .FirstOrDefault(m => m.Name == "FindObjectsOfTypeAll" && !m.IsGenericMethod &&
                                     m.GetParameters().Length == 1 && m.GetParameters()[0].ParameterType == typeof(Type));
            if (method == null) return false;
            var found = method.Invoke(null, new object[] { _groupNetworkBaseType });

            foreach (var item in ReflectionUtil.Enumerate(found))
            {
                if (item is not Component component) continue;
                if (Vector3.Distance(component.transform.position, deathPos) >= 5f) continue;
                var hash = ReflectionUtil.AsInt(ReflectionUtil.Invoke(item, "GetGroupHash"), int.MinValue);
                if (targetHash != int.MinValue && hash != targetHash) continue;
                target = component.transform;
                return true;
            }
        }
        catch (Exception ex)
        {
            Plugin.Instance.Log.LogWarning("Death canister scan error: " + ex.Message);
        }
        return false;
    }

    private static void DrawMarker(Transform marker)
    {
        if (_mainCam == null) return;
        var worldPos = marker.position;
        var distance = Vector3.Distance(_mainCam.transform.position, worldPos);
        var screenPos = _mainCam.WorldToScreenPoint(worldPos);
        var guiY = Screen.height - screenPos.y;
        var label = $"DEATH CHEST  -  {Mathf.RoundToInt(distance)}m";

        if (screenPos.z > 0f && screenPos.x > 50f && screenPos.x < Screen.width - 50f && guiY > 50f && guiY < Screen.height - 50f)
        {
            const float w = 320f;
            const float h = 36f;
            GUI.DrawTexture(new Rect(screenPos.x - w / 2f - 6f, guiY - h - 10f, w + 12f, h + 8f), _bgTex!);
            var r = new Rect(screenPos.x - w / 2f, guiY - h - 6f, w, h);
            GUI.Label(new Rect(r.x + 2f, r.y + 2f, r.width, r.height), label, _shadowStyle!);
            GUI.Label(r, label, _textStyle!);
        }
        else
        {
            DrawEdgeIndicator(screenPos, distance);
        }
    }

    private static void DrawEdgeIndicator(Vector3 screenPos, float distance)
    {
        var cx = Screen.width / 2f;
        var cy = Screen.height / 2f;
        var sx = screenPos.x;
        var sy = Screen.height - screenPos.y;
        if (screenPos.z < 0f) { sx = Screen.width - sx; sy = Screen.height - sy; }

        var dx = sx - cx;
        var dy = sy - cy;
        var adx = Mathf.Abs(dx);
        var ady = Mathf.Abs(dy);
        var maxX = cx - 50f;
        var maxY = cy - 50f;
        var scale = adx / maxX > ady / maxY
            ? maxX / Mathf.Max(adx, 0.001f)
            : maxY / Mathf.Max(ady, 0.001f);
        var x = cx + dx * scale;
        var y = cy + dy * scale;
        var text = $"{GetArrowChar(Mathf.Atan2(dy, dx) * 57.29578f)}  {Mathf.RoundToInt(distance)}m";
        const float w = 200f;
        const float h = 40f;
        GUI.DrawTexture(new Rect(x - w / 2f - 4f, y - h / 2f - 2f, w + 8f, h + 4f), _bgTex!);
        var r = new Rect(x - w / 2f, y - h / 2f, w, h);
        GUI.Label(new Rect(r.x + 2f, r.y + 2f, r.width, r.height), text, _arrowShadowStyle!);
        GUI.Label(r, text, _arrowStyle!);
    }

    private static string GetArrowChar(float angleDeg)
    {
        if (angleDeg < -157.5f) return "◀";
        if (angleDeg < -112.5f) return "◀▲";
        if (angleDeg < -67.5f) return "▲";
        if (angleDeg < -22.5f) return "▲▶";
        if (angleDeg < 22.5f) return "▶";
        if (angleDeg < 67.5f) return "▼▶";
        if (angleDeg < 112.5f) return "▼";
        if (angleDeg < 157.5f) return "◀▼";
        return "◀";
    }

    private static void InitStyles()
    {
        foreach (var fontName in new[] { "Arial", "Liberation Sans", "Segoe UI", "Helvetica", "Verdana" })
        {
            _font = Font.CreateDynamicFontFromOSFont(fontName, 22);
            if (_font != null) break;
        }

        _bgTex = new Texture2D(1, 1);
        _bgTex.SetPixel(0, 0, new Color(0f, 0f, 0f, 0.6f));
        _bgTex.Apply();

        _textStyle = new GUIStyle();
        if (_font != null) _textStyle.font = _font;
        _textStyle.normal.textColor = new Color(1f, 0.25f, 0.25f, 1f);
        _textStyle.fontSize = 22;
        _textStyle.fontStyle = FontStyle.Bold;
        _textStyle.alignment = TextAnchor.MiddleCenter;
        _textStyle.wordWrap = false;
        _textStyle.clipping = TextClipping.Overflow;

        _shadowStyle = new GUIStyle(_textStyle);
        _shadowStyle.normal.textColor = new Color(0f, 0f, 0f, 0.8f);
        _arrowStyle = new GUIStyle(_textStyle) { fontSize = 28 };
        _arrowShadowStyle = new GUIStyle(_shadowStyle) { fontSize = 28 };
    }
}

internal static class ReflectionUtil
{
    private const BindingFlags All = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static;

    internal static Type? FindType(string fullName)
    {
        foreach (var a in AppDomain.CurrentDomain.GetAssemblies())
        {
            try
            {
                var t = a.GetType(fullName, false);
                if (t != null) return t;
            }
            catch { }
        }
        return null;
    }

    internal static MethodInfo? FindMethod(Type type, string name) =>
        type.GetMethods(All).FirstOrDefault(m => m.Name == name);

    internal static object? Get(object? obj, string name)
    {
        if (obj == null) return null;
        var t = obj.GetType();
        try { var p = t.GetProperty(name, All); if (p != null) return p.GetValue(obj); } catch { }
        try { var f = t.GetField(name, All); if (f != null) return f.GetValue(obj); } catch { }
        try { var m = t.GetMethod("get_" + name, All, null, Type.EmptyTypes, null); if (m != null) return m.Invoke(obj, null); } catch { }
        return null;
    }

    internal static object? Invoke(object? obj, string name)
    {
        if (obj == null) return null;
        try { return obj.GetType().GetMethods(All).FirstOrDefault(m => m.Name == name && m.GetParameters().Length == 0)?.Invoke(obj, null); }
        catch { return null; }
    }

    internal static bool GetBool(object? obj, string name, bool fallback) => AsBool(Get(obj, name), fallback);

    internal static bool AsBool(object? value, bool fallback)
    {
        if (value == null) return fallback;
        try { return Convert.ToBoolean(value); } catch { return fallback; }
    }

    internal static int AsInt(object? value, int fallback)
    {
        if (value == null) return fallback;
        try { return Convert.ToInt32(value); } catch { }
        try { return int.Parse(value.ToString() ?? ""); } catch { return fallback; }
    }

    internal static IEnumerable<object?> Enumerate(object? source)
    {
        if (source == null) yield break;
        if (source is IEnumerable e)
        {
            foreach (var x in e) yield return x;
            yield break;
        }

        var t = source.GetType();
        var lenObj = Get(source, "Length") ?? Get(source, "Count");
        var len = AsInt(lenObj, 0);
        var item = t.GetProperties(All).FirstOrDefault(p => p.GetIndexParameters().Length == 1);
        if (item == null) yield break;
        for (var i = 0; i < len; i++)
        {
            object? value = null;
            try { value = item.GetValue(source, new object[] { i }); } catch { }
            yield return value;
        }
    }
}
