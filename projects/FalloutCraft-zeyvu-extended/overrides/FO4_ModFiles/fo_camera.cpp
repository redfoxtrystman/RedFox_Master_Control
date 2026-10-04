// FalloutCraft: Minecraft's F5 camera in Fallout.
//
// Minecraft has three views: first person, behind the player and in front looking back. In the
// two third-person views Minecraft tells us how far its camera sits from the eye (after its own
// zoom collision against its blocks and Fallout's triangles). Fallout stays in its first-person
// camera state; right after its camera update the camera is moved back (or in front, turned
// around) from the eye, and Minecraft's own body is drawn at the feet (fo_blocks.cpp).
//
// PlayerCamera::Update is TESCamera vfunc 3; like Skyrim's it is mostly called directly, so its
// call sites in Fallout4.exe are redirected too.

#include "fo_common.h"

#define NOMINMAX
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#undef ERROR

#include <algorithm>
#include <cmath>
#include <mutex>
#include <vector>

namespace skycraft::Camera
{
	namespace
	{
		std::mutex   lock;
		RE::NiPoint3 eye{};           // Minecraft's eye, Fallout coords
		float        heading = 0.0f;  // radians, as Fallout's
		float        pitch = 0.0f;    // radians, positive looks down
		float        distance = 0.0f; // units
		float        fovDeg = 70.0f;  // Minecraft effective vertical FOV
		int          mode = 0;        // 0 first person, 1 behind, 2 in front
		bool         active = false;
		bool         fovSaved = false;
		float        savedWorldFov = 0.0f;
		float        savedFirstPersonFov = 0.0f;
		bool         loggedApplied = false;
		bool         axesInRows = true;  // the turn on the left side (columns) spun the view in circles
		bool         loggedConvention = false;

		// Fallout/Skyrim look direction: heading clockwise from north, positive pitch looks down.
		RE::NiPoint3 Forward(float a_heading, float a_pitch)
		{
			return { std::sin(a_heading) * std::cos(a_pitch), std::cos(a_heading) * std::cos(a_pitch), -std::sin(a_pitch) };
		}

		// Bethesda stores camera FOV in the same 4:3-horizontal convention SkyCraft has to
		// feed Skyrim, while Minecraft publishes an effective vertical FOV. Convert the live
		// Minecraft value so sprinting, speed/slowness, flying and other vanilla FOV effects survive
		// the Fallout render handoff.
		float McFovToFallout(float a_verticalDeg)
		{
			const float half = std::clamp(a_verticalDeg, 10.0f, 170.0f) * 0.5f * (3.14159265358979323846f / 180.0f);
			return 2.0f * std::atan(std::tan(half) * (4.0f / 3.0f)) * (180.0f / 3.14159265358979323846f);
		}

		void ApplyFov(RE::PlayerCamera* a_camera, bool a_active, float a_mcFov)
		{
			if (!a_camera) {
				return;
			}
			if (!a_active) {
				if (fovSaved) {
					a_camera->worldFOV = savedWorldFov;
					a_camera->firstPersonFOV = savedFirstPersonFov;
					fovSaved = false;
				}
				return;
			}
			if (!fovSaved) {
				savedWorldFov = a_camera->worldFOV;
				savedFirstPersonFov = a_camera->firstPersonFOV;
				fovSaved = true;
			}
			if (std::isfinite(a_mcFov) && a_mcFov > 1.0f) {
				const float falloutFov = McFovToFallout(a_mcFov);
				a_camera->worldFOV = falloutFov;
				a_camera->firstPersonFOV = falloutFov;
			}
		}

		void Apply(RE::PlayerCamera* a_camera)
		{
			RE::NiPoint3 e;
			float        h, p, d, fov;
			int          m;
			bool         on;
			{
				std::scoped_lock l(lock);
				on = active;
				e = eye, h = heading, p = pitch, d = distance, fov = fovDeg, m = mode;
			}
			ApplyFov(a_camera, on, fov);
			if (!on) {
				return;
			}
			auto* root = a_camera ? a_camera->cameraRoot.get() : nullptr;
			if (!root) {
				return;
			}
			const RE::NiPoint3 f = Forward(h, p);
			// First person is Minecraft's exact eye position (including the smoothed sneak/crouch
			// eye height). Third person then offsets from that eye by Minecraft's own collision-
			// limited F5 camera distance.
			RE::NiPoint3 pos = e;
			if (m == 1 && d > 1.0f) {
				pos = e - f * d;
			} else if (m == 2 && d > 1.0f) {
				pos = e + f * d;
			}
			if (m == 2 && d > 1.0f) {
				// Turn the camera 180 degrees about the world-space axis that is "up" for the view
				// (perpendicular to the look direction): it then looks back at the player.
				RE::NiPoint3 up{ 0.0f, 0.0f, 1.0f };
				up = up - f * f.Dot(up);
				const float len = up.Length();
				if (len > 1e-4f) {
					up = up * (1.0f / len);
					RE::NiMatrix3 turn;
					for (int r = 0; r < 3; ++r) {
						const float ur = r == 0 ? up.x : r == 1 ? up.y : up.z;
						for (int c = 0; c < 3; ++c) {
							const float uc = c == 0 ? up.x : c == 1 ? up.y : up.z;
							turn.entry[r][c] = 2.0f * ur * uc - (r == c ? 1.0f : 0.0f);
						}
					}
					// Which way round the root's matrix holds its axes decides the side the turn goes
					// on: the look direction is one of its rows or one of its columns.
					const auto& R = root->world.rotate;
					float       bestRow = 0.0f, bestCol = 0.0f;
					for (int i = 0; i < 3; ++i) {
						bestRow = std::max(bestRow, std::fabs(R.entry[i][0] * f.x + R.entry[i][1] * f.y + R.entry[i][2] * f.z));
						bestCol = std::max(bestCol, std::fabs(R.entry[0][i] * f.x + R.entry[1][i] * f.y + R.entry[2][i] * f.z));
					}
					if (std::fabs(bestRow - bestCol) > 0.05f) {
						const bool rows = bestRow > bestCol;
						if (rows != axesInRows || !loggedConvention) {
							loggedConvention = true;
							REX::INFO("third person: camera axes are the matrix {} (row match {:.2f}, column match {:.2f})", rows ? "rows" : "columns", bestRow, bestCol);
						}
						axesInRows = rows;
					}
					root->world.rotate = axesInRows ? R * turn : turn * R;
					root->local.rotate = root->world.rotate;
				}
			}
			const bool identityParent = !root->parent || root->parent->world.translate.Length() < 0.001f;
			if (identityParent) {
				root->local.translate = pos;
			}
			root->world.translate = pos;
			a_camera->bufferedCameraPos = pos;
			a_camera->cameraPosBuffered = true;
			RE::NiUpdateData update{};
			root->UpdateDownwardPass(update, 0);
			if (!loggedApplied) {
				loggedApplied = true;
				REX::INFO("Minecraft camera takeover active (mode {}, distance {:.0f}, FOV {:.1f}, root parent {})", m, d, fov,
					root->parent ? root->parent->name.c_str() : "(none)");
			}
		}

		struct UpdateHook
		{
			static void thunk(RE::PlayerCamera* a_this)
			{
				func(a_this);
				Apply(a_this);
			}
			static inline REL::Relocation<decltype(thunk)> func;
		};
	}

	void Set(bool a_active, int a_mode, const RE::NiPoint3& a_eye, float a_heading, float a_pitch, float a_distance, float a_fovDeg)
	{
		std::scoped_lock l(lock);
		active = a_active;
		mode = a_mode;
		eye = a_eye;
		heading = a_heading;
		pitch = a_pitch;
		distance = a_distance;
		fovDeg = a_fovDeg;
	}

	void Install()
	{
		REL::Relocation<std::uintptr_t> vtbl{ RE::VTABLE::PlayerCamera[0] };
		const auto                      target = *reinterpret_cast<const std::uintptr_t*>(vtbl.address() + 3 * sizeof(void*));

		// Every `call PlayerCamera::Update` in Fallout4.exe's code.
		auto*       base = reinterpret_cast<const std::uint8_t*>(::GetModuleHandleW(nullptr));
		const auto* dos = reinterpret_cast<const IMAGE_DOS_HEADER*>(base);
		const auto* nt = reinterpret_cast<const IMAGE_NT_HEADERS64*>(base + dos->e_lfanew);
		const auto* sec = IMAGE_FIRST_SECTION(nt);
		std::vector<std::uintptr_t> sites;
		for (int s = 0; s < nt->FileHeader.NumberOfSections; ++s, ++sec) {
			if (!(sec->Characteristics & IMAGE_SCN_MEM_EXECUTE)) {
				continue;
			}
			const auto* code = base + sec->VirtualAddress;
			const auto  size = sec->Misc.VirtualSize;
			for (std::size_t i = 0; i + 5 <= size; ++i) {
				if (code[i] != 0xE8) {
					continue;
				}
				std::int32_t rel;
				std::memcpy(&rel, code + i + 1, 4);
				if (reinterpret_cast<std::uintptr_t>(code + i + 5) + static_cast<std::intptr_t>(rel) == target) {
					sites.push_back(reinterpret_cast<std::uintptr_t>(code + i));
				}
			}
		}
		auto& trampoline = REL::GetTrampoline();
		for (const auto site : sites) {
			UpdateHook::func = trampoline.write_call<5>(site, UpdateHook::thunk);
		}
		// And calls through the vtable.
		const auto original = vtbl.write_vfunc(3, UpdateHook::thunk);
		if (sites.empty()) {
			UpdateHook::func = original;
		}
		REX::INFO("third person: PlayerCamera::Update hooked ({} call sites + vtable)", sites.size());
	}
}
