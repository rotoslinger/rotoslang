#pragma once
#include "formatErrorMacros.h"
#include "matrixCommon.h"
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPlug.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnMesh.h>
#include <maya/MFloatMatrix.h>
#include <maya/MTransformationMatrix.h>

#include <math.h>

class LHGeometryConstraint : public MPxNode {
 public:
    LHGeometryConstraint() {};
    virtual MStatus compute( const MPlug& plug, MDataBlock& data );
    static void* creator();
    static MStatus initialize();
    virtual SchedulingType schedulingType()const{return kParallel;}

    static MTypeId id;

    static MObject aMesh;
    static MObject aOutputMatrix;
    static MObject aParentMatrix;
    static MObject aAPointIdx;
    static MObject aBPointIdx;
    static MObject aCPointIdx;
    static MObject aDPointIdx;
    static MObject aBaryWeight;

    inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[LHGeometryConstraint] " );
        txt += msg ;
        txt += ", File: ";
        txt += sourceFile;
        txt += " Line: ";
        txt += sourceLine;
        return txt;
    }
};

///////////////////////////////////////////////////////////
