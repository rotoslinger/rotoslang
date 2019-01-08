cmake_minimum_required(VERSION 2.8)

include(RezBuild)
include(AL_CMakeLib)

SET(CMAKE_CXX_FLAGS "-std=c++11")

rez_find_packages(PREFIX pkgs AUTO)

set(source_files
	"src/pluginMain.cpp"
#	"LHRepulsorDeformer.cpp"
#	"LHRepulsorDeformer.h"
#	"LHGetDeformPoints.cpp"
#	"LHGetDeformPoints.h"
#	"LHTemplateNode.cpp"
#	"LHTemplateNode.h"
#	"LHTemplateDeformer.cpp"
#	"LHTemplateDeformer.h"
#	"LHWeightNode.cpp"
#	"LHWeightNode.h"
#	"LHMultiCluster.cpp"
#	"LHMultiCluster.h"
#	"LHComputeDeformer.cpp"
#	"LHComputeDeformer.h"
#	"splatDeformer.cpp"
#	"splatDeformer.h"
#	"sseDeformer.cpp"
#	"sseDeformer.h"
#	"LHMultiClusterThreaded.cpp"
#	"LHMultiClusterThreaded.h"
	"src/LHCollisionDeformer.cpp"
	"src/LHCollisionDeformer.h"
)

add_library(collision SHARED ${source_files})
set_target_properties(collision PROPERTIES PREFIX "")

link_directories(${stdlib_ROOT}/lib64)

target_link_libraries(collision ${maya_LIBRARIES} Foundation OpenMaya)

install(TARGETS collision DESTINATION plugins)
