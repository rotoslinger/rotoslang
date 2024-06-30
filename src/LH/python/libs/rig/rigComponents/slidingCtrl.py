from maya import cmds
from rig.rigComponents import base

from rig.control import base as control_base
from rig.utils.misc import formatName
from rig.control import base as control_base
import importlib
importlib.reload(control_base)
from rig.utils import misc
from rig.utils import exportUtils
from rig.utils import faceWeights


class Component(base.Component):
    def __init__(self,
                 uSpeedDefault=.05,
                 vSpeedDefault=.05,
                 initUDefault=0.5,
                 initVDefault=0.5,
                 baseUDefault=0.5,
                 baseVDefault=0.5,
                 amountUDefault=1.1,
                 amountVDefault=2.4,
                 uOutConnectionAttr="",
                 vOutConnectionAttr="",
                 curveData=None,
                 **kw):
        super(Component, self).__init__(**kw)
        self.uSpeedDefault = uSpeedDefault
        self.vSpeedDefault = vSpeedDefault
        self.initUDefault = initUDefault
        self.initVDefault = initVDefault
        self.baseUDefault = baseUDefault
        self.baseVDefault = baseVDefault
        self.amountUDefault = amountUDefault
        self.amountVDefault = amountVDefault
        self.uOutConnectionAttr = uOutConnectionAttr
        self.vOutConnectionAttr = vOutConnectionAttr
        self.curveData = curveData
        self.componentName = "slidingCtrl"


    def createCtrl(self):
        self.locator = misc.createLocator(name=misc.formatName(self.side, self.name, "LOC"),
                                          parent=self.cmptMasterParent,
                                          shapeVis=False)
        self.ctrl = control_base.create_ctl(side=self.side,
                                                name=self.name,
                                                parent=self.locator,
                                                shape="circle",
                                                orient=[180, 90, 0],
                                                offset=[0, 0, 1],
                                                scale=[1, 1, 1],
                                                num_buffer=2,
                                                lock_attrs=["tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                                gimbal=True,
                                                size=.5)

        # self.buffer1 = self.ctrl.buffers[1]
        # self.buffer2 = self.ctrl.buffers[0]
        #
        self.ctrlOffset = self.ctrl.buffers[0]
        self.ctrlInverseMatrix = self.ctrl.buffers[1]
        self.ctrl = self.ctrl.ctl
        # if self.curveData:
        #     # get Curve data for transfer
        #     sourceCurve = cmds.listRelatives(self.ctrl, type = "nurbsCurve")[0]
        #     color = cmds.getAttr(sourceCurve + ".overrideColor")
        #     override = cmds.getAttr(sourceCurve + ".overrideRGBColors")
        #     colorR = cmds.getAttr(sourceCurve + ".overrideColorR")
        #     colorG = cmds.getAttr(sourceCurve + ".overrideColorG")
        #     colorB = cmds.getAttr(sourceCurve + ".overrideColorB")
        #     cmds.delete(sourceCurve)
        #
        #     # create curve
        #     curve = exportUtils.create_curve_2(self.curveData, self.curveData["name"], self.curveData["parent"])
        #
        #     # transfer Curve data
        #     cmds.setAttr(curve.fullPathName() + ".overrideRGBColors", override)
        #     cmds.setAttr(curve.fullPathName() + ".overrideEnabled", True)
        #     cmds.setAttr(curve.fullPathName() + ".overrideColor", color)
        #     cmds.setAttr(curve.fullPathName() + ".overrideColorR", colorR)
        #     cmds.setAttr(curve.fullPathName() + ".overrideColorG", colorG)
        #     cmds.setAttr(curve.fullPathName() + ".overrideColorB", colorB)



    def createAttrs(self):
        inputAttrs = ["uSpeed", "vSpeed", "initU", "initV", "baseU", "baseV", "amountU", "amountV"]
        outputAttrs = ["currentU", "currentV", "outU", "outV", ]
        for attr in inputAttrs:
            setattr(self, attr, "{0}.{1}".format(self.ctrl, attr))

            cmds.addAttr(self.ctrl, ln=attr, at="float",
                         dv=getattr(self, "{0}Default".format(attr)), k=True)
        for attr in outputAttrs:
            setattr(self, attr, "{0}.{1}".format(self.ctrl, attr))
            cmds.addAttr(self.ctrl, ln=attr, at="double",
                         dv=0.0, k=True)


    def createNodes(self):
        #---invert the matrix of the control
        self.decomposeMatrix = misc.createAndConnectNode("decomposeMatrix",
                                                         name=misc.formatName(self.side,
                                                                              self.name + "DecomposeCtrl",
                                                                              "DMX"),
                                                         selfOutput="outputTranslate",
                                                         dstInput="{0}.{1}".format(self.ctrlInverseMatrix, "translate"))

        self.inverseMatrix = misc.createAndConnectNode("inverseMatrix",
                                                       name=misc.formatName(self.side,
                                                                            self.name + "InvertCtrl",
                                                                            "IMX"),
                                                       srcOutput="{0}.{1}".format(self.ctrl, "xformMatrix"),
                                                       selfInput="inputMatrix",
                                                       selfOutput="outputMatrix",
                                                       dstInput="{0}.{1}".format(self.decomposeMatrix, "inputMatrix")
                                                       )
        #--Combine UVSpeed and init
        #---Multuply by the speed first
        self.multNode = cmds.createNode("multiplyDivide", name=misc.formatName(self.side,
                                                                               "{0}{1}".format(self.name, "MultCtrl"),
                                                                               "MTD"))
        cmds.setAttr("{0}.operation".format(self.multNode), 1)
        cmds.connectAttr(self.ctrl + ".translateX", self.multNode + ".input1X")
        cmds.connectAttr(self.ctrl + ".translateY", self.multNode + ".input1Y")
        cmds.connectAttr(self.ctrl + ".uSpeed", self.multNode + ".input2X")
        cmds.connectAttr(self.ctrl + ".vSpeed", self.multNode + ".input2Y")
        #---Add the offset in for nuetral pose
        self.pmaNode = cmds.createNode("plusMinusAverage", name=misc.formatName(self.side,
                                                                                "{0}{1}".format(self.name, "AddCtrl"),
                                                                                "PMA"))
        cmds.setAttr("{0}.operation".format(self.multNode), 1)
        cmds.connectAttr(self.multNode + ".outputX", self.pmaNode + ".input2D[0].input2Dx")
        cmds.connectAttr(self.multNode + ".outputY", self.pmaNode + ".input2D[0].input2Dy")
        #---We want to clamp between 0 and 1 because this is the limit of nurbs UVs
        cmds.connectAttr(self.ctrl + ".initU", self.pmaNode + ".input2D[1].input2Dx")
        cmds.connectAttr(self.ctrl + ".initV", self.pmaNode + ".input2D[1].input2Dy")
        #---We want to clamp between 0 and 1 because this is the limit of nurbs UVs
        self.clampNode = cmds.createNode("clamp", name=misc.formatName(self.side,
                                                                       "{0}{1}".format(self.name, "ClampCtrl"),
                                                                       "CLP"))
        cmds.setAttr(self.clampNode + ".maxR", 1)
        cmds.setAttr(self.clampNode + ".maxG", 1)

        cmds.connectAttr(self.pmaNode + ".output2Dx", self.clampNode + ".inputR")
        cmds.connectAttr(self.pmaNode + ".output2Dy", self.clampNode + ".inputG")
        #---Wire the output back into the ctrl,
        cmds.connectAttr(self.clampNode + ".outputR", self.currentU)
        cmds.connectAttr(self.clampNode + ".outputG", self.currentV)

        #---Get info from the nurbs
        self.surfaceInfo = cmds.createNode("pointOnSurfaceInfo",
                                           name=misc.formatName(self.side,
                                                                self.name + "SurfaceInfo",
                                                                "SFI"),
                                           )
        cmds.connectAttr(self.currentU, self.surfaceInfo + ".parameterU")
        cmds.connectAttr(self.currentV, self.surfaceInfo + ".parameterV")
        cmds.connectAttr(self.helperGeo + ".worldSpace[0]", self.surfaceInfo + ".inputSurface")

        #---Create an aim constraint on some dummy objects
        cmds.connectAttr(self.surfaceInfo + ".position", self.locator + ".translate")

        dummyDst = cmds.spaceLocator(name="target", p=(0, 0, 0))[0]
        cmds.move(0, 1, 0, dummyDst)
        self.aim = cmds.aimConstraint(dummyDst,
                                      self.locator,
                                      name = misc.formatName(self.side,
                                                             self.name,
                                                             "AIM"),
                                      aimVector=[1, 0, 0],
                                      upVector=[0, 1, 0],
                                      worldUpType="vector",
                                      )[0]

        # cmds.connectAttr(self.surfaceInfo + ".position", self.aim + ".target[0].targetRotatePivot", force=True)
        cmds.connectAttr(self.surfaceInfo + ".tangentU", self.aim + ".target[0]targetTranslate", force=True)
        cmds.connectAttr(self.surfaceInfo + ".normalizedNormal", self.aim + ".worldUpVector")
        cmds.delete(dummyDst)
        cmds.setAttr(self.ctrlOffset + ".rx", -90)


        #---Get a clean output for the face rig
        cmds.connectAttr(self.surfaceInfo + ".position", self.aim + ".target[0].targetRotatePivot", force=True)
        self.pmaNtrlzNode = cmds.createNode("plusMinusAverage", name=misc.formatName(self.side,
                                                                                     "{0}{1}".format(self.name, "Nuetralize"),
                                                                                     "PMA"))

        #---We want to clamp between 0 and 1 because this is the limit of nurbs UVs
        cmds.connectAttr(self.baseU, self.pmaNtrlzNode + ".input2D[0].input2Dx")
        cmds.connectAttr(self.baseV, self.pmaNtrlzNode + ".input2D[0].input2Dy")
        cmds.connectAttr(self.currentU, self.pmaNtrlzNode + ".input2D[1].input2Dx")
        cmds.connectAttr(self.currentV, self.pmaNtrlzNode + ".input2D[1].input2Dy")
        cmds.setAttr("{0}.operation".format(self.pmaNtrlzNode), 2)

        self.multNodeReverse = cmds.createNode("multiplyDivide", name=misc.formatName(self.side,
                                                                               "{0}{1}".format(self.name, "ReverseUV"),
                                                                               "MTD"))
        cmds.setAttr("{0}.operation".format(self.multNode), 1)
        cmds.setAttr(self.multNodeReverse + ".input2X", -1)
        cmds.setAttr(self.multNodeReverse + ".input2Y", -1)
        cmds.connectAttr(self.pmaNtrlzNode + ".output2Dx", self.multNodeReverse + ".input1X")
        cmds.connectAttr(self.pmaNtrlzNode + ".output2Dy", self.multNodeReverse + ".input1Y")

        self.multNodeAmount = cmds.createNode("multiplyDivide", name=misc.formatName(self.side,
                                                                               "{0}{1}".format(self.name, "Amount"),
                                                                               "MTD"))

        cmds.connectAttr(self.multNodeReverse + ".outputX", self.multNodeAmount + ".input1X")
        cmds.connectAttr(self.multNodeReverse + ".outputY", self.multNodeAmount + ".input1Y")

        cmds.connectAttr(self.amountU, self.multNodeAmount + ".input2X")
        cmds.connectAttr(self.amountV, self.multNodeAmount + ".input2Y")

        cmds.setAttr("{0}.operation".format(self.multNode), 1)
        cmds.connectAttr(self.multNodeAmount + ".outputX", self.outU)
        cmds.connectAttr(self.multNodeAmount + ".outputY", self.outV)

        cmds.connectAttr(self.ctrl + ".tz", self.ctrlOffset +".ty")

        if self.uOutConnectionAttr:
            cmds.connectAttr(self.outU, self.uOutConnectionAttr)
        if self.vOutConnectionAttr:
            cmds.connectAttr(self.outV, self.vOutConnectionAttr)


def normalizeSlidingCtrls(mayaObjects=None):
    if not mayaObjects: mayaObjects = cmds.ls(sl=True)
    #-- Shift currentU and V to initU and V
    #-- zero out translateX and Y
    # copy current to base
    for ctrl in mayaObjects:
        currentU = cmds.getAttr(ctrl + ".currentU")
        currentV = cmds.getAttr(ctrl + ".currentV")
        cmds.setAttr(ctrl + ".initU", currentU)
        cmds.setAttr(ctrl + ".initV", currentV)
        cmds.setAttr(ctrl + ".tx", 0.0)
        cmds.setAttr(ctrl + ".ty", 0.0)
        # you need to get these attribute values again because they have changed
        currentU = cmds.getAttr(ctrl + ".currentU")
        currentV = cmds.getAttr(ctrl + ".currentV")
        cmds.setAttr(ctrl + ".baseU", currentU)
        cmds.setAttr(ctrl + ".baseV", currentV)

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

def mirrorSlidingCtrls(mayaObjects=None, mirrorWeights=False):
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
        attrs = (".initU", ".initV", ".baseU", ".baseV", ".uSpeed", ".vSpeed", ".amountU",
                 ".amountV", ".rotateOrder", ".vis", ".gimbal_vis")
        for attr in attrs:
            attrsDict[ctrl + attr] = cmds.getAttr(ctrl + attr)
        # Get connected attributes, find L to R, or R to L depending on what is selected
        inU = findOppositeSlideConnection(ctrl, "outU")
        if not inU:
            continue
        inV = findOppositeSlideConnection(ctrl, "outV")
        if not inV:
            continue

        # Find Surface
        surf = cmds.listConnections(ctrl + ".currentU", d=True, t="pointOnSurfaceInfo", et=True)[0]
        nurbs = cmds.listConnections(surf + ".inputSurface", s=True, t="nurbsSurface", et=True)[0]

        # Create component with Opposite side and opposite attributes
        slideComponent = Component(name=name, side=side, helperGeo = nurbs, uOutConnectionAttr = inU, vOutConnectionAttr = inV)

        # Set the location and the attributes
        for attr in attrs:
            cmds.setAttr(slideComponent.ctrl + attr, attrsDict[ctrl + attr])

        # Copy Curve shape, then mirror curve shape
        misc.pushCurveShape(ctrl, slideComponent.ctrl, True, True)


        uMirror = cmds.getAttr(ctrl + ".baseU")
        if uMirror < .5:
            uMirror = abs(uMirror-0.5)
            uMirror = .5 + uMirror
        elif uMirror > .5:
            uMirror = uMirror-0.5
            uMirror = .5 - uMirror
        for uAttr in (".baseU", ".initU"):
            cmds.setAttr(slideComponent.ctrl + uAttr, uMirror)

        # Normalize Control
        normalizeSlidingCtrls([slideComponent.ctrl])

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


def copyWeightsFromSlideCtrls(sourceSlideCtrl=None, targetSlideCtrl=None, cache=True):
    if not sourceSlideCtrl and not targetSlideCtrl:
        sourceSlideCtrl = cmds.ls(sl=True)[0]
        targetSlideCtrl = cmds.ls(sl=True)[1]

    # getDeformer
    deformer = cmds.listConnections(sourceSlideCtrl + ".outU", d=True, p=True, t="LHSlideDeformer", et=True)[0]
    deformer = deformer.split(".")[0]

    # get Mesh
    geo = cmds.deformer(deformer, q = True, g = True)[0]

    if not 'SYMMETRYDICT' in globals():
        global SYMMETRYDICT
        SYMMETRYDICT = faceWeights.create_symmetric_partners( geo = geo).symmetry_dict


    # get sides, then see if they are opposite, if they are you will want to copy and flip, otherwise you just want to copy
    flip = False
    sourceSide = getSide(sourceSlideCtrl)
    targetSide = getSide(targetSlideCtrl)
    if sourceSide != targetSide:
        flip=True

    # get source attrs
    for attr in ("outU", "outV"):
        attrConnection = cmds.listConnections(sourceSlideCtrl + "." + attr, d=True, p=True, t="LHSlideDeformer", et=True)[0]
        srcWeights, srcAnimCurve, srcAnimCurveFalloff = getSlideWeightAttrNames(attrConnection)
        attrConnection = cmds.listConnections(targetSlideCtrl + "." + attr, d=True, p=True, t="LHSlideDeformer", et=True)[0]
        targetWeights, targetAnimCurve, targetAnimCurveFalloff = getSlideWeightAttrNames(attrConnection)

        try:
            copyFlipSlideAnimCurves(sourceSide, flip, srcAnimCurve, targetAnimCurve)
        except:
            print("Unable to copy animation curve as there weren't enough points")
        try:
            copyFlipSlideAnimCurves(sourceSide, flip, srcAnimCurveFalloff, targetAnimCurveFalloff)
        except:
            print("Unable to copy animation curve as there weren't enough points")

        sourceWeights = getWeightAttributes(deformer)
        source = sourceWeights.get(srcWeights)
        target = sourceWeights.get(targetWeights)
        source = "{0}.{1}".format(deformer, source)
        target = "{0}.{1}".format(deformer, target)
        print(sourceWeights)
        print(source, srcWeights)
        print(target, targetWeights)

        faceWeights.copy_double_array_weights(source = source,
                                              target = [target],
                                              flip = flip,
                                              symmetry_dict = SYMMETRYDICT)


    if cache:
        cacheSlideDeformer(deformer, 0)
        cmds.refresh()
        cacheSlideDeformer(deformer, 1)


        




