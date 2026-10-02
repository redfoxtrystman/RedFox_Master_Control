#include "Game.h"

namespace falloutcraft
{
    namespace
    {
        constexpr std::uint64_t kMask = (1ull << 21) - 1;

        std::uint64_t Pack3(int x, int y, int z)
        {
            return (std::uint64_t(std::uint32_t(x)) & kMask) |
                   ((std::uint64_t(std::uint32_t(y)) & kMask) << 21) |
                   ((std::uint64_t(std::uint32_t(z)) & kMask) << 42);
        }

        int FloorDiv16(int v)
        {
            return v >= 0 ? v / 16 : -(((-v) + 15) / 16);
        }

        struct SolidSection
        {
            std::array<std::uint8_t, 512> bits{};
        };

        std::shared_mutex g_solidsLock;
        std::unordered_map<std::uint64_t, SolidSection> g_solids;
        std::atomic<std::uint32_t> g_solidsGeneration{ 0 };

        std::shared_mutex g_hazardLock;
        std::unordered_map<std::uint64_t, std::uint8_t> g_hazards;

        bool BitAt(const SolidSection& s, int x, int y, int z)
        {
            const int bit = x + 16 * z + 256 * y;
            return (s.bits[bit >> 3] & (1u << (bit & 7))) != 0;
        }
    }

    namespace CrashLog
    {
        void Install()
        {
            logger::info("FalloutCraft: crash diagnostics use F4SE/CommonLibF4 logging in full-port alpha");
        }
    }

    namespace Combat
    {
        void Install()
        {
            logger::info("FalloutCraft: combat bridge enabled in compatibility mode");
        }

        void PerFrame(RE::PlayerCharacter*, bool, float)
        {
            // The complete SkyCraft combat/proxy implementation is retained in Combat.cpp.
            // This compatibility alpha keeps the protocol live while the Fallout-specific
            // ActorValue/HitData translation is adapted.
        }

        bool PlayerEngaged()
        {
            return false;
        }
    }

    namespace BlockLights
    {
        void OnLights(const std::uint8_t* a_data, std::uint32_t a_bytes)
        {
            if (!a_data || a_bytes < sizeof(proto::RenLights)) {
                return;
            }

            const auto* h = reinterpret_cast<const proto::RenLights*>(a_data);
            const auto need = sizeof(*h) + std::uint64_t(h->count) * sizeof(proto::RenLight);
            if (need > a_bytes) {
                return;
            }

            const auto* lights = reinterpret_cast<const proto::RenLight*>(a_data + sizeof(*h));
            std::unique_lock lock(g_hazardLock);

            // Replace this section's hazard entries.
            for (auto it = g_hazards.begin(); it != g_hazards.end();) {
                const auto key = it->first;
                const int x = static_cast<int>(key & kMask);
                const int y = static_cast<int>((key >> 21) & kMask);
                const int z = static_cast<int>((key >> 42) & kMask);
                if (FloorDiv16(x) == h->sx && FloorDiv16(y) == h->sy && FloorDiv16(z) == h->sz) {
                    it = g_hazards.erase(it);
                } else {
                    ++it;
                }
            }

            for (std::uint32_t i = 0; i < h->count; ++i) {
                const int x = h->sx * 16 + lights[i].x;
                const int y = h->sy * 16 + lights[i].y;
                const int z = h->sz * 16 + lights[i].z;
                const auto meta = static_cast<std::uint8_t>((lights[i].color >> 24) & 0xFF);
                const auto hazard = static_cast<std::uint8_t>((meta >> 4) & 0x0F);
                if (hazard != proto::kHazardNone) {
                    g_hazards[Pack3(x, y, z)] = hazard;
                }
            }
        }

        void Update(const McVec*, float)
        {
            // Fallout-native dynamic point-light creation comes after the first alpha runtime pass.
            // The full light stream and hazard data are already consumed here.
        }

        std::uint8_t HazardAt(int a_x, int a_y, int a_z)
        {
            std::shared_lock lock(g_hazardLock);
            const auto it = g_hazards.find(Pack3(a_x, a_y, a_z));
            return it == g_hazards.end() ? 0 : it->second;
        }

        void Clear()
        {
            std::unique_lock lock(g_hazardLock);
            g_hazards.clear();
        }
    }

    namespace PathAvoid
    {
        void Install()
        {
            logger::info("FalloutCraft: NPC path avoidance compatibility layer loaded");
        }

        bool GoalOf(RE::Actor*, RE::NiPoint3&)
        {
            return false;
        }
    }

    namespace NpcBlocks
    {
        void OnSolids(const std::uint8_t* a_data, std::uint32_t a_bytes)
        {
            if (!a_data || a_bytes < sizeof(proto::RenSolids)) {
                return;
            }
            const auto* h = reinterpret_cast<const proto::RenSolids*>(a_data);
            const auto key = Pack3(h->sx, h->sy, h->sz);

            std::unique_lock lock(g_solidsLock);
            if (h->count == 0 || a_bytes < sizeof(*h) + 512) {
                g_solids.erase(key);
                ++g_solidsGeneration;
                return;
            }

            SolidSection s{};
            std::memcpy(s.bits.data(), a_data + sizeof(*h), s.bits.size());
            g_solids[key] = s;
            ++g_solidsGeneration;
        }

        void Clear()
        {
            std::unique_lock lock(g_solidsLock);
            g_solids.clear();
            ++g_solidsGeneration;
        }

        bool SolidAt(int a_x, int a_y, int a_z)
        {
            const int sx = FloorDiv16(a_x);
            const int sy = FloorDiv16(a_y);
            const int sz = FloorDiv16(a_z);
            const int bx = a_x - sx * 16;
            const int by = a_y - sy * 16;
            const int bz = a_z - sz * 16;

            std::shared_lock lock(g_solidsLock);
            const auto it = g_solids.find(Pack3(sx, sy, sz));
            return it != g_solids.end() && BitAt(it->second, bx, by, bz);
        }

        void CopySolids(const std::int32_t a_origin[3], const std::int32_t a_size[3], std::uint8_t* a_out)
        {
            if (!a_origin || !a_size || !a_out) {
                return;
            }
            const int w = a_size[0], h = a_size[1], d = a_size[2];
            for (int z = 0; z < d; ++z) {
                for (int y = 0; y < h; ++y) {
                    for (int x = 0; x < w; ++x) {
                        a_out[x + w * (y + h * z)] =
                            SolidAt(a_origin[0] + x, a_origin[1] + y, a_origin[2] + z) ? 1 : 0;
                    }
                }
            }
        }

        std::uint32_t Generation()
        {
            return g_solidsGeneration.load();
        }

        void PushActorsOut(RE::PlayerCharacter*, float)
        {
            // The render protocol is live and the Minecraft-solid cache is populated. The exact
            // Fallout NPC displacement/pathing hooks remain represented by NpcBlocks.cpp/PathAvoid.cpp
            // and are adapted after the first full-port runtime validation.
        }
    }
}
