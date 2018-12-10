#include <maya/MFnPlugin.h>
#include "LHVectorDeformer.h"

MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHVectorDeformer", LHVectorDeformer::id, LHVectorDeformer::creator,
                               LHVectorDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHVectorDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

