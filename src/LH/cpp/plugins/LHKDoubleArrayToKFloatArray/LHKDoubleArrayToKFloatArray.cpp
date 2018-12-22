#include "LHKDoubleArrayToKFloatArray.h"

MTypeId LHKDoubleArrayToKFloatArray::id(0x00568819);

MObject LHKDoubleArrayToKFloatArray::aBias;
MObject LHKDoubleArrayToKFloatArray::aBiasOut;

MObject LHKDoubleArrayToKFloatArray::aInWeights;
MObject LHKDoubleArrayToKFloatArray::aOutWeights;


void* LHKDoubleArrayToKFloatArray::creator() { return new LHKDoubleArrayToKFloatArray; }

MStatus LHKDoubleArrayToKFloatArray::compute( const MPlug& plug, MDataBlock& data)
{
    MStatus status;
    if(plug == LHKDoubleArrayToKFloatArray::aOutWeights or plug == LHKDoubleArrayToKFloatArray::aBiasOut)
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
        MGlobal::displayInfo(MString("The MDataHandle InputArray is Connected"));



        MArrayDataHandle hOutArray = data.outputArrayValue( aOutWeights, &status);
        if (!status)
        {
            MGlobal::displayInfo(MString("The MArrayDataHandle hOutArray is NULL"));
        }
        MArrayDataBuilder bOutArray = hOutArray.builder( &status );
        if (!status)
        {
            MGlobal::displayInfo(MString("The MArrayDataBuilder bOutArray is NULL"));
        }
        for( int i = 0; i < arrayDataToSet.length(); i++)
        {
            MDataHandle hOut = bOutArray.addElement(i, &status);
            if (!status)
            {
                MGlobal::displayInfo(MString("couldnt add element"));
            }
            else
            {
                float val = (float) arrayDataToSet[i];
                hOut.set(val);
            }
        }
        //
        hOutArray.set(bOutArray);
        data.setClean( plug );










        double inputValue = data.inputValue(LHKDoubleArrayToKFloatArray::aBias).asDouble();
        MDataHandle outputDataHandle = data.outputValue( aBiasOut, &status );
        outputDataHandle.setDouble( inputValue );
    }

    return MS::kSuccess;
}



MStatus LHKDoubleArrayToKFloatArray::setDependentsDirty( MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs)
    {
        if ( inPlug.attribute() != aInWeights
         and inPlug.attribute() != aBias)
        {
            return MS::kSuccess;
        }

        MPlug outArrayPlug(thisMObject(), aOutWeights);

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
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aInWeights);



    aOutWeights = nAttr.create("outWeights", "ow", MFnNumericData::kFloat);
    nAttr.setKeyable(false);
    nAttr.setChannelBox(false);
    nAttr.setConnectable(true);
    nAttr.setArray(true);
    nAttr.setWritable(false);
    nAttr.setStorable(true);
    nAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutWeights);








    attributeAffects(aInWeights, aOutWeights);










    return MStatus::kSuccess;
}

