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

from rig_2.node import utils as node_utils
reload(node_utils)

from rig_2.component import utils as component_utils
reload(component_utils)

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
                 C_projectionMesh="C_brow_PRJ",
                 rivet_orient_patch = "browGuide_RivetOrientPatch",
                 l_brow_fit_curve = "L_brow_CRV",
                 r_brow_fit_curve = "R_brow_CRV",
                 c_brow_fit_curve = "C_unibrow_CRV",
                 l_brow_fit_curve_base = "L_brow_CRVBASE",
                 r_brow_fit_curve_base = "R_brow_CRVBASE",
                 c_brow_fit_curve_base = "C_brow_CRVBASE",
                 order_before_deformer = None,
                 primaryBrowShapeAnimCurveDict = elements.BROW_PRIMARY_ANIM_CURVE,
                 ctrlAutoPositionThreshold=.09,
                 slideIconShapeDict = manipulator_elements.circle,
                 slideControlSpeedDefaults = [.1,.1,.1],
                 leftBrowSlideFalloffDict = elements.L_BROW_SLIDE_FALLOFF,
                 rightBrowSlideFalloffDict = elements.R_BROW_SLIDE_FALLOFF,
                 leftBrowMatDefFalloffDict = elements.L_BROW_SLIDE_FALLOFF,
                 rightBrowMatDefFalloffDict = elements.R_BROW_SLIDE_FALLOFF,
                 slideCtrlSizes = [1, .65, .35],
                 slideCtrlShapeOffset1=[0,0.0,.2],
                 slideCtrlShapeOffset2=[0,0.0,.2],
                 slideCtrlShapeOffset3=[0,0.0,.2],

                 matDefCtrlSizes = [.7, .65, .35],
                 matDefCtrlShapeOffset1=[0,-2.0,.2],
                 matDefCtrlShapeOffset2=[0,-2.0,.1],
                 matDefCtrlShapeOffset3=[0,-2.0,.1],

                 tierDefaultVisibility = [True, True, True],
                 fit_curve=False,
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
        self.C_projectionMesh=C_projectionMesh
        self.rivet_orient_patch = rivet_orient_patch
        self.l_brow_fit_curve = l_brow_fit_curve
        self.r_brow_fit_curve = r_brow_fit_curve
        self.c_brow_fit_curve = c_brow_fit_curve
        self.l_brow_fit_curve_base = l_brow_fit_curve_base
        self.r_brow_fit_curve_base = r_brow_fit_curve_base
        self.c_brow_fit_curve_base = c_brow_fit_curve_base
        self.order_before_deformer = order_before_deformer
                  
        
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
        self.fit_curve =fit_curve
        
        self.tierNames = ["Primary", "Secondary", "Tertiary"]
        self.input_anchor_nodes.append(self.control_parent)
        if not self.fit_curve:
            self.order_before_deformer = None
    def prepare(self):
        self.control = cmds.circle(n= self.nameBrows + "Control", nr=[0,1,0])[0]
        cmds.parent(self.control, self.control_parent)

                    
    def unpack_args_from_guide(self):
        # TODO need geo class to get geometry args from!!!
        # For Example, it would look something like this:
        # if self.model_class:
            # self.leftBrowMesh = self.model_class.leftBrowMesh
            # self.leftBrowBaseMesh = self.model_class.leftBrowBaseMesh
            # self.rightBrowMesh =  self.model_class.rightBrowMesh
            # self.rightBrowBaseMesh = self.model_class.rightBrowBaseMesh

        if self.guide_class:
            # In order for the volume lip curves to deforme in the correct way, while keeping the guides live, we need to reorder the deformers
            self.order_before_deformer = self.guide_class.ffd_deformer
            if not self.fit_curve:
                self.order_before_deformer = None
                
            # find args from the guide class:
            self.slidePatch = self.guide_class.slide_nurbs
            self.slidePatchBase = self.guide_class.slide_nurbs_base
            self.L_projectionMesh=self.guide_class.l_projection_mesh
            self.R_projectionMesh=self.guide_class.r_projection_mesh
            self.C_projectionMesh=self.guide_class.c_projection_mesh
            self.rivet_orient_patch = self.guide_class.rivet_orient_patch
            self.l_brow_fit_curve = self.guide_class.l_curve
            self.r_brow_fit_curve = self.guide_class.r_curve
            self.c_brow_fit_curve = self.guide_class.c_curve
            self.l_brow_fit_curve_base = self.guide_class.l_curve_base
            self.r_brow_fit_curve_base = self.guide_class.r_curve_base
            self.c_brow_fit_curve_base = self.guide_class.c_curve_base
            self.brow_curves = {
                                "L":self.l_brow_fit_curve,
                                "R":self.r_brow_fit_curve,
                                "C":self.c_brow_fit_curve,
                                
                                
                                
                                }


    def browSlide(self):
        self.deformMeshes =  [self.leftBrowMesh, self.rightBrowMesh]
        self.repositionRivetCtrls = False

        if self.fit_curve:
            self.deformMeshes =  [self.l_brow_fit_curve, self.r_brow_fit_curve]
            self.repositionRivetCtrls = True
        # Eventually this will need to be dynamic so we can rivet to the final mesh
        self.controlRivetMeshes =  [self.leftBrowMesh, self.rightBrowMesh]
        self.baseGeosToDeform = [self.leftBrowBaseMesh, self.rightBrowBaseMesh]
        if self.fit_curve:
            self.baseGeosToDeform = [self.l_brow_fit_curve_base, self.r_brow_fit_curve_base]
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
                self.slideCurveWeights[side] = weightStack.AnimCurveWeight(name=currName + "_CurveWeights",
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
                self.slideWeightStack[side] = weightStack.WeightStack(name=currName + "_WeightStack",
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
                                                                      repositionRivetCtrls = self.repositionRivetCtrls
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
            currName = side + "_" + self.nameBrows + "MatDef"
            for idx in range(3):
                ################################## MATRIX DEFORMER #####################################################################
                self.matDefCurveWeights[side] = weightStack.AnimCurveWeight(name=currName + "_CurveWeights",
                                                                            baseGeo=self.baseGeosToDeform[posIdx],
                                                                            ctrlNode=self.control,
                                                                            projectionGeo=self.projectionMeshes[posIdx],
                                                                            weightCurveNames=[],
                                                                            addNewElem=self.isAddingNewElems[idx],
                                                                            autoCreateAnimCurves = True,
                                                                            autoCreateName = self.ctrlName + side + self.tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                                            singleFalloffName = self.ctrlName + side + "MatDefSingle",
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

    def reorder_deformers(self):
        if self.order_before_deformer:
            for posIdx, side in enumerate(["L", "R"]):
                deform_mesh = misc.getShape(self.deformMeshes[posIdx])
                
                # print deform_mesh, "deform_mesh", self.slideDeformers[side].deformer, "deformer",self.order_before_deformer, "orderBefore Deformer"
                cmds.reorderDeformers( self.slideDeformers[side].deformer, self.order_before_deformer, deform_mesh)
                cmds.reorderDeformers( self.matDeformersTranslate[side].deformer, self.order_before_deformer, deform_mesh)
                cmds.reorderDeformers( self.matDeformersRotate[side].deformer, self.order_before_deformer, deform_mesh)

    def post_create(self):
        cmds.refresh()
        deformer_utils.cacheOutAllSlideDeformers()
        
    def reposition_controls_by_weights(self):
        for side in ["L", "R"]:
            
            component_utils.autoposition_weight_stack_controls(self.slideWeightStack[side].node, project_to_curve=self.brow_curves[side])

    def create(self):
        super(Brow, self).create()
        self.prepare()
        self.unpack_args_from_guide()
        self.browSlide()
        self.browMatDef()
        self.reorder_deformers()
        self.post_create()
        self.reposition_controls_by_weights()



class Unibrow(Brow):
    def __init__(self,
                 tierCounts=[1,3,10],
                 primaryBrowShapeAnimCurveDict = elements.BROW_PRIMARY_ANIM_CURVE,
                 c_secondary_anim_curve_dict=None,
                 l_secondary_anim_curve_dict=None,
                 r_secondary_anim_curve_dict=None,
                 browSlideFalloffDict = elements.L_BROW_SLIDE_FALLOFF,
                 browMatDefFalloffDict = elements.L_BROW_SLIDE_FALLOFF,
                 deform_mesh="",
                 base_deform_mesh = "",
                 **kw
    ):
        super(Unibrow, self).__init__(tierCounts=tierCounts, primaryBrowShapeAnimCurveDict=primaryBrowShapeAnimCurveDict, **kw)
        # self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()
        self.tierCouts = tierCounts
        self.primaryBrowShapeAnimCurveDict = primaryBrowShapeAnimCurveDict
        self.c_secondary_anim_curve_dict = c_secondary_anim_curve_dict
        self.l_secondary_anim_curve_dict = l_secondary_anim_curve_dict
        self.r_secondary_anim_curve_dict = r_secondary_anim_curve_dict
        self.browSlideFalloffDict = browSlideFalloffDict
        self.browMatDefFalloffDict = browMatDefFalloffDict
        self.deform_mesh = deform_mesh
        self.base_deform_mesh = base_deform_mesh


    def browSlide(self):
        self.repositionRivetCtrls = False
        if self.fit_curve:
            self.deform_mesh =  self.c_brow_fit_curve
            self.repositionRivetCtrls = True
            
        # Eventually this will need to be dynamic so we can rivet to the final mesh
        self.base_deform_mesh = [self.leftBrowBaseMesh, self.rightBrowBaseMesh]
        if self.fit_curve:
            self.base_deform_mesh = self.c_brow_fit_curve_base
        self.projectionMeshes = [self.L_projectionMesh, self.R_projectionMesh]
        self.slideFalloffDicts = [self.leftBrowSlideFalloffDict, self.rightBrowSlideFalloffDict]
        self.slideCtrlShapeOffsets = [self.slideCtrlShapeOffset1, self.slideCtrlShapeOffset2, self.slideCtrlShapeOffset3]
        self.tierCounts = [self.tierCounts[0], self.tierCounts[1], self.tierCounts[2]]
        self.tierStartElemIdxs = [0, self.tierCounts[0], self.tierCounts[1] + self.tierCounts[0]]
        self.tierAddAtIndex = [0, self.tierCounts[0], self.tierCounts[1] + self.tierCounts[0]]
        # if not self.rivet_orient_patch:
        #     self.rivet_orient_patch = self.slidePatch
        self.isAddingNewElems = [False, True, True]
        self.connectFalloffs = [False, True, True]
        self.matDefNames = ["MatrixDeformer1", "MatrixDeformer2", "MatrixDeformer3"]
        self.curveOverrideDict = [self.primaryBrowShapeAnimCurveDict, None, None]
        # falloffCurveWeightNodes= [None, self.name + "CurveWeights", self.name + "CurveWeights"]
        currName = side + "_" + self.nameBrows + "Slide"
        self.slideDeformer = slideSimple.SlideSimple(name = currName,
                                            geoToDeform=self.deform_mesh,
                                            slidePatch=self.slidePatch,
                                            slidePatchBase=self.slidePatchBase,
                                            baseGeoToDeform=self.base_deform_mesh,
                                            rotationAmount=True,
                                            component_name=self.component_name,
                                            
                                            )
        self.slideDeformer.create()
        
        outputAttrs = [self.slideDeformer.deformer + ".weightArrays[0].vWeights"]
        outputAttrs_LR = [self.slideDeformer.deformer + ".weightArrays[0].uWeights"]
        self.ctrlPositions = []
        self.ctrlRotations = []

        for idx in range(3):
            self.slideCurveWeights = weightStack.AnimCurveWeight(name=currName + "_CurveWeights",
                                                                        baseGeo=self.base_deform_mesh,
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
            self.slideCurveWeights.create()
            currFalloffCurveWeightNode = None
            if posIdx > 0:
                currFalloffCurveWeightNode = currName + "CurveWeights"
            self.slideWeightStack = weightStack.WeightStack(name=currName + "_WeightStack",
                                                                    geoToWeight=self.deform_mesh,
                                                                    ctrlNode=self.control,
                                                                    inputWeightAttrs=self.slideCurveWeights.newKDoubleArrayOutputPlugs,
                                                                    addNewElem=self.isAddingNewElems[idx],
                                                                    outputAttrs = outputAttrs,
                                                                    outputAttrs_LR = outputAttrs_LR,
                                                                    autoCreate=True,
                                                                    controlPositionWeightsThreshold=self.ctrlAutoPositionThreshold,
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
                                                                    repositionRivetCtrls = self.repositionRivetCtrls
                                                                    )
            self.slideWeightStack.create()
            
            
            self.ctrlPositions.append(self.slideWeightStack.positionsFromWeights)
            self.ctrlRotations.append(self.slideWeightStack.rotationsFromWeights)
            
            weightStack.connect_weight_stack_anim_curve(self.slideWeightStack, self.slideCurveWeights)

            
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
            currName = side + "_" + self.nameBrows + "MatDef"
            for idx in range(3):
                ################################## MATRIX DEFORMER #####################################################################
                self.matDefCurveWeights[side] = weightStack.AnimCurveWeight(name=currName + "_CurveWeights",
                                                                            baseGeo=self.base_deform_mesh,
                                                                            ctrlNode=self.control,
                                                                            projectionGeo=self.projectionMeshes[posIdx],
                                                                            weightCurveNames=[],
                                                                            addNewElem=self.isAddingNewElems[idx],
                                                                            autoCreateAnimCurves = True,
                                                                            autoCreateName = self.ctrlName + side + self.tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                                            singleFalloffName = self.ctrlName + side + "MatDefSingle",
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
                                                                                 geoToDeform=self.deform_mesh,
                                                                                 ctrlName=self.ctrlName + side + self.matDefNames[idx],
                                                                                 centerToParent=True,
                                                                                 addAtIndex=self.tierAddAtIndex[idx],
                                                                                 numToAdd=self.tierCounts[idx],
                                                                                 reverseDeformerOrder = True,
                                                                                 locatorName=currName + self.tierNames[idx] + "Trans",  # Primary, Secondary, Or Tertiatry
                                                                                 curveWeightsNode=self.matDefCurveWeights[side].node,
                                                                                 control_rivet_mesh=self.deform_mesh,
                                                                                 curveWeightsConnectionIdx=self.tierAddAtIndex[idx],
                                                                                 translations = self.ctrlPositions[idx],
                                                                                 rotations = self.ctrlRotations[idx],
                                                                                 controlParent = self.slideWeightStack.controls,
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
                                                                              geoToDeform=self.deform_mesh,
                                                                              ctrlName=self.ctrlName + side + self.matDefNames[idx],
                                                                              centerToParent=True,
                                                                              addAtIndex=self.tierAddAtIndex[idx],
                                                                              numToAdd=self.tierCounts[idx],
                                                                              reverseDeformerOrder = True,
                                                                              locatorName=currName + self.tierNames[idx] + "Rot",  # Primary, Secondary, Or Tertiatry
                                                                              curveWeightsNode=self.matDefCurveWeights[side].node,
                                                                              control_rivet_mesh=self.deform_mesh,
                                                                              curveWeightsConnectionIdx=self.tierAddAtIndex[idx],
                                                                              translations = self.ctrlPositions[idx],
                                                                              rotations = self.ctrlRotations[idx],
                                                                              controlParent = self.slideWeightStack.controls,
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

    def reorder_deformers(self):
        if self.order_before_deformer:
            for posIdx, side in enumerate(["L", "R"]):
                deform_mesh = misc.getShape(self.deform_mesh)
                
                # print deform_mesh, "deform_mesh", self.slideDeformer.deformer, "deformer",self.order_before_deformer, "orderBefore Deformer"
                cmds.reorderDeformers( self.slideDeformer.deformer, self.order_before_deformer, deform_mesh)
                cmds.reorderDeformers( self.matDeformersTranslate[side].deformer, self.order_before_deformer, deform_mesh)
                cmds.reorderDeformers( self.matDeformersRotate[side].deformer, self.order_before_deformer, deform_mesh)
        
    def reposition_controls_by_weights(self):
        component_utils.autoposition_weight_stack_controls(self.slideWeightStack.node, project_to_curve=self.brow_curves["C"])

    def create(self):
        super(Unibrow, self).create()
        self.prepare()
        self.unpack_args_from_guide()
        self.browSlide()
        # self.browMatDef()
        # self.reorder_deformers()
        self.post_create()
        self.reposition_controls_by_weights()
