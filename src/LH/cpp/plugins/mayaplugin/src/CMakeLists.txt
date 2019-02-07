cmake_minimum_required(VERSION 3.8)

set(SOURCE_FILES
	"pluginMain.cpp"
#	"LHRepulsorDeformer.cpp"
#	"LHRepulsorDeformer.h"
#	"LHGetDeformPoints.cpp"
#	"LHGetDeformPoints.h"
#	"LHTemplateNode.cpp"
#	"LHTemplateNode.h"
#	"LHTemplateDeformer.cpp"
#	"LHTemplateDeformer.h"
	"LHWeightNode.cpp"
	"LHWeightNode.h"
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
	"LHCollisionDeformer.cpp"
	"LHCollisionDeformer.h"
	"LHLocator.cpp"
	"LHLocator.h"
	"LHCollisionLocator.cpp"
	"LHCollisionLocator.h"
	"constants.h"
	"nullTransform.cpp"
	"nullTransform.h"
#	"nullMatrixTransform.cpp"
#	"nullMatrixTransform.h"
	"LHGeometryConstraint.cpp"
	"LHGeometryConstraint.h"
	"LHSlideDeformer.cpp"
	"LHSlideDeformer.h"
	"LHVectorDeformer.cpp"
	"LHVectorDeformer.h"
	"LHCurveRollDeformer.cpp"
	"LHCurveRollDeformer.h"
	"LHCurveWeightNode.cpp"
	"LHCurveWeightNode.h"
	"LHKDoubleArrayToKFloatArray.cpp"
	"LHKDoubleArrayToKFloatArray.h"
	"LHWeightNodeFloat.cpp"
	"LHWeightNodeFloat.h"
	"LHTemplateGPUDeformer.cpp"
	"LHTemplateGPUDeformer.h"
	"LHTemplateGPUDeformer.cl"


)

#set(CMAKE_C_COMPILER clang-omp CACHE STRING "C compiler" FORCE)
#set(CMAKE_CXX_COMPILER clang-omp++ CACHE STRING "C++ compiler" FORCE)
#
#find_package(OpenMP REQUIRED)
#
#set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
#set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS}
#${OpenMP_EXE_LINKER_FLAGS}")

#include_directories("/Users/leviharrison/Desktop/dev/openmp/build/runtime/src")
#include_directories("/usr/local/include")
#include_directories("/usr/local/Cellar/llvm/3.4.2/include")

# Test find openMP
#find_package(OpenMP)
#if (OPENMP_FOUND)
#    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
#    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
#    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
#endif()


find_package(OpenGL REQUIRED)
if (OPENGL_FOUND)
	include_directories(${OPENGL_INCLUDE_DIR})
	link_libraries(${OPENGL_LIBRARIES})

endif()
#OPENGL


find_package(Maya REQUIRED)

include_directories(${MAYA_INCLUDE_DIR})
include_directories(${MAYA_LIBRARY_DIR})

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${MAYA_LIBRARIES})

MAYA_PLUGIN(${PROJECT_NAME})