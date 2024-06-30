import inspect
from collections import OrderedDict

from maya import cmds
import sys

from rig_2.weights import utils as weights_utils
import importlib
importlib.reload(weights_utils)

from rig_2.component.subcomponent import weightStack
# from rig.deformers import utils as deformer_utils
from rig.deformers import matrixDeformer
importlib.reload(matrixDeformer)
from rig.deformers import slideSimple
importlib.reload(slideSimple)
from rig.deformers import blendshapeSimple
importlib.reload(blendshapeSimple)
from rig.deformers import vectorDeformerSimple
importlib.reload(vectorDeformerSimple)
from rig.deformers import curveRollSimple
importlib.reload(curveRollSimple)
from rig.deformers import utils as deformer_utils
importlib.reload(deformer_utils)
# reload(deformer_utils)
# reload(base)
from rig.utils import misc
importlib.reload(misc)
from rig.utils import LHCurveDeformerCmds
importlib.reload(LHCurveDeformerCmds)
from rig.rigComponents import meshRivetCtrl 
importlib.reload(meshRivetCtrl)
from rig.rigComponents import elements
importlib.reload(elements)


from rig.utils import lhExport
importlib.reload(lhExport)

from rig_2.manipulator import elements as manipulator_elements
importlib.reload(manipulator_elements)

from rig_2.component import base
from rig.rigComponents import mouthJaw

importlib.reload(base) 


class Lid(base.Component):
    def __init__(self,
                 component_name="lids",
                 tierCounts=[1,3,5],
                 side="L",
                 guide_class=None,
                 ctrlName = "lidControl",  # this will be used as a way to reuse controls between different components and deformers
                 upperLipMesh = "L_upperLid",
                 upperLipBaseMesh = "L_upperLidBase",
                 lowerLidMesh = "L_lowerLid",
                 lowerLidBaseMesh = "L_lowerLidbase",
                 slidePatch="L_lidGuide_SLDE",
                 slidePatchBase="L_lidGuide_SLDEBASE",
                 projectionMeshUpper="L_upperLid_REF_PRJ",
                 projectionMeshLower="L_lowerLid_REF_PRJ",
                 rivet_orient_patch = "L_lidGuide_RivetOrientPatch",
                 ctrlAutoPositionThreshold=.09,
                 containerName = "L_lids",
                 slideIconShapeDict = manipulator_elements.circle,
                 slideControlSpeedDefaults = [.1,.1,.1],
                 upperLidSlideFalloffDict = elements.UPPER_LID_SLIDE_FALLOFF_DICT,
                 lowerLidSlideFalloffDict = elements.LOWER_LID_SLIDE_FALLOFF_DICT,
                 upperLidMatDefFalloffDict = elements.UPPER_LID_MATDEF_FALLOFF_DICT,
                 lowerLidMatDefFalloffDict = elements.LOWER_LID_MATDEF_FALLOFF_DICT,
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
        super(Lid, self).__init__(component_name=component_name, **kw)
        self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()
        
        # args
        self.component_name=component_name
        self.tierCounts=tierCounts
        self.side=side
        self.guide_class=guide_class
        self.component_name=component_name
        self.ctrlName = ctrlName
        self.upperLipMesh = upperLipMesh
        self.upperLipBaseMesh =upperLipBaseMesh
        self.lowerLidMesh = lowerLidMesh
        self.lowerLidBaseMesh =lowerLidBaseMesh
        self.slidePatch=slidePatch
        self.slidePatchBase=slidePatchBase
        self.projectionMeshUpper=projectionMeshUpper
        self.projectionMeshLower=projectionMeshLower
        self.rivet_orient_patch=rivet_orient_patch
        self.ctrlAutoPositionThreshold=ctrlAutoPositionThreshold
        self.containerName = containerName
        self.slideIconShapeDict = slideIconShapeDict
        self.slideControlSpeedDefaults =slideControlSpeedDefaults
        self.upperLidSlideFalloffDict = upperLidSlideFalloffDict
        self.lowerLidSlideFalloffDict = lowerLidSlideFalloffDict
        self.upperLidMatDefFalloffDict = upperLidMatDefFalloffDict
        self.lowerLidMatDefFalloffDict = lowerLidMatDefFalloffDict
        self.slideCtrlSizes =slideCtrlSizes
        self.slideCtrlShapeOffset1=slideCtrlShapeOffset1
        self.slideCtrlShapeOffset2=slideCtrlShapeOffset2
        self.slideCtrlShapeOffset3=slideCtrlShapeOffset3
        self.matDefCtrlSizes = matDefCtrlSizes
        self.matDefCtrlShapeOffset1=matDefCtrlShapeOffset1
        self.matDefCtrlShapeOffset2=matDefCtrlShapeOffset2
        self.matDefCtrlShapeOffset3=matDefCtrlShapeOffset3
        self.tierDefaultVisibility =tierDefaultVisibility
        self.input_anchor_nodes.append(self.control_parent)

        
        
        
        self.tierNames = ["Primary", "Secondary", "Tertiary"]


    def prepare(self):

        self.control = cmds.circle(n= self.component_name + "Control", nr=[0,1,0])[0]
        cmds.parent(self.control, self.control_parent)


        # upperLipMesh = "L_upperLid",
        # upperLipBaseMesh = "L_upperLidBase",
        # lowerLidMesh = "L_lowerLid",
        # lowerLidBaseMesh = "L_lowerLidbase",
        # slidePatch="L_lidGuide_SLDE",
        # slidePatchBase="L_lidGuide_SLDEBASE",
        # projectionMeshUpper="L_upperLid_REF_PRJ",
        # projectionMeshLower="L_lowerLid_REF_PRJ",

        # # Create container
        # if not cmds.objExists(self.containerName):
        #     self.container = cmds.container(n=self.containerName)
        # else:
        #     self.container = self.containerName
        # self.slideContainerAttrNames = []
        # self.matDefContainerAttrNames = []
        # for ctrlTypeName in ["slide", "matDef"]:
        #     for posIdx, tierName in enumerate(self.tierNames):
        #         attrName = ctrlTypeName + tierName + "Vis"
        #         fullAttrName = self.container + "." + attrName
        #         if not cmds.objExists(fullAttrName):
        #             cmds.addAttr(self.container, ln = attrName, at = "short", dv = self.tierDefaultVisibility[posIdx], min = 0, max = 1)
        #             cmds.setAttr( fullAttrName, cb = True, k = False)
        #         if ctrlTypeName == "slide":
        #             self.slideContainerAttrNames.append(fullAttrName)
        #         if ctrlTypeName == "matDef":
        #             self.matDefContainerAttrNames.append(fullAttrName)
                    
    def unpack_args_from_guide(self):
        if not self.guide_class:
            return

    def lidSlide(self):
        self.deformMeshes =  [self.upperLipMesh, self.lowerLidMesh]
        # Eventually this will need to be dynamic so we can rivet to the final mesh
        self.controlRivetMeshes =  [self.upperLipMesh, self.lowerLidMesh]
        self.baseGeosToDeform = [self.upperLipBaseMesh, self.lowerLidBaseMesh]
        self.projectionMeshes = [self.projectionMeshUpper, self.projectionMeshLower]
        self.slideFalloffDicts = [self.upperLidSlideFalloffDict, self.lowerLidSlideFalloffDict]
        self.slideCtrlShapeOffsets = [self.slideCtrlShapeOffset1, self.slideCtrlShapeOffset2, self.slideCtrlShapeOffset3]
        self.tierCounts = [self.tierCounts[0], self.tierCounts[1], self.tierCounts[2]]
        self.tierStartElemIdxs = [0, self.tierCounts[0], self.tierCounts[1] + self.tierCounts[0]]
        self.tierAddAtIndex = [0, self.tierCounts[0], self.tierCounts[1] + self.tierCounts[0]]


        if not self.rivet_orient_patch:
            self.rivet_orient_patch = self.slidePatch
        self.slideDeformers = {}
        self.slideCurveWeights = {}
        self.slideWeightStack = {}
        self.isAddingNewElems = [False, True, True]
        self.connectFalloffs = [False, True, True]
        self.matDefNames = ["MatrixDeformer1", "MatrixDeformer2", "MatrixDeformer3"]
        self.ctrlPositions = {}
        self.ctrlRotations = {}
        # falloffCurveWeightNodes= [None, self.name + "CurveWeights", self.name + "CurveWeights"]
        for posIdx, position in enumerate(["Upper", "Lower"]):
            currName = self.side + "_" + self.component_name + position + "Slide"
            self.slideDeformers[position] = slideSimple.SlideSimple(name = currName,
                                                geoToDeform=self.deformMeshes[posIdx],
                                                slidePatch=self.slidePatch,
                                                slidePatchBase=self.slidePatchBase,
                                                baseGeoToDeform=self.baseGeosToDeform[posIdx],
                                                rotationAmount=True,
                                                component_name=self.component_name)
            self.slideDeformers[position].create()
            
            outputAttrs = [self.slideDeformers[position].deformer + ".weightArrays[0].vWeights"]
            outputAttrs_LR = [self.slideDeformers[position].deformer + ".weightArrays[0].uWeights"]
            self.ctrlPositions[position] = []
            self.ctrlRotations[position] = []

            for idx in range(3):

                self.slideCurveWeights[position] = weightStack.AnimCurveWeight(name=currName + "CurveWeights",
                                                                               baseGeo=self.baseGeosToDeform[posIdx],
                                                                               ctrlNode=self.control,
                                                                               projectionGeo=self.projectionMeshes[posIdx],
                                                                               weightCurveNames=[],
                                                                               addNewElem=self.isAddingNewElems[idx],
                                                                               autoCreateAnimCurves = True,
                                                                               auto_create_name_side = self.side,
                                                                               autoCreateName = self.ctrlName + position + self.tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                                               singleFalloffName = self.ctrlName + position,
                                                                               autoCreateNum = self.tierCounts[idx],
                                                                               falloffCurveDict = self.slideFalloffDicts[posIdx],
                                                                               centerWeight = elements.CENTER_WEIGHTS[idx],
                                                                               outerWeight = elements.OUTER_WEIGHTS[idx],
                                                                               angle = elements.ANGLES[idx],
                                                                               nudge = elements.NUDGES[idx],
                                                                               lastAngle=elements.LAST_ANGLES[idx],
                                                                               component_name=self.component_name,

                                                                               )
                self.slideCurveWeights[position].create()

                currFalloffCurveWeightNode = None
                if posIdx > 0:
                    currFalloffCurveWeightNode = currName + "CurveWeights"
                self.slideWeightStack[position] = weightStack.WeightStack(name=currName + "WeightStack",
                                                                          geoToWeight=self.deformMeshes[posIdx],
                                                                          ctrlNode=self.control,
                                                                          inputWeightAttrs=self.slideCurveWeights[position].newKDoubleArrayOutputPlugs,
                                                                          addNewElem=self.isAddingNewElems[idx],
                                                                          outputAttrs = outputAttrs,
                                                                          outputAttrs_LR = outputAttrs_LR,
                                                                          autoCreate=True,
                                                                          auto_create_name_side = self.side,
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
                                                                          autoCreateName = self.ctrlName + position + self.tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                                          controlSize = self.slideCtrlSizes[idx],
                                                                          controlShapeOffset = self.slideCtrlShapeOffsets[idx],
                                                                          controlShape = self.slideIconShapeDict,
                                                                          controlLockAttrs=["ry", "rz", "sx", "sz"],
                                                                          component_name=self.component_name,

                                                                          )
                self.slideWeightStack[position].create()
                self.ctrlPositions[position].append(self.slideWeightStack[position].positionsFromWeights)
                self.ctrlRotations[position].append(self.slideWeightStack[position].rotationsFromWeights)
                weightStack.connect_weight_stack_anim_curve(self.slideWeightStack[position], self.slideCurveWeights[position])

                # Add controls to the container and connect to visibility

                # for ctrl in self.slideWeightStack[position].controls:
                #     cmds.container(self.container, edit=True, addNode=[ctrl])
                #     shape = misc.getShape(ctrl)
                #     cmds.connectAttr(self.slideContainerAttrNames[posIdx], shape + ".visibility", f=True)

    def lidMatDef(self):
        self.matDefCurveWeights = {}
        self.matDefCurveWeights = {}
        self.matDefWeightStack = {}
        self.matDeformersTranslate = {}
        self.matDeformersRotate = {}
        self.matDefCtrlShapeOffsets =  [self.matDefCtrlShapeOffset1,
                                        self.matDefCtrlShapeOffset2,
                                        self.matDefCtrlShapeOffset3]

        self.matDefIconShapeDicts = [manipulator_elements.primary_plus, manipulator_elements.secondary_plus, manipulator_elements.tertiary_plus]
        self.matDefFalloffDicts = [self.upperLidMatDefFalloffDict, self.lowerLidMatDefFalloffDict]

        for posIdx, position in enumerate(["Upper", "Lower"]):
            currName = self.side + "_" + self.component_name + position + "MatDef"
            for idx in range(3):
                ################################## MATRIX DEFORMER #####################################################################
                self.matDefCurveWeights[position] = weightStack.AnimCurveWeight(name=currName + "_AnimCurveWeights",
                                                                                baseGeo=self.baseGeosToDeform[posIdx],
                                                                                ctrlNode=self.control,
                                                                                projectionGeo=self.projectionMeshes[posIdx],
                                                                                weightCurveNames=[],
                                                                                addNewElem=self.isAddingNewElems[idx],
                                                                                autoCreateAnimCurves = True,
                                                                                auto_create_name_side = self.side,
                                                                                autoCreateName = self.ctrlName + position + self.tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                                                singleFalloffName = self.ctrlName + position + "MATDEFTEST",
                                                                                autoCreateNum = self.tierCounts[idx],
                                                                                falloffCurveDict = self.matDefFalloffDicts[posIdx],
                                                                                centerWeight = elements.CENTER_WEIGHTS[idx],
                                                                                outerWeight = elements.OUTER_WEIGHTS[idx],
                                                                                angle = elements.ANGLES[idx],
                                                                                nudge = elements.NUDGES[idx],
                                                                                lastAngle=elements.LAST_ANGLES[idx],
                                                                                component_name=self.component_name,
                                                                                )
                self.matDefCurveWeights[position].create()

                # Create a single matrix deformer (rotation order issues)
                self.matDeformersTranslate[position] = matrixDeformer.MatrixDeformer(name=currName + "_MatDefTranslate",
                                                                                     geoToDeform=self.deformMeshes[posIdx],
                                                                                     ctrlName=self.ctrlName + position + self.matDefNames[idx],
                                                                                     centerToParent=True,
                                                                                     addAtIndex=self.tierAddAtIndex[idx],
                                                                                     numToAdd=self.tierCounts[idx],
                                                                                     reverseDeformerOrder = True,
                                                                                     auto_create_name_side = self.side,
                                                                                     locatorName=currName + self.tierNames[idx] + "Trans",  # Primary, Secondary, Or Tertiatry
                                                                                     curveWeightsNode=self.matDefCurveWeights[position].node,
                                                                                     control_rivet_mesh=self.deformMeshes[posIdx],
                                                                                     curveWeightsConnectionIdx=self.tierAddAtIndex[idx],
                                                                                     translations = self.ctrlPositions[position][idx],
                                                                                     rotations = self.ctrlRotations[position][idx],
                                                                                     controlParent = self.slideWeightStack[position].controls,
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
                self.matDeformersTranslate[position].create()

                self.matDeformersRotate[position] = matrixDeformer.MatrixDeformer(name=currName + "_MatDefRotate",
                                                                                  geoToDeform=self.deformMeshes[posIdx],
                                                                                  ctrlName=self.ctrlName + position + self.matDefNames[idx],
                                                                                  centerToParent=True,
                                                                                  addAtIndex=self.tierAddAtIndex[idx],
                                                                                  numToAdd=self.tierCounts[idx],
                                                                                  reverseDeformerOrder = True,
                                                                                  auto_create_name_side = self.side,
                                                                                  locatorName=currName + self.tierNames[idx] + "Rot",  # Primary, Secondary, Or Tertiatry
                                                                                  curveWeightsNode=self.matDefCurveWeights[position].node,
                                                                                  control_rivet_mesh=self.deformMeshes[posIdx],
                                                                                  curveWeightsConnectionIdx=self.tierAddAtIndex[idx],
                                                                                  translations = self.ctrlPositions[position][idx],
                                                                                  rotations = self.ctrlRotations[position][idx],
                                                                                  controlParent = self.slideWeightStack[position].controls,
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
                self.matDeformersRotate[position].create()
                weightStack.connect_weight_stack_anim_curve(self.matDeformersRotate[position], self.matDefCurveWeights[position])
                weightStack.connect_weight_stack_anim_curve(self.matDeformersTranslate[position], self.matDefCurveWeights[position])

                # for ctrl in self.matDeformersTranslate[position].controls:
                #     cmds.container(self.container, edit=True, addNode=[ctrl])
                #     shape = misc.getShape(ctrl)
                #     cmds.connectAttr(self.matDefContainerAttrNames[idx], shape + ".visibility", f=True)

    def post_create(self):
        cmds.refresh()
        deformer_utils.cacheOutAllSlideDeformers()

    def create(self):
        super(Lid, self).create()
        self.prepare()
        self.unpack_args_from_guide()
        self.lidSlide()
        self.lidMatDef()
        self.post_create()

