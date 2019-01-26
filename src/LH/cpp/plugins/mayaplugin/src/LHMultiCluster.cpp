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

#include "LHMultiCluster.h"

MTypeId LHMultiCluster::id(0x00328467);
MObject LHMultiCluster::aInputs;
MObject LHMultiCluster::aMatrix;

MStatus LHMultiCluster::initialize() {

  MFnMatrixAttribute mAttr;
  MFnCompoundAttribute cAttr;

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
  MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer LHMultiCluster weights;");

  return MS::kSuccess;
}

void* LHMultiCluster::creator() { return new LHMultiCluster; }

MStatus LHMultiCluster::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MStatus status;

  float env = data.inputValue(envelope).asFloat();
  if (env<=0.0)
  {
	  return MS::kSuccess;

  }
  MMatrixArray matrixArray;
  MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHMultiCluster::aInputs, &status));
  CheckStatusReturn( status, "Unable to get inputs" );
  unsigned int inputCount = inputsArrayHandle.elementCount(&status);
  CheckStatusReturn( status, "Unable to get number of inputs" );
  MMatrix tempMatrix;
  for (unsigned int i=0;i < inputCount;i++)
  {
      status = inputsArrayHandle.jumpToElement(i);
      matrixArray.append(inputsArrayHandle.inputValue().child( LHMultiCluster::aMatrix ).asMatrix());

  }
  int nPlugs = matrixArray.length();
  MPoint pt;
  MPointArray allPoints;
  for (; !itGeo.isDone(); itGeo.next())
  {
	  pt = itGeo.position();
      for (unsigned int i=0;i < nPlugs;i++)
      {
          pt = pt * matrixArray[i];
      }
      allPoints.append(pt);
      //itGeo.setPosition(pt);
  }
  itGeo.setAllPositions(allPoints);
  return MS::kSuccess;
}

//---For debugging the matrices
//double sm[4][4];
//baseMatrix.get(sm);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[0][0] + sm[0][1] + sm[0][2] + sm[0][3]);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[1][0] + sm[1][1] + sm[1][2] + sm[1][3]);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[2][0] + sm[2][1] + sm[2][2] + sm[2][3]);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[3][0] + sm[3][1] + sm[3][2] + sm[3][3]);
