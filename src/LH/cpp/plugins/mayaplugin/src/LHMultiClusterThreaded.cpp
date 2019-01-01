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

#include "LHMultiClusterThreaded.h"
#include <maya/MFnPlugin.h>

MTypeId LHMultiClusterThreaded::id(0x00833467);
MObject LHMultiClusterThreaded::aInputs;
MObject LHMultiClusterThreaded::aMatrix;
MObject LHMultiClusterThreaded::aStart;
MObject LHMultiClusterThreaded::aEnd;
MObject LHMultiClusterThreaded::aNumTasks;
MObject LHMultiClusterThreaded::aMultiThread;



MStatus LHMultiClusterThreaded::initialize() {

  MFnMatrixAttribute mAttr;
  MFnCompoundAttribute cAttr;
  MFnNumericAttribute nAttr;

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


  aMatrix = mAttr.create("Matrix", "matrix");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aMatrix );

  aInputs = cAttr.create("Inputs", "inputs");
  cAttr.setKeyable(true);
  cAttr.setArray(true);
  cAttr.addChild( aMatrix );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aInputs);

  attributeAffects(aInputs, outputGeom);
  //attributeAffects(aMatrix, outputGeom);


  // Make the deformer weights paintable
  MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer LHMultiClusterThreaded weights;");

  return MS::kSuccess;
}


static bool TestForPrime(int val)
{
    int limit, factor = 3;
    limit = (long)(sqrtf((float)val)+0.5f);
    while( (factor <= limit) && (val % factor))
        factor ++;
    return (factor > limit);
}

// Primes finder. This function is called from multiple threads
MThreadRetVal Primes(void *data)
{
    threadData *myData = (threadData *)data;
    int numTasks = myData->numTasks;
    for( int i = myData->start + myData->threadNo*2; i <= myData->end; i += 2*numTasks )
    {
        if( TestForPrime(i) )
        myData->primesFound++;
    }
    return (MThreadRetVal)0;
}

// Function to create thread tasks
void DecomposePrimes(void *data, MThreadRootTask *root)
{
    taskData *taskD = (taskData *)data;
    int numTasks = taskD->numTasks;
    threadData tdata[numTasks];

    for( int i = 0; i < numTasks; ++i )
    {
        tdata[i].threadNo = i;
        tdata[i].primesFound = 0;
        tdata[i].start = taskD->start;
        tdata[i].end = taskD->end;
        tdata[i].numTasks = numTasks;
        MThreadPool::createTask(Primes, (void *)&tdata[i], root);
    }
    MThreadPool::executeAndJoin(root);
    for( int i = 0; i < numTasks; ++i )
    {
        taskD->totalPrimes += tdata[i].primesFound;
    }
}

// Single threaded calculation
int SerialPrimes(int start, int end)
{
    int primesFound = 0;
    for( int i = start; i <= end; i+=2)
    {
        if( TestForPrime(i) )
            primesFound++;
    }
    return primesFound;
}

// Set up and tear down parallel tasks
int ParallelPrimes(int start, int end, int numTasks)
{
    MStatus stat = MThreadPool::init();
    if( MStatus::kSuccess != stat ) {
        MString str = MString("Error creating threadpool");
        MGlobal::displayError(str);
        return 0;
    }

    taskData tdata;
    tdata.totalPrimes = 0;
    tdata.start = start;
    tdata.end = end;
    tdata.numTasks = numTasks;
    MThreadPool::newParallelRegion(DecomposePrimes, (void *)&tdata);
    // pool is reference counted. Release reference to current thread instance
    MThreadPool::release();
    // release reference to whole pool which deletes all threads
    MThreadPool::release();
    return tdata.totalPrimes;
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
        	pt = pt * task_data->matrixArray[x];
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
MPointArray MainParallelDeformationCalc(float env, MMatrixArray matrixArray, MPointArray allPoints,
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


void* LHMultiClusterThreaded::creator() { return new LHMultiClusterThreaded; }

MStatus LHMultiClusterThreaded::deform(MDataBlock& data, MItGeometry& itGeo,
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

//  MGlobal::displayInfo(MString("DEBUG:  Start ") + start);
//  MGlobal::displayInfo(MString("DEBUG:  end ") + end);

  //======================================================
  //=======THREADTEST=====================================
  //======================================================

  // start search on an odd number
//  if((start % 2) == 0 ) start++;
//  // run single threaded
//  MTimer timer;
//  timer.beginTimer();
//  int serialPrimes = SerialPrimes(start, end);
//  timer.endTimer();
//  double serialTime = timer.elapsedTime();
//  // run multithreaded
//  timer.beginTimer();
//  int parallelPrimes = ParallelPrimes(start, end, numTasks);
//  timer.endTimer();
//  double parallelTime = timer.elapsedTime();
//  // check for correctness
//  if ( serialPrimes != parallelPrimes ) {
//      MString str("Error: Computations inconsistent");
//      MGlobal::displayError(str);
//      return MStatus::kFailure;
//  }
//  // print results
//  double ratio = serialTime/parallelTime;
//  MString str = MString("\nElapsed time for serial computation: ") + serialTime + MString("s\n");
//  str += MString("Elapsed time for parallel computation: ") + parallelTime + MString("s\n");
//  str += MString("Speedup: ") + ratio + MString("x\n");
//  MGlobal::displayInfo(str);
  //return MStatus::kSuccess;
  //======================================================
  //======================================================
  //======================================================

  if (env<=0.0)
  {
	  return MS::kSuccess;

  }
  MMatrixArray matrixArray;
  MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHMultiClusterThreaded::aInputs, &status));
  CheckStatusReturn( status, "Unable to get inputs" );
  unsigned int inputCount = inputsArrayHandle.elementCount(&status);
  CheckStatusReturn( status, "Unable to get number of inputs" );
  MMatrix tempMatrix;
  for (unsigned int i=0;i < inputCount;i++){
      status = inputsArrayHandle.jumpToElement(i);
      matrixArray.append(inputsArrayHandle.inputValue().child( LHMultiClusterThreaded::aMatrix ).asMatrix());
  }
  int nPlugs = matrixArray.length();
  MPoint pt;
  MPointArray finalPoints;

  if (multiThread == 0){
	  for (; !itGeo.isDone(); itGeo.next()){
		  pt = itGeo.position();
		  for (unsigned int i=0;i < nPlugs;i++)
		  {
			  pt = pt * matrixArray[i];
		  }
		  finalPoints.append(pt);
		  //itGeo.setPosition(pt);
	  }
	  itGeo.setAllPositions(finalPoints);
	  return MS::kSuccess;
	}

  if (multiThread == 1){
	  MPointArray allPoints;
	  itGeo.allPositions(allPoints);
	  unsigned int tStart = 0;
	  unsigned int tEnd = allPoints.length();
	  finalPoints = MainParallelDeformationCalc(env, matrixArray, allPoints, pt, nPlugs, tStart, tEnd, numTasks);
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
	          pt = pt * matrixArray[i];
	      }
	      finalPoints.append(pt);
	      //itGeo.setPosition(pt);
	  }
	  itGeo.setAllPositions(finalPoints);
	  timer.endTimer();
	  double serialTime = timer.elapsedTime();
	  timer.beginTimer();

	  MPointArray allPoints;
	  itGeo.allPositions(allPoints);
	  unsigned int tStart = 0;
	  unsigned int tEnd = allPoints.length();
	  finalPoints = MainParallelDeformationCalc(env, matrixArray, allPoints, pt, nPlugs, tStart, tEnd, numTasks);
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
