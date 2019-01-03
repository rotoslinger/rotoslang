//==============================================================
// Ultra simple deformer to be used as a starter template//////
// In commented out lines you can see steps involved in trying to get as much speed as possible
// such as not getting painted weight values on every iteration
// Tried putting all positions into an array and setting all positions at once
// because it is supposed to be faster, but this was actually 3fps slower on a mesh of 39,000 points...
// also, not setting pt to a variable, just doing the whole algorithm in one step was 2 fps faster
// If weights are needed, they should be gathered outside the main loop
// and even cached into a std::vector <MFloatArray> with a boolean attribute to turn caching on and off
//==============================================================

#include "LHCollisionDeformer.h"
#include <maya/MFnPlugin.h>

MTypeId LHCollisionDeformer::id(0x67438467);
MObject LHCollisionDeformer::aBulgeAmount;
MObject LHCollisionDeformer::aBulgeDistance;
MObject LHCollisionDeformer::aColGeo;
MObject LHCollisionDeformer::aInputs;

MObject LHCollisionDeformer::aMainBBoxMinX;
MObject LHCollisionDeformer::aMainBBoxMinY;
MObject LHCollisionDeformer::aMainBBoxMinZ;
MObject LHCollisionDeformer::aMainBBoxMaxX;
MObject LHCollisionDeformer::aMainBBoxMaxY;
MObject LHCollisionDeformer::aMainBBoxMaxZ;

MObject LHCollisionDeformer::aMainBBMin;
MObject LHCollisionDeformer::aMainBBMax;
MObject LHCollisionDeformer::aMainWorldMatrix;

MObject LHCollisionDeformer::aColBBoxMinX;
MObject LHCollisionDeformer::aColBBoxMinY;
MObject LHCollisionDeformer::aColBBoxMinZ;
MObject LHCollisionDeformer::aColBBoxMaxX;
MObject LHCollisionDeformer::aColBBoxMaxY;
MObject LHCollisionDeformer::aColBBoxMaxZ;

MObject LHCollisionDeformer::aColBBMin;
MObject LHCollisionDeformer::aColBBMax;
MObject LHCollisionDeformer::aColWorldMatrix;
MObject LHCollisionDeformer::aFalloffRamp;

MObject LHCollisionDeformer::aTestGeo;


MStatus LHCollisionDeformer::initialize() {
  MFnNumericAttribute nAttr;
  MFnGenericAttribute gAttr;
  MFnCompoundAttribute cAttr;
  MFnMatrixAttribute mAttr;
  MRampAttribute rAttr;
  MFnTypedAttribute tAttr;

  //Main Matrix
  aMainWorldMatrix = mAttr.create("aMainWorldMatrix", "mwmatrix");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aMainWorldMatrix );
  attributeAffects(aMainWorldMatrix, outputGeom);


  //Main BBOXES
  aMainBBoxMinX = nAttr.create("mainBBMinX", "mainbbminx", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMinX);
  attributeAffects(aMainBBoxMinX, outputGeom);

  aMainBBoxMinY = nAttr.create("mainBBMinY", "mainbbminy", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMinY);
  attributeAffects(aMainBBoxMinY, outputGeom);

  aMainBBoxMinZ = nAttr.create("mainBBMinZ", "mainbbminz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMinZ);
  attributeAffects(aMainBBoxMinZ, outputGeom);

  aMainBBMin = cAttr.create("mainBBMin", "mainbbmin");
  cAttr.addChild( aMainBBoxMinX );
  cAttr.addChild( aMainBBoxMinY );
  cAttr.addChild( aMainBBoxMinZ );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aMainBBMin);
  attributeAffects(aMainBBMin, outputGeom);


  aMainBBoxMaxX = nAttr.create("mainBBMaxX", "mainbbmaxx", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMaxX);
  attributeAffects(aMainBBoxMaxX, outputGeom);

  aMainBBoxMaxY = nAttr.create("mainBBMaxY", "mainbbmaxy", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMaxY);
  attributeAffects(aMainBBoxMaxY, outputGeom);

  aMainBBoxMaxZ = nAttr.create("mainBBMaxZ", "mainbbmaxz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMaxZ);
  attributeAffects(aMainBBoxMaxZ, outputGeom);

  aMainBBMax = cAttr.create("mainBBMax", "mainbbmax");
  cAttr.addChild( aMainBBoxMaxX );
  cAttr.addChild( aMainBBoxMaxY );
  cAttr.addChild( aMainBBoxMaxZ );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aMainBBMax);
  attributeAffects(aMainBBMax, outputGeom);
  ///////////////////////////



//
//
//  ///ARRAY BOUNDS
//
  //Col Matrix
  aColWorldMatrix = mAttr.create("aColWorldMatrix", "colwmatrix");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aColWorldMatrix );
  attributeAffects(aColWorldMatrix, outputGeom);


  //Col BBOXES
  aColBBoxMinX = nAttr.create("colBBMinX", "colbbminx", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMinX);
  attributeAffects(aColBBoxMinX, outputGeom);

  aColBBoxMinY = nAttr.create("colBBMinY", "colbbminy", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMinY);
  attributeAffects(aColBBoxMinY, outputGeom);

  aColBBoxMinZ = nAttr.create("colBBMinZ", "colbbminz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMinZ);
  attributeAffects(aColBBoxMinZ, outputGeom);

  aColBBMin = cAttr.create("colBBMin", "colbbmin");
  cAttr.addChild( aColBBoxMinX );
  cAttr.addChild( aColBBoxMinY );
  cAttr.addChild( aColBBoxMinZ );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aColBBMin);
  attributeAffects(aColBBMin, outputGeom);


  aColBBoxMaxX = nAttr.create("colBBMaxX", "colbbmaxx", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMaxX);
  attributeAffects(aColBBoxMaxX, outputGeom);

  aColBBoxMaxY = nAttr.create("colBBMaxY", "colbbmaxy", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMaxY);
  attributeAffects(aColBBoxMaxY, outputGeom);

  aColBBoxMaxZ = nAttr.create("colBBMaxZ", "colbbmaxz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMaxZ);
  attributeAffects(aColBBoxMaxZ, outputGeom);

  aColBBMax = cAttr.create("colBBMax", "colbbmax");
  cAttr.addChild( aColBBoxMaxX );
  cAttr.addChild( aColBBoxMaxY );
  cAttr.addChild( aColBBoxMaxZ );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aColBBMax);
  attributeAffects(aColBBMax, outputGeom);






  aBulgeAmount = nAttr.create("bulgeAmount", "bamnt", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  nAttr.setDefault(0.0);
  addAttribute(aBulgeAmount);
  attributeAffects(aBulgeAmount, outputGeom);

  aBulgeDistance = nAttr.create("bulgeDistance", "bdist", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  nAttr.setDefault(0.0);
  addAttribute(aBulgeDistance);
  attributeAffects(aBulgeDistance, outputGeom);

//  aColGeo = gAttr.create("inputGeo", "ingeo");
//  gAttr.addAccept(MFnData::kMesh);
  // addAttribute(aColGeo);
  // attributeAffects(aColGeo, outputGeom);
//  gAttr.addAccept(MFnData::kNurbsSurface);
//  gAttr.addAccept(MFnData::kNurbsCurve);

  aTestGeo = gAttr.create("testGeo", "tgeo");
  gAttr.addAccept(MFnData::kMesh);
  addAttribute(aTestGeo);
  attributeAffects(aTestGeo, outputGeom);


  aColGeo = tAttr.create("inputGeo", "ingeo", MFnData::kMesh);
  addAttribute(aColGeo);
  attributeAffects(aColGeo, outputGeom);

  aInputs = cAttr.create("inputGeoArray", "ingeoarray");
  cAttr.setKeyable(false);
  cAttr.setArray(true);
  cAttr.addChild( aColBBMin );
  cAttr.addChild( aColBBMax );
  cAttr.addChild( aColWorldMatrix );
  cAttr.addChild( aColGeo );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  cAttr.setUsesArrayDataBuilder(true);
  addAttribute(aInputs);
  attributeAffects(aInputs, outputGeom);

	aFalloffRamp = rAttr.createCurveRamp("falloffShape", "fshape");
  addAttribute(aFalloffRamp);
  attributeAffects(aFalloffRamp, outputGeom);


  // Make the deformer weights paintable
  MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer LHCollisionDeformer weights;");

  return MS::kSuccess;
}
MBoundingBox LHCollisionDeformer::getBoundingBox(MDataBlock& data, MObject worldMatrix, MObject oMinBB, MObject oMaxBB){
	  bBMatrix = data.inputValue( worldMatrix ).asMatrix();
	  double3& minBB = data.inputValue( oMinBB ).asDouble3();
	  double3& maxBB = data.inputValue( oMaxBB ).asDouble3();
	  MPoint minBBPoint(minBB[0], minBB[1], minBB[2]);
	  MPoint maxBBPoint(maxBB[0], maxBB[1], maxBB[2]);
	  MBoundingBox mainBB(minBBPoint, maxBBPoint);
	  mainBB.transformUsing(bBMatrix);
	  return mainBB;
}

MBoundingBox LHCollisionDeformer::getBoundingBoxMultiple(MDataBlock& data, MMatrix &colWorldMatrix, MObject oMinBB, MObject oMaxBB,
												 unsigned int index, MObject oCompound){
//	  MStatus status;
	  MArrayDataHandle compoundArrayHandle(data.inputArrayValue( oCompound));
//	  CheckStatusReturn( status, "Unable to get inputs for col bounding box" );

      compoundArrayHandle.jumpToElement(index);
//	  CheckStatusReturn( status, "Unable to jumpt to element for col bounding box" );

//      colWorldMatrix =compoundArrayHandle.inputValue().child( worldMatrix ).asMatrix();
      double3& minBB =compoundArrayHandle.inputValue().child( oMinBB ).asDouble3();
      double3& maxBB =compoundArrayHandle.inputValue().child( oMaxBB ).asDouble3();
	  MPoint minBBPoint(minBB[0], minBB[1], minBB[2]);
	  MPoint maxBBPoint(maxBB[0], maxBB[1], maxBB[2]);
	  MBoundingBox mainBB(minBBPoint, maxBBPoint);
	  mainBB.transformUsing(colWorldMatrix);
//	  rBBox = mainBB;
	  return mainBB;
}

MPoint LHCollisionDeformer::getBulge(MPoint currPoint, MPoint closestPoint, double bulgeAmount,
                                     double bulgeDistance, MVector vRay, MMatrix mainMatrix, double maxDisp, MRampAttribute curveAttribute){
    distance = currPoint.distanceTo(closestPoint);
    double relativeDistance = distance/bulgeDistance;
    float value;
    curveAttribute.getValueAtPosition((float) relativeDistance, value);
    finalPoint = currPoint + vRay * bulgeAmount * (relativeDistance * maxDisp * value) ;
    return finalPoint * mainMatrix.inverse();

}




void* LHCollisionDeformer::creator() { return new LHCollisionDeformer; }

MStatus LHCollisionDeformer::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;

  //Retrieve all data
  float env = data.inputValue(envelope).asFloat();
  if (env<=0.0)
	  return MS::kSuccess;
  float bulgeAmount = data.inputValue(aBulgeAmount).asFloat();
  float bulgeDistance = data.inputValue(aBulgeDistance).asFloat();

  // Get bounding box

  MObject oThis = thisMObject();
  MRampAttribute curveAttribute(oThis, aFalloffRamp);


  MMatrix bBMatrix = data.inputValue( LHCollisionDeformer::aMainWorldMatrix ).asMatrix();
//  double3& minBB = data.inputValue( LHCollisionDeformer::aMainBBMin ).asDouble3();
//  double3& maxBB = data.inputValue( LHCollisionDeformer::aMainBBMax ).asDouble3();
//  MPoint minBBPoint(minBB[0], minBB[1], minBB[2]);
//  MPoint maxBBPoint(maxBB[0], maxBB[1], maxBB[2]);
//  MBoundingBox mainBB(minBBPoint, maxBBPoint);
//  mainBB.transformUsing(bBMatrix);

  mainBB = getBoundingBox(data, LHCollisionDeformer::aMainWorldMatrix, LHCollisionDeformer::aMainBBMin, LHCollisionDeformer::aMainBBMax);

  //Get collision geo
  MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHCollisionDeformer::aInputs, &status));
  CheckStatusReturn( status, "Unable to get inputs" );
  unsigned int inputCount = inputsArrayHandle.elementCount(&status);
  CheckStatusReturn( status, "Unable to get number of inputs" );

  MObjectArray oColMeshArray;
  std::vector <MBoundingBox> colBBArray;

  MMatrixArray colMatrices;

  for (i=0;i < inputCount; i++){

      status = inputsArrayHandle.jumpToElement(i);
      oTestMesh =inputsArrayHandle.inputValue().child( LHCollisionDeformer::aColGeo).asMeshTransformed();


      colMatrix =inputsArrayHandle.inputValue().child( LHCollisionDeformer::aColWorldMatrix ).asMatrix();
      colMatrices.append(colMatrix);


      colBBArray.push_back(LHCollisionDeformer::getBoundingBoxMultiple(data, colMatrix, LHCollisionDeformer::aColBBMin,
    		               LHCollisionDeformer::aColBBMax, inputCount, LHCollisionDeformer::aInputs));
//      MPoint centerTest;
//      centerTest = colBBArray[i].center();
//
// 	  MGlobal::displayInfo(MString("DEBUG: BBoxCenter ")+ centerTest.x);
//
//
      if (oTestMesh.isNull()){
    	  continue;
      }
//      MFnMesh tmpMesh(oTestMesh);
//      fnMeshArray[i](oTestMesh);
      oColMeshArray.append(oTestMesh);
  }
  int nColMeshes = oColMeshArray.length();
  if (!nColMeshes)
	  return MS::kSuccess;
/*
  MIntArray hitMeshes;
  // Do bounding box collision check first, before even touching any point data to be as efficient as possible
  // Test intersections "Quick" collision test. Can run in parallel but not sure if expensive enough to offload...
  for (i=0;i < colBBArray.size();i++){
	  testBounds = colBBArray[i];
	  intersects = testBounds.intersects(mainBB);
	  if (intersects){
		  hitMeshes.append(1);
		  //MGlobal::displayInfo(MString("DEBUG: INTERSECTING "));
	  }
	  //else{
		 //MGlobal::displayInfo(MString("DEBUG: NOT INTERSECTING "));
	  //}
  }
//  if(!hitMeshes.length())
//	 return MS::kSuccess;
*/
  //===============================================================================================================
  // Containment test/deformation algorithm.  If num hits is even, outside the mesh, if odd, inside, if 0, neither.
  // This is MFnMesh AllIntersections, it is slow and NOT threadsafe.
  MArrayDataHandle inputGeoArrayHandle(data.inputArrayValue( input, &status));
  status = inputGeoArrayHandle.jumpToElement(mIndex);
  CheckStatusReturn( status, "Unable to get inputGeom" );
  oMainMesh =inputGeoArrayHandle.inputValue().child( inputGeom ).asMeshTransformed();
  if (oMainMesh.isNull()){
	 MGlobal::displayInfo(MString("DEBUG: oMainMesh is null "));
	 return MS::kFailure;
  }
  //===============================================================================================================
  MFnMesh fnMainMesh(oMainMesh);
  MPoint tmptstPoint;
  fnMainMesh.getPoint(0,tmptstPoint);

// Cannot Run in parallel. Checks if points are in bounding box, if they are, find intersections.
  MMeshIntersector fnMeshIntersector;

  MPointArray allPoints;
  fnMainMesh.getPoints(allPoints);
//  itGeo.allPositions(allPoints);

  numPoints = allPoints.length();
  //=========================
  //====Only used for debug==
  //=========================

  MPointArray finalPoints;
  MPoint initPoint(0.0, 0.0, 0.0);
  //Initialize points, as set length does not...
  for (i=0;i < numPoints; i++){
    finalPoints.append(initPoint);
  }

  for (x=0;x < inputCount; x++){
    MPointArray tPoints;
    MVectorArray vertexNormalArray;

    isInBBox = false;
    MIntArray hitArray;
    maxDisp = 0.0;

	  colMatrix = colMatrices[x];
	  // fnMeshIntersector.create(oColMeshArray[x], colMatrix);
	  MFnMesh fnColMesh(oColMeshArray[x]);
	  fnColMesh.getPoints(allColPoints);

    //=========================
    // Needs to be multiThreaded!!
	  for (i=0;i < allColPoints.length(); i++){
		  allColPoints[i] = allColPoints[i] * colMatrix;
	  }
    //=========================
	  fnColMesh.setPoints(allColPoints);

	  MMeshIsectAccelParams mmAccelParams = fnColMesh.autoUniformGridParams();
	  for (i=0;i < numPoints; i++){
        fnMainMesh.getVertexNormal(i, vRay);
        vertexNormalArray.append(vRay);
        //Check if the point is within the bounding box
        MPoint bbMin = colBBArray[x].min();
        MPoint bbMax = colBBArray[x].max();
        allPoints[i] = allPoints[i]; 
        // If inside bounds run more expensive calculations
        if (allPoints[i].x > bbMin.x &&
          allPoints[i].y > bbMin.y &&
          allPoints[i].z > bbMin.z &&
          allPoints[i].x < bbMax.x &&
          allPoints[i].y < bbMax.y &&
          allPoints[i].z < bbMax.z){
            //Use vertex normal vector to create a ray for casting
            // fnMainMesh.getVertexNormal(i, vRay);
            MFloatPointArray hitPoints;

            hit = fnColMesh.allIntersections(allPoints[i], vRay, NULL, NULL, false, MSpace::kObject, 99999999999.0,
                              false, &mmAccelParams, false, hitPoints, NULL, NULL, NULL, NULL, NULL);

            numHits = hitPoints.length();

            if (!hit || numHits % 2 == 0){
              hitArray.append(0);
              continue;
            }
            //Project with closest point on surface
            hitArray.append(1);
            isInBBox = true;
            //=========================
            //====Only used for debug==
            tPoints.append(allPoints[i]);
            //=========================
          }
      else{
        hitArray.append(0);
	    }
    }
  // Can Mostly be Run in Parallel, the fnMeshIntersector CANNOT be sent outside of this function, so an MObject needs to be passed out and the intersector created in the parallel function
    if (isInBBox){
      //=========================
      // Cannot be run in parallel, the MObject needs to be passed as an arg to the parallel function
      fnMeshIntersector.create(oColMeshArray[x]);
      //=========================

      for (i=0;i < numPoints; i++){
        if  (hitArray[i]){
            fnMeshIntersector.getClosestPoint(allPoints[i], closestPointOn);
            closestPoint = closestPointOn.getPoint();

            testDist = closestPoint.distanceTo(allPoints[i]);
            if (testDist>maxDisp){
              maxDisp = testDist;
            }
            finalPoints[i] = closestPoint * bBMatrix.inverse();
            }
        else{
          finalPoints[i] = allPoints[i] * bBMatrix.inverse();
        }
      }
      for (i=0;i < numPoints; i++){
        if (!hitArray[i]){
          //=========================
          // Cannot be run in parallel, the normal needs to be passed as an arg to the parallel function
          // fnMainMesh.getVertexNormal(i, vRay);
          vRay = vertexNormalArray[i];
          //=========================
          fnMeshIntersector.getClosestPoint(allPoints[i], closestPointOn);
          closestPoint = closestPointOn.getPoint();
          //=========================
          // Need to check whether this can be called from a parallel function, or if a threaded version will need to be written
          finalPoints[i] = LHCollisionDeformer::getBulge(allPoints[i], closestPoint, bulgeAmount, bulgeDistance, vRay, bBMatrix, maxDisp, curveAttribute);
          //=========================
        }
      }
    }
    else{
      for (i=0;i < numPoints; i++){
        finalPoints[i] = allPoints[i] * bBMatrix.inverse();
      }
    }
    if (finalPoints.length() > 0)
      MGlobal::displayInfo(MString("DEBUG: NumPoints in BB") + tPoints.length());

  }
  // MGlobal::displayInfo(MString("DEBUG: Is in BBox ") + tPoints.length());
  // MGlobal::displayInfo(MString("DEBUG: NumPoints in MESH") + numPoints);
  // MGlobal::displayInfo(MString("DEBUG: NumPoints in FINAL") + finalPoints.length());


  itGeo.setAllPositions(finalPoints);
  return MS::kSuccess;
}

