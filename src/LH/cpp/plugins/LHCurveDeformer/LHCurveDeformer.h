#ifndef _LHCURVEDEFORMER_H
#define _LHCURVEDEFORMER_H

#include <maya/MCppCompat.h>

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
#include <maya/MSyntax.h>
#include <maya/MFnNumericAttribute.h>

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
#include <iostream>
#include <algorithm>
#include <set>
#include <math.h>
#include <vector>
using namespace std;

#define PI 3.14159265

class LHCurveDeformer : public MPxDeformerNode {
 public:
  LHCurveDeformer() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& MitGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
//  virtual MStatus setDependentsDirty(MPlug const & inPlug,
//                                       MPlugArray  & affectedPlugs);
//
  static void* creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aCurve;
  static MObject aAimCurve;
  static MObject aCurveBase;
  static MObject aAimCurveBase;
// attributes
  static MObject aRotationAmount;
  static MObject aRevolveAmount;
  static MObject aFalloff;
  static MObject aScale;
  static MObject aMaintainVolume;
  static MObject aSlide;
  static MObject aLength;

// Weights
  static MObject aTranslateWeights;
  static MObject aLengthWeights;
  static MObject aRotationWeights;
  static MObject aRevolveWeights;
  static MObject aScaleWeights;
  static MObject aVolumeWeights;
  static MObject aSlideWeights;
  // ParamsParents
  static MObject aRotationWeightsParent;
  static MObject aRevolveWeightsParent;
  static MObject aScaleWeightsParent;
  static MObject aVolumeWeightsParent;
  static MObject aSlideWeightsParent;
  static MObject aCacheParams;
  static MObject aCacheWeights;
  static MObject aCacheBase;
  static MObject aContinuousSlide;

  //CacheObjects
  MDoubleArray rotationWeights;
  MDoubleArray revolveWeights;
  MDoubleArray scaleWeights;
  MDoubleArray volumeWeights;
  MDoubleArray slideWeights;
  MDoubleArray dummyWeights;



  vector <MDoubleArray> rotationWeightsArray;
  vector <MDoubleArray> revolveWeightsArray;
  vector <MDoubleArray> scaleWeightsArray;
  vector <MDoubleArray> volumeWeightsArray;
  vector <MDoubleArray> slideWeightsArray;

  MDoubleArray baseParams;
  MPointArray  baseClosestPts;
  MPointArray  aimCurveBaseClosestPts;

  vector <MDoubleArray> baseParamsArray;
  vector <MPointArray> baseClosestPtsArray;
  vector <MPointArray> aimBaseClosestPtsArray;


  MMatrixArray  baseMatrixArray;

  vector <MMatrixArray> baseMatrixVecArray;

  vector <MEulerRotation> baseEulerRotation;

  vector < vector <MEulerRotation> > baseEulerRotationArray;

    double MaxParam;
    double MinParam;
    float w;

    double rotationW;
    double revolveW;
    double scaleW;
    double volumeW;
    double slideW;


    double lengthDir;
    double slideParamValue;
    double slideCheck;

    double falloffWeight;
    double distance;
    double baseLength;
    double driveLength;
    double lengthParam;
    double lengthBaseParam;

    MPoint lengthPt, lengthBasePt, slidePoint, slidePt, slidePointBase, curveBasePt, aimCurveBasePt, driverPt, aimPt, dummyPoint;
    //Matrices
    MMatrix BaseMatrix, rotateMatrixX, rotateMatrixY, rotateMatrixZ, dummyMatrix;
    //EulerRotations
    MEulerRotation rotMatrix, DriveMatrixEuler, dummyEuler;
    //Vectors
    MVector slideVec, xBaseVector, baseVecCross, yBaseVector, zBaseVector, xAxisVec, vecCross, yAxisVec, zAxisVec, toCenterBase;

    float length, pLength, slideValue, lengthComp, lengthFinal, maintainVolume;

    double slideParam;
    double lengthCompensate;
    double lengthPoint;
    double stretchAmount;
    double stretchParam;
    double compensateParam;
    double slideVal;
    float slideTest;
    float compensate;
    int fixMIndex;
    int count;
    int indexPtCount;
    int index;
    int iterIndex;
    int iterGeoCount;
    vector<int> indexIntArray;
    int indicesLength;
    MIntArray indices;
    int numIndexTest;
    int numIndex;

    inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[LHCurveDeformer] " );
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

    ////////////////////////////////////////////////////////////
    ////////////////////getWeightValues/////////////////////////
    ////////////////////////////////////////////////////////////

    inline MStatus getPlugWeightValues(MObject &weightParent,MObject &weightChild,
                                           int MitGeoCount, int mIndex,
                                           MDoubleArray &returnWeightlist)
    {
        MStatus status;

        returnWeightlist.setLength(MitGeoCount) ;

        MObject thisNode = thisMObject();
        MPlug parent( thisNode, weightParent) ;
        double weight;
        MPlug parentElement = parent.elementByLogicalIndex(mIndex, &status);
        CheckStatusReturn( status, "Unable to get unable to get parentElement" );

        MPlug child = parentElement.child(weightChild, &status);
        CheckStatusReturn( status, "Unable to get unable to get child" );

        for (unsigned int i = 0; i < MitGeoCount; ++i)
        {
            MPlug childWeight = child.elementByLogicalIndex(i);
            status = childWeight.getValue(weight);
            if (status != MS::kSuccess)
            {
                returnWeightlist[i] = 1.0 ;
             }
            else
            {
                returnWeightlist[i] = weight;
            }
        }
        return status;
    }

};

///////////////////////////////////////////////////////////

#endif
