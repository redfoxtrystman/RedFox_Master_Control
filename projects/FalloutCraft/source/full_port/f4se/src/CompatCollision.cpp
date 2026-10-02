#include "Collision.h"

namespace falloutcraft
{
    namespace
    {
        constexpr std::uint64_t kCoordMask = (1ull << 21) - 1;
        constexpr std::uint64_t kSignBit = 1ull << 20;

        std::uint64_t Pack(int x, int y, int z)
        {
            return (std::uint64_t(std::uint32_t(x)) & kCoordMask) |
                   ((std::uint64_t(std::uint32_t(y)) & kCoordMask) << 21) |
                   ((std::uint64_t(std::uint32_t(z)) & kCoordMask) << 42);
        }

        int UnpackPart(std::uint64_t v)
        {
            v &= kCoordMask;
            if (v & kSignBit) {
                v |= ~kCoordMask;
            }
            return static_cast<int>(static_cast<std::int64_t>(v));
        }

        void Unpack(std::uint64_t key, int& x, int& y, int& z)
        {
            x = UnpackPart(key);
            y = UnpackPart(key >> 21);
            z = UnpackPart(key >> 42);
        }

        int FloorDiv8(int v)
        {
            return v >= 0 ? v / 8 : -(((-v) + 7) / 8);
        }

        void PushTri(std::vector<proto::ColTri>& out,
            float ax, float ay, float az,
            float bx, float by, float bz,
            float cx, float cy, float cz)
        {
            proto::ColTri t{};
            const float v[9]{ ax, ay, az, bx, by, bz, cx, cy, cz };
            std::copy(std::begin(v), std::end(v), std::begin(t.v));
            t.flags = 0;
            out.push_back(t);
        }

        void CubeTriangles(int x, int y, int z, std::vector<proto::ColTri>& out)
        {
            const float x0 = static_cast<float>(x), x1 = x0 + 1.0f;
            const float y0 = static_cast<float>(y), y1 = y0 + 1.0f;
            const float z0 = static_cast<float>(z), z1 = z0 + 1.0f;

            // -X
            PushTri(out, x0,y0,z0, x0,y0,z1, x0,y1,z1);
            PushTri(out, x0,y0,z0, x0,y1,z1, x0,y1,z0);
            // +X
            PushTri(out, x1,y0,z0, x1,y1,z0, x1,y1,z1);
            PushTri(out, x1,y0,z0, x1,y1,z1, x1,y0,z1);
            // -Y
            PushTri(out, x0,y0,z0, x1,y0,z0, x1,y0,z1);
            PushTri(out, x0,y0,z0, x1,y0,z1, x0,y0,z1);
            // +Y
            PushTri(out, x0,y1,z0, x0,y1,z1, x1,y1,z1);
            PushTri(out, x0,y1,z0, x1,y1,z1, x1,y1,z0);
            // -Z
            PushTri(out, x0,y0,z0, x0,y1,z0, x1,y1,z0);
            PushTri(out, x0,y0,z0, x1,y1,z0, x1,y0,z0);
            // +Z
            PushTri(out, x0,y0,z1, x1,y0,z1, x1,y1,z1);
            PushTri(out, x0,y0,z1, x1,y1,z1, x0,y1,z1);
        }

        std::uint64_t RegionKey(int rx, int ry, int rz)
        {
            return Pack(rx, ry, rz);
        }
    }

    namespace
    {
        enum class GuardedPickResult : int
        {
            kMiss = 0,
            kHit = 1,
            kCtorFault = -1,
            kSetupFault = -2,
            kPickFault = -3,
            kResultFault = -4,
        };

        // Fallout 4 1.11.x verified bhkPickData shim. The CommonLibF4 wrappers for
        // HasHit/GetHitFraction are not reliable on the user's 1.11.240 runtime: v0.5.2
        // proved TESObjectCELL::Pick returned, then faulted only when those result helpers ran.
        // These Address Library IDs/offsets match the current Fallout hknp layout used by
        // working FO4 raycast plugins.
        struct alignas(16) VerifiedPickStorage
        {
            std::byte data[0xE0]{};
        };

        GuardedPickResult SafeFullPick(
            RE::TESObjectCELL* a_cell,
            const RE::NiPoint3* a_from,
            const RE::NiPoint3* a_to,
            float* a_fraction)
        {
            if (!a_cell || !a_from || !a_to || !a_fraction) {
                return GuardedPickResult::kSetupFault;
            }

            using CtorFn = void* (*)(void*);
            using SetStartEndFn = void (*)(void*, const RE::NiPoint3&, const RE::NiPoint3&);
            using HasHitFn = bool (*)(void*);
            using GetFractionFn = float (*)(void*);
            using CellPickFn = RE::NiAVObject* (*)(RE::TESObjectCELL*, void*);

            static REL::Relocation<CtorFn> ctor{ REL::ID(526783) };
            static REL::Relocation<SetStartEndFn> setStartEnd{ REL::ID(747470) };
            static REL::Relocation<HasHitFn> hasHit{ REL::ID(1181584) };
            static REL::Relocation<GetFractionFn> getFraction{ REL::ID(476687) };
            static REL::Relocation<CellPickFn> cellPick{ REL::ID(434717) };

            VerifiedPickStorage storage{};
            void* pick = storage.data;
            GuardedPickResult stage = GuardedPickResult::kCtorFault;
            bool hit = false;
            float fraction = 0.0f;

#if defined(_MSC_VER)
            __try {
                ctor(pick);

                stage = GuardedPickResult::kSetupFault;
                // castQuery.m_filterData.m_collisionFilterInfo is +0x0C.
                *reinterpret_cast<std::uint32_t*>(
                    reinterpret_cast<std::byte*>(pick) + 0x0C) =
                    static_cast<std::uint32_t>(RE::COL_LAYER::kLOS);
                setStartEnd(pick, *a_from, *a_to);

                stage = GuardedPickResult::kPickFault;
                (void)cellPick(a_cell, pick);

                stage = GuardedPickResult::kResultFault;
                hit = hasHit(pick);
                if (hit) {
                    fraction = getFraction(pick);
                }
            } __except (EXCEPTION_EXECUTE_HANDLER) {
                return stage;
            }
#else
            ctor(pick);
            *reinterpret_cast<std::uint32_t*>(
                reinterpret_cast<std::byte*>(pick) + 0x0C) =
                static_cast<std::uint32_t>(RE::COL_LAYER::kLOS);
            setStartEnd(pick, *a_from, *a_to);
            (void)cellPick(a_cell, pick);
            hit = hasHit(pick);
            if (hit) {
                fraction = getFraction(pick);
            }
#endif

            if (!hit) {
                return GuardedPickResult::kMiss;
            }
            *a_fraction = fraction;
            return GuardedPickResult::kHit;
        }

        const char* GuardedPickStageName(GuardedPickResult a_result)
        {
            switch (a_result) {
            case GuardedPickResult::kCtorFault: return "verified bhkPickData constructor";
            case GuardedPickResult::kSetupFault: return "verified bhkPickData SetStartEnd/query setup";
            case GuardedPickResult::kPickFault: return "verified CellPick";
            case GuardedPickResult::kResultFault: return "verified bhkPickData result helpers";
            default: return "unknown";
            }
        }
    }

    Collision& Collision::Get()
    {
        static Collision c;
        return c;
    }

    void Collision::Start()
    {
        lastSample_ = {};
        logger::info("FalloutCraft: Fallout hknp collision sampler ready");
    }

    void Collision::Reset(std::uint32_t a_epoch)
    {
        epoch_ = a_epoch;
        occupied_.clear();
        lastSample_ = {};
        firstSampleLogged_ = false;
        firstRayLogged_ = false;
        fallbackFloorSet_ = false;
        fallbackFloorY_ = 0;
        {
            std::unique_lock lock(boxesLock_);
            boxes_.clear();
            ++boxesGen_;
        }
        Link::Get().WriteCollision(proto::kColClear, &epoch_, sizeof(epoch_));
    }

    bool Collision::Ray(const RE::NiPoint3& a_from, const RE::NiPoint3& a_to, RE::NiPoint3& a_hit) const
    {
        auto* player = RE::PlayerCharacter::GetSingleton();
        auto* cell = player ? player->GetParentCell() : nullptr;
        if (!cell || !cell->IsAttached()) {
            return false;
        }

        if (raycastingDisabled_) {
            return false;
        }

        float raw = 0.0f;
        // CellPick is the engine's own main-thread wrapper around the loaded hknp world.
        // Do not externally lock m_worldLock here; working Fallout raycast code leaves the
        // lock discipline to the engine wrapper itself.
        const auto result = SafeFullPick(cell, &a_from, &a_to, &raw);
        if (static_cast<int>(result) < 0) {
            logger::error(
                "FalloutCraft: guarded collision fault in {}; disabling live Fallout collision rays for this session",
                GuardedPickStageName(result));
            const_cast<Collision*>(this)->raycastingDisabled_ = true;
            return false;
        }
        if (result == GuardedPickResult::kMiss) {
            return false;
        }

        if (!std::isfinite(raw) || raw <= 0.0001f || raw > 1.0f) {
            return false;
        }
        if (!firstRayLogged_) {
            logger::info("FalloutCraft: first guarded Fallout collision ray returned safely (fraction {:.3f})", raw);
            const_cast<Collision*>(this)->firstRayLogged_ = true;
        }

        const float f = std::clamp(raw, 0.0f, 1.0f);
        a_hit.x = a_from.x + (a_to.x - a_from.x) * f;
        a_hit.y = a_from.y + (a_to.y - a_from.y) * f;
        a_hit.z = a_from.z + (a_to.z - a_from.z) * f;
        return true;
    }

    void Collision::MarkBlock(std::int32_t a_x, std::int32_t a_y, std::int32_t a_z)
    {
        occupied_.insert(Pack(a_x, a_y, a_z));
    }

    void Collision::Sample(const McVec& a_playerMc)
    {
        occupied_.clear();

        if (!firstSampleLogged_) {
            firstSampleLogged_ = true;
            logger::info("FalloutCraft: first post-link collision sample beginning (guarded hknp Pick, low ray budget)");
        }

        const int cx = static_cast<int>(std::floor(a_playerMc.x));
        const int cy = static_cast<int>(std::floor(a_playerMc.y));
        const int cz = static_cast<int>(std::floor(a_playerMc.z));

        // Floors/terrain/stairs. Sampling a generous grid makes the arrival region usable before
        // Minecraft is released and keeps several seconds of walking around the player populated.
        for (int dz = -4; dz <= 4; ++dz) {
            for (int dx = -4; dx <= 4; ++dx) {
                RE::NiPoint3 hit{};
                const auto from = McToSky(cx + dx + 0.5, cy + 6.0, cz + dz + 0.5);
                const auto to = McToSky(cx + dx + 0.5, cy - 18.0, cz + dz + 0.5);
                if (Ray(from, to, hit)) {
                    const auto mc = SkyToMc(hit);
                    MarkBlock(
                        static_cast<int>(std::floor(mc.x)),
                        static_cast<int>(std::floor(mc.y - 0.05)),
                        static_cast<int>(std::floor(mc.z)));
                }
            }
        }

        // Ceilings immediately around the player.
        for (int dz = -2; dz <= 2; ++dz) {
            for (int dx = -2; dx <= 2; ++dx) {
                RE::NiPoint3 hit{};
                const auto from = McToSky(cx + dx + 0.5, a_playerMc.y + 0.15, cz + dz + 0.5);
                const auto to = McToSky(cx + dx + 0.5, a_playerMc.y + 7.0, cz + dz + 0.5);
                if (Ray(from, to, hit)) {
                    const auto mc = SkyToMc(hit);
                    MarkBlock(
                        static_cast<int>(std::floor(mc.x)),
                        static_cast<int>(std::floor(mc.y + 0.05)),
                        static_cast<int>(std::floor(mc.z)));
                }
            }
        }

        // Walls, doors, vault geometry and other vertical collision. Multiple eye/body heights
        // prevent a low railing or a high overhang from disappearing from Minecraft's collision.
        constexpr int kRays = 24;
        constexpr double kRange = 10.0;
        constexpr std::array<double, 2> kHeights{ 0.65, 1.55 };
        for (double h : kHeights) {
            for (int i = 0; i < kRays; ++i) {
                const double a = (double(i) / kRays) * 6.2831853071795864769;
                const double dx = std::cos(a);
                const double dz = std::sin(a);
                const auto from = McToSky(a_playerMc.x, a_playerMc.y + h, a_playerMc.z);
                const auto to = McToSky(a_playerMc.x + dx * kRange, a_playerMc.y + h, a_playerMc.z + dz * kRange);
                RE::NiPoint3 hit{};
                if (Ray(from, to, hit)) {
                    auto mc = SkyToMc(hit);
                    // Step a little into the surface so a hit lying exactly on a cell edge is
                    // assigned to the solid side rather than the empty side.
                    mc.x += dx * 0.06;
                    mc.z += dz * 0.06;
                    MarkBlock(
                        static_cast<int>(std::floor(mc.x)),
                        static_cast<int>(std::floor(mc.y)),
                        static_cast<int>(std::floor(mc.z)));
                }
            }
        }

        // If Fallout's live ray path faults on this machine/runtime, do not take the
        // host down with it. Keep a small temporary support plane under the MC player so the
        // rest of the full-port stack (link, input, HUD, renderer, avatar) can still be tested.
        if (raycastingDisabled_ && occupied_.empty()) {
            // Keep the fallback at the ORIGINAL arrival height. v0.5.2 recomputed it from
            // Minecraft's falling Y every sample, so the emergency floor literally fell with
            // the player and could never catch them.
            if (!fallbackFloorSet_) {
                fallbackFloorSet_ = true;
                fallbackFloorY_ = static_cast<int>(std::floor(a_playerMc.y - 0.05)) - 1;
                logger::warn("FalloutCraft: anchoring emergency collision floor at Minecraft Y {}", fallbackFloorY_);
            }
            for (int dz = -8; dz <= 8; ++dz) {
                for (int dx = -8; dx <= 8; ++dx) {
                    MarkBlock(cx + dx, fallbackFloorY_, cz + dz);
                }
            }
        }

        // Cache full-block contact boxes for the renderer/NPC systems.
        {
            std::unique_lock lock(boxesLock_);
            boxes_.clear();
            constexpr std::uint32_t full =
                2u | (7u << 11) | (7u << 14) | (7u << 17);
            for (auto key : occupied_) {
                int x, y, z;
                Unpack(key, x, y, z);
                const int rx = FloorDiv8(x), ry = FloorDiv8(y), rz = FloorDiv8(z);
                auto& box = boxes_[RegionKey(rx, ry, rz)];
                const int bx = x - rx * 8, by = y - ry * 8, bz = z - rz * 8;
                if (bx >= 0 && bx < 8 && by >= 0 && by < 8 && bz >= 0 && bz < 8) {
                    box[bx + 8 * (by + 8 * bz)] = full;
                }
            }
            ++boxesGen_;
        }
    }

    void Collision::Publish(const McVec& a_playerMc)
    {
        const int prx = FloorDiv8(static_cast<int>(std::floor(a_playerMc.x)));
        const int pry = FloorDiv8(static_cast<int>(std::floor(a_playerMc.y)));
        const int prz = FloorDiv8(static_cast<int>(std::floor(a_playerMc.z)));

        for (int rz = prz - 1; rz <= prz + 1; ++rz) {
            for (int ry = pry - 2; ry <= pry + 1; ++ry) {
                for (int rx = prx - 1; rx <= prx + 1; ++rx) {
                    std::vector<std::array<int, 3>> blocks;
                    for (auto key : occupied_) {
                        int x, y, z;
                        Unpack(key, x, y, z);
                        if (FloorDiv8(x) == rx && FloorDiv8(y) == ry && FloorDiv8(z) == rz) {
                            blocks.push_back({ x, y, z });
                        }
                    }

                    proto::ColRegion region{};
                    region.minX = rx * 8;
                    region.minY = ry * 8;
                    region.minZ = rz * 8;
                    region.maxX = region.minX + 7;
                    region.maxY = region.minY + 7;
                    region.maxZ = region.minZ + 7;
                    region.epoch = epoch_;

                    // Exact triangles for the local player's smooth collider.
                    std::vector<proto::ColTri> tris;
                    tris.reserve(blocks.size() * 12);
                    for (const auto& b : blocks) {
                        CubeTriangles(b[0], b[1], b[2], tris);
                    }
                    region.count = static_cast<std::uint32_t>(tris.size());
                    std::vector<std::uint8_t> triPayload(sizeof(region) + tris.size() * sizeof(proto::ColTri));
                    std::memcpy(triPayload.data(), &region, sizeof(region));
                    if (!tris.empty()) {
                        std::memcpy(triPayload.data() + sizeof(region), tris.data(), tris.size() * sizeof(proto::ColTri));
                    }
                    Link::Get().WriteCollision(proto::kColTris, triPayload.data(), static_cast<std::uint32_t>(triPayload.size()));

                    // 1/8 voxel protocol remains intact. This first Fallout-native pass emits
                    // conservative whole-block occupancy; later hknp body harvesting can refine it
                    // without changing Minecraft or the wire format.
                    region.count = static_cast<std::uint32_t>(blocks.size());
                    std::vector<std::uint8_t> payload(sizeof(region) + blocks.size() * sizeof(proto::ColBlock));
                    std::memcpy(payload.data(), &region, sizeof(region));
                    auto* out = reinterpret_cast<proto::ColBlock*>(payload.data() + sizeof(region));
                    for (std::size_t i = 0; i < blocks.size(); ++i) {
                        out[i].x = blocks[i][0];
                        out[i].y = blocks[i][1];
                        out[i].z = blocks[i][2];
                        out[i].pad = 0;
                        std::fill(std::begin(out[i].bits), std::end(out[i].bits), ~0ull);
                    }
                    Link::Get().WriteCollision(proto::kColRegion, payload.data(), static_cast<std::uint32_t>(payload.size()));
                }
            }
        }
    }

    void Collision::Update(const McVec& a_playerMc)
    {
        const auto now = std::chrono::steady_clock::now();
        if (lastSample_.time_since_epoch().count() != 0 &&
            now - lastSample_ < std::chrono::milliseconds(350)) {
            return;
        }
        lastSample_ = now;
        Sample(a_playerMc);
        Publish(a_playerMc);
    }

    void Collision::CopyBoxes(const std::int32_t a_origin[3], const std::int32_t a_size[3],
        std::uint32_t* a_out) const
    {
        if (!a_out) {
            return;
        }
        std::shared_lock lock(boxesLock_);
        const int w = a_size[0], h = a_size[1], d = a_size[2];
        for (int z = 0; z < d; ++z) {
            for (int y = 0; y < h; ++y) {
                for (int x = 0; x < w; ++x) {
                    const int wx = a_origin[0] + x;
                    const int wy = a_origin[1] + y;
                    const int wz = a_origin[2] + z;
                    const int rx = FloorDiv8(wx), ry = FloorDiv8(wy), rz = FloorDiv8(wz);
                    const auto it = boxes_.find(RegionKey(rx, ry, rz));
                    if (it == boxes_.end()) {
                        continue;
                    }
                    const int bx = wx - rx * 8, by = wy - ry * 8, bz = wz - rz * 8;
                    a_out[x + w * (y + h * z)] |= it->second[bx + 8 * (by + 8 * bz)];
                }
            }
        }
    }

    void Collision::DigChanged(const std::vector<std::array<int, 3>>&)
    {
        lastSample_ = {};
    }
}
