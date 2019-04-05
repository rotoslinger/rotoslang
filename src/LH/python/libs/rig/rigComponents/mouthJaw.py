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
                 ctrlAutoPositionThreshold=.9999,
                 slideSpeedDefaults = [.05, .05, .05],
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

                 matDefAttrs = ["mouth",
                                "L_corner",
                                "R_corner",
                                "L_cornerTwist",
                                "R_cornerTwist",
                                "L_cheekMass",
                                "R_cheekMass",
                                "jaw",
                                "jawSecondary"],
                 ):
        pass

    def slide(self):
        # Temporary, create character hierarchy
        if not (cmds.objExists("C_{0}_GRP".format(self.characterName))):
            misc.create_rig_hier(char_name=self.characterName)

        self.control = cmds.circle(n= self.nameMouth + "Control", nr=[0,1,0])[0]
        cmds.parent(self.control, self.controlParent)

        
        self.slideUDLR = slideSimple.SlideSimple(name = self.nameMouth + "LipSlide",
                                               geoToDeform=self.deformMesh,
                                               slidePatch=self.slidePatch,
                                               slidePatchBase=self.slidePatchBase,
                                               baseGeoToDeform=self.baseGeoToDeform)
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
                                        geoToWeight=self.baseGeoToDeform,
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
        pass
    
    def create(self):
        self.slide()
        self.matDef()


