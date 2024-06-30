from maya import cmds

from rig_2.message import utils as message_utils
import importlib
importlib.reload(message_utils)
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)
from rig.rigComponents import base
importlib.reload(base)
from rig.utils import misc
importlib.reload(misc)
from rig.utils import exportUtils
importlib.reload(exportUtils)
from rig.utils import faceWeights
importlib.reload(faceWeights)
from . import elements
importlib.reload(elements)
from rig_2.shape import nurbscurve
importlib.reload(nurbscurve)

from rig_2.manipulator import elements as manipulator_elements
importlib.reload(manipulator_elements)

from rig_2.node import utils as node_utils
importlib.reload(node_utils)

class Component(base.Component):
    def __init__(self,
                # Inherited Attrs
                #  side="C",
                #  name="component",
                #  suffix="CPT",
                #  worldInverseNodes=[],
                #  curveData=None,
                #  parent=None,
                #  helperGeo=elements.componentNurbs,
                #  numBuffer=2,
                #  orient=[0, 0, 0],
                #  offset=[0, 0, 0],
                #  shapeScale=[1, 1, 1],
                #  lock_attrs=[],
                # #  lock_attrs=["sx", "sy", "sz"],
                #  gimbal=True,
                #  size=1,
                #  translate = None,
                #  rotate = None,
                #  scale = None,
                #  selection=False,
                #  createJoint=False,
                #  nullTransform = False

                 speedTxDefault=.1,
                 speedTyDefault=.1,
                 speedTzDefault=.1,
                 curveData=None,
                 mesh = None,

                 guide = False,
                 
                 txConnectionAttr=None,
                 tyConnectionAttr=None,
                 tzConnectionAttr=None,

                 rxConnectionAttr=None,
                 ryConnectionAttr=None,
                 rzConnectionAttr=None,

                 sxConnectionAttr=None,
                 syConnectionAttr=None,
                 szConnectionAttr=None,

                 normalConstraintPatch=None,

                 mirror=False,
                 component_name="",
                 **kw):
        super(Component, self).__init__(**kw)
        self.component_name = component_name

        self.speedTxDefault = speedTxDefault
        self.speedTyDefault = speedTyDefault
        self.speedTzDefault = speedTzDefault
        self.curveData = curveData
        self.mesh = mesh
        self.componentName = "meshRivetCtrl"
        self.guide = guide

        self.txConnectionAttr = txConnectionAttr
        self.tyConnectionAttr = tyConnectionAttr
        self.tzConnectionAttr = tzConnectionAttr

        self.rxConnectionAttr = rxConnectionAttr
        self.ryConnectionAttr = ryConnectionAttr
        self.rzConnectionAttr = rzConnectionAttr

        self.sxConnectionAttr = sxConnectionAttr
        self.syConnectionAttr = syConnectionAttr
        self.szConnectionAttr = szConnectionAttr
        self.normalConstraintPatch = normalConstraintPatch
        self.mirror = mirror

        self.nullTransform=True

    def createHelperGeo(self):
        return

    def createCtrl(self):
        super(Component, self).createCtrl()
        self.buffer1 = self.buffers[1]
        self.buffer2 = self.buffers[0]

    def createGuide(self):
        # The guide is really just the buffer above the rivet.  This creates a shape for that buffer for easier selection
        self.guide_transform, self.guideShapes = nurbscurve.create_curve(manipulator_elements.sphere_small,
                                                                            self.buffer2,
                                                                         self.buffer2,
                                                                         transform_suffix=None,
                                                                         check_existing=False,
                                                                         outliner_color = False,
                                                                         color = False,
                                                                         shape_name = "{0}_{1}".format(self.side, self.name))

        tag_utils.tag_guide(self.guide_transform)
        tag_utils.create_component_tag(self.guide_transform, self.component_name)

        for guide_shape in self.guideShapes:
            tag_utils.tag_guide_shape(guide_shape)
            tag_utils.create_component_tag(guide_shape, self.component_name)
            # Set the default visibility of the guide
            if not self.guide:
                cmds.setAttr(guide_shape + ".v", 0)
        self.guideShape = self.guideShapes[0]

    def createAttrs(self):
        inputAttrs = ["speedTx", "speedTy", "speedTz"]
        for attr in inputAttrs:
            cmds.setAttr(self.ctrl + "." + attr, getattr(self, "{0}Default".format(attr)))
        for node in self.cmptMasterParent, self.ctrl, self.locator, self.buffer1, self.buffer2:
            self.addComponentTypeAttr(node)
            cmds.addAttr(node, ln = "root", at = "message")
            cmds.connectAttr(self.cmptMasterParent + ".message", node + ".root")
        cmds.addAttr(self.cmptMasterParent, ln = "control", at = "message")
        cmds.connectAttr(self.ctrl + ".message", self.cmptMasterParent + ".control")
        cmds.addAttr(self.cmptMasterParent, ln = "transform", at = "message")
        cmds.connectAttr(self.buffer2 + ".message", self.cmptMasterParent + ".transform")
        
        message_utils.create_message_attr_setup(self.cmptMasterParent, "guide", self.guide_transform, "master")
        message_utils.create_message_attr_setup(self.ctrl, "guide", self.guide_transform, "ctrl")
        
        message_utils.create_message_attr_setup(self.cmptMasterParent, "guide_shape", self.guideShape, "master")
        message_utils.create_message_attr_setup(self.ctrl, "guide_shape", self.guideShape, "ctrl")

        tag_utils.create_tag(self.guide_transform, "RIVET_GUIDE")
        tag_utils.tag_rivet_mesh(self.mesh)
        tag_utils.create_component_tag(self.guide_transform, self.component_name)
        tag_utils.create_component_tag(self.guideShape, self.component_name)

    def createNodes(self):
        # self.geoConstraint = misc.geoConstraint(driverMesh = self.mesh, driven = self.locator, parent = self.cmptMasterParent,
        #                                         name = "{0}_{1}_GCS".format(self.side, self.name), translate=True, rotate=True,
        #                                         scale=True, offsetBuffer = self.buffer2, maintainOffsetT=True, 
        #                                         maintainOffsetR=True, maintainOffsetS=True, normalConstraintPatch=None)
        self.up_vector_object = node_utils.get_locator(name = "{0}_{1}_UpVector".format(self.side, self.name), parent = self.cmptMasterParent)
        cmds.setAttr(self.up_vector_object + ".v", 0)
        tag_utils.tag_rivet_mesh(self.mesh)
        if self.component_name:
            tag_utils.create_component_tag(self.mesh, component_name=self.component_name)
        self.geoConstraint = misc.geoConstraint(driverMesh = self.mesh, driven = self.locator, parent = self.cmptMasterParent,
                                                name = "{0}_{1}_GCS".format(self.side, self.name),
                                                translate=True,
                                                rotate=False,
                                                scale=False,
                                                offsetBuffer = self.buffer2,
                                                maintainOffsetT=True, 
                                                maintainOffsetR=True,
                                                maintainOffsetS=True,
                                                normalConstraintPatch=self.normalConstraintPatch,
                                                up_vector_object=self.up_vector_object,
                                                up_vector=[0,1,0],
                                                up_vec_mult=100)

        driverAttributes = ["txOut", "tyOut", "tzOut",
                            "rx", "ry", "rz",
                            "sx", "sy", "sz"]
        for idx, attr in enumerate([self.txConnectionAttr, self.tyConnectionAttr, self.tzConnectionAttr,
                                   self.rxConnectionAttr, self.ryConnectionAttr, self.rzConnectionAttr,
                                   self.sxConnectionAttr, self.syConnectionAttr, self.szConnectionAttr]):
            if not attr:
                continue
            cmds.connectAttr("{0}.{1}".format(self.ctrl, driverAttributes[idx]), attr, f=True)

def updateWithGeoConstraint():
    cmds.addAttr(cmds.ls(sl=True)[0], ln = "geoConstraint", at = "message")
    cmds.connectAttr(cmds.ls(sl=True)[1] + ".message", cmds.ls(sl=True)[0] + ".geoConstraint")
    
def findOppositeSlideConnection(ctrl, attr):
    outU = cmds.listConnections(ctrl + "." + attr, d=True, p=True, t="LHSlideDeformer", et=True)
    if not outU:
        return
    outU = outU[0]
    outUAttrShort = outU.split(".")[1]
    deformer = outU.split(".")[0]
    if not "L_" and not "R_" in outUAttrShort:
        return
    if "L_" in outUAttrShort:
        outUAttrShort = outUAttrShort.replace("L_", "R_")
    elif "R_" in outUAttrShort:
        outUAttrShort = outUAttrShort.replace("R_", "L_")

    if cmds.objExists(deformer + "." + outUAttrShort):
        return deformer + "." + outUAttrShort

def mirrorSlidingCtrls(mayaObjects=None, mirrorWeights=False, guide=False, normalConstraintPatch=None, geo=None, flip=False, flipAll=False):
    if not mayaObjects: mayaObjects = cmds.ls(sl=True)
    for ctrl in mayaObjects:
        # Get name and side of selected control
        side=""
        if not normalConstraintPatch or not geo:
            buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo = getRivetParts(ctrl)
        if not "L_" and not "R_" in ctrl:
            continue
        if "L_" in ctrl:
            side = "R"
        if "R_" in ctrl:
            side = "L"
        name = ctrl.split("_")[1]
        # Get location of control and all attributes
        attrsDict = {}
        attrs = (".speedTx",".speedTy", ".speedTz", ".rotateOrder", ".vis", ".gimbal_vis")
        for attr in attrs:
            attrsDict[ctrl + attr] = cmds.getAttr(ctrl + attr)
        # Get connected attributes, find L to R, or R to L depending on what is selected
        inU = findOppositeSlideConnection(ctrl, "txOut")
        # if not inU:
        #     continue
        inV = findOppositeSlideConnection(ctrl, "tyOut")
        # if not inV:
        #     continue

        # Find Surface

        # surf = cmds.listConnections(ctrl + ".currentU", d=True, t="pointOnSurfaceInfo", et=True)[0]
        # nurbs = cmds.listConnections(surf + ".inputSurface", s=True, t="nurbsSurface", et=True)[0]

        # Create component with Opposite side and opposite attributes
        # slideComponent = component(name=name, side=side, helperGeo = nurbs, uOutConnectionAttr = inU, vOutConnectionAttr = inV)

        # Get opposite side
        # locator = cmds.listRelatives(ctrl, f=True, p=True)[0]
        # locator = cmds.listRelatives(locator,f=True, p=True)[0]
        # locator = cmds.listRelatives(locator,f=True, p=True)[0]
        translate = cmds.xform(locator, q=True, t=True, ws=True)
        rotate = cmds.xform(locator, q=True, ro=True, ws=True)
        scale = cmds.xform(locator, q=True, s=True,ws=True)
        
        rotate = [rotate[0], rotate[1]+180.0, rotate[2]]

        dummyParent = cmds.createNode("transform")
        dummy = cmds.createNode("transform", p=dummyParent)

        misc.move(dummy, translate, rotate, None)

        cmds.xform(dummyParent, ws=True, s=[-1,1,1])
        translate = cmds.xform(dummy, q=True, t=True, ws=True)
        rotate = cmds.xform(dummy, q=True, ro=True, ws=True)

        cmds.delete(dummy, dummyParent)


        # cmds.xform(self.cmptMasterParent, ws=True, s=[-1,1,1])
        rivetCtrl = "{0}_{1}_CTL".format(side, name)
        if not cmds.objExists("{0}_{1}_CPT".format(side, name)):
            rivetComponent = Component(name=name, guide=guide, side=side, normalConstraintPatch = normalConstraintGeo,
                                    txConnectionAttr = inU, tyConnectionAttr = inV, mesh = mesh, selection=False, mirror=True, translate=translate, rotate=rotate, scale=scale)
            rivetComponent.create()
        # Set the location and the attributes

        for attr in attrs:
            cmds.setAttr(rivetCtrl + attr, attrsDict[ctrl + attr])

        # Copy Curve shape, then mirror curve shape
        misc.pushCurveShape(ctrl, rivetCtrl, mirror=True, inheritColor=True)
        if flip:
            speedTx = cmds.getAttr(rivetCtrl + ".speedTx")
            cmds.setAttr(rivetCtrl + ".speedTx", speedTx * -1.0)
                # if self.mirror:
        if flipAll:
            speedTx = cmds.getAttr(rivetCtrl + ".speedTx")
            cmds.setAttr(rivetCtrl + ".speedTx", speedTx * -1.0)
            speedTx = cmds.getAttr(rivetCtrl + ".speedTy")
            cmds.setAttr(rivetCtrl + ".speedTy", speedTx * -1.0)
            speedTx = cmds.getAttr(rivetCtrl + ".speedTz")
            cmds.setAttr(rivetCtrl + ".speedTz", speedTx * -1.0)


def getSlideWeightAttrNames(attrName):
    splitName = attrName.split(".")
    deformer = splitName[0]
    attr = splitName[1]
    weights = "{0}Weight".format(attr)
    animCurve = "{0}_ACV".format(attr)
    animCurveFalloff = "{0}Falloff_ACV".format(attr)
    return weights, animCurve, animCurveFalloff

def getSide(name):
    return name.split("_")[0]

def cacheSlideDeformer(deformer, val):
    cmds.setAttr(deformer + ".cacheWeights", val)
    cmds.setAttr(deformer + ".cacheWeightMesh", val)
    cmds.setAttr(deformer + ".cacheWeightCurves", val)

def copyFlipSlideAnimCurves(side, flip, source, target):
    faceWeights.copy_flip_anim_curves(side = side, 
                                      center_frame = 0, 
                                    flip = flip,
                                    source = source,
                                    target = target)

def getWeightAttributes(deformerName):
    sourceAttrs = cmds.listAttr(deformerName, 
                    ud = True, 
                    a = True,
                    m=True)

    sourceWeightNames = []
    for i in range(len(sourceAttrs)):
        tmp_name = sourceAttrs[i].split(".")
        sourceWeightNames.append(tmp_name[1])
    return dict(list(zip(sourceWeightNames,sourceAttrs)))

def getRivetParts(ctrl):
    buffer1 = cmds.listRelatives(ctrl, p=True)[0]
    buffer2 = cmds.listRelatives(buffer1, p=True)[0]
    locator = cmds.listRelatives(buffer2, p=True)[0]
    root = cmds.listRelatives(locator, p=True)[0]

    # Will Likely need to be replaced when we come up with a better way of constraining the up vector
    normalConstraint = cmds.listConnections(locator + ".rx")
    normalConstraintGeo = None
    if normalConstraint:
        normalConstraintGeo = cmds.listConnections(normalConstraint[0] + ".target[0].targetGeometry")
        if normalConstraintGeo:
            normalConstraintGeo = normalConstraintGeo[0]
    geoConstraint = cmds.listConnections(buffer2 + ".geoConstraint")[0]
    mesh = cmds.listConnections(geoConstraint + ".inMesh", sh=True)[0]
    return buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo

def rivetGuidesVis(vis=False):
    controls = base.getComponents("meshRivetCtrl")
    for control in controls:
        buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo = getRivetParts(control)
        guideShape = cmds.listRelatives(buffer2, s=True)
        if not guideShape:
            return
        cmds.setAttr(guideShape[0] + ".v", vis)
