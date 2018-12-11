//    float myfloat = fabs(allWeightsArray[0][0][0].length());
//    MGlobal::displayInfo(MString()+myfloat);

#include "LHUVBlendshape.h"

MTypeId LHUVBlendshape::id(0x74508017);

MObject LHUVBlendshape::aDriveMesh;
MObject LHUVBlendshape::aOutMesh;

MObject LHUVBlendshape::aBlendAmt;


void* LHUVBlendshape::creator() { return new LHUVBlendshape; }

MStatus LHUVBlendshape::deform(MDataBlock& data, MItGeometry& MitGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
    MStatus status;
    // envelope
    float envelope = data.inputValue(MPxDeformerNode::envelope).asFloat();
    if (envelope == 0)
    {
        return MS::kSuccess;
    }

    // numeric
    double blendAmt = data.inputValue(aBlendAmt).asDouble();
    // typed
    MObject oDriveMesh = data.inputValue(aDriveMesh).asMeshTransformed();
    MFnMesh fnDriveMesh(oDriveMesh);

    MArrayDataHandle arrayHandle(data.inputArrayValue( MPxDeformerNode::input, &status ));
	CheckStatusReturn( status, "Unable to input" );

    arrayHandle.jumpToElement(0);
    MObject oOutMesh = (arrayHandle.inputValue().child( MPxDeformerNode::inputGeom).asMeshTransformed());

    MFnMesh fnOutMesh(oOutMesh, &status);
	CheckStatusReturn( status, "Unable to fnMesh" );

/*
	float2 returnUV;
//---get uv at point
    MItMeshPolygon iter(oOutMesh);
    int count = iter.count();
    for (; !iter.isDone();)
    {
        pt = iter.position();
        idx = iter.index();

		status = fnOutMesh.getUVAtPoint(pt, returnUV,MSpace::kObject);
    	iter.next();
    }
//    MGlobal::displayInfo(MString(" ")+goodPoint.x+MString(" ")+goodPoint.y+MString(" ")+goodPoint.z);
*/





//---get point at UV example

    MPoint testPoint;
    MPoint goodPoint;
    float2 uv = {0.5,0.5};
    /*
//    MItMeshPolygon iter(oOutMesh);
    int count = iter.count();
    for( unsigned int idx = 0; idx < count; ++idx)
    {
        try
        {
    		status = fnOutMesh.getPointAtUV(idx,testPoint,uv,MSpace::kObject,NULL,.00000000001);
    		if (status == MS::kSuccess)
    			goodPoint = testPoint;
        }
        catch(...)
        {
        ;
        }
//    	iter.next();
    }
//    MGlobal::displayInfo(MString(" ")+goodPoint.x+MString(" ")+goodPoint.y+MString(" ")+goodPoint.z);
*/

    MPoint pos1;
    MPoint pos2;
    MPoint pos3;
    MPoint finalPoint;


    for (; !MitGeo.isDone();)
    {
        pt = MitGeo.position();
        idx = MitGeo.index();
        w = weightValue(data, mIndex, idx)* envelope;
        if (fabs(w) <= 0)
        {
            MitGeo.next();
            continue;
        }
//		status = fnOutMesh.getPointAtUV(idx,testPoint,uv,MSpace::kObject,NULL,.00000000001);

        // test how fast it would be to compose a point from barycentric points

		fnOutMesh.getPoint(0,pos1,MSpace::kObject);
		fnOutMesh.getPoint(0,pos2,MSpace::kObject);
		fnOutMesh.getPoint(0,pos3,MSpace::kObject);

		pos1.x *= 1;
		pos1.y *= 1;
		pos1.z *= 1;

		pos2.x *= 0;
		pos2.y *= 0;
		pos2.z *= 0;

		pos3.x *= 1-1-0;
		pos3.y *= 1-1-0;
		pos3.z *= 1-1-0;

		finalPoint.x *= pos1.x+pos2.x+pos3.x;
		finalPoint.y *= pos1.y+pos2.y+pos3.y;
		finalPoint.z *= pos1.z+pos2.z+pos3.z;






//		u*a + v*b + (1 - u - v)*c
//				+ v*b + (1 - u - v)*c

		//get 3 points, then add them
		pt.x += envelope;
		pt.y += envelope;
		pt.z += envelope;


        //set point

        MitGeo.setPosition(pt);

        MitGeo.next();
    }

    return MS::kSuccess;
}

MStatus LHUVBlendshape::initialize() {

	MFnTypedAttribute tAttr;
	MFnNumericAttribute nAttr;

    ///////////////////////////////////////////
    /////////////// INPUTS ////////////////////
    ///////////////////////////////////////////



    ////////// typed attributes ////////////

    // weight patchallVals
    aDriveMesh = tAttr.create("driveMesh", "dm", MFnData::kMesh);
    addAttribute( aDriveMesh );

    aOutMesh = tAttr.create("outputMesh", "om", MFnData::kMesh);
    addAttribute( aOutMesh );

    // cache attributes

    aBlendAmt = nAttr.create("blendAmount", "ba", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);
    addAttribute(aBlendAmt);


    //////Affects outputs and inputs
    MObject outputGeom = MPxDeformerNode::outputGeom;
    attributeAffects(aDriveMesh, outputGeom);
    attributeAffects(aBlendAmt, outputGeom);



    // Make deformer weights paintable


    MGlobal::executeCommand("makePaintable -attrType multiFloat -shapeMode deformer LHUVBlendshape weights;");

    // Make deformer weights paintable

  return MS::kSuccess;
}
