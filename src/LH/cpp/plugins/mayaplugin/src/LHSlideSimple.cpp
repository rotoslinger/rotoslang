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

#include "LHSlideSimple.h"

MTypeId LHSlideSimple::id(0x09435467);
MObject LHSlideSimple::aUAmount;
MObject LHSlideSimple::aVAmount;
MObject LHSlideSimple::aRotationAmount;

MObject LHSlideSimple::aBaseGeo;
MObject LHSlideSimple::aBaseGeoParent;

MObject LHSlideSimple::aSurface;
MObject LHSlideSimple::aSurfaceBase;

MObject LHSlideSimple::aCacheBind;

// MObject LHSlideSimple::aUValue;
// MObject LHSlideSimple::aVValue;

MObject LHSlideSimple::aUWeights;
MObject LHSlideSimple::aVWeights;
MObject LHSlideSimple::aMembershipWeight;
MObject LHSlideSimple::aWeightArray;

MStatus LHSlideSimple::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnGenericAttribute gAttr;


    aUAmount = nAttr.create("uAmount", "uamnt", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    addAttribute(aUAmount);
    attributeAffects(aUAmount, outputGeom);

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

    aUWeights = tAttr.create("uWeights", "uw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUWeights);
    // attributeAffects(aUWeights, outputGeom);


    aVWeights = tAttr.create("vWeights", "vw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVWeights);
    // attributeAffects(aVWeights, outputGeom);

    aMembershipWeight = tAttr.create("membershipWeight", "mw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aMembershipWeight);
    // attributeAffects(aMembershipWeight, outputGeom);

    aWeightArray = cAttr.create("weightArrays", "warray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aBaseGeo );
    cAttr.addChild( aUWeights );
    cAttr.addChild( aVWeights );
    cAttr.addChild( aMembershipWeight );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aWeightArray);
    attributeAffects(aWeightArray, outputGeom);

    // surface
    aSurface = tAttr.create("surface", "s", MFnData::kNurbsSurface);
    addAttribute(aSurface);
    attributeAffects(aSurface, outputGeom);
    // base
    aSurfaceBase = tAttr.create("surfaceBase", "sb", MFnData::kNurbsSurface);
    addAttribute(aSurfaceBase);
    attributeAffects(aSurfaceBase, outputGeom);

    // Make the deformer weights paintable
    //MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer LHSlideSimple weights;");
    MGlobal::executeCommand("makePaintable -attrType doubleArray -sm deformer LHSlideSimple membershipWeight;");
    MGlobal::executeCommand("makePaintable -attrType doubleArray -sm deformer LHSlideSimple uWeights;");
    MGlobal::executeCommand("makePaintable -attrType doubleArray -sm deformer LHSlideSimple vWeights;");

    return MS::kSuccess;
}

void *LHSlideSimple::creator() { return new LHSlideSimple; }


MStatus LHSlideSimple::deform(MDataBlock &data, MItGeometry &itGeo,
                              const MMatrix &localToWorldMatrix, unsigned int mIndex)
{
  MStatus status;

  //  float env = data.inputValue(envelope).asFloat();
  float uAmount = data.inputValue(aUAmount).asFloat();
  float vAmount = data.inputValue(aVAmount).asFloat();
  float rotationAmount = data.inputValue(aRotationAmount).asFloat();
  int cacheBind = data.inputValue(aCacheBind).asInt();
  oSurface = data.inputValue(aSurface).asNurbsSurfaceTransformed();
  oSurfaceBase = data.inputValue(aSurfaceBase).asNurbsSurfaceTransformed();
  if (oSurface.isNull() || oSurfaceBase.isNull())
  {
      MGlobal::displayError(MString("Couldn't get surface, check connections"));
      return MS::kFailure;
  }
  fnSurface = new MFnNurbsSurface(oSurface);
  fnSurfaceBase = new MFnNurbsSurface(oSurfaceBase);

  if (!cacheBind || !deformedVertIds.size() || deformedVertIds.size() < mIndex ||  !deformedVertIds[mIndex].length())
  {
    MGlobal::displayInfo(MString("NOT CACHING"));
    status =  GetAllBaseGeoIter(data);
    CheckStatusReturn( status, "Couldn't get base Geometry" );
    LHSlideSimple::CacheDeformPointMembership(data);
  }

  if (!deformedVertIds.size() || deformedVertIds.size() < mIndex ||  !deformedVertIds[mIndex].length())
  {
    MGlobal::displayInfo(MString("NOT CACHING"));
      MGlobal::displayError(MString("Weight missmatch, make sure you have the same number of weights as inputGeometry"));
      return MS::kFailure;
  }

  if (!cacheBind || !slideUParam.size() || slideUParam.size() < mIndex ||  !slideUParam[mIndex].length())
  {
    MGlobal::displayInfo(MString("NOT CACHING"));
    LHSlideSimple::CacheClosestPoints();
  }

  if (!cacheBind || !baseEuler.size() || baseEuler.size() < mIndex ||  !baseEuler[mIndex].size() || baseEuler[mIndex].size() != deformedVertIds[mIndex].length())
  {
    MGlobal::displayInfo(MString("NOT CACHING"));
    LHSlideSimple::CacheBaseRotations();
  }
// getWeights(MDataBlock &data, int mIndex, MDoubleArray &rDoubleArray, MObject weightObject)
  status =  LHSlideSimple::getWeights(data, mIndex, uWeights, aUWeights);
  CheckStatusReturn( status, "Couldn't get uWeights" );
  status =  LHSlideSimple::getWeights(data, mIndex, vWeights, aVWeights);
  CheckStatusReturn( status, "Couldn't get vWeights" );


  // MPoint pt;
  //float w = 0.0f;
  MPointArray allPoints;
  itGeo.allPositions(allPoints);
  MVector direction(1.0, 0.0, 0.0);
  for (int idx=0;idx < deformedVertIds[mIndex].length(); idx++)
  {
    int currentVertID = deformedVertIds[mIndex][idx];
    //  allPoints[deformedVertIds[mIndex][x]] = allPoints[deformedVertIds[mIndex][x]] + (direction * uAmount);
    // LHSlideSimple::Algorithm(mIndex, x, uWeights, vWeights, deformedVertIds[mIndex][x], allPoints[deformedVertIds[mIndex][x]], uAmount);
//     void LHSlideSimple::Algorithm(int mIndex, int idx, MDoubleArray uWeights, MDoubleArray vWeights, int currentVertID, MPoint &pt, float uAmount)
// {
        MPoint slideUVBasePoint = closestPointArray[mIndex][idx];
        //curveBasePtParam
        double slideUBasePointParam = slideUParam[mIndex][idx];
        double slideVBasePointParam = slideVParam[mIndex][idx];

        // get min&&max parameter
        // MGlobal::displayInfo(MString("WEIGHTS!!!") + uWeights[currentVertID]);
        double unclampedUValue = slideUBasePointParam + uWeights[currentVertID];
        // double unclampedUValue = slideUBasePointParam + uWeights[currentVertID]* vAmount;
        double clampedUValue = std::max(uMinParam, std::min(unclampedUValue, uMaxParam));

        // double unclampedVValue = slideVBasePointParam + vWeights[currentVertID] * uAmount;
        double unclampedVValue = slideVBasePointParam + vWeights[currentVertID];
        double clampedVValue = std::max(vMinParam, std::min(unclampedVValue, vMaxParam));
        fnSurface->getDerivativesAtParm( clampedUValue,
                                        clampedVValue,
                                        slideUVPoint, fnUVec, fnVVec,
                                        MSpace::kObject);
        // U Min
        if (unclampedUValue <= uMinParam)
        {
            slideUVec = fnUVec;
            slideUVPoint -= -slideUVec * unclampedUValue;
        }
        // U Max
        else if (unclampedUValue >= uMaxParam)
        {
            slideUVec = fnUVec;
            unclampedUValue = unclampedUValue -1;
            slideUVPoint -= -slideUVec * unclampedUValue;
        }
        // V Min
        if (unclampedVValue <= vMinParam)
        {
          slideVVec = fnVVec;
          slideUVPoint -= -slideVVec * unclampedVValue;
        }
        // V Max
        else if (unclampedVValue >= vMaxParam)
        {
            slideVVec = fnVVec;
            unclampedVValue = unclampedVValue -1;
            slideUVPoint -= -slideVVec * unclampedVValue;
        }

        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        ////////////////////////// Slide Ends //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // float rotationAmount = 0.0;
        if (rotationAmount != 0)
        {
            fnSurface->getTangents( clampedUValue, clampedVValue, xVec, yVec, MSpace::kObject );
            normal = fnSurface->normal( clampedUValue, clampedVValue, MSpace::kObject );
            yVec.normalize();
            zVec = normal;
            zVec.normalize();
            xVec = yVec ^ zVec;
            xVec.normalize();
            rotateEuler = baseEuler[mIndex][idx];
            // apply rotate offset dereference address pointer rotateMatrix with *
            MQuaternion rotateX(-(rotateEuler[0]),xVec);
            rotateMatrixX = rotateX.asMatrix();
            yVec = yVec * rotateMatrixX;
            zVec = zVec * rotateMatrixX;

            MQuaternion rotateY(-(rotateEuler[1]),yVec);
            rotateMatrixY = rotateY.asMatrix();
            xVec = xVec * rotateMatrixY;
            zVec = zVec * rotateMatrixY;

            MQuaternion rotateZ(-(rotateEuler[2]),zVec);
            rotateMatrixZ = rotateZ.asMatrix();
            xVec = xVec * rotateMatrixZ;
            yVec = yVec * rotateMatrixZ;

            double driveMatrix[4][4]={{ xVec[0], xVec[1], xVec[2], 0.0},
                          { yVec[0], yVec[1], yVec[2], 0.0},
                          { zVec[0], zVec[1], zVec[2], 0.0},
                          {         0.0,         0.0,         0.0, 1.0},};

            MMatrix DriveMatrix(driveMatrix);

            // find the rotation offset, then apply later
            MEulerRotation DriveMatrixEuler;
            DriveMatrixEuler = DriveMatrixEuler.decompose(DriveMatrix,
                                                          MEulerRotation::kXYZ);
            // apply rotation uAmount
            DriveMatrixEuler = MEulerRotation( DriveMatrixEuler[0] * rotationAmount,
                                               DriveMatrixEuler[1] * rotationAmount,
                                               DriveMatrixEuler[2] * rotationAmount);
            DriveMatrix = DriveMatrixEuler.asMatrix();
            // finalMatrix = DriveMatrix;



            
            ////// ApplyRotation uAmount
            MVector toCenterBase(-slideUVBasePoint.x,
                                 -slideUVBasePoint.y,
                                 -slideUVBasePoint.z);
            allPoints[currentVertID] = allPoints[currentVertID] + toCenterBase;

            // do rotationAmount, then put pts back
            allPoints[currentVertID] = ( allPoints[currentVertID] * DriveMatrix ) - toCenterBase;
        }

        ////// apply slide
        allPoints[currentVertID].x +=(slideUVPoint.x - slideUVBasePoint.x);
        allPoints[currentVertID].y +=(slideUVPoint.y - slideUVBasePoint.y);
        allPoints[currentVertID].z +=(slideUVPoint.z - slideUVBasePoint.z);
  }
  itGeo.setAllPositions(allPoints);
  return MS::kSuccess;
}


// void LHSlideSimple::Algorithm(int mIndex, int idx, MDoubleArray uWeights, MDoubleArray vWeights, int currentVertID, MPoint &pt, float uAmount)
// {
//         MPoint slideUVBasePoint = closestPointArray[mIndex][idx];
//         //curveBasePtParam
//         double slideUBasePointParam = slideUParam[mIndex][idx];
//         double slideVBasePointParam = slideVParam[mIndex][idx];

//         // get min&&max parameter

//         double unclampedUValue = slideUBasePointParam + uWeights[currentVertID]* 0;
//         double clampedUValue = std::max(uMinParam, std::min(unclampedUValue, uMaxParam));

//         double unclampedVValue = slideVBasePointParam + vWeights[currentVertID] * uAmount;
//         double clampedVValue = std::max(vMinParam, std::min(unclampedVValue, vMaxParam));
//         fnSurface->getDerivativesAtParm( clampedUValue,
//                                         clampedVValue,
//                                         slideUVPoint, fnUVec, fnVVec,
//                                         MSpace::kObject);
//         // U Min
//         if (unclampedUValue <= uMinParam)
//         {
//             slideUVec = fnUVec;
//             slideUVPoint -= -slideUVec * unclampedUValue;
//         }
//         // U Max
//         else if (unclampedUValue >= uMaxParam)
//         {
//             slideUVec = fnUVec;
//             unclampedUValue = unclampedUValue -1;
//             slideUVPoint -= -slideUVec * unclampedUValue;
//         }
//         // V Min
//         if (unclampedVValue <= vMinParam)
//         {
//           slideVVec = fnVVec;
//           slideUVPoint -= -slideVVec * unclampedVValue;
//         }
//         // V Max
//         else if (unclampedVValue >= vMaxParam)
//         {
//             slideVVec = fnVVec;
//             unclampedVValue = unclampedVValue -1;
//             slideUVPoint -= -slideVVec * unclampedVValue;
//         }

//         ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//         ////////////////////////// Slide Ends //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//         ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//         //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//         float rotationAmount = 0.0;
//         if (rotationAmount != 0)
//         {
//             fnSurface->getTangents( clampedUValue, clampedVValue, xVec, yVec, MSpace::kObject );
//             normal = fnSurface->normal( clampedUValue, clampedVValue, MSpace::kObject );
//             yVec.normalize();
//             zVec = normal;
//             zVec.normalize();
//             xVec = yVec ^ zVec;
//             xVec.normalize();
//             rotateEuler = baseEuler[mIndex][idx];
//             // apply rotate offset dereference address pointer rotateMatrix with *
//             MQuaternion rotateX(-(rotateEuler[0]),xVec);
//             rotateMatrixX = rotateX.asMatrix();
//             yVec = yVec * rotateMatrixX;
//             zVec = zVec * rotateMatrixX;

//             MQuaternion rotateY(-(rotateEuler[1]),yVec);
//             rotateMatrixY = rotateY.asMatrix();
//             xVec = xVec * rotateMatrixY;
//             zVec = zVec * rotateMatrixY;

//             MQuaternion rotateZ(-(rotateEuler[2]),zVec);
//             rotateMatrixZ = rotateZ.asMatrix();
//             xVec = xVec * rotateMatrixZ;
//             yVec = yVec * rotateMatrixZ;

//             double driveMatrix[4][4]={{ xVec[0], xVec[1], xVec[2], 0.0},
//                           { yVec[0], yVec[1], yVec[2], 0.0},
//                           { zVec[0], zVec[1], zVec[2], 0.0},
//                           {         0.0,         0.0,         0.0, 1.0},};

//             MMatrix DriveMatrix(driveMatrix);

//             // find the rotation offset, then apply later
//             MEulerRotation DriveMatrixEuler;
//             DriveMatrixEuler = DriveMatrixEuler.decompose(DriveMatrix,
//                                                           MEulerRotation::kXYZ);
//             // apply rotation uAmount
//             DriveMatrixEuler = MEulerRotation( DriveMatrixEuler[0] * rotationAmount,
//                                                DriveMatrixEuler[1] * rotationAmount,
//                                                DriveMatrixEuler[2] * rotationAmount);
//             DriveMatrix = DriveMatrixEuler.asMatrix();
//             finalMatrix = DriveMatrix;
//         }

//         if (rotationAmount != 0)
//         {
//             ////// ApplyRotation uAmount
//             MVector toCenterBase(-slideUVBasePoint.x,
//                                  -slideUVBasePoint.y,
//                                  -slideUVBasePoint.z);
//             pt = pt + toCenterBase;

//             // do rotationAmount, then put pts back
//             pt = ( pt * finalMatrix ) - toCenterBase;
//         }

//         ////// apply slide
//         pt.x +=(slideUVPoint.x - slideUVBasePoint.x);
//         pt.y +=(slideUVPoint.y - slideUVBasePoint.y);
//         pt.z +=(slideUVPoint.z - slideUVBasePoint.z);


// }

MStatus LHSlideSimple::CacheBaseRotations()
{
    MStatus status;
    if (baseEuler.size())
    {
      baseEuler.clear();
    }
    for (int x=0;x < allGeoIter.size(); x++)
    {
      allGeoIter[x]->allPositions(currentGeoPoints);
      std::vector <  MEulerRotation > tempBaseEuler;
      for (int i=0;i < deformedVertIds[x].length(); i++)
      {
        currentPt = currentGeoPoints[deformedVertIds[x][i]];
        fnSurfaceBase->getTangents( slideUParam[x][i], slideVParam[x][i], xVec, yVec, MSpace::kObject );
        normal = fnSurfaceBase->normal( slideUParam[x][i], slideVParam[x][i], MSpace::kObject );

        yVector = yVec;
        yVector.normalize();

        zVector = normal;
        zVector.normalize();

        xVector = yVector^zVector;
        xVector.normalize();
        double baseMatrix[4][4]={{ xVector[0], xVector[1], xVector[2], 0.0},
                      { yVector[0], yVector[1], yVector[2], 0.0},
                      { zVector[0], zVector[1], zVector[2], 0.0},
                      {         0.0,         0.0,         0.0, 1.0},};
        rotateEuler = rotateEuler.decompose(BaseMatrix, MEulerRotation::kXYZ);
        tempBaseEuler.push_back(rotateEuler);
      }
      baseEuler.push_back(tempBaseEuler);
    }
    return MS::kSuccess;
    }


MStatus LHSlideSimple::GetAllBaseGeoIter(MDataBlock &data)
{
    MStatus status;
    if (allGeoIter.size())
    {
      allGeoIter.clear();
    }
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHSlideSimple::aWeightArray, &status));
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
      MItGeometry* baseIter = new MItGeometry(hBaseMesh, true, &status);
      CheckStatusReturn( status, "Couldn't get baseMesh" );
      allGeoIter.push_back(baseIter);
    }
    return MS::kSuccess;
}

void LHSlideSimple::ClearCachedData()
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
}

MStatus LHSlideSimple::CacheClosestPoints()
{  
  LHSlideSimple::ClearCachedData();
  fnSurfaceBase->getKnotDomain(uMinParam,uMaxParam,vMinParam,vMaxParam);
  MNurbsIntersector fnBaseIntersector;
  fnBaseIntersector.create(oSurfaceBase);
  for (int x=0;x < allGeoIter.size(); x++)
  {
    allGeoIter[x]->allPositions(currentGeoPoints);
    MDoubleArray tempSlideUParam, tempSlideVParam;
    MPointArray tempClosestPointArray;
    for (int i=0;i < deformedVertIds[x].length(); i++)
    {
      currentPt = currentGeoPoints[deformedVertIds[x][i]];
      fnBaseIntersector.getClosestPoint(currentPt, ptON);
      tempClosestPointArray.append(ptON.getPoint());
      UV = ptON.getUV();
      tempSlideUParam.append(UV.x);
      tempSlideVParam.append(UV.y);
    }
    closestPointArray.push_back(tempClosestPointArray);
    slideUParam.push_back(tempSlideUParam);
    slideVParam.push_back(tempSlideVParam);
  }
  return MS::kSuccess;
}

MStatus LHSlideSimple::CacheDeformPointMembership(MDataBlock &data)
{
    MStatus status;
    if (deformedVertIds.size())
    {
      deformedVertIds.clear();
    }
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHSlideSimple::aWeightArray, &status));
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

MStatus LHSlideSimple::getWeights(MDataBlock &data, int mIndex, MDoubleArray &rDoubleArray, MObject weightObject)
{
    MStatus status;
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHSlideSimple::aWeightArray, &status));
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
