#include "rnkRollNode.h"

MTypeId rnkRollNode::id(0x00007019);

//doubles
MObject rnkRollNode::aParamUAmount;
MObject rnkRollNode::aParamVAmount;
//CompoundAttributes
MObject rnkRollNode::aInputs;
MObject rnkRollNode::aOutputs;

MObject rnkRollNode::aParamU;
MObject rnkRollNode::aParamV;

MObject rnkRollNode::aMatrix;
MObject rnkRollNode::aBaseMatrix;

MObject rnkRollNode::aSurface;


void* rnkRollNode::creator() { return new rnkRollNode; }

MStatus rnkRollNode::compute( const MPlug& plug, MDataBlock& data )
{
    MStatus status;
    if ( plug == rnkRollNode::aParamU or plug == rnkRollNode::aParamV)
    {
        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( rnkRollNode::aInputs, &status));
        CheckStatusReturn( status, "Unable to get inputs" );

        MArrayDataHandle outputsArrayHandle(data.outputArrayValue( rnkRollNode::aOutputs, &status));
        CheckStatusReturn( status, "Unable to get outputs" );

        unsigned int elemCount = outputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get number of rotates" );

        int i = 0;
        for (i=0;i < elemCount;i++)
        {
            status = inputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to input element" );

            status = outputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to element" );

            double uAmount = data.inputValue(rnkRollNode::aParamUAmount ).asDouble();
            double vAmount = data.inputValue(rnkRollNode::aParamVAmount ).asDouble();
            MObject oSurface = data.inputValue(aSurface).asNurbsSurfaceTransformed();
            MMatrix matrix = inputsArrayHandle.inputValue().child( rnkRollNode::aMatrix ).asMatrix();
            MMatrix baseMatrix = inputsArrayHandle.inputValue().child( rnkRollNode::aBaseMatrix ).asMatrix();
            MGlobal::displayInfo(MString("THIS IS THE AMT")+uAmount+ " , " + vAmount);

            if (oSurface.isNull())
            {
                return MS::kSuccess;
            }
            //Surface Base


            //---Get Points from matrices
            MTransformationMatrix tMatrix(matrix);
            MTransformationMatrix tBaseMatrix(baseMatrix);

            MVector vMatrix = tMatrix.getTranslation(MSpace::kWorld);
            MVector vBaseMatrix = tBaseMatrix.getTranslation(MSpace::kWorld);


            MPoint pMatrix(vMatrix.x, vMatrix.y, vMatrix.z);
            MPoint pBaseMatrix(vBaseMatrix.x, vBaseMatrix.y, vBaseMatrix.z);


			MNurbsIntersector fnIntersector;
			fnIntersector.create(oSurface);

			MPointOnNurbs ptON;
			fnIntersector.getClosestPoint(pMatrix, ptON);
			MPoint UV = ptON.getUV();

			MPointOnNurbs ptONBase;
			fnIntersector.getClosestPoint(pBaseMatrix, ptONBase);
			MPoint UVB = ptONBase.getUV();


            MDataHandle paramUData = outputsArrayHandle.outputValue().child( rnkRollNode::aParamU );
            paramUData.setDouble( (UV.x - UVB.x) * uAmount );

            MDataHandle paramVData = outputsArrayHandle.outputValue().child( rnkRollNode::aParamV );
            paramVData.setDouble( (UV.y - UVB.y) * vAmount );


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

//    aDistance = nAttr.create( "distance", "dist", MFnNumericData::kFloat);
//    nAttr.setDefault(0.0);
//    nAttr.setKeyable(true);
//
//    aRadius = nAttr.create( "radius", "rad", MFnNumericData::kFloat);
//    nAttr.setKeyable(true);
//    nAttr.setDefault(0.0);
//
//    aRotAmount = nAttr.create( "rotationAmount", "rotamount", MFnNumericData::kFloat);
//    nAttr.setKeyable(true);
//    nAttr.setDefault(1.0);
//
    aParamUAmount = nAttr.create( "uParamAmount", "upa", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(1.0);
    nAttr.setChannelBox(true);
    addAttribute( aParamUAmount );

    aParamVAmount = nAttr.create( "vParamAmount", "vpa", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);

    nAttr.setDefault(1.0);
    nAttr.setChannelBox(true);
    addAttribute( aParamVAmount );


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
    cAttr.addChild( aMatrix );
    cAttr.addChild( aBaseMatrix );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aInputs);


//    aRotation = nAttr.create( "rotation", "rot", MFnNumericData::kFloat);
//    nAttr.setWritable(false);
//    nAttr.setKeyable(false);

    aParamU = nAttr.create( "parameterU", "pu", MFnNumericData::kDouble);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);

    aParamV = nAttr.create( "parameterV", "pv", MFnNumericData::kDouble);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);


    aOutputs = cAttr.create("Outputs", "outputs");
    cAttr.setKeyable(false);
    cAttr.setArray(true);
//    cAttr.addChild( aRotation );
    cAttr.addChild( aParamU );
    cAttr.addChild( aParamV );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aOutputs);

    // Effects

    aSurface = tAttr.create("surface", "sb", MFnData::kNurbsSurface);
    addAttribute( aSurface );

    attributeAffects( aSurface, aOutputs);
    attributeAffects( aParamUAmount, aOutputs);
    attributeAffects( aParamVAmount, aOutputs);
    attributeAffects( aInputs, aOutputs);

  return MS::kSuccess;
}

//---For debugging the matrices
//double sm[4][4];
//baseMatrix.get(sm);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[0][0] + sm[0][1] + sm[0][2] + sm[0][3]);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[1][0] + sm[1][1] + sm[1][2] + sm[1][3]);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[2][0] + sm[2][1] + sm[2][2] + sm[2][3]);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[3][0] + sm[3][1] + sm[3][2] + sm[3][3]);
//			MGlobal::displayInfo(MString("THIS IS THE src Values") + UV.x + "," + UV.y);
//			MGlobal::displayInfo(MString("THIS IS THE base Values") + UVB.x + "," + UVB.y);
//			MGlobal::displayInfo(MString("THIS IS THE Final ParameterValues") + (UV.x - UVB.x) + " , "+ (UV.y - UVB.y));

