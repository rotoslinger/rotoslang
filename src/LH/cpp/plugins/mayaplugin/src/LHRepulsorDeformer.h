#pragma once

#include "formatErrorMacros.h"

#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>

#include <maya/MFnMesh.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrixArray.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MFnGenericAttribute.h>

#include <maya/MPxDeformerNode.h>

class LHRepulsorDeformer : public MPxDeformerNode {
 public:
  LHRepulsorDeformer() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  static void* creator();
  //virtual void draw(M3dView &view, const MDagPath &path,M3dView::DisplayStyle style, M3dView::DisplayStatus status);
  static MStatus initialize();

  static MTypeId id;
  static MObject aInputs;
  static MObject aRepulsorMatrix;
  static MObject aRepulsorRadius;
  static MObject aAmount;

    inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[LHRepulsorDeformer] " );
        txt += msg ;
        txt += ", File: ";
        txt += sourceFile;
        txt += " Line: ";
        txt += sourceLine;
        return txt;
    }



};
