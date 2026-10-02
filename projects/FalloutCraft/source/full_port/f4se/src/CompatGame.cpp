#include "Game.h"
#include "Collision.h"
#include <RE/B/BSVisit.h>

namespace falloutcraft
{
    Runtime& State()
    {
        static Runtime state;
        return state;
    }


    namespace
    {
        constexpr float kDegToRad = 0.01745329251994329577f;
        constexpr float kRadToDeg = 57.295779513082320876f;

        proto::McState g_mc{};
        bool g_wasAlive = false;
        std::uint32_t g_lastMcPid = 0;
        std::uint32_t g_worldId = 0;
        std::uint32_t g_epoch = 1;
        std::uint32_t g_teleportSeq = 1;
        bool g_forceTeleport = true;

        RE::NiMatrix3 CameraRotation(float a_mcYawDeg, float a_mcPitchDeg)
        {
            // Fallout 4's NiMatrix3 is NOT Skyrim's packed camera basis. FO4 stores padded
            // ROWS and the camera-root convention is row0=right, row1=forward, row2=up.
            // v0.5.2 copied SkyCraft's column basis verbatim, cyclically permuting the axes;
            // that is the 90-degree "walking on an incline / world on its side" view.
            const float heading = McYawToHeading(a_mcYawDeg);
            const float pitch = a_mcPitchDeg * kDegToRad;
            const float sh = std::sin(heading);
            const float ch = std::cos(heading);
            const float sp = std::sin(pitch);
            const float cp = std::cos(pitch);

            const RE::NiPoint3 forward{ sh * cp, ch * cp, -sp };
            const RE::NiPoint3 right{ ch, -sh, 0.0f };
            const RE::NiPoint3 up{
                right.y * forward.z - right.z * forward.y,
                right.z * forward.x - right.x * forward.z,
                right.x * forward.y - right.y * forward.x
            };

            RE::NiMatrix3 m{};
            m.entry[0] = { right.x, right.y, right.z, 0.0f };
            m.entry[1] = { forward.x, forward.y, forward.z, 0.0f };
            m.entry[2] = { up.x, up.y, up.z, 0.0f };
            return m;
        }

        RE::NiPoint3 CameraPosition(const proto::McState& a_mc)
        {
            double x = a_mc.eyeX;
            double y = a_mc.eyeY;
            double z = a_mc.eyeZ;
            if (a_mc.cameraMode != 0 && a_mc.cameraDistance > 0.0f) {
                const double yaw = double(a_mc.yaw) * 0.01745329251994329577;
                const double pitch = double(a_mc.pitch) * 0.01745329251994329577;
                const double cp = std::cos(pitch);
                const double fx = -std::sin(yaw) * cp;
                const double fy = -std::sin(pitch);
                const double fz = std::cos(yaw) * cp;
                const double sign = a_mc.cameraMode == 2 ? 1.0 : -1.0;
                x += fx * double(a_mc.cameraDistance) * sign;
                y += fy * double(a_mc.cameraDistance) * sign;
                z += fz * double(a_mc.cameraDistance) * sign;
            }
            return McToSky(x, y, z);
        }

        RE::NiPoint3 g_cameraPos{};
        RE::NiMatrix3 g_cameraRot{};
        float g_cameraHeading = 0.0f;
        float g_cameraFov = 0.0f;
        std::atomic<bool> g_cameraActive{ false };
        std::atomic<bool> g_loggedPostCamera{ false };
        // Fallout can rebuild/re-show its first-person and player scene roots after our actor
        // update. Hide the actual roots (not only their current geometry children), remember each
        // object's original cull state, and reassert this after PlayerCamera::Update as well.
        struct HiddenRoot
        {
            RE::NiPointer<RE::NiAVObject> object;
            bool originallyCulled{ false };
        };
        std::vector<HiddenRoot> g_hiddenPlayerRoots;
        bool g_firstPersonHideActive = false;
        bool g_savedHideFirstPersonGeometry = false;

        void HideRoot(RE::NiAVObject* a_object)
        {
            if (!a_object) {
                return;
            }
            auto it = std::find_if(g_hiddenPlayerRoots.begin(), g_hiddenPlayerRoots.end(),
                [&](const HiddenRoot& a_entry) { return a_entry.object.get() == a_object; });
            if (it == g_hiddenPlayerRoots.end()) {
                HiddenRoot entry;
                entry.originallyCulled = a_object->GetAppCulled();
                entry.object.reset(a_object);
                g_hiddenPlayerRoots.push_back(std::move(entry));
            }
            if (!a_object->GetAppCulled()) {
                a_object->SetAppCulled(true);
            }
        }

        void SetFalloutFirstPersonHidden(RE::PlayerCharacter* a_player, bool a_hide)
        {
            if (!a_player) {
                return;
            }

            if (!a_hide) {
                for (auto& entry : g_hiddenPlayerRoots) {
                    if (entry.object && entry.object->GetAppCulled() != entry.originallyCulled) {
                        entry.object->SetAppCulled(entry.originallyCulled);
                    }
                }
                g_hiddenPlayerRoots.clear();
                if (g_firstPersonHideActive) {
                    a_player->hideFirstPersonGeometry = g_savedHideFirstPersonGeometry;
                    g_firstPersonHideActive = false;
                }
                return;
            }

            if (!g_firstPersonHideActive) {
                g_savedHideFirstPersonGeometry = a_player->hideFirstPersonGeometry;
                g_firstPersonHideActive = true;
            }
            a_player->hideFirstPersonGeometry = true;

            // firstPerson3D owns the normal weapon/hands. Fallout can also submit the torso
            // separately, and some camera states render loadedData->data3D even in a nominally
            // first-person view. Minecraft supplies both its own hand and its own F5 avatar, so
            // all three Fallout roots must stay out of the final frame during takeover.
            HideRoot(a_player->firstPerson3D.get());
            HideRoot(a_player->firstPersonTorso);
            if (a_player->loadedData && a_player->loadedData->data3D) {
                HideRoot(a_player->loadedData->data3D.get());
            }
        }

        void StageMinecraftCamera(RE::PlayerCharacter* a_player, const proto::McState& a_mc, float a_yaw, float a_pitch)
        {
            float cameraYaw = a_yaw;
            float cameraPitch = a_pitch;
            if (a_mc.cameraMode == 2) {
                cameraYaw = std::fmod(cameraYaw + 180.0f, 360.0f);
                cameraPitch = -cameraPitch;
            }

            g_cameraHeading = McYawToHeading(a_yaw);
            a_player->data.angle.x = a_pitch * kDegToRad;
            a_player->data.angle.z = g_cameraHeading;

            g_cameraRot = CameraRotation(cameraYaw, cameraPitch);

            // CameraPosition uses MC's actual eye and third-person distance, but its detached
            // camera offset must use the same host-authoritative look angle as the render root.
            proto::McState cameraState = a_mc;
            cameraState.yaw = a_yaw;
            cameraState.pitch = a_pitch;
            g_cameraPos = CameraPosition(cameraState);
            g_cameraFov = a_mc.fovDeg;
            g_cameraActive = true;
        }

        void ApplyStagedCamera(RE::PlayerCamera* a_camera)
        {
            if (!a_camera || !g_cameraActive.load() || !a_camera->cameraRoot) {
                return;
            }

            auto* root = a_camera->cameraRoot.get();

            // Drive the camera in WORLD space, but compute a matching LOCAL transform before
            // running Fallout's downward scene-graph update. v0.5.5 wrote the desired world
            // transform and then also wrote the same values into local space. If cameraRoot has
            // a transformed parent, UpdateDownwardPass composes that parent a second time and
            // partially fights Minecraft's pitch/position. That is especially visible near
            // straight up/down. Invert the parent transform so the update lands exactly on the
            // Minecraft camera instead.
            if (root->parent) {
                const auto& parentWorld = root->parent->world;
                const auto invParent = parentWorld.rotate.Transpose();
                const float parentScale = std::abs(parentWorld.scale) > 1e-6f ? parentWorld.scale : 1.0f;
                root->local.rotate = invParent * g_cameraRot;
                root->local.translate = invParent * ((g_cameraPos - parentWorld.translate) / parentScale);
            } else {
                root->local.translate = g_cameraPos;
                root->local.rotate = g_cameraRot;
            }
            root->world.translate = g_cameraPos;
            root->world.rotate = g_cameraRot;

            // These are Fallout-specific camera caches. Keeping them in lock-step with the
            // scene-graph anchor prevents Fallout's own smoothing/collision pass from pulling
            // the view back toward its previous frame.
            a_camera->bufferedCameraPos = g_cameraPos;
            a_camera->cameraPosBuffered = true;
            a_camera->heading = g_cameraHeading;

            if (g_cameraFov > 1.0f) {
                const float half = std::clamp(g_cameraFov, 10.0f, 170.0f) * 0.5f * kDegToRad;
                a_camera->worldFOV =
                    2.0f * std::atan(std::tan(half) * (4.0f / 3.0f)) * kRadToDeg;
            }

            // Push the corrected root down into Fallout's NiCamera child after Fallout has
            // completed its own PlayerCamera::Update for this frame.
            RE::NiUpdateData update{};
            root->UpdateDownwardPass(update, 0);

            // Fallout's camera update can re-enable first-person/weapon nodes. Reassert the
            // Minecraft takeover cull at the last camera hook before rendering.
            if (State().minecraftOwnsPlayer.load()) {
                SetFalloutFirstPersonHidden(RE::PlayerCharacter::GetSingleton(), true);
            }

            if (!g_loggedPostCamera.exchange(true)) {
                logger::info("FalloutCraft: Minecraft camera now applied after Fallout PlayerCamera::Update (FO4 row-major basis)");
            }
        }

        std::uint32_t CurrentWorldId(RE::PlayerCharacter* a_player)
        {
            auto* cell = a_player ? a_player->GetParentCell() : nullptr;
            if (!cell) {
                return 0;
            }
            if (cell->IsInterior()) {
                return cell->GetFormID();
            }
            if (a_player->cachedWorldspace) {
                return a_player->cachedWorldspace->GetFormID();
            }
            return cell->GetFormID();
        }

        void WriteHostState(RE::PlayerCharacter* a_player, bool a_loading)
        {
            auto& link = Link::Get();
            proto::SkyState out{};

            if (a_player && !a_loading) {
                out.flags |= proto::kSkyInGame;
            }
            if (a_loading) {
                out.flags |= proto::kSkyLoading;
            }
            if (Game::FalloutMenuOpen()) {
                out.flags |= proto::kSkyMenuOpen;
            }

            out.worldId = g_worldId;
            out.collisionEpoch = g_epoch;
            const auto pos = a_player ? SkyToMc(a_player->GetPosition()) : McVec{};
            out.posX = pos.x;
            out.posY = pos.y;
            out.posZ = pos.z;
            auto& st = State();
            out.yaw = a_player ? st.yaw : 0.0f;
            out.pitch = a_player ? st.pitch : 0.0f;
            out.teleportSeq = g_teleportSeq;

            if (auto* w = RE::BSGraphics::GetCurrentRendererWindow()) {
                out.viewportW = static_cast<std::uint32_t>(std::max(1, w->windowWidth));
                out.viewportH = static_cast<std::uint32_t>(std::max(1, w->windowHeight));
                State().viewportW = static_cast<int>(out.viewportW);
                State().viewportH = static_cast<int>(out.viewportH);
            } else {
                out.viewportW = static_cast<std::uint32_t>(State().viewportW.load());
                out.viewportH = static_cast<std::uint32_t>(State().viewportH.load());
            }
            out.gameHour = 12.0f;
            link.WriteSkyState(out);

            proto::WaterGrid water{};
            water.originX = static_cast<std::int32_t>(std::floor(pos.x)) - 8;
            water.originZ = static_cast<std::int32_t>(std::floor(pos.z)) - 8;
            water.worldId = g_worldId;
            std::fill(std::begin(water.surface), std::end(water.surface), proto::kNoWater);
            link.WriteWaterGrid(water);
        }

        void PerFrame(RE::PlayerCharacter* a_player, float a_delta)
        {
            if (!a_player) {
                return;
            }

            auto& link = Link::Get();
            auto& st = State();
            link.Heartbeat();

            // These install functions are idempotent and become active as soon as Fallout's
            // real window/swap chain exists.
            Input::Install();
            WorldRender::Install();

            const bool mcAlive = link.McAlive();
            const bool haveMc = mcAlive && link.ReadMcState(g_mc);
            const auto mcPid = link.McPid();

            if (mcAlive && (!g_wasAlive || (mcPid != 0 && mcPid != g_lastMcPid))) {
                logger::info("Minecraft connected to full-port host (pid {})", mcPid);
                g_lastMcPid = mcPid;
                ++g_epoch;
                ++g_teleportSeq;
                g_forceTeleport = false;
                st.lookInitialized = false;
                Collision::Get().Reset(g_epoch);
                link.ResetOverlay();
            }
            g_wasAlive = mcAlive;

            auto* cell = a_player->GetParentCell();
            const bool loading = cell == nullptr || !cell->IsAttached();
            const auto world = CurrentWorldId(a_player);
            if (world != 0 && world != g_worldId) {
                logger::info("Fallout world changed {:08X} -> {:08X}", g_worldId, world);
                g_worldId = world;
                ++g_epoch;
                ++g_teleportSeq;
                Collision::Get().Reset(g_epoch);
                g_forceTeleport = false;
                st.lookInitialized = false;
            }

            st.mcInWorld = haveMc && ((g_mc.flags & proto::kMcInWorld) != 0);
            const bool screenOpen = haveMc && ((g_mc.flags & proto::kMcScreenOpen) != 0);
            if (screenOpen && !st.mcScreenOpen.load()) {
                st.cursorX = std::max(1, st.viewportW.load()) / 2;
                st.cursorY = std::max(1, st.viewportH.load()) / 2;
            }
            st.mcScreenOpen = screenOpen;
            const bool falloutMenu = Game::FalloutMenuOpen();
            if (falloutMenu && !st.falloutMenuOpen.load()) {
                Input::ReleaseAll();
            }
            st.falloutMenuOpen = falloutMenu;
            if (haveMc && g_mc.sensitivity > 0.0f) {
                st.sensitivity = g_mc.sensitivity;
            }
            st.mcGuiScale = haveMc ? static_cast<int>(g_mc.guiScale) : 0;
            st.mcCrosshair = haveMc && g_mc.cameraMode == 0 && !st.mcScreenOpen && !st.falloutMenuOpen;

            // Preserve SkyCraft's proven input ownership model: Fallout consumes the raw mouse
            // event, applies Minecraft's exact sensitivity curve here, then publishes one stable
            // yaw/pitch to both engines. Letting the hidden Minecraft window independently
            // integrate mouse deltas caused the v0.5.3 snap/jitter feedback loop.
            float lookDx = 0.0f;
            float lookDy = 0.0f;
            Input::ConsumeLook(lookDx, lookDy);
            if (!st.lookInitialized) {
                st.yaw = HeadingToMcYaw(a_player->data.angle.z);
                st.pitch = a_player->data.angle.x * kRadToDeg;
                st.lookInitialized = true;
            }
            if (!st.mcScreenOpen.load() && !st.falloutMenuOpen.load()) {
                const float s = st.sensitivity * 0.6f + 0.2f;
                const float factor = s * s * s * 8.0f * 0.15f;
                st.yaw = std::fmod(st.yaw + lookDx * factor, 360.0f);
                st.pitch = std::clamp(st.pitch + lookDy * factor, -90.0f, 90.0f);
            }

            // Collision must stream before takeover. Minecraft deliberately withholds teleportAck
            // until the arrival regions are known.
            const bool acknowledged = haveMc && g_mc.teleportAck == g_teleportSeq;
            if (haveMc && st.mcInWorld && !loading) {
                // Do not touch Fallout's physics merely because the shared-memory heartbeat exists.
                // Wait until Minecraft has an actual LocalPlayer in the mirror world and is publishing
                // kMcInWorld. Before teleport acknowledgement, harvest around Fallout's real arrival
                // point so the collision regions Minecraft is waiting for can arrive.
                const McVec collisionAt = acknowledged
                    ? McVec{ g_mc.x, g_mc.y, g_mc.z }
                    : SkyToMc(a_player->GetPosition());
                Collision::Get().Update(collisionAt);
            }

            const bool arriving = haveMc && st.mcInWorld && !acknowledged && !loading;
            const bool puppet = haveMc && st.mcInWorld && acknowledged && !loading;
            // Route input to Minecraft during the collision/teleport arrival hold too, matching
            // SkyCraft. The hold may temporarily pin position, but Fallout must not steal keys.
            st.minecraftOwnsPlayer = puppet || arriving;
            st.puppeting = puppet;
            SetFalloutFirstPersonHidden(a_player, st.minecraftOwnsPlayer.load());

            static int lastCameraMode = -1;
            if (haveMc && static_cast<int>(g_mc.cameraMode) != lastCameraMode) {
                lastCameraMode = static_cast<int>(g_mc.cameraMode);
                logger::info("FalloutCraft: Minecraft camera mode {}{}", lastCameraMode,
                    lastCameraMode == 0 ? " (first person)" : lastCameraMode == 1 ? " (third person back)" : " (third person front)");
            }

            if (puppet) {
                // Minecraft remains authoritative. The Fallout reference follows without warping
                // Fallout's character controller -- the safe behavior proven by the no-GDI tests.
                const auto p = McToSky(g_mc.x, g_mc.y, g_mc.z);
                a_player->SetPosition(p, false);
                StageMinecraftCamera(a_player, g_mc, st.yaw, st.pitch);

                st.feetX = g_mc.x;
                st.feetY = g_mc.y;
                st.feetZ = g_mc.z;
                st.feetValid = true;
            } else {
                st.feetValid = false;
                g_cameraActive = false;
            }

            Combat::PerFrame(a_player, puppet, a_delta);
            McVec lightPos{ g_mc.x, g_mc.y, g_mc.z };
            BlockLights::Update(puppet ? &lightPos : nullptr, a_delta);
            if (puppet) {
                NpcBlocks::PushActorsOut(a_player, a_delta);
            }

            WriteHostState(a_player, loading);
        }

        struct PlayerUpdateHook
        {
            static void thunk(RE::Actor* a_this, float a_delta)
            {
                func(a_this, a_delta);
                auto* player = RE::PlayerCharacter::GetSingleton();
                if (player && a_this == player) {
                    PerFrame(player, a_delta);
                }
            }
            static inline REL::Relocation<decltype(thunk)> func;
        };

        // Fallout 4 TESCamera has Update at vfunc 0x03. Applying the Minecraft camera
        // only from Actor::Update is too early: Fallout's camera update subsequently overwrites
        // part of the transform. Re-pin it after the real camera update, like SkyCraft does.
        struct PlayerCameraUpdateHook
        {
            static void thunk(RE::TESCamera* a_this)
            {
                func(a_this);
                auto* playerCamera = RE::PlayerCamera::GetSingleton();
                if (playerCamera && a_this == static_cast<RE::TESCamera*>(playerCamera)) {
                    ApplyStagedCamera(playerCamera);
                }
            }
            static inline REL::Relocation<decltype(thunk)> func;
        };

        std::atomic<bool> g_installed{ false };
    }

    namespace Game
    {
        void Install()
        {
            bool expected = false;
            if (!g_installed.compare_exchange_strong(expected, true)) {
                return;
            }
            REL::Relocation<std::uintptr_t> vtbl{ RE::PlayerCharacter::VTABLE[0] };
            // Fallout 4 Actor::Update(float) is vfunc 0xCF. 0xAD is TESObjectREFR::ApplyMovementDelta
            // and has a completely different signature; hooking it as Update corrupts the call frame
            // and was the immediate v0.5.0/v0.5.1 post-link crash.
            PlayerUpdateHook::func = vtbl.write_vfunc(0xCF, PlayerUpdateHook::thunk);
            logger::info("FalloutCraft: PlayerCharacter::Update hook installed at Fallout vfunc 0xCF");

            REL::Relocation<std::uintptr_t> cameraVtbl{ RE::PlayerCamera::VTABLE[0] };
            PlayerCameraUpdateHook::func = cameraVtbl.write_vfunc(0x03, PlayerCameraUpdateHook::thunk);
            logger::info("FalloutCraft: PlayerCamera::Update post-hook installed at Fallout vfunc 0x03");
        }

        void OnGameLoaded()
        {
            ++g_teleportSeq;
            ++g_epoch;
            g_forceTeleport = false;
            g_cameraActive = false;
            SetFalloutFirstPersonHidden(RE::PlayerCharacter::GetSingleton(), false);
            State().lookInitialized = false;
            Collision::Get().Reset(g_epoch);
            logger::info("FalloutCraft: game load/new game resync requested");
        }

        bool FalloutMenuOpen()
        {
            auto* ui = RE::UI::GetSingleton();
            if (!ui) {
                return false;
            }
            for (const auto& menu : ui->menuStack) {
                if (!menu || !menu->OnStack()) {
                    continue;
                }
                if (menu->menuFlags.any(RE::UI_MENU_FLAGS::kPausesGame, RE::UI_MENU_FLAGS::kUsesCursor)) {
                    return true;
                }
            }
            return false;
        }

        void CheckRenderedCamera() {}
        void NoteRenderedCamera(const RE::NiPoint3&, const RE::NiMatrix3&) {}
        void NoteFrameStep(char) {}
    }
}
