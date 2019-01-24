#ifndef _NULLTRANSFORM_H
#define _NULLTRANSFORM_H
#define _MApiVersion

#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPlug.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MNurbsIntersector.h>
#include <maya/MFnGenericAttribute.h>
#include <maya/MPxTransform.h>
#include <maya/MPxTransformationMatrix.h>

#include <math.h>

class nullTransform : public MPxTransform {
 public:
    nullTransform();
    virtual ~nullTransform();
    // virtual MStatus compute( const MPlug& plug, MDataBlock& data );

    virtual MPxTransformationMatrix* createTransformationMatrix();

    static MTypeId id;
    static void* creator();
    static MStatus initialize();

    inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[nullTransform] " );
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

#endif
