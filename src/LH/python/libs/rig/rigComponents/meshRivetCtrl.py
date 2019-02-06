from maya import cmds
from rigComponents import base
from utils.misc import formatName, create_ctl
from utils import misc
from utils import exportUtils
from utils import faceWeights



class component(base.component):
    def __init__(self,
                 xSpeedDefault=.1,
                 ySpeedDefault=.1,
                 zSpeedDefault=.1,
                 curveData=None,
                 mesh = None,
                 **kw):
        self.xSpeedDefault = xSpeedDefault
        self.ySpeedDefault = ySpeedDefault
        self.zSpeedDefault = zSpeedDefault

        self.curveData = curveData
        super(component, self).__init__(**kw)

    def createHier(self):
        self.cmptMasterParent = cmds.createNode("transform",
                                                n=misc.formatName(self.side,
                                                                self.name,
                                                                self.suffix),
                                                ss=False)
        if self.parent and cmds.objExists(self.parent):
            cmds.parent(self.cmptMasterParent, self.parent)

    def createHelperGeo(self):
        return

    def createCtrl(self):
        self.locator = misc.createLocator(name=misc.formatName(self.side, self.name, "LOC"),
                                          parent=self.cmptMasterParent,
                                          shapeVis=False)
        self.ctrl = misc.create_ctl(side=self.side,
                                    name=self.name,
                                    parent=self.locator,
                                    shape="sphere",
                                    orient=[180, 90, 0],
                                    offset=[0, 0, 1],
                                    scale=[1, 1, 1],
                                    num_buffer=1,
                                    lock_attrs=["sx", "sy", "sz"],
                                    # lock_attrs=["tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                    gimbal=True,
                                    size=.5,
                                    nullTransform = True)

        self.ctrl = self.ctrl.ctl
        if self.curveData:
            # get Curve data for transfer
            sourceCurve = cmds.listRelatives(self.ctrl, type = "nurbsCurve")[0]
            color = cmds.getAttr(sourceCurve + ".overrideColor")
            override = cmds.getAttr(sourceCurve + ".overrideRGBColors")
            colorR = cmds.getAttr(sourceCurve + ".overrideColorR")
            colorG = cmds.getAttr(sourceCurve + ".overrideColorG")
            colorB = cmds.getAttr(sourceCurve + ".overrideColorB")
            cmds.delete(sourceCurve)
            
            # create curve
            curve = exportUtils.create_curve_2(self.curveData, self.curveData["name"], self.curveData["parent"])
            
            # transfer Curve data
            cmds.setAttr(curve.fullPathName() + ".overrideRGBColors", override)
            cmds.setAttr(curve.fullPathName() + ".overrideEnabled", True)
            cmds.setAttr(curve.fullPathName() + ".overrideColor", color)
            cmds.setAttr(curve.fullPathName() + ".overrideColorR", colorR)
            cmds.setAttr(curve.fullPathName() + ".overrideColorG", colorG)
            cmds.setAttr(curve.fullPathName() + ".overrideColorB", colorB)


    def createAttrs(self):
        inputAttrs = ["xSpeed", "ySpeed", "zSpeed"]
        for attr in inputAttrs:
            cmds.addAttr(self.ctrl, ln=attr, at="float",
                         dv=getattr(self, "{0}Default".format(attr)), k=True)

    def createNodes(self):
        misc.geoConstraint()
