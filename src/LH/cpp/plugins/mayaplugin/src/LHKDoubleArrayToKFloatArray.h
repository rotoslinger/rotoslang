#pragma once
#include "formatErrorMacros.h"

#include <string.h>
#include <maya/MIOStream.h>
#include <math.h>

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnEnumAttribute.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MGlobal.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MPlugArray.h>
#include <maya/MString.h>
#include <maya/MObjectArray.h>

#include <math.h>


class LHKDoubleArrayToKFloatArray : public MPxNode {
 public:
  LHKDoubleArrayToKFloatArray() {};
  virtual MStatus compute( const MPlug& plug, MDataBlock& data );
  virtual MStatus setDependentsDirty(MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs);
  static void* creator();
  static MStatus initialize();

  static MTypeId id;

  static  MObject         aInWeights;
  static  MObject         aOutWeights;
  static  MObject         aOutWeightList;
  static  MObject         aBias;
  static  MObject         aBiasOut;



  //Output
//  static MObject aOutputWeights;

  inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[LHKDoubleArrayToKFloatArray] " );
        txt += msg ;
        txt += ", File: ";
        txt += sourceFile;
        txt += " Line: ";
        txt += sourceLine;
        return txt;
    }
};

///////////////////////////////////////////////////////////





