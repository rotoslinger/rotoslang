#include "LHWeightNode.h"

MTypeId LHWeightNode::id(0x00093019);

MObject LHWeightNode::aOutputWeightsDoubleArray;
MObject LHWeightNode::aOutputWeightsFloatArray;
MObject LHWeightNode::aOutWeights;

MObject LHWeightNode::aInputs;
MObject LHWeightNode::aInputWeights;
MObject LHWeightNode::aFactor;
MObject LHWeightNode::aOperation;


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


MDoubleArray LHWeightNode::doubleArrayMathOperation(MDoubleArray doubleArray1,
                                                    MDoubleArray doubleArray2,
                                                    short operation)
{
    MDoubleArray rDoubleArray;
    int length1 = doubleArray1.length();
    int length2 = doubleArray2.length();

    // Only check that the arrays match if you are performing an operation on both.
    // The clamp doesn't care about doubleArray2, so no need to check.
    if (operation != 4 && length1 != length2)
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
            case 4 : // clampStack
                rDoubleArray.append(std::max(0.0, std::min(doubleArray1[i], 1.0)));
                break;
            case 5 : // clampPainted
                clampWeight = std::max(0.0, std::min((doubleArray1[i]), 1.0));
                // interp between clamped and non clamped
                rDoubleArray.append(doubleArray1[i] + (clampWeight - doubleArray1[i]) * doubleArray2[i]);
                break;
        }
    }
    return rDoubleArray;
}


MStatus LHWeightNode::compute( const MPlug& plug, MDataBlock& data)
{
    if( plug == LHWeightNode::aOutputWeightsDoubleArray)
    {
        LHWeightNode::computeDoubleArray(data);
    }
    if( plug == LHWeightNode::aOutputWeightsFloatArray)
    {
        LHWeightNode::computeFloatArray(data);
    }
    return MS::kSuccess;
}

MStatus LHWeightNode::computeDoubleArray(MDataBlock& data)
{
    MDoubleArray finalWeights;
    MStatus status = LHWeightNode::getWeightsFromInputs(data, finalWeights);
    CheckStatusReturn( status, "Unable to get weights" );

    ////////Set the final weights
    MFnDoubleArrayData outputDoubleArrayFn;
    MObject oOutputArray = outputDoubleArrayFn.create(finalWeights);
    MDataHandle handle = data.outputValue(LHWeightNode::aOutputWeightsDoubleArray);
    handle.setMObject(oOutputArray);

    if (oOutputArray.isNull())
    {
        MGlobal::displayInfo(MString("The output is NULL"));
        return MS::kSuccess;
    }
}

MStatus LHWeightNode::getWeightsFromInputs(MDataBlock& data, MDoubleArray &finalWeights)
{
    MStatus status;
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHWeightNode::aInputs, &status));
    CheckStatusReturn( status, "Unable to get inputs" );
    unsigned int elemCount = inputsArrayHandle.elementCount(&status);
    CheckStatusReturn( status, "Unable to get number of inputs" );
    // MDoubleArray finalWeights;

    for (int i=0;i < elemCount;i++)
    {
        status = inputsArrayHandle.jumpToElement(i);
        CheckStatusReturn( status, "Unable to jump to input element" );
        double dAmount = inputsArrayHandle.inputValue().child( LHWeightNode::aFactor ).asDouble();
        short operation = inputsArrayHandle.inputValue().child( LHWeightNode::aOperation ).asShort();
        if ((operation == 4 && dAmount == 0.0) || (operation == 5 && dAmount == 0.0))
        {
            return MS::kSuccess;
        }
        MDataHandle hInputArray = inputsArrayHandle.inputValue().child( LHWeightNode::aInputWeights);
        MObject oInputArray = hInputArray.data();
        MFnDoubleArrayData dataDoubleArrayFn(oInputArray);
        MDoubleArray tempWeights;
        dataDoubleArrayFn.copyTo(tempWeights);
        // This conditional makes sure not to multiply by the factor if clamping
        if (operation != 4 && operation != 5)
            LHWeightNode::multiplyKDoubleArrayByVal(tempWeights, dAmount);
        if (!finalWeights.length())
        {
            finalWeights = tempWeights;
        }
        else
            finalWeights = LHWeightNode::doubleArrayMathOperation(finalWeights, tempWeights, operation);
    }
    if (finalWeights.length() && finalWeights.length() != 0)
        return MS::kSuccess;
    else
        return MS::kFailure;

}

MStatus LHWeightNode::computeFloatArray(MDataBlock& data)
{
    MDoubleArray finalWeights;
    MStatus status = LHWeightNode::getWeightsFromInputs(data, finalWeights);
    CheckStatusReturn( status, "Unable to get weights" );
    
    MObject thisNode = thisMObject();
    MPlug parent( thisNode, LHWeightNode::aOutputWeightsFloatArray) ;
    MPlug parentElement;

    for (unsigned int j = 0; j < parent.numElements(); ++j)
    {
        parentElement = parent.elementByLogicalIndex(j, &status);
        CheckStatusReturn( status, "Unable to get unable to get parentElement" );

        MPlug child = parentElement.child(LHWeightNode::aOutWeights, &status);
        CheckStatusReturn( status, "Unable to get unable to get child" );

        for (unsigned int i = 0; i < finalWeights.length(); ++i)
        {
            MPlug childWeight = child.elementByLogicalIndex(i);
            float val = (float) finalWeights[i];
            status = childWeight.setValue(val);
        }
    }
    return MS::kSuccess;
}

void dirtyPlug(MPlug const & inPlug, MPlugArray  & affectedPlugs, MPlug outArrayPlug)
{
    if (inPlug.isElement())
    {
        // First dirty the output output element first.
        // Of course, dirty output element itself
        MPlug elemPlug = outArrayPlug.elementByLogicalIndex(
                                            inPlug.logicalIndex());
        affectedPlugs.append(elemPlug);

        // We also need to dirty the parent.
        //
        affectedPlugs.append(outArrayPlug);
    }
    else
    {
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
}

MStatus LHWeightNode::setDependentsDirty( MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs)
    {
        if ( (inPlug.attribute() != aInputs)
        & (inPlug.attribute() != aFactor)
        & (inPlug.attribute() != aInputWeights)
        & (inPlug.attribute() != aOperation))
        {
            return MS::kSuccess;
        }
        MPlug outArrayPlug(thisMObject(), aOutputWeightsDoubleArray);
        dirtyPlug(inPlug, affectedPlugs, outArrayPlug);
        MPlug outArrayPlugFloat(thisMObject(), aOutputWeightsFloatArray);
        dirtyPlug(inPlug, affectedPlugs, outArrayPlugFloat);

        return MS::kSuccess;
    }

MStatus LHWeightNode::initialize()
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

    aInputWeights = tAttr.create("inputWeights", "iw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aInputWeights);

    aOperation = eAttr.create("operation", "op", 0);
    eAttr.addField( "add", 0 );
    eAttr.addField( "subtract", 1 );
    eAttr.addField( "multiply", 2 );
    eAttr.addField( "divide", 3 );
    eAttr.addField( "clampStack", 4 );
    eAttr.addField( "clampPainted", 5 );
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
    cAttr.setIndexMatters(false);
    addAttribute(aInputs);

    aOutputWeightsDoubleArray = tAttr.create("outWeightsDoubleArray", "owd", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(false);
    tAttr.setArray(false);
    tAttr.setWritable(true);
    tAttr.setStorable(true);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutputWeightsDoubleArray);

    attributeAffects(aOperation, aOutputWeightsDoubleArray);
    attributeAffects(aInputWeights, aOutputWeightsDoubleArray);
    attributeAffects(aInputs, aOutputWeightsDoubleArray);
    attributeAffects(aFactor, aOutputWeightsDoubleArray);

    aOutWeights = nAttr.create("outFloatWeights", "outflw", MFnNumericData::kFloat, 0.0);
    nAttr.setKeyable(false);
    nAttr.setArray(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setInternal(true);
    nAttr.setIndexMatters(false);
    nAttr.setUsesArrayDataBuilder(true);

    aOutputWeightsFloatArray = cAttr.create("outWeightsFloatArray", "wlf");
    cAttr.addChild( aOutWeights );
    cAttr.setHidden(false);
    cAttr.setArray(true);
    cAttr.setChannelBox(true);
    cAttr.setConnectable(true);
    cAttr.setKeyable(false);
    cAttr.setReadable(true);
    cAttr.setInternal(true);
    cAttr.setIndexMatters(false);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutputWeightsFloatArray);

    attributeAffects(aOperation, aOutputWeightsFloatArray);
    attributeAffects(aInputWeights, aOutputWeightsFloatArray);
    attributeAffects(aInputs, aOutputWeightsFloatArray);
    attributeAffects(aFactor, aOutputWeightsFloatArray);

    return MStatus::kSuccess;
}

