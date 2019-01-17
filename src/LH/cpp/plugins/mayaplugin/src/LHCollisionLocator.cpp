#include "LHCollisionLocator.h"

MObject LHCollisionLocator::aSize;

// MObject LHCollisionLocator::aPrimCapsuleType;
// MObject LHCollisionLocator::aPrimCapsuleRadiusA;
// MObject LHCollisionLocator::aPrimCapsuleRadiusB;
// MObject LHCollisionLocator::aPrimCapsuleRadiusC;
// MObject LHCollisionLocator::aPrimCapsuleMatrix;
// MObject LHCollisionLocator::aPrimLengthA;
// MObject LHCollisionLocator::aPrimLengthB;

MTypeId LHCollisionLocator::id(10983797);
static float circle[][3] = {{0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
                          {-1.26431706078e-16f, 6.78573232311e-17f, -1.10819418755f},
                          {-0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
                          {-1.10819418755f, 1.96633546162e-32f, -3.21126950724e-16f},
                          {-0.783611624891f, -4.79823734099e-17f, 0.783611624891f},
                          {-3.33920536359e-16f, -6.78573232311e-17f, 1.10819418755f},
                          {0.783611624891f, -4.79823734099e-17f, 0.783611624891f},
                          {1.10819418755f, -3.6446300679e-32f, 5.95213259928e-16f},
                          {0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
                          {-1.26431706078e-16f, 6.78573232311e-17f, -1.10819418755f},
                          {-0.783611624891f, 4.79823734099e-17f, -0.783611624891f}};
static int circleCount = sizeof(circle)/sizeof(circle[0]) -1;

MString LHCollisionLocator::drawDbClassification("drawdb/geometry/LHCollisionLocator");

MString LHCollisionLocator::drawRegistrantId("LHCollisionLocatorPlugin");

LHCollisionLocator::LHCollisionLocator() {}

LHCollisionLocator::~LHCollisionLocator() {}

void* LHCollisionLocator::creator() {
  return new LHCollisionLocator();
}
bool LHCollisionLocator::isBounded() const
{
    return true;
}
MBoundingBox LHCollisionLocator::boundingBox() const
{
    static MBoundingBox circleBBox;
    for (int i = 0; i < circleCount; i++)
    {
        MPoint shapePoint(circle[i][0], circle[i][1], circle[i][2]);
        circleBBox.expand(shapePoint);
    }

    return circleBBox;
}

void LHCollisionLocator::draw(M3dView &view, const MDagPath &path,
                              M3dView::DisplayStyle style,
                              M3dView::DisplayStatus status)
{
    // just drawing the lines for selection, without this legacy draw you cannot select the locator
    MObject thisNode = thisMObject();

    //Get Size
    MPlug sizePlug(thisNode, aSize);
    double sizeVal;
    sizePlug.getValue(sizeVal);

    //Get Locators World Matrix
    MPlug matrixPlug(thisNode, LHCollisionLocator::worldMatrix);
    MFnMatrixData matrixData(matrixPlug.asMObject());
    MMatrix worldMatrix = matrixData.matrix();

    MPoint origin(0.0, 0.0, 0.0);
    origin = origin * worldMatrix;

    view.beginGL();
    glPushAttrib(GL_CURRENT_BIT);
    glBegin(GL_LINE_STRIP);
    for (unsigned int i = 0; i < circleCount; ++i)
    {
        MPoint point(circle[i][0], circle[i][1], circle[i][2]);
        point = point + (point - origin) * sizeVal;
        glVertex3f(point.x, point.y, point.z);
    }
    glEnd();
    glPopAttrib();
    view.endGL();
}

LHCollisionLocatorOverride::LHCollisionLocatorOverride(const MObject& obj)
    : MPxDrawOverride(obj, NULL) {}

LHCollisionLocatorOverride::~LHCollisionLocatorOverride() {}

MHWRender::DrawAPI LHCollisionLocatorOverride::supportedDrawAPIs() const {
    return (MHWRender::kOpenGL | MHWRender::kDirectX11 | MHWRender::kOpenGLCoreProfile);
}

bool LHCollisionLocatorOverride::isBounded(const MDagPath&, const MDagPath&) const {
  return true;
}

MBoundingBox LHCollisionLocatorOverride::boundingBox(const MDagPath& objPath, const MDagPath& cameraPath) const {
    static MBoundingBox circleBBox;
    for (int i = 0; i < circleCount; i++)
    {
    MPoint shapePoint(circle[i][0], circle[i][1], circle[i][2]);
    circleBBox.expand(shapePoint);
}
    return circleBBox;
}

LocatorCapsuleData LHCollisionLocatorOverride::getPlugValuesFromLocatorNode(const MDagPath &objPath) const
{
    LocatorCapsuleData rData;
    // Retrieve value of the size attribute from the node
    MStatus status;
    MObject locatorNode = objPath.node(&status);

    // Put your objects into an array so you can loop through them by type
    MPlug plug(locatorNode, LHCollisionLocator::aSize);
    double sizeVal;
    plug.getValue(sizeVal);
    rData.size = sizeVal;

    //Get Locators World Matrix
    MPlug matrixPlug(locatorNode, LHCollisionLocator::worldMatrix);
    MFnMatrixData matrixData(matrixPlug.asMObject());
    MMatrix worldMatrix = matrixData.matrix();
    rData.mWorldMatrix = worldMatrix;

    return rData;
}

MUserData* LHCollisionLocatorOverride::prepareForDraw(const MDagPath& objPath, const MDagPath& cameraPath,
                                                  const MHWRender::MFrameContext& frameContext, MUserData* oldData) {

    LocatorCapsuleData *data = dynamic_cast<LocatorCapsuleData *>(oldData);
    if (!data)
    {
        data = new LocatorCapsuleData();
    }

    LocatorCapsuleData plugData = getPlugValuesFromLocatorNode(objPath);
    MPoint origin(0.0, 0.0, 0.0);
    origin = origin * plugData.mWorldMatrix;

    if (data->shapePoints.length())
        data->shapePoints.clear();

    for (int i = 0; i < circleCount; i++)
    {
        MPoint shapePoint(circle[i][0], circle[i][1], circle[i][2]);
        shapePoint = shapePoint + (shapePoint - origin) * (plugData.size -1.0);
        data->shapePoints.append(shapePoint);
    }

    if (M3dView::displayStatus(objPath) == M3dView::kLead)
        data->mColor = M3dView::leadColor();

    if (M3dView::displayStatus(objPath) == M3dView::kActive)
        data->mColor = M3dView::hiliteColor();

    if (M3dView::displayStatus(objPath) == M3dView::kDormant)
        data->mColor = MColor(1.0, 0.0, 0.0, 1.0);

    if (M3dView::displayStatus(objPath) == M3dView::kActiveAffected)
        data->mColor = M3dView::activeAffectedColor();

    if (M3dView::displayStatus(objPath) == M3dView::kTemplate)
        data->mColor = M3dView::templateColor();
        
    if (M3dView::displayStatus(objPath) == M3dView::kActiveTemplate)
        data->mColor = M3dView::activeTemplateColor();

    if (frameContext.getDisplayStyle() == MFrameContext::kWireFrame)
        data->mColor = MHWRender::MGeometryUtilities::wireframeColor(objPath);
    return data;
}

void LHCollisionLocatorOverride::addUIDrawables(const MDagPath& objPath,
                                            MHWRender::MUIDrawManager& drawManager,
                                            const MHWRender::MFrameContext& frameContext,
                                            const MUserData* data) {
  const LocatorCapsuleData* drawData = dynamic_cast<const LocatorCapsuleData*>(data);
  if (!drawData) {
    return;
  }

    drawManager.beginDrawable();
    drawManager.setColor(drawData->mColor);
    drawManager.setLineWidth(1.0);
    drawManager.lineStrip(drawData->shapePoints, false);
    drawManager.endDrawable();
}

MStatus LHCollisionLocator::initialize() {
  MStatus status;
  MFnNumericAttribute nAttr;
  MFnCompoundAttribute cAttr;
  MFnEnumAttribute eAttr;
  MFnUnitAttribute uAttr;

  aSize = nAttr.create("size", "sz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aSize);

  return MS::kSuccess;
}
