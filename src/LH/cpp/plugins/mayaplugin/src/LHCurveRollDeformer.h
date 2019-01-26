#ifndef _LHCURVEROLLDEFORMER_H
#define _LHCURVEROLLDEFORMER_H

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
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnGenericAttribute.h>
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

class LHCurveRollDeformer : public MPxDeformerNode {
 public:
  LHCurveRollDeformer() {};
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

  static MObject aVecCurve;
  static MObject aOutCurve;
  static MObject aInCurve;
  static MObject aBaseGeo;
  static MObject aBaseGeoParent;
  static MObject aUseBaseGeo;

  // nAttrs

  static MObject aAlignToCurve;
  static MObject aCacheWeights;
  static MObject aCacheWeightMesh;
  static MObject aCacheWeightCurves;
  static MObject aCacheParams;
  static MObject aCacheTangents;

  static MObject aRValue;
  static MObject aRValueParent;
  static MObject aRWeights;
  static MObject aRWeightsParent;
  static MObject aRWeightsParentArray;
  static MObject aRAnimCurveU;
  static MObject aRAnimCurveUParent;
  static MObject aRAnimCurveV;
  static MObject aRAnimCurveVParent;
  static MObject aRPivot;
  static MObject aRPivotArray;


  // Global cache vars
//  std::array <int,2>t;

  // tmpVectors

  // rot cache paran cache
//  std::vector < MPointArray > rotatePivots;

  std::vector < std::vector < MDoubleArray > > closestParam;
  std::vector < std::vector < MVectorArray > > closestTangent;
//  std::vector < std::vector < MPoint > > closestPoint;

  std::vector < std::vector < MPointArray > > closestPoint;



  std::vector < std::vector < std::vector < MDoubleArray > > > allWeightsArray;

  // weightMesh cache

//  std::vector <float> tmpUCoord,tmpVCoord;
  std::vector < std::vector < float > > uCoord,vCoord;


  // animCurve cache
  std::vector < std::vector < std::vector < MFnAnimCurve* > > > allUFnCurvesArray,
  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	allVFnCurvesArray;

  std::vector < std::vector < std::vector < MVector > > > allPivots;
  std::vector < std::vector < std::vector < MPoint > > > allPivotPositions;

  std::vector < std::vector <std::vector < MFnNurbsCurve* > > > curves;

  std::vector < std::vector < std::vector < float > > > allUTimeOffsetArray,
  	  	  	  	  	  	  	  	  	  	  	  	  	  	allUTimeLengthArray,
										   			    allVTimeOffsetArray,
													    allVTimeLengthArray;


  std::vector < std::vector < std::vector < std::vector < double > > > > allUAnimCurveWeights,allVAnimCurveWeights;


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
  rotVectorUValue, rotVectorVValue, uPivOffset, vPivOffset,pivotU, pivotV,
  uMinParam, uMaxParam, vMinParam, vMaxParam;

//  double fnUParam, fnVParam

  float u, v, curveW, w;

  float2 uvCoord;

  bool hitYN;

  MPoint slideUVPoint, tmpVectorUVPoint, fakePt, resultPt, intersectPoint,
  weightPt, paramPoint, pt;

  MVector fakePt2, fnUVec, fnVVec, fakeVecU, fakeVecV, xAxisVec, yAxisVec,
  zAxisVec, xVecBase, yVecBase, zVecBase, slideVVec, slideUVec, slideNormal;

  MMatrix BaseMatrix, DriveMatrix, weightMatrix, rotateMatrix, rotateMatrixX,
  rotateMatrixY, rotateMatrixZ;
  MQuaternion rotateX, rotateY, rotateZ;
  inline MString FormatError( const MString &msg, const MString
                                &sourceFile, const int &sourceLine )
  {
      MString txt( "[LHCurveRollDeformer] " );
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

//  inline MStatus getPlugWeightValues(MObject &weightParent,MObject &weightChild,
//                                         int MitGeoCount, int mIndex,
//                                         MDoubleArray &returnWeightlist)
//  {
//      MStatus status;
//      returnWeightlist.setLength(MitGeoCount) ;
//
//      MObject thisNode = thisMObject();
//      MPlug parent( thisNode, weightParent) ;
//      double weight;
//      MPlug parentElement = parent.elementByLogicalIndex(mIndex, &status);
//      CheckStatusReturn( status, "Unable to get unable to get parentElement" );
//
//      MPlug child = parentElement.child(weightChild, &status);
//      CheckStatusReturn( status, "Unable to get unable to get child" );
//
//      for (unsigned int i = 0; i < MitGeoCount; ++i)
//      {
//          MPlug childWeight = child.elementByLogicalIndex(i);
//          status = childWeight.getValue(weight);
//          if (status != MS::kSuccess)
//          {
//              returnWeightlist[i] = 1.0 ;
//           }
//          else
//          {
//              returnWeightlist[i] = weight;
//          }
//      }
//      return status;
//  }
};


//inline MStatus getPlugWeightValues(MObjectArray &weightParentArray,
//                                   MObjectArray &weightParent,
//                                   MObjectArray &weightChild,
//                                   int MitGeoCount,
//                                   int mIndex,
//                                   std::vector < std::vector < std::vector < MDoubleArray > > > &returnWeightlist)
//{
//    MStatus status;
//    returnWeightlist.setLength(MitGeoCount) ;
//
//    MObject thisNode = thisMObject();
//    MPlug parent( thisNode, weightParent) ;
//    double weight;
//    MPlug parentElement = parent.elementByLogicalIndex(mIndex, &status);
//    CheckStatusReturn( status, "Unable to get unable to get parentElement" );
//
//    MPlug child = parentElement.child(weightChild, &status);
//    CheckStatusReturn( status, "Unable to get child" );
//
//    for (unsigned int i = 0; i < MitGeoCount; ++i)
//    {
//        MPlug childWeight = child.elementByLogicalIndex(i);
//        status = childWeight.getValue(weight);
//        if (status != MS::kSuccess)
//        {
//            returnWeightlist[i] = 1.0 ;
//         }
//        else
//        {
//            returnWeightlist[i] = weight;
//        }
//    }
//    return status;
//}



#endif
