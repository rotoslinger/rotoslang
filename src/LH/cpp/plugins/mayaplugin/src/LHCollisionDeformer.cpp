//==============================================================
// Ultra simple deformer to be used as a starter template//////
// In commented out lines you can see steps involved in trying to get as much speed as possible
// such as not getting painted weight values on every iteration
// Tried putting all positions into an array and setting all positions at once
// because it is supposed to be faster, but this was actually 3fps slower on a mesh of 39,000 points...
// also, not setting pt to a variable, just doing the whole algorithm in one step was 2 fps faster
// If weights are needed, they should be gathered outside the main loop
// and even cached into a std::vector <MFloatArray> with a boolean attribute to turn caching on and off
//==============================================================

#include "LHCollisionDeformer.h"
#include "threading.cpp"
#include <maya/MFnPlugin.h>

MTypeId LHCollisionDeformer::id(0x67438467);
MObject LHCollisionDeformer::aBulgeAmount;
MObject LHCollisionDeformer::aBulgeDistance;
MObject LHCollisionDeformer::aColGeo;
MObject LHCollisionDeformer::aInputs;

MObject LHCollisionDeformer::aMainBBoxMinX;
MObject LHCollisionDeformer::aMainBBoxMinY;
MObject LHCollisionDeformer::aMainBBoxMinZ;
MObject LHCollisionDeformer::aMainBBoxMaxX;
MObject LHCollisionDeformer::aMainBBoxMaxY;
MObject LHCollisionDeformer::aMainBBoxMaxZ;

MObject LHCollisionDeformer::aMainBBMin;
MObject LHCollisionDeformer::aMainBBMax;
MObject LHCollisionDeformer::aMainWorldMatrix;

MObject LHCollisionDeformer::aColBBoxMinX;
MObject LHCollisionDeformer::aColBBoxMinY;
MObject LHCollisionDeformer::aColBBoxMinZ;
MObject LHCollisionDeformer::aColBBoxMaxX;
MObject LHCollisionDeformer::aColBBoxMaxY;
MObject LHCollisionDeformer::aColBBoxMaxZ;

MObject LHCollisionDeformer::aColBBMin;
MObject LHCollisionDeformer::aColBBMax;
MObject LHCollisionDeformer::aColWorldMatrix;
MObject LHCollisionDeformer::aPermanent;
MObject LHCollisionDeformer::aFlipCheck;

MObject LHCollisionDeformer::aBlendBulgeCollision;
MObject LHCollisionDeformer::aFalloffRamp;
MObject LHCollisionDeformer::aInnerFalloffRamp;
MObject LHCollisionDeformer::aBlendBulgeCollisionRamp;

MObject LHCollisionDeformer::aAlgorithm;
// Weights
MObject LHCollisionDeformer::aCollisionWeights;
MObject LHCollisionDeformer::aBulgeWeights;
// WeightParents
MObject LHCollisionDeformer::aWeightsParent;

MObject LHCollisionDeformer::aCacheWeights;
MObject LHCollisionDeformer::aMainInputs;


MObject LHCollisionDeformer::aMultiThread;
MObject LHCollisionDeformer::aNumTasks;
MObject LHCollisionDeformer::aGrainSize;

// MObject LHCollisionDeformer::aAllowCapsule;
// MObject LHCollisionDeformer::aAllowPerPoly;
MObject LHCollisionDeformer::aDefType;


MObject LHCollisionDeformer::tmpCapsuleCurve;

MObject LHCollisionDeformer::tmpCapsuleRadius;
MObject LHCollisionDeformer::tmpCapsuleMatrix;
MObject LHCollisionDeformer::tmpCapsuleAllowScale;



MObject LHCollisionDeformer::aPrimCapsuleCurve;
MObject LHCollisionDeformer::aPrimCapsuleType;
MObject LHCollisionDeformer::aPrimCapsuleRadiusA;
MObject LHCollisionDeformer::aPrimCapsuleRadiusB;
MObject LHCollisionDeformer::aPrimCapsuleRadiusC;
MObject LHCollisionDeformer::aPrimCapsuleRadiusD;
MObject LHCollisionDeformer::aPrimCapsuleMatrix;
MObject LHCollisionDeformer::aPrimCapsuleAllowScale;

MObject LHCollisionDeformer::aPrimCollisionInputs;
MObject LHCollisionDeformer::aPrimCollisionWeights;
MObject LHCollisionDeformer::aPrimBulgeWeights;
MObject LHCollisionDeformer::aPrimWeightsParent;
MObject LHCollisionDeformer::aPrimLengthA;
MObject LHCollisionDeformer::aPrimLengthB;
MObject LHCollisionDeformer::aPrimBulgeAmount;
MObject LHCollisionDeformer::aPrimBulgeDistance;
MObject LHCollisionDeformer::aPrimBulgeClampStart;
MObject LHCollisionDeformer::aPrimBulgeClampEnd;

MStatus LHCollisionDeformer::initialize() {
  MFnNumericAttribute nAttr;
  MFnGenericAttribute gAttr;
  MFnCompoundAttribute cAttr;
  MFnMatrixAttribute mAttr;
  MRampAttribute rAttr;
  MFnTypedAttribute tAttr;
  MFnEnumAttribute eAttr;


  //Col Matrix
  tmpCapsuleMatrix = mAttr.create("capsuleMatrix", "capmat");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( tmpCapsuleMatrix );
  attributeAffects(tmpCapsuleMatrix, outputGeom);

  tmpCapsuleCurve = tAttr.create("capsuleCurve", "ccurve", MFnData::kNurbsCurve);
  addAttribute( tmpCapsuleCurve );
  attributeAffects(tmpCapsuleCurve, outputGeom);

  tmpCapsuleRadius = nAttr.create("capsuleRadius", "cradius", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(tmpCapsuleRadius);
  attributeAffects(tmpCapsuleRadius, outputGeom);

  tmpCapsuleAllowScale = nAttr.create( "allowScale", "allowscale", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setMin(0);
  nAttr.setMax(1);
  nAttr.setDefault(1);
  nAttr.setChannelBox(true);
  addAttribute( tmpCapsuleAllowScale );
  attributeAffects(tmpCapsuleAllowScale, outputGeom);

  aDefType = eAttr.create("deformationType", "deftyp", 0);
  eAttr.addField( "mesh", 0 );
  eAttr.addField( "capsule", 1 );
  eAttr.setHidden( false );
  eAttr.setKeyable( true );
  eAttr.setWritable(true);
  eAttr.setStorable(true);
  eAttr.setChannelBox(true);
  addAttribute(aDefType);
  attributeAffects(aDefType, outputGeom);





  /////////////////////////////////////////////////////////////////////////////////////
  // CAPSULE STUFF
  aPrimCapsuleCurve = tAttr.create("pCapsuleCurve", "pcapcurve", MFnData::kNurbsCurve);
  addAttribute( aPrimCapsuleCurve );
  attributeAffects(aPrimCapsuleCurve, outputGeom);

  aPrimCapsuleMatrix = mAttr.create("pCapsuleMatrix", "pcapmat");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aPrimCapsuleMatrix );
  attributeAffects(aPrimCapsuleMatrix, outputGeom);

  aPrimCapsuleRadiusA = nAttr.create("capsuleRadiusA", "cradiusa", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusA);
  attributeAffects(aPrimCapsuleRadiusA, outputGeom);

  aPrimCapsuleRadiusB = nAttr.create("capsuleRadiusB", "cradiusb", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusB);
  attributeAffects(aPrimCapsuleRadiusB, outputGeom);

  aPrimCapsuleRadiusC = nAttr.create("capsuleRadiusC", "cradiusc", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusC);
  attributeAffects(aPrimCapsuleRadiusC, outputGeom);

  aPrimCapsuleRadiusD = nAttr.create("capsuleRadiusD", "cradiusd", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusD);
  attributeAffects(aPrimCapsuleRadiusD, outputGeom);

  aPrimLengthA = nAttr.create("pLengthA", "plena", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(0.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimLengthA);
  attributeAffects(aPrimLengthA, outputGeom);

  aPrimLengthB = nAttr.create("pLengthB", "plenb", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(0.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimLengthB);
  attributeAffects(aPrimLengthB, outputGeom);

  aPrimBulgeAmount = nAttr.create("pBulgeAmount", "pbulgea", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimBulgeAmount);
  attributeAffects(aPrimBulgeAmount, outputGeom);

  aPrimBulgeDistance = nAttr.create("pBulgeDistance", "pbulged", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimBulgeDistance);
  attributeAffects(aPrimBulgeDistance, outputGeom);

  aPrimBulgeClampStart = nAttr.create("pBulgeClampStart", "pbulgecs", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(0.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimBulgeClampStart);
  attributeAffects(aPrimBulgeClampStart, outputGeom);


  aPrimBulgeClampEnd = nAttr.create("pBulgeClampEnd", "pbulgece", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(0.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimBulgeClampEnd);
  attributeAffects(aPrimBulgeClampEnd, outputGeom);


  aPrimCapsuleAllowScale = nAttr.create( "pAllowScale", "pallowscale", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setMin(0);
  nAttr.setMax(1);
  nAttr.setDefault(1);
  nAttr.setChannelBox(true);
  addAttribute( aPrimCapsuleAllowScale );
  attributeAffects(aPrimCapsuleAllowScale, outputGeom);

  aPrimCapsuleType = eAttr.create("primType", "ptyp", 0);
  eAttr.addField( "sphere", 0 );
  eAttr.addField( "elipsoidCapsule", 1 );
  eAttr.addField( "elipsoid", 2 );
  eAttr.addField( "cylinder", 3 );
  eAttr.addField( "plane", 4 );
  eAttr.addField( "capsule", 5 );
  eAttr.addField( "cone", 6 );
  eAttr.setHidden( false );
  eAttr.setKeyable( true );
  eAttr.setWritable(true);
  eAttr.setStorable(true);
  eAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleType);
  attributeAffects(aPrimCapsuleType, outputGeom);

  aPrimCollisionWeights = tAttr.create("pCollisionWeights", "pcweights", MFnNumericData::kDoubleArray);
  tAttr.setKeyable(true);
  tAttr.setArray(false);
  tAttr.setReadable(true);
  tAttr.setUsesArrayDataBuilder(true);
  addAttribute(aPrimCollisionWeights);
  attributeAffects(aPrimCollisionWeights, outputGeom);

  aPrimBulgeWeights = tAttr.create("pBulgeWeights", "pbWeights", MFnNumericData::kDoubleArray);
  tAttr.setKeyable(true);
  tAttr.setArray(false);
  tAttr.setReadable(true);
  tAttr.setUsesArrayDataBuilder(true);
  addAttribute(aPrimBulgeWeights);
  attributeAffects(aPrimBulgeWeights, outputGeom);

  aPrimWeightsParent = cAttr.create("pWeightsParent", "pweightsparent");
  cAttr.setKeyable(true);
  cAttr.setArray(true);
  cAttr.addChild( aPrimCollisionWeights );
  cAttr.addChild( aPrimBulgeWeights );
  cAttr.setReadable(true);
  cAttr.setUsesArrayDataBuilder(true);
  addAttribute(aPrimWeightsParent);
  attributeAffects(aPrimWeightsParent, outputGeom);

  aPrimCollisionInputs = cAttr.create("primitiveCollisionInputs", "primcolin");
  cAttr.addChild( aPrimCapsuleCurve );
  cAttr.addChild( aPrimCapsuleMatrix );
  cAttr.addChild( aPrimCapsuleRadiusA );
  cAttr.addChild( aPrimCapsuleRadiusB );
  cAttr.addChild( aPrimCapsuleRadiusC );
  cAttr.addChild( aPrimCapsuleRadiusD );
  cAttr.addChild( aPrimBulgeAmount );
  cAttr.addChild( aPrimBulgeDistance );
  cAttr.addChild( aPrimBulgeClampStart );
  cAttr.addChild( aPrimBulgeClampEnd );
  cAttr.addChild( aPrimCapsuleAllowScale );
  cAttr.addChild( aPrimCapsuleType );
  cAttr.addChild( aPrimWeightsParent );
  cAttr.addChild( aPrimLengthA );
  cAttr.addChild( aPrimLengthB );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  cAttr.setArray(true);
  cAttr.setUsesArrayDataBuilder(true);
  addAttribute(aPrimCollisionInputs);
  attributeAffects(aPrimCollisionInputs, outputGeom);

  /////////////////////////////////////////////////////////////////////////////////////









  aMultiThread = nAttr.create( "multiThread", "mthread", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setMin(0);
  nAttr.setMax(2);
  nAttr.setDefault(1);
  nAttr.setChannelBox(true);
  addAttribute( aMultiThread );
  attributeAffects(aMultiThread, outputGeom);

  aNumTasks = nAttr.create( "numTasks", "nt", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(16);
  nAttr.setChannelBox(true);
  addAttribute( aNumTasks );
  attributeAffects(aNumTasks, outputGeom);

  aGrainSize = nAttr.create( "grainSize", "gsize", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1000);
  nAttr.setChannelBox(true);
  addAttribute( aGrainSize );
  attributeAffects(aGrainSize, outputGeom);


  aCollisionWeights = nAttr.create("collisionWeights", "cweights", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setArray(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setUsesArrayDataBuilder(true);
  addAttribute(aCollisionWeights);

  aBulgeWeights = nAttr.create("bulgeWeights", "bWeights", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setArray(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setUsesArrayDataBuilder(true);
  addAttribute(aBulgeWeights);

  aWeightsParent = cAttr.create("weightsParent", "pweights");
  cAttr.setKeyable(true);
  cAttr.setArray(true);
  cAttr.addChild( aCollisionWeights );
  cAttr.addChild( aBulgeWeights );
  cAttr.setReadable(true);
  cAttr.setUsesArrayDataBuilder(true);
  addAttribute(aWeightsParent);

  attributeAffects(aBulgeWeights, outputGeom);
  attributeAffects(aCollisionWeights, outputGeom);
  attributeAffects(aWeightsParent, outputGeom);

  //Permanent
  aCacheWeights = nAttr.create("cacheWeights", "cacheweights", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0);
  nAttr.setMin(0);
  nAttr.setMax(1);
  addAttribute(aCacheWeights);
  attributeAffects(aCacheWeights, outputGeom);

  aAlgorithm = eAttr.create("operation", "op", 0);
  eAttr.addField( "cheap", 0 );
  eAttr.addField( "flipCheck", 1 );
  eAttr.addField( "blend", 2 );
  eAttr.setHidden( false );
  eAttr.setKeyable( true );
  eAttr.setWritable(true);
  eAttr.setStorable(true);
  eAttr.setChannelBox(true);
  addAttribute(aAlgorithm);
  attributeAffects(aAlgorithm, outputGeom);


	aBlendBulgeCollisionRamp = rAttr.createCurveRamp("blendBulgeCollisionRamp", "bbulgecolramp");
  addAttribute(aBlendBulgeCollisionRamp);
  attributeAffects(aBlendBulgeCollisionRamp, outputGeom);


  //Permanent
  aPermanent = nAttr.create("permanent", "perm", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0);
  nAttr.setMin(0);
  nAttr.setMax(1);
  addAttribute(aPermanent);
  attributeAffects(aPermanent, outputGeom);


  //Main Matrix
  aMainWorldMatrix = mAttr.create("mainWorldMatrix", "mwmatrix");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aMainWorldMatrix );
  attributeAffects(aMainWorldMatrix, outputGeom);


  //Main BBOXES
  aMainBBoxMinX = nAttr.create("mainBBMinX", "mainbbminx", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMinX);
  attributeAffects(aMainBBoxMinX, outputGeom);

  aMainBBoxMinY = nAttr.create("mainBBMinY", "mainbbminy", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMinY);
  attributeAffects(aMainBBoxMinY, outputGeom);

  aMainBBoxMinZ = nAttr.create("mainBBMinZ", "mainbbminz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMinZ);
  attributeAffects(aMainBBoxMinZ, outputGeom);

  aMainBBMin = cAttr.create("mainBBMin", "mainbbmin");
  cAttr.addChild( aMainBBoxMinX );
  cAttr.addChild( aMainBBoxMinY );
  cAttr.addChild( aMainBBoxMinZ );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aMainBBMin);
  attributeAffects(aMainBBMin, outputGeom);


  aMainBBoxMaxX = nAttr.create("mainBBMaxX", "mainbbmaxx", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMaxX);
  attributeAffects(aMainBBoxMaxX, outputGeom);

  aMainBBoxMaxY = nAttr.create("mainBBMaxY", "mainbbmaxy", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMaxY);
  attributeAffects(aMainBBoxMaxY, outputGeom);

  aMainBBoxMaxZ = nAttr.create("mainBBMaxZ", "mainbbmaxz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aMainBBoxMaxZ);
  attributeAffects(aMainBBoxMaxZ, outputGeom);

  aMainBBMax = cAttr.create("mainBBMax", "mainbbmax");
  cAttr.addChild( aMainBBoxMaxX );
  cAttr.addChild( aMainBBoxMaxY );
  cAttr.addChild( aMainBBoxMaxZ );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aMainBBMax);
  attributeAffects(aMainBBMax, outputGeom);



  aMainInputs = cAttr.create("deformInputArray", "definarray");
  cAttr.setKeyable(false);
  cAttr.setArray(true);
  cAttr.addChild( aMainBBMin );
  cAttr.addChild( aMainBBMax );
  cAttr.addChild( aMainWorldMatrix );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  cAttr.setUsesArrayDataBuilder(true);
  addAttribute(aMainInputs);
  attributeAffects(aMainInputs, outputGeom);
  
///ARRAY BOUNDS
//
  //Col Matrix
  aColWorldMatrix = mAttr.create("colWorldMatrix", "colwmatrix");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aColWorldMatrix );
  attributeAffects(aColWorldMatrix, outputGeom);


  //Col BBOXES
  aColBBoxMinX = nAttr.create("colBBMinX", "colbbminx", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMinX);
  attributeAffects(aColBBoxMinX, outputGeom);

  aColBBoxMinY = nAttr.create("colBBMinY", "colbbminy", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMinY);
  attributeAffects(aColBBoxMinY, outputGeom);

  aColBBoxMinZ = nAttr.create("colBBMinZ", "colbbminz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMinZ);
  attributeAffects(aColBBoxMinZ, outputGeom);

  aColBBMin = cAttr.create("colBBMin", "colbbmin");
  cAttr.addChild( aColBBoxMinX );
  cAttr.addChild( aColBBoxMinY );
  cAttr.addChild( aColBBoxMinZ );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aColBBMin);
  attributeAffects(aColBBMin, outputGeom);


  aColBBoxMaxX = nAttr.create("colBBMaxX", "colbbmaxx", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMaxX);
  attributeAffects(aColBBoxMaxX, outputGeom);

  aColBBoxMaxY = nAttr.create("colBBMaxY", "colbbmaxy", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMaxY);
  attributeAffects(aColBBoxMaxY, outputGeom);

  aColBBoxMaxZ = nAttr.create("colBBMaxZ", "colbbmaxz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setChannelBox(true);
  nAttr.setDefault(0.0);
  addAttribute(aColBBoxMaxZ);
  attributeAffects(aColBBoxMaxZ, outputGeom);

  aColBBMax = cAttr.create("colBBMax", "colbbmax");
  cAttr.addChild( aColBBoxMaxX );
  cAttr.addChild( aColBBoxMaxY );
  cAttr.addChild( aColBBoxMaxZ );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aColBBMax);
  attributeAffects(aColBBMax, outputGeom);

  aBulgeAmount = nAttr.create("bulgeAmount", "bamnt", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  nAttr.setDefault(1.0);
  addAttribute(aBulgeAmount);
  attributeAffects(aBulgeAmount, outputGeom);

  aBulgeDistance = nAttr.create("bulgeDistance", "bdist", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  nAttr.setDefault(1.0);
  addAttribute(aBulgeDistance);
  attributeAffects(aBulgeDistance, outputGeom);

  aColGeo = tAttr.create("inputGeo", "ingeo", MFnData::kMesh);
  addAttribute(aColGeo);
  attributeAffects(aColGeo, outputGeom);

  aInputs = cAttr.create("colliderInputArray", "colinarray");
  cAttr.setKeyable(false);
  cAttr.setArray(true);
  cAttr.addChild( aColBBMin );
  cAttr.addChild( aColBBMax );
  cAttr.addChild( aColWorldMatrix );
  cAttr.addChild( aColGeo );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  cAttr.setUsesArrayDataBuilder(true);
  addAttribute(aInputs);
  attributeAffects(aInputs, outputGeom);

	aFalloffRamp = rAttr.createCurveRamp("falloffShape", "fshape");
  addAttribute(aFalloffRamp);
  attributeAffects(aFalloffRamp, outputGeom);

	aInnerFalloffRamp = rAttr.createCurveRamp("falloffShapeInner", "fshapein");
  addAttribute(aInnerFalloffRamp);
  attributeAffects(aInnerFalloffRamp, outputGeom);

  // Make the deformer weights paintable
  // MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer LHCollisionDeformer weights;");
  MGlobal::executeCommand("makePaintable -attrType multiDouble -shapeMode deformer LHCollisionDeformer collisionWeights;");
  MGlobal::executeCommand("makePaintable -attrType multiDouble -shapeMode deformer LHCollisionDeformer bulgeWeights;");


  return MS::kSuccess;
}

//===Post Constructor===
 


MStatus postConstructor_initialise_ramp_curve( MObject parentNode, MObject rampObj, int index, float position, float value, int interpolation){
  MStatus status;
  MPlug rampPlug( parentNode, rampObj );
  MPlug elementPlug = rampPlug.elementByLogicalIndex( index, &status );
  MPlug positionPlug = elementPlug.child(0, &status);
  status = positionPlug.setFloat(position);
  MPlug valuePlug = elementPlug.child(1);
  status = valuePlug.setFloat(value);
  MPlug interpPlug = elementPlug.child(2);
  interpPlug.setInt(interpolation);
  return MS::kSuccess;
}


void LHCollisionDeformer::postConstructor(){
MStatus status;
MObject thisMObj(LHCollisionDeformer::thisMObject());
// Not in a loop because eventually these will be customized individually, possibly based on the bounding box of the geo...
postConstructor_initialise_ramp_curve( thisMObj, aFalloffRamp, 0, 0.0f, 1.0f, 2 );
postConstructor_initialise_ramp_curve( thisMObj, aFalloffRamp, 1, 1.0f, 0.0f, 2 );
postConstructor_initialise_ramp_curve( thisMObj, aInnerFalloffRamp, 0, 0.0f, 1.0f, 2 );
postConstructor_initialise_ramp_curve( thisMObj, aInnerFalloffRamp, 1, 1.0f, 0.0f, 2 );
postConstructor_initialise_ramp_curve( thisMObj, aBlendBulgeCollisionRamp, 0, 0.0f, 0.0f, 2 );
postConstructor_initialise_ramp_curve( thisMObj, aBlendBulgeCollisionRamp, 1, 1.0f, 1.0f, 2 );
}

double SafelyGetWeights(std::vector <MDoubleArray> weights, unsigned int currentMIndex, unsigned int currentPointIndex){
// Bitwise && to make sure if anything fails it won't check the condition to the right...
if (weights.size() && weights.size() >= currentMIndex && weights[currentMIndex].length() && weights[currentMIndex].length() >= currentPointIndex){
  return weights[currentMIndex][currentPointIndex];
}
return 1.0;
}

double SafelyGetMDoubleArrayWeights(MDoubleArray weights, unsigned int currentPointIndex){
// Bitwise && to make sure if anything fails it won't check the condition to the right...
if (weights.length() && weights.length() >= currentPointIndex){
  return weights[currentPointIndex];
}
return 1.0;
}


MBoundingBox LHCollisionDeformer::getBoundingBox(MDataBlock& data, MMatrix worldMatrix, MObject oMinBB, MObject oMaxBB,
                                                 MArrayDataHandle mainArrayHandle, unsigned int index){
    MStatus status;
    status = mainArrayHandle.jumpToElement(index);
    double3& minBB = mainArrayHandle.inputValue().child( oMinBB).asDouble3();
    double3& maxBB = mainArrayHandle.inputValue().child( oMaxBB).asDouble3();
	  MPoint minBBPoint(minBB[0], minBB[1], minBB[2]);
	  MPoint maxBBPoint(maxBB[0], maxBB[1], maxBB[2]);
	  MBoundingBox mainBB(minBBPoint, maxBBPoint);
	  mainBB.transformUsing(worldMatrix);
	  return mainBB;
}

MBoundingBox LHCollisionDeformer::getBoundingBoxMultiple(MDataBlock& data, MMatrix &colWorldMatrix, MObject oMinBB, MObject oMaxBB,
												 unsigned int index, MObject oCompound){
	  MArrayDataHandle compoundArrayHandle(data.inputArrayValue( oCompound));

    compoundArrayHandle.jumpToElement(index);
    double3& minBB =compoundArrayHandle.inputValue().child( oMinBB ).asDouble3();
    double3& maxBB =compoundArrayHandle.inputValue().child( oMaxBB ).asDouble3();
	  MPoint minBBPoint(minBB[0], minBB[1], minBB[2]);
	  MPoint maxBBPoint(maxBB[0], maxBB[1], maxBB[2]);
	  MBoundingBox mainBB(minBBPoint, maxBBPoint);
	  mainBB.transformUsing(colWorldMatrix);
	  return mainBB;
}

MStatus LHCollisionDeformer::RetrieveWeightsForAllIndicies(MObject weightsParent, MObject weights, int numIndex, std::vector <MDoubleArray> &weightsArray,
                                                           MPlug inPlug, MDataBlock& data){

  MStatus status;
  if (weightsArray.size()){
    weightsArray.clear();
  }
  for( i = 0; i < numIndex; ++i)
  {
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //Find out how many points are in each piece of geo that will be deformed, if non fail safely and create a dummy count of 0
    MArrayDataHandle ahInput = data.inputArrayValue(input, &status) ;
    CheckStatusReturn( status, "Unable to Make ahInput" );
    try{
        status = ahInput.jumpToElement( i ) ;
    }
    catch(...){
        iterGeoCount = 0;
    }
    if (status == MS::kSuccess){
        // if status fails set array to 0
        MDataHandle dhInput = ahInput.inputValue(&status) ;
        CheckStatusReturn( status, "Unable to dhInput" );

      MDataHandle dhWeightChild = dhInput.child( inputGeom ) ;
      CheckStatusReturn( status, "Unable to ahWeightChild" );


        MItGeometry iter( dhWeightChild, true, &status );
        iterGeoCount = iter.count(&status);
        CheckStatusReturn( status, "Unable to Make iterGeoCount" );
    }
    if(iterGeoCount > 0){
        rWeights.clear();
        status = getPlugWeightValues(weightsParent, weights, iterGeoCount, i, rWeights);
        CheckStatusReturn( status, "Unable to get weightsArray" );
        weightsArray.push_back(rWeights);
    }
    else
    {
      dummyWeights.clear();
      dummyWeights.setLength(1) ;
      dummyWeights[0] = 0.0;
      weightsArray.push_back(dummyWeights);
    }
  }
  return MS::kSuccess;
}

MStatus LHCollisionDeformer::getCapsuleWeights(MDataBlock& data, std::vector<MDoubleArray> &rColWeights,
                                               std::vector<MDoubleArray> &rBulgeWeights, MArrayDataHandle inputsArrayHandle)
{




  MStatus status;
  MDataHandle weightsHandle = inputsArrayHandle.inputValue().child(LHCollisionDeformer::aPrimWeightsParent);
  MArrayDataHandle weightsArrayHandle(weightsHandle);
  weightsCount = weightsArrayHandle.elementCount(&status);

  CheckStatusReturn( status, "Can't find weight elements" );
  for (x=0;x < weightsCount; x++){
    weightsArrayHandle.jumpToElement(x);
    MDataHandle handle(weightsArrayHandle.inputValue(&status) );
    CheckStatusReturn( status, "Couldn't get array handle" );

    MDataHandle colChild(handle.child( aPrimBulgeWeights) );
    // MFnDoubleArrayData newData(colChild.data());
    MDoubleArray dABulgeWeights = MFnDoubleArrayData(colChild.data()).array(&status);
    CheckStatusReturn( status, "Couldn't get bulgeWeights" );
    rBulgeWeights.push_back(dABulgeWeights);
    MDataHandle bulgeChild(handle.child( aPrimCollisionWeights) );
    // MFnDoubleArrayData newData(bulgeChild.data());
    MDoubleArray dACollisionWeights = MFnDoubleArrayData(bulgeChild.data()).array(&status);
    CheckStatusReturn( status, "Couldn't get collisionWeights" );
    rColWeights.push_back(dACollisionWeights);

  }
  return MS::kSuccess;

}



MStatus LHCollisionDeformer::getCapsuleData(MDataBlock& data, CapsuleData &rCapsuleData)
{
  CapsuleData fCapsuleData;
  MStatus status;
  // MDoubleArray bulgeWeights;
  // MDoubleArray collisionWeights;
  std::vector <std::vector <MDoubleArray>> colWeights;
  std::vector <std::vector <MDoubleArray>> bulgeWeights;

  // Get Input Array
  MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHCollisionDeformer::aPrimCollisionInputs, &status));
  CheckStatusReturn( status, "Unable to get inputs" );
  inputCount = inputsArrayHandle.elementCount(&status);
  MObject oTestCurve;
  CheckStatusReturn( status, "Unable to get number of inputs" );
  for (i=0;i < inputCount; i++){
      status = inputsArrayHandle.jumpToElement(i);
      CheckStatusReturn( status, "Unable to jump to element" );
      oTestCurve =inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimCapsuleCurve).asNurbsCurveTransformed();
      if (oTestCurve.isNull()){
        CheckStatusReturn( status, "Unable to get curve" );
    	  continue;
      }
      
      MFnNurbsCurve testCurve(oTestCurve);
      testCurve.getCVs(capsuleCurvePoints, MSpace::kObject);
      fCapsuleData.pPointAArray.append(capsuleCurvePoints[0]);
      fCapsuleData.pPointBArray.append(capsuleCurvePoints[1]);
      fCapsuleData.dRadiusAArray.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimCapsuleRadiusA).asDouble());
      fCapsuleData.dRadiusBArray.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimCapsuleRadiusB).asDouble());
      fCapsuleData.dRadiusCArray.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimCapsuleRadiusC).asDouble());
      fCapsuleData.dRadiusDArray.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimCapsuleRadiusD).asDouble());
      fCapsuleData.mWorldMatrixArray.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimCapsuleMatrix).asMatrix());
      fCapsuleData.allowScaleArray.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimCapsuleAllowScale).asInt());
      fCapsuleData.eTypeArray.push_back(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimCapsuleType).asShort());
      fCapsuleData.dLengthAArray.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimLengthA).asDouble());
      fCapsuleData.dLengthBArray.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimLengthB).asDouble());
      fCapsuleData.dBulgeAmount.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimBulgeAmount).asDouble());
      fCapsuleData.dBulgeDistance.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimBulgeDistance).asDouble());
      fCapsuleData.dBulgeClampStart.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimBulgeClampStart).asDouble());
      fCapsuleData.dBulgeClampEnd.append(inputsArrayHandle.inputValue().child( LHCollisionDeformer::aPrimBulgeClampEnd).asDouble());


      std::vector<MDoubleArray> rColWeights;
      std::vector<MDoubleArray> rBulgeWeights;

      MStatus status;
      MDataHandle weightsHandle = inputsArrayHandle.inputValue().child(LHCollisionDeformer::aPrimWeightsParent);
      MArrayDataHandle weightsArrayHandle(weightsHandle);
      weightsCount = weightsArrayHandle.elementCount(&status);

      CheckStatusReturn( status, "Can't find weight elements" );
      for (x=0;x < weightsCount; x++){
        weightsArrayHandle.jumpToElement(x);
        MDataHandle handle(weightsArrayHandle.inputValue(&status) );
        CheckStatusReturn( status, "Couldn't get array handle" );

        MDataHandle colChild(handle.child( aPrimBulgeWeights) );
        // MFnDoubleArrayData newData(colChild.data());
        MDoubleArray dABulgeWeights = MFnDoubleArrayData(colChild.data()).array(&status);
        CheckStatusReturn( status, "Couldn't get bulgeWeights" );
        rBulgeWeights.push_back(dABulgeWeights);
        MDataHandle bulgeChild(handle.child( aPrimCollisionWeights) );
        // MFnDoubleArrayData newData(bulgeChild.data());
        MDoubleArray dACollisionWeights = MFnDoubleArrayData(bulgeChild.data()).array(&status);
        CheckStatusReturn( status, "Couldn't get collisionWeights" );
        rColWeights.push_back(dACollisionWeights);
      }

      colWeights.push_back(rColWeights);
      bulgeWeights.push_back(rBulgeWeights);
      }

  rCapsuleData = fCapsuleData;
  if (!fCapsuleData.pPointAArray.length())
    return MS::kFailure;

  rCapsuleData.numCapsules = fCapsuleData.pPointAArray.length();
  rCapsuleData.colWeights = colWeights;
  rCapsuleData.bulgeWeights = bulgeWeights;

    // MGlobal::displayInfo(MString("BULGE WEIGHT 0 in get weights!!!!!!!!!!!!!!!!!!!!!!!!")+ rCapsuleData.bulgeWeights[0][0][0]);

    // MGlobal::displayInfo(MString("BULGE WEIGHT 1 in get weights!!!!!!!!!!!!!!!!!!!!!!!!")+ rCapsuleData.bulgeWeights[1][0][0]);

    // MGlobal::displayInfo(MString("BULGE WEIGHT 2 in get weights!!!!!!!!!!!!!!!!!!!!!!!!")+ rCapsuleData.bulgeWeights[2][0][0]);



  return MS::kSuccess;
}

void* LHCollisionDeformer::creator() { return new LHCollisionDeformer; }

MStatus LHCollisionDeformer::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;
  MObject thisMObj( thisMObject() );

  currentMIndex = mIndex;
   //////////// get highest index in array //////////////////

  if (indexIntArray.size()){
    indexIntArray.clear();
  }
  MPlug inPlug(thisMObj, input);
  inPlug.getExistingArrayAttributeIndices(indices,&status);
  CheckStatusReturn( status, "Unable to get NumIndexes" );

  indicesLength = indices.length();

  //loop to put indices into std vector
  for( i = 0; i < indicesLength; ++i)
  {
      indexIntArray.push_back(indices[i]);
  }

  if (indicesLength == 1)
      numIndex = indices[0]+1;
  if (indicesLength == 2)
      numIndex = std::max(indices[0],indices[1])+1;
  if (indicesLength >= 3)
      numIndex = *(max_element(indexIntArray.begin(), indexIntArray.end()))+1;

  //Retrieve all data
  float env = data.inputValue(envelope).asFloat();
  if (env<=0.0)
	  return MS::kSuccess;
  float bulgeAmount = data.inputValue(aBulgeAmount).asFloat();
  float bulgeDistance = data.inputValue(aBulgeDistance).asFloat();
  eAlgorithm = data.inputValue(aAlgorithm).asShort();
  int cacheWeights = data.inputValue( aCacheWeights ).asInt();
  int iNumTasks = data.inputValue( LHCollisionDeformer::aNumTasks ).asInt();
  iMultiThread = data.inputValue( LHCollisionDeformer::aMultiThread ).asInt();
  iGrainSize = data.inputValue( LHCollisionDeformer::aGrainSize ).asInt();
  oCapsuleCurve = data.inputValue(tmpCapsuleCurve).asNurbsCurveTransformed();
  oCapsuleRadius = data.inputValue(tmpCapsuleRadius).asDouble();
  mCapsuleMatrix = data.inputValue(tmpCapsuleMatrix).asMatrix();
  iAllowScale = data.inputValue(tmpCapsuleAllowScale).asInt();

  short eDefType = data.inputValue( LHCollisionDeformer::aDefType ).asShort();


  LHCollisionDeformer::getCapsuleData(data, capsuleData);
  
  // Set up some caching logic, make sure if the state of iPermanent changes we are aware of it for the first iteration
  int permCheck = iPermanent;
  iPermanent = data.inputValue( LHCollisionDeformer::aPermanent ).asInt();
  if (permCheck != iPermanent)
  {
    permanentChanged = true;
  }
  else
  {
    permanentChanged = false;
  }

  // Get weights
	if((!bulgeWeightsArray.size() ||  bulgeWeightsArray.size() < numIndex) || !cacheWeights){
  status = LHCollisionDeformer::RetrieveWeightsForAllIndicies(aWeightsParent, aBulgeWeights, numIndex, bulgeWeightsArray, inPlug, data);
  CheckStatusReturn( status, "Unable to get bulge Weights" );
  }

	if((!collisionWeightsArray.size() || collisionWeightsArray.size() < numIndex) || !cacheWeights){
  status = LHCollisionDeformer::RetrieveWeightsForAllIndicies(aWeightsParent, aCollisionWeights, numIndex, collisionWeightsArray, inPlug, data);
  CheckStatusReturn( status, "Unable to get collision Weights" );
  }

  // Get ramps
  MRampAttribute rFalloffRamp(thisMObj, aFalloffRamp);
  MRampAttribute rInnerFalloffRamp(thisMObj, aInnerFalloffRamp);
  MRampAttribute rBlendBulgeCollisionRamp(thisMObj, aBlendBulgeCollisionRamp);


  MArrayDataHandle mainArrayHandle(data.inputArrayValue( LHCollisionDeformer::aMainInputs, &status));
  CheckStatusReturn( status, "Unable to get deformer inputs" );
  inputCount = mainArrayHandle.elementCount(&status);
  CheckStatusReturn( status, "Unable to get number of inputs" );
  if (inputCount<=mIndex){
	  return MS::kSuccess;
  }
  status = mainArrayHandle.jumpToElement(mIndex);
  CheckStatusReturn( status, "Unable to jump to element" );
  MMatrix bBMatrix = mainArrayHandle.inputValue().child( LHCollisionDeformer::aMainWorldMatrix).asMatrix();


  mainBB = getBoundingBox(data, bBMatrix, LHCollisionDeformer::aMainBBMin, LHCollisionDeformer::aMainBBMax, mainArrayHandle, mIndex);

  //Get collision geo
  MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHCollisionDeformer::aInputs, &status));
  CheckStatusReturn( status, "Unable to get inputs" );
  inputCount = inputsArrayHandle.elementCount(&status);
  CheckStatusReturn( status, "Unable to get number of inputs" );
  MObjectArray oColMeshArray;
  std::vector <MBoundingBox> colBBArray;
  MMatrixArray colMatrices;
  for (i=0;i < inputCount; i++){
      status = inputsArrayHandle.jumpToElement(i);
      oTestMesh =inputsArrayHandle.inputValue().child( LHCollisionDeformer::aColGeo).asMeshTransformed();
      colMatrix =inputsArrayHandle.inputValue().child( LHCollisionDeformer::aColWorldMatrix ).asMatrix();
      colMatrices.append(colMatrix);
      colBBArray.push_back(LHCollisionDeformer::getBoundingBoxMultiple(data, colMatrix, LHCollisionDeformer::aColBBMin,
    		               LHCollisionDeformer::aColBBMax, inputCount, LHCollisionDeformer::aInputs));
      if (oTestMesh.isNull()){
    	  continue;
      }
      oColMeshArray.append(oTestMesh);
  }


  int nColMeshes = oColMeshArray.length();
  if (!nColMeshes)
	  return MS::kSuccess;

  //===============================================================================================================
  // Get the main mesh from the MpxDeformer class
  MArrayDataHandle inputGeoArrayHandle(data.inputArrayValue( input, &status));
  status = inputGeoArrayHandle.jumpToElement(mIndex);
  CheckStatusReturn( status, "Unable to get inputGeom" );
  oMainMesh =inputGeoArrayHandle.inputValue().child( inputGeom ).asMeshTransformed();
  if (oMainMesh.isNull()){
	 MGlobal::displayInfo(MString("DEBUG: oMainMesh is null "));
	 return MS::kFailure;
  }
  // MFnMesh fnMainMesh(oMainMesh);
  MFnMesh* fnMainMesh = new MFnMesh(oMainMesh);

  MPoint tmptstPoint;
  fnMainMesh->getPoint(0,tmptstPoint);

  fnMainMesh->getPoints(countTest);

  // =============== This will set up the std::vector to store the points ===============
  if (!allPointsArray.size()){
      allPointsArray.push_back(countTest);
  }
  if (allPointsArray.size() && allPointsArray.size()-1 <= mIndex){
      allPointsArray.push_back(countTest);
  }

  if (!allPointsArray[mIndex].length()){
      allPointsArray[mIndex] = countTest;
  }

  if (allPointsArray[mIndex].length() && allPointsArray[mIndex].length() != countTest.length())
  {
    allPointsArray[mIndex] = countTest;
  }
  //======================================================================================

  // If permanent store the currently posed points, if not reset every iteration
  if (iPermanent & !permanentChanged){
      allPoints = allPointsArray[mIndex];
        for (i = 0; i < numPoints; i++)
        {
          allPoints[i] = allPoints[i] * bBMatrix;
        }
  }
  else{
      fnMainMesh->getPoints(allPoints);
      allPointsArray[mIndex] = allPoints;
  }

  numPoints = allPoints.length();

///////////////////////////////// CAPSULE IMPLEMENTATION //////////////////////////////////////////////////////////
  if (eDefType == 1)
  {

    if (!oCapsuleCurve.isNull()) {
      MFnMesh* newMainMesh = new MFnMesh(oMainMesh);
      LHCollisionDeformer::primitiveCollision(allPoints, newMainMesh, bulgeAmount, bulgeDistance, rFalloffRamp, bBMatrix);
    }
  }

// ///////////////////////////////// MESH PER POINT IMPLEMENTATION //////////////////////////////////////////////////////////
  if (eDefType == 0)
  {
    LHCollisionDeformer::perPolyDeformation(allPoints, colMatrices, oColMeshArray, fnMainMesh, bulgeDistance, bulgeAmount, rInnerFalloffRamp, rFalloffRamp, rBlendBulgeCollisionRamp, itGeo, bBMatrix);
  }


  // Do the deformation
  for (i = 0; i < allPoints.length(); i++)
  {
    allPoints[i] = allPoints[i] * bBMatrix.inverse();
  }
  allPointsArray[currentMIndex] = allPoints;
  itGeo.setAllPositions(allPoints);

  return MS::kSuccess;
}

void LHCollisionDeformer::primitiveCollision(MPointArray &allPoints, MFnMesh *newMainMesh, double bulgeAmount, double bulgeDistance,
                        MRampAttribute rFalloffRamp, MMatrix bBMatrix)
{
  for (x = 0; x < capsuleData.numCapsules; x++)
  {
    LHCollisionDeformer::capsuleDeformation(x, allPoints, newMainMesh, bulgeAmount, bulgeDistance, rFalloffRamp, bBMatrix);
  }
}


MDoubleArray safelyGetArrayWeights(std::vector <std::vector <MDoubleArray>> arrayWeights, unsigned int parentIndex, unsigned int childIndex, unsigned int targetPointCount)
{

    if (arrayWeights.size() && arrayWeights[parentIndex].size() && arrayWeights[parentIndex][childIndex].length() && arrayWeights[parentIndex][childIndex].length() >= targetPointCount)
    {
      return arrayWeights[parentIndex][childIndex];
    }
    else
    {
      MDoubleArray allOnes;
      for (unsigned int i = 0; i < targetPointCount; i++)
      {
        allOnes.append(1.0);

      }
      return allOnes;
    }
}


// MPointArray getCapsuleFrame(MMatrix capsuleWorldMatrix, MVectorArray &boundsData, MPoint &startUpVector, MPoint &endUpVector, MPoint start, MPoint end, MPoint &capsuleCenter)
// {

//     capsuleCenter = start + 0.5 * (start-end);

//     MPoint startupvec(0.0, 1, 0.0);
//     MPoint endupvec = end + startupvec;

//     MPoint capCenter(1, 1, 1);
//     MPoint capY(-0.5, -0.5, 0.5);
//     MPoint capZ(-0.5, -0.5, -0.5);
//     MPoint capX(0.5, -0.5, 0.5);



//     MPoint capNegX(-0.5, 0.0, 0.0);
//     MPoint capNegY(0.0, -0.5, 0.0);
//     MPoint capNegZ(0.0, 0.0, -0.5);

//     startUpVector = startupvec * capsuleWorldMatrix;
//     endUpVector = endupvec * capsuleWorldMatrix.inverse();

    
//     capCenter = capCenter * capsuleWorldMatrix;
//     capY = capY * capsuleWorldMatrix;
//     capZ = capZ * capsuleWorldMatrix;
//     capNegX = capNegX * capsuleWorldMatrix;
//     capNegY = capNegY * capsuleWorldMatrix;
//     capNegZ = capNegZ * capsuleWorldMatrix;
//     MPointArray framePoints;
//     framePoints.append(capCenter);
//     framePoints.append(capX);
//     framePoints.append(capY);
//     framePoints.append(capZ);
//     boundsData.append(capCenter - capX);
//     boundsData.append(capCenter - capY);
//     boundsData.append(capCenter - capZ);

//     return framePoints;
// }

MVector convertMPointToMVector(MPoint pnt)
{
        MVector vec;
        vec.x = pnt.x;
        vec.y = pnt.y;
        vec.z = pnt.z;
        return vec;
}

void getMaxDisplacement(MPoint pPointFrom, MPoint pPointTo, double &currMaxVal)
{
    double dCheckVal = pPointFrom.distanceTo(pPointTo);
    if (dCheckVal > currMaxVal)
    {
        currMaxVal = dCheckVal;
    }
}

double getLengthOfPointProjectedToLine(MPoint point, MPoint lineStart, MPoint lineEnd)
{
  MPoint newPoint;
  double lineMagnitude = lineEnd.distanceTo(lineStart);
  return ( ( ( point.x - lineStart.x ) * ( lineEnd.x - lineStart.x ) ) +
               ( ( point.y - lineStart.y ) * ( lineEnd.y - lineStart.y ) ) +
               ( ( point.z - lineStart.z ) * ( lineEnd.z - lineStart.z ) ) ) /
                 ( lineMagnitude * lineMagnitude );
}


bool getClosestPointOnPlane(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, bool bulge, unsigned int i)
{
  double uParam = getLengthOfPointProjectedToLine(point, capsuleStart, capsuleEnd);

  if (bulge || uParam <= 0.0 )
  {
    MVector direction = capsuleStart - capsuleEnd;
    // direction.normalize();
    closestPoint = point + ( direction ) * uParam;
    return true;
  }
  else
  {
    closestPoint = point;
    return false;
  }
}

void LHCollisionDeformer::planePointLogic(MPoint &closestPoint, MPointArray &allPoints, unsigned int currentIdx,
                                          double &maxDisp, MIntArray &hitPoints, bool &capsuleHit, MPoint capsuleStart, MPoint capsuleEnd)
{
  if (getClosestPointOnPlane(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, false, currentIdx ))
  {
    getMaxDisplacement(allPoints[currentIdx], closestPoint, dispCheck, maxDisp);
    allPoints[currentIdx] = closestPoint;
    hitPoints.append(1);
    capsuleHit = true;
  }
  else
  {
    hitPoints.append(0);
  }
}

void LHCollisionDeformer::planeBulgeLogic(MPointArray &allPoints, unsigned int currentIdx,  MPoint capsuleStart, MPoint capsuleEnd, MFnMesh *newMainMesh, double bulgeDistance,
                                             double bulgeAmount, MRampAttribute rFalloffRamp, double bulgeWeight)
{
  getClosestPointOnPlane(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, true, currentIdx );
  distanceToCenter = allPoints[currentIdx].distanceTo(closestPoint);
  if (distanceToCenter < bulgeDistance)
  {
    newMainMesh->getVertexNormal(currentIdx, vRay);
    vRay.normalize();
    allPoints[currentIdx] = LHCollisionDeformer::getCapsuleBulge(allPoints[currentIdx], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp, bulgeWeight);
  }
}

MPoint getClosestPointOnSphere(MPoint testPoint, MPoint capsuleStart, double radius){
        MVector capsuleSurfaceDirection = testPoint - capsuleStart;
        capsuleSurfaceDirection.normalize();
        return capsuleStart + capsuleSurfaceDirection * radius;
}


bool getClosestPointOnCapsule(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, unsigned int i, double radiusA, double radiusB)
{
  double uParam = getLengthOfPointProjectedToLine(point, capsuleStart, capsuleEnd);

  MVector direction = capsuleEnd - capsuleStart;
  // direction.normalize();

  double modulationValue = uParam;

  if (modulationValue>1.0)
  {
    // check whether within the sphere, if so project to sphere
    if (point.distanceTo(capsuleEnd) < radiusB)
    {
      closestPoint = getClosestPointOnSphere(point, capsuleEnd, radiusB);
      return true;
    }
    else
    {
      closestPoint = point;
      return false;
    }
  }
  if (modulationValue < 0.0)
  {
    if (point.distanceTo(capsuleStart) < radiusA)
    {
      closestPoint = getClosestPointOnSphere(point, capsuleStart, radiusA);
      return true;
    }
    else
    {
      closestPoint = point;
      return false;
    }
  }

  double currentRadius = radiusA + (radiusB-radiusA) * modulationValue;
  MPoint closestPointOnCurve = capsuleStart + ( direction ) * uParam;

  if (point.distanceTo(closestPointOnCurve) < currentRadius)
  {
    MVector directionVec(point-closestPointOnCurve);
    directionVec.normalize();
    closestPoint = closestPointOnCurve + directionVec * currentRadius;
    return true;
  }
  else
  {
    closestPoint = point;
    return false;
  }

}


bool projectPointOnCapsule(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, unsigned int i, double radiusA, double radiusB)
{
  double uParam = getLengthOfPointProjectedToLine(point, capsuleStart, capsuleEnd);
  // if (i == 21)
  //   MGlobal::displayInfo(MString(" ") + uParam);
  MVector direction = capsuleEnd - capsuleStart;
  // direction.normalize();
  double modulationValue = uParam;
  if (modulationValue>1.0)
  {
    closestPoint = getClosestPointOnSphere(point, capsuleEnd, radiusB);
    return true;
  }
  if (modulationValue < 0.0)
  {
    closestPoint = getClosestPointOnSphere(point, capsuleStart, radiusA);
    return true;
  }
  double currentRadius = radiusA + (radiusB-radiusA) * modulationValue;
  MPoint closestPointOnCurve = capsuleStart + ( direction ) * uParam;
  MVector directionVec(point-closestPointOnCurve);
  directionVec.normalize();
  closestPoint = closestPointOnCurve + directionVec * currentRadius;
}




void LHCollisionDeformer::capsuleBulgeLogic(MPointArray &allPoints, unsigned int currentIdx,  MPoint capsuleStart, MPoint capsuleEnd, double radiusA, double radiusB, MFnMesh *newMainMesh, double bulgeDistance,
                                double bulgeAmount, MRampAttribute rFalloffRamp, double bulgeWeight)
{
  projectPointOnCapsule(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB);
  distanceToCenter = allPoints[currentIdx].distanceTo(closestPoint);
  if (distanceToCenter < bulgeDistance)
  {
    newMainMesh->getVertexNormal(currentIdx, vRay);
    vRay.normalize();
    allPoints[currentIdx] = LHCollisionDeformer::getCapsuleBulge(allPoints[currentIdx], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp, bulgeWeight);
  }
}


void LHCollisionDeformer::capsulePointLogic(MPoint &closestPoint, MPointArray &allPoints, unsigned int currentIdx,
                                            double &maxDisp, MIntArray &hitPoints, bool &capsuleHit, MPoint capsuleStart, MPoint capsuleEnd, double radiusA, double radiusB)
{
  if (getClosestPointOnCapsule(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB))
  {
    getMaxDisplacement(allPoints[currentIdx], closestPoint, dispCheck, maxDisp);
    allPoints[currentIdx] = closestPoint;
    hitPoints.append(1);
    capsuleHit = true;
  }
  else
  {
    hitPoints.append(0);
  }
}
void getClosestPointOnPlaneCylindrical(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, bool bulge, double radius)
{
  double uParam = getLengthOfPointProjectedToLine(point, capsuleStart, capsuleEnd);
  MVector direction = capsuleStart - capsuleEnd;
  // direction.normalize();
  MPoint pointOnPlane = point + ( direction ) * uParam;
  direction = pointOnPlane - capsuleStart;
  direction.normalize();
  // If it is further away than the radius, bring to the edge of the radius
  if (pointOnPlane.distanceTo(capsuleStart) > radius)
  {
    closestPoint = capsuleStart + direction * radius;
  }
  else
  {
    closestPoint = pointOnPlane;

  }
}


bool projectPointOnCylinder(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, unsigned int i, double radiusA, double radiusB)
{
  double uParam = getLengthOfPointProjectedToLine(point, capsuleStart, capsuleEnd);
  // if (i == 21)
  //   MGlobal::displayInfo(MString(" ") + uParam);
  MVector direction = capsuleEnd - capsuleStart;
  // direction.normalize();
  double modulationValue = uParam;
  if (modulationValue>1.0)
  {
    getClosestPointOnPlaneCylindrical(point, closestPoint, capsuleEnd, capsuleStart, true, radiusB);

    return true;
  }
  if (modulationValue < 0.0)
  {
    getClosestPointOnPlaneCylindrical(point, closestPoint, capsuleStart, capsuleEnd, true, radiusA);
    return true;
  }
  double currentRadius = radiusA + (radiusB-radiusA) * modulationValue;
  MPoint closestPointOnCurve = capsuleStart + ( direction ) * uParam;
  MVector directionVec(point-closestPointOnCurve);
  directionVec.normalize();
  closestPoint = closestPointOnCurve + directionVec * currentRadius;
}



bool closestPointOnCylinder(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, unsigned int i, double radiusA, double radiusB)
{
  double uParam = getLengthOfPointProjectedToLine(point, capsuleStart, capsuleEnd);
  // if (i == 21)
  //   MGlobal::displayInfo(MString(" ") + uParam);
  MVector direction = capsuleEnd - capsuleStart;
  // direction.normalize();
  double modulationValue = uParam;
  if (modulationValue>1.0)
  {
    if (getClosestPointOnPlane(point, closestPoint, capsuleStart, capsuleEnd, false, 0 ))
    {

      return true;
    }
    else
    {
      closestPoint = point;
      return false;
    }
  }
  if (modulationValue < 0.0)
    if (getClosestPointOnPlane(point, closestPoint, capsuleEnd, capsuleStart, false, 0 ))
    {

      return true;
    }
    else
    {
      closestPoint = point;
      return false;
    }
  double currentRadius = radiusA + (radiusB-radiusA) * modulationValue;
  MPoint closestPointOnCurve = capsuleStart + ( direction ) * uParam;

  if (point.distanceTo(closestPointOnCurve) < currentRadius)
  {
    MVector directionVec(point-closestPointOnCurve);
    directionVec.normalize();
    closestPoint = closestPointOnCurve + directionVec * currentRadius;
    return true;
  }
  else
  {
    closestPoint = point;
    return false;
  }

}

void LHCollisionDeformer::cylinderBulgeLogic(MPointArray &allPoints, unsigned int currentIdx,  MPoint capsuleStart, MPoint capsuleEnd, double radiusA, double radiusB, MFnMesh *newMainMesh, double bulgeDistance,
                                double bulgeAmount, MRampAttribute rFalloffRamp, double bulgeWeight)
{
  projectPointOnCylinder(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB);
  distanceToCenter = allPoints[currentIdx].distanceTo(closestPoint);
  if (distanceToCenter < bulgeDistance)
  {
    newMainMesh->getVertexNormal(currentIdx, vRay);
    vRay.normalize();
    allPoints[currentIdx] = LHCollisionDeformer::getCapsuleBulge(allPoints[currentIdx], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp, bulgeWeight);
  }
}



void LHCollisionDeformer::cylinderPointLogic(MPoint &closestPoint, MPointArray &allPoints, unsigned int currentIdx,
                                            double &maxDisp, MIntArray &hitPoints, bool &capsuleHit, MPoint capsuleStart, MPoint capsuleEnd, double radiusA, double radiusB)
{
    // projectPointOnCylinder(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB);
    // allPoints[currentIdx] = closestPoint;

  if (closestPointOnCylinder(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB))
  {
    getMaxDisplacement(allPoints[currentIdx], closestPoint, dispCheck, maxDisp);
    allPoints[currentIdx] = closestPoint;
    hitPoints.append(1);
    capsuleHit = true;
  }
  else
  {
    hitPoints.append(0);
  }
}

void projectPointOnEllipsoid(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, unsigned int i, double radiusA, double radiusB, double radiusC, MMatrix capsuleMatrix)
{
  MVector collsionVector = point - capsuleStart;
  collsionVector = collsionVector * capsuleMatrix.inverse();
  double uParam = ((collsionVector.x * collsionVector.x)/(radiusA * radiusA)) + ((collsionVector.y * collsionVector.y)/(radiusB*radiusB)) + ((collsionVector.z * collsionVector.z)/(radiusC*radiusC));
  double lenToSurface = sqrt(1/uParam);
  collsionVector = collsionVector * capsuleMatrix;
  closestPoint = capsuleStart + collsionVector *lenToSurface;
}

bool getClosestPointOnEllipsoid(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, unsigned int i, double radiusA, double radiusB, double radiusC, MMatrix capsuleMatrix)
{
  MVector collsionVector = point - capsuleStart;
  collsionVector = collsionVector * capsuleMatrix.inverse();
  double uParam = ((collsionVector.x * collsionVector.x)/(radiusA * radiusA)) + ((collsionVector.y * collsionVector.y)/(radiusB*radiusB)) + ((collsionVector.z * collsionVector.z)/(radiusC*radiusC));
  if (uParam < 1)
  {
    double lenToSurface = sqrt(1/uParam);
    collsionVector = collsionVector * capsuleMatrix;
    closestPoint = capsuleStart + collsionVector *lenToSurface;
    return true;
  }
  else
  {
    return false;
  }
}




void LHCollisionDeformer::ellipsoidPointLogic(MPoint &closestPoint, MPointArray &allPoints, unsigned int currentIdx,
                                            double &maxDisp, MIntArray &hitPoints, bool &capsuleHit, MPoint capsuleStart,
                                            MPoint capsuleEnd, double radiusA, double radiusB, double radiusC, MMatrix capsuleMatrix)
{
    // getClosestPointOnEllipsoid(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB, radiusC, capsuleMatrix);
    // allPoints[currentIdx] = closestPoint;

  if (getClosestPointOnEllipsoid(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB, radiusC, capsuleMatrix))
  {
    getMaxDisplacement(allPoints[currentIdx], closestPoint, dispCheck, maxDisp);
    allPoints[currentIdx] = closestPoint;
    hitPoints.append(1);
    capsuleHit = true;
  }
  else
  {
    hitPoints.append(0);
  }
}

void LHCollisionDeformer::ellipsoidBulgeLogic(MPointArray &allPoints, unsigned int currentIdx,  MPoint capsuleStart, MPoint capsuleEnd, double radiusA, double radiusB,
                                              double radiusC, MMatrix capsuleMatrix, MFnMesh *newMainMesh, double bulgeDistance, double bulgeAmount, MRampAttribute rFalloffRamp, double bulgeWeight)
{
  projectPointOnEllipsoid(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB, radiusC, capsuleMatrix);
  distanceToCenter = allPoints[currentIdx].distanceTo(closestPoint);
  if (distanceToCenter < bulgeDistance)
  {
    newMainMesh->getVertexNormal(currentIdx, vRay);
    vRay.normalize();
    allPoints[currentIdx] = LHCollisionDeformer::getCapsuleBulge(allPoints[currentIdx], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp, bulgeWeight);
  }
}

bool getClosestPointOnEllipsoidCapsule(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, unsigned int i, double radiusA, double radiusB,
                                       double radiusC, double radiusD, MMatrix capsuleMatrix, unsigned int currentIdx)
{
  double uParam = getLengthOfPointProjectedToLine(point, capsuleStart, capsuleEnd);

  MVector direction = capsuleEnd - capsuleStart;
  // direction.normalize();

  double modulationValue = uParam;

  if (modulationValue>1.0)
  {
    // check whether within the sphere, if so project to sphere
    if (getClosestPointOnEllipsoid(point, closestPoint, capsuleEnd, capsuleStart, currentIdx, radiusB, radiusB, radiusD, capsuleMatrix))
    {
      return true;
    }
    else
    {
      closestPoint = point;
      return false;
    }
  }
  if (modulationValue < 0.0)
  {
    if (getClosestPointOnEllipsoid(point, closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusA, radiusC, capsuleMatrix))
    {
      return true;
    }
    else
    {
      closestPoint = point;
      return false;
    }
  }
  double currentRadius = radiusA + (radiusB-radiusA) * modulationValue;
  MPoint closestPointOnCurve = capsuleStart + ( direction ) * uParam;

  if (point.distanceTo(closestPointOnCurve) < currentRadius)
  {
    MVector directionVec(point-closestPointOnCurve);
    directionVec.normalize();
    closestPoint = closestPointOnCurve + directionVec * currentRadius;
    return true;
  }
  else
  {
    closestPoint = point;
    return false;
  }

}


bool projectPointOnElipsoidCapsule(MPoint point, MPoint &closestPoint, MPoint capsuleStart, MPoint capsuleEnd, unsigned int i,
                                   double radiusA, double radiusB, double radiusC, double radiusD, MMatrix capsuleMatrix, unsigned int currentIdx)
{
  double uParam = getLengthOfPointProjectedToLine(point, capsuleStart, capsuleEnd);
  MVector direction = capsuleEnd - capsuleStart;
  double modulationValue = uParam;
  if (modulationValue>1.0)
  {
    projectPointOnEllipsoid(point, closestPoint, capsuleEnd, capsuleStart, currentIdx, radiusB, radiusB, radiusD, capsuleMatrix);
    return true;
  }
  if (modulationValue < 0.0)
  {
    projectPointOnEllipsoid(point, closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusA, radiusC, capsuleMatrix);
    return true;
  }
  double currentRadius = radiusA + (radiusB-radiusA) * modulationValue;
  MPoint closestPointOnCurve = capsuleStart + ( direction ) * uParam;
  MVector directionVec(point-closestPointOnCurve);
  directionVec.normalize();
  closestPoint = closestPointOnCurve + directionVec * currentRadius;
}




void LHCollisionDeformer::capsuleElipsoidLogic(MPoint &closestPoint, MPointArray &allPoints, unsigned int currentIdx,
                                            double &maxDisp, MIntArray &hitPoints, bool &capsuleHit, MPoint capsuleStart,
                                            MPoint capsuleEnd, double radiusA, double radiusB, double radiusC, double radiusD, MMatrix capsuleMatrix)
{
    // projectPointOnElipsoidCapsule(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB, radiusC, radiusD, capsuleMatrix, currentIdx);
    // allPoints[currentIdx] = closestPoint;

  if (getClosestPointOnEllipsoidCapsule(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB, radiusC, radiusD, capsuleMatrix, currentIdx))
  {
    getMaxDisplacement(allPoints[currentIdx], closestPoint, dispCheck, maxDisp);
    allPoints[currentIdx] = closestPoint;
    hitPoints.append(1);
    capsuleHit = true;
  }
  else
  {
    hitPoints.append(0);
  }
}

void LHCollisionDeformer::capsuleEllipsoidBulgeLogic(MPointArray &allPoints, unsigned int currentIdx, MPoint capsuleStart,
                                                     MPoint capsuleEnd, double radiusA, double radiusB, double radiusC, double radiusD, MMatrix capsuleMatrix,
                                                     MFnMesh *newMainMesh, double bulgeDistance, double bulgeAmount, MRampAttribute rFalloffRamp, double bulgeWeight)
{
  projectPointOnElipsoidCapsule(allPoints[currentIdx], closestPoint, capsuleStart, capsuleEnd, currentIdx, radiusA, radiusB, radiusC, radiusD, capsuleMatrix, currentIdx);
  distanceToCenter = allPoints[currentIdx].distanceTo(closestPoint);
  if (distanceToCenter < bulgeDistance)
  {
    newMainMesh->getVertexNormal(currentIdx, vRay);
    vRay.normalize();
    allPoints[currentIdx] = LHCollisionDeformer::getCapsuleBulge(allPoints[currentIdx], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp, bulgeWeight);
  }
}
//AMD's implementation of clamp (from wikipedia)
double clamp(double value, double lowerlimit, double upperlimit) {
  if (value < lowerlimit)
    value = lowerlimit;
  if (value > upperlimit)
    value = upperlimit;
  return value;
}
//AMD's implementation of smoothstep (from wikipedia)
double smoothstep(double low, double high, double value) {
  // Scale, bias and saturate x to 0..1 range
  value = clamp((value - low) / (high - low), 0.0, 1.0); 
  // Evaluate polynomial
  return value * value * (3 - 2 * value);
}

void LHCollisionDeformer::capsuleDeformation(unsigned int capsuleIdx, MPointArray &allPoints, MFnMesh *newMainMesh, double bulgeAmount, double bulgeDistance,
                                                 MRampAttribute rFalloffRamp, MMatrix bBMatrix)
{

    MIntArray hitArray;
    maxDisp = 0.0;
    capsuleHit = false;

    MDoubleArray collisionWeightsArray = safelyGetArrayWeights(capsuleData.colWeights, capsuleIdx, currentMIndex, allPoints.length());
    MDoubleArray bulgeWeightsArray = safelyGetArrayWeights(capsuleData.bulgeWeights, capsuleIdx, currentMIndex, allPoints.length());

    MPoint capsuleStart = capsuleData.pPointAArray[capsuleIdx];
    MPoint capsuleEnd = capsuleData.pPointBArray[capsuleIdx];
    MMatrix capsuleMatrix = capsuleData.mWorldMatrixArray[capsuleIdx];
    double capsuleLengthA = capsuleData.dLengthAArray[capsuleIdx];
    double capsuleLengthB = capsuleData.dLengthBArray[capsuleIdx];


    capsuleStart = capsuleStart + (capsuleStart - capsuleEnd) * capsuleLengthA;
    capsuleEnd = capsuleEnd + (capsuleEnd - capsuleStart) * capsuleLengthB;

    MPoint capsuleFromToVec = capsuleEnd -capsuleStart;
    double distanceBetweenPoints = capsuleStart.distanceTo(capsuleEnd);

    // The ellipsoid will do its own scaling, it doesn't need world scale
    double capsuleRadiusA = capsuleData.dRadiusAArray[capsuleIdx];
    double capsuleRadiusB = capsuleData.dRadiusBArray[capsuleIdx];
    double capsuleRadiusC = capsuleData.dRadiusCArray[capsuleIdx];
    double capsuleRadiusD = capsuleData.dRadiusDArray[capsuleIdx];

    // per prim bulge 

    double pBulgeAmount = capsuleData.dBulgeAmount[capsuleIdx];
    double pBulgeDistance = capsuleData.dBulgeDistance[capsuleIdx];
    LHCollisionDeformer::bulgeClampStart = capsuleData.dBulgeClampStart[capsuleIdx];
    LHCollisionDeformer::bulgeClampEnd = capsuleData.dBulgeClampEnd[capsuleIdx];

    // Thinking about adding global scaling ....
    double scaleMatrixArray[3];
    MTransformationMatrix capsuleScalarMatrix(capsuleMatrix);
    capsuleScalarMatrix.getScale(scaleMatrixArray, MSpace::kWorld);
    double averageScale = (scaleMatrixArray[0] + scaleMatrixArray[1] + scaleMatrixArray[2])/3;

    if (capsuleData.eTypeArray[x] != 2)
    {
      capsuleRadiusA = capsuleRadiusA * averageScale;
      capsuleRadiusB = capsuleRadiusB * averageScale;
      capsuleRadiusC = capsuleRadiusC * averageScale;
      capsuleRadiusD = capsuleRadiusD * averageScale;
    }

    MVectorArray boundsData;
    MPoint startUpVector;
    MPoint endUpVector;
    MPoint capsuleCenter;
    // MPointArray framePoints = getCapsuleFrame(capsuleMatrix, boundsData, startUpVector, endUpVector, capsuleStart, capsuleEnd, capsuleCenter);
    MVector planarNormal(capsuleFromToVec);
    MVector planarUpVector(startUpVector);

    bool logicCheck;
    // Closest point
    for (i = 0; i < allPoints.length(); i++)
    {
      if (collisionWeightsArray[i] <= 0.0)
        continue;
      switch( capsuleData.eTypeArray[x] )
      {
          case 0 : // sphere
              LHCollisionDeformer::sphereClosestPointLogic(offsetPoint, allPoints, i, capsuleStart, capsuleRadiusA, newMainMesh, hitArray, capsuleHit, collisionWeightsArray[i]);
              break;
          case 1 : // elipsoidCapsule
              capsuleElipsoidLogic(offsetPoint, allPoints, i, maxDisp, hitArray, capsuleHit, capsuleStart, capsuleEnd, capsuleRadiusA, capsuleRadiusB, capsuleRadiusC, capsuleRadiusD, capsuleMatrix);
              break;
          case 2 : // elipsoid
              ellipsoidPointLogic(offsetPoint, allPoints, i, maxDisp, hitArray, capsuleHit, capsuleStart, capsuleEnd, capsuleRadiusA, capsuleRadiusB, capsuleRadiusC, capsuleMatrix);
              break;
          case 3 : // cylinder
              cylinderPointLogic(offsetPoint, allPoints, i, maxDisp, hitArray, capsuleHit, capsuleStart, capsuleEnd, capsuleRadiusA, capsuleRadiusB);
              break;
          case 4 : // plane
              planePointLogic(offsetPoint, allPoints, i, maxDisp, hitArray, capsuleHit, capsuleStart, capsuleEnd);
              break;
          case 5 : // capsule
              capsulePointLogic(offsetPoint, allPoints, i, maxDisp, hitArray, capsuleHit, capsuleStart, capsuleEnd, capsuleRadiusA, capsuleRadiusB);
              break;
          case 6 : // cone
              cylinderPointLogic(offsetPoint, allPoints, i, maxDisp, hitArray, capsuleHit, capsuleStart, capsuleEnd, capsuleRadiusA, 0.01);
              break;
      }
    }
    // Bulge
    if (LHCollisionDeformer::bulgeClampStart != 0.0 || LHCollisionDeformer::bulgeClampEnd != 0.0)
    {
      if (maxDisp < LHCollisionDeformer::bulgeClampStart)
        maxDisp = 0.0;
      else if (maxDisp - LHCollisionDeformer::bulgeClampStart > LHCollisionDeformer::bulgeClampEnd)
        maxDisp = LHCollisionDeformer::bulgeClampEnd;
      else
        maxDisp = maxDisp - LHCollisionDeformer::bulgeClampStart;
      maxDisp = smoothstep(LHCollisionDeformer::bulgeClampStart, LHCollisionDeformer::bulgeClampEnd, maxDisp);

    }

    if (capsuleHit)
    {

      for (i = 0; i < allPoints.length(); i++)
      {
        if (!hitArray[i])
        {
          if (bulgeWeightsArray[i] <= 0.0)
            continue;
          
          switch( capsuleData.eTypeArray[x] )
          {
              case 0 : // sphere
                  LHCollisionDeformer::sphereBulgeLogic(allPoints, i, capsuleStart, capsuleRadiusA, newMainMesh, pBulgeDistance, pBulgeAmount, rFalloffRamp, bulgeWeightsArray[i]);
                  break;
              case 1 : // elipsoidCapsule
                  capsuleEllipsoidBulgeLogic(allPoints, i, capsuleStart, capsuleEnd, capsuleRadiusA, capsuleRadiusB, capsuleRadiusC, capsuleRadiusD, capsuleMatrix, newMainMesh, pBulgeDistance, pBulgeAmount, rFalloffRamp, bulgeWeightsArray[i]);
                  break;
              case 2 : // elipsoid
                  ellipsoidBulgeLogic(allPoints, i, capsuleStart, capsuleEnd, capsuleRadiusA, capsuleRadiusB, capsuleRadiusC, capsuleMatrix, newMainMesh, pBulgeDistance, pBulgeAmount, rFalloffRamp, bulgeWeightsArray[i]);
                  break;
              case 3 : // cylinder
                  cylinderBulgeLogic(allPoints, i, capsuleStart, capsuleEnd, capsuleRadiusA, capsuleRadiusB, newMainMesh, pBulgeDistance, pBulgeAmount, rFalloffRamp, bulgeWeightsArray[i]);
                  break;
              case 4 : // plane
                  planeBulgeLogic(allPoints, i, capsuleStart, capsuleEnd, newMainMesh, pBulgeDistance, pBulgeAmount, rFalloffRamp, bulgeWeightsArray[i]);
                  break;
              case 5 : // capsule
                  capsuleBulgeLogic(allPoints, i, capsuleStart, capsuleEnd, capsuleRadiusA, capsuleRadiusB, newMainMesh, pBulgeDistance, pBulgeAmount, rFalloffRamp, bulgeWeightsArray[i]);
                  break;
              case 6 : // cone
                  cylinderBulgeLogic(allPoints, i, capsuleStart, capsuleEnd, capsuleRadiusA, 0.01, newMainMesh, pBulgeDistance, pBulgeAmount, rFalloffRamp, bulgeWeightsArray[i]);
                  break;
          }
        }
      }
    }
  }

double getLineMagnitude(MPoint from, MPoint to)
{
  //This is getting the distance, it is written out here just as a mathmatical exercise, it will be replaced with a simple call to the length() function
  MPoint magnitude = to - from;
  return ( double )sqrt(magnitude.x * magnitude.x + magnitude.y * magnitude.y + magnitude.z * magnitude.z);
}

MPoint LHCollisionDeformer::getCapsuleBulge(MPoint currPoint, MPoint closestPoint, double bulgeAmount,
                                     double bulgeDistance, MVector vRay, double maxDisp, MRampAttribute rFalloffRamp, double bulgeWeight)
{
  // get distance vector in regular world matrix
  testDist = closestPoint.distanceTo(currPoint);
  relativeDistance = (testDist / bulgeDistance) ;
  rFalloffRamp.getValueAtPosition((float)relativeDistance, value);

  // Clamp Max displacement
  // maxDisp = low2 + (maxDisp - low1) * (high2 - low2) / (high1 - low1)

  return currPoint + vRay * bulgeAmount * relativeDistance * maxDisp * value * bulgeWeight;
}


void LHCollisionDeformer::sphereBulgeLogic(MPointArray &allPoints, unsigned int currentIdx,  MPoint capsuleStart, double capsuleRadiusA, MFnMesh *newMainMesh, double bulgeDistance,
                                             double bulgeAmount, MRampAttribute rFalloffRamp, double bulgeWeight)
{
  distanceToCenter = allPoints[currentIdx].distanceTo(capsuleStart);
  if (distanceToCenter < capsuleRadiusA + bulgeDistance)
  {
    closestPoint = LHCollisionDeformer::getClosestPointOnSphereImplicit(allPoints[currentIdx], capsuleStart, capsuleRadiusA);
    newMainMesh->getVertexNormal(currentIdx, vRay);
    vRay.normalize();
    allPoints[currentIdx] = LHCollisionDeformer::getCapsuleBulge(allPoints[currentIdx], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp, bulgeWeight);
  }
}


void LHCollisionDeformer::sphereClosestPointLogic(MPoint &offsetPoint, MPointArray &allPoints, unsigned int currentIdx, MPoint capsuleStart,
                                                  double capsuleRadiusA, MFnMesh *newMainMesh, MIntArray &hitArray, bool &capsuleHit, double collisionWeight)
{
      distanceToCenter = allPoints[currentIdx].distanceTo(capsuleStart);
      if (distanceToCenter < capsuleRadiusA)
      {
        capsuleHit = true;
        hitArray.append(1);
        offsetPoint = LHCollisionDeformer::getClosestPointOnSphereImplicit(allPoints[currentIdx], capsuleStart, capsuleRadiusA);
        getMaxDisplacement(offsetPoint, allPoints[currentIdx], dispCheck, maxDisp);
        if (!iPermanent && eAlgorithm > 0)
        {
          offsetPoint = LHCollisionDeformer::transformPointByClosestPointDistance(offsetPoint, allPoints[currentIdx], currentIdx, newMainMesh, dispCheck);
        }
        allPoints[i] = allPoints[i] + (offsetPoint - allPoints[i]) * collisionWeight;
      }
      else
      {
        hitArray.append(0);
      }
}

MPoint LHCollisionDeformer::getClosestPointOnSphereImplicit(MPoint testPoint, MPoint capsuleStart, double radius){
        capsuleSurfaceDirection = testPoint - capsuleStart;
        capsuleSurfaceDirection.normalize();
        convertMVectorToMPoint(capsuleSurfaceDirection, capsulePoint);
        return capsuleStart + (capsulePoint * radius);
}

MPoint LHCollisionDeformer::transformPointByClosestPointDistance(MPoint closestPoint, MPoint currentPoint,unsigned int currentPointIndex, MFnMesh *newMainMesh, double distance)
{
    newMainMesh->getVertexNormal(currentPointIndex, vRay);
    vRay.normalize();
    convertMVectorToMPoint(vRay, capsulePoint);
    return currentPoint + capsulePoint * -distance;
}

void LHCollisionDeformer::perPolyDeformation(MPointArray &allPoints, MMatrixArray colMatrices, MObjectArray oColMeshArray, MFnMesh *fnMainMesh,
                                             double bulgeDistance, double bulgeAmount, MRampAttribute rInnerFalloffRamp,
                                             MRampAttribute rFalloffRamp, MRampAttribute rBlendBulgeCollisionRamp, MItGeometry itGeo, MMatrix bBMatrix)
{

  ///////////////////////////////// MESH PER POINT IMPLEMENTATION //////////////////////////////////////////////////////////
  MPoint initPoint(0.0, 0.0, 0.0);

  for (x=0;x < inputCount; x++){
    MVectorArray vertexNormalArray;
    maxDisp =0.0;
    isInBBox = false;
    MIntArray hitArray;
    MIntArray flipRayArray;
    MPointArray flipPointArray;
	  colMatrix = colMatrices[x];
    MFnMesh* fnColMesh = new MFnMesh(oColMeshArray[x]);
	  fnColMesh->getPoints(allColPoints);
    MBoundingBox colBounds;
	  for (i=0;i < allColPoints.length(); i++){
      colBounds.expand(allColPoints[i]);
		  allColPoints[i] = allColPoints[i] * colMatrix;
	  }
    colBounds.transformUsing(colMatrix);
	  fnColMesh->setPoints(allColPoints);

	  MMeshIsectAccelParams mmAccelParams = fnColMesh->autoUniformGridParams();
	  for (i=0;i < numPoints; i++){
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
        bulgeWeight = SafelyGetWeights(bulgeWeightsArray, currentMIndex, i);
        if (collisionWeight <= 0.0){
          hitArray.append(0);
          flipRayArray.append(0);
          flipPointArray.append(initPoint);
          fnMainMesh->getVertexNormal(i, vRay);
          vertexNormalArray.append(vRay);
          continue;
        }
        fnMainMesh->getVertexNormal(i, vRay);
        vertexNormalArray.append(vRay);
        //Check if the point is within the bounding box
        MPoint bbMin = colBounds.min();
        MPoint bbMax = colBounds.max();
        LHCollisionDeformer::getIntersectionData(allPoints[i], bbMin, bbMax, fnColMesh, mmAccelParams, initPoint, hitArray, flipRayArray, flipPointArray);
    }

  // Can Mostly be Run in Parallel
    if (isInBBox){
      fnMeshIntersector.create(oColMeshArray[x]);
      if (eAlgorithm == 2){
      LHCollisionDeformer::BlendBulgeAndCollisionSerial(oColMeshArray, x, numPoints, hitArray,  flipRayArray, allPoints, vertexNormalArray, currentMIndex, bulgeDistance,
                                                     rInnerFalloffRamp, bulgeAmount, flipPointArray, rFalloffRamp, rBlendBulgeCollisionRamp, currentMIndex);
      }
      else{
      LHCollisionDeformer::seperateBulgeAndCollisionSerial(oColMeshArray, x, numPoints, hitArray,  flipRayArray, allPoints, vertexNormalArray, maxDisp, bulgeDistance,
                                                     rInnerFalloffRamp, bulgeAmount, flipPointArray, rFalloffRamp, eAlgorithm, currentMIndex);
      }
    }
  }
}







MPoint LHCollisionDeformer::getBulgeCapsuleScaled(MPoint currPoint, MPoint closestPoint, double bulgeAmount,
                                     double bulgeDistance, MVector vRay, double maxDisp, MRampAttribute rFalloffRamp, double bulgeWeight, MMatrix mCapsuleMatrix)
{
  // get distance vector in regular world matrix
  skewedDistance = closestPoint - currPoint;
  skewedDistance = skewedDistance * mCapsuleMatrix;
  relativeDistance = (skewedDistance.length() / bulgeDistance) ;
  rFalloffRamp.getValueAtPosition((float)relativeDistance, value);
  return currPoint + vRay * bulgeAmount * relativeDistance * maxDisp * value * bulgeWeight;
}


MPoint LHCollisionDeformer::transformPointByClosestPointDistanceScaled(MPoint closestPoint, MPoint currentPoint,unsigned int currentPointIndex, MFnMesh *newMainMesh, MMatrix mCapsuleMatrix, double distance)
{
    newMainMesh->getVertexNormal(currentPointIndex, vRay);
    vRay = vRay * mCapsuleMatrix.inverse();
    vRay.normalize();
    convertMVectorToMPoint(vRay, capsulePoint);
    return currentPoint + capsulePoint * -distance;
}





MPoint LHCollisionDeformer::getBulge(MPoint currPoint, MPoint closestPoint, double bulgeAmount,
                                     double bulgeDistance, MVector vRay, double maxDisp, MRampAttribute rFalloffRamp, double bulgeWeight)
{
  distance = currPoint.distanceTo(closestPoint);
  relativeDistance = distance / bulgeDistance;
  rFalloffRamp.getValueAtPosition((float)relativeDistance, value);
  return currPoint + vRay * bulgeAmount * relativeDistance * maxDisp * value * bulgeWeight;
}







void LHCollisionDeformer::BlendBulgeAndCollisionSerial(MObjectArray oColMeshArray, unsigned int colMeshIndex, unsigned int numPoints, MIntArray hitArray, MIntArray flipRayArray,
                                                       MPointArray &allPoints, MVectorArray vertexNormalArray, double maxDisp, double bulgeDistance, MRampAttribute rInnerFalloffRamp, double bulgeAmount,
                                                       MPointArray flipPointArray, MRampAttribute rFalloffRamp, MRampAttribute rBlendBulgeCollisionRamp, unsigned int mIndex)
{
  if (iMultiThread == 0)
  {
    for (i = 0; i < numPoints; i++)
    {
      collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
      if (hitArray[i] && collisionWeight)
      {
        collisionPoint = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i, bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
        blendPoint = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
        distance = blendPoint.distanceTo(collisionPoint);
        relativeDistance = distance / bulgeDistance;
        rBlendBulgeCollisionRamp.getValueAtPosition((float)relativeDistance, value);
        collisionWeightPoint = blendPoint + (collisionPoint - blendPoint) * value;
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
        allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
      }
    }
  }
  MPointArray tempPoints = allPoints;
  if (iMultiThread == 1)
  {
    for (i = 0; i < numPoints; i++)
    {
      collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
      if (hitArray[i] && collisionWeight)
      {
        collisionPoint = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i, bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
        blendPoint = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
        distance = blendPoint.distanceTo(collisionPoint);
        relativeDistance = distance / bulgeDistance;
        rBlendBulgeCollisionRamp.getValueAtPosition((float)relativeDistance, value);
        collisionWeightPoint = blendPoint + (collisionPoint - blendPoint) * value;
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
        allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
      }
    }
  }

  if (iMultiThread == 2)
  {

      MTimer timer;
      timer.beginTimer();

      for (i = 0; i < numPoints; i++)
      {
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
        if (hitArray[i] && collisionWeight)
        {
          collisionPoint = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i, bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
          blendPoint = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
          distance = blendPoint.distanceTo(collisionPoint);
          relativeDistance = distance / bulgeDistance;
          rBlendBulgeCollisionRamp.getValueAtPosition((float)relativeDistance, value);
          collisionWeightPoint = blendPoint + (collisionPoint - blendPoint) * value;
          collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
          allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
        }
      }

      timer.endTimer();
      double serialTime = timer.elapsedTime();
      timer.beginTimer();

    for (i = 0; i < numPoints; i++)
    {
      collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
      if (hitArray[i] && collisionWeight)
      {
        collisionPoint = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i, bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
        blendPoint = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
        distance = blendPoint.distanceTo(collisionPoint);
        relativeDistance = distance / bulgeDistance;
        rBlendBulgeCollisionRamp.getValueAtPosition((float)relativeDistance, value);
        collisionWeightPoint = blendPoint + (collisionPoint - blendPoint) * value;
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
        allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
      }
    }

      timer.endTimer();
      double parallelTime = timer.elapsedTime();
      double ratio = serialTime / parallelTime;
      MString str = MString("\nElapsed time for serial computation: ") + serialTime + MString("s\n");
      str += MString("Elapsed time for parallel computation: ") + parallelTime + MString("s\n");
      str += MString("Speedup: ") + ratio + MString("x\n");
      MGlobal::displayInfo(str);

  }
  for (i = 0; i < numPoints; i++)
  {
    bulgeWeight = SafelyGetWeights(bulgeWeightsArray, currentMIndex, i);
    if (!hitArray[i] && bulgeWeight)
    {
      allPoints[i] = LHCollisionDeformer::PerformBulgeSerial(vertexNormalArray, i, allPoints, bulgeAmount, bulgeDistance, maxDisp, rFalloffRamp);
    }
  }
}

void LHCollisionDeformer::seperateBulgeAndCollisionSerial(MObjectArray oColMeshArray, unsigned int colMeshIndex, unsigned int numPoints, MIntArray hitArray, MIntArray flipRayArray,
                                                          MPointArray &allPoints, MVectorArray vertexNormalArray, double maxDisp, double bulgeDistance, MRampAttribute rInnerFalloffRamp, double bulgeAmount,
                                                          MPointArray flipPointArray, MRampAttribute rFalloffRamp, short algorithm, unsigned int mIndex)
{
  for (i = 0; i < numPoints; i++)
  {
    collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
    if (hitArray[i] && collisionWeight)
    {
      if (flipRayArray[i] && algorithm > 0)
      {
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);

        collisionWeightPoint = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i, bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
        allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
      }
      else
      {
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentMIndex, i);
        collisionWeightPoint = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
        allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
      }
    }
  }
  for (i = 0; i < numPoints; i++)
  {
    bulgeWeight = SafelyGetWeights(bulgeWeightsArray, currentMIndex, i);
    if (!hitArray[i] && bulgeWeight)
    {
      allPoints[i] = LHCollisionDeformer::PerformBulgeSerial(vertexNormalArray, i, allPoints, bulgeAmount, bulgeDistance, maxDisp, rFalloffRamp);
    }
  }
}

MPoint LHCollisionDeformer::CollisionFlipCheckSerial(MPointArray allPoints, unsigned int pointIdx, double bulgeDistance, double bulgeAmount, MVectorArray vertexNormalArray,
                                                     double &maxDisp, MPointArray flipPointArray, MRampAttribute rInnerFalloffRamp)
{
  fnMeshIntersector.getClosestPoint(allPoints[pointIdx], closestPointOn);
  closestPoint = closestPointOn.getPoint();
  closestNormal = closestPointOn.getNormal();
  vRay = vertexNormalArray[pointIdx];
  flipCheck = closestNormal * vRay;
  testDist = closestPoint.distanceTo(allPoints[pointIdx]);
  if (testDist > maxDisp)
  {
    maxDisp = testDist;
  }
  distance = allPoints[i].distanceTo(closestPoint);
  relativeDistance = distance / bulgeDistance;
  rInnerFalloffRamp.getValueAtPosition((float)relativeDistance, value);

  interPoint = closestPoint + (((closestPoint - flipPointArray[pointIdx]) * (value - 1.1F)));
  return interPoint;
}

MPoint LHCollisionDeformer::CollisionCheapSerial(MPointArray allPoints, unsigned int pointIdx, double &maxDisp)
{
  fnMeshIntersector.getClosestPoint(allPoints[pointIdx], closestPointOn);
  closestPoint = closestPointOn.getPoint();
  testDist = closestPoint.distanceTo(allPoints[pointIdx]);
  if (testDist > maxDisp)
  {
    maxDisp = testDist;
  }
  return closestPoint;
}

MPoint LHCollisionDeformer::PerformBulgeSerial(MVectorArray vertexNormalArray, unsigned int pointIdx, MPointArray allPoints, double bulgeAmount, double bulgeDistance, double maxDisp,
                                               MRampAttribute rFalloffRamp)
{
  vRay = vertexNormalArray[pointIdx];
  fnMeshIntersector.getClosestPoint(allPoints[pointIdx], closestPointOn);
  closestPoint = closestPointOn.getPoint();
  bulgeWeight = SafelyGetWeights(bulgeWeightsArray, currentMIndex, pointIdx);
  //=========================
  // Need to check whether this can be called from a parallel function, or if a threaded version will need to be written
  return LHCollisionDeformer::getBulge(allPoints[pointIdx], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp, bulgeWeight);
  //=========================
}


MStatus LHCollisionDeformer::getIntersectionData(MPoint &currPnt, MPoint bbMin, MPoint bbMax, MFnMesh *fnColMesh, MMeshIsectAccelParams &mmAccelParams, MPoint initPoint,
                                                MIntArray &hitArray, MIntArray &flipRayArray, MPointArray &flipPointArray)
{
  
  // If inside bounds run more expensive calculations
  if (currPnt.x > bbMin.x &&
      currPnt.y > bbMin.y &&
      currPnt.z > bbMin.z &&
      currPnt.x < bbMax.x &&
      currPnt.y < bbMax.y &&
      currPnt.z < bbMax.z)
  {
    //Use vertex normal vector to create a ray for casting
    MFloatPointArray hitPoints;

    hit = fnColMesh->allIntersections(currPnt, vRay, NULL, NULL, false, MSpace::kObject, 9999999.0,
                                     false, &mmAccelParams, true, hitPoints, NULL, &hitFaceIdArray, NULL, NULL, NULL);

    numHits = hitPoints.length();
    // If no hit, or the hit is divisible by 2 skip it, we are outside the mesh (Hormann & Agathos, 2001)
    if (!hit || numHits % 2 == 0)
    {
      hitArray.append(0);
      flipRayArray.append(0);
      flipPointArray.append(initPoint);
      return MS::kSuccess;
    }

    //========================================================================================================================================
    //========================================================================================================================================
    //This is a slower but more accurate cleanup pass of the algorithm to avoid swimming points and points flipping to the inside of the mesh.
    // Need to be sure there is actually a face in the opposite direction, if not there is no point to flipping

    if (eAlgorithm > 0)
    {
      fnColMesh->getPolygonNormal(hitFaceIdArray[0], polyNormal);
      flipCheck = polyNormal * vRay;
      if (flipCheck > 0)
      {
        vRay = vRay * -1.0;
        MFloatPointArray hitPointsFlipped;
        hit = fnColMesh->allIntersections(currPnt, vRay, NULL, NULL, false, MSpace::kObject, 9999999.0,
                                         false, &mmAccelParams, true, hitPointsFlipped, NULL, NULL, NULL, NULL, NULL);
        if (hit)
        {
          flipRayArray.append(1);
          flipPointArray.append(hitPointsFlipped[0]);
        }
        else
        {
          flipRayArray.append(0);
          flipPointArray.append(hitPoints[0]);
        }
      }
      else
      {
        flipRayArray.append(0);
        flipPointArray.append(hitPoints[0]);
      }
    }
    else
    {
      flipRayArray.append(0);
      flipPointArray.append(hitPoints[0]);
    }
    hitArray.append(1);
    isInBBox = true;
    return MS::kSuccess;
  }
  else
  {
    hitArray.append(0);
    flipRayArray.append(0);
    flipPointArray.append(initPoint);
    return MS::kSuccess;
  }
  return MS::kSuccess;
}

// void LHCollisionDeformer::sphereCapsuleCollision(unsigned int capsuleIdx, MPointArray &allPoints, MFnMesh *newMainMesh, double bulgeAmount, double bulgeDistance,
//                                                  MRampAttribute rFalloffRamp)
// {

//     MIntArray hitArray;
//     maxDisp = 0.0;
//     capsuleHit = false;
//     MDoubleArray collisionWeightsArray = capsuleData.colWeights[capsuleIdx][currentMIndex];
//     MDoubleArray bulgeWeightsArray = capsuleData.bulgeWeights[capsuleIdx][currentMIndex];
//     MPoint capsuleStart = capsuleData.pPointAArray[capsuleIdx];
//     double capsuleRadius = capsuleData.dRadiusAArray[capsuleIdx];
//     // Closest point
//     for (i = 0; i < allPoints.length(); i++)
//     {
//       if (collisionWeightsArray[i] <= 0.0)
//         continue;
//       distanceToCenter = allPoints[i].distanceTo(capsuleStart);
//       if (distanceToCenter < capsuleRadius)
//       {
//         capsuleHit = true;
//         hitArray.append(1);
//         offsetPoint = LHCollisionDeformer::getClosestPointOnSphereImplicit(allPoints[i], capsuleStart, capsuleRadius);
//         getMaxDisplacement(offsetPoint, allPoints[i], dispCheck, maxDisp);
//         if (!iPermanent && eAlgorithm > 0)
//         {
//           offsetPoint = LHCollisionDeformer::transformPointByClosestPointDistance(offsetPoint, allPoints[i], i, newMainMesh, dispCheck);
//         }
//         allPoints[i] = allPoints[i] + (offsetPoint - allPoints[i]) * collisionWeightsArray[i];
//       }
//       else
//       {
//         hitArray.append(0);
//       }
//     }
//     // Bulge

//     if (capsuleHit)
//     {

//       for (i = 0; i < allPoints.length(); i++)
//       {
//         if (!hitArray[i])
//         {
//           if (bulgeWeightsArray[i] <= 0.0)
//             continue;
//           distanceToCenter = allPoints[i].distanceTo(capsuleStart);
//           if (distanceToCenter < capsuleRadius + bulgeDistance)
//           {
//             closestPoint = LHCollisionDeformer::getClosestPointOnSphereImplicit(allPoints[i], capsuleStart, capsuleRadius);
//             bulgeWeight = bulgeWeightsArray[i];
//             newMainMesh->getVertexNormal(i, vRay);
//             vRay.normalize();
//             allPoints[i] = LHCollisionDeformer::getCapsuleBulge(allPoints[i], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp, bulgeWeight);
//           }
//         }
//       }
//     }
// }
