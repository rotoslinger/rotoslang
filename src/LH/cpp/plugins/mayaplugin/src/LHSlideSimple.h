#pragma once
#if defined _WIN32  || defined _WIN64
#define NOMINMAX
#endif

#include "formatErrorMacros.h"
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>

#include <maya/MFnMesh.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnGenericAttribute.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MNurbsIntersector.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>

#include <maya/MPxDeformerNode.h>
#include <vector>

class LHSlideSimple : public MPxDeformerNode {
 public:
  LHSlideSimple() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  virtual MStatus CacheDeformPointMembership(MDataBlock& data);
  virtual MStatus getWeights(MDataBlock &data, int mIndex, MDoubleArray &rDoubleArray);
  virtual MStatus CacheClosestPoints();
  virtual MStatus CacheBaseRotations();
  virtual MStatus GetAllBaseGeoIter(MDataBlock &data);
  virtual void ClearCachedData();
  // virtual void Algorithm(int mIndex, int idx, MDoubleArray uWeights, MDoubleArray vWeights, int currentVertID, MPoint &pt, float amount);
  static void* creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aUAmount;
  static MObject aVAmount;
  static MObject aRotationAmount;
  static MObject aSurface;
  static MObject aSurfaceBase;
  static MObject aCacheBind;
  // static MObject aUValue;
  // static MObject aVValue;
  static MObject aUWeights;
  static MObject aVWeights;
  static MObject aBaseGeo;
  static MObject aBaseGeoParent;
  static MObject aMembershipWeight;
  static MObject aWeightArray;
  std::vector <MIntArray> deformedVertIds;
  std::vector <MDoubleArray> slideUParam, slideVParam;
  std::vector <MPointArray> closestPointArray;
  std::vector <MItGeometry*> allGeoIter;
  MDoubleArray uWeights;
  MDoubleArray vWeights;
  MPointArray currentGeoPoints;
  MPoint currentPt;
  MFnNurbsSurface* fnSurface;
  MFnNurbsSurface* fnSurfaceBase;
  MObject oSurface;
  MObject oSurfaceBase;
  MPointOnNurbs ptON;
  MPoint UV;
  std::vector < std::vector < MEulerRotation > > baseEuler;
  MVector xVec, yVec, zVec, normal, yVector, zVector, xVector;
  MEulerRotation rotateEuler;
  MMatrix BaseMatrix, rotateMatrixX, rotateMatrixY, rotateMatrixZ, finalMatrix;
  double  uMinParam,uMaxParam,vMinParam,vMaxParam;
  MPoint slideUVPoint;
  MVector fnUVec, fnVVec, slideVVec, slideUVec;
  inline MString FormatError( const MString &msg, const MString
                              &sourceFile, const int &sourceLine )
  {
      MString txt( "[LHSlideSimple] " );
      txt += msg ;
      txt += ", File: ";
      txt += sourceFile;
      txt += " Line: ";
      txt += sourceLine;
      return txt;
  }

};
