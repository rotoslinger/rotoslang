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

#include "LHMatrixDeformer.h"

MTypeId LHMatrixDeformer::id(0x008954863);
MObject LHMatrixDeformer::aInputs;
MObject LHMatrixDeformer::aMatrix;
MObject LHMatrixDeformer::aMatrixBase;
MObject LHMatrixDeformer::aStart;
MObject LHMatrixDeformer::aEnd;
MObject LHMatrixDeformer::aNumTasks;
MObject LHMatrixDeformer::aMultiThread;
MObject LHMatrixDeformer::aMatrixWeight;
// MObject LHMatrixDeformer::aMatrixWeights;
MObject LHMatrixDeformer::aMembershipWeight;



MStatus LHMatrixDeformer::initialize() {

  MFnMatrixAttribute mAttr;
  MFnCompoundAttribute cAttr;
  MFnNumericAttribute nAttr;
  MFnTypedAttribute tAttr;

  aMultiThread = nAttr.create( "multiThread", "mthread", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setMin(0);
  nAttr.setMax(2);
  nAttr.setDefault(1);
  nAttr.setChannelBox(true);
  addAttribute( aMultiThread );


  aStart = nAttr.create( "start", "st", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1);
  nAttr.setChannelBox(true);
  addAttribute( aStart );


  aEnd = nAttr.create( "end", "ed", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(100);
  nAttr.setChannelBox(true);
  addAttribute( aEnd );

  aNumTasks = nAttr.create( "numTasks", "nt", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(16);
  nAttr.setChannelBox(true);
  addAttribute( aNumTasks );

  attributeAffects(aMultiThread, outputGeom);
  attributeAffects(aStart, outputGeom);
  attributeAffects(aEnd, outputGeom);
  attributeAffects(aNumTasks, outputGeom);


  aMatrix = mAttr.create("matrix", "matrix");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aMatrix );

  aMatrixBase = mAttr.create("matrixBase", "matrixbase");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aMatrixBase );



    aMatrixWeight = tAttr.create("matrixWeight", "matrixweight", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aMatrixWeight);

    aMembershipWeight = tAttr.create("membershipWeight", "mw", MFnNumericData::kDoubleArray);
    tAttr.setKeyable(true);
    tAttr.setArray(false);
    tAttr.setUsesArrayDataBuilder(true);
    addAttribute(aMembershipWeight);


  aInputs = cAttr.create("Inputs", "inputs");
  cAttr.setKeyable(true);
  cAttr.setArray(true);
  cAttr.addChild( aMatrix );
  cAttr.addChild( aMatrixBase );
  cAttr.addChild( aMatrixWeight );
  cAttr.addChild( aMembershipWeight );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aInputs);

  attributeAffects(aInputs, outputGeom);
  //attributeAffects(aMatrix, outputGeom);


  // Make the deformer weights paintable
//   MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer LHMatrixDeformer weights;");
    MGlobal::executeCommand("makePaintable -attrType doubleArray -sm deformer LHMatrixDeformer membershipWeight;");
    MGlobal::executeCommand("makePaintable -attrType doubleArray -sm deformer LHMatrixDeformer matrixWeight;");

  return MS::kSuccess;
}


//Step3
// This is what performs the actual deformation calculations
MThreadRetVal ParallelDeformationCalc(void *data)
{
    TaskData *task_data = (TaskData *)data;
	MPoint pt;
    for( unsigned int i = task_data->start + task_data->currThreadNum; i <= task_data->end; i += task_data->numTasks )
    {
    	if (i >= task_data->end)
    	{
    		break;
    	}
    	pt = task_data->allPoints[i];
        for (unsigned int x=0;x < task_data->nPlugs;x++)
        {
            if (task_data->matrixArray[x] != task_data->matrixArrayBase[x])
                pt = (pt * task_data->matrixArrayBase[x].inverse() * task_data->matrixArray[x]);

        }
    	task_data->finalPointArray.append(pt);
    	task_data->finalIndexArray.append(i);

    }

    return (MThreadRetVal)0;

}
//Step2
// Decomposition refers to breaking up an algorithm into multiple tasks
void DecomposeDeformationCalc(void *data, MThreadRootTask *root)
{
    TaskData *tdata = (TaskData *)data;
    int numTasks = tdata->numTasks;
    std::vector <TaskData> task_data(numTasks);
    MPointArray finalPoints;
    finalPoints.setLength(tdata->allPoints.length());
    tdata->finalPoints.setLength(tdata->allPoints.length());
//    tdata->finalPoints = finalPoints;
    for( int i = 0; i < numTasks; ++i ){
//		MGlobal::displayInfo(MString("DEBUG: task iter ") + i);
//	    TaskData task_data;
		task_data[i].env = tdata->env;
		task_data[i].matrixArray = tdata->matrixArray;
		task_data[i].matrixArrayBase = tdata->matrixArrayBase;
		task_data[i].allPoints = tdata->allPoints;
		task_data[i].pt = tdata->pt;
		task_data[i].nPlugs = tdata->nPlugs;
		task_data[i].start = tdata->start;
		task_data[i].end = tdata->end;
		task_data[i].numTasks = numTasks;
        task_data[i].currThreadNum = i;
        task_data[i].finalPoints = tdata->finalPoints;
        MThreadPool::createTask(ParallelDeformationCalc, (void *)&task_data[i], root);
    }
    MThreadPool::executeAndJoin(root);
    for( int i = 0; i < numTasks; ++i ){
        for( int x = 0; x < task_data[i].finalPointArray.length(); ++x ){
        	finalPoints[task_data[i].finalIndexArray[x]] = task_data[i].finalPointArray[x];
        }
    }
    tdata->finalPoints = finalPoints;
}

// Step1
// Main threading this will create the threadpool, create the parallel region, decompose
// then release the threadpool after everything is done
MPointArray MainParallelDeformationCalc(float env, MMatrixArray matrixArray, MMatrixArray matrixArrayBase, MPointArray allPoints,
						        MPoint pt, unsigned int nPlugs,
								int start, int end, int numTasks){
    MStatus stat = MThreadPool::init();
    if( MStatus::kSuccess != stat )
    {
        MString str = MString("Error creating threadpool");
        MGlobal::displayError(str);
        MPointArray empty;
        return empty;
    }
    TaskData task_data;
    task_data.env = env;
    task_data.matrixArray = matrixArray;
    task_data.matrixArrayBase = matrixArrayBase;
    task_data.allPoints = allPoints;
    task_data.pt = pt;
    task_data.nPlugs = nPlugs;
    task_data.start = start;
    task_data.end = end;
    task_data.numTasks = numTasks;
    MThreadPool::newParallelRegion(DecomposeDeformationCalc, (void *)&task_data);
    // pool is reference counted. Release reference to current thread instance
    MThreadPool::release();
    // release reference to whole pool which deletes all threads
    MThreadPool::release();
    return task_data.finalPoints;

}


void* LHMatrixDeformer::creator() { return new LHMatrixDeformer; }

MStatus LHMatrixDeformer::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;

  float env = data.inputValue(envelope).asFloat();
  int start = data.inputValue(aStart).asInt();
  int end = data.inputValue(aEnd).asInt();
  int numTasks = data.inputValue(aNumTasks).asInt();
  int multiThread = data.inputValue(aMultiThread).asInt();
  if (multiThread and numTasks==0)
  {
	  return MS::kFailure;

  }

  if (env<=0.0)
  {
	  return MS::kSuccess;

  }
  MMatrixArray matrixArray;
  MMatrixArray matrixArrayBase;
  std::vector <MDoubleArray> matrixWeights;
  MDoubleArray checkWeights;
  MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHMatrixDeformer::aInputs, &status));
  CheckStatusReturn( status, "Unable to get inputs" );
  unsigned int inputCount = inputsArrayHandle.elementCount(&status);
  CheckStatusReturn( status, "Unable to get number of inputs" );
  MMatrix tempMatrix;
  for (unsigned int i=0;i < inputCount;i++){
      status = inputsArrayHandle.jumpToElement(i);
      MDataHandle handle(inputsArrayHandle.inputValue(&status) );
      CheckStatusReturn( status, "Couldn't get array handle" );
      
      matrixArray.append(handle.child( LHMatrixDeformer::aMatrix ).asMatrix());
      matrixArrayBase.append(handle.child( LHMatrixDeformer::aMatrixBase ).asMatrix());

      MDataHandle weightChild(handle.child( aMatrixWeight) );
      checkWeights = MFnDoubleArrayData(weightChild.data()).array(&status);
      CheckStatusReturn( status, "Couldn't get Weights" );
      if (checkWeights.length() != itGeo.count())
            {
                MGlobal::displayError(MString("Weights do not coorespond with Geometry"));
                return MS::kFailure;
            }
      matrixWeights.push_back(checkWeights);
  }
  int nPlugs = matrixArray.length();
  MPoint pt;
  MPointArray finalPoints;

  if (multiThread == 0){
	  for (; !itGeo.isDone(); itGeo.next()){
		  pt = itGeo.position();
		  for (unsigned int i=0;i < nPlugs;i++)
		  {
			// pt = pt + (pt - (pt * matrixArray[i] * matrixArrayBase[i].inverse())) * matrixWeights[i][itGeo.index()];
			//pt = pt * matrixArray[i] * matrixArrayBase[i].inverse();
            MPoint deformedPt = pt * (matrixArray[i] * matrixArrayBase[i].inverse());
			pt = pt + (deformedPt - pt)* matrixWeights[i][itGeo.index()];
		  }
		  finalPoints.append(pt);
	  }
	  itGeo.setAllPositions(finalPoints);
	  return MS::kSuccess;
	}

  if (multiThread == 1){
	  MPointArray allPoints;
	  itGeo.allPositions(allPoints);
	  unsigned int tStart = 0;
	  unsigned int tEnd = allPoints.length();
	  finalPoints = MainParallelDeformationCalc(env, matrixArray, matrixArrayBase, allPoints, pt, nPlugs, tStart, tEnd, numTasks);
	  // Make sure the points to set are exactly the same as the poly count or you will crash maya!
	  if (finalPoints.length() != allPoints.length())
		  return MS::kFailure;
	  itGeo.setAllPositions(finalPoints);
	  return MS::kSuccess;
  }


  if (multiThread == 2){
	  MTimer timer;
	  timer.beginTimer();

	  for (; !itGeo.isDone(); itGeo.next()){
		  pt = itGeo.position();
	      for (unsigned int i=0;i < nPlugs;i++)
	      {
			  pt = pt * matrixArray[i] * matrixArrayBase[i].inverse();
	      }
	      finalPoints.append(pt);
	  }
	  itGeo.setAllPositions(finalPoints);
	  timer.endTimer();
	  double serialTime = timer.elapsedTime();
	  timer.beginTimer();

	  MPointArray allPoints;
	  itGeo.allPositions(allPoints);
	  unsigned int tStart = 0;
	  unsigned int tEnd = allPoints.length();
	  finalPoints = MainParallelDeformationCalc(env, matrixArray, matrixArrayBase, allPoints, pt, nPlugs, tStart, tEnd, numTasks);
	  // Make sure the points to set are exactly the same as the poly count or you will crash maya!
	  if (finalPoints.length() != allPoints.length())
		  return MS::kFailure;
	  itGeo.setAllPositions(finalPoints);

	  timer.endTimer();
	  double parallelTime = timer.elapsedTime();


	  double ratio = serialTime/parallelTime;
	  MString str = MString("\nElapsed time for serial computation: ") + serialTime + MString("s\n");
	  str += MString("Elapsed time for parallel computation: ") + parallelTime + MString("s\n");
	  str += MString("Speedup: ") + ratio + MString("x\n");
	  MGlobal::displayInfo(str);
	  return MStatus::kSuccess;


  }



  return MS::kSuccess;

}
MStatus LHMatrixDeformer::getWeights(MObject oInputsCompound, MObject oWeightsChild, MDataBlock &data, int mIndex, MDoubleArray &rDoubleArray)
{
    MStatus status;
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( oInputsCompound, &status));
    CheckStatusReturn( status, "Unable to get inputs" );
    int inputCount = inputsArrayHandle.elementCount(&status);
    CheckStatusReturn( status, "Unable to get number of inputs" );
    if (inputCount >= mIndex)
    {
      status = inputsArrayHandle.jumpToElement(mIndex);
      CheckStatusReturn( status, "Couldn't jump to element" );
      MDataHandle handle(inputsArrayHandle.inputValue(&status) );
      CheckStatusReturn( status, "Couldn't get array handle" );
      MDataHandle weightChild(handle.child( oWeightsChild) );
      rDoubleArray = MFnDoubleArrayData(weightChild.data()).array(&status);
      CheckStatusReturn( status, "Couldn't get Weights" );
      return MS::kSuccess;
    }
    return MS::kFailure;
}
