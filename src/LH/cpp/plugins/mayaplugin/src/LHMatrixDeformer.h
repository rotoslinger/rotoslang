#pragma once
#include "formatErrorMacros.h"
#include "threadingStructs.h"
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>
#include <maya/MMatrixArray.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnDoubleArrayData.h>

#include <maya/MPxDeformerNode.h>

#include <math.h>
#include <maya/MIOStream.h>
#include <maya/MSimple.h>
#include <maya/MTimer.h>
#include <maya/MThreadPool.h>
#include <iostream>
#include <string>
#include <vector>


// typedef struct _threadDataTag
// {
//     int threadNo;
//     long primesFound;
//     long start, end;
//     int numTasks;

// } threadData;

// typedef struct _taskDataTag
// {
//     long start, end, totalPrimes;
//     int numTasks;

// } taskData;

// #define NUM_TASKS	16








class LHMatrixDeformer : public MPxDeformerNode {
 public:
  LHMatrixDeformer() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  MStatus getWeights(MObject oInputsCompound, MObject oWeightsChild, MDataBlock &data, int mIndex, MDoubleArray &rDoubleArray);
  static void* creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aInputs;
  static MObject aMatrix;
  static MObject aMatrixBase;
  static MObject aStart;
  static MObject aEnd;
  static MObject aNumTasks;
  static MObject aMultiThread;
  static MObject aMatrixWeight;
  static MObject aMembershipWeight;


  inline MString FormatError( const MString &msg, const MString
                                &sourceFile, const int &sourceLine )
  {
      MString txt( "[LHMatrixDeformer] " );
      txt += msg ;
      txt += ", File: ";
      txt += sourceFile;
      txt += " Line: ";
      txt += sourceLine;
      return txt;
  }


};
