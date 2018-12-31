#include "sseDeformer.h"
//======================================================================
MTypeId     sseDeformer::id( 0x8104E );
// local attributes
MObject sseDeformer::sseEnabled;
sseDeformer::sseDeformer() {}
sseDeformer::~sseDeformer() {}
//======================================================================
void* sseDeformer::creator()
{
    return new sseDeformer();
}
//======================================================================
MStatus sseDeformer::initialize()
{
    // local attribute initialization
    MStatus status;
    MFnNumericAttribute mSSEAttr;
    sseEnabled=mSSEAttr.create( "enableSSE", "sse", MFnNumericData::kBoolean, 0, &status);
    mSSEAttr.setStorable(true);
    //  deformation attributes
    status = addAttribute( sseEnabled );
    MCheckStatus(status, "ERROR in addAttribute\n");
    status = attributeAffects( sseEnabled, outputGeom );
    MCheckStatus(status, "ERROR in attributeAffects\n");
    return MStatus::kSuccess;
}
//======================================================================
//
// Standard compute method. Notice how it handles both the case of
// evaluation of the child and the parent array plugs.
//
// Normal deformer plug-ins only override the deform() method, which is
// the simpler way to do things. In those cases where you have other
// reasons for wanting to override the compute() method directly use this
// as a template for how to do that.
//
MStatus sseDeformer::compute(const MPlug& plug, MDataBlock& data)
{
    MStatus status;
    MObject thisNode = this->thisMObject();
    if (plug.attribute() != outputGeom)
    {
        printf("Ignoring requested plug\n");
        return status;
    }
    // The evaluation manager always evaluates root attributes so it is
    // necessary in the compute() method to handle that case, as well as
    // the case of only evaluating a single child attribute.
    //
    if( plug.isArray() )
    {
        // In the EM evaluation the input array will already have been
        // computed so inputArrayReference() could also be used, but
        // this way the same code works for EM and DG modes.
        //
        MPlug inPlug(thisNode,input);
        MArrayDataHandle hInput = data.inputArrayValue(inPlug, &status);
        MCheckStatus(status, "ERROR getting input mesh\n");

        status = hInput.jumpToArrayElement(0);
        if( MStatus::kSuccess == status )
        {
            do
            {
                MDataHandle hInputElement = hInput.inputValue( &status );
                MCheckStatus(status, "ERROR getting input mesh element\n");
                unsigned int inputIndex = hInput.elementIndex(&status);
                MCheckStatus(status, "ERROR getting input mesh element index\n");
                computeOneOutput( inputIndex, data, hInputElement );
            } while( MStatus::kSuccess == hInput.next() );
        }
    }
    else
    {
        // Children are still computed when you are doing some types of manipulation,
        // when the EM is disabled, when the EM mode is set to "off", or in those rare
        // cases where an internal evaluation has triggered a non-root plug request.
        //
        MPlug inPlug(thisNode,input);
        inPlug.selectAncestorLogicalIndex(plug.logicalIndex(),input);
        MDataHandle hInput = data.inputValue(inPlug, &status);
        MCheckStatus(status, "ERROR getting input mesh\n");

        computeOneOutput( plug.logicalIndex(), data, hInput );
    }
    return status;
}
//======================================================================
//
// Given the index of a single input, compute the corresponding deformed output
// and put it back into the datablock.
//
MStatus sseDeformer::computeOneOutput(unsigned int index, MDataBlock& data, MDataHandle& hInput)
{
    MStatus status;
    MObject thisNode = this->thisMObject();
    MPlug outPlug(thisNode, outputGeom);
    outPlug.selectAncestorLogicalIndex(index, outputGeom);
    // get the input geometry
    MDataHandle inputData = hInput.child(inputGeom);
    if (inputData.type() != MFnData::kMesh) {
        printf("Incorrect input geometry type\n");
        return MStatus::kFailure;
    }
    MObject iSurf = inputData.asMesh() ;
    MFnMesh inMesh;
    inMesh.setObject( iSurf ) ;
    MDataHandle outputData = data.outputValue(outPlug);
    outputData.copyWritable(inputData);
    if (outputData.type() != MFnData::kMesh) {
        printf("Incorrect output mesh type\n");
        return MStatus::kFailure;
    }

    MObject oSurf = outputData.asMesh() ;
    if(oSurf.isNull()) {
        printf("Output surface is NULL\n");
        return MStatus::kFailure;
    }
    MFnMesh outMesh;
    outMesh.setObject( oSurf ) ;
    MCheckStatus(status, "ERROR setting points\n");
    // get all points at once for demo purposes. Really should get points from the current group using iterator
    MFloatPointArray pts;
    outMesh.getPoints(pts);
    int nPoints = pts.length();
    MDataHandle envData = data.inputValue(envelope, &status);
    float env = envData.asFloat();
    MDataHandle sseData = data.inputValue(sseEnabled, &status);
    bool sseEnabled = (bool) sseData.asBool();
    // NOTE: Using MTimer and possibly other classes disables
    // autovectorization with Intel <=10.1 compiler on OSX and Linux!!
    // Must compile this function with -fno-exceptions on OSX and
    // Linux to guarantee autovectorization is done. Use -fvec_report2
    // to check for vectorization status messages with Intel compiler.
    MTimer timer; timer.beginTimer();
    if(sseEnabled) {
        // Innter loop will autovectorize. Around 3x faster than the
        // loop below it. It would be faster if first element was
        // guaranteed to be aligned on 16 byte boundary.
        for(int i=0; i<nPoints; i++) {
            float* ptPtr = &pts[i].x;
            for(int j=0; j<4; j++) {
                ptPtr[j] = env * (cosf(ptPtr[j]) * sinf(ptPtr[j]) * tanf(ptPtr[j]));
            }
        }
    } else {
        // This inner loop will not autovectorize.
        for(int i=0; i<nPoints; i++) {
            MFloatPoint& pt = pts[i];
            for(int j=0; j<3; j++) {
                pt[j] = env * (cosf(pt[j]) * sinf(pt[j]) * tanf(pt[j]));
            }
        }
    }
    timer.endTimer();
    if(sseEnabled) {
        printf("SSE enabled, runtime %f\n", timer.elapsedTime());
    } else {
        printf("SSE disabled, runtime %f\n", timer.elapsedTime());
    }
    outMesh.setPoints(pts);
    // NOTE: This is a crucial step in EM evaluation, especially in
    //       the case where you have multiple outgoing connections.
    //       It keeps the EM state up to date and prevents multiple
    //       evaluation requests that at best will slow things down
    //       and at worst could crash the system.
    //
    // Tell the EM that data has been set and is now valid.
    //
    outputData.setMObject( oSurf );
    return status;
}
