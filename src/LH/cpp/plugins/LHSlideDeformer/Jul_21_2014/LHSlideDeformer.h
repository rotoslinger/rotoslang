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
#include <maya/MFnNurbsSurface.h>
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
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnAnimCurve.h>
#include <maya/MTime.h>
#include <iostream>
#include <algorithm>
#include <set>
#include <math.h>
#include <vector>
//#include <sys>
using namespace std;

#define PI 3.14159265

class LHSlideDeformer : public MPxDeformerNode {
 public:
  LHSlideDeformer() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& MitGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  static void* creator();
  static MStatus initialize();
 
  static MTypeId id;
  static MObject aSurface;
  static MObject aSurfaceBase;
  static MObject aWeightPatch;
  static MObject aRotationAmount;
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

//  vector <float> returnAnimCurve;
//  vector <float> returnTimeOffset;
//  vector <float> returnTimeLength;

//  //CacheObjects
//  MDoubleArray rotationWeights;
//  MDoubleArray revolveWeights;
//  MDoubleArray scaleWeights;
//  MDoubleArray volumeWeights;
//  MDoubleArray slideWeights;
//  MDoubleArray dummyWeights;
//
//
//
//
//
//
//
//  vector <MDoubleArray> rotationWeightsArray;
//  vector <MDoubleArray> revolveWeightsArray;
//  vector <MDoubleArray> scaleWeightsArray;
//  vector <MDoubleArray> volumeWeightsArray;
//  vector <MDoubleArray> slideWeightsArray;
//
//  MDoubleArray baseParams;
//  MPointArray  baseClosestPts;
//  MPointArray  aimCurveBaseClosestPts;
//
//  vector <MDoubleArray> baseParamsArray;
//  vector <MPointArray> baseClosestPtsArray;
//  vector <MPointArray> aimBaseClosestPtsArray;
//
//
//  MMatrixArray  baseMatrixArray;
//
//  vector <MMatrixArray> baseMatrixVecArray;
//
//  vector <MEulerRotation> baseEulerRotation;
//
//  vector < vector <MEulerRotation> > baseEulerRotationArray;
//
//    double MaxParam;
//    double MinParam;
//    float w;
//
//    double rotationW;
//    double revolveW;
//    double scaleW;
//    double volumeW;
//    double slideW;
//
//
//    double lengthDir;
//    double slideParamValue;
//    double slideCheck;
//
//    double falloffWeight;
//    double distance;
//    double baseLength;
//    double driveLength;
//    double lengthParam;
//    double lengthBaseParam;
//
//    MPoint lengthPt, lengthBasePt, slidePoint, slidePt, slidePointBase, curveBasePt, aimCurveBasePt, driverPt, aimPt, dummyPoint;
//    //Matrices
//    MMatrix BaseMatrix, rotateMatrixX, rotateMatrixY, rotateMatrixZ, dummyMatrix;
//    //EulerRotations
//    MEulerRotation rotMatrix, DriveMatrixEuler, dummyEuler;
//    //Vectors
//    MVector slideVec, xBaseVector, baseVecCross, yBaseVector, zBaseVector, xAxisVec, vecCross, yAxisVec, zAxisVec, toCenterBase;
//
//    float length, pLength, slideValue, lengthComp, lengthFinal, maintainVolume;
//
//
//    double slideParam;
//    double lengthCompensate;
//    double lengthPoint;
//    double stretchAmount;
//    double stretchParam;
//    double compensateParam;
//    double slideVal;
//    float slideTest;
//    float compensate;
//    int fixMIndex;
//    int count;
//    int indexPtCount;
//    int index;
//    int iterIndex;
//    int iterGeoCount;
//    vector<int> indexIntArray;
//    int indicesLength;
//    MIntArray indices;
//    int numIndexTest;
//    int numIndex;
};

inline MString MyFormatError( const MString &msg, const MString 
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
inline MDagPath getCurveArrayDagNode(MObject &oThis, MPlug &attrArg ){
    MPlug plugArg = attrArg;
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


////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////// get mfnNurbsCurves ////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////

///// get anim curves for weighting
inline MPointArray getMfnNurbsCurves(MObject &oThis, MDataBlock &data, MObject &thisNode,
                                     MObject &curveParent, MObject &curveChild){
	MPointArray returnPoints;
    MPlug parentPlug(thisNode, curveParent );
//    int count = parentPlug.numConnectedChildren();
    MIntArray curveIndex;
    parentPlug.getExistingArrayAttributeIndices(curveIndex);
    int indexLength = curveIndex.length();
	int index=0;
	for (index=0; index < indexLength; ++index){
        MPlug childPlug = parentPlug.connectionByPhysicalIndex(curveIndex[index]);
        MPlug oChild = childPlug.child(0);
//        float dummy = oChild.asFloat();
        MDagPath fnCurvePath = getCurveArrayDagNode(oThis,oChild);
        MDagPath dagPathCurve;
        fnCurvePath.getPath(dagPathCurve);
        dagPathCurve.extendToShape();
        ////// get Cvs from Curve
        MFnNurbsCurve fnNurbsCurve( dagPathCurve );
        MPointArray curvePoints;
        fnNurbsCurve.getCVs(curvePoints,MSpace::kWorld);
        MPoint point = curvePoints[0];
        returnPoints.append(point);
    }
    return returnPoints;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////// get anim curves ////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
//vector <MFnAnimCurve> &returnAnimCurve;
//vector <float> &returnTimeOffset;
//vector <float> &returnTimeLength;
//''' get anim curves for weighting '''
MStatus getAnimCurves(MObject &oThis, MDataBlock &data, MObject &thisNode,
                      MObject &animCurveParent, MObject &animCurveChild){
//         try:
    MPlug parentPlug(thisNode, animCurveParent );
    int count = parentPlug.numConnectedChildren();

    MIntArray curveIndex;
    parentPlug.getExistingArrayAttributeIndices(curveIndex);
    int indexLength = curveIndex.length();
    int index=0;
    for (index=0; index < indexLength; ++index){
        MPlug childPlug = parentPlug.connectionByPhysicalIndex(curveIndex[index]);
        MPlug oChild = childPlug.child(0);
        oChild.asFloat();
        MFnAnimCurve fnAnimCurve(oChild);
        int numKeys = fnAnimCurve.numKeys();
        MTime timeAtFirstKey = fnAnimCurve.time(0);
        MTime timeAtLastKey = fnAnimCurve.time(numKeys-1);
        float timeStart = timeAtFirstKey.value();
        float timeEnd = timeAtLastKey.value();
        float tTimeOff = timeStart * -1;
        float tTimeLength = timeEnd + tTimeOff;
        vector <MFnAnimCurve*> returnAnimCurve;
        vector <float> returnTimeOffset;
        vector <float> returnTimeLength;
////        MFnAnimCurve tCurve = fnAnimCurve;
        returnAnimCurve.push_back(fnAnimCurve);
        returnTimeOffset.push_back(tTimeOff);
        returnTimeLength.push_back(tTimeLength);
    }
	return MS::kSuccess ;
    }
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////// get Values ////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//def getValues(self, data, valueParent, valueChild, returnValuelist):
//    try:
//        arrayHandle = OpenMaya.MArrayDataHandle(data.inputArrayValue( valueParent ))
//        count = arrayHandle.elementCount()
//        temp= dict()
//        for i in range(count):
//            arrayHandle.jumpToElement(i)
//            val = arrayHandle.inputValue().child( valueChild ).asFloat()
//            temp[i] = val
//        returnValuelist = temp.items()
//    except:
//        pass
//
//
//            //uWeightArray = weightDict.items()
//            //returnValuelist = OpenMaya.MFnDoubleArrayData(arrayHandle.data())
//            //returnValuelist[i] = OpenMaya.MFnDoubleArrayData(child.data()).array()
//            //print i, val
//
//    //returnWeightlist = OpenMaya.MFnDoubleArrayData(handle.data()).array()
//    return returnValuelist
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////// Weights //////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//def getWeightValues(self, data, weightParent, weightChild, mIndex, returnWeightlist):
//
//arrayHandle = OpenMaya.MArrayDataHandle(data.inputArrayValue( weightParent ))
//count = arrayHandle.elementCount()
//result = 0.0
//    if count and mIndex <= mIndex:
//        try:
//        arrayHandle.jumpToElement(mIndex)
//
//        handle = OpenMaya.MDataHandle(arrayHandle.inputValue() )
//        child = OpenMaya.MDataHandle(handle.child( weightChild ) )
//            newData = OpenMaya.MFnDoubleArrayData(child.data())
//            returnWeightlist = OpenMaya.MFnDoubleArrayData(child.data()).array()
//        except:
//            pass
//
//    //returnWeightlist = OpenMaya.MFnDoubleArrayData(handle.data()).array()
//    return returnWeightlist
//
//
//
//def getWeightParentValues(self, data, weightParent, weightParentParent, weightChild, parentIndex, mIndex, returnWeightlist):
//    result = 0.0
//    try:
//        //parentArray
//        arrayHandleParentParent = OpenMaya.MArrayDataHandle(data.inputArrayValue( weightParentParent ))
//        countParentParent = arrayHandleParentParent.elementCount()
//        arrayHandleParentParent.jumpToArrayElement(parentIndex)
//
//
//        //parent
//        hArrayHandleParent = arrayHandleParentParent.inputValue().child(weightParent)
//        hArrayHandleParentArray = OpenMaya.MArrayDataHandle(hArrayHandleParent)
//        countParent = hArrayHandleParentArray.elementCount()
//
//        //child
//        hArrayHandleParentArray.jumpToElement(mIndex)
//        handle = OpenMaya.MDataHandle(hArrayHandleParentArray.inputValue() )
//        child = OpenMaya.MDataHandle(handle.child( weightChild ) )
//        newData = OpenMaya.MFnDoubleArrayData(child.data())
//        returnWeightlist = OpenMaya.MFnDoubleArrayData(child.data()).array()
//    except:
//        pass
//
//
//    return returnWeightlist



#endif
