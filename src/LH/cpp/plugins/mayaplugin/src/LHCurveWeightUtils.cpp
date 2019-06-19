#pragma once
#include "LHCurveWeightUtils.h"

MStatus animCurveObjectCheck(MObject curve)
{
    if (curve.isNull())
    {
        return MS::kFailure;
    } 
    return MS::kSuccess;
}

double remapcurveWeight(MFnAnimCurve *fnAnimCurve, double coord, float timeOffset, float timeLength)
{
    double remap = coord * timeLength;
    remap = remap - timeOffset;
    MTime remapTime(remap);
    return fnAnimCurve->evaluate(remapTime);
}

double remapcurveWeightPlus(MFnAnimCurve *fnAnimCurve, double coord, float timeOffset, float timeLength, double falloffUAmount, double center) 
{
    coord = coord + (coord-center) * falloffUAmount;
    double remap = coord * timeLength;
    remap = remap - timeOffset;
    MTime remapTime(remap);
    return fnAnimCurve->evaluate(remapTime);
}
