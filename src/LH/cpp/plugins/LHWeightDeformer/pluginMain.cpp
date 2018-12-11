#include <maya/MCppCompat.h>

#include <maya/MFnPlugin.h>
#include "LHWeightDeformer.h"

MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHWeightDeformer", LHWeightDeformer::id, LHWeightDeformer::creator,
                               LHWeightDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHWeightDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

