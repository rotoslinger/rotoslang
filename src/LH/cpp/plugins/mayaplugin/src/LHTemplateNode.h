#pragma once

#include "formatErrorMacros.h"
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPlug.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MNurbsIntersector.h>
#include <maya/MFnGenericAttribute.h>

#include <math.h>


class LHTemplateNode : public MPxNode {
 public:
  LHTemplateNode() {};
  virtual MStatus compute( const MPlug& plug, MDataBlock& data );
  static void* creator();
  static MStatus initialize();

  static MTypeId id;

  static MObject aBiasIn;
  static MObject aBiasOut;

    inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[LHTemplateNode] " );
        txt += msg ;
        txt += ", File: ";
        txt += sourceFile;
        txt += " Line: ";
        txt += sourceLine;
        return txt;
    }
};

///////////////////////////////////////////////////////////
