#include "rnkCurveDeformer.h"
#include <maya/MFnPlugin.h>

MTypeId rnkCurveDeformer::id(0x00007019);
// curves
MObject rnkCurveDeformer::aCurve;
MObject rnkCurveDeformer::aAimCurve;
MObject rnkCurveDeformer::aCurveBase;
MObject rnkCurveDeformer::aAimCurveBase;
// attributes
MObject rnkCurveDeformer::aRotationAmount;
MObject rnkCurveDeformer::aRevolveAmount;
MObject rnkCurveDeformer::aFalloff;
MObject rnkCurveDeformer::aScale;
MObject rnkCurveDeformer::aMaintainVolume;
MObject rnkCurveDeformer::aSlide;
// Weights
MObject rnkCurveDeformer::aRotationWeights;
MObject rnkCurveDeformer::aRevolveWeights;
MObject rnkCurveDeformer::aScaleWeights;
MObject rnkCurveDeformer::aVolumeWeights;
MObject rnkCurveDeformer::aSlideWeights;
// WeightParents
MObject rnkCurveDeformer::aRotationWeightsParent;
MObject rnkCurveDeformer::aRevolveWeightsParent;
MObject rnkCurveDeformer::aScaleWeightsParent;
MObject rnkCurveDeformer::aVolumeWeightsParent;
MObject rnkCurveDeformer::aSlideWeightsParent;

//Cache attributes
MObject rnkCurveDeformer::aCacheParams;
MObject rnkCurveDeformer::aCacheWeights;
MObject rnkCurveDeformer::aCacheBase;
MObject rnkCurveDeformer::aContinuousSlide;


void* rnkCurveDeformer::creator() { return new rnkCurveDeformer; }

MStatus rnkCurveDeformer::deform(MDataBlock& data, MItGeometry& MitGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
    MObject thisMObj( thisMObject() );
    MStatus status;
    MSyntax syntax;
    // envelope
    float envelope = data.inputValue(MPxDeformerNode::envelope).asFloat();

   //////////// get highest index in array //////////////////

    MPlug inPlug(thisMObj, input);
    inPlug.getExistingArrayAttributeIndices(indices,&status);
    MyCheckStatusReturn( status, "Unable to get NumIndexes" );

    indicesLength = indices.length();

    //vector <int> Test;
    //int myints[] = {1,4,7,4};

    //loop to put indices into test std vector

    for( index = 0; index < indicesLength; ++index)
    {
        indexIntArray.push_back(indices[index]);
    }

    //status = indices.get(Test);
        //MIntArray indices;

    //if index length = 1
    if (indicesLength == 1)
       numIndex = indices[0]+1;
    if (indicesLength == 2)
       numIndex = max(indices[0],indices[1])+1;
    if (indicesLength >= 3)
       //numIndex = *(max_element(indices[0], indices[3]));
       numIndex = *(max_element(indexIntArray.begin(), indexIntArray.end()))+1;

////////////////////////Create point arrays for output geoms////////////////////

    int cacheWeights = data.inputValue( aCacheWeights ).asInt();
    int cacheParams = data.inputValue( aCacheParams ).asInt();
    int cacheBase = data.inputValue( aCacheBase ).asInt();
    int countinuousSlide = data.inputValue( aContinuousSlide ).asInt();

    float rotationAmount = data.inputValue(aRotationAmount).asFloat();
    float RevolveAmount = data.inputValue(aRevolveAmount).asFloat();
    //float falloff = data.inputValue(aFalloff).asFloat();
    float scale = data.inputValue(aScale).asFloat();
    float volume = data.inputValue(aMaintainVolume).asFloat();
    float slide = data.inputValue(aSlide).asFloat();

    // curves
    MObject oCurve = data.inputValue(aCurve).asNurbsCurve();
    MObject oAimCurve = data.inputValue(aAimCurve).asNurbsCurve();
    MObject oCurveBase = data.inputValue(aCurveBase).asNurbsCurve();
    MObject oAimCurveBase = data.inputValue(aAimCurveBase).asNurbsCurve();

    if ((oCurve.isNull()) || (oAimCurve.isNull()) || (oCurveBase.isNull()) || (oAimCurveBase.isNull())) {
        return MS::kSuccess;
    }

// Test new method to get dag path

    //Get Curve
    MDataHandle dhCurve = data.inputValue( aCurve );
    MDagPath fnCurvePath = getConnectedDagNode(thisMObj, rnkCurveDeformer::aCurve );
    MDagPath dagPathCurve;
    fnCurvePath.getPath(dagPathCurve);
    dagPathCurve.extendToShape();
    MFnNurbsCurve fnCurve( dagPathCurve,  &status );
    MyCheckStatusReturn( status, "Unable to Make curve" );

    //Get AimCurve
    MDataHandle dhAimCurve = data.inputValue( aAimCurve );
    MDagPath fnAimCurvePath = getConnectedDagNode(thisMObj, rnkCurveDeformer::aAimCurve );
    MDagPath dagPathAimCurve;
    fnAimCurvePath.getPath(dagPathAimCurve);
    dagPathAimCurve.extendToShape();
    MFnNurbsCurve fnAimCurve( dagPathAimCurve,  &status );
    MyCheckStatusReturn( status, "Unable to Make aimCurve" );

    //Get CurveBase
    MDataHandle dhCurveBase = data.inputValue( aCurveBase );
    MDagPath fnCurveBasePath = getConnectedDagNode(thisMObj, rnkCurveDeformer::aCurveBase );
    MDagPath dagPathCurveBase;
    fnCurveBasePath.getPath(dagPathCurveBase);
    dagPathCurveBase.extendToShape();
    MFnNurbsCurve fnCurveBase( dagPathCurveBase,  &status );
    MyCheckStatusReturn( status, "Unable to Make curveBase" );

    //Get AimCurveBase
    MDataHandle dhAimCurveBase = data.inputValue( aAimCurveBase );
    MDagPath fnAimCurveBasePath = getConnectedDagNode(thisMObj, rnkCurveDeformer::aAimCurveBase );
    MDagPath dagPathAimCurveBase;
    fnAimCurveBasePath.getPath(dagPathAimCurveBase);
    dagPathAimCurveBase.extendToShape();
    MFnNurbsCurve fnAimCurveBase( dagPathAimCurveBase,  &status );
    MyCheckStatusReturn( status, "Unable to Make aimCurveBase" );

    ///////////////////////////////////////////////////////////////
    //////////////// Cache as much ish as possible ////////////////
    ///////////////////////////////////////////////////////////////
    
	if(rotationWeightsArray.size() < numIndex)
	{

		{
		    if (rotationWeightsArray.size() > 0)
    		{
    		    rotationWeightsArray.clear();
    		}
		    if (revolveWeightsArray.size() > 0)
    		{
    		    revolveWeightsArray.clear();
    		}
		    if (scaleWeightsArray.size() > 0)
    		{
    		    scaleWeightsArray.clear();
    		}
		    if (volumeWeightsArray.size() > 0)
    		{
    		    volumeWeightsArray.clear();
    		}
		    if (slideWeightsArray.size() > 0)
    		{
    		    slideWeightsArray.clear();
    		}

    		for( index = 0; index < numIndex; ++index)
    		{

                /////////////////////////////////////////////////////////////////////////////////////////////////////////////
                //Find out how many points are in each piece of geo that will be deformed, if non fail safely and create a dummy count of 0
                MPlug inPlug(thisMObj, input);
                MArrayDataHandle ahInput = data.inputArrayValue(input, &status) ;
                MyCheckStatusReturn( status, "Unable to Make ahInput" );
                try
                {
                    status = ahInput.jumpToElement( index ) ;
                }
                catch(...)
                {
                    iterGeoCount = 0;
                }

                if (status == MS::kSuccess)
                {
                    // if status fails set array to 0
                    MDataHandle dhInput = ahInput.inputValue(&status) ;
                    MyCheckStatusReturn( status, "Unable to dhInput" );

                	MDataHandle dhWeightChild = dhInput.child( inputGeom ) ;
                	MyCheckStatusReturn( status, "Unable to ahWeightChild" );


                    MItGeometry iter( dhWeightChild, true, &status );
                    iterGeoCount = iter.count(&status);
                    MyCheckStatusReturn( status, "Unable to Make iterGeoCount" );
                }
                /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    			if(iterGeoCount > 0)
        		{
        			rotationWeights.clear();
        			revolveWeights.clear();
        			scaleWeights.clear();
        			volumeWeights.clear();
        			slideWeights.clear();

        	        getWeightValues(data, aRotationWeightsParent, aRotationWeights, iterGeoCount, index, rotationWeights);
                    getWeightValues(data, aRevolveWeightsParent, aRevolveWeights, iterGeoCount, index, revolveWeights);
                    getWeightValues(data, aScaleWeightsParent, aScaleWeights, iterGeoCount, index, scaleWeights);
                    getWeightValues(data, aVolumeWeightsParent, aVolumeWeights, iterGeoCount, index, volumeWeights);
                    getWeightValues(data, aSlideWeightsParent, aSlideWeights, iterGeoCount, index, slideWeights);

                    rotationWeightsArray.push_back(rotationWeights);
                    revolveWeightsArray.push_back(revolveWeights);
                    scaleWeightsArray.push_back(scaleWeights);
                    volumeWeightsArray.push_back(volumeWeights);
                    slideWeightsArray.push_back(slideWeights);

        	    }
        	    else
                {
            		dummyWeights.clear();

                	dummyWeights.setLength(1) ;

                    dummyWeights[0] = 0.0;

                    rotationWeightsArray.push_back(dummyWeights);
                    revolveWeightsArray.push_back(dummyWeights);
                    scaleWeightsArray.push_back(dummyWeights);
                    volumeWeightsArray.push_back(dummyWeights);
                    slideWeightsArray.push_back(dummyWeights);
                }
            }
        }
    }
	else
	{
		if(cacheWeights == 1)
		{
		    if (rotationWeightsArray.size() > 0)
    		{
    		    rotationWeightsArray.clear();
    		}
		    if (revolveWeightsArray.size() > 0)
    		{
    		    revolveWeightsArray.clear();
    		}
		    if (scaleWeightsArray.size() > 0)
    		{
    		    scaleWeightsArray.clear();
    		}
		    if (volumeWeightsArray.size() > 0)
    		{
    		    volumeWeightsArray.clear();
    		}
		    if (slideWeightsArray.size() > 0)
    		{
    		    slideWeightsArray.clear();
    		}

    		for( index = 0; index < numIndex; ++index)
    		{

                /////////////////////////////////////////////////////////////////////////////////////////////////////////////
                //Find out how many points are in each piece of geo that will be deformed, if non fail safely and create a dummy count of 0
                MPlug inPlug(thisMObj, input);
                MArrayDataHandle ahInput = data.inputArrayValue(input, &status) ;
                MyCheckStatusReturn( status, "Unable to Make ahInput" );

                try
                {
                    status = ahInput.jumpToElement( index ) ;
                }
                catch(...)
                {
                    iterGeoCount = 0;
                }
                //MyCheckStatusReturn( status, "Unable to jumpToElement" );
                if (status == MS::kSuccess)
                {
                    // if status fails set array to 0
                    MDataHandle dhInput = ahInput.inputValue(&status) ;
                    MyCheckStatusReturn( status, "Unable to dhInput" );

                	MDataHandle dhWeightChild = dhInput.child( inputGeom ) ;
                	MyCheckStatusReturn( status, "Unable to ahWeightChild" );


                    MItGeometry iter( dhWeightChild, true, &status );
                    iterGeoCount = iter.count(&status);
                    MyCheckStatusReturn( status, "Unable to Make iterGeoCount" );
                }
                /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    			if(iterGeoCount > 0)
        		{
        			rotationWeights.clear();
        			revolveWeights.clear();
        			scaleWeights.clear();
        			volumeWeights.clear();
        			slideWeights.clear();

        	        getWeightValues(data, aRotationWeightsParent, aRotationWeights, iterGeoCount, index, rotationWeights);
                    getWeightValues(data, aRevolveWeightsParent, aRevolveWeights, iterGeoCount, index, revolveWeights);
                    getWeightValues(data, aScaleWeightsParent, aScaleWeights, iterGeoCount, index, scaleWeights);
                    getWeightValues(data, aVolumeWeightsParent, aVolumeWeights, iterGeoCount, index, volumeWeights);
                    getWeightValues(data, aSlideWeightsParent, aSlideWeights, iterGeoCount, index, slideWeights);

                    rotationWeightsArray.push_back(rotationWeights);
                    revolveWeightsArray.push_back(revolveWeights);
                    scaleWeightsArray.push_back(scaleWeights);
                    volumeWeightsArray.push_back(volumeWeights);
                    slideWeightsArray.push_back(slideWeights);

        	    }
        	    else
                {
            		dummyWeights.clear();

                	dummyWeights.setLength(1) ;

                    dummyWeights[0] = 0.0;

                    rotationWeightsArray.push_back(dummyWeights);
                    revolveWeightsArray.push_back(dummyWeights);
                    scaleWeightsArray.push_back(dummyWeights);
                    volumeWeightsArray.push_back(dummyWeights);
                    slideWeightsArray.push_back(dummyWeights);
                }
            }
        }
	}



    double curveBasePtParam = 0.0;
    MPoint pt;

    status = fnCurveBase.getKnotDomain( MinParam, MaxParam  );
    MyCheckStatusReturn( status, "Unable to getKnotDomain" );

    slideParamValue = 0.0;
    baseLength = fnCurveBase.length( 0.00001 );
    driveLength = fnCurve.length( 0.00001 );
    lengthComp = baseLength/driveLength;
    lengthFinal = lengthComp * driveLength;
    stretchParam = (.5*MaxParam);

    //cache parameters

    if(baseParamsArray.size() < numIndex)
    {
        // get rid of any information in the arrays
    	if (baseParamsArray.size() > 0)
		{
    	    baseParamsArray.clear();
		}
	    for( index = 0; index < numIndex; ++index)
	    {

            MPlug inPlug(thisMObj, input);
            MArrayDataHandle ahInput = data.inputArrayValue(input, &status) ;
            MyCheckStatusReturn( status, "Unable to Make ahInput" );

            try
            {
                status = ahInput.jumpToElement( index ) ;
            }
            catch(...)
            {
                iterGeoCount = 0;
            }
            if (status == MS::kSuccess)
            {
                // if status fails set array to 0
                MDataHandle dhInput = ahInput.inputValue(&status) ;
                MyCheckStatusReturn( status, "Unable to dhInput" );

            	MDataHandle dhWeightChild = dhInput.child( inputGeom ) ;
            	MyCheckStatusReturn( status, "Unable to ahWeightChild" );


                MItGeometry iter( dhWeightChild, true, &status );
                iterGeoCount = iter.count(&status);
                MyCheckStatusReturn( status, "Unable to Make iterGeoCount" );
                if(iterGeoCount > 0)
	            {
    	            baseParams.clear();
        	        baseParams.setLength(iterGeoCount) ;
            	    for (; !iter.isDone(&status);)
            	    {
                	    pt = iter.position();
                	    iterIndex = iter.index(&status);
                        fnCurveBase.closestPoint( pt, &baseParams[iterIndex], 0.00001, MSpace::kWorld, &status);
                        MyCheckStatusReturn( status, "Unable to get closestPoint" );
                        iter.next();
            	    }
            	    iter.reset();
            	    baseParamsArray.push_back(baseParams);
        	    }
            }
        	else
            {
                baseParams.clear();
            	baseParams.setLength(1) ;
                baseParams[0] = 0.0;
                baseParamsArray.push_back(baseParams);
            }
        }
    }
    else
    {
        if(cacheParams == 1)
        {
        	if (baseParamsArray.size() > 0)
    		{
        	    baseParamsArray.clear();
    		}
    	    for( index = 0; index < numIndex; ++index)
    	    {

                MPlug inPlug(thisMObj, input);
                MArrayDataHandle ahInput = data.inputArrayValue(input, &status) ;
                MyCheckStatusReturn( status, "Unable to Make ahInput" );

                try
                {
                    status = ahInput.jumpToElement( index ) ;
                }
                catch(...)
                {
                    iterGeoCount = 0;
                }
                if (status == MS::kSuccess)
                {
                    // if status fails set array to 0
                    MDataHandle dhInput = ahInput.inputValue(&status) ;
                    MyCheckStatusReturn( status, "Unable to dhInput" );

                	MDataHandle dhWeightChild = dhInput.child( inputGeom ) ;
                	MyCheckStatusReturn( status, "Unable to ahWeightChild" );


                    MItGeometry iter( dhWeightChild, true, &status );
                    iterGeoCount = iter.count(&status);
                    MyCheckStatusReturn( status, "Unable to Make iterGeoCount" );
                    if(iterGeoCount > 0)
    	            {
        	            baseParams.clear();
            	        baseParams.setLength(iterGeoCount) ;
                	    for (; !iter.isDone(&status);)
                	    {
                    	    pt = iter.position();
                    	    iterIndex = iter.index(&status);
                            fnCurveBase.closestPoint( pt, &baseParams[iterIndex], 0.00001, MSpace::kWorld, &status);
                            MyCheckStatusReturn( status, "Unable to get closestPoint" );
                            iter.next();
                	    }
                	    iter.reset();
                	    baseParamsArray.push_back(baseParams);
            	    }
                }
            	else
                {
                    baseParams.clear();
                	baseParams.setLength(1) ;
                    baseParams[0] = 0.0;
                    baseParamsArray.push_back(baseParams);
                }
            }
        }
    }
    

/////////////////////////////////////////////////////////////
    //CacheBase
    if(baseClosestPtsArray.size() < numIndex)
    {

    	if (baseClosestPtsArray.size() > 0)
		{
    	    baseClosestPtsArray.clear();
		}
		
    	if (aimBaseClosestPtsArray.size() > 0)
		{
    	    aimBaseClosestPtsArray.clear();
		}		
		
    	if (baseEulerRotationArray.size() > 0)
		{
    	    baseEulerRotationArray.clear();
		}	
			
    	if (baseMatrixVecArray.size() > 0)
		{
    	    baseMatrixVecArray.clear();
		}		

	    for( index = 0; index < numIndex; ++index)
	    {
            MPlug inPlug(thisMObj, input);
            MArrayDataHandle ahInput = data.inputArrayValue(input, &status) ;
            MyCheckStatusReturn( status, "Unable to Make ahInput" );

            try
            {
                status = ahInput.jumpToElement( index ) ;
            }
            catch(...)
            {
                iterGeoCount = 0;
                MGlobal::displayInfo(MString()+"Broken");
            }
            if (status == MS::kSuccess)
            {
                // if status fails set array to 0
                MDataHandle dhInput = ahInput.inputValue(&status) ;
                MyCheckStatusReturn( status, "Unable to dhInput" );

            	MDataHandle dhWeightChild = dhInput.child( inputGeom ) ;
            	MyCheckStatusReturn( status, "Unable to ahWeightChild" );


                MItGeometry iter( dhWeightChild, true, &status );
                iterGeoCount = iter.count(&status);
                MyCheckStatusReturn( status, "Unable to Make iterGeoCount" );
                if(iterGeoCount > 0)
    	        {
    	        

        	        // get rid of any information in the arrays
        	        baseClosestPts.clear();
            		aimCurveBaseClosestPts.clear();

            	    baseClosestPts.setLength(iterGeoCount) ;
            	    aimCurveBaseClosestPts.setLength(iterGeoCount) ;

            	    //baseCurveMatrixArray.clear();

            	    baseMatrixArray.clear();
            	    baseMatrixArray.setLength(iterGeoCount) ;

            	    baseEulerRotation.clear() ;


            	    for (; !iter.isDone(&status);)
            	    {
                	    pt = iter.position();
                	    iterIndex = iter.index(&status);

                        status = fnCurveBase.getPointAtParam( baseParamsArray[index][iterIndex], baseClosestPts[iterIndex], MSpace::kWorld );
                	    MyCheckStatusReturn( status, "Unable to get getPointAtParam" );

                	    status = fnAimCurveBase.getPointAtParam( baseParamsArray[index][iterIndex], aimCurveBaseClosestPts[iterIndex], MSpace::kWorld );
                	    MyCheckStatusReturn( status, "Unable to get getPointAtParam" );

                    	/////////////////////////////////////////////////////////////////////////////////////////////

                        // x vec
                	    xBaseVector = fnCurveBase.tangent( baseParamsArray[index][iterIndex], MSpace::kWorld, &status);
                	    MyCheckStatusReturn( status, "Unable to get tangent" );


                	    baseVecCross = (baseClosestPts[iterIndex] - aimCurveBaseClosestPts[iterIndex]);
                	    yBaseVector = (xBaseVector ^ baseVecCross);
                	    zBaseVector = (xBaseVector ^  yBaseVector);

                	    // normalize all vectors
                	    xBaseVector.normalize();
                	    yBaseVector.normalize();
                	    zBaseVector.normalize();

                	    float baseMatrix[4][4]={{ xBaseVector[0], xBaseVector[1], xBaseVector[2], 0.0},
                				                  { yBaseVector[0], yBaseVector[1], yBaseVector[2], 0.0},
                				                  { zBaseVector[0], zBaseVector[1], zBaseVector[2], 0.0},
                				                  {            0.0,            0.0,            0.0, 1.0},};

                	    MMatrix tempBaseMatrix(baseMatrix);


                        baseMatrixArray[iterIndex] = tempBaseMatrix;
                	    // decompose to Euler rotation
                	    rotMatrix = rotMatrix.decompose(tempBaseMatrix, MEulerRotation::kXYZ);
                        baseEulerRotation.push_back(rotMatrix);
                        iter.next();
                    }
                    baseClosestPtsArray.push_back(baseClosestPts);

                    aimBaseClosestPtsArray.push_back(aimCurveBaseClosestPts);

                    baseMatrixVecArray.push_back(baseMatrixArray);

                    baseEulerRotationArray.push_back(baseEulerRotation);
        	    }  
            }
            else
            {
                baseClosestPts.clear();
            	baseClosestPts.setLength(1) ;
                baseClosestPts[0] = dummyPoint;

                aimCurveBaseClosestPts.clear();
            	aimCurveBaseClosestPts.setLength(1) ;
                aimCurveBaseClosestPts[0] = dummyPoint;

                baseMatrixArray.clear();
            	baseMatrixArray.setLength(1) ;
                baseMatrixArray[0] = dummyMatrix;

                baseEulerRotation.clear();

                baseEulerRotation[0] = dummyEuler;

                baseClosestPtsArray.push_back(baseClosestPts);

                aimBaseClosestPtsArray.push_back(aimCurveBaseClosestPts);

                baseMatrixVecArray.push_back(baseMatrixArray);

                baseEulerRotationArray.push_back(baseEulerRotation);
            }
        }
    }
    else
    {
        if(cacheBase == 1)
        {

        	if (baseClosestPtsArray.size() > 0)
    		{
        	    baseClosestPtsArray.clear();
    		}
    		
        	if (aimBaseClosestPtsArray.size() > 0)
    		{
        	    aimBaseClosestPtsArray.clear();
    		}		
    		
        	if (baseEulerRotationArray.size() > 0)
    		{
        	    baseEulerRotationArray.clear();
    		}	
    			
        	if (baseMatrixVecArray.size() > 0)
    		{
        	    baseMatrixVecArray.clear();
    		}		

    	    for( index = 0; index < numIndex; ++index)
    	    {
                MPlug inPlug(thisMObj, input);
                MArrayDataHandle ahInput = data.inputArrayValue(input, &status) ;
                MyCheckStatusReturn( status, "Unable to Make ahInput" );

                try
                {
                    status = ahInput.jumpToElement( index ) ;
                }
                catch(...)
                {
                    iterGeoCount = 0;
                }
                if (status == MS::kSuccess)
                {
                    // if status fails set array to 0
                    MDataHandle dhInput = ahInput.inputValue(&status) ;
                    MyCheckStatusReturn( status, "Unable to dhInput" );

                	MDataHandle dhWeightChild = dhInput.child( inputGeom ) ;
                	MyCheckStatusReturn( status, "Unable to ahWeightChild" );


                    MItGeometry iter( dhWeightChild, true, &status );
                    iterGeoCount = iter.count(&status);
                    MyCheckStatusReturn( status, "Unable to Make iterGeoCount" );
                    if(iterGeoCount > 0)
        	        {
            	        // get rid of any information in the arrays
            	        baseClosestPts.clear();
                		aimCurveBaseClosestPts.clear();

                	    baseClosestPts.setLength(iterGeoCount) ;
                	    aimCurveBaseClosestPts.setLength(iterGeoCount) ;

                	    //baseCurveMatrixArray.clear();

                	    baseMatrixArray.clear();
                	    baseMatrixArray.setLength(iterGeoCount) ;

                	    baseEulerRotation.clear() ;


                	    for (; !iter.isDone(&status);)
                	    {
                    	    pt = iter.position();
                    	    iterIndex = iter.index(&status);

                            status = fnCurveBase.getPointAtParam( baseParamsArray[index][iterIndex], baseClosestPts[iterIndex], MSpace::kWorld );
                    	    MyCheckStatusReturn( status, "Unable to get getPointAtParam" );

                    	    status = fnAimCurveBase.getPointAtParam( baseParamsArray[index][iterIndex], aimCurveBaseClosestPts[iterIndex], MSpace::kWorld );
                    	    MyCheckStatusReturn( status, "Unable to get getPointAtParam" );

                        	/////////////////////////////////////////////////////////////////////////////////////////////

                            // x vec
                    	    xBaseVector = fnCurveBase.tangent( baseParamsArray[index][iterIndex], MSpace::kWorld, &status);
                    	    MyCheckStatusReturn( status, "Unable to get tangent" );


                	        baseVecCross = (baseClosestPts[iterIndex] - aimCurveBaseClosestPts[iterIndex]);
                    	    yBaseVector = (xBaseVector ^ baseVecCross);
                    	    zBaseVector = (xBaseVector ^  yBaseVector);

                    	    // normalize all vectors
                    	    xBaseVector.normalize();
                    	    yBaseVector.normalize();
                    	    zBaseVector.normalize();

                    	    float baseMatrix[4][4]={{ xBaseVector[0], xBaseVector[1], xBaseVector[2], 0.0},
                    				                  { yBaseVector[0], yBaseVector[1], yBaseVector[2], 0.0},
                    				                  { zBaseVector[0], zBaseVector[1], zBaseVector[2], 0.0},
                    				                  {            0.0,            0.0,            0.0, 1.0},};

                    	    MMatrix tempBaseMatrix(baseMatrix);


                            baseMatrixArray[iterIndex] = tempBaseMatrix;
                    	    // decompose to Euler rotation
                    	    rotMatrix = rotMatrix.decompose(tempBaseMatrix, MEulerRotation::kXYZ);
                            baseEulerRotation.push_back(rotMatrix);
                            ///////////////////////////////////////////////////////////////////////////////////////////
                            iter.next();
                        }
                        baseClosestPtsArray.push_back(baseClosestPts);

                        aimBaseClosestPtsArray.push_back(aimCurveBaseClosestPts);

                        baseMatrixVecArray.push_back(baseMatrixArray);

                        baseEulerRotationArray.push_back(baseEulerRotation);
            	    }  
                }
                else
                {
                    baseClosestPts.clear();
                	baseClosestPts.setLength(1) ;
                    baseClosestPts[0] = dummyPoint;

                    aimCurveBaseClosestPts.clear();
                	aimCurveBaseClosestPts.setLength(1) ;
                    aimCurveBaseClosestPts[0] = dummyPoint;

                    baseMatrixArray.clear();
                	baseMatrixArray.setLength(1) ;
                    baseMatrixArray[0] = dummyMatrix;

                    baseEulerRotation.clear();
                	//baseEulerRotation.setLength(1) ;
                    baseEulerRotation[0] = dummyEuler;

                    baseClosestPtsArray.push_back(baseClosestPts);

                    aimBaseClosestPtsArray.push_back(aimCurveBaseClosestPts);

                    baseMatrixVecArray.push_back(baseMatrixArray);

                    baseEulerRotationArray.push_back(baseEulerRotation);
                }
            }
        }
    }

    //////////////////////////////////////////////////////////////////////////////
    ////////////////////////// caching ends  /////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////






    for (; !MitGeo.isDone();)
    {
        pt = MitGeo.position();
        index = MitGeo.index();
        w = weightValue(data, mIndex, index)* envelope;

        if (fabs(w) == 0)
        {
            MitGeo.next();
            continue;
        }



    ////////////////////////////////////////////////////////////////
    ///////////////// CurveDeform //////////////////////////////////
    ////////////////////////////////////////////////////////////////


	curveBasePt = baseClosestPtsArray[mIndex][index];

	curveBasePtParam = baseParamsArray[mIndex][index];

    ///////////////////////////////////////////////////////
    ///////////////////////get slide///////////////////////


    if (countinuousSlide == 0)
    {
    	if (fabs(slide) != 0.0)
    	{

            slideW = (double)slideWeightsArray[mIndex][index];

    	    slidePt = curveBasePt;
    	    slideParam = curveBasePtParam;

    	    slideValue = 0.0;

    	    slideValue = slide * slideW;
    	    slideCheck = slideParam + slideValue;

    	    // insure you never go over the curves highest and lowest params
    	    if ((slideCheck > MinParam) || (slideCheck < MaxParam))
    		slideParamValue = slideParam + slideValue;
    	    if (slideCheck <= MinParam)
    		slideParamValue = MinParam;
    	    if (slideCheck >= MaxParam)
    		slideParamValue = MaxParam;

    	    // make vector or point on curve depending on slideValue value
    	    if ((slideCheck > MinParam) || (slideCheck < MaxParam))
    		status = fnCurve.getPointAtParam( slideParamValue, slidePoint, MSpace::kWorld);
    		MyCheckStatusReturn( status, "Unable to getPointAtParam" );

    	    if (slideCheck <= MinParam)
    	    {
        		status = fnCurve.getPointAtParam( slideParamValue, slidePoint, MSpace::kWorld );
        		MyCheckStatusReturn( status, "Unable to getPointAtParam" );
        		slideVec = fnCurve.tangent( MinParam, MSpace::kWorld, &status );
        		MyCheckStatusReturn( status, "Unable to get tangent" );
        		slideVec = slideVec * (driveLength/MaxParam);
        		slideValue = slideValue + curveBasePtParam;
        		slidePoint -= (-slideVec) * slideValue;
    	    }

    	    if (slideCheck >= MaxParam)
    	    {
        		status = fnCurve.getPointAtParam( slideParamValue, slidePoint, MSpace::kWorld );
        		MyCheckStatusReturn( status, "Unable to getPointAtParam" );
        		slideVec = fnCurve.tangent( MaxParam - .00001, MSpace::kWorld , &status );
        		MyCheckStatusReturn( status, "Unable to get tangent" );
        		slideVec = slideVec * (driveLength/MaxParam);
        		slideValue = slideValue + (curveBasePtParam - MaxParam);
        		slidePoint -= (-slideVec) * slideValue;
    	    }
    	    slidePoint = slidePoint * w ;

        }
        if (fabs(slide) == 0.0)
    	    {
    	        status = fnCurve.getPointAtParam( curveBasePtParam, slidePoint, MSpace::kWorld );
    	        slideParamValue = curveBasePtParam;
            }
    }

    // if continuous slide is on use modulus to loop the slide from parameter 0 to 1; 0 to 1; 0 to 1; forever, also works in reverse.
    if (countinuousSlide == 1)
    {
    	if (fabs(slide) != 0.0)
    	{

            slideW = (double)slideWeightsArray[mIndex][index];
    	    if (status != MS::kSuccess)
    	        slideW = 1.0 ;

    	    slidePt = curveBasePt;
    	    slideParam = curveBasePtParam;

    	    slideValue = 0.0;

    	    slideValue = slide * slideW;
    	    slideCheck = slideParam + slideValue;

    	    // modulus
            slideParamValue = fmod(slideCheck,MaxParam);
            if(slideParamValue < 0)
                slideParamValue+=MaxParam;

    		status = fnCurve.getPointAtParam( slideParamValue, slidePoint, MSpace::kWorld);

    	    slidePoint = slidePoint * w ;

        }
        if (fabs(slide) == 0.0)
    	    {
    	        status = fnCurve.getPointAtParam( curveBasePtParam, slidePoint, MSpace::kWorld );
    	        slideParamValue = curveBasePtParam;
            }
    }


///////////////////////////////////////////////////////
///////////////////////get rotation///////////////////////

// create a rotation matrix using 3 vectors
// you need to invert any initial rotation by subtracting the rotation of the base curves from the driver curves


////////////////////Get points needed to create a rotation matrix



	if (fabs(rotationAmount) > 0.0)
	{

        rotationW = (double)rotationWeightsArray[mIndex][index];
	    revolveW = (double)revolveWeightsArray[mIndex][index];
        status = fnCurve.getPointAtParam( slideParamValue, driverPt, MSpace::kWorld );
	    MyCheckStatusReturn( status, "Unable to get getPointAtParam" );
	    //aimCurveBasePt

	    //aimPt
	    status = fnAimCurve.getPointAtParam( slideParamValue, aimPt, MSpace::kWorld );
	    MyCheckStatusReturn( status, "Unable to get getPointAtParam" );

        status = fnAimCurveBase.getPointAtParam( slideParamValue, aimCurveBasePt, MSpace::kWorld );
        MyCheckStatusReturn( status, "Unable to get getPointAtParam" );

      /////////////////////////////////////////////////////////////////////
      /////////////// BaseVec for RotationCompensation //////////////////
        aimCurveBasePt = aimBaseClosestPtsArray[mIndex][index];
        
        BaseMatrix = baseMatrixVecArray[mIndex][index];

        rotMatrix = baseEulerRotationArray[mIndex][index];

      ///////////////////////////////////////////////////////////////////////////////

	    xAxisVec = fnCurve.tangent( slideParamValue, MSpace::kWorld, &status);
	    MyCheckStatusReturn( status, "Unable to get tangent" );
	    vecCross = driverPt - aimPt;
	    yAxisVec = xAxisVec ^ vecCross;
	    zAxisVec = xAxisVec ^ yAxisVec;

	    xAxisVec.normalize();
	    yAxisVec.normalize();
	    zAxisVec.normalize();

	    // apply rotate offset
	    MQuaternion rotateX(-rotMatrix[0]+ (RevolveAmount * revolveW),xAxisVec);
	    rotateMatrixX = rotateX.asMatrix();
	    yAxisVec = yAxisVec * rotateMatrixX;
	    zAxisVec = zAxisVec * rotateMatrixX;

	    MQuaternion rotateY(-rotMatrix[1],yAxisVec);
	    rotateMatrixY = rotateY.asMatrix();
	    xAxisVec = xAxisVec * rotateMatrixY;
	    zAxisVec = zAxisVec * rotateMatrixY;

	    MQuaternion rotateZ(-rotMatrix[2],zAxisVec);
	    rotateMatrixZ = rotateZ.asMatrix();
	    xAxisVec = xAxisVec * rotateMatrixZ;
	    yAxisVec = yAxisVec * rotateMatrixZ;

	    float driveMatrix[4][4]={{ xAxisVec[0], xAxisVec[1], xAxisVec[2], 0.0},
				      { yAxisVec[0], yAxisVec[1], yAxisVec[2], 0.0},
				      { zAxisVec[0], zAxisVec[1], zAxisVec[2], 0.0},
				      {         0.0,         0.0,         0.0, 1.0},};

	    MMatrix DriveMatrix(driveMatrix);

      //////// Apply RotationAmount /////////////////////////////

	    if (fabs(rotationAmount) <= 1.0){
    		DriveMatrixEuler = DriveMatrixEuler.decompose(DriveMatrix,MEulerRotation::kXYZ);
    		DriveMatrixEuler.setValue( DriveMatrixEuler[0] * (rotationAmount * rotationW) /* * falloffWeight*/ , DriveMatrixEuler[1] * (rotationAmount * rotationW)/* * falloffWeight*/, DriveMatrixEuler[2] * (rotationAmount * rotationW)/* * falloffWeight*/);
    		DriveMatrix = DriveMatrixEuler.asMatrix();
	    }

	    //preserve the pt's rest position
	    MVector toCenterBase(-curveBasePt.x, -curveBasePt.y, -curveBasePt.z);
	    pt = pt + toCenterBase;

	    // do rotation, then put pts back
	    pt = ( pt * DriveMatrix ) - toCenterBase;
    }

    ///////////////////////////
    //// Slide/Translation ////
    ///////////////////////////

	pt.x +=(slidePoint.x - curveBasePt.x) * w /* * falloffWeight */;
	pt.y +=(slidePoint.y - curveBasePt.y) * w /* * falloffWeight */;
	pt.z +=(slidePoint.z - curveBasePt.z) * w /* * falloffWeight */;

    //////////////////////
    //// Scale/Volume ////
    //////////////////////

	if (fabs(volume) > 0.0)
        {
            volumeW = (double)volumeWeightsArray[mIndex][index];
	    if (status != MS::kSuccess){
	        volumeW = 1.0 ;
            }
            maintainVolume = volume;
            pt = pt - (slidePoint - pt) * (lengthComp - 1.0) * maintainVolume * w /* * falloffWeight */ * volumeW;
        }

	if (fabs(scale) != 1.0)
        {
            scaleW = (double)scaleWeightsArray[mIndex][index];
	    if (status != MS::kSuccess){
	        scaleW = 1.0 ;
            }
            pt = pt - (slidePoint - pt) * (scale - 1.0) * w /* * falloffWeight */ * scaleW;
        }

        MitGeo.setPosition(pt);
        MitGeo.next();
    }
    return MS::kSuccess;
}

MStatus rnkCurveDeformer::initialize() {
	MStatus status ;
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MObject outputGeom = MPxDeformerNode::outputGeom;

    // create typed attributes

    // curve
    aCurve = tAttr.create("curve", "curve", MFnData::kNurbsCurve);
    addAttribute( aCurve );

    // curveBase
    aCurveBase = tAttr.create("curveBase", "curvebase", MFnData::kNurbsCurve);
    addAttribute( aCurveBase );

    // aimCurveBase
    aAimCurve = tAttr.create("aimCurve", "aimcurve", MFnData::kNurbsCurve);
    addAttribute( aAimCurve );

    // aimCurveBase
    aAimCurveBase = tAttr.create("aimCurveBase", "aimcurvebase", MFnData::kNurbsCurve);
    addAttribute( aAimCurveBase );

    // create numeric attributes

    //   CacheWeights

    aCacheWeights = nAttr.create("CacheWeights", "cacheweights", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheWeights);

    aCacheParams = nAttr.create("CacheParams", "cparams", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheParams);

    aCacheBase = nAttr.create("CacheBase", "cbase", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aCacheBase);


    aContinuousSlide = nAttr.create("ContinuousSlide", "cContinuouss", MFnNumericData::kInt);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(0.0);
    addAttribute(aContinuousSlide);

    //   aRotationAmount
    aRotationAmount = nAttr.create("RotationAmount", "ramount", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aRotationAmount);

    //   aRevolveAmount
    aRevolveAmount = nAttr.create("RevolveAmount", "revamount", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);
    addAttribute(aRevolveAmount);

    //   aFalloff
    aFalloff = nAttr.create("Falloff", "falloff", MFnNumericData::kFloat);
    nAttr.setKeyable(true);

    nAttr.setDefault(100.0);
    addAttribute(aFalloff);

    //   aScale
    aScale = nAttr.create("Scale", "scale", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(1.0);
    addAttribute(aScale);

    //   aMaintainVolume
    aMaintainVolume = nAttr.create("MaintainVolume", "vol", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(0.0);
    addAttribute(aMaintainVolume);

    //   aSlide
    aSlide = nAttr.create("Slide", "slide", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);
    addAttribute(aSlide);

    // Weights

    aRotationWeights = nAttr.create("rotationWeights", "rweights", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setArray(true);
    nAttr.setDefault(1.0);
    nAttr.setReadable(true);
    nAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRotationWeights);

    aRevolveWeights = nAttr.create("revolveWeights", "revweights", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setArray(true);
    nAttr.setDefault(1.0);
    nAttr.setReadable(true);
    nAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRevolveWeights);

    aScaleWeights = nAttr.create("scaleWeights", "scaleweights", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setArray(true);
    nAttr.setDefault(1.0);
    nAttr.setReadable(true);
    nAttr.setUsesArrayDataBuilder(true);
    addAttribute(aScaleWeights);

    aVolumeWeights = nAttr.create("volumeWeights", "vweights", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setArray(true);
    nAttr.setDefault(1.0);
    nAttr.setReadable(true);
    nAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVolumeWeights);

    aSlideWeights = nAttr.create("slideWeights", "slideweights", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setArray(true);
    nAttr.setDefault(1.0);
    nAttr.setReadable(true);
    nAttr.setUsesArrayDataBuilder(true);
    addAttribute(aSlideWeights);


    // Weight Parents

    // rotationWeightsParent
    aRotationWeightsParent = cAttr.create("rotationWeightsParent", "rweightsp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRotationWeights );
    cAttr.setReadable(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRotationWeightsParent);

    // revolveWeightsParent
    aRevolveWeightsParent = cAttr.create("revolveWeightsParent", "revweightsp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRevolveWeights );
    cAttr.setReadable(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRevolveWeightsParent);

    // scaleWeights
    aScaleWeightsParent = cAttr.create("scaleWeightsParent", "sweightsp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aScaleWeights );
    cAttr.setReadable(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aScaleWeightsParent);

    // volumeWeightsParent
    aVolumeWeightsParent = cAttr.create("volumeWeightsParent", "vweightsp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVolumeWeights );
    cAttr.setReadable(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVolumeWeightsParent);

    // slideWeightsParent
    aSlideWeightsParent = cAttr.create("slideWeightsParent", "slideweightsp");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aSlideWeights );
    cAttr.setReadable(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aSlideWeightsParent);

    // Effects

    // Typed Attrs

    attributeAffects(aCurve, outputGeom);
    attributeAffects(aCurveBase, outputGeom);
    attributeAffects(aAimCurve, outputGeom);
    attributeAffects(aAimCurveBase, outputGeom);

    // Numeric Attrs

    //Bool-like ints
    attributeAffects(aCacheWeights, outputGeom);
    attributeAffects(aCacheParams, outputGeom);
    attributeAffects(aCacheBase, outputGeom);
    attributeAffects(aContinuousSlide, outputGeom);

    //floats

    attributeAffects(aRotationAmount, outputGeom);
    attributeAffects(aRevolveAmount, outputGeom);
    attributeAffects(aFalloff, outputGeom);
    attributeAffects(aScale, outputGeom);
    attributeAffects(aMaintainVolume, outputGeom);
    attributeAffects(aSlide, outputGeom);

    // Weights

    attributeAffects(aRotationWeights, outputGeom);
    attributeAffects(aRevolveWeights, outputGeom);
    attributeAffects(aScaleWeights, outputGeom);
    attributeAffects(aVolumeWeights, outputGeom);
    attributeAffects(aSlideWeights, outputGeom);


    // WeightParents

    attributeAffects(aRotationWeightsParent, outputGeom);
    attributeAffects(aRevolveWeightsParent, outputGeom);
    attributeAffects(aScaleWeightsParent, outputGeom);
    attributeAffects(aVolumeWeightsParent, outputGeom);
    attributeAffects(aSlideWeightsParent, outputGeom);

    // Make deformer weights paintable
    MGlobal::executeCommand("makePaintable -attrType multiFloat -shapeMode deformer rnkCurveDeformer weights;");

    MGlobal::executeCommand("makePaintable -attrType multiDouble -shapeMode deformer rnkCurveDeformer rotationWeights;");
    MGlobal::executeCommand("makePaintable -attrType multiDouble -shapeMode deformer rnkCurveDeformer revolveWeights;");
    MGlobal::executeCommand("makePaintable -attrType multiDouble -shapeMode deformer rnkCurveDeformer scaleWeights;");
    MGlobal::executeCommand("makePaintable -attrType multiDouble -shapeMode deformer rnkCurveDeformer volumeWeights;");
    MGlobal::executeCommand("makePaintable -attrType multiDouble -shapeMode deformer rnkCurveDeformer slideWeights;");

  return MS::kSuccess;
}

MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("rnkCurveDeformer", rnkCurveDeformer::id, rnkCurveDeformer::creator,
                               rnkCurveDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(rnkCurveDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

