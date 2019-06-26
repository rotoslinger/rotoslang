#include "matrixCommon.h"


MVector vInitX(1.0, 0.0, 0.0);
MVector vInitY(0.0, 1.0, 0.0);
MVector vInitZ(0.0, 0.0, 1.0);
MPoint pInit(0.0, 0.0, 0.0);


MMatrix ComposeMatrix(MVector rowX, MVector rowY, MVector rowZ, MPoint translation)
{
        double compMatrix[4][4]={{ rowX[0], rowX[1], rowX[2], 0.0},
                                { rowY[0], rowY[1], rowY[2], 0.0},
                                { rowZ[0], rowZ[1], rowZ[2], 0.0},
                                {translation.x, translation.y, translation.z, 1.0}};
        MMatrix composedMatrix(compMatrix);
        return composedMatrix;
}

void ComposeMatrixWithRotation(MPoint a, MPoint b, MPoint c, MPoint translation, MMatrix &composedMatrix)
{
    //////////////////////////////////////// Composing the rotation matrix ///////////////////////////////////////////////////////////////
    // Composing in a right handed style (make a backward L with your right hand)
    //      C
    //      |
    //   A--B
    // A is the tip of the thumb
    // B is the interdigital fold between thumb and forefinger
    // C is the tip of the forefinger
    // This will aim at the A-B vector
    // Switch A and C to flip the aim axis (this will be done via script logic)
    //      A
    //      |
    //   C--B
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    MVector rowZ = b - a ^ c-a;
    MVector rowY =  rowZ ^ b - a;
    MVector rowX = rowY ^ rowZ;
    rowX.normalize();
    rowY.normalize();
    rowZ.normalize();
    composedMatrix = ComposeMatrix(rowX, rowY, rowZ, translation);
}

MPoint GetPointWithBaryCoords(MPoint a, MPoint b, MPoint c, MFloatVector baryWeights)
{
    //////////////////////////////////////// Normalizing bary weights ////////////////////////////////////////////////////////////////////
    // This is how you would normalize the bary weights.  (The node does not need to be normalized interatively, this will be scripted....)
    // double sumBarys = baryWeights[0] + baryWeights[1] + baryWeights[2];
    // MPoint normalizedPoint = a*(baryWeights[0]/sumBarys) + b*(baryWeights[1]/sumBarys) + c*(baryWeights[2]/sumBarys);
    //////////////////////////////////////// Normalizing bary weights ////////////////////////////////////////////////////////////////////

    return a*baryWeights[0] + b*baryWeights[1] + c*baryWeights[2];

}



MMatrix SinglePointLogic( int iAPointIdx, MFnMesh *fnMesh)
{
    MPoint a;
    fnMesh->getPoint(iAPointIdx, a, MSpace::kObject);
    MMatrix composedMatrix = ComposeMatrix(vInitX, vInitY, vInitZ, a);
    return composedMatrix;
}


MMatrix DoublePointLogic( int iAPointIdx, int iBPointIdx, MFnMesh *fnMesh, MFloatVector baryWeights)
{
    MPoint a;
    MPoint b;
    fnMesh->getPoint(iAPointIdx, a, MSpace::kObject);
    fnMesh->getPoint(iBPointIdx, b, MSpace::kObject);
    MPoint normalizedPoint = a*baryWeights[0] + b*baryWeights[1];
    MMatrix composedMatrix = ComposeMatrix(vInitX, vInitY, vInitZ, normalizedPoint);
    return composedMatrix;
}

MMatrix TriplePointLogic( int iAPointIdx, int iBPointIdx, int iCPointIdx,  MFnMesh *fnMesh, MFloatVector baryWeights)
{
        MPoint a;
        MPoint b;
        MPoint c;
        fnMesh->getPoint(iAPointIdx, a, MSpace::kObject);
        fnMesh->getPoint(iBPointIdx, b, MSpace::kObject);
        fnMesh->getPoint(iCPointIdx, c, MSpace::kObject);
        MPoint normalizedPoint = GetPointWithBaryCoords(a, b, c, baryWeights);
        MMatrix composedMatrix;
        ComposeMatrixWithRotation(a, b, c, normalizedPoint, composedMatrix);
        return composedMatrix;
}

MMatrix TriplePointLogicTest( int iAPointIdx, int iBPointIdx, int iCPointIdx,  MFnMesh *fnMesh, MFloatVector baryWeights, MPoint testPoint)
{
        MPoint a;
        MPoint b;
        MPoint c;
        fnMesh->getPoint(iAPointIdx, a, MSpace::kObject);
        fnMesh->getPoint(iBPointIdx, b, MSpace::kObject);
        fnMesh->getPoint(iCPointIdx, c, MSpace::kObject);

        a = a-testPoint;
        b = b-testPoint;
        b = b-testPoint;
        MPoint normalizedPoint = GetPointWithBaryCoords(a, b, c, baryWeights);
        MMatrix composedMatrix;
        ComposeMatrixWithRotation(a, b, c, normalizedPoint, composedMatrix);

        double baseMatrix[4][4]={{ 1, 0.0, 0.0, 0.0},
                                { 0.0, 1, 0.0, 0.0},
                                { 0.0, 0.0, 1, 0.0},
                                {            testPoint.x,            testPoint.y,            testPoint.z, 1.0},};
        MMatrix testPointMatrix(baseMatrix);

        composedMatrix = composedMatrix;
        return composedMatrix;
}

MMatrix QuadPointLogic( int iAPointIdx, int iBPointIdx, int iCPointIdx, int iDPointIdx,  MFnMesh *fnMesh, MFloatVector baryWeights)
{
        MPoint a;
        MPoint b;
        MPoint c;
        MPoint d;
        fnMesh->getPoint(iAPointIdx, a, MSpace::kObject);
        fnMesh->getPoint(iBPointIdx, b, MSpace::kObject);
        fnMesh->getPoint(iCPointIdx, c, MSpace::kObject);
        fnMesh->getPoint(iDPointIdx, d, MSpace::kObject);
        // Average location of c and d
        c = (c+d)/2.0;
        MPoint normalizedPoint = GetPointWithBaryCoords(a, b, c, baryWeights);
        MMatrix composedMatrix;
        ComposeMatrixWithRotation(a, b, c, normalizedPoint, composedMatrix);
        return composedMatrix;
}

// void GetBarycentricCoordinates(const MPoint& P, const MPoint& A, const MPoint& B, const MPoint& C,
//                                BaryCoords& coords) {
//   // Compute the normal of the triangle
//   MVector N = (B - A) ^ (C - A);
//   MVector unitN = N.normal();

//   // Compute twice area of triangle ABC
//   double areaABC = unitN * N;

//   if (areaABC == 0.0) {
//     // If the triangle is degenerate, just use one of the points.
//     coords[0] = 1.0f;
//     coords[1] = 0.0f;
//     coords[2] = 0.0f;
//     return;
//   }

//   // Compute a
//   double areaPBC = unitN * ((B - P) ^ (C - P));
//   coords[0] = (float)(areaPBC / areaABC);

//   // Compute b
//   double areaPCA = unitN * ((C - P) ^ (A - P));
//   coords[1] = (float)(areaPCA / areaABC);

//   // Compute c
//   coords[2] = 1.0f - coords[0] - coords[1];
// }

// void CreateMatrix(const MPoint& origin, const MVector& normal, const MVector& up,
//                   MMatrix& matrix) {
//   const MPoint& t = origin;
//   const MVector& y = normal;
//   MVector x = y ^ up;
//   MVector z = x ^ y;
//   // Renormalize vectors
//   x.normalize();
//   z.normalize();
//   matrix[0][0] = x.x; matrix[0][1] = x.y; matrix[0][2] = x.z; matrix[0][3] = 0.0;
//   matrix[1][0] = y.x; matrix[1][1] = y.y; matrix[1][2] = y.z; matrix[1][3] = 0.0;
//   matrix[2][0] = z.x; matrix[2][1] = z.y; matrix[2][2] = z.z; matrix[2][3] = 0.0;
//   matrix[3][0] = t.x; matrix[3][1] = t.y; matrix[3][2] = t.z; matrix[3][3] = 1.0;
// }


// void CalculateBasisComponents(const MDoubleArray& weights, const BaryCoords& coords,
//                               const MIntArray& triangleVertices, const MPointArray& points,
//                               const MFloatVectorArray& normals, const MIntArray& sampleIds,
//                               double* alignedStorage,
//                               MPoint& origin, MVector& up, MVector& normal) {
//   // Start with the recreated point and normal using the barycentric coordinates of the hit point.
//   unsigned int hitIndex = weights.length()-1;

//   MVector hitNormal;
//   // Create the barycentric point and normal.
//   for (int i = 0; i < 3; ++i) {
//     origin += points[triangleVertices[i]] * coords[i];
//     hitNormal += MVector(normals[triangleVertices[i]]) * coords[i];
//   }
//   // Use crawl data to calculate normal
//   normal = hitNormal * weights[hitIndex];
//   for (unsigned int j = 0; j < hitIndex; j++) {
//     normal += MVector(normals[sampleIds[j]]) * weights[j];
//   }

//   // Calculate the up vector
//   // The triangle vertices are sorted by decreasing barycentric coordinates so the first two are
//   // the two closest vertices in the triangle.
//   up = ((points[triangleVertices[0]] + points[triangleVertices[1]]) * 0.5) - origin;
//   normal.normalize();
//   GetValidUp(weights, points, sampleIds, origin, normal, up);
// }


// void GetValidUp(const MDoubleArray& weights, const MPointArray& points,
//                 const MIntArray& sampleIds, const MPoint& origin, const MVector& normal,
//                 MVector& up) {
//   MVector unitUp = up.normal();
//   // Adjust up if it's parallel to normal or if it's zero length
//   if (std::abs((unitUp * normal) - 1.0) < 0.001 || up.length() < 0.0001) {
//     for (unsigned int j = 0; j < weights.length()-1; ++j) {
//       up -= (points[sampleIds[j]] - origin) * weights[j];
//       unitUp = up.normal();
//       if (std::abs((unitUp * normal) - 1.0) > 0.001 && up.length() > 0.0001) {
//         // If the up and normal vectors are no longer parallel and the up vector has a length,
//         // then we are good to go.
//         break;
//       }
//     }
//     up.normalize();
//   } else {
//     up = unitUp;
//   }
// }
