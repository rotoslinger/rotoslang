from maya import cmds
import base
reload(base)
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
reload(misc)

class CurveRollSimple(base.Deformer):
    def __init__(self,
                    name="testCurveRollSimple",
                    deformerType="LHCurveRollSimple",
                    membershipWeightsAttr = "",
                    rollWeightsAttr = "",
                    geoToDeform="humanLipTest_humanLipsUpper",
                    baseGeoToDeform="humanLipTest_humanLipsUpperBase",
                    rollCurve="humanLipTest_upperLipCurve",
                    duplicateCurve=True,
                    simplifyCurve=True,
                    cvCount = 6,
                    parent="",
                    centerToParent=True,
                    rotationTranforms=[],
                    addAtIndex=0,
                    numToAdd=1,
                    locatorName="test",
                    curveWeightsNode="",
                    curveWeightsConnectionIdx=0,
                    locations=[],
                    weightStackNode="",
                    hide=True,
                 **kw):
        super(CurveRollSimple, self).__init__(**kw)
        self.name = name
        self.addAtIndex = addAtIndex
        self.deformerType = deformerType
        self.membershipWeightsAttr = membershipWeightsAttr
        self.rollWeightsAttr = rollWeightsAttr
        self.geoToDeform = geoToDeform
        self.baseGeoToDeform = baseGeoToDeform
        self.rollCurve = rollCurve
        self.parent = parent
        self.centerToParent = centerToParent
        self.rotationTranforms = rotationTranforms
        self.numToAdd = numToAdd
        self.locatorName = locatorName
        self.curveWeightsNode = curveWeightsNode
        self.curveWeightsConnectionIdx = curveWeightsConnectionIdx
        self.locations = locations
        self.hide = hide
        self.weightStackNode = weightStackNode


        self.deformer = ""
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.deformerType = "LHCurveRollSimple"
        self.duplicateCurve=duplicateCurve
        self.simplifyCurve=simplifyCurve
        self.cvCount = cvCount

    def getDeformer(self):
        if cmds.objExists(self.name):
            self.deformer = self.name
            return
        self.deformer = cmds.deformer(self.geoToDeform, type=self.deformerType, n=self.name, par=True)[0]

    def getNodes(self):
        if self.duplicateCurve and not cmds.objExists(self.name+"RollCurve"):
            self.rollCurve = cmds.duplicate(self.rollCurve, name = self.name+"RollCurve")[0]
        if self.duplicateCurve and cmds.objExists(self.name+"RollCurve"):
            self.rollCurve = self.name+"RollCurve"
        
        if self.simplifyCurve:

            cmds.rebuildCurve(self.rollCurve, rt = 0, ch=False, rpo=True, s=self.cvCount, d=3, kr=True, end=0, kep=True)
            # cmds.rebuildCurve(self.rollCurve, ch=False, rpo=True, rt=True, end=1, kr=False, kcp=False, kep=1, kt=0, s=5, d=3, tol=0.01)
            # cmds.rebuildCurve(self.rollCurve, ch=True, rpo=True, rt=True, end=1, kr=False, kcp=False, kep=1, kt=0, s=self.cvCount, d=3, tol=0.01)
# rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s 5 -d 3 -tol 0.01 "humanLipTest_lowerLipCurveAim";


        self.rollCurve = misc.getShape(self.rollCurve)
        if not type(self.baseGeoToDeform) == list:
            self.baseGeoToDeform = [self.baseGeoToDeform]
        for idx, geo in enumerate(self.baseGeoToDeform):
            self.baseGeoToDeform[idx] = misc.getShape(geo)
        if not type(self.geoToDeform) == list:
            self.geoToDeform = [self.geoToDeform]
        for idx, geo in enumerate(self.geoToDeform):
            self.geoToDeform[idx] = misc.getShape(geo)

        if not cmds.objExists( self.geoToDeform[0] + "." + self.name + "MembershipWeights"):
            self.membershipWeightsAttr = weightMapUtils.createWeightMapOnSingleObject(self.geoToDeform[0], self.name + "MembershipWeights", defaultValue=1.0, addAttr=True)
        else:
            self.membershipWeightsAttr = self.geoToDeform[0] + "." + self.name + "MembershipWeights"

        if not self.weightStackNode and not cmds.objExists(self.rollWeightsAttr):
            self.weightMap = weightMapUtils.createWeightMapOnSingleObject(self.geoToDeform[0], self.name + "RollWeights", defaultValue=1.0, addAttr=True)
        else:
            self.weightMap = "{0}.outWeightsDoubleArray".format(self.weightStackNode)

    def setDefaults(self):
        if not type(self.geoToDeform) == list:
            self.geoToDeform = [self.geoToDeform]

    def connectDeformer(self):
        cmds.connectAttr(self.rollCurve + ".worldSpace", self.deformer + ".rollCurve", f=True)

        if not type(self.baseGeoToDeform) == list:
            self.baseGeoToDeform = [self.baseGeoToDeform]

        for idx, geo in enumerate(self.baseGeoToDeform):
            geoAttrType = ".worldMesh"
            objectType = cmds.objectType(geo)
            if objectType == "nurbsCurve" or objectType == "nurbsSurface":
                geoAttrType = ".worldSpace"
            if objectType == "lattice":
                geoAttrType = ".worldLattice"

            cmds.connectAttr(geo + geoAttrType, self.deformer + ".weightArrays[{0}].baseGeo".format(idx), f=True)
            cmds.connectAttr(self.membershipWeightsAttr, self.deformer + ".weightArrays[{0}].membershipWeight".format(idx), f=True)
            cmds.connectAttr(self.weightMap, self.deformer + ".weightArrays[{0}].rollWeights".format(idx), f=True)

    def cleanup(self):
        cmds.setAttr(self.deformer + ".cacheBind", 1)
        cmds.setAttr(self.deformer + ".rollAmount", 1)

