#include "Game.h"
#include "Collision.h"

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
            // Fallout: X east, Y north, Z up. Minecraft yaw 0 looks +Z/south.
            const float heading = McYawToHeading(a_mcYawDeg);
            const float pitch = a_mcPitchDeg * kDegToRad;
            const float sh = std::sin(heading);
            const float ch = std::cos(heading);
            const float sp = std::sin(pitch);
            const float cp = std::cos(pitch);

            RE::NiPoint3 forward{ sh * cp, ch * cp, -sp };
            RE::NiPoint3 right{ ch, -sh, 0.0f };
            RE::NiPoint3 up{
                right.y * forward.z - right.z * forward.y,
                right.z * forward.x - right.x * forward.z,
                right.x * forward.y - right.y * forward.x
            };

            RE::NiMatrix3 m{};
            m.entry[0][0] = forward.x; m.entry[1][0] = forward.y; m.entry[2][0] = forward.z;
            m.entry[0][1] = up.x;      m.entry[1][1] = up.y;      m.entry[2][1] = up.z;
            m.entry[0][2] = right.x;   m.entry[1][2] = right.y;   m.entry[2][2] = right.z;
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

        void ApplyMinecraftCamera(RE::PlayerCharacter* a_player, const proto::McState& a_mc)
        {
            float yaw = a_mc.yaw;
            float pitch = a_mc.pitch;
            if (a_mc.cameraMode == 2) {
                yaw = std::fmod(yaw + 180.0f, 360.0f);
                pitch = -pitch;
            }

            const float heading = McYawToHeading(a_mc.yaw);
            a_player->data.angle.x = a_mc.pitch * kDegToRad;
            a_player->data.angle.z = heading;

            auto rot = CameraRotation(yaw, pitch);
            const auto pos = CameraPosition(a_mc);

            if (auto* camera = RE::Main::WorldRootCamera()) {
                camera->world.translate = pos;
                camera->world.rotate = rot;
                camera->local.translate = pos;
                camera->local.rotate = rot;
            }
            if (auto* playerCamera = RE::PlayerCamera::GetSingleton()) {
                playerCamera->heading = heading;
                if (playerCamera->cameraRoot) {
                    playerCamera->cameraRoot->world.translate = pos;
                    playerCamera->cameraRoot->world.rotate = rot;
                }
                if (a_mc.fovDeg > 1.0f) {
                    const float half = std::clamp(a_mc.fovDeg, 10.0f, 170.0f) * 0.5f * kDegToRad;
                    playerCamera->worldFOV = 2.0f * std::atan(std::tan(half) * (4.0f / 3.0f)) * kRadToDeg;
                }
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
            out.yaw = a_player ? HeadingToMcYaw(a_player->data.angle.z) : 0.0f;
            out.pitch = a_player ? a_player->data.angle.x * kRadToDeg : 0.0f;
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
            }

            st.mcInWorld = haveMc && ((g_mc.flags & proto::kMcInWorld) != 0);
            st.mcScreenOpen = haveMc && ((g_mc.flags & proto::kMcScreenOpen) != 0);
            st.falloutMenuOpen = Game::FalloutMenuOpen();
            st.mcGuiScale = haveMc ? static_cast<int>(g_mc.guiScale) : 0;
            st.mcCrosshair = haveMc && g_mc.cameraMode == 0 && !st.mcScreenOpen && !st.falloutMenuOpen;

            // Collision must stream before takeover. Minecraft deliberately withholds teleportAck
            // until the arrival regions are known.
            const bool acknowledged = haveMc && g_mc.teleportAck == g_teleportSeq;
            if (mcAlive && !loading) {
                // Until Minecraft acknowledges the current teleport, collision must be harvested
                // around Fallout's real player. Sampling stale MC coordinates here deadlocks the
                // arrival hold because the regions Minecraft is waiting for never arrive.
                const McVec collisionAt = (st.mcInWorld && acknowledged)
                    ? McVec{ g_mc.x, g_mc.y, g_mc.z }
                    : SkyToMc(a_player->GetPosition());
                Collision::Get().Update(collisionAt);
            }

            const bool puppet = haveMc && st.mcInWorld && acknowledged && !loading;
            st.minecraftOwnsPlayer = puppet;
            st.puppeting = puppet;

            if (puppet) {
                // Minecraft remains authoritative. The Fallout reference follows without warping
                // Fallout's character controller -- the safe behavior proven by the no-GDI tests.
                const auto p = McToSky(g_mc.x, g_mc.y, g_mc.z);
                a_player->SetPosition(p, false);
                ApplyMinecraftCamera(a_player, g_mc);

                st.feetX = g_mc.x;
                st.feetY = g_mc.y;
                st.feetZ = g_mc.z;
                st.feetValid = true;
            } else {
                st.feetValid = false;
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
            REL::Relocation<std::uintptr_t> vtbl{ RE::VTABLE_PlayerCharacter[0] };
            PlayerUpdateHook::func = vtbl.write_vfunc(0xAD, PlayerUpdateHook::thunk);
            logger::info("FalloutCraft: PlayerCharacter::Update hook installed at vfunc 0xAD");
        }

        void OnGameLoaded()
        {
            ++g_teleportSeq;
            ++g_epoch;
            g_forceTeleport = false;
            Collision::Get().Reset(g_epoch);
            logger::info("FalloutCraft: game load/new game resync requested");
        }

        bool FalloutMenuOpen()
        {
            // Fallout's own input still receives its native messages in this first full-port alpha.
            // MC screen ownership is handled independently through McState.
            return false;
        }

        void CheckRenderedCamera() {}
        void NoteRenderedCamera(const RE::NiPoint3&, const RE::NiMatrix3&) {}
        void NoteFrameStep(char) {}
    }
}
