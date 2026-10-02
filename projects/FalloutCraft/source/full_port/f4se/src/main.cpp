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

F4SEPluginLoad(const F4SE::LoadInterface* a_skse)
{
	F4SE::Init(a_skse, { .trampoline = true, .trampolineSize = 1024 });
	SetupLog();
	falloutcraft::CrashLog::Install();
	logger::info("FalloutCraft {} loading (runtime {})", "0.1.2", a_skse->RuntimeVersion().string());
	F4SE::GetMessagingInterface()->RegisterListener(OnMessage);
	// As early as possible: Minecraft takes about as long to start as Fallout does to reach its menu.
	falloutcraft::Launcher::StartMinecraft();
	return true;
}
