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
    return MStatus::kSuccess;

    MStatus returnStatus;
    float env = data.inputValue(identityNode::envelope).asFloat();
    if (!env)
        return MStatus::kSuccess;


    float amount = data.inputValue(identityNode::aAmount).asFloat();
    MVector direction(1.0, 0.0, 0.0);

    for ( ; !itGeo.isDone(); itGeo.next()) {
        // MPoint pt = itGeo.position();
        itGeo.setPosition(itGeo.position() + (direction * amount));
        // itGeo.setPosition(pt);
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
MString identityGPUDeformer::pluginLoadPath;
MPxGPUDeformer::DeformerStatus identityGPUDeformer::evaluate(
    MDataBlock& data,
    const MEvaluationNode& evaluationNode,
    const MPlug& plug,
    const MGPUDeformerData& inputData,
    MGPUDeformerData& outputData
    // unsigned int numElements,
    // const MAutoCLMem inputBuffer,
    // const MAutoCLEvent inputEvent,
    // MAutoCLMem outputBuffer,
    // MAutoCLEvent& outputEvent
    )
{

    MGPUDeformerBuffer inputDeformerBuffer = inputData.getBuffer(sPositionsName());
    const MAutoCLMem inputBuffer = inputDeformerBuffer.buffer();
    unsigned int numElements = inputDeformerBuffer.elementCount();
    const MAutoCLEvent inputEvent = inputDeformerBuffer.bufferReadyEvent();

    // create the output buffer
	MGPUDeformerBuffer outputDeformerBuffer = createOutputBuffer(inputDeformerBuffer);
	MAutoCLEvent outputEvent;
	MAutoCLMem outputBuffer = outputDeformerBuffer.buffer();

    cl_int err = CL_SUCCESS;
    MGlobal::displayInfo(MString("init ") + err);

    float envelope = data.inputValue(identityNode::envelope).asFloat();
    if (!envelope)
        return MPxGPUDeformer::kDeformerSuccess;
    float amount = data.inputValue(identityNode::aAmount).asFloat();
    // Setup OpenCL kernel.
    if ( !fKernel.get() )
    {
        // Get and compile the kernel.

        MString openCLKernelFile( identityGPUDeformer::pluginLoadPath );
        openCLKernelFile +="/LHTemplateGPUDeformer.cl";

        MString openCLKernelName("identity");

        fKernel = MOpenCLInfo::getOpenCLKernel( openCLKernelFile, openCLKernelName );
        if ( fKernel.isNull() )
        {
            return MPxGPUDeformer::kDeformerFailure;
        }
    }


    // Set all of our kernel parameters.  Input buffer and output buffer may be changing every frame
    // so always set them.
    unsigned int parameterId = 0;
    err = clSetKernelArg(fKernel.get(), parameterId++, sizeof(cl_mem), (void*)outputBuffer.getReadOnlyRef());
    MOpenCLInfo::checkCLErrorStatus(err);
    MGlobal::displayInfo(MString("1 ") + err);
    err = clSetKernelArg(fKernel.get(), parameterId++, sizeof(cl_mem), (void*)inputBuffer.getReadOnlyRef());
    MOpenCLInfo::checkCLErrorStatus(err);
    MGlobal::displayInfo(MString("2 ") + err);
    err = clSetKernelArg(fKernel.get(), parameterId++, sizeof(cl_uint), (void*)&numElements);
    MGlobal::displayInfo(MString("3 ") + err);
    MOpenCLInfo::checkCLErrorStatus(err);
    err = clSetKernelArg(fKernel.get(), parameterId++, sizeof(cl_float), (void*)&envelope);
    MOpenCLInfo::checkCLErrorStatus(err);
    err = clSetKernelArg(fKernel.get(), parameterId++, sizeof(cl_float), (void*)&amount);
    MOpenCLInfo::checkCLErrorStatus(err);

    // Set up our input events.  The input event could be NULL, in that case we need to pass
    // slightly different parameters into clEnqueueNDRangeKernel.
    // cl_event events[ 1 ] = { 0 };
    // cl_uint eventCount = 0;
    // if ( inputEvent.get() )
    // {
    //     events[ eventCount++ ] = inputEvent.get();
    // }


    // size_t workGroupSize;
    // size_t retSize;
    // err = clGetKernelWorkGroupInfo(
    //     fKernel.get(),
    //     MOpenCLInfo::getOpenCLDeviceId(),
    //     CL_KERNEL_WORK_GROUP_SIZE,
    //     sizeof(size_t),
    //     &workGroupSize,
    //     &retSize);
    // MOpenCLInfo::checkCLErrorStatus(err);

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


    // size_t workGroupSize;
    size_t localWorkSize = 256;
    if (retSize > 0) {
        localWorkSize = fLocalWorkSize;
    }
    // global work size must be a multiple of localWorkSize
    size_t globalWorkSize = (localWorkSize - numElements % localWorkSize) + numElements;

    // set up our input events.  The input event could be NULL, in that case we need to pass
    // slightly different parameters into clEnqueueNDRangeKernel
    unsigned int numInputEvents = 0;
    if (inputEvent.get())
    {
        numInputEvents = 1;
    }

    // Run the kernel
    //CL_INVALID_EVENT_WAIT_LIST

    // cl_int err = CL_SUCCESS;
    // cl_command_queue,
 	//cl_kernel
 	//cl_uint
 	//const size_t *
 	//const size_t *
 	//const size_t *
 	//cl_uint 
 	//const cl_event *
 	//cl_event *
    MGlobal::displayInfo(MString("clEnqueueNDRangeKernel ") + err);

    err = clEnqueueNDRangeKernel(
        MOpenCLInfo::getMayaDefaultOpenCLCommandQueue(),//cl_command_queue
        fKernel.get(), 	//cl_kernel
        1, //cl_uint
        NULL, //const size_t*
        &globalWorkSize,
        &localWorkSize,
        numInputEvents,
        numInputEvents ? inputEvent.getReadOnlyRef() : 0,
        outputEvent.getReferenceForAssignment()//cl_event *
        );
    MOpenCLInfo::checkCLErrorStatus(err);
    MGlobal::displayInfo(MString("clEnqueueNDRangeKernel ") + err);

    if ( err != CL_SUCCESS )
    {
        return MPxGPUDeformer::kDeformerFailure;
    }
    MGlobal::displayInfo(MString("Success") + err);

    return MPxGPUDeformer::kDeformerSuccess;
}

void identityGPUDeformer::terminate()
{
    MOpenCLInfo::releaseOpenCLKernel(fKernel);
    fKernel.reset();
}

