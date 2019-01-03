#ifndef LHCOLLISIONEFORMER_H
#define LHCOLLISIONEFORMER_H
#define _MApiVersion

#include <maya/MCppCompat.h>
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
#include <maya/MFnCompoundAttribute.h>
#include <maya/MBoundingBox.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MMeshIntersector.h>
#include <maya/MFloatPointArray.h>
#include <maya/MRampAttribute.h>

#include <maya/MFnGenericAttribute.h>
#include <vector>

class LHCollisionDeformer : public MPxDeformerNode {
    public:
        LHCollisionDeformer() {};
        virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                                const MMatrix &localToWorldMatrix, unsigned int mIndex);
        virtual MBoundingBox getBoundingBox(MDataBlock& data, MObject worldMatrix, MObject oMinBB, MObject oMaxBB);
        virtual MBoundingBox getBoundingBoxMultiple(MDataBlock& data, MObject worldMatrix, MObject oMinBB, MObject oMaxBB,
                                                    unsigned int index, MObject oCompound);
        virtual MPoint getBulge(int numColPoints, MPoint currPoint, MPoint closestPoint, double bulgeAmount, double bulgeDistance,
                                MVector vRay, MMatrix bBMatrix, double maxDisp, MRampAttribute curveAttribute);
        // virtual MPoint getBulge(MPoint currPoint, MMatrix mainMatrix);
        static void* creator();
        static MStatus initialize();

        static MTypeId id;
        static MObject aBulgeAmount;
        static MObject aBulgeDistance;
        static MObject aInputGeo;
        static MObject aInputs;

        static MObject aMainBBoxMinX;
        static MObject aMainBBoxMinY;
        static MObject aMainBBoxMinZ;
        static MObject aMainBBoxMaxX;
        static MObject aMainBBoxMaxY;
        static MObject aMainBBoxMaxZ;

        static MObject aMainBBMin;
        static MObject aMainBBMax;

        static MObject aMainWorldMatrix;

        static MObject aColBBoxMinX;
        static MObject aColBBoxMinY;
        static MObject aColBBoxMinZ;
        static MObject aColBBoxMaxX;
        static MObject aColBBoxMaxY;
        static MObject aColBBoxMaxZ;

        static MObject aColBBMin;
        static MObject aColBBMax;

        static MObject aColWorldMatrix;
        static MObject aFalloffRamp;


        bool hit;
        unsigned int i;
        unsigned int x;
        unsigned int numPoints;
        unsigned int numHits;
        MObject oTestMesh;
        MObject oMainMesh;
        MBoundingBox mainBounds;
        MBoundingBox testBounds;
        const MBoundingBox tmpBB;
        MVector vRay;
        MPoint xformPoint;
        MPoint closestPoint;
        MPoint clearPoint;
        MPoint finalPoint;
        //  MFloatPoint closestPoint;
        MPointOnMesh closestPointOn;
        //Bounds attrs
        MMatrix bBMatrix;
        //  MPoint minBBPoint;
        //  MPoint maxBBPoint;
        //  MBoundingBox mainBB;
        
        MBoundingBox mainBB;
        double distance;
        MPoint pDistance;        

        bool intersects;
        //MFnMesh mTestMesh;


        inline MString FormatError( const MString &msg, const MString
                                        &sourceFile, const int &sourceLine )
        {
            MString txt( "[LHCollisionDeformer] " );
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
