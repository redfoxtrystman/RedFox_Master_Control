#include "Game.h"
#include "Collision.h"

namespace
{
    constexpr auto kName = "FalloutCraft"sv;

    void OnMessage(F4SE::MessagingInterface::Message* a_msg)
    {
        if (!a_msg) {
            return;
        }
        switch (a_msg->type) {
        case F4SE::MessagingInterface::kInputLoaded:
            falloutcraft::Input::Install();
            break;
        case F4SE::MessagingInterface::kGameDataReady:
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
    v.PluginVersion({ 0, 5, 5, 0 });
    v.PluginName("FalloutCraft");
    v.AuthorName("RedFox");
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

extern "C" __declspec(dllexport) bool F4SEAPI F4SEPlugin_Query(
    const F4SE::QueryInterface* a_f4se, F4SE::PluginInfo* a_info)
{
    a_info->infoVersion = F4SE::PluginInfo::kVersion;
    a_info->name = kName.data();
    a_info->version = 505;
    return !a_f4se->IsEditor();
}

extern "C" __declspec(dllexport) bool F4SEAPI F4SEPlugin_Load(const F4SE::LoadInterface* a_f4se)
{
    F4SE::Init(a_f4se, { .log = true, .trampoline = true, .trampolineSize = 1024 });
    logger::info("FalloutCraft 0.5.5 full-port host loading");

    if (!falloutcraft::Link::Get().Create()) {
        logger::critical("FalloutCraft: shared-memory link creation failed");
        return false;
    }

    auto* messaging = F4SE::GetMessagingInterface();
    if (messaging) {
        messaging->RegisterListener(OnMessage);
    }

    falloutcraft::Collision::Get().Start();
    falloutcraft::Game::Install();
    falloutcraft::Overlay::Install();
    falloutcraft::WorldRender::Install();
    falloutcraft::CrashLog::Install();
    falloutcraft::Launcher::StartMinecraft();

    logger::info("FalloutCraft full-port host loaded");
    return true;
}
