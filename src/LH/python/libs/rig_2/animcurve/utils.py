from maya import cmds, OpenMaya, OpenMayaAnim

from rig.utils import misc
import importlib
importlib.reload(misc)
from rig_2.node import utils as node_utils
importlib.reload(node_utils)

from rig_2 import decorator
importlib.reload(decorator)

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


def create_set_anim_curves(animCurveDictList, falloff=False, component_name=""):
    tag_name = "WEIGHT_CURVE"
    if falloff:
        tag_name = "FALLOFF_WEIGHT_CURVE"
    retCurves=[]
    for animCurveDict in animCurveDictList:
        newCurve = node_utils.get_node_agnostic(nodeType="animCurveTU",
                                                name=animCurveDict["name"],
                                                parent=None,
                                                tag_name=tag_name,
                                                component_name=component_name)
        setAnimCurveShape(newCurve, animCurveDict)
        retCurves.append(newCurve)
    return retCurves

# class mirror_anim_curves():
#     def __init__(self,
#                  anim_curve = '',
#                  side = "L",
#                  center_frame = 0,
#                  flip = False,
#                  ):
#         """
#         type  anim_curve:            list
#         param anim_curve:            anim curves     

#         type  side:                  string
#         param side:                  if "L" mirrors from timeline right to left
#                                       if "R" mirrors from timeline left to right
#                                       this happens under the assumption that you
#                                       are looking at a character's face from the
#                                       front while modifying anim curves.  In
#                                       this case "L" is referring to the left side
#                                       of the face, not the left side of the
#                                       timeline, or the screen

#         type  center_frame:          int
#         param center_frame:          the mirror axis, can be thought of as
#                                       the scale pivot

#         type  flip:                  bool
#         param flip:                  if False mirrors from left to right
#         """
#         #----args
#         self.anim_curve                   = anim_curve
#         self.side                         = side
#         self.center_frame                 = center_frame
#         self.flip                         = flip
#         #----vars
#         self.num_keys                     = 0
#         # all
#         self.api_anim_curve               = ""
#         self.all_frame_values             = []
#         self.all_frame_times              = []
#         self.all_tangents_locked            = []
#         self.all_weights_locked             = []
#         self.all_is_weighted                = []
#         self.all_is_breakdown               = []
#         self.all_in_x_tangents            = []
#         self.all_in_y_tangents            = []
#         self.all_out_x_tangents           = []
#         self.all_out_y_tangents           = []
#         self.all_in_tangents_type         = []
#         self.all_out_tangents_type        = []
#         self.all_frame_idx                = []
#         self.remove_keys                  = []
#         # side
#         self.side_frame_values            = []
#         self.side_frame_times             = []
#         self.side_tangents_locked            = []
#         self.side_weights_locked             = []
#         self.side_is_weighted                = []
#         self.side_is_breakdown               = []
#         self.side_in_x_tangents           = []
#         self.side_in_y_tangents           = []
#         self.side_out_x_tangents          = []
#         self.side_out_y_tangents          = []
#         self.side_in_tangents_type         = []
#         self.side_out_tangents_type        = []
#         self.side_frame_idx                = []
#         self.center_key                   = []

#         self.__create()

#     def get_anim_curve_info(self):
#         type = cmds.nodeType(self.anim_curve)
#         if "animCurve" in type:
#             #--- get all keys and times of all_frame_values and num all_frame_values and frame range
#             anim_curve_node = OpenMaya.MSelectionList()
#             anim_curve_node.add(self.anim_curve)
#             c_plug = OpenMaya.MPlug()
#             anim_curve_node.getPlug(0,c_plug)
#             oAnimCurve = OpenMaya.MObject()
#             oAnimCurve = c_plug.node()
#             self.api_anim_curve = OpenMayaAnim.MFnAnimCurve(oAnimCurve)
#             self.num_keys = self.api_anim_curve.numKeys()
#             if self.num_keys > 1:
#                 for i in range(self.num_keys):
#                     tmp_x = 0
#                     tmp_y = 0
#                     tmp_times = self.api_anim_curve.time(i)
#                     self.all_frame_times.append(tmp_times.value())

#             else:
#                 raise Exception( self.api_anim_curve + ''' doesn't have enough keys to mirror ''')
#                 quit()        
#         else:
#             raise Exception( self.api_anim_curve + ''' is not an anim_curve ''')
#             quit()

#     def flatten_opposite(self):
#         """zeros out all keys on the opposite side"""

#         if self.side == "L":
#             #---get all info from time greater than center frame
#             for i in range(len(self.all_frame_times)):
#                 if self.all_frame_times[i] < self.center_frame:
#                     self.remove_keys.append(self.all_frame_times[i])

#         elif self.side == "R":
#             #---get all info from time greater than center frame
#             for i in range(len(self.all_frame_times)):
#                 if self.all_frame_times[i] > self.center_frame:
#                     self.remove_keys.append(self.all_frame_times[i])

#         self.center_tolerance = -.00001
#         if self.side == "R":
#             self.center_tolerance = .00001

#         remove_idx = 0
#         if self.side == "R":
#             remove_idx = 1

#         cmds.cutKey(self.anim_curve, time = (self.center_frame + self.center_tolerance, self.remove_keys[remove_idx]))

#     def flip_keys(self):
#         """inverse scale keys"""
#         self.range = self.all_frame_times[-1]
#         if self.side == "R":
#             self.range = self.all_frame_times[0]

#         self.keyCopy = cmds.copyKey(self.anim_curve, time = (self.center_frame+self.center_tolerance, self.range))
#         cmds.scaleKey(self.anim_curve, 
#                       scaleSpecifiedKeys = True,
#                       timeScale = -1,
#                       timePivot = self.center_frame,
#                       floatScale = -1, 
#                       floatPivot = self.center_frame,
#                       valueScale = 1,
#                       valuePivot = 0)

#     def set_keys(self):
#         """sets original keys"""
#         #get index
#         if self.flip == False:
#             paste_time = self.center_frame
#             if self.side == "R":
#                 paste_time = self.all_frame_times[0]
#             cmds.pasteKey(self.anim_curve, time = (paste_time, paste_time), option="merge")

#     def __create(self):
#         """put everything together"""
#         self.get_anim_curve_info()
#         # self.get_keys_from_side()
#         self.flatten_opposite()
#         self.flip_keys()
#         self.set_keys()

class mirror_anim_curves():
    def __init__(self,
                 anim_curve = '',
                 side = "L",
                 center_frame = 0,
                 flip = False,
                 ):
        """
        type  anim_curve:            list
        param anim_curve:            anim curves     

        type  side:                  string
        param side:                  if "L" mirrors from timeline right to left
                                      if "R" mirrors from timeline left to right
                                      this happens under the assumption that you
                                      are looking at a character's face from the
                                      front while modifying anim curves.  In
                                      this case "L" is referring to the left side
                                      of the face, not the left side of the
                                      timeline, or the screen

        type  center_frame:          int
        param center_frame:          the mirror axis, can be thought of as
                                      the scale pivot

        type  flip:                  bool
        param flip:                  if False mirrors from left to right
        """
        #----args
        self.anim_curve                   = anim_curve
        self.side                         = side
        self.center_frame                 = center_frame
        self.flip                         = flip
        #----vars
        self.num_keys                     = 0
        # all
        self.api_anim_curve               = ""
        self.all_frame_values             = []
        self.all_frame_times              = []
        self.all_tangents_locked            = []
        self.all_weights_locked             = []
        self.all_is_weighted                = []
        self.all_is_breakdown               = []
        self.all_in_x_tangents            = []
        self.all_in_y_tangents            = []
        self.all_out_x_tangents           = []
        self.all_out_y_tangents           = []
        self.all_in_tangents_type         = []
        self.all_out_tangents_type        = []
        self.all_frame_idx                = []
        self.remove_keys                  = []
        # side
        self.side_frame_values            = []
        self.side_frame_times             = []
        self.side_tangents_locked            = []
        self.side_weights_locked             = []
        self.side_is_weighted                = []
        self.side_is_breakdown               = []
        self.side_in_x_tangents           = []
        self.side_in_y_tangents           = []
        self.side_out_x_tangents          = []
        self.side_out_y_tangents          = []
        self.side_in_tangents_type         = []
        self.side_out_tangents_type        = []
        self.side_frame_idx                = []
        self.center_key                   = []

        self.__create()

    def get_anim_curve_info(self):
        type = cmds.nodeType(self.anim_curve)
        if "animCurve" in type:
            #--- get all keys and times of all_frame_values and num all_frame_values and frame range
            anim_curve_node = OpenMaya.MSelectionList()
            anim_curve_node.add(self.anim_curve)
            c_plug = OpenMaya.MPlug()
            anim_curve_node.getPlug(0,c_plug)
            oAnimCurve = OpenMaya.MObject()
            oAnimCurve = c_plug.node()
            self.api_anim_curve = OpenMayaAnim.MFnAnimCurve(oAnimCurve)
            self.num_keys = self.api_anim_curve.numKeys()
            if self.num_keys > 1:
                for i in range(self.num_keys):
                    tmp_x = 0
                    tmp_y = 0
                    tmp_times = self.api_anim_curve.time(i)
                    self.all_frame_times.append(tmp_times.value())

            else:
                raise Exception( self.api_anim_curve + ''' doesn't have enough keys to mirror ''')
                quit()        
        else:
            raise Exception( self.api_anim_curve + ''' is not an anim_curve ''')
            quit()

    def flatten_opposite(self):
        """zeros out all keys on the opposite side"""

        if self.side == "L":
            #---get all info from time greater than center frame
            for i in range(len(self.all_frame_times)):
                if self.all_frame_times[i] < self.center_frame:
                    self.remove_keys.append(self.all_frame_times[i])

        elif self.side == "R":
            #---get all info from time greater than center frame
            for i in range(len(self.all_frame_times)):
                if self.all_frame_times[i] > self.center_frame:
                    self.remove_keys.append(self.all_frame_times[i])

        self.center_tolerance = -.00001
        if self.side == "R":
            self.center_tolerance = .00001

        remove_idx = 0
        if self.side == "R":
            remove_idx = 1

        cmds.cutKey(self.anim_curve, time = (self.center_frame + self.center_tolerance, self.remove_keys[remove_idx]))

    def flip_keys(self):
        """inverse scale keys"""
        self.range = self.all_frame_times[-1]
        if self.side == "R":
            self.range = self.all_frame_times[0]

        self.keyCopy = cmds.copyKey(self.anim_curve, time = (self.center_frame+self.center_tolerance, self.range))
        cmds.scaleKey(self.anim_curve, 
                      scaleSpecifiedKeys = True,
                      timeScale = -1,
                      timePivot = self.center_frame,
                      floatScale = -1, 
                      floatPivot = self.center_frame,
                      valueScale = 1,
                      valuePivot = 0)

    def set_keys(self):
        """sets original keys"""
        #get index
        if self.flip == False:
            paste_time = self.center_frame
            if self.side == "R":
                paste_time = self.all_frame_times[0]
            cmds.pasteKey(self.anim_curve, time = (paste_time, paste_time), option="merge")

    def __create(self):
        """put everything together"""
        self.get_anim_curve_info()
        # self.get_keys_from_side()
        self.flatten_opposite()
        self.flip_keys()
        self.set_keys()

def copy_flip_anim_curves(side = "L",
                          source = "",
                          target = "",
                          center_frame = 0,
                          flip = False):

        """use the option replace completely"""
        cmds.copyKey(source, o = "curve")
        if not type(target) == list:
            target = [target]
        for t in target:
            cmds.pasteKey(t, o = "replaceCompletely")
            if flip == True:
                cmds.scaleKey(t, 
                            scaleSpecifiedKeys = True,
                            timeScale = -1,
                            timePivot = center_frame,
                            floatScale = -1, 
                            floatPivot = center_frame,
                            valueScale = 1,
                            valuePivot = 0)

@decorator.undo_chunk
def mirrorAnimCurve(side="R"):
    curves = cmds.ls(sl=True, typ="animCurveTU")[0]
    mirror_anim_curves(anim_curve=curves,
                       side=side,
                       flip=False
                       )

@decorator.undo_chunk
def copyAnimCurve():
    # Select source and then destination anim curve, then run this function
    curves = cmds.ls(sl=True, typ="animCurveTU")
    copy_flip_anim_curves(
                          source = curves[0],
                          target = curves[0:]
                          )

@decorator.undo_chunk
def copyFlipAnimCurve(side="L"):
    # Select source and then destination anim curve, then run this function
    curves = cmds.ls(sl=True, typ="animCurveTU")
    copy_flip_anim_curves(side=side,
                          source = curves[0],
                          target = curves[1],
                          flip=True
                          )
