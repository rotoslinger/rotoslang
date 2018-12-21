#include "LHWeightNode.h"

MTypeId LHWeightNode::id(0x00007019);

MObject LHWeightNode::aWeightsList;
MObject LHWeightNode::aWeights;
MObject LHWeightNode::aBias;
MObject LHWeightNode::aOutputWeights;
MObject LHWeightNode::aInputWeights;
MObject LHWeightNode::aBiasOut;
MObject LHWeightNode::aInputs;
MObject LHWeightNode::aTestWeights;
MObject LHWeightNode::aAmount;


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


MDoubleArray LHWeightNode::addDoubleArrays(MDoubleArray doubleArray1, MDoubleArray doubleArray2)
{
    MDoubleArray rDoubleArray;
    int length1 = doubleArray1.length();
    int length2 = doubleArray2.length();
    if (length1 != length2)
    {
        return rDoubleArray;
    }
    for (int i=0;i < length1;i++)
    {
        rDoubleArray.append(doubleArray1[i] + doubleArray2[i]);
    }
    return rDoubleArray;
}




MStatus LHWeightNode::compute( const MPlug& plug, MDataBlock& data)
{
    MStatus status;
//    if( plug != LHWeightNode::aOutputWeights ) { return MS::kUnknownParameter; }
//    if( plug == LHWeightNode::aOutputWeights or  plug == LHWeightNode::aOutputWeights)
//    if( plug == LHWeightNode::aBiasOut or plug == LHWeightNode::aOutputWeights)
    if( plug == LHWeightNode::aBiasOut or plug == LHWeightNode::aOutputWeights)
    {
//        MArrayDataHandle outputsHnd = data.outputArrayValue( LHWeightNode::aOutputWeights );
//        MArrayDataHandle inputsHnd = data.inputArrayValue( LHWeightNode::aInputWeights );

        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHWeightNode::aInputs, &status));
        CheckStatusReturn( status, "Unable to get inputs" );
        unsigned int elemCount = inputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get number of inputs" );
        MDoubleArray finalWeights;
        for (int i=0;i < elemCount;i++)
        {

            status = inputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to input element" );
            double dAmount = inputsArrayHandle.inputValue().child( LHWeightNode::aAmount ).asDouble();

            MDataHandle hInputArray = inputsArrayHandle.inputValue().child( LHWeightNode::aInputWeights);

            MObject oInputArray = hInputArray.data();
            MFnDoubleArrayData dataDoubleArrayFn(oInputArray);
            MDoubleArray tempWeights;
            dataDoubleArrayFn.copyTo(tempWeights);
            LHWeightNode::multiplyKDoubleArrayByVal(tempWeights, dAmount);
            if (!finalWeights.length())
            {
                finalWeights = tempWeights;
            }
            else
                finalWeights = LHWeightNode::addDoubleArrays(finalWeights, tempWeights);
//            hInputArray.setClean();

        }
        MGlobal::displayInfo(MString("Weight array length ")+finalWeights.length());






        double inputValue = data.inputValue(LHWeightNode::aBias).asDouble();


//        MDataHandle hInputArray = data.inputValue( LHWeightNode::aInputWeights );
//        MObject oInputArray = hInputArray.data();
//        MFnDoubleArrayData dataDoubleArrayFn(oInputArray);
//        MDoubleArray arrayDataToSet;
//        dataDoubleArrayFn.copyTo(arrayDataToSet);
//        if (oInputArray.isNull())
//        {
//            MGlobal::displayInfo(MString("The MDataHandle InputArray is NULL"));
//            return MS::kSuccess;
//
//        }
//        ///////// Multiply values
//        LHWeightNode::multiplyKDoubleArrayByVal(arrayDataToSet, inputValue);


        ////////Set the final weights
        MFnDoubleArrayData outputDoubleArrayFn;
        MObject oOutputArray = outputDoubleArrayFn.create(finalWeights);
        MDataHandle handle = data.outputValue(LHWeightNode::aOutputWeights);
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
//        handle.setClean();
//        hInputArray.setClean();
//        data.setClean( plug );

    }

    return MS::kSuccess;
}



MStatus LHWeightNode::setDependentsDirty( MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs)
    {
        if ( inPlug.attribute() != aInputs
        and inPlug.attribute() != aInputWeights
        and inPlug.attribute() != aAmount
        and inPlug.attribute() != aTestWeights
        and inPlug.attribute() != aInputs)
        {
            return MS::kSuccess;
        }

        MPlug outArrayPlug(thisMObject(), aOutputWeights);

        if (inPlug.isElement()) {
            // First dirty the output output element first.
            // Of course, dirty output element itself
            MPlug elemPlug = outArrayPlug.elementByLogicalIndex(
                                                inPlug.logicalIndex());
            affectedPlugs.append(elemPlug);

            // We also need to dirty the parent.
            //
            affectedPlugs.append(outArrayPlug);
        } else {
            // Mark the parent output plug as dirty.
            //
            affectedPlugs.append(outArrayPlug);

            // Also visit each element.
            //
            unsigned int i,n = outArrayPlug.numElements();
            for (i = 0; i < n; i++) {
                MPlug elemPlug = outArrayPlug.elementByPhysicalIndex(i);
                affectedPlugs.append(elemPlug);
            }
        }
        return MS::kSuccess;
    }


MStatus LHWeightNode::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;

    aAmount = nAttr.create( "amount", "amt", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(0.0);
    nAttr.setChannelBox(true);
    addAttribute(aAmount);


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

    ////////////////////////////////Test///////////////////////
    aTestWeights = tAttr.create("testWeights", "tw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aTestWeights);
    ////////////////////////////////Test///////////////////////


    aInputs = cAttr.create("Inputs", "inputs");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aTestWeights );
    cAttr.addChild( aAmount );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aInputs);



    aOutputWeights = tAttr.create("outWeights", "ow", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setWritable(true);
    tAttr.setStorable(true);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutputWeights);

    attributeAffects(aTestWeights, aOutputWeights);
    attributeAffects(aInputs, aOutputWeights);
    attributeAffects(aInputs, aBiasOut);
    attributeAffects(aBias, aOutputWeights);
    attributeAffects(aInputWeights, aOutputWeights);
    attributeAffects(aBias, aBiasOut);
    attributeAffects(aInputWeights, aBiasOut);
    attributeAffects(aInputs, aBiasOut);
    attributeAffects(aTestWeights, aBiasOut);
    attributeAffects(aAmount, aBiasOut);

    return MStatus::kSuccess;
}

