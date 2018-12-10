#ifndef LHNURBSBLEND_H
#define LHNURBSBLEND_H
#include <maya/MCppCompat.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MNurbsIntersector.h>

#include <maya/MFnMesh.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MPxDeformerNode.h>

#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>
#include <maya/MMatrixArray.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnGenericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MGlobal.h>


#include <iostream>
#include <algorithm>
#include <set>
#include <math.h>
#include <vector>
#include <numeric>
#include <valarray>
//#include <string>
//#include <sstream>
//#include <iostream>
//using namespace std;

class LHNurbsBlend : public MPxDeformerNode {
 public:
  LHNurbsBlend() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  virtual MStatus pushbackNurbsParams(MObject &oSurfaceBase,
                                      int &numIndex,
									  MArrayDataHandle &geomArrayHandle,
									  std::vector <MPointArray> &slideUVBasePt,
									  int &cacheParamsAmt,
									  std::vector < std::vector < double > > &slideUBasePtParam,
									  std::vector < std::vector < double > > &slideVBasePtParam,
									  MObject &childGeom);


  static void* creator();
  static MStatus initialize();
 
  static MTypeId id;
  static MObject aBlendOldMesh;
  static MObject aBlendWeight;
  static MObject aSurface;
  static MObject aSurfaceBase;
  static MObject aCacheParams;
  static MObject aCacheBase;

  static MObject aTargetGeo;
  static MObject aTargetGeoParent;
  static MObject aUseBaseGeo;

  static MObject aBaseMesh;
  static MObject aBaseMeshParent;

  static MObject aBlendAttr;
  static MObject aBlendAttrParent;


  std::vector < MMatrixArray > rotMatrix;
  std::vector < std::vector < MEulerRotation > > baseEuler;


  std::vector < MPointArray > rotatePivots, slideUVBasePt, slideUVTargetPt;

  // index check
  std::vector < int > indexIntArray;
  MIntArray indices;
  int indicesLength,numIndex;
  // misc
  unsigned int weightMeshCheck, success, rotatePivotsLength, iterGeoCount,
  i, j, k, idx, ii;

  std::vector < std::vector < double > > rotUParams, rotVParams,
                                         slideUBasePtParam, slideVBasePtParam,
										 slideUTargetPtParam, slideVTargetPtParam;
  MPoint slideUVPoint, tmpSlideUVPoint, fakePt, resultPt, intersectPoint,
  weightPt, paramPoint, pt;
  double fnUParam, fnVParam, fnUMinParam, fnUMaxParam, fnVMinParam, fnVMaxParam,
  U, V, fakeDouble3, fnMinParam, fnMaxParam, uParam, vParam, tmpU, tmpV,
  tempW, tempVal, uW, vW, nW, rW, slideUBasePointParam, slideVBasePointParam,
  slideUValue, slideVValue, slideUCheck, slideVCheck, allURotVals,allVRotVals,
  rotSlideUValue, rotSlideVValue, uPivOffset, vPivOffset,pivotU, pivotV,
  uMinParam, uMaxParam, vMinParam, vMaxParam;

  MVector fakePt2, fnUVec, fnVVec, fakeVecU, fakeVecV, xAxisVec, yAxisVec,
  zAxisVec, xVecBase, yVecBase, zVecBase, slideVVec, slideUVec, slideNormal, normal;

  MMatrix BaseMatrix, DriveMatrix, weightMatrix, rotateMatrix, rotateMatrixX,
  rotateMatrixY, rotateMatrixZ, finalMatrix;

  MQuaternion rotateX, rotateY, rotateZ;
  MEulerRotation rotateEuler;
};

#endif
