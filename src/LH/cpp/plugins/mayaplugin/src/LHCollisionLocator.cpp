#include "LHCollisionLocator.h"
#include "constants.h"

MObject LHCollisionLocator::aSize;

MObject LHCollisionLocator::aPrimCapsuleType;
MObject LHCollisionLocator::aPrimCapsuleRadiusA;
MObject LHCollisionLocator::aPrimCapsuleRadiusB;
MObject LHCollisionLocator::aPrimCapsuleRadiusC;
MObject LHCollisionLocator::aPrimCapsuleRadiusD;
MObject LHCollisionLocator::aPrimLengthA;
MObject LHCollisionLocator::aPrimLengthB;

MTypeId LHCollisionLocator::id(10983797);

MString LHCollisionLocator::drawDbClassification("drawdb/geometry/LHCollisionLocator");

MString LHCollisionLocator::drawRegistrantId("LHCollisionLocatorPlugin");

LHCollisionLocator::LHCollisionLocator() {}

LHCollisionLocator::~LHCollisionLocator() {}

void* LHCollisionLocator::creator() {
  return new LHCollisionLocator();
}
// In case we need to implement in the future:
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


    switch( rData.eType )
    {
        case 0 : // sphere
            rData.shape = sphere;
            rData.intArray = sphereIntArray;
            // rData.doShapeA = true;
            // rData.doShapeB = false;
            // rData.doShapeC = false;
            break;
        case 1 : // elipsoidCapsule
            rData.shape = capsule;
            rData.intArray = capsuleIntArray;
            // rData.doShapeA = true;
            // rData.doShapeB = false;
            // rData.doShapeC = false;
            break;
        case 2 : // elipsoid
            rData.shape = sphere;
            rData.intArray = sphereIntArray;
            break;
        case 3 : // cylinder
            rData.shape = cylinder;
            rData.intArray = cylinderIntArray;
            break;
        case 4 : // plane
            rData.shape = plane;
            rData.intArray = planeIntArray;
            break;
        case 5 : // capsule
            rData.shape = capsule;
            rData.intArray = capsuleIntArray;
            break;
        case 6 : // cone
            rData.shape = cone;
            rData.intArray = coneIntArray;
            break;
    }
    return rData;
}
MPoint cylinderEndPointLogic(MPoint inPoint, LocatorCapsuleData capsuleData, int index)
{
    if  (std::find(std::begin(capsuleData.intArray[0]), std::end(capsuleData.intArray[0]), index) == std::end(capsuleData.intArray[0]))
    {
        return inPoint + (inPoint - capsuleData.pPointEnd) * (capsuleData.dRadiusB -1.0);
    }
    if  (std::find(std::begin(capsuleData.intArray[1]), std::end(capsuleData.intArray[1]), index) == std::end(capsuleData.intArray[1]))
    {
        return inPoint + (inPoint - capsuleData.pPointStart) * (capsuleData.dRadiusA -1.0);
    }
    MPoint nullPoint(0.0, 0.0, 0.0);
    return nullPoint;
}

MPoint lengthLogic(MPoint inPoint, LocatorCapsuleData capsuleData, int index)
{
    if  (std::find(std::begin(capsuleData.intArray[0]), std::end(capsuleData.intArray[0]), index) == std::end(capsuleData.intArray[0]))
    {
        return inPoint + (capsuleData.pPointEnd - capsuleData.pPointStart) * capsuleData.dLengthB;
    }
    if  (std::find(std::begin(capsuleData.intArray[1]), std::end(capsuleData.intArray[1]), index) == std::end(capsuleData.intArray[1]))
    {
        return inPoint + (capsuleData.pPointStart - capsuleData.pPointEnd) * capsuleData.dLengthA;
    }
    MPoint nullPoint(0.0, 0.0, 0.0);
    return nullPoint;

}
MPoint capWidthLogic(MPoint inPoint, LocatorCapsuleData capsuleData, int index, MTransformationMatrix capsuleMatrix)
{
            double matScaleArray[3];

    if  (std::find(std::begin(capsuleData.intArray[0]), std::end(capsuleData.intArray[0]), index) == std::end(capsuleData.intArray[0]))
    {
        MVector translate(0.0, 0.0, 1.0);
        inPoint = inPoint -translate;
        capsuleMatrix.getScale( matScaleArray, MSpace::kObject);
        matScaleArray[2] = matScaleArray[2] * capsuleData.dRadiusD;
        capsuleMatrix.setScale( matScaleArray, MSpace::kObject);
        inPoint = inPoint * capsuleMatrix.asMatrix();
        return inPoint + translate;
    }
    if  (std::find(std::begin(capsuleData.intArray[1]), std::end(capsuleData.intArray[1]), index) == std::end(capsuleData.intArray[1]))
    {
        capsuleMatrix.getScale( matScaleArray, MSpace::kObject);
        matScaleArray[2] = matScaleArray[2] * capsuleData.dRadiusC;
        capsuleMatrix.setScale( matScaleArray, MSpace::kObject);
        return inPoint * capsuleMatrix.asMatrix();
    }
    MPoint nullPoint(0.0, 0.0, 0.0);
    return nullPoint;
}


MPoint drawType(MPoint inPoint, LocatorCapsuleData capsuleData, int index)
{
    MTransformationMatrix capsuleMatrix(capsuleData.mWorldMatrix);

    switch( capsuleData.eType )
    {
        case 0 : // sphere
            inPoint = inPoint + (inPoint - capsuleData.pPointStart) * (capsuleData.dRadiusA -1.0);
            break;
        case 1 : // elipsoidCapsule
            inPoint = cylinderEndPointLogic(inPoint, capsuleData, index);
            inPoint = capWidthLogic(inPoint, capsuleData, index, capsuleMatrix);
            inPoint = lengthLogic(inPoint, capsuleData, index);
            break;
        case 2 : // elipsoid
            double matScaleArray[3];
            capsuleMatrix.getScale( matScaleArray, MSpace::kObject);
            matScaleArray[0] = matScaleArray[0] * capsuleData.dRadiusA;
            matScaleArray[1] = matScaleArray[1] * capsuleData.dRadiusB;
            matScaleArray[2] = matScaleArray[2] * capsuleData.dRadiusC;
            capsuleMatrix.setScale( matScaleArray, MSpace::kObject);
            inPoint = inPoint * capsuleMatrix.asMatrix();
            break;
        case 3 : // cylinder
            inPoint = cylinderEndPointLogic(inPoint, capsuleData, index);
            inPoint = lengthLogic(inPoint, capsuleData, index);
            break;
        case 4 : // plane
            // The plane has the simplest logic, it does nothing
            break;
        case 5 : // capsule
            inPoint = cylinderEndPointLogic(inPoint, capsuleData, index);
            inPoint = lengthLogic(inPoint, capsuleData, index);
            break;
        case 6 : // cone
            inPoint = cylinderEndPointLogic(inPoint, capsuleData, index);
            inPoint = lengthLogic(inPoint, capsuleData, index);
            break;
    }

    return inPoint;
}

void collectShapeData(LocatorCapsuleData plugData, MPointArray &shapePoints)
{
    if (shapePoints.length())
        shapePoints.clear();

    // std::vector<std::vector<float>> shape;

    // getShape(shape, plugData);

    for (int i = 0; i < plugData.shape.size(); i++)
    {
        MPoint shapePoint(plugData.shape[i][0], plugData.shape[i][1], plugData.shape[i][2]);
        shapePoint = drawType(shapePoint, plugData, i);
        shapePoints.append(shapePoint);
    }

}

void drawShape(MPointArray shapePoints, LocatorCapsuleData plugData)
{
    for (unsigned int i = 0; i < shapePoints.length(); ++i)
    {
        MPoint shapePoint(shapePoints[i][0], shapePoints[i][1], shapePoints[i][2]);
        shapePoint = drawType(shapePoint, plugData, i);
        glVertex3f(shapePoint.x, shapePoint.y, shapePoint.z);
    }
}

void LHCollisionLocator::draw(M3dView &view, const MDagPath &path,
                              M3dView::DisplayStyle style,
                              M3dView::DisplayStatus status)
{

    LocatorCapsuleData plugData = getPlugValuesFromLocatorNode(path);

    // if (plugData.doShapeA)
    collectShapeData(plugData, plugData.shapePointsA);
    // if (plugData.doShapeB)
    //     collectShapeData(plugData, plugData.shapePointsB);
    // if (plugData.doShapeC)
    //     collectShapeData(plugData, plugData.shapePointsC);

    view.beginGL();

    // if (plugData.doShapeA)
    glPushAttrib(GL_CURRENT_BIT);
    glBegin(GL_LINE_STRIP);
    drawShape(plugData.shapePointsA, plugData);
    glEnd();
    glPopAttrib();
    // if (plugData.doShapeB)
    //     view.beginGL();
    //     glPushAttrib(GL_CURRENT_BIT);
    //     glBegin(GL_LINE_STRIP);
    //     drawShape(plugData.shapePointsB, plugData);
    //     glEnd();
    //     glPopAttrib();
    // if (plugData.doShapeC)
    //     view.beginGL();
    //     glPushAttrib(GL_CURRENT_BIT);
    //     glBegin(GL_LINE_STRIP);
    //     drawShape(plugData.shapePointsC, plugData);
    //     glEnd();
    //     glPopAttrib();

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
    // data->doShapeA = plugData.doShapeA ;
    // data->doShapeB = plugData.doShapeB ;
    // data->doShapeB = plugData.doShapeB ;

    // if (plugData.doShapeA)
    collectShapeData(plugData, data->shapePointsA);
    // if (plugData.doShapeB)
    //     collectShapeData(plugData, data->shapePointsB);
    // if (plugData.doShapeC)
    //     collectShapeData(plugData, data->shapePointsC);



    // if (data->shapePointsA.length())
    //     data->shapePointsA.clear();
    // std::vector<std::vector<float>> shape;
    // getShape(shape, plugData);

    // for (int i = 0; i < shape.size(); i++)
    // {
    //     MPoint shapePoint(shape[i][0], shape[i][1], shape[i][2]);
    //     shapePoint = drawType(shapePoint, plugData);
    //     data->shapePointsA.append(shapePoint);
    // }

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
    drawManager.lineStrip(drawData->shapePointsA, false);
    drawManager.endDrawable()
    ;
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
