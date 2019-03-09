#pragma once
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
	MMatrixArray matrixArrayBase;
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
