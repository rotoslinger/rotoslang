#include "rnkRollNode.h"

MTypeId rnkRollNode::id(0x00007019);

//Floats
MObject rnkRollNode::aDistance;
MObject rnkRollNode::aRadius;
MObject rnkRollNode::aRotAmount;
MObject rnkRollNode::aGlobalScale;
MObject rnkRollNode::aRotation;
//CompoundAttributes
MObject rnkRollNode::aInputs;
MObject rnkRollNode::aOutputs;


void* rnkRollNode::creator() { return new rnkRollNode; }

MStatus rnkRollNode::compute( const MPlug& plug, MDataBlock& data )
{
    MStatus status;
    if ( plug == rnkRollNode::aRotation )
    {
        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( rnkRollNode::aInputs, &status));
        CheckStatusReturn( status, "Unable to get inputs" );

        MArrayDataHandle outputsArrayHandle(data.outputArrayValue( rnkRollNode::aOutputs, &status));
        CheckStatusReturn( status, "Unable to get outputs" );

        unsigned int rotCount = outputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get number of rotates" );

        int i = 0;
        for (i=0;i < rotCount;i++)
        {
            status = inputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to input element" );

            status = outputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to element" );

            float dist = inputsArrayHandle.inputValue().child( rnkRollNode::aDistance ).asFloat();
            float rad = inputsArrayHandle.inputValue().child( rnkRollNode::aRadius ).asFloat();
            float rotAmount = inputsArrayHandle.inputValue().child( rnkRollNode::aRotAmount ).asFloat();
            float gScale = inputsArrayHandle.inputValue().child( rnkRollNode::aGlobalScale ).asFloat();
            float RotationValue = 0.0;

            rad = rad * gScale;

            RotationValue = (-360 * dist /(2 * 3.14 * rad)) * rotAmount;

            MDataHandle rotData = outputsArrayHandle.outputValue().child( rnkRollNode::aRotation );
            rotData.setFloat( RotationValue );
            data.setClean( plug );
        }
    }
    return MS::kSuccess;
}

MStatus rnkRollNode::initialize() {
	MStatus status ;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;

    aDistance = nAttr.create( "distance", "dist", MFnNumericData::kFloat);
    nAttr.setDefault(0.0);
    nAttr.setKeyable(true);

    aRadius = nAttr.create( "radius", "rad", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);

    aRotAmount = nAttr.create( "rotationAmount", "rotamount", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(1.0);

    aGlobalScale = nAttr.create( "globalScale", "gs", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(1.0);

    aRotation = nAttr.create( "rotation", "rot", MFnNumericData::kFloat);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);

    aInputs = cAttr.create("Inputs", "inputs");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aDistance );
    cAttr.addChild( aRadius );
    cAttr.addChild( aRotAmount );
    cAttr.addChild( aGlobalScale );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aInputs);

    aOutputs = cAttr.create("Outputs", "outputs");
    cAttr.setKeyable(false);
    cAttr.setArray(true);
    cAttr.addChild( aRotation );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aOutputs);

    // Effects

    attributeAffects( aInputs, aOutputs);

  return MS::kSuccess;
}


