#ifndef LHMULTICLUSTER_H
#define LHMULTICLUSTER_H

#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>
#include <maya/MStatus.h>
#include <maya/MMatrixArray.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>

#include <maya/MPxDeformerNode.h>

class LHMultiCluster : public MPxDeformerNode {
 public:
  LHMultiCluster() {};
  virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                         const MMatrix &localToWorldMatrix, unsigned int mIndex);
  static void* creator();
  static MStatus initialize();

  static MTypeId id;
  static MObject aInputs;
  static MObject aMatrix;
  inline MString FormatError( const MString &msg, const MString
                                &sourceFile, const int &sourceLine )
  {
      MString txt( "[LHMultiCluster] " );
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
