// This is a template for the MPxNode
//====================================

#include "LHCurveTransform.h"

MTypeId LHCurveTransform::id(0x39765487);

//doubles
MObject LHCurveTransform::aBiasIn;
MObject LHCurveTransform::aBiasOut;

MObject LHCurveTransform::aCurve;

// MObject LHCurveTransform::aNumOutputs;

MObject LHCurveTransform::aMatrixInput;
MObject LHCurveTransform::aInputs;

MObject LHCurveTransform::aMatrixOutput;
MObject LHCurveTransform::aOutputs;
MObject LHCurveTransform::aInMat;
MObject LHCurveTransform::aOutMat;
// MObject LHCurveTransform::aOutMatrixArray;


MStatus LHCurveTransform::initialize() {
	MStatus status ;
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;
    MFnTypedAttribute tAttr;
    MFnCompoundAttribute cAttr;

    aBiasIn = nAttr.create( "biasIn", "binput", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setStorable(true);
    nAttr.setDefault(1.0);
    nAttr.setChannelBox(true);
    addAttribute( aBiasIn );



	aBiasOut = nAttr.create( "biasOut", "boutput", MFnNumericData::kFloat);
	/////////////////// KEYABLE MUST BE FALSE for attributeAffects to work on an output
    nAttr.setKeyable(false);
	/////////////////// KEYABLE MUST BE FALSE for attributeAffects to work on an output
    nAttr.setWritable(true);
    nAttr.setStorable(true);
	nAttr.setDefault(1.0);
	nAttr.setChannelBox(true);
	addAttribute( aBiasOut );


  // Inputs
  aInMat = mAttr.create("matIn", "matin");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
    mAttr.setKeyable(true);

  addAttribute( aInMat );

  aOutMat = mAttr.create("matOut", "matOut");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
    mAttr.setKeyable(false);

  addAttribute( aOutMat );



    // aOutMatrixArray = tAttr.create("outMatricies", "outmatricies", MFnNumericData::kMatrixArray);
    // tAttr.setKeyable(false);
    // tAttr.setArray(false);
    // tAttr.setUsesArrayDataBuilder(true);
    // addAttribute(aOutMatrixArray);

    // aNumOutputs = nAttr.create( "numOutputs", "numoutputs", MFnNumericData::kInt);
    // nAttr.setKeyable(false);
    // nAttr.setWritable(true);
    // nAttr.setStorable(true);
    // nAttr.setDefault(3);
    // nAttr.setChannelBox(true);
    // addAttribute( aNumOutputs );

// curve
  aCurve = tAttr.create("curve", "curve", MFnData::kNurbsCurve);
  addAttribute( aCurve );

  // Inputs
  aMatrixInput = mAttr.create("matrixIn", "matrixin");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
    mAttr.setKeyable(true);

  addAttribute( aMatrixInput );

  aInputs = cAttr.create("inputs", "inputs");
  cAttr.setKeyable(true);
  cAttr.setArray(true);
  cAttr.addChild( aMatrixInput );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aInputs);

  // Outputs
  aMatrixOutput = mAttr.create("matrixOut", "matrixout");
   addAttribute( aMatrixOutput );

  aOutputs = cAttr.create("outputs", "outputs");
  cAttr.setKeyable(false);
  cAttr.setArray(true);
  cAttr.addChild( aMatrixOutput );
  cAttr.setReadable(true);
  cAttr.setWritable(true);
  cAttr.setConnectable(true);
  cAttr.setChannelBox(true);
  addAttribute(aOutputs);



	attributeAffects( aBiasIn, aBiasOut);
	attributeAffects( aInputs, aOutputs);
	attributeAffects( aCurve, aOutputs);
	attributeAffects( aMatrixInput, aOutputs);
	attributeAffects( aMatrixInput, aMatrixOutput);
	attributeAffects( aInMat, aOutMat);




    
  return MS::kSuccess;
}


void* LHCurveTransform::creator() { return new LHCurveTransform; }

MStatus LHCurveTransform::compute( const MPlug& plug, MDataBlock& data )
{

    MStatus status;
    // if ( plug == aBiasOut ||  plug == aOutputs || plug == aMatrixOutput || plug == aOutMat)
    if ( plug == aMatrixOutput || plug == aOutMat)
    {


        MObject oCurve = data.inputValue(aCurve).asNurbsCurveTransformed();
        if (oCurve.isNull())
        {
            MGlobal::displayError(MString("Couldn't get curve, check connections"));
            return MS::kFailure;
        }
        fnCurve = new MFnNurbsCurve(oCurve);

        MMatrix mInMat = data.inputValue(aInMat).asMatrix();

            // MDataHandle testHandle = data.outputValue(aOutMat).asMatrix();

            // testHandle.set(temp);
            // testHandle.setClean();
            // data.setClean(plug);

        MDataHandle outMatrixHandle = data.outputValue(aOutMat);
        outMatrixHandle.set(mInMat);
        outMatrixHandle.setClean();
        data.setClean(plug);

        ////////////////////////////////////////////////////////////////////////////////
        MArrayDataHandle outputsArrayHandle(data.inputArrayValue( aOutputs, &status));
        MArrayDataHandle inputsArrayHandle(data.inputArrayValue( aInputs, &status));

        CheckStatusReturn( status, "Unable to get inputs" );
        unsigned int elemCount = inputsArrayHandle.elementCount(&status);

        // If not input, there will be no output
        if (!elemCount)
        {
            CheckStatusReturn( MS::kFailure, "No Inputs, add at least one matrix to the input matrix array" );
            return MS::kFailure;
        }
        outputCount = (float) elemCount;
        MMatrixArray finalMatrixArray;
        for (int i=0;i < elemCount;i++)
        {
            
            status = inputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to input element" );
            MDataHandle tempHandle(inputsArrayHandle.inputValue(&status) );
            CheckStatusReturn( status, "Couldn't get array handle" );
            MMatrix temp = tempHandle.child( aMatrixInput ).asMatrix();

            finalMatrixArray.append(tempHandle.child( aMatrixInput ).asMatrix());

            status = outputsArrayHandle.jumpToElement(i);
            CheckStatusReturn( status, "Unable to jump to output element" );
            currentIndex = (float)i;

            if (i == 0)
            {
                currentParameter = 0;
            }
            else if (i ==elemCount-1)
            {
                currentParameter = 1;
            }
            else 
            {
                currentParameter = (1.0 / outputCount) * currentIndex;
            }

            
            MGlobal::displayInfo (MString("PARAM") + " " + currentParameter + " OutputCount " +outputCount+ " CurrentIndex " +currentIndex );
            // composedMatrix = MMatrix::identity;

            MDataHandle handle = outputsArrayHandle.outputValue().child(aMatrixOutput);
            handle.set(temp);
            handle.setClean();
            data.setClean(plug);
        }

        //////////////////////////////////////////////////////////////////////////////////

    }
    else
    {
            return MS::kUnknownParameter;
    }
    return MS::kSuccess;
}


MStatus LHCurveTransform::computeMatricies(const MPlug& plug, MDataBlock& data, MFnNurbsCurve *fnCurve)
{
    MStatus status;
    MArrayDataHandle outputsArrayHandle(data.inputArrayValue( aOutputs, &status));
    MArrayDataHandle inputsArrayHandle(data.inputArrayValue( aInputs, &status));

    CheckStatusReturn( status, "Unable to get inputs" );
    unsigned int elemCount = inputsArrayHandle.elementCount(&status);

    // If not input, there will be no output
    if (!elemCount)
    {
        CheckStatusReturn( MS::kFailure, "No Inputs, add at least one matrix to the input matrix array" );
        return MS::kFailure;
    }

    outputCount = (float) elemCount;
    MMatrixArray finalMatrixArray;
    for (int i=0;i < elemCount;i++)
    {
        
        status = inputsArrayHandle.jumpToElement(i);
        CheckStatusReturn( status, "Unable to jump to input element" );
        MDataHandle tempHandle(inputsArrayHandle.inputValue(&status) );
        CheckStatusReturn( status, "Couldn't get array handle" );
        MMatrix temp = tempHandle.child( aMatrixInput ).asMatrix();

        finalMatrixArray.append(tempHandle.child( aMatrixInput ).asMatrix());

        status = outputsArrayHandle.jumpToElement(i);
        CheckStatusReturn( status, "Unable to jump to output element" );
        currentIndex = (float)i;

        if (i == 0)
        {
            currentParameter = 0;
        }
        else if (i ==elemCount-1)
        {
            currentParameter = 1;
        }
        else 
        {
            currentParameter = (1.0 / outputCount) * currentIndex;
        }

        
        MGlobal::displayInfo (MString("PARAM") + " " + currentParameter + " OutputCount " +outputCount+ " CurrentIndex " +currentIndex );
        composedMatrix = MMatrix::identity;


        MDataHandle handle = outputsArrayHandle.outputValue().child(aMatrixOutput);
        handle.set(temp);
        handle.setClean();
        data.setClean(plug);

    }
    ////////Set the final weights
    // MFnMatrixArrayData outputMatrixArrayFn;
    // MObject oOutputArray = outputMatrixArrayFn.create(finalMatrixArray);
    // MDataHandle handle = data.outputValue(aOutMatrixArray);
    // handle.setMObject(oOutputArray);

    // data.setClean(LHCurveTransform::aOutputs);
    return MS::kSuccess;
}

// MStatus LHCurveTransform::setDependentsDirty( MPlug const & inPlug,
//                                             MPlugArray  & affectedPlugs)
//     {
//         if ( (inPlug.attribute() != aInputs)
//         & (inPlug.attribute() != aCurve)
//         & (inPlug.attribute() != aBiasIn)
//         // & (inPlug.attribute() != aBiasOut)
//         & (inPlug.attribute() != aMatrixInput))
//         // & (inPlug.attribute() != aMatrixOutput))
//         {
//             return MS::kSuccess;
//         }
        
//         MPlug outArrayPlug(thisMObject(), aOutputs);
//         if (inPlug.isElement()) {
//             // First dirty the output output element first.
//             // Of course, dirty output element itself
//             MPlug elemPlug = outArrayPlug.elementByLogicalIndex(
//                                                 inPlug.logicalIndex());
//             affectedPlugs.append(elemPlug);

//             // We also need to dirty the parent.
//             //
//             affectedPlugs.append(outArrayPlug);
//         } else {
//             // Mark the parent output plug as dirty.
//             //
//             affectedPlugs.append(outArrayPlug);

//             // Also visit each element.
//             //
//             unsigned int i,n = outArrayPlug.numElements();
//             for (i = 0; i < n; i++) {
//                 MPlug elemPlug = outArrayPlug.elementByPhysicalIndex(i);
//                 affectedPlugs.append(elemPlug);
//             }
//         }
//         return MS::kSuccess;
//     }

// MMatrix ComposeMatrix(MVector rowX, MVector rowY, MVector rowZ, MPoint translation)
// {
//         double compMatrix[4][4]={{ rowX[0], rowX[1], rowX[2], 0.0},
//                                 { rowY[0], rowY[1], rowY[2], 0.0},
//                                 { rowZ[0], rowZ[1], rowZ[2], 0.0},
//                                 {translation.x, translation.y, translation.z, 1.0}};
//         MMatrix composedMatrix(compMatrix);
//         return composedMatrix;
// }

// void ComposeMatrixWithRotation(MPoint a, MPoint b, MPoint c, MPoint translation, MMatrix &composedMatrix)
// {
//     //////////////////////////////////////// Composing the rotation matrix ///////////////////////////////////////////////////////////////
//     // Composing in a right handed style (make a backward L with your right hand)
//     //      C
//     //      |
//     //   A--B
//     // A is the tip of the thumb
//     // B is the interdigital fold between thumb and forefinger
//     // C is the tip of the forefinger
//     // This will aim at the A-B vector
//     // Switch A and C to flip the aim axis (this will be done via script logic)
//     //      A
//     //      |
//     //   C--B
//     //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//     MVector rowZ = b - a ^ c-a;
//     MVector rowY =  rowZ ^ b - a;
//     MVector rowX = rowY ^ rowZ;
//     rowX.normalize();
//     rowY.normalize();
//     rowZ.normalize();
//     composedMatrix = ComposeMatrix(rowX, rowY, rowZ, translation);
// }

//---For debugging the matrices
//double sm[4][4];
//baseMatrix.get(sm);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[0][0] + sm[0][1] + sm[0][2] + sm[0][3]);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[1][0] + sm[1][1] + sm[1][2] + sm[1][3]);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[2][0] + sm[2][1] + sm[2][2] + sm[2][3]);
//MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[3][0] + sm[3][1] + sm[3][2] + sm[3][3]);

//MStatus MyLocator::initialize()
//{
//MRampAttribute rAttr;
//MFnEnumAttribute eAttr;
//MFnUnitAttribute uAttr;
//MFnTypedAttribute tAttr;
//MFnNumericAttribute nAttr;
//MFnMessageAttribute gAttr;
// 
//timeObj = uAttr.create( "time", "time", MFnUnitAttribute::kTime, 0.0 );
//addAttribute( timeObj );
// 
//angleObj = uAttr.create( "angle", "angle", MFnUnitAttribute::kAngle, 0.0 );
//addAttribute( angleObj );
// 
//boolObj = nAttr.create( "bool", "bool", MFnNumericData::kBoolean, false );
//addAttribute( boolObj );
// 
//intObj = nAttr.create( "int", "int", MFnNumericData::kInt, 0 );
//addAttribute( intObj );
// 
//floatObj = nAttr.create( "float", "float", MFnNumericData::kFloat, 0.f );
//addAttribute( floatObj );
// 
//doubleObj = nAttr.create( "double", "double", MFnNumericData::kDouble, 0.0 );
//addAttribute( doubleObj );
// 
//int2Obj = nAttr.create( "int2", "int2", MFnNumericData::k2Int, 0 );
//addAttribute( int2Obj );
// 
//int3Obj = nAttr.create( "int3", "int3", MFnNumericData::k3Int, 0 );
//addAttribute( int3Obj );
// 
//float2Obj = nAttr.create( "float2", "float2", MFnNumericData::k2Float, 0.f );
//addAttribute( float2Obj );
// 
//float3Obj = nAttr.create( "float3", "float3", MFnNumericData::k3Float, 0.f );
//addAttribute( float3Obj );
// 
//double2Obj = nAttr.create( "double2", "double2", MFnNumericData::k2Double, 0.0 );
//addAttribute( double2Obj );
// 
//double3Obj = nAttr.create( "double3", "double3", MFnNumericData::k3Double, 0.0 );
//addAttribute( double3Obj );
// 
//stringObj = tAttr.create( "string", "string", MFnData::kString, "abc" );
//addAttribute( stringObj );
// 
//matrixObj = tAttr.create( "matrix", "matrix", MFnMatrixAttribute::kDouble );
//addAttribute( matrixObj );
// 
//curveObj = tAttr.create( "curve", "curve", MFnData::kNurbsCurve );
//addAttribute( curveObj );
// 
//meshObj = tAttr.create( "mesh", "mesh", MFnData::kMesh );
//addAttribute( meshObj );
// 
//iaObj = tAttr.create( "iArray", "iArray", MFnData::kIntArray );
//addAttribute( iaObj );
// 
//faObj = tAttr.create( "fArray", "fArray", MFnData::kFloatArray );
//addAttribute( faObj );
// 
//daObj = tAttr.create( "dArray", "dArray", MFnData::kDoubleArray );
//addAttribute( daObj );
// 
//paObj = tAttr.create( "pArray", "pArray", MFnData::kPointArray );
//addAttribute( paObj );
// 
//vaObj = tAttr.create( "vArray", "vArray", MFnData::kVectorArray );
//addAttribute( vaObj );
// 
//saObj = tAttr.create( "sArray", "sArray", MFnData::kStringArray );
//addAttribute( saObj );
// 
//msgObj = gAttr.create( "message", "message" );
//addAttribute( msgObj );
// 
//clrObj = nAttr.createColor( "color", "color" );
//addAttribute( clrObj );
// 
//pntObj = nAttr.createPoint( "point", "point" );
//addAttribute( pntObj );
// 
//enumObj = eAttr.create( "enum", "enum" 0 );
//eAttr.addField( "A", 0 );
//eAttr.addField( "B", 0 );
//addAttribute( enumObj );
// 
//crvRmpObj = rAttr.createCurveRampAttr( "crvRamp", "crvRamp" );
//addAttribute( crvRmpObj );
// 
//clrRmpObj = rAttr.createColorRampAttr( "clrRamp", "clrRamp" );
//addAttribute( clrRmpObj );
// 
//fileNameObj = tAttr.create( "fileName", "fileName", MFnData::kString );
//tAttr.setUsedAsFilename( true );
//addAttribute( fileNameObj );
// 
//}
