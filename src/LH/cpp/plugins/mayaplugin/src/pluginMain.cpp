// #include <maya/MCppCompat.h>
#define _MApiVersion
#include "formatErrorMacros.h"
#include "LHCurveWeightUtils.h"

#include <maya/MFnPlugin.h>
// #include "LHRepulsorDeformer.h"
// #include "LHGetDeformPoints.h"
// #include "LHTemplateNode.h"
#include "LHWeightNode.h"
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
#include "LHGeometryConstraint.h"
#include "LHSlideDeformer.h"
#include "LHVectorDeformer.h"
#include "LHCurveRollDeformer.h"
#include "LHCurveWeightNode.h"
#include "LHKDoubleArrayToKFloatArray.h"
#include "LHWeightNodeFloat.h"
#include "LHTemplateGPUDeformer.h"
#include "nullMatrixTransform.h"
#include "LHMultiWrap.h"
#include "LHSlideSimple.h"
#include "LHNakedLocator.h"
#include "LHMatrixDeformer.h"
#include "LHBlendshapeSimple.h"
#include "LHCurveDeformer.h"
#include "LHVectorDeformerSimple.h"
#include "LHCurveRollSimple.h"
#include "LHCurveTransform.h"
#include "LHCurveWeightNode_2.h"

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

 status = plugin.registerNode( "LHVectorDeformerSimple", LHVectorDeformerSimple::id, LHVectorDeformerSimple::creator,
		  LHVectorDeformerSimple::initialize, MPxNode::kDeformerNode );

 status = plugin.registerNode( "LHCurveRollSimple", LHCurveRollSimple::id, LHCurveRollSimple::creator,
		  LHCurveRollSimple::initialize, MPxNode::kDeformerNode );

 status = plugin.registerNode( "LHCurveDeformer", LHCurveDeformer::id, LHCurveDeformer::creator,
		  LHCurveDeformer::initialize, MPxNode::kDeformerNode );

 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.registerNode( "LHMatrixDeformer", LHMatrixDeformer::id, LHMatrixDeformer::creator,
		  LHMatrixDeformer::initialize, MPxNode::kDeformerNode );

 CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode(
            "identity" ,
            identityNode::id ,
            &identityNode::creator ,
            &identityNode::initialize ,
            MPxNode::kDeformerNode
            );
  CHECK_MSTATUS_AND_RETURN_IT(status);

  MString nodeClassName("identity");
  MString registrantId("mayaPluginExample");
  MGPUDeformerRegistry::registerGPUDeformerCreator(
      nodeClassName,
      registrantId,
      identityGPUDeformer::getGPUDeformerInfo()
      );
  identityGPUDeformer::pluginLoadPath = plugin.loadPath();


  status = plugin.registerNode("LHCurveTransform",
                               LHCurveTransform::id,
                               LHCurveTransform::creator,
                               LHCurveTransform::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);


  status = plugin.registerNode("LHWeightNodeFloat",
                               LHWeightNodeFloat::id,
                               LHWeightNodeFloat::creator,
                               LHWeightNodeFloat::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHWeightNode", LHWeightNode::id, LHWeightNode::creator, LHWeightNode::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHKDoubleArrayToKFloatArray",
                               LHKDoubleArrayToKFloatArray::id,
                               LHKDoubleArrayToKFloatArray::creator,
                               LHKDoubleArrayToKFloatArray::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHCurveWeightNode", LHCurveWeightNode::id, LHCurveWeightNode::creator, LHCurveWeightNode::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHCurveWeightNode_2", LHCurveWeightNode_2::id, LHCurveWeightNode_2::creator, LHCurveWeightNode_2::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHCurveRollDeformer", LHCurveRollDeformer::id, LHCurveRollDeformer::creator,
                               LHCurveRollDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHBlendshapeSimple", LHBlendshapeSimple::id, LHBlendshapeSimple::creator,
                               LHBlendshapeSimple::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);


  status = plugin.registerNode("LHMultiWrap", LHMultiWrap::id, LHMultiWrap::creator,
                               LHMultiWrap::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHSlideSimple", LHSlideSimple::id, LHSlideSimple::creator,
                               LHSlideSimple::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);


  status = plugin.registerNode("LHSlideDeformer", LHSlideDeformer::id, LHSlideDeformer::creator,
                               LHSlideDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHVectorDeformer", LHVectorDeformer::id, LHVectorDeformer::creator,
                               LHVectorDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.registerNode("LHGeometryConstraint", LHGeometryConstraint::id, LHGeometryConstraint::creator, LHGeometryConstraint::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);


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

  status = plugin.registerNode("LHNakedLocator",
                                LHNakedLocator::id,
                                LHNakedLocator::creator,
                                LHNakedLocator::initialize,
                                MPxNode::kLocatorNode,
                                &LHNakedLocator::drawDbClassification);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  if (!sUseLegacyDraw)
  {
    status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(
            LHNakedLocator::drawDbClassification,
            LHNakedLocator::drawRegistrantId,
            LHNakedLocatorOverride::creator);
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
 status = plugin.deregisterNode(LHVectorDeformerSimple::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHCurveRollSimple::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHCurveDeformer::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHBlendshapeSimple::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHMatrixDeformer::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHWeightNodeFloat::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);


 status = plugin.deregisterNode(LHWeightNode::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.deregisterNode(LHKDoubleArrayToKFloatArray::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHCurveWeightNode::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHCurveWeightNode_2::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);


 status = plugin.deregisterNode(LHCurveRollDeformer::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHMultiWrap::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHSlideSimple::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHVectorDeformer::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

 status = plugin.deregisterNode(LHGeometryConstraint::id);
 CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.deregisterNode(LHCollisionDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.deregisterNode(LHLocator::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = plugin.deregisterNode(nullTransform::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  status = plugin.deregisterNode(LHCurveTransform::id);
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

  status = plugin.deregisterNode(LHSlideDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  MString nodeClassName("identity");
  MString registrantId("mayaPluginExample");
  MGPUDeformerRegistry::deregisterGPUDeformerCreator(
      nodeClassName,
      registrantId
      );

  status = plugin.deregisterNode( identityNode::id );
  CHECK_MSTATUS_AND_RETURN_IT(status);

  if (!sUseLegacyDraw)
  {
    status = MDrawRegistry::deregisterGeometryOverrideCreator(
            LHNakedLocator::drawDbClassification,
            LHNakedLocator::drawRegistrantId);
  }


  status = plugin.deregisterNode( LHNakedLocator::id);
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