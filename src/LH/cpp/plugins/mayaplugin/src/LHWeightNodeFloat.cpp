#include "LHWeightNodeFloat.h"

MTypeId LHWeightNodeFloat::id(0x00054019);

MObject LHWeightNodeFloat::aOutputWeights;
MObject LHWeightNodeFloat::aInputs;
MObject LHWeightNodeFloat::aInputWeights;
MObject LHWeightNodeFloat::aFactor;
MObject LHWeightNodeFloat::aOperation;
MObject LHWeightNodeFloat::aWeightList;


void* LHWeightNodeFloat::creator() { return new LHWeightNodeFloat; }


MStatus LHWeightNodeFloat::multiplyKFloatArrayByVal(MFloatArray &rFloatArray, double val)
{
    int len = rFloatArray.length();
    if (!len)
    {
        return MS::kFailure;
    }
    for (int i= 0; i < len; ++i)
    {
        rFloatArray[i] = rFloatArray[i] * val;
    }
    return MS::kSuccess;
}


MFloatArray LHWeightNodeFloat::floatArrayMathOperation(MFloatArray floatArray1,
                                                    MFloatArray floatArray2,
                                                    short operation)
{
    MFloatArray rFloatArray;
    int length1 = floatArray1.length();
    int length2 = floatArray2.length();
    if (length1 != length2)
    {
        return rFloatArray;
    }
    for (int i=0;i < length1;i++)
    {

        switch( operation )
        {
            case 0 : // add
                rFloatArray.append(floatArray1[i] + floatArray2[i]);
                break;
            case 1 : // subtract
                rFloatArray.append(floatArray1[i] - floatArray2[i]);
                break;
            case 2 : // multiply
                rFloatArray.append(floatArray1[i] * floatArray2[i]);
                break;
            case 3 : // divide
                if (floatArray1[i] == 0.0)
                {
                    floatArray1[i] = .00001;
                }
                if (floatArray2[i] == 0.0)
                {
                    floatArray2[i] = .00001;
                }
                rFloatArray.append(floatArray1[i] / floatArray2[i]);
                break;
        }
    }
    return rFloatArray;
}




MStatus LHWeightNodeFloat::compute( const MPlug& plug, MDataBlock& data)
{
    MStatus status;
    if( plug == LHWeightNodeFloat::aWeightList)
    {
        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHWeightNodeFloat::aInputs, &status));
        CheckStatusReturn( status, "Unable to get inputs" );
        unsigned int elemCount = inputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get number of inputs" );
        MFloatArray finalWeights;

        for (int i=0;i < elemCount;i++)
        {
            status = inputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to input element" );
            double dAmount = inputsArrayHandle.inputValue().child( LHWeightNodeFloat::aFactor ).asDouble();
            short operation = inputsArrayHandle.inputValue().child( LHWeightNodeFloat::aOperation ).asShort();
            MDataHandle hInputArray = inputsArrayHandle.inputValue().child( LHWeightNodeFloat::aInputWeights);
            MObject oInputArray = hInputArray.data();
            MFnFloatArrayData dataFloatArrayFn(oInputArray);
            MFloatArray tempWeights;
            dataFloatArrayFn.copyTo(tempWeights);
            LHWeightNodeFloat::multiplyKFloatArrayByVal(tempWeights, dAmount);
            if (!finalWeights.length())
            {
                finalWeights = tempWeights;
            }
            else
                finalWeights = LHWeightNodeFloat::floatArrayMathOperation(finalWeights, tempWeights, operation);
//            hInputArray.setClean();

        }






//        MDataHandle hInputArray = data.inputValue( LHWeightNodeFloat::aInWeights );
//        MObject oInputArray = hInputArray.data();
//        MFnDoubleArrayData dataDoubleArrayFn(oInputArray);
//        MDoubleArray arrayDataToSet;
//        dataDoubleArrayFn.copyTo(arrayDataToSet);

        MObject thisNode = thisMObject();
        MPlug parent( thisNode, LHWeightNodeFloat::aWeightList) ;
        MPlug parentElement;

        for (unsigned int j = 0; j < parent.numElements(); ++j)
        {
            parentElement = parent.elementByLogicalIndex(j, &status);
            CheckStatusReturn( status, "Unable to get unable to get parentElement" );

            MPlug child = parentElement.child(LHWeightNodeFloat::aOutputWeights, &status);
            CheckStatusReturn( status, "Unable to get unable to get child" );

            for (unsigned int i = 0; i < finalWeights.length(); ++i)
            {
                MPlug childWeight = child.elementByLogicalIndex(i);
                float val = finalWeights[i];
                status = childWeight.setValue(val);
            }
        }
        MGlobal::displayInfo(MString("updating"));






        ////////Set the final weights
//        MFnFloatArrayData outputFloatArrayFn;
//        MObject oOutputArray = outputFloatArrayFn.create(finalWeights);
//        MDataHandle handle = data.outputValue(LHWeightNodeFloat::aOutputWeights);
//        handle.setMObject(oOutputArray);

//        MGlobal::displayInfo(MString("DEBUG:  UPDATING ") + status);

    }

    return MS::kSuccess;
}


MStatus LHWeightNodeFloat::setDependentsDirty( MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs)
    {
        if ( inPlug.attribute() != aInputs
        and inPlug.attribute() != aFactor
        and inPlug.attribute() != aInputWeights
        and inPlug.attribute() != aOperation)
        {
            return MS::kSuccess;
        }

        MPlug outArrayPlug(thisMObject(), aWeightList);

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


MStatus LHWeightNodeFloat::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnEnumAttribute eAttr;

    /////// Attrs for compound
    aFactor = nAttr.create( "factor", "f", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(0.0);
    nAttr.setChannelBox(true);
    addAttribute(aFactor);

    aInputWeights = tAttr.create("inputWeights", "iw", MFnNumericData::kFloatArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aInputWeights);

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
    cAttr.addChild( aInputWeights );
    cAttr.addChild( aFactor );
    cAttr.addChild( aOperation );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aInputs);

    aOutputWeights = nAttr.create("outWeights", "ow", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setArray(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setInternal(true);
    nAttr.setIndexMatters(true);
    nAttr.setUsesArrayDataBuilder(true);
    //addAttribute(aOutputWeights);


    aWeightList = cAttr.create("weightList", "wl");
    cAttr.addChild( aOutputWeights );
    cAttr.setHidden(false);
    cAttr.setArray(true);
    cAttr.setChannelBox(true);
    cAttr.setConnectable(true);
    cAttr.setKeyable(true);
    cAttr.setReadable(true);
    cAttr.setInternal(true);
    cAttr.setIndexMatters(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aWeightList);







    attributeAffects(aOperation, aOutputWeights);
    attributeAffects(aInputWeights, aOutputWeights);
    attributeAffects(aInputs, aOutputWeights);
    attributeAffects(aFactor, aOutputWeights);

    attributeAffects(aOperation, aWeightList);
    attributeAffects(aInputWeights, aWeightList);
    attributeAffects(aInputs, aWeightList);
    attributeAffects(aFactor, aWeightList);




    return MStatus::kSuccess;
}

