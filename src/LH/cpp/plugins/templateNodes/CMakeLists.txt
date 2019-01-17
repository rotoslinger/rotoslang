cmake_minimum_required(VERSION 2.8)

include(RezBuild)
include(AL_CMakeLib)
include ( ExternalProject )

SET(CMAKE_CXX_FLAGS "-std=c++11")

# must put find_package before rez_find_packages or will not work......
find_package(OpenGL REQUIRED)
if (OPENGL_FOUND)
	include_directories(${OPENGL_INCLUDE_DIR})
	link_libraries(${OPENGL_LIBRARIES})

endif()

rez_find_packages(PREFIX pkgs AUTO)

set(source_files
	"src/pluginMain.cpp"
	"src/locatorTemplate.cpp"
	"src/locatorTemplate.h"
)
#message( "BLAAAAAAAAAA" ${source_files})

add_library(template SHARED ${source_files})
set_target_properties(template PROPERTIES PREFIX "")

link_directories(${stdlib_ROOT}/lib64)
find_package(OpenMP)

target_link_libraries(template tbb clew cuda cudart ${maya_LIBRARIES} Foundation OpenMaya)

install(TARGETS template DESTINATION plugins)


