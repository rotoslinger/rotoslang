#pragma once

#include <maya/MStatus.h>
#include <maya/MTypeId.h>
#include <maya/MMatrix.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MPxTransform.h>
#include <maya/MPxTransformationMatrix.h>
#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MPlugArray.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>


class nullTransform : public MPxTransform {
 public:
    nullTransform();
    virtual ~nullTransform();
    virtual MStatus compute( const MPlug& plug, MDataBlock& data );

    virtual MPxTransformationMatrix* createTransformationMatrix();
    // virtual MStatus setDependentsDirty( MPlug const & inPlug, MPlugArray  & affectedPlugs);
    // virtual void dirtyPlug(MPlug const & inPlug, MPlugArray  & affectedPlugs, MPlug outArrayPlug);
    virtual SchedulingType schedulingType() const { return kParallel; }

    static MTypeId id;
    static void* creator();
    static MStatus initialize();

    static MObject aSpeedTx;
    static MObject aSpeedTy;
    static MObject aSpeedTz;
    static MObject aSpeedT;
    static MObject aSpeedOutTx;
    static MObject aSpeedOutTy;
    static MObject aSpeedOutTz;
    static MObject aSpeedOutT;
};

///////////////////////////////////////////////////////////

class nullTMatrix : public MPxTransformationMatrix
{
    // A really simple implementation of MPxTransformationMatrix.
    // The methods include:
    // - Two accessor methods for getting and setting the 
    // rock
    // - The virtual asMatrix() method which passes the matrix 
    // back to Maya when the command "xform -q -ws -m" is invoked
    public:
        nullTMatrix();
        virtual ~nullTMatrix();
        static void *creator();
        MMatrix asMatrix() const override;
        MMatrix asMatrix(double percent) const override;
        static	MTypeId	id;
        
    protected:		
        typedef MPxTransformationMatrix ParentClass;
};
