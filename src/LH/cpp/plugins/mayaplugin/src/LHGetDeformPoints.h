#ifndef _LHGETDEFORMPOINTS_H
#define _LHGETDEFORMPOINTS_H

#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPlug.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnGenericAttribute.h>
#include <maya/MPlugArray.h>
#include <maya/MItGeometry.h>
#include <maya/MFnPointArrayData.h>
#include <maya/MPointArray.h>

#include <math.h>


class LHGetDeformPoints : public MPxNode {
 public:
  LHGetDeformPoints() {};
  virtual MStatus compute( const MPlug& plug, MDataBlock& data );
  static void* creator();
  static MStatus initialize();
  virtual MStatus setDependentsDirty(MPlug const & inPlug,
                                            MPlugArray  & affectedPlugs);

  static MTypeId id;

  static MObject aInputGeo;
  static MObject aInputGeoArray;
  static MObject aOutPoints;
  static MObject aOutPointArray;

  static MObject aBiasIn;
  static MObject aBiasOut;

	inline MString FormatError( const MString &msg, const MString
								  &sourceFile, const int &sourceLine )
	{
		MString txt( "[LHGetDeformPoints] " );
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
