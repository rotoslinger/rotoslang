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

#include "LHVectorDeformerSimple.h"

MTypeId LHVectorDeformerSimple::id(0x24358709);
MObject LHVectorDeformerSimple::aAmount;
// MObject LHVectorDeformerSimple::aNormalize;
MObject LHVectorDeformerSimple::aVectorCurve;
MObject LHVectorDeformerSimple::aVectorWeights;
// MObject LHVectorDeformerSimple::aMembershipWeights;

MStatus LHVectorDeformerSimple::initialize() {
    MFnNumericAttribute nAttr;
    MFnTypedAttribute tAttr;

    aAmount = nAttr.create("amount", "amnt", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    // nAttr.setMin(0);
    // nAttr.setMax(1);
    nAttr.setDefault(1.0);
    addAttribute(aAmount);
    attributeAffects(aAmount, outputGeom);

    aVectorCurve = tAttr.create("vectorCurve", "vectorCurve", MFnData::kNurbsCurve);
    addAttribute( aVectorCurve );
    attributeAffects(aVectorCurve, outputGeom);

    aVectorWeights = tAttr.create("vectorWeights", "vectorWeights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVectorWeights);
    attributeAffects(aVectorWeights, outputGeom);

    return MS::kSuccess;
}

void* LHVectorDeformerSimple::creator() { return new LHVectorDeformerSimple; }

MStatus LHVectorDeformerSimple::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
    MStatus status;
    float env = data.inputValue(envelope).asFloat();
    if (!env)
    {
      MS::kSuccess;
    }

    float amount = data.inputValue(aAmount).asFloat();
    env = env * amount;

    // Geo target geometry
    MDataHandle hVectorCurve = data.inputValue(aVectorCurve, &status);
    CheckStatusReturn( MS::kFailure, "couldn't get target handle" );

    MObject oCurve = data.inputValue(aVectorCurve).asNurbsCurveTransformed();

    if (oCurve.isNull())
    {
      CheckStatusReturn( MS::kFailure, "Connect the world space of a nurbs curve with 2 points that describe a directional vector" );
    }

    MFnNurbsCurve fnCurve( oCurve,  &status );
    CheckStatusReturn( status, "Unable to Make curve" );

    fnCurve.getCV(0, toPoint, MSpace::kWorld);
    fnCurve.getCV(1, fromPoint, MSpace::kWorld);

    MVector direction = fromPoint - toPoint;
    
    // get weights
    MDataHandle hWeights = data.inputValue(aVectorWeights, &status);
    CheckStatusReturn( status, "Couldn't get weights" );

    MDoubleArray weights = MFnDoubleArrayData(hWeights.data()).array(&status);
    CheckStatusReturn( status, "Couldn't get weights" );

    if (itGeo.count() <= weights.length())
    {
      CheckStatusReturn( MS::kFailure, "Weights count does not match the source geometry point count.  Make sure to set a weight value for each index. " );
    }

    for (; !itGeo.isDone(); itGeo.next())
    {
      idx = itGeo.index();
      w = weights[idx] * env;
      pt = itGeo.position();
      itGeo.setPosition(pt + (direction) * w);
    }
    return MS::kSuccess;
}

