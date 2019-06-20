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