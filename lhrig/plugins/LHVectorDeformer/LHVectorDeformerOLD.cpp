//    float myfloat = fabs(allWeightsArray[0][0][0].length());
//    MGlobal::displayInfo(MString()+myfloat);

#include "LHVectorDeformer.h"

MTypeId LHVectorDeformer::id(0x78908017);


// nAttrs
MObject LHVectorDeformer::aDeformationOrder;
//////// cache attrs ////////
MObject LHVectorDeformer::aCachePivots;
MObject LHVectorDeformer::aCacheWeights;
//T Values
MObject LHVectorDeformer::aTValue;
MObject LHVectorDeformer::aTValueParent;

// TWeights

MObject LHVectorDeformer::aTWeightsBaby;
MObject LHVectorDeformer::aTWeights;
MObject LHVectorDeformer::aTWeightsParent;
MObject LHVectorDeformer::aTWeightsParentArray;


//////////////// R ////////////////////////////
//R Values

MObject LHVectorDeformer::aRValue;
MObject LHVectorDeformer::aRValueParent;

// RWeights
MObject LHVectorDeformer::aRWeights;
MObject LHVectorDeformer::aRWeightsParent;
MObject LHVectorDeformer::aRWeightsParentArray;


//R Pivots
MObject LHVectorDeformer::aRPivot;
MObject LHVectorDeformer::aRPivotArray;
//R Pivots
MObject LHVectorDeformer::aTPivot;
MObject LHVectorDeformer::aTPivotArray;


//////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////// get anim curves ////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////


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
    int deformationOrder = data.inputValue(aDeformationOrder).asInt();
//    float scaleAmount = data.inputValue(aScaleAmount).asFloat();
    // cache attrs
    int cachePivotsAmt = data.inputValue(aCachePivots).asInt();
    int cacheWeightsAmt = data.inputValue(aCacheWeights).asInt();
//    int cacheOutWeightsAmt = data.inputValue(aCacheOutWeights).asInt();

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

    MArrayDataHandle geomArrayHandle = data.inputArrayValue(geomPlug);

    // cache weight Mesh----
    // only worry about the weight mesh at scene load/mesh connection,
    // or if weight mesh caching is off


    ////////////////////////////////////////////////////////////////////
    ////////   get rotate pivots    ////////
    ////////////////////////////////////////////////////////////////////

//    allTPivots

    if (allPivots.size() < numIndex or cachePivotsAmt == 0)
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

    if (allWeightsArray.size() < numIndex or cacheWeightsAmt == 0)
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
                                unsigned int countParentParent = arrayHandleParentParent.elementCount();
                                arrayHandleParentParent.jumpToArrayElement(connectedArray[k]);

                                //parent
                                MDataHandle hArrayHandleParent = arrayHandleParentParent.inputValue().child(allWeightParents[j]);
                                MArrayDataHandle hArrayHandleParentArray(hArrayHandleParent);
//                                unsigned int countParent = hArrayHandleParentArray.elementCount();

                                //child
                                hArrayHandleParentArray.jumpToElement(i);
//                                MDataHandle hArrayHandleChild = hArrayHandleParentArray.inputValue().child(allWeightChildren[j]);
//                                MArrayDataHandle hArrayHandleChildArray(hArrayHandleChild);
//                                unsigned int countParent = hArrayHandleChildArray.elementCount();
//
//                                float myfloat = fabs(countParent);
//                                MGlobal::displayInfo(MString("CountParent")+myfloat);

//                                MGlobal::displayInfo(MString("k"));

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


//    MGlobal::displayInfo(MString("BigBreak"));





















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

            ////////////////////////////////////////////////////////
            //////////// U V N R combine //////////
            ////////////////////////////////////////////////////////
        vW = 0.0;
        rW = 0.0;

        if (allVals.size() > 0)
        {
            vW = std::accumulate(allVals[0].begin(),allVals[0].end(),0.0);
        }
        if (allVals.size() > 1)
        {
            rW = std::accumulate(allVals[1].begin(),allVals[1].end(),0.0);
        }

        if (vW == 0 and nW == 0)
        {
            MitGeo.next();
            continue;
        }
        // order the translates and rotates based on user preference
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

    ///////////////////////////////////////////
    /////////////// INPUTS ////////////////////
    ///////////////////////////////////////////



    ////////// typed attributes ////////////


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


    //////Affects outputs and inputs

    MObject outputGeom = MPxDeformerNode::outputGeom;


    // nAttrs

    attributeAffects(aDeformationOrder, outputGeom);


    attributeAffects(aCachePivots, outputGeom);
    attributeAffects(aCacheWeights, outputGeom);

    // V ATTRS

    attributeAffects(aTValueParent, outputGeom);
    attributeAffects(aTWeightsParentArray, outputGeom);
    attributeAffects(aTPivotArray, outputGeom);

    // R ATTRS

    attributeAffects(aRValueParent, outputGeom);
    attributeAffects(aRWeightsParentArray, outputGeom);
    attributeAffects(aRPivotArray, outputGeom);



    // Make deformer weights paintable


    MGlobal::executeCommand("makePaintable -attrType multiFloat -shapeMode deformer LHVectorDeformer weights;");

    // Make deformer weights paintable

  return MS::kSuccess;
}
