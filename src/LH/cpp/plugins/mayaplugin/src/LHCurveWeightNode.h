#ifndef _LHCURVEWEIGHTNODE_H
#define _LHCURVEWEIGHTNODE_H

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
#include <maya/MFloatArray.h>
#include <maya/MMeshIntersector.h>
#include <maya/MFnAnimCurve.h>

#include <math.h>

class LHCurveWeightNode : public MPxNode
{
  public:
    LHCurveWeightNode(){};
    virtual MStatus compute(const MPlug &plug, MDataBlock &data);
    virtual MStatus setDependentsDirty(MPlug const &inPlug,
                                       MPlugArray &affectedPlugs);

    virtual MStatus getMeshData(MDataBlock& data, MObject &oInputMesh, MObject &oProjectionMesh);
    MStatus getWeightMeshData(MObject oProjectionMesh, MFnMesh *mInputMesh, MFloatArray &uCoords, MFloatArray &vCoords, int numVerts, int iCacheWeightMesh);

    virtual MStatus multiplyKDoubleArrayByVal(MDoubleArray &rDoubleArray,
                                              double val);
    virtual MDoubleArray doubleArrayMathOperation(MDoubleArray doubleArray1,
                                                  MDoubleArray doubleArray2,
                                                  short operation);
    virtual MStatus getWeightsFromInputs(MDataBlock &data, MDoubleArray &finalWeights);
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

    static MObject aInputWeights;
    static MObject aFactor;
    static MObject aOperation;
    static MObject aInputs;

    static MObject aMembershipWeights;
    static MObject aCacheMembershipWeights;
    static MObject aInputMesh;
    static MObject aProjectionMesh;
    static MObject aCacheWeightMesh;
    static MObject aOutputWeightsDoubleArray;
    static MObject aOutputWeightsFloatArray;
    static MObject aOutWeights;
    static MObject aAnimCurveU;
    static MObject aAnimCurveV;
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
    #define Error(msg)                                            \
        {                                                         \
            MString __txt = FormatError(msg, __FILE__, __LINE__); \
            MGlobal::displayError(__txt);                         \
            cerr << endl                                          \
                << "Error: " << __txt;                           \
        }

    #define CheckBool(result) \
        if (!(result))        \
        {                     \
            Error(#result);   \
        }

    #define CheckStatus(stat, msg) \
        if (!stat)                 \
        {                          \
            Error(msg);            \
        }

    #define CheckObject(obj, msg) \
        if (obj.isNull())         \
        {                         \
            Error(msg);           \
        }

    #define CheckStatusReturn(stat, msg) \
        if (!stat)                       \
        {                                \
            Error(msg);                  \
            return stat;                 \
        }
};

///////////////////////////////////////////////////////////
#endif