//#include <maya/MCppCompat.h>
//#include <maya/MFnPlugin.h>
#include "LHKDoubleArrayToKFloatArray.h"

MStatus initializePlugin(MObject obj)
{
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHKDoubleArrayToKFloatArray",
                               LHKDoubleArrayToKFloatArray::id,
                               LHKDoubleArrayToKFloatArray::creator,
                               LHKDoubleArrayToKFloatArray::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj)
{
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHKDoubleArrayToKFloatArray::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}
