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
#include <maya/MPointArray.h>
#include <maya/MFloatVectorArray.h>

#include <math.h>

MMatrix ComposeMatrix(MVector rowX, MVector rowY, MVector rowZ, MPoint translation);
void ComposeMatrixWithRotation(MPoint a, MPoint b, MPoint c, MPoint translation, MMatrix &composedMatrix);
MPoint GetPointWithBaryCoords(MPoint a, MPoint b, MPoint c, MFloatVector baryWeights);
MMatrix SinglePointLogic( int iAPointIdx, MFnMesh *fnMesh);
MMatrix DoublePointLogic( int iAPointIdx, int iBPointIdx, MFnMesh *fnMesh, MFloatVector baryWeights);
MMatrix TriplePointLogic( int iAPointIdx, int iBPointIdx, int iCPointIdx,  MFnMesh *fnMesh, MFloatVector baryWeights);
MMatrix QuadPointLogic( int iAPointIdx, int iBPointIdx, int iCPointIdx, int iDPointIdx,  MFnMesh *fnMesh, MFloatVector baryWeights);

struct BaryCoords {
  float coords[3];
  float operator[](int index) const { return coords[index]; }
  float& operator[](int index) { return coords[index]; }
};

void GetBarycentricCoordinates(const MPoint& P, const MPoint& A, const MPoint& B, const MPoint& C,
                               BaryCoords& coords);

void CreateMatrix(const MPoint& origin, const MVector& normal, const MVector& up,
                  MMatrix& matrix);

/**
  Calculates the components necessary to create a wrap basis matrix.
  @param[in] weights The sample weights array from the wrap binding.
  @param[in] coords The barycentric coordinates of the closest point.
  @param[in] triangleVertices The vertex ids forming the triangle of the closest point.
  @param[in] points The driver point array.
  @param[in] normals The driver per-vertex normal array.
  @param[in] sampleIds The vertex ids on the driver of the current sample.
  @param[in] alignedStorage double array that is 32 byte aligned for AVX.
  @param[out] origin The origin of the coordinate system.
  @param[out] up The up vector of the coordinate system.
  @param[out] normal The normal vector of the coordinate system.
*/



void CalculateBasisComponents(const MDoubleArray& weights, const BaryCoords& coords,
                              const MIntArray& triangleVertices, const MPointArray& points,
                              const MFloatVectorArray& normals, const MIntArray& sampleIds,
                              double* alignedStorage,
                              MPoint& origin, MVector& up, MVector& normal);

/**
  Ensures that the up and normal vectors are perpendicular to each other.
  @param[in] weights The sample weights array from the wrap binding.
  @param[in] points The driver point array.
  @param[in] sampleIds The vertex ids on the driver of the current sample.
  @param[in] origin The origin of the coordinate system.
  @param[in] up The up vector of the coordinate system.
  @param[out] normal The normal vector of the coordinate system.
*/

void GetValidUp(const MDoubleArray& weights, const MPointArray& points,
                const MIntArray& sampleIds, const MPoint& origin, const MVector& normal,
                MVector& up);
