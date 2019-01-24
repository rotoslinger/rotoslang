#include "nullMatrixTransform.h"

MTypeId nullMatrixTMatrix::id(0x10886639);
nullMatrixTMatrix::nullMatrixTMatrix(){}
nullMatrixTMatrix::~nullMatrixTMatrix(){}
void* nullMatrixTMatrix::creator()  { return new nullMatrixTMatrix();}
MMatrix nullMatrixTMatrix::asMatrix() const { return MMatrix::identity; }
MMatrix nullMatrixTMatrix::asMatrix(double percent) const { return MMatrix::identity; }


MTypeId nullMatrixTransform::id(0x1084739);
nullMatrixTransform::nullMatrixTransform(){}
nullMatrixTransform::~nullMatrixTransform(){}
void* nullMatrixTransform::creator()  { return new nullMatrixTransform();}

MStatus nullMatrixTransform::initialize() {
    MStatus status ;
  return MS::kSuccess;
}

MPxTransformationMatrix* nullMatrixTransform::createTransformationMatrix() { return new nullMatrixTMatrix(); }


