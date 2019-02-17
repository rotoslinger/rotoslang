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
	"nullMatrixTransform.cpp"
	"nullMatrixTransform.h"
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
	"LHMultiWrap.h"
	"LHMultiWrap.cpp"


)



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

install(FILES "LHTemplateGPUDeformer.cl" DESTINATION plug-ins)