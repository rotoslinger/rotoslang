//==============================================================
/// Ultra simple deformer to be used as a starter template//////
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

  float env = data.inputValue(envelope).asFloat();
  float amount = data.inputValue(aAmount).asFloat();
  amount *= env;

  MPoint pt;
  float w = 0.0f;
  for (; !itGeo.isDone(); itGeo.next()) {
    // Get the input geometry point
    pt = itGeo.position();
    // Get the painted weight value
    w = weightValue(data, mIndex, itGeo.index());
    // Just translate in x
    MVector direction(1.0, 0.0, 0.0);
    pt = pt + (direction * amount * w);
    itGeo.setPosition(pt);
  }

  return MS::kSuccess;
}

