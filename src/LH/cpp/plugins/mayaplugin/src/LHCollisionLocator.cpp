#include "LHCollisionLocator.h"

MObject LHCollisionLocator::aSize;

MObject LHCollisionLocator::aPrimCapsuleType;
MObject LHCollisionLocator::aPrimCapsuleRadiusA;
MObject LHCollisionLocator::aPrimCapsuleRadiusB;
MObject LHCollisionLocator::aPrimCapsuleRadiusC;
MObject LHCollisionLocator::aPrimCapsuleRadiusD;
MObject LHCollisionLocator::aPrimLengthA;
MObject LHCollisionLocator::aPrimLengthB;

MTypeId LHCollisionLocator::id(10983797);
// static float circle[][3] = {{0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
//                           {-1.26431706078e-16f, 6.78573232311e-17f, -1.10819418755f},
//                           {-0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
//                           {-1.10819418755f, 1.96633546162e-32f, -3.21126950724e-16f},
//                           {-0.783611624891f, -4.79823734099e-17f, 0.783611624891f},
//                           {-3.33920536359e-16f, -6.78573232311e-17f, 1.10819418755f},
//                           {0.783611624891f, -4.79823734099e-17f, 0.783611624891f},
//                           {1.10819418755f, -3.6446300679e-32f, 5.95213259928e-16f},
//                           {0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
//                           {-1.26431706078e-16f, 6.78573232311e-17f, -1.10819418755f},
//                           {-0.783611624891f, 4.79823734099e-17f, -0.783611624891f}};
// static int circleCount = sizeof(circle)/sizeof(circle[0]) -1;

std::vector<std::vector<float>> newCircle = {{0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
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

std::vector<std::vector<float>> sphere = {{-5.36587337206e-16f, -6.12203396374e-17f, 0.999804019903f},
                                          {0.308956433194f, -5.8224002942e-17f, 0.950870128147f},
                                          {0.587670058082f, -4.95282951681e-17f, 0.808858443146f},
                                          {0.808858443146f, -3.59844127792e-17f, 0.587670058082f},
                                          {0.950870128147f, -1.89181253494e-17f, 0.308956433194f},
                                          {0.999804019903f, -3.57023946799e-32f, 5.83064353e-16f},
                                          {0.950870128147f, 1.89181253494e-17f, -0.308956433194f},
                                          {0.808858443146f, 3.59844127792e-17f, -0.587670058082f},
                                          {0.587670058082f, 4.95282951681e-17f, -0.808858443146f},
                                          {0.308956433194f, 5.8224002942e-17f, -0.950870128147f},
                                          {-6.16179902019e-17f, 6.12203396374e-17f, -0.999804019903f},
                                          {-0.308956433194f, 5.8224002942e-17f, -0.950870128147f},
                                          {-0.587670058082f, 4.95282951681e-17f, -0.808858443146f},
                                          {-0.808858443146f, 3.59844127792e-17f, -0.587670058082f},
                                          {-0.950870128147f, 1.89181253494e-17f, -0.308956433194f},
                                          {-0.999804019903f, 1.12083152919e-32f, -1.83045679778e-16f},
                                          {-0.950870128147f, -1.89181253494e-17f, 0.308956433194f},
                                          {-0.808858443146f, -3.59844127792e-17f, 0.587670058082f},
                                          {-0.587670058082f, -4.95282951681e-17f, 0.808858443146f},
                                          {-0.308956433194f, -5.8224002942e-17f, 0.950870128147f},
                                          {-5.36587337206e-16f, -6.12203396374e-17f, 0.999804019903f},
                                          {4.37515205623e-15f, 0.308956433194f, 0.950870128147f},
                                          {8.32203374572e-15f, 0.587670058082f, 0.808858443146f},
                                          {1.14542967892e-14f, 0.808858443146f, 0.587670058082f},
                                          {1.34653334561e-14f, 0.950870128147f, 0.308956433194f},
                                          {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f},
                                          {1.34653334561e-14f, 0.950870128147f, -0.308956433194f},
                                          {1.14542967892e-14f, 0.808858443146f, -0.587670058082f},
                                          {8.32203374572e-15f, 0.587670058082f, -0.808858443146f},
                                          {4.37515205623e-15f, 0.308956433194f, -0.950870128147f},
                                          {-6.16179902019e-17f, 6.12203396374e-17f, -0.999804019903f},
                                          {-4.37515205623e-15f, -0.308956433194f, -0.950870128147f},
                                          {-8.32203374572e-15f, -0.587670058082f, -0.808858443146f},
                                          {-1.14542967892e-14f, -0.808858443146f, -0.587670058082f},
                                          {-1.34653334561e-14f, -0.950870128147f, -0.308956433194f},
                                          {-5.36587337206e-16f, -0.999804019903f, 1.60780748964e-16f},
                                          {-1.34653334561e-14f, -0.950870128147f, 0.308956433194f},
                                          {-1.14542967892e-14f, -0.808858443146f, 0.587670058082f},
                                          {-8.32203374572e-15f, -0.587670058082f, 0.808858443146f},
                                          {-4.37515205623e-15f, -0.308956433194f, 0.950870128147f},
                                          {-5.36587337206e-16f, -6.12203396374e-17f, 0.999804019903f},
                                          {4.37515205623e-15f, 0.308956433194f, 0.950870128147f},
                                          {8.32203374572e-15f, 0.587670058082f, 0.808858443146f},
                                          {1.14542967892e-14f, 0.808858443146f, 0.587670058082f},
                                          {1.34653334561e-14f, 0.950870128147f, 0.308956433194f},
                                          {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f},
                                          {0.308956433194f, 0.950870128147f, -1.52911578997e-16f},
                                          {0.587670058082f, 0.808858443146f, -1.3007435828e-16f},
                                          {0.808858443146f, 0.587670058082f, -9.45045530938e-17f},
                                          {0.950870128147f, 0.308956433194f, -4.96839837983e-17f},
                                          {0.999804019903f, -3.57023946799e-32f, 5.83064353e-16f},
                                          {0.950870128147f, -0.308956433194f, 4.96839837983e-17f},
                                          {0.808858443146f, -0.587670058082f, 9.45045530938e-17f},
                                          {0.587670058082f, -0.808858443146f, 1.3007435828e-16f},
                                          {0.308956433194f, -0.950870128147f, 1.52911578997e-16f},
                                          {-5.36587337206e-16f, -0.999804019903f, 1.60780748964e-16f},
                                          {-0.308956433194f, -0.950870128147f, 1.52911578997e-16f},
                                          {-0.587670058082f, -0.808858443146f, 1.3007435828e-16f},
                                          {-0.808858443146f, -0.587670058082f, 9.45045530938e-17f},
                                          {-0.950870128147f, -0.308956433194f, 4.96839837983e-17f},
                                          {-0.999804019903f, 1.12083152919e-32f, -1.83045679778e-16f},
                                          {-0.950870128147f, 0.308956433194f, -4.96839837983e-17f},
                                          {-0.808858443146f, 0.587670058082f, -9.45045530938e-17f},
                                          {-0.587670058082f, 0.808858443146f, -1.3007435828e-16f},
                                          {-0.308956433194f, 0.950870128147f, -1.52911578997e-16f},
                                          {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f}};

MString LHCollisionLocator::drawDbClassification("drawdb/geometry/LHCollisionLocator");

MString LHCollisionLocator::drawRegistrantId("LHCollisionLocatorPlugin");

LHCollisionLocator::LHCollisionLocator() {}

LHCollisionLocator::~LHCollisionLocator() {}

void* LHCollisionLocator::creator() {
  return new LHCollisionLocator();
}
// bool LHCollisionLocator::isBounded() const
// {
//     return false;
// }
// MBoundingBox LHCollisionLocator::boundingBox() const
// {
//     static MBoundingBox circleBBox;
//     for (int i = 0; i < circleCount; i++)
//     {
//         MPoint shapePoint(circle[i][0], circle[i][1], circle[i][2]);
//         circleBBox.expand(shapePoint);
//     }
//     MBoundingBox bounds;
//     return bounds;
// }

LocatorCapsuleData getPlugValuesFromLocatorNode(const MDagPath &objPath)
{
    LocatorCapsuleData rData;
    // Retrieve value of the size attribute from the node
    MStatus status;
    MObject locatorNode = objPath.node(&status);

    // Put your objects into an array so you can loop through them by type
    MPlug plug(locatorNode, LHCollisionLocator::aSize);
    double val;
    plug.getValue(val);
    rData.size = val;

    MPlug radiusAPlug(locatorNode, LHCollisionLocator::aPrimCapsuleRadiusA);
    radiusAPlug.getValue(val);
    rData.dRadiusA = val;

    MPlug radiusBPlug(locatorNode, LHCollisionLocator::aPrimCapsuleRadiusB);
    radiusBPlug.getValue(val);
    rData.dRadiusB = val;

    MPlug radiusCPlug(locatorNode, LHCollisionLocator::aPrimCapsuleRadiusC);
    radiusCPlug.getValue(val);
    rData.dRadiusC = val;

    MPlug radiusDPlug(locatorNode, LHCollisionLocator::aPrimCapsuleRadiusD);
    radiusDPlug.getValue(val);
    rData.dRadiusD = val;


    MPlug lengthAPlug(locatorNode, LHCollisionLocator::aPrimLengthA);
    lengthAPlug.getValue(val);
    rData.dLengthA = val;

    MPlug lengthBPlug(locatorNode, LHCollisionLocator::aPrimLengthB);
    lengthBPlug.getValue(val);
    rData.dLengthB = val;


    MPlug eTypePlug(locatorNode, LHCollisionLocator::aPrimCapsuleType);
    short eVal;
    eTypePlug.getValue(eVal);
    rData.eType = eVal;


    //Get Locators World Matrix
    MPlug matrixPlug(locatorNode, LHCollisionLocator::worldMatrix);
    MFnMatrixData matrixData(matrixPlug.asMObject());
    MMatrix worldMatrix = matrixData.matrix();
    rData.mWorldMatrix = worldMatrix;


    // Start and end points
    MPoint pointStart(0.0, 0.0, 0.0);
    MPoint pointEnd(0.0, 0.0, 1.0);

    rData.pPointStart = pointStart * worldMatrix;
    rData.pPointEnd = pointEnd * worldMatrix;


    return rData;
}


MPoint drawType(MPoint inPoint, LocatorCapsuleData capsuleData)
{
    switch( capsuleData.eType )
    {
        case 0 : // sphere
            inPoint = inPoint + (inPoint - capsuleData.pPointStart) * (capsuleData.dRadiusA -1.0);
            break;
        case 1 : // elipsoidCapsule
            break;
        case 2 : // elipsoid
            break;
        case 3 : // cylinder
            break;
        case 4 : // plane
            break;
        case 5 : // capsule
            break;
        case 6 : // cone
            break;
    }

    return inPoint;
}

 void getShape(std::vector<std::vector<float>> &shape, LocatorCapsuleData capsuleData)
 {
     switch (capsuleData.eType)
     {
     case 0: // sphere
         shape = sphere;
         break;
     case 1: // elipsoidCapsule
         break;
     case 2: // elipsoid
         break;
     case 3: // cylinder
         break;
     case 4: // plane
         break;
     case 5: // capsule
         break;
     case 6: // cone
         break;
     }


}

void LHCollisionLocator::draw(M3dView &view, const MDagPath &path,
                              M3dView::DisplayStyle style,
                              M3dView::DisplayStatus status)
{

    LocatorCapsuleData plugData = getPlugValuesFromLocatorNode(path);

    std::vector<std::vector<float>> shape;
    getShape(shape, plugData);

    view.beginGL();
    glPushAttrib(GL_CURRENT_BIT);
    glBegin(GL_LINE_STRIP);
    for (unsigned int i = 0; i < shape.size(); ++i)
    {
        MPoint shapePoint(shape[i][0], shape[i][1], shape[i][2]);
        shapePoint = drawType(shapePoint, plugData);
        glVertex3f(shapePoint.x, shapePoint.y, shapePoint.z);
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

// bool LHCollisionLocatorOverride::isBounded(const MDagPath&, const MDagPath&) const {
//   return false;
// }

// MBoundingBox LHCollisionLocatorOverride::boundingBox(const MDagPath& objPath, const MDagPath& cameraPath) const {
//     static MBoundingBox circleBBox;
//     for (int i = 0; i < circleCount; i++)
//     {
//     MPoint shapePoint(circle[i][0], circle[i][1], circle[i][2]);
//     circleBBox.expand(shapePoint);
//     }
//     return circleBBox;
// }










MUserData* LHCollisionLocatorOverride::prepareForDraw(const MDagPath& objPath, const MDagPath& cameraPath,
                                                  const MHWRender::MFrameContext& frameContext, MUserData* oldData) {

    LocatorCapsuleData *data = dynamic_cast<LocatorCapsuleData *>(oldData);
    if (!data)
    {
        data = new LocatorCapsuleData();
    }

    LocatorCapsuleData plugData = getPlugValuesFromLocatorNode(objPath);

    if (data->shapePoints.length())
        data->shapePoints.clear();
    std::vector<std::vector<float>> shape;
    getShape(shape, plugData);

    for (int i = 0; i < shape.size(); i++)
    {
        MPoint shapePoint(shape[i][0], shape[i][1], shape[i][2]);
        shapePoint = drawType(shapePoint, plugData);
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

  aPrimCapsuleRadiusA = nAttr.create("capsuleRadiusA", "cradiusa", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusA);

  aPrimCapsuleRadiusB = nAttr.create("capsuleRadiusB", "cradiusb", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusB);

  aPrimCapsuleRadiusC = nAttr.create("capsuleRadiusC", "cradiusc", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusC);

  aPrimCapsuleRadiusD = nAttr.create("capsuleRadiusD", "cradiusd", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusD);

  aPrimLengthA = nAttr.create("pLengthA", "plena", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(0.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimLengthA);

  aPrimLengthB = nAttr.create("pLengthB", "plenb", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(0.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimLengthB);

  aPrimCapsuleType = eAttr.create("primType", "ptyp", 0);
  eAttr.addField( "sphere", 0 );
  eAttr.addField( "elipsoidCapsule", 1 );
  eAttr.addField( "elipsoid", 2 );
  eAttr.addField( "cylinder", 3 );
  eAttr.addField( "plane", 4 );
  eAttr.addField( "capsule", 5 );
  eAttr.addField( "cone", 6 );
  eAttr.setHidden( false );
  eAttr.setKeyable( true );
  eAttr.setWritable(true);
  eAttr.setStorable(true);
  eAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleType);



  return MS::kSuccess;
}
