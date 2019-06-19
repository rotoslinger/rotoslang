#pragma once
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
#include <maya/MFnGenericAttribute.h>
#include <maya/MItGeometry.h>
#include <maya/MFloatArray.h>
#include <maya/MMeshIntersector.h>
#include <maya/MFnAnimCurve.h>
#include <maya/MPointArray.h>
#include <vector>

#include <math.h>

MStatus animCurveObjectCheck(MObject curve);

double remapcurveWeight(MFnAnimCurve *fnAnimCurve, double coord, float timeOffset, float timeLength);

double remapcurveWeightPlus(MFnAnimCurve *fnAnimCurve, double coord, float timeOffset, float timeLength, double falloffUAmount, double center) ;
