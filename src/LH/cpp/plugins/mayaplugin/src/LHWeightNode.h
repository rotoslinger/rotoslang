#pragma once

#include "windowsMinMax.h"
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
#include <maya/MFnFloatArrayData.h>
#include <maya/MPlugArray.h>
#include <maya/MString.h>
#include <maya/MFloatArray.h>
#include <math.h>
#include <algorithm>
#include <vector>

class LHWeightNode : public MPxNode
{
  public:
    LHWeightNode(){};
    virtual MStatus compute(const MPlug &plug, MDataBlock &data);
    virtual MStatus setDependentsDirty(MPlug const &inPlug,
                                       MPlugArray &affectedPlugs);

    virtual MStatus multiplyKDoubleArrayByVal(MDoubleArray &rDoubleArray,
                                              double val);
    virtual MDoubleArray doubleArrayMathOperation(MDoubleArray doubleArray1,
                                                  MDoubleArray doubleArray2,
                                                  short operation);
    virtual MStatus getWeightsFromInputs(MDataBlock &data, MDoubleArray &finalWeights);
    virtual SchedulingType schedulingType() const { return kParallel; }

    virtual MStatus computeDoubleArray(MDataBlock &data);
    virtual MStatus computeFloatArray(MDataBlock &data);
    static void *creator();
    static MStatus initialize();

    static MTypeId id;

    static MObject aInputWeights;
    static MObject aFactor;
    static MObject aOperation;
    static MObject aInputs;

    static MObject aOutputWeightsDoubleArray;
    static MObject aOutputWeightsFloatArray;
    static MObject aOutWeights;

    double clampWeight;

    inline MString FormatError(const MString &msg, const MString &sourceFile, const int &sourceLine)
    {
        MString txt("[LHWeightNode] ");
        txt += msg;
        txt += ", File: ";
        txt += sourceFile;
        txt += " Line: ";
        txt += sourceLine;
        return txt;
    }

};

///////////////////////////////////////////////////////////
