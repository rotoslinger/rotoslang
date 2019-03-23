//==============================================================
// Ultra simple blendshape deformer that allows 1 target only
// This deformer is only meant to blend between 2 deformer stacks
// The maya blendshape has a weight attribute that is difficult to connect weight stacks to, (you have to connect individual weight elements per point)
// so this deformer has been written to make this process simpler and allow the entire array of point weights to be connected.
// This is mostly to allow for interactive feedback of weight stack influences.  Once weighting is finished, weights can be saved out and the maya
// blendshape can be reapplied with these weights.
// The idea behind using the maya blendshape is the fact that it is cpu and gpu multithreaded and optimized,
// while the blendshapeSimple only works on a single thread and is limited to a single target.
//==============================================================

#include "LHCurveRollSimple.h"

MTypeId LHCurveRollSimple::id(0x56873254);
MObject LHCurveRollSimple::aAmount;
MObject LHCurveRollSimple::aTargetGeo;
MObject LHCurveRollSimple::aTargetWeights;
// MObject LHCurveRollSimple::aMembershipWeights;

MStatus LHCurveRollSimple::initialize() {
    MFnNumericAttribute nAttr;
    MFnGenericAttribute gAttr;
    MFnTypedAttribute tAttr;

    aAmount = nAttr.create("amount", "amnt", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setMin(0);
    nAttr.setMax(1);
    addAttribute(aAmount);
    attributeAffects(aAmount, outputGeom);

    aTargetGeo = gAttr.create("targetGeo", "targetgeo");
    gAttr.addAccept(MFnData::kMesh);
    gAttr.addAccept(MFnData::kNurbsSurface);
    gAttr.addAccept(MFnData::kNurbsCurve);
    gAttr.addAccept(MFnData::kLattice);
    addAttribute(aTargetGeo);
    attributeAffects(aTargetGeo, outputGeom);

    aTargetWeights = tAttr.create("targetWeights", "targetweights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aTargetWeights);
    attributeAffects(aTargetWeights, outputGeom);

    // aMembershipWeights = tAttr.create("membershipWeights", "membershipweights", MFnNumericData::kDoubleArray);
    // tAttr.setKeyable(true);
    // tAttr.setArray(false);
    // tAttr.setUsesArrayDataBuilder(false);
    // addAttribute(aMembershipWeights);
    // attributeAffects(aMembershipWeights, outputGeom);

    // MGlobal::executeCommand("makePaintable -attrType doubleArray -sm deformer LHCurveRollSimple membershipWeights;");

    return MS::kSuccess;
}

void* LHCurveRollSimple::creator() { return new LHCurveRollSimple; }

MStatus LHCurveRollSimple::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
    MStatus status;
    float env = data.inputValue(envelope).asFloat();

    // Only ever want 1 target
    if (mIndex > 0 or env==0)
    {
      return MS::kSuccess;
    }

    float amount = data.inputValue(aAmount).asFloat();
    env = env * amount;

    // Geo target geometry
    MDataHandle hTargetGeo = data.inputValue(aTargetGeo, &status);
    CheckStatusReturn( MS::kFailure, "couldn't get target handle" );
    bool isNumeric;
    bool isNull;
    hTargetGeo.isGeneric( isNumeric, isNull );
    if (isNull)
    {
      CheckStatusReturn( MS::kFailure, "target geometry has not been connected" );
    }
    MItGeometry targetIter(hTargetGeo, true, &status);
    CheckStatusReturn( status, "Couldn't get target geom" );

    if (itGeo.count() != targetIter.count())
    {
      CheckStatusReturn( MS::kFailure, "the source and target geometry have different point count, make sure geo matches" );
    }

    // get weights
    MDataHandle hWeights = data.inputValue(aTargetWeights, &status);
    CheckStatusReturn( status, "Couldn't get weights" );
    MDoubleArray weights = MFnDoubleArrayData(hWeights.data()).array(&status);
    CheckStatusReturn( status, "Couldn't get weights" );
    if (itGeo.count() <= weights.length())
    {
      CheckStatusReturn( MS::kFailure, "Weights count does not match the source geometry point count.  Make sure to set a weight value for each index. " );
    }
    // hWeights = data.inputValue(aMembershipWeights, &status);
    // CheckStatusReturn( status, "Couldn't get weights" );
    // MDoubleArray membershipWeights = MFnDoubleArrayData(hWeights.data()).array(&status);
    // CheckStatusReturn( status, "Couldn't get weights" );
    // if (itGeo.count() <= weights.length())
    // {
    //   CheckStatusReturn( MS::kFailure, "Weights count does not match the source geometry point count.  Make sure to set a weight value for each index. " );
    // }

    MPointArray allTargetPoints;
    targetIter.allPositions(allTargetPoints, MSpace::kObject);
    MPoint pt;
    int idx;
    double w;
    for (; !itGeo.isDone(); itGeo.next())
    {
      idx = itGeo.index();
      w = weights[idx] * env;
      pt = itGeo.position();
      itGeo.setPosition(pt + (allTargetPoints[idx] - pt) * w);
    }
    return MS::kSuccess;
}

