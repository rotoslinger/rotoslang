from maya import cmds
from rigComponents import base
reload(base)
from rig.utils.misc import formatName, create_ctl
from rig.utils import misc
from rig.utils import exportUtils
from rig.utils import faceWeights
import elements


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
                 **kw):
        super(Component, self).__init__(**kw)

        self.speedTxDefault = speedTxDefault
        self.speedTyDefault = speedTyDefault
        self.speedTzDefault = speedTzDefault
        self.curveData = curveData
        self.mesh = mesh
        # self.translate = translate
        # self.rotate = rotate
        # self.scale = scale
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
        # if not self.translate and not self.rotate and not self.scale and selection:
        #     sel = cmds.ls(sl=True)[0]
        #     self.translate = cmds.xform(sel, q=True, t=True, ws=True)
        #     self.rotate = cmds.xform(sel, q=True, ro=True, ws=True)
        #     self.scale = cmds.xform(sel, q=True, s=True,ws=True)

        self.nullTransform=True
        #self.suffix="MRC"

    def createHelperGeo(self):
        return

    def createCtrl(self):
        super(Component, self).createCtrl()
        self.buffer1 = self.buffers[1]
        self.buffer2 = self.buffers[0]

    def createGuide(self):
        if self.guide:
            self.guideShape = exportUtils.create_curve_2(elements.sphereSmall, "{0}_{1}_SHP".format(self.side, self.name), self.buffer2)

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

    # def preConnect(self):
    #     misc.move(self.locator, self.translate, self.rotate, self.scale)
        # misc.move(self.buffer2, self.translate, self.rotate, self.scale)
        # if self.mirror:
        #     cmds.xform(self.cmptMasterParent, ws=True, s=[-1,1,1])

        #     # cmds.setAttr(self.cmptMasterParent + ".sx", -1)
        #     cmds.refresh()

    def createNodes(self):
        self.geoConstraint = misc.geoConstraint(driverMesh = self.mesh, driven = self.locator, parent = self.cmptMasterParent,
                                                name = "{0}_{1}_GCS".format(self.side, self.name), translate=True, rotate=False,
                                                scale=False, offsetBuffer = self.buffer2, maintainOffsetT=True, 
                                                maintainOffsetR=True, maintainOffsetS=True, normalConstraintPatch=self.normalConstraintPatch)
        # self.geoConstraint = misc.geoConstraint(driverMesh = self.mesh, driven = self.locator, parent = self.cmptMasterParent,
        #                                         name = "{0}_{1}_GCS".format(self.side, self.name), translate=True, rotate=True,
        #                                         scale=True, offsetBuffer = self.buffer2, maintainOffsetT=True, 
        #                                         maintainOffsetR=True, maintainOffsetS=True, normalConstraintPatch=None)

        # make the geo constraint much easier to find on the guide
        cmds.addAttr(self.buffer2, ln = "geoConstraint", at = "message")
        cmds.connectAttr(self.geoConstraint + ".message", self.buffer2 + ".geoConstraint")


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
    return dict(zip(sourceWeightNames,sourceAttrs))

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
