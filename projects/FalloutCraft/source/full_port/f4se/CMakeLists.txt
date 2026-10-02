cmake_minimum_required(VERSION 3.25)
project(FalloutCraft VERSION 0.5.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")

set(COMMONLIBF4_PATH "" CACHE PATH "Path to CommonLibF4 source tree")
if(NOT COMMONLIBF4_PATH)
  message(FATAL_ERROR "COMMONLIBF4_PATH must point at CommonLibF4")
endif()
if(NOT TARGET CommonLibF4)
  add_subdirectory("${COMMONLIBF4_PATH}" CommonLibF4)
endif()

find_package(spdlog REQUIRED CONFIG)

# The complete SkyCraft-derived source remains in src/ for reference/adaptation.
# The Fallout runtime target uses the Fallout-native compatibility implementations below.
set(FALLOUTCRAFT_SOURCES
  src/Link.cpp
  src/Launcher.cpp
  src/CompatMain.cpp
  src/CompatGame.cpp
  src/CompatInput.cpp
  src/CompatRenderer.cpp
  src/CompatCollision.cpp
  src/CompatSubsystems.cpp
)
add_library(FalloutCraft SHARED ${FALLOUTCRAFT_SOURCES})
target_include_directories(FalloutCraft PRIVATE src ${CMAKE_CURRENT_SOURCE_DIR}/../protocol)
target_precompile_headers(FalloutCraft PRIVATE src/PCH.h)
target_compile_definitions(FalloutCraft PRIVATE NOMINMAX WIN32_LEAN_AND_MEAN)
target_link_libraries(FalloutCraft PRIVATE
  CommonLibF4::CommonLibF4
  spdlog::spdlog
  d3d11
  d3dcompiler
  dxgi
  ole32
  oleaut32
)
if(MSVC)
  target_compile_options(FalloutCraft PRIVATE /W4 /permissive- /Zc:preprocessor /utf-8 /MP /wd4200 /wd4100 /wd4189)
  target_link_options(FalloutCraft PRIVATE /DEBUG:FULL)
endif()
set_target_properties(FalloutCraft PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/out"
  RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}/out"
)
