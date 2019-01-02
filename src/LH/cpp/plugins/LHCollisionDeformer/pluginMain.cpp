#include <maya/MCppCompat.h>
#define _MApiVersion

#include <maya/MFnPlugin.h>
#include "LHCollisionDeformer.h"


MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  // Specify we are making a deformer node
  status = plugin.registerNode("LHCollisionDeformer", LHCollisionDeformer::id, LHCollisionDeformer::creator,
                               LHCollisionDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHCollisionDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}