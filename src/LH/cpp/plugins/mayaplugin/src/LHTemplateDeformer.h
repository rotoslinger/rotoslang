#ifndef LHTEMPLATEDEFORMER_H
#define LHTEMPLATEDEFORMER_H
#define _MApiVersion

#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>

#include <maya/MFnMesh.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MPxDeformerNode.h>

class LHTemplateDeformer : public MPxDeformerNode {
 public:
  LHTemplateDeformer() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  static void* creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aAmount;

  inline MString FormatError( const MString &msg, const MString
                                &sourceFile, const int &sourceLine )
  {
      MString txt( "[LHTemplateDeformer] " );
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
#endif
