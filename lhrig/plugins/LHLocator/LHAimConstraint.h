//#ifndef _LHAIMCONSTRAINT_H
//#define _LHAIMCONSTRAINT_H

#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPlug.h>
#include <maya/MGlobal.h>
#include <maya/MPxConstraint.h>
#include <maya/MEulerRotation.h>
#include <maya/MMatrix.h>

#include <math.h>


class LHAimConstraint : public MPxConstraint {
 public:
  LHAimConstraint() {};
  virtual MStatus compute( const MPlug& plug, MDataBlock& data );
  static void* creator();
  static MStatus initialize();

  static MTypeId id;

  static MObject aTargetRotPivTranslate;
  static MObject aTargetRotPiv;
  static MObject aTargetTranslate;
  static MObject aAimRotPivTranslate;
  static MObject aAimRotPiv;
  static MObject aAimTranslate;
  static MObject aUpRotPivTranslate;
  static MObject aUpRotPiv;
  static MObject aUpTranslate;
  static MObject aOffRx;
  static MObject aOffRy;
  static MObject aOffRz;
  static MObject aOffRotate;
  static MObject aRx;
  static MObject aRy;
  static MObject aRz;
  static MObject aOutRotate;


};

///////////////////////////////////////////////////////////

//#endif
