//==============================================================
// Ultra simple deformer to be used as a starter template//////
// In commented out lines you can see steps involved in trying to get as much speed as possible
// such as not getting painted weight values on every iteration
// Tried putting all positions into an array and setting all positions at once
// because it is supposed to be faster, but this was actually 3fps slower on a mesh of 39,000 points...
// also, not setting pt to a variable, just doing the whole algorithm in one step was 2 fps faster
// If weights are needed, they should be gathered outside the main loop
// and even cached into a std::vector <MFloatArray> with a boolean attribute to turn caching on and off
//==============================================================

#include "LHTemplateDeformer.h"
#include <maya/MFnPlugin.h>

MTypeId LHTemplateDeformer::id(0x00008467);
MObject LHTemplateDeformer::aAmount;

MStatus LHTemplateDeformer::initialize() {
  MFnNumericAttribute nAttr;

  aAmount = nAttr.create("amount", "amnt", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  addAttribute(aAmount);
  attributeAffects(aAmount, outputGeom);

  // Make the deformer weights paintable
  MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer LHTemplateDeformer weights;");

  return MS::kSuccess;
}

void* LHTemplateDeformer::creator() { return new LHTemplateDeformer; }

MStatus LHTemplateDeformer::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;

//  float env = data.inputValue(envelope).asFloat();
  float amount = data.inputValue(aAmount).asFloat();
//  amount *= env;

//MPoint pt;
  //float w = 0.0f;
  //MPointArray allPoints;
  MVector direction(1.0, 0.0, 0.0);

  for (; !itGeo.isDone(); itGeo.next()) {
    // Get the input geometry point
    // Get the painted weight value
//    w = weightValue(data, mIndex, itGeo.index());
    // Just translate in x
    itGeo.setPosition(itGeo.position() + (direction * amount));
  }
  //itGeo.setAllPositions(allPoints);
  return MS::kSuccess;
}

