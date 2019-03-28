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

#include "LHCurveRollSimple.h"

MTypeId LHCurveRollSimple::id(0x06760267);
MObject LHCurveRollSimple::aRollAmount;
MObject LHCurveRollSimple::aVAmount;
MObject LHCurveRollSimple::aRotationAmount;

MObject LHCurveRollSimple::aBaseGeo;
MObject LHCurveRollSimple::aBaseGeoParent;

MObject LHCurveRollSimple::aSurface;
MObject LHCurveRollSimple::aSurfaceBase;

MObject LHCurveRollSimple::aRollCurve;

MObject LHCurveRollSimple::aCacheBind;

MObject LHCurveRollSimple::aRollWeights;
MObject LHCurveRollSimple::aVWeights;
MObject LHCurveRollSimple::aMembershipWeight;
MObject LHCurveRollSimple::aWeightArray;

MStatus LHCurveRollSimple::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnGenericAttribute gAttr;


    aRollAmount = nAttr.create("rollAmount", "rollamount", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    addAttribute(aRollAmount);
    attributeAffects(aRollAmount, outputGeom);

    aVAmount = nAttr.create("vAmount", "vamnt", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    addAttribute(aVAmount);
    attributeAffects(aVAmount, outputGeom);

    aRotationAmount = nAttr.create("rotationAmount", "ramnt", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    addAttribute(aRotationAmount);
    attributeAffects(aRotationAmount, outputGeom);

    aCacheBind = nAttr.create("cacheBind", "cbind", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setChannelBox(true);
    nAttr.setDefault(0);
    nAttr.setMin(0);
    nAttr.setMax(1);
    addAttribute(aCacheBind);
    attributeAffects(aCacheBind, outputGeom);


    aBaseGeo = gAttr.create("baseGeo", "bGeo");
    gAttr.addAccept(MFnData::kMesh);
    gAttr.addAccept(MFnData::kNurbsSurface);
    gAttr.addAccept(MFnData::kNurbsCurve);
    gAttr.addAccept(MFnData::kLattice);

    aRollWeights = tAttr.create("rollWeights", "rollweights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRollWeights);
    attributeAffects(aRollWeights, outputGeom);

    aMembershipWeight = tAttr.create("membershipWeight", "mw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aMembershipWeight);
    attributeAffects(aMembershipWeight, outputGeom);

    aWeightArray = cAttr.create("weightArrays", "warray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aBaseGeo );
    cAttr.addChild( aRollWeights );
    // cAttr.addChild( aVWeights );
    cAttr.addChild( aMembershipWeight );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aWeightArray);
    attributeAffects(aWeightArray, outputGeom);


    aRollCurve = tAttr.create("rollCurve", "rollcurve", MFnData::kNurbsCurve);
    addAttribute(aRollCurve);
    attributeAffects(aRollCurve, outputGeom);

    // surface
    aSurface = tAttr.create("surface", "s", MFnData::kNurbsSurface);
    addAttribute(aSurface);
    attributeAffects(aSurface, outputGeom);
    // base
    aSurfaceBase = tAttr.create("surfaceBase", "sb", MFnData::kNurbsSurface);
    addAttribute(aSurfaceBase);
    attributeAffects(aSurfaceBase, outputGeom);

    return MS::kSuccess;
}

void *LHCurveRollSimple::creator() { return new LHCurveRollSimple; }


MStatus LHCurveRollSimple::deform(MDataBlock &data, MItGeometry &itGeo,
                              const MMatrix &localToWorldMatrix, unsigned int mIndex)
{
  MStatus status;

  float env = data.inputValue(envelope).asFloat();
  float rollAmount = data.inputValue(aRollAmount).asFloat();
  env = env * rollAmount;
  if (!env)
  {
    return MS::kSuccess;
  }


  // float vAmount = data.inputValue(aVAmount).asFloat();
  float rotationAmount = data.inputValue(aRotationAmount).asFloat();
  int cacheBind = data.inputValue(aCacheBind).asInt();

  oCurve = data.inputValue(aRollCurve).asNurbsCurveTransformed();
  if (oCurve.isNull())
  {
      MGlobal::displayError(MString("Couldn't get curve, check connections"));
      return MS::kFailure;
  }
  fnCurve = new MFnNurbsCurve(oCurve);

  if (!cacheBind || !deformedVertIds.size() || deformedVertIds.size()-1 < mIndex ||  !deformedVertIds[mIndex].length())
  {
    // MGlobal::displayInfo(MString("NOT CACHING"));
    status =  GetAllBaseGeoIter(data);
    CheckStatusReturn( status, "Couldn't get base Geometry" );
    status = LHCurveRollSimple::CacheDeformPointMembership(data);
    CheckStatusReturn( status, "Couldn't get membership weights" );
  }

  if (!deformedVertIds.size() || deformedVertIds.size()-1 < mIndex ||  !deformedVertIds[mIndex].length())
  {
      // MGlobal::displayInfo(MString("NOT CACHING"));
      MGlobal::displayError(MString("Weight missmatch, make sure you have the same number of weights as inputGeometry"));
      return MS::kFailure;
  }

  if (!cacheBind || !slideUParam.size() || slideUParam.size()-1 < mIndex ||  !slideUParam[mIndex].length())
  {
    // MGlobal::displayInfo(MString("NOT CACHING"));
    status = LHCurveRollSimple::CacheClosestPoints();
    CheckStatusReturn( status, "Couldn't cache closest points" );
  }

  // if (!cacheBind || !baseEuler.size() || baseEuler.size()-1 < mIndex ||  !baseEuler[mIndex].size() || baseEuler[mIndex].size() != deformedVertIds[mIndex].length())
  // {
  //   status = LHCurveRollSimple::CacheBaseRotations();
  //   CheckStatusReturn( status, "Couldn't cache base rotations" );
  // }

  status =  LHCurveRollSimple::getWeights(data, mIndex, rollWeights, aRollWeights);
  CheckStatusReturn( status, "Couldn't get rollWeights" );


  // MPoint pt;
  //float w = 0.0f;
  MPointArray allPoints;
  itGeo.allPositions(allPoints);
  double degree;
  // // MVector direction(1.0, 0.0, 0.0);
  // MGlobal::displayInfo(MString("DeformedVerts  !!!!! ") + deformedVertIds[mIndex].length());
  // MGlobal::displayInfo(MString("DeformedVerts  !!!!! ")+ deformedVertIds[mIndex].length());
  // MGlobal::displayInfo(MString("TANGENT ARRAY  !!!!! ")+ closestTangentArray[mIndex].length());
  // MGlobal::displayInfo(MString("TANGENT ARRAY  !!!!! ")+ closestTangentArray[mIndex].length());
  // MGlobal::displayInfo(MString("rollWeights  !!!!! ")+ rollWeights.length());
  // MGlobal::displayInfo(MString("rollWeights  !!!!! ")+ rollWeights.length());
  // MGlobal::displayInfo(MString("rollWeights  !!!!! ")+ rollWeights.length());


//   MVector direction(1.0, 0.0, 0.0);
//   for (int idx=0;idx < deformedVertIds[mIndex].length(); idx++)
//   {
//     int currentVertID = deformedVertIds[mIndex][idx];
//     //  allPoints[deformedVertIds[mIndex][x]] = allPoints[deformedVertIds[mIndex][x]] + (direction * uAmount);
//     // LHSlideSimple::Algorithm(mIndex, x, uWeights, vWeights, deformedVertIds[mIndex][x], allPoints[deformedVertIds[mIndex][x]], uAmount);
// //     void LHSlideSimple::Algorithm(int mIndex, int idx, MDoubleArray uWeights, MDoubleArray vWeights, int currentVertID, MPoint &pt, float uAmount)
// // {
//         MPoint slideUVBasePoint = closestPointArray[mIndex][idx];


  MVector direction(1.0, 0.0, 0.0);
  float tmpEnv;
  int currentVertID;
  MMatrix rotateMatrix;
  for (int idx=0;idx < deformedVertIds[mIndex].length(); idx++)
  {
    int currentVertID = deformedVertIds[mIndex][idx];

    tmpEnv = env * rollWeights[currentVertID];
    degree = (tmpEnv * (3.14159265/180.0 ));
    // //Compose rotation
    MQuaternion tmpRotate(degree,closestTangentArray[mIndex][idx]);
    rotateMatrix = tmpRotate.asMatrix();

    allPoints[currentVertID] = allPoints[currentVertID] - closestPointArray[mIndex][idx];
    // do rotation, then put pts back
    allPoints[currentVertID] = ( allPoints[currentVertID] * rotateMatrix )  + closestPointArray[mIndex][idx];
  

  }
  itGeo.setAllPositions(allPoints);
  return MS::kSuccess;
}

MStatus LHCurveRollSimple::GetAllBaseGeoIter(MDataBlock &data)
{
    MStatus status;
    if (allGeoIter.size())
    {
      allGeoIter.clear();
    }
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHCurveRollSimple::aWeightArray, &status));
    CheckStatusReturn( status, "Unable to get inputs" );
    int inputCount = inputsArrayHandle.elementCount(&status);
    CheckStatusReturn( status, "Unable to get number of inputs" );
    for (int i=0;i < inputCount; i++)
    {
      status = inputsArrayHandle.jumpToElement(i);
      CheckStatusReturn( status, "Couldn't jump to geo index" );
      MDataHandle hInput =inputsArrayHandle.inputValue(&status);
      CheckStatusReturn( status, "Couldn't get inputHandle" );
      MDataHandle hBaseMesh =hInput.child( aBaseGeo );
      bool isNumeric;
      bool isNull;
      hBaseMesh.isGeneric( isNumeric, isNull );
      if (isNull)
      {
        CheckStatusReturn( MS::kFailure, "couldn't get base mesh at this MIndex" );
      }
      MItGeometry* baseIter = new MItGeometry(hBaseMesh, true, &status);
      CheckStatusReturn( status, "Couldn't get baseMesh" );
      allGeoIter.push_back(baseIter);
    }
    return MS::kSuccess;
}

void LHCurveRollSimple::ClearCachedData()
{
  if (slideUParam.size())
  {
    slideUParam.clear();
  }
  if (slideVParam.size())
  {
    slideVParam.clear();
  }
  if (closestPointArray.size())
  {
    closestPointArray.clear();
  }
  if (closestTangentArray.size())
  {
    closestTangentArray.clear();
  }

}



MStatus LHCurveRollSimple::CacheClosestPoints()
{  
  LHCurveRollSimple::ClearCachedData();
  // fnSurfaceBase->getKnotDomain(uMinParam,uMaxParam,vMinParam,vMaxParam);
  // MNurbsIntersector fnBaseIntersector;
  // fnBaseIntersector.create(oSurfaceBase);
  if (!allGeoIter.size())
  {
    return MS::kFailure;
  }
  for (int x=0;x < allGeoIter.size(); x++)
  {
    if (!deformedVertIds.size() || deformedVertIds.size()-1 < x || !deformedVertIds[x].length())
    {
      return MS::kFailure;
    }
    allGeoIter[x]->allPositions(currentGeoPoints);
    // MDoubleArray tempSlideUParam, tempSlideVParam;
    MVectorArray tempClosestTangent;
    MPointArray tempClosestPointArray;
    for (int i=0;i < deformedVertIds[x].length(); i++)
    {
        currentPt = currentGeoPoints[deformedVertIds[x][i]];
        tempClosestPointArray.append(fnCurve->closestPoint( currentPt, &closestParam, 0.00001, MSpace::kObject));
        tempClosestTangent.append(fnCurve->tangent(closestParam, MSpace::kObject));
    //   currentPt = currentGeoPoints[deformedVertIds[x][i]];
    //   fnBaseIntersector.getClosestPoint(currentPt, ptON);
    //   tempClosestPointArray.append(ptON.getPoint());
    //   UV = ptON.getUV();
    //   tempSlideUParam.append(UV.x);
    //   tempSlideVParam.append(UV.y);
    }
    closestPointArray.push_back(tempClosestPointArray);
    closestTangentArray.push_back(tempClosestTangent);
    // slideUParam.push_back(tempSlideUParam);
    // slideVParam.push_back(tempSlideVParam);
  }
  return MS::kSuccess;
}














MStatus LHCurveRollSimple::CacheDeformPointMembership(MDataBlock &data)
{
    MStatus status;
    if (deformedVertIds.size())
    {
      deformedVertIds.clear();
    }
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHCurveRollSimple::aWeightArray, &status));
    CheckStatusReturn( status, "Unable to get inputs" );
    int inputCount = inputsArrayHandle.elementCount(&status);
    CheckStatusReturn( status, "Unable to get number of inputs" );
    for (int i=0;i < inputCount; i++)
    {
      MIntArray tempMembershipIdx;
      inputsArrayHandle.jumpToElement(i);
      MDataHandle handle(inputsArrayHandle.inputValue(&status) );
      CheckStatusReturn( status, "Couldn't get array handle" );
      MDataHandle weightChild(handle.child( aMembershipWeight) );
      MDoubleArray dAWeights = MFnDoubleArrayData(weightChild.data()).array(&status);
      CheckStatusReturn( status, "Couldn't get Weights" );
      if (allGeoIter[i]->count() != dAWeights.length())
      {
          MGlobal::displayError(MString("Weights Don't exist!!"));
        return MS::kFailure;
      }
      for (int x=0;x < dAWeights.length(); x++)
      {
        if (dAWeights[x] > 0.0)
        {
          tempMembershipIdx.append(x);
        }
      }
      deformedVertIds.push_back(tempMembershipIdx);
    }
    return MS::kSuccess;
}

MStatus LHCurveRollSimple::getWeights(MDataBlock &data, int mIndex, MDoubleArray &rDoubleArray, MObject weightObject)
{
    MStatus status;
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHCurveRollSimple::aWeightArray, &status));
    CheckStatusReturn( status, "Unable to get inputs" );
    int inputCount = inputsArrayHandle.elementCount(&status);
    CheckStatusReturn( status, "Unable to get number of inputs" );
    if (inputCount >= mIndex)
    {
      status = inputsArrayHandle.jumpToElement(mIndex);
      CheckStatusReturn( status, "Couldn't jump to element" );
      MDataHandle handle(inputsArrayHandle.inputValue(&status) );
      CheckStatusReturn( status, "Couldn't get array handle" );
      MDataHandle weightChild(handle.child( weightObject) );
      rDoubleArray = MFnDoubleArrayData(weightChild.data()).array(&status);
      CheckStatusReturn( status, "Couldn't get Weights" );
      return MS::kSuccess;
    }
    return MS::kFailure;
}
