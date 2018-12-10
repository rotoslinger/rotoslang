#ifndef _LHUVBLENDSHAPEDEFORMER_H
#define _LHUVBLENDSHAPEDEFORMER_H

#include <maya/MDataBlock.h>
#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MTimer.h>

#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MFloatMatrix.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnMesh.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MPointArray.h>
#include <maya/MFloatArray.h>
#include <maya/MMeshIntersector.h>

#include <maya/MFnTypedAttribute.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MThreadUtils.h>

class LHUVBlendshape : public MPxDeformerNode {
 public:
  LHUVBlendshape() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& MitGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  static void* creator();
  static MStatus initialize();
 
  static MTypeId id;
  // tAttrs
  static MObject aDriveMesh;
  static MObject aOutMesh;

  // nAttrs
  static MObject aBlendAmt;

  unsigned int idx;
  MPoint pt;
  float w;
  float2 uv;

  inline MString FormatError( const MString &msg, const MString
                                &sourceFile, const int &sourceLine )
  {
      MString txt( "[LHUVBlendshape] " );
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
