#ifndef _LHSURFACEOUTPUTMANIP_H
#define _LHSURFACEOUTPUTMANIP_H
#include <maya/MCppCompat.h>

#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MMatrix.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MNurbsIntersector.h>

#include <maya/MPlug.h>
#include <maya/MGlobal.h>
#include <math.h>


class LHSurfaceOutputManip : public MPxNode {
 public:
  LHSurfaceOutputManip() {};
  virtual MStatus compute( const MPlug& plug, MDataBlock& data );
  static void* creator();
  static MStatus initialize();

  static MTypeId id;

//  static MObject aDistance;
//  static MObject aRadius;
//  static MObject aRotAmount;
//  static MObject aGlobalScale;
//  static MObject aRotation;
  static MObject aInputs;
  static MObject aOutputs;

  //Inputs
  static MObject aBaseTransform;
  static MObject aTransform;
  static MObject aTransformArray;
  static MObject aSurface;

  //Outputs
  static MObject aOutParamArray;
  static MObject aOutParamU;
  static MObject aOutParamV;





    inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[LHSurfaceOutputManip] " );
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

#endif
