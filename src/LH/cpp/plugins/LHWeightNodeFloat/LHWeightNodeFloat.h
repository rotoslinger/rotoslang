#ifndef _LHWEIGHTNODE_H
#define _LHWEIGHTNODE_H
#define _MApiVersion

#include <maya/MCppCompat.h>

#include <string.h>
#include <maya/MIOStream.h>
#include <math.h>

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnEnumAttribute.h>

#include <maya/MFnPlugin.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MGlobal.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnFloatArrayData.h>
#include <maya/MPlugArray.h>
#include <maya/MString.h>
#include <maya/MFloatArray.h>


#include <math.h>

#define McheckErr(stat,msg)             \
        if ( MS::kSuccess != stat ) {   \
                cerr << msg;            \
                return MS::kFailure;    \
        }

class LHWeightNodeFloat : public MPxNode {
 public:
  LHWeightNodeFloat() {};
  virtual MStatus compute( const MPlug& plug, MDataBlock& data );
  virtual MStatus setDependentsDirty(MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs);

  virtual MStatus multiplyKFloatArrayByVal(MFloatArray &rFloatArray,
                                         double val);
  virtual MFloatArray floatArrayMathOperation(MFloatArray floatArray1,
                                                MFloatArray floatArray2,
                                                short operation);
  static void* creator();
  static MStatus initialize();

  static MTypeId id;

  static  MObject         aInputWeights;
  static  MObject         aFactor;
  static  MObject         aOperation;
  static  MObject         aInputs;

  static  MObject         aOutputWeights;
  static  MObject         aWeightList;


  inline MString FormatError( const MString &msg, const MString
                                  &sourceFile, const int &sourceLine )
    {
        MString txt( "[LHWeightNodeFloat] " );
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





