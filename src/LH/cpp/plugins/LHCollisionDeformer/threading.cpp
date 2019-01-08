#include "LHCollisionDeformer.h"



//Step3
// This is what performs the actual deformation calculations
MThreadRetVal ParallelDeformationCalc(void *data)
{
    matrixSpaceTaskData *task_data = (matrixSpaceTaskData *)data;

    for( unsigned int i = 0 + task_data->threadData.currThreadNum; i <= task_data->allPoints.length(); i += task_data->threadData.numTasks )
    {
    	if (i >= task_data->allPoints.length())
    	{
    		break;
    	}
    	task_data->finalPointArray.append(task_data->allPoints[i] * task_data->wSpaceMatrix);
    	task_data->finalIndexArray.append(i);
    }
    return (MThreadRetVal)0;
}

//Step2
// Decomposition refers to breaking up an algorithm into multiple tasks
void DecomposeDeformationCalc(void *data, MThreadRootTask *root)
{
    // Casting data to the matrixSpaceTaskData
    matrixSpaceTaskData *tdata = (matrixSpaceTaskData *)data;
    int numTasks = tdata->threadData.numTasks;
    std::vector <matrixSpaceTaskData> task_data(numTasks);
    MPointArray finalPoints;
    finalPoints.setLength(tdata->allPoints.length());
    tdata->finalPoints.setLength(tdata->allPoints.length());
    for( int i = 0; i < numTasks; ++i )
    {
      task_data[i].wSpaceMatrix = tdata->wSpaceMatrix;
      task_data[i].allPoints = tdata->allPoints;
      task_data[i].threadData.numTasks = tdata->threadData.numTasks;
      task_data[i].threadData.currThreadNum = i;
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
MPointArray MainParallelDeformationCalc(MMatrix wSpaceMatrix, MPointArray allPoints, int numTasks){
    MStatus stat = MThreadPool::init();
    if( MStatus::kSuccess != stat )
    {
        MString str = MString("Error creating threadpool");
        MGlobal::displayError(str);
        MPointArray empty;
        return empty;
    }
    matrixSpaceTaskData task_data;
    task_data.wSpaceMatrix = wSpaceMatrix;
    task_data.allPoints = allPoints;
    task_data.threadData.numTasks = numTasks;
    MThreadPool::newParallelRegion(DecomposeDeformationCalc, (void *)&task_data);
    // pool is reference counted. Release reference to current thread instance
    MThreadPool::release();
    // release reference to whole pool which deletes all threads
    MThreadPool::release();
    return task_data.finalPoints;

}


double SafelyGetWeights(std::vector <MDoubleArray> weights, unsigned int currentIndex, unsigned int currentPointIndex){
// Bitwise && to make sure if anything fails it won't check the condition to the right...
if (weights.size() && weights.size() >= currentIndex && weights[currentIndex].length() && weights[currentIndex].length() >= currentPointIndex){
  return weights[currentIndex][currentPointIndex];
}
return 1.0;
}





void LHCollisionDeformer::DecomposeBlendBulgeAndCollision(void *data, MThreadRootTask *root)
{
    // Casting data to the matrixSpaceTaskData
    bulgeTaskData *tdata = (bulgeTaskData *)data;
    int numTasks = tdata->numTasks;
    std::vector<bulgeTaskData> task_data(numTasks);
    // MPointArray finalPoints;
    // finalPoints.length() = tdata->allPoints.length();
    // tdata->finalPoints.setLength(tdata->allPoints.length());

    for (int i = 0; i < numTasks; ++i)
    {
        task_data[i].oColMeshArray = tdata->oColMeshArray;
        task_data[i].colMeshIndex = tdata->colMeshIndex;    
        task_data[i].numPoints = tdata->numPoints;
        task_data[i].hitArray = tdata->hitArray;
        task_data[i].flipRayArray = tdata->flipRayArray;
        task_data[i].vertexNormalArray = tdata->vertexNormalArray;
        task_data[i].maxDisp = tdata->maxDisp;
        task_data[i].bulgeDistance = tdata->bulgeDistance;
        task_data[i].rInnerFalloffRamp = tdata->rInnerFalloffRamp;
        task_data[i].flipPointArray = tdata->flipPointArray;
        task_data[i].rFalloffRamp = tdata->rFalloffRamp;
        task_data[i].rBlendBulgeCollisionRamp = tdata->rBlendBulgeCollisionRamp;
        task_data[i].mIndex = tdata->mIndex;
        task_data[i].numTasks = tdata->numTasks;
        task_data[i].currThreadNum = i;
        task_data[i].finalPointArray.setLength(tdata->allPoints.length());

        MThreadPool::createTask(BlendBulgeAndCollisionLoop, (void *)&task_data[i], root);
    }

    MThreadPool::executeAndJoin(root);

    //retrieve needed data, especially allPoints and maxDisp.  Find largest maxDisp out of all the tasks.

    // for( int i = 0; i < numTasks; ++i ){
    //     for( int x = 0; x < task_data[i].finalPointArray.length(); ++x ){
    //     	tdata->allPoints[task_data[i].finalIndexArray[x]] = task_data[i].finalPointArray[x];
    //     }
    // }
    // tdata->allPoints = finalPoints;
}


//Step3
// This is what performs the actual deformation calculations
MThreadRetVal LHCollisionDeformer::BlendBulgeAndCollisionLoop(void *data)
{

    MMeshIntersector fnMeshIntersector;
    bulgeTaskData *task_data = (bulgeTaskData *)data;
    fnMeshIntersector.create(task_data->oColMeshArray[task_data->colMeshIndex]);
    
    // float value;
    // for( unsigned int i = 0 + task_data->currThreadNum; i <= task_data->allPoints.length(); i += task_data->numTasks )
    // {

    //     double collisionWeight = SafelyGetWeights(collisionWeightsArray, task_data->mIndex, i);
    //     if (task_data->hitArray[i] && collisionWeight)
    //     {
    //         collisionPoint = LHCollisionDeformer::CollisionFlipCheckSerial(task_data->allPoints, i, task_data->bulgeDistance, task_data->bulgeAmount, task_data->vertexNormalArray, task_data->maxDisp, task_data->flipPointArray, task_data->rInnerFalloffRamp);
    //         blendPoint = LHCollisionDeformer::CollisionCheapSerial(task_data->allPoints, i, task_data->maxDisp);
    //         distance = blendPoint.distanceTo(collisionPoint);
    //         relativeDistance = distance / task_data->bulgeDistance;
    //         task_data->rBlendBulgeCollisionRamp.getValueAtPosition((float)relativeDistance, value);
    //         collisionWeightPoint = blendPoint + (collisionPoint - blendPoint) * value;
    //         collisionWeight = SafelyGetWeights(collisionWeightsArray, task_data->mIndex, i);
    //         task_data->finalPointArray[i] = task_data->allPoints[i] + (collisionWeightPoint - task_data->allPoints[i]) * collisionWeight;
    //     }





    // }
    return (MThreadRetVal)0;
}

// struct Average {
//     const float* input;
//     float* output;
//     MObject* oMesh;
//     MMeshIntersector* fnMeshIntersector;
//     void operator()( const blocked_range<int> &range ) const {
//         for( int i=range.begin(); i!=range.end(); ++i )
//             // MMeshIntersector* fnMeshIntersector;
//             fnMeshIntersector->create(*oMesh);
//             // output[i] = (input[i-1]+input[i]+input[i+1])*(1/3.f);
//     }
// };

// // Note: Reads input[0..n] and writes output[1..n-1]. 
// void ParallelAverage( MObject* oMesh, MMeshIntersector* fnMeshIntersector,float* output, const float* input, size_t n ) {
//     Average avg;
//     avg.input = input;
//     avg.output = output;
//     parallel_for( blocked_range<int>( 0, n ), avg );
//     }

// void SerialParallelAverage( float* output, const float* input, size_t n ) {
//     Average avg;
//     avg.input = input;
//     avg.output = output;
//     serial::parallel_for( blocked_range<int>( 0, n ), avg );
//     }



void LHCollisionDeformer::BlendBulgeAndCollisionParallel(MObjectArray oColMeshArray, unsigned int colMeshIndex, unsigned int numPoints, MIntArray hitArray, MIntArray flipRayArray,
                                                       MPointArray &allPoints, MVectorArray vertexNormalArray, double maxDisp, double bulgeDistance, MRampAttribute rInnerFalloffRamp, double bulgeAmount,
                                                       MPointArray flipPointArray, MRampAttribute rFalloffRamp, MRampAttribute rBlendBulgeCollisionRamp, unsigned int mIndex, unsigned int numTasks)
{
    MStatus stat = MThreadPool::init();
    if( MStatus::kSuccess != stat )
    {
        MString str = MString("Error creating threadpool");
        MGlobal::displayError(str);
    }

    //=========================
    // Cannot be run in parallel, the MObject needs to be passed as an arg to the parallel function
    // fnMeshIntersector.create(oColMeshArray[colMeshIndex]);

    bulgeTaskData task_data;


    task_data.oColMeshArray = oColMeshArray;
    task_data.colMeshIndex = colMeshIndex;    
    task_data.numPoints = numPoints;
    task_data.hitArray = hitArray;
    task_data.flipRayArray = flipRayArray;
    task_data.vertexNormalArray = vertexNormalArray;
    task_data.maxDisp = maxDisp;
    task_data.bulgeDistance = bulgeDistance;
    task_data.rInnerFalloffRamp = rInnerFalloffRamp;
    task_data.flipPointArray = flipPointArray;
    task_data.rFalloffRamp = rFalloffRamp;
    task_data.rBlendBulgeCollisionRamp = rBlendBulgeCollisionRamp;
    task_data.mIndex = mIndex;
    task_data.numTasks = numTasks;




    MThreadPool::newParallelRegion(DecomposeBlendBulgeAndCollision, (void *)&task_data);
    // pool is reference counted. Release reference to current thread instance
    MThreadPool::release();
    // release reference to whole pool which deletes all threads
    MThreadPool::release();

    // //=========================
    // for (i = 0; i < numPoints; i++)
    // {
    //     collisionWeight = SafelyGetWeights(collisionWeightsArray, currentIndex, i);
    //     if (hitArray[i] && collisionWeight)
    //     {
    //         collisionPoint = LHCollisionDeformer::CollisionFlipCheckSerial(allPoints, i, bulgeDistance, bulgeAmount, vertexNormalArray, maxDisp, flipPointArray, rInnerFalloffRamp);
    //         blendPoint = LHCollisionDeformer::CollisionCheapSerial(allPoints, i, maxDisp);
    //         distance = blendPoint.distanceTo(collisionPoint);
    //         relativeDistance = distance / bulgeDistance;
    //         rBlendBulgeCollisionRamp.getValueAtPosition((float)relativeDistance, value);
    //         collisionWeightPoint = blendPoint + (collisionPoint - blendPoint) * value;
    //         collisionWeight = SafelyGetWeights(collisionWeightsArray, currentIndex, i);
    //         allPoints[i] = allPoints[i] + (collisionWeightPoint - allPoints[i]) * collisionWeight;
    //     }
    // }

    // for (i = 0; i < numPoints; i++)
    // {
    //     bulgeWeight = SafelyGetWeights(bulgeWeightsArray, currentIndex, i);
    //     if (!hitArray[i] && bulgeWeight)
    //     {
    //         allPoints[i] = LHCollisionDeformer::PerformBulgeSerial(vertexNormalArray, i, allPoints, bulgeAmount, bulgeDistance, maxDisp, rFalloffRamp);
    //     }
    // }
}




//======================================================================
// Cancelable range implementation, so that a parallel_for can end early
// if a failure (or for that matter, a success) is found.
//
// From https://software.intel.com/en-us/blogs/2007/11/08/have-a-fish-how-break-from-a-parallel-loop-in-tbb
//
template <typename Value>
class cancelable_range
{
        tbb::blocked_range<Value> my_range;
        volatile bool &my_stop;

      public:
        // Constructor for client code
        cancelable_range(int begin, int end, int grainsize, volatile bool &stop) : my_range(begin, end, grainsize),
                                                                                   my_stop(stop)
        {
        }
        cancelable_range(cancelable_range &r, tbb::split) : my_range(r.my_range, tbb::split()),
                                                            my_stop(r.my_stop)
        {
        }
        cancelable_range &operator=(const cancelable_range &);
        void cancel() const { my_stop = true; }
        bool empty() const { return my_stop || my_range.empty(); }
        bool is_divisible() const { return !my_stop && my_range.is_divisible(); }
        Value begin() const { return my_range.begin(); }
        Value end() const { return my_stop ? my_range.begin() : my_range.end(); }
};
//======================================================================
