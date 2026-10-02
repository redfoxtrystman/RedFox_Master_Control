#include "Dig.h"
#include "Game.h"

namespace
{
	std::optional<std::filesystem::path> GetLogDirectory()
	{
		wchar_t* docsRaw = nullptr;
		if (FAILED(::SHGetKnownFolderPath(FOLDERID_Documents, KF_FLAG_DEFAULT, nullptr, &docsRaw))) {
			if (docsRaw) {
				::CoTaskMemFree(docsRaw);
			}
			return std::nullopt;
		}
		std::filesystem::path docs(docsRaw);
		::CoTaskMemFree(docsRaw);
		return docs / "My Games" / "Fallout4" / "F4SE";
	}

	void SetupLog()
	{
		auto dir = GetLogDirectory();
		if (!dir) {
			return;
		}
		std::error_code ec;
		std::filesystem::create_directories(*dir, ec);
		auto path = *dir / "FalloutCraft.log";
		auto sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(path.string(), true);
		auto log = std::make_shared<spdlog::logger>("global", std::move(sink));
		log->set_level(spdlog::level::info);
		log->flush_on(spdlog::level::info);
		spdlog::set_default_logger(std::move(log));
		spdlog::set_pattern("[%H:%M:%S.%e] [%l] %v");
	}

	void OnMessage(F4SE::MessagingInterface::Message* a_msg)
	{
		switch (a_msg->type) {
		case F4SE::MessagingInterface::kGameDataReady:
			if (!falloutcraft::Link::Get().Create()) {
				logger::error("FalloutCraft disabled: could not create shared memory");
				return;
			}
			falloutcraft::Game::Install();
			falloutcraft::Input::Install();
			falloutcraft::Overlay::Install();
			falloutcraft::WorldRender::Install();
			falloutcraft::PathAvoid::Install();
			falloutcraft::Dig::Install();
			falloutcraft::CrashLog::Install();
			break;
		case F4SE::MessagingInterface::kPostLoadGame:
		case F4SE::MessagingInterface::kNewGame:
			falloutcraft::Game::OnGameLoaded();
			break;
		default:
			break;
		}
	}
}

F4SE_PLUGIN_VERSION = []() noexcept {
	F4SE::PluginVersionData v{};
	v.PluginVersion({ 0, 5, 0, 0 });
	v.PluginName("FalloutCraft");
	v.AuthorName("FalloutCraft");
	v.UsesAddressLibraryNG(true);
	v.UsesAddressLibraryAE(true);
	v.UsesSigScanning(false);
	v.IsLayoutDependentNG(true);
	v.IsLayoutDependentAE(true);
	v.CompatibleVersions({
		F4SE::RUNTIME_1_10_163,
		F4SE::RUNTIME_1_10_980,
		F4SE::RUNTIME_1_10_984,
		F4SE::RUNTIME_LATEST,
		REL::Version{ 1, 11, 240, 0 },
	});
	return v;
}();

extern "C" DLLEXPORT bool F4SEAPI F4SEPlugin_Query(
	const F4SE::QueryInterface* a_f4se,
	F4SE::PluginInfo* a_info)
{
	a_info->infoVersion = F4SE::PluginInfo::kVersion;
	a_info->name = "FalloutCraft";
	a_info->version = 0x00050000;
	return !a_f4se->IsEditor();
}

extern "C" DLLEXPORT bool F4SEAPI F4SEPlugin_Load(const F4SE::LoadInterface* a_f4se)
{
	SetupLog();
	F4SE::Init(a_f4se, { .log = false, .trampoline = true, .trampolineSize = 1024 });
	falloutcraft::CrashLog::Install();
	logger::info("FalloutCraft 0.5.0 full-port loading (runtime {})", a_f4se->RuntimeVersion().string());

	auto* messaging = F4SE::GetMessagingInterface();
	if (!messaging || !messaging->RegisterListener(OnMessage)) {
		logger::critical("FalloutCraft: failed to register F4SE messaging listener");
		return false;
	}

	// Start Minecraft as early as possible; takeover itself waits for game data and a loaded player.
	falloutcraft::Launcher::StartMinecraft();
	return true;
}
