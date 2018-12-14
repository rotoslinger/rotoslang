#include "LHSurfaceOutputManip.h"

MTypeId LHSurfaceOutputManip::id(0x00006219);

//Floats
//MObject LHSurfaceOutputManip::aDistance;
//MObject LHSurfaceOutputManip::aRadius;
//MObject LHSurfaceOutputManip::aRotAmount;
//MObject LHSurfaceOutputManip::aGlobalScale;
//MObject LHSurfaceOutputManip::aRotation;
//CompoundAttributes
MObject LHSurfaceOutputManip::aInputs;
MObject LHSurfaceOutputManip::aOutputs;

//Inputs
MObject LHSurfaceOutputManip::aBaseTransform;
MObject LHSurfaceOutputManip::aTransform;
MObject LHSurfaceOutputManip::aTransformArray;
MObject LHSurfaceOutputManip::aSurface;

//Outputs
MObject LHSurfaceOutputManip::aOutParamArray;
MObject LHSurfaceOutputManip::aOutParamU;
MObject LHSurfaceOutputManip::aOutParamV;


void* LHSurfaceOutputManip::creator() { return new LHSurfaceOutputManip; }

MStatus LHSurfaceOutputManip::compute( const MPlug& plug, MDataBlock& data )
{
    MStatus status;
    MGlobal::displayInfo("Start");

    if ( plug == LHSurfaceOutputManip::aBaseTransform)
//	if ( plug == LHSurfaceOutputManip::aBaseTransform or plug == LHSurfaceOutputManip::aTransform)
    {
		MGlobal::displayInfo("Working");
		MMatrix transform = data.inputValue( LHSurfaceOutputManip::aTransform, &status ).asMatrix();
        MDataHandle baseData = data.inputValue( LHSurfaceOutputManip::aBaseTransform, &status );
        baseData.setMMatrix(transform);
        data.setClean( plug );
        //			paramUData.setDouble( tmp );
        //	//            paramVData.setFloat( vVal );
        //			MGlobal::displayInfo(MString()+uVal+" UVALUE");
        //
        //			MGlobal::displayInfo(MString()+uVal+" UVALUE");
        //			MGlobal::displayInfo(MString()+closest.x +" VVALUE");
        //
        //			data.setClean( plug );

//		MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHSurfaceOutputManip::aInputs, &status));
//		CheckStatusReturn( status, "Unable to get inputs" );
//		MGlobal::displayInfo("Got Outputs");
//
//		MArrayDataHandle outputsArrayHandle(data.outputArrayValue( LHSurfaceOutputManip::aOutputs, &status));
//		CheckStatusReturn( status, "Unable to get outputs" );
//		MGlobal::displayInfo("Got Inputs");
//
//		unsigned int outputCount = outputsArrayHandle.elementCount(&status);
//		CheckStatusReturn( status, "Unable to get number of outputs" );
//		MGlobal::displayInfo("Got Outputs");
//
//		int i = 0;
//		for (i=0;i < outputCount;i++)
//		{
//			status = inputsArrayHandle.jumpToElement(i);
//			CheckStatusReturn( status, "Unable to jump to input element" );
//
//			status = outputsArrayHandle.jumpToElement(i);
//			CheckStatusReturn( status, "Unable to jump to element" );
//
//
//			MMatrix transform = inputsArrayHandle.inputValue().child( LHSurfaceOutputManip::aTransform ).asMatrix();
//			MTransformationMatrix transMatrix(transform);
//			MMatrix baseTransform = inputsArrayHandle.inputValue().child( LHSurfaceOutputManip::aBaseTransform ).asMatrix();
//			MTransformationMatrix baseTransMatrix(transform);
//
//			MVector pt = transMatrix.getTranslation(MSpace::kWorld);
//			MPoint tPoint(pt.x, pt.y, pt.z);
//
//			pt = baseTransMatrix.getTranslation(MSpace::kWorld);
//			MPoint bPoint(pt.x, pt.y, pt.z);
//			MGlobal::displayInfo(MString()+tPoint.x +" transMatrix");
//
//			MObject oSurface = data.inputValue(aSurface).asNurbsSurfaceTransformed();
//			if (oSurface.isNull())
//				{
//					return MS::kSuccess;
//				}
//
//			MFnNurbsSurface fnSurface( oSurface );
//			MNurbsIntersector fnIntersector;
//			fnIntersector.create(oSurface);
//			MPointOnNurbs ptON;
//			fnIntersector.getClosestPoint(tPoint, ptON);
//			MPoint closest = ptON.getPoint();
//			MPoint UV = ptON.getUV();
//			fnIntersector.getClosestPoint(bPoint, ptON);
//			MPoint UVB = ptON.getUV();
//
//			double uVal = UV.x - UVB.x;
//			double vVal = UV.y - UVB.y;
//
//			MDataHandle paramUData = outputsArrayHandle.outputValue().child( LHSurfaceOutputManip::aOutParamU );
//	//            MDataHandle paramVData = outputsArrayHandle.outputValue().child( LHSurfaceOutputManip::aOutParamV );
//			double tmp = 10.0;
//			paramUData.setDouble( tmp );
//	//            paramVData.setFloat( vVal );
//			MGlobal::displayInfo(MString()+uVal+" UVALUE");
//
//			MGlobal::displayInfo(MString()+uVal+" UVALUE");
//			MGlobal::displayInfo(MString()+closest.x +" VVALUE");
//
//			data.setClean( plug );
//			MGlobal::displayInfo("END");
//
//			}
    }
    return MS::kSuccess;
}

MStatus LHSurfaceOutputManip::initialize() {
	MStatus status ;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnTypedAttribute tAttr;

    //---Inputs

//    aSurface = tAttr.create("surface", "s", MFnData::kNurbsSurface);
//    addAttribute( aSurface );
//
//
    aBaseTransform = tAttr.create("baseMatrix", "bm", MFnData::kMatrix);
    addAttribute( aBaseTransform );

    aTransform = tAttr.create("matrix", "m", MFnData::kMatrix);
    addAttribute( aTransform );

	attributeAffects(aTransform, aBaseTransform);


//    aInputs = cAttr.create("Inputs", "inputs");
//    cAttr.setKeyable(false);
//    cAttr.setArray(true);
//    cAttr.addChild( aBaseTransform );
//    cAttr.addChild( aTransform );
//    cAttr.setReadable(true);
//    cAttr.setWritable(true);
//    cAttr.setConnectable(true);
//    cAttr.setChannelBox(true);
//    addAttribute(aInputs);



    //---Outputs

//    aOutParamU = nAttr.create("outParamU", "opu", MFnNumericData::kDouble);
//    addAttribute( aOutParamU );
	//nAttr.setWritable(false);
	//nAttr.setKeyable(false);

//    attributeAffects(aOutParamU, aOutParamArray);

//    aOutParamV = nAttr.create("outParamV", "opv", MFnNumericData::kDouble);
//    addAttribute( aOutParamV );
//	nAttr.setWritable(false);
//	nAttr.setKeyable(false);

//    attributeAffects(aOutParamV, aOutParamArray);


//	aOutputs = cAttr.create("Outputs", "outputpars");
//    cAttr.setKeyable(false);
//    cAttr.setArray(true);
//    cAttr.addChild( aOutParamU );
////    cAttr.addChild( aOutParamV );
//    cAttr.setReadable(true);
//    cAttr.setWritable(true);
//    cAttr.setConnectable(true);
//    cAttr.setChannelBox(true);
//    addAttribute(aOutputs);
//
//    attributeAffects(aSurface, aOutputs);
//    attributeAffects(aInputs, aOutputs);
//    attributeAffects(aBaseTransform, aOutputs);
//    attributeAffects(aTransform, aOutputs);



  return MS::kSuccess;
}


