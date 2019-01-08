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

  return status;
}

