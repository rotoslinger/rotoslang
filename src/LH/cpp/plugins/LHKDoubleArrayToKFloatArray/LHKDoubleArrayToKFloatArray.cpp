#include "LHKDoubleArrayToKFloatArray.h"

MTypeId LHKDoubleArrayToKFloatArray::id(0x00568819);

MObject LHKDoubleArrayToKFloatArray::aInWeights;
MObject LHKDoubleArrayToKFloatArray::aOutWeights;
MObject LHKDoubleArrayToKFloatArray::aOutWeightList;
MObject LHKDoubleArrayToKFloatArray::aBias;
MObject LHKDoubleArrayToKFloatArray::aBiasOut;


void* LHKDoubleArrayToKFloatArray::creator() { return new LHKDoubleArrayToKFloatArray; }

MStatus LHKDoubleArrayToKFloatArray::compute( const MPlug& plug, MDataBlock& data)
{
    MStatus status;
    if(plug == LHKDoubleArrayToKFloatArray::aOutWeightList or plug == LHKDoubleArrayToKFloatArray::aBiasOut or plug == LHKDoubleArrayToKFloatArray::aOutWeights)
    {
        MDataHandle hInputArray = data.inputValue( LHKDoubleArrayToKFloatArray::aInWeights );
        MObject oInputArray = hInputArray.data();
        MFnDoubleArrayData dataDoubleArrayFn(oInputArray);
        MDoubleArray arrayDataToSet;
        dataDoubleArrayFn.copyTo(arrayDataToSet);
        if (oInputArray.isNull())
        {
            MGlobal::displayInfo(MString("The MDataHandle InputArray is NULL"));
            return MS::kSuccess;
        }

        MObject thisNode = thisMObject();
        MPlug parent( thisNode, LHKDoubleArrayToKFloatArray::aOutWeightList) ;
        MPlug parentElement;

        for (unsigned int j = 0; j < parent.numElements(); ++j)

            parentElement = parent.elementByLogicalIndex(j, &status);
            CheckStatusReturn( status, "Unable to get unable to get parentElement" );

            MPlug child = parentElement.child(LHKDoubleArrayToKFloatArray::aOutWeights, &status);
            CheckStatusReturn( status, "Unable to get unable to get child" );

            for (unsigned int i = 0; i < arrayDataToSet.length(); ++i)
            {
                MPlug childWeight = child.elementByLogicalIndex(i);
                float val = (float) arrayDataToSet[i];
                status = childWeight.setValue(val);
            }
        double inputValue = data.inputValue(LHKDoubleArrayToKFloatArray::aBias).asDouble();
        MDataHandle outputDataHandle = data.outputValue( aBiasOut, &status );
        outputDataHandle.setDouble( inputValue );
        MGlobal::displayInfo(MString("updating"));

//        data.setClean( plug );
    }

    return MS::kSuccess;
}



MStatus LHKDoubleArrayToKFloatArray::setDependentsDirty( MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs)
    {
        if ( inPlug.attribute() != aInWeights)
        {
            return MS::kSuccess;
        }
        MPlugArray outputPlugs;
        MPlug outArrayPlug(thisMObject(), aOutWeightList);

        if (inPlug.isElement()) {
            // First dirty the output output element first.
            // Of course, dirty output element itself
            MPlug elemPlug = outArrayPlug.elementByLogicalIndex(inPlug.logicalIndex());
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




    aInWeights = tAttr.create("inWeights", "iw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setWritable(true);
    tAttr.setStorable(true);
    tAttr.setConnectable(true);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aInWeights);



    aOutWeights = nAttr.create("outFloatWeights", "outflw", MFnNumericData::kFloat, 0.0);
    nAttr.setKeyable(true);
    nAttr.setArray(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setInternal(true);
    nAttr.setIndexMatters(true);
    nAttr.setUsesArrayDataBuilder(true);



    aOutWeightList = cAttr.create("outFloatWeightList", "outflwl");
    cAttr.addChild( aOutWeights );
    cAttr.setHidden(false);
    cAttr.setArray(true);
    cAttr.setChannelBox(true);
    cAttr.setConnectable(true);
    cAttr.setKeyable(true);
    cAttr.setReadable(true);
    cAttr.setInternal(true);
    cAttr.setIndexMatters(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutWeightList);

    attributeAffects(aInWeights, aOutWeights);
    attributeAffects(aInWeights, aOutWeightList);










    return MStatus::kSuccess;
}

