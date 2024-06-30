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

class Mouth(base.Component):
    def __init__(self,
                 component_name="mouth",
                 mouth_guide_class=None, 
                nameMouth="mouth",
                nameJaw="jaw",
                deformMesh="jawMouth",
                baseGeoToDeform="jawMouthBase",
                
                slidePatch="C_mouthGuide_SLDE",
                slidePatchBase="C_mouthGuide_SLDEBASE",
                projectionMesh="C_mouthJawPkg_PRJ",
                rivet_orient_patch = "mouthGuide_RivetOrientPatch",
                 ###########################################################################################
                 # if you would like to auto place controls base on weights set these values to empty lists []
                 matDefTranslations = None,
                 matDefRotations = None,
                 matDefScales = None,
                 matDefHandWeightsDictionary = None,

                 ###########################################################################################
                 slideHandWeightsDictionary = None,

                 ctrlAutoPositionThreshold=.09,
                 slideSpeedDefaults = [.05, .05, .05],
                 rotationAmount = 1,
                 slideAttrs = ["C_mouth",
                               "L_corner",
                               "R_corner"],

                 slideWeightCurves_UD = [
                                         elements.MOUTH_UD,
                                         elements.L_CORNER_UD,
                                         elements.R_CORNER_UD,
                                        ],
                 slideWeightCurvesFalloff_UD = [
                                                elements.MOUTH_UD_FALLOFF,
                                                elements.L_CORNER_UD_FALLOFF,
                                                elements.R_CORNER_UD_FALLOFF,
                                               ], 

                 slideWeightCurves_LR = [
                                         elements.MOUTH_LR,
                                         elements.L_CORNER_LR,
                                         elements.R_CORNER_LR,
                                        ],
                 slideWeightCurvesFalloff_LR = [
                                                elements.MOUTH_LR_FALLOFF,
                                                elements.L_CORNER_LR_FALLOFF,
                                                elements.R_CORNER_LR_FALLOFF,
                                               ], 

                 matDefAttrs = ["C_mouth",
                                "L_corner",
                                "R_corner",
                                "L_cornerTwist",
                                "R_cornerTwist",
                                "L_cheekMass",
                                "R_cheekMass",
                                "C_jaw",
                                "C_jawSecondary"],

                manual_no_rivet_names = [ "C_jaw",
                                        "C_jawSecondary"],
                manual_constraint_dict = {"C_jaw":"head_control",
                                          "C_jawSecondary":"head_control"},
        
                 matDefCustomControlShapes=elements.JAW_MOUTH_MATDEF_CTRL_SHAPES,

                 matDefWeightCurves = [
                                        elements.C_MOUTH_MATDEF,
                                        elements.L_CORNER_MATDEF,
                                        elements.R_CORNER_MATDEF,
                                        elements.L_CORNER_TWIST_MATDEF,
                                        elements.R_CORNER_TWIST_MATDEF,
                                        elements.L_CHEEK_MASS_MATDEF,
                                        elements.R_CHEEK_MASS_MATDEF,
                                        elements.C_JAW_MATDEF,
                                        elements.C_JAW_SECONDARY_MATDEF,
                                        ],
                 matDefWeightCurvesFalloff = [
                                                elements.C_MOUTH_MATDEF_FALLOFF,
                                                elements.L_CORNER_MATDEF_FALLOFF,
                                                elements.R_CORNER_MATDEF_FALLOFF,
                                                elements.L_CORNER_TWIST_MATDEF_FALLOFF,
                                                elements.R_CORNER_TWIST_MATDEF_FALLOFF,
                                                elements.L_CHEEK_MASS_MATDEF_FALLOFF,
                                                elements.R_CHEEK_MASS_MATDEF_FALLOFF,
                                                elements.C_JAW_MATDEF_FALLOFF,
                                                elements.C_JAW_SECONDARY_MATDEF_FALLOFF,
                                               ],
                 componentDict = elements.MATDEF_COMPONENT_DICT,
                 control_rivet_mesh = None,

                **kw
                 ):
        super(Mouth, self).__init__(component_name=component_name, **kw)
        # Creating a clean dictionary to avoid inheriting arguments from base.Component
        self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()
        
        
        self.nameMouth=nameMouth
        self.nameJaw=nameJaw
        self.deformMesh=deformMesh
        self.baseGeoToDeform=baseGeoToDeform
        self.slidePatch=slidePatch
        self.slidePatchBase=slidePatchBase
        self.rivet_orient_patch = rivet_orient_patch
        self.projectionMesh=projectionMesh
        self.matDefTranslations = matDefTranslations
        self.matDefRotations = matDefRotations
        self.matDefScales = matDefScales
        self.matDefHandWeightsDictionary = matDefHandWeightsDictionary
        self.slideHandWeightsDictionary = slideHandWeightsDictionary
        self.ctrlAutoPositionThreshold=ctrlAutoPositionThreshold
        self.slideSpeedDefaults = slideSpeedDefaults
        self.rotationAmount = rotationAmount
        self.slideAttrs = slideAttrs
        self.slideWeightCurves_UD = slideWeightCurves_UD
        self.slideWeightCurvesFalloff_UD = slideWeightCurvesFalloff_UD
        self.slideWeightCurves_LR =slideWeightCurves_LR
        self.slideWeightCurvesFalloff_LR = slideWeightCurvesFalloff_LR
        self.matDefAttrs = matDefAttrs
        self.manual_no_rivet_names = manual_no_rivet_names
        self.manual_constraint_dict = manual_constraint_dict
        
        self.matDefCustomControlShapes=matDefCustomControlShapes
        self.matDefWeightCurves = matDefWeightCurves
        self.matDefWeightCurvesFalloff =matDefWeightCurvesFalloff
        self.componentDict=componentDict
        self.component_name= component_name
        self.control_rivet_mesh = control_rivet_mesh
        if not self.control_rivet_mesh:
            self.control_rivet_mesh = self.deformMesh
        self.input_anchor_nodes.append(self.control_parent)

    def unpack_args_from_guide_class(self):
        return

    def prepare(self):
        self.control = cmds.circle(n= self.nameMouth + "Control", nr=[0,1,0])[0]
        cmds.parent(self.control, self.control_parent)


    def slide(self):
        # Temporary, create character hierarchy
        
        self.slideUDLR = slideSimple.SlideSimple(name = self.nameMouth + "_Slide",
                                               geoToDeform=self.deformMesh,
                                               slidePatch=self.slidePatch,
                                               slidePatchBase=self.slidePatchBase,
                                               baseGeoToDeform=self.baseGeoToDeform,
                                               rotationAmount=True,
                                               component_name=self.component_name
                                               
                                               )
        self.slideUDLR.create()


        UD_Names = [x + "UD" for x in self.slideAttrs]


        curveWeights_UD = weightStack.AnimCurveWeight(name=self.nameMouth + "_CurveWeights",
                                                      baseGeo=self.baseGeoToDeform,
                                                      ctrlNode=self.control,
                                                      projectionGeo=self.projectionMesh,
                                                      # weightCurveNames=UD_Names,
                                                      addNewElem=False,
                                                      autoCreateAnimCurves = False,
                                                      inputWeightCurvesDict=self.slideWeightCurves_UD,
                                                      inputWeightCurvesFalloffDict=self.slideWeightCurvesFalloff_UD,
                                                      component_name=self.component_name


                                                      )
        curveWeights_UD.create()

        LR_Names = [x + "LR" for x in self.slideAttrs]

        curveWeights_LR = weightStack.AnimCurveWeight(name=self.nameMouth + "_CurveWeights_LR",
                                                      baseGeo=self.baseGeoToDeform,
                                                      ctrlNode=self.control,
                                                      projectionGeo=self.projectionMesh,
                                                      # weightCurveNames=LR_Names,
                                                      addNewElem=False,
                                                      autoCreateAnimCurves = False,
                                                      inputWeightCurvesDict=self.slideWeightCurves_LR,
                                                      inputWeightCurvesFalloffDict=self.slideWeightCurvesFalloff_LR,
                                                      component_name=self.component_name

                                                      )
        curveWeights_LR.create()

        outputAttrs = [self.slideUDLR.deformer + ".weightArrays[0].vWeights"]
        outputAttrs_LR = [self.slideUDLR.deformer + ".weightArrays[0].uWeights"]

        slideCtrlPosOffsets=[0,0,0]
        slideCtrlShapeOffsets=[0,0,7]
        if not self.rivet_orient_patch:
            self.rivet_orient_patch = self.slidePatch
        slideIconShapeDict = manipulator_elements.circle

        stack = weightStack.WeightStack(name=self.nameMouth + "_WeightStack",
                                        geoToWeight=self.deformMesh,
                                        ctrlNode=self.control,
                                        factorAttrNames=self.slideAttrs,
                                        # inputWeightAttrs=curveWeights_LR.newKDoubleArrayOutputPlugs,
                                        addNewElem=False,
                                        outputAttrs = outputAttrs,
                                        outputAttrs_LR = outputAttrs_LR,
                                        autoCreate=False,
                                        controlPositionWeightsThreshold=self.ctrlAutoPositionThreshold,
                                        controlPositionOffset=slideCtrlPosOffsets,
                                        controlRivetMesh = self.control_rivet_mesh,
                                        controlAutoOrientMesh=self.rivet_orient_patch,
                                        
                                        controlRivetAimMesh=self.rivet_orient_patch,
                                        controlSpeedDefaults = self.slideSpeedDefaults,
                                        controlParent = self.control_parent,
                                        connectFalloff = True,
                                        isOutputKDoubleArray=True,
                                        falloffCurveWeightNode=None,  # If a weight node already exists, use it
                                        # autoCreateName=ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                        controlSize = 3,
                                        controlShapeOffset = slideCtrlShapeOffsets,
                                        controlShape = slideIconShapeDict,
                                        repositionRivetCtrls = False,
                                        controlLockAttrs=[],
                                        inputWeightAttrs_UD=curveWeights_UD.newKDoubleArrayOutputPlugs,
                                        inputWeightAttrs_LR=curveWeights_LR.newKDoubleArrayOutputPlugs,
                                        component_name=self.component_name
                                        )
        stack.create()
        weightStack.connect_weight_stack_anim_curve(stack, curveWeights_UD)
        weightStack.connect_weight_stack_anim_curve(stack, curveWeights_LR, is_node_LR=True)

    def matDef(self):
        self.matDefCurveWeights = weightStack.AnimCurveWeight(name=self.nameJaw + "MatDefCurveWeights",
                                                              baseGeo=self.baseGeoToDeform,
                                                              ctrlNode=self.control,
                                                              projectionGeo=self.projectionMesh,
                                                              # weightCurveNames=[],
                                                              addNewElem=False,
                                                              autoCreateAnimCurves = False,
                                                              inputWeightCurvesDict=self.matDefWeightCurves,
                                                              inputWeightCurvesFalloffDict=self.matDefWeightCurvesFalloff,
                                                              controlAutoOrientMesh = self.rivet_orient_patch,
                                                              component_name=self.component_name

                                                              )
        self.matDefCurveWeights.create()

        cmds.refresh()
        # you can only get the positions after the node has been created and had a chance to calculate the weights
        self.matDefCurveWeights.getPositionsAndRotationsFromWeights()

        # Create a single matrix deformer (rotation order issues)
        matDefCtrlShapeOffsets = [0,2,4.5]
        matDefCtrlShapeSizes = 1

        rotLocatorNames = [x + "Rot" for x in self.matDefAttrs]
        transLocatorNames = [x + "Trans" for x in self.matDefAttrs]
        
        pivotTranslations = self.matDefCurveWeights.positionsFromWeights
        pivotRotations = self.matDefCurveWeights.rotationsFromWeights
        pivotScale = [[1,1,1] for x in self.matDefAttrs]
        # ctrlTranslations = []
        # ctrlRotations = []
        # ctrlScale = []
        if self.matDefTranslations:
            pivotTranslations = self.matDefTranslations
        # if self.matDefTranslations and self.ctrlTranslations:
        #     ctrlTranslations = self.ctrlTranslations
        if self.matDefRotations:
            pivotRotations = self.matDefRotations
        # if self.matDefTranslations and self.ctrlRotations:
        #     ctrlRotations = self.ctrlRotations

        if self.matDefScales:
            pivotScale = self.matDefScales
        # if self.matDefTranslations and self.ctrlScale:
        #     ctrlScale = self.ctrlScale

        if self.matDefCustomControlShapes:
            matDefCtrlShapeOffsets =  [0,0,0]
            matDefCtrlShapeSizes = 1
        self.mat_def_translate = matrixDeformer.MatrixDeformer(name=self.nameJaw + "Translate_MatrixDef",
                                                               geoToDeform=self.deformMesh,
                                                               ctrlName=self.matDefAttrs,
                                                               manualLocatorNames = transLocatorNames,
                                                               manual_no_rivet_names = self.manual_no_rivet_names,
                                                               manual_constraint_dict = self.manual_constraint_dict,
                                                               centerToParent=True,
                                                               addAtIndex=0,
                                                               numToAdd=False,
                                                               # offset=[0,0,1],
                                                               reverseDeformerOrder = True,
                                                               # locatorName=name + tierNames[idx] + "Trans", # Primary, Secondary, Or Tertiatry
                                                               # rotationTranforms=stack.controls,
                                                               curveWeightsNode=self.matDefCurveWeights.node,
                                                               control_rivet_mesh=self.control_rivet_mesh,
                                                               curveWeightsConnectionIdx=0,
                                                               translations = pivotTranslations,
                                                               rotations = pivotRotations,
                                                               scales = pivotScale,
                                                               # ctrlTranslations = ctrlTranslations,
                                                               # ctrlRotations = ctrlRotations,
                                                               # ctrlScales = ctrlScale,
                                                               controlParent = self.control_parent,
                                                               rigParent = self.rig,
                                                               offset = matDefCtrlShapeOffsets,
                                                               size = matDefCtrlShapeSizes,
                                                               # locatorName = name + "MatDefTranslateLocator",
                                                               # locations=[position],
                                                               hide = True,
                                                               connectTranslate = True,
                                                               connectRotate = False,
                                                               connectScale = False,
                                                               controlShapeDict=manipulator_elements.primary_plus,
                                                               controlAutoOrientMesh = self.rivet_orient_patch,
                                                               controlType=1,
                                                               # customControlShapes = self.matDefCustomControlShapes,
                                                               component_name=self.component_name
                                                               )
        self.mat_def_translate.create()

        self.mat_def_rotate = matrixDeformer.MatrixDeformer(name=self.nameJaw + "Rotate_MatrixDef",
                                                            geoToDeform=self.deformMesh,
                                                            ctrlName=self.matDefAttrs,
                                                            manualLocatorNames = rotLocatorNames,
                                                            manual_no_rivet_names = self.manual_no_rivet_names,
                                                            manual_constraint_dict = self.manual_constraint_dict,
                                                            centerToParent=True,
                                                            addAtIndex=0,
                                                            numToAdd=False,
                                                            # offset=[0,0,1],
                                                            reverseDeformerOrder = True,
                                                            # locatorName=name + tierNames[idx] + "Trans", # Primary, Secondary, Or Tertiatry
                                                            # rotationTranforms=stack.controls,
                                                            curveWeightsNode=self.matDefCurveWeights.node,
                                                            control_rivet_mesh=self.control_rivet_mesh,
                                                            curveWeightsConnectionIdx=0,
                                                            translations = pivotTranslations,
                                                            rotations = pivotRotations,
                                                            controlParent = self.control_parent,
                                                            rigParent = self.rig,
                                                            offset = matDefCtrlShapeOffsets,
                                                            size = matDefCtrlShapeSizes,
                                                            # locatorName = name + "MatDefTranslateLocator",
                                                            # locations=[position],
                                                            hide = True,
                                                            connectTranslate = False,
                                                            connectRotate = True,
                                                            connectScale = False,
                                                            controlShapeDict=manipulator_elements.primary_plus,
                                                            controlAutoOrientMesh = self.rivet_orient_patch,
                                                            controlType=1,
                                                            component_name=self.component_name
                                                            )
                              
        self.mat_def_rotate.create()
        weightStack.connect_weight_stack_anim_curve(self.mat_def_translate, self.matDefCurveWeights)
        weightStack.connect_weight_stack_anim_curve(self.mat_def_rotate, self.matDefCurveWeights)

    def post_create(self):
        cmds.refresh()
        deformer_utils.cacheOutAllSlideDeformers()

    def create(self):
        super(Mouth, self).create()
        self.unpack_args_from_guide_class()
        self.prepare()
        self.slide()
        self.matDef()
        self.post_create()