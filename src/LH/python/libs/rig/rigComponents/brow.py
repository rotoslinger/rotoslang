from maya import cmds
import maya.OpenMaya as OpenMaya
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)
# from rig.utils import weightMapUtils
# from rig.deformers import base
from rig.deformers import weightStack
reload(weightStack)
# from rig.deformers import utils as deformerUtils
from rig.deformers import matrixDeformer
reload(matrixDeformer)
from rig.deformers import slideSimple
reload(slideSimple)
from rig.deformers import blendshapeSimple
reload(blendshapeSimple)
from rig.deformers import vectorDeformerSimple
reload(vectorDeformerSimple)
from rig.deformers import curveRollSimple
reload(curveRollSimple)
from rig.deformers import utils as deformerUtils
reload(deformerUtils)
# reload(deformerUtils)
# reload(base)
from rig.utils import weightMapUtils, misc
reload(misc)
from rig.utils import LHCurveDeformerCmds
reload(LHCurveDeformerCmds)
from rig.rigComponents import meshRivetCtrl 
reload(meshRivetCtrl)
from rig.rigComponents import elements
reload(elements)

from decorators import initialize
reload(elements)

from rig.utils import lhExport
reload(lhExport)



class Brow(object):
    @initialize.initializer
    def __init__(self,
                 tierCounts=[1,3,5],
                 side="L",
                 nameBrows="Brow",
                 ctrlName = None,  # this will be used as a way to reuse controls between different components and deformers
                 leftBrowMesh = "",
                 leftBrowBaseMesh = "",
                 rightBrowMesh = "",
                 rightBrowBaseMesh = "",
                 slidePatch="",
                 slidePatchBase="",
                 L_projectionMesh="",
                 R_projectionMesh="",
                 primaryBrowShapeAnimCurveDict = elements.BROW_PRIMARY_ANIM_CURVE,
                 characterName = "character",
                 controlParent="C_control_GRP",
                 rigParent="C_rig_GRP",
                 ctrlAutoPositionThreshold=.09,
                 containerName = "L_lids",
                 slideIconShapeDict = elements.circle,
                 slideControlSpeedDefaults = [.1,.1,.1],
                 leftBrowSlideFalloffDict = elements.L_BROW_SLIDE_FALLOFF,
                 rightBrowSlideFalloffDict = elements.R_BROW_SLIDE_FALLOFF,
                 leftBrowMatDefFalloffDict = elements.L_BROW_SLIDE_FALLOFF,
                 rightBrowMatDefFalloffDict = elements.R_BROW_SLIDE_FALLOFF,
                 slideCtrlSizes = [1, .65, .35],
                 slideCtrlShapeOffset1=[0,0.0,2],
                 slideCtrlShapeOffset2=[0,0.0,2],
                 slideCtrlShapeOffset3=[0,0.0,2],

                 matDefCtrlSizes = [.7, .65, .35],
                 matDefCtrlShapeOffset1=[0,-2.0,2],
                 matDefCtrlShapeOffset2=[0,-2.0,1],
                 matDefCtrlShapeOffset3=[0,-2.0,1],

                 tierDefaultVisibility = [True, True, True]


    ):
        self.tierNames = ["Primary", "Secondary", "Tertiary"]


    def prepare(self):
        if not (cmds.objExists("C_{0}_GRP".format(self.characterName))):
            misc.create_rig_hier(char_name=self.characterName)

        self.control = cmds.circle(n= self.nameBrows + "Control", nr=[0,1,0])[0]
        cmds.parent(self.control, self.controlParent)

        # Create container
        if not cmds.objExists(self.containerName):
            self.container = cmds.container(n=self.containerName)
        else:
            self.container = self.containerName
        self.slideContainerAttrNames = []
        self.matDefContainerAttrNames = []
        for ctrlTypeName in ["slide", "matDef"]:
            for posIdx, tierName in enumerate(self.tierNames):
                attrName = ctrlTypeName + tierName + "Vis"
                fullAttrName = self.container + "." + attrName
                if not cmds.objExists(fullAttrName):
                    cmds.addAttr(self.container, ln = attrName, at = "short", dv = self.tierDefaultVisibility[posIdx], min = 0, max = 1)
                    cmds.setAttr( fullAttrName, cb = True, k = False)
                if ctrlTypeName == "slide":
                    self.slideContainerAttrNames.append(fullAttrName)
                if ctrlTypeName == "matDef":
                    self.matDefContainerAttrNames.append(fullAttrName)

    def browSlide(self):
        self.deformMeshes =  [self.leftBrowMesh, self.rightBrowMesh]
        # Eventually this will need to be dynamic so we can rivet to the final mesh
        self.controlRivetMeshes =  [self.leftBrowMesh, self.rightBrowMesh]
        self.baseGeosToDeform = [self.leftBrowBaseMesh, self.rightBrowBaseMesh]
        self.projectionMeshes = [self.L_projectionMesh, self.R_projectionMesh]
        self.slideFalloffDicts = [self.leftBrowSlideFalloffDict, self.rightBrowSlideFalloffDict]
        self.slideCtrlShapeOffsets = [self.slideCtrlShapeOffset1, self.slideCtrlShapeOffset2, self.slideCtrlShapeOffset3]
        self.tierCounts = [self.tierCounts[0], self.tierCounts[1], self.tierCounts[2]]
        self.tierStartElemIdxs = [0, self.tierCounts[0], self.tierCounts[1] + self.tierCounts[0]]
        self.tierAddAtIndex = [0, self.tierCounts[0], self.tierCounts[1] + self.tierCounts[0]]

        self.controlAutoOrientMesh = self.slidePatch
        self.slideDeformers = {}
        self.slideCurveWeights = {}
        self.slideWeightStack = {}
        self.isAddingNewElems = [False, True, True]
        self.connectFalloffs = [False, True, True]
        self.matDefNames = ["MatrixDeformer1", "MatrixDeformer2", "MatrixDeformer3"]
        self.curveOverrideDict = [self.primaryBrowShapeAnimCurveDict, None, None]
        self.ctrlPositions = {}
        self.ctrlRotations = {}
        # falloffCurveWeightNodes= [None, self.name + "CurveWeights", self.name + "CurveWeights"]
        for posIdx, side in enumerate(["L", "R"]):
            currName = side + "_" + self.nameBrows + "Slide"
            self.slideDeformers[side] = slideSimple.SlideSimple(name = currName,
                                                geoToDeform=self.deformMeshes[posIdx],
                                                slidePatch=self.slidePatch,
                                                slidePatchBase=self.slidePatchBase,
                                                baseGeoToDeform=self.baseGeosToDeform[posIdx],
                                                rotationAmount=True)
            self.slideDeformers[side].create()
            
            outputAttrs = [self.slideDeformers[side].deformer + ".weightArrays[0].vWeights"]
            outputAttrs_LR = [self.slideDeformers[side].deformer + ".weightArrays[0].uWeights"]
            self.ctrlPositions[side] = []
            self.ctrlRotations[side] = []

            for idx in range(3):

                self.slideCurveWeights[side] = weightStack.AnimCurveWeight(name=currName + "CurveWeights",
                                                    baseGeo=self.baseGeosToDeform[posIdx],
                                                    ctrlNode=self.control,
                                                    projectionGeo=self.projectionMeshes[posIdx],
                                                    weightCurveNames=[],
                                                    addNewElem=self.isAddingNewElems[idx],
                                                    autoCreateAnimCurves = True,
                                                    autoCreateName = self.ctrlName + side + self.tierNames[idx], # Primary, Secondary, Or Tertiatry
                                                    singleFalloffName = self.ctrlName + side,
                                                    autoCreateNum = self.tierCounts[idx],
                                                    falloffCurveDict = self.slideFalloffDicts[posIdx],
                                                    curveOverrideDict = self.curveOverrideDict[idx],
                                                    centerWeight = elements.BROW_CENTER_WEIGHTS[idx],
                                                    outerWeight = elements.OUTER_WEIGHTS[idx],
                                                    angle = elements.BROW_ANGLES[idx],
                                                    nudge = elements.NUDGES[idx],
                                                    lastAngle=elements.LAST_ANGLES[idx],

                )
                self.slideCurveWeights[side].create()

                currFalloffCurveWeightNode = None
                if posIdx > 0:
                    currFalloffCurveWeightNode = currName + "CurveWeights"
                self.slideWeightStack[side] = weightStack.WeightStack(name=currName + "WeightStack",
                                                geoToWeight=self.deformMeshes[posIdx],
                                                ctrlNode=self.control,
                                                inputWeightAttrs=self.slideCurveWeights[side].newKDoubleArrayOutputPlugs,
                                                addNewElem=self.isAddingNewElems[idx],
                                                outputAttrs = outputAttrs,
                                                outputAttrs_LR = outputAttrs_LR,
                                                autoCreate=True,
                                                controlPositionWeightsThreshold=self.ctrlAutoPositionThreshold,
                                                controlRivetMesh = self.controlRivetMeshes[posIdx],
                                                controlAutoOrientMesh=self.controlAutoOrientMesh,
                                                controlRivetAimMesh=self.slidePatch,
                                                controlSpeedDefaults = self.slideControlSpeedDefaults,
                                                controlParent = self.controlParent,
                                                connectFalloff = self.connectFalloffs[idx],
                                                isOutputKDoubleArray=True,
                                                falloffCurveWeightNode=currFalloffCurveWeightNode, # If a weight node already exists, use it
                                                # falloffCurveWeightNode="TestCurveWeights",
                                                autoCreateName = self.ctrlName + side + self.tierNames[idx], # Primary, Secondary, Or Tertiatry
                                                controlSize = self.slideCtrlSizes[idx],
                                                controlShapeOffset = self.slideCtrlShapeOffsets[idx],
                                                controlShape = self.slideIconShapeDict,
                                                controlLockAttrs=["ry", "rz", "sx", "sz"],
                                                )
                self.slideWeightStack[side].create()
                self.ctrlPositions[side].append(self.slideWeightStack[side].positionsFromWeights)
                self.ctrlRotations[side].append(self.slideWeightStack[side].rotationsFromWeights)
                # Add controls to the container and connect to visibility

                for ctrl in self.slideWeightStack[side].controls:
                    cmds.container(self.container, edit=True, addNode=[ctrl])
                    shape = misc.getShape(ctrl)
                    cmds.connectAttr(self.slideContainerAttrNames[posIdx], shape + ".visibility", f=True)

    def browMatDef(self):
        self.matDefCurveWeights = {}
        self.matDefCurveWeights = {}
        self.matDefWeightStack = {}
        self.matDeformersTranslate = {}
        self.matDeformersRotate = {}
        self.matDefCtrlShapeOffsets =  [self.matDefCtrlShapeOffset1,
                                        self.matDefCtrlShapeOffset2,
                                        self.matDefCtrlShapeOffset3]

        self.matDefIconShapeDicts = [elements.primaryPlus, elements.secondaryPlus, elements.tertiaryPlus]
        self.matDefFalloffDicts = [self.leftBrowMatDefFalloffDict, self.rightBrowMatDefFalloffDict]

        for posIdx, side in enumerate(["L", "R"]):
            currName = side + "_" + self.nameBrows + "Slide"
            for idx in range(3):
                ################################## MATRIX DEFORMER #####################################################################
                self.matDefCurveWeights[side] = weightStack.AnimCurveWeight(name=currName + "MatDef",
                                                            baseGeo=self.baseGeosToDeform[posIdx],
                                                            ctrlNode=self.control,
                                                            projectionGeo=self.projectionMeshes[posIdx],
                                                            weightCurveNames=[],
                                                            addNewElem=self.isAddingNewElems[idx],
                                                            autoCreateAnimCurves = True,
                                                            autoCreateName = self.ctrlName + side + self.tierNames[idx], # Primary, Secondary, Or Tertiatry
                                                            singleFalloffName = self.ctrlName + side + "MATDEFTEST",
                                                            autoCreateNum = self.tierCounts[idx],
                                                            falloffCurveDict = self.matDefFalloffDicts[posIdx],
                                                            curveOverrideDict = self.curveOverrideDict[idx],
                                                            centerWeight = elements.BROW_CENTER_WEIGHTS[idx],
                                                            outerWeight = elements.OUTER_WEIGHTS[idx],
                                                            angle = elements.BROW_ANGLES[idx],
                                                            nudge = elements.NUDGES[idx],
                                                            lastAngle=elements.LAST_ANGLES[idx],
                )
                self.matDefCurveWeights[side].create()

                # Create a single matrix deformer (rotation order issues)
                self.matDeformersTranslate[side] = matrixDeformer.MatrixDeformer(name=currName + "_MatDefTranslate",
                                        geoToDeform=self.deformMeshes[posIdx],
                                        ctrlName=self.ctrlName + side + self.matDefNames[idx],
                                        centerToParent=True,
                                        addAtIndex=self.tierAddAtIndex[idx],
                                        numToAdd=self.tierCounts[idx],
                                        reverseDeformerOrder = True,
                                        locatorName=currName + self.tierNames[idx] + "Trans", # Primary, Secondary, Or Tertiatry
                                        curveWeightsNode=self.matDefCurveWeights[side].node,
                                        geoToConstrainMesh=self.deformMeshes[posIdx],
                                        curveWeightsConnectionIdx=self.tierAddAtIndex[idx],
                                        translations = self.ctrlPositions[side][idx],
                                        rotations = self.ctrlRotations[side][idx],
                                        controlParent = self.slideWeightStack[side].controls,
                                        rigParent = self.rigParent,
                                        offset = self.matDefCtrlShapeOffsets[idx],
                                        size = self.matDefCtrlSizes[idx],
                                        hide = True,
                                        connectTranslate = True,
                                        connectRotate = False,
                                        connectScale = False,
                                        controlShapeDict=self.matDefIconShapeDicts[idx],
                                        )
                self.matDeformersTranslate[side].create()

                self.matDeformersRotate[side] = matrixDeformer.MatrixDeformer(name=currName + "_MatDefRotate",
                                        geoToDeform=self.deformMeshes[posIdx],
                                        ctrlName=self.ctrlName + side + self.matDefNames[idx],
                                        centerToParent=True,
                                        addAtIndex=self.tierAddAtIndex[idx],
                                        numToAdd=self.tierCounts[idx],
                                        reverseDeformerOrder = True,
                                        locatorName=currName + self.tierNames[idx] + "Rot", # Primary, Secondary, Or Tertiatry
                                        curveWeightsNode=self.matDefCurveWeights[side].node,
                                        geoToConstrainMesh=self.deformMeshes[posIdx],
                                        curveWeightsConnectionIdx=self.tierAddAtIndex[idx],
                                        translations = self.ctrlPositions[side][idx],
                                        rotations = self.ctrlRotations[side][idx],
                                        controlParent = self.slideWeightStack[side].controls,
                                        rigParent = self.rigParent,
                                        offset = self.matDefCtrlShapeOffsets[idx],
                                        size = self.matDefCtrlSizes[idx],
                                        hide = True,
                                        connectTranslate = False,
                                        connectRotate = True,
                                        connectScale = True,
                                        controlShapeDict=self.matDefIconShapeDicts[idx],
                                        )
                self.matDeformersRotate[side].create()

                for ctrl in self.matDeformersTranslate[side].controls:
                    cmds.container(self.container, edit=True, addNode=[ctrl])
                    shape = misc.getShape(ctrl)
                    cmds.connectAttr(self.matDefContainerAttrNames[idx], shape + ".visibility", f=True)

                
    def create(self):
        self.prepare()
        self.browSlide()
        self.browMatDef()