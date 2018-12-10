#include <maya/MFnPlugin.h>
#include "LHSlideDeformer.h"

MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHSlideDeformer", LHSlideDeformer::id, LHSlideDeformer::creator,
                               LHSlideDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHSlideDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

