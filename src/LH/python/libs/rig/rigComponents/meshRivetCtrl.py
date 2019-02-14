from maya import cmds
from rigComponents import base
from rig.utils.misc import formatName, create_ctl
from rig.utils import misc
from rig.utils import exportUtils
from rig.utils import faceWeights
import elements


class component(base.component):
    def __init__(self,
                 speedTxDefault=.1,
                 speedTyDefault=.1,
                 speedTzDefault=.1,
                 curveData=None,
                 mesh = None,
                 translate = None,
                 rotate = None,
                 scale = None,
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
                 selection=False,
                 mirror=False,

                 **kw):

        self.speedTxDefault = speedTxDefault
        self.speedTyDefault = speedTyDefault
        self.speedTzDefault = speedTzDefault
        self.curveData = curveData
        self.mesh = mesh
        self.translate = translate
        self.rotate = rotate
        self.scale = scale
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

        if not self.translate and not self.rotate and not self.scale and selection:
            sel = cmds.ls(sl=True)[0]
            self.translate = cmds.xform(sel, q=True, t=True, ws=True)
            self.rotate = cmds.xform(sel, q=True, ro=True, ws=True)
            self.scale = cmds.xform(sel, q=True, s=True,ws=True)


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
                                    num_buffer=2,
                                    lock_attrs=["sx", "sy", "sz"],
                                    # lock_attrs=["tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                    gimbal=True,
                                    size=.5,
                                    nullTransform = True)
        self.buffer1 = self.ctrl.buffers[1]
        self.buffer2 = self.ctrl.buffers[0]
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

    def preConnect(self):
        misc.move(self.locator, self.translate, self.rotate, self.scale)
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
    outU = cmds.listConnections(ctrl + "." + attr, d=True, p=True, t="LHSlideDeformer", et=True)[0]
    if not outU:
        return
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

def mirrorSlidingCtrls(mayaObjects=None, mirrorWeights=False, guide=False, normalConstraintPatch="C_mouthSurface_EX", geo="C_body_HI", flip=False):
    if not mayaObjects: mayaObjects = cmds.ls(sl=True)
    for ctrl in mayaObjects:
        # Get name and side of selected control
        side=""
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
        if not inU:
            continue
        inV = findOppositeSlideConnection(ctrl, "tyOut")
        if not inV:
            continue

        # Find Surface

        # surf = cmds.listConnections(ctrl + ".currentU", d=True, t="pointOnSurfaceInfo", et=True)[0]
        # nurbs = cmds.listConnections(surf + ".inputSurface", s=True, t="nurbsSurface", et=True)[0]

        # Create component with Opposite side and opposite attributes
        # slideComponent = component(name=name, side=side, helperGeo = nurbs, uOutConnectionAttr = inU, vOutConnectionAttr = inV)

        # Get opposite side
        locator = cmds.listRelatives(ctrl, f=True, p=True)[0]
        locator = cmds.listRelatives(locator,f=True, p=True)[0]
        locator = cmds.listRelatives(locator,f=True, p=True)[0]
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


        rivetComponent = component(name=name, guide=guide, side=side, normalConstraintPatch = normalConstraintPatch,
        txConnectionAttr = inU, tyConnectionAttr = inV, mesh = geo, selection=False, mirror=True, translate=translate, rotate=rotate, scale=scale)

        # Set the location and the attributes

        for attr in attrs:
            cmds.setAttr(rivetComponent.ctrl + attr, attrsDict[ctrl + attr])

        # Copy Curve shape, then mirror curve shape
        misc.pushCurveShape(ctrl, rivetComponent.ctrl, mirror=True, inheritColor=True)
        if flip:
            speedTx = cmds.getAttr(rivetComponent.ctrl + ".speedTx")
            cmds.setAttr(rivetComponent.ctrl + ".speedTx", speedTx * -1.0)
                # if self.mirror:

        #     # cmds.setAttr(self.cmptMasterParent + ".sx", -1)
        #     cmds.refresh()


        # misc.updateGeoConstraint(offsetBuffer = rivetComponent.buffer2)
        # uMirror = cmds.getAttr(ctrl + ".baseU")
        # if uMirror < .5:
        #     uMirror = abs(uMirror-0.5)
        #     uMirror = .5 + uMirror
        # elif uMirror > .5:
        #     uMirror = uMirror-0.5
        #     uMirror = .5 - uMirror
        # for uAttr in (".baseU", ".initU"):
        #     cmds.setAttr(slideComponent.ctrl + uAttr, uMirror)

        # # Normalize Control
        # normalizeSlidingCtrls([slideComponent.ctrl])

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