# Planet Crafter Game Pass - Legacy BepInEx 5 bridge test

Experimental bridge for BepInEx 6 IL2CPP build 6.0.0-be.785.

The bridge loads old BepInEx 5 Mono-style plugins from `BepInEx/legacy_plugins`, registers their BaseUnityPlugin classes into IL2CPP, and attaches them to a persistent Unity GameObject so normal Unity lifecycle methods (Awake/Update/etc.) can execute.

`MiscModEnabler.dll` is intentionally skipped because its only relevant current function is replacing `HideManagerGameObject=true`, which is already required in the working Game Pass configuration, and the original DLL references Steam/GOG-specific assemblies.
