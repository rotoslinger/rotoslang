#include "nullTransform.h"

MTypeId nullTMatrix::id(0x10886639);
nullTMatrix::nullTMatrix(){}
nullTMatrix::~nullTMatrix(){}
void* nullTMatrix::creator()  { return new nullTMatrix();}
MMatrix nullTMatrix::asMatrix() const { return MMatrix::identity; }
MMatrix nullTMatrix::asMatrix(double percent) const { return MMatrix::identity; }


MTypeId nullTransform::id(0x1084739);
nullTransform::nullTransform(){}
nullTransform::~nullTransform(){}
void* nullTransform::creator()  { return new nullTransform();}

MStatus nullTransform::initialize() {
    MStatus status ;
  return MS::kSuccess;
}

MPxTransformationMatrix* nullTransform::createTransformationMatrix() { return new nullTMatrix(); }


