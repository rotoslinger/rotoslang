#pragma once
#include "matrixCommon.h"

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
#include <maya/MMeshIntersector.h>
#include <maya/MFnPointArrayData.h>
#include <maya/MFloatPointArray.h>

#include <vector>

#include <maya/MPxDeformerNode.h>

class LHMultiWrap : public MPxDeformerNode {
 public:
  LHMultiWrap() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  virtual MStatus getMeshes(MArrayDataHandle inputsArrayHandle, int inputCount, MObjectArray& oDriverMeshArray, int debug);
  virtual MStatus storeBindData(MArrayDataHandle inputsArrayHandle, int inputCount, MIntArray& vertIDArray, MObjectArray& oDriverMeshArray, int cache, int debug);
  // virtual MStatus getBindData(MArrayDataHandle inputsArrayHandle, int inputCount, int cache, int debug);
  virtual MStatus getBindData(MDataBlock& data, std::vector <MFnMesh*> inputFnMeshArray, MFnMesh* fnBaseMesh,
                                   MArrayDataHandle inputsArrayHandle, int inputCount, MObjectArray& oDriverMeshArray,
                                    int vertCount, float thresholdAmt, int cache, int debug);


  static void *creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aThresholdAmount;
  static MObject aCacheClosest;
  static MObject aInputGeo;
  static MObject aInputParent;
  static MObject aBaseMesh;
  static MObject aBindVertexIDArray;
  static MObject aDebug;

  static MObject aBindPolyIDArray;
  static MObject aBindTriangleIDArray;
  static MObject aBaryCoordsArray;

  std::vector <MIntArray> vertIndexArray;
  std::vector <MIntArray> storedVertIndexArray;

  std::vector <MIntArray> polyIndexArray;
  std::vector <MIntArray> storedPolyIndexArray;

  std::vector <MIntArray> triangleIndexArray;
  std::vector <MIntArray> storedTriangleIndexArray;

  std::vector <MPointArray> baryCoordsArray;
  std::vector <MPointArray> storedBaryCoordsArray;
  
  MMeshIntersector fnWeightIntersector;
  MPointOnMesh ptOnMesh;
  MPoint pt;
  MPoint pointOnPoint;
  int polyID;
  int triangleID;
  int trianglePointIDs[3];
};
