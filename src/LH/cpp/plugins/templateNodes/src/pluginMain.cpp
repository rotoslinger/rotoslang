// #include <maya/MCppCompat.h>
#define _MApiVersion

#include <maya/MFnPlugin.h>
#include "locatorTemplate.h"
static bool sUseLegacyDraw = (getenv("MAYA_ENABLE_VP2_PLUGIN_LOCATOR_LEGACY_DRAW") != NULL);


MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "levih", "1.0", "Any");

  status = plugin.registerNode("locatorTemplate",
                                locatorTemplate::id,
                                locatorTemplate::creator,
                                locatorTemplate::initialize,
                                MPxNode::kLocatorNode,
                                &locatorTemplate::drawDbClassification);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  if (!sUseLegacyDraw)
  {
    status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(
            locatorTemplate::drawDbClassification,
            locatorTemplate::drawRegistrantId,
            locatorTemplateOverride::creator);
    CHECK_MSTATUS_AND_RETURN_IT(status);
  }

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);


  if (!sUseLegacyDraw)
  {
    status = MDrawRegistry::deregisterGeometryOverrideCreator(
            locatorTemplate::drawDbClassification,
            locatorTemplate::drawRegistrantId);
  }


  status = plugin.deregisterNode( locatorTemplate::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);


  return status;
}


// MStatus initializePlugin(MObject obj)
// {
//     MStatus status;
//     MFnPlugin plugin(obj, PLUGIN_COMPANY, "3.0", "Any");
//     // status = plugin.registerNode(
//     //     "LHCollisionLocator",
//     //     LHCollisionLocator::id,
//     //     &LHCollisionLocator::creator,
//     //     &LHCollisionLocator::initialize,
//     //     MPxNode::kLocatorNode,
//     //     sUseLegacyDraw ? NULL : &LHCollisionLocator::drawDbClassification);
//     if (!status)
//     {
//         status.perror("registerNode");
//         return status;
//     }
//     if (!sUseLegacyDraw)
//     {
//         status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(
//             LHCollisionLocator::drawDbClassification,
//             LHCollisionLocator::drawRegistrantId,
//             LHCollisionLocatorDrawOverride::Creator);
//         if (!status)
//         {
//             status.perror("registerDrawOverrideCreator");
//             return status;
//         }
//     }
//     return status;
// }
// MStatus uninitializePlugin(MObject obj)
// {
//     MStatus status;
//     MFnPlugin plugin(obj);
//     if (!sUseLegacyDraw)
//     {
//         status = MHWRender::MDrawRegistry::deregisterDrawOverrideCreator(
//             LHCollisionLocator::drawDbClassification,
//             LHCollisionLocator::drawRegistrantId);
//         if (!status)
//         {
//             status.perror("deregisterDrawOverrideCreator");
//             return status;
//         }
//     }
//     status = plugin.deregisterNode(LHCollisionLocator::id);
//     if (!status)
//     {
//         status.perror("deregisterNode");
//         return status;
//     }
//     return status;
// }