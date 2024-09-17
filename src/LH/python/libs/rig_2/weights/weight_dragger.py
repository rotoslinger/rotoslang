from maya import cmds
import maya.OpenMaya as OpenMaya
import maya.mel as mel
from rig_2.weights import self_contained_katools as ka_tools
import importlib
importlib.reload(ka_tools)
import maya.api.OpenMaya as OpenMaya

#######################################################################
##########################  SKIN WEIGHT DRAGGER #######################
#######################################################################


import sys

# from ka_rigTools import ka_weightBlender
# importlib.reload(ka_weightBlender)   

from rig_2.tools import dragger
importlib.reload(dragger)

drag = dragger.Value_Dragger(range_start = 100,
                             range_min = 0,
                             range_max = 200,
                             start_func = ka_tools.start,
                             change_func = ka_tools.change,
                             end_func = ka_tools.finish,
                             exit_func = ka_tools.restore_selection)

drag.clickAndMoveCommand()
cmds.setToolTo("selectSuperContext")
cmds.setToolTo("valueDragger")

# This class adds the dragging feature (left to right mung)
class Value_Dragger(object):
    # You will want to set add cmds.setToolTo("valueDragger") in your hotkeys to be able to use this feature
    # value_func is a function that will be setting the values, make sure this function only has one arg and that is for a -100 to 100 range
    CONTEXTNAME = "valueDragger"

    print("NEW CONTEXT")
    def __init__(self,
                 start_func = None,
                 change_func = None,
                 end_func = None,
                 exit_func = None,
                 range_start = 0,
                 range_min = -100,
                 range_max = 100,
                 sensitivity=.2):
        # args
        self.start_func = start_func
        self.change_func = change_func
        self.end_func = end_func
        self.exit_func = exit_func
        self.range_start = range_start
        self.range_min = range_min
        self.range_max = range_max
        self.sensitivity = sensitivity
        # vars
        self.weightAttr = ""
        self.vertexColorWeightVis= True
        self.toggleVisOnDrag= False
        self.originalWeightValues=""
        self.left = None
        self.right = None
        self.stored_selection = [""]
        self.selection_context = "vertex"
        self.store_selection_list()

    def clickAndMoveCommand(self):

        Context = "valueDragger"

        def getFirstClick():
            cmds.undoInfo(openChunk=True)
            self.store_selection_list()

            vec = tuple(cmds.draggerContext(Context, query=1, anchorPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])

            if self.start_func:
                self.start_func()
            # print vec[0], vec[1], vec[2]

        def getCursorPosition():
            vec = tuple(cmds.draggerContext(Context, query=1, dragPoint=1))
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])
            dotProd = OpenMaya.MVector(self.vectorStart- self.vectorEnd).normal()*(OpenMaya.MVector(-1.0, 0.0, 0.0))
            # dotProd = OpenMaya.MVector(self.vectorStart- self.vectorEnd).normal()*(OpenMaya.MVector(-1.0, 0.0, 0.0))
            length = OpenMaya.MVector(self.vectorStart- self.vectorEnd).length()
            posNeg = -1

            if dotProd >= 0:
                posNeg = 1
            
            # print "UP", self.up
            # print "DOWN", self.down
            # print "Left", self.left
            # print "Right", self.right

            # if self.left and self.right and self.left < self.right:
            #     posNeg = posNeg * -1

            self.wt = (length * self.sensitivity)*posNeg + self.range_start
            self.wt = clamp(self.wt, self.range_min, self.range_max)

            if self.change_func:
                self.change_func(self.wt)

            cmds.refresh()
            # self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])


        def releaseClick():
            self.restore_selection()
            self.vectorStart = OpenMaya.MVector(0.0, 0.0, 0.0)
            self.wt = 0.0
            sel = cmds.ls(sl=True, fl=True)
            geo = sel[0].split(".")[0]

            if self.end_func:
                self.end_func()

            cmds.undoInfo(closeChunk=True)
        def exit_context():
            self.restore_selection()
            if self.exit_func:
                self.exit_func()
            print("WHYYYYYYYYYYYYYY")

        def initialize():
            self.store_selection_list()

        def holdCommand():
            vec = tuple(cmds.draggerContext(Context, query=1, anchorPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])

        if cmds.draggerContext(Context, exists=True):
            cmds.deleteUI(Context)

        cmds.draggerContext(Context, um="sequence", pressCommand=getFirstClick, dragCommand=getCursorPosition, name=Context,
                            cursor='crossHair', sp="screen", pr="viewPlane", rc=releaseClick, finalize=exit_context, initialize=initialize)

        cmds.setToolTo(Context)

    def store_selection_list(self):
        # global stored_selection, selection_context

        self.stored_selection = cmds.ls(sl=True, fl=True)
        if "vtx" in self.stored_selection[0]:
            self.selection_context = "vertex"
        elif ".e[" in self.stored_selection[0]:
            self.selection_context = "edge"
        vertices = cmds.polyListComponentConversion(toVertex=True)
        cmds.select(vertices)
        
    def restore_selection(self):
        cmds.select(self.stored_selection)
        if self.selection_context == "vertex":
            cmds.selectMode(component=True )
            cmds.selectType(vertex=True)
            cmds.hilite(self.stored_selection[0].split(".")[0])

        if self.selection_context == "edge":
            cmds.selectMode(component=True )
            cmds.hilite(self.stored_selection[0].split(".")[0])


def clamp(_val, _min, _max):
    return max(min(_max, _val), _min)




