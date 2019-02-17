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
MObject LHMultiWrap::aAmount;
MObject LHMultiWrap::aCacheClosest;
MObject LHMultiWrap::aInputGeo;
MObject LHMultiWrap::aInputParent;
MObject LHMultiWrap::aBaseMesh;

MStatus LHMultiWrap::initialize() {
  MFnNumericAttribute nAttr;
  MFnCompoundAttribute cAttr;
  MFnTypedAttribute tAttr;
  aAmount = nAttr.create("bindThreshold", "bindthreshold", MFnNumericData::kFloat);
  nAttr.setMin(0.0);
  nAttr.setDefault(0.0);
  nAttr.setKeyable(true);
  addAttribute(aAmount);
  attributeAffects(aAmount, outputGeom);

  aCacheClosest = nAttr.create("cacheClosestPoint", "cacheclosest", MFnNumericData::kInt);
  nAttr.setKeyable(false);
  nAttr.setMax(1);
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

MStatus LHMultiWrap::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;

  float env = data.inputValue(envelope).asFloat();
  if (!env)
  {
    return MS::kSuccess;
  }
  float thresholdAmt = data.inputValue(aAmount).asFloat();
  int cache = data.inputValue(aCacheClosest).asInt();
  MObject oBaseMesh = data.inputValue(LHMultiWrap::aBaseMesh).asMeshTransformed();
  if (oBaseMesh.isNull())
  {
      MGlobal::displayError(MString("Unable to get baseMesh, baseMesh should be duplicate of deformed mesh"));
      return MS::kFailure;
  }

  MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHMultiWrap::aInputParent, &status));
  CHECK_MSTATUS_AND_RETURN_IT( status);
  int inputCount = inputsArrayHandle.elementCount(&status);
  CHECK_MSTATUS_AND_RETURN_IT( status);
  MObjectArray oColMeshArray;
  MObject oTestMesh;
  for (int i=0;i < inputCount; i++){
      status = inputsArrayHandle.jumpToElement(i);
      oTestMesh =inputsArrayHandle.inputValue().child( LHMultiWrap::aInputGeo).asMeshTransformed();
      if (oTestMesh.isNull()){
    	  continue;
      }
      oColMeshArray.append(oTestMesh);
  }
  if (!oColMeshArray.length())
  {
    MGlobal::displayError(MString("Couldn't get any driver meshes, connect to inputGeo"));
    return MS::kFailure;
  }

  // Make sure base mesh and input geo are the same number of points, return if not
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
  for (int i=0;i < oColMeshArray.length(); i++){
      inputFnMeshArray.push_back(new MFnMesh(oColMeshArray[i]));
  }


  MPoint closestPointDummy;
  int polyID;
  MIntArray polyPointIds;
  MPoint currentPoint;
  MPoint baseCurrentPoint;
  MMeshIsectAccelParams mmAccelParams = fnBaseMesh->autoUniformGridParams();

  // Closest point cache
  if (!cache || !vertIndexArray.size() || vertIndexArray.size() != oColMeshArray.length())
  {
    if (vertIndexArray.size())
    {
      vertIndexArray.clear();
    }
    for (int inputMeshID = 0; inputMeshID < inputFnMeshArray.size(); inputMeshID++)
    {
      MIntArray tempVertIdxArray;
      for (int vertID = 0; vertID < vertCount; vertID++)
      {
        // inputFnMeshArray[inputMeshID]->getPoint(vertID, currentPoint);
        fnBaseMesh->getPoint(vertID, currentPoint);
        inputFnMeshArray[inputMeshID]->getClosestPoint(currentPoint, closestPointDummy, MSpace::kWorld, &polyID, &mmAccelParams);
        inputFnMeshArray[inputMeshID]->getPolygonVertices(polyID, polyPointIds);
        int closestIdx = -1;
        for (int polyPointID = 0; polyPointID < polyPointIds.length(); polyPointID++)
        {
          inputFnMeshArray[inputMeshID]->getPoint(polyPointIds[polyPointID], baseCurrentPoint);
          if (currentPoint.distanceTo(baseCurrentPoint) <= thresholdAmt)
          {
            closestIdx = polyPointIds[polyPointID];
            //MGlobal::displayInfo(MString("Closest ") + polyPointIds[polyPointID] + " " + currentPoint.distanceTo(baseCurrentPoint));
            break;
          }
        }
        //MGlobal::displayInfo(MString("Closest ") + closestIdx + " " + vertID + " " + currentPoint.distanceTo(baseCurrentPoint));

        tempVertIdxArray.append(closestIdx);
      }
      vertIndexArray.push_back(tempVertIdxArray);
    }
  }
  // // Closest point cache
  // if (!cache || !vertIndexArray.size() || vertIndexArray.size() != oColMeshArray.length())
  // {
  //   if (vertIndexArray.size())
  //   {
  //     vertIndexArray.clear();
  //   }
  //   for (int inputMeshID = 0; inputMeshID < inputFnMeshArray.size(); inputMeshID++)
  //   {
  //     MIntArray tempVertIdxArray;
  //     for (int vertID = 0; vertID < vertCount; vertID++)
  //     {
  //       // inputFnMeshArray[inputMeshID]->getPoint(vertID, currentPoint);
  //       inputFnMeshArray[inputMeshID]->getPoint(vertID, currentPoint);
  //       fnBaseMesh->getClosestPoint(currentPoint, closestPointDummy, MSpace::kWorld, &polyID, &mmAccelParams);
  //       fnBaseMesh->getPolygonVertices(polyID, polyPointIds);
  //       int closestIdx = -1;
  //       for (int polyPointID = 0; polyPointID < polyPointIds.length(); polyPointID++)
  //       {
  //         fnBaseMesh->getPoint(polyPointIds[polyPointID], baseCurrentPoint);
  //         if (currentPoint.distanceTo(baseCurrentPoint) <= thresholdAmt)
  //         {
  //           closestIdx = polyPointIds[polyPointID];
  //           //MGlobal::displayInfo(MString("Closest ") + polyPointIds[polyPointID] + " " + currentPoint.distanceTo(baseCurrentPoint));
  //           break;
  //         }
  //       }
  //       MGlobal::displayInfo(MString("Closest ") + closestIdx + " " + vertID + " " + currentPoint.distanceTo(baseCurrentPoint));

  //       tempVertIdxArray.append(closestIdx);
  //     }
  //     vertIndexArray.push_back(tempVertIdxArray);
  //   }
  // }

  //  thresholdAmt *= env;
  MPointArray accumulatedVectors;
  MPoint pt;
  MPoint toPoint;
  MPoint fromPoint;
  //float w = 0.0f;
  //MPointArray allPoints;
  MVector direction(1.0, 0.0, 0.0);

  for (; !itGeo.isDone(); itGeo.next()) {
    // Get the input geometry point
    // Get the painted weight value
//    w = weightValue(data, mIndex, itGeo.index());
    // Just translate in x
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
  //itGeo.setAllPositions(allPoints);
  return MS::kSuccess;
}

