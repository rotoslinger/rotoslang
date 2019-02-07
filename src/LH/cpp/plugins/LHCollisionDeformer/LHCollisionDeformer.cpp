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


MStatus LHCollisionDeformer::initialize() {
  MFnNumericAttribute nAttr;
  MFnGenericAttribute gAttr;
  MFnCompoundAttribute cAttr;
  MFnMatrixAttribute mAttr;
  MRampAttribute rAttr;
  MFnTypedAttribute tAttr;
  MFnEnumAttribute eAttr;


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
postConstructor_initialise_ramp_curve( thisMObj, aBlendBulgeCollisionRamp, 0, 0.0f, 1.0f, 2 );
postConstructor_initialise_ramp_curve( thisMObj, aBlendBulgeCollisionRamp, 1, 1.0f, 0.0f, 2 );
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

void* LHCollisionDeformer::creator() { return new LHCollisionDeformer; }

MStatus LHCollisionDeformer::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;
  MObject thisMObj( thisMObject() );

  currentIndex = mIndex;
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
  short eAlgorithm = data.inputValue(aAlgorithm).asShort();
  int cacheWeights = data.inputValue( aCacheWeights ).asInt();
  int iPermanent = data.inputValue( LHCollisionDeformer::aPermanent ).asInt();
  int iMultiThread = data.inputValue( LHCollisionDeformer::aMultiThread ).asInt();
  int iNumTasks = data.inputValue( LHCollisionDeformer::aNumTasks ).asInt();

  // Get weights
	if((!bulgeWeightsArray.size() ||  bulgeWeightsArray.size() < numIndex) or !cacheWeights){
  status = LHCollisionDeformer::RetrieveWeightsForAllIndicies(aWeightsParent, aBulgeWeights, numIndex, bulgeWeightsArray, inPlug, data);
  CheckStatusReturn( status, "Unable to get bulge Weights" );
  }

	if((!collisionWeightsArray.size() || collisionWeightsArray.size() < numIndex) or !cacheWeights){
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

  // MMatrix bBMatrix = data.inputValue( LHCollisionDeformer::aMainWorldMatrix ).asMatrix();

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
  MFnMesh fnMainMesh(oMainMesh);
  MPoint tmptstPoint;
  fnMainMesh.getPoint(0,tmptstPoint);








  fnMainMesh.getPoints(countTest);

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
  if (iPermanent){
      allPoints = allPointsArray[mIndex];
      //============================= multi thread=================================================
      //May not speed up much, may even make slower, but should at least try to multiThread

      // if (iMultiThread == 0)
      // {
      //   for (i = 0; i < numPoints; i++)
      //   {
      //     allPoints[i] = allPoints[i] * bBMatrix;
      //   }
      // }

      if (iMultiThread == 1)
      {
        countTest = MainParallelDeformationCalc(bBMatrix, countTest, iNumTasks);
      }

      if (iMultiThread == 2)
      {
        MTimer timer;
        timer.beginTimer();
        for (i = 0; i < numPoints; i++)
        {
          countTest[i] = countTest[i] * bBMatrix;
        }
        timer.endTimer();
        double serialTime = timer.elapsedTime();

        timer.beginTimer();
        countTest = MainParallelDeformationCalc(bBMatrix, countTest, iNumTasks);
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
          allPoints[i] = allPoints[i] * bBMatrix;
        }


  }

  //============================= multi thread=================================================
  else{
      fnMainMesh.getPoints(allPoints);
      allPointsArray[mIndex] = allPoints;
  }

  numPoints = allPoints.length();


  MPoint initPoint(0.0, 0.0, 0.0);
  for (x=0;x < inputCount; x++){
    MVectorArray vertexNormalArray;
    maxDisp =0.0;
    isInBBox = false;
    MIntArray hitArray;
    MIntArray flipRayArray;
    MPointArray flipPointArray;
    MIntArray hitFaceIdArray;


	  colMatrix = colMatrices[x];
	  MFnMesh fnColMesh(oColMeshArray[x]);
	  fnColMesh.getPoints(allColPoints);
    //=========================
    // Needs to be multiThreaded!!
    MBoundingBox colBounds;
	  for (i=0;i < allColPoints.length(); i++){
      colBounds.expand(allColPoints[i]);
		  allColPoints[i] = allColPoints[i] * colMatrix;
	  }
    colBounds.transformUsing(colMatrix);
    //=========================
	  fnColMesh.setPoints(allColPoints);

	  MMeshIsectAccelParams mmAccelParams = fnColMesh.autoUniformGridParams();
	  for (i=0;i < numPoints; i++){
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentIndex, i);
        bulgeWeight = SafelyGetWeights(bulgeWeightsArray, currentIndex, i);
        if (collisionWeight <= 0.0){
          hitArray.append(0);
          flipRayArray.append(0);
          flipPointArray.append(initPoint);
          fnMainMesh.getVertexNormal(i, vRay);
          vertexNormalArray.append(vRay);
          continue;
        }
        fnMainMesh.getVertexNormal(i, vRay);
        vertexNormalArray.append(vRay);
        //Check if the point is within the bounding box
        MPoint bbMin = colBounds.min();
        MPoint bbMax = colBounds.max();
        //OLD WAY LESS EXPENSIVE, BUT INACURATE FOR SOME REASON
        // MPoint bbMin = colBBArray[x].min();
        // MPoint bbMax = colBBArray[x].max();

        // If inside bounds run more expensive calculations
        if (allPoints[i].x > bbMin.x &&
          allPoints[i].y > bbMin.y &&
          allPoints[i].z > bbMin.z &&
          allPoints[i].x < bbMax.x &&
          allPoints[i].y < bbMax.y &&
          allPoints[i].z < bbMax.z){
            //Use vertex normal vector to create a ray for casting
            MFloatPointArray hitPoints;

            hit = fnColMesh.allIntersections(allPoints[i], vRay, NULL, NULL, false, MSpace::kObject, 9999999.0,
                              false, &mmAccelParams, true, hitPoints, NULL, &hitFaceIdArray, NULL, NULL, NULL);

            numHits = hitPoints.length();
            // If no hit, or the hit is divisible by 2 skip it, we are outside the mesh (Hormann & Agathos, 2001)
            if (!hit || numHits % 2 == 0){
              hitArray.append(0);
              flipRayArray.append(0);
              flipPointArray.append(initPoint);
              continue;
            }

            //========================================================================================================================================
            //========================================================================================================================================
            //This is a slower but more accurate cleanup pass of the algorithm to avoid swimming points and points flipping to the inside of the mesh.
            // Need to be sure there is actually a face in the opposite direction, if not there is no point to flipping

            if (eAlgorithm > 0)
            {
              fnColMesh.getPolygonNormal(hitFaceIdArray[0], polyNormal);
              flipCheck = polyNormal * vRay;
              if (flipCheck > 0)
              {
                vRay = vRay * -1.0;
                MFloatPointArray hitPointsFlipped;
                hit = fnColMesh.allIntersections(allPoints[i], vRay, NULL, NULL, false, MSpace::kObject, 9999999.0,
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
            //========================================================================================================================================
            //========================================================================================================================================
            hitArray.append(1);
            isInBBox = true;
        }
        else
        {
          hitArray.append(0);
          flipRayArray.append(0);
          flipPointArray.append(initPoint);
	    }
    }

  // Can Mostly be Run in Parallel, the fnMeshIntersector CANNOT be sent outside of this function, so an MObject needs to be passed out and the intersector created in the parallel function
    if (isInBBox){
      
      MObject oMesh = oColMeshArray[0];

      MMeshIntersector fnMeshIntersector;
      fnMeshIntersector.create(oMesh);


      MTimer timer;
      timer.beginTimer();

      // SerialParallelAverage(&tOutput, &tInput, 10);


      timer.endTimer();
      double serialTime = timer.elapsedTime();

      timer.beginTimer();

      bool failed = false;
      bool stop = false;
      // tbb::parallel_for(cancelable_range<unsigned int>(0, numPoints, numPoints / 1000, stop),
      //                   [&](const cancelable_range<unsigned int> &r) {
      //                           // Iterate over subrange. It is important that "<" be used for comparison,
      //                           // because the value of r.end() changes to r.begin() if r is cancelled.
      //                           for (unsigned int i = r.begin(); i < r.end(); ++i)
      //                           {
      //                                   // mesh point object must be in loop-local scope to avoid race conditions
      //                                   MPointOnMesh meshPoint;
      //                                   // Do intersection. Need to use per-thread status value as
      //                                   // MStatus has internal state and may trigger race conditions
      //                                   // if set from multiple threads. Probably benign in this case,
      //                                   // but worth being careful.
      //                                   MStatus localStatus = fnMeshIntersector.getClosestPoint(allPoints[i], meshPoint);
      //                                   if (localStatus != MStatus::kSuccess)
      //                                   {
      //                                           failed = true;
      //                                           r.cancel();
      //                                   }
      //                                   else
      //                                   {
      //                                           // default scheduling breaks traversal into large
      //                                           // chunks, so low risk of false sharing here in array write.
      //                                           allPoints[i] = meshPoint.getPoint();
      //                                   }
      //                           }
      //                   });

      // void test(const tbb::blocked_range<size_t> &r)
      // {
      //   for (size_t i = r.begin(); i != r.end(); ++i)
      //   {
      //     // mesh point object must be in loop-local scope to avoid race conditions
      //     MPointOnMesh meshPoint;
      //     // Do intersection. Need to use per-thread status value as
      //     // MStatus has internal state and may trigger race conditions
      //     // if set from multiple threads. Probably benign in this case,
      //     // but worth being careful.
      //     MStatus localStatus = fnMeshIntersector.getClosestPoint(allPoints[i], meshPoint);
      //   }
      // }


      // tbb::parallel_for( tbb::blocked_range<size_t>(0, numPoints), LHCollisionDeformer::testIntersector);




      timer.endTimer();
      double parallelTime = timer.elapsedTime();

      double ratio = serialTime / parallelTime;
      MString str = MString("\nElapsed time for serial computation: ") + serialTime + MString("s\n");
      str += MString("Elapsed time for parallel computation: ") + parallelTime + MString("s\n");
      str += MString("Speedup: ") + ratio + MString("x\n");
      MGlobal::displayInfo(str);











      if (eAlgorithm == 2){
      LHCollisionDeformer::BlendBulgeAndCollisionSerial(oColMeshArray, x, numPoints, hitArray,  flipRayArray, allPoints, vertexNormalArray, maxDisp, bulgeDistance,
                                                     rInnerFalloffRamp, bulgeAmount, flipPointArray, rFalloffRamp, rBlendBulgeCollisionRamp, mIndex);
      }
      else{
      LHCollisionDeformer::seperateBulgeAndCollisionSerial(oColMeshArray, x, numPoints, hitArray,  flipRayArray, allPoints, vertexNormalArray, maxDisp, bulgeDistance,
                                                     rInnerFalloffRamp, bulgeAmount, flipPointArray, rFalloffRamp, eAlgorithm, mIndex);
      }
    }
  }
  //============================= multi thread=================================================
  for (i=0;i < numPoints; i++){
    allPoints[i] = allPoints[i] * bBMatrix.inverse();
  }
  allPointsArray[mIndex] = allPoints;
  //==============================================================================================
  itGeo.setAllPositions(allPoints);
  return MS::kSuccess;
}
void LHCollisionDeformer::testIntersector(const tbb::blocked_range<size_t> &r)
{
  for (size_t i = r.begin(); i != r.end(); ++i)
  {
    // mesh point object must be in loop-local scope to avoid race conditions
    MPointOnMesh meshPoint;
    // Do intersection. Need to use per-thread status value as
    // MStatus has internal state and may trigger race conditions
    // if set from multiple threads. Probably benign in this case,
    // but worth being careful.
    MStatus localStatus = fnMeshIntersector.getClosestPoint(allPoints[i], meshPoint);
  }
}

void LHCollisionDeformer::BlendBulgeAndCollisionSerial(MObjectArray oColMeshArray, unsigned int colMeshIndex, unsigned int numPoints, MIntArray hitArray, MIntArray flipRayArray,
                                                       MPointArray &allPoints, MVectorArray vertexNormalArray, double maxDisp, double bulgeDistance, MRampAttribute rInnerFalloffRamp, double bulgeAmount,
                                                       MPointArray flipPointArray, MRampAttribute rFalloffRamp, MRampAttribute rBlendBulgeCollisionRamp, unsigned int mIndex)
{
  //=========================
  // Cannot be run in parallel, the MObject needs to be passed as an arg to the parallel function
  fnMeshIntersector.create(oColMeshArray[colMeshIndex]);
  //=========================
  for (i = 0; i < numPoints; i++)
  {
    collisionWeight = SafelyGetWeights(collisionWeightsArray, currentIndex, i);
    if (hitArray[i] && collisionWeight)
    {
      collisionPoint = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i, bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
      blendPoint = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
      distance = blendPoint.distanceTo(collisionPoint);
      relativeDistance = distance / bulgeDistance;
      rBlendBulgeCollisionRamp.getValueAtPosition((float)relativeDistance, value);
      collisionWeightPoint = blendPoint + (collisionPoint - blendPoint) * value;
      collisionWeight = SafelyGetWeights(collisionWeightsArray, currentIndex, i);
      allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
    }
  }
  for (i = 0; i < numPoints; i++)
  {
    bulgeWeight = SafelyGetWeights(bulgeWeightsArray, currentIndex, i);
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

  //=========================
  // Cannot be run in parallel, the MObject needs to be passed as an arg to the parallel function
  fnMeshIntersector.create(oColMeshArray[colMeshIndex]);
  //=========================

  for (i = 0; i < numPoints; i++)
  {
    collisionWeight = SafelyGetWeights(collisionWeightsArray, currentIndex, i);
    if (hitArray[i] && collisionWeight)
    {
      if (flipRayArray[i] && algorithm > 0)
      {
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentIndex, i);

        collisionWeightPoint = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i, bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
        allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
      }
      else
      {
        collisionWeight = SafelyGetWeights(collisionWeightsArray, currentIndex, i);
        collisionWeightPoint = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
        allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
      }
    }
  }

  for (i = 0; i < numPoints; i++)
  {
    bulgeWeight = SafelyGetWeights(bulgeWeightsArray, currentIndex, i);
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
  bulgeWeight = SafelyGetWeights(bulgeWeightsArray, currentIndex, pointIdx);
  //=========================
  // Need to check whether this can be called from a parallel function, or if a threaded version will need to be written
  return LHCollisionDeformer::getBulge(allPoints[pointIdx], closestPoint, bulgeAmount, bulgeDistance, vRay, maxDisp, rFalloffRamp, bulgeWeight);
  //=========================
}
MPoint LHCollisionDeformer::getBulge(MPoint currPoint, MPoint closestPoint, double bulgeAmount,
                                     double bulgeDistance, MVector vRay, double maxDisp, MRampAttribute rFalloffRamp, double bulgeWeight)
{
  distance = currPoint.distanceTo(closestPoint);
  relativeDistance = distance / bulgeDistance;
  rFalloffRamp.getValueAtPosition((float)relativeDistance, value);
  return currPoint + vRay * bulgeAmount * relativeDistance * maxDisp * value * bulgeWeight;
}
