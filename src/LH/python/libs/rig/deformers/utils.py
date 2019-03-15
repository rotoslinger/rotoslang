import sys
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
reload(misc)
from rig.utils import exportUtils
reload(exportUtils)
from rig.utils import weightMapUtils
reload(weightMapUtils)

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
        mesh_iter.next()

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


def nameBasedOnRange(count, name, suffixSeperator="_", suffix="", ):
    retNames = []
    midpoint = count/2
    for idx in range(count):
        current = idx
        side = "L"
        formatName = "{0}_{1}{2:02}{3}{4}"
        if idx == midpoint:
            side = "C"
            current = ""
            formatName = "{0}_{1}{2}{3}{4}"
        if idx > midpoint:
            side = "R"
            current = count -1 - idx
        # finalName = formatName.format(side, name, current, suffixSeperator, suffix)
        # if suffix is "None":
        #     finalName = finalName.replace("_None", "")
        retNames.append(formatName.format(side, name, current, suffixSeperator, suffix))
    return retNames


def createNormalizedAnimWeights(name="Temp", num=9, timeRange=20.0, suffix="ACV", offset=.15, centerWeight = .35, outerWeight = .3, angle = 50, nudge = 0,
                                intermediateVal=.2, lastAngle=0, lastIntermediateVal=.2, intermediateAngle=0, lastIntermediateAngle=0,
                                createSingleFalloff=True, singleFalloffName="Single",
                                falloffStart=-10,
                                falloffStartInner=-9,
                                falloffEndInner=9,
                                falloffEnd=10):

    keyframes = []
    falloffKeyframes = []
    ratio = timeRange/num
    midpoint = num/2
    alreadyExists = False
    for idx in range(num):
        count = idx
        side = "L"
        formatName = "{0}_{1}{2:02}_{3}"
        formatNameFalloff = "{0}_{1}Falloff{2:02}_{3}"
        if idx == midpoint:
            side = "C"
            count = ""
            formatName = "{0}_{1}{2}_{3}"
            formatNameFalloff = "{0}_{1}Falloff{2}_{3}"
        if idx > midpoint:
            side = "R"
            count = num -1 - idx
        generatedName = formatName.format(side, name, count, suffix)

        if cmds.objExists(generatedName):
            keyframes.append(generatedName)
            # Assumes the falloff also exists
            falloffName = formatNameFalloff.format(side, name, count, suffix)
            if not singleFalloffName:
                singleFalloffName = name
            if createSingleFalloff:
                falloffName = "{0}Falloff_{1}".format(singleFalloffName, suffix)
            falloffKeyframes.append(falloffName)
            # Potentially dangerous.  Assumes that if one of the curves exists, all of them exist and will skip some later steps
            # Be extremely careful when naming or this could come back to bite you!!!
            alreadyExists = True
            continue

        weightCurve = getNodeAgnostic(nodeType="animCurveTU", name=generatedName, parent=None)
        try:
            cmds.cutKey(weightCurve, cl=True, option="keys")
        except:
            pass
        keyframes.append(weightCurve)
        # Falloff V curve
        falloffName = formatNameFalloff.format(side, name, count, suffix)
        if not singleFalloffName:
            singleFalloffName = name
        if createSingleFalloff:
            falloffName = "{0}Falloff_{1}".format(singleFalloffName, suffix)
        falloffKeyframes.append(getNodeAgnostic(nodeType="animCurveTU", name=falloffName, parent=None))
        # Make sure there is at least 1 key on the curves.  Will do nothing if keyframes already exist.
        for key in range(3):
            fIdx = float(idx)
            val=1.0
            itt = "spline"
            ott = "spline"

            currLeftIntermediateVal = intermediateVal
            currRightIntermediateVal = intermediateVal

            currentLeftAngle = angle
            currentLeftIntermediateAngle = intermediateAngle
            currentRightAngle = -angle
            currentRightIntermediateAngle = -intermediateAngle

            if idx == 0:
                currentLeftAngle = lastAngle
                currentRightAngle = -angle
                currentLeftIntermediateAngle = lastIntermediateAngle
                currentRightIntermediateAngle = -intermediateAngle
                currLeftIntermediateVal = lastIntermediateVal
                currRightIntermediateVal = intermediateVal



            if idx == num-1:
                currentLeftAngle = angle
                currentRightAngle = -lastAngle
                currentLeftIntermediateAngle = intermediateAngle
                currentRightIntermediateAngle = -lastIntermediateAngle
                currLeftIntermediateVal = intermediateVal
                currRightIntermediateVal = lastIntermediateVal

            time=fIdx+key
            if key == 0:
                itt = "linear"
                ott = "slow"
                val=0.0
                time=fIdx+key + offset
                time=time+nudge

            if key == 2:
                itt = "fast"
                ott = "linear"
                val=0.0
                time=fIdx+key - offset
                time=time-nudge


            cmds.setKeyframe(weightCurve, v=val, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=time, itt=itt, ott=ott)
            time = (time,time)



            if key == 0:
                cmds.keyTangent( weightCurve, time=time, edit=True,  weightedTangents=True)
                cmds.keyTangent( weightCurve, time=time, edit=True,  lock=False)
                cmds.keyTangent( weightCurve, time=time, edit=True,  outWeight=outerWeight, inWeight=outerWeight, outAngle=currentLeftAngle,inAngle=0)

            if key == 1:
                cmds.keyTangent( weightCurve, time=time, edit=True,  weightedTangents=True)
                cmds.keyTangent( weightCurve, time=time, edit=True,  outWeight=centerWeight, inWeight=centerWeight, outAngle=0,inAngle=0)

            if key == 2:
                cmds.keyTangent( weightCurve, time=time, edit=True,  weightedTangents=True)
                cmds.keyTangent( weightCurve, time=time, edit=True,  lock=False)
                cmds.keyTangent( weightCurve, time=time, edit=True,  outWeight=outerWeight, inWeight=outerWeight, outAngle=0,inAngle=currentRightAngle)
    if alreadyExists:
        return keyframes, falloffKeyframes

    flatTime = int(time[0])
    scaleAmt = float(timeRange)/float(flatTime)
    cmds.scaleKey(keyframes,
                scaleSpecifiedKeys = False,
                timeScale = scaleAmt,
                timePivot = 0.0,
                floatScale = 1,
                floatPivot = 0.0,
                valueScale = 1,
                valuePivot = 0)

    # Center at 0
    for key in keyframes:
        cmds.keyframe(key, edit=True,relative=True,timeChange=-(timeRange/2),time=(-100,timeRange + 100))
        cmds.setKeyframe(key, breakdown=0,
                            hierarchy="none", controlPoints=2,
                            shape=0, time=-timeRange/2)
        cmds.setKeyframe(key, breakdown=0,
                            hierarchy="none", controlPoints=2,
                            shape=0, time=timeRange/2)

    cmds.select(keyframes)

    initVFalloff(falloffKeyframes,
                 falloffStart=falloffStart,
                 falloffStartInner=falloffStartInner,
                 falloffEndInner=falloffEndInner,
                 falloffEnd=falloffEnd)
    
    return keyframes, falloffKeyframes


def getNodeAgnostic(name, nodeType, parent):
    if cmds.objExists(name):
        return name
    return cmds.createNode(nodeType, n=name, p=parent)


def getNodeAgnosticMultiple(names=[], nodeType=None,  parent=None):
    retNodes = []
    for name in names:
        retNodes.append(getNodeAgnostic(name=name, nodeType=nodeType, parent=parent))
    return retNodes


def initUKeyframes(animCurves):
    for animCurve in animCurves:
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=-10)
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=0)
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=10)


def initVKeyframes(animCurves):
    for animCurve in animCurves:
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=-10)
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=10)


def initVKeyframesLinear(animCurves):
    for animCurve in animCurves:
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=-10, itt="linear")
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=9.7, itt="linear")
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=10, itt="linear")

def initVKeyframesLinearWithValues(animCurves, inTime=-5, outTime=8):
    for animCurve in animCurves:
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=-10, itt="linear")

            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=inTime, itt="linear")

            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=outTime, itt="linear")
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=10, itt="linear")

def initVFalloff(animCurves, falloffStart=-10, falloffStartInner=-5, falloffEndInner=8, falloffEnd=10):
    for animCurve in animCurves:
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=falloffStart, itt="linear", ott="linear")

            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=falloffStartInner, itt="linear", ott="linear")

            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=falloffEndInner, itt="linear", ott="linear")
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=falloffEnd, itt="linear", ott="linear")


def checkOutputWeightType(outputAttrToCheck):
    testAttr = outputAttrToCheck
    if "[" in outputAttrToCheck:
        testAttr = outputAttrToCheck.split("[")[0]
    node, attr = extractNodeAttr(testAttr)
    isMulti = cmds.attributeQuery(attr, node=node, multi=True)
    if isMulti:
        return False
    return True


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

        node, attr = extractNodeAttr(multiAttrToCheck)
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


def extractNodeAttr(fullAttrName):
    names = fullAttrName.split(".")
    node, attr = names[0], names[-1]
    return node, attr


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



