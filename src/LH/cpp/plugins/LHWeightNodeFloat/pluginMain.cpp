//#include <maya/MCppCompat.h>
//#include <maya/MFnPlugin.h>
#include "LHWeightNodeFloat.h"

MStatus initializePlugin(MObject obj)
{
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHWeightNodeFloat",
                               LHWeightNodeFloat::id,
                               LHWeightNodeFloat::creator,
                               LHWeightNodeFloat::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj)
{
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHWeightNodeFloat::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}
