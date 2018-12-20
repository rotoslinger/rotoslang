#include "LHWeightNode.h"

MTypeId LHWeightNode::id(0x00007019);

//doubles
MObject LHWeightNode::aParamUAmount;
MObject LHWeightNode::aParamVAmount;
//CompoundAttributes
MObject LHWeightNode::aOutputs;

MObject LHWeightNode::aParamU;
MObject LHWeightNode::aParamV;

MObject LHWeightNode::aMatrix;
MObject LHWeightNode::aBaseMatrix;

MObject LHWeightNode::aSurface;

//Inputs
MObject LHWeightNode::aAmount;
MObject LHWeightNode::aInputWeights;
MObject LHWeightNode::aInputs;

//Output
MObject LHWeightNode::aOutputWeights;



void* LHWeightNode::creator() { return new LHWeightNode; }

MStatus LHWeightNode::compute( const MPlug& plug, MDataBlock& data )
{
    MStatus status;
    if ( plug == LHWeightNode::aOutputWeights)
    {
        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHWeightNode::aInputs, &status));
        CheckStatusReturn( status, "Unable to get inputs" );

//        MArrayDataHandle outputsArrayHandle(data.outputArrayValue( LHWeightNode::aOutputs, &status));
//        CheckStatusReturn( status, "Unable to get outputs" );

        unsigned int elemCount = inputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get number of rotates" );

        MDoubleArray finalWeights;


        int i = 0;
        for (i=0;i < elemCount;i++)
        {
            status = inputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to input element" );

//            status = outputsArrayHandle.jumpToElement(i);
//            CheckStatusReturn( status, "Unable to jump to element" );

            double uAmount = data.inputValue(LHWeightNode::aParamUAmount ).asDouble();
            double vAmount = data.inputValue(LHWeightNode::aParamVAmount ).asDouble();
            MObject oSurface = data.inputValue(aSurface).asNurbsSurfaceTransformed();
            MMatrix matrix = inputsArrayHandle.inputValue().child( LHWeightNode::aMatrix ).asMatrix();
            MMatrix baseMatrix = inputsArrayHandle.inputValue().child( LHWeightNode::aBaseMatrix ).asMatrix();
            MGlobal::displayInfo(MString("THIS IS THE AMT")+uAmount+ " , " + vAmount);
//            MFnDoubleArrayData uAmount = data.inputValue(LHWeightNode::aParamUAmount ).asDouble();

            MDoubleArray weights;
            MDataHandle inputWeights = inputsArrayHandle.inputValue().child( LHWeightNode::aInputWeights );
            weights = MFnDoubleArrayData(inputWeights.data()).array();



        }
        MDataHandle hOutputWeights = data.outputValue(aOutputWeights);
        hOutput.setFloat(inputValue);
        data.setClean( plug );

    }
    return MS::kSuccess;
}

MStatus LHWeightNode::initialize() {
	MStatus status ;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnTypedAttribute tAttr;
    MFnMatrixAttribute mAttr;

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


    ////////WIEGHTS
    aInputWeights = tAttr.create("inWeights", "iw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);

    aAmount = nAttr.create( "amount", "a", MFnNumericData::kDouble);
    nAttr.setWritable(true);
    nAttr.setKeyable(true);
    nAttr.setConnectable(true);



    aInputs = cAttr.create("Inputs", "inputs");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aMatrix );
    cAttr.addChild( aBaseMatrix );
    cAttr.addChild( aInputWeights );
    cAttr.addChild( aAmount );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aInputs);


    aParamU = nAttr.create( "parameterU", "pu", MFnNumericData::kDouble);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);

    aParamV = nAttr.create( "parameterV", "pv", MFnNumericData::kDouble);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);


    aOutputs = cAttr.create("Outputs", "outputs");
    cAttr.setKeyable(false);
    cAttr.setArray(true);
    cAttr.addChild( aParamU );
    cAttr.addChild( aParamV );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aOutputs);


    ////////WIEGHTS
    aOutputWeights = tAttr.create("outWeights", "ow", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(false);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutputWeights);


    // Effects

    aSurface = tAttr.create("surface", "sb", MFnData::kNurbsSurface);
    addAttribute( aSurface );

    attributeAffects( aSurface, aOutputs);
    attributeAffects( aParamUAmount, aOutputs);
    attributeAffects( aParamVAmount, aOutputs);
    attributeAffects( aInputs, aOutputs);
    attributeAffects( aInputs, aOutputWeights);

  return MS::kSuccess;
}

