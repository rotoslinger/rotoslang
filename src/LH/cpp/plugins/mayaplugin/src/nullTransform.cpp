#include "nullTransform.h"

MTypeId nullTMatrix::id(0x10886639);
nullTMatrix::nullTMatrix(){}
nullTMatrix::~nullTMatrix(){}
void* nullTMatrix::creator()  { return new nullTMatrix();}
MMatrix nullTMatrix::asMatrix() const { return MMatrix::identity; }
MMatrix nullTMatrix::asMatrix(double percent) const { return MMatrix::identity; }


MTypeId nullTransform::id(0x1084739);
MObject nullTransform::aSpeedTx;
MObject nullTransform::aSpeedTy;
MObject nullTransform::aSpeedTz;
MObject nullTransform::aSpeedT;

MObject nullTransform::aSpeedOutTx;
MObject nullTransform::aSpeedOutTy;
MObject nullTransform::aSpeedOutTz;
MObject nullTransform::aSpeedOutT;

nullTransform::nullTransform(){}
nullTransform::~nullTransform(){}
void* nullTransform::creator()  { return new nullTransform();}

MStatus nullTransform::initialize() {
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;


    aSpeedTx = nAttr.create( "speedTx", "speedtx", MFnNumericData::kDouble, 1.0 );
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setConnectable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    addAttribute( aSpeedTx );

    aSpeedTy = nAttr.create( "speedTy", "speedty", MFnNumericData::kDouble, 1.0 );
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setConnectable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    addAttribute( aSpeedTy );

    aSpeedTz = nAttr.create( "speedTz", "speedtz", MFnNumericData::kDouble, 1.0 );
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setConnectable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    addAttribute( aSpeedTz );


    aSpeedOutTx = nAttr.create( "txOut", "speedtxout", MFnNumericData::kDouble, 0.0 );
    nAttr.setKeyable(false);
    nAttr.setWritable(true);
    nAttr.setConnectable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(false);
    addAttribute( aSpeedOutTx );

    aSpeedOutTy = nAttr.create( "tyOut", "speedtyout", MFnNumericData::kDouble, 0.0 );
    nAttr.setKeyable(false);
    nAttr.setWritable(true);
    nAttr.setConnectable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(false);
    addAttribute( aSpeedOutTy );

    aSpeedOutTz = nAttr.create( "tzOut", "speedtzout", MFnNumericData::kDouble, 0.0 );
    nAttr.setKeyable(false);
    nAttr.setWritable(true);
    nAttr.setConnectable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(false);
    addAttribute( aSpeedOutTz );

    aSpeedT = cAttr.create("speedT", "speedt");
    cAttr.setKeyable(true);
    cAttr.setArray(false);
    cAttr.addChild( aSpeedTx );
    cAttr.addChild( aSpeedTy );
    cAttr.addChild( aSpeedTz );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aSpeedT);

    aSpeedOutT = cAttr.create("tOut", "tout");
    cAttr.setKeyable(true);
    cAttr.setArray(false);
    cAttr.addChild( aSpeedOutTx );
    cAttr.addChild( aSpeedOutTy );
    cAttr.addChild( aSpeedOutTz );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aSpeedOutT);

    attributeAffects(aSpeedTx, aSpeedOutTx);
    attributeAffects(aSpeedTy, aSpeedOutTy);
    attributeAffects(aSpeedTz, aSpeedOutTz);

    attributeAffects(translateX, aSpeedOutTx);
    attributeAffects(translateY, aSpeedOutTy);
    attributeAffects(translateZ, aSpeedOutTz);


    return MS::kSuccess;
}

MPxTransformationMatrix* nullTransform::createTransformationMatrix() { return new nullTMatrix(); }

MStatus nullTransform::compute( const MPlug& plug, MDataBlock& data )
{

    MStatus status;
    if ( plug == aSpeedOutT || plug == aSpeedOutTx || plug == aSpeedOutTy || plug == aSpeedOutTz)
    {
    	double drive_x = data.inputValue(translateX).asDouble();
    	double drive_y = data.inputValue(translateY).asDouble();
    	double drive_z = data.inputValue(translateZ).asDouble();

    	double tx = data.inputValue(aSpeedTx).asDouble();
      tx = tx * drive_x;
      MDataHandle out = data.outputValue(aSpeedOutTx);
      out.setDouble(tx);

    	double ty = data.inputValue(aSpeedTy).asDouble();
      ty = ty * drive_y;
      out = data.outputValue(aSpeedOutTy);
      out.setDouble(ty);

    	double tz = data.inputValue(aSpeedTz).asDouble();
      tz = tz * drive_z;
      out = data.outputValue(aSpeedOutTz);
      out.setDouble(tz);

	    data.setClean(plug);

    }
    return MS::kSuccess;

}
