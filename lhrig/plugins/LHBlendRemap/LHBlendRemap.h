#ifndef _RNKROLLNODE_H
#define _RNKROLLNODE_H

#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPlug.h>
#include <maya/MGlobal.h>
#include <math.h>


class LHBlendRemap : public MPxNode {
 public:
  LHBlendRemap() {};
  virtual MStatus compute( const MPlug& plug, MDataBlock& data );
  static void* creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aCachePlugs;
  static MObject aInVal;
  static MObject aRemapOne;
  static MObject aRemapNegOne;
  static MObject aPosOut;
  static MObject aNegOut;
  static MObject aInputs;
  static MObject aOutputs;
//  int cached = 0;

    inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[LHBlendRemap] " );
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
