#include <maya/MFnPlugin.h>
#include "LHUVBlendshape.h"

MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHUVBlendshape", LHUVBlendshape::id, LHUVBlendshape::creator,
                               LHUVBlendshape::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHUVBlendshape::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

