//    float myfloat = fabs(allWeightsArray[0][0][0].length());
//    MGlobal::displayInfo(MString()+myfloat);

#include "LHCurveRollDeformer.h"

MTypeId LHCurveRollDeformer::id(0x78578017);


MObject LHCurveRollDeformer::aWeightMesh;

MObject LHCurveRollDeformer::aVecCurve;
MObject LHCurveRollDeformer::aOutCurve;
MObject LHCurveRollDeformer::aInCurve;

// baseGeoAttrs
MObject LHCurveRollDeformer::aBaseGeo;
MObject LHCurveRollDeformer::aBaseGeoParent;
MObject LHCurveRollDeformer::aUseBaseGeo;

//////// cache attrs ////////
MObject LHCurveRollDeformer::aAlignToCurve;
MObject LHCurveRollDeformer::aCacheWeights;
MObject LHCurveRollDeformer::aCacheWeightMesh;
MObject LHCurveRollDeformer::aCacheWeightCurves;
MObject LHCurveRollDeformer::aCacheParams;
MObject LHCurveRollDeformer::aCacheTangents;


//////////////// R ////////////////////////////
//R Values

MObject LHCurveRollDeformer::aRValue;
MObject LHCurveRollDeformer::aRValueParent;

// RWeights
MObject LHCurveRollDeformer::aRWeights;
MObject LHCurveRollDeformer::aRWeightsParent;
MObject LHCurveRollDeformer::aRWeightsParentArray;

// RAnimCurves
//RU
MObject LHCurveRollDeformer::aRAnimCurveU;
MObject LHCurveRollDeformer::aRAnimCurveUParent;
//RV

MObject LHCurveRollDeformer::aRAnimCurveV;
MObject LHCurveRollDeformer::aRAnimCurveVParent;


//////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////// get anim curves ////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
MStatus LHCurveRollDeformer::getAnimCurves(
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
void* LHCurveRollDeformer::creator() { return new LHCurveRollDeformer; }

MStatus LHCurveRollDeformer::deform(MDataBlock& data, MItGeometry& MitGeo,
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

    // cache attrs
    int useBaseGeo = data.inputValue(aUseBaseGeo).asInt();
    int alignToCurve = data.inputValue(aAlignToCurve).asInt();
    int cacheWeightsAmt = data.inputValue(aCacheWeights).asInt();
    int cacheWeightMeshAmt = data.inputValue(aCacheWeightMesh).asInt();
    int cacheWeightCurvesAmt = data.inputValue(aCacheWeightCurves).asInt();
    int cacheParamsAmt = data.inputValue(aCacheParams).asInt();
    int cacheTangentsAmt = data.inputValue(aCacheTangents).asInt();
    // typed attrs
    MObject oWeightMesh = data.inputValue(aWeightMesh).asMeshTransformed();

    MVector customVec;
    if (alignToCurve == 0 )
    {
        // If align to curve is off
        MPlug curveCheck(thisMObj, aVecCurve );
        if (curveCheck.isConnected())
        {
            // check if connected if not, use vector 1,0,0
            MObject oVecCurve = data.inputValue(aVecCurve).asNurbsCurveTransformed();
            MFnNurbsCurve fnTmpVecCurve(oVecCurve);
            MPoint pFrom;
            fnTmpVecCurve.getCV(0, pFrom);
            MPoint pTo;
            fnTmpVecCurve.getCV(1, pTo);
            MVector tmpVec(pFrom.x - pTo.x, pFrom.y - pTo.y, pFrom.z - pTo.z);
            customVec = tmpVec;
        }
        else
        {
            MVector tmpVec(1,0,0);
            customVec = tmpVec;
        }
    }
    //////////////////////////////////////////////////////////////////////////////////////////
    ////////   get all attrVals (can't cache)    ////////
    //////////////////////////////////////////////////////////////////////////////////////////

    MObject allValParents[]={
                             aRValueParent};
    MObject allValChildren[]={
                              aRValue};

    std::vector < std::vector <float> > allValsArray;
    len = sizeof(allValParents);
    for (i= 0; i < 1; ++i)
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

    MArrayDataHandle geomArrayHandle = data.inputArrayValue(geomPlug);
    if (useBaseGeo == 1)
    {
        geomArrayHandle = data.inputArrayValue(aBaseGeoParent);
    }

    // cache weight Mesh----
    // only worry about the weight mesh at scene load/mesh connection,
    // or if weight mesh caching is off
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

	iterGeoCount = MitGeo.count();

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
	//    float myfloat = fabs(allWeightsArray[0][0][0].length());
//	    MGlobal::displayInfo(MString("WORKING"));

    //////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////   get all weights (cache if specified)      ////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////
//    MPlug weightCheck(thisMObj, aUWeightsParentArray );
//    unsigned int weightSize = weightCheck.numConnectedChildren();

    if (allWeightsArray.size() < numIndex || cacheWeightsAmt == 0)
    {
        MObject allWeightParentArrays[]= {

                                          aRWeightsParentArray};
        MObject allWeightParents[] = {
                                      aRWeightsParent};
        MObject allWeightChildren[] = {
                                       aRWeights};

        // if they exist, dump old weights
        if (allWeightsArray.size() > 0)
            allWeightsArray.clear();

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
                std::vector < std::vector < MDoubleArray > > tmpAllWeightsArray;
                for(j = 0; j < 1; j++ )
                {
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
                                              aRAnimCurveUParent};
            MObject allAnimCurveUChildren[] = {
                                               aRAnimCurveU};
            MObject allAnimCurveVParents[] = {
                                              aRAnimCurveVParent};
            MObject allAnimCurveVChildren[] = {
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
                    for(j = 0; j < 1; j++ )
                    {
                        //tmp 1-ds
                        std::vector <float> tmpUTimeLength,tmpVTimeLength;
                        std::vector <float> tmpUTimeOffset,tmpVTimeOffset;
                        std::vector <MFnAnimCurve*> tmpUAnimCurves,tmpVAnimCurves;

                        try
                        {
                            //U
                            status = LHCurveRollDeformer::getAnimCurves(thisMObj,
                                          allAnimCurveUParents[j],
                                          allAnimCurveUChildren[j],
                                          tmpUTimeLength,tmpUTimeOffset,
                                          tmpUAnimCurves);
                            //V
                            status = LHCurveRollDeformer::getAnimCurves(thisMObj,
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
            // the idea here is to fine the time range of all the keys and convert that to  0-1 range
            // in a perfect world the time would only range 0-1
            // but because we might want to be remotely accurate
            // a larger range will be needed
            // therefore, a time range of seven means that we will have to divide by 7
            // in order to get back in the 0-1 range
            // this means that later, when charting the anim curve to a nurbsSurface,
            // we will have to multiply the (0-1) parameter of the nearest point by 7
            // say the parameter is .8 * 7 = 5.6
            // this means we will get the value of the anim curve at 5.6

            // of course this only works if the frame range starts at 0 and goes to 6
            // what happens when someone decides to start on frame 98.3 and ends 7 frames later?
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

//Cache get closest point

    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////   get closest param infos (cache if specified)    ////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Caches out closest point functions for sliding """
    if (closestPoint.size() < numIndex || cacheParamsAmt == 0)
    {
        MObject oOutCurve = data.inputValue(aOutCurve).asNurbsCurveTransformed();
        MFnNurbsCurve* fnOutCurve = new MFnNurbsCurve( oOutCurve, &status);
//        CheckStatusReturn( status, "Unable to Make curve" );

        MObject oInCurve = data.inputValue(aInCurve).asNurbsCurveTransformed();
        MFnNurbsCurve* fnInCurve = new MFnNurbsCurve( oInCurve,  &status );
//        CheckStatusReturn( status, "Unable to Make curve" );

        MFnNurbsCurve* allCurves[]= {fnOutCurve,
                                     fnInCurve};


        // dump existing infos
        if (closestPoint.size() > 0)
            closestPoint.clear();
        if (closestParam.size() > 0)
            closestParam.clear();

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
            // if you find a connection, get the geometry
            if (success == 1)
            {
                MDataHandle dhInput = geomArrayHandle.inputValue();
                MDataHandle dhWeightChild = dhInput.child( inputGeom );
                MItGeometry iter(dhWeightChild, true );
                unsigned int iterGeoCount = iter.count();
                std::vector <MPointArray> tmpPointArray;
                std::vector <MDoubleArray> tmpParamArray;

                if (iterGeoCount > 0)
                {
                    for(j = 0; j < 2; j++ )
                    {
                        MPointArray tmpPoint;
                        MDoubleArray tmpParam;
                        tmpParam.setLength(iterGeoCount) ;
                        tmpPoint.setLength(iterGeoCount) ;
                        for (; !iter.isDone();)
                        {
                            pt = iter.position();
                            idx = iter.index();
                            tmpPoint[idx] = allCurves[j]->closestPoint( pt, &tmpParam[idx], 0.00001, MSpace::kObject);
                            iter.next();

                        }
                        iter.reset();
                        tmpPointArray.push_back(tmpPoint);
                        tmpParamArray.push_back(tmpParam);
                    }
                    closestPoint.push_back(tmpPointArray);
                    closestParam.push_back(tmpParamArray);
                }
                else
                {
                    for(j = 0; j < 2; j++ )
                    {
                        MPointArray tmpPoint;
                        MDoubleArray tmpParam;
                        tmpPoint.append( 0.0, 0.0, 0.0 );
                        tmpParam.append(0.0);

                        tmpPointArray.push_back(tmpPoint);
                        tmpParamArray.push_back(tmpParam);
                    }
                    closestPoint.push_back(tmpPointArray);
                    closestParam.push_back(tmpParamArray);
                }
            }
            else if (success == 0)
            {
                std::vector <MPointArray> tmpPointArray;
                std::vector <MDoubleArray> tmpParamArray;
                for(j = 0; j < 2; j++ )
                {

                    MPointArray tmpPoint;
                    MDoubleArray tmpParam;
                    tmpPoint.append( 0.0, 0.0, 0.0 );
                    tmpParam.append(0.0);

                    tmpPointArray.push_back(tmpPoint);
                    tmpParamArray.push_back(tmpParam);
                }
                closestPoint.push_back(tmpPointArray);
                closestParam.push_back(tmpParamArray);
            }
        }
    }
//Cache get tangents

    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////   get tangents infos (cache if specified)    ////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Caches out closest point functions for sliding """
    if (closestTangent.size() < numIndex || cacheTangentsAmt == 0)
    {

        MObject oOutCurve = data.inputValue(aOutCurve).asNurbsCurveTransformed();
        MFnNurbsCurve* fnOutCurve = new MFnNurbsCurve( oOutCurve, &status);
//        CheckStatusReturn( status, "Unable to Make curve" );

        MObject oInCurve = data.inputValue(aInCurve).asNurbsCurveTransformed();
        MFnNurbsCurve* fnInCurve = new MFnNurbsCurve( oInCurve,  &status );
//        CheckStatusReturn( status, "Unable to Make curve" );

        MFnNurbsCurve* allCurves[]= {fnOutCurve,
                                     fnInCurve};


        // dump existing infos
        if (closestTangent.size() > 0)
        	closestTangent.clear();

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
            // if you find a connection, get the geometry
            if (success == 1)
            {
                MDataHandle dhInput = geomArrayHandle.inputValue();
                MDataHandle dhWeightChild = dhInput.child( inputGeom );
                MItGeometry iter(dhWeightChild, true );
                unsigned int iterGeoCount = iter.count();
                std::vector < MVectorArray > tmpTangentArray;
                if (iterGeoCount > 0)
                {
                    for(j = 0; j < 2; j++ )
                    {
                        MVectorArray tmpTangent;
                        tmpTangent.setLength(iterGeoCount) ;
                        for (; !iter.isDone();)
                        {
                            idx = iter.index();
                            if (closestParam.size() > i)
                            {
                                if (closestParam[i].size() > j)
                                {
                                    if (closestParam[i][j].length() > idx)
                                    {
                                        tmpTangent[idx] = allCurves[j]->tangent( closestParam[i][j][idx], MSpace::kObject);
                                        iter.next();
                                    }
                                }
                            }

                        }
                        iter.reset();
                        tmpTangentArray.push_back(tmpTangent);
                    }
                    closestTangent.push_back(tmpTangentArray);
                }
                else
                {
                    for(j = 0; j < 2; j++ )
                    {
                        MVectorArray tmpTangent;
                        MVector tmp;
                        tmpTangent.append(tmp);
                        tmpTangentArray.push_back(tmpTangent);
                    }
                    closestTangent.push_back(tmpTangentArray);
                }
            }
            else if (success == 0)
            {
                std::vector < MVectorArray > tmpTangentArray;
                for(j = 0; j < 2; j++ )
                {
                    MVectorArray tmpTangent;
                    MVector tmp;
                    tmpTangent.append(tmp);
                    tmpTangentArray.push_back(tmpTangent);
                }
                closestTangent.push_back(tmpTangentArray);
            }
        }
    }
//    MGlobal::displayInfo(MString()+closestTangent[0][0].length());


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
        ////////////////////////////////////////////
//        MGlobal::displayInfo(MString("WORKING"));

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




            //sum of val array

            rW = std::accumulate(allVals[0].begin(),allVals[0].end(),0.0);

        }


        else if (weightMeshCheck == 0)
        {
            rW = std::accumulate(allVals[0].begin(),allVals[0].end(),0.0);
        }
        if (rW == 0)
        {
            MitGeo.next();
            continue;
        }
        // order the translates and rotates based on user preference
        // if 0 translates fire first
        // if 1 rotates fire first
        //now do rotates they are index 1
//        pt = pt * rW;
        for(j = 0; j < allVals[0].size(); j++ )
        {
            if (closestTangent.size() > mIndex && closestPoint.size() > mIndex)
        	{
                if (closestTangent[0].size() > 1 && closestTangent[1].size() > 1 && closestPoint[0].size() > 1 && closestPoint[1].size() > 1)
                {
                    if (closestTangent[mIndex][0].length() > idx && closestTangent[mIndex][1].length() > idx && closestPoint[mIndex][0].length() > idx && closestPoint[mIndex][1].length() > idx)
                    {
                        // convert from radians
                        double degree = (allVals[0][j] * (3.14159265/180.0 ));
                        //Compose rotation
                        MQuaternion rotate;
                        //determine whether or not to use in or out curve
                        if (degree >= 0)
                        {
                            if (alignToCurve == 1 )
                            {
                                MQuaternion tmpRotate(degree,closestTangent[mIndex][0][idx]);
                                rotate = tmpRotate;
                            }
                            else
                            {
                                MQuaternion tmpRotate(degree,customVec);
                                rotate = tmpRotate;
                            }
                        }
                        if (degree < 0)
                        {
                            if (alignToCurve == 1 )
                            {
                                MQuaternion tmpRotate(degree,closestTangent[mIndex][1][idx]);
                                rotate = tmpRotate;
                            }
                            else
                            {
                                MQuaternion tmpRotate(degree,customVec);
                                rotate = tmpRotate;
                            }
                        }
                        MMatrix rotateMatrix = rotate.asMatrix();


                        MVector toCenterBase;
                        //Snap point to pivot
                        if (degree >= 0)
                        {
                            MVector tmpToCenterBase(-(closestPoint[mIndex][0][idx].x),
                                                    -(closestPoint[mIndex][0][idx].y),
                                                    -(closestPoint[mIndex][0][idx].z));
                            toCenterBase = tmpToCenterBase;
                        }
                        if (degree < 0)
                        {
                            MVector tmpToCenterBase(-(closestPoint[mIndex][1][idx].x),
                                                    -(closestPoint[mIndex][1][idx].y),
                                                    -(closestPoint[mIndex][1][idx].z));
                            toCenterBase = tmpToCenterBase;
                        }


                        pt = pt + toCenterBase;
                        // do rotation, then put pts back
                        pt = ( pt * rotateMatrix ) - toCenterBase;
                    }
            	}
        	}
		}

        MitGeo.setPosition(pt);

        MitGeo.next();
    }

    return MS::kSuccess;
}

MStatus LHCurveRollDeformer::initialize() {

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






//    aBaseGeo = tAttr.create("baseGeo", "bmesh", MFnData::kMesh);
//
//    aBaseGeoParent = cAttr.create("baseGeoArray", "bMeshArray");
//    cAttr.setKeyable(true);
//    cAttr.setArray(true);
//    cAttr.addChild( aBaseGeo );
//    cAttr.setReadable(true);
//    cAttr.setWritable(true);
//    cAttr.setConnectable(true);
//    cAttr.setChannelBox(true);
//    cAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aBaseGeoParent);



    // curves
    aVecCurve = tAttr.create("vectorCurve", "vCurve", MFnData::kNurbsCurve);
    addAttribute( aVecCurve );

    aOutCurve = tAttr.create("outCurve", "oCurve", MFnData::kNurbsCurve);
    addAttribute( aOutCurve );

    aInCurve = tAttr.create("inCurve", "iCurve", MFnData::kNurbsCurve);
    addAttribute( aInCurve );


    // cache attributes
    aUseBaseGeo = nAttr.create("useBaseGeo", "uBaseGeo", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aUseBaseGeo);

    aCacheParams = nAttr.create("cacheParams", "cp", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheParams);


    aCacheTangents = nAttr.create("cacheTangents", "ct", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheTangents);



    aAlignToCurve = nAttr.create("alignToCurve", "aToCurve", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aAlignToCurve);


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


    ////////////////// UATTRS //////////////////////////////////////////////////////




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


    ///////////////////////////////////////////
    /////////////// OUTPUTS ///////////////////
    ///////////////////////////////////////////


    //////Affects outputs and inputs

    MObject outputGeom = MPxDeformerNode::outputGeom;

    attributeAffects(aWeightMesh, outputGeom);

    attributeAffects(aVecCurve, outputGeom);
    attributeAffects(aOutCurve, outputGeom);
    attributeAffects(aInCurve, outputGeom);

    attributeAffects(aUseBaseGeo, outputGeom);
    attributeAffects(aBaseGeoParent, outputGeom);


    // nAttrs
    attributeAffects(aAlignToCurve, outputGeom);
    attributeAffects(aCacheTangents, outputGeom);


    attributeAffects(aCacheParams, outputGeom);
    attributeAffects(aCacheWeights, outputGeom);
    attributeAffects(aCacheWeightMesh, outputGeom);
    attributeAffects(aCacheWeightCurves, outputGeom);

    // R ATTRS

    attributeAffects(aRValueParent, outputGeom);
    attributeAffects(aRAnimCurveUParent, outputGeom);
    attributeAffects(aRAnimCurveVParent, outputGeom);
    attributeAffects(aRWeights, outputGeom);
    attributeAffects(aRWeightsParent, outputGeom);
    attributeAffects(aRWeightsParentArray, outputGeom);

//    attributeAffects(aRPivotArray, outputGeom);
//    attributeAffects(aTPivotArray, outputGeom);



    // Make deformer weights paintable


    MGlobal::executeCommand("makePaintable -attrType multiFloat -shapeMode deformer LHCurveRollDeformer weights;");

    // Make deformer weights paintable

  return MS::kSuccess;
}
