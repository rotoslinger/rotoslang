# WINDOWS cmake -G "Visual Studio 15 2017" -DMAYA_VERSION=2018 .. 
# OSX terminal build in build dir: cmake -G "Unix Makefiles" -DMAYA_VERSION=2018 ..
cmake_minimum_required(VERSION 3.1.3)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)  # not necessary, but encouraged


project(LHDeformerNodes)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)


add_subdirectory(src)
