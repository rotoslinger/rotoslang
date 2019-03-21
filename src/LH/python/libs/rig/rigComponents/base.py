from maya import cmds
from rig.utils import elements, misc
from rig.utils import exportUtils

class Component(object):
    def __init__(self,
                 side="C",
                 name="component",
                 suffix="CPT",
                 curveData=None,
                 parent=None,
                 helperGeo=elements.componentNurbs,
                 ):
        """
        @param side:
        @param name:
        @param suffix:
        @param parent:
        @param helperGeo: If it already exists in scene, just give the object as an arg
                          To create, give a dictionary created from export utils
                          By default a dictionary will be selected from elements

        """

        self.side = side
        self.name = name
        self.suffix = suffix
        self.parent = parent
        self.helperGeo = helperGeo

        self.createHier()
        self.createHelperGeo()
        self.createCtrl()
        self.setControlShape()
        self.createGuide()
        self.createAttrs()
        self.preConnect()
        self.createNodes()
        self.postConnect()
        self.componentName = "component"

    def createHier(self):
        self.cmptMasterParent = cmds.createNode("transform",
                                                n=misc.formatName(self.side,
                                                             self.name,
                                                             self.suffix),
                                                ss=False)
        if self.parent and cmds.objExists(self.parent):
            cmds.parent(self.cmptMasterParent, self.parent)
        elif self.parent and not cmds.objExists(self.parent):
            self.parent = cmds.createNode("transform", n=self.parent)
            cmds.parent(self.cmptMasterParent, self.parent)

    def createHelperGeo(self):
        if type(self.helperGeo) is unicode:
            self.helperGeo = str(self.helperGeo)
        if type(self.helperGeo) is str and cmds.objExists(self.helperGeo):
            return

        self.helperGeo = misc.createGeoFromData(self.helperGeo,
                                                name=misc.formatName(self.side,
                                                                     self.name,
                                                                     "EX"),
                                                parent=self.cmptMasterParent).fullPathName()
    def addComponentTypeAttr(self, node):
        cmds.addAttr(node, ln = "componentType", dt = "string", k=False)
        cmds.setAttr(node + ".componentType", self.componentName, typ = "string", l=True)

    def createCtrl(self):
        # self.locator = misc.createLocator(name=misc.formatName(self.side, self.name, "LOC"),
        #                                   parent=self.cmptMasterParent,
        #                                   shapeVis=False)
        # self.ctrl = misc.create_ctl(side=self.side,
        #                             name=self.name,
        #                             parent=self.locator,
        #                             shape="circle",
        #                             orient=[180, 90, 0],
        #                             offset=[0, 0, 1],
        #                             scale=[1, 1, 1],
        #                             num_buffer=2,
        #                             lock_attrs=["tz", "rx", "ry", "rz", "sx", "sy", "sz"],
        #                             gimbal=True,
        #                             size=.5)
        #
        # self.buffer1 = self.ctrl.buffers[1]
        # self.buffer2 = self.ctrl.buffers[0]
        # self.ctrl = self.ctrl.ctl
        return

    def setControlShape(self):
        if self.curveData:
            # get Curve data for transfer
            sourceCurve = cmds.listRelatives(self.ctrl, type="nurbsCurve")[0]
            color = cmds.getAttr(sourceCurve + ".overrideColor")
            override = cmds.getAttr(sourceCurve + ".overrideRGBColors")
            colorR = cmds.getAttr(sourceCurve + ".overrideColorR")
            colorG = cmds.getAttr(sourceCurve + ".overrideColorG")
            colorB = cmds.getAttr(sourceCurve + ".overrideColorB")
            cmds.delete(sourceCurve)

            # create curve, set curve shape
            curve = exportUtils.create_curve_2(self.curveData, self.curveData["name"], self.curveData["parent"])

            # transfer Curve data
            cmds.setAttr(curve.fullPathName() + ".overrideRGBColors", override)
            cmds.setAttr(curve.fullPathName() + ".overrideEnabled", True)
            cmds.setAttr(curve.fullPathName() + ".overrideColor", color)
            cmds.setAttr(curve.fullPathName() + ".overrideColorR", colorR)
            cmds.setAttr(curve.fullPathName() + ".overrideColorG", colorG)
            cmds.setAttr(curve.fullPathName() + ".overrideColorB", colorB)

    def createGuide(self):
        pass

    def createAttrs(self):
        return

    def preConnect(self):
        return

    def createNodes(self):
        return

    def postConnect(self):
        return


def getComponents(componentType="componentType"):
    componentTemp = cmds.ls(et="nullTransform")
    component=[]
    for comp in componentTemp:
        parent = cmds.listRelatives(comp, parent=True)
        if not parent:
            continue
        parent = parent[0]
        if not cmds.objExists(parent + ".componentType"):
            continue
        if cmds.getAttr(parent + ".componentType") == componentType:
            component.append(comp)
    return component
