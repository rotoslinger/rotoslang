#include "LHGetDeformPoints.h"

MTypeId LHGetDeformPoints::id(0x03147019);

MObject LHGetDeformPoints::aInputGeo;
MObject LHGetDeformPoints::aInputGeoArray;

MObject LHGetDeformPoints::aOutPoints;
MObject LHGetDeformPoints::aOutPointArray;

MObject LHGetDeformPoints::aBiasIn;
MObject LHGetDeformPoints::aBiasOut;


MStatus LHGetDeformPoints::initialize() {
	MStatus status ;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnTypedAttribute tAttr;
    MFnGenericAttribute gAttr;

    aBiasIn = nAttr.create( "biasIn", "binput", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(1.0);
    nAttr.setChannelBox(true);
    addAttribute( aBiasIn );


	aBiasOut = nAttr.create( "biasOut", "boutput", MFnNumericData::kFloat);
	/////////////////// KEYABLE MUST BE FALSE for attributeAffects to work on an output
    nAttr.setKeyable(false);
	/////////////////// KEYABLE MUST BE FALSE for attributeAffects to work on an output
    nAttr.setWritable(true);
    nAttr.setStorable(true);
	nAttr.setDefault(1.0);
	nAttr.setChannelBox(true);
	addAttribute( aBiasOut );


	attributeAffects( aBiasIn, aBiasOut);

    aInputGeo = gAttr.create("inputGeo", "ingeo");
    gAttr.addAccept(MFnData::kMesh);
    gAttr.addAccept(MFnData::kNurbsSurface);
    gAttr.addAccept(MFnData::kNurbsCurve);
    addAttribute(aInputGeo);

    aInputGeoArray = cAttr.create("inputGeoArray", "ingeoarray");
    cAttr.setKeyable(false);
    cAttr.setArray(true);
    cAttr.addChild( aInputGeo );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aInputGeoArray);


    aOutPoints = tAttr.create( "outPoints", "opoints", MFnPointArrayData::kPointArray );
    tAttr.setKeyable(false);
//    tAttr.setArray(false);
//    tAttr.setUsesArrayDataBuilder(true);
    addAttribute( aOutPoints );

    aOutPointArray = cAttr.create("outPointArray", "oparray");
    cAttr.addChild( aOutPoints );
    cAttr.setHidden(false);
    cAttr.setArray(true);
    cAttr.setChannelBox(true);
    cAttr.setConnectable(true);
    cAttr.setKeyable(false);
    cAttr.setReadable(true);
    cAttr.setInternal(true);
    cAttr.setIndexMatters(true);
    cAttr.setStorable(true);

    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutPointArray);

	attributeAffects( aInputGeo, aOutPoints);
	attributeAffects( aInputGeoArray, aOutPoints);
	attributeAffects( aInputGeoArray, aOutPointArray);


  return MS::kSuccess;
}

void* LHGetDeformPoints::creator() { return new LHGetDeformPoints; }

MStatus LHGetDeformPoints::compute( const MPlug& plug, MDataBlock& data )
{
    MStatus status;
    if ( plug == LHGetDeformPoints::aOutPointArray or plug == aBiasOut)
    {

    	MArrayDataHandle geomArrayHandle = data.inputArrayValue(LHGetDeformPoints::aInputGeoArray, &status);
        CheckStatusReturn( status, "Unable to get base geo" );

        MArrayDataHandle outputsArrayHandle(data.outputArrayValue( LHGetDeformPoints::aOutPointArray, &status));
        CheckStatusReturn( status, "Unable to get outputs" );

        unsigned int outputElemCount = outputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get outputPoints make sure element has been created" );

        if (outputElemCount > geomArrayHandle.elementCount())
        {
            MGlobal::displayInfo(MString("There are more output elements than geometry elements,"
            		" you may want to delete unneeded output elements"));
            outputElemCount = geomArrayHandle.elementCount();
        }

        int i = 0;
        for (i=0;i < outputElemCount;i++)
        {
            status = geomArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to geometry element" );

            status = outputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to output element" );

            MDataHandle dhInput = geomArrayHandle.inputValue(&status);
            CheckStatusReturn( status, "Unable to get geometry array input value" );

            MDataHandle dhInputGeo = dhInput.child( aInputGeo );
            MItGeometry iter(dhInputGeo, true, &status);
            CheckStatusReturn( status, "Unable to get geometry iterator.  It is likely geo has not been connected to this plug." );

            MPointArray positions;
            iter.allPositions(positions, MSpace::kWorld);

			MGlobal::displayInfo(MString("Updating"));

			MFnPointArrayData outputPointArrayFn;
			MObject oOutputArray = outputPointArrayFn.create(positions, &status);
            CheckStatusReturn( status, "Unable to create the output array" );
            //return MS::kSuccess;
    		MGlobal::displayInfo(MString("DEBUG:  Number of points ") + positions.length());
			MDataHandle handle = outputsArrayHandle.outputValue(&status);
			CheckStatusReturn( status, "Unable to get the output array value" );
			MDataHandle childHandle = handle.child(LHGetDeformPoints::aOutPoints);
			childHandle.setMObject(oOutputArray);
            data.setClean( plug );

	        if (oOutputArray.isNull())
	        {
	            MGlobal::displayInfo(MString("The output is NULL"));
	            return MS::kSuccess;
	        }

        }
    	MDataHandle hBiasIn = data.inputValue(aBiasIn, &status);
        float inVal = hBiasIn.asFloat();
        MDataHandle hBiasOut = data.outputValue(aBiasOut);
        hBiasOut.setFloat(inVal);

		MGlobal::displayInfo(MString("DEBUG:  UPDATING output value is ") + inVal);
	    data.setClean(plug);
    }
    return MS::kSuccess;
}


MStatus LHGetDeformPoints::setDependentsDirty( MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs)
    {
        if ( inPlug.attribute() != aInputGeo
        and inPlug.attribute() != aInputGeoArray)
        {
            return MS::kSuccess;
        }

        MPlug outArrayPlug(thisMObject(), aOutPointArray);

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



