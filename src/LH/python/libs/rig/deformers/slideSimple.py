from maya import cmds
from rig.deformers import base
import importlib
importlib.reload(base)
from rig.utils import weightMapUtils, misc
importlib.reload(weightMapUtils)
importlib.reload(misc)
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)
from rig_2.component import base as component_base
importlib.reload(component_base)

class SlideSimple(base.Deformer):
    def __init__(self,
                    name="testSlideSimple",
                    deformerType="LHSlideSimple",
                    membershipWeightsAttr = "",
                    geoToDeform="",
                    baseGeoToDeform="",
                    slidePatch="",
                    slidePatchBase="",
                    parent="",
                    centerToParent=True,
                    rotationTranforms=[],
                    addAtIndex=0,
                    numToAdd=1,
                    locatorName="test",
                    curveWeightsNode="",
                    curveWeightsConnectionIdx=0,
                    locations=[],
                    hide=True,
                    rotationAmount = 0,
                    **kw):
        super(SlideSimple, self).__init__(**kw)
        self.name = name
        self.addAtIndex = addAtIndex
        self.deformerType = deformerType
        self.membershipWeightsAttr = membershipWeightsAttr
        self.geoToDeform = geoToDeform
        self.baseGeoToDeform = baseGeoToDeform
        self.slidePatch = slidePatch
        self.slidePatchBase = slidePatchBase
        self.parent = parent
        self.centerToParent = centerToParent
        self.rotationTranforms = rotationTranforms
        self.numToAdd = numToAdd
        self.locatorName = locatorName
        self.curveWeightsNode = curveWeightsNode
        self.curveWeightsConnectionIdx = curveWeightsConnectionIdx
        self.locations = locations
        self.hide = hide
        self.rotationAmount = rotationAmount


        self.deformer = ""
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.deformerType = "LHSlideSimple"

    def getNodes(self):
        self.slidePatch = misc.getShape(self.slidePatch)
        self.slidePatchBase = misc.getShape(self.slidePatchBase)
        if not type(self.baseGeoToDeform) == list:
            self.baseGeoToDeform = [self.baseGeoToDeform]
        for idx, geo in enumerate(self.baseGeoToDeform):
            self.baseGeoToDeform[idx] = misc.getShape(geo)

        for node in [self.slidePatch, self.slidePatchBase] + self.baseGeoToDeform:
            tag_utils.create_component_tag(node, self.component_name)


    def setDefaults(self):
        if not type(self.geoToDeform) == list:
            self.geoToDeform = [self.geoToDeform]
        for idx, deformGeo in enumerate(self.geoToDeform):
            iterGeo = misc.getOMItergeo(deformGeo)
            polyCount = iterGeo.count()
            defaultVals = [1.0 for x in range(polyCount)]
            finalAttrName = "{0}.{1}[{2}].{3}".format(self.deformer, "weightArrays", idx, "membershipWeight")
            cmds.getAttr(finalAttrName)
            cmds.setAttr(finalAttrName, defaultVals, type="doubleArray")
        if self.rotationAmount:
            cmds.setAttr(self.deformer + ".rotationAmount", 1)

    def connectDeformer(self):
        cmds.connectAttr(self.slidePatch + ".worldSpace", self.deformer + ".surface")
        cmds.connectAttr(self.slidePatchBase + ".worldSpace", self.deformer + ".surfaceBase")

        if not type(self.baseGeoToDeform) == list:
            self.baseGeoToDeform = [self.baseGeoToDeform]

        for idx, geo in enumerate(self.baseGeoToDeform):
            geoAttrType = ".worldMesh"
            objectType = cmds.objectType(geo)
            if objectType == "nurbsCurve" or objectType == "nurbsSurface":
                geoAttrType = ".worldSpace"
            if objectType == "lattice":
                geoAttrType = ".worldLattice"

            cmds.connectAttr(geo + geoAttrType, self.deformer + ".weightArrays[{0}].baseGeo".format(idx))
            if not cmds.objExists(self.membershipWeightsAttr):
                continue
            cmds.connectAttr(self.membershipWeightsAttr, self.deformer + ".weightArrays[{0}].membershipWeight".format(idx))


