# Binary recovery notes

## Native Fallout DLL

`FalloutCraft.dll` is a small x64 F4SE plugin exporting:

- `F4SEPlugin_Query`
- `F4SEPlugin_Load`
- `F4SEPlugin_Version`

The binary contains explicit v0.3.4 diagnostic strings for the per-frame interpolated `Actor::SetPosition` path and the temporary GDI overlay worker.

## Fabric JNI bridge

The Fabric JAR embeds `falloutcraft_native.dll`. Its exported JNI functions include host state getters, input-ring getters, QPC timing, overlay publication, shared-memory polling/status, and Minecraft-state publication.

## Fabric bytecode

The recovery ZIP contains `javap` output generated from the exact owner-supplied JAR and extracted text resources. These are loss-recovery aids and are not claimed to be the original source formatting.
