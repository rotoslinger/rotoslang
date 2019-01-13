#ifndef LHCOLLISIONEFORMER_H
#define LHCOLLISIONEFORMER_H
#define _MApiVersion
#define NOMINMAX
// #include <maya/MCppCompat.h>
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
#include <maya/MMatrixArray.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MPlugArray.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MThreadPool.h>
#include <maya/MTimer.h>
#include <maya/MFnNurbsCurve.h>

#include <maya/MFnGenericAttribute.h>
#include <iostream>
#include <algorithm>
#include <set>
#include <math.h>
#include <vector>
 
#include <stdio.h>

// #include "tbb/blocked_range.h"


struct ThreadData
{
	int numTasks;
	int currThreadNum;
};




struct CapsuleData
{
    unsigned int numCapsules;
	MPointArray pPointAArray;
	MPointArray pPointBArray;
    MDoubleArray dRadiusAArray;
    MDoubleArray dRadiusBArray;
    std::vector <short> eTypeArray;
    MIntArray allowScaleArray;
    MMatrixArray mWorldMatrixArray;
    // std::vector <MDoubleArray> colWeights;
    // std::vector <MDoubleArray> bulgeWeights;

    std::vector <std::vector <MDoubleArray>> colWeights;
    std::vector <std::vector <MDoubleArray>> bulgeWeights;
};


struct matrixSpaceTaskData
{
	MMatrix wSpaceMatrix;
	MIntArray finalIndexArray;
	MPointArray finalPoints;
	MPointArray finalPointArray;
    MPointArray allPoints;
    ThreadData threadData;
};

struct bulgeTaskData
{
    MObjectArray oColMeshArray;
    unsigned int colMeshIndex;
    unsigned int numPoints;
    MIntArray hitArray;
    MIntArray flipRayArray;
    MPointArray allPoints;
    MVectorArray vertexNormalArray;
    double maxDisp;
    double bulgeDistance;
    MRampAttribute rInnerFalloffRamp;
    double bulgeAmount;
    MPointArray flipPointArray;
    MRampAttribute rFalloffRamp;
    MRampAttribute rBlendBulgeCollisionRamp;
    unsigned int mIndex;
	int numTasks;
	int currThreadNum;
	MPointArray finalPointArray;
	MIntArray finalIndexArray;
};

class LHCollisionDeformer : public MPxDeformerNode {
    public:
        LHCollisionDeformer() {};
        void postConstructor();

        virtual MStatus deform(MDataBlock& data, MItGeometry& itGeo,
                                const MMatrix &localToWorldMatrix, unsigned int mIndex);
        virtual MBoundingBox getBoundingBox(MDataBlock& data, MMatrix worldMatrix, MObject oMinBB, MObject oMaxBB, MArrayDataHandle mainArrayHandle, unsigned int index);
        virtual MBoundingBox getBoundingBoxMultiple(MDataBlock& data, MMatrix &colWorldMatrix, MObject oMinBB, MObject oMaxBB,
                                                    unsigned int index, MObject oCompound);
        virtual MPoint getBulge(MPoint currPoint, MPoint closestPoint, double bulgeAmount, double bulgeDistance,
                                MVector vRay, double maxDisp, MRampAttribute curveAttribute, double bulgeWeight);
        virtual void seperateBulgeAndCollisionSerial(MObjectArray oColMeshArray, unsigned int colMeshIndex, unsigned int numPoints, MIntArray hitArray,  MIntArray flipRayArray,
                                               MPointArray &allPoints, MVectorArray vertexNormalArray,double maxDisp, double bulgeDistance, MRampAttribute rInnerFalloffRamp, double bulgeAmount,
                                               MPointArray flipPointArray, MRampAttribute rFalloffRamp, short algorithm, unsigned int mIndex);
        virtual void BlendBulgeAndCollisionSerial(MObjectArray oColMeshArray, unsigned int colMeshIndex, unsigned int numPoints, MIntArray hitArray,  MIntArray flipRayArray,
                                               MPointArray &allPoints, MVectorArray vertexNormalArray,double maxDisp, double bulgeDistance, MRampAttribute rInnerFalloffRamp, double bulgeAmount,
                                               MPointArray flipPointArray, MRampAttribute rFalloffRamp, MRampAttribute rBlendBulgeCollisionRamp, unsigned int mIndex);
        MPoint CollisionFlipCheckSerial(MPointArray allPoints, unsigned int pointIdx,  double bulgeDistance, double bulgeAmount, MVectorArray vertexNormalArray, double &maxDisp,
                                        MPointArray flipPointArray, MRampAttribute rInnerFalloffRamp);
        MPoint CollisionCheapSerial(MPointArray allPoints, unsigned int pointIdx, double &maxDisp);
        MPoint PerformBulgeSerial(MVectorArray vertexNormalArray, unsigned int pointIdx, MPointArray allPoints, double bulgeAmount, double bulgeDistance,
                                  double maxDisp, MRampAttribute rFalloffRamp);
        virtual MStatus RetrieveWeightsForAllIndicies(MObject weightsParent, MObject weights, int numIndex, std::vector<MDoubleArray> &weightsArray,
                                                      MPlug inPlug, MDataBlock &data);
        virtual void sphereDeformScaledSingle(MPointArray &allPoints, MItGeometry itGeo, MMatrix bBMatrix, MFnMesh *newMainMesh, double bulgeAmount,
                                   double bulgeDistance, MRampAttribute rFalloffRamp, std::vector <MPointArray> &allPointsArray);
        virtual MPoint getClosestPointOnSphereImplicit(MPoint testPoint, MPoint capsuleCenter, double radius);
        virtual MPoint transformPointByClosestPointDistanceScaled(MPoint closestPoint, MPoint currentPoint,unsigned int currentPointIndex, MFnMesh *newMainMesh, MMatrix mCapsuleMatrix, double distance);
        virtual MStatus getIntersectionData(MPoint &currPnt, MPoint bbMin, MPoint bbMax, MFnMesh *fnColMesh, MMeshIsectAccelParams &mmAccelParams,
                                            MPoint initPoint, MIntArray &hitArray, MIntArray &flipRayArray, MPointArray &flipPointArray);
        virtual MPoint getBulgeCapsuleScaled(MPoint currPoint, MPoint closestPoint, double bulgeAmount,
                                       double bulgeDistance, MVector vRay, double maxDisp, MRampAttribute rFalloffRamp,
                                       double bulgeWeight, MMatrix mCapsuleMatrix);
        MStatus getCapsuleData(MDataBlock& data, CapsuleData &rCapsuleData);
        void perPolyDeformation(MPointArray &allPoints, MMatrixArray colMatrices, MObjectArray oColMeshArray, MFnMesh *fnMainMesh,
                                double bulgeDistance, double bulgeAmount, MRampAttribute rInnerFalloffRamp,
                                MRampAttribute rFalloffRamp, MRampAttribute rBlendBulgeCollisionRamp, MItGeometry itGeo, MMatrix bBMatrix);
        void primitiveCollision(MPointArray &allPoints, MFnMesh *newMainMesh, double bulgeAmount, double bulgeDistance,
                                MRampAttribute rFalloffRamp, MMatrix bBMatrix);
        MStatus getCapsuleWeights(MDataBlock& data, std::vector<MDoubleArray> &rColWeights,
                                               std::vector<MDoubleArray> &rBulgeWeights, MArrayDataHandle inputsArrayHandle);
        // virtual void BlendBulgeAndCollisionParallel(MObjectArray oColMeshArray, unsigned int colMeshIndex, unsigned int numPoints, MIntArray hitArray, MIntArray flipRayArray,
        //                                                MPointArray &allPoints, MVectorArray vertexNormalArray, double maxDisp, double bulgeDistance, MRampAttribute rInnerFalloffRamp, double bulgeAmount,
        //                                                MPointArray flipPointArray, MRampAttribute rFalloffRamp, MRampAttribute rBlendBulgeCollisionRamp, unsigned int mIndex, unsigned int numTasks);
        // static void DecomposeBlendBulgeAndCollision(void *data, MThreadRootTask *root);
        // static MThreadRetVal BlendBulgeAndCollisionLoop(void *data);
        // virtual void testIntersector( const tbb::blocked_range<size_t> & r );
        void sphereCapsuleCollision(unsigned int capsuleIdx, MPointArray &allPoints, MFnMesh *newMainMesh, double bulgeAmount, double bulgeDistance,
                                                 MRampAttribute rFalloffRamp);

        MPoint transformPointByClosestPointDistance(MPoint closestPoint, MPoint currentPoint,unsigned int currentPointIndex, MFnMesh *newMainMesh, double distance);
        MPoint getSphereCapsuleBulge(MPoint currPoint, MPoint closestPoint, double bulgeAmount,
                                     double bulgeDistance, MVector vRay, double maxDisp, MRampAttribute rFalloffRamp, double bulgeWeight);

        void cubeCapsuleCollision(unsigned int capsuleIdx, MPointArray &allPoints, MFnMesh *newMainMesh, double bulgeAmount, double bulgeDistance,
                                                            MRampAttribute rFalloffRamp);             
        void capsuleDeformation(unsigned int capsuleIdx, MPointArray &allPoints, MFnMesh *newMainMesh, double bulgeAmount, double bulgeDistance,
                            MRampAttribute rFalloffRamp, MMatrix bBMatrix);

        void sphereClosestPointLogic(MPoint &offsetPoint, MPointArray &allPoints, unsigned int currentIdx, MPoint capsuleCenter,
                                     double capsuleRadius, MFnMesh *newMainMesh, MIntArray &hitArray, bool &capsuleHit, double collisionWeight);
        void sphereBulgeLogic(MPointArray &allPoints, unsigned int currentIdx, MPoint capsuleCenter, double capsuleRadiusA, MFnMesh *newMainMesh, double bulgeDistance,
                              double bulgeAmount, MRampAttribute rFalloffRamp, double bulgeWeight);
        void cubeClosestPointLogic(MPoint &offsetPoint, MPointArray &allPoints, unsigned int currentIdx, MPoint capsuleCenter,
                                                        double capsuleRadiusA, MFnMesh *newMainMesh, MIntArray &hitArray, bool &capsuleHit,
                                                        double collisionWeight, MPointArray framePoints, MVectorArray boundsData, MMatrix capsuleWorldMatrix, MMatrix bBMatrix);
        MPoint getClosestPointOnCubeImplicit(MPoint checkPoint, MPointArray framePoints, MMatrix capsuleWorldMatrix);



        void cylinderPointLogic(MPoint &offsetPoint, MPointArray &allPoints, unsigned int currentIdx, MPoint capsuleCenter, MPoint capsuleEnd,
                                                        double capsuleRadiusA, MFnMesh *newMainMesh, MIntArray &hitArray, bool &capsuleHit,
                                                        double collisionWeight, MPointArray framePoints, MVectorArray boundsData, MMatrix capsuleWorldMatrix,
                                                        MMatrix bBMatrix, double distanceBetweenPoints, MPoint capsuleFromToVec);

        void cylinderBulgeLogic(MPoint &offsetPoint, MPointArray &allPoints, unsigned int currentIdx, MPoint capsuleCenter,
                                                        MPoint capsuleEnd,
                                                        double capsuleRadiusA, MFnMesh *newMainMesh, MIntArray &hitArray, bool &capsuleHit,
                                                        double collisionWeight, MPointArray framePoints, MVectorArray boundsData, MMatrix capsuleWorldMatrix,
                                                        MMatrix bBMatrix, double distanceBetweenPoints, MPoint capsuleFromToVec,double bulgeDistance, double bulgeAmount, MRampAttribute rFalloffRamp);

        static void *creator();
        static MStatus initialize();

        static MTypeId id;
        static MObject aBulgeAmount;
        static MObject aBulgeDistance;
        static MObject aColGeo;
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

        static MObject aPermanent;
        static MObject aFlipCheck;
        static MObject aInnerFalloffRamp;

        static MObject aBlendBulgeCollision;
        static MObject aBlendBulgeCollisionRamp;
        static MObject aAlgorithm;

        static MObject aCollisionWeights;
        static MObject aBulgeWeights;
        static MObject aWeightsParent;
        static MObject aCacheWeights;

        static MObject aNumTasks;
        static MObject aMultiThread;
        static MObject aMainInputs;
        static MObject aGrainSize;
        // static MObject aAllowCapsule;
        static MObject tmpCapsuleCurve;
        static MObject tmpCapsuleRadius;
        static MObject tmpCapsuleMatrix;
        static MObject tmpCapsuleAllowScale;

        static MObject aPrimCapsuleCurve;
        static MObject aPrimCapsuleType;
        static MObject aPrimCapsuleRadiusA;
        static MObject aPrimCapsuleRadiusB;
        static MObject aPrimCapsuleMatrix;
        static MObject aPrimCapsuleAllowScale;
        static MObject aPrimCollisionInputs;
        // static MObject aAllowPerPoly;
        static MObject aDefType;
        static MObject aPrimCollisionWeights;
        static MObject aPrimBulgeWeights;
        static MObject aPrimWeightsParent;

        unsigned int inputCount;

        double flipCheck;
        MVector closestNormal;

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
        MMatrix colMatrix;
        //  MPoint minBBPoint;
        //  MPoint maxBBPoint;
        //  MBoundingBox mainBB;
    
        MBoundingBox mainBB;
        double distance;
        MPoint pDistance;

        bool intersects;
        double maxDisp;
        double testDist;
        bool isInBBox;
  	    MPointArray allColPoints;
        MPointArray allPoints;
        MVector polyNormal;
        MPoint interPoint;
        MMeshIntersector fnMeshIntersector;
        MPoint collisionPoint;
        MPoint bulgePoint;
        MPoint blendPoint;
        MPoint rClosestPoint;

        MIntArray indices;
        unsigned int indicesLength;
        double relativeDistance;
        float value;
        float w;
        std::vector<int> indexIntArray;
        int numIndex;
        unsigned int iterGeoCount;
        MDoubleArray rWeights;
        MDoubleArray dummyWeights;
        unsigned int currentMIndex;
        std::vector <MDoubleArray> bulgeWeightsArray;
        std::vector <MDoubleArray> collisionWeightsArray;
        double bulgeWeight;
        double collisionWeight;
        MPoint collisionWeightPoint;
        std::vector <MPointArray> allPointsArray;
        MPointArray countTest;

        int iGrainSize;
        int iMultiThread;
        int iCapsule;
        MObject oCapsuleCurve;
        MPointArray capsuleCurvePoints;
        double oCapsuleRadius;
        MVector capsuleSurfaceDirection;
        short eAlgorithm;
        MPoint capsulePoint;
        double dispCheck;
        MIntArray hitFaceIdArray;
        MMatrix mCapsuleMatrix;
        double matScaleArray[3];
        double averagedScale;
        double averagedInverseScale;
        MVector skewedDistance;
        int iAllowScale;
        int iPermanent;
        bool permanentChanged;
        MPoint transformedPoint;
        MPoint offsetPoint;
        double distanceToCenter;
        bool capsuleHit;
        double bulgeAmountScaled;
        CapsuleData capsuleData;
        std::vector <std::vector <MDoubleArray>> colWeights;
        std::vector <std::vector <MDoubleArray>> bulgeWeights;
        unsigned int weightsCount;
        MVector pointAsVector;

        double distanceA;
        double distanceB;
        double X;
        double Y;
        double Z;
        double distanceToFirst;
        double halfRadius;
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

    inline MStatus getPlugWeightValues(MObject &weightParent,MObject &weightChild,
                                           int MitGeoCount, int mIndex,
                                           MDoubleArray &returnWeightlist)
    {
        MStatus status;

        returnWeightlist.setLength(MitGeoCount) ;

        MObject thisNode = thisMObject();
        MPlug parent( thisNode, weightParent) ;
        double weight;
        MPlug parentElement = parent.elementByLogicalIndex(mIndex, &status);
        CheckStatusReturn( status, "Unable to get unable to get parentElement" );

        MPlug child = parentElement.child(weightChild, &status);
        CheckStatusReturn( status, "Unable to get unable to get child" );

        for (unsigned int i = 0; i < MitGeoCount; ++i)
        {
            MPlug childWeight = child.elementByLogicalIndex(i);
            status = childWeight.getValue(weight);
            if (status != MS::kSuccess)
            {
                returnWeightlist[i] = 1.0 ;
             }
            else
            {
                returnWeightlist[i] = weight;
            }
        }
        return status;
    }
    void convertMVectorToMPoint(MVector vec, MPoint &pnt)
    {
            pnt.x = vec.x;
            pnt.y = vec.y;
            pnt.z = vec.z;
    }
    void convertMPointToMVector(MPoint pnt, MVector &vec)
    {
            vec.x = pnt.x;
            vec.y = pnt.y;
            vec.z = pnt.z;
    }

    MPointArray closestPointTest(MPointArray testPoints, MMeshIntersector* meshIntersector)
    {
    MPointArray rPoints;
    MPointOnMesh ptOn;
    MPoint closestPoint;
    for (unsigned int x = 0; x < 1; x++)
    {
        meshIntersector->getClosestPoint(testPoints[x], ptOn);
        rPoints.append(ptOn.getPoint());
    }
    return rPoints;
    }

    void getMaxDisplacement(MPoint pPointFrom, MPoint pPointTo, double &dCheckVal, double &currMaxVal)
    {
        dCheckVal = pPointFrom.distanceTo(pPointTo);
        if (dCheckVal > currMaxVal)
        {
            currMaxVal = dCheckVal;
        }
    }
};
#endif
