#include "LHNakedLocator.h"

MObject LHNakedLocator::aSize;

MObject LHNakedLocator::aGeo;
MObject LHNakedLocator::aFaceIds;
MObject LHNakedLocator::aCachePlugs;

MObject LHNakedLocator::aColorR;
MObject LHNakedLocator::aColorG;
MObject LHNakedLocator::aColorB;

MTypeId LHNakedLocator::id(90790790);
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

MString LHNakedLocator::drawDbClassification("drawdb/geometry/LHNakedLocator");

MString LHNakedLocator::drawRegistrantId("LHNakedLocatorPlugin");

LHNakedLocator::LHNakedLocator() {}

LHNakedLocator::~LHNakedLocator() {}

void* LHNakedLocator::creator() {
  return new LHNakedLocator();
}
bool LHNakedLocator::isBounded() const
{
    return true;
}
MBoundingBox LHNakedLocator::boundingBox() const
{
    static MBoundingBox circleBBox;
    for (int i = 0; i < circleCount; i++)
    {
        MPoint shapePoint(circle[i][0], circle[i][1], circle[i][2]);
        circleBBox.expand(shapePoint);
    }

    return circleBBox;
}
LHNakedLocatorData getNakedPlugValuesFromLocatorNode(const MDagPath &objPath)
{
    LHNakedLocatorData rData;
    // Retrieve value of the size attribute from the node
    MStatus status;
    MObject locatorNode = objPath.node(&status);

    // Put your objects into an array so you can loop through them by type
    MPlug plug(locatorNode, LHNakedLocator::aSize);
    double sizeVal;
    plug.getValue(sizeVal);
    rData.size = sizeVal;

    //Get Locators World Matrix
    MPlug matrixPlug(locatorNode, LHNakedLocator::worldMatrix);
    MFnMatrixData matrixData(matrixPlug.asMObject());
    MMatrix worldMatrix = matrixData.matrix();
    rData.mWorldMatrix = worldMatrix;

    //Get Locators World Matrix
    MPlug cachePlug(locatorNode, LHNakedLocator::aCachePlugs);
    int cachePlugs;
    cachePlug.getValue(cachePlugs);
    rData.cachePlugs = cachePlugs;

    MPlug rPlug(locatorNode, LHNakedLocator::aColorR);
    int rColor;
    rPlug.getValue(rColor);
    rData.r = rColor;

    MPlug gPlug(locatorNode, LHNakedLocator::aColorG);
    int gColor;
    gPlug.getValue(gColor);
    rData.g = gColor;

    MPlug bPlug(locatorNode, LHNakedLocator::aColorB);
    int bColor;
    bPlug.getValue(bColor);
    rData.b = bColor;

    // MDoubleArray temp;
    // MObject oFaceIds = MPlug( locatorNode, LHNakedLocator::aFaceIds ).asMObject();
    // if (oFaceIds.isNull())
    // {
    //   rData.faceIds = temp;
    // }
    // else
    // {
    // rData.faceIds = MFnDoubleArrayData(oFaceIds).array();
    // }
    
    // rData.oGeo = MPlug( locatorNode, LHNakedLocator::aGeo ).asMObject();
    // rData.oGeo = new MFnMesh(oGeo);

    return rData;
}

void LHNakedLocator::draw(M3dView &view, const MDagPath &path,
                              M3dView::DisplayStyle style,
                              M3dView::DisplayStatus status)
{
    MStatus stat;
    // just drawing the lines for selection, without this legacy draw you cannot select the locator
    MObject thisMObj = thisMObject();

    //Get Size
    MPlug sizePlug(thisMObj, aSize);
    double sizeVal;
    sizePlug.getValue(sizeVal);

    //Get Locators World Matrix
    MPlug matrixPlug(thisMObj, LHNakedLocator::worldMatrix);
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

    LHNakedLocatorData plugData = getNakedPlugValuesFromLocatorNode(path);

    // int cachePlugs = MPlug( thisMObj, aCachePlugs ).asInt();
    // if (faceIds.length() == 0 or cachePlugs == 0)
    //     {
    //     r = MPlug( thisMObj, aColorR ).asFloat();
    //     g = MPlug( thisMObj, aColorG ).asFloat();
    //     b = MPlug( thisMObj, aColorB ).asFloat();
    //     MObject oFaceIds = MPlug( thisMObj, aFaceIds ).asMObject();
    //     faceIds = MFnDoubleArrayData(oFaceIds).array();
    //     }
    MObject oGeo = MPlug( thisMObj, aGeo ).asMObject();
    MObject oFaceIds = MPlug( thisMObj, aFaceIds ).asMObject();
    faceIds = MFnDoubleArrayData(oFaceIds).array();

    if (faceIds.length() && faceIds.length() > 0 && !plugData.oGeo.isNull())
    {
        MFnMesh fnGeo(plugData.oGeo);

        int drawOn = 1;
        glEnable(GL_BLEND);
        glEnable( GL_POLYGON_OFFSET_FILL);
        float factor;
        glGetFloatv(GL_POLYGON_OFFSET_FACTOR, &factor);
        float unit;
        glGetFloatv(GL_POLYGON_OFFSET_FACTOR, &unit);

        glPolygonOffset(-10.0f, -50.0f);
        view.beginGL();

        glBegin(GL_QUADS);
        if (status == M3dView::kLead)
        {
            glColor4f(plugData.r, plugData.g, plugData.b, .2);
        }
        if (status == M3dView::kActive)
        {
            glColor4f(1, 1, 1, .2);
        }
        //---not selected
        if (status == M3dView::kDormant)
        {
            glColor4f(plugData.r, plugData.g, plugData.b, .0);
        }
        //---affected
        if (status == M3dView::kActiveAffected)
        {
            glColor4f(2.0, 0.0, 2.0, .5);
        }

        if (status == M3dView::kTemplate)
        {
            glColor4f(0.47, 0.47, 0.47, .5);
        }

        if (status == M3dView::kActiveTemplate)
        {
            glColor4f(1.0, 0.47, 0.47, .5);
        }
        for (unsigned int i=0; i<faceIds.length();++i)
        {
            MIntArray facePointIds;

            stat = fnGeo.getPolygonVertices(faceIds[i], facePointIds);
            for (unsigned int j=0; j<facePointIds.length();++j)
            {
                MPoint pt;
                stat = fnGeo.getPoint(facePointIds[j], pt);
                glNormal3f( 0.0, 1.0, 0.0 );
                glVertex3f( pt.x, pt.y, pt.z) ;
            }

        }

        glPopAttrib();
        glEnd();
        view.endGL();
        glPolygonOffset(factor, unit);
        glDisable(GL_BLEND);
        glDisable( GL_POLYGON_OFFSET_FILL);
        glDisable(GL_BLEND);
        glDisable( GL_POLYGON_OFFSET_FILL);
    }
    glDisable(GL_BLEND);
    glDisable( GL_POLYGON_OFFSET_FILL);
        




}

LHNakedLocatorOverride::LHNakedLocatorOverride(const MObject& obj)
    : MPxDrawOverride(obj, NULL) {}

LHNakedLocatorOverride::~LHNakedLocatorOverride() {}

MHWRender::DrawAPI LHNakedLocatorOverride::supportedDrawAPIs() const {
    return (MHWRender::kOpenGL | MHWRender::kDirectX11 | MHWRender::kOpenGLCoreProfile);
}

bool LHNakedLocatorOverride::isBounded(const MDagPath&, const MDagPath&) const {
  return true;
}

MBoundingBox LHNakedLocatorOverride::boundingBox(const MDagPath& objPath, const MDagPath& cameraPath) const {
    static MBoundingBox circleBBox;
    for (int i = 0; i < circleCount; i++)
    {
    MPoint shapePoint(circle[i][0], circle[i][1], circle[i][2]);
    circleBBox.expand(shapePoint);
}
    return circleBBox;
}


MUserData* LHNakedLocatorOverride::prepareForDraw(const MDagPath& objPath, const MDagPath& cameraPath,
                                                  const MHWRender::MFrameContext& frameContext, MUserData* oldData) {

    LHNakedLocatorData *data = dynamic_cast<LHNakedLocatorData *>(oldData);
    if (!data)
    {
        data = new LHNakedLocatorData();
    }

    LHNakedLocatorData plugData = getNakedPlugValuesFromLocatorNode(objPath);
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

void LHNakedLocatorOverride::addUIDrawables(const MDagPath& objPath,
                                            MHWRender::MUIDrawManager& drawManager,
                                            const MHWRender::MFrameContext& frameContext,
                                            const MUserData* data) {
  const LHNakedLocatorData* drawData = dynamic_cast<const LHNakedLocatorData*>(data);
  if (!drawData) {
    return;
  }

    drawManager.beginDrawable();
    drawManager.setColor(drawData->mColor);
    drawManager.setLineWidth(1.0);
    drawManager.lineStrip(drawData->shapePoints, false);
    drawManager.endDrawable();
}

MStatus LHNakedLocator::initialize() {
  MStatus status;
  MFnNumericAttribute nAttr;
  MFnCompoundAttribute cAttr;
  MFnEnumAttribute eAttr;
  MFnUnitAttribute uAttr;
  MFnTypedAttribute tAttr;

  aSize = nAttr.create("size", "sz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aSize);

  aGeo = tAttr.create( "geom", "geo", MFnData::kMesh);
  addAttribute(aGeo);

  aFaceIds = tAttr.create( "faceIds", "fids", MFnNumericData::kDoubleArray);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  addAttribute(aFaceIds);

  aCachePlugs = nAttr.create( "cachePlugs", "cp", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  addAttribute(aCachePlugs);


  aColorR = nAttr.create( "Color_R", "cr", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  addAttribute(aColorR);

  aColorG = nAttr.create( "Color_G", "cg", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  addAttribute(aColorG);

  aColorB = nAttr.create( "Color_B", "cb", MFnNumericData::kFloat);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  addAttribute(aColorB);




  return MS::kSuccess;
}
