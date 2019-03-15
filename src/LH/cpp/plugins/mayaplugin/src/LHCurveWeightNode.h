#ifndef _LHCURVEWEIGHTNODE_H
#define _LHCURVEWEIGHTNODE_H
#include "formatErrorMacros.h"

#include <string.h>
#include <maya/MIOStream.h>
#include <math.h>

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnEnumAttribute.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MGlobal.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MPlugArray.h>
#include <maya/MString.h>
#include <maya/MFnMesh.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsSurface.h>

#include <maya/MFloatArray.h>
#include <maya/MMeshIntersector.h>
#include <maya/MFnAnimCurve.h>
#include <maya/MPointArray.h>
#include <vector>

#include <math.h>

class LHCurveWeightNode : public MPxNode
{
  public:
    LHCurveWeightNode(){};
    virtual MStatus compute(const MPlug &plug, MDataBlock &data);
    virtual MStatus setDependentsDirty(MPlug const &inPlug,
                                       MPlugArray &affectedPlugs);

    virtual MStatus getMeshData(MDataBlock& data, MObject &oInputMesh, MObject &oProjectionMesh, MObject &oInputCurve, MObject &oInputNurbs);
    MStatus getWeightMeshData(MObject oProjectionMesh, MFnMesh *mInputMesh, MFnMesh *mProjectionMesh, MFloatArray &uCoords, MFloatArray &vCoords, int numVerts, int iCacheWeightMesh);
    MStatus getWeightMeshDataFromPoints(MObject oProjectionMesh, MPointArray allPoints, MFnMesh *mProjectionMesh, MFloatArray &uCoords, MFloatArray &vCoords, int numVerts, int iCacheWeightMesh);

    virtual MStatus getWeightsFromInputs(MDataBlock &data, MDoubleArray &finalWeights, std::vector<MDoubleArray>& finalWeightsArray);
    virtual MStatus getAnimCurveWeights(MArrayDataHandle inputsArrayHandle, MDoubleArray &rWeights, int numVerts, int currentElem);

    virtual MStatus computeDoubleArray(MDataBlock &data);
    virtual MStatus computeFloatArray(MDataBlock &data);
    virtual void dirtyPlug(MPlug const & inPlug, MPlugArray  & affectedPlugs, MPlug outArrayPlug);
    virtual SchedulingType schedulingType() const { return kParallel; }
    virtual MStatus getAnimCurveInfo(MFnAnimCurve *fnAnimCurve, float &timeOffset, float &timeLength);
    virtual MStatus getAnimCurvePlug(int currentElem, MPlug& rPCurve, MObject curveObject);



    static void *creator();
    static MStatus initialize();

    static MTypeId id;

    static MObject aInputs;

    static MObject aMembershipWeights;
    static MObject aCacheMembershipWeights;
    static MObject aInputMesh;
    static MObject aInputCurve;
    static MObject aInputNurbs;

    
    static MObject aProjectionMesh;
    static MObject aCacheWeightMesh;
    static MObject aOutputWeightsDoubleArrayParent;
    static MObject aOutputWeightsFloatArrayParent;
    static MObject aOutputWeightsDoubleArray;
    static MObject aOutputWeightsFloatArray;
    static MObject aOutWeights;
    static MObject aAnimCurveU;
    static MObject aAnimCurveV;
    static MObject aFalloffU;
    static MObject aFalloffUPivot;





    MObject thisMObj;
    MStatus status;
    // Used for caching
    MDoubleArray membershipWeights;
    MFloatArray uCoords, vCoords;
    MPointOnMesh ptOnMesh;
    MPoint weightPt;
    float2 uvCoord;
    MMeshIntersector fnWeightIntersector;
    MPoint pt;

    // getAnimCurveInfo() attributes
    int numKeys;
    MTime timeAtFirstKey;
    MTime timeAtLastKey;
    float timeStart;
    float timeEnd;
    float tTimeOff;
    float tTimeLength;

    // getAnimCurveWeights() attributes
    float timeOffsetU;
    float timeLengthU;
    float timeOffsetV;
    float timeLengthV;
    double uWeight;
    double vWeight;
    MDoubleArray animCurveWeights;


    MPointArray testWeights;
    MPoint pointOnPoint;







  private:
    inline MString FormatError(const MString &msg, const MString &sourceFile, const int &sourceLine)
    {
        MString txt("[LHCurveWeightNode] ");
        txt += msg;
        txt += ", File: ";
        txt += sourceFile;
        txt += " Line: ";
        txt += sourceLine;
        return txt;
    }

};

///////////////////////////////////////////////////////////
#endif
