# import math, sys
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.OpenMayaAnim as OpenMayaAnim


#===============================================================================
#CLASS:         mirror_anim_curves
#DESCRIPTION:   mirrors anim curves
#USAGE:         give list of anim curves
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          Oct. 14th, 2014
#Version        1.0.0
#===============================================================================

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
##############################################
#Example:
# mirror_anim_curves(anim_curve = 'L_innUDVU_ACV')
###############################################

#===============================================================================
#CLASS:         mirror_anim_curves
#DESCRIPTION:   copies from one anim curve to another and flips to the opposite
#               side
#USAGE:         give list of anim curves
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          Oct. 14th, 2014
#Version        1.0.0
#===============================================================================

class copy_flip_anim_curves():
    def __init__(self,
                 side = "L",
                 source = "",
                 target = "",
                 center_frame = 0,
                 flip = False
                 ):
        """
        type  side:                  string
        param side:                  the side you are copying from
        
        type  source:                string
        param source:                the curve to copy from

        type  target:           string
        param target:           the curve to copy to

        type  center_frame:          int
        param center_frame:          the mirror axis, can be thought of as
                                      the scale pivot

        type  flip:                  bool
        param flip:                  if false only a regular copy is done
        """
        #----args
        self.side                         = side
        self.source                       = source
        self.target                  = target
        self.center_frame                 = center_frame
        self.flip                         = flip
        
        self.__create()

    def check(self):
        # makes sure source and target are anim curves
        for i in [self.source, self.target]:
            type = cmds.nodeType(i)
            if "animCurve" in type:
                continue
            else:
                raise Exception( i + ''' is not an anim_curve ''')
                quit()

    def copy_anim_curve(self):
        """use the option replace completely"""
        cmds.copyKey(self.source, o = "curve")
        cmds.pasteKey(self.target, o = "replaceCompletely")

    def flip_dest(self):
        """use the option replace completely"""
        if self.flip == True:
            cmds.scaleKey(self.target, 
                        scaleSpecifiedKeys = True,
                        timeScale = -1,
                        timePivot = self.center_frame,
                        floatScale = -1, 
                        floatPivot = self.center_frame,
                        valueScale = 1,
                        valuePivot = 0)

    def __create(self):
        """put everything together"""
        self.check()
        self.copy_anim_curve()
        self.flip_dest()

def mirrorAnimCurve(side="R"):
    curves = cmds.ls(sl=True, typ="animCurveTU")[0]
    mirror_anim_curves(anim_curve=curves,
                       side=side,
                       flip=False
                       )

def copyAnimCurve(side="L"):
    # Select source and then destination anim curve, then run this function
    curves = cmds.ls(sl=True, typ="animCurveTU")
    copy_flip_anim_curves(side=side,
                          source = curves[0],
                          target = curves[1]
                          )

def copyFlipAnimCurve(side="L"):
    # Select source and then destination anim curve, then run this function
    curves = cmds.ls(sl=True, typ="animCurveTU")
    copy_flip_anim_curves(side=side,
                          source = curves[0],
                          target = curves[1],
                          flip=True
                          )
