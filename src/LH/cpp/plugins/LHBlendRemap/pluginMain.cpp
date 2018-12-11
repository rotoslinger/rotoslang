#include <maya/MFnPlugin.h>
#include "LHBlendRemap.h"

MStatus initializePlugin(MObject obj)
{
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHBlendRemap", LHBlendRemap::id, LHBlendRemap::creator,
                               LHBlendRemap::initialize);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj)
{
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHBlendRemap::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}
