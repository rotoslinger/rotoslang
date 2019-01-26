#ifndef _LHSLIDEDEFORMER_H
#define _LHSLIDEDEFORMER_H

#include <maya/MDataBlock.h>
#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MFloatMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>
#include <maya/MVector.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MIOStream.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnMesh.h>
#include <maya/MMeshIntersector.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MNurbsIntersector.h>
#include <maya/MSyntax.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnGenericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MArgList.h>
#include <maya/MPlugArray.h>
#include <maya/MPlug.h>
#include <maya/MIntArray.h>
#include <maya/MMatrixArray.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnAnimCurve.h>
#include <maya/MTime.h>
#include <maya/MFloatArray.h>
#include <maya/MFloatVector.h>
#include <maya/MFloatPoint.h>
#include <iostream>
#include <algorithm>
#include <set>
#include <math.h>
#include <vector>
#include <numeric>
#include <valarray>
//#include <array>
//#include <sys>
//using namespace std;

#define PI 3.14159265

class LHSlideDeformer : public MPxDeformerNode {
 public:
  LHSlideDeformer() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& MitGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  virtual MStatus getAnimCurves(MObject &thisMObj,
                                MObject &animCurveParent, MObject &animCurveChild,
                                std::vector <float> &returnTimeLength,
                                std::vector <float> &returnTimeOffset,
                                std::vector <MFnAnimCurve*> &returnAnimCurve);
  static void* creator();
  static MStatus initialize();
 
  static MTypeId id;
  // tAttrs
  static MObject aSurface;
  static MObject aSurfaceBase;
  static MObject aWeightMesh;

  static MObject aBaseGeo;
  static MObject aBaseGeoParent;
  static MObject aUseBaseGeo;

  // nAttrs
  static MObject aRotationAmount;
  static MObject aScaleAmount;
  static MObject aCacheWeights;
  static MObject aCacheParams;
  static MObject aCacheWeightMesh;
  static MObject aCacheWeightCurves;
  static MObject aCacheBase;
  // others
  static MObject aUValue;
  static MObject aUValueParent;
  static MObject aUWeights;
  static MObject aUWeightsParent;
  static MObject aUWeightsParentArray;
  static MObject aUAnimCurveU;
  static MObject aUAnimCurveUParent;
  static MObject aUAnimCurveV;
  static MObject aUAnimCurveVParent;
  static MObject aVValue;
  static MObject aVValueParent;
  static MObject aVWeights;
  static MObject aVWeightsParent;
  static MObject aVWeightsParentArray;
  static MObject aVAnimCurveU;
  static MObject aVAnimCurveUParent;
  static MObject aVAnimCurveV;
  static MObject aVAnimCurveVParent;
  static MObject aNValue;
  static MObject aNValueParent;
  static MObject aNWeights;
  static MObject aNWeightsParent;
  static MObject aNWeightsParentArray;
  static MObject aNAnimCurveU;
  static MObject aNAnimCurveUParent;
  static MObject aNAnimCurveV;
  static MObject aNAnimCurveVParent;

  // Global cache vars
//  std::array <int,2>t;

  // tmpVectors

  // rot cache paran cache
  std::vector < MPointArray > rotatePivots, slideUVBasePt;
  std::vector < std::vector < double > > rotUParams, rotVParams,
                                         slideUBasePtParam, slideVBasePtParam;
  std::vector < std::vector < std::vector < MDoubleArray > > > allWeightsArray, allOutWeightsArray;
//  std::vector < std::vector < std::vector < MDoubleArray > > > newAllWeightsArray;
//  std::vector < std::vector < std::vector < std::vector < MDoubleArray > > > > allWeightsArray;

  // weightMesh cache

//  std::vector <float> tmpUCoord,tmpVCoord;
  std::vector < std::vector < float > > uCoord,vCoord;

//  std::vector <bool> tmpIntersectYN;
  std::vector < std::vector < bool > > intersectYN;

  // animCurve cache
  std::vector < std::vector < std::vector < MFnAnimCurve* > > > allUFnCurvesArray,
  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	allVFnCurvesArray;

  std::vector < std::vector < std::vector < float > > > allUTimeOffsetArray,
  	  	  	  	  	  	  	  	  	  	  	  	  	  	allUTimeLengthArray,
										   			    allVTimeOffsetArray,
													    allVTimeLengthArray;


  std::vector < std::vector < std::vector < std::vector < double > > > > allUAnimCurveWeights,allVAnimCurveWeights;

  // base cache
  std::vector < MMatrixArray > rotMatrix;
  std::vector < std::vector < MEulerRotation > > baseEuler;


  // index check
  std::vector < int > indexIntArray;
  MIntArray indices;
  int indicesLength,numIndex;

  // misc
  unsigned int weightMeshCheck, success, rotatePivotsLength, iterGeoCount,
  i, j, k, idx, ii;




////////////////////////////////////////////////////////////////////
////////       loop variables     ////////
////////////////////////////////////////////////////////////////////

// pointers
  double fnUParam, fnVParam, fnUMinParam, fnUMaxParam, fnVMinParam, fnVMaxParam,
  U, V, fakeDouble3, fnMinParam, fnMaxParam, uParam, vParam, tmpU, tmpV,
  tempW, tempVal, uW, vW, nW, rW, slideUBasePointParam, slideVBasePointParam,
  slideUValue, slideVValue, slideUCheck, slideVCheck, allURotVals,allVRotVals,
  rotSlideUValue, rotSlideVValue, uPivOffset, vPivOffset,pivotU, pivotV,
  uMinParam, uMaxParam, vMinParam, vMaxParam;

//  double fnUParam, fnVParam

  float u, v, curveW, w;

  float2 uvCoord;

  bool hitYN;

  MPoint slideUVPoint, tmpSlideUVPoint, fakePt, resultPt, intersectPoint,
  weightPt, paramPoint, pt;

  MVector fakePt2, fnUVec, fnVVec, fakeVecU, fakeVecV, xAxisVec, yAxisVec,
  zAxisVec, xVecBase, yVecBase, zVecBase, slideVVec, slideUVec, slideNormal, normal;

  MMatrix BaseMatrix, DriveMatrix, weightMatrix, rotateMatrix, rotateMatrixX,
  rotateMatrixY, rotateMatrixZ, finalMatrix;
;
  MQuaternion rotateX, rotateY, rotateZ;
  MEulerRotation rotateEuler;
};

inline MString FormatError( const MString &msg, const MString
                              &sourceFile, const int &sourceLine ) 
{
    MString txt( "[LHSlideDeformer] " );
    txt += msg ; 
    txt += ", File: "; 
    txt += sourceFile; 
    txt += " Line: "; 
    txt += sourceLine; 
    return txt; 
}
#define Error( msg ) \
    { \
    MString __txt = FormatError( msg, __FILE__, __LINE__ ); \
    MGlobal::displayError( __txt ); \
    cerr << endl << "Error: " << __txt; \
    } \

#define CheckBool( result ) \
    if( !(result) ) \
        { \
        Error( #result ); \
        }

#define CheckStatus( stat, msg ) \
    if( !stat ) \
        { \
        Error( msg ); \
        } 

#define CheckObject( obj, msg ) \
    if(obj.isNull() ) \
        { \
        Error( msg ); \
        } 

#define CheckStatusReturn( stat, msg ) \
    if( !stat ) \
        { \
        Error( msg ); \
        return stat; \
        } 




#endif
