#ifndef LHMULTICLUSTERTHREADED_H
#define LHMULTICLUSTERTHREADED_H

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

#include <maya/MPxDeformerNode.h>

#include <math.h>
#include <maya/MIOStream.h>
#include <maya/MSimple.h>
#include <maya/MTimer.h>
#include <maya/MThreadPool.h>
#include <iostream>
#include <string>
#include <vector>


typedef struct _threadDataTag
{
    int threadNo;
    long primesFound;
    long start, end;
    int numTasks;

} threadData;

typedef struct _taskDataTag
{
    long start, end, totalPrimes;
    int numTasks;

} taskData;

#define NUM_TASKS	16




struct ThreadData
{
	int start;
	int end;
	int numTasks = 10;
	int currThreadNum;

};

struct TaskData
{
	float env;
	MMatrixArray matrixArray;
	MPointArray allPoints;
	MPointArray finalPoints;
	MPoint pt;
	MIntArray finalIndexArray;
	MPointArray finalPointArray;
	unsigned int nPlugs;
	// I could pass the thread data struct in here, but I am trying to make this as simple as possible
	// For learning purposes...
	int start;
	int end;
	int numTasks = 10;
	int currThreadNum;
};






class LHMultiClusterThreaded : public MPxDeformerNode {
 public:
  LHMultiClusterThreaded() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  static void* creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aInputs;
  static MObject aMatrix;
  static MObject aStart;
  static MObject aEnd;
  static MObject aNumTasks;
  static MObject aMultiThread;


  inline MString FormatError( const MString &msg, const MString
                                &sourceFile, const int &sourceLine )
  {
      MString txt( "[LHMultiClusterThreaded] " );
      txt += msg ;
      txt += ", File: ";
      txt += sourceFile;
      txt += " Line: ";
      txt += sourceLine;
      return txt;
  }
  #define Error( msg ) \
      { \
      MString __txt = FormatError( msg, __FILE__, __LINE__ ); \
      MGlobal::displayError( __txt ); \
      cerr << endl << "Error: " << __txt; \
      } \

  #define CheckBool( result ) \
      if( !(result) ) \
          { \
          Error( #result ); \
          }

  #define CheckStatus( stat, msg ) \
      if( !stat ) \
          { \
          Error( msg ); \
          }

  #define CheckObject( obj, msg ) \
      if(obj.isNull() ) \
          { \
          Error( msg ); \
          }

  #define CheckStatusReturn( stat, msg ) \
      if( !stat ) \
          { \
          Error( msg ); \
          return stat; \
          }

};
#endif
