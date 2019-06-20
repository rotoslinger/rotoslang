#pragma once
#include "formatErrorMacros.h"
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPlug.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnMesh.h>
#include <maya/MFloatMatrix.h>
#include <maya/MTransformationMatrix.h>

#include <math.h>

MMatrix ComposeMatrix(MVector rowX, MVector rowY, MVector rowZ, MPoint translation);
void ComposeMatrixWithRotation(MPoint a, MPoint b, MPoint c, MPoint translation, MMatrix &composedMatrix);
MPoint GetPointWithBaryCoords(MPoint a, MPoint b, MPoint c, MFloatVector baryWeights);
MMatrix SinglePointLogic( int iAPointIdx, MFnMesh *fnMesh);
MMatrix DoublePointLogic( int iAPointIdx, int iBPointIdx, MFnMesh *fnMesh, MFloatVector baryWeights);
MMatrix TriplePointLogic( int iAPointIdx, int iBPointIdx, int iCPointIdx,  MFnMesh *fnMesh, MFloatVector baryWeights);
MMatrix QuadPointLogic( int iAPointIdx, int iBPointIdx, int iCPointIdx, int iDPointIdx,  MFnMesh *fnMesh, MFloatVector baryWeights);







