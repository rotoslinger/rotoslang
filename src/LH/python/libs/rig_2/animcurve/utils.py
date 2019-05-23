from maya import cmds, OpenMaya

from rig.utils import misc
reload(misc)
from rig_2.node import utils as node_utils
reload(node_utils)

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


def create_set_anim_curves(animCurveDictList, falloff=False):
    tag_name = "WEIGHT_CURVE"
    if falloff:
        tag_name = "FALLOFF_WEIGHT_CURVE"
    retCurves=[]
    for animCurveDict in animCurveDictList:
        newCurve = node_utils.get_node_agnostic(nodeType="animCurveTU", name=animCurveDict["name"], parent=None, tag_name=tag_name)
        setAnimCurveShape(newCurve, animCurveDict)
        retCurves.append(newCurve)
    return retCurves