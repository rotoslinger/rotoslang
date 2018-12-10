#ifndef _LHWEIGHTDEFORMER_H
#define _LHWEIGHTDEFORMER_H
#include <maya/MCppCompat.h>

#include <maya/MDataBlock.h>
#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>
#include <maya/MVector.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MIOStream.h>
#include <maya/MFnMesh.h>
#include <maya/MMeshIntersector.h>
#include <maya/MSyntax.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>

#include <maya/MFnDoubleArrayData.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MArgList.h>
#include <maya/MPlugArray.h>
#include <maya/MPlug.h>
#include <maya/MIntArray.h>
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


class LHWeightDeformer : public MPxDeformerNode {
 public:
  LHWeightDeformer() {};
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
  static MObject aWeightMesh;
  // nAttrs
  static MObject aCacheWeights;
  static MObject aCacheWeightMesh;
  static MObject aCacheWeightCurves;

  // others
  static MObject aWeights;
  static MObject aWeightsParent;
  static MObject aWeightsParentArray;
  static MObject aUAnimCurve;
  static MObject aUAnimCurveParent;
  static MObject aVAnimCurve;
  static MObject aVAnimCurveParent;
  static MObject aCacheOutWeights;
  static MObject aOutWeights;
  static MObject aOutWeightsParent;
  static MObject aOutWeightsParentArray;

  // Global cache vars
//  std::array <int,2>t;

  // tmpVectors

  // rot cache paran cache
  std::vector < std::vector < std::vector < MDoubleArray > > > allWeightsArray;
  std::vector < std::vector < std::vector < MDoubleArray > > > allOutWeightsArray;
  // weightMesh cache

//  std::vector <float> tmpUCoord,tmpVCoord;
  std::vector < std::vector < float > > uCoord,vCoord;


  // animCurve cache
  std::vector < std::vector < std::vector < MFnAnimCurve* > > > allUFnCurvesArray,
                                                                allVFnCurvesArray;

  std::vector < std::vector < std::vector < float > > > allUTimeOffsetArray,
                                                        allUTimeLengthArray,
                                                        allVTimeOffsetArray,
                                                        allVTimeLengthArray;


  std::vector < std::vector < std::vector < std::vector < double > > > > allUAnimCurveWeights,
                                                                         allVAnimCurveWeights;


  // index check
  std::vector < int > indexIntArray;
  MIntArray indices;
  int indicesLength,numIndex;

  // misc
  unsigned int weightMeshCheck, success, iterGeoCount,
  i, j, k, idx, ii;



////////////////////////////////////////////////////////////////////
////////       loop variables     ////////
////////////////////////////////////////////////////////////////////

// pointers
  double U, V, fakeDouble3, uParam, vParam, tmpU, tmpV, tempW, tempVal;
//  double fnUParam, fnVParam

  float u, v, curveW, w, allW;

  float2 uvCoord;

  MPoint fakePt, resultPt, weightPt, paramPoint, pt;

};

inline MString FormatError( const MString &msg, const MString
                              &sourceFile, const int &sourceLine ) 
{
    MString txt( "[LHWeightDeformer] " );
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
