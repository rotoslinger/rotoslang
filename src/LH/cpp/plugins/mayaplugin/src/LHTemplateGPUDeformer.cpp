#include "LHTemplateGPUDeformer.h"

MTypeId identityNode::id( 0x8000d );
MObject identityNode::aAmount;


void* identityNode::creator()
{
    return new identityNode();
}

MStatus identityNode::initialize()
{
    MFnNumericAttribute nAttr;

    aAmount = nAttr.create("amount", "amnt", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    addAttribute(aAmount);
    attributeAffects(aAmount, outputGeom);

    return MStatus::kSuccess;
}


MStatus
identityNode::deform( MDataBlock& data,
                      MItGeometry& itGeo,
                      const MMatrix& /*m*/,
                      unsigned int multiIndex)
{
    MStatus returnStatus;
    float env = data.inputValue(identityNode::envelope).asFloat();
    if (!env)
        return MStatus::kSuccess;


    float amount = data.inputValue(identityNode::aAmount).asFloat();
    MVector direction(1.0, 0.0, 0.0);

    for ( ; !itGeo.isDone(); itGeo.next()) {
        MPoint pt = itGeo.position();
        itGeo.setPosition(itGeo.position() + (direction * amount));
    }
    return returnStatus;
}


MGPUDeformerRegistrationInfo* identityGPUDeformer::getGPUDeformerInfo()
{
    static identityGPUDeformerInfo theOne;
	return &theOne;
}

identityGPUDeformer::identityGPUDeformer()
{
}

identityGPUDeformer::~identityGPUDeformer()
{
    terminate();
}

bool identityGPUDeformer::validateNode(MDataBlock& block, const MEvaluationNode& evaluationNode, const MPlug& plug, MStringArray* messages)
{
    // Support everything.
    return true;
}

MPxGPUDeformer::DeformerStatus identityGPUDeformer::evaluate(
    MDataBlock& block,
    const MEvaluationNode& evaluationNode,
    const MPlug& plug,
    unsigned int numElements,
    const MAutoCLMem inputBuffer,
    const MAutoCLEvent inputEvent,
    MAutoCLMem outputBuffer,
    MAutoCLEvent& outputEvent
    )
{
    cl_int err = CL_SUCCESS;    
    
    // Setup OpenCL kernel.
    if ( !fKernel.get() )
    {
        // Get and compile the kernel.
        const char* mayaLocation = getenv( "MAYA_LOCATION" );

        MString openCLKernelFile( mayaLocation );
        openCLKernelFile +="/LHTemplateGPUDeformer.cl";

        MString openCLKernelName("identity");

        MAutoCLKernel kernel = MOpenCLInfo::getOpenCLKernel( openCLKernelFile, openCLKernelName );
        if ( kernel.isNull() )
        {
            return MPxGPUDeformer::kDeformerFailure;
        }

        fKernel = kernel;
        
        // Figure out a good work group size for our kernel.
        fLocalWorkSize = 0;
        fGlobalWorkSize = 0;
        size_t retSize = 0;
        err = clGetKernelWorkGroupInfo(
            fKernel.get(),
            MOpenCLInfo::getOpenCLDeviceId(),
            CL_KERNEL_WORK_GROUP_SIZE,
            sizeof(size_t),
            &fLocalWorkSize,
            &retSize
            );
        MOpenCLInfo::checkCLErrorStatus(err);
        if ( err != CL_SUCCESS || retSize == 0 || fLocalWorkSize == 0)
        {
            return MPxGPUDeformer::kDeformerFailure;
        }

        // Global work size must be a multiple of local work size.
        const size_t remain = numElements % fLocalWorkSize;
        if ( remain )
        {
            fGlobalWorkSize = numElements + ( fLocalWorkSize - remain );
        }
        else
        {
            fGlobalWorkSize = numElements;
        }
    }

    // Set all of our kernel parameters.  Input buffer and output buffer may be changing every frame
    // so always set them.
    unsigned int parameterId = 0;
    err = clSetKernelArg(fKernel.get(), parameterId++, sizeof(cl_mem), (void*)outputBuffer.getReadOnlyRef());
    MOpenCLInfo::checkCLErrorStatus(err);
    err = clSetKernelArg(fKernel.get(), parameterId++, sizeof(cl_mem), (void*)inputBuffer.getReadOnlyRef());
    MOpenCLInfo::checkCLErrorStatus(err);
    err = clSetKernelArg(fKernel.get(), parameterId++, sizeof(cl_uint), (void*)&numElements);
    MOpenCLInfo::checkCLErrorStatus(err);

    // Set up our input events.  The input event could be NULL, in that case we need to pass
    // slightly different parameters into clEnqueueNDRangeKernel.
    cl_event events[ 1 ] = { 0 };
    cl_uint eventCount = 0;
    if ( inputEvent.get() )
    {
        events[ eventCount++ ] = inputEvent.get();
    }

    // Run the kernel

    err = clEnqueueNDRangeKernel(
        MOpenCLInfo::getMayaDefaultOpenCLCommandQueue(), fKernel.get(), 1, NULL, &fGlobalWorkSize,
        &fLocalWorkSize, eventCount, events, outputEvent.getReferenceForAssignment());
    MOpenCLInfo::checkCLErrorStatus(err);
    if ( err != CL_SUCCESS )
    {
        return MPxGPUDeformer::kDeformerFailure;
    }

    return MPxGPUDeformer::kDeformerSuccess;
}

void identityGPUDeformer::terminate()
{
    MOpenCLInfo::releaseOpenCLKernel(fKernel);
    fKernel.reset();
}

