#pragma once

// #include <AL_MTypeId.h>
#include <maya/MPxNode.h>
#include <maya/MTypeId.h>
#include <maya/MDrawRegistry.h>
#include <maya/MPxDrawOverride.h>
#include <maya/MUserData.h>
#include <maya/MPxLocatorNode.h>
#include <maya/MUIDrawManager.h>
#include <maya/MPointArray.h>
#include <maya/MAngle.h>
#include <maya/MEulerRotation.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MDoubleArray.h>
#include <maya/MPointArray.h>
#include <maya/MPoint.h>
#include <maya/MMatrix.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MHWGeometryUtilities.h>
#include <maya/MGlobal.h>
#include <maya/MFnMatrixData.h>

// #include "../utils.h"

// using namespace MHWRender;

class LHCollisionLocator : public MPxLocatorNode
{
  public:
    LHCollisionLocator();
    virtual ~LHCollisionLocator();
    static void *creator();
    static MStatus initialize();
    virtual bool isBounded() const;
    virtual MBoundingBox boundingBox() const;
    virtual void draw(M3dView &view, const MDagPath &path,
                      M3dView::DisplayStyle style,
                      M3dView::DisplayStatus status);

  public:
    static MTypeId id;
    static MString drawDbClassification;
    static MString drawRegistrantId;
    static MObject aSize;
};

class LocatorCapsuleData : public MUserData
{
  public:
    LocatorCapsuleData() : MUserData(false) {}
    virtual ~LocatorCapsuleData() {}
    double size;
    MColor mColor;
    MPointArray shapePoints;
    MPoint pPointA;
    MPoint pPointB;
    double dRadiusA;
    double dRadiusB;
    double dRadiusC;
    double dLengthA;
    double dLengthB;
    short eType;
    MMatrix mWorldMatrix;
};


class LHCollisionLocatorOverride : public MPxDrawOverride {
public:
  static MPxDrawOverride* creator(const MObject& obj) {
    return new LHCollisionLocatorOverride(obj);
  }
  virtual ~LHCollisionLocatorOverride();

  virtual MHWRender::DrawAPI supportedDrawAPIs() const;
  virtual bool isBounded(const MDagPath& objPath,
                         const MDagPath& cameraPath) const;
  virtual MBoundingBox boundingBox(const MDagPath& objPath,
                                   const MDagPath& cameraPath) const;
  virtual MUserData* prepareForDraw(const MDagPath& objPath,
                                    const MDagPath& cameraPath,
                                    const MFrameContext& frameContext,
                                    MUserData* oldData);
  virtual bool hasUIDrawables() const { return true; }
  virtual void addUIDrawables(const MDagPath& objPath,
                              MHWRender::MUIDrawManager& drawManager,
                              const MHWRender::MFrameContext& frameContext,
                              const MUserData* data);
  virtual LocatorCapsuleData getPlugValuesFromLocatorNode(const MDagPath &objPath) const;


private:
  LHCollisionLocatorOverride(const MObject& obj);
};