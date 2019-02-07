//-
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
//  File: identityNode.cpp
//
//  Description:
//      Empty implementation of a deformer. This node
//      performs no deformation and is basically an empty
//      shell that can be used to create actual deformers.
//
//
//      Use this script to create a simple example with the identity node.
//      
//      loadPlugin identityNode;
//      
//      polyTorus -r 1 -sr 0.5 -tw 0 -sx 50 -sy 50 -ax 0 1 0 -cuv 1 -ch 1;
//      deformer -type "identity";
//      setKeyframe -v 0 -at weightList[0].weights[0] -t 1 identity1;
//      setKeyframe -v 1 -at weightList[0].weights[0] -t 60 identity1;
//      select -cl;

// #include <maya/MFnPlugin.h>
#pragma once

#include <maya/MTypeId.h> 

#include <maya/MStringArray.h>

#include <maya/MPxDeformerNode.h> 
#include <maya/MItGeometry.h>
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MFnNumericAttribute.h>

#include <maya/MPxGPUDeformer.h>
#include <maya/MGPUDeformerRegistry.h>
#include <maya/MOpenCLInfo.h>
#include <clew/clew_cl.h>



class identityNode : public MPxDeformerNode
{
public:
    static  void*   creator();
    static  MStatus initialize();

    // Deformation function
    //
    virtual MStatus deform(MDataBlock&    block,
                           MItGeometry&   iter,
                           const MMatrix& mat,
                           unsigned int multiIndex);
    static MObject aAmount;

    static MTypeId id;
};




// The GPU override implementation of the identityNode
//
class identityGPUDeformer : public MPxGPUDeformer
{
public:
    static MGPUDeformerRegistrationInfo* getGPUDeformerInfo();
    static bool validateNode(MDataBlock& block, const MEvaluationNode&, const MPlug& plug, MStringArray* messages);

    // Virtual methods from MPxGPUDeformer
    identityGPUDeformer();
    virtual ~identityGPUDeformer();

    // Implementation of MPxGPUDeformer.
    virtual MPxGPUDeformer::DeformerStatus evaluate(MDataBlock&, const MEvaluationNode&, const MPlug& plug, unsigned int, const MAutoCLMem, const MAutoCLEvent, MAutoCLMem, MAutoCLEvent&);
    virtual void terminate();

private:
    // Kernel
    MAutoCLKernel fKernel;
    size_t fLocalWorkSize;
    size_t fGlobalWorkSize;
};

// registration information for the identity GPU deformer.
class identityGPUDeformerInfo : public MGPUDeformerRegistrationInfo
{
public:
	identityGPUDeformerInfo(){}
	virtual ~identityGPUDeformerInfo(){}

	virtual MPxGPUDeformer* createGPUDeformer()
	{
		return new identityGPUDeformer();
	}
	virtual bool validateNodeInGraph(MDataBlock& block, const MEvaluationNode& evaluationNode,
                                   const MPlug& plug, MStringArray* messages)	{
		return true;
	}

	virtual bool validateNodeValues(MDataBlock& block, const MEvaluationNode& evaluationNode,
                                  const MPlug& plug, MStringArray* messages) {
		return true;
	}
	virtual bool validateNode(MDataBlock& block, const MEvaluationNode& evaluationNode, const MPlug& plug, MStringArray* messages)
	{
		return identityGPUDeformer::validateNode(block, evaluationNode, plug, messages);
	}
};

// // standard initialization procedures
// //

// MStatus initializePlugin( MObject obj )
// {
//     MStatus result;

//     MFnPlugin plugin( obj, PLUGIN_COMPANY, "3.0", "Any");
//     result = plugin.registerNode(
//         "identity" ,
//         identityNode::id ,
//         &identityNode::creator ,
//         &identityNode::initialize ,
//         MPxNode::kDeformerNode
//         );

//     MString nodeClassName("identity");
//     MString registrantId("mayaPluginExample");
//     MGPUDeformerRegistry::registerGPUDeformerCreator(
//         nodeClassName,
//         registrantId,
//         identityGPUDeformer::getGPUDeformerInfo()
//         );

//     return result;
// }

// MStatus uninitializePlugin( MObject obj )
// {
//     MStatus result;

//     MString nodeClassName("identity");
//     MString registrantId("mayaPluginExample");
//     MGPUDeformerRegistry::deregisterGPUDeformerCreator(
//         nodeClassName,
//         registrantId
//         );

//     MFnPlugin plugin( obj );
//     result = plugin.deregisterNode( identityNode::id );

//     return result;
// }