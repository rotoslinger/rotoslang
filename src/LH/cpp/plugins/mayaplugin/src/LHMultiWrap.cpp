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

#include "LHMultiWrap.h"

MTypeId LHMultiWrap::id(0x000063464);
MObject LHMultiWrap::aThresholdAmount;
MObject LHMultiWrap::aCacheClosest;
MObject LHMultiWrap::aInputGeo;
MObject LHMultiWrap::aInputParent;
MObject LHMultiWrap::aBaseMesh;
MObject LHMultiWrap::aBindVertexIDArray;
MObject LHMultiWrap::aDebug;

MObject LHMultiWrap::aBindPolyIDArray;
MObject LHMultiWrap::aBindTriangleIDArray;
MObject LHMultiWrap::aBaryCoordsArray;








MStatus LHMultiWrap::initialize() {
  MFnNumericAttribute nAttr;
  MFnCompoundAttribute cAttr;
  MFnTypedAttribute tAttr;
  
  aThresholdAmount = nAttr.create("bindThreshold", "bindthreshold", MFnNumericData::kFloat);
  nAttr.setMin(0.0);
  nAttr.setDefault(0.001);
  nAttr.setKeyable(true);
  addAttribute(aThresholdAmount);
  attributeAffects(aThresholdAmount, outputGeom);

  aBindVertexIDArray = tAttr.create( "bindVertexIDArray", "bindvertexidarray", MFnData::kIntArray );
  tAttr.setKeyable(false);
  tAttr.setStorable(true);
  addAttribute( aBindVertexIDArray );

  aBindPolyIDArray = tAttr.create( "bindPolyIDArray", "bindpolyidarray", MFnData::kIntArray );
  tAttr.setKeyable(false);
  tAttr.setStorable(true);
  addAttribute( aBindPolyIDArray );

  aBindTriangleIDArray = tAttr.create( "bindTriangleIDArray", "bindtriangleidarray", MFnData::kIntArray );
  tAttr.setKeyable(false);
  tAttr.setStorable(true);
  addAttribute( aBindTriangleIDArray );

  aBaryCoordsArray = tAttr.create( "baryCoordsArray", "barycoordsarray", MFnData::kPointArray );
  tAttr.setKeyable(false);
  tAttr.setStorable(true);
  addAttribute( aBaryCoordsArray );
  aDebug = nAttr.create("debug", "debug", MFnNumericData::kInt);
  nAttr.setKeyable(false);
  nAttr.setMax(1);
  nAttr.setMin(0);

  nAttr.setDefault(0);
  nAttr.setChannelBox(true);
  addAttribute(aDebug);
  attributeAffects(aDebug, outputGeom);




  aCacheClosest = nAttr.create("cacheClosestPoint", "cacheclosest", MFnNumericData::kInt);
  nAttr.setKeyable(false);
  nAttr.setMax(1);
  nAttr.setMin(0);

  nAttr.setDefault(1);
  nAttr.setChannelBox(true);
  addAttribute(aCacheClosest);
  attributeAffects(aCacheClosest, outputGeom);

  aBaseMesh = tAttr.create("baseMesh", "basemesh", MFnData::kMesh);
  addAttribute(aBaseMesh);
  attributeAffects(aBaseMesh, outputGeom);

  aInputGeo = tAttr.create("inputGeo", "ingeo", MFnData::kMesh);
  addAttribute(aInputGeo);
  attributeAffects(aInputGeo, outputGeom);

  aInputParent = cAttr.create("inputGeoArray", "inputgeoarray");
  cAttr.setKeyable(false);
  cAttr.setArray(true);
  cAttr.addChild( aInputGeo );
  cAttr.addChild( aBindVertexIDArray );

  cAttr.addChild( aBindPolyIDArray );
  cAttr.addChild( aBindTriangleIDArray );
  cAttr.addChild( aBaryCoordsArray );
  
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  cAttr.setUsesArrayDataBuilder(true);
  addAttribute(aInputParent);
  attributeAffects(aInputParent, outputGeom);

  // Make the deformer weights paintable
  // MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer LHMultiWrap weights;");

  return MS::kSuccess;
}

void* LHMultiWrap::creator() { return new LHMultiWrap; }



MPoint getBarycentricCoords(MPoint sourcePoint, MPoint pointA, MPoint pointB, MPoint pointC)
{
    // My special bary coord getter.  Not sure how I figured this out...
    MPoint baryWeights;
    MVector vector0 = pointA - pointC;
    MVector vector1 = pointB - pointC;
    MVector vector2 = MVector(sourcePoint) - pointC;
    float dot00 = vector0 * vector0;
    float dot01 = vector0 * vector1;
    float dot11 = vector1 * vector1;
    float dot20 = vector2 * vector0;
    float dot21 = vector2 * vector1;
    float denominator = dot00 * dot11 - dot01 * dot01;
    baryWeights.x = (dot11 * dot20 - dot01 * dot21) / denominator;
    baryWeights.y = (dot00 * dot21 - dot01 * dot20) / denominator;
    baryWeights.z = 1.0 - baryWeights.x  - baryWeights.y;
    return baryWeights;
}




// void GetBarycentricCoordinates(const MPoint& P, const MPoint& A, const MPoint& B, const MPoint& C,
//                                MFloatVector& baryWeights) {
//   // From Chad Vernon's CVWrap deformer.  Thank you Chad!!
//   // Compute the normal of the triangle
//   MVector N = (B - A) ^ (C - A);
//   MVector unitN = N.normal();

//   // Compute twice area of triangle ABC
//   double areaABC = unitN * N;

//   if (areaABC == 0.0) {
//     // If the triangle is degenerate, just use one of the points.
//     baryWeights.x = 1.0f;
//     baryWeights.y = 0.0f;
//     baryWeights.z = 0.0f;
//     return;
//   }

//   // Compute a
//   double areaPBC = unitN * ((B - P) ^ (C - P));
//   baryWeights.x = (float)(areaPBC / areaABC);

//   // Compute b
//   double areaPCA = unitN * ((C - P) ^ (A - P));
//   baryWeights.y = (float)(areaPCA / areaABC);

//   // Compute c
//   baryWeights.z = 1.0f - baryWeights.x - baryWeights.y;
// }

// void GetBarycentricCoordinates(const MPoint& P, const MPoint& A, const MPoint& B, const MPoint& C,
//                                BaryCoords& coords) {
//   // From Chad Vernon's CVWrap deformer.  Thank you Chad!!
//   // Compute the normal of the triangle
//   MVector N = (B - A) ^ (C - A);
//   MVector unitN = N.normal();

//   // Compute twice area of triangle ABC
//   double areaABC = unitN * N;

//   if (areaABC == 0.0) {
//     // If the triangle is degenerate, just use one of the points.
//     coords[0] = 1.0f;
//     coords[1] = 0.0f;
//     coords[2] = 0.0f;
//     return;
//   }

//   // Compute a
//   double areaPBC = unitN * ((B - P) ^ (C - P));
//   coords[0] = (float)(areaPBC / areaABC);

//   // Compute b
//   double areaPCA = unitN * ((C - P) ^ (A - P));
//   coords[1] = (float)(areaPCA / areaABC);

//   // Compute c
//   coords[2] = 1.0f - coords[0] - coords[1];
// }

MStatus LHMultiWrap::getBindData(  MDataBlock& data, std::vector <MFnMesh*> inputFnMeshArray, MFnMesh* fnBaseMesh,
                                   MArrayDataHandle inputsArrayHandle, int inputCount,
                                   MObjectArray& oDriverMeshArray, int vertCount, float thresholdAmt, int cache, int debug)
{
  // Will be storing 3 important kinds of data for now.
  // These are each per point informations.
  // If you don't find a point coorespondance, just fill with dummy info and move on

  // 1. bary coordinates in an MFloatVectorArray (index per point)
      // Each point will be associated with a bary coord that cooresponds to a specific triangle
      // MFloatVector is a tuple of three, which cooresponds to each point of a triangle
  // 2. int array of polygon ID in an MIntArray (index per point)
    // Each point will be associated with a face ID and Triangle ID
  // 3. int array of triangle ID in an MIntArray (index per point)
    // Each point will be associated with a face ID and Triangle ID

  // Will be Using MMeshInteresector to find the polygon ID and triangleID
  MStatus status;

  MPoint closestPointDummy;
  MIntArray polyPointIds;
  MPoint currentPoint;
  MPoint baseCurrentPoint;

  MMeshIsectAccelParams mmAccelParams = fnBaseMesh->autoUniformGridParams();


  // only checking the first index could be risky,
  // but this is probably the fastest way to make sure the bind data is valid without checking all kinds of different things
  if (storedVertIndexArray.size() && storedVertIndexArray[0].length() == vertCount)
  {
    vertIndexArray = storedVertIndexArray;
    polyIndexArray = storedPolyIndexArray;
    triangleIndexArray = storedTriangleIndexArray;
    baryCoordsArray = storedBaryCoordsArray;

  }

  
  // Closest point cache
  if (!cache || !vertIndexArray.size() || vertIndexArray.size() != oDriverMeshArray.length())
  {
    if (vertIndexArray.size())
    {
      vertIndexArray.clear();
    }
    for (int inputMeshID = 0; inputMeshID < inputFnMeshArray.size(); inputMeshID++)
    {
      fnWeightIntersector.create(oDriverMeshArray[inputMeshID]);
      MIntArray tempVertIdxArray;
      MIntArray tempPolyIdxArray;
      MIntArray tempTriangleIdxArray;
      MPointArray tempBaryCoordsArray;
      for (int vertID = 0; vertID < vertCount; vertID++)
      {
        fnBaseMesh->getPoint(vertID, currentPoint, MSpace::kWorld);
        fnWeightIntersector.getClosestPoint(currentPoint, ptOnMesh);
        pointOnPoint = ptOnMesh.getPoint();
        polyID = ptOnMesh.faceIndex();
        triangleID = ptOnMesh.triangleIndex();

        // Get triangle Ids
        inputFnMeshArray[inputMeshID]->getPolygonTriangleVertices(polyID, triangleID, trianglePointIDs);
        MPointArray trianglePoints;
        for (int triangleIdx = 0; triangleIdx < 3; triangleIdx++)
        {
          inputFnMeshArray[inputMeshID]->getPoint(trianglePointIDs[triangleIdx], pt, MSpace::kWorld);
          trianglePoints.append(pt);
        }
        
        tempBaryCoordsArray.append(getBarycentricCoords(currentPoint, trianglePoints[0], trianglePoints[1], trianglePoints[2]));

        inputFnMeshArray[inputMeshID]->getPolygonVertices(polyID, polyPointIds);
        int closestIdx = -1;
        for (int polyPointID = 0; polyPointID < polyPointIds.length(); polyPointID++)
        {
          inputFnMeshArray[inputMeshID]->getPoint(polyPointIds[polyPointID], baseCurrentPoint, MSpace::kWorld);
          if (currentPoint.distanceTo(baseCurrentPoint) <= thresholdAmt)
          {
            closestIdx = polyPointIds[polyPointID];
            break;
          }
        }
        tempVertIdxArray.append(closestIdx);
        tempPolyIdxArray.append(polyID);
        tempTriangleIdxArray.append(triangleID);
      }
      vertIndexArray.push_back(tempVertIdxArray);
      polyIndexArray.push_back(tempPolyIdxArray);
      triangleIndexArray.push_back(tempTriangleIdxArray);
      baryCoordsArray.push_back(tempBaryCoordsArray);
    }

    for (int i=0;i < inputCount; i++)
    {
      status = inputsArrayHandle.jumpToElement(i);
      CHECK_MSTATUS_AND_RETURN_IT( status);

      // Set value in MObject
      MFnIntArrayData outputIntArrayFn;
      MObject oOutputArray = outputIntArrayFn.create(vertIndexArray[i]);
      MFnIntArrayData outputPolyIntArrayFn;
      MObject oPolyOutputArray = outputPolyIntArrayFn.create(polyIndexArray[i]);
      MFnIntArrayData outputTriangleIntArrayFn;
      MObject oTriangleOutputArray = outputTriangleIntArrayFn.create(triangleIndexArray[i]);

      MFnPointArrayData outputBaryCoordsArrayFn;
      MObject oBaryCoordsArray = outputBaryCoordsArrayFn.create(baryCoordsArray[i]);
      
      if (oOutputArray.isNull() || oPolyOutputArray.isNull()|| oTriangleOutputArray.isNull() )
      {
          MGlobal::displayInfo(MString("The output is NULL"));
          return MS::kFailure;
      }
      MDataHandle handle = inputsArrayHandle.outputValue().child(LHMultiWrap::aBindVertexIDArray);
      handle.setMObject(oOutputArray);

      MDataHandle polyHandle = inputsArrayHandle.outputValue().child(LHMultiWrap::aBindPolyIDArray);
      polyHandle.setMObject(oPolyOutputArray);

      MDataHandle triangleHandle = inputsArrayHandle.outputValue().child(LHMultiWrap::aBindTriangleIDArray);
      triangleHandle.setMObject(oTriangleOutputArray);

      MDataHandle baryCoordsHandle = inputsArrayHandle.outputValue().child(LHMultiWrap::aBaryCoordsArray);
      baryCoordsHandle.setMObject(oBaryCoordsArray);
    }
    data.setClean(LHMultiWrap::aBindVertexIDArray);
    data.setClean(LHMultiWrap::aBindPolyIDArray);
    data.setClean(LHMultiWrap::aBindTriangleIDArray);
    data.setClean(LHMultiWrap::aBaryCoordsArray);
    data.setClean(LHMultiWrap::aInputParent);
  }

  return MS::kSuccess;

}

MStatus LHMultiWrap::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;

  float env = data.inputValue(envelope).asFloat();
  if (!env)
  {
    return MS::kSuccess;
  }
  float thresholdAmt = data.inputValue(aThresholdAmount).asFloat();
  int cache = data.inputValue(aCacheClosest).asInt();
  int debug = data.inputValue(aDebug).asInt();
  MObject oBaseMesh = data.inputValue(LHMultiWrap::aBaseMesh).asMeshTransformed();
  if (oBaseMesh.isNull())
  {
      if (debug)
      {
      MGlobal::displayError(MString("Unable to get baseMesh, baseMesh should be duplicate of deformed mesh"));
      }
      return MS::kFailure;
  }

  MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHMultiWrap::aInputParent, &status));
  CHECK_MSTATUS_AND_RETURN_IT( status);


  int inputCount = inputsArrayHandle.elementCount(&status);
  CHECK_MSTATUS_AND_RETURN_IT( status);

  MObjectArray oDriverMeshArray;
  status = LHMultiWrap::getMeshes(inputsArrayHandle,
                                  inputCount,
                                  oDriverMeshArray,
                                  debug);
  if (status == MS::kFailure)
  {
      return MS::kFailure;
  }

  MIntArray vertIDArray;
  status = LHMultiWrap::storeBindData(inputsArrayHandle, inputCount, vertIDArray, oDriverMeshArray, cache, debug);
  if (status == MS::kFailure)
  {
      return MS::kFailure;
  }

  // Having a mismatach of points between the driven mesh and the base will result in a crash, it is very important to make sure this doesn't happen
  MArrayDataHandle inputGeoArrayHandle(data.inputArrayValue( input, &status));
  status = inputGeoArrayHandle.jumpToElement(mIndex);
  CHECK_MSTATUS_AND_RETURN_IT( status);
  MObject oMainMesh =inputGeoArrayHandle.inputValue().child( inputGeom ).asMeshTransformed();
  if (oMainMesh.isNull()){
	 MGlobal::displayError(MString("DEBUG: oMainMesh is null "));
	 return MS::kFailure;
  }
  MFnMesh* fnMainMesh = new MFnMesh(oMainMesh);
  MFnMesh* fnBaseMesh = new MFnMesh(oBaseMesh);
  int vertCount = fnMainMesh->numVertices();
  if (vertCount != fnBaseMesh->numVertices())
  {
    MGlobal::displayError(MString("Point mismatch between main and base geometries"));
    return MS::kFailure;
  }

  std::vector <MFnMesh*> inputFnMeshArray;
  for (int i=0;i < oDriverMeshArray.length(); i++){
      inputFnMeshArray.push_back(new MFnMesh(oDriverMeshArray[i]));
  }

  status = LHMultiWrap::getBindData(data, inputFnMeshArray, fnBaseMesh,
                                   inputsArrayHandle, inputCount,
                                   oDriverMeshArray, vertCount, thresholdAmt, cache, debug);
  if (status == MS::kFailure)
  {
      return MS::kFailure;
  }

  // if (baryCoordsArray.size())
  // {
  //   MGlobal::displayInfo(MString("AAAAAAA ") + baryCoordsArray[2][2].x + " " + baryCoordsArray[2][2].y + " " + baryCoordsArray[2][2].z);
  // }

  MPoint toPoint;
  MPoint fromPoint;

  for (; !itGeo.isDone(); itGeo.next()) {
    int currentID = itGeo.index();
    pt = itGeo.position();
    for (int inputMeshID = 0; inputMeshID < inputFnMeshArray.size(); inputMeshID++)
    {
      int idx = vertIndexArray[inputMeshID][currentID];
      if (idx == -1)
      {
        continue;
      }
      else 
      {
        inputFnMeshArray[inputMeshID]->getPoint(idx, fromPoint);
        fnBaseMesh->getPoint(currentID, toPoint);
        pt = pt + (fromPoint-toPoint);
      }
    }
    itGeo.setPosition(pt);

  }
  return MS::kSuccess;
}


MStatus LHMultiWrap::storeBindData(MArrayDataHandle inputsArrayHandle, int inputCount, MIntArray& vertIDArray, MObjectArray& oDriverMeshArray, int cache, int debug)
{
  
  MStatus status;
  MDataHandle testHandle;
  // Get bind data
  if (!cache || !storedVertIndexArray.size() || storedVertIndexArray.size() != oDriverMeshArray.length())
  {
    if (storedVertIndexArray.size())
    {
      storedVertIndexArray.clear();
    }
    for (int i=0;i < inputCount; i++)
    {
      status = inputsArrayHandle.jumpToElement(i);
      CHECK_MSTATUS_AND_RETURN_IT( status);

      testHandle = inputsArrayHandle.inputValue(&status);
      CHECK_MSTATUS_AND_RETURN_IT( status);


      // Get the stored bind data
      MDataHandle hInputArray = testHandle.child( aBindVertexIDArray);
      MObject oInputArray = hInputArray.data();
      MFnIntArrayData dataIntArrayFn(oInputArray);
      dataIntArrayFn.copyTo(vertIDArray);
      // Put the stored bind data into a std vector
      storedVertIndexArray.push_back(vertIDArray);
    }
  }  
  return MS::kSuccess;
}


MStatus LHMultiWrap::getMeshes(MArrayDataHandle inputsArrayHandle,
                               int inputCount,
                               MObjectArray& oDriverMeshArray,
                               int debug)
{
  MStatus status;
  MObject oTestMesh;
  MDataHandle testHandle;
  for (int i=0;i < inputCount; i++){
      status = inputsArrayHandle.jumpToElement(i);
      CHECK_MSTATUS_AND_RETURN_IT( status);

      testHandle = inputsArrayHandle.inputValue(&status);
      CHECK_MSTATUS_AND_RETURN_IT( status);


      oTestMesh = testHandle.child( LHMultiWrap::aInputGeo).asMeshTransformed();
      if (oTestMesh.isNull()){
    	  continue;
      }
      oDriverMeshArray.append(oTestMesh);
  }
  if (!oDriverMeshArray.length())
  {
    if (debug)
    {
      MGlobal::displayError(MString("Couldn't get any driver meshes, connect to inputGeo"));
    }
    return MS::kFailure;
  }
  return MS::kSuccess;
  
}