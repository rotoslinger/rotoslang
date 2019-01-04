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
MObject LHCollisionDeformer::aPermanent;
MObject LHCollisionDeformer::aFlipCheck;
MObject LHCollisionDeformer::aInnerFalloffRamp;

MObject LHCollisionDeformer::aBlendBulgeCollision;
MObject LHCollisionDeformer::aBlendBulgeCollisionRamp;

MObject LHCollisionDeformer::aAlgorithm;


MStatus LHCollisionDeformer::initialize() {
  MFnNumericAttribute nAttr;
  MFnGenericAttribute gAttr;
  MFnCompoundAttribute cAttr;
  MFnMatrixAttribute mAttr;
  MRampAttribute rAttr;
  MFnTypedAttribute tAttr;
  MFnEnumAttribute eAttr;

  aAlgorithm = eAttr.create("operation", "op", 0);
  eAttr.addField( "cheap", 0 );
  eAttr.addField( "flipCheck", 1 );
  eAttr.addField( "blend", 2 );
  eAttr.setHidden( false );
  eAttr.setKeyable( true );
  eAttr.setWritable(true);
  eAttr.setStorable(true);
  eAttr.setChannelBox(true);
  addAttribute(aAlgorithm);
  attributeAffects(aAlgorithm, outputGeom);


	aBlendBulgeCollisionRamp = rAttr.createCurveRamp("blendBulgeCollisionRamp", "bbulgecolramp");
  addAttribute(aBlendBulgeCollisionRamp);
  attributeAffects(aBlendBulgeCollisionRamp, outputGeom);


  //Permanent
  aPermanent = nAttr.create("permanent", "perm", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0);
  nAttr.setMin(0);
  nAttr.setMax(1);
  addAttribute(aPermanent);
  attributeAffects(aPermanent, outputGeom);


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

  
///ARRAY BOUNDS
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

	aInnerFalloffRamp = rAttr.createCurveRamp("falloffShapeInner", "fshapein");
  addAttribute(aInnerFalloffRamp);
  attributeAffects(aInnerFalloffRamp, outputGeom);


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
  short eAlgorithm = data.inputValue(aAlgorithm).asShort();

  // Get bounding box

  MObject oThis = thisMObject();
  MRampAttribute rFalloffRamp(oThis, aFalloffRamp);
  MRampAttribute rInnerFalloffRamp(oThis, aInnerFalloffRamp);
  MRampAttribute rBlendBulgeCollisionRamp(oThis, aBlendBulgeCollisionRamp);

  MMatrix bBMatrix = data.inputValue( LHCollisionDeformer::aMainWorldMatrix ).asMatrix();
  int iPermanent = data.inputValue( LHCollisionDeformer::aPermanent ).asInt();
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
  //===============================================================================================================
  // Get the main mesh from the MpxDeformer class
  MArrayDataHandle inputGeoArrayHandle(data.inputArrayValue( input, &status));
  status = inputGeoArrayHandle.jumpToElement(mIndex);
  CheckStatusReturn( status, "Unable to get inputGeom" );
  oMainMesh =inputGeoArrayHandle.inputValue().child( inputGeom ).asMeshTransformed();
  if (oMainMesh.isNull()){
	 MGlobal::displayInfo(MString("DEBUG: oMainMesh is null "));
	 return MS::kFailure;
  }
  MFnMesh fnMainMesh(oMainMesh);
  MPoint tmptstPoint;
  fnMainMesh.getPoint(0,tmptstPoint);

// Will Be used later. Checks if points are in bounding box, if they are, find intersections.
  // MMeshIntersector fnMeshIntersector;

  if (iPermanent){
    if (allPoints.length() == 0){
      fnMainMesh.getPoints(allPoints);
      maxDisp = 0.0;

    }
    else
    {
      for (i=0;i < numPoints; i++){
        allPoints[i] = allPoints[i] * bBMatrix;
        maxDisp = 0.0;

      }
    }
  }
  else{
      fnMainMesh.getPoints(allPoints);
      maxDisp = 0.0;

  }

//  itGeo.allPositions(allPoints);

  numPoints = allPoints.length();
  MPoint initPoint(0.0, 0.0, 0.0);
  for (x=0;x < inputCount; x++){

    //=========================
    //====Only used for debug==
    MPointArray tPoints;
    //=========================
    MVectorArray vertexNormalArray;

    isInBBox = false;
    MIntArray hitArray;
    MIntArray flipRayArray;
    MPointArray flipPointArray;
    MIntArray hitFaceIdArray;


	  colMatrix = colMatrices[x];
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
        // allPoints[i] = allPoints[i]; 
        // If inside bounds run more expensive calculations
        if (allPoints[i].x > bbMin.x &&
          allPoints[i].y > bbMin.y &&
          allPoints[i].z > bbMin.z &&
          allPoints[i].x < bbMax.x &&
          allPoints[i].y < bbMax.y &&
          allPoints[i].z < bbMax.z){
            //Use vertex normal vector to create a ray for casting
            MFloatPointArray hitPoints;

            hit = fnColMesh.allIntersections(allPoints[i], vRay, NULL, NULL, false, MSpace::kObject, 9999999.0,
                              false, &mmAccelParams, true, hitPoints, NULL, &hitFaceIdArray, NULL, NULL, NULL);

            numHits = hitPoints.length();
            // If no hit, or the hit is divisible by 2 skip it, we are outside the mesh (Hormann & Agathos, 2001)
            if (!hit || numHits % 2 == 0){
              hitArray.append(0);
              flipRayArray.append(0);
              flipPointArray.append(initPoint);
              continue;
            }

            //========================================================================================================================================
            //========================================================================================================================================
            //This is a slower, but more accurate cleanup pass of the algorithm to avoid swimming points and points flipping to the inside of the mesh.
            // Need to be sure there is actually a face in the opposite direction, if not there is no point to flipping
            fnColMesh.getPolygonNormal(hitFaceIdArray[0], polyNormal);

						flipCheck = polyNormal * vRay;

						if (eAlgorithm>0){
              vRay = vRay * -1.0;
              MFloatPointArray hitPointsFlipped;
              hit = fnColMesh.allIntersections(allPoints[i], vRay, NULL, NULL, false, MSpace::kObject, 9999999.0,
                                false, &mmAccelParams, true, hitPointsFlipped, NULL, NULL, NULL, NULL, NULL);

              if (hit){
                  flipRayArray.append(1);
                  flipPointArray.append(hitPointsFlipped[0]);
              }
              else{
                  flipRayArray.append(0);
                  flipPointArray.append(hitPoints[0]);
              }
            }
            else{
                  flipRayArray.append(0);
                  flipPointArray.append(hitPoints[0]);
            }
            //========================================================================================================================================
            //========================================================================================================================================




            hitArray.append(1);
            isInBBox = true;
            //=========================
            //====Only used for debug==
            tPoints.append(allPoints[i]);
            //=========================
          }
      else{
        hitArray.append(0);
        flipRayArray.append(0);
        flipPointArray.append(initPoint);
	    }
    }

  // Can Mostly be Run in Parallel, the fnMeshIntersector CANNOT be sent outside of this function, so an MObject needs to be passed out and the intersector created in the parallel function
    if (isInBBox){
      if (eAlgorithm == 2){
      LHCollisionDeformer::BlendBulgeAndCollisionSerial(oColMeshArray, x, numPoints, hitArray,  flipRayArray, allPoints, vertexNormalArray, maxDisp, bulgeDistance,
                                                     rInnerFalloffRamp, bulgeAmount, flipPointArray, rFalloffRamp, rBlendBulgeCollisionRamp);
      }
      else{
      LHCollisionDeformer::seperateBulgeAndCollisionSerial(oColMeshArray, x, numPoints, hitArray,  flipRayArray, allPoints, vertexNormalArray, maxDisp, bulgeDistance,
                                                     rInnerFalloffRamp, bulgeAmount, flipPointArray, rFalloffRamp, eAlgorithm);
      }
    }
    else{
      for (i=0;i < numPoints; i++){
        allPoints[i] = allPoints[i];
      }
    }
    // if (allPoints.length() > 0)
    //   MGlobal::displayInfo(MString("DEBUG: NumPoints in BB") + tPoints.length());
  }
  for (i=0;i < numPoints; i++){
    allPoints[i] = allPoints[i] * bBMatrix.inverse();
  }
  // MGlobal::displayInfo(MString("DEBUG: Is in BBox ") + tPoints.length());
  // MGlobal::displayInfo(MString("DEBUG: NumPoints in MESH") + numPoints);
  // MGlobal::displayInfo(MString("DEBUG: NumPoints in FINAL") + finalPoints.length());


  itGeo.setAllPositions(allPoints);
  return MS::kSuccess;
}


MPoint LHCollisionDeformer::getBulge(MPoint currPoint, MPoint closestPoint, double bulgeAmount,
                                     double bulgeDistance, MVector vRay, double maxDisp, MRampAttribute rFalloffRamp){
    distance = currPoint.distanceTo(closestPoint);
    relativeDistance = distance/bulgeDistance;
    rFalloffRamp.getValueAtPosition((float) relativeDistance, value);
    // return currPoint + vRay * bulgeAmount * (relativeDistance * maxDisp * value) ;
    return currPoint + vRay * bulgeAmount * relativeDistance * maxDisp * value ;

}



void LHCollisionDeformer::seperateBulgeAndCollisionSerial(MObjectArray oColMeshArray, unsigned int colMeshIndex, unsigned int numPoints, MIntArray hitArray,  MIntArray flipRayArray,
                                                      MPointArray &allPoints, MVectorArray vertexNormalArray,double maxDisp, double bulgeDistance, MRampAttribute rInnerFalloffRamp, double bulgeAmount,
                                                      MPointArray flipPointArray, MRampAttribute rFalloffRamp, short algorithm){

  //=========================
  // Cannot be run in parallel, the MObject needs to be passed as an arg to the parallel function
  fnMeshIntersector.create(oColMeshArray[colMeshIndex]);
  //=========================

  for (i=0;i < numPoints; i++){
    if  (hitArray[i]){
        if (flipRayArray[i] && algorithm > 0){
             allPoints[i] = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i,  bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
        }
        else{
          allPoints[i] = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
        }
    }
    else{
        allPoints[i] = allPoints[i];
    }
  }

  for (i=0;i < numPoints; i++){
    if (!hitArray[i]){
      allPoints[i] = LHCollisionDeformer::PerformBulgeSerial(vertexNormalArray, i, allPoints, bulgeAmount, bulgeDistance, maxDisp, rFalloffRamp);
    }
  }
}

void LHCollisionDeformer::BlendBulgeAndCollisionSerial(MObjectArray oColMeshArray, unsigned int colMeshIndex, unsigned int numPoints, MIntArray hitArray,  MIntArray flipRayArray,
                                                      MPointArray &allPoints, MVectorArray vertexNormalArray,double maxDisp, double bulgeDistance, MRampAttribute rInnerFalloffRamp, double bulgeAmount,
                                                      MPointArray flipPointArray, MRampAttribute rFalloffRamp, MRampAttribute rBlendBulgeCollisionRamp){
  //=========================
  // Cannot be run in parallel, the MObject needs to be passed as an arg to the parallel function
  fnMeshIntersector.create(oColMeshArray[colMeshIndex]);
  //=========================
  for (i=0;i < numPoints; i++){
        if  (hitArray[i]){
        collisionPoint = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i,  bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
        blendPoint = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
        distance = blendPoint.distanceTo(collisionPoint);
        relativeDistance = distance/bulgeDistance;
        rBlendBulgeCollisionRamp.getValueAtPosition((float) relativeDistance, value);
        allPoints[i] = blendPoint + (collisionPoint - blendPoint ) *  value;
        }
  }
  for (i=0;i < numPoints; i++){
    if (!hitArray[i]){
      allPoints[i] = LHCollisionDeformer::PerformBulgeSerial(vertexNormalArray, i, allPoints, bulgeAmount, bulgeDistance, maxDisp, rFalloffRamp);
    }
  }
}


MPoint LHCollisionDeformer::PerformBulgeSerial(MVectorArray vertexNormalArray, unsigned int pointIdx, MPointArray allPoints, double bulgeAmount, double bulgeDistance, double maxDisp,
                                                MRampAttribute rFalloffRamp){
    vRay = vertexNormalArray[pointIdx];
    fnMeshIntersector.getClosestPoint(allPoints[pointIdx], closestPointOn);
    closestPoint = closestPointOn.getPoint();
    //=========================
    // Need to check whether this can be called from a parallel function, or if a threaded version will need to be written
    return LHCollisionDeformer::getBulge(allPoints[pointIdx], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp);
    //=========================

}

MPoint LHCollisionDeformer::CollisionFlipCheckSerial(MPointArray allPoints, unsigned int pointIdx,  double bulgeDistance, double bulgeAmount, MVectorArray vertexNormalArray,
                                                     double &maxDisp, MPointArray flipPointArray, MRampAttribute rInnerFalloffRamp){

    fnMeshIntersector.getClosestPoint(allPoints[pointIdx], closestPointOn);
    closestPoint = closestPointOn.getPoint();
    closestNormal = closestPointOn.getNormal();
    vRay = vertexNormalArray[pointIdx];
    flipCheck = closestNormal * vRay;
    testDist = closestPoint.distanceTo(allPoints[pointIdx]);
    if (testDist>maxDisp){
      maxDisp = testDist;
    }
    distance = allPoints[i].distanceTo(closestPoint);
    relativeDistance = distance/bulgeDistance;
    rInnerFalloffRamp.getValueAtPosition((float) relativeDistance, value);
    interPoint = closestPoint + (( closestPoint - flipPointArray[pointIdx]) * (value - 1.1F));
    return interPoint;

}

MPoint LHCollisionDeformer::CollisionCheapSerial(MPointArray allPoints, unsigned int pointIdx, double &maxDisp){
  fnMeshIntersector.getClosestPoint(allPoints[pointIdx], closestPointOn);
  closestPoint = closestPointOn.getPoint();
  testDist = closestPoint.distanceTo(allPoints[pointIdx]);
  if (testDist>maxDisp){
    maxDisp = testDist;
  }
  return closestPoint;
}