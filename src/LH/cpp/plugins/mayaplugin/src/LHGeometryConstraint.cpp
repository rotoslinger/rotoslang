// This is a template for the MPxNode
//====================================

#include "LHGeometryConstraint.h"

MTypeId LHGeometryConstraint::id(043653470);

//doubles
MObject LHGeometryConstraint::aMesh;

MObject LHGeometryConstraint::aInputMatrix;
MObject LHGeometryConstraint::aOutputMatrix;
MObject LHGeometryConstraint::aU;
MObject LHGeometryConstraint::aV;
MObject LHGeometryConstraint::aAPointIdx;
MObject LHGeometryConstraint::aBPointIdx;
MObject LHGeometryConstraint::aCPointIdx;
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

    aInputMatrix = mAttr.create("inputMatrix", "inmatrix");
    mAttr.setKeyable(true);
    mAttr.setWritable(true);
    mAttr.setConnectable(true);
    mAttr.setStorable(true);
    addAttribute( aInputMatrix );
    attributeAffects(aInputMatrix, aOutputMatrix);

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

    aU = nAttr.create( "parameterU", "paramu", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(0.5);
    nAttr.setChannelBox(true);
    addAttribute( aU );
    attributeAffects(aU, aOutputMatrix);

    aV = nAttr.create( "parameterV", "paramV", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(0.5);
    nAttr.setChannelBox(true);
    addAttribute( aV );
    attributeAffects(aV, aOutputMatrix);

    aAPointIdx = nAttr.create("aPointIdx", "apointidx", MFnNumericData::kInt);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    nAttr.setDefault(2);
    nAttr.setMin(0);
    addAttribute(aAPointIdx);
    attributeAffects(aAPointIdx, aOutputMatrix);

    aBPointIdx = nAttr.create("bPointIdx", "bpointidx", MFnNumericData::kInt);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    nAttr.setDefault(0);
    nAttr.setMin(0);
    addAttribute(aBPointIdx);
    attributeAffects(aBPointIdx, aOutputMatrix);

    aCPointIdx = nAttr.create("cPointIdx", "cpointidx", MFnNumericData::kInt);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    nAttr.setDefault(1);
    nAttr.setMin(0);
    addAttribute(aCPointIdx);
    attributeAffects(aCPointIdx, aOutputMatrix);



  return MS::kSuccess;
}

void* LHGeometryConstraint::creator() { return new LHGeometryConstraint; }

MStatus LHGeometryConstraint::compute( const MPlug& plug, MDataBlock& data )
{

    MStatus status;
    if (plug == aOutputMatrix)
    {

        MDataHandle hMesh = data.inputValue(aMesh, &status);
        CheckStatusReturn( status, "Unable to get mesh" );
        MObject oMesh = hMesh.asMeshTransformed();
        MFnMesh fnMesh(oMesh);
    	// short sOrientationType = data.inputValue(aOrientationType).asShort();
    	MMatrix inMatrix = data.inputValue(aInputMatrix).asMatrix();
    	float dU = data.inputValue(aU).asFloat();
    	float dV = data.inputValue(aV).asFloat();
    	// float dUTangent = data.inputValue(aUTangent).asFloat();
    	// float dVTangent = data.inputValue(aVTangent).asFloat();
    	// int iPolyID = data.inputValue(aPolygonID).asInt();
    	// int iVertID = data.inputValue(aVertID).asInt();
    	int iAPointIdx = data.inputValue(aAPointIdx).asInt();
    	int iBPointIdx = data.inputValue(aBPointIdx).asInt();
    	int iCPointIdx = data.inputValue(aCPointIdx).asInt();

        //////////////////////////////// note on MFnNumericAttribute.createPoint() /////////////////////////////
        // nAttr.createPoint return broken values when you get is asVector()......
        // Why is this happening?
        // For some reason MFloatVector works...
        // need to find out if it is possible to get a handle as an MObject and convert that to an MPoint....
        //////////////////////////////// //////////////////////////////// /////////////////////////////
        
    	MFloatVector vBaryWeight = data.inputValue(aBaryWeight).asFloatVector();

        MPoint a;
        MPoint b;
        MPoint c;

        fnMesh.getPoint(iAPointIdx, a, MSpace::kObject);
        fnMesh.getPoint(iBPointIdx, b, MSpace::kObject);
        fnMesh.getPoint(iCPointIdx, c, MSpace::kObject);
        
        //////////////////////////////////////// Normalizing bary weights ////////////////////////////////////////////////////////////////////
        // This is how you would normalize the bary weights.  (The node does not need to be normalized interatively, this will be scripted....)
        // double sumBarys = vBaryWeight[0] + vBaryWeight[1] + vBaryWeight[2];
        // MPoint averagePoint = a*(vBaryWeight[0]/sumBarys) + b*(vBaryWeight[1]/sumBarys) + c*(vBaryWeight[2]/sumBarys);
        //////////////////////////////////////// Normalizing bary weights ////////////////////////////////////////////////////////////////////

        MPoint averagePoint = a*vBaryWeight[0] + b*vBaryWeight[1] + c*vBaryWeight[2];

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

        MVector pointZ = b - a ^ c-a;
        MVector pointY =  pointZ ^ b - a;
        MVector pointX = pointY ^ pointZ;

        pointX.normalize();
        pointY.normalize();
        pointZ.normalize();

        float compMatrix[4][4]={{ pointX[0], pointX[1], pointX[2], 0.0},
                                { pointY[0], pointY[1], pointY[2], 0.0},
                                { pointZ[0], pointZ[1], pointZ[2], 0.0},
                                {averagePoint.x, averagePoint.y, averagePoint.z, 1.0}};

        MMatrix composedMatrix(compMatrix);
        composedMatrix = composedMatrix * inMatrix;

        MDataHandle outMatrixHandle = data.outputValue(aOutputMatrix);
        outMatrixHandle.set(composedMatrix);
        outMatrixHandle.setClean();
        data.setClean(plug);

    }
    else
        return MS::kUnknownParameter;

    return MS::kSuccess;
}

