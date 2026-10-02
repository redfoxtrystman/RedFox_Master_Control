FalloutCraft v0.5.7 FULL-PORT ALPHA
==================================

This is the guarded follow-up to the first whole-system Fallout 4 port of the SkyCraft architecture.

Install:
  Data/F4SE/Plugins/FalloutCraft.dll -> Fallout 4
  mods/FalloutCraft-fabric-0.1.0.jar -> the Minecraft 26.3 Fabric instance

IMPORTANT:
- Remove/replace older FalloutCraft.dll and older FalloutCraft Fabric jars.
- Launch Fallout 4 through F4SE exactly as before.
- The old GDI/layered-window overlay is permanently removed.

0.5.7 input/collision/HUD/lighting pass:
- Restores the Fallout HWND as the single authoritative keyboard/mouse-button source while Minecraft owns the player. WM_KEYDOWN/UP, mouse buttons, wheel and WM_CHAR now reach Minecraft even though Fallout gameplay/menu receivers are suppressed. This restores Escape, E/inventory, F5, held movement, block breaking and block placing without Fallout also reacting to the same input.
- Adds a MenuControls vtable suppression hook alongside PlayerControls, matching SkyCraft's ownership model: Minecraft receives the raw Windows input while Fallout's gameplay/menu handlers do not double-consume it during takeover.
- Replaces the temporary whole-block Fallout collision samples with SkyCraft-style 8x8x8 sub-voxel ColBlock masks. Floor and ceiling ray hits become thin horizontal slices; wall/door/railing hits become 1/8-block vertical slabs. The fallback whole-cube floor remains only for a faulted hknp ray path.
- Samples nearby Fallout collision every 100 ms with denser floor/ceiling grids and a 48-ray, three-height wall fan. Contact boxes are rebuilt from the same sub-voxel masks using SkyCraft's packed min/max convention.
- Culls Fallout's actual firstPerson3D root, separate first-person torso and loaded player data3D root while Minecraft owns the camera, and reasserts the cull after Fallout PlayerCamera::Update so Fallout cannot re-show its hands/weapon before rendering.
- Moves BottomCenterGroup_mc.CompassWidget_mc upward by 48 HUD stage pixels while the Minecraft HUD is active, preserving and restoring the user's original compass Y position.
- Applies Fallout's live six-direction directional ambient cube to Minecraft world vertices using the face-normal flags exported by Minecraft, while retaining Minecraft block emission. Blocks now react to the Fallout interior/weather/time-of-day environment instead of rendering fullbright.
- Locks the detected standard/reversed depth convention after the first valid camera comparison so post-scene block depth ordering cannot alternate between frames.

0.5.6 runtime-correction pass:
- Fixes the native keyboard bridge at the source: Fallout ButtonEvent IDs are DirectInput scan codes, not Win32 virtual keys. The bridge now uses the proven SkyCraft DIK -> SDL/HID table, so E, F5, movement keys, function keys and modifiers map to the Minecraft keys they actually represent.
- Native keyboard and mouse buttons now forward only QJustPressed/QReleased edges. Fallout held events are consumed without being replayed as repeated Minecraft presses/clicks.
- Keeps raw WM_INPUT as the only look-delta source, so pitch is not limited by a Fallout cursor edge and Minecraft remains the single yaw/pitch authority.
- Applies the Minecraft camera root through the inverse of any Fallout parent transform before the scene-graph update. This prevents Fallout from composing a parent transform on top of Minecraft's requested camera and restores the intended full Minecraft vertical pitch, including near straight up/down.
- Stops coarse Fallout ray hits at player body/ceiling height from becoming full Minecraft collision cubes. Until exact hknp triangles are available, the player only receives conservative support cells at/below the feet, preventing fake walls from pinning movement.
- Replaces absolute-world block projection with SkyCraft's camera-relative rebased world-to-clip multiply, preserving float precision near the camera and rejecting triangles wholly behind it. This specifically targets the giant/flattened block faces visible in the v0.5.5 test.
- Hides Fallout's actual PlayerCharacter::firstPerson3D geometry meshes (plus the separate torso when present) and restores only geometry FalloutCraft itself hid. The old Get3D(true) root path did not reliably point at Fallout's first-person hands/weapon.
- F5 still uses Minecraft's own camera mode/state; with the corrected DIK mapping a physical F5 press now reaches Minecraft once and the host follows first-person / third-person-back / third-person-front from Minecraft's published camera mode.

0.5.5 movement/input/viewmodel/block-projection pass:
- Filters Fallout's held key/button events into true press/release edges before sending them to Minecraft. This stops E, F5, mouse buttons and other base Minecraft controls from firing multiple times per physical press.
- Uses WM_INPUT raw relative mouse movement as the single host look source while the native Fallout input handler only consumes Fallout's duplicate mouse event. This removes cursor-bounded vertical look and preserves Minecraft's full pitch range.
- Stops the temporary Fallout hknp sampler from advertising conservative whole-block samples as exact collision triangles. Minecraft now uses its vanilla voxel collision solver until real hknp triangles exist, preventing the smooth collider from pinning the player in place.
- Reduces the arrival collision hold fail-open to 2.5 seconds so missing early collision data cannot leave movement frozen.
- Hides Fallout's first-person scene root while Minecraft owns the player, removing Fallout hands/weapons from behind Minecraft's HUD and hand.
- Keeps F5 as a normal one-shot Minecraft key and logs camera-mode changes on the host; the existing host camera follows Minecraft first/third/front modes.
- Replaces the temporary renderer's CPU screen-space projection (w=1, z=.5) with Fallout's true homogeneous clip coordinates so block textures interpolate perspectively and near-plane clipping works correctly.
- Adds a per-frame Minecraft depth buffer to the compatibility renderer so Minecraft blocks occlude their own far faces instead of drawing in arbitrary triangle order.

0.5.4 input/look/cursor pass:
- Restores SkyCraft's proven single look authority: Fallout consumes raw mouse deltas, applies Minecraft's sensitivity curve once, then publishes stable yaw/pitch back to Minecraft. This removes the v0.5.3 double-integration snap/jitter loop.
- Routes Fallout 4 input through a native BSInputEventUser inserted first in MenuControls, marking Minecraft-owned events handled so Fallout does not also open menus or move its own player.
- Restores host-driven Minecraft yaw/pitch every frame so WASD movement direction, ray picking and the Fallout camera all use the same look state.
- Adds the missing virtual Minecraft cursor to the Fallout D3D11 compositor for inventory/crafting/chest screens.
- Adds a hard timeout to the arrival hold so a missing early Fallout collision region cannot freeze Minecraft movement forever.
- Rejects behind-camera and extreme projected block vertices to stop near-plane triangles from exploding across the screen while the temporary post-scene block renderer is still in use.

0.5.3 camera/collision pass:
- Corrects Fallout 4's padded row-major camera basis (row0=right, row1=forward, row2=up). The previous Skyrim-style column basis is what rotated/tilted the world.
- Adds a Fallout PlayerCamera::Update post-hook at vfunc 0x03 so Minecraft's camera is applied after Fallout's own camera smoothing/collision pass instead of being overwritten later in the frame.
- Sends raw relative mouse deltas to Minecraft; removes the first-frame fake 960x540 camera kick.
- Replaces the failing CommonLibF4 bhkPickData result wrappers with Fallout 1.11.x verified Address Library raycast entry points and collision-filter offset.
- Anchors the emergency collision floor at the arrival height so it cannot fall downward with the player.

0.5.2 crash fix:
- Corrected the Fallout player update hook: Actor::Update is vfunc 0xCF. The previous full-port alpha incorrectly hooked TESObjectREFR::ApplyMovementDelta at 0xAD with the wrong function signature, which could corrupt movement calls and run bridge work on the wrong engine path.
- Fallout collision sampling now waits until Minecraft has a real player in the mirror world instead of firing as soon as the heartbeat appears.
- The entire bhkPickData constructor/setup/Pick/result/destructor sequence is guarded, and the hknp world is read-locked during queries.

0.5.1 crash fix:\r\n- Guards Fallout hknp Pick() calls with SEH, sets the required LOS query filter, and drastically lowers the per-frame ray budget.\r\n- If a live Fallout physics pick faults, collision rays disable for the session and a small support plane keeps the rest of the bridge testable instead of crashing Fallout.\r\n\r\nSystems present in this alpha:
- Minecraft-authoritative movement and camera state
- Fallout->Minecraft keyboard/mouse bridge
- Fallout collision stream -> Minecraft collision queries
- exact-triangle + voxel collision protocol
- Minecraft HUD/hand composited through Fallout's D3D11 Present
- Minecraft block/section render stream
- Minecraft entity/particle/item scene stream
- real Minecraft F5 avatar stream (skin/armor/held items/pose)
- texture atlas + animated atlas updates
- block placing/breaking/export protocol
- block light/hazard stream
- NPC-solid stream
- water/combat/digging/ragdoll protocols retained from the full SkyCraft port
- shared-memory heartbeat, teleport handoff and frame pacing architecture

Known first-alpha compromises:
- Fallout 4 uses hknp rather than Skyrim's hkp physics. The first Fallout-native collision
  producer samples Fallout's real cell physics with bhkPickData rays and publishes conservative
  full-block collision plus cube triangles. It is intentionally rough before the full hknp body
  harvester is validated.
- World-space Minecraft geometry is initially drawn in Fallout's final D3D11 frame. It does not
  yet use Fallout's scene depth, so some occlusion/post-processing will be wrong.
- Fallout-native combat/NPC pathing/light-spawn glue is in compatibility mode while the complete
  imported SkyCraft implementations remain in source for Fallout-specific API adaptation.

This is deliberately a full-system alpha: test the whole thing first, then fix behavior/runtime
bugs against actual Fallout 4 rather than continuing the old half-finished binary bridge.
