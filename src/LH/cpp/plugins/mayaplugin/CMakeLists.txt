# OSX terminal build in build dir: cmake -G "Unix Makefiles" -DMAYA_VERSION=2018 ..
cmake_minimum_required(VERSION 3.13)
project(LHDeformerNodes)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)

add_subdirectory(src)