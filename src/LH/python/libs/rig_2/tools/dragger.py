from maya import cmds
import maya.OpenMaya as OpenMaya
import maya.mel as mel


# drag = dragger.Value_Dragger(start_func = ka_weightBlender.start,
#                              change_func = ka_weightBlender.change,
#                              end_func = None)


class Value_Dragger(object):
    # You will want to set add cmds.setToolTo("valueDragger") in your hotkeys to be able to use this feature
    # value_func is a function that will be setting the values, make sure this function only has one arg and that is for a -100 to 100 range
    CONTEXTNAME = "valueDragger"
    print("NEW CONTEXT")
    def __init__(self,
                 start_func = None,
                 change_func = None,
                 end_func = None,
                 range_start = 0,
                 range_min = -100,
                 range_max = 100,
                 sensitivity=.2):
        # args
        self.start_func = start_func
        self.change_func = change_func
        self.end_func = end_func
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
    

    def clickAndMoveCommand(self):

        Context = "valueDragger"

        def getFirstClick():
            cmds.undoInfo(openChunk=True)
            
            vec = tuple(cmds.draggerContext(Context, query=1, anchorPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])

            if self.start_func:
                # self.left, self.right, self.up, self.down = self.start_func()
                self.start_func()
            # print vec[0], vec[1], vec[2]

        def getCursorPosition():
            vec = tuple(cmds.draggerContext(Context, query=1, dragPoint=1))
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])
            dotProd = OpenMaya.MVector(self.vectorStart- self.vectorEnd).normal()*(OpenMaya.MVector(-1.0, 0.0, 0.0))
            length = OpenMaya.MVector(self.vectorStart- self.vectorEnd).length()
            posNeg = -1
            if dotProd >= 0:
                posNeg = 1
            self.wt = (length * self.sensitivity)*posNeg + self.range_start
            self.wt = clamp(self.wt, self.range_min, self.range_max)
            if self.change_func:
                self.change_func(self.wt)
            cmds.refresh()

        def releaseClick():
            self.vectorStart = OpenMaya.MVector(0.0, 0.0, 0.0)
            self.wt = 0.0
            sel = cmds.ls(sl=True, fl=True)
            geo = sel[0].split(".")[0]

            if self.end_func:
                self.end_func()

            cmds.undoInfo(closeChunk=True)

        def holdCommand():
            vec = tuple(cmds.draggerContext(Context, query=1, anchorPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])



        if cmds.draggerContext(Context, exists=True):
            cmds.deleteUI(Context)

        cmds.draggerContext(Context, um="sequence", pressCommand=getFirstClick, dragCommand=getCursorPosition, name=Context,
                            cursor='crossHair', sp="screen", pr="viewPlane", rc=releaseClick)
        cmds.setToolTo(Context)

def clamp(_val, _min, _max):
    return max(min(_max, _val), _min)



