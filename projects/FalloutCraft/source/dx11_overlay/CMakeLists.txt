cmake_minimum_required(VERSION 3.21)
project(FalloutCraftDX11Overlay VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(COMMONLIBF4_PATH "" CACHE PATH "Path to CommonLibF4 source tree")
if(NOT COMMONLIBF4_PATH)
  message(FATAL_ERROR "COMMONLIBF4_PATH must point at a CommonLibF4 checkout")
endif()

if(NOT TARGET CommonLibF4)
  add_subdirectory("${COMMONLIBF4_PATH}" CommonLibF4)
endif()

find_package(spdlog REQUIRED CONFIG)

add_library(FalloutCraftDX11Overlay SHARED src/main.cpp)
target_compile_definitions(FalloutCraftDX11Overlay PRIVATE
  NOMINMAX
  WIN32_LEAN_AND_MEAN
  _UNICODE
  UNICODE
)
target_link_libraries(FalloutCraftDX11Overlay PRIVATE
  CommonLibF4::CommonLibF4
  spdlog::spdlog
  d3d11
  dxgi
  d3dcompiler
)

if(MSVC)
  target_compile_options(FalloutCraftDX11Overlay PRIVATE /utf-8 /EHsc /permissive-)
endif()

set_target_properties(FalloutCraftDX11Overlay PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/out"
  RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}/out"
)
