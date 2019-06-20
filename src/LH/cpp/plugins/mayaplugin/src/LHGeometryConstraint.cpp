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

