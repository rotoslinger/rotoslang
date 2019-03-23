#pragma once

#include "formatErrorMacros.h"
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MDoubleArray.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MPxDeformerNode.h>

class LHVectorDeformerSimple : public MPxDeformerNode {
    public:
    LHVectorDeformerSimple() {};
    virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                            const MMatrix &localToWorldMatrix, unsigned int mIndex);
    static void* creator();
    static MStatus initialize();

    static MTypeId id;
    static MObject aAmount;
    static MObject aVectorCurve;
    //   static MObject aNormalize;
    static MObject aVectorWeights;
    static MObject aMembershipWeights;
    MPoint fromPoint, toPoint, pt;
    int idx;
    double w;

  inline MString FormatError( const MString &msg, const MString
                                &sourceFile, const int &sourceLine )
  {
      MString txt( "[LHVectorDeformerSimple] " );
      txt += msg ;
      txt += ", File: ";
      txt += sourceFile;
      txt += " Line: ";
      txt += sourceLine;
      return txt;
  }
};
