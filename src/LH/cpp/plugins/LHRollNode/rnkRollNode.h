#ifndef _RNKROLLNODE_H
#define _RNKROLLNODE_H
#include <maya/MCppCompat.h>

#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnMatrixAttribute.h>

#include <maya/MArrayDataHandle.h>

#include <maya/MPlug.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFnDependencyNode.h>

#include <math.h>


class rnkRollNode : public MPxNode {
 public:
  rnkRollNode() {};
  virtual MStatus compute( const MPlug& plug, MDataBlock& data );
  static void* creator();
  static MStatus initialize();

  static MTypeId id;

  static MObject aDistance;
  static MObject aRadius;
  static MObject aRotAmount;
  static MObject aGlobalScale;
  static MObject aRotation;
  static MObject aInputs;
  static MObject aOutputs;
  static MObject aParamU;
  static MObject aParamV;

  static MObject aMatrix;
  static MObject aBaseMatrix;

  inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[rnkRollNode] " );
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
