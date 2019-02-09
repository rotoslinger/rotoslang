//    float myfloat = fabs(allWeightsArray[0][0][0].length());
//    MGlobal::displayInfo(MString()+myfloat);

#include "LHVectorDeformer.h"

MTypeId LHVectorDeformer::id(0x78908017);


MObject LHVectorDeformer::aWeightMesh;

// baseMeshAttrs
MObject LHVectorDeformer::aBaseGeo;
MObject LHVectorDeformer::aBaseGeoParent;
MObject LHVectorDeformer::aUseBaseGeo;

// nAttrs
MObject LHVectorDeformer::aDeformationOrder;
//////// cache attrs ////////
MObject LHVectorDeformer::aCachePivots;
MObject LHVectorDeformer::aCacheWeights;
MObject LHVectorDeformer::aCacheWeightMesh;
MObject LHVectorDeformer::aCacheWeightCurves;
//T Values
MObject LHVectorDeformer::aTValue;
MObject LHVectorDeformer::aTValueParent;

// TWeights

MObject LHVectorDeformer::aTWeightsBaby;
MObject LHVectorDeformer::aTWeights;
MObject LHVectorDeformer::aTWeightsParent;
MObject LHVectorDeformer::aTWeightsParentArray;

// UAnimCurves
//UU
MObject LHVectorDeformer::aTAnimCurveU;
MObject LHVectorDeformer::aTAnimCurveUParent;

//UV
MObject LHVectorDeformer::aTAnimCurveV;
MObject LHVectorDeformer::aTAnimCurveVParent;

//////////////// R ////////////////////////////
//R Values

MObject LHVectorDeformer::aRValue;
MObject LHVectorDeformer::aRValueParent;

// RWeights
MObject LHVectorDeformer::aRWeights;
MObject LHVectorDeformer::aRWeightsParent;
MObject LHVectorDeformer::aRWeightsParentArray;

// RAnimCurves
//RU
MObject LHVectorDeformer::aRAnimCurveU;
MObject LHVectorDeformer::aRAnimCurveUParent;
//RV

MObject LHVectorDeformer::aRAnimCurveV;
MObject LHVectorDeformer::aRAnimCurveVParent;
//R Pivots
MObject LHVectorDeformer::aRPivot;
MObject LHVectorDeformer::aRPivotArray;
//R Pivots
MObject LHVectorDeformer::aTPivot;
MObject LHVectorDeformer::aTPivotArray;


//////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////// get anim curves ////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
MStatus LHVectorDeformer::getAnimCurves(
                                       MObject &thisMObj,
                                       MObject &animCurveParent,
                                       MObject &animCurveChild,
                                       std::vector <float> &returnTimeLength,
                                       std::vector <float> &returnTimeOffset,
                                       std::vector <MFnAnimCurve*> &returnAnimCurve)
{
    MPlug parentPlug(thisMObj, animCurveParent );
    //int count = parentPlug.numConnectedChildren();

    MIntArray curveIndex;
    parentPlug.getExistingArrayAttributeIndices(curveIndex);
    int indexLength = curveIndex.length();
    int index=0;

    for (index=0; index < indexLength; ++index)
    {
            // MGlobal::displayInfo( parentPlug.partialName() + MString(" plug is null at index ") + index);

        MPlug childPlug = parentPlug.connectionByPhysicalIndex(curveIndex[index]);
        if (childPlug.isNull())
        {
            MGlobal::displayInfo( parentPlug.partialName() + MString(" plug is null at index ") + index);
            return MS::kFailure;
        }
        MPlug oChild = childPlug.child(0);
        if (oChild.isNull())
        {
            MGlobal::displayInfo( parentPlug.partialName() + MString(" child plug is null at index ") + index);
            return MS::kFailure;
        }
        oChild.asFloat();
        MFnAnimCurve fnAnimCurve(oChild);
        int numKeys = fnAnimCurve.numKeys();

        if (!numKeys)
        {
            MGlobal::displayInfo( MString("NO KEYS"));
            // MGlobal::displayInfo(oChild.partialName() + MString(" doesn't have any keys."));
            return MS::kFailure;
        }
        MTime timeAtFirstKey = fnAnimCurve.time(0);
        MTime timeAtLastKey = fnAnimCurve.time(numKeys-1);
        float timeStart = timeAtFirstKey.value();
        float timeEnd = timeAtLastKey.value();
        float tTimeOff = timeStart * -1;
        float tTimeLength = timeEnd + tTimeOff;
        MFnAnimCurve* fnReturnAnimCurve = new MFnAnimCurve(oChild);
        returnAnimCurve.push_back(fnReturnAnimCurve);
        returnTimeOffset.push_back(tTimeOff);
        returnTimeLength.push_back(tTimeLength);
    }
    return MS::kSuccess ;
}


void* LHVectorDeformer::creator() { return new LHVectorDeformer; }

MStatus LHVectorDeformer::deform(MDataBlock& data, MItGeometry& MitGeo,
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

    int useBaseGeo = data.inputValue(aUseBaseGeo).asInt();
    int deformationOrder = data.inputValue(aDeformationOrder).asInt();
//    float scaleAmount = data.inputValue(aScaleAmount).asFloat();
    // cache attrs
    int cachePivotsAmt = data.inputValue(aCachePivots).asInt();
    int cacheWeightsAmt = data.inputValue(aCacheWeights).asInt();
//    int cacheOutWeightsAmt = data.inputValue(aCacheOutWeights).asInt();
    int cacheWeightMeshAmt = data.inputValue(aCacheWeightMesh).asInt();
    int cacheWeightCurvesAmt = data.inputValue(aCacheWeightCurves).asInt();

    //////////////////////////////////////////////////////////////////////////////////////////
    ////////   get all attrVals (can't cache)    ////////
    //////////////////////////////////////////////////////////////////////////////////////////

    MObject allValParents[]={
                             aTValueParent,
                             aRValueParent};
    MObject allValChildren[]={
                              aTValue,
                              aRValue};

    std::vector < std::vector <float> > allValsArray;
    len = sizeof(allValParents);
    for (i= 0; i < 2; ++i)
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


    ///////////////////////////////////////////////////////////////////////
    ///////////////////// get all base meshes /////////////////////////////
    ///////////////////////////////////////////////////////////////////////
    MArrayDataHandle geomArrayHandle = data.inputArrayValue(geomPlug);
    if (useBaseGeo == 1)
    {
        geomArrayHandle = data.inputArrayValue(aBaseGeoParent);
    }
//    MArrayDataHandle geomBaseArrayHandle = data.inputArrayValue(aBaseGeoParent);
    // cache weight Mesh----
    // only worry about the weight mesh at scene load/mesh connection,
    // || if weight mesh caching is off
    MObject oWeightMesh = data.inputValue(aWeightMesh).asMeshTransformed();
    MPlug weightMeshCheckPlug(thisMObj, aWeightMesh );
    if (weightMeshCheckPlug.isConnected())
    {
        weightMeshCheck = 1;
    }
    else
    {
        weightMeshCheck = 0;
    }

    // Weight Mesh
    MFnMesh fnWeightMesh(oWeightMesh);

    if ((uCoord.size() < numIndex) || (cacheWeightMeshAmt == 0))
    {
        MMeshIntersector fnWeightIntersector;
        fnWeightIntersector.create(oWeightMesh);
    // try to get weight mesh connections
        // cache weight Mesh
        if (weightMeshCheck == 1)
        {

            //----dump any previous info if it exists
            if (uCoord.size() > 0)
                uCoord.clear();
            if (vCoord.size() > 0)
                vCoord.clear();

            for (i= 0; i < numIndex; ++i)
            {
                std::vector <float> tmpUCoord;
                std::vector <float> tmpVCoord;
                std::vector <bool> tmpIntersectYN;
                status = geomArrayHandle.jumpToElement( i );
//                CheckStatusReturn( status, "Unable to jump to element" );
                if (status == MS::kSuccess)
                {
                    success = 1;
                }
                else
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

                        for (; !iter.isDone();)
                        {
                            MPoint pt = iter.position();

                            MPointOnMesh ptOnMesh;
                            fnWeightIntersector.getClosestPoint(pt, ptOnMesh);
                            weightPt = ptOnMesh.getPoint();
                            fnWeightMesh.getUVAtPoint( weightPt, uvCoord,
                                                       MSpace::kObject );


                            float ucoord = uvCoord[0];
                            float vcoord = uvCoord[1];

                            tmpUCoord.push_back(ucoord);
                            tmpVCoord.push_back(vcoord);
//                            tmpIntersectYN.push_back(intersectYN);

                            iter.next();
                        }
                        iter.reset();

                        uCoord.push_back(tmpUCoord);
                        vCoord.push_back(tmpVCoord);
//                        intersectYN.push_back(tmpIntersectYN);
                    }
                    else
                    {
                        tmpUCoord.push_back(0.0);
                        tmpVCoord.push_back(0.0);
                        tmpIntersectYN.push_back(false);

                        uCoord.push_back( tmpUCoord );
                        vCoord.push_back( tmpVCoord );
//                        intersectYN.push_back( tmpIntersectYN );
                    }
                }
                else
                {
                    tmpUCoord.push_back(0.0);
                    tmpVCoord.push_back(0.0);
                    tmpIntersectYN.push_back(false);

                    uCoord.push_back( tmpUCoord );
                    vCoord.push_back( tmpVCoord );
//                    intersectYN.push_back( tmpIntersectYN );
                }
            }
        }
    }

    ////////////////////////////////////////////////////////////////////
    ////////   get rotate pivots    ////////
    ////////////////////////////////////////////////////////////////////

//    allTPivots

    if (allPivots.size() < numIndex || cachePivotsAmt == 0)
    {
            //----dump all old info

        if (allPivots.size() > 0)
            allPivots.clear();
        if (curves.size() > 0)
            curves.clear();
        // tmp 2-ds

        ////////////////////////////////////////////////////
        //////////  all U Curves  //////////
        ////////////////////////////////////////////////////
        MObject allPivParents[] = {aTPivotArray,
                                   aRPivotArray};
        MObject allPivChildren[] = {aTPivot,
                                    aRPivot};
        for(i = 0; i < numIndex; i++ )
        {
            std::vector< std::vector < MVector > > tmpVecParentArray;
            std::vector< std::vector < MFnNurbsCurve* > > tmpVecPosParentArray;
            std::vector < std::vector < MVector  > > tmpAllPivotPositions;
            status = geomArrayHandle.jumpToElement( i );
//                CheckStatusReturn( status, "Unable to jump to element" );
            if (status == MS::kSuccess)
            {
                success = 1;
            }
            else
            {
                success = 0;
            }
            // if you find a connection, get the weights
            if (success == 1)
            {
                for (j= 0; j < 2; ++j)
                {
                    std::vector < MFnNurbsCurve* > tmpPosVecArray;
                    MArrayDataHandle arrayHandle(data.inputArrayValue( allPivParents[j], &status ));
                    CheckStatusReturn( status, "Unable to get array handle" );

                    unsigned int count = arrayHandle.elementCount();
//                    float myfloat = fabs(count);
//                    MGlobal::displayInfo(MString()+myfloat);

//                    MArrayDataHandle pivArrayHandle(data.inputArrayValue( aRPivotArray ));
//                    unsigned int pivCount = pivArrayHandle.elementCount();
//                    MPlug pivCheckPlug(thisMObj, aRPivotArray );



                    for (k= 0; k < count; ++k)
                    {
                        status = arrayHandle.jumpToElement(k);
                        CheckStatusReturn( status, "Unable to jump" );
                        //Get pivots here
                        MObject oTempCurve = arrayHandle.inputValue().child( allPivChildren[j] ).asNurbsCurveTransformed();
                        MFnNurbsCurve fnNurbsCurve( oTempCurve );
                        MFnNurbsCurve* pushCurve = new MFnNurbsCurve(oTempCurve);
                        MPointArray curvePoints;
                        pushCurve->getCVs(curvePoints, MSpace::kObject);
                        tmpPosVecArray.push_back(pushCurve);
                    }
                    tmpVecPosParentArray.push_back(tmpPosVecArray);
                }
            curves.push_back(tmpVecPosParentArray);

            }
            else if (success == 0)
            {
                MVector pivot;
                std::vector < MVector > tmpVecArray;
                std::vector< std::vector < MVector > > tmpVecParentArray;

                tmpVecArray.push_back(pivot);
                tmpVecParentArray.push_back(tmpVecArray);
                allPivots.push_back(tmpVecParentArray);

            }
        }
        if (allPivots.size() > 0)
            allPivots.clear();
        if (allPivotPositions.size() > 0)
            allPivotPositions.clear();
        for(i = 0; i < curves.size(); i++ )
        {
            std::vector< std::vector < MVector > > tmpVecParentArray;
            std::vector < std::vector < MPoint  > > tmpAllPivotPositions;
            for (j= 0; j < curves[i].size(); ++j)
            {
                std::vector < MVector > tmpVecArray;
                std::vector < MPoint  > tmpPPositions;
                for (k= 0; k < curves[i][j].size(); ++k)
                {

                    MPointArray curvePoints;
                    curves[i][j][k]->getCVs(curvePoints, MSpace::kObject);
                    //get pivot
                    MVector pivot(curvePoints[0].x-curvePoints[1].x,
                                  curvePoints[0].y-curvePoints[1].y,
                                  curvePoints[0].z-curvePoints[1].z);
                    //Compose rotation
                    MPoint position(curvePoints[0]);
                    //Snap point to pivot

                    tmpVecArray.push_back(pivot);
                    tmpPPositions.push_back(position);
                }
                tmpVecParentArray.push_back(tmpVecArray);
                tmpAllPivotPositions.push_back(tmpPPositions);
            }
            allPivots.push_back(tmpVecParentArray);
            allPivotPositions.push_back(tmpAllPivotPositions);
        }
    }
    iterGeoCount = MitGeo.count();




    //////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////   get all weights (cache if specified)      ////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////
//    MPlug weightCheck(thisMObj, aUWeightsParentArray );
//    unsigned int weightSize = weightCheck.numConnectedChildren();

    if (allWeightsArray.size() < numIndex || cacheWeightsAmt == 0)
    {
        MObject allWeightParentArrays[]= {
                                          aTWeightsParentArray,

                                          aRWeightsParentArray};
        MObject allWeightParents[] = {
                                      aTWeightsParent,
                                      aRWeightsParent};
        MObject allWeightChildren[] = {
                                       aTWeights,
                                       aRWeights};

        // if they exist, dump old weights
        if (allWeightsArray.size() > 0)
            allWeightsArray.clear();

        for(i = 0; i < numIndex; i++ )
        {
//            MGlobal::displayInfo(MString("i"));
            status = geomArrayHandle.jumpToElement( i );
//                CheckStatusReturn( status, "Unable to jump to element" );
            if (status == MS::kSuccess)
            {
                success = 1;
            }
            else
            {
                success = 0;
            }
            // if you find a connection, get the weights
            if (success == 1)
            {
//              tmpAllWeightsArray = [];
                std::vector < std::vector < MDoubleArray > > tmpAllWeightsArray;
                for(j = 0; j < 2; j++ )
                {
//                    MGlobal::displayInfo(MString("j"));
//              for j in range(len(allWeightParentArrays)):
//                  tempWeights = [];
                    std::vector < MDoubleArray > tempWeights;
                    MPlug weightArrayCheck(thisMObj, allWeightParentArrays[j] );
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
                                arrayHandleParentParent.jumpToArrayElement(connectedArray[k]);

                                //parent
                                MDataHandle hArrayHandleParent = arrayHandleParentParent.inputValue().child(allWeightParents[j]);
                                MArrayDataHandle hArrayHandleParentArray(hArrayHandleParent);

                                //child
                                status = hArrayHandleParentArray.jumpToElement(i);
                                if (!status)
                                    for(ii = 0; ii < iterGeoCount; ii++ )
                                        tmp.append(1.0);
                                else
                                {
                                    // CheckStatusReturn( status, "Unable to jump to element" );
                                    MDataHandle handle(hArrayHandleParentArray.inputValue(&status) );
                                    CheckStatusReturn( status, "Unable to get handle" );
                                    MDataHandle child(handle.child( allWeightChildren[j] ) );
                                    MFnDoubleArrayData newData(child.data());
                                    tmp = MFnDoubleArrayData(child.data()).array();
                                    // MGlobal::displayInfo(MString("STATUS") + status);
                                }
                                
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


//    MGlobal::displayInfo(MString("BigBreak"));










//    float myfloat = fabs(iterGeoCount);

//    float myfloat = fabs(allWeightsArray[1][0][0].length());
//    MGlobal::displayInfo(MString()+myfloat);
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////   get multiAnimCurves (cache if specified)    ////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // to keep the size of code small,
    // we will put all u,v,n,r anim curve info into an array
    // indexes are as follows:
    // 0 = u anim stuff
    // 1 = v anim stuff
    // 2 = n anim stuff
    // 3 = r anim stuff



    if (allUAnimCurveWeights.size() < numIndex || cacheWeightCurvesAmt == 0)
    {
        if (weightMeshCheck == 1)
        {
            //----dump all old info

            if (allUFnCurvesArray.size() > 0)
                allUFnCurvesArray.clear();

            if (allUTimeOffsetArray.size() > 0)
                allUTimeOffsetArray.clear();

            if (allUTimeLengthArray.size() > 0)
                allUTimeLengthArray.clear();

            if (allVFnCurvesArray.size() > 0)
                allVFnCurvesArray.clear();

            if (allVTimeOffsetArray.size() > 0)
                allVTimeOffsetArray.clear();

            if (allVTimeLengthArray.size() > 0)
                allVTimeLengthArray.clear();

            if (allUAnimCurveWeights.size() > 0)
                allUAnimCurveWeights.clear();

            if (allVAnimCurveWeights.size() > 0)
                allVAnimCurveWeights.clear();

            // tmp 2-ds
            std::vector < std::vector < float > > tmpUTimeLengthArray,tmpVTimeLengthArray;
            std::vector < std::vector < float > > tmpUTimeOffsetArray,tmpVTimeOffsetArray;
            std::vector < std::vector < MFnAnimCurve* > > tmpUAnimCurvesArray,tmpVAnimCurvesArray;

            ////////////////////////////////////////////////////
            //////////  all U Curves  //////////
            ////////////////////////////////////////////////////

            MObject allAnimCurveUParents[] = {
                                              aTAnimCurveUParent,
                                              aRAnimCurveUParent};
            MObject allAnimCurveUChildren[] = {
                                               aTAnimCurveU,
                                               aRAnimCurveU};
            MObject allAnimCurveVParents[] = {
                                              aTAnimCurveVParent,
                                              aRAnimCurveVParent};
            MObject allAnimCurveVChildren[] = {
                                               aTAnimCurveV,
                                               aRAnimCurveV};
            for(i = 0; i < numIndex; i++ )
            {
                status = geomArrayHandle.jumpToElement( i );
//                CheckStatusReturn( status, "Unable to jump to element" );
                if (status == MS::kSuccess)
                {
                    success = 1;
                }
                else
                {
                    success = 0;
                }
                // if you find a connection, get the weights
                if (success == 1)
                {
                    for(j = 0; j < 2; j++ )
                    {
                        //tmp 1-ds
                        std::vector <float> tmpUTimeLength,tmpVTimeLength;
                        std::vector <float> tmpUTimeOffset,tmpVTimeOffset;
                        std::vector <MFnAnimCurve*> tmpUAnimCurves,tmpVAnimCurves;

                        try
                        {
                            //U
                            status = LHVectorDeformer::getAnimCurves(thisMObj,
                                          allAnimCurveUParents[j],
                                          allAnimCurveUChildren[j],
                                          tmpUTimeLength,tmpUTimeOffset,
                                          tmpUAnimCurves);
                            //V
                            status = LHVectorDeformer::getAnimCurves(thisMObj,
                                          allAnimCurveVParents[j],
                                          allAnimCurveVChildren[j],
                                          tmpVTimeLength,tmpVTimeOffset,
                                          tmpVAnimCurves);
                        }
                        catch(...)
                        {
                            ;
                        }
                        if (tmpUAnimCurves.size() == 0)
                        {
                            MFnAnimCurve* dummyCurve;
                            tmpUAnimCurves.push_back(dummyCurve);
                            tmpUTimeOffset.push_back(0.0);
                            tmpUTimeLength.push_back(0.0);
                        }
                        if (tmpVAnimCurves.size() == 0)
                        {
                            MFnAnimCurve* dummyCurve;
                            tmpVAnimCurves.push_back(dummyCurve);
                            tmpVTimeOffset.push_back(0.0);
                            tmpVTimeLength.push_back(0.0);
                        }
                        tmpUAnimCurvesArray.push_back(tmpUAnimCurves);
                        tmpUTimeOffsetArray.push_back(tmpUTimeOffset);
                        tmpUTimeLengthArray.push_back(tmpUTimeLength);

                        tmpVAnimCurvesArray.push_back(tmpVAnimCurves);
                        tmpVTimeOffsetArray.push_back(tmpVTimeOffset);
                        tmpVTimeLengthArray.push_back(tmpVTimeLength);
                    }
                    allUFnCurvesArray.push_back(tmpUAnimCurvesArray);
                    allUTimeOffsetArray.push_back(tmpUTimeOffsetArray);
                    allUTimeLengthArray.push_back(tmpUTimeLengthArray);

                    allVFnCurvesArray.push_back(tmpVAnimCurvesArray);
                    allVTimeOffsetArray.push_back(tmpVTimeOffsetArray);
                    allVTimeLengthArray.push_back(tmpVTimeLengthArray);
                }
                else if (success == 0)
                {
                    std::vector <MFnAnimCurve*> dummyCurveArray;

                    MFnAnimCurve* dummyCurve;
                    dummyCurveArray.push_back(dummyCurve);
                    tmpUAnimCurvesArray.push_back(dummyCurveArray);

                    std::vector <float> dummyFloat;
                    dummyFloat.push_back(0.0);
                    tmpUTimeLengthArray.push_back(dummyFloat);

                    allUFnCurvesArray.push_back(tmpUAnimCurvesArray);
                    allUTimeOffsetArray.push_back(tmpUTimeLengthArray);
                    allUTimeLengthArray.push_back(tmpUTimeLengthArray);
                    allVFnCurvesArray.push_back(tmpUAnimCurvesArray);
                    allVTimeOffsetArray.push_back(tmpUTimeLengthArray);
                    allVTimeLengthArray.push_back(tmpUTimeLengthArray);
                }
            }

            // AnimCURVE
            // the idea here is to fine the time range of all the keys && convert that to  0-1 range
            // in a perfect world the time would only range 0-1
            // but because we might want to be remotely accurate
            // a larger range will be needed
            // therefore, a time range of seven means that we will have to divide by 7
            // in order to get back in the 0-1 range
            // this means that later, when charting the anim curve to a nurbsSurface,
            // we will have to multiply the (0-1) parameter of the nearest point by 7
            // say the parameter is .8 * 7 = 5.6
            // this means we will get the value of the anim curve at 5.6

            // of course this only works if the frame range starts at 0 && goes to 6
            // what happens when someone decides to start on frame 98.3 && ends 7 frames later?
            // you simply subtract 98.3, then, then do the steps above.

            // if stuff exists already then dump it
            if (allUAnimCurveWeights.size() > 0)
                allUAnimCurveWeights.clear();
            if (allVAnimCurveWeights.size() > 0)
                allVAnimCurveWeights.clear();


            for(i = 0; i < numIndex; i++ )
            {
                //3-d arrays
                std::vector < std::vector < std::vector < double > > > tempU,tempV;
                status = geomArrayHandle.jumpToElement( i );
//                CheckStatusReturn( status, "Unable to jump to element" );
                if (status == MS::kSuccess)
                {
                    success = 1;
                }
                else
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
                        for(j = 0; j < allUFnCurvesArray[i].size(); j++ )
                        {
                            //2-d array
                            std::vector < std::vector < double > > tempUVals;
                            for(k = 0; k < allUFnCurvesArray[i][j].size(); k++ )
                            {
                                //1-d array
                                std::vector < double > tempUPointVals;
                                for (; !iter.isDone();)
                                {
                                    pt = iter.position();
                                    try
                                    {
                                        double remap = uCoord[i][iter.index()] * allUTimeLengthArray[i][j][k];
                                        remap = remap - allUTimeOffsetArray[i][j][k];
//                                        remap = OpenMaya.MTime(remap);
                                        MTime remapTime(remap);
//                                        MFnAnimCurve* fnReturnAnimCurve = new MFnAnimCurve(oChild);
//                                        MFnAnimCurve * wCurve(allUFnCurvesArray[i][j][k]);
                                        double weight = allUFnCurvesArray[i][j][k]->evaluate(remapTime);
                                        tempUPointVals.push_back(weight);
                                    }
                                    catch(...)
                                    {
                                        tempUPointVals.push_back(1.0);
                                    }
                                    iter.next();
                                }
                                iter.reset();
                                tempUVals.push_back(tempUPointVals);
                            }
                            tempU.push_back(tempUVals);
                        }
                        allUAnimCurveWeights.push_back(tempU);

                        for(j = 0; j < allVFnCurvesArray[i].size(); j++ )
                        {
                            //2-d array
                            std::vector < std::vector < double > > tempVVals;
                            for(k = 0; k < allVFnCurvesArray[i][j].size(); k++ )
                            {//                          MDoubleArray tmp;

                                //1-d array
                                std::vector < double > tempVPointVals;

                                for (; !iter.isDone();)
                                {
                                    pt = iter.position();
                                    try
                                    {
                                        double remap = vCoord[i][iter.index()] * allVTimeLengthArray[i][j][k];
                                        remap = remap - allVTimeOffsetArray[i][j][k];
                                        MTime remapTime(remap);
                                        double weight = allVFnCurvesArray[i][j][k]->evaluate(remapTime);
                                        tempVPointVals.push_back(weight);
                                    }
                                    catch(...)
                                    {
                                        tempVPointVals.push_back(1.0);
                                    }
                                    iter.next();
                                }
                                iter.reset();
                                tempVVals.push_back(tempVPointVals);
                            }
                            tempV.push_back(tempVVals);
                        }
                        allVAnimCurveWeights.push_back(tempV);
                    }
                    else if (iterGeoCount == 0)
                    {
                        double dummy = 0.0;
                        std::vector < double > dummy1d;
                        std::vector < std::vector < double > > dummy2d;
                        std::vector < std::vector < std::vector < double > > > dummy3d;
                        dummy1d.push_back(dummy);
                        dummy2d.push_back(dummy1d);
                        dummy3d.push_back(dummy2d);
                        allUAnimCurveWeights.push_back(dummy3d);
                        allVAnimCurveWeights.push_back(dummy3d);
                    }
                }
                else if (success == 0)
                {
                    double dummy = 0.0;
                    std::vector < double > dummy1d;
                    std::vector < std::vector < double > > dummy2d;
                    std::vector < std::vector < std::vector < double > > > dummy3d;
                    dummy1d.push_back(dummy);
                    dummy2d.push_back(dummy1d);
                    dummy3d.push_back(dummy2d);
                    allUAnimCurveWeights.push_back(dummy3d);
                    allVAnimCurveWeights.push_back(dummy3d);
                }
            }
        }
        else
        {
            ;
        }
        }
    else
    {
        ;
    }

    for (; !MitGeo.isDone();)
    {
        pt = MitGeo.position();
        idx = MitGeo.index();
        w = weightValue(data, mIndex, idx)* envelope;
        if (allValsArray.size() == 0)
        {
            return MS::kSuccess;
        }
        if (fabs(w) <= 0)
        {
            MitGeo.next();
            continue;
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

                            }
                        }
                        else
                        {
                            tempW = 1.0;

                        }
                    }
                    else
                    {
                        tempW = 1.0;

                    }
                }
                else
                {
                    tempW = 1.0;

                }
                tempVals.push_back(tempW * tempVal);

            }
            allVals.push_back(tempVals);
        }


//    float myfloat = fabs(allVals[0][0]);
//    MGlobal::displayInfo(MString()+myfloat);



        ////////////////////////////////////////////
        //////// curveWeights ////////
        ////////////////////////////////////////////
        if (weightMeshCheck == 1)
        {

            ////////////////////////////////////////////////////////
            //////////// U V N R combine //////////
            ////////////////////////////////////////////////////////
            tW = 0.0;
            rW = 0.0;
            //---Multiply painted weights by curve weights
            // the length of all arrays should be the same
            // this is currently up to the user
            // but I should write a failsafe

            //Make sure all vals is properly filled up
            for(i = 0; i < allVals[0].size(); i++ )
            {
                if (allUAnimCurveWeights[mIndex][0].size() > i && allVAnimCurveWeights[mIndex][0].size() > i)
                {
                    if (allUAnimCurveWeights[mIndex][0][i].size() >= idx+1 && allVAnimCurveWeights[mIndex][0][i].size() >= idx+1)
                    {
                        allVals[0][i] = (allVals[0][i] *
                                         allUAnimCurveWeights[mIndex][0][i][idx] *
                                         allVAnimCurveWeights[mIndex][0][i][idx]);
                    }
                    else
                    {
                        allVals[0][i] = allVals[0][i] * 1.0;
                    }
                }
                else
                {
                    allVals[0][i] = allVals[0][i] * 1.0;
                }
            }



            for(i = 0; i < allVals[1].size(); i++ )
            {
                if (allUAnimCurveWeights[mIndex][1].size() > i && allVAnimCurveWeights[mIndex][1].size() > i)
                {
                    if (allUAnimCurveWeights[mIndex][1][i].size() >= idx+1 && allVAnimCurveWeights[mIndex][1][i].size() >= idx+1)
                    {
                        allVals[1][i] = (allVals[1][i] *
                                         allUAnimCurveWeights[mIndex][1][i][idx] *
                                         allVAnimCurveWeights[mIndex][1][i][idx]);
                    }
                    else
                    {
                        allVals[1][i] = allVals[1][i] * 1.0;
                    }
                }
                else
                {
                    allVals[1][i] = allVals[1][i] * 1.0;
                }
            }

            //sum of val array
            if (allVals.size() > 0)
            {
                tW = std::accumulate(allVals[0].begin(),allVals[0].end(),0.0);
            }
            if (allVals.size() > 1)
            {
                rW = std::accumulate(allVals[1].begin(),allVals[1].end(),0.0);
            }

        }


        else if (weightMeshCheck == 0)
        {
            if (allVals.size() > 0)
            {
                tW = std::accumulate(allVals[0].begin(),allVals[0].end(),0.0);
            }
            if (allVals.size() > 1)
            {
                rW = std::accumulate(allVals[1].begin(),allVals[1].end(),0.0);
            }
        }
        if (tW == 0 && rW == 0)
        {
            MitGeo.next();
            continue;
        }
        // order the translates && rotates based on user preference
        // if 0 translates fire first
        // if 1 rotates fire first
        if (deformationOrder == 0)
        {
            if (allVals.size() > 0)
            {
            //first do translates they are index 0
                for(j = 0; j < allVals[0].size(); j++ )
                {
                    if (allPivots.size() > mIndex)
                    {
                        if (allPivots[mIndex].size() > 1)
                        {
                            if (allPivots[mIndex][0].size() > j)
                            {
                                pt -=(allPivots[mIndex][0][j]) * allVals[0][j];
                            }
                            else
                            {
                                ;
                            }
                        }
                        else
                        {
                            ;
                        }
                    }
                    else
                    {
                        ;
                    }
                }
            }
        }

        //now do rotates they are index 1
        if (allVals.size() > 1)
        {
            for(j = 0; j < allVals[1].size(); j++ )
            {
                if (allPivots.size() > mIndex)
                {
                    if (allPivots[mIndex].size() > 1)
                    {
                        if (allPivots[mIndex][1].size() > j)
                        {
                            // convert from radians
                            double degree = (allVals[1][j] * (3.14159265/180.0 ));

                            //Compose rotation
                            MQuaternion rotate(degree,allPivots[mIndex][1][j]);
                            MMatrix rotateMatrix = rotate.asMatrix();

                            //Snap point to pivot
                            MVector toCenterBase(-(allPivotPositions[mIndex][1][j].x),
                                                 -(allPivotPositions[mIndex][1][j].y),
                                                 -(allPivotPositions[mIndex][1][j].z));
                            pt = pt + toCenterBase;
                            // do rotation, then put pts back
                            pt = ( pt * rotateMatrix ) - toCenterBase;
                        }
                        else
                        {
                            ;
                        }
                    }
                    else
                    {
                        ;
                    }
                }
                else
                {
                    ;
                }
            }
        }
        if (deformationOrder == 1)
        {
            if (allVals.size() > 0)
            {
            //first do translates they are index 0
                for(j = 0; j < allVals[0].size(); j++ )
                {
                    if (allPivots.size() > mIndex)
                    {
                        if (allPivots[mIndex].size() > 1)
                        {
                            if (allPivots[mIndex][0].size() > j)
                            {
                                pt -=(allPivots[mIndex][0][j]) * allVals[0][j];
                            }
                            else
                            {
                                ;
                            }
                        }
                        else
                        {
                            ;
                        }
                    }
                    else
                    {
                        ;
                    }
                }
            }
        }
        MitGeo.setPosition(pt);

        MitGeo.next();
    }

    return MS::kSuccess;
}

MStatus LHVectorDeformer::initialize() {

    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnMatrixAttribute mAttr;
    MFnGenericAttribute gAttr;
    ///////////////////////////////////////////
    /////////////// INPUTS ////////////////////
    ///////////////////////////////////////////



    ////////// typed attributes ////////////

    // weight patchallVals
    aWeightMesh = tAttr.create("weightPatch", "wp", MFnData::kMesh);
    addAttribute( aWeightMesh );


    //base geoms
    aBaseGeo = gAttr.create("baseGeo", "bGeo");
    gAttr.addAccept(MFnData::kMesh);
    gAttr.addAccept(MFnData::kNurbsSurface);
    gAttr.addAccept(MFnData::kNurbsCurve);

    aBaseGeoParent = cAttr.create("baseGeoArray", "bGeoArray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aBaseGeo );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aBaseGeoParent);


    // cache attributes
    aUseBaseGeo = nAttr.create("useBaseGeo", "uBaseGeo", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aUseBaseGeo);

    aCachePivots = nAttr.create("cachePivots", "cp", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCachePivots);

    aCacheWeights = nAttr.create("cacheWeights", "cw", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheWeights);

    aCacheWeightMesh = nAttr.create("cacheWeightMesh", "cwm", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheWeightMesh);

    aCacheWeightCurves = nAttr.create("cacheWeightCurves", "cwc", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheWeightCurves);
    // numeric attributes

    aDeformationOrder = nAttr.create("deformationOrder", "ra", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aDeformationOrder);

    ////////////////// UATTRS //////////////////////////////////////////////////////


    ////////////////////////////////////////////////////////////////////////////////////////
    ////////////////// VATTRS //////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////

    //////////////////////// VALUE ////////////////////////////////////////////////////
    aTValue = nAttr.create("tValue", "tv", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);

    aTValueParent = cAttr.create("tValueParentArray", "tva");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aTValue );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aTValueParent);


    //baby

    //child
    aTWeights = tAttr.create("tWeights", "tw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);

    //Parent
    aTWeightsParent = cAttr.create("tWeightsParent", "twp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aTWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);

    //ParentParent
    aTWeightsParentArray = cAttr.create("tWeightsParentArray", "twpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aTWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aTWeightsParentArray);


    aTAnimCurveU = nAttr.create("tAnimCurveU", "tuac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);

    aTAnimCurveUParent = cAttr.create("tAnimCurveUArray", "tuaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aTAnimCurveU );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aTAnimCurveUParent);

    aTAnimCurveV = nAttr.create("tAnimCurveV", "tvac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);

    aTAnimCurveVParent = cAttr.create("tAnimCurveVArray", "tvaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aTAnimCurveV );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aTAnimCurveVParent);

    //////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////// N Attrs ////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////
//

    //////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////// R Attrs ////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////

    aRValue = nAttr.create("rValue", "rv", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);

    aRValueParent = cAttr.create("rValueParentArray", "rva");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRValue );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRValueParent);

    //child
    aRWeights = tAttr.create("rWeights", "rw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);

    //Parent
    aRWeightsParent = cAttr.create("rWeightsParent", "rwp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);

    //ParentParent
    aRWeightsParentArray = cAttr.create("rWeightsParentArray", "rwpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRWeightsParentArray);


    aRAnimCurveU = nAttr.create("rAnimCurveU", "ruac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);

    aRAnimCurveUParent = cAttr.create("rAnimCurveUArray", "ruaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRAnimCurveU );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRAnimCurveUParent);

    aRAnimCurveV = nAttr.create("rAnimCurveV", "rvac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);

    aRAnimCurveVParent = cAttr.create("rAnimCurveVArray", "rvaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRAnimCurveV );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRAnimCurveVParent);


    //R Pivot Curves
    aRPivot = tAttr.create("rPivotCurve", "rpc", MFnData::kNurbsCurve);

    aRPivotArray = cAttr.create("rPivotCurveArray", "rpca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRPivot );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRPivotArray);

    //R Pivot Curves
    aTPivot = tAttr.create("tPivotCurve", "tpc", MFnData::kNurbsCurve);

    aTPivotArray = cAttr.create("tPivotCurveArray", "tpca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aTPivot );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aTPivotArray);


    ///////////////////////////////////////////
    /////////////// OUTPUTS ///////////////////
    ///////////////////////////////////////////


    //////Affects outputs && inputs

    MObject outputGeom = MPxDeformerNode::outputGeom;

    attributeAffects(aWeightMesh, outputGeom);

    // nAttrs

    attributeAffects(aDeformationOrder, outputGeom);

    attributeAffects(aUseBaseGeo, outputGeom);
    attributeAffects(aBaseGeoParent, outputGeom);

    attributeAffects(aCachePivots, outputGeom);
    attributeAffects(aCacheWeights, outputGeom);
    attributeAffects(aCacheWeightMesh, outputGeom);
    attributeAffects(aCacheWeightCurves, outputGeom);

    // V ATTRS

    attributeAffects(aTValueParent, outputGeom);

    attributeAffects(aTWeightsParentArray, outputGeom);

    attributeAffects(aTAnimCurveUParent, outputGeom);

    attributeAffects(aTAnimCurveVParent, outputGeom);

    // R ATTRS

    attributeAffects(aRValueParent, outputGeom);
    attributeAffects(aRWeightsParentArray, outputGeom);
    attributeAffects(aRAnimCurveUParent, outputGeom);
    attributeAffects(aRAnimCurveVParent, outputGeom);
    attributeAffects(aRPivotArray, outputGeom);
    attributeAffects(aTPivotArray, outputGeom);



    // Make deformer weights paintable


    MGlobal::executeCommand("makePaintable -attrType multiFloat -shapeMode deformer LHVectorDeformer weights;");

    // Make deformer weights paintable

  return MS::kSuccess;
}
