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

from rig.rigComponents import meshRivetCtrl
reload(meshRivetCtrl)

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
                                falloffEnd=10,
                                itts=["linear","linear","linear","linear"],
                                otts=["linear","linear","linear","linear"],
                                falloffCurveDict=None,

):

    keyframes = []
    falloffKeyframes = []
    ratio = timeRange/num
    midpoint = num/2
    alreadyExists = False
    keyframeAlreadyExists = False
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


        #################################################################################################################
        # This is to get nodes that already exist...very bad, needs to be reworked
        if cmds.objExists(generatedName):
            keyframes.append(generatedName)
            # Assumes the falloff also exists
            falloffName = formatNameFalloff.format(side, name, count, suffix)
            if not singleFalloffName:
                singleFalloffName = name
            if createSingleFalloff:
                falloffName = "{0}Falloff_{1}".format(singleFalloffName, suffix)
            if cmds.objExists(falloffName):
                keyframeAlreadyExists = True
                # You need to create a new falloff

            falloffKeyframes.append(falloffName)
            # Potentially dangerous.  Assumes that if one of the curves exists, all of them exist and will skip some later steps
            # Be extremely careful when naming or this could come back to bite you!!!
            alreadyExists = True
            continue
        #################################################################################################################

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
    if alreadyExists and keyframeAlreadyExists:
        return keyframes, falloffKeyframes


    #################################################################################################################
    # Super bad, but need to create single falloff if doesn't already exist.  All this needs severe reworking,,,
    if alreadyExists and not keyframeAlreadyExists:
        falloffKeyframes = []
        if createSingleFalloff:
            falloffName = "{0}Falloff_{1}".format(singleFalloffName, suffix)
        falloffKeyframes.append(getNodeAgnostic(nodeType="animCurveTU", name=falloffName, parent=None))
        initVFalloff(falloffKeyframes,
                    falloffCurveDict=falloffCurveDict,
                    falloffStart=falloffStart,
                    falloffStartInner=falloffStartInner,
                    falloffEndInner=falloffEndInner,
                    falloffEnd=falloffEnd,
                    itts=itts,
                    otts=otts
                    )
        return keyframes, falloffKeyframes
    #################################################################################################################


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
                 falloffCurveDict=falloffCurveDict,
                 falloffStart=falloffStart,
                 falloffStartInner=falloffStartInner,
                 falloffEndInner=falloffEndInner,
                 falloffEnd=falloffEnd,
                 itts=itts,
                 otts=otts
                 )

    
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

def initUKeyframeAllOnes(animCurves):
    for animCurve in animCurves:
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=-10)
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=0)
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
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

def initVFalloff(animCurves, falloffCurveDict = None, falloffStart=-10, falloffStartInner=-5, falloffEndInner=8, falloffEnd=10,
                 itts=["linear","linear","linear","linear"],
                 otts=["linear","linear","linear","linear"],
                 ):
    for animCurve in animCurves:
        if falloffCurveDict:
            setAnimCurveShape(animCurve, falloffCurveDict)
            continue
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=falloffStart, itt=itts[0], ott=otts[0],
                                )

            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=falloffStartInner, itt=itts[1], ott=otts[1],)

            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=falloffEndInner, itt=itts[2], ott=otts[2],)
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=falloffEnd, itt=itts[3], ott=otts[3],)
            cmds.keyTangent( animCurve, edit=True, time=(falloffStart,falloffStart), lock=False)
            cmds.keyTangent( animCurve, edit=True, time=(falloffStartInner,falloffStartInner), lock=False)
            cmds.keyTangent( animCurve, edit=True, time=(falloffEndInner,falloffEndInner), lock=False)
            cmds.keyTangent( animCurve, edit=True, time=(falloffEnd,falloffEnd), lock=False)

            cmds.keyTangent( animCurve, edit=True,  weightedTangents=True)


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

def getAnimCurve(animCurve):
    frame_values             = []
    frame_times              = []
    weights_locked           = []
    tangents_locked          = []
    is_weighted              = []
    is_breakdown             = []
    in_x_tangents            = []
    in_y_tangents            = []
    out_x_tangents           = []
    out_y_tangents           = []
    in_tangents_type         = []
    out_tangents_type        = []
    #--- get all keys and times of frame_values
    # and num frame_values and frame range
    api_anim_curve = misc.getOMAnimCurve(animCurve)
    num_keys = api_anim_curve.numKeys()
    #---get all info for anim curve
    fn_x = OpenMaya.MScriptUtil()
    fn_x.createFromDouble(0.0)
    x = fn_x.asFloatPtr()
    fn_y = OpenMaya.MScriptUtil()
    fn_y.createFromDouble(0.0)
    y = fn_y.asFloatPtr()
    for i in range(num_keys):
        tmp_times = api_anim_curve.time(i)
        frame_times.append(tmp_times.value())
        frame_values.append(api_anim_curve.value(i))

        weights_locked.append(api_anim_curve.weightsLocked(i))
        tangents_locked.append(api_anim_curve.tangentsLocked(i))
        is_weighted.append(api_anim_curve.isWeighted())
        is_breakdown.append(api_anim_curve.isBreakdown(i))


        #get tangent types
        in_tangents_type.append(api_anim_curve.inTangentType(i))
        out_tangents_type.append(api_anim_curve.outTangentType(i))
        # get in tangents
        api_anim_curve.getTangent(i,x,y,True)
        in_x_tangents.append(OpenMaya.MScriptUtil.getFloat(x))
        in_y_tangents.append(OpenMaya.MScriptUtil.getFloat(y))
        # get out tangents
        api_anim_curve.getTangent(i,x,y,False)
        out_x_tangents.append(OpenMaya.MScriptUtil.getFloat(x))
        out_y_tangents.append(OpenMaya.MScriptUtil.getFloat(y))

    curve_dict = {"name": animCurve,
                "frame_values":     frame_values,
                "frame_times":      frame_times,
                "tangents_locked":  tangents_locked,
                "weights_locked":   weights_locked,
                "is_weighted":      is_weighted,
                "is_breakdown":     is_breakdown,
                "in_x_tangents":    in_x_tangents,
                "in_y_tangents":    in_y_tangents,
                "out_x_tangents":   out_x_tangents,
                "out_y_tangents":   out_y_tangents,
                "in_tangents_type": in_tangents_type,
                "out_tangents_type":out_tangents_type
                }
    return curve_dict

def setAnimCurveShape(animCurve, animCurveDict):
    api_anim_curve = misc.getOMAnimCurve(animCurve)

    # anim_curves = animCurveDict["name"]
    frame_values = animCurveDict["frame_values"]
    frame_times= animCurveDict["frame_times"]
    in_x_tangents= animCurveDict["in_x_tangents"]
    in_y_tangents= animCurveDict["in_y_tangents"]
    out_x_tangents= animCurveDict["out_x_tangents"]
    out_y_tangents= animCurveDict["out_y_tangents"]
    in_tangents_type= animCurveDict["in_tangents_type"]
    out_tangents_type= animCurveDict["out_tangents_type"]

    tangents_locked= animCurveDict["tangents_locked"]
    weights_locked= animCurveDict["weights_locked"]
    is_weighted= animCurveDict["is_weighted"]
    is_breakdown= animCurveDict["is_breakdown"]


    num_keys = api_anim_curve.numKeys()
    # delete any existing keys
    if num_keys>0:
        for i in range(num_keys):
            api_anim_curve.remove(api_anim_curve.numKeys()-1)
    # set keys based on args
    for i in range(len(frame_times)):
        time = OpenMaya.MTime(frame_times[i])
        index = api_anim_curve.addKey(time,
                                        frame_values[i],
                                        in_tangents_type[i],
                                        out_tangents_type[i])
        api_anim_curve.setIsWeighted(is_weighted[i])
        api_anim_curve.setWeightsLocked(i, weights_locked[i])
        api_anim_curve.setTangentsLocked(i, tangents_locked[i])
        api_anim_curve.setIsWeighted(is_weighted[i])
        api_anim_curve.setIsBreakdown(i, is_breakdown[i])



        api_anim_curve.setTangent(index,
                                    in_x_tangents[i],
                                    in_y_tangents[i],
                                    True,
                                    None,
                                    False)
        # set out tangent 0
        api_anim_curve.setTangent(index,
                                    out_x_tangents[i],
                                    out_y_tangents[i],
                                    False,
                                    None,
                                    False)
        api_anim_curve.setInTangentType(index,
                                    in_tangents_type[i])
        # set out tangent 0
        api_anim_curve.setOutTangentType(index,
                                    out_tangents_type[i])

def create_set_anim_curves(animCurveDictList):
    retCurves=[]
    for animCurveDict in animCurveDictList:
        newCurve = getNodeAgnostic(nodeType="animCurveTU", name=animCurveDict["name"], parent=None)
        setAnimCurveShape(newCurve, animCurveDict)
        retCurves.append(newCurve)
    return retCurves

###################################################################################################
############################ Matrix deformer utils ################################################
###################################################################################################

def getMatrixDeformerFromControl(ctrl=None, attrConnectionToCheck = ".rotate"):
    if not ctrl:
        ctrl = cmds.ls(sl=True, typ="transform")[0]
    locator = cmds.listConnections(ctrl + attrConnectionToCheck)
    if not locator:
        return
    locator = locator[0]
    matDef = cmds.listConnections(locator + ".worldMatrix", d=True, s=False, scn=True)
    if not matDef:
        return
    return matDef[0]

def getMatrixDeformerPivotLocations(matrixDeformer=None, debug=False):
    if matrixDeformer == None:
        matrixDeformer = cmds.ls(sl=True, typ="LHMatrixDeformer")
        if matrixDeformer:
            matrixDeformer = matrixDeformer[0]
    if not matrixDeformer:
        matrixDeformer = getMatrixDeformerFromControl()
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
        print "rotations", rotations
        print "translations", translations
        print "scales", scales

    return rotations, translations, scales

def getMatrixDeformerCtrlLocations(matrixDeformer=None, debug=False):
    if matrixDeformer == None:
        matrixDeformer = cmds.ls(sl=True, typ="LHMatrixDeformer")
        if matrixDeformer:
            matrixDeformer = matrixDeformer[0]
    if not matrixDeformer:
        matrixDeformer = getMatrixDeformerFromControl()
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
        print "rotations", rotations
        print "translations", translations
        print "scales", scales

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
        matrixDeformer = getMatrixDeformerFromControl()
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
        matrixDeformer = getMatrixDeformerFromControl()
    shapeDict = {}
    elemLength = cmds.getAttr(matrixDeformer + ".inputs", s=True)
    for idx in range(elemLength):
        locator = cmds.listConnections(matrixDeformer + ".inputs[{0}].matrix".format(idx))[0]
        control = cmds.listConnections(locator + attrConnectionToCheck.format(idx))[0]
        shape = cmds.listRelatives(control, s=True)[0]
        shapeDict[control] = exportUtils.nurbsCurveData(name = shape, space=OpenMaya.MSpace.kObject).nurbsCurve
    print shapeDict
    return shapeDict

def getMatDefElemIndexFromCtrl(ctrl=None, attrConnectionToCheck=".rotate"):
    # get the index the ctrl is connected to in the array of inputs on the matrix deformer
    if not ctrl:
        ctrl = cmds.ls(sl=True, typ="transform")[0]
    locator = cmds.listConnections(ctrl + attrConnectionToCheck)
    if not locator:
        return
    locator = locator[0]
    connection = cmds.listConnections(locator + ".worldMatrix", d=True, s=False, scn=True, plugs=True)
    if not connection:
        return
    connection= connection[0]
    if not "[" in connection:
        return
    elemIndex = int(connection.split("[")[1].split("]")[0])
    return elemIndex

def getMatDefWeightInfoFromCtrl(ctrl=None, attrConnectionToCheck=".rotate"):
    # Will return
    # elementIdex
    # weightValues
    # weightConnectionObjectType (to check whether or not the connection comes from curve weights)
    # weightedMesh
    emptyRet = None, None, None, None, None
    if not ctrl:
        ctrl = cmds.ls(sl=True, typ="transform")[0]
    elemIndex = getMatDefElemIndexFromCtrl(ctrl, attrConnectionToCheck)
    # The element index could be 0 so we need to specifically check if the return was None to see if the output was return correctly....
    if elemIndex == None:
        return emptyRet
    matDef = getMatrixDeformerFromControl(ctrl, attrConnectionToCheck)
    if not matDef:
        return emptyRet
    weightConnection = cmds.listConnections(matDef + ".inputs[{0}].matrixWeight".format(elemIndex))
    if weightConnection:
        weightConnection = weightConnection[0]
    else:
        weightConnection = None
    weightValues = cmds.getAttr(matDef + ".inputs[{0}].matrixWeight".format(elemIndex))
    weightConnectionObjectType = None
    weightedMesh = cmds.deformer(matDef, q=True ,g=True)
    if weightedMesh:
        weightedMesh = weightedMesh[0]
    weightPlug = matDef + ".inputs[{0}].matrixWeight".format(elemIndex)
    if weightConnection:
        # get the weights from the deformer input so you can add a hand weights attribute
        weightConnection = cmds.listConnections(matDef + ".inputs[{0}].matrixWeight".format(elemIndex), d=False, s=True)
        weightConnectionObjectType = cmds.objectType(weightConnection)

    return elemIndex, weightValues, weightConnectionObjectType, weightedMesh, weightPlug

    
def convertAnimCurveWeightsToHandWeights(ctrl=None, matDef=True, attrsToCheck = [".rotate", ".tOut"], weightValuesOverride=None):
    if not ctrl:
        ctrl = cmds.ls(sl=True, typ="transform")[0]

    for attr in attrsToCheck:
        if matDef:
            elemIndex, weightValues, weightConObjectType, weightedMesh, weightPlug = getMatDefWeightInfoFromCtrl(ctrl, attrConnectionToCheck=attr)
        # If the attribute is already connected to a mesh that means it is connected to hand weights and we dont need to do anything
        if weightConObjectType == "transform":
            continue
        weightName = ctrl.replace("_CTL", "_WEIGHTS")
        if not weightedMesh:
            continue
        weightAttr = None
        if not cmds.objExists(weightedMesh + "." + weightName):
            weightMapUtils.createWeightMapOnSingleObject(mayaObject=weightedMesh,
                                                        weightName=weightName)
        weightAttr = weightedMesh + "." + weightName

        if weightValuesOverride:
            weightValues = weightValuesOverride
        # set the weights
        cmds.setAttr(weightAttr, weightValues, type="doubleArray")
        cmds.connectAttr(weightAttr, weightPlug, f=True)

def getMatDefWeightsDict(attrsToCheck = [".rotate", ".tOut"]):
    ctrls = getMatrixDeformerCtrls()
    retWeightDict = {}
    for ctrl in ctrls:
        attrDict = {}
        for attr in attrsToCheck:
            elemIndex, weightValues, weightConObjectType, weightedMesh, weightPlug = getMatDefWeightInfoFromCtrl(ctrl, attr)
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
    print retWeightDict
    return retWeightDict

def rebuildMatDefWeightOverrides(weightDict):
    for ctrl in weightDict.keys():
        # unpack from the dict
        weightName = ctrl.replace("_CTL", "_WEIGHTS")
        for attrType in weightDict[ctrl].keys():

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

def getWeightStackFromCtrl(ctrl=None, attrConnectionToCheck = ".txOut"):
    if not ctrl:
        ctrl = cmds.ls(sl=True, typ="transform")[0]
    elemIndex = getWeightStackElemIndexFromCtrl(ctrl)
    weightStack = cmds.listConnections(ctrl + attrConnectionToCheck)
    if not weightStack:
        return
    return weightStack[0]

    
def getWeightStackElemIndexFromCtrl(ctrl=None, attrConnectionToCheck=".txOut"):
    # get the index the ctrl is connected to in the array of inputs on the matrix deformer
    if not ctrl:
        ctrl = cmds.ls(sl=True, typ="transform")[0]
    connection = cmds.listConnections(ctrl + attrConnectionToCheck, plugs=True)
    if not connection:
        return
    connection= connection[0]
    if not "[" in connection:
        return
    elemIndex = int(connection.split("[")[1].split("]")[0])
    return elemIndex

def getControlsFromWeightStack(weightStack=None, attrConnectionToCheck=".txOut"):
    retCtrls = []
    if weightStack == None:
        weightStack = cmds.ls(sl=True, typ="LHMatrixDeformer")
        if weightStack:
            weightStack = weightStack[0]
    if not weightStack:
        weightStack = getWeightStackFromCtrl()
    elemLength = cmds.getAttr(weightStack + ".inputs", s=True)
    for idx in range(elemLength):
        ctrl = cmds.listConnections(weightStack + ".inputs[{0}].factor".format(idx))
        if not ctrl:
            continue
        retCtrls.append(ctrl[0])
    return retCtrls


def getWeightStackInfoFromCtrl(ctrl=None, attrConnectionToCheck=".txOut"):
    # Will return
    # elementIdex
    # weightValues
    # weightConnectionObjectType (to check whether or not the connection comes from curve weights)
    # weightedMesh
    emptyRet = None, None, None, None, None, None
    if not ctrl:
        ctrl = cmds.ls(sl=True, typ="transform")[0]
    elemIndex = getWeightStackElemIndexFromCtrl(ctrl, attrConnectionToCheck)
    # The element index could be 0 so we need to specifically check if the return was None to see if the output was return correctly....
    if elemIndex == None:
        return emptyRet
    weightStack = getWeightStackFromCtrl(ctrl, attrConnectionToCheck)
    if not weightStack:
        return emptyRet
    weightConnection = cmds.listConnections(weightStack + ".inputs[{0}].inputWeights".format(elemIndex))
    weightAttribute = cmds.listConnections(weightStack + ".inputs[{0}].inputWeights".format(elemIndex), p=True)
    if weightConnection:
        weightConnection = weightConnection[0]
        weightAttribute = weightAttribute[0]
    else:
        weightConnection = None
        weightAttribute = None
    weightValues = cmds.getAttr(weightStack + ".inputs[{0}].inputWeights".format(elemIndex))
    weightConnectionObjectType = None
    weightedMesh = cmds.listConnections(weightStack + ".weightedMesh")
    if weightedMesh:
        weightedMesh = weightedMesh[0]
    weightPlug = weightStack + ".inputs[{0}].inputWeights".format(elemIndex)
    if weightConnection:
        # get the weights from the deformer input so you can add a hand weights attribute
        weightConnection = cmds.listConnections(weightStack + ".inputs[{0}].inputWeights".format(elemIndex), d=False, s=True)
        weightConnectionObjectType = cmds.objectType(weightConnection)
    return elemIndex, weightValues, weightConnectionObjectType, weightedMesh, weightPlug, weightAttribute

    
def convertWeightStackAnimCurveWeightsToHandWeights(ctrl=None, weightStack=True, attrsToCheck = [".txOut", ".tyOut"],
                                         weightValuesOverride=None, splitUDLR=False, splitSides = ["LR", "UD"]):
    if not ctrl:
        ctrl = cmds.ls(sl=True, typ="transform")[0]

    for idx, attr in enumerate(attrsToCheck):
        if weightStack:
            elemIndex, weightValues, weightConObjectType, weightedMesh, weightPlug, weightAttribute = getWeightStackInfoFromCtrl(ctrl, attrConnectionToCheck=attr)
        # If the attribute is already connected to a mesh that means it is connected to hand weights and we dont need to do anything
        if weightConObjectType == "transform":
            continue
        if not splitUDLR:
            splitSides = ""
        weightName = ctrl.replace("_CTL", "{0}_WEIGHTS".format(splitSides[idx]))
        if not weightedMesh:
            continue
        weightAttr = None
        if not cmds.objExists(weightedMesh + "." + weightName):
            weightMapUtils.createWeightMapOnSingleObject(mayaObject=weightedMesh,
                                                        weightName=weightName)
        weightAttr = weightedMesh + "." + weightName

        if weightValuesOverride:
            weightValues = weightValuesOverride
        # set the weights
        cmds.setAttr(weightAttr, weightValues, type="doubleArray")
        cmds.connectAttr(weightAttr, weightPlug, f=True)


def getWeightStackHandWeightsDict(attrsToCheck = [".txOut", ".tyOut"], splitSides = ["LR", "UD"]):
    ctrls = getControlsFromWeightStack()
    retWeightDict = {}
    for ctrl in ctrls:
        attrDict = {}
        for attr in attrsToCheck:
            elemIndex, weightValues, weightConObjectType, weightedMesh, weightPlug, weightAttribute = getWeightStackInfoFromCtrl(ctrl, attr)
            print weightPlug
            if weightConObjectType != "transform" and weightConObjectType != "mesh":
                continue
            if not weightValues or not weightConObjectType or not weightedMesh or not weightPlug:
                continue
            weightName = weightAttribute.split(".")[1]
            internalWeightDict = {}
            internalWeightDict["elemIndex"] = elemIndex
            internalWeightDict["weightName"] = weightName
            internalWeightDict["weightValues"] = weightValues
            internalWeightDict["weightConObjectType"] = weightConObjectType
            internalWeightDict["weightedMesh"] = weightedMesh
            internalWeightDict["weightPlug"] = weightPlug
            attrDict[attr] = internalWeightDict
            retWeightDict[ctrl] = attrDict
    print retWeightDict
    return retWeightDict


def rebuildSlideWeightOverrides(weightDict):
    for ctrl in weightDict.keys():
        # unpack from the dict
        # weightName = ctrl.replace("txOut", "tyOut")
        for attrType in weightDict[ctrl].keys():

            internalWeightDict = weightDict[ctrl][attrType]
            weightName = internalWeightDict["weightName"]
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
