#include <maya/MCppCompat.h>
#include <maya/MFnPlugin.h>
#include "rnkRollNode.h"

MStatus initializePlugin(MObject obj)
{
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("rnkRollNode", rnkRollNode::id, rnkRollNode::creator,
                               rnkRollNode::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj)
{
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(rnkRollNode::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}
