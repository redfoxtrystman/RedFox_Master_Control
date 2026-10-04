// Source-backed Subnautica host compositor adapted from
// rehan-remade/universal-modder/examples/minecraft-gta5-passthrough/gta/src/compositor.cpp
// ReShade API target: 6.8.0, matching Universal Modder's working example.

#include <windows.h>
#include <algorithm>
#include <atomic>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <mutex>
#include <reshade.hpp>

using namespace reshade::api;

extern "C" __declspec(dllexport) const char *NAME = "Minecraft Subnautica Passthrough";
extern "C" __declspec(dllexport) const char *DESCRIPTION =
	"Composites Minecraft world colour/depth and HUD into Subnautica using the host depth buffer.";

namespace
{
	constexpr const wchar_t *kFrameMapping = L"Local\\SkyCraft_Subnautica_Frame_v1";
	constexpr const wchar_t *kCameraMapping = L"Local\\SkyCraft_Subnautica_Camera_v1";
	constexpr std::uint32_t kFrameMagic = 0x46435353;
	constexpr std::uint32_t kCameraMagic = 0x4D414353;
	constexpr std::uint32_t kVersion = 1;
	constexpr int kHeader = 4096;
	constexpr int kSlotDesc = 256;
	constexpr int kSlotDescBytes = 128;
	constexpr char kEffect[] = "MinecraftSubnautica.fx";

	template <typename T>
	T read(const std::uint8_t *p)
	{
		T v;
		std::memcpy(&v, p, sizeof(T));
		return v;
	}

	struct Mapping
	{
		HANDLE handle = nullptr;
		const std::uint8_t *view = nullptr;
		SIZE_T bytes = 0;

		void close()
		{
			if (view) UnmapViewOfFile(view);
			if (handle) CloseHandle(handle);
			view = nullptr;
			handle = nullptr;
			bytes = 0;
		}
	};

	Mapping g_frameMap, g_cameraMap;
	DWORD g_nextFrameOpen = 0, g_nextCameraOpen = 0;

	struct Pose
	{
		std::uint64_t hostFrame = 0;
		float yaw = 0, pitch = 0, roll = 0, fov = 70;
		float nearClip = 0.1f, farClip = 1000.0f;
		double x = 0, y = 0, z = 0;
		bool firstPerson = true;
		bool valid = false;
	};
	Pose g_hostPose, g_mcPose;

	int32_t g_slots = 0;
	int64_t g_stride = 0;
	int64_t g_lastPublish = -1;

	struct Layer
	{
		resource tex = {0};
		resource_view srv = {0};
	};
	Layer g_world, g_depth, g_overlay;
	uint32_t g_width = 0, g_height = 0;
	bool g_hasFrame = false;
	float g_mcNear = 0.05f, g_mcFar = 2048.0f;
	int32_t g_mcFlags = 7;

	bool open_frame_mapping()
	{
		if (g_frameMap.view)
			return true;
		if (GetTickCount() < g_nextFrameOpen)
			return false;
		g_nextFrameOpen = GetTickCount() + 1000;

		HANDLE h = OpenFileMappingW(FILE_MAP_READ, FALSE, kFrameMapping);
		if (!h)
			return false;
		const auto *head = static_cast<const std::uint8_t *>(MapViewOfFile(h, FILE_MAP_READ, 0, 0, kHeader));
		if (!head || read<std::uint32_t>(head) != kFrameMagic || read<std::uint32_t>(head + 4) != kVersion)
		{
			if (head) UnmapViewOfFile(head);
			CloseHandle(h);
			return false;
		}
		g_slots = read<int32_t>(head + 12);
		g_stride = read<int64_t>(head + 16);
		const SIZE_T total = static_cast<SIZE_T>(kHeader + g_stride * g_slots);
		UnmapViewOfFile(head);

		const auto *view = static_cast<const std::uint8_t *>(MapViewOfFile(h, FILE_MAP_READ, 0, 0, total));
		if (!view)
		{
			CloseHandle(h);
			return false;
		}
		g_frameMap.handle = h;
		g_frameMap.view = view;
		g_frameMap.bytes = total;
		reshade::log::message(reshade::log::level::info,
			"MinecraftSubnautica: connected to Minecraft world/depth/HUD frame export");
		return true;
	}

	bool open_camera_mapping()
	{
		if (g_cameraMap.view)
			return true;
		if (GetTickCount() < g_nextCameraOpen)
			return false;
		g_nextCameraOpen = GetTickCount() + 1000;

		HANDLE h = OpenFileMappingW(FILE_MAP_READ, FALSE, kCameraMapping);
		if (!h)
			return false;
		const auto *view = static_cast<const std::uint8_t *>(MapViewOfFile(h, FILE_MAP_READ, 0, 0, 4096));
		if (!view || read<std::uint32_t>(view) != kCameraMagic || read<std::uint32_t>(view + 4) != kVersion)
		{
			if (view) UnmapViewOfFile(view);
			CloseHandle(h);
			return false;
		}
		g_cameraMap.handle = h;
		g_cameraMap.view = view;
		g_cameraMap.bytes = 4096;
		reshade::log::message(reshade::log::level::info,
			"MinecraftSubnautica: connected to Subnautica MainCamera.camera state");
		return true;
	}

	bool read_host_pose()
	{
		if (!open_camera_mapping())
			return false;
		const auto *v = g_cameraMap.view;
		const std::uint64_t beat = read<std::uint64_t>(v + 0x10);
		const std::uint64_t now = GetTickCount64();
		if (beat == 0 || now < beat || now - beat > 2000)
			return false;

		for (int attempt = 0; attempt < 32; ++attempt)
		{
			const std::uint64_t s1 = read<std::uint64_t>(v + 0x20);
			if (s1 & 1)
				continue;

			Pose p;
			p.hostFrame = read<std::uint64_t>(v + 0x28);
			p.x = read<double>(v + 0x30);
			p.y = read<double>(v + 0x38);
			p.z = read<double>(v + 0x40);
			p.yaw = read<float>(v + 0x48);
			p.pitch = read<float>(v + 0x4C);
			p.roll = read<float>(v + 0x50);
			p.fov = read<float>(v + 0x54);
			p.nearClip = read<float>(v + 0x58);
			p.farClip = read<float>(v + 0x5C);
			p.firstPerson = (read<std::uint32_t>(v + 0x60) & 1u) != 0;
			p.valid = true;

			MemoryBarrier();
			const std::uint64_t s2 = read<std::uint64_t>(v + 0x20);
			if (s1 == s2 && !(s2 & 1))
			{
				g_hostPose = p;
				return true;
			}
		}
		return false;
	}

	void destroy_layers(device *dev)
	{
		for (Layer *layer : { &g_world, &g_depth, &g_overlay })
		{
			if (layer->srv.handle != 0) dev->destroy_resource_view(layer->srv);
			if (layer->tex.handle != 0) dev->destroy_resource(layer->tex);
			*layer = Layer();
		}
		g_width = g_height = 0;
		g_hasFrame = false;
	}

	bool create_layer(device *dev, Layer &layer, uint32_t w, uint32_t h, format fmt)
	{
		if (!dev->create_resource(
				resource_desc(w, h, 1, 1, fmt, 1, memory_heap::default_,
					resource_usage::shader_resource | resource_usage::copy_dest),
				nullptr, resource_usage::shader_resource, &layer.tex))
			return false;
		return dev->create_resource_view(
			layer.tex, resource_usage::shader_resource, resource_view_desc(fmt), &layer.srv);
	}

	void bind(effect_runtime *runtime)
	{
		runtime->update_texture_bindings("MCWORLD", g_world.srv, g_world.srv);
		runtime->update_texture_bindings("MCDEPTH", g_depth.srv, g_depth.srv);
		runtime->update_texture_bindings("MCOVERLAY", g_overlay.srv, g_overlay.srv);
	}

	void upload(effect_runtime *runtime)
	{
		if (!open_frame_mapping())
			return;
		const auto *v = g_frameMap.view;
		const int64_t published = read<int64_t>(v + 32);
		if (published == g_lastPublish)
			return;
		const int32_t slot = read<int32_t>(v + 40);
		if (slot < 0 || slot >= g_slots)
			return;

		const std::uint8_t *desc = v + kSlotDesc + kSlotDescBytes * slot;
		const int64_t seq = read<int64_t>(desc);
		if (seq & 1)
			return;

		const uint32_t w = read<uint32_t>(desc + 24);
		const uint32_t h = read<uint32_t>(desc + 28);
		if (w == 0 || h == 0)
			return;

		device *dev = runtime->get_device();
		if (w != g_width || h != g_height)
		{
			destroy_layers(dev);
			if (!create_layer(dev, g_world, w, h, format::r8g8b8a8_unorm) ||
				!create_layer(dev, g_depth, w, h, format::r32_float) ||
				!create_layer(dev, g_overlay, w, h, format::r8g8b8a8_unorm))
			{
				destroy_layers(dev);
				return;
			}
			g_width = w;
			g_height = h;
			bind(runtime);
		}

		const std::uint8_t *base = v + kHeader + g_stride * slot;
		const size_t layerBytes = size_t(w) * h * 4;
		subresource_data data;
		data.row_pitch = w * 4;
		data.slice_pitch = static_cast<uint32_t>(layerBytes);
		data.data = const_cast<std::uint8_t *>(base);
		dev->update_texture_region(data, g_world.tex, 0);
		data.data = const_cast<std::uint8_t *>(base + layerBytes);
		dev->update_texture_region(data, g_depth.tex, 0);
		data.data = const_cast<std::uint8_t *>(base + 2 * layerBytes);
		dev->update_texture_region(data, g_overlay.tex, 0);

		if (read<int64_t>(desc) != seq)
			return;

		g_lastPublish = published;
		g_mcNear = read<float>(desc + 32);
		g_mcFar = read<float>(desc + 36);
		g_mcFlags = read<int32_t>(desc + 44);
		g_mcPose.fov = read<float>(desc + 40);
		g_mcPose.x = read<double>(desc + 48);
		g_mcPose.y = read<double>(desc + 56);
		g_mcPose.z = read<double>(desc + 64);
		g_mcPose.yaw = read<float>(desc + 72);
		g_mcPose.pitch = read<float>(desc + 76);
		g_mcPose.roll = read<float>(desc + 80);
		g_mcPose.firstPerson = read<int32_t>(desc + 84) != 0;
		g_mcPose.valid = true;
		g_hasFrame = true;
	}

	void camera_rotation(const Pose &p, float m[3][3])
	{
		const float d2r = 3.14159265f / 180.0f;
		const float a = 3.14159265f - p.yaw * d2r;
		const float b = -p.pitch * d2r;
		const float c = p.roll * d2r;
		const float ca = std::cos(a), sa = std::sin(a);
		const float cb = std::cos(b), sb = std::sin(b);
		const float cc = std::cos(c), sc = std::sin(c);
		const float ry[3][3] = { {ca,0,sa},{0,1,0},{-sa,0,ca} };
		const float rx[3][3] = { {1,0,0},{0,cb,-sb},{0,sb,cb} };
		const float rz[3][3] = { {cc,-sc,0},{sc,cc,0},{0,0,1} };
		float t[3][3] = {};
		for (int i = 0; i < 3; ++i)
			for (int j = 0; j < 3; ++j)
				for (int k = 0; k < 3; ++k)
					t[i][j] += ry[i][k] * rx[k][j];
		for (int i = 0; i < 3; ++i)
			for (int j = 0; j < 3; ++j)
			{
				m[i][j] = 0;
				for (int k = 0; k < 3; ++k)
					m[i][j] += t[i][k] * rz[k][j];
			}
	}

	void warp_matrix(const Pose &host, const Pose &mc, float out[3][3])
	{
		float rh[3][3], rm[3][3];
		camera_rotation(host, rh);
		camera_rotation(mc, rm);
		for (int i = 0; i < 3; ++i)
			for (int j = 0; j < 3; ++j)
			{
				out[i][j] = 0;
				for (int k = 0; k < 3; ++k)
					out[i][j] += rm[k][i] * rh[k][j];
			}
	}

	void set3(effect_runtime *runtime, const char *name, float a, float b, float c)
	{
		const effect_uniform_variable u = runtime->find_uniform_variable(kEffect, name);
		if (u.handle != 0)
			runtime->set_uniform_value_float(u, a, b, c);
	}

	void on_begin_effects(effect_runtime *runtime, command_list *, resource_view, resource_view)
	{
		const bool hostLive = read_host_pose();
		if (hostLive)
			upload(runtime);
		const bool on = hostLive && g_hasFrame;

		if (const effect_uniform_variable u = runtime->find_uniform_variable(kEffect, "McActive"); u.handle != 0)
			runtime->set_uniform_value_bool(u, on);
		if (!on)
			return;

		if (const effect_uniform_variable u = runtime->find_uniform_variable(kEffect, "McPlanes"); u.handle != 0)
			runtime->set_uniform_value_float(u, g_mcNear, g_mcFar, float(g_mcFlags));
		if (const effect_uniform_variable u = runtime->find_uniform_variable(kEffect, "HostPlanes"); u.handle != 0)
			runtime->set_uniform_value_float(u, g_hostPose.nearClip, g_hostPose.farClip);

		float m[3][3] = { {1,0,0},{0,1,0},{0,0,1} };
		float t[3] = { 0,0,0 };
		if (g_mcPose.valid)
		{
			warp_matrix(g_hostPose, g_mcPose, m);
			float rm[3][3];
			camera_rotation(g_mcPose, rm);
			const float d[3] = {
				float(g_hostPose.x - g_mcPose.x),
				float(g_hostPose.y - g_mcPose.y),
				float(g_hostPose.z - g_mcPose.z)
			};
			for (int i = 0; i < 3; ++i)
				t[i] = rm[0][i] * d[0] + rm[1][i] * d[1] + rm[2][i] * d[2];
		}

		set3(runtime, "WarpRow0", m[0][0], m[0][1], m[0][2]);
		set3(runtime, "WarpRow1", m[1][0], m[1][1], m[1][2]);
		set3(runtime, "WarpRow2", m[2][0], m[2][1], m[2][2]);
		set3(runtime, "WarpT", t[0], t[1], t[2]);

		const float d2r = 3.14159265f / 180.0f;
		const float tanHost = std::tan(g_hostPose.fov * d2r * 0.5f);
		const float tanMc = std::tan(g_mcPose.fov * d2r * 0.5f);
		set3(runtime, "WarpTan", tanHost, tanMc, float(g_width) / float(g_height));
	}

	void on_reloaded_effects(effect_runtime *runtime)
	{
		if (g_width != 0)
			bind(runtime);
	}

	void on_destroy_effect_runtime(effect_runtime *runtime)
	{
		destroy_layers(runtime->get_device());
	}
}

BOOL APIENTRY DllMain(HMODULE module, DWORD reason, LPVOID)
{
	switch (reason)
	{
	case DLL_PROCESS_ATTACH:
		if (!reshade::register_addon(module))
			return FALSE;
		reshade::register_event<reshade::addon_event::reshade_begin_effects>(on_begin_effects);
		reshade::register_event<reshade::addon_event::reshade_reloaded_effects>(on_reloaded_effects);
		reshade::register_event<reshade::addon_event::destroy_effect_runtime>(on_destroy_effect_runtime);
		break;
	case DLL_PROCESS_DETACH:
		g_frameMap.close();
		g_cameraMap.close();
		reshade::unregister_addon(module);
		break;
	}
	return TRUE;
}
