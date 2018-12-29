#include "LHRepulsorDeformer.h"
#include <maya/MFnPlugin.h>

MTypeId LHRepulsorDeformer::id(0x00002398);
MObject LHRepulsorDeformer::aRepulsorMatrix;
MObject LHRepulsorDeformer::aRepulsorRadius;
MObject LHRepulsorDeformer::aInputs;
MObject LHRepulsorDeformer::aAmount;


void* LHRepulsorDeformer::creator() { return new LHRepulsorDeformer; }

MStatus LHRepulsorDeformer::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex)
   {
    MStatus status;

    // Get the envelope and blend weight
    MObject thisMObj( thisMObject() );
    MPlug geomPlug( thisMObj, input );
    float env = data.inputValue(envelope).asFloat();
    MArrayDataHandle geomArrayHandle = data.inputArrayValue(geomPlug);
    status = geomArrayHandle.jumpToElement( mIndex );
    CheckStatusReturn( status, "Unable to get current base geo" );


    MFloatArray radiusArray;
    MFloatArray worldScale;
    MMatrixArray matrixArray;
    MVectorArray worldPosition;
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( LHRepulsorDeformer::aInputs, &status));
    CheckStatusReturn( status, "Unable to get inputs" );
    MFloatArray amountArray;
    MFloatArray modBArray;
    unsigned int inputCount = inputsArrayHandle.elementCount(&status);
    CheckStatusReturn( status, "Unable to get number of rotates" );

    for (unsigned int i=0;i < inputCount;i++)
    {
        status = inputsArrayHandle.jumpToElement(i);
        float prescaleRadius = inputsArrayHandle.inputValue().child( LHRepulsorDeformer::aRepulsorRadius ).asFloat();
        amountArray.append(inputsArrayHandle.inputValue().child( LHRepulsorDeformer::aAmount ).asFloat());
        MMatrix tempMatrix = inputsArrayHandle.inputValue().child( LHRepulsorDeformer::aRepulsorMatrix ).asMatrix();
        MTransformationMatrix tMatrix(tempMatrix);
        worldPosition.append(tMatrix.getTranslation(MSpace::kWorld));
        matrixArray.append(tempMatrix);
        double scalr[3];
        status = tMatrix.getScale(scalr, MSpace::kWorld);
        worldScale.append((scalr[0] + scalr[1] + scalr[2])/3);
        MGlobal::displayInfo(MString("DEBUG:  UPDATING ") + scalr[0] + scalr[1] + scalr[2]);
        MGlobal::displayInfo(MString("DEBUG:  UPDATING ") + ((scalr[0] + scalr[1] + scalr[2])/3));
        radiusArray.append(prescaleRadius * (scalr[0] + scalr[1] + scalr[2])/3);

    }
    MDataHandle dhInput = geomArrayHandle.inputValue();
    MDataHandle dhWeightChild = dhInput.child( inputGeom );
    MItGeometry baseIter(dhWeightChild, true );
    MPointArray allBasePts;
    baseIter.allPositions(allBasePts, MSpace::kObject);
    MPoint pt;
    float w = 0.0f;
    int currentPoint =-1;
    for (; !itGeo.isDone(); itGeo.next())
    {
    // Get the input point
        pt = itGeo.position();
        currentPoint +=1;
//        int beenSet = 0;
        MPointArray avrPoint;
        for (unsigned int i=0;i < worldPosition.length();i++)
        {
            MVector dirVector = pt - worldPosition[i] ;
            float length = dirVector.length();
            if (length > radiusArray[i])
            {
                continue;
            }
            float directionalAlgorithm =( (radiusArray[i])/length - 1.0) * (amountArray[i] * (amountArray[i]/radiusArray[i]));
            pt = pt + dirVector *  directionalAlgorithm;


        }
//            pt = pt* matrixArray[i];

          itGeo.setPosition(pt);
    }

  return MS::kSuccess;
}

MStatus LHRepulsorDeformer::initialize() {
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;
    MFnCompoundAttribute cAttr;
    MFnGenericAttribute gAttr;



    aAmount = nAttr.create( "amount", "amt", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(1.0);
    nAttr.setChannelBox(true);
    addAttribute( aAmount );


  aRepulsorMatrix = mAttr.create("repulsorMatrix", "repulsorMatrix");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aRepulsorMatrix );

  aRepulsorRadius = nAttr.create("radius", "rad", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  addAttribute(aRepulsorRadius);


  aInputs = cAttr.create("Inputs", "inputs");
  cAttr.setKeyable(true);
  cAttr.setArray(true);
  cAttr.addChild( aRepulsorMatrix );
  cAttr.addChild( aRepulsorRadius );
  cAttr.addChild( aAmount );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aInputs);

  attributeAffects(aRepulsorRadius, outputGeom);
  attributeAffects(aRepulsorMatrix, outputGeom);
  attributeAffects(aInputs, outputGeom);
  attributeAffects(aAmount, outputGeom);


  // Make the deformer weights paintable
  MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer LHRepulsorDeformer weights;");

  return MS::kSuccess;
}
