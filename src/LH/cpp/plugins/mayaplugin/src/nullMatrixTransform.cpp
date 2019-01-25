#include "nullMatrixTransform.h"

// MPxTransformationMatrix implementation
MTypeId nullMatrixTMatrix::id(0x10856349);
nullMatrixTMatrix::nullMatrixTMatrix(){}
nullMatrixTMatrix::~nullMatrixTMatrix(){}
void* nullMatrixTMatrix::creator()  { return new nullMatrixTMatrix();}
MMatrix nullMatrixTMatrix::asMatrix() const
{
    // MPlug matrixPlug(thisMObject(), aInputMatrix);
    // MFnMatrixData matrixData(matrixPlug.asMObject());
    // MMatrix inMatrix = matrixData.matrix();
    // return inMatrix;

    return MMatrix::identity;
    // MMatrix mtx = ParentClass::asMatrix();
    // return mtx;

    }
MMatrix nullMatrixTMatrix::asMatrix(double percent)const
{
    // MPlug matrixPlug(thisMObject(), aInputMatrix);
    // MFnMatrixData matrixData(matrixPlug.asMObject());
    // MMatrix inMatrix = matrixData.matrix();
    // return inMatrix;
    // MMatrix mtx = ParentClass::asMatrix();
    // return mtx;

    return MMatrix::identity;
}

// MPxTransform implementation
MObject nullMatrixTransform::aInputMatrix;
MObject nullMatrixTransform::aOutputMatrix;
MTypeId nullMatrixTransform::id(69869866);
nullMatrixTransform::nullMatrixTransform(){}
nullMatrixTransform::~nullMatrixTransform(){}
void* nullMatrixTransform::creator()  { return new nullMatrixTransform();}

MStatus nullMatrixTransform::initialize() {
    MStatus status ;
    MFnMatrixAttribute mAttr;

    aInputMatrix = mAttr.create("inputMatrix", "inmatrix");
    mAttr.setWritable(true);
    mAttr.setConnectable(true);
    mAttr.setStorable(true);
    addAttribute( aInputMatrix );

    aOutputMatrix = mAttr.create("outputMatrix", "outmatrix");
    mAttr.setKeyable(false);
    mAttr.setWritable(true);
    mAttr.setConnectable(true);
    mAttr.setStorable(true);
    addAttribute( aOutputMatrix );
	attributeAffects( aInputMatrix, aOutputMatrix);
	attributeAffects( aInputMatrix, matrix);

    return MS::kSuccess;
}



MStatus nullMatrixTransform::validateAndSetValue(const MPlug& plug,
												const MDataHandle& handle,
												const MDGContext& context)
{
	MStatus status = MS::kSuccess;

	//	Make sure that there is something interesting to process.
	//
	if (plug.isNull())
		return MS::kFailure;
    MDataBlock block = forceCache(*(MDGContext *)&context);
    MDataHandle blockHandle = block.outputValue(plug, &status);	// MDataHandle blockHandle = block.outputValue(plug, &status);

    if( plug == nullMatrixTransform::aOutputMatrix)
    {
        inMatrix = handle.asMatrix();
        double sm[4][4];
        nullMatrixTransform::inMatrix.get(sm);
        MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[0][0] + sm[0][1] + sm[0][2] + sm[0][3]);
        MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[1][0] + sm[1][1] + sm[1][2] + sm[1][3]);
        MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[2][0] + sm[2][1] + sm[2][2] + sm[2][3]);
        MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[3][0] + sm[3][1] + sm[3][2] + sm[3][3]);
        MDataHandle outMatrixHandle = block.outputValue(nullMatrixTransform::matrix);
        blockHandle.set(inMatrix);
        blockHandle.setClean();
        dirtyMatrix();		
    }

	// Allow processing for other attributes
	return ParentClass::validateAndSetValue(plug, handle, context);
}



// MStatus nullMatrixTransform::compute( const MPlug& plug, MDataBlock& data)
// {
//     MStatus status;
//     if( plug == nullMatrixTransform::aOutputMatrix or plug == nullMatrixTransform::aOutputMatrix)
//     {
//         inMatrix = data.inputValue( nullMatrixTransform::aInputMatrix ).asMatrix();
//         double sm[4][4];
//         nullMatrixTransform::inMatrix.get(sm);
//         MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[0][0] + sm[0][1] + sm[0][2] + sm[0][3]);
//         MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[1][0] + sm[1][1] + sm[1][2] + sm[1][3]);
//         MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[2][0] + sm[2][1] + sm[2][2] + sm[2][3]);
//         MGlobal::displayInfo(MString("THIS IS THE MATRIX")+sm[3][0] + sm[3][1] + sm[3][2] + sm[3][3]);
//         MDataHandle outMatrixHandle = data.outputValue(nullMatrixTransform::matrix);
//         outMatrixHandle.set(inMatrix);
//         outMatrixHandle.setClean();
//     }
// }

MPxTransformationMatrix* nullMatrixTransform::createTransformationMatrix()
{
    // MPlug matrixPlug(thisMObject(), aInputMatrix);
    // MFnMatrixData matrixData(matrixPlug.asMObject());
    // MMatrix inMatrix = matrixData.matrix();
    //---For debugging the matrices
    return new MPxTransformationMatrix( inMatrix);
}


