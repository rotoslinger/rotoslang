//    float myfloat = fabs(allWeightsArray[0][0][0].length());
//    MGlobal::displayInfo(MString()+myfloat);
#include <maya/MCppCompat.h>

#include "LHWeightDeformer.h"

MTypeId LHWeightDeformer::id(0x00008787);

// tAttrs
MObject LHWeightDeformer::aWeightMesh;
// nAttrs
//////// cache attrs ////////
MObject LHWeightDeformer::aCacheWeights;
MObject LHWeightDeformer::aCacheWeightMesh;
MObject LHWeightDeformer::aCacheWeightCurves;
//////////////// U ////////////////////////////
//U Values

// UWeights
MObject LHWeightDeformer::aWeights;
MObject LHWeightDeformer::aWeightsParent;
MObject LHWeightDeformer::aWeightsParentArray;

// UAnimCurves
//UU
MObject LHWeightDeformer::aUAnimCurve;
MObject LHWeightDeformer::aUAnimCurveParent;

//UV
MObject LHWeightDeformer::aVAnimCurve;
MObject LHWeightDeformer::aVAnimCurveParent;

// OutPuts
MObject LHWeightDeformer::aCacheOutWeights;

MObject LHWeightDeformer::aOutWeights;
MObject LHWeightDeformer::aOutWeightsParent;
MObject LHWeightDeformer::aOutWeightsParentArray;



//////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////// get anim curves ////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
MStatus LHWeightDeformer::getAnimCurves(
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
        MPlug childPlug = parentPlug.connectionByPhysicalIndex(curveIndex[index]);
        MPlug oChild = childPlug.child(0);
        oChild.asFloat();
        MFnAnimCurve fnAnimCurve(oChild);
        int numKeys = fnAnimCurve.numKeys();
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

void* LHWeightDeformer::creator() { return new LHWeightDeformer; }

MStatus LHWeightDeformer::deform(MDataBlock& data, MItGeometry& MitGeo,
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
    MArrayDataHandle geomArrayHandle = data.inputArrayValue(geomPlug);

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
    int cacheWeightsAmt = data.inputValue(aCacheWeights).asInt();
    int cacheOutWeightsAmt = data.inputValue(aCacheOutWeights).asInt();
    int cacheWeightMeshAmt = data.inputValue(aCacheWeightMesh).asInt();
    int cacheWeightCurvesAmt = data.inputValue(aCacheWeightCurves).asInt();
	iterGeoCount = MitGeo.count();

    ////////////////////////////////////////////////////////////////////////////
    ////////   get weightMesh //////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
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

    if ((uCoord.size() < numIndex) or (cacheWeightMeshAmt == 0))
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
//      MGlobal::displayInfo(MString("WORKING"));

    //////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////   get all weights (cache if specified)      ////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////
//    MPlug weightCheck(thisMObj, aUWeightsParentArray );
//    unsigned int weightSize = weightCheck.numConnectedChildren();

    if (allWeightsArray.size() < numIndex or cacheWeightsAmt == 0)
    {
        MObject allWeightParentArrays[]= {

                                          aWeightsParentArray};
        MObject allWeightParents[] = {
                                      aWeightsParent};
        MObject allWeightChildren[] = {
                                       aWeights};

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
                std::vector < std::vector < MDoubleArray > > tmpAllWeightsArray;
                for(j = 0; j < 1; j++ )
                {
                    std::vector < MDoubleArray > tempWeights;
                    MPlug weightArrayCheck(thisMObj, allWeightParentArrays[j] );
                    MIntArray connectedArray;
                    weightArrayCheck.getExistingArrayAttributeIndices(connectedArray);
//                    MGlobal::displayInfo(MString("GETWEIGHTS")+ i);
                    if (weightArrayCheck.numConnectedChildren() > 0)
                    {
                        for(k = 0; k < connectedArray.length(); k++ )
                        {
                            MDoubleArray tmp;
                            try
                            {
                                MArrayDataHandle arrayHandleParentParent(data.inputArrayValue( allWeightParentArrays[j] ));
                                unsigned int countParentParent = arrayHandleParentParent.elementCount();
                                arrayHandleParentParent.jumpToArrayElement(connectedArray[k]);

                                //parent
                                MDataHandle hArrayHandleParent = arrayHandleParentParent.inputValue().child(allWeightParents[j]);
                                MArrayDataHandle hArrayHandleParentArray(hArrayHandleParent);

                                //child
                                hArrayHandleParentArray.jumpToElement(i);

                                MDataHandle handle(hArrayHandleParentArray.inputValue() );
                                MDataHandle child(handle.child( allWeightChildren[j] ) );

                                MFnDoubleArrayData newData(child.data());
                                tmp = MFnDoubleArrayData(child.data()).array();
//                                MGlobal::displayInfo(MString("GETWEIGHTS")+ i);
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



    if (allUAnimCurveWeights.size() < numIndex or cacheWeightCurvesAmt == 0)
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

            MObject allUAnimCurveParents[] = {
                                              aUAnimCurveParent};
            MObject allUAnimCurveChildren[] = {
                                               aUAnimCurve};
            MObject allVAnimCurveParents[] = {
                                              aVAnimCurveParent};
            MObject allVAnimCurveChildren[] = {
                                               aVAnimCurve};
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
                    for(j = 0; j < 1; j++ )
                    {
                        //tmp 1-ds
                        std::vector <float> tmpUTimeLength,tmpVTimeLength;
                        std::vector <float> tmpUTimeOffset,tmpVTimeOffset;
                        std::vector <MFnAnimCurve*> tmpUAnimCurves,tmpVAnimCurves;

                        try
                        {
                            //U
                            status = LHWeightDeformer::getAnimCurves(thisMObj,
                                          allUAnimCurveParents[j],
                                          allUAnimCurveChildren[j],
                                          tmpUTimeLength,tmpUTimeOffset,
                                          tmpUAnimCurves);
                            //V
                            status = LHWeightDeformer::getAnimCurves(thisMObj,
                                          allVAnimCurveParents[j],
                                          allVAnimCurveChildren[j],
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

//    MGlobal::displayInfo(MString("vanimcurves")+allVAnimCurveWeights[0][0][0].size());

    ////////////////////////////////////////////////////////////////////
    ////////   set all output weights (cache if specified)      ////////
    ////////////////////////////////////////////////////////////////////

//    MPlug weightCheck(thisMObj, aUWeightsParentArray );
//    unsigned int weightSize = weightCheck.numConnectedChildren();

    if (allOutWeightsArray.size() < numIndex or cacheOutWeightsAmt == 0)
    {

        // if they exist, dump old weights
        if (allOutWeightsArray.size() > 0)
            allOutWeightsArray.clear();

        for(unsigned int iIndex = 0; iIndex < numIndex; iIndex++ )
        {
            try
            {
                geomArrayHandle.jumpToElement( iIndex );
                success = 1;
            }
            catch(...)
            {
                success = 0;
            }
            // if you find a connection, get the weights
            if (success == 1)
            {
                //iterate
                MDataHandle dhInput = geomArrayHandle.inputValue();
                MDataHandle dhWeightChild = dhInput.child( inputGeom );
                MItGeometry iter(dhWeightChild, true );
                unsigned int iterGeoCount = iter.count();
                if (iterGeoCount > 0)
                {

                    std::vector < std::vector < MDoubleArray > > tmpAllWeightsArray;
                    for(j = 0; j < allWeightsArray[iIndex].size(); j++ )
                    {
                        //2-d array
    //                    std::vector < std::vector < double > > tempUVals;
                        std::vector < MDoubleArray > tempWeightsArray;
                        for(k = 0; k < allWeightsArray[iIndex][j].size(); k++ )
                        {
                            //1-d array
    //                        std::vector < double > tempUPointVals;
                            MDoubleArray tmpWeights;
                            for(unsigned int idx = 0; idx < iterGeoCount; idx++ )

                            {

//                                unsigned int idx = iter.index();
                                double tmpW;


                                //paint weights check
                                if (allWeightsArray.size() > iIndex )
                                {
                                    if (allWeightsArray[iIndex].size() > j )
                                    {
                                        if (allWeightsArray[iIndex][j].size() > k )
                                        {
                                            if (allWeightsArray[iIndex][j][k].length() > idx )
                                            {
                                                tmpW = allWeightsArray[iIndex][j][k][idx];
//                                                MGlobal::displayInfo(MString("No Fail")+idx +allWeightsArray[iIndex][j][k][idx]+allUAnimCurveWeights[iIndex][j][k][idx]+allVAnimCurveWeights[iIndex][j][k][idx]);
                                            }
                                            else
                                            {
                                                tmpW = 1.0;
//                                                    float myfloat = fabs(allWeightsArray[0][0][0].length());
//                                                    MGlobal::displayInfo(MString("Fail 4")+allWeightsArray.size()+allUAnimCurveWeights.size()+allVAnimCurveWeights.size()+iIndex);
                                            }
                                        }
                                        else
                                        {
                                            tmpW = 1.0;
//                                            MGlobal::displayInfo(MString("Fail 3"));
                                        }
                                    }
                                    else
                                    {
                                        tmpW = 1.0;
//                                        MGlobal::displayInfo(MString("Fail 2"));
                                    }
                                }
                                else
                                {
                                    tmpW = 1.0;
//                                    MGlobal::displayInfo(MString("Fail 1"));
                                }

                                //animcurveWeights
                                if (allUAnimCurveWeights.size() > iIndex and allVAnimCurveWeights.size() > iIndex)
                                {
                                    if (allUAnimCurveWeights[iIndex].size() > j and allVAnimCurveWeights[iIndex].size() > j)
                                    {
                                        if (allUAnimCurveWeights[iIndex][j].size() > k and allVAnimCurveWeights[iIndex][j].size() > k)
                                        {
                                            if (allUAnimCurveWeights[iIndex][j][k].size() > idx and allVAnimCurveWeights[iIndex][j][k].size() > idx)
                                            {
                                                tmpW = tmpW*
                                                        allUAnimCurveWeights[iIndex][j][k][idx] *
                                                        allVAnimCurveWeights[iIndex][j][k][idx];
                                            }
                                            else
                                            {
                                                tmpW = tmpW*1.0;
//                                                    float myfloat = fabs(allWeightsArray[0][0][0].length());
//                                                    MGlobal::displayInfo(MString("Fail 4")+allWeightsArray.size()+allUAnimCurveWeights.size()+allVAnimCurveWeights.size()+iIndex);
                                            }
                                        }
                                        else
                                        {
                                            tmpW = tmpW*1.0;
//                                            MGlobal::displayInfo(MString("Fail 3"));
                                        }
                                    }
                                    else
                                    {
                                        tmpW = tmpW*1.0;
//                                        MGlobal::displayInfo(MString("Fail 2"));
                                    }
                                }
                                else
                                {
                                    tmpW = tmpW*1.0;
//                                    MGlobal::displayInfo(MString("Fail 1"));
                                }
                                tmpWeights.append(tmpW);
//                                iter.next();
                            }

                            tempWeightsArray.push_back(tmpWeights);
                        }
                        tmpAllWeightsArray.push_back(tempWeightsArray);
                    }
                    allOutWeightsArray.push_back(tmpAllWeightsArray);
                }
            }
        }
//        float myfloat = fabs(allOutWeightsArray[0][0][0][0]);
//        MGlobal::displayInfo(MString("Fail 4")+myfloat);
        MObject allOutWeightParentArrays[]= {aOutWeightsParentArray};
        MObject allOutWeightParents[] = {aOutWeightsParent};
        MObject allOutWeightChildren[] = {aOutWeights};
        for(unsigned int i = 0; i < numIndex; i++ )
        {
            if (allOutWeightsArray.size() > i)
            {
                for(j = 0; j < 1; j++ )
                {
                    if (allOutWeightsArray[i].size() > j)
                    {
                        MPlug weightArrayCheck(thisMObj, allOutWeightParentArrays[j] );
                        MIntArray connectedArray;
                        weightArrayCheck.getExistingArrayAttributeIndices(connectedArray);
                        if (weightArrayCheck.numConnectedChildren() > 0)
                        {
                            for(k = 0; k < connectedArray.length(); k++ )
                            {
                                if (allOutWeightsArray[i][j].size() > k)
                                {
//                                    MGlobal::displayInfo(MString()+connectedArray.length());
                                    MArrayDataHandle arrayHandleParentParent(data.outputArrayValue( allOutWeightParentArrays[j], &status  ));
                //                    CheckStatusReturn( status, "Unable to get outputs" );
                                    status = arrayHandleParentParent.jumpToArrayElement(connectedArray[k]);
                                    CheckStatusReturn( status, "Unable to jump to element" );
                                    //parent
                                    MDataHandle hArrayHandleParent = arrayHandleParentParent.outputValue().child(allOutWeightParents[j]);
                                    MArrayDataHandle hArrayHandleParentArray(hArrayHandleParent);

                                    //child
                                    hArrayHandleParentArray.jumpToElement(i);
                                    MDataHandle handle(hArrayHandleParentArray.outputValue(&status) );
                                    CheckStatusReturn( status, "Unable to get parent output" );
                                    MDataHandle child(handle.child( allOutWeightChildren[j] ) );
                                    MFnDoubleArrayData weightsData;
                                    MObject oWeights = weightsData.create(allOutWeightsArray[i][j][k], &status);
                                    CheckStatusReturn( status, "Unable to make out weights MObject" );
                                    status = child.setMObject(oWeights);
                                    child.setClean();
                                    CheckStatusReturn( status, "Unable to set weights" );
//                                    MGlobal::displayInfo(MString("setIT")+k);
                                }
                            }
                        }
                    }
                }
            }
        }



    }

    return MS::kSuccess;
}

MStatus LHWeightDeformer::initialize() {

    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    ///////////////////////////////////////////
    /////////////// INPUTS ////////////////////
    ///////////////////////////////////////////



    ////////// typed attributes ////////////

    // surface
    // weight patchall
    aWeightMesh = tAttr.create("weightPatch", "wp", MFnData::kMesh);
    addAttribute( aWeightMesh );


    // cache attributes

    aCacheWeights = nAttr.create("cacheWeights", "cw", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheWeights);

    aCacheOutWeights = nAttr.create("cacheOutputWeights", "cow", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheOutWeights);

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



    //---child weight
    aWeights = tAttr.create("pointWeight", "pweight", MFnNumericData::kDoubleArray);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
//    tAttr.setInternal(true);


    //---parent weight
    aWeightsParent = cAttr.create("weightsParent", "wsp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);

    //---parentParent weight
    aWeightsParentArray = cAttr.create("weightsParentArray", "wpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aWeightsParentArray);

    //child anim curve
    aUAnimCurve = nAttr.create("uAnimCurve", "uac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);

    //parent anim curve
    aUAnimCurveParent = cAttr.create("uAnimCurveArray", "uaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUAnimCurve );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUAnimCurveParent);

    aVAnimCurve = nAttr.create("vAnimCurve", "vac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);

    aVAnimCurveParent = cAttr.create("vAnimCurveArray", "vaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVAnimCurve );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVAnimCurveParent);


    ////////////////////////////////////////////////////////////////////////////
    ////////////////// OUTPUTS /////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////

    //---child weight
    aOutWeights = tAttr.create("outWeights", "ow", MFnNumericData::kDoubleArray);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
//    tAttr.setInternal(true);

    //---parent weight
    aOutWeightsParent = cAttr.create("outWeightsParent", "owp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aOutWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);

    //---parentParent weight
    aOutWeightsParentArray = cAttr.create("outWeightsParentArray", "owpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aOutWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutWeightsParentArray);



    //////Affects outputs and inputs

//    MObject outputGeom = MPxDeformerNode::outputGeom;


//    attributeAffects(aOutWeightsParentArray,outputGeom);

    attributeAffects(aWeightMesh,aOutWeightsParentArray);

    attributeAffects(aCacheWeights, aOutWeightsParentArray);
    attributeAffects(aCacheWeightMesh, aOutWeightsParentArray);
    attributeAffects(aCacheWeightCurves, aOutWeightsParentArray);

    attributeAffects(aWeightsParentArray, aOutWeightsParentArray);
    attributeAffects(aUAnimCurveParent, aOutWeightsParentArray);
    attributeAffects(aVAnimCurveParent, aOutWeightsParentArray);





    attributeAffects(aWeightMesh,aOutWeights);

    attributeAffects(aCacheWeights, aOutWeights);
    attributeAffects(aCacheWeightMesh, aOutWeights);
    attributeAffects(aCacheWeightCurves, aOutWeights);

    attributeAffects(aWeightsParentArray, aOutWeights);
    attributeAffects(aUAnimCurveParent, aOutWeights);
    attributeAffects(aVAnimCurveParent, aOutWeights);



    attributeAffects(aWeightMesh,aOutWeightsParent);

    attributeAffects(aCacheWeights, aOutWeightsParent);
    attributeAffects(aCacheWeightMesh, aOutWeightsParent);
    attributeAffects(aCacheWeightCurves, aOutWeightsParent);

    attributeAffects(aWeightsParentArray, aOutWeightsParent);
    attributeAffects(aUAnimCurveParent, aOutWeightsParent);
    attributeAffects(aVAnimCurveParent, aOutWeightsParent);




//    attributeAffects(aCacheWeights, outputGeom);
//    attributeAffects(aCacheWeightMesh, outputGeom);
//    attributeAffects(aCacheWeightCurves, outputGeom);
//
//    attributeAffects(aWeightsParentArray, outputGeom);
//    attributeAffects(aUAnimCurveParent, outputGeom);
//    attributeAffects(aVAnimCurveParent, outputGeom);



    // Make deformer weights paintable


//    MGlobal::executeCommand("makePaintable -attrType multiFloat -shapeMode deformer LHWeightDeformer weights;");

    // Make deformer weights paintable

  return MS::kSuccess;
}