//============================================== NOTES ==============================================
//========================================= WHY ANIM CURVES? ==============================================
// The purpose of this node is to create area weights that are independent of point count, spacing, and order
// The Anim Curve is used to manipulate this weighting, instead of an MRampAttribute for example, for a
// number of reasons.
//
// First and formost, the dynamic creation and use of MRampAttributes are clunky at best, at worst they are
// impossible to add as a dynamic array that can grow and shrink in size because they rely on the creation of an
// AEAttributeEditorTemplate file to even be viewable in the attribute editor.
//
// Second, when planning out weights it is important to be able to visualize what multiple curves are doing
// on top of each other so you can see how one fades out and one fades in.
//
// Lastly, and perhaps more important, is the controlability of animation curves are much higher than curves created
// with the MRampAttribute.  You get handles and control over tangents, the option to unify or break handles and all of
// the commands and classes that are used to create/manipulate animation curves.  You can easily copy them, add
// points, mirror, flip, or even simplify them.
//
//============================================== Implementation ==============================================
// The 2-Dimensional nature of the anim curve means that we need to convert them to 3-Dimensional coordinates.
// The easiest way of doing this is to project them onto a static mesh, or thinking of it in a different way, you
// project the 3-d points to the 2-dimensional range of the curve.
// This "projection" is accomplished by creating a mesh with a clean 0-1 uv range that can be "wrapped" around the
// geometry.
// The points are then "projected" to the mesh's UVs using a closest point calculation.
// Once the UV coordinates for each point are known you have their location in 2-D space.
// We know that Length x Width = Area.  You can think of the V coordinates as Length and U coordinates as Width.
// We must remap range of the curve to be 0-1, just like the UV coordinates.  Once the curve
// Is in the 0-1 range, you can think of the U-V cordinate as a point in time.
// You need to have an animation curve for both the U and the V, and you must evaluate both to get the final area.
// The U curve is easiest to visualize as the direct influence, while the V curve can be seen as a falloff
// This could easily be flipped, depending on the orientation of the points and what angle you are viewing in.
//=================================================================================================================
#include "LHCurveWeightNode_2.h"

MTypeId LHCurveWeightNode_2::id(0x354653598);

MObject LHCurveWeightNode_2::aOutputWeightsDoubleArrayParent;
MObject LHCurveWeightNode_2::aOutputWeightsDoubleArray;
MObject LHCurveWeightNode_2::aInputs;
MObject LHCurveWeightNode_2::aMembershipWeights;
MObject LHCurveWeightNode_2::aCacheMembershipWeights;
MObject LHCurveWeightNode_2::aInputMesh;
MObject LHCurveWeightNode_2::aInputCurve;
MObject LHCurveWeightNode_2::aInputNurbs;
MObject LHCurveWeightNode_2::aProjectionMesh;
MObject LHCurveWeightNode_2::aCacheWeightMesh;
MObject LHCurveWeightNode_2::aOutputWeightsFloatArrayParent;
MObject LHCurveWeightNode_2::aOutputWeightsFloatArray;
MObject LHCurveWeightNode_2::aOutWeights;
MObject LHCurveWeightNode_2::aAnimCurveU;
MObject LHCurveWeightNode_2::aAnimCurveV;
MObject LHCurveWeightNode_2::aFalloffU;
MObject LHCurveWeightNode_2::aFalloffUPivot;
MObject LHCurveWeightNode_2::aInputGeo;

MObject LHCurveWeightNode_2::aCacheOverrideWeights;
MObject LHCurveWeightNode_2::aOverrideWeights;
// MObject LHCurveWeightNode_2::aOverrideWeightsV;


void* LHCurveWeightNode_2::creator() { return new LHCurveWeightNode_2; }

MStatus LHCurveWeightNode_2::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnEnumAttribute eAttr;
    MFnGenericAttribute gAttr;

    aInputGeo = gAttr.create("inputGeo", "inputgeo");
    gAttr.addAccept(MFnData::kMesh);
    gAttr.addAccept(MFnData::kNurbsSurface);
    gAttr.addAccept(MFnData::kNurbsCurve);
    gAttr.addAccept(MFnData::kLattice);
    addAttribute(aInputGeo);


    aInputMesh = tAttr.create("inMesh", "inmesh", MFnData::kMesh);
    addAttribute(aInputMesh);

    aInputCurve = tAttr.create("inCurve", "incurve", MFnData::kNurbsCurve);
    addAttribute(aInputCurve);

    aInputNurbs = tAttr.create("inNurbs", "innurbs", MFnData::kNurbsSurface);
    addAttribute(aInputNurbs);

    aProjectionMesh = tAttr.create("projectionMesh", "pmesh", MFnData::kMesh);
    addAttribute(aProjectionMesh);

    aMembershipWeights = tAttr.create("membershipWeights", "mweights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aMembershipWeights);

    aAnimCurveU = nAttr.create("animCurveU", "AnimCurveU", MFnNumericData::kFloat);
    nAttr.setKeyable(true);

    aAnimCurveV = nAttr.create("animCurveV", "AnimCurveV", MFnNumericData::kFloat);
    nAttr.setKeyable(true);

    // aFalloffU = nAttr.create("falloffU", "falloffu", MFnNumericData::kFloat);
    // nAttr.setDefault(1);
    // nAttr.setKeyable(true);

    // aFalloffUPivot = nAttr.create("falloffUPivot", "falloffupivot", MFnNumericData::kFloat);
    // nAttr.setDefault(0.0);
    // nAttr.setKeyable(true);

    aOverrideWeights = tAttr.create("overrideWeights", "overrideweights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOverrideWeights);

    // aOverrideWeightsV = tAttr.create("overrideWeightsV", "overrideweightsv", MFnNumericData::kDoubleArray);
    // tAttr.setKeyable(true);
    // tAttr.setArray(false);
    // tAttr.setUsesArrayDataBuilder(true);
    // addAttribute(aOverrideWeightsV);

    aInputs = cAttr.create("Inputs", "inputs");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aAnimCurveU );
    cAttr.addChild( aAnimCurveV );
    cAttr.addChild( aOverrideWeights );
    // cAttr.addChild( aOverrideWeightsV );
    // cAttr.addChild( aFalloffU );
    // cAttr.addChild( aFalloffUPivot );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setIndexMatters(false);
    addAttribute(aInputs);

    aOutputWeightsDoubleArray = tAttr.create("outWeightsDoubleArray", "owd", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(false);
    tAttr.setArray(false);
    tAttr.setWritable(true);
    tAttr.setStorable(true);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutputWeightsDoubleArray);

    aCacheMembershipWeights = nAttr.create("cacheMembershipWeights", "cmweights", MFnNumericData::kInt);
    nAttr.setKeyable(false);
    nAttr.setMin(0);
    nAttr.setMax(1);
    nAttr.setDefault(1);
    nAttr.setChannelBox(true);
    addAttribute(aCacheMembershipWeights);

    aCacheWeightMesh = nAttr.create("cacheWeightMesh", "cwmesh", MFnNumericData::kInt);
    nAttr.setKeyable(false);
    nAttr.setMin(0);
    nAttr.setMax(1);
    nAttr.setDefault(1);
    nAttr.setChannelBox(true);
    addAttribute(aCacheWeightMesh);

    aCacheOverrideWeights = nAttr.create("cacheOverrideWeights", "cacheoverrideweights", MFnNumericData::kInt);
    nAttr.setKeyable(false);
    nAttr.setMin(0);
    nAttr.setMax(1);
    nAttr.setDefault(1);
    nAttr.setChannelBox(true);
    addAttribute(aCacheOverrideWeights);

    aOutWeights = nAttr.create("outFloatWeight", "outflw", MFnNumericData::kFloat, 0.0);
    nAttr.setKeyable(false);
    nAttr.setArray(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setInternal(true);
    nAttr.setIndexMatters(false);
    nAttr.setUsesArrayDataBuilder(true);

    aOutputWeightsFloatArray = cAttr.create("outWeightsFloatArray", "wlf");
    cAttr.addChild( aOutWeights );
    cAttr.setHidden(false);
    cAttr.setArray(true);
    cAttr.setChannelBox(true);
    cAttr.setConnectable(true);
    cAttr.setKeyable(false);
    cAttr.setReadable(true);
    cAttr.setInternal(true);
    cAttr.setIndexMatters(false);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutputWeightsFloatArray);

    aOutputWeightsFloatArrayParent = cAttr.create("outFloatWeights", "outfloatweights");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aOutputWeightsFloatArray );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setIndexMatters(false);
    addAttribute(aOutputWeightsFloatArrayParent);

    aOutputWeightsDoubleArrayParent = cAttr.create("outDoubleWeights", "outDoubleweights");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aOutputWeightsDoubleArray );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setIndexMatters(false);
    addAttribute(aOutputWeightsDoubleArrayParent);

    attributeAffects(aCacheWeightMesh, aOutputWeightsDoubleArray);
    attributeAffects(aInputMesh, aOutputWeightsDoubleArray);
    attributeAffects(aProjectionMesh, aOutputWeightsDoubleArray);
    attributeAffects(aCacheMembershipWeights, aOutputWeightsDoubleArray);
    attributeAffects(aMembershipWeights, aOutputWeightsDoubleArray);
    attributeAffects(aInputs, aOutputWeightsDoubleArray);

    attributeAffects(aCacheWeightMesh, aOutputWeightsFloatArray);
    attributeAffects(aInputMesh, aOutputWeightsFloatArray);
    attributeAffects(aProjectionMesh, aOutputWeightsFloatArray);
    attributeAffects(aCacheMembershipWeights, aOutputWeightsFloatArray);
    attributeAffects(aMembershipWeights, aOutputWeightsFloatArray);
    attributeAffects(aInputs, aOutputWeightsFloatArray);


    attributeAffects(aInputGeo, aOutputWeightsDoubleArray);
    attributeAffects(aInputGeo, aOutputWeightsFloatArray);

    return MStatus::kSuccess;
}


MStatus LHCurveWeightNode_2::compute( const MPlug& plug, MDataBlock& data)
{
    if( plug == LHCurveWeightNode_2::aOutputWeightsDoubleArray)
    {
        computeDoubleArray(data);
    }
    
    if( plug == LHCurveWeightNode_2::aOutputWeightsFloatArray)
    {
        LHCurveWeightNode_2::computeFloatArray(data);
    }
    return MS::kSuccess;
}









MStatus LHCurveWeightNode_2::getMeshData(MDataBlock& data, MObject &oInputMesh, MObject &oProjectionMesh, MObject &oInputCurve, MObject &oInputNurbs,
                                       MDataHandle &hInputGeo)
{
    
    oInputMesh = data.inputValue(LHCurveWeightNode_2::aInputMesh).asMeshTransformed();
    oInputCurve = data.inputValue(LHCurveWeightNode_2::aInputCurve).asNurbsCurveTransformed();
    oInputNurbs = data.inputValue(LHCurveWeightNode_2::aInputNurbs).asNurbsSurfaceTransformed();
    hInputGeo = data.inputValue(LHCurveWeightNode_2::aInputGeo);

	bool isNumeric;
    bool isNull;
    hInputGeo.isGeneric(isNumeric, isNull);
    if (isNull)
    {
        MGlobal::displayInfo(MString("Unable to get inputGeo"));
        return MS::kFailure;
    }

    // if (oInputMesh.isNull() and oInputCurve.isNull() and oInputNurbs.isNull())
    // {
    //     MGlobal::displayInfo(MString("Unable to get inMesh, or inCurve"));
    //     return MS::kFailure;
    // }

    // if (!oInputMesh.isNull() and !oInputCurve.isNull() and !oInputNurbs.isNull())
    // {
    //     MGlobal::displayInfo(MString("Multiple geometry types are connected, please only connect 1 geometry per node"));
    //     return MS::kFailure;
    // }


    oProjectionMesh = data.inputValue(LHCurveWeightNode_2::aProjectionMesh).asMeshTransformed();
    if (oProjectionMesh.isNull())
    {
        MGlobal::displayInfo(MString("Unable to get projectionMesh"));
        return MS::kFailure;
    }
    return MS::kSuccess;
}

MDoubleArray LHCurveWeightNode_2::getMembershipWeights(MDataBlock& data, MDoubleArray membershipWeights, int numVerts, int iCacheMemberWeights)
{
    MDoubleArray rMembershipWeights;
    if (!membershipWeights.length() || membershipWeights.length() != numVerts || !iCacheMemberWeights)
    {
        // Get Membership Weights, these will be used to ignore non membership points
        MDataHandle hMembershipArray = data.inputValue( LHCurveWeightNode_2::aMembershipWeights);
        MObject oMemebershipArray = hMembershipArray.data();
        MFnDoubleArrayData membershipData(oMemebershipArray);
        membershipData.copyTo(rMembershipWeights);
        return rMembershipWeights;
    }
    else
    {
        return membershipWeights;
    }
    return membershipWeights;

}


MStatus LHCurveWeightNode_2::computeDoubleArray(MDataBlock& data)
{
    MDoubleArray finalWeights;
    std::vector <MDoubleArray> finalWeightsArray;
    MStatus status = LHCurveWeightNode_2::getWeightsFromInputs(data, finalWeights, finalWeightsArray);
    CheckStatusReturn( status, "Unable to get weights" );

    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHCurveWeightNode_2::aOutputWeightsDoubleArrayParent, &status));
    CheckStatusReturn( status, "Unable to get inputs" );
    unsigned int elemCount = inputsArrayHandle.elementCount(&status);

    if (!finalWeightsArray.size() || finalWeightsArray.size() != elemCount)
        CheckStatusReturn( MS::kFailure, "Input and output element sizes don't match" );

    for (int i=0;i < elemCount;i++)
    {
        status = inputsArrayHandle.jumpToElement(i);
        CheckStatusReturn( status, "Unable to jump to doubleArray element" );


        MFnDoubleArrayData outputDoubleArrayFn;
        MObject oOutputArray = outputDoubleArrayFn.create(finalWeightsArray[i]);
        if (oOutputArray.isNull())
        {
            MGlobal::displayInfo(MString("The output is NULL"));
            return MS::kFailure;
        }
        MDataHandle handle = inputsArrayHandle.outputValue().child(LHCurveWeightNode_2::aOutputWeightsDoubleArray);
        handle.setMObject(oOutputArray);
        
    }
    data.setClean(LHCurveWeightNode_2::aOutputWeightsDoubleArray);
    data.setClean(LHCurveWeightNode_2::aOutputWeightsDoubleArrayParent);
    return MS::kSuccess;
}


MStatus LHCurveWeightNode_2::getAnimCurveInfo(MFnAnimCurve *fnAnimCurve, float &timeOffset, float &timeLength)
{
    numKeys = fnAnimCurve->numKeys();
    if (!numKeys)
    {
        return MS::kFailure;
    }
    timeAtFirstKey = fnAnimCurve->time(0);
    timeAtLastKey = fnAnimCurve->time(numKeys-1);
    timeStart = timeAtFirstKey.value();
    timeEnd = timeAtLastKey.value();
    timeOffset = timeStart * -1;
    timeLength = timeEnd + timeOffset;
    return MS::kSuccess;
}



MStatus LHCurveWeightNode_2::getAnimCurvePlug(int currentElem, MPlug& rPCurve, MObject curveObject)
{
    MPlug pInputs( thisMObj, aInputs) ;
    MPlug pInputElem = pInputs.elementByLogicalIndex(currentElem, &status);
    CheckStatusReturn( status, "Unable to get unable to get parentElement" );

    rPCurve = pInputElem.child(curveObject, &status);
    CheckStatusReturn( status, "Unable to get unable to get child" );
    return MS::kSuccess;
}


MStatus LHCurveWeightNode_2::getWeightMeshData(MObject oProjectionMesh, MFnMesh *mInputMesh, MFnMesh *mProjectionMesh, MFloatArray &uCoords, MFloatArray &vCoords, int numVerts, int iCacheWeightMesh)
{
    if (!uCoords.length() || uCoords.length() != numVerts || !vCoords.length() || vCoords.length() != numVerts || !iCacheWeightMesh)
    {
        fnWeightIntersector.create(oProjectionMesh);
        MFnMesh projectionMesh(oProjectionMesh);
        if (uCoords.length())
            uCoords.clear();
        if (vCoords.length())
            vCoords.clear();
        for (int i=0;i < numVerts;i++)
        {
            mInputMesh->getPoint(i, pt, MSpace::kObject);
            fnWeightIntersector.getClosestPoint(pt, ptOnMesh);
            pointOnPoint = ptOnMesh.getPoint();
            mProjectionMesh->getUVAtPoint( pointOnPoint, uvCoord, MSpace::kObject );
            uCoords.append(uvCoord[0]);
            vCoords.append(uvCoord[1]);
        }
    }
    return MS::kSuccess;
}

MStatus LHCurveWeightNode_2::getWeightMeshDataFromPoints(MObject oProjectionMesh, MPointArray allPoints, MFnMesh *mProjectionMesh, MFloatArray &uCoords, MFloatArray &vCoords, int numVerts, int iCacheWeightMesh)
{
    if (!uCoords.length() || uCoords.length() != numVerts || !vCoords.length() || vCoords.length() != numVerts || !iCacheWeightMesh)
    {
        fnWeightIntersector.create(oProjectionMesh);
        MFnMesh projectionMesh(oProjectionMesh);
        if (uCoords.length())
            uCoords.clear();
        if (vCoords.length())
            vCoords.clear();
        for (int i=0;i < numVerts;i++)
        {
            pt = allPoints[i];
            fnWeightIntersector.getClosestPoint(pt, ptOnMesh);
            pointOnPoint = ptOnMesh.getPoint();
            mProjectionMesh->getUVAtPoint( pointOnPoint, uvCoord, MSpace::kObject );
            uCoords.append(uvCoord[0]);
            vCoords.append(uvCoord[1]);
        }
    }
    return MS::kSuccess;
}



MStatus LHCurveWeightNode_2::computeFloatArray(MDataBlock& data)
{
    MDoubleArray finalWeights;
    std::vector <MDoubleArray> finalWeightsArray;
    MStatus status = LHCurveWeightNode_2::getWeightsFromInputs(data, finalWeights, finalWeightsArray);
    CheckStatusReturn( status, "Unable to get weights" );
    
    MObject thisNode = thisMObject();
    MPlug weightsParent( thisNode, LHCurveWeightNode_2::aOutputWeightsFloatArrayParent) ;
    MPlug parentElement;

    if (!finalWeightsArray.size() || finalWeightsArray.size() != weightsParent.numElements())
        CheckStatusReturn( MS::kFailure, "Input and output element sizes don't match" );

    for (int i=0;i < weightsParent.numElements();i++)
    {
        MPlug parentWeightsElement = weightsParent.elementByLogicalIndex(i, &status);
        MPlug parent = parentWeightsElement.child(LHCurveWeightNode_2::aOutputWeightsFloatArray, &status);

        for (unsigned int j = 0; j < parent.numElements(); ++j)
        {
            parentElement = parent.elementByLogicalIndex(j, &status);
            CheckStatusReturn( status, "Unable to get unable to get parentElement" );

            MPlug child = parentElement.child(LHCurveWeightNode_2::aOutWeights, &status);
            CheckStatusReturn( status, "Unable to get unable to get child" );

            for (unsigned int k = 0; k < finalWeightsArray[j].length(); ++k)
            {
                MPlug childWeight = child.elementByLogicalIndex(k);
                float val = (float) finalWeightsArray[j][k];
                childWeight.setValue(val);
            }
        }
    }
    return MS::kSuccess;
}

void LHCurveWeightNode_2::dirtyPlug(MPlug const & inPlug, MPlugArray  & affectedPlugs, MPlug outArrayPlug)
{
    if (inPlug.isElement())
    {
        MPlug elemPlug = outArrayPlug.elementByLogicalIndex(
                                            inPlug.logicalIndex());
        affectedPlugs.append(elemPlug);
        affectedPlugs.append(outArrayPlug);
    }
    else
    {
        affectedPlugs.append(outArrayPlug);
        unsigned int i,n = outArrayPlug.numElements();
        for (i = 0; i < n; i++) {
            MPlug elemPlug = outArrayPlug.elementByPhysicalIndex(i);
            affectedPlugs.append(elemPlug);
        }
    }
}

MStatus LHCurveWeightNode_2::setDependentsDirty( MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs)
    {
        if ( (inPlug.attribute() != aInputs)
        & (inPlug.attribute() != aAnimCurveU)
        & (inPlug.attribute() != aAnimCurveV)
        & (inPlug.attribute() != aFalloffU)
        & (inPlug.attribute() != aMembershipWeights)
        & (inPlug.attribute() != aCacheMembershipWeights)
        & (inPlug.attribute() != aProjectionMesh)
        & (inPlug.attribute() != aCacheWeightMesh)
        & (inPlug.attribute() != aInputGeo))
        {
            return MS::kSuccess;
        }
        if ( inPlug.attribute() == aOutputWeightsDoubleArray)
        {
            MPlug doubleArrayPlug(thisMObject(), aOutputWeightsDoubleArray);
            dirtyPlug(inPlug, affectedPlugs, doubleArrayPlug);
            return MS::kSuccess;
        }
        else if ( inPlug.attribute() == aOutputWeightsFloatArray)
        {
            MPlug floatArrayPlug(thisMObject(), aOutputWeightsFloatArray);
            dirtyPlug(inPlug, affectedPlugs, floatArrayPlug);
            return MS::kSuccess;
        }
        else if ( inPlug.attribute() == aOutputWeightsDoubleArrayParent)
        {
            MPlug doubleArrayMultiPlug(thisMObject(), aOutputWeightsDoubleArrayParent);
            dirtyPlug(inPlug, affectedPlugs, doubleArrayMultiPlug);
            return MS::kSuccess;
        }
        else if ( inPlug.attribute() == aOutputWeightsFloatArrayParent)
        {
            MPlug floatArrayMultiPlug(thisMObject(), aOutputWeightsFloatArrayParent);
            dirtyPlug(inPlug, affectedPlugs, floatArrayMultiPlug);
            return MS::kSuccess;
        }
        return MS::kSuccess;
    }









































MStatus LHCurveWeightNode_2::getWeightsFromInputs(MDataBlock& data, MDoubleArray& finalWeights, std::vector <MDoubleArray>& finalWeightsArray)
{
    // MStatus status;
    thisMObj = thisMObject();

    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHCurveWeightNode_2::aInputs, &status));
    CheckStatusReturn( status, "Unable to get inputs" );
    unsigned int elemCount = inputsArrayHandle.elementCount(&status);
    CheckStatusReturn( status, "Unable to get number of inputs" );

    // Get mesh objects
    MObject oInputMesh;
    MObject oProjectionMesh;
    MObject oInputCurve;
    MObject oInputNurbs;
    MDataHandle hInputGeo;
    MPointArray allPoints;

    status = getMeshData(data, oInputMesh, oProjectionMesh, oInputCurve, oInputNurbs, hInputGeo);
    CheckStatusReturn( status, "Unable to get meshes" );

    MItGeometry iterGeo(hInputGeo);
    iterGeo.allPositions(allPoints, MSpace::kWorld);

    int numVerts = allPoints.length();
    if (!numVerts)
    {
        CheckStatusReturn( MS::kFailure, "No Points!!!" );

    }

    MFnMesh *mProjectionMesh = new MFnMesh(oProjectionMesh);

    // Get membership weights
    int iCacheMemberWeights = data.inputValue(aCacheMembershipWeights).asInt();
    membershipWeights = LHCurveWeightNode_2::getMembershipWeights(data, membershipWeights, numVerts, iCacheMemberWeights);

    // Get projection mesh data
    int iCacheWeightMesh = data.inputValue(aCacheWeightMesh).asInt();
    int doCacheOverride = data.inputValue(aCacheOverrideWeights).asInt();
    // status = getWeightMeshData(oProjectionMesh, mInputMesh, mProjectionMesh, uCoords, vCoords, numVerts, iCacheWeightMesh);
    status = getWeightMeshDataFromPoints(oProjectionMesh, allPoints, mProjectionMesh, uCoords, vCoords, numVerts, iCacheWeightMesh);
    CheckStatusReturn( status, "Unable to get weight mesh" );

    if (finalWeightsArray.size())
        finalWeightsArray.clear();
    for (int i=0;i < elemCount;i++)
    {
        status = inputsArrayHandle.jumpToElement(i);
        CheckStatusReturn( status, "Unable to jump to input element" );
        status = LHCurveWeightNode_2::getAnimCurveWeights( inputsArrayHandle, finalWeights, numVerts, i, doCacheOverride);
        CheckStatusReturn( status, "Unable to get Anim Curves" );
        finalWeightsArray.push_back(finalWeights);

    }
    if (finalWeights.length() && finalWeights.length() != 0)
        return MS::kSuccess;
    else
        return MS::kFailure;
}

bool LHCurveWeightNode_2::getOverrideWeights(MArrayDataHandle inputsArrayHandle,
                                             MObject childWeightObject,
                                             MDoubleArray& currentWeights,
                                             int numVerts, int currentElem, int doCacheOverride)
{
    MDoubleArray checkWeights;
    if (!currentWeights.length() || currentWeights.length() != numVerts || !doCacheOverride)
    {
        MStatus status = inputsArrayHandle.jumpToElement(currentElem);
        MDataHandle handle(inputsArrayHandle.inputValue(&status) );
        if (status == MS::kFailure)
        {
            return false;
        }

        MDataHandle weightChild(handle.child( childWeightObject) );
        checkWeights = MFnDoubleArrayData(weightChild.data()).array(&status);
        if (status == MS::kFailure)
        {
            return false;
        }

        if (checkWeights.length() != numVerts)
        {
            return false;
        }
    }
    currentWeights = checkWeights;
    if (currentWeights.length() != numVerts)
    {
        return false;
    }
    
    return true;
}



MStatus LHCurveWeightNode_2::getAnimCurveWeights(MArrayDataHandle inputsArrayHandle,
                                                 MDoubleArray& rWeights,
                                                 int numVerts, int currentElem,
                                                 int doCacheOverride
                                                 )
{
    MPlug pAnimCurveU;
    bool override = false;
    MDoubleArray overrideWeight;



    status = LHCurveWeightNode_2::getAnimCurvePlug(currentElem, pAnimCurveU, aAnimCurveU);
    CheckStatusReturn( animCurveObjectCheck(pAnimCurveU), "Unable to get curveU" );
    MPlug pAnimCurveV;
    status = LHCurveWeightNode_2::getAnimCurvePlug(currentElem, pAnimCurveV, aAnimCurveV);
    CheckStatusReturn( animCurveObjectCheck(pAnimCurveV), "Unable to get curveV" );

    MFnAnimCurve *fnAnimCurveU = new MFnAnimCurve(pAnimCurveU);
    status = getAnimCurveInfo(fnAnimCurveU, timeOffsetU, timeLengthU);
    CheckStatusReturn( status, "AnimCurveU does not have keys" );

    MFnAnimCurve *fnAnimCurveV = new MFnAnimCurve(pAnimCurveV);
    status =getAnimCurveInfo(fnAnimCurveV, timeOffsetV, timeLengthV);
    CheckStatusReturn( status, "AnimCurveV does not have keys" );

    override = LHCurveWeightNode_2::getOverrideWeights(inputsArrayHandle,
                                                        aOverrideWeights,
                                                        overrideWeight,
                                                        numVerts, currentElem, doCacheOverride);


    if (!membershipWeights.length())
    {
        CheckStatusReturn( MS::kFailure, "Membership has not been weighted" );
    }


    if (rWeights.length())
        rWeights.clear();
        for (int i=0;i < numVerts;i++)
        {
            if (membershipWeights[i] == 0.0)
            {
                rWeights.append(0.0);
                continue;
            }
            uWeight = remapcurveWeight(fnAnimCurveU, uCoords[i], timeOffsetU, timeLengthU);
            vWeight = remapcurveWeight(fnAnimCurveV, vCoords[i], timeOffsetV, timeLengthV);
            // rWeights.append(uWeight*vWeight);
            if (!override)
            {
                rWeights.append(uWeight*vWeight);
            }
            else
            {
                rWeights.append(uWeight*vWeight*overrideWeight[i]);

            }

        }
    return MS::kSuccess;
}
