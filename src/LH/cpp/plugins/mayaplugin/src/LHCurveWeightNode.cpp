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
#include "LHCurveWeightNode.h"

MTypeId LHCurveWeightNode::id(0x35443568);

MObject LHCurveWeightNode::aOutputWeights;
MObject LHCurveWeightNode::aInputs;
MObject LHCurveWeightNode::aInputWeights;
MObject LHCurveWeightNode::aFactor;
MObject LHCurveWeightNode::aOperation;
MObject LHCurveWeightNode::aMembershipWeights;
MObject LHCurveWeightNode::aCacheMembershipWeights;
MObject LHCurveWeightNode::aInputMesh;
MObject LHCurveWeightNode::aProjectionMesh;
MObject LHCurveWeightNode::aCacheWeightMesh;
MObject LHCurveWeightNode::aOutputWeightsFloatArray;
MObject LHCurveWeightNode::aOutWeights;


void* LHCurveWeightNode::creator() { return new LHCurveWeightNode; }

MStatus LHCurveWeightNode::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnCompoundAttribute cAttr;
    MFnEnumAttribute eAttr;


    aInputMesh = tAttr.create("inMesh", "inmesh", MFnData::kMesh);
    addAttribute(aInputMesh);

    aProjectionMesh = tAttr.create("projectionMesh", "pmesh", MFnData::kMesh);
    addAttribute(aProjectionMesh);

    /////// Attrs for compound
    aFactor = nAttr.create( "factor", "f", MFnNumericData::kDouble);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(0.0);
    nAttr.setChannelBox(true);
    addAttribute(aFactor);

    aMembershipWeights = tAttr.create("membershipWeights", "mweights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aMembershipWeights);

    aInputWeights = tAttr.create("inputWeights", "iw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aInputWeights);

    aOperation = eAttr.create("operation", "op", 0);
    eAttr.addField( "add", 0 );
    eAttr.addField( "subtract", 1 );
    eAttr.addField( "multiply", 2 );
    eAttr.addField( "divide", 3 );
    eAttr.setHidden( false );
    eAttr.setKeyable( true );
    eAttr.setWritable(true);
    eAttr.setStorable(true);
    eAttr.setChannelBox(true);
    addAttribute(aOperation);

    aInputs = cAttr.create("Inputs", "inputs");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aInputWeights );
    cAttr.addChild( aFactor );
    cAttr.addChild( aOperation );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    addAttribute(aInputs);

    aOutputWeights = tAttr.create("outWeights", "ow", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(false);
    tAttr.setArray(false);
    tAttr.setWritable(true);
    tAttr.setStorable(true);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aOutputWeights);

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

    attributeAffects(aCacheWeightMesh, aOutputWeights);
    attributeAffects(aInputMesh, aOutputWeights);
    attributeAffects(aProjectionMesh, aOutputWeights);
    attributeAffects(aCacheMembershipWeights, aOutputWeights);
    attributeAffects(aMembershipWeights, aOutputWeights);
    attributeAffects(aOperation, aOutputWeights);
    attributeAffects(aInputWeights, aOutputWeights);
    attributeAffects(aInputs, aOutputWeights);
    attributeAffects(aFactor, aOutputWeights);


    return MStatus::kSuccess;
}


MStatus LHCurveWeightNode::multiplyKDoubleArrayByVal(MDoubleArray &rDoubleArray, double val)
{
    int len = rDoubleArray.length();
    if (!len)
    {
        return MS::kFailure;
    }
    for (int i= 0; i < len; ++i)
    {
        rDoubleArray[i] = rDoubleArray[i] * val;
    }
    return MS::kSuccess;
}


MDoubleArray LHCurveWeightNode::doubleArrayMathOperation(MDoubleArray doubleArray1,
                                                    MDoubleArray doubleArray2,
                                                    short operation)
{
    MDoubleArray rDoubleArray;
    int length1 = doubleArray1.length();
    int length2 = doubleArray2.length();
    if (length1 != length2)
    {
        return rDoubleArray;
    }
    for (int i=0;i < length1;i++)
    {

        switch( operation )
        {
            case 0 : // add
                rDoubleArray.append(doubleArray1[i] + doubleArray2[i]);
                break;
            case 1 : // subtract
                rDoubleArray.append(doubleArray1[i] - doubleArray2[i]);
                break;
            case 2 : // multiply
                rDoubleArray.append(doubleArray1[i] * doubleArray2[i]);
                break;
            case 3 : // divide
                if (doubleArray1[i] == 0.0)
                {
                    doubleArray1[i] = .00001;
                }
                if (doubleArray2[i] == 0.0)
                {
                    doubleArray2[i] = .00001;
                }
                rDoubleArray.append(doubleArray1[i] / doubleArray2[i]);
                break;
        }
    }
    return rDoubleArray;
}


MStatus LHCurveWeightNode::getMeshData(MDataBlock& data, MObject &oInputMesh, MObject &oProjectionMesh)
{
    
    oInputMesh = data.inputValue(LHCurveWeightNode::aInputMesh).asMeshTransformed();
    if (oInputMesh.isNull())
    {
        MGlobal::displayInfo(MString("Unable to get inMesh"));
        return MS::kFailure;

    }
    oProjectionMesh = data.inputValue(LHCurveWeightNode::aProjectionMesh).asMeshTransformed();
    if (oProjectionMesh.isNull())
    {
        MGlobal::displayInfo(MString("Unable to get projectionMesh"));
        return MS::kFailure;
    }
    return MS::kSuccess;
}

MDoubleArray getMembershipWeights(MDataBlock& data, MDoubleArray membershipWeights, int numVerts, int iCacheMemberWeights)
{
    MDoubleArray rMembershipWeights;
    if (!membershipWeights.length() || membershipWeights.length() != numVerts || !iCacheMemberWeights)
    {
        // Get Membership Weights, these will be used to ignore non membership points
        MDataHandle hMembershipArray = data.inputValue( LHCurveWeightNode::aMembershipWeights);
        MObject oMemebershipArray = hMembershipArray.data();
        MFnDoubleArrayData membershipData(oMemebershipArray);
        membershipData.copyTo(rMembershipWeights);
        return rMembershipWeights;
    }
    else
    {
        return membershipWeights;
    }
}

MStatus LHCurveWeightNode::getWeightMeshData(MObject oProjectionMesh, MFnMesh *mInputMesh, MFloatArray &uCoords, MFloatArray &vCoords, int numVerts, int iCacheWeightMesh)
{
    if (!uCoords.length() || uCoords.length() != numVerts || !vCoords.length() || vCoords.length() != numVerts || !iCacheWeightMesh)
    {
        fnWeightIntersector.create(oProjectionMesh);
        if (uCoords.length())
            uCoords.clear();
        if (vCoords.length())
            vCoords.clear();
        for (int i=0;i < numVerts;i++)
        {
            mInputMesh->getPoint(i, pt, MSpace::kObject);
            fnWeightIntersector.getClosestPoint(pt, ptOnMesh);
            mInputMesh->getUVAtPoint( weightPt, uvCoord, MSpace::kObject );
            uCoords.append(uvCoord[0]);
            vCoords.append(uvCoord[1]);
        }
    }
    return MS::kSuccess;
}

MStatus LHCurveWeightNode::compute( const MPlug& plug, MDataBlock& data)
{
    MStatus status;
    if( plug == LHCurveWeightNode::aOutputWeights)
    {
        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHCurveWeightNode::aInputs, &status));
        CheckStatusReturn( status, "Unable to get inputs" );
        unsigned int elemCount = inputsArrayHandle.elementCount(&status);
        CheckStatusReturn( status, "Unable to get number of inputs" );

        // Get mesh objects
        MObject oInputMesh;
        MObject oProjectionMesh;
        status = getMeshData(data, oInputMesh, oProjectionMesh);
        CheckStatusReturn( status, "Unable to get meshes" );
        MFnMesh *mInputMesh = new MFnMesh(oInputMesh);
        int numVerts = mInputMesh->numVertices();
        // MFnMesh mProjectionMesh(oProjectionMesh);

        // Get membership weights
        int iCacheMemberWeights = data.inputValue(aCacheMembershipWeights).asInt();
        membershipWeights = getMembershipWeights(data, membershipWeights, numVerts, iCacheMemberWeights);
        MDoubleArray finalWeights;

        // Get projection mesh data
        int iCacheWeightMesh = data.inputValue(aCacheWeightMesh).asInt();
        status = getWeightMeshData(oProjectionMesh, mInputMesh, uCoords, vCoords, numVerts, iCacheWeightMesh);
        CheckStatusReturn( status, "Unable to get weight mesh" );

        for (int i=0;i < elemCount;i++)
        {
            status = inputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to input element" );
            double dAmount = inputsArrayHandle.inputValue().child( LHCurveWeightNode::aFactor ).asDouble();
            short operation = inputsArrayHandle.inputValue().child( LHCurveWeightNode::aOperation ).asShort();
            MDataHandle hInputArray = inputsArrayHandle.inputValue().child( LHCurveWeightNode::aInputWeights);
            MObject oInputArray = hInputArray.data();
            MFnDoubleArrayData dataDoubleArrayFn(oInputArray);
            MDoubleArray tempWeights;
            dataDoubleArrayFn.copyTo(tempWeights);
            LHCurveWeightNode::multiplyKDoubleArrayByVal(tempWeights, dAmount);
            if (!finalWeights.length())
            {
                finalWeights = tempWeights;
            }
            else
                finalWeights = LHCurveWeightNode::doubleArrayMathOperation(finalWeights, tempWeights, operation);

        }

        ////////Set the final weights
        MFnDoubleArrayData outputDoubleArrayFn;
        MObject oOutputArray = outputDoubleArrayFn.create(finalWeights);
        MDataHandle handle = data.outputValue(LHCurveWeightNode::aOutputWeights);
        handle.setMObject(oOutputArray);

//        MGlobal::displayInfo(MString("DEBUG:  UPDATING ") + status);

        if (oOutputArray.isNull())
        {
            MGlobal::displayInfo(MString("The output is NULL"));
            return MS::kSuccess;
        }
    }

    return MS::kSuccess;
}


MStatus LHCurveWeightNode::setDependentsDirty( MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs)
    {
        if ( (inPlug.attribute() != aInputs)
        & (inPlug.attribute() != aFactor)
        & (inPlug.attribute() != aInputWeights)
        & (inPlug.attribute() != aOperation))
        {
            return MS::kSuccess;
        }

        MPlug outArrayPlug(thisMObject(), aOutputWeights);

        if (inPlug.isElement()) {
            // First dirty the output output element first.
            // Of course, dirty output element itself
            MPlug elemPlug = outArrayPlug.elementByLogicalIndex(
                                                inPlug.logicalIndex());
            affectedPlugs.append(elemPlug);

            // We also need to dirty the parent.
            //
            affectedPlugs.append(outArrayPlug);
        } else {
            // Mark the parent output plug as dirty.
            //
            affectedPlugs.append(outArrayPlug);

            // Also visit each element.
            //
            unsigned int i,n = outArrayPlug.numElements();
            for (i = 0; i < n; i++) {
                MPlug elemPlug = outArrayPlug.elementByPhysicalIndex(i);
                affectedPlugs.append(elemPlug);
            }
        }
        return MS::kSuccess;
    }


