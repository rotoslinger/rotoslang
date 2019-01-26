
// ==========================================================================
// Copyright 2015 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk
// license agreement provided at the time of installation or download,
// or which otherwise accompanies this software in either electronic
// or hard copy form.
// ==========================================================================
//+
//
//  File: sseDeformer.cc
//
//  Description:
//      Example implementation of a deformer. This node
//      offsets vertices according to the CV's weights.
//      The weights are set using the set editor or the
//      percent command.
//
#include <string.h>
#include <float.h> // for FLT_MAX
#include <maya/MIOStream.h>
#include <math.h>
#include <maya/MPxGeometryFilter.h>
#include <maya/MItGeometry.h>
#include <maya/MPxLocatorNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFnPlugin.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MTimer.h>
#include <maya/MDagModifier.h>
#include <maya/MFnMesh.h>
#include <maya/MFloatPointArray.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMeshData.h>
#include <maya/MFloatVectorArray.h>
// Macros
//
#define MCheckStatus(status,message)    \
    if( MStatus::kSuccess != status ) { \
        cerr << message << "\n";        \
        return status;                  \
    }
//======================================================================
class sseDeformer : public MPxGeometryFilter
{
public:
                        sseDeformer();
    virtual             ~sseDeformer();
    static  void*       creator();
    static  MStatus     initialize();
    // deformation function
    //
    virtual MStatus compute(const MPlug& plug, MDataBlock& dataBlock);
public:
    // local node attributes
    static  MObject sseEnabled; // Boolean indicating whether the SSE path is to be used
    static  MTypeId     id;     // Plug-in ID
private:
    // Helper method to make it easier to handle both the case of evaluating
    // one child (as in DG evaluation) and the case of evaluating all children
    // (as in EM evaluation).
    MStatus computeOneOutput(unsigned int index, MDataBlock& data, MDataHandle& hInput);
};

