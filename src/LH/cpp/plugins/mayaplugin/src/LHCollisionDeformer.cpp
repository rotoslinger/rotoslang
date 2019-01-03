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
MObject LHCollisionDeformer::aInputGeo;
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

//  aInputGeo = gAttr.create("inputGeo", "ingeo");
//  gAttr.addAccept(MFnData::kMesh);


  aInputGeo = tAttr.create("inputGeo", "ingeo", MFnData::kMesh);

//  gAttr.addAccept(MFnData::kNurbsSurface);
//  gAttr.addAccept(MFnData::kNurbsCurve);
  addAttribute(aInputGeo);
  attributeAffects(aInputGeo, outputGeom);

  aInputs = cAttr.create("inputGeoArray", "ingeoarray");
  cAttr.setKeyable(false);
  cAttr.setArray(true);
  cAttr.addChild( aColBBMin );
  cAttr.addChild( aColBBMax );
  cAttr.addChild( aColWorldMatrix );
  cAttr.addChild( aInputGeo );
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

MPoint LHCollisionDeformer::getBulge(int numColPoints, MPoint currPoint, MPoint closestPoint, double bulgeAmount,
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
      oTestMesh =inputsArrayHandle.inputValue().child( LHCollisionDeformer::aInputGeo).asMeshTransformed();


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
  MGlobal::displayInfo(MString("DEBUG: TemptTest ")+tmptstPoint.x);







//  MFnMesh differentMesh;
//  differentMesh = fnMainMesh;
//  fnMainMesh.AllIntersections



// Can Run in parallel. For all intents and purposes this is the main deformation algorithm iterator.
// Some data is gathered, but point information should be
// set in this iteration for optimization
  MMeshIntersector fnMeshIntersector;

  MPointArray allPoints;
  fnMainMesh.getPoints(allPoints);
//  itGeo.allPositions(allPoints);

  numPoints = allPoints.length();

  MPointArray tPoints;
  MPointArray finalPoints;
  isInBBox = false;
  MIntArray hitArray;
  maxDisp = 0.0;
  for (x=0;x < inputCount; x++){
	  colMatrix = colMatrices[x];
//	  double sm[4][4];
//	  colMatrix.get(sm);
//	  MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[0][0] + sm[0][1] + sm[0][2] + sm[0][3]);
//	  MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[1][0] + sm[1][1] + sm[1][2] + sm[1][3]);
//	  MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[2][0] + sm[2][1] + sm[2][2] + sm[2][3]);
//	  MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[3][0] + sm[3][1] + sm[3][2] + sm[3][3]);

//	  double sm[4][4];
//	  colMatrix.get(sm);
//	  MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[0][0] + sm[0][1] + sm[0][2] + sm[0][3]);
//	  MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[1][0] + sm[1][1] + sm[1][2] + sm[1][3]);
//	  MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[2][0] + sm[2][1] + sm[2][2] + sm[2][3]);
//	  MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[3][0] + sm[3][1] + sm[3][2] + sm[3][3]);







	  fnMeshIntersector.create(oColMeshArray[x], colMatrix);
	  MFnMesh fnColMesh(oColMeshArray[x]);


	  MPoint tmptstPoint;
	  fnColMesh.getPoint(0,tmptstPoint);
	  MGlobal::displayInfo(MString("DEBUG: TemptTest ")+tmptstPoint.x);


//	  fnColMesh.getPoints(allColPoints);
//	  for (i=0;i < allColPoints.length(); i++){
//		  allColPoints[i] = allColPoints[i] * colMatrix;
//	  }
//	  fnColMesh.setPoints(allColPoints);
//


	  MMeshIsectAccelParams mmAccelParams = fnColMesh.autoUniformGridParams();
	  for (i=0;i < numPoints; i++){
		  //Check if the point is within the bounding box
		  MPoint bbMin = colBBArray[0].min();
		  MPoint bbMax = colBBArray[0].max();
		  allPoints[i] = allPoints[i]; //* bBMatrix;
		  // If inside bounds run more expensive calculations
	//	  xformPoint = allPoints[i] * bBMatrix;
		  if (allPoints[i].x > bbMin.x &&
			  allPoints[i].y > bbMin.y &&
			  allPoints[i].z > bbMin.z &&
			  allPoints[i].x < bbMax.x &&
			  allPoints[i].y < bbMax.y &&
			  allPoints[i].z < bbMax.z){
	//		  MGlobal::displayInfo(MString("DEBUG: NumPointsOUT ")+ i);
			//Use vertex normal vector to create a ray for casting
			fnMainMesh.getVertexNormal(i, vRay);
			MFloatPointArray hitPoints;

			hit = fnColMesh.allIntersections(allPoints[i], vRay, NULL, NULL, false, MSpace::kObject, 99999999999.0,
											  false, &mmAccelParams, false, hitPoints, NULL, NULL, NULL, NULL, NULL);

			numHits = hitPoints.length();

			if (!hit || numHits % 2 == 0){
				finalPoints.append(allPoints[i]* bBMatrix.inverse());
				hitArray.append(0);
			  // if (isInBBox){
			  //   fnMainMesh.getVertexNormal(i, vRay);
			  //   fnMeshIntersector.getClosestPoint(allPoints[i], closestPointOn);
			  //   closestPoint = closestPointOn.getPoint();
			  //   finalPoints.append(LHCollisionDeformer::getBulge(tPoints.length(), allPoints[i], closestPoint, bulgeAmount,
			  //                                                   bulgeDistance, vRay, bBMatrix));
			  // }

				continue;
			}
			//Project with closest point on surface
			hitArray.append(1);
			isInBBox = true;
			tPoints.append(allPoints[i]);

			fnMeshIntersector.getClosestPoint(allPoints[i], closestPointOn);
			closestPoint = closestPointOn.getPoint();


			testDist = closestPoint.distanceTo(allPoints[i]);
			if (testDist>maxDisp){
			  maxDisp = testDist;
			}


			finalPoints.append(closestPoint * bBMatrix.inverse());
		  }
		else{
			finalPoints.append(allPoints[i] * bBMatrix.inverse());
			hitArray.append(0);
		}
	  }
  }
  if (isInBBox){
    for (i=0;i < numPoints; i++){
        if (!hitArray[i]){
          fnMainMesh.getVertexNormal(i, vRay);
          fnMeshIntersector.getClosestPoint(allPoints[i], closestPointOn);
          closestPoint = closestPointOn.getPoint();
          finalPoints[i] = LHCollisionDeformer::getBulge(tPoints.length(), allPoints[i], closestPoint, bulgeAmount, bulgeDistance, vRay, bBMatrix, maxDisp, curveAttribute);
        }
      }
  }
	  // else{
      //finalPoints.append(allPoints[i]);
      //   if (isInBBox){
      //     fnMainMesh.getVertexNormal(i, vRay);
      //     fnMeshIntersector.getClosestPoint(allPoints[i], closestPointOn);
      //     closestPoint = closestPointOn.getPoint();
      //     finalPoints.append(LHCollisionDeformer::getBulge(tPoints.length(), allPoints[i], closestPoint, bulgeAmount,
      //                                                     bulgeDistance, vRay, bBMatrix));
      //   }
      // else{
      //   finalPoints.append(allPoints[i]);
      // }
      // fnMainMesh.getVertexNormal(i, vRay);
      // fnMeshIntersector.getClosestPoint(allPoints[i], closestPointOn);
      // closestPoint = closestPointOn.getPoint();
      // finalPoints.append(LHCollisionDeformer::getBulge(tPoints.length(), allPoints[i], closestPoint, bulgeAmount,
      //                                                  bulgeDistance, vRay, bBMatrix));
      // finalPoints.append(LHCollisionDeformer::getBulge(allPoints[i], bBMatrix));
    // }

      // if (tPoints.length() > 0){
      //   fnMeshIntersector.getClosestPoint(allPoints[i], closestPointOn);
      //   closestPoint = closestPointOn.getPoint();

      //   pDistance = allPoints[i] - closestPoint;
      //   MVector vDistance(pDistance.x, pDistance.y, pDistance.z);
      //   distance = vDistance.length();
      //   // float bulgeAmount = data.inputValue(aBulgeAmount).asFloat();
      //   // float bulgeDistance = data.inputValue(aBulgeDistance).asFloat();

      //   if (distance < bulgeDistance){
      //     fnMainMesh.getVertexNormal(i, vRay);
      //     finalPoint = allPoints[i] + vRay * bulgeAmount;
      //     finalPoints.append(finalPoint );
      //   }
      //   else{
      //     finalPoints.append(allPoints[i]);
      //   }
      // }
      // else{
      //   finalPoints.append(allPoints[i]);
      // }

   MGlobal::displayInfo(MString("DEBUG: Is in BBox ")+ tPoints.length());
  // MGlobal::displayInfo(MString("DEBUG: NumPoints in MESH") + numPoints);
  // MGlobal::displayInfo(MString("DEBUG: NumPoints in FINAL") + finalPoints.length());


  itGeo.setAllPositions(finalPoints);
  return MS::kSuccess;
}

