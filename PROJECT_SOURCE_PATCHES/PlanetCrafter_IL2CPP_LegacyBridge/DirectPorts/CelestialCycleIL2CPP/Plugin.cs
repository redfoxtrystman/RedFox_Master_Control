using System;
using System.Collections;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Unity.IL2CPP;
using UnityEngine;
using KeyboardShortcut = BepInEx.Unity.IL2CPP.Configuration.KeyboardShortcut;

namespace RedFox.CelestialCycle.GamePass.IL2CPP;

[BepInPlugin(GUID, NAME, VERSION)]
public sealed class Plugin : BasePlugin
{
    public const string GUID = "redfox.planetcrafter.gamepass.celestialcycle";
    public const string NAME = "Celestial Cycle - Game Pass IL2CPP Core Port";
    public const string VERSION = "1.0.0-gp.1";

    internal static Plugin Instance = null!;
    internal static ConfigEntry<bool> MasterEnabled = null!;
    internal static ConfigEntry<bool> CycleEnabled = null!;
    internal static ConfigEntry<float> MinutesPerDay = null!;
    internal static ConfigEntry<float> DayHoldFraction = null!;
    internal static ConfigEntry<float> NightHoldFraction = null!;
    internal static ConfigEntry<float> StartPhase = null!;
    internal static ConfigEntry<bool> MoveSun = null!;
    internal static ConfigEntry<float> AxialTilt = null!;
    internal static ConfigEntry<float> SkyYaw = null!;
    internal static ConfigEntry<bool> ShowClock = null!;
    internal static ConfigEntry<bool> Clock24Hour = null!;
    internal static ConfigEntry<float> ClockPositionX = null!;
    internal static ConfigEntry<float> ClockPositionY = null!;
    internal static ConfigEntry<float> ClockFontSize = null!;
    internal static ConfigEntry<KeyboardShortcut> ClockToggle = null!;

    public override void Load()
    {
        Instance = this;
        BindConfig();
        AddComponent<CelestialCycleHost>();
        Log.LogMessage("CELESTIAL CYCLE IL2CPP CORE PORT ACTIVE - Game Pass test build.");
        Log.LogInfo("Core features in this test: repeating cycle, saved phase, day/night lerp, moving main sun, clock HUD.");
        Log.LogInfo("Advanced sky bodies / realistic placement / celestial lights are intentionally deferred until the core hook is verified in Game Pass.");
    }

    private void BindConfig()
    {
        MasterEnabled = Config.Bind("General", "MasterEnabled", true, "Master switch. False stops the port and restores captured vanilla values where possible.");
        CycleEnabled = Config.Bind("Cycle", "Enabled", true, "Drive a repeating day/night cycle.");
        MinutesPerDay = Config.Bind("Cycle", "MinutesPerDay", 30f, new ConfigDescription("Real minutes for one full in-game day.", new AcceptableValueRange<float>(1f, 600f)));
        DayHoldFraction = Config.Bind("Cycle", "DayHoldFraction", 0.32f, new ConfigDescription("Fraction held at full daylight.", new AcceptableValueRange<float>(0f, 0.9f)));
        NightHoldFraction = Config.Bind("Cycle", "NightHoldFraction", 0.22f, new ConfigDescription("Fraction held at full night.", new AcceptableValueRange<float>(0f, 0.9f)));
        StartPhase = Config.Bind("Cycle", "StartPhase", 0.30f, new ConfigDescription("Initial phase if no saved clock exists. 0=midnight, 0.5=noon.", new AcceptableValueRange<float>(0f, 1f)));

        MoveSun = Config.Bind("SkyMotion", "MoveSun", true, "Move the main directional light with the cycle.");
        AxialTilt = Config.Bind("SkyMotion", "AxialTilt", 15f, new ConfigDescription("Daily rotation axis tilt.", new AcceptableValueRange<float>(-89f, 89f)));
        SkyYaw = Config.Bind("SkyMotion", "SkyYaw", 0f, new ConfigDescription("Compass yaw of the rotation axis.", new AcceptableValueRange<float>(0f, 360f)));

        ShowClock = Config.Bind("Clock", "ShowClock", true, "Show a simple clock HUD.");
        Clock24Hour = Config.Bind("Clock", "Use24Hour", true, "24-hour clock when true.");
        ClockPositionX = Config.Bind("Clock", "PositionX", 0.5f, new ConfigDescription("0=left, .5=center, 1=right.", new AcceptableValueRange<float>(0f, 1f)));
        ClockPositionY = Config.Bind("Clock", "PositionY", 1f, new ConfigDescription("0=bottom, 1=top.", new AcceptableValueRange<float>(0f, 1f)));
        ClockFontSize = Config.Bind("Clock", "FontSize", 24f, new ConfigDescription("Clock text size.", new AcceptableValueRange<float>(8f, 120f)));
        ClockToggle = Config.Bind("Clock", "ToggleKey", new KeyboardShortcut(KeyCode.Insert), "Toggle the clock. Original mod default is Insert.");
    }
}

public sealed class CelestialCycleHost : MonoBehaviour
{
    private object? _cycle;
    private object? _lerpNv;
    private PropertyInfo? _lerpValueProperty;
    private MemberInfo? _fullDayStayMember;
    private float? _originalFullDayStay;
    private Light? _sun;
    private Quaternion _sunOriginalRotation;
    private bool _sunCaptured;
    private float _phase;
    private bool _phaseLoaded;
    private float _saveTimer;
    private float _acquireTimer;
    private float _lastWritten = float.NaN;
    private bool _hudVisible = true;
    private bool _loggedReady;
    private GUIStyle? _clockStyle;
    private GUIStyle? _clockShadow;
    private Texture2D? _clockBg;

    private static string PhaseFile => Path.Combine(Paths.ConfigPath, "CelestialCycle_phase.txt");

    public CelestialCycleHost(IntPtr ptr) : base(ptr) { }

    private void Awake()
    {
        _hudVisible = Plugin.ShowClock.Value;
        LoadPhaseOnce();
    }

    private void Update()
    {
        if (Plugin.ClockToggle.Value.IsDown())
        {
            _hudVisible = !_hudVisible;
            Plugin.Instance.Log.LogInfo("[Clock] toggled " + (_hudVisible ? "shown" : "hidden") + ".");
        }

        if (!Plugin.MasterEnabled.Value)
        {
            RestoreVanilla();
            return;
        }

        if (_cycle == null || _lerpNv == null || _lerpValueProperty == null)
        {
            _acquireTimer -= Time.unscaledDeltaTime;
            if (_acquireTimer <= 0f)
            {
                _acquireTimer = 1f;
                TryAcquire();
            }
        }

        if (Plugin.CycleEnabled.Value)
        {
            AdvancePhase();
            DriveLerp();
            DriveSun();
        }

        PersistPhase();
    }

    private void OnDestroy() => RestoreVanilla();

    private void OnGUI()
    {
        if (!Plugin.MasterEnabled.Value || !Plugin.ShowClock.Value || !_hudVisible) return;
        if (_clockStyle == null) BuildClockStyle();
        if (_clockStyle == null || _clockBg == null) return;

        var text = FormatClock(_phase);
        var width = 180f;
        var height = Math.Max(34f, Plugin.ClockFontSize.Value + 12f);
        var x = Mathf.Clamp01(Plugin.ClockPositionX.Value) * Screen.width - width * Mathf.Clamp01(Plugin.ClockPositionX.Value);
        var yFromBottom = Mathf.Clamp01(Plugin.ClockPositionY.Value) * Screen.height;
        var y = Screen.height - yFromBottom;
        if (Plugin.ClockPositionY.Value >= 0.5f) y += 8f;
        else y -= height + 8f;
        x = Mathf.Clamp(x, 4f, Math.Max(4f, Screen.width - width - 4f));
        y = Mathf.Clamp(y, 4f, Math.Max(4f, Screen.height - height - 4f));

        var bg = new Rect(x, y, width, height);
        GUI.DrawTexture(bg, _clockBg);
        var r = new Rect(x + 4f, y, width - 8f, height);
        GUI.Label(new Rect(r.x + 2f, r.y + 2f, r.width, r.height), text, _clockShadow!);
        GUI.Label(r, text, _clockStyle!);
    }

    private void TryAcquire()
    {
        var cycleType = ReflectionUtil.FindType("SpaceCraft.EnvironmentDayNightCycle");
        if (cycleType == null)
        {
            Plugin.Instance.Log.LogWarning("EnvironmentDayNightCycle type is not available yet.");
            return;
        }

        var cycle = ReflectionUtil.FindUnityObject(cycleType);
        if (cycle == null) return;
        _cycle = cycle;

        _fullDayStayMember = ReflectionUtil.FindMember(cycle.GetType(), "fullDayStayTime");
        if (_fullDayStayMember != null)
        {
            if (!_originalFullDayStay.HasValue && ReflectionUtil.TryGetFloat(cycle, _fullDayStayMember, out var old))
                _originalFullDayStay = old;
            ReflectionUtil.TrySetFloat(cycle, _fullDayStayMember, 1_000_000_000f);
        }

        var lerpMember = ReflectionUtil.FindMember(cycle.GetType(), "_dayNightLerpValue")
                         ?? ReflectionUtil.FindMemberContains(cycle.GetType(), "dayNightLerp");
        if (lerpMember != null)
        {
            _lerpNv = ReflectionUtil.GetMemberValue(cycle, lerpMember);
            if (_lerpNv != null)
                _lerpValueProperty = _lerpNv.GetType().GetProperty("Value", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
        }

        AcquireSun();

        if (_lerpNv == null || _lerpValueProperty == null)
        {
            Plugin.Instance.Log.LogError("Celestial Cycle core found the day/night manager but could not access _dayNightLerpValue.Value. Send LogOutput.log so this Game Pass wrapper can be mapped.");
            return;
        }

        if (!_loggedReady)
        {
            _loggedReady = true;
            Plugin.Instance.Log.LogMessage("CELESTIAL CORE HOOK READY: day/night network value acquired.");
        }
    }

    private void AcquireSun()
    {
        if (_sun != null) return;
        var updaterType = ReflectionUtil.FindType("SpaceCraft.EnvironmentUpdater");
        if (updaterType == null) return;
        var updater = ReflectionUtil.FindUnityObject(updaterType);
        if (updater == null) return;
        var member = ReflectionUtil.FindMember(updater.GetType(), "mainLight");
        var value = member == null ? null : ReflectionUtil.GetMemberValue(updater, member);
        _sun = value as Light;
        if (_sun != null && !_sunCaptured)
        {
            _sunCaptured = true;
            _sunOriginalRotation = _sun.transform.rotation;
            Plugin.Instance.Log.LogInfo("[Sun] mainLight acquired.");
        }
    }

    private void AdvancePhase()
    {
        var minutes = Mathf.Max(0.01f, Plugin.MinutesPerDay.Value);
        _phase = Mathf.Repeat(_phase + Time.deltaTime / (minutes * 60f), 1f);
    }

    private float NightLerp(float phase)
    {
        var dayHold = Mathf.Clamp(Plugin.DayHoldFraction.Value, 0f, 0.9f);
        var nightHold = Mathf.Clamp(Plugin.NightHoldFraction.Value, 0f, 0.9f);
        var total = dayHold + nightHold;
        if (total > 0.95f)
        {
            var k = 0.95f / total;
            dayHold *= k;
            nightHold *= k;
        }

        var d = Mathf.Min(phase, 1f - phase);
        var nightHalf = nightHold * 0.5f;
        var daylightBegins = 0.5f - dayHold * 0.5f;
        if (d <= nightHalf) return 1f;
        if (d >= daylightBegins) return 0f;
        var t = Mathf.InverseLerp(nightHalf, daylightBegins, d);
        return 1f - Mathf.SmoothStep(0f, 1f, t);
    }

    private void DriveLerp()
    {
        if (_cycle == null || _lerpNv == null || _lerpValueProperty == null) return;

        var isServerMember = ReflectionUtil.FindMember(_cycle.GetType(), "IsServer");
        if (isServerMember != null)
        {
            var server = ReflectionUtil.GetMemberValue(_cycle, isServerMember);
            if (server != null && !ReflectionUtil.AsBool(server, true)) return;
        }

        var value = NightLerp(_phase) * 100f;
        if (!float.IsNaN(_lastWritten) && Mathf.Abs(value - _lastWritten) < 0.01f) return;
        try
        {
            _lerpValueProperty.SetValue(_lerpNv, value);
            _lastWritten = value;
        }
        catch (Exception ex)
        {
            Plugin.Instance.Log.LogWarning("Failed writing day/night value: " + ReflectionUtil.Root(ex).Message);
            _lerpNv = null;
            _lerpValueProperty = null;
        }
    }

    private void DriveSun()
    {
        if (!Plugin.MoveSun.Value) return;
        if (_sun == null) { AcquireSun(); if (_sun == null) return; }
        var tilt = Quaternion.AngleAxis(Plugin.AxialTilt.Value, Vector3.forward);
        var yaw = Quaternion.AngleAxis(Plugin.SkyYaw.Value, Vector3.up);
        var axis = (yaw * (tilt * Vector3.right)).normalized;
        var daily = Quaternion.AngleAxis(_phase * 360f, axis);
        _sun.transform.forward = daily * Vector3.up;
    }

    private void LoadPhaseOnce()
    {
        if (_phaseLoaded) return;
        _phaseLoaded = true;
        try
        {
            if (File.Exists(PhaseFile) && float.TryParse(File.ReadAllText(PhaseFile).Trim(), NumberStyles.Float, CultureInfo.InvariantCulture, out var p))
            {
                _phase = Mathf.Repeat(p, 1f);
                return;
            }
        }
        catch (Exception ex)
        {
            Plugin.Instance.Log.LogWarning("Could not read saved clock: " + ex.Message);
        }
        _phase = Mathf.Repeat(Plugin.StartPhase.Value, 1f);
    }

    private void PersistPhase()
    {
        _saveTimer += Time.deltaTime;
        if (_saveTimer < 5f) return;
        _saveTimer = 0f;
        try { File.WriteAllText(PhaseFile, _phase.ToString("R", CultureInfo.InvariantCulture)); }
        catch { }
    }

    private void RestoreVanilla()
    {
        if (_sun != null && _sunCaptured) _sun.transform.rotation = _sunOriginalRotation;
        if (_cycle != null && _fullDayStayMember != null && _originalFullDayStay.HasValue)
            ReflectionUtil.TrySetFloat(_cycle, _fullDayStayMember, _originalFullDayStay.Value);
        _loggedReady = false;
    }

    private static string FormatClock(float phase)
    {
        var hours = phase * 24f;
        var hour = Mathf.FloorToInt(hours) % 24;
        var minute = Mathf.FloorToInt((hours - Mathf.Floor(hours)) * 60f) % 60;
        if (Plugin.Clock24Hour.Value) return $"{hour:00}:{minute:00}";
        var suffix = hour >= 12 ? "PM" : "AM";
        var h12 = hour % 12;
        if (h12 == 0) h12 = 12;
        return $"{h12}:{minute:00} {suffix}";
    }

    private void BuildClockStyle()
    {
        _clockBg = new Texture2D(1, 1);
        _clockBg.SetPixel(0, 0, new Color(0f, 0f, 0f, 0.55f));
        _clockBg.Apply();

        _clockStyle = new GUIStyle
        {
            alignment = TextAnchor.MiddleCenter,
            fontSize = Mathf.RoundToInt(Plugin.ClockFontSize.Value),
            fontStyle = FontStyle.Bold,
            clipping = TextClipping.Overflow,
            wordWrap = false
        };
        _clockStyle.normal.textColor = Color.white;
        _clockShadow = new GUIStyle(_clockStyle);
        _clockShadow.normal.textColor = new Color(0f, 0f, 0f, 0.9f);
    }
}

internal static class ReflectionUtil
{
    private const BindingFlags All = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static;

    internal static Type? FindType(string fullName)
    {
        foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
        {
            try { var t = asm.GetType(fullName, false); if (t != null) return t; }
            catch { }
        }
        return null;
    }

    internal static object? FindUnityObject(Type type)
    {
        try
        {
            var method = typeof(Resources).GetMethods(BindingFlags.Public | BindingFlags.Static)
                .FirstOrDefault(m => m.Name == "FindObjectsOfTypeAll" && !m.IsGenericMethod && m.GetParameters().Length == 1 && m.GetParameters()[0].ParameterType == typeof(Type));
            var result = method?.Invoke(null, new object[] { type });
            foreach (var item in Enumerate(result)) if (item != null) return item;
        }
        catch (Exception ex)
        {
            Plugin.Instance.Log.LogWarning("Unity object search failed for " + type.FullName + ": " + Root(ex).Message);
        }
        return null;
    }

    internal static MemberInfo? FindMember(Type t, string name)
    {
        return (MemberInfo?)t.GetField(name, All) ?? t.GetProperty(name, All);
    }

    internal static MemberInfo? FindMemberContains(Type t, string fragment)
    {
        return t.GetFields(All).Cast<MemberInfo>().Concat(t.GetProperties(All)).FirstOrDefault(m => m.Name.IndexOf(fragment, StringComparison.OrdinalIgnoreCase) >= 0);
    }

    internal static object? GetMemberValue(object obj, MemberInfo member)
    {
        try
        {
            return member switch
            {
                FieldInfo f => f.GetValue(obj),
                PropertyInfo p => p.GetValue(obj),
                _ => null
            };
        }
        catch { return null; }
    }

    internal static bool TryGetFloat(object obj, MemberInfo member, out float value)
    {
        value = 0f;
        var raw = GetMemberValue(obj, member);
        if (raw == null) return false;
        try { value = Convert.ToSingle(raw, CultureInfo.InvariantCulture); return true; } catch { return false; }
    }

    internal static bool TrySetFloat(object obj, MemberInfo member, float value)
    {
        try
        {
            if (member is FieldInfo f) f.SetValue(obj, value);
            else if (member is PropertyInfo p) p.SetValue(obj, value);
            else return false;
            return true;
        }
        catch { return false; }
    }

    internal static bool AsBool(object value, bool fallback)
    {
        try { return Convert.ToBoolean(value, CultureInfo.InvariantCulture); } catch { return fallback; }
    }

    internal static IEnumerable EnumerateRaw(object source)
    {
        if (source is IEnumerable e) return e;
        return Array.Empty<object>();
    }

    internal static System.Collections.Generic.IEnumerable<object?> Enumerate(object? source)
    {
        if (source == null) yield break;
        if (source is IEnumerable e)
        {
            foreach (var x in e) yield return x;
            yield break;
        }
        var lenMember = FindMember(source.GetType(), "Length") ?? FindMember(source.GetType(), "Count");
        var lenRaw = lenMember == null ? null : GetMemberValue(source, lenMember);
        var len = 0;
        try { if (lenRaw != null) len = Convert.ToInt32(lenRaw); } catch { }
        var indexer = source.GetType().GetProperties(All).FirstOrDefault(p => p.GetIndexParameters().Length == 1);
        if (indexer == null) yield break;
        for (var i = 0; i < len; i++)
        {
            object? x = null;
            try { x = indexer.GetValue(source, new object[] { i }); } catch { }
            yield return x;
        }
    }

    internal static Exception Root(Exception ex) => ex is TargetInvocationException tie && tie.InnerException != null ? tie.InnerException : ex;
}
