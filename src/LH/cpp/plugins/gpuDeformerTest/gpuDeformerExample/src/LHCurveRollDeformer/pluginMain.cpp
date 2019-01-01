#include <maya/MCppCompat.h>

#include <maya/MFnPlugin.h>
#include "LHCurveRollDeformer.h"

MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHCurveRollDeformer", LHCurveRollDeformer::id, LHCurveRollDeformer::creator,
                               LHCurveRollDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHCurveRollDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

