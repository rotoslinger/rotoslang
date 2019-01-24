// #include <maya/MCppCompat.h>
#define _MApiVersion

#include <maya/MFnPlugin.h>
// #include "LHRepulsorDeformer.h"
// #include "LHGetDeformPoints.h"
// #include "LHTemplateNode.h"
// #include "LHWeightNode.h"
// #include "LHTemplateDeformer.h"
// #include "LHMultiCluster.h"
// #include "LHComputeDeformer.h"
// #include "splatDeformer.h"
// #include "sseDeformer.h"
// #include "LHMultiClusterThreaded.h"
#include "LHCollisionDeformer.h"
#include "LHLocator.h"
#include "LHCollisionLocator.h"
#include "nullTransform.h"
#include "nullMatrixTransform.h"
static bool sUseLegacyDraw = (getenv("MAYA_ENABLE_VP2_PLUGIN_LOCATOR_LEGACY_DRAW") != NULL);


MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

//  // Specify we are making a deformer node
//  status = plugin.registerNode("LHRepulsorDeformer", LHRepulsorDeformer::id, LHRepulsorDeformer::creator,
//                               LHRepulsorDeformer::initialize, MPxNode::kDeformerNode);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.registerNode("LHGetDeformPoints", LHGetDeformPoints::id, LHGetDeformPoints::creator, LHGetDeformPoints::initialize);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.registerNode("LHTemplateNode", LHTemplateNode::id, LHTemplateNode::creator, LHTemplateNode::initialize);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.registerNode("LHWeightNode", LHWeightNode::id, LHWeightNode::creator, LHWeightNode::initialize);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.registerNode("LHTemplateDeformer", LHTemplateDeformer::id, LHTemplateDeformer::creator,
//                               LHTemplateDeformer::initialize, MPxNode::kDeformerNode);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.registerNode("LHMultiCluster", LHMultiCluster::id, LHMultiCluster::creator,
//		  	  	  	  	  	   LHMultiCluster::initialize, MPxNode::kDeformerNode);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.registerNode("LHComputeDeformer", LHComputeDeformer::id, LHComputeDeformer::creator,
//		  	  	  	  	  	   LHComputeDeformer::initialize, MPxNode::kDeformerNode);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//  status = plugin.registerNode( "splatDeformer", splatDeformer::id, splatDeformer::creator,
//                                                            splatDeformer::initialize, MPxNode::kDeformerNode );
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.registerNode( "sseDeformer", sseDeformer::id, sseDeformer::creator,
//		  sseDeformer::initialize, MPxNode::kDeformerNode );
//
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.registerNode( "LHMultiClusterThreaded", LHMultiClusterThreaded::id, LHMultiClusterThreaded::creator,
//		  LHMultiClusterThreaded::initialize, MPxNode::kDeformerNode );
//
//  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode( "LHCollisionDeformer", LHCollisionDeformer::id, LHCollisionDeformer::creator,
		  LHCollisionDeformer::initialize, MPxNode::kDeformerNode );
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerTransform( "nullTransform",
                                    nullTransform::id,
                                    &nullTransform::creator,
                                    &nullTransform::initialize,
                                    nullTMatrix::creator,
                                    nullTMatrix::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerTransform( "nullMatrixTransform",
                                    nullMatrixTransform::id,
                                    &nullMatrixTransform::creator,
                                    &nullMatrixTransform::initialize,
                                    nullMatrixTMatrix::creator,
                                    nullMatrixTMatrix::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);


  status = plugin.registerNode( "LHLocator", LHLocator::id, LHLocator::creator,
		  LHLocator::initialize, MPxNode::kLocatorNode );
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHCollisionLocator",
                                LHCollisionLocator::id,
                                LHCollisionLocator::creator,
                                LHCollisionLocator::initialize,
                                MPxNode::kLocatorNode,
                                &LHCollisionLocator::drawDbClassification);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  if (!sUseLegacyDraw)
  {
    status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(
            LHCollisionLocator::drawDbClassification,
            LHCollisionLocator::drawRegistrantId,
            LHCollisionLocatorOverride::creator);
    CHECK_MSTATUS_AND_RETURN_IT(status);
  }

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

//  status = plugin.deregisterNode(LHRepulsorDeformer::id);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.deregisterNode(LHGetDeformPoints::id);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.deregisterNode(LHTemplateNode::id);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.deregisterNode(LHWeightNode::id);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.deregisterNode(LHMultiCluster::id);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.deregisterNode(LHComputeDeformer::id);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//  status = plugin.deregisterNode(splatDeformer::id);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.deregisterNode(sseDeformer::id);
//  CHECK_MSTATUS_AND_RETURN_IT(status);
//
//  status = plugin.deregisterNode(LHMultiClusterThreaded::id);
//  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.deregisterNode(LHCollisionDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.deregisterNode(LHLocator::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.deregisterNode(nullTransform::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.deregisterNode(nullMatrixTransform::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);


  if (!sUseLegacyDraw)
  {
    status = MDrawRegistry::deregisterGeometryOverrideCreator(
            LHCollisionLocator::drawDbClassification,
            LHCollisionLocator::drawRegistrantId);
  }


  status = plugin.deregisterNode( LHCollisionLocator::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);


  return status;
}


// MStatus initializePlugin(MObject obj)
// {
//     MStatus status;
//     MFnPlugin plugin(obj, PLUGIN_COMPANY, "3.0", "Any");
//     // status = plugin.registerNode(
//     //     "LHCollisionLocator",
//     //     LHCollisionLocator::id,
//     //     &LHCollisionLocator::creator,
//     //     &LHCollisionLocator::initialize,
//     //     MPxNode::kLocatorNode,
//     //     sUseLegacyDraw ? NULL : &LHCollisionLocator::drawDbClassification);
//     if (!status)
//     {
//         status.perror("registerNode");
//         return status;
//     }
//     if (!sUseLegacyDraw)
//     {
//         status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(
//             LHCollisionLocator::drawDbClassification,
//             LHCollisionLocator::drawRegistrantId,
//             LHCollisionLocatorDrawOverride::Creator);
//         if (!status)
//         {
//             status.perror("registerDrawOverrideCreator");
//             return status;
//         }
//     }
//     return status;
// }
// MStatus uninitializePlugin(MObject obj)
// {
//     MStatus status;
//     MFnPlugin plugin(obj);
//     if (!sUseLegacyDraw)
//     {
//         status = MHWRender::MDrawRegistry::deregisterDrawOverrideCreator(
//             LHCollisionLocator::drawDbClassification,
//             LHCollisionLocator::drawRegistrantId);
//         if (!status)
//         {
//             status.perror("deregisterDrawOverrideCreator");
//             return status;
//         }
//     }
//     status = plugin.deregisterNode(LHCollisionLocator::id);
//     if (!status)
//     {
//         status.perror("deregisterNode");
//         return status;
//     }
//     return status;
// }