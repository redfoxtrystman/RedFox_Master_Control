# MinecraftSubnautica native compositor

This host-side visual path is derived directly from Universal Modder's working
examples/minecraft-gta5-passthrough implementation.

It uses ReShade 6.8.0's full add-on build and the normal D3D11 dxgi.dll route.

## Install

Run PowerShell:

~~~powershell
.\Install-MinecraftSubnauticaCompositor.ps1 -GameDir "C:\path\to\Subnautica"
~~~

If ReShade is not installed, the script downloads and opens the official ReShade 6.8.0 Add-on
installer. Select Subnautica.exe and DirectX 10/11/12. Run the script again after that installer
finishes if necessary.

The script installs:

- MinecraftSubnautica.addon64 beside Subnautica.exe
- reshade-shaders\Shaders\MinecraftSubnautica.fx
- ReShade.fxh
- MinecraftSubnauticaPreset.ini

It does not silently replace an existing ReShade runtime or an existing ReShade.ini.

## Runtime architecture

Minecraft publishes three layers through Local\SkyCraft_Subnautica_Frame_v1:

1. world colour RGBA8
2. world depth float32
3. hand/HUD/GUI overlay RGBA8

Subnautica's BepInEx plugin publishes MainCamera.camera through
Local\SkyCraft_Subnautica_Camera_v1.

The ReShade add-on uploads the Minecraft layers and uses the same camera reprojection and host-depth
comparison architecture as Universal Modder's proven Minecraft/GTA passthrough. HUD/hand is composed
last in screen space.

## Provenance

Ported from rehan-remade/universal-modder commit
8607693be42ce02442251f05e0495f58c2b77e5d, especially:

- examples/minecraft-gta5-passthrough/mc/.../FrameExporter.java
- GameRendererMixin.java
- GlCommandEncoderMixin.java
- CameraMixin.java
- gta/src/compositor.cpp
- gta/shaders/MCPassthrough.fx

ReShade API target is pinned to 6.8.0, matching that source.
