#pragma once
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>

#include <maya/MFnMesh.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnIntArrayData.h>
#include <maya/MObjectArray.h>
#include <vector>

#include <maya/MPxDeformerNode.h>

class LHMultiWrap : public MPxDeformerNode {
 public:
  LHMultiWrap() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  static void* creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aAmount;
  static MObject aCacheClosest;
  static MObject aInputGeo;
  static MObject aInputParent;
  static MObject aBaseMesh;
  static MObject aBindVertexIDArray;

  std::vector <MIntArray> vertIndexArray;
  std::vector <MIntArray> storedVertIndexArray;

};
