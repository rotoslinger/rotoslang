import os, json, ast
from maya import cmds, OpenMaya

from rig_2.animcurve import utils as animcurve_utils
import importlib
importlib.reload(animcurve_utils)

from rig_2.node import utils as node_utils
importlib.reload(node_utils)
from rig_2.tag import utils as tag_utils

from rig.utils import misc
from rig.utils import weightMapUtils

importlib.reload(misc)
from rig.utils import exportUtils
importlib.reload(exportUtils)
from rig.utils import weightMapUtils
importlib.reload(weightMapUtils)

from rig.rigComponents import meshRivetCtrl
importlib.reload(meshRivetCtrl)

from rig_2.attr import utils as attr_utils
importlib.reload(attr_utils)



def tag_selected_weight_curves_no_export(add, weight_curve_checkbox, falloff_weight_curve_checkbox):
    curve_nodes = []
    for sel in cmds.ls(sl=True):
        if ((cmds.objExists(sel + ".WEIGHT_CURVE") and weight_curve_checkbox)
            or
            (cmds.objExists(sel + ".FALLOFF_WEIGHT_CURVE") and falloff_weight_curve_checkbox)):
            curve_nodes.append(sel)
    tag_utils.no_export_add_remove_selector(curve_nodes, add)

def tag_all_no_export(do_weight_curve, do_falloff_weight_curve, do_hand_painted_weights):
    tag_utils.tag_no_export_from_control_connection_dict(add=True,
                                                         weight_curves=do_weight_curve,
                                                         falloff_weight_curves=do_falloff_weight_curve,
                                                         hand_painted_weights=do_hand_painted_weights
                                                        )
    tag_selected_weight_curves_no_export(True, weight_curve_checkbox=do_weight_curve, falloff_weight_curve_checkbox=do_falloff_weight_curve)

def remove_tag_all_no_export(do_weight_curve, do_falloff_weight_curve, do_hand_painted_weights):
    tag_utils.tag_no_export_from_control_connection_dict(add=False,
                                                         weight_curves=do_weight_curve,
                                                         falloff_weight_curves=do_falloff_weight_curve,
                                                         hand_painted_weights=do_hand_painted_weights
                                                        )
    tag_selected_weight_curves_no_export(False, weight_curve_checkbox=do_weight_curve, falloff_weight_curve_checkbox=do_falloff_weight_curve)


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
                                component_name="",
                                auto_create_reverse = False,


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
        if auto_create_reverse:
            side = "R"
        formatName = "{0}_{1}{2:02}_{3}"
        formatNameFalloff = "{0}_{1}Falloff{2:02}_{3}"
        if idx == midpoint:
            side = "C"
            count = ""
            formatName = "{0}_{1}{2}_{3}"
            formatNameFalloff = "{0}_{1}Falloff{2}_{3}"
        if idx > midpoint:
            side = "R"
            if auto_create_reverse:
                side = "L"
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

        weightCurve = node_utils.get_node_agnostic(nodeType="animCurveTU", name=generatedName, parent=None, tag_name="WEIGHT_CURVE", component_name=component_name)
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
        falloffKeyframes.append(node_utils.get_node_agnostic(nodeType="animCurveTU", name=falloffName, parent=None, tag_name="FALLOFF_WEIGHT_CURVE", component_name=component_name))
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
        falloffKeyframes.append(node_utils.get_node_agnostic(nodeType="animCurveTU", name=falloffName, parent=None, tag_name="FALLOFF_WEIGHT_CURVE", component_name=component_name))
        animcurve_utils.initVFalloff(falloffKeyframes,
                     falloffCurveDict=falloffCurveDict,
                     falloffStart=falloffStart,
                     falloffStartInner=falloffStartInner,
                     falloffEndInner=falloffEndInner,
                     falloffEnd=falloffEnd,
                     itts=itts,
                     otts=otts
                     )
        if createSingleFalloff:
            # make sure same number of falloffs as other curves
            falloffKeyframes = [falloffName for x in range(num)]
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

    animcurve_utils.initVFalloff(falloffKeyframes,
                 falloffCurveDict=falloffCurveDict,
                 falloffStart=falloffStart,
                 falloffStartInner=falloffStartInner,
                 falloffEndInner=falloffEndInner,
                 falloffEnd=falloffEnd,
                 itts=itts,
                 otts=otts
                 )


    return keyframes, falloffKeyframes


def checkOutputWeightType(outputAttrToCheck):
    testAttr = outputAttrToCheck
    if "[" in outputAttrToCheck:
        testAttr = outputAttrToCheck.split("[")[0]
    node, attr = extractNodeAttr(testAttr)
    isMulti = cmds.attributeQuery(attr, node=node, multi=True)
    if isMulti:
        return False
    return True


def extractNodeAttr(fullAttrName):
    names = fullAttrName.split(".")
    node, attr = names[0], names[-1]
    return node, attr


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
                                         weightValuesOverride=None, splitUDLR=True, splitSides = ["LR", "UD"]):
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
    return retWeightDict


def rebuildSlideWeightOverrides(weightDict):
    for ctrl in list(weightDict.keys()):
        # unpack from the dict
        # weightName = ctrl.replace("txOut", "tyOut")
        for attrType in list(weightDict[ctrl].keys()):

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


def getAllAnimCurveWeightNodeCurves():
    # need to write a filter so you can only save out anim curve weights per component if you so choose...
    nodes = cmds.ls(type="LHCurveWeightNode_2")
    animCurves = []
    for node in nodes:
        elemLength = cmds.getAttr(node + ".inputs", s=True)
        for elemIdx in range(elemLength):
            animCurveU = cmds.listConnections(node + ".inputs[{0}].animCurveU".format(elemIdx))
            if animCurveU:
                animCurves.append(animCurveU[0])
            animCurveV = cmds.listConnections(node + ".inputs[{0}].animCurveV".format(elemIdx))
            if animCurveV:
                animCurves.append(animCurveV[0])
    return animCurves

def get_all_weight_anim_curves(no_export_check=True):
    weight_curves = tag_utils.get_weight_curves() 
    falloff_weight_curves =  tag_utils.get_falloff_weight_curves()
    if not no_export_check:
        return weight_curves, falloff_weight_curves
    # Remove the weight curves that have been tagged no export
    weight_curves = tag_utils.remove_nodes_with_tags_from_list("NO_EXPORT", weight_curves)
    falloff_weight_curves = tag_utils.remove_nodes_with_tags_from_list("NO_EXPORT", falloff_weight_curves)
    return weight_curves, falloff_weight_curves

def get_weight_curves_dict(no_export_dict, do_weight_curves=True, do_falloff_weight_curves=True,):
    # get all animCurveWeightsNodes
    weight_curves, falloff_weight_curves = get_all_weight_anim_curves()
    # put all animCurves in a dict
    weight_curve_dict = {}
    falloff_weight_curve_dict = {}
    if do_weight_curves:
        for curve in weight_curves:
            if curve in list(no_export_dict.keys()) and "NO_EXPORT" in no_export_dict[curve]:
                continue
            weight_curve_dict[curve] = animcurve_utils.getAnimCurve(curve)

    if do_falloff_weight_curves:
        for curve in falloff_weight_curves:
            if curve in list(no_export_dict.keys()) and "NO_EXPORT" in no_export_dict[curve]:
                continue
            falloff_weight_curve_dict[curve] = animcurve_utils.getAnimCurve(curve)
    
    return weight_curve_dict, falloff_weight_curve_dict


def rebuildAnimCurveWeightsCurves(no_export_tag_dict,
                                  weight_curve_dict,
                                  falloff_weight_curve_dict,
                                  weight_curves=True,
                                  falloff_weight_curves=True):

    if weight_curves and weight_curve_dict:
        for curve in list(weight_curve_dict.keys()):
            if curve in list(no_export_tag_dict.keys()) and "NO_EXPORT" in no_export_tag_dict[curve]:
                continue
            if not cmds.objExists(curve):
                print(curve + " Does not exist anymore, will not be able to set it")
                continue
            animcurve_utils.setAnimCurveShape(curve, weight_curve_dict[curve])

    if falloff_weight_curves and falloff_weight_curve_dict:
        for curve in list(falloff_weight_curve_dict.keys()):
            if curve in list(no_export_tag_dict.keys()) and "NO_EXPORT" in no_export_tag_dict[curve]:
                continue
            if not cmds.objExists(curve):
                print(curve + " Does not exist anymore, will not be able to set it")
                continue
            animcurve_utils.setAnimCurveShape(curve, falloff_weight_curve_dict[curve])

def removeAllCurveWeightsNodes():
    nodes = cmds.ls(type="LHCurveWeightNode_2")
    animCurves = []
    for node in nodes:
        cmds.delete(node)

def get_all_hand_painted_weight_attrs(filter_type="mesh"):
    full_name_attrs = []
    weighted_meshes = []
    attrs = []
    connects = []
    weight_values=[]
    
    for mesh in cmds.ls(type="mesh"):
        all_attrs = cmds.listAttr(mesh, userDefined=True, a=True)
        if not all_attrs:
            continue
        for attr in all_attrs:
            full_attr_name = mesh + "." + attr
            attr_type = cmds.addAttr(full_attr_name, q=True, dt=True)[0]
            if attr_type != "doubleArray":
                continue
            weight_values.append(cmds.getAttr(full_attr_name))
            connects.append(cmds.listConnections(full_attr_name, p=True, d=True))
            full_name_attrs.append(full_attr_name)
            weighted_meshes.append(mesh)
            attrs.append(attr)
    return weighted_meshes, attrs, full_name_attrs, connects, weight_values

def get_hand_painted_weight_dict():
    hand_painted_weights_dict = {}
    weighted_meshes, attrs, full_name_attrs, connects, weight_values = get_all_hand_painted_weight_attrs()
    for idx, full_name_attr in enumerate(full_name_attrs):
        mesh_dict = {}
        mesh_dict["node"] = weighted_meshes[idx]
        mesh_dict["attr"] = attrs[idx]
        # mesh_dict["full_name_attr"] = full_name_attrs[idx]
        mesh_dict["connects"] = connects[idx]
        mesh_dict["weight_values"] = weight_values[idx]
        hand_painted_weights_dict[full_name_attr] = mesh_dict
    return hand_painted_weights_dict

def rebuild_hand_painted_weights(weight_dict):
    for full_name_attr in list(weight_dict.keys()):
        # if not cmds.objExists(full_name_attr):
        #     print "The final connection for the weights attribute "+ full_name_attr + " Does not exist, unable to add hand weights."
        #     continue

        mesh_dict = weight_dict[full_name_attr]
        # full_name_attr=mesh_dict["full_name_attr"]
        connections = mesh_dict["connects"]
        
        if not cmds.objExists(mesh_dict["node"]):
            print("Geo named " + mesh_dict["node"] + " Does not exist, unable to add hand weights.")
            continue
        
        attr_utils.get_attr(node=mesh_dict["node"], attr=mesh_dict["attr"], weightmap=True)
        # Make sure no incoming connections before setting the weight values
        if not cmds.listConnections(full_name_attr, s=True, d=False):
            cmds.setAttr(full_name_attr, mesh_dict["weight_values"], typ="doubleArray")
        # Have the appropriate connections been made?
        # if cmds.listConnections(full_name_attr, p=True, d=True) != connections:
        if not connections:
            continue
        for connection in connections:
            if not cmds.objExists(connection):
                print("The connecting attribute " + connection + " does not exist.  The connection of " + full_name_attr + " to " + connection + " could not be made.")
                continue
            cmds.connectAttr(full_name_attr, connection, f=True)

        
def export_all(filename, weight_curves=True, falloff_weight_curves=True, hand_painted_weights=True):
    export_dict = {}
    no_export_tag_dict = tag_utils.get_no_exports()
    export_dict["no_export_tag_dict"] = no_export_tag_dict
    weight_curve_dict, falloff_weight_curve_dict = get_weight_curves_dict(do_weight_curves=weight_curves, do_falloff_weight_curves=falloff_weight_curves)

    export_dict["weight_curves"] = weight_curve_dict
    export_dict["falloff_weight_curves"] = falloff_weight_curve_dict

    export_dict["hand_painted_weights"] = {}
    if hand_painted_weights:
        export_dict["hand_painted_weights"] = get_hand_painted_weight_dict()

    # Make sure the path exists
    path = os.path.dirname(os.path.normpath(filename))
    if not os.path.exists(path):
        os.mkdir(path)

    file = open(filename, "wb")
    json.dump(export_dict, file, sort_keys = False, indent = 4)
    file.close()
    return export_dict

def import_all(filename, weight_curves=True, falloff_weight_curves=True, hand_painted_weights=True):
    file = open(filename, "rb")
    import_dict = json.load(file)
    file.close()

    no_export_tag_dict = import_dict["no_export_tag_dict"]

    # Set NO_EXPORT tags
    tag_utils.set_tags_from_dict(no_export_tag_dict)
    rebuildAnimCurveWeightsCurves(weight_curve_dict=import_dict["weight_curves"],
                                  falloff_weight_curve_dict=import_dict["falloff_weight_curves"],
                                  weight_curves=weight_curves,
                                  falloff_weight_curves=falloff_weight_curves)

    if hand_painted_weights:
        rebuild_hand_painted_weights(import_dict["hand_painted_weights"])

def convert_selected_curve_to_hand_weights():
    sorted_ctrls = tag_utils.control_from_selected()
    for ctrl in sorted_ctrls:
        convert_control_to_painted_weights(ctrl)

def convert_control_to_painted_weights(ctrl):
        controls, curve_names, curve_weights, weight_stacks, output_indices, hand_weights = tag_utils.get_connection_weight_data(ctrl,
                                                                                                                     connection_attr_name="weight_curve_connection_dicts")
        convert_curve_data_to_painted_weights(ctrl=ctrl, elemIndicies=output_indices, weight_stacks=weight_stacks, curve_names=curve_names)

def convert_curve_data_to_painted_weights(ctrl, elemIndicies, weight_stacks, curve_names):
    for idx, curve in enumerate(curve_names):
        weightValues, weightConObjectType, weightedMesh, weightPlug, weightAttribute = get_weight_data_from_ctrl(ctrl, elemIndicies[idx], weight_stacks[idx])
        # If the attribute is already connected to a mesh that means it is connected to hand weights and we dont need to do anything
        if weightConObjectType == "transform" or not weightedMesh:
            continue
        weightName = curve.replace("_ACV", "_WEIGHTS")
        weightAttr = None
        if not cmds.objExists(weightedMesh + "." + weightName):
            attr_utils.get_attr(node=weightedMesh, attr=weightName, weightmap=True)
            # weightMapUtils.createWeightMapOnSingleObject(mayaObject=weightedMesh,
            #                                             weightName=weightName)
            # Once the weightmap exists, add it to the connection dicts on the control so they can be tagged if the user specifies
            attr_utils.add_to_string_array_dict_at_index(ctrl + ".weight_curve_connection_dicts",
                                                         idx, "hand_weights",
                                                         weightedMesh + "." + weightName)
            attr_utils.add_to_string_array_dict_at_index(ctrl + ".falloff_weight_curve_connection_dicts",
                                                         idx, "hand_weights",
                                                         weightedMesh + "." + weightName)
            attr_utils.add_to_string_array_dict_at_index(string_array_attr = ctrl + ".weight_curve_connection_dicts",
                                                         index=idx,
                                                         dictionary_key ="geo_shape",
                                                         dictionary_value= weightedMesh)
            attr_utils.add_to_string_array_dict_at_index(string_array_attr = ctrl + ".falloff_weight_curve_connection_dicts",
                                                         index=idx,
                                                         dictionary_key="geo_shape",
                                                         dictionary_value=weightedMesh)
        weightAttr = weightedMesh + "." + weightName
        # set the weights
        cmds.setAttr(weightAttr, weightValues, type="doubleArray")
        cmds.connectAttr(weightAttr, weightPlug, f=True)

def get_weight_data_from_ctrl(ctrl, elemIndex, weight_stack):
    # Will return
    # weightValues
    # weightConnectionObjectType (to check whether or not the connection comes from curve weights)
    # weightedMesh
    weightConnection = None
    weightAttribute = None
    if cmds.objectType(weight_stack) == "LHWeightNode":
        plug_name = "inputWeights"
    elif cmds.objectType(weight_stack) == "LHMatrixDeformer":
        plug_name = "matrixWeight"
        # weightConnection = cmds.listConnections(weight_stack + ".inputs[{0}].matrixWeight".format(elemIndex))
        # weightAttribute = cmds.listConnections(weight_stack + ".inputs[{0}].matrixWeight".format(elemIndex), p=True)
        # weightValues = cmds.getAttr(weight_stack + ".inputs[{0}].matrixWeight".format(elemIndex))


    weightConnection = cmds.listConnections(weight_stack + ".inputs[{0}].{1}".format(elemIndex, plug_name))
    weightAttribute = cmds.listConnections(weight_stack + ".inputs[{0}].{1}".format(elemIndex, plug_name), p=True)
    weightValues = cmds.getAttr(weight_stack + ".inputs[{0}].{1}".format(elemIndex, plug_name))


    if weightConnection:
        weightConnection = weightConnection[0]
        weightAttribute = weightAttribute[0]
    else:
        weightConnection = None
        weightAttribute = None

    weightConnectionObjectType = None
    if cmds.objectType(weight_stack) == "LHWeightNode":
        weightedMesh = cmds.listConnections(weight_stack + ".weightedMesh")
    elif cmds.objectType(weight_stack) == "LHMatrixDeformer":
        weightedMesh = cmds.deformer(weight_stack, q=True, geometry=True)
    if weightedMesh:
        weightedMesh = weightedMesh[0]
    weightPlug = weight_stack + ".inputs[{0}].{1}".format(elemIndex, plug_name)
    if weightConnection:
        # get the weights from the deformer input so you can add a hand weights attribute
        weightConnection = cmds.listConnections(weight_stack + ".inputs[{0}].{1}".format(elemIndex, plug_name), d=False, s=True)
        weightConnectionObjectType = cmds.objectType(weightConnection)
    return weightValues, weightConnectionObjectType, weightedMesh, weightPlug, weightAttribute

def cache_all_curve_weights(cache=True):
    nodes = cmds.ls(type="LHCurveWeightNode_2")
    for node in nodes:
        cmds.setAttr(node + ".cacheWeightMesh", cache)

def cache_all_slide_deformers(cache=True):
    nodes = cmds.ls(type="LHSlideSimple")
    for node in nodes:
        cmds.setAttr(node + ".cacheBind", cache)
