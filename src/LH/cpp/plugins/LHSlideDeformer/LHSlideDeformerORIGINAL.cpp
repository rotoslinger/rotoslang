//    float myfloat = fabs(allWeightsArray[0][0][0].length());
//    MGlobal::displayInfo(MString()+myfloat);

#include "LHSlideDeformer.h"

MTypeId LHSlideDeformer::id(0x00008017);

// tAttrs
MObject LHSlideDeformer::aSurface;
MObject LHSlideDeformer::aSurfaceBase;
MObject LHSlideDeformer::aWeightMesh;
// nAttrs
MObject LHSlideDeformer::aRotationAmount;
MObject LHSlideDeformer::aScaleAmount;
//////// cache attrs ////////
MObject LHSlideDeformer::aCachePivots;
MObject LHSlideDeformer::aCacheWeights;
MObject LHSlideDeformer::aCacheParams;
MObject LHSlideDeformer::aCacheWeightMesh;
MObject LHSlideDeformer::aCacheWeightCurves;
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
MObject LHSlideDeformer::aUAnimCurveU;
MObject LHSlideDeformer::aUAnimCurveUParent;

//UV
MObject LHSlideDeformer::aUAnimCurveV;
MObject LHSlideDeformer::aUAnimCurveVParent;

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
MObject LHSlideDeformer::aVAnimCurveU;
MObject LHSlideDeformer::aVAnimCurveUParent;

//UV
MObject LHSlideDeformer::aVAnimCurveV;
MObject LHSlideDeformer::aVAnimCurveVParent;

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
MObject LHSlideDeformer::aNAnimCurveU;
MObject LHSlideDeformer::aNAnimCurveUParent;

//NV
MObject LHSlideDeformer::aNAnimCurveV;
MObject LHSlideDeformer::aNAnimCurveVParent;
//////////////// R ////////////////////////////
//R Values

MObject LHSlideDeformer::aRValue;
MObject LHSlideDeformer::aRValueParent;

// RWeights
MObject LHSlideDeformer::aRWeights;
MObject LHSlideDeformer::aRWeightsParent;
MObject LHSlideDeformer::aRWeightsParentArray;

// RAnimCurves
//RU
MObject LHSlideDeformer::aRAnimCurveU;
MObject LHSlideDeformer::aRAnimCurveUParent;
//RV

MObject LHSlideDeformer::aRAnimCurveV;
MObject LHSlideDeformer::aRAnimCurveVParent;
//R Pivots
MObject LHSlideDeformer::aRPivot;
MObject LHSlideDeformer::aRPivotArray;

// OutPuts
MObject LHSlideDeformer::aCacheOutWeights;
MObject LHSlideDeformer::aUOutWeights;
MObject LHSlideDeformer::aUOutWeightsParent;
MObject LHSlideDeformer::aUOutWeightsParentArray;
MObject LHSlideDeformer::aVOutWeights;
MObject LHSlideDeformer::aVOutWeightsParent;
MObject LHSlideDeformer::aVOutWeightsParentArray;
MObject LHSlideDeformer::aNOutWeights;
MObject LHSlideDeformer::aNOutWeightsParent;
MObject LHSlideDeformer::aNOutWeightsParentArray;
MObject LHSlideDeformer::aROutWeights;
MObject LHSlideDeformer::aROutWeightsParent;
MObject LHSlideDeformer::aROutWeightsParentArray;



//////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////// get anim curves ////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////
MStatus LHSlideDeformer::getAnimCurves(
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
    int cachePivotsAmt = data.inputValue(aCachePivots).asInt();
    int cacheWeightsAmt = data.inputValue(aCacheWeights).asInt();
    int cacheOutWeightsAmt = data.inputValue(aCacheOutWeights).asInt();
    int cacheWeightMeshAmt = data.inputValue(aCacheWeightMesh).asInt();
    int cacheWeightCurvesAmt = data.inputValue(aCacheWeightCurves).asInt();
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
                             aNValueParent,
                             aRValueParent};
    MObject allValChildren[]={aUValue,
                              aVValue,
                              aNValue,
                              aRValue};

    std::vector < std::vector <float> > allValsArray;
    len = sizeof(allValParents);
    for (i= 0; i < 4; ++i)
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
            if (intersectYN.size() > 0)
            	intersectYN.clear();

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
                            //project weights based on Mesh
//                            fnWeightMesh.getClosestPoint( pt, weightPt,
//                                                          MSpace::kObject );

                            MPointOnMesh ptOnMesh;
                            fnWeightIntersector.getClosestPoint(pt, ptOnMesh);
                            weightPt = ptOnMesh.getPoint();
//                            MVector rayDirection(0.0,0.0,0.0);
//                            fnWeightMesh.getClosestNormal( pt, rayDirection,
//                                                           MSpace::kObject );
//                            MFloatVector rayFloatDirection(rayDirection[0],
//                                                         rayDirection[1],
//                                                           rayDirection[2]);
//                            MFloatPoint rayFloatPt(pt.x, pt.y, pt.z);
//                            // find out if point falls within the coverage of the mesh
//                            MFloatPoint hitPt(0.0,0.0,0.0);
//                            bool intersectYN = fnWeightMesh.anyIntersection( rayFloatPt,
//                                                                        rayFloatDirection,
//                                                                        NULL, NULL, false,
//                                                                        MSpace::kObject,
//                                                                        100.0, true, NULL,
//                                                                        hitPt, NULL, NULL,
//                                                                        NULL, NULL, NULL,
//                                                                        0.00001);
                            // we need to chart each point to the weight mesh's uvs
                            // it is important for the mesh to have clean nurbs-like 0-1 uvs
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

	// cache r pivots
	////////////////////////////////////////////////////////////////////
	////////   get rotate pivots    ////////
	////////////////////////////////////////////////////////////////////
	MArrayDataHandle pivArrayHandle(data.inputArrayValue( aRPivotArray ));
	unsigned int pivCount = pivArrayHandle.elementCount();
	MPlug pivCheckPlug(thisMObj, aRPivotArray );
	int pivCheck;
	if (pivCheckPlug.numConnectedChildren() > 0)
	{
		pivCheck = 1;
	}
	else
		pivCheck = 0;
	if (pivCheck > 0)
	{
		if(rotatePivots.size() < numIndex || cachePivotsAmt == 0)
		{
            if (rotatePivots.size() > 0)
            	rotatePivots.clear();
            if (rotUParams.size() > 0)
            	rotUParams.clear();
            if (rotVParams.size() > 0)
            	rotVParams.clear();

			for(i = 0; i < numIndex; i++ )
			{
				MPointArray tmpRotatePivots;
				std::vector <double> tmpRotUParams;
				std::vector <double> tmpRotVParams;
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
					for (j=0; j < pivCount; j++)
					{
						pivArrayHandle.jumpToElement(j);
						MObject oTempCurve = pivArrayHandle.inputValue().child( aRPivot ).asNurbsCurveTransformed();
						MFnNurbsCurve fnNurbsCurve( oTempCurve );
						MPointArray curvePoints;
						fnNurbsCurve.getCVs(curvePoints, MSpace::kObject);
						MPoint point = curvePoints[0];

						tmpRotatePivots.append(point);
					rotatePivots.push_back(tmpRotatePivots);
					////////////////////////////////////////////////////////////////////////////////
					////////   get closest rotate pivots    ////////
					////////////////////////////////////////////////////////////////////////////////

					}

					//in order to get the rotate pivot when it falls outside the mesh you can find the
					for (j = 0; j < rotatePivots[i].length(); j++)
					{
						fnSurfaceBase.closestPoint( rotatePivots[i][j], &tmpU,
													&tmpV, false, 0.00001,
													MSpace::kObject );
						tmpRotUParams.push_back(tmpU);
						tmpRotVParams.push_back(tmpV);
					}
					rotUParams.push_back(tmpRotUParams);
					rotVParams.push_back(tmpRotVParams);

				}
				else if (success == 0)
				{
					tmpRotatePivots.append( 0.0, 0.0, 0.0 );
					rotatePivots.push_back(tmpRotatePivots);

					tmpRotUParams.push_back(0.0);
					tmpRotVParams.push_back(0.0);

					rotUParams.push_back( tmpRotUParams );
					rotVParams.push_back( tmpRotVParams );
				}
			}
		}
	}
	rotatePivotsLength = rotatePivots[mIndex].length();
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
                                          aNWeightsParentArray,
                                          aRWeightsParentArray};
        MObject allWeightParents[] = {aUWeightsParent,
                                      aVWeightsParent,
                                      aNWeightsParent,
                                      aRWeightsParent};
        MObject allWeightChildren[] = {aUWeights,
                                       aVWeights,
                                       aNWeights,
                                       aRWeights};

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
                for(j = 0; j < 4; j++ )
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
//    float myfloat = fabs(allWeightsArray[0][0][0].length());
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

            MObject allAnimCurveUParents[] = {aUAnimCurveUParent,
                                              aVAnimCurveUParent,
                                              aNAnimCurveUParent,
                                              aRAnimCurveUParent};
            MObject allAnimCurveUChildren[] = {aUAnimCurveU,
                                               aVAnimCurveU,
                                               aNAnimCurveU,
                                               aRAnimCurveU};
            MObject allAnimCurveVParents[] = {aUAnimCurveVParent,
                                              aVAnimCurveVParent,
                                              aNAnimCurveVParent,
                                              aRAnimCurveVParent};
            MObject allAnimCurveVChildren[] = {aUAnimCurveV,
                                               aVAnimCurveV,
                                               aNAnimCurveV,
                                               aRAnimCurveV};
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
                    for(j = 0; j < 4; j++ )
                    {
                        //tmp 1-ds
                        std::vector <float> tmpUTimeLength,tmpVTimeLength;
                        std::vector <float> tmpUTimeOffset,tmpVTimeOffset;
                        std::vector <MFnAnimCurve*> tmpUAnimCurves,tmpVAnimCurves;

                        try
                        {
                            //U
                            status = LHSlideDeformer::getAnimCurves(thisMObj,
                                          allAnimCurveUParents[j],
                                          allAnimCurveUChildren[j],
                                          tmpUTimeLength,tmpUTimeOffset,
                                          tmpUAnimCurves);
                            //V
                            status = LHSlideDeformer::getAnimCurves(thisMObj,
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
//                                        remap = OpenMaya.MTime(remap);
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
//                        fnSurfaceBase.getDerivativesAtParm( slideUBasePtParam[i][idx],
//                                                            slideVBasePtParam[i][idx],
//                                                            fakePt, xVecBase, yVecBase,
//                                                            MSpace::kObject,
//                                                            &fakePt2, &fakeVecU, &fakeVecV);
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


    ////////////////////////////////////////////////////////////////////
    ////////   set all output weights (cache if specified)      ////////
    ////////////////////////////////////////////////////////////////////

//    MPlug weightCheck(thisMObj, aUWeightsParentArray );
//    unsigned int weightSize = weightCheck.numConnectedChildren();
/*
    if (allOutWeightsArray.size() < numIndex or cacheOutWeightsAmt == 0)
    {

        // if they exist, dump old weights
        if (allOutWeightsArray.size() > 0)
            allOutWeightsArray.clear();

        for(unsigned int iIndex = 0; iIndex < numIndex; iIndex++ )
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
                //iterate
                MDataHandle dhInput = geomArrayHandle.inputValue();
                MDataHandle dhWeightChild = dhInput.child( inputGeom );
                MItGeometry iter(dhWeightChild, true );
                unsigned int iterGeoCount = iter.count();
                if (iterGeoCount > 0)
                {
                    MDoubleArray uOutWeight;
                    MDoubleArray vOutWeight;
                    MDoubleArray rOutWeight;
                    MDoubleArray nOutWeight;

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
                            for (; !iter.isDone();)
                            {

                                unsigned int idx = iter.index();
                                double tmpW;
                                if (allWeightsArray.size() > iIndex and allUAni                        normal = fnSurfaceBase.normal( slideUBasePtParam[i][idx], slideVBasePtParam[i][idx], MSpace::kObject );
                                mCurveWeights.size() > iIndex and allVAnimCurveWeights.size() > iIndex)
                                {
                                    if (allWeightsArray[iIndex].size() > j and allUAnimCurveWeights[iIndex].size() > j and allVAnimCurveWeights[iIndex].size() > j)
                                    {
                                        if (allWeightsArray[iIndex][j].size() > j and allUAnimCurveWeights[iIndex][j].size() > j and allVAnimCurveWeights[iIndex][j].size() > j)
                                        {
                                            if (allWeightsArray[iIndex][j][k].length() > idx and allUAnimCurveWeights[iIndex][j][k].size() > idx and allVAnimCurveWeights[iIndex][j][k].size() > idx)
                                            {
                                                tmpW = allWeightsArray[iIndex][j][k][idx]*
                                                        allUAnimCurveWeights[iIndex][j][k][idx] *
                                                        allVAnimCurveWeights[iIndex][j][k][idx];
//                                                MGlobal::displayInfo(MString("No Fail"));
                                            }
                                            else
                                            {
                                                tmpW = 1.0;
//                                                    float myfloat = fabs(allWeightsArray[0][0][0].length());
//                                                    MGlobal::displayInfo(MString("Fail 4"));
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
                                tmpWeights.append(tmpW);
                                if (idx == 525)
                                {
//                                    float myfloat = tmpW;
//                                    MGlobal::displayInfo(MString()+myfloat);
                                }
                                iter.next();
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
        MObject allOutWeightParentArrays[]= {aUOutWeightsParentArray,
                                          aVOutWeightsParentArray,
                                          aNOutWeightsParentArray,
                                          aROutWeightsParentArray};
        MObject allOutWeightParents[] = {aUOutWeightsParent,
                                      aVOutWeightsParent,
                                      aNOutWeightsParent,
                                      aROutWeightsParent};
        MObject allOutWeightChildren[] = {aUOutWeights,
                                       aVOutWeights,
                                       aNOutWeights,
                                       aROutWeights};
        for(unsigned int i = 0; i < numIndex; i++ )
        {
            for(j = 0; j < 4; j++ )
            {
//                MPlug weightArrayCheck(thisMObj, allOutWeightParentArrays[j] );
//                MIntArray connectedArray;
//                MArrayDataHandle arrayHandleParentParent(data.outputArrayValue( allOutWeightParentArrays[j], &status ));
//                CheckStatusReturn( status, "Unable to get outputs" );
//                weightArrayCheck.getExistingArrayAttributeIndices(connectedArray);


                MPlug weightArrayCheck(thisMObj, allOutWeightParentArrays[i] );
                MIntArray connectedArray;
                weightArrayCheck.getExistingArrayAttributeIndices(connectedArray);
                if (weightArrayCheck.numConnectedChildren() > 0)



//                float myfloat = fabs(connectedArray.length());
//                MGlobal::displayInfo(MString("WORKING")+myfloat);
                if (weightArrayCheck.numConnectedChildren() > 0)
                {
                    for(k = 0; k < connectedArray.length(); k++ )
                    {
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



    //                    MDataHandle child;
    //                    child = handle.child( allOutWeightChildren[j]);

                        MDataHandle child(handle.child( allOutWeightChildren[j] ) );



                        MFnDoubleArrayData newData(child.data(), &status);
    //                    newData(child.data());
                        CheckStatusReturn( status, "Unable to get data" );
                        status = newData.set(allOutWeightsArray[i][j][k]);
                        CheckStatusReturn( status, "Unable to set output weights" );
    //                    float myfloat = fabs(allWeightsArray[0][0][0].length());

//                        child.setClean();
//                                tmp = MFnDoubleArrayData(child.data()).array();
                    }

                }
            }
        }
}


*/

















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
        if (allValsArray.size() != 4)
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



        ////////////////////////////////////////////
        //////// curveWeights ////////
        ////////////////////////////////////////////
        if (weightMeshCheck == 1)
        {

            ////////////////////////////////////////////////////////
            //////////// U V N R combine //////////
            ////////////////////////////////////////////////////////
            uW = 0.0;
            vW = 0.0;
            nW = 0.0;
            rW = 0.0;
            //---Multiply painted weights by curve weights
            // the length of all arrays should be the same
            // this is currently up to the user
            // but I should write a failsafe

            //Make sure all vals is properly filled up
            for(i = 0; i < allVals[0].size(); i++ )
            {
                if (allUAnimCurveWeights[mIndex][0].size() > i and allVAnimCurveWeights[mIndex][0].size() > i)
                {
                    if (allUAnimCurveWeights[mIndex][0][i].size() >= idx+1 and allVAnimCurveWeights[mIndex][0][i].size() >= idx+1)
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
                if (allUAnimCurveWeights[mIndex][1].size() > i and allVAnimCurveWeights[mIndex][1].size() > i)
                {
                    if (allUAnimCurveWeights[mIndex][1][i].size() >= idx+1 and allVAnimCurveWeights[mIndex][1][i].size() >= idx+1)
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

            for(i = 0; i < allVals[2].size(); i++ )
            {
                if (allUAnimCurveWeights[mIndex][2].size() > i and allVAnimCurveWeights[mIndex][2].size() > i)
                {

                    if (allUAnimCurveWeights[mIndex][2][i].size() >= idx+1 and allVAnimCurveWeights[mIndex][2][i].size() >= idx+1)
                    {
                        allVals[2][i] = (allVals[2][i] *
                                         allUAnimCurveWeights[mIndex][2][i][idx] *
                                         allVAnimCurveWeights[mIndex][2][i][idx]);
                    }
                    else
                    {
                        allVals[2][i] = allVals[2][i] * 1.0;
                    }
                }
                else
                {
                    allVals[2][i] = allVals[2][i] * 1.0;
                }
            }
            for(i = 0; i < allVals[3].size(); i++ )
            {
                if (allUAnimCurveWeights[mIndex][3].size() > i and allVAnimCurveWeights[mIndex][3].size() > i)
                {

                    if (allUAnimCurveWeights[mIndex][3][i].size() >= idx+1 and allVAnimCurveWeights[mIndex][3][i].size() >= idx+1)
                    {
                        allVals[3][i] = (allVals[3][i] *
                                         allUAnimCurveWeights[mIndex][3][i][idx] *
                                         allVAnimCurveWeights[mIndex][3][i][idx]);
                    }
                    else
                    {
                        allVals[3][i] = allVals[3][i] * 1.0;
                    }
                }
                else
                {
                    allVals[3][i] = allVals[3][i] * 1.0;
                }
            }


            //sum of val array

            uW = std::accumulate(allVals[0].begin(),allVals[0].end(),0.0);
            vW = std::accumulate(allVals[1].begin(),allVals[1].end(),0.0);
            nW = std::accumulate(allVals[2].begin(),allVals[2].end(),0.0);
            rW = std::accumulate(allVals[3].begin(),allVals[3].end(),0.0);

//            if (intersectYN[mIndex][idx] == false)
//            {
//                uW = 0.0;
//                vW = 0.0;
//                nW = 0.0;
//                rW = 0.0;
//            }


        }


        else if (weightMeshCheck == 0)
        {
            uW = std::accumulate(allVals[0].begin(),allVals[0].end(),0.0);
            vW = std::accumulate(allVals[1].begin(),allVals[1].end(),0.0);
            nW = std::accumulate(allVals[2].begin(),allVals[2].end(),0.0);
            rW = std::accumulate(allVals[3].begin(),allVals[3].end(),0.0);
        }
        if (uW == 0 and vW == 0 and nW == 0)
        {
            MitGeo.next();
            continue;
        }
//        float myfloat = fabs(allVals[0][0]);
//        MGlobal::displayInfo(MString()+myfloat);
//
//        myfloat = fabs(uW);
//        MGlobal::displayInfo(MString()+myfloat);
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

        ////////////////////////////////////////////
        //////////////// slideUV //////////////
        ////////////////////////////////////////////


//        allURotVals = 0.0;
//        allVRotVals = 0.0;
//        rotSlideUValue = 0.0;
//        rotSlideVValue = 0.0;
//        //////////////// rotateUV //////////////
//        uPivOffset = 0.0;
//        vPivOffset = 0.0;
//        if (pivCheck > 0)
//        {
//            for(i = 0; i < rotatePivotsLength; i++ )
////            for i in range(rotatePivotsLength)
//            {
//
//                pivotU = rotUParams[mIndex][i];
//                pivotV = rotVParams[mIndex][i];
//
//                double surfaceRot[] = {slideUCheck-pivotU , slideVCheck-pivotV};
//                double surfaceRotCalc[] =  {(surfaceRot[0] * cos(rW*allVals[3][i])-surfaceRot[1]* sin(rW*allVals[3][i])) , (surfaceRot[0] * sin(rW*allVals[3][i])+surfaceRot[1] * cos(rW*allVals[3][i]))};
//                double surfaceRotPiv[] = {surfaceRotCalc[0]+pivotU , surfaceRotCalc[1]+pivotV};
//
//                slideUCheck = surfaceRotPiv[0];
//                slideVCheck = surfaceRotPiv[1];
//            }
//        }
//            rotSlideUValue = slideUCheck;
//            rotSlideVValue = slideVCheck;
//        if (pivCheck == 0)
//        {
//            rotSlideUValue = slideUCheck;
//            rotSlideVValue = slideVCheck;
//        }
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
//            if (idx == 525)
//            {
////                float myfloat = fabs(allWeightsArray[0][0][0].length());
//                MGlobal::displayInfo(MString()+ slideUBasePointParamValue +MString(" ")+ uMaxParam +MString(" ")+slideVBasePointParamValue);
//            }
            fnSurface.getTangents( slideUBasePointParamValue, slideVBasePointParamValue, xAxisVec, yAxisVec, MSpace::kObject );
//            fnSurface.getDerivativesAtParm( slideUBasePointParamValue,
//                                            slideVBasePointParamValue,
//                                            fakePt, xAxisVec, yAxisVec,
//                                            MSpace::kObject,
//                                            &fakePt2, &fakeVecU, &fakeVecV);
            normal = fnSurface.normal( slideUBasePointParamValue, slideVBasePointParamValue, MSpace::kObject );
    //        xAxisVec = xVec;

    //        yAxisVec = yVec;
            yAxisVec.normalize();

            zAxisVec = normal;
            zAxisVec.normalize();

            xAxisVec = yAxisVec ^ zAxisVec;
            xAxisVec.normalize();
//            yAxisVec = xAxisVec ^ zAxisVec;
//            yAxisVec.normalize();

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

    // weight patchallVals
    aWeightMesh = tAttr.create("weightPatch", "wp", MFnData::kMesh);
    addAttribute( aWeightMesh );


    // cache attributes

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

    aCacheOutWeights = nAttr.create("cacheOutputWeights", "cow", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheOutWeights);

    aCacheParams = nAttr.create("cacheParams", "cpar", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheParams);

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


    aUAnimCurveU = nAttr.create("uAnimCurveU", "uuac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
//    addAttribute(aUAnimCurveU);

    aUAnimCurveUParent = cAttr.create("uAnimCurveUArray", "uuaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUAnimCurveU );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUAnimCurveUParent);

    aUAnimCurveV = nAttr.create("uAnimCurveV", "uvac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
//    addAttribute(aUAnimCurveV);

    aUAnimCurveVParent = cAttr.create("uAnimCurveVArray", "uvaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUAnimCurveV );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUAnimCurveVParent);

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


    aVAnimCurveU = nAttr.create("vAnimCurveU", "vuac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
//    addAttribute(aVAnimCurveU);

    aVAnimCurveUParent = cAttr.create("vAnimCurveUArray", "vuaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVAnimCurveU );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVAnimCurveUParent);

    aVAnimCurveV = nAttr.create("vAnimCurveV", "vvac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
//    addAttribute(aVAnimCurveV);

    aVAnimCurveVParent = cAttr.create("vAnimCurveVArray", "vvaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVAnimCurveV );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVAnimCurveVParent);

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


    aNAnimCurveU = nAttr.create("nAnimCurveU", "nuac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
//    addAttribute(aNAnimCurveU);

    aNAnimCurveUParent = cAttr.create("nAnimCurveUArray", "nuaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNAnimCurveU );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aNAnimCurveUParent);

    aNAnimCurveV = nAttr.create("nAnimCurveV", "nvac", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
//    addAttribute(aNAnimCurveV);

    aNAnimCurveVParent = cAttr.create("nAnimCurveVArray", "nvaca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNAnimCurveV );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aNAnimCurveVParent);


    //////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////// R Attrs ////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////

    aRValue = nAttr.create("rValue", "rv", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);
//    addAttribute(aRValue);

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
//    addAttribute(aRWeights);

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
//    addAttribute(aRWeightsParent);

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
//    addAttribute(aRAnimCurveU);

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
//    addAttribute(aRAnimCurveV);

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
//    addAttribute( aRPivot );

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

    ///////////////////////////////////////////
    /////////////// OUTPUTS ///////////////////
    ///////////////////////////////////////////

    ///////////// U Outputs

    //child
    aUOutWeights = tAttr.create("uOutWeights", "uo", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
//    addAttribute(aUOutWeights);

    //Parent
    aUOutWeightsParent = cAttr.create("uOutWeightsParent", "uowp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUOutWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aUOutWeightsParent);

    //ParentParent
    aUOutWeightsParentArray = cAttr.create("uOutWeightsParentArray", "uowpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUOutWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUOutWeightsParentArray);

    ///////////// V Outputs

    //child
    aVOutWeights = tAttr.create("vOutWeights", "vo", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
//    addAttribute(aVOutWeights);

    //Parent
    aVOutWeightsParent = cAttr.create("vOutWeightsParent", "vowp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVOutWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aVOutWeightsParent);

    //ParentParent
    aVOutWeightsParentArray = cAttr.create("vOutWeightsParentArray", "vowpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVOutWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVOutWeightsParentArray);

    ///////////// N Outputs

    //child
    aNOutWeights = tAttr.create("nOutWeights", "no", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
//    addAttribute(aNOutWeights);

    //Parent
    aNOutWeightsParent = cAttr.create("nOutWeightsParent", "nowp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNOutWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aNOutWeightsParent);

    //ParentParent
    aNOutWeightsParentArray = cAttr.create("nOutWeightsParentArray", "nowpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNOutWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aNOutWeightsParentArray);

    ///////////// R Outputs

    //child
    aROutWeights = tAttr.create("rOutWeights", "ro", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
//    addAttribute(aROutWeights);

    //Parent
    aROutWeightsParent = cAttr.create("rOutWeightsParent", "rowp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aROutWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
//    addAttribute(aROutWeightsParent);

    //ParentParent
    aROutWeightsParentArray = cAttr.create("rOutWeightsParentArray", "rowpa");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aROutWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aROutWeightsParentArray);


    //////Affects outputs and inputs

    MObject outputGeom = MPxDeformerNode::outputGeom;

    // tAttrs
    attributeAffects(aSurface, outputGeom);
    attributeAffects(aSurfaceBase, outputGeom);
    attributeAffects(aWeightMesh, outputGeom);

    // nAttrs

    attributeAffects(aRotationAmount, outputGeom);
    attributeAffects(aScaleAmount, outputGeom);


    attributeAffects(aCachePivots, outputGeom);
    attributeAffects(aCacheWeights, outputGeom);
    attributeAffects(aCacheParams, outputGeom);
    attributeAffects(aCacheWeightMesh, outputGeom);
    attributeAffects(aCacheWeightCurves, outputGeom);
    attributeAffects(aCacheBase, outputGeom);


    // U ATTRS

//    attributeAffects(aUValue, outputGeom);
    attributeAffects(aUValueParent, outputGeom);

//    attributeAffects(aUWeights, outputGeom);
//    attributeAffects(aUWeightsParent, outputGeom);
    attributeAffects(aUWeightsParentArray, outputGeom);

//    attributeAffects(aUAnimCurveU, outputGeom);
    attributeAffects(aUAnimCurveUParent, outputGeom);

//    attributeAffects(aUAnimCurveV, outputGeom);
    attributeAffects(aUAnimCurveVParent, outputGeom);

    // V ATTRS

//    attributeAffects(aVValue, outputGeom);
    attributeAffects(aVValueParent, outputGeom);

//    attributeAffects(aVWeights, outputGeom);
//    attributeAffects(aVWeightsParent, outputGeom);
    attributeAffects(aVWeightsParentArray, outputGeom);


//    attributeAffects(aVAnimCurveU, outputGeom);
    attributeAffects(aVAnimCurveUParent, outputGeom);

//    attributeAffects(aVAnimCurveV, outputGeom);
    attributeAffects(aVAnimCurveVParent, outputGeom);

    // N ATTRS

//    attributeAffects(aNValue, outputGeom);
    attributeAffects(aNValueParent, outputGeom);

//    attributeAffects(aNWeights, outputGeom);
//    attributeAffects(aNWeightsParent, outputGeom);
    attributeAffects(aNWeightsParentArray, outputGeom);


//    attributeAffects(aNAnimCurveU, outputGeom);
    attributeAffects(aNAnimCurveUParent, outputGeom);

//    attributeAffects(aNAnimCurveV, outputGeom);
    attributeAffects(aNAnimCurveVParent, outputGeom);

    // R ATTRS

//    attributeAffects(aRValue, outputGeom);
    attributeAffects(aRValueParent, outputGeom);

//    attributeAffects(aRWeights, outputGeom);
//    attributeAffects(aRWeightsParent, outputGeom);
    attributeAffects(aRWeightsParentArray, outputGeom);


//    attributeAffects(aRAnimCurveU, outputGeom);
    attributeAffects(aRAnimCurveUParent, outputGeom);

//    attributeAffects(aRAnimCurveV, outputGeom);
    attributeAffects(aRAnimCurveVParent, outputGeom);

//    attributeAffects(aRPivot, outputGeom);
    attributeAffects(aRPivotArray, outputGeom);

    ///Outputs

    attributeAffects(aCacheOutWeights, outputGeom);
    attributeAffects(aCacheOutWeights, aUOutWeightsParentArray);
    attributeAffects(aCacheOutWeights, aVOutWeightsParentArray);
    attributeAffects(aCacheOutWeights, aNOutWeightsParentArray);
    attributeAffects(aCacheOutWeights, aROutWeightsParentArray);

    attributeAffects(aUWeightsParentArray, aUOutWeightsParentArray);
    attributeAffects(aUAnimCurveUParent, aUOutWeightsParentArray);
    attributeAffects(aUAnimCurveVParent, aUOutWeightsParentArray);

    attributeAffects(aVWeightsParentArray, aVOutWeightsParentArray);
    attributeAffects(aVAnimCurveUParent, aVOutWeightsParentArray);
    attributeAffects(aVAnimCurveVParent, aVOutWeightsParentArray);

    attributeAffects(aNWeightsParentArray, aNOutWeightsParentArray);
    attributeAffects(aNAnimCurveUParent, aNOutWeightsParentArray);
    attributeAffects(aNAnimCurveVParent, aNOutWeightsParentArray);

    attributeAffects(aRWeightsParentArray, aROutWeightsParentArray);
    attributeAffects(aRAnimCurveUParent, aROutWeightsParentArray);
    attributeAffects(aRAnimCurveVParent, aROutWeightsParentArray);

    // Make deformer weights paintable


    MGlobal::executeCommand("makePaintable -attrType multiFloat -shapeMode deformer LHSlideDeformer weights;");

    // Make deformer weights paintable

  return MS::kSuccess;
}
