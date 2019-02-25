#pragma once

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
#include <maya/MFnDoubleArrayData.h>
#include <maya/MFnMesh.h>

class LHNakedLocator : public MPxLocatorNode
{
  public:
    LHNakedLocator();
    virtual ~LHNakedLocator();
    static void *creator();
    static MStatus initialize();
    virtual bool isBounded() const;
    virtual void draw(M3dView &view, const MDagPath &path,
                      M3dView::DisplayStyle style,
                      M3dView::DisplayStatus status);

  public:
    static MTypeId id;
    static MString drawDbClassification;
    static MString drawRegistrantId;
    static MObject aSize;
    static  MObject         aGeo;
    static  MObject         aFaceIds;
    static  MObject         aCachePlugs;
    static  MObject         aColorR;
    static  MObject         aColorG;
    static  MObject         aColorB;
    static  MObject         aInvertMatrix;

    MDoubleArray faceIds;
    float r;
    float g;
    float b;
    double tx;
    double ty;
    double tz;
    int cachePlugs;
};

class LHNakedLocatorData : public MUserData
{
  public:
    LHNakedLocatorData() : MUserData(false) {}
    virtual ~LHNakedLocatorData() {}
    double size;
    MColor mColor;
    // MPointArray shapePoints;
    MMatrix mWorldInverseMatrix;
    int cachePlugs;
    float r;
    float g;
    float b;
    MDoubleArray faceIds;
    MObject oGeo;
    MPointArray geoPoints;
};


class LHNakedLocatorOverride : public MPxDrawOverride {
public:
  static MPxDrawOverride* creator(const MObject& obj) {
    return new LHNakedLocatorOverride(obj);
  }
  virtual ~LHNakedLocatorOverride();

  virtual MHWRender::DrawAPI supportedDrawAPIs() const;
  virtual bool isBounded(const MDagPath& objPath,
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
  MVector normal;


private:
  LHNakedLocatorOverride(const MObject& obj);
};