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

MObject rnkRollNode::aParamU;
MObject rnkRollNode::aParamV;

MObject rnkRollNode::aMatrix;
MObject rnkRollNode::aBaseMatrix;



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
            MMatrix matrix = inputsArrayHandle.inputValue().child( rnkRollNode::aMatrix ).asMatrix();
            MMatrix baseMatrix = inputsArrayHandle.inputValue().child( rnkRollNode::aBaseMatrix ).asMatrix();

            //---Get Points from matrices
            MTransformationMatrix tMatrix(matrix);
            MTransformationMatrix tBaseMatrix(matrix);

            MVector vMatrix = tMatrix.getTranslation(MSpace::kWorld);
            MVector vBaseMatrix = tBaseMatrix.getTranslation(MSpace::kWorld);


            MPoint pMatrix(vMatrix.x, vMatrix.y, vMatrix.z);
            MPoint pBaseMatrix(vBaseMatrix.x, vBaseMatrix.y, vBaseMatrix.z);


//			MGlobal::displayInfo(MString("THIS IS THE MATRIX Translation") + vMatrix.x + "," + vMatrix.y + "," + vMatrix.z);
//			MGlobal::displayInfo(MString("THIS IS THE Base MATRIX Translation") + vBaseMatrix.x + "," + vBaseMatrix.y + "," + vBaseMatrix.z);

            //---For debugging the matrices
            //double sm[4][4];
            //baseMatrix.get(sm);
			//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[0][0] + sm[0][1] + sm[0][2] + sm[0][3]);
			//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[1][0] + sm[1][1] + sm[1][2] + sm[1][3]);
			//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[2][0] + sm[2][1] + sm[2][2] + sm[2][3]);
			//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[3][0] + sm[3][1] + sm[3][2] + sm[3][3]);





            float RotationValue = 0.0;

            rad = rad * gScale;

            RotationValue = (-360 * dist /(2 * 3.14 * rad)) * rotAmount;

            MDataHandle rotData = outputsArrayHandle.outputValue().child( rnkRollNode::aRotation );
            rotData.setFloat( RotationValue );

            MDataHandle paramUData = outputsArrayHandle.outputValue().child( rnkRollNode::aParamU );
            paramUData.setDouble( (double)dist );

            MDataHandle paramVData = outputsArrayHandle.outputValue().child( rnkRollNode::aParamV );
            paramVData.setDouble( (double)rad );


            data.setClean( plug );
        }
    }
    return MS::kSuccess;
}

MStatus rnkRollNode::initialize() {
	MStatus status ;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnTypedAttribute tAttr;
    MFnMatrixAttribute mAttr;

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


    // CREATE AND ADD ".position" ATTRIBUTE:
    aMatrix = mAttr.create("matrix", "m");
    mAttr.setWritable(true);
    mAttr.setStorable(true);
    addAttribute( aMatrix );

    aBaseMatrix = mAttr.create("baseMatrix", "bm");
    mAttr.setWritable(true);
    mAttr.setStorable(true);
    addAttribute( aBaseMatrix );

    aInputs = cAttr.create("Inputs", "inputs");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aDistance );
    cAttr.addChild( aRadius );
    cAttr.addChild( aRotAmount );
    cAttr.addChild( aGlobalScale );
    cAttr.addChild( aMatrix );
    cAttr.addChild( aBaseMatrix );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aInputs);


    aRotation = nAttr.create( "rotation", "rot", MFnNumericData::kFloat);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);

    aParamU = nAttr.create( "parameterU", "pu", MFnNumericData::kDouble);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);

    aParamV = nAttr.create( "parameterV", "pv", MFnNumericData::kDouble);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);






    // CREATE AND ADD ".normalX" ATTRIBUTE:


    aOutputs = cAttr.create("Outputs", "outputs");
    cAttr.setKeyable(false);
    cAttr.setArray(true);
    cAttr.addChild( aRotation );
    cAttr.addChild( aParamU );
    cAttr.addChild( aParamV );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aOutputs);

    // Effects

    attributeAffects( aInputs, aOutputs);

  return MS::kSuccess;
}


