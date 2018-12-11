#include "LHSlideDeformer.h"
#include <maya/MFnPlugin.h>

MTypeId LHSlideDeformer::id(0x00008017);

// tAttrs
MObject LHSlideDeformer::aSurface;
MObject LHSlideDeformer::aSurfaceBase;
// curve weights
MObject LHSlideDeformer::aWeightPatch;
MObject LHSlideDeformer::aRotationAmount;



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






void* LHSlideDeformer::creator() { return new LHSlideDeformer; }

MStatus LHSlideDeformer::deform(MDataBlock& data, MItGeometry& MitGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
    MObject thisMObj( thisMObject() );
    MStatus status;
    MSyntax syntax;
    // envelope
    float envelope = data.inputValue(MPxDeformerNode::envelope).asFloat();


    for (; !MitGeo.isDone();)
    {
        MitGeo.next();
    }
    return MS::kSuccess;
}

MStatus LHSlideDeformer::initialize() {
	MFnTypedAttribute tAttr;
	MFnNumericAttribute nAttr;
	MFnCompoundAttribute cAttr;
	MFnMatrixAttribute mAttr;
    ////////// typed attributes ////////////

    // surface
    aSurface = tAttr.create("surface", "surf", MFnData::kNurbsSurface);
    addAttribute( aSurface );
    // base
    aSurfaceBase = tAttr.create("surfaceBase", "surfbase", MFnData::kNurbsSurface);
    addAttribute( aSurfaceBase );

    // weight patch
    aWeightPatch = tAttr.create("weightPatch", "wpatch", MFnData::kMesh);
    addAttribute( aWeightPatch );

    // numeric attributes

    aRotationAmount = nAttr.create("RotationAmount", "rotamount", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aRotationAmount);


    ////////////////// UATTRS //////////////////////////////////////////////////////

    //////////////////////// VALUE ////////////////////////////////////////////////////
    aUValue = nAttr.create("uValue", "uvalue", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);
//     addAttribute(aUValue)

    aUValueParent = cAttr.create("uValueParentArray", "uValueParentArray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUValue );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUValueParent);


    //child
    aUWeights = tAttr.create("uWeights", "uweights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
//     addAttribute(aUWeights)

    //Parent
    aUWeightsParent = cAttr.create("uWeightsParent", "uweightsparent");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUWeightsParent);

    //ParentParent
    aUWeightsParentArray = cAttr.create("uWeightsParentArray", "uweightsparentarray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUWeightsParentArray);


    aUAnimCurveU = nAttr.create("uAnimCurveU", "uanimcurveu", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    //addAttribute(aUAnimCurveU)

    aUAnimCurveUParent = cAttr.create("uAnimCurveUArray", "uanimcurveuarray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aUAnimCurveU );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aUAnimCurveUParent);

    aUAnimCurveV = nAttr.create("uAnimCurveV", "uanimcurvev", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    //addAttribute(aUAnimCurveV)

    aUAnimCurveVParent = cAttr.create("uAnimCurveVArray", "uanimcurvevarray");
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
    aVValue = nAttr.create("vValue", "vvalue", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);
    addAttribute(aVValue);

    aVValueParent = cAttr.create("vValueParentArray", "vValueParentArray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVValue );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVValueParent);


    //child
    aVWeights = tAttr.create("vWeights", "vweights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    addAttribute(aVWeights);

    //Parent
    aVWeightsParent = cAttr.create("vWeightsParent", "vweightsparent");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVWeightsParent);

    //ParentParent
    aVWeightsParentArray = cAttr.create("vWeightsParentArray", "vweightsparentarray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVWeightsParentArray);


    aVAnimCurveU = nAttr.create("vAnimCurveU", "vanimcurveu", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    //addAttribute(aVAnimCurveU)

    aVAnimCurveUParent = cAttr.create("vAnimCurveUArray", "vanimcurveuarray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aVAnimCurveU );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aVAnimCurveUParent);

    aVAnimCurveV = nAttr.create("vAnimCurveV", "vanimcurvev", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    //addAttribute(aVAnimCurveV)

    aVAnimCurveVParent = cAttr.create("vAnimCurveVArray", "vanimcurvevarray");
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

    aNValue = nAttr.create("nValue", "nvalue", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);
//     addAttribute(aNValue)

    aNValueParent = cAttr.create("nValueParentArray", "nValueParentArray");
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
    aNWeights = tAttr.create("nWeights", "nweights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
//     addAttribute(aNWeights)

    //Parent
    aNWeightsParent = cAttr.create("nWeightsParent", "nweightsparent");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aNWeightsParent);

    //ParentParent
    aNWeightsParentArray = cAttr.create("nWeightsParentArray", "nweightsparentarray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aNWeightsParentArray);


    aNAnimCurveU = nAttr.create("nAnimCurveU", "nanimcurveu", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    //addAttribute(aNAnimCurveU)

    aNAnimCurveUParent = cAttr.create("nAnimCurveUArray", "nanimcurveuarray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aNAnimCurveU );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aNAnimCurveUParent);

    aNAnimCurveV = nAttr.create("nAnimCurveV", "nanimcurvev", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    //addAttribute(aNAnimCurveV)

    aNAnimCurveVParent = cAttr.create("nAnimCurveVArray", "nanimcurvevarray");
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

    aRValue = nAttr.create("rValue", "rvalue", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setDefault(0.0);
//     addAttribute(aRValue)

    aRValueParent = cAttr.create("rValueParentArray", "rValueParentArray");
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
    aRWeights = tAttr.create("rWeights", "rweights", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
//     addAttribute(aRWeights)

    //Parent
    aRWeightsParent = cAttr.create("rWeightsParent", "rweightsparent");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRWeights );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRWeightsParent);

    //ParentParent
    aRWeightsParentArray = cAttr.create("rWeightsParentArray", "rweightsparentarray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRWeightsParent );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRWeightsParentArray);


    aRAnimCurveU = nAttr.create("rAnimCurveU", "ranimcurveu", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    //addAttribute(aRAnimCurveU)

    aRAnimCurveUParent = cAttr.create("rAnimCurveUArray", "ranimcurveuarray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRAnimCurveU );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRAnimCurveUParent);

    aRAnimCurveV = nAttr.create("rAnimCurveV", "ranimcurvev", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    //addAttribute(aRAnimCurveV)

    aRAnimCurveVParent = cAttr.create("rAnimCurveVArray", "ranimcurvevarray");
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
    aRPivot = tAttr.create("rPivotCurve", "rpivotcurve", MFnData::kNurbsCurve);
    addAttribute( aRPivot );

    aRPivotArray = cAttr.create("rPivotCurveArray", "rpivotcurvearray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aRPivot );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aRPivotArray);





    //////Affects outputs and inputs

    MObject outputGeom = MPxDeformerNode::outputGeom;

    // tAttrs
    attributeAffects(aSurface, outputGeom);
    attributeAffects(aSurfaceBase, outputGeom);

    attributeAffects(aWeightPatch, outputGeom);

    // U ATTRS

    attributeAffects(aUValue, outputGeom);
    attributeAffects(aUValueParent, outputGeom);

    attributeAffects(aUWeights, outputGeom);
    attributeAffects(aUWeightsParent, outputGeom);
    attributeAffects(aUWeightsParentArray, outputGeom);

    attributeAffects(aVValue, outputGeom);

    attributeAffects(aUAnimCurveU, outputGeom);
    attributeAffects(aUAnimCurveUParent, outputGeom);

    attributeAffects(aUAnimCurveV, outputGeom);
    attributeAffects(aUAnimCurveVParent, outputGeom);

    // V ATTRS

    attributeAffects(aVValue, outputGeom);
    attributeAffects(aVValueParent, outputGeom);

    attributeAffects(aVWeights, outputGeom);
    attributeAffects(aVWeightsParent, outputGeom);
    attributeAffects(aVWeightsParentArray, outputGeom);


    attributeAffects(aVAnimCurveU, outputGeom);
    attributeAffects(aVAnimCurveUParent, outputGeom);

    attributeAffects(aVAnimCurveV, outputGeom);
    attributeAffects(aVAnimCurveVParent, outputGeom);

    // N ATTRS

    attributeAffects(aNValue, outputGeom);
    attributeAffects(aNValueParent, outputGeom);

    attributeAffects(aNWeights, outputGeom);
    attributeAffects(aNWeightsParent, outputGeom);
    attributeAffects(aNWeightsParentArray, outputGeom);


    attributeAffects(aNAnimCurveU, outputGeom);
    attributeAffects(aNAnimCurveUParent, outputGeom);

    attributeAffects(aNAnimCurveV, outputGeom);
    attributeAffects(aNAnimCurveVParent, outputGeom);

    // R ATTRS

    attributeAffects(aRValue, outputGeom);
    attributeAffects(aRValueParent, outputGeom);

    attributeAffects(aRWeights, outputGeom);
    attributeAffects(aRWeightsParent, outputGeom);
    attributeAffects(aRWeightsParentArray, outputGeom);


    attributeAffects(aRAnimCurveU, outputGeom);
    attributeAffects(aRAnimCurveUParent, outputGeom);

    attributeAffects(aRAnimCurveV, outputGeom);
    attributeAffects(aRAnimCurveVParent, outputGeom);

    attributeAffects(aRPivot, outputGeom);
    attributeAffects(aRPivotArray, outputGeom);



    // Make deformer weights paintable


    MGlobal::executeCommand("makePaintable -attrType multiFloat -shapeMode deformer LHSlideDeformer weights;");

    // Make deformer weights paintable

  return MS::kSuccess;
}

MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  status = plugin.registerNode("LHSlideDeformer", LHSlideDeformer::id, LHSlideDeformer::creator,
                               LHSlideDeformer::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHSlideDeformer::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

