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

class MouthJaw(object):
    @initialize.initializer
    def __init__(self,
                 nameMouth="mouth",
                 nameJaw="jaw",
                 deformMesh=[""],
                 baseGeoToDeform=[""],
                 slidePatch="",
                 slidePatchBase="",
                 projectionMesh="",
                 characterName = "character",
                 controlParent="C_control_GRP",
                 rigParent="C_rig_GRP",

                 ###########################################################################################
                 # if you would like to auto place controls base on weights set these values to empty lists []
                 matDefTranslations = None,
                 matDefRotations = None,
                 matDefScales = None,
                 matDefHandWeightsDictionary = None,
                #  ctrlTranslations = elements.JAW_MOUTH_MATDEF_CTRL_TRANSLATIONS,
                #  ctrlRotations = elements.JAW_MOUTH_MATDEF_CTRL_ROTATIONS,
                #  ctrlScale = elements.JAW_MOUTH_MATDEF_CTRL_SCALES,


                 ###########################################################################################
                 slideHandWeightsDictionary = None,

                 ctrlAutoPositionThreshold=.9999,
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

                                
                 ):
        pass

    def prepare(self):
        if not (cmds.objExists("C_{0}_GRP".format(self.characterName))):
            misc.create_rig_hier(char_name=self.characterName)

        self.control = cmds.circle(n= self.nameMouth + "Control", nr=[0,1,0])[0]
        cmds.parent(self.control, self.controlParent)


    def slide(self):
        # Temporary, create character hierarchy
        
        self.slideUDLR = slideSimple.SlideSimple(name = self.nameMouth + "LipSlide",
                                               geoToDeform=self.deformMesh,
                                               slidePatch=self.slidePatch,
                                               slidePatchBase=self.slidePatchBase,
                                               baseGeoToDeform=self.baseGeoToDeform,
                                               rotationAmount=True)
        self.slideUDLR.create()


        UD_Names = [x + "UD" for x in self.slideAttrs]


        curveWeights_UD = weightStack.AnimCurveWeight(name=self.nameMouth + "CurveWeights",
                                            baseGeo=self.baseGeoToDeform,
                                            ctrlNode=self.control,
                                            projectionGeo=self.projectionMesh,
                                            # weightCurveNames=UD_Names,
                                            addNewElem=False,
                                            autoCreateAnimCurves = False,
                                            inputWeightCurvesDict=self.slideWeightCurves_UD,
                                            inputWeightCurvesFalloffDict=self.slideWeightCurvesFalloff_UD,

        )
        curveWeights_UD.create()

        LR_Names = [x + "LR" for x in self.slideAttrs]

        curveWeights_LR = weightStack.AnimCurveWeight(name=self.nameMouth + "CurveWeights_LR",
                                            baseGeo=self.baseGeoToDeform,
                                            ctrlNode=self.control,
                                            projectionGeo=self.projectionMesh,
                                            # weightCurveNames=LR_Names,
                                            addNewElem=False,
                                            autoCreateAnimCurves = False,
                                            inputWeightCurvesDict=self.slideWeightCurves_LR,
                                            inputWeightCurvesFalloffDict=self.slideWeightCurvesFalloff_LR,


        )
        curveWeights_LR.create()

        outputAttrs = [self.slideUDLR.deformer + ".weightArrays[0].vWeights"]
        outputAttrs_LR = [self.slideUDLR.deformer + ".weightArrays[0].uWeights"]

        slideCtrlPosOffsets=[0,0,0]
        slideCtrlShapeOffsets=[0,0,7]
        controlRivetMesh = self.deformMesh
        controlAutoOrientMesh = self.slidePatch
        slideIconShapeDict = elements.circle

        stack = weightStack.WeightStack(name=self.nameMouth + "WeightStack",
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
                                        controlRivetMesh = controlRivetMesh,
                                        controlAutoOrientMesh=controlAutoOrientMesh,
                                        controlRivetAimMesh=controlAutoOrientMesh,
                                        controlSpeedDefaults = self.slideSpeedDefaults,
                                        controlParent = self.controlParent,
                                        connectFalloff = True,
                                        isOutputKDoubleArray=True,
                                        falloffCurveWeightNode=None, # If a weight node already exists, use it
                                        # autoCreateName=ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                        controlSize = 3,
                                        controlShapeOffset = slideCtrlShapeOffsets,
                                        controlShape = slideIconShapeDict,
                                        repositionRivetCtrls = False,
                                        controlLockAttrs=[],
                                        inputWeightAttrs_UD=curveWeights_UD.newKDoubleArrayOutputPlugs,
                                        inputWeightAttrs_LR=curveWeights_LR.newKDoubleArrayOutputPlugs,
                                        )
        stack.create()

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
                                                    controlAutoOrientMesh = self.slidePatch,

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

        matDef = matrixDeformer.MatrixDeformer(name=self.nameJaw + "_MatDefTranslate",
                                geoToDeform=self.deformMesh,
                                ctrlName=self.matDefAttrs,
                                manualLocatorNames = transLocatorNames,
                                centerToParent=True,
                                addAtIndex=0,
                                numToAdd=False,
                                # offset=[0,0,1],
                                reverseDeformerOrder = True,
                                # locatorName=name + tierNames[idx] + "Trans", # Primary, Secondary, Or Tertiatry
                                # rotationTranforms=stack.controls,
                                curveWeightsNode=self.matDefCurveWeights.node,
                                geoToConstrainMesh=self.deformMesh,
                                curveWeightsConnectionIdx=0,
                                translations = pivotTranslations,
                                rotations = pivotRotations,
                                scales = pivotScale,
                                # ctrlTranslations = ctrlTranslations,
                                # ctrlRotations = ctrlRotations,
                                # ctrlScales = ctrlScale,
                                controlParent = self.controlParent,
                                rigParent = self.rigParent,
                                offset = matDefCtrlShapeOffsets,
                                size = matDefCtrlShapeSizes,
                                # locatorName = name + "MatDefTranslateLocator",
                                # locations=[position],
                                hide = True,
                                connectTranslate = True,
                                connectRotate = False,
                                connectScale = False,
                                controlShapeDict=elements.primaryPlus,
                                controlAutoOrientMesh = self.slidePatch,
                                controlType=1,
                                customControlShapes = self.matDefCustomControlShapes,

                                )
                              
        matDef.create()
        matDef = matrixDeformer.MatrixDeformer(name=self.nameJaw + "_MatDefRotate",
                            geoToDeform=self.deformMesh,
                            ctrlName=self.matDefAttrs,
                            manualLocatorNames = rotLocatorNames,
                            centerToParent=True,
                            addAtIndex=0,
                            numToAdd=False,
                            # offset=[0,0,1],
                            reverseDeformerOrder = True,
                            # locatorName=name + tierNames[idx] + "Trans", # Primary, Secondary, Or Tertiatry
                            # rotationTranforms=stack.controls,
                            curveWeightsNode=self.matDefCurveWeights.node,
                            geoToConstrainMesh=self.deformMesh,
                            curveWeightsConnectionIdx=0,
                            translations = pivotTranslations,
                            rotations = pivotRotations,
                            controlParent = self.controlParent,
                            rigParent = self.rigParent,
                            offset = matDefCtrlShapeOffsets,
                            size = matDefCtrlShapeSizes,
                            # locatorName = name + "MatDefTranslateLocator",
                            # locations=[position],
                            hide = True,
                            connectTranslate = False,
                            connectRotate = True,
                            connectScale = True,
                            controlShapeDict=elements.primaryPlus,
                            controlAutoOrientMesh = self.slidePatch,
                            controlType=1,
                            )
                              
        matDef.create()

    def create(self):
        self.prepare()
        self.slide()
        self.matDef()

    def setPositions(self):
        if self.componentDict:
            lhExport.lh_component_import(manipDict=self.componentDict)

    def setHandWeights(self):
        if self.matDefHandWeightsDictionary:
            deformerUtils.rebuildMatDefWeightOverrides(self.matDefHandWeightsDictionary)
        if self.slideHandWeightsDictionary:
            deformerUtils.rebuildSlideWeightOverrides(self.slideHandWeightsDictionary)




