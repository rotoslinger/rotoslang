#include "LHNakedLocator.h"

MObject LHNakedLocator::aSize;

MObject LHNakedLocator::aGeo;
MObject LHNakedLocator::aFaceIds;
MObject LHNakedLocator::aCachePlugs;

MObject LHNakedLocator::aColorR;
MObject LHNakedLocator::aColorG;
MObject LHNakedLocator::aColorB;
MObject LHNakedLocator::aInvertMatrix;

MTypeId LHNakedLocator::id(90790790);

MString LHNakedLocator::drawDbClassification("drawdb/geometry/LHNakedLocator");

MString LHNakedLocator::drawRegistrantId("LHNakedLocatorPlugin");

LHNakedLocator::LHNakedLocator() {}

LHNakedLocator::~LHNakedLocator() {}

void* LHNakedLocator::creator() {
  return new LHNakedLocator();
}
bool LHNakedLocator::isBounded() const
{
    return false;
}

void LHNakedLocator::draw(M3dView &view, const MDagPath &path,
                              M3dView::DisplayStyle style,
                              M3dView::DisplayStatus status)
{
    MStatus stat;
    // just drawing the lines for selection, without this legacy draw you cannot select the locator
    MObject thisMObj = thisMObject();

    int cachePlugs = MPlug( thisMObj, aCachePlugs ).asInt();
    if (faceIds.length() == 0 or cachePlugs == 0)
        {
        r = MPlug( thisMObj, aColorR ).asFloat();
        g = MPlug( thisMObj, aColorG ).asFloat();
        b = MPlug( thisMObj, aColorB ).asFloat();
        MObject oFaceIds = MPlug( thisMObj, aFaceIds ).asMObject();
        faceIds = MFnDoubleArrayData(oFaceIds).array();
        }
    MObject oGeo = MPlug( thisMObj, aGeo ).asMObject();
    MObject oFaceIds = MPlug( thisMObj, aFaceIds ).asMObject();
    faceIds = MFnDoubleArrayData(oFaceIds).array();
    if (faceIds.length() && faceIds.length() > 0 && !oGeo.isNull())
    {
        MFnMesh fnGeo(oGeo);
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
            glColor4f(r, g, b, .2);
        }
        if (status == M3dView::kActive)
        {
            glColor4f(1, 1, 1, .2);
        }
        //---not selected
        if (status == M3dView::kDormant)
        {
            glColor4f(r, g, b, .0);
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
  return false;
}

LHNakedLocatorData getNakedPlugValuesFromLocatorNode(const MDagPath &objPath)
{
    LHNakedLocatorData rData;
    // Retrieve value of the size attribute from the node
    MStatus status;
    MObject locatorNode = objPath.node(&status);
    if (status == MS::kFailure)
    {
        MGlobal::displayError(MString("Couldn't get node"));
    }
    MPlug plug(locatorNode, LHNakedLocator::aSize);
    double sizeVal;
    plug.getValue(sizeVal);
    rData.size = sizeVal;

    //Get Locators World Matrix
    MPlug matrixPlug(locatorNode, LHNakedLocator::aInvertMatrix);
    MFnMatrixData matrixData(matrixPlug.asMObject());
    MMatrix worldMatrix = matrixData.matrix();
    rData.mWorldInverseMatrix = worldMatrix;

    //Get Locators World Matrix
    MPlug cachePlug(locatorNode, LHNakedLocator::aCachePlugs);
    int cachePlugs;
    cachePlug.getValue(cachePlugs);
    rData.cachePlugs = cachePlugs;
    rData.r = MPlug( locatorNode, LHNakedLocator::aColorR ).asFloat();
    rData.g = MPlug( locatorNode, LHNakedLocator::aColorG ).asFloat();
    rData.b = MPlug( locatorNode, LHNakedLocator::aColorB ).asFloat();

    MDoubleArray temp;
    MObject oFaceIds = MPlug( locatorNode, LHNakedLocator::aFaceIds ).asMObject();
    if (oFaceIds.isNull())
    {
      rData.faceIds = temp;
    }
    else
    {
    rData.faceIds = MFnDoubleArrayData(oFaceIds).array();
    }
    
    rData.oGeo = MPlug( locatorNode, LHNakedLocator::aGeo ).asMObject();
    return rData;
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
    origin = origin * plugData.mWorldInverseMatrix;

    if (M3dView::displayStatus(objPath) == M3dView::kLead)
        data->mColor = MColor(plugData.r, plugData.g, plugData.b, .2);

    if (M3dView::displayStatus(objPath) == M3dView::kDormant)
        data->mColor = MColor(1.0, 0.0, 0.0, 0.0);

    if (plugData.faceIds.length() && plugData.faceIds.length() > 0 && !plugData.oGeo.isNull())
    {
        if (data->geoPoints.length())
        {
            data->geoPoints.clear();
        }
        MFnMesh fnGeo(plugData.oGeo);
        MStatus status;
        for (unsigned int i=0; i<plugData.faceIds.length();++i)
        {
            // MIntArray facePointIds;
            int facePointIds[3];
            
            for (unsigned int k=0; k<2;++k)
            {
                status = fnGeo.getPolygonTriangleVertices(plugData.faceIds[i], k, facePointIds);
                if (status != MS::kSuccess)
                {
                    continue;
                }
                for (unsigned int j=0; j<3;++j)
                {
                    MPoint pt;
                    // fnGeo.getPolygonNormal(facePointIds[j], normal);
                    fnGeo.getPoint(facePointIds[j], pt);
                    // pt = pt + (pt - normal) * .5;
                    data->geoPoints.append(pt * plugData.mWorldInverseMatrix);
                }
            }
        }
    }
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
    drawManager.setDepthPriority(100);

    // drawManager.setLineWidth(1.0);
    // drawManager.lineStrip(drawData->shapePoints, false);
    drawManager.mesh(MHWRender::MUIDrawManager::kTriangles, drawData->geoPoints);
    drawManager.endDrawable();
}

MStatus LHNakedLocator::initialize() {
  MStatus status;
  MFnNumericAttribute nAttr;
  MFnCompoundAttribute cAttr;
  MFnEnumAttribute eAttr;
  MFnUnitAttribute uAttr;
  MFnTypedAttribute tAttr;
  MFnMatrixAttribute mAttr;

  //Main Matrix
  aInvertMatrix = mAttr.create("nakedInvertMatrix", "nimatrix");
  mAttr.setWritable(true);
  mAttr.setStorable(true);
  addAttribute( aInvertMatrix );
//   attributeAffects(aMainWorldMatrix, outputGeom);


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
