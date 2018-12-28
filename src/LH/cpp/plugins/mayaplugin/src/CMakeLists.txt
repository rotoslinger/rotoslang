cmake_minimum_required(VERSION 3.13)

set(SOURCE_FILES
	"pluginMain.cpp"
	"LHRepulsorDeformer.cpp"
	"LHRepulsorDeformer.h"
)

find_package(Maya REQUIRED)

include_directories(${MAYA_INCLUDE_DIR})
include_directories(${MAYA_LIBRARY_DIR})

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${MAYA_LIBRARIES})


MAYA_PLUGIN(${PROJECT_NAME})