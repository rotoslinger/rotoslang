// This is a template for the MPxNode
//====================================

#include "LHComputeDeformer.h"

MTypeId LHComputeDeformer::id(0x10067539);

//doubles
MObject LHComputeDeformer::aBiasIn;
MObject LHComputeDeformer::aBiasOut;


MStatus LHComputeDeformer::initialize() {
	MStatus status ;
    MFnNumericAttribute nAttr;


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
  return MS::kSuccess;
}


void* LHComputeDeformer::creator() { return new LHComputeDeformer; }

MStatus LHComputeDeformer::compute( const MPlug& plug, MDataBlock& data )
{

    MStatus status;
    if ( plug == aBiasOut)
    {

    	MDataHandle hBiasIn = data.inputValue(aBiasIn, &status);
        float inVal = hBiasIn.asFloat();
        MDataHandle hBiasOut = data.outputValue(aBiasOut);
        hBiasOut.setFloat(inVal);

		MGlobal::displayInfo(MString("DEBUG:  UPDATING output value is ") + inVal);
	    data.setClean(plug);
    } else
            return MS::kUnknownParameter;

    return MS::kSuccess;
}







//MStatus MyLocator::initialize()
//{
//MRampAttribute rAttr;
//MFnEnumAttribute eAttr;
//MFnUnitAttribute uAttr;
//MFnTypedAttribute tAttr;
//MFnNumericAttribute nAttr;
//MFnMessageAttribute gAttr;
// 
//timeObj = uAttr.create( "time", "time", MFnUnitAttribute::kTime, 0.0 );
//addAttribute( timeObj );
// 
//angleObj = uAttr.create( "angle", "angle", MFnUnitAttribute::kAngle, 0.0 );
//addAttribute( angleObj );
// 
//boolObj = nAttr.create( "bool", "bool", MFnNumericData::kBoolean, false );
//addAttribute( boolObj );
// 
//intObj = nAttr.create( "int", "int", MFnNumericData::kInt, 0 );
//addAttribute( intObj );
// 
//floatObj = nAttr.create( "float", "float", MFnNumericData::kFloat, 0.f );
//addAttribute( floatObj );
// 
//doubleObj = nAttr.create( "double", "double", MFnNumericData::kDouble, 0.0 );
//addAttribute( doubleObj );
// 
//int2Obj = nAttr.create( "int2", "int2", MFnNumericData::k2Int, 0 );
//addAttribute( int2Obj );
// 
//int3Obj = nAttr.create( "int3", "int3", MFnNumericData::k3Int, 0 );
//addAttribute( int3Obj );
// 
//float2Obj = nAttr.create( "float2", "float2", MFnNumericData::k2Float, 0.f );
//addAttribute( float2Obj );
// 
//float3Obj = nAttr.create( "float3", "float3", MFnNumericData::k3Float, 0.f );
//addAttribute( float3Obj );
// 
//double2Obj = nAttr.create( "double2", "double2", MFnNumericData::k2Double, 0.0 );
//addAttribute( double2Obj );
// 
//double3Obj = nAttr.create( "double3", "double3", MFnNumericData::k3Double, 0.0 );
//addAttribute( double3Obj );
// 
//stringObj = tAttr.create( "string", "string", MFnData::kString, "abc" );
//addAttribute( stringObj );
// 
//matrixObj = tAttr.create( "matrix", "matrix", MFnMatrixAttribute::kDouble );
//addAttribute( matrixObj );
// 
//curveObj = tAttr.create( "curve", "curve", MFnData::kNurbsCurve );
//addAttribute( curveObj );
// 
//meshObj = tAttr.create( "mesh", "mesh", MFnData::kMesh );
//addAttribute( meshObj );
// 
//iaObj = tAttr.create( "iArray", "iArray", MFnData::kIntArray );
//addAttribute( iaObj );
// 
//faObj = tAttr.create( "fArray", "fArray", MFnData::kFloatArray );
//addAttribute( faObj );
// 
//daObj = tAttr.create( "dArray", "dArray", MFnData::kDoubleArray );
//addAttribute( daObj );
// 
//paObj = tAttr.create( "pArray", "pArray", MFnData::kPointArray );
//addAttribute( paObj );
// 
//vaObj = tAttr.create( "vArray", "vArray", MFnData::kVectorArray );
//addAttribute( vaObj );
// 
//saObj = tAttr.create( "sArray", "sArray", MFnData::kStringArray );
//addAttribute( saObj );
// 
//msgObj = gAttr.create( "message", "message" );
//addAttribute( msgObj );
// 
//clrObj = nAttr.createColor( "color", "color" );
//addAttribute( clrObj );
// 
//pntObj = nAttr.createPoint( "point", "point" );
//addAttribute( pntObj );
// 
//enumObj = eAttr.create( "enum", "enum" 0 );
//eAttr.addField( "A", 0 );
//eAttr.addField( "B", 0 );
//addAttribute( enumObj );
// 
//crvRmpObj = rAttr.createCurveRampAttr( "crvRamp", "crvRamp" );
//addAttribute( crvRmpObj );
// 
//clrRmpObj = rAttr.createColorRampAttr( "clrRamp", "clrRamp" );
//addAttribute( clrRmpObj );
// 
//fileNameObj = tAttr.create( "fileName", "fileName", MFnData::kString );
//tAttr.setUsedAsFilename( true );
//addAttribute( fileNameObj );
// 
//}
