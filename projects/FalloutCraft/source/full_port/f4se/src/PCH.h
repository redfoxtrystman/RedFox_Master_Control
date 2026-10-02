#pragma once

#include <RE/Fallout.h>
#include <F4SE/F4SE.h>

#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>

#include <atomic>
#include <array>
#include <chrono>
#include <condition_variable>
#include <deque>
#include <functional>
#include <filesystem>
#include <algorithm>
#include <cfloat>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <memory>
#include <limits>
#include <mutex>
#include <shared_mutex>
#include <optional>
#include <span>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include <Windows.h>
#include <ShlObj_core.h>
#include <d3d11.h>
#include <dxgi.h>

namespace logger = spdlog;
using namespace std::literals;

// CommonLibSSE compatibility used by the imported SkyCraft host code.
namespace RE { using FormID = std::uint32_t; }
