#include "LHKDoubleArrayToKFloatArray.h"

MTypeId LHKDoubleArrayToKFloatArray::id(0x00568819);

MObject LHKDoubleArrayToKFloatArray::aWeightsList;
MObject LHKDoubleArrayToKFloatArray::aWeights;
MObject LHKDoubleArrayToKFloatArray::aBias;
MObject LHKDoubleArrayToKFloatArray::aOutputWeights;
MObject LHKDoubleArrayToKFloatArray::aInputWeights;
MObject LHKDoubleArrayToKFloatArray::aBiasOut;
MObject LHKDoubleArrayToKFloatArray::aInputs;
MObject LHKDoubleArrayToKFloatArray::aTestWeights;
MObject LHKDoubleArrayToKFloatArray::aAmount;
MObject LHKDoubleArrayToKFloatArray::aOperation;
MObject LHKDoubleArrayToKFloatArray::aTestKFloatArray;


void* LHKDoubleArrayToKFloatArray::creator() { return new LHKDoubleArrayToKFloatArray; }


MStatus LHKDoubleArrayToKFloatArray::multiplyKDoubleArrayByVal(MDoubleArray &rDoubleArray, double val)
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


MDoubleArray LHKDoubleArrayToKFloatArray::doubleArrayMathOperation(MDoubleArray doubleArray1,
                                                    MDoubleArray doubleArray2,
                                                    short operation)
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

        switch( operation )
        {
            case 0 : // add
                rDoubleArray.append(doubleArray1[i] + doubleArray2[i]);
                break;
            case 1 : // subtract
                rDoubleArray.append(doubleArray1[i] - doubleArray2[i]);
                break;
            case 2 : // multiply
                rDoubleArray.append(doubleArray1[i] * doubleArray2[i]);
                break;
            case 3 : // divide
                if (doubleArray1[i] == 0.0)
                {
                    doubleArray1[i] = .00001;
                }
                if (doubleArray2[i] == 0.0)
                {
                    doubleArray2[i] = .00001;
                }
                rDoubleArray.append(doubleArray1[i] / doubleArray2[i]);
                break;
        }








//        if (operation == "add")
//        {
//            rDoubleArray.append(doubleArray1[i] + doubleArray2[i]);
//        }
//        if (operation == "subtract")
//        {
//            rDoubleArray.append(doubleArray1[i] - doubleArray2[i]);
//        }
//        if (operation == "multiply")
//        {
//            rDoubleArray.append(doubleArray1[i] * doubleArray2[i]);
//        }
//        if (operation == "divide")
//        {
//            if (doubleArray1[i] == 0.0)
//            {
//                doubleArray1[i] = .00001;
//            }
//            if (doubleArray2[i] == 0.0)
//            {
//                doubleArray2[i] = .00001;
//            }
//            rDoubleArray.append(doubleArray1[i] / doubleArray2[i]);
//        }
    }
    return rDoubleArray;
}




MStatus LHKDoubleArrayToKFloatArray::compute( const MPlug& plug, MDataBlock& data)
{
    MStatus status;
//    if( plug != LHKDoubleArrayToKFloatArray::aOutputWeights ) { return MS::kUnknownParameter; }
//    if( plug == LHKDoubleArrayToKFloatArray::aOutputWeights or  plug == LHKDoubleArrayToKFloatArray::aOutputWeights)
//    if( plug == LHKDoubleArrayToKFloatArray::aBiasOut or plug == LHKDoubleArrayToKFloatArray::aOutputWeights)
    if( plug == LHKDoubleArrayToKFloatArray::aBiasOut or plug == LHKDoubleArrayToKFloatArray::aOutputWeights)
    {
//        MArrayDataHandle outputsHnd = data.outputArrayValue( LHKDoubleArrayToKFloatArray::aOutputWeights );
//        MArrayDataHandle inputsHnd = data.inputArrayValue( LHKDoubleArrayToKFloatArray::aInputWeights );

        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHKDoubleArrayToKFloatArray::aInputs, &status));
        CheckStatusReturn( status, "Unable to get inputs" );
        unsigned int elemCount = inputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get number of inputs" );
        MDoubleArray finalWeights;
//        MString tempOperation = "add";

        for (int i=0;i < elemCount;i++)
        {

            status = inputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to input element" );
            double dAmount = inputsArrayHandle.inputValue().child( LHKDoubleArrayToKFloatArray::aAmount ).asDouble();
            short operation = inputsArrayHandle.inputValue().child( LHKDoubleArrayToKFloatArray::aOperation ).asShort();
            MDataHandle hInputArray = inputsArrayHandle.inputValue().child( LHKDoubleArrayToKFloatArray::aInputWeights);
            MObject oInputArray = hInputArray.data();
            MFnDoubleArrayData dataDoubleArrayFn(oInputArray);
            MDoubleArray tempWeights;
            dataDoubleArrayFn.copyTo(tempWeights);
            LHKDoubleArrayToKFloatArray::multiplyKDoubleArrayByVal(tempWeights, dAmount);
            if (!finalWeights.length())
            {
                finalWeights = tempWeights;
            }
            else
                finalWeights = LHKDoubleArrayToKFloatArray::doubleArrayMathOperation(finalWeights, tempWeights, operation);
//            hInputArray.setClean();

        }
        MGlobal::displayInfo(MString("Weight array length ")+finalWeights.length());






        double inputValue = data.inputValue(LHKDoubleArrayToKFloatArray::aBias).asDouble();


//        MDataHandle hInputArray = data.inputValue( LHKDoubleArrayToKFloatArray::aInputWeights );
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
//        LHKDoubleArrayToKFloatArray::multiplyKDoubleArrayByVal(arrayDataToSet, inputValue);


        ////////Set the final weights
        MFnDoubleArrayData outputDoubleArrayFn;
        MObject oOutputArray = outputDoubleArrayFn.create(finalWeights);
        MDataHandle handle = data.outputValue(LHKDoubleArrayToKFloatArray::aOutputWeights);
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



MStatus LHKDoubleArrayToKFloatArray::setDependentsDirty( MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs)
    {
        if ( inPlug.attribute() != aInputs
        and inPlug.attribute() != aInputWeights
        and inPlug.attribute() != aAmount
        and inPlug.attribute() != aTestWeights
        and inPlug.attribute() != aInputs
        and inPlug.attribute() != aOperation)
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


MStatus LHKDoubleArrayToKFloatArray::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnEnumAttribute eAttr;

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

    aOperation = eAttr.create("operation", "op", 0);
    eAttr.addField( "add", 0 );
    eAttr.addField( "subtract", 1 );
    eAttr.addField( "multiply", 2 );
    eAttr.addField( "divide", 3 );
    eAttr.setHidden( false );
    eAttr.setKeyable( true );
    eAttr.setWritable(true);
    eAttr.setStorable(true);
    eAttr.setChannelBox(true);
    addAttribute(aOperation);

    aInputs = cAttr.create("Inputs", "inputs");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aTestWeights );
    cAttr.addChild( aAmount );
    cAttr.addChild( aOperation );
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



    aTestKFloatArray = nAttr.create("testKFloat", "tkf", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setArray(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setUsesArrayDataBuilder(true);
    addAttribute(aTestKFloatArray);




    attributeAffects(aOperation, aOutputWeights);
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

