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
#include <maya/MFnNurbsCurve.h>

#include <maya/MNurbsIntersector.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>

#include <maya/MPxDeformerNode.h>
#include <vector>
#include <string>

class LHCurveRollSimple : public MPxDeformerNode {
 public:
  LHCurveRollSimple() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  virtual MStatus CacheDeformPointMembership(MDataBlock& data);
  virtual MStatus getWeights(MDataBlock &data, int mIndex, MDoubleArray &rDoubleArray, MObject weightObject);
  virtual MStatus CacheClosestPoints();
//   virtual MStatus CacheBaseRotations();
  virtual MStatus GetAllBaseGeoIter(MDataBlock &data);
  virtual void ClearCachedData();
  // virtual void Algorithm(int mIndex, int idx, MDoubleArray rollWeights, MDoubleArray vWeights, int currentVertID, MPoint &pt, float amount);
  static void* creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aRollAmount;
  static MObject aVAmount;
  static MObject aRotationAmount;
  static MObject aSurface;
  static MObject aSurfaceBase;
  static MObject aCacheBind;
  // static MObject aUValue;
  // static MObject aVValue;
  static MObject aRollWeights;
  static MObject aVWeights;
  static MObject aBaseGeo;
  static MObject aBaseGeoParent;
  static MObject aMembershipWeight;
  static MObject aWeightArray;
  static MObject aRollCurve;



  std::vector <MIntArray> deformedVertIds;
  std::vector <MDoubleArray> slideUParam, slideVParam;
  std::vector <MPointArray> closestPointArray;
  std::vector <MVectorArray> closestTangentArray;
  std::vector <MItGeometry*> allGeoIter;
  MDoubleArray rollWeights;
  MDoubleArray vWeights;
  MPointArray currentGeoPoints;
  MPoint currentPt, closestPoint;
  MFnNurbsCurve* fnCurve;
  MFnNurbsSurface* fnSurface;
  MFnNurbsSurface* fnSurfaceBase;

  MObject oCurve;
  MObject oSurface;
  MObject oSurfaceBase;
  MPointOnNurbs ptON;
  MPoint UV;
  std::vector < std::vector < MEulerRotation > > baseEuler;
  MVector xVec, yVec, zVec, normal, yVector, zVector, xVector;
  MEulerRotation rotateEuler;
  MMatrix BaseMatrix, rotateMatrixX, rotateMatrixY, rotateMatrixZ, finalMatrix;
  double  uMinParam,uMaxParam,vMinParam,vMaxParam, closestParam;
  MPoint slideUVPoint;
  MVector fnUVec, fnVVec, slideVVec, slideUVec, closestTangent;
  inline MString FormatError( const MString &msg, const MString
                              &sourceFile, const int &sourceLine )
  {
      MString txt( "[LHCurveRollSimple] " );
      txt += msg ;
      txt += ", File: ";
      txt += sourceFile;
      txt += " Line: ";
      txt += sourceLine;
      return txt;
  }

};
