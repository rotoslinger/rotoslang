#ifndef _RNKCURVEDEFORMER_H
#define _RNKCURVEDEFORMER_H

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

class rnkCurveDeformer : public MPxDeformerNode {
 public:
  rnkCurveDeformer() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& MitGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
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
};

inline MString MyFormatError( const MString &msg, const MString 
                              &sourceFile, const int &sourceLine ) 
{
    MString txt( "[rnkCurveDeformer] " );
    txt += msg ; 
    txt += ", File: "; 
    txt += sourceFile; 
    txt += " Line: "; 
    txt += sourceLine; 
    return txt; 
}
#define MyError( msg ) \
    { \
    MString __txt = MyFormatError( msg, __FILE__, __LINE__ ); \
    MGlobal::displayError( __txt ); \
    cerr << endl << "Error: " << __txt; \
    } \

#define MyCheckBool( result ) \
    if( !(result) ) \
        { \
        MyError( #result ); \
        }

#define MyCheckStatus( stat, msg ) \
    if( !stat ) \
        { \
        MyError( msg ); \
        } 

#define MyCheckObject( obj, msg ) \
    if(obj.isNull() ) \
        { \
        MyError( msg ); \
        } 

#define MyCheckStatusReturn( stat, msg ) \
    if( !stat ) \
        { \
        MyError( msg ); \
        return stat; \
        } 

////////////////////////////////////////////////////////////
////////////////////getWeightValues/////////////////////////
////////////////////////////////////////////////////////////


//Set Param values
MStatus getWeightValues(MDataBlock &data, MObject &weightParent, MObject &weightChild, int MitGeoCount, int mIndex, MDoubleArray &returnWeightlist)
{
	MStatus status ;
    // Make your weight list the same size as your weight children
	returnWeightlist.setLength(MitGeoCount) ;	
	int index=0;
	// Get weight parent array handle
	MArrayDataHandle ahWeightParent = data.inputArrayValue(weightParent, &status) ;

	// go to the right geo index
	status = ahWeightParent.jumpToElement( mIndex ) ;
        // If this doesn't exist, weights don't exist yet, so set all to 1 and send it back
	if (status != MS::kSuccess)
	{
	    for (index=0; index < MitGeoCount; ++index) 
	    {
	    returnWeightlist[index] = 1.0 ;
        }
	    return status ;
    }

	// Get weight parent data handle
	MDataHandle dhWeightParent = ahWeightParent.inputValue(&status) ;
    // If this doesn't exist, weights don't exist yet, so set all to 1 and send it back
	if (status != MS::kSuccess)
	{
	    for (index=0; index < MitGeoCount; ++index) 
	    {
		    returnWeightlist[index] = 1.0 ;
        }
		return status ;
	}
	// get child handle
	MDataHandle dhWeightChild = dhWeightParent.child( weightChild ) ;
	// get child array handle
	MArrayDataHandle ahWeightChild (dhWeightChild, &status) ;
	if (status != MS::kSuccess)
		{
		return status ;
		}
	// go through all children, get their weight value, and put it into the return weight list
	for (index=0; index < MitGeoCount; ++index)
		{
		status = ahWeightChild.jumpToElement(index) ;
        //If element doesn't exist yet set it to 1
		if (status != MS::kSuccess)
			returnWeightlist[index] = 1.0 ;
		else
			{
			MDataHandle dhWeight = ahWeightChild.inputValue(&status) ;
			if (status != MS::kSuccess)
			{
                //if weight hasn't been set yet for this point set to 1
				returnWeightlist[index] = 1.0 ;
				}
			else
				returnWeightlist[index] = dhWeight.asDouble() ; 
			}
		}

	return MS::kSuccess ;
}

////////////////////////////////////////////////////////
////////////////////getDagNodes/////////////////////////
////////////////////////////////////////////////////////

inline MDagPath getConnectedDagNode(MObject &oThis, MObject &attrArg )
{
    MPlug plugArg( oThis, attrArg );
    MDagPath dagPath;
    if( plugArg.isConnected() ) {
        MPlugArray plugArr;
        plugArg.connectedTo( plugArr, true, false );
        MPlug plugDag( plugArr[0] );
        MFnDagNode fnDagNode(plugDag.node());
        fnDagNode.getPath( dagPath );
	return dagPath;
    }
    else {
        MDagPath dagPath;
        return dagPath;
    }

}
///////////////////////////////////////////////////////////

#endif
