#pragma once

#include "Link.h"

namespace falloutcraft
{
    // Fallout-native collision streamer.
    //
    // The full SkyCraft hkp implementation is retained in Collision.cpp for reference, but Fallout 4
    // uses hknp. This runtime implementation samples the active Fallout cell with bhkPickData and
    // streams nearby occupied Minecraft cells through the same collision-ring protocol. It is a
    // deliberately conservative first Fallout pass: Minecraft remains authoritative for movement,
    // and no Fallout character-controller warp is used.
    class Collision
    {
    public:
        static Collision& Get();

        void Start();
        void Reset(std::uint32_t a_epoch);
        void Update(const McVec& a_playerMc);

        static constexpr int kRegionSize = 8;

        void CopyBoxes(const std::int32_t a_origin[3], const std::int32_t a_size[3],
            std::uint32_t* a_out) const;
        std::uint32_t BoxesGeneration() const { return boxesGen_.load(); }
        void DigChanged(const std::vector<std::array<int, 3>>&);

    private:
        void Sample(const McVec& a_playerMc);
        bool Ray(const RE::NiPoint3& a_from, const RE::NiPoint3& a_to, RE::NiPoint3& a_hit) const;
        void MarkBlock(std::int32_t a_x, std::int32_t a_y, std::int32_t a_z);
        void Publish(const McVec& a_playerMc);

        std::uint32_t epoch_{ 0 };
        std::chrono::steady_clock::time_point lastSample_{};
        std::unordered_set<std::uint64_t> occupied_;
        bool raycastingDisabled_{ false };
        bool firstSampleLogged_{ false };
        bool firstRayLogged_{ false };

        mutable std::shared_mutex boxesLock_;
        std::unordered_map<std::uint64_t, std::array<std::uint32_t, 512>> boxes_;
        std::atomic<std::uint32_t> boxesGen_{ 0 };
    };
}
