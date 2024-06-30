import sys

from rig_2.animcurve import utils as animcurve_utils
import importlib
importlib.reload(animcurve_utils)
from rig_2.weights import utils as weight_utils
importlib.reload(weight_utils)

importlib.reload(animcurve_utils)
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
win = "C:\\Users\\harri\\Desktop\\dev\\rotoslang\\src\\LH\\python\\libs"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win32" in os:
    os = mac

if os not in sys.path:
    sys.path.append(os)

from maya import cmds
import maya.OpenMaya as OpenMaya
from rig.utils import misc
importlib.reload(misc)
from rig.utils import exportUtils
importlib.reload(exportUtils)
from rig.utils import weightMapUtils
importlib.reload(weightMapUtils)

from rig.rigComponents import meshRivetCtrl
importlib.reload(meshRivetCtrl)

def calimari(skinCluster, mesh, bias, hide=True):
    vertCount = cmds.polyEvaluate(mesh, v=1) - 1
    jnts = cmds.skinCluster(skinCluster, q=True, inf=True)
    tmpMeshTransform = cmds.duplicate(mesh, name="TEMPORARY")[0]
    tmpMesh = cmds.listRelatives(tmpMeshTransform, shapes=True)
    tmpSkinCluster = cmds.skinCluster(jnts, tmpMeshTransform, mi=1)[0]
    cmds.copySkinWeights(ss=skinCluster, ds=tmpSkinCluster, noMirror=True, ia="oneToOne")
    cmds.skinCluster(tmpSkinCluster, e=True, mi=1)
    # skincluster always locks transforms, unlock them so you can constrain later
    misc.lock_attrs(tmpMeshTransform, unhide=True)
    
    for idx, jnt in enumerate(jnts):
        attr = '{0}.weightList[0:{1}].weights[{2}]'.format(tmpSkinCluster, vertCount, idx)
        newMeshName = "{0}Calimari_GEO".format(jnt)
        newMesh, newMeshTransform = facesFromWeightmap(attr, newMeshName, tmpMeshTransform, bias)
        cmds.parentConstraint(jnt, newMeshTransform, mo=True)

    cmds.delete(tmpMesh, tmpMeshTransform, tmpSkinCluster)
    if hide:
        cmds.setAttr(mesh + ".v", 0)

def facesFromWeightmap(weightAttribute="cluster1.weightList[0].weights", newGeoName=None, geo=None, bias=.2):
    weightlist = cmds.getAttr(weightAttribute)
    filterArray=[]
    fnMesh = misc.getOMMesh(geo)
    meshDag = misc.getDag(geo)
    allPoints = OpenMaya.MPointArray()
    fnMesh.getPoints(allPoints)
    vertices_to_delete = {}
    vertices_to_delete["points"] = OpenMaya.MPointArray()
    vertices_to_delete['indices'] = OpenMaya.MIntArray()
    for idx in range(len(weightlist)):
        if weightlist[idx] > bias:
            filterArray.append(idx)

    mesh_iter = OpenMaya.MItMeshPolygon(meshDag)
    poly_to_delete = []
    while mesh_iter.isDone() == False :
        proceed = 1
        temp_vert_ids = OpenMaya.MIntArray()
        mesh_iter.getVertices(temp_vert_ids)
        # If the vert isn't in our filter, skip the face
        for i in range(temp_vert_ids.length()):
            if temp_vert_ids[i] not in filterArray:
                proceed = 0
        if proceed:
            poly_to_delete.append(mesh_iter.index())
        next(mesh_iter)

    allPolys = OpenMaya.MIntArray()
    poly_to_delete = [x for x in range(mesh_iter.count()) if x not in poly_to_delete]
    faces = []
    newMeshTransform = cmds.duplicate(geo, name=newGeoName)[0]
    newMesh = cmds.listRelatives(newMeshTransform, shapes=True)
    for i in range(len(poly_to_delete)):
        faces.append("{0}.f[{1}]".format(newMeshTransform, poly_to_delete[i]))
    if faces:
        cmds.delete(faces)
    return newMesh, newMeshTransform


def getPointPositionByWeights(weightList, geo, threshold = .9):
    iterGeo = misc.getOMItergeo(geo)
    allPoints = OpenMaya.MPointArray()
    iterGeo.allPositions(allPoints, OpenMaya.MSpace.kWorld)
    bBox = OpenMaya.MBoundingBox()
    for idx in range(len(weightList)):
        if weightList[idx] >= threshold:
            bBox.expand(allPoints[idx])
    return bBox.height(), bBox.width(), bBox.depth(), bBox.center()

def getPointPositionBySelectedVerts():
    #!!!! use `moveManipulatorContext` to simplify this to 1 line!!!!!
    verts = cmds.ls(sl=True, fl=True)
    geo = verts[0].split(".")[0]
    verts = [int(x.split("[")[1].split("]")[0]) for x in verts]
    iterGeo = misc.getOMItergeo(geo)
    allPoints = OpenMaya.MPointArray()
    iterGeo.allPositions(allPoints, OpenMaya.MSpace.kWorld)
    bBox = OpenMaya.MBoundingBox()
    for idx in range(len(verts)):
        bBox.expand(allPoints[verts[idx]])
    return bBox.center().x, bBox.center().y, bBox.center().z
    # return bBox.height(), bBox.width(), bBox.depth(), bBox.center()


def getNodeAgnostic(name, nodeType, parent):
    if cmds.objExists(name):
        return name
    return cmds.createNode(nodeType, n=name, p=parent)


def getNodeAgnosticMultiple(names=[], nodeType=None,  parent=None):
    retNodes = []
    for name in names:
        retNodes.append(getNodeAgnostic(name=name, nodeType=nodeType, parent=parent))
    return retNodes


def availableElemCheck(multiAttrToCheck):
    availableInputElem = 0
    if multiAttrToCheck:
        allElemsConnected = 0
        availableInputElem = -1
        if not cmds.objExists(multiAttrToCheck):
            return 0
        numElements = cmds.getAttr(multiAttrToCheck, mi=True)
        if not numElements:
            return 0
        numElements = len(numElements)

        node, attr = weight_utils.extractNodeAttr(multiAttrToCheck)
        if not node:
            return 0
        for elemIdx in range(numElements):
            isConnections = False
            for child in cmds.attributeQuery(attr, node=node, lc=True):
                connections = cmds.listConnections("{0}[{1}].{2}".format(multiAttrToCheck, elemIdx, child))
                if connections:
                    isConnections = True
            # If none of the children are connected, you know the element is free to be connected to
            if not isConnections:
                availableInputElem = elemIdx
                break
        if availableInputElem == -1:
            availableInputElem = numElements

    return availableInputElem


def attrCheck(node, attrs, attrType=None, enumName=None, k=False, weightmap=False, defaultVals=[]):
    if not node:
        return
    retAttrs = []
    for idx, attr in enumerate(attrs):
        dv = 0.0
        if defaultVals:
            dv = defaultVals[idx]
        fullName = node + "." + attr
        if cmds.objExists(fullName):
            retAttrs.append(fullName)
            # update dv
            if defaultVals:
                cmds.addAttr(fullName, e=True, dv=dv)
                cmds.setAttr(fullName, dv)
            continue
        if weightmap:
            # weightMapUtils.createWeightMapOnObject(node, attr)
            weightMapUtils.createWeightMapOnSingleObject(node, attr)
        else:
            if attrType == "enum":
                cmds.addAttr(node, at=attrType, ln=attr, enumName=enumName, k=k, dv=dv)
            else:
                cmds.addAttr(node, at=attrType, ln=attr, k=k, dv=dv)

        retAttrs.append(fullName)
    return retAttrs


###################################################################################################
############################ Matrix deformer utils ################################################
###################################################################################################

def getMatrixDeformerPivotLocations(matrixDeformer=None, debug=False):
    if matrixDeformer == None:
        matrixDeformer = cmds.ls(sl=True, typ="LHMatrixDeformer")
        if matrixDeformer:
            matrixDeformer = matrixDeformer[0]
    if not matrixDeformer:
        matrixDeformer = weight_utils.getMatrixDeformerFromControl()
    elemLength = cmds.getAttr(matrixDeformer + ".inputs", s=True)
    rotations = []
    translations = []
    scales = []
    for idx in range(elemLength):
        # print cmds.getAttr(matrixDeformer + ".inputs[{0}].matrix".format(idx))
        locator = cmds.listConnections(matrixDeformer + ".inputs[{0}].matrix".format(idx))[0]
        translations.append(cmds.xform(locator, q=True, ws=True, t=True))
        rotations.append(cmds.xform(locator, q=True, ws=True, ro=True))
        scales.append(cmds.xform(locator, q=True, ws=True, s=True))
    if debug:
        print("rotations", rotations)
        print("translations", translations)
        print("scales", scales)

    return rotations, translations, scales

def getMatrixDeformerCtrlLocations(matrixDeformer=None, debug=False):
    if matrixDeformer == None:
        matrixDeformer = cmds.ls(sl=True, typ="LHMatrixDeformer")
        if matrixDeformer:
            matrixDeformer = matrixDeformer[0]
    if not matrixDeformer:
        matrixDeformer = weight_utils.getMatrixDeformerFromControl()
    ctrls = getMatrixDeformerCtrls(matrixDeformer)
    rotations = []
    translations = []
    scales = []
    for idx, ctrl in enumerate(ctrls):
        buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo = meshRivetCtrl.getRivetParts(ctrl)
        # print cmds.getAttr(matrixDeformer + ".inputs[{0}].matrix".format(idx))
        translations.append(cmds.xform(locator, q=True, ws=True, t=True))
        rotations.append(cmds.xform(locator, q=True, ws=True, ro=True))
        scales.append(cmds.xform(locator, q=True, ws=True, s=True))
    if debug:
        print("rotations", rotations)
        print("translations", translations)
        print("scales", scales)

    return rotations, translations, scales

def mirrorSelectedLocatorLToR(ctrls=None):
    if not ctrls:
        ctrls = cmds.ls(sl=True, typ="transform")
    for ctrl in ctrls:
        mirrorSelectedLocatorLToRSingle(ctrl=ctrl)

def mirrorSelectedLocatorLToRSingle(ctrl=None):
    locator = cmds.listConnections(ctrl + ".rotate")
    if not locator:
        return
    lParent = cmds.listRelatives(locator, p=True)[0]
    if not "L_" in lParent:
        return
    rParent = lParent.replace("L_", "R_")
    if not cmds.objExists(rParent):
        return
    lParentTranslate = cmds.xform(lParent, q=True, ws = True, t=True)
    rParentTranslate = [lParentTranslate[0] *-1, lParentTranslate[1], lParentTranslate[2] ]
    lParentRotate = cmds.xform(lParent, q=True, ws = True, ro=True)
    rParentRotate,rParentScale = getMirroredTransform(lParentTranslate, lParentRotate)
    cmds.xform(rParent, ws=True, ro=rParentRotate, t=rParentTranslate, s=rParentScale)

def getMirroredTransform(position, rotation):
    rootGrp  = cmds.createNode("transform", n="TEMP_ROOT_GRP")
    tmpRootJnt = cmds.joint(rootGrp, name = "ROOT", o=[0,0,0], p=[0,0,0])
    tmpJnt = cmds.joint(tmpRootJnt, name = "TEMPO", o=rotation, p=position)
    tmpFinal = cmds.mirrorJoint(tmpJnt, mirrorBehavior=True, mirrorYZ=True, sr = ["L_", "R_"])[0]
    rotate = cmds.xform(tmpFinal, q=True, ws=True, ro=True)
    scale = cmds.xform(tmpFinal, q=True, ws=True, s=True)
    cmds.delete([rootGrp, tmpRootJnt, tmpJnt, tmpFinal])
    return rotate, scale


def getMatrixDeformerCtrls(matrixDeformer=None):
    retCtrls = []
    if matrixDeformer == None:
        matrixDeformer = cmds.ls(sl=True, typ="LHMatrixDeformer")
        if matrixDeformer:
            matrixDeformer = matrixDeformer[0]
    if not matrixDeformer:
        matrixDeformer = weight_utils.getMatrixDeformerFromControl()
    shapeDict = {}
    elemLength = cmds.getAttr(matrixDeformer + ".inputs", s=True)
    for idx in range(elemLength):
        locator = cmds.listConnections(matrixDeformer + ".inputs[{0}].matrix".format(idx))[0]
        retCtrls.append(cmds.listConnections(locator + ".rotate".format(idx))[0])
    return retCtrls

def getControlShapes(matrixDeformer=None, attrConnectionToCheck=".rotate"):
    # Get the matrix deformer if arg not set
    if matrixDeformer == None:
        matrixDeformer = cmds.ls(sl=True, typ="LHMatrixDeformer")
        if matrixDeformer:
            matrixDeformer = matrixDeformer[0]
    if not matrixDeformer:
        matrixDeformer = weight_utils.getMatrixDeformerFromControl()
    shapeDict = {}
    elemLength = cmds.getAttr(matrixDeformer + ".inputs", s=True)
    for idx in range(elemLength):
        locator = cmds.listConnections(matrixDeformer + ".inputs[{0}].matrix".format(idx))[0]
        control = cmds.listConnections(locator + attrConnectionToCheck.format(idx))[0]
        shape = cmds.listRelatives(control, s=True)[0]
        shapeDict[control] = exportUtils.nurbsCurveData(name = shape, space=OpenMaya.MSpace.kObject).nurbsCurve
    print(shapeDict)
    return shapeDict


def getMatDefWeightsDict(attrsToCheck = [".rotate", ".tOut"]):
    ctrls = getMatrixDeformerCtrls()
    retWeightDict = {}
    for ctrl in ctrls:
        attrDict = {}
        for attr in attrsToCheck:
            elemIndex, weightValues, weightConObjectType, weightedMesh, weightPlug = weight_utils.getMatDefWeightInfoFromCtrl(ctrl, attr)
            if weightConObjectType != "transform" and weightConObjectType != "mesh":
                continue
            if not weightValues or not weightConObjectType or not weightedMesh or not weightPlug:
                continue
            internalWeightDict = {}
            internalWeightDict["elemIndex"] = elemIndex
            internalWeightDict["weightValues"] = weightValues
            internalWeightDict["weightConObjectType"] = weightConObjectType
            internalWeightDict["weightedMesh"] = weightedMesh
            internalWeightDict["weightPlug"] = weightPlug
            attrDict[attr] = internalWeightDict
            retWeightDict[ctrl] = attrDict
    print(retWeightDict)
    return retWeightDict

def rebuildMatDefWeightOverrides(weightDict):
    for ctrl in list(weightDict.keys()):
        # unpack from the dict
        weightName = ctrl.replace("_CTL", "_WEIGHTS")
        for attrType in list(weightDict[ctrl].keys()):

            internalWeightDict = weightDict[ctrl][attrType]
            elemIndex = internalWeightDict["elemIndex"]
            weightValues = internalWeightDict["weightValues"]
            weightConObjectType = internalWeightDict["weightConObjectType"]
            weightedMesh = internalWeightDict["weightedMesh"]
            weightPlug = internalWeightDict["weightPlug"]

            weightAttr = None
            if not cmds.objExists(weightedMesh + "." + weightName):
                weightMapUtils.createWeightMapOnSingleObject(mayaObject=weightedMesh,
                                                            weightName=weightName)
            weightAttr = weightedMesh + "." + weightName

            # set the weights
            cmds.setAttr(weightAttr, weightValues, type="doubleArray")
            cmds.connectAttr(weightAttr, weightPlug, f=True)

################################################################################################
############################ Weight Stack utils ################################################
################################################################################################


def cacheOutAllSlideDeformers(cache=True):
    # need to write a filter so you can only save out anim curve weights per component if you so choose...
    nodes = cmds.ls(type="LHSlideSimple")
    animCurves = []
    for node in nodes:
        cmds.setAttr(node + ".cacheBind", cache)


