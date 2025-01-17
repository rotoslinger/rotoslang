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
MObject LHMultiWrap::aBindMatrixArray;

MObject LHMultiWrap::aBindPointsArray;
MObject LHMultiWrap::aBarycentricWeights;
MObject LHMultiWrap::aTriangleVertArray;
MObject LHMultiWrap::aTriangleParent;

// MObject LHMultiWrap::aBindTrianglePointIDArray;

// MObject LHMultiWrap::aTriangleIDParent;







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
  
  aBarycentricWeights = nAttr.create("barycentricWeights", "barycentricWeights", MFnNumericData::k3Float);
  nAttr.setArray(true);




  aBaryCoordsArray = tAttr.create( "baryCoordsArray", "barycoordsarray", MFnData::kPointArray );
  tAttr.setKeyable(false);
  tAttr.setStorable(true);
  addAttribute( aBaryCoordsArray );

  aBindMatrixArray = tAttr.create( "bindMatrixArray", "bindMatrixArray", MFnData::kMatrixArray );
  tAttr.setKeyable(false);
  tAttr.setStorable(true);
  addAttribute( aBindMatrixArray );


  aBindPointsArray = tAttr.create( "bindPointsArray", "bindpointsarray", MFnData::kPointArray );
  tAttr.setKeyable(false);
  tAttr.setStorable(true);
  addAttribute( aBindPointsArray );

  aTriangleVertArray = nAttr.create( "triangleVertIDs", "trianglevertids", MFnNumericData::k3Int );
  nAttr.setArray(true);
  addAttribute( aTriangleVertArray );


  // aTriangleParent = cAttr.create("inputTriangleArray", "inputTriangleArray");
  // cAttr.setKeyable(false);
  // cAttr.setArray(true);
  // cAttr.setReadable(true);
  // cAttr.addChild( aTriangleVertArray );
  // cAttr.setWritable(true);
  // cAttr.setConnectable(true);
  // cAttr.setChannelBox(true);
  // cAttr.setUsesArrayDataBuilder(true);


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



  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  cAttr.setUsesArrayDataBuilder(true);
  addAttribute(aInputParent);
  attributeAffects(aInputParent, outputGeom);



  aInputParent = cAttr.create("inputGeoArray", "inputgeoarray");
  cAttr.setKeyable(false);
  cAttr.setArray(true);
  cAttr.addChild( aInputGeo );
  cAttr.addChild( aBindVertexIDArray );

  cAttr.addChild( aBindPolyIDArray );
  cAttr.addChild( aBindTriangleIDArray );
  cAttr.addChild( aBaryCoordsArray );
  cAttr.addChild( aBindMatrixArray );
  cAttr.addChild( aBindPointsArray );
  cAttr.addChild( aBarycentricWeights );
  cAttr.addChild( aTriangleVertArray );
  
  
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



MStatus LHMultiWrap::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;
  thisMObj = thisMObject();

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
  MPoint origin(0,0,0);
  MPointArray allPoints;
  itGeo.allPositions(allPoints, MSpace::kObject);

  for (; !itGeo.isDone(); itGeo.next()) {
    int currentID = itGeo.index();
    pt = itGeo.position();
    for (int inputMeshID = 0; inputMeshID < inputFnMeshArray.size(); inputMeshID++)
    {
      int idx = vertIndexArray[inputMeshID][currentID];
      // if (idx == -1)
      // {
      //   continue;
      // }
      // else 
      // {
        // MFloatVector baryCoords(baryCoordsArray[inputMeshID][currentID].x,
        //                         baryCoordsArray[inputMeshID][currentID].y,
        //                         baryCoordsArray[inputMeshID][currentID].z);

        // // CANNOT GET THE TRIANGLE AT DEFORM AS THE TRIANGLES CONSTANTLY CHANGE BASED ON THE LOCATIONS OF THE POINTS, GET VERTS IN BIND!!!!!!
        // composedMatrix = TriplePointLogic(triangleVertIDArray[inputMeshID][currentID][0],
        //                                   triangleVertIDArray[inputMeshID][currentID][1],
        //                                   triangleVertIDArray[inputMeshID][currentID][2],
        //                                   inputFnMeshArray[inputMeshID], baryCoords);
        
        inputFnMeshArray[inputMeshID]->getPoint(idx, fromPoint);
        fnBaseMesh->getPoint(currentID, toPoint);
        pt = pt + (fromPoint-toPoint);
        // allPoints[currentID] =  allPoints[currentID] - fromPoint;

        // allPoints[currentID] = allPoints[currentID] * (composedMatrix * bindMatrixArray[inputMeshID][currentID].inverse());

        // allPoints[currentID] =  allPoints[currentID] * bindMatrixArray[inputMeshID][currentID].inverse() * composedMatrix;

        // allPoints[currentID] =  allPoints[currentID] + fromPoint * localToWorldMatrix;
          
        // allPoints[currentID] = (allPoints[currentID] * composedMatrix) + (toPoint -bindPointsArray[inputMeshID][currentID]);
        // allPoints[currentID] = allPoints[currentID] * composedMatrix;
        // allPoints[currentID] = allPoints[currentID] * composedMatrix* bindMatrixArray[inputMeshID][currentID].inverse();

        // if (inputMeshID == 0 )
        // {
        //   allPoints[currentID] =  origin * composedMatrix;
        // }
        // else
        // {
        //   allPoints[currentID] =  allPoints[currentID] * composedMatrix;
        // }
        
      // }
    }
    itGeo.setPosition(pt);

  }
  return MS::kSuccess;
}

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
    bindMatrixArray = storedBindMatrixArray;
    bindPointsArray = storedBindPointsArray;
    triangleVertIDArray = storedTriangleVertIDArray;

  }

  MFnNumericData fnNumericData;

  // Closest point cache
  if (!cache || !vertIndexArray.size() || vertIndexArray.size() != oDriverMeshArray.length())
  {
    if (vertIndexArray.size())
    {
      vertIndexArray.clear();
      polyIndexArray.clear();
      triangleIndexArray.clear();
      baryCoordsArray.clear();
      bindMatrixArray.clear();
      bindPointsArray.clear();
      triangleVertIDArray.clear();
    }
    for (int inputMeshID = 0; inputMeshID < inputFnMeshArray.size(); inputMeshID++)
    {
      fnWeightIntersector.create(oDriverMeshArray[inputMeshID]);
      MIntArray tempVertIdxArray;
      MIntArray tempPolyIdxArray;
      MIntArray tempTriangleIdxArray;
      MPointArray tempBaryCoordsArray;
      MMatrixArray tempBindMatrixArray;
      MPointArray tempBindPointsArray;
      std::vector <MIntArray> tempTriangleVertIDArray;

      for (int vertID = 0; vertID < vertCount; vertID++)
      {
        fnBaseMesh->getPoint(vertID, currentPoint, MSpace::kObject);
        fnWeightIntersector.getClosestPoint(currentPoint, ptOnMesh);
        pointOnPoint = ptOnMesh.getPoint();
        polyID = ptOnMesh.faceIndex();
        triangleID = ptOnMesh.triangleIndex();

        // Get triangle Ids
        
        inputFnMeshArray[inputMeshID]->getPolygonTriangleVertices(polyID, triangleID, trianglePointIDs);
        MPointArray trianglePoints;


        for (int triangleIdx = 0; triangleIdx < 3; triangleIdx++)
        {
          inputFnMeshArray[inputMeshID]->getPoint(trianglePointIDs[triangleIdx], pt, MSpace::kObject);
          trianglePoints.append(pt);
        }
        
        MPoint baryCoords = getBarycentricCoords(currentPoint, trianglePoints[0], trianglePoints[1], trianglePoints[2]);

        MMatrix bindMatrix = TriplePointLogic(trianglePointIDs[0], trianglePointIDs[1], trianglePointIDs[2], inputFnMeshArray[inputMeshID], baryCoords);



        inputFnMeshArray[inputMeshID]->getPolygonVertices(polyID, polyPointIds);
        int closestIdx = -1;
        for (int polyPointID = 0; polyPointID < polyPointIds.length(); polyPointID++)
        {
          inputFnMeshArray[inputMeshID]->getPoint(polyPointIds[polyPointID], baseCurrentPoint, MSpace::kObject);
          if (currentPoint.distanceTo(baseCurrentPoint) <= thresholdAmt)
          {
            closestIdx = polyPointIds[polyPointID];
            break;
          }
        }
        currentPoint = currentPoint * bindMatrix;

        MIntArray triangleIDs(3);
        triangleIDs[0] = trianglePointIDs[0];
        triangleIDs[1] = trianglePointIDs[1];
        triangleIDs[2] = trianglePointIDs[2];

        tempVertIdxArray.append(closestIdx);
        tempPolyIdxArray.append(polyID);
        tempTriangleIdxArray.append(triangleID);
        tempBaryCoordsArray.append(baryCoords);
        tempBindMatrixArray.append(bindMatrix);
        tempBindPointsArray.append(currentPoint);
        tempTriangleVertIDArray.push_back(triangleIDs);

      }
      vertIndexArray.push_back(tempVertIdxArray);
      polyIndexArray.push_back(tempPolyIdxArray);
      triangleIndexArray.push_back(tempTriangleIdxArray);
      baryCoordsArray.push_back(tempBaryCoordsArray);
      bindMatrixArray.push_back(tempBindMatrixArray);
      bindPointsArray.push_back(tempBindPointsArray);
      triangleVertIDArray.push_back(tempTriangleVertIDArray);
    }
    MPlug inputParent(thisMObj, aInputParent);
    MPlug parentElement;
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
      
      MFnMatrixArrayData ouputBindMatrixArrayFn;
      MObject oBindMatrixArray = ouputBindMatrixArrayFn.create(bindMatrixArray[i]);

      MFnPointArrayData ouputBindPointArrayFn;
      MObject oBindPointsArray = ouputBindPointArrayFn.create(bindPointsArray[i]);

      if (oOutputArray.isNull() || oPolyOutputArray.isNull()|| oTriangleOutputArray.isNull() || oBaryCoordsArray.isNull() || oBindMatrixArray.isNull() || oBindPointsArray.isNull())
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

      MDataHandle bindMatrixHandle = inputsArrayHandle.outputValue().child(LHMultiWrap::aBindMatrixArray);
      bindMatrixHandle.setMObject(oBindMatrixArray);

      MDataHandle bindbindPointsHandle = inputsArrayHandle.outputValue().child(LHMultiWrap::aBindPointsArray);
      bindbindPointsHandle.setMObject(oBindPointsArray);

      MPlug parentElement = inputParent.elementByLogicalIndex(i, &status);
      CHECK_MSTATUS_AND_RETURN_IT( status);

      MPlug child = parentElement.child(LHMultiWrap::aTriangleVertArray, &status);
      CHECK_MSTATUS_AND_RETURN_IT( status);
      
      for (int vertID = 0; vertID < vertCount; vertID++)
      {
        MPlug childTriangleVerts = child.elementByLogicalIndex(vertID, &status);
        // MFnIntArrayData outputTriangleArrayFn;
        // MObject oOutputTriangleArray = outputTriangleArrayFn.create(triangleVertIDArray[i][vertID]);

        MObject oNumericData = fnNumericData.create(MFnNumericData::k3Int, &status);
        CHECK_MSTATUS_AND_RETURN_IT(status);
        status = fnNumericData.setData3Int(triangleVertIDArray[i][vertID][0],
                                           triangleVertIDArray[i][vertID][1],
                                           triangleVertIDArray[i][vertID][2]);


        childTriangleVerts.setMObject(oNumericData);
        // MGlobal::displayInfo(MString("cACHING ") + triangleVertIDArray[i][vertID][0] +  ", " + triangleVertIDArray[i][vertID][1] + ", " + triangleVertIDArray[i][vertID][2]);

      }

    }
    data.setClean(LHMultiWrap::aBindVertexIDArray);
    data.setClean(LHMultiWrap::aBindPolyIDArray);
    data.setClean(LHMultiWrap::aBindTriangleIDArray);
    data.setClean(LHMultiWrap::aBaryCoordsArray);
    data.setClean(LHMultiWrap::aBindMatrixArray);
    data.setClean(LHMultiWrap::aBindPointsArray);
    data.setClean(LHMultiWrap::aTriangleParent);
    data.setClean(LHMultiWrap::aTriangleVertArray);
    data.setClean(LHMultiWrap::aInputParent);
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
      storedPolyIndexArray.clear();
      storedTriangleIndexArray.clear();
      storedBaryCoordsArray.clear();
      storedBindMatrixArray.clear();
      storedTriangleVertIDArray.clear();
    }

    // std::vector <std::vector <MIntArray>> tempTriangleVertIDArrayArray;

    for (int i=0;i < inputCount; i++)
    {
      
      status = inputsArrayHandle.jumpToElement(i);
      CHECK_MSTATUS_AND_RETURN_IT( status);

      testHandle = inputsArrayHandle.inputValue(&status);
      CHECK_MSTATUS_AND_RETURN_IT( status);

      MIntArray bindVertexArray;
      // Get the stored bind data
      MDataHandle hInputArray = testHandle.child( aBindVertexIDArray);
      MObject oInputArray = hInputArray.data();
      MFnIntArrayData dataIntArrayFn(oInputArray);
      dataIntArrayFn.copyTo(bindVertexArray);
      // Put the stored bind data into a std vector
      storedVertIndexArray.push_back(bindVertexArray);

      MIntArray bindPolyArray;
      // Get the stored bind data
      hInputArray = testHandle.child( aBindPolyIDArray);
      oInputArray = hInputArray.data();
      MFnIntArrayData dataPolyIntArrayFn(oInputArray);
      dataPolyIntArrayFn.copyTo(bindPolyArray);
      // Put the stored bind data into a std vector
      storedPolyIndexArray.push_back(bindPolyArray);

      MIntArray bindTriangleArray;
      // Get the stored bind data
      hInputArray = testHandle.child( aBindTriangleIDArray);
      oInputArray = hInputArray.data();
      MFnIntArrayData dataTriangleIntArrayFn(oInputArray);
      dataTriangleIntArrayFn.copyTo(bindTriangleArray);
      // Put the stored bind data into a std vector
      storedTriangleIndexArray.push_back(bindTriangleArray);

      MPointArray tmpBaryCoordsArray;
      // Get the stored bind data
      hInputArray = testHandle.child( aBaryCoordsArray);
      oInputArray = hInputArray.data();
      MFnPointArrayData dataBaryCoordsArrayFn(oInputArray);
      dataBaryCoordsArrayFn.copyTo(tmpBaryCoordsArray);
      // Put the stored bind data into a std vector
      storedBaryCoordsArray.push_back(tmpBaryCoordsArray);

      MMatrixArray tmpBindMatrixArray;
      // Get the stored bind data
      hInputArray = testHandle.child( aBindMatrixArray);
      oInputArray = hInputArray.data();
      MFnMatrixArrayData dataBindMatrixArrayFn(oInputArray);
      dataBindMatrixArrayFn.copyTo(tmpBindMatrixArray);
      // Put the stored bind data into a std vector
      storedBindMatrixArray.push_back(tmpBindMatrixArray);

      MPointArray tmpBindPointsArray;
      // Get the stored bind data
      hInputArray = testHandle.child( aBindPointsArray);
      oInputArray = hInputArray.data();
      MFnPointArrayData dataBindPointArrayFn(oInputArray);
      dataBindPointArrayFn.copyTo(tmpBindPointsArray);
      // Put the stored bind data into a std vector
      storedBindPointsArray.push_back(tmpBindPointsArray);

      std::vector <MIntArray> tempTriangleVertIDArray;

      MArrayDataHandle inputVertexArray(inputsArrayHandle.inputValue().child( aTriangleVertArray));
      int triangleCount = inputVertexArray.elementCount(&status);
      CHECK_MSTATUS_AND_RETURN_IT( status);
      
      MObject oOutputTriangleVertArray;
      MIntArray triangleIDs(3);
      
      for (int vertID = 0; vertID < triangleCount; vertID++)
      {
        status = inputVertexArray.jumpToElement(vertID);
        CHECK_MSTATUS_AND_RETURN_IT( status);
        
        int3& something = inputVertexArray.inputValue().asInt3();
        triangleIDs[0] = something[0];
        triangleIDs[1] = something[1];
        triangleIDs[2] = something[2];
        // MGlobal::displayInfo(MString("THIS IS WORKING ") + something[0] + " " + something[1] + " " + something[2] );
        tempTriangleVertIDArray.push_back(triangleIDs);
        
      }

      storedTriangleVertIDArray.push_back(tempTriangleVertIDArray);

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