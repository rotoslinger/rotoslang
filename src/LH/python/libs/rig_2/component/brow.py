import inspect
from collections import OrderedDict
from maya import cmds
import sys
from rig_2.component.subcomponent import weightStack
reload(weightStack)
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
from rig.deformers import utils as deformer_utils
reload(deformer_utils)
from rig.utils import misc
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
from rig_2.manipulator import elements as manipulator_elements
from rig_2.component import base
from rig.rigComponents import mouthJaw
reload(base) 


class Brow(base.Component):
    def __init__(self,
                 component_name="brow",
                 guide_class=None,
                 tierCounts=[1,3,5],
                 side="C",
                 nameBrows="Brow",
                 ctrlName = "brow",  # this will be used as a way to reuse controls between different components and deformers
                 leftBrowMesh = "C_brow_GEO",
                 leftBrowBaseMesh = "C_browBase_GEO",
                 rightBrowMesh = "C_brow_GEO",
                 rightBrowBaseMesh = "C_browBase_GEO",
                 slidePatch="C_browGuide_SLDE",
                 slidePatchBase="C_browGuide_SLDEBASE",
                 L_projectionMesh="L_brow_REF_PRJ",
                 R_projectionMesh="R_brow_REF_PRJ",
                 rivet_orient_patch = "browGuide_RivetOrientPatch",
                 primaryBrowShapeAnimCurveDict = elements.BROW_PRIMARY_ANIM_CURVE,
                 ctrlAutoPositionThreshold=.09,
                 slideIconShapeDict = manipulator_elements.circle,
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

                 tierDefaultVisibility = [True, True, True],
                 **kw

    ):
        super(Brow, self).__init__(component_name=component_name, **kw)
        self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()
        
        # args
        self.component_name=component_name
        self.guide_class=guide_class
        self.tierCounts=tierCounts
        self.side=side
        self.nameBrows=nameBrows
        self.ctrlName =ctrlName
        self.leftBrowMesh = leftBrowMesh
        self.leftBrowBaseMesh = leftBrowBaseMesh
        self.rightBrowMesh =  rightBrowMesh
        self.rightBrowBaseMesh = rightBrowBaseMesh
        self.slidePatch=slidePatch
        self.slidePatchBase=slidePatchBase
        self.L_projectionMesh=L_projectionMesh
        self.R_projectionMesh=R_projectionMesh
        self.rivet_orient_patch = rivet_orient_patch
        self.primaryBrowShapeAnimCurveDict = primaryBrowShapeAnimCurveDict
        self.ctrlAutoPositionThreshold=ctrlAutoPositionThreshold
        self.slideIconShapeDict = slideIconShapeDict
        self.slideControlSpeedDefaults = slideControlSpeedDefaults
        self.leftBrowSlideFalloffDict =leftBrowSlideFalloffDict
        self.rightBrowSlideFalloffDict = rightBrowSlideFalloffDict
        self.leftBrowMatDefFalloffDict = leftBrowMatDefFalloffDict
        self.rightBrowMatDefFalloffDict = rightBrowMatDefFalloffDict
        self.slideCtrlSizes = slideCtrlSizes
        self.slideCtrlShapeOffset1=slideCtrlShapeOffset1
        self.slideCtrlShapeOffset2=slideCtrlShapeOffset2
        self.slideCtrlShapeOffset3=slideCtrlShapeOffset3

        self.matDefCtrlSizes = matDefCtrlSizes
        self.matDefCtrlShapeOffset1=matDefCtrlShapeOffset1
        self.matDefCtrlShapeOffset2=matDefCtrlShapeOffset2
        self.matDefCtrlShapeOffset3=matDefCtrlShapeOffset3

        self.tierDefaultVisibility =tierDefaultVisibility
        
        
        
        
        self.tierNames = ["Primary", "Secondary", "Tertiary"]


    def prepare(self):


        self.control = cmds.circle(n= self.nameBrows + "Control", nr=[0,1,0])[0]
        cmds.parent(self.control, self.control_parent)

        # upperLipMesh = "L_upperLid",
        # upperLipBaseMesh = "L_upperLidBase",
        # lowerLidMesh = "L_lowerLid",
        # lowerLidBaseMesh = "L_lowerLidbase",
        # slidePatch="L_lidGuide_SLDE",
        # slidePatchBase="L_lidGuide_SLDEBASE",
        # projectionMeshUpper="L_upperLid_REF_PRJ",
        # projectionMeshLower="L_lowerLid_REF_PRJ",


                    
    def unpack_args_from_guide(self):
        if not self.guide_class:
            return

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
        # if not self.rivet_orient_patch:
        #     self.rivet_orient_patch = self.slidePatch
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
                                                rotationAmount=True,
                                                component_name=self.component_name,
                                                
                                                )
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
                                                                           autoCreateName = self.ctrlName + side + self.tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                                           singleFalloffName = self.ctrlName + side,
                                                                           autoCreateNum = self.tierCounts[idx],
                                                                           falloffCurveDict = self.slideFalloffDicts[posIdx],
                                                                           curveOverrideDict = self.curveOverrideDict[idx],
                                                                           centerWeight = elements.BROW_CENTER_WEIGHTS[idx],
                                                                           outerWeight = elements.OUTER_WEIGHTS[idx],
                                                                           angle = elements.BROW_ANGLES[idx],
                                                                           nudge = elements.NUDGES[idx],
                                                                           lastAngle=elements.LAST_ANGLES[idx],
                                                                           component_name=self.component_name,

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
                                                                      controlAutoOrientMesh=self.rivet_orient_patch,
                                                                      controlRivetAimMesh=self.rivet_orient_patch,
                                                                      controlSpeedDefaults = self.slideControlSpeedDefaults,
                                                                      controlParent = self.control_parent,
                                                                      connectFalloff = self.connectFalloffs[idx],
                                                                      isOutputKDoubleArray=True,
                                                                      falloffCurveWeightNode=currFalloffCurveWeightNode,  # If a weight node already exists, use it
                                                                      # falloffCurveWeightNode="TestCurveWeights",
                                                                      autoCreateName = self.ctrlName + side + self.tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                                      controlSize = self.slideCtrlSizes[idx],
                                                                      controlShapeOffset = self.slideCtrlShapeOffsets[idx],
                                                                      controlShape = self.slideIconShapeDict,
                                                                      controlLockAttrs=["ry", "rz", "sx", "sz"],
                                                                      component_name=self.component_name,
                                                                      )
                self.slideWeightStack[side].create()
                self.ctrlPositions[side].append(self.slideWeightStack[side].positionsFromWeights)
                self.ctrlRotations[side].append(self.slideWeightStack[side].rotationsFromWeights)
                weightStack.connect_weight_stack_anim_curve(self.slideWeightStack[side], self.slideCurveWeights[side])

    def browMatDef(self):
        self.matDefCurveWeights = {}
        self.matDefCurveWeights = {}
        self.matDefWeightStack = {}
        self.matDeformersTranslate = {}
        self.matDeformersRotate = {}
        self.matDefCtrlShapeOffsets =  [self.matDefCtrlShapeOffset1,
                                        self.matDefCtrlShapeOffset2,
                                        self.matDefCtrlShapeOffset3]

        self.matDefIconShapeDicts = [manipulator_elements.primary_plus, manipulator_elements.secondary_plus, manipulator_elements.tertiary_plus]
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
                                                                            autoCreateName = self.ctrlName + side + self.tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                                            singleFalloffName = self.ctrlName + side + "MATDEFTEST",
                                                                            autoCreateNum = self.tierCounts[idx],
                                                                            falloffCurveDict = self.matDefFalloffDicts[posIdx],
                                                                            curveOverrideDict = self.curveOverrideDict[idx],
                                                                            centerWeight = elements.BROW_CENTER_WEIGHTS[idx],
                                                                            outerWeight = elements.OUTER_WEIGHTS[idx],
                                                                            angle = elements.BROW_ANGLES[idx],
                                                                            nudge = elements.NUDGES[idx],
                                                                            lastAngle=elements.LAST_ANGLES[idx],
                                                                            component_name=self.component_name,
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
                                                                                 locatorName=currName + self.tierNames[idx] + "Trans",  # Primary, Secondary, Or Tertiatry
                                                                                 curveWeightsNode=self.matDefCurveWeights[side].node,
                                                                                 control_rivet_mesh=self.deformMeshes[posIdx],
                                                                                 curveWeightsConnectionIdx=self.tierAddAtIndex[idx],
                                                                                 translations = self.ctrlPositions[side][idx],
                                                                                 rotations = self.ctrlRotations[side][idx],
                                                                                 controlParent = self.slideWeightStack[side].controls,
                                                                                 rigParent = self.rig,
                                                                                 offset = self.matDefCtrlShapeOffsets[idx],
                                                                                 size = self.matDefCtrlSizes[idx],
                                                                                 hide = True,
                                                                                 connectTranslate = True,
                                                                                 connectRotate = False,
                                                                                 connectScale = False,
                                                                                 controlShapeDict=self.matDefIconShapeDicts[idx],
                                                                                 component_name=self.component_name,
                                                                                 )
                self.matDeformersTranslate[side].create()

                self.matDeformersRotate[side] = matrixDeformer.MatrixDeformer(name=currName + "_MatDefRotate",
                                                                              geoToDeform=self.deformMeshes[posIdx],
                                                                              ctrlName=self.ctrlName + side + self.matDefNames[idx],
                                                                              centerToParent=True,
                                                                              addAtIndex=self.tierAddAtIndex[idx],
                                                                              numToAdd=self.tierCounts[idx],
                                                                              reverseDeformerOrder = True,
                                                                              locatorName=currName + self.tierNames[idx] + "Rot",  # Primary, Secondary, Or Tertiatry
                                                                              curveWeightsNode=self.matDefCurveWeights[side].node,
                                                                              control_rivet_mesh=self.deformMeshes[posIdx],
                                                                              curveWeightsConnectionIdx=self.tierAddAtIndex[idx],
                                                                              translations = self.ctrlPositions[side][idx],
                                                                              rotations = self.ctrlRotations[side][idx],
                                                                              controlParent = self.slideWeightStack[side].controls,
                                                                              rigParent = self.rig,
                                                                              offset = self.matDefCtrlShapeOffsets[idx],
                                                                              size = self.matDefCtrlSizes[idx],
                                                                              hide = True,
                                                                              connectTranslate = False,
                                                                              connectRotate = True,
                                                                              connectScale = True,
                                                                              controlShapeDict=self.matDefIconShapeDicts[idx],
                                                                              component_name=self.component_name,
                                                                              )
                self.matDeformersRotate[side].create()
                weightStack.connect_weight_stack_anim_curve(self.matDeformersRotate[side], self.matDefCurveWeights[side])
                weightStack.connect_weight_stack_anim_curve(self.matDeformersTranslate[side], self.matDefCurveWeights[side])

    def post_create(self):
        cmds.refresh()
        deformer_utils.cacheOutAllSlideDeformers()

    def create(self):
        super(Brow, self).create()
        self.prepare()
        self.unpack_args_from_guide()
        self.browSlide()
        self.browMatDef()
        self.post_create()

