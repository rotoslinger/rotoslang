#include "LHWeightNode.h"

MTypeId LHWeightNode::id(0x00093019);

MObject LHWeightNode::aOutputWeights;
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
    }
    return rDoubleArray;
}


MStatus LHWeightNode::compute( const MPlug& plug, MDataBlock& data)
{
    MStatus status;
    if( plug == LHWeightNode::aOutputWeights)
    {
        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHWeightNode::aInputs, &status));
        CheckStatusReturn( status, "Unable to get inputs" );
        unsigned int elemCount = inputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get number of inputs" );
        MDoubleArray finalWeights;

        for (int i=0;i < elemCount;i++)
        {
            MGlobal::displayInfo(MString("UPDATING"));

            status = inputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to input element" );
            double dAmount = inputsArrayHandle.inputValue().child( LHWeightNode::aFactor ).asDouble();
            short operation = inputsArrayHandle.inputValue().child( LHWeightNode::aOperation ).asShort();
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
                finalWeights = LHWeightNode::doubleArrayMathOperation(finalWeights, tempWeights, operation);
//            hInputArray.setClean();

        }

        ////////Set the final weights
        MFnDoubleArrayData outputDoubleArrayFn;
        MObject oOutputArray = outputDoubleArrayFn.create(finalWeights);
        MDataHandle handle = data.outputValue(LHWeightNode::aOutputWeights);
        handle.setMObject(oOutputArray);

//        MGlobal::displayInfo(MString("DEBUG:  UPDATING ") + status);

        if (oOutputArray.isNull())
        {
            MGlobal::displayInfo(MString("The output is NULL"));
            return MS::kSuccess;
        }
    }

    return MS::kSuccess;
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

    aOutputWeights = tAttr.create("outWeights", "ow", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setWritable(true);
    tAttr.setStorable(true);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutputWeights);

    attributeAffects(aOperation, aOutputWeights);
    attributeAffects(aInputWeights, aOutputWeights);
    attributeAffects(aInputs, aOutputWeights);
    attributeAffects(aFactor, aOutputWeights);

    return MStatus::kSuccess;
}

