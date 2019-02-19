#pragma once
#include "formatErrorMacros.h"
#include <maya/MStatus.h>
#include <maya/MTypeId.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MMatrix.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MPxTransform.h>
#include <maya/MPxTransformationMatrix.h>
#include <maya/MFnMatrixData.h>
#include <maya/MDataBlock.h>


class nullMatrixTransform : public MPxTransform {
    public:
        nullMatrixTransform();
        virtual ~nullMatrixTransform();
        // virtual MStatus compute( const MPlug& plug, MDataBlock& data );

        virtual MPxTransformationMatrix* createTransformationMatrix();
        virtual MStatus validateAndSetValue(const MPlug& plug,
                    const MDataHandle& handle, const MDGContext& context);

        static MTypeId id;
        static void* creator();
        static MStatus initialize();
        static MObject aInputMatrix;
        static MObject aOutputMatrix;
        MMatrix inMatrix;

        
        inline MString FormatError( const MString &msg, const MString
                                    &sourceFile, const int &sourceLine )
        {
            MString txt( "[nullMatrixTransform] " );
            txt += msg ;
            txt += ", File: ";
            txt += sourceFile;
            txt += " Line: ";
            txt += sourceLine;
            return txt;
        }

    protected:
		// Degrees
		typedef MPxTransform ParentClass;



};

///////////////////////////////////////////////////////////

class nullMatrixTMatrix : public MPxTransformationMatrix
{
    // A really simple implementation of MPxTransformationMatrix.
    // The methods include:
    // - Two accessor methods for getting and setting the 
    // rock
    // - The virtual asMatrix() method which passes the matrix 
    // back to Maya when the command "xform -q -ws -m" is invoked
    public:
        nullMatrixTMatrix();
        virtual ~nullMatrixTMatrix();
        static void *creator();
        MMatrix asMatrix() const override;
        MMatrix asMatrix(double percent) const override;
        static	MTypeId	id;
    protected:		
        typedef MPxTransformationMatrix ParentClass;
};

