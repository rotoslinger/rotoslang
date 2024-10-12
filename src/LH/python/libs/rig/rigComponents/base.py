from maya import cmds

from rig.utils import misc
from rig.utils import exportUtils
from rig_2.manipulator import control, elements
import importlib
importlib.reload(control)
importlib.reload(elements)
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)
from rig_2.node import utils as node_utils
importlib.reload(node_utils)
from rig_2.shape import nurbscurve
importlib.reload(nurbscurve)

from rig_2.manipulator import elements as manipulator_elements
importlib.reload(manipulator_elements)


from rig_2.manipulator import elements as manip_elements
importlib.reload(manip_elements)

class Component(object):
    def __init__(self,
                 side="C",
                 name="component",
                 suffix="CPT",
                 worldInverseNodes=[],
                 curveData=None,
                 parent=None,
                 helperGeo=elements.circle,
                 numBuffer=2,
                 orient=[0, 0, 0],
                 offset=[0, 0, 0],
                 shapeScale=[1, 1, 1],
                 lockAttrs=[],
                #  lock_attrs=["sx", "sy", "sz"],
                 gimbal=True,
                 size=1,
                 translate = None,
                 rotate = None,
                 scale = None,
                 selection=False,
                 createJoint=False,
                 nullTransform = False,
                 component_name = "",
                 is_ctrl_guide = False,
                 do_guide = False,
                 ):
        """
        param side:
        param name:
        param suffix:
        param parent:
        param helperGeo: If it already exists in scene, just give the object as an arg
                          To create, give a dictionary created from export utils
                          By default a dictionary will be selected from elements
        """
        self.component_name = component_name
        self.side = side
        self.name = name
        self.suffix = suffix
        if not curveData:
             self.curveData = elements.circle,
        else: self.curveData = curveData


        self.parent = parent
        self.helperGeo = helperGeo
        self.numBuffer = numBuffer
        self.orient = orient
        self.offset = offset
        self.shapeScale = shapeScale
        self.lockAttrs = lockAttrs
        self.gimbal = gimbal
        self.size = size
        self.do_guide = do_guide

        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        self.createJoint = createJoint
        self.nullTransform = nullTransform
        self.is_ctrl_guide = is_ctrl_guide
        if not self.translate and not self.rotate and not self.scale and selection:
            sel = cmds.ls(sl=True)[0]
            self.translate = cmds.xform(sel, q=True, t=True, ws=True)
            self.rotate = cmds.xform(sel, q=True, ro=True, ws=True)
            self.scale = cmds.xform(sel, q=True, s=True,ws=True)

        if not self.translate:
            self.translate = [0,0,0]
        if not self.rotate:
            self.rotate = [0,0,0]
        if not self.scale:
            self.scale = [1,1,1]


    def createHier(self):
        self.cmptMasterParent = node_utils.get_node_agnostic("transform",
                                                             name=misc.formatName(self.side,
                                                                                  self.name,
                                                                                  self.suffix),
                                                             parent = self.parent
                                                             )
        # self.cmptMasterParent = cmds.createNode("transform",
        #                                         n=misc.formatName(self.side,
        #                                                      self.name,
        #                                                      self.suffix),
        #                                         ss=False)
        # if self.parent and cmds.objExists(self.parent):
        #     cmds.parent(self.cmptMasterParent, self.parent)
        # elif self.parent and not cmds.objExists(self.parent):
        #     self.parent = cmds.createNode("transform", n=self.parent)
        #     cmds.parent(self.cmptMasterParent, self.parent)

    def createHelperGeo(self):
        if type(self.helperGeo) is str:
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
        self.locator = misc.formatName(self.side, self.name, "LOC")
        if not cmds.objExists(self.locator):
            self.locator = misc.createLocator(name=misc.formatName(self.side, self.name, "LOC"),
                                            parent=self.cmptMasterParent,
                                            shapeVis=False)
            
        self.ctrl = control.Ctrl(side=self.side,
                                                name=self.name,
                                                parent=self.locator,
                                                # shape=shape,
                                                shape_dict=self.curveData,
                                                orient=self.orient,
                                                offset=self.offset,
                                                scale=self.shapeScale,
                                                num_buffer=self.numBuffer,
                                                lock_attrs=self.lockAttrs,
                                                gimbal=self.gimbal,
                                                size=self.size,
                                                null_transform=self.nullTransform,
                                                guide=self.is_ctrl_guide)
        self.ctrl.create()



        self.buffers = self.ctrl.buffers
        reversedBuffers = self.ctrl.buffers[::-1]
        # create self.buffer in decending order going further away from the control, ascending goes opposite...
        # -buffer02
        #   -buffer01
        #     -buffer00
        #       -ctrl
        for idx, buff in enumerate(reversedBuffers):
            setattr(self, "buffer{0:02}".format(idx), buff)
        self.buffersAscending = reversedBuffers
        self.buffersDecending = self.ctrl.buffers
        self.ctrl = self.ctrl.ctrl
        tag_utils.create_component_tag(self.ctrl, self.component_name)

    def createJoints(self):
        if not self.createJoint:
            return
        self.joint=cmds.joint(self.ctrl, p=self.translate, orientation=self.rotate, scale=self.scale, name = "{0}_{1}_JNT".format(self.side, self.name))
        cmds.setAttr(self.joint + ".visibility", 0)
        cmds.addAttr(self.joint, ln = "BIND",
                            at = "bool",)
        cmds.setAttr(self.joint+".BIND", True,
                        l = True,
                        k=False, )

    def setControlShape(self):
        return
        # if self.curveData:
        #     # get Curve data for transfer
        #     sourceCurve = cmds.listRelatives(self.ctrl, type="nurbsCurve")[0]
        #     color = cmds.getAttr(sourceCurve + ".overrideColor")
        #     override = cmds.getAttr(sourceCurve + ".overrideRGBColors")
        #     colorR = cmds.getAttr(sourceCurve + ".overrideColorR")
        #     colorG = cmds.getAttr(sourceCurve + ".overrideColorG")
        #     colorB = cmds.getAttr(sourceCurve + ".overrideColorB")
        #     cmds.delete(sourceCurve)

        #     # create curve, set curve shape
        #     curve = exportUtils.create_curve_2(self.curveData, self.curveData["name"], self.curveData["parent"])

        #     # transfer Curve data
        #     cmds.setAttr(curve.fullPathName() + ".overrideRGBColors", override)
        #     cmds.setAttr(curve.fullPathName() + ".overrideEnabled", True)
        #     cmds.setAttr(curve.fullPathName() + ".overrideColor", color)
        #     cmds.setAttr(curve.fullPathName() + ".overrideColorR", colorR)
        #     cmds.setAttr(curve.fullPathName() + ".overrideColorG", colorG)
        #     cmds.setAttr(curve.fullPathName() + ".overrideColorB", colorB)

    # def createGuide(self):
    #     pass
    def createGuide(self):
        if not self.numBuffer >= 2 or not self.do_guide:
            return
        # The guide is really just the buffer above the rivet.  This creates a shape for that buffer for easier selection
        self.guide_transform, self.guideShapes = nurbscurve.create_curve(manipulator_elements.sphere_small,
                                                                        self.buffer01,
                                                                         self.buffer01,
                                                                         transform_suffix=None,
                                                                         check_existing=False,
                                                                         outliner_color=False,
                                                                         color=False,
                                                                         shape_name="{0}_{1}".format(self.side, self.name))

        tag_utils.tag_guide(self.guide_transform)
        tag_utils.create_component_tag(self.guide_transform, self.component_name)

        for guide_shape in self.guideShapes:
            tag_utils.tag_guide_shape(guide_shape)
            tag_utils.create_component_tag(guide_shape, self.component_name)
            # Set the default visibility of the guide
            cmds.setAttr(guide_shape + ".v", 0)
        self.guideShape = self.guideShapes[0]

    def createAttrs(self):
        return

    def setDefaultLocation(self):
        misc.move(self.locator, self.translate, self.rotate, self.scale)

    def preConnect(self):
        return


    def createNodes(self):
        return

    def postConnect(self):
        return

    def create(self):

        self.createHier()
        self.createHelperGeo()
        self.createCtrl()
        self.createJoints()
        self.setControlShape()
        self.createGuide()
        self.createAttrs()
        self.setDefaultLocation()
        self.preConnect()
        self.createNodes()
        self.postConnect()
        self.componentName = "component"

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
