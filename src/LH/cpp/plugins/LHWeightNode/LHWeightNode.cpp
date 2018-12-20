#include "LHWeightNode.h"

MTypeId LHWeightNode::id(0x00007019);

MObject LHWeightNode::aWeightsList;
MObject LHWeightNode::aWeights;
MObject LHWeightNode::aBias;
MObject LHWeightNode::aOutputWeights;
MObject LHWeightNode::aInputWeights;
MObject LHWeightNode::aOutputWeightArray;
MObject LHWeightNode::aBiasOut;


void* LHWeightNode::creator() { return new LHWeightNode; }


MStatus LHWeightNode::multiplyKDoubleArrayByVal(MDoubleArray &rDoubleArray, double val)
{
    int len = rDoubleArray.length();
    if (!len)
    {
        return MS::kFailure;
    }
    for (int i= 0; i < len; ++i)
    {
        rDoubleArray[i] = rDoubleArray[i] * val;
    }
    return MS::kSuccess;
}


MDoubleArray LHWeightNode::addDoubleArrays(MDoubleArray doubleArray1,
                                      MDoubleArray doubleArray2)
{
    MDoubleArray rDoubleArray;
    return rDoubleArray;
}




MStatus LHWeightNode::compute( const MPlug& plug, MDataBlock& data)
{
    MStatus status;
//    if( plug != LHWeightNode::aOutputWeightArray ) { return MS::kUnknownParameter; }
//    if( plug == LHWeightNode::aOutputWeightArray or  plug == LHWeightNode::aOutputWeights)
//    if( plug == LHWeightNode::aBiasOut or plug == LHWeightNode::aOutputWeightArray)
    if( plug == LHWeightNode::aBiasOut or plug == LHWeightNode::aOutputWeightArray)
    {
//        MArrayDataHandle outputsHnd = data.outputArrayValue( LHWeightNode::aOutputWeights );
//        MArrayDataHandle inputsHnd = data.inputArrayValue( LHWeightNode::aInputWeights );

        double inputValue = data.inputValue(LHWeightNode::aBias).asDouble();


        MDataHandle hInputArray = data.inputValue( LHWeightNode::aInputWeights );
        MObject oInputArray = hInputArray.data();
        MFnDoubleArrayData dataDoubleArrayFn(oInputArray);
        MDoubleArray arrayDataToSet;
        dataDoubleArrayFn.copyTo(arrayDataToSet);
        if (oInputArray.isNull())
        {
            MGlobal::displayInfo(MString("The MDataHandle InputArray is NULL"));
            return MS::kSuccess;

        }
        ///////// Multiply values
        LHWeightNode::multiplyKDoubleArrayByVal(arrayDataToSet, inputValue);


        MFnDoubleArrayData outputDoubleArrayFn;
        MObject oOutputArray = outputDoubleArrayFn.create(arrayDataToSet);
        MDataHandle handle = data.outputValue(LHWeightNode::aOutputWeightArray);
        handle.setMObject(oOutputArray);

        MGlobal::displayInfo(MString("DEBUG:  UPDATING ") + status);

        if (oOutputArray.isNull())
        {
            MGlobal::displayInfo(MString("The MObject hOutputArray is NULL"));
            return MS::kSuccess;


        }
//        if (!oOutputArray.isNull())
//        {
//            MGlobal::displayInfo(MString("The MDataHandle hOutputArray is NOT NULL!!!!!!"));
//
//        }


        MDataHandle outputDataHandle = data.outputValue( aBiasOut, &status );
        outputDataHandle.setDouble( inputValue );
        handle.setClean();
        hInputArray.setClean();
        data.setClean( plug );

    }

    return MS::kSuccess;
}

MStatus LHWeightNode::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cmpAttr;

    aBias = nAttr.create( "bias", "b", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(1.0);
    nAttr.setChannelBox(true);
    addAttribute(aBias);

    aBiasOut = nAttr.create( "biasOut", "bOut", MFnNumericData::kDouble);
    nAttr.setReadable(true);
    nAttr.setWritable(true);
    nAttr.setConnectable(true);
    nAttr.setChannelBox(true);
    nAttr.setKeyable(false);
    addAttribute(aBiasOut);
    attributeAffects(aBias, aBiasOut);



    aInputWeights = tAttr.create("inWeights", "iw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aInputWeights);

    aOutputWeightArray = tAttr.create("outWeights", "ow", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setWritable(true);
    tAttr.setStorable(true);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutputWeightArray);


    attributeAffects(aBias, aOutputWeightArray);
    attributeAffects(aInputWeights, aOutputWeightArray);
    attributeAffects(aBias, aBiasOut);
    attributeAffects(aInputWeights, aBiasOut);

    return MStatus::kSuccess;
}

