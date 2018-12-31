
//-
// ==========================================================================
// Copyright 1995,2006,2008 Autodesk, Inc. All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk
// license agreement provided at the time of installation or download,
// or which otherwise accompanies this software in either electronic
// or hard copy form.
// ==========================================================================
//+

//
//  File: splatDeformer.cc
//
//  Description:
//              Example implementation of a threaded deformer. This node
//              deforms one mesh using another.
//

#include <maya/MIOStream.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MItGeometry.h>
#include <maya/MFnPlugin.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MPoint.h>
#include <maya/MTimer.h>
#include <maya/MFnMesh.h>
#include <maya/MPointArray.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMeshData.h>
#include <maya/MMeshIntersector.h>
#include <maya/MGlobal.h>

#include <maya/MThreadUtils.h>

// Macros
//
#define MCheckStatus(status,message)    \
        if( MStatus::kSuccess != status ) {     \
                cerr << message << "\n";                \
                return status;                                  \
        }

class splatDeformer : public MPxDeformerNode
{
public:
                                                splatDeformer();
        virtual                         ~splatDeformer();

        static  void*           creator();
        static  MStatus         initialize();

        // deformation function
        //
        virtual MStatus compute(const MPlug& plug, MDataBlock& dataBlock);

public:
        // local node attributes

        static  MTypeId         id;

        static MObject deformingMesh;

private:
};
