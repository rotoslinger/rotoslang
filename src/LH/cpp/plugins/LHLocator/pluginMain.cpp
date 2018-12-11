#include <maya/MFnPlugin.h>
#include "LHLocator.h"
#include "LHAimConstraint.h"

MStatus initializePlugin(MObject obj)
{
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHLocator",
                               LHLocator::id,
                               &LHLocator::creator,
                               &LHLocator::initialize,
                               MPxNode::kLocatorNode);
  status = plugin.registerNode("LHAimConstraint",
                               LHAimConstraint::id,
                               LHAimConstraint::creator,
                               LHAimConstraint::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj)
{
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHLocator::id);
  status = plugin.deregisterNode(LHAimConstraint::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}
