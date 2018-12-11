//    float myfloat = fabs(allWeightsArray[0][0][0].length());
//    MGlobal::displayInfo(MString()+myfloat);

#include "LHSlideDeformer.h"

MTypeId LHSlideDeformer::id(0x00008017);

// tAttrs
MObject LHSlideDeformer::aSurface;
MObject LHSlideDeformer::aSurfaceBase;
// nAttrs
MObject LHSlideDeformer::aRotationAmount;
MObject LHSlideDeformer::aScaleAmount;
//////// cache attrs ////////
MObject LHSlideDeformer::aCacheWeights;
MObject LHSlideDeformer::aCacheParams;
MObject LHSlideDeformer::aCacheBase;
//////////////// U ////////////////////////////
//U Values
MObject LHSlideDeformer::aUValue;
MObject LHSlideDeformer::aUValueParent;

// UWeights
MObject LHSlideDeformer::aUWeights;
MObject LHSlideDeformer::aUWeightsParent;
MObject LHSlideDeformer::aUWeightsParentArray;

// UAnimCurves
//UU

//////////////// V ////////////////////////////
//U Values
MObject LHSlideDeformer::aVValue;
MObject LHSlideDeformer::aVValueParent;

// UWeights
MObject LHSlideDeformer::aVWeights;
MObject LHSlideDeformer::aVWeightsParent;
MObject LHSlideDeformer::aVWeightsParentArray;

// UAnimCurves
//UU

//////////////// N ////////////////////////////
//N Values
MObject LHSlideDeformer::aNValue;
MObject LHSlideDeformer::aNValueParent;

// NWeights
MObject LHSlideDeformer::aNWeights;
MObject LHSlideDeformer::aNWeightsParent;
MObject LHSlideDeformer::aNWeightsParentArray;

// NAnimCurves
//NU
//////////////// R ////////////////////////////
//R Values

MObject LHSlideDeformer::aRValue;
MObject LHSlideDeformer::aRValueParent;

// RWeights
MObject LHSlideDeformer::aRWeights;
MObject LHSlideDeformer::aRWeightsParent;
MObject LHSlideDeformer::aRWeightsParentArray;






void* LHSlideDeformer::creator() { return new LHSlideDeformer; }

MStatus LHSlideDeformer::deform(MDataBlock& data, MItGeometry& MitGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
    MObject thisMObj( thisMObject() );
    MStatus status;
    MSyntax syntax;
    // envelope
    float envelope = data.inputValue(MPxDeformerNode::envelope).asFloat();
    if (envelope == 0)
    {
        return MS::kSuccess;
    }

    //make sure num index is equal to the highest index of connected geometry
    //to avoid index scrambling
    MPlug geomPlug( thisMObj, input );
    MIntArray geomIndices;
    geomPlug.getExistingArrayAttributeIndices(geomIndices);
    int len = geomIndices.length();

    //loop to put indices into std vector

    if (indexIntArray.size() > 0)
    {
		indexIntArray.clear();
    }

    for (i= 0; i < len; ++i)
//    for( index = 0; index < indicesLength; ++index)
    {
        indexIntArray.push_back(geomIndices[i]);
    }

    if (len == 1)
       numIndex = geomIndices[0]+1;
    if (len == 2)
       numIndex = std::max(geomIndices[0], geomIndices[1])+1;
    if (len >= 3)
       numIndex = *(std::max_element(indexIntArray.begin(), indexIntArray.end()))+1;



    // get attrs
    float rotationAmount = data.inputValue(aRotationAmount).asFloat();
    float scaleAmount = data.inputValue(aScaleAmount).asFloat();
    // cache attrs
    int cacheWeightsAmt = data.inputValue(aCacheWeights).asInt();
    int cacheParamsAmt = data.inputValue(aCacheParams).asInt();
    int cacheBaseAmt = data.inputValue(aCacheBase).asInt();

    // surfaces
    MObject oSurface = data.inputValue(aSurface).asNurbsSurfaceTransformed();
    MObject oSurfaceBase = data.inputValue(aSurfaceBase).asNurbsSurfaceTransformed();

    if (oSurface.isNull() or oSurfaceBase.isNull())
    {
        return MS::kSuccess;
    }
    //Surface Base
    MFnNurbsSurface fnSurfaceBase( oSurfaceBase );

    // get Surface
    MFnNurbsSurface fnSurface( oSurface );

    //////////////////////////////////////////////////////////////////////////////////////////
    ////////   get all attrVals (can't cache)    ////////
    //////////////////////////////////////////////////////////////////////////////////////////

    MObject allValParents[]={aUValueParent,
                             aVValueParent,
                             aNValueParent};
    MObject allValChildren[]={aUValue,
                              aVValue,
                              aNValue};

    std::vector < std::vector <float> > allValsArray;
    len = sizeof(allValParents);
    for (i= 0; i < 3; ++i)
    {
        MArrayDataHandle arrayHandle(data.inputArrayValue( allValParents[i] ));
        unsigned int count = arrayHandle.elementCount();
//        float myfloat = fabs(count);
//        MGlobal::displayInfo(MString()+myfloat);
        std::vector <float> tmpValArray;

        for (j= 0; j < count; ++j)
        {

            arrayHandle.jumpToElement(j);
            tmpValArray.push_back(arrayHandle.inputValue().child( allValChildren[i] ).asFloat());
        }
        allValsArray.push_back(tmpValArray);

    }
//    if (allValsArray.size() == 4)
//    {
//        float myfloat = fabs(allValsArray[1].size());
//        MGlobal::displayInfo(MString()+myfloat);
//    }


    MArrayDataHandle geomArrayHandle = data.inputArrayValue(geomPlug);

    // cache weight Mesh----
    // only worry about the weight mesh at scene load/mesh connection,
    // or if weight mesh caching is off

	iterGeoCount = MitGeo.count();
////    myfloat = fabs(uW);
//    MGlobal::displayInfo(MString()+iterGeoCount);

    ////////////////////////////////////////////////////////////////////
    //get multiValues and multi weights
    ////////////////////////////////////////////////////////////////////
    // to keep the size of code small,
    // we will put all u,v,n,r values into an array
    // the same for weights
    // indexes are as follows:
    // 0 = u vals/weights
    // 1 = v vals/weights
    // 2 = n vals/weights
    // 3 = r vals/weights


    //////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////   get all weights (cache if specified)      ////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////
//    MPlug weightCheck(thisMObj, aUWeightsParentArray );
//    unsigned int weightSize = weightCheck.numConnectedChildren();

    if (allWeightsArray.size() < numIndex or cacheWeightsAmt == 0)
    {
        MObject allWeightParentArrays[]= {aUWeightsParentArray,
                                          aVWeightsParentArray,
                                          aNWeightsParentArray};
        MObject allWeightParents[] = {aUWeightsParent,
                                      aVWeightsParent,
                                      aNWeightsParent};
        MObject allWeightChildren[] = {aUWeights,
                                       aVWeights,
                                       aNWeights};

        // if they exist, dump old weights
        if (allWeightsArray.size() > 0)
            allWeightsArray.clear();

        for(i = 0; i < numIndex; i++ )
        {
            try
            {
                geomArrayHandle.jumpToElement( i );
                success = 1;
            }
            catch(...)
            {
                success = 0;
            }
            // if you find a connection, get the weights
            if (success == 1)
            {
//              tmpAllWeightsArray = [];
                std::vector < std::vector < MDoubleArray > > tmpAllWeightsArray;
                for(j = 0; j < 3; j++ )
                {
//              for j in range(len(allWeightParentArrays)):
//                  tempWeights = [];
                    std::vector < MDoubleArray > tempWeights;
                    MPlug weightArrayCheck(thisMObj, allWeightParentArrays[i] );
                    MIntArray connectedArray;
                    weightArrayCheck.getExistingArrayAttributeIndices(connectedArray);
                    if (weightArrayCheck.numConnectedChildren() > 0)
                    {
                        for(k = 0; k < connectedArray.length(); k++ )
                        {
                            MDoubleArray tmp;
                            try
                            {
                                MArrayDataHandle arrayHandleParentParent(data.inputArrayValue( allWeightParentArrays[j] ));
//                                unsigned int countParentParent = arrayHandleParentParent.elementCount();
                                arrayHandleParentParent.jumpToArrayElement(connectedArray[k]);

                                //parent
                                MDataHandle hArrayHandleParent = arrayHandleParentParent.inputValue().child(allWeightParents[j]);
                                MArrayDataHandle hArrayHandleParentArray(hArrayHandleParent);
//                                unsigned int countParent = hArrayHandleParentArray.elementCount();

                                //child
                                hArrayHandleParentArray.jumpToElement(i);
                                MDataHandle handle(hArrayHandleParentArray.inputValue() );
                                MDataHandle child(handle.child( allWeightChildren[j] ) );
                                MFnDoubleArrayData newData(child.data());
                                tmp = MFnDoubleArrayData(child.data()).array();
//                                tmp = OpenMaya.MFnDoubleArrayData(child.data()).array()
                            }
                            catch(...)
                            {
                                MDoubleArray weight;
                                for(ii = 0; ii < iterGeoCount; ii++ )
                                    tmp.append(1.0);
                            }
                            tempWeights.push_back(tmp);
                        }
                        tmpAllWeightsArray.push_back(tempWeights);
                    }
                    else
                    {
                        std::vector < std::vector < MDoubleArray > > tmpAllWeightsArray;
                        std::vector < MDoubleArray > tempWeights;
                        MDoubleArray tmp;
                        tmp.append(1.0);
                        tempWeights.push_back(tmp);
                        tmpAllWeightsArray.push_back(tempWeights);
                    }
                }
                allWeightsArray.push_back(tmpAllWeightsArray);
            }
            else if (success == 0)
            {
                // if nothing connected build dummy array to avoid future crashes
                std::vector < std::vector < MDoubleArray > > tmpAllWeightsArray;
                std::vector < MDoubleArray > tempWeights;
                MDoubleArray tmp;
                tmp.append(1.0);
                tempWeights.push_back(tmp);
                tmpAllWeightsArray.push_back(tempWeights);
                allWeightsArray.push_back(tmpAllWeightsArray);
            }
        }
    }

    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////   get closest param infos (cache if specified)    ////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Caches out closest point functions for sliding """
    if (slideUVBasePt.size() < numIndex or cacheParamsAmt == 0)
    {
        MNurbsIntersector fnBaseIntersector;
        fnBaseIntersector.create(oSurfaceBase);
        // dump existing infos
        if (slideUVBasePt.size() > 0)
            slideUVBasePt.clear();
        if (slideUBasePtParam.size() > 0)
            slideUBasePtParam.clear();
        if (slideVBasePtParam.size() > 0)
            slideVBasePtParam.clear();

        for(i = 0; i < numIndex; i++ )
        {
            try
            {
                geomArrayHandle.jumpToElement( i );
                success = 1;
            }
            catch(...)
            {
                success = 0;
            }
            // if you find a connection, get the geometry
            if (success == 1)
            {
                MPointArray tmpPoint;
                std::vector < double > tmpUParam, tmpVParam;
                MDataHandle dhInput = geomArrayHandle.inputValue();
                MDataHandle dhWeightChild = dhInput.child( inputGeom );
                MItGeometry iter(dhWeightChild, true );
                unsigned int iterGeoCount = iter.count();
                if (iterGeoCount > 0)
                {
                    for (; !iter.isDone();)
                    {
                        pt = iter.position();

                        MPointOnNurbs ptON;
                        fnBaseIntersector.getClosestPoint(pt, ptON);
                        tmpSlideUVPoint = ptON.getPoint();
                        MPoint UV = ptON.getUV();
                        fnUParam = UV.x;
                        fnVParam = UV.y;


                        tmpPoint.append(tmpSlideUVPoint);
                        tmpUParam.push_back(fnUParam);
                        tmpVParam.push_back(fnVParam);
                        iter.next();
                    }
                    iter.reset();
                    slideUVBasePt.push_back(tmpPoint);
                    slideUBasePtParam.push_back(tmpUParam);
                    slideVBasePtParam.push_back(tmpVParam);
                }
                else
                {
                    tmpPoint.append( 0.0, 0.0, 0.0 );
                    tmpUParam.push_back(0.0);
                    tmpVParam.push_back(0.0);

                    slideUVBasePt.push_back(tmpPoint);
                    slideUBasePtParam.push_back(tmpUParam);
                    slideVBasePtParam.push_back(tmpVParam);
                }
            }
            else if (success == 0)
            {
                MPointArray tmpPoint;
                std::vector < double > tmpUParam, tmpVParam;
                tmpPoint.append( 0.0, 0.0, 0.0 );
                tmpUParam.push_back(0.0);
                tmpVParam.push_back(0.0);

                slideUVBasePt.push_back(tmpPoint);
                slideUBasePtParam.push_back(tmpUParam);
                slideVBasePtParam.push_back(tmpVParam);
            }
        }
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////   get surface base infos (cache if specified)    ////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //In most situations you can cache the surface base

    if (rotMatrix.size() < numIndex or cacheBaseAmt == 0)
    {


        //----get parameter range
        fnSurfaceBase.getKnotDomain(uMinParam,uMaxParam,vMinParam,vMaxParam);

        if (rotMatrix.size() > 0)
            rotMatrix.clear();

        for(i = 0; i < numIndex; i++ )
        {
            try
            {
                geomArrayHandle.jumpToElement( i );
                success = 1;
            }
            catch(...)
            {
                success = 0;
            }
            // if you find a connection, get the geometry
            if (success == 1)
            {
                MDataHandle dhInput = geomArrayHandle.inputValue();
                MDataHandle dhWeightChild = dhInput.child( inputGeom );
                MItGeometry iter(dhWeightChild, true );
                unsigned int iterGeoCount = iter.count();
                if (iterGeoCount > 0)
                {
                    std::vector < MEulerRotation > tmpEulerArray;

//                    MMatrixArray tmpRotMatrix;
                    //----dump old info
                    for (; !iter.isDone();)
                    {
                        unsigned int idx = iter.index();
                        fnSurfaceBase.getTangents( slideUBasePtParam[i][idx], slideVBasePtParam[i][idx], xVecBase, yVecBase, MSpace::kObject );
                        normal = fnSurfaceBase.normal( slideUBasePtParam[i][idx], slideVBasePtParam[i][idx], MSpace::kObject );

                        MVector yBaseVector = yVecBase;
                        yBaseVector.normalize();

                        MVector zBaseVector = normal;
                        zBaseVector.normalize();

                        MVector xBaseVector = yBaseVector^zBaseVector;
                        xBaseVector.normalize();

//                        yBaseVector = xBaseVector ^ zBaseVector;
//                        yBaseVector.normalize();


                        float baseMatrix[4][4]={{ xBaseVector[0], xBaseVector[1], xBaseVector[2], 0.0},
                                      { yBaseVector[0], yBaseVector[1], yBaseVector[2], 0.0},
                                      { zBaseVector[0], zBaseVector[1], zBaseVector[2], 0.0},
                                      {         0.0,         0.0,         0.0, 1.0},};

                        MMatrix BaseMatrix(baseMatrix);

                        // find the rotation offset, then apply later
                        MEulerRotation rotMatrix;
                        //////// 0 = XYZ rotation order, check maya api doc for other rotation orders
                        rotMatrix = rotMatrix.decompose(BaseMatrix,
                                                        MEulerRotation::kXYZ);
                        tmpEulerArray.push_back(rotMatrix);
//                        tmpRotMatrix.append(rotMatrix.asMatrix());
                        iter.next();
                    }
                    iter.reset();
//                    rotMatrix.push_back(tmpRotMatrix);
                    baseEuler.push_back(tmpEulerArray);
                }
                else
                {
                    std::vector < MEulerRotation > tmpEulerArray;
                    MEulerRotation rotMatrix;
                    tmpEulerArray.push_back(rotMatrix);
                    baseEuler.push_back(tmpEulerArray);
//                    MMatrix dummy;
//                    MMatrixArray tmpRotMatrix;
//                    tmpRotMatrix.append(dummy);
//                    rotMatrix.push_back(tmpRotMatrix);
                }
            }
            else if (success==0)
            {
                std::vector < MEulerRotation > tmpEulerArray;
                MEulerRotation rotMatrix;
                tmpEulerArray.push_back(rotMatrix);
                baseEuler.push_back(tmpEulerArray);
            }
        }
    }
    else
        ;

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
        if (allValsArray.size() == 0)
        {
            return MS::kSuccess;
        }
        ////////////////////////////////////////////

        //////////////////////////////////////////////////////////////////////////////////
        //////// all user defined painted weights //////
        //////////////////////////////////////////////////////////////////////////////////
        std::vector < std::vector < double > > allVals;
        for(i = 0; i < allValsArray.size(); i++ )
        {

            std::vector < double > tempVals;
            for(j = 0; j < allValsArray[i].size(); j++ )
            {
                tempVal = (double)allValsArray[i][j];
                if (allWeightsArray.size() > mIndex)
                {
                    if (allWeightsArray[mIndex].size() > i)
                    {
                        if (allWeightsArray[mIndex][i].size() > j)
                        {
                            if (allWeightsArray[mIndex][i][j].length() > idx)
                            {
                                tempW = allWeightsArray[mIndex][i][j][idx];
                            }
                            else
                            {
                                tempW = 1.0;
    //                            tempVal = 1.0;
                            }
                        }
                        else
                        {
                            tempW = 1.0;
    //                        tempVal = 1.0;
                        }
                    }
                    else
                    {
                        tempW = 1.0;
    //                    tempVal = 1.0;

                    }
                }
                else
                {
                    tempW = 1.0;
    //                tempVal = 1.0;

                }
                tempVals.push_back(tempW * tempVal);

            }
            allVals.push_back(tempVals);
        }


//    float myfloat = fabs(allVals[0][0]);
//    MGlobal::displayInfo(MString()+myfloat);



        if (allVals.size() > 0)
        {
                uW = std::accumulate(allVals[0].begin(),allVals[0].end(),0.0);
        }
        if (allVals.size() > 1)
        {
        vW = std::accumulate(allVals[1].begin(),allVals[1].end(),0.0);
        }
        if (allVals.size() > 2)
        {
        nW = std::accumulate(allVals[2].begin(),allVals[2].end(),0.0);
        }
        if (uW == 0 and vW == 0 and nW == 0)
        {
            MitGeo.next();
            continue;
        }
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////
        slideUBasePointParam = 0.0;
        slideVBasePointParam = 0.0;


        //curveBasePt
        MPoint slideUVBasePoint = slideUVBasePt[mIndex][idx];
        //curveBasePtParam
        slideUBasePointParam = slideUBasePtParam[mIndex][idx];
        slideVBasePointParam = slideVBasePtParam[mIndex][idx];

        // get min and max parameter

        slideUValue = uW;
        slideUCheck = slideUBasePointParam + slideUValue;
        double slideUBasePointParamValue = 0.0;

        slideVValue = vW;
        slideVCheck = slideVBasePointParam + slideVValue;
        double slideVBasePointParamValue = 0.0;

        rotSlideUValue = slideUCheck;
        rotSlideVValue = slideVCheck;
        // UCheck
        if ((slideUCheck > uMinParam) or (slideUCheck < uMaxParam))
        {
            slideUBasePointParamValue = rotSlideUValue;
        }
        if (slideUCheck <= uMinParam)
        {
            slideUBasePointParamValue = uMinParam;
        }
        if (slideUCheck >= uMaxParam)
        {
            slideUBasePointParamValue = uMaxParam;
        }

        // VCheck
        if ((slideVCheck > vMinParam) or (slideVCheck < vMaxParam))
        {
            slideVBasePointParamValue = rotSlideVValue;
        }
        if (slideVCheck <= vMinParam)
        {
            slideVBasePointParamValue = vMinParam;
        }
        if (slideVCheck >= vMaxParam)
        {
            slideVBasePointParamValue = vMaxParam;
        }

        // use U and V attributes to drive sliding on a surface
        // if surface goes further than the surface, find the last point traveled over, get the tangent in that direction, and have the pt travel on in that vector forever

        //// U and V on surface
        if ((slideUCheck > uMinParam or slideUCheck < uMaxParam) and
                (slideVCheck > vMinParam or slideVCheck < vMaxParam))
        {
            fnSurface.getPointAtParam( slideUBasePointParamValue,
                                       slideVBasePointParamValue,
                                       slideUVPoint,
                                       MSpace::kObject );
//            float myfloat = fabs(allVals[0][0]);
//            MGlobal::displayInfo(MString()+"uandVOnSurface");
        }
        // V Min
        if (slideVCheck <= vMinParam)
        {
            fnSurface.getDerivativesAtParm( slideUBasePointParamValue,
                                            slideVBasePointParamValue,
                                            fakePt, fnUVec, fnVVec,
                                            MSpace::kObject,
                                            &fakePt2, &fakeVecU, &fakeVecV);
            slideVVec = fnVVec;
            slideVValue = rotSlideVValue + slideVBasePointParam;
            slideUVPoint -= -slideVVec * rotSlideVValue;
        }
        // V Max
        if (slideVCheck >= vMaxParam)
        {
            fnSurface.getDerivativesAtParm( slideUBasePointParamValue,
                                            slideVBasePointParamValue,
                                            fakePt, fnUVec, fnVVec,
                                            MSpace::kObject,
                                            &fakePt2, &fakeVecU, &fakeVecV);
            slideVVec = fnVVec;
            rotSlideVValue = rotSlideVValue -1;
            slideVValue = rotSlideVValue + (slideVBasePointParam - vMaxParam);
            slideUVPoint -= -slideVVec * rotSlideVValue;
        }

        // U Min
        if (slideUCheck <= uMinParam)
        {
            fnSurface.getDerivativesAtParm( slideUBasePointParamValue,
                                            slideVBasePointParamValue,
                                            fakePt, fnUVec, fnVVec,
                                            MSpace::kObject,
                                            &fakePt2, &fakeVecU, &fakeVecV);
            slideUVec = fnUVec;
            slideUValue = rotSlideUValue + slideUBasePointParam;
            slideUVPoint -= -slideUVec * rotSlideUValue;
        }
        // U Max
        if (slideUCheck >= uMaxParam)
        {
            fnSurface.getDerivativesAtParm( slideUBasePointParamValue,
                                            slideVBasePointParamValue,
                                            fakePt, fnUVec, fnVVec,
                                            MSpace::kObject,
                                            &fakePt2, &fakeVecU, &fakeVecV);
            slideUVec = fnUVec;
            rotSlideUValue = rotSlideUValue -1;
            slideUValue = rotSlideUValue + (slideUBasePointParam - uMaxParam);
            slideUVPoint -= -slideUVec * rotSlideUValue;
        }

        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        ////////////////////////// Slide Ends //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//        rotateMatrix = rotMatrix[mIndex][idx];
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if (rotationAmount != 0)
        {
            fnSurface.getTangents( slideUBasePointParamValue, slideVBasePointParamValue, xAxisVec, yAxisVec, MSpace::kObject );
            normal = fnSurface.normal( slideUBasePointParamValue, slideVBasePointParamValue, MSpace::kObject );
    //        xAxisVec = xVec;

    //        yAxisVec = yVec;
            yAxisVec.normalize();

            zAxisVec = normal;
            zAxisVec.normalize();

            xAxisVec = yAxisVec ^ zAxisVec;
            xAxisVec.normalize();

            rotateEuler = baseEuler[mIndex][idx];
            // apply rotate offset dereference address pointer rotateMatrix with *
            MQuaternion rotateX(-(rotateEuler[0]),xAxisVec);
            rotateMatrixX = rotateX.asMatrix();
            yAxisVec = yAxisVec * rotateMatrixX;
            zAxisVec = zAxisVec * rotateMatrixX;

            MQuaternion rotateY(-(rotateEuler[1]),yAxisVec);
            rotateMatrixY = rotateY.asMatrix();
            xAxisVec = xAxisVec * rotateMatrixY;
            zAxisVec = zAxisVec * rotateMatrixY;

            MQuaternion rotateZ(-(rotateEuler[2]),zAxisVec);
            rotateMatrixZ = rotateZ.asMatrix();
            xAxisVec = xAxisVec * rotateMatrixZ;
            yAxisVec = yAxisVec * rotateMatrixZ;

            float driveMatrix[4][4]={{ xAxisVec[0], xAxisVec[1], xAxisVec[2], 0.0},
                          { yAxisVec[0], yAxisVec[1], yAxisVec[2], 0.0},
                          { zAxisVec[0], zAxisVec[1], zAxisVec[2], 0.0},
                          {         0.0,         0.0,         0.0, 1.0},};

            MMatrix DriveMatrix(driveMatrix);

            // find the rotation offset, then apply later
            MEulerRotation DriveMatrixEuler;
            DriveMatrixEuler = DriveMatrixEuler.decompose(DriveMatrix,
                                                          MEulerRotation::kXYZ);
            // apply rotation amount
            DriveMatrixEuler = MEulerRotation( DriveMatrixEuler[0] * rotationAmount,
                                               DriveMatrixEuler[1] * rotationAmount,
                                               DriveMatrixEuler[2] * rotationAmount);
            DriveMatrix = DriveMatrixEuler.asMatrix();
            finalMatrix = DriveMatrix;
        }

        ////// apply normal translation before anything else
        if (nW != 0.0)
        {
            slideNormal = fnSurfaceBase.normal( slideUBasePointParamValue,
                                                slideVBasePointParamValue,
                                                MSpace::kObject );
            pt -=(slideNormal) * nW * w;
        }
        if (rotationAmount != 0)
        {
            ////// ApplyRotation Amount
            MVector toCenterBase(-slideUVBasePoint.x,
                                 -slideUVBasePoint.y,
                                 -slideUVBasePoint.z);
            pt = pt + toCenterBase;

            // do rotationAmount, then put pts back
            pt = ( pt * finalMatrix ) - toCenterBase;
        }

        ////// apply slide
        pt.x +=(slideUVPoint.x - slideUVBasePoint.x) * w;
        pt.y +=(slideUVPoint.y - slideUVBasePoint.y) * w;
        pt.z +=(slideUVPoint.z - slideUVBasePoint.z) * w;


        if (scaleAmount != 1.0)
        {
            pt = pt - (slideUVPoint - pt) * (scaleAmount - 1.0) * w;
        }

        MitGeo.setPosition(pt);

        MitGeo.next();
    }

    return MS::kSuccess;
}

MStatus LHSlideDeformer::initialize() {

	MFnTypedAttribute tAttr;
	MFnNumericAttribute nAttr;
	MFnCompoundAttribute cAttr;
	MFnMatrixAttribute mAttr;

    ///////////////////////////////////////////
    /////////////// INPUTS ////////////////////
    ///////////////////////////////////////////



    ////////// typed attributes ////////////

    // surface
    aSurface = tAttr.create("surface", "s", MFnData::kNurbsSurface);
    addAttribute( aSurface );
    // base
    aSurfaceBase = tAttr.create("surfaceBase", "sb", MFnData::kNurbsSurface);
    addAttribute( aSurfaceBase );



    aCacheWeights = nAttr.create("cacheWeights", "cw", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheWeights);

    aCacheParams = nAttr.create("cacheParams", "cpar", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheParams);



    aCacheBase = nAttr.create("cacheBase", "cb", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheBase);


    // numeric attributes

    aRotationAmount = nAttr.create("rotationAmount", "ra", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aRotationAmount);

    aScaleAmount = nAttr.create("scaleAmount", "sa", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(1.0);
    addAttribute(aScaleAmount);

    ////////////////// UATTRS //////////////////////////////////////////////////////

    //////////////////////// VALUE ////////////////////////////////////////////////////
    aUValue = nAttr.create("uValue", "uv", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setIndexMatters(false);
    nAttr.setDefault(0.0);
//    addAttribute(aUValue);

    aUValueParent = cAttr.create("uValueParentArray", "uva");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUValue );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    nAttr.setIndexMatters(false);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUValueParent);


    //child
    aUWeights = tAttr.create("uWeights", "uw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aUWeights);

    //Parent
    aUWeightsParent = cAttr.create("uWeightsParent", "uwp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aUWeightsParent);

    //ParentParent
    aUWeightsParentArray = cAttr.create("uWeightsParentArray", "uwpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUWeightsParentArray);


    ////////////////////////////////////////////////////////////////////////////////////////
    ////////////////// VATTRS //////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////

    //////////////////////// VALUE ////////////////////////////////////////////////////
    aVValue = nAttr.create("vValue", "vv", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    cAttr.setIndexMatters( false );
    nAttr.setDefault(0.0);
//    addAttribute(aVValue);

    aVValueParent = cAttr.create("vValueParentArray", "vva");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVValue );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setIndexMatters( false );
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVValueParent);


    //child
    aVWeights = tAttr.create("vWeights", "vw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aVWeights);

    //Parent
    aVWeightsParent = cAttr.create("vWeightsParent", "vwp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aVWeightsParent);

    //ParentParent
    aVWeightsParentArray = cAttr.create("vWeightsParentArray", "vwpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVWeightsParentArray);

    //////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////// N Attrs ////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////

    aNValue = nAttr.create("nValue", "nv", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);
//     addAttribute(aNValue);

    aNValueParent = cAttr.create("nValueParentArray", "nva");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNValue );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aNValueParent);


    //child
    aNWeights = tAttr.create("nWeights", "nw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aNWeights);

    //Parent
    aNWeightsParent = cAttr.create("nWeightsParent", "nwp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aNWeightsParent);

    //ParentParent
    aNWeightsParentArray = cAttr.create("nWeightsParentArray", "nwpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aNWeightsParentArray);



    //////Affects outputs and inputs

    MObject outputGeom = MPxDeformerNode::outputGeom;

    // tAttrs
    attributeAffects(aSurface, outputGeom);
    attributeAffects(aSurfaceBase, outputGeom);

    // nAttrs

    attributeAffects(aRotationAmount, outputGeom);
    attributeAffects(aScaleAmount, outputGeom);


    attributeAffects(aCacheWeights, outputGeom);
    attributeAffects(aCacheParams, outputGeom);
    attributeAffects(aCacheBase, outputGeom);


    // U ATTRS

    attributeAffects(aUValueParent, outputGeom);

    attributeAffects(aUWeightsParentArray, outputGeom);

    // V ATTRS

    attributeAffects(aVValueParent, outputGeom);

    attributeAffects(aVWeightsParentArray, outputGeom);



    // N ATTRS

    attributeAffects(aNValueParent, outputGeom);

    attributeAffects(aNWeightsParentArray, outputGeom);




    // Make deformer weights paintable


    MGlobal::executeCommand("makePaintable -attrType multiFloat -shapeMode deformer LHSlideDeformer weights;");

    // Make deformer weights paintable

  return MS::kSuccess;
}
