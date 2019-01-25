#include "LHGeometryConstraint.h"

MTypeId LHGeometryConstraint::id(043653470);

MObject LHGeometryConstraint::aOutputMatrix;
MObject LHGeometryConstraint::aParentMatrix;
MObject LHGeometryConstraint::aMesh;
MObject LHGeometryConstraint::aAPointIdx;
MObject LHGeometryConstraint::aBPointIdx;
MObject LHGeometryConstraint::aCPointIdx;
MObject LHGeometryConstraint::aDPointIdx;
MObject LHGeometryConstraint::aBaryWeight;

MStatus LHGeometryConstraint::initialize() {
	MStatus status ;
    MFnNumericAttribute nAttr;
    MFnTypedAttribute tAttr;
    MFnMatrixAttribute mAttr;

    // Remember to always instantiate your output before setting up attribute affects.
    // Though the MObject already exists, the node will not update as expected
    aOutputMatrix = mAttr.create("outputMatrix", "outmatrix");
    mAttr.setKeyable(false);
    mAttr.setWritable(true);
    mAttr.setConnectable(true);
    mAttr.setStorable(true);
    addAttribute( aOutputMatrix );

    aParentMatrix = mAttr.create("parentMatrix", "pmatrix");
    mAttr.setKeyable(true);
    mAttr.setWritable(true);
    mAttr.setConnectable(true);
    mAttr.setStorable(true);
    addAttribute( aParentMatrix );
    attributeAffects(aParentMatrix, aOutputMatrix);

    // When retrieving the plug info, or data handle get input value as MFloatVector for this createPoint attr
    aBaryWeight = nAttr.createPoint("baryWeights", "bweights");
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setConnectable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    addAttribute(aBaryWeight);
    attributeAffects(aBaryWeight, aOutputMatrix);

    aMesh = tAttr.create("inMesh", "inmesh", MFnData::kMesh);
    addAttribute(aMesh);
    attributeAffects(aMesh, aOutputMatrix);

    aAPointIdx = nAttr.create("aPointIdx", "apointidx", MFnNumericData::kInt);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    nAttr.setDefault(0);
    nAttr.setMin(0);
    addAttribute(aAPointIdx);
    attributeAffects(aAPointIdx, aOutputMatrix);

    aBPointIdx = nAttr.create("bPointIdx", "bpointidx", MFnNumericData::kInt);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    nAttr.setDefault(1);
    nAttr.setMin(-1);
    addAttribute(aBPointIdx);
    attributeAffects(aBPointIdx, aOutputMatrix);

    aCPointIdx = nAttr.create("cPointIdx", "cpointidx", MFnNumericData::kInt);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    nAttr.setDefault(2);
    nAttr.setMin(-1);
    addAttribute(aCPointIdx);
    attributeAffects(aCPointIdx, aOutputMatrix);

    aDPointIdx = nAttr.create("dPointIdx", "dpointidx", MFnNumericData::kInt);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    nAttr.setDefault(-1);
    nAttr.setMin(-1);
    addAttribute(aDPointIdx);
    attributeAffects(aDPointIdx, aOutputMatrix);

  return MS::kSuccess;
}

void* LHGeometryConstraint::creator() { return new LHGeometryConstraint; }

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

MStatus LHGeometryConstraint::compute( const MPlug& plug, MDataBlock& data )
{

    MStatus status;
    if (plug == aOutputMatrix)
    {

        MDataHandle hMesh = data.inputValue(aMesh, &status);
        // Stop here if no mesh
        CheckStatusReturn( status, "Unable to get mesh" );
        MObject oMesh = hMesh.asMeshTransformed();
        MFnMesh * fnMesh = new MFnMesh(oMesh);
    	MMatrix mParentMatrix = data.inputValue(aParentMatrix).asMatrix();
    	// MMatrix mOffsetMatrix = data.inputValue(aOffsetMatrix).asMatrix();
    	int iAPointIdx = data.inputValue(aAPointIdx).asInt();
    	int iBPointIdx = data.inputValue(aBPointIdx).asInt();
    	int iCPointIdx = data.inputValue(aCPointIdx).asInt();
    	int iDPointIdx = data.inputValue(aDPointIdx).asInt();
        //////////////////////////////// note on MFnNumericAttribute.createPoint() /////////////////////////////
        // nAttr.createPoint return broken values when you get is asVector()......
        // Why is this happening?
        // For some reason MFloatVector works...
        // need to find out if it is possible to get a handle as an MObject and convert that to an MPoint....
        //////////////////////////////// //////////////////////////////// /////////////////////////////
    	MFloatVector baryWeights = data.inputValue(aBaryWeight).asFloatVector();

        // Decide what algorithm to use.
        // If any point is set to -1 no points after that point will be used. (point A must always be used)
        // If less than 3 points are used the matrix will not have rotations
        // If 4 points are used, the forth point will be averaged with the up vector to make a more polygonal orientation
        MMatrix composedMatrix;
        if (iBPointIdx == -1)
        {
            composedMatrix = SinglePointLogic(iAPointIdx, fnMesh);
        }
        else if (iCPointIdx == -1)
        {
            composedMatrix = DoublePointLogic(iAPointIdx, iBPointIdx, fnMesh, baryWeights);

        }
        else if (iDPointIdx == -1)
        {
            composedMatrix = TriplePointLogic(iAPointIdx, iBPointIdx, iCPointIdx, fnMesh, baryWeights);

        }
        else
        {
            composedMatrix = QuadPointLogic(iAPointIdx, iBPointIdx, iCPointIdx, iDPointIdx, fnMesh, baryWeights);

        }

        composedMatrix = composedMatrix * mParentMatrix;
        MDataHandle outMatrixHandle = data.outputValue(aOutputMatrix);
        outMatrixHandle.set(composedMatrix);
        outMatrixHandle.setClean();
        data.setClean(plug);

    }
    else
        return MS::kUnknownParameter;

    return MS::kSuccess;
}

