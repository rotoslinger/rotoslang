#include "LHBlendRemap.h"

MTypeId LHBlendRemap::id(0x00007345);

//Floats
MObject LHBlendRemap::aCachePlugs;
MObject LHBlendRemap::aInVal;
MObject LHBlendRemap::aRemapOne;
MObject LHBlendRemap::aRemapNegOne;
MObject LHBlendRemap::aPosOut;
MObject LHBlendRemap::aNegOut;

//CompoundAttributes
MObject LHBlendRemap::aInputs;
MObject LHBlendRemap::aOutputs;


void* LHBlendRemap::creator() { return new LHBlendRemap; }

MStatus LHBlendRemap::compute( const MPlug& plug, MDataBlock& data )
{
    MStatus status;
    if ( plug == LHBlendRemap::aPosOut or plug == LHBlendRemap::aNegOut)
    {

//        int cachePlugs = data.inputValue( LHBlendRemap::aCachePlugs).asInt();

        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHBlendRemap::aInputs, &status));
        CheckStatusReturn( status, "Unable to get inputs" );

        MArrayDataHandle outputsArrayHandle(data.outputArrayValue( LHBlendRemap::aOutputs, &status));
        CheckStatusReturn( status, "Unable to get outputs" );

        unsigned int outCount = outputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get number of rotates" );

        int i = 0;
        for (i=0;i < outCount;i++)
        {
            status = inputsArrayHandle.jumpToArrayElement(i);
            CheckStatusReturn( status, "Unable to jump to input element, you have more outputs than inputs" );

            status = outputsArrayHandle.jumpToArrayElement(i);
            CheckStatusReturn( status, "Unable to jump to element" );

            double dInVal = inputsArrayHandle.inputValue().child( LHBlendRemap::aInVal ).asDouble();


//            if (cache == 0 or cachePlugs == 0)
//            {
//                dRemapOne = inputsArrayHandle.inputValue().child( LHBlendRemap::aRemapOne ).asDouble();
//
//                dRemapNegOne = inputsArrayHandle.inputValue().child( LHBlendRemap::aRemapNegOne ).asDouble();
//            }
            if (dInVal > 0)
            {
                double dPosVal = 0.0 ;
                double dRemapOne = inputsArrayHandle.inputValue().child( LHBlendRemap::aRemapOne ).asDouble();
                dPosVal = dInVal*dRemapOne;
                MDataHandle posData = outputsArrayHandle.outputValue().child( LHBlendRemap::aPosOut );
                posData.setDouble( dPosVal );
            }
            if (dInVal < 0)
            {
                double dNegVal = 0.0;
                double dRemapNegOne = inputsArrayHandle.inputValue().child( LHBlendRemap::aRemapNegOne ).asDouble();
                dNegVal = dInVal*dRemapNegOne;
                MDataHandle negData = outputsArrayHandle.outputValue().child( LHBlendRemap::aNegOut );
                negData.setDouble( dNegVal );
            }

            data.setClean( plug );
        }
//        cached = 1;
    }
    return MS::kSuccess;
}

MStatus LHBlendRemap::initialize() {
	MStatus status ;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;

    aCachePlugs = nAttr.create( "cachePlugs", "cplugs", MFnNumericData::kInt);
    nAttr.setDefault(0);
    nAttr.setMin(0);
    nAttr.setMax(1);
    nAttr.setKeyable(false);
    addAttribute(aCachePlugs);

    aInVal = nAttr.create( "inputValue", "inval", MFnNumericData::kDouble);
    nAttr.setDefault(0.0);
    nAttr.setKeyable(true);

    aRemapOne = nAttr.create( "remapOne", "rone", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setDefault(1.0);

    aRemapNegOne = nAttr.create( "remapNegOne", "rnone", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setDefault(-1.0);

    aPosOut = nAttr.create( "posOutput", "pout", MFnNumericData::kDouble);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);

    aNegOut = nAttr.create( "negOutput", "nout", MFnNumericData::kDouble);
    nAttr.setWritable(false);
    nAttr.setKeyable(false);


    aInputs = cAttr.create("Inputs", "inputs");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aInVal );
    cAttr.addChild( aRemapOne );
    cAttr.addChild( aRemapNegOne );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aInputs);

    aOutputs = cAttr.create("Outputs", "outputs");
    cAttr.setKeyable(false);
    cAttr.setArray(true);
    cAttr.addChild( aPosOut );
    cAttr.addChild( aNegOut );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aOutputs);

    // Effects

    attributeAffects( aInputs, aOutputs);

  return MS::kSuccess;
}


