#include <maya/MCppCompat.h>
#define _MApiVersion

#include <maya/MFnPlugin.h>
#include "LHRepulsorDeformer.h"


MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  // Specify we are making a deformer node
  status = plugin.registerNode("LHRepulsorDeformer", LHRepulsorDeformer::id, LHRepulsorDeformer::creator,
                               LHRepulsorDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHRepulsorDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}