#include "splatDeformer.h"

MTypeId     splatDeformer::id( 0x8104D );
MObject         splatDeformer::deformingMesh;

splatDeformer::splatDeformer() {}
splatDeformer::~splatDeformer() {}

void* splatDeformer::creator()
{
        return new splatDeformer();
}

MStatus splatDeformer::initialize()
{
        // local attribute initialization
        MStatus status;
        MFnTypedAttribute mAttr;
        deformingMesh=mAttr.create( "deformingMesh", "dm", MFnMeshData::kMesh);
        mAttr.setStorable(true);

        //  deformation attributes
        status = addAttribute( deformingMesh );
        MCheckStatus(status, "ERROR in addAttribute\n");

        status = attributeAffects( deformingMesh, outputGeom );
        MCheckStatus(status, "ERROR in attributeAffects\n");

        return MStatus::kSuccess;
}

MStatus splatDeformer::compute(const MPlug& plug, MDataBlock& data)
{
        // do this if we are using an OpenMP implementation that is not the same as Maya's.
        // Even if it is the same, it does no harm to make this call.
        MThreadUtils::syncNumOpenMPThreads();

        MStatus status = MStatus::kUnknownParameter;
        if (plug.attribute() != outputGeom) {
                return status;
        }

        unsigned int index = plug.logicalIndex();
        MObject thisNode = this->thisMObject();

        // get input value
        MPlug inPlug(thisNode,input);
        inPlug.selectAncestorLogicalIndex(index,input);
        MDataHandle hInput = data.inputValue(inPlug, &status);
        MCheckStatus(status, "ERROR getting input mesh\n");

        // get the input geometry
        MDataHandle inputData = hInput.child(inputGeom);
        if (inputData.type() != MFnData::kMesh) {
                printf("Incorrect input geometry type\n");
                return MStatus::kFailure;
        }

        // get the input groupId - ignored for now...
        MDataHandle hGroup = inputData.child(groupId);
        unsigned int groupId = hGroup.asLong();

        // get deforming mesh
        MDataHandle deformData = data.inputValue(deformingMesh, &status);
        MCheckStatus(status, "ERROR getting deforming mesh\n");
    if (deformData.type() != MFnData::kMesh) {
                printf("Incorrect deformer geometry type %d\n", deformData.type());
                return MStatus::kFailure;
        }

        MObject dSurf = deformData.asMeshTransformed();
        MFnMesh fnDeformingMesh;
        fnDeformingMesh.setObject( dSurf ) ;

        MDataHandle outputData = data.outputValue(plug);
        outputData.copy(inputData);
        if (outputData.type() != MFnData::kMesh) {
                printf("Incorrect output mesh type\n");
                return MStatus::kFailure;
        }

        MItGeometry iter(outputData, groupId, false);

        // create fast intersector structure
        MMeshIntersector intersector;
        intersector.create(dSurf);

        // get all points at once. Faster to query, and also better for
        // threading than using iterator
        MPointArray verts;
        iter.allPositions(verts);
        int nPoints = verts.length();

        // use bool variable as lightweight object for failure check in loop below
        bool failed = false;

        MTimer timer; timer.beginTimer();

#ifdef _OPENMP
        MGlobal::displayInfo(MString("OPEN MP EXISTS! ") );

#pragma omp parallel for
        MGlobal::displayInfo(MString("OPEN MP EXISTS! ") );

#endif
        for(int i=0; i<nPoints; i++) {

                // Cannot break out of an OpenMP loop, so if one of the
                // intersections failed, skip the rest
                if(failed) continue;

                // mesh point object must be in loop-local scope to avoid race conditions
                MPointOnMesh meshPoint;

                // Do intersection. Need to use per-thread status value as
                // MStatus has internal state and may trigger race conditions
                // if set from multiple threads. Probably benign in this case,
                // but worth being careful.
                MStatus localStatus = intersector.getClosestPoint(verts[i], meshPoint);
                if(localStatus != MStatus::kSuccess) {
                        // NOTE - we cannot break out of an OpenMP region, so set
                        // bad status and skip remaining iterations
                        failed = true;
                        continue;
                }

                // default OpenMP scheduling breaks traversal into large
                // chunks, so low risk of false sharing here in array write.
                verts[i] = meshPoint.getPoint();
        }

        timer.endTimer();
        MGlobal::displayInfo(MString() + timer.elapsedTime());
        // write values back onto output using fast set method on iterator
        iter.setAllPositions(verts);

        if(failed) {
                printf("Closest point failed\n");
                return MStatus::kFailure;
        }

        return status;
}












