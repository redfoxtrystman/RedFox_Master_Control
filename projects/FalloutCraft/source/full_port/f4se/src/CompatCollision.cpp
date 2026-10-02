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

        using PickCtorFn = void* (*)(void*);
        using PickSetStartEndFn = void (*)(void*, const RE::NiPoint3&, const RE::NiPoint3&);
        using PickHasHitFn = bool (*)(void*);
        using PickGetFractionFn = float (*)(void*);
        using CellPickFn = RE::NiAVObject* (*)(RE::TESObjectCELL*, void*);

        REL::Relocation<PickCtorFn> g_pickCtor{ REL::ID(526783) };
        REL::Relocation<PickSetStartEndFn> g_pickSetStartEnd{ REL::ID(747470) };
        REL::Relocation<PickHasHitFn> g_pickHasHit{ REL::ID(1181584) };
        REL::Relocation<PickGetFractionFn> g_pickGetFraction{ REL::ID(476687) };
        REL::Relocation<CellPickFn> g_cellPick{ REL::ID(434717) };

        GuardedPickResult SafeFullPick(
            RE::TESObjectCELL* a_cell,
            const RE::NiPoint3* a_from,
            const RE::NiPoint3* a_to,
            float* a_fraction)
        {
            if (!a_cell || !a_from || !a_to || !a_fraction) {
                return GuardedPickResult::kSetupFault;
            }

            VerifiedPickStorage storage{};
            void* pick = storage.data;
            GuardedPickResult stage = GuardedPickResult::kCtorFault;
            bool hit = false;
            float fraction = 0.0f;

#if defined(_MSC_VER)
            __try {
                g_pickCtor(pick);

                stage = GuardedPickResult::kSetupFault;
                // castQuery.m_filterData.m_collisionFilterInfo is +0x0C.
                *reinterpret_cast<std::uint32_t*>(
                    reinterpret_cast<std::byte*>(pick) + 0x0C) =
                    static_cast<std::uint32_t>(RE::COL_LAYER::kLOS);
                g_pickSetStartEnd(pick, *a_from, *a_to);

                stage = GuardedPickResult::kPickFault;
                (void)g_cellPick(a_cell, pick);

                stage = GuardedPickResult::kResultFault;
                hit = g_pickHasHit(pick);
                if (hit) {
                    fraction = g_pickGetFraction(pick);
                }
            } __except (EXCEPTION_EXECUTE_HANDLER) {
                return stage;
            }
#else
            g_pickCtor(pick);
            *reinterpret_cast<std::uint32_t*>(
                reinterpret_cast<std::byte*>(pick) + 0x0C) =
                static_cast<std::uint32_t>(RE::COL_LAYER::kLOS);
            g_pickSetStartEnd(pick, *a_from, *a_to);
            (void)g_cellPick(a_cell, pick);
            hit = g_pickHasHit(pick);
            if (hit) {
                fraction = g_pickGetFraction(pick);
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
        voxels_.clear();
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

    void Collision::SetVoxel(std::int32_t a_x, std::int32_t a_y, std::int32_t a_z,
        int a_sx, int a_sy, int a_sz)
    {
        if (a_sx < 0 || a_sx > 7 || a_sy < 0 || a_sy > 7 || a_sz < 0 || a_sz > 7) {
            return;
        }
        auto& bits = voxels_[Pack(a_x, a_y, a_z)];
        bits[static_cast<std::size_t>(a_sy)] |=
            1ull << static_cast<unsigned>(a_sx + 8 * a_sz);
    }

    void Collision::SetFullBlock(std::int32_t a_x, std::int32_t a_y, std::int32_t a_z)
    {
        auto& bits = voxels_[Pack(a_x, a_y, a_z)];
        bits.fill(~0ull);
    }

    void Collision::MarkFloorSurface(double a_x, double a_y, double a_z)
    {
        // Quantize DOWN to the nearest 1/8-block boundary and occupy the slice directly
        // below it. The top of the collision never protrudes above Fallout's sampled floor,
        // so Minecraft cannot spawn embedded in a whole fake cube.
        const int globalSy = static_cast<int>(std::floor(a_y * 8.0 + 1.0e-4)) - 1;
        const int by = FloorDiv8(globalSy);
        const int sy = globalSy - by * 8;
        const int bx = static_cast<int>(std::floor(a_x));
        const int bz = static_cast<int>(std::floor(a_z));
        auto& bits = voxels_[Pack(bx, by, bz)];
        bits[static_cast<std::size_t>(sy)] = ~0ull;
    }

    void Collision::MarkCeilingSurface(double a_x, double a_y, double a_z)
    {
        // Mirror of MarkFloorSurface: occupy the first 1/8 slice wholly above the sampled
        // ceiling so head collision does not extend down into empty space.
        const int globalSy = static_cast<int>(std::ceil(a_y * 8.0 - 1.0e-4));
        const int by = FloorDiv8(globalSy);
        const int sy = globalSy - by * 8;
        const int bx = static_cast<int>(std::floor(a_x));
        const int bz = static_cast<int>(std::floor(a_z));
        auto& bits = voxels_[Pack(bx, by, bz)];
        bits[static_cast<std::size_t>(sy)] = ~0ull;
    }

    void Collision::MarkWallSurface(double a_x, double a_y, double a_z, double a_dx, double a_dz)
    {
        // The ray travels from the player INTO the wall, so move a few centimetres past the
        // hit to choose the solid side. Then represent it as a 1/8-block vertical slab, the
        // same sub-voxel resolution SkyCraft feeds to Minecraft rather than a whole block.
        const double ix = a_x + a_dx * 0.04;
        const double iz = a_z + a_dz * 0.04;
        const int bx = static_cast<int>(std::floor(ix));
        const int by = static_cast<int>(std::floor(a_y));
        const int bz = static_cast<int>(std::floor(iz));
        const int sx = std::clamp(static_cast<int>(std::floor((ix - bx) * 8.0)), 0, 7);
        const int sz = std::clamp(static_cast<int>(std::floor((iz - bz) * 8.0)), 0, 7);
        auto& bits = voxels_[Pack(bx, by, bz)];

        if (std::abs(a_dx) >= std::abs(a_dz)) {
            std::uint64_t column = 0;
            for (int z = 0; z < 8; ++z) {
                column |= 1ull << static_cast<unsigned>(sx + 8 * z);
            }
            bits.fill(column);
        } else {
            const std::uint64_t row = 0xFFull << static_cast<unsigned>(sz * 8);
            bits.fill(row);
        }
    }

    void Collision::RebuildContactBoxes()
    {
        std::unordered_map<std::uint64_t, std::array<std::uint32_t, 512>> fresh;
        constexpr std::uint32_t kBoxPresent = 2u;

        for (const auto& [key, bits] : voxels_) {
            int x, y, z;
            Unpack(key, x, y, z);

            int loX = 8, loY = 8, loZ = 8;
            int hiX = -1, hiY = -1, hiZ = -1;
            for (int sy = 0; sy < 8; ++sy) {
                std::uint64_t layer = bits[static_cast<std::size_t>(sy)];
                if (!layer) {
                    continue;
                }
                loY = std::min(loY, sy);
                hiY = std::max(hiY, sy);
                while (layer) {
                    const int bit = std::countr_zero(layer);
                    layer &= layer - 1;
                    const int sx = bit & 7;
                    const int sz = bit >> 3;
                    loX = std::min(loX, sx);
                    hiX = std::max(hiX, sx);
                    loZ = std::min(loZ, sz);
                    hiZ = std::max(hiZ, sz);
                }
            }
            if (hiX < 0) {
                continue;
            }

            const int rx = FloorDiv8(x), ry = FloorDiv8(y), rz = FloorDiv8(z);
            auto& region = fresh[RegionKey(rx, ry, rz)];
            const int bx = x - rx * 8, by = y - ry * 8, bz = z - rz * 8;
            if (bx < 0 || bx >= 8 || by < 0 || by >= 8 || bz < 0 || bz >= 8) {
                continue;
            }
            region[bx + 8 * (by + 8 * bz)] =
                kBoxPresent |
                (static_cast<std::uint32_t>(loX) << 2) |
                (static_cast<std::uint32_t>(loY) << 5) |
                (static_cast<std::uint32_t>(loZ) << 8) |
                (static_cast<std::uint32_t>(hiX) << 11) |
                (static_cast<std::uint32_t>(hiY) << 14) |
                (static_cast<std::uint32_t>(hiZ) << 17);
        }

        std::unique_lock lock(boxesLock_);
        boxes_.swap(fresh);
        ++boxesGen_;
    }

    void Collision::Sample(const McVec& a_playerMc)
    {
        voxels_.clear();

        if (!firstSampleLogged_) {
            firstSampleLogged_ = true;
            logger::info("FalloutCraft: first post-link collision sample beginning (SkyCraft-style 1/8 voxel surfaces)");
        }

        const int cx = static_cast<int>(std::floor(a_playerMc.x));
        const int cy = static_cast<int>(std::floor(a_playerMc.y));
        const int cz = static_cast<int>(std::floor(a_playerMc.z));

        // Floors/terrain/stairs. Fallout's ray gives us the exact surface height; preserve that
        // height at 1/8-block resolution instead of inflating every hit to a whole Minecraft cube.
        for (int dz = -5; dz <= 5; ++dz) {
            for (int dx = -5; dx <= 5; ++dx) {
                RE::NiPoint3 hit{};
                const auto from = McToSky(cx + dx + 0.5, cy + 6.0, cz + dz + 0.5);
                const auto to = McToSky(cx + dx + 0.5, cy - 18.0, cz + dz + 0.5);
                if (Ray(from, to, hit)) {
                    const auto mc = SkyToMc(hit);
                    MarkFloorSurface(mc.x, mc.y, mc.z);
                }
            }
        }

        // Ceilings: thin 1/8-block support plane on the solid side only.
        for (int dz = -3; dz <= 3; ++dz) {
            for (int dx = -3; dx <= 3; ++dx) {
                RE::NiPoint3 hit{};
                const auto from = McToSky(cx + dx + 0.5, a_playerMc.y + 0.15, cz + dz + 0.5);
                const auto to = McToSky(cx + dx + 0.5, a_playerMc.y + 7.0, cz + dz + 0.5);
                if (Ray(from, to, hit)) {
                    const auto mc = SkyToMc(hit);
                    MarkCeilingSurface(mc.x, mc.y, mc.z);
                }
            }
        }

        // Walls/doors/railings. Two body heights plus a denser angular fan give Minecraft thin
        // vertical slabs near the real Fallout collision rather than body-sized fake cubes.
        constexpr int kRays = 48;
        constexpr double kRange = 10.0;
        constexpr std::array<double, 3> kHeights{ 0.35, 1.0, 1.65 };
        for (double h : kHeights) {
            for (int i = 0; i < kRays; ++i) {
                const double a = (double(i) / kRays) * 6.2831853071795864769;
                const double dx = std::cos(a);
                const double dz = std::sin(a);
                const auto from = McToSky(a_playerMc.x, a_playerMc.y + h, a_playerMc.z);
                const auto to = McToSky(a_playerMc.x + dx * kRange, a_playerMc.y + h, a_playerMc.z + dz * kRange);
                RE::NiPoint3 hit{};
                if (Ray(from, to, hit)) {
                    const auto mc = SkyToMc(hit);
                    MarkWallSurface(mc.x, mc.y, mc.z, dx, dz);
                }
            }
        }

        // If the verified Fallout ray path faults, retain a stable emergency support floor so
        // the rest of the bridge remains testable. This fallback is intentionally the only place
        // that still publishes whole cubes.
        if (raycastingDisabled_ && voxels_.empty()) {
            if (!fallbackFloorSet_) {
                fallbackFloorSet_ = true;
                fallbackFloorY_ = static_cast<int>(std::floor(a_playerMc.y - 0.05)) - 1;
                logger::warn("FalloutCraft: anchoring emergency collision floor at Minecraft Y {}", fallbackFloorY_);
            }
            for (int dz = -8; dz <= 8; ++dz) {
                for (int dx = -8; dx <= 8; ++dx) {
                    SetFullBlock(cx + dx, fallbackFloorY_, cz + dz);
                }
            }
        }

        RebuildContactBoxes();
    }

    void Collision::Publish(const McVec& a_playerMc)
    {
        const int prx = FloorDiv8(static_cast<int>(std::floor(a_playerMc.x)));
        const int pry = FloorDiv8(static_cast<int>(std::floor(a_playerMc.y)));
        const int prz = FloorDiv8(static_cast<int>(std::floor(a_playerMc.z)));

        // Publish the same ColBlock 8x8x8 sub-voxel representation used by SkyCraft. Empty
        // regions are sent too, which tells Minecraft old collision in that region is gone.
        for (int rz = prz - 1; rz <= prz + 1; ++rz) {
            for (int ry = pry - 2; ry <= pry + 1; ++ry) {
                for (int rx = prx - 1; rx <= prx + 1; ++rx) {
                    std::vector<proto::ColBlock> blocks;
                    blocks.reserve(96);
                    for (const auto& [key, bits] : voxels_) {
                        int x, y, z;
                        Unpack(key, x, y, z);
                        if (FloorDiv8(x) != rx || FloorDiv8(y) != ry || FloorDiv8(z) != rz) {
                            continue;
                        }
                        bool any = false;
                        for (auto layer : bits) {
                            any |= layer != 0;
                        }
                        if (!any) {
                            continue;
                        }
                        proto::ColBlock block{};
                        block.x = x;
                        block.y = y;
                        block.z = z;
                        block.pad = 0;
                        std::copy(bits.begin(), bits.end(), std::begin(block.bits));
                        blocks.push_back(block);
                    }

                    proto::ColRegion region{};
                    region.minX = rx * 8;
                    region.minY = ry * 8;
                    region.minZ = rz * 8;
                    region.maxX = region.minX + 7;
                    region.maxY = region.minY + 7;
                    region.maxZ = region.minZ + 7;
                    region.epoch = epoch_;
                    region.count = static_cast<std::uint32_t>(blocks.size());

                    std::vector<std::uint8_t> payload(sizeof(region) + blocks.size() * sizeof(proto::ColBlock));
                    std::memcpy(payload.data(), &region, sizeof(region));
                    if (!blocks.empty()) {
                        std::memcpy(payload.data() + sizeof(region), blocks.data(), blocks.size() * sizeof(proto::ColBlock));
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
            now - lastSample_ < std::chrono::milliseconds(100)) {
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
