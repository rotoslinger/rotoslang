#include "LHAimConstraint.h"

MTypeId LHAimConstraint::id(0x00002112);

MObject LHAimConstraint::aTargetRotPivTranslate;
MObject LHAimConstraint::aTargetRotPiv;
MObject LHAimConstraint::aTargetTranslate;
MObject LHAimConstraint::aAimRotPivTranslate;
MObject LHAimConstraint::aAimRotPiv;
MObject LHAimConstraint::aAimTranslate;
MObject LHAimConstraint::aUpRotPivTranslate;
MObject LHAimConstraint::aUpRotPiv;
MObject LHAimConstraint::aUpTranslate;

MObject LHAimConstraint::aOffRx;
MObject LHAimConstraint::aOffRy;
MObject LHAimConstraint::aOffRz;
MObject LHAimConstraint::aOffRotate;

MObject LHAimConstraint::aRx;
MObject LHAimConstraint::aRy;
MObject LHAimConstraint::aRz;
MObject LHAimConstraint::aOutRotate;


void* LHAimConstraint::creator() { return new LHAimConstraint; }

MStatus LHAimConstraint::compute( const MPlug& plug, MDataBlock& data )
{
    MStatus status;
    if ( plug == LHAimConstraint::aOutRotate )
    {
        //---get outputs
        MDataHandle hOutRotate(data.outputValue( aOutRotate ));
        //---get offsets
        MDataHandle hOffRotate(data.outputValue( aOffRotate ));
        double offRx = hOffRotate.child( aOffRx ).asDouble();
        double offRy = hOffRotate.child( aOffRy ).asDouble();
        double offRz = hOffRotate.child( aOffRz ).asDouble();

        //targets
        MVector targetPivTranslate = data.inputValue(aTargetRotPivTranslate).asFloatVector();
        MVector targetRotPiv = data.inputValue(aTargetRotPiv).asFloatVector();
        MVector targetTranslate = data.inputValue(aTargetTranslate).asFloatVector();

        //aims
        MVector aimPivTranslate = data.inputValue(aAimRotPivTranslate).asFloatVector();
        MVector aimRotPiv = data.inputValue(aAimRotPiv).asFloatVector();
        MVector aimTranslate = data.inputValue(aAimTranslate).asFloatVector();

        //ups
        MVector upPivTranslate = data.inputValue(aUpRotPivTranslate).asFloatVector();
        MVector upRotPiv = data.inputValue(aUpRotPiv).asFloatVector();
        MVector upTranslate = data.inputValue(aUpTranslate).asFloatVector();

        MVector targetVector(targetPivTranslate[0]+targetRotPiv[0]+targetTranslate[0],
                             targetPivTranslate[1]+targetRotPiv[1]+targetTranslate[1],
                             targetPivTranslate[2]+targetRotPiv[2]+targetTranslate[2]);
        MVector aimVector(aimPivTranslate[0]+aimRotPiv[0]+aimTranslate[0],
                          aimPivTranslate[1]+aimRotPiv[1]+aimTranslate[1],
                          aimPivTranslate[2]+aimRotPiv[2]+aimTranslate[2]);
        MVector upVector(upPivTranslate[0]+upRotPiv[0]+upTranslate[0],
                         upPivTranslate[1]+upRotPiv[1]+upTranslate[1],
                         upPivTranslate[2]+upRotPiv[2]+upTranslate[2]);

        MVector xVec = aimVector - targetVector;
        xVec.normalize();
        MVector yVec = targetVector - upVector;
        yVec.normalize();

        //---cross product
        MVector zVec = yVec ^ xVec;
        zVec.normalize();

        yVec = zVec ^ xVec;
        yVec.normalize();

        double mValues[4][4] = {{xVec[0], xVec[1], xVec[2], 0.0},
                                {yVec[0], yVec[1],yVec[2], 0.0},
                                {zVec[0], zVec[1],zVec[2], 0.0},
                                {0.0, 0.0, 0.0, 1.0}};
        MMatrix rotMatrix(mValues);

        MEulerRotation rotation;

        rotation = rotation.decompose(rotMatrix,MEulerRotation::kXYZ);

        // Convert offset values to radians
        offRx = (offRx * (3.14159265/180.0 ));
        offRy = (offRy * (3.14159265/180.0 ));
        offRz = (offRz * (3.14159265/180.0 ));

        //---set rotate outputs
        //---Rx
        MDataHandle rotateData = hOutRotate.child( aRx );
        rotateData.setDouble( rotation[0] - offRx );
        //---Ry
        rotateData = hOutRotate.child( aRy );
        rotateData.setDouble( rotation[1] - offRy);
        //---Rz
        rotateData = hOutRotate.child( aRz );
        rotateData.setDouble( rotation[2] - offRz);
        data.setClean( plug );

    }
    return MS::kSuccess;
}

MStatus LHAimConstraint::initialize() {
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;

    //---TARGET
    aTargetRotPivTranslate = nAttr.createPoint( "targetRotPivTranslate", "trpt");
    addAttribute(aTargetRotPivTranslate);

    aTargetRotPiv = nAttr.createPoint( "targetRotPivot", "trp");
    addAttribute(aTargetRotPiv);

    aTargetTranslate = nAttr.createPoint( "targetTranslate", "tt");
    addAttribute(aTargetTranslate);

    //---AIM
    aAimRotPivTranslate = nAttr.createPoint( "aimRotPivTranslate", "arpt");
    addAttribute(aAimRotPivTranslate);

    aAimRotPiv = nAttr.createPoint( "aimRotPivot", "arp");
    addAttribute(aAimRotPiv);

    aAimTranslate = nAttr.createPoint( "aimTranslate", "at");
    addAttribute(aAimTranslate);

    //---UP
    aUpRotPivTranslate = nAttr.createPoint( "upRotPivTranslate", "urpt");
    addAttribute(aUpRotPivTranslate);

    aUpRotPiv = nAttr.createPoint( "upRotPivot", "urp");
    addAttribute(aUpRotPiv);

    aUpTranslate = nAttr.createPoint( "upTranslate", "ut");
    addAttribute(aUpTranslate);


    aOffRx = nAttr.create( "offsetRx", "orx", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    aOffRy = nAttr.create( "offsetRy", "ory", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    aOffRz = nAttr.create( "offsetRz", "orz", MFnNumericData::kDouble);
    nAttr.setKeyable(true);

    aOffRotate = cAttr.create("Offset_Rotate", "offr");
    cAttr.setKeyable(true);
    cAttr.addChild( aOffRx );
    cAttr.addChild( aOffRy );
    cAttr.addChild( aOffRz );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aOffRotate);

    //---outputs
    aRx = nAttr.create( "rotateX", "rx", MFnNumericData::kDouble);
    nAttr.setKeyable(false);
    aRy = nAttr.create( "rotateY", "ry", MFnNumericData::kDouble);
    nAttr.setKeyable(false);
    aRz = nAttr.create( "rotateZ", "rz", MFnNumericData::kDouble);
    nAttr.setKeyable(false);


    aOutRotate = cAttr.create("outRotate", "r");
    cAttr.setKeyable(false);
    cAttr.addChild( aRx );
    cAttr.addChild( aRy );
    cAttr.addChild( aRz );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aOutRotate);

    attributeAffects( aTargetRotPivTranslate, aOutRotate);
    attributeAffects( aTargetRotPiv, aOutRotate);
    attributeAffects( aTargetTranslate, aOutRotate);
    attributeAffects( aAimRotPivTranslate, aOutRotate);
    attributeAffects( aAimRotPiv, aOutRotate);
    attributeAffects( aAimTranslate, aOutRotate);

    attributeAffects( aUpRotPivTranslate, aOutRotate);
    attributeAffects( aUpRotPiv, aOutRotate);
    attributeAffects( aUpTranslate, aOutRotate);
    attributeAffects( aOffRotate, aOutRotate);

  return MS::kSuccess;
}


