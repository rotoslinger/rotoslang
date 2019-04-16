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
# from rig.deformers import self.base
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
# reload(self.base)
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



class Line(object):
    @initialize.initializer
    def __init__(
                self,
                name="lowerLip",
                characterName = "character",
                controlParent="C_control_GRP",
                rigParent="C_rig_GRP",
                upperLip = False,
                ctrlName = None,  # this will be used as a way to reuse controls between different components and deformers
                containerName = "lip_container",
                multiSlideForBaseCurve=False,

                tierCount1=1,
                tierCount2=3,
                tierCount3=9,

                falloffDefaults=(-10, -9.9, -4, 10.0),

                ################# Slides ########################

                falloffSlideName = None,

                slideCtrlSize1=1,
                slideCtrlSize2=.65,
                slideCtrlSize3=.35,

                slideCtrlShapeOffset1=[0,0.0,2],
                slideCtrlShapeOffset2=[0,0.0,2],
                slideCtrlShapeOffset3=[0,0.0,2],

                slideCtrlPosOffset1=[0, 0.0, 0],
                slideCtrlPosOffset2=[0, 0.0, 0],
                slideCtrlPosOffset3=[0, 0.0, 0],

                slideFalloffDefaults=(-10, -9.9, -4, 10.0),
                slideFalloffDefaultCurve = None,

                slideIconShapeDict = elements.circle,

                slideControlSpeedDefaults = [.1,.1,.1],

                ################# MatrixDeformers ###############
                falloffMatrixDeformerName = None,

                matDefCtrlSize1=.5,
                matDefCtrlSize2=.5,
                matDefCtrlSize3=.5,

                matDefCtrlShapeOffset1=[0,0.0,2],
                matDefCtrlShapeOffset2=[0,0.0,2],
                matDefCtrlShapeOffset3=[0,0.0,2],

                matDefFalloffCurve=None,

                falloffMatrixDefaults=(-11, -7, -2, 10.0),
                falloffIttsMatDef=["linear","linear","linear","linear"],
                falloffOttsMatDef=["linear","spline","linear","linear"],
                matDefIconShapeDicts = [elements.primaryPlus, elements.secondaryPlus, elements.tertiaryPlus],

                ################# ThickDeformers ###############
                doLipThick = True,
                falloffLipThickName = None,
                thickCtrlSize1=.7,
                thickCtrlSize2=.65,
                thickCtrlSize3=.35,

                thickCtrlShapeOffset1 = [ 0, -2, 2],
                thickCtrlShapeOffset2 = [0,-2.0,1],
                thickCtrlShapeOffset3 = [0,-2.0,1],

                thickToPoint = (0, 0.978, -0.208),
                falloffThickDefaults=(10, -1, -4, 10.0),

                thickFalloffCurve = elements.LOWER_LIP_THICK_FALLOFF,


                ################ Roll Deformer ####################
                rollCurveName = "upperLipCurve",
                doLipRoll = True,
                falloffLipRollName = None,
                falloffRollDefaults=(-10, -9.9, -4, 10.0),

                controlRivetMesh = None,
                ctrlAutoPositionThreshold = .9,

                rollFalloffCurve = elements.LOWER_LIP_ROLL_FALLOFF,

                controlAutoOrientMesh="slide",
                repositionRivetCtrls=False,

                fileName="/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/humanLipTest.ma",
                deformMesh="humanLipsLower",
                base="humanLipsLowerBase",
                projectionMesh="lowLipProjection",


                slidePatch="slide",
                slidePatchBase="slideBase"):
                pass

    def create(self):

        # if you want to share falloffs between all deformers leave the falloff names None, but more self.control is better...
        if not self.ctrlName:
            self.ctrlName = self.name

        if not self.falloffSlideName: # Falloff for lip slide should have a much more broad falloff compared to the rest
            self.falloffSlideName = self.ctrlName

        if not self.falloffMatrixDeformerName: # Falloff for lip the matrix deformer is going to be minimal because it is used for tweaks and puckers
            self.falloffMatrixDeformerName = self.ctrlName + "MATDEFTEST"

        if not self.falloffLipThickName: # Falloff for lip thick should be minimal
            self.falloffLipThickName = self.ctrlName + "LIPTHICK"

        if not self.falloffLipRollName: # Falloff for lip roll may be more broad, but not as broad as the slide falloff
            self.falloffLipRollName = self.ctrlName + "LIPROLL"

        if self.fileName:
            cmds.file( self.fileName, i=True, f=True )

        if not self.controlRivetMesh:
            self.controlRivetMesh = self.deformMesh

        # Temporary, create character hierarchy
        if not (cmds.objExists("C_{0}_GRP".format(self.characterName))):
            misc.create_rig_hier(char_name=self.characterName)

        self.control = cmds.circle(n= self.name + "Control", nr=[0,1,0])[0]
        cmds.parent(self.control, self.controlParent)

        slideUD = slideSimple.SlideSimple(self.name + "LipSlide", geoToDeform=self.deformMesh, slidePatch=self.slidePatch, slidePatchBase=self.slidePatchBase, baseGeoToDeform=self.base)
        slideUD.create()

        outputAttrs = [slideUD.deformer + ".weightArrays[0].vWeights"]
        outputAttrs_LR = [slideUD.deformer + ".weightArrays[0].uWeights"]
        # super crappy implementation, this should be made more elegant ASAP
        if self.multiSlideForBaseCurve:
            outputAttrs = [slideUD.deformer + ".weightArrays[0].vWeights", slideUD.deformer + ".weightArrays[1].vWeights"]
            outputAttrs_LR = [slideUD.deformer + ".weightArrays[0].uWeights", slideUD.deformer + ".weightArrays[1].uWeights"]
        # Loop Vars each divided into 3
        tierNames = ["Primary", "Secondary", "Tertiary"]
        tierDefaultVisibility = [True, True, True]
        tierCounts = [self.tierCount1, self.tierCount2, self.tierCount3]
        tierStartElemIdxs = [0, self.tierCount1, self.tierCount2 + self.tierCount1]
        tierAddAtIndex = [0, self.tierCount1, self.tierCount2 + self.tierCount1]
        isAddingNewElems = [False, True, True]
        slideCtrlShapeOffsets = [self.slideCtrlShapeOffset1, self.slideCtrlShapeOffset2, self.slideCtrlShapeOffset3]
        slideCtrlSizes = [self.slideCtrlSize1, self.slideCtrlSize2, self.slideCtrlSize3]
        matDefNames = ["MatrixDeformer1", "MatrixDeformer2", "MatrixDeformer3"]
        matDefCtrlShapeOffsets = [self.matDefCtrlShapeOffset1, self.matDefCtrlShapeOffset2, self.matDefCtrlShapeOffset3]
        matDefCtrlSizes = [self.matDefCtrlSize1, self.matDefCtrlSize2, self.matDefCtrlSize3]
        thickCtrlShapeOffsets = [self.thickCtrlShapeOffset1, self.thickCtrlShapeOffset2, self.thickCtrlShapeOffset3]
        thickCtrlSizes = [self.thickCtrlSize1, self.thickCtrlSize2, self.thickCtrlSize3 ]
        connectFalloffs = [False, True, True]
        falloffCurveWeightNodes= [None, self.name + "CurveWeights", self.name + "CurveWeights"]
        slideCtrlPosOffsets = [self.slideCtrlPosOffset1, self.slideCtrlPosOffset2, self.slideCtrlPosOffset3]
        centerWeights = [.6, .3, .3]
        outerWeights = [0, .5, .5]
        angles = [50, 0, 0]
        nudges = [0, -0.14, -0.14]
        lastAngles = [50, 60, 60]


        # Create container
        if not cmds.objExists(self.containerName):
            container = cmds.container(n=self.containerName)
        else:
            container = self.containerName
        slideContainerAttrNames = []
        matDefContainerAttrNames = []
        for ctrlTypeName in ["slide", "matDef"]:
            for idx, tierName in enumerate(tierNames):
                attrName = ctrlTypeName + tierName + "Vis"
                fullAttrName = container + "." + attrName
                if not cmds.objExists(fullAttrName):
                    cmds.addAttr(container, ln = attrName, at = "short", dv = tierDefaultVisibility[idx], min = 0, max = 1)
                    cmds.setAttr( fullAttrName, cb = True, k = False)
                if ctrlTypeName == "slide":
                    slideContainerAttrNames.append(fullAttrName)
                if ctrlTypeName == "matDef":
                    matDefContainerAttrNames.append(fullAttrName)


        for idx in range(3):
            autoCreateTimeRange = 20.0
            offset=0
            centerWeight = .6
            outerWeight = .0
            angle = 50
            nudge = -0.0
            intermediateVal = .0
            intermediateAngle=0

            lastAngle = 50
            lastIntermediateVal=.8
            lastIntermediateAngle=30

            curveWeights = weightStack.AnimCurveWeight(name=self.name + "CurveWeights",
                                                baseGeo=self.base,
                                                ctrlNode=self.control,
                                                projectionGeo=self.projectionMesh,
                                                weightCurveNames=[],
                                                addNewElem=isAddingNewElems[idx],
                                                autoCreateAnimCurves = True,
                                                autoCreateName = self.ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                                singleFalloffName = self.ctrlName,
                                                autoCreateNum = tierCounts[idx],
                                                falloffDefaults=self.falloffDefaults,
                                                centerWeight = elements.CENTER_WEIGHTS[idx],
                                                outerWeight = elements.OUTER_WEIGHTS[idx],
                                                angle = elements.ANGLES[idx],
                                                nudge = elements.NUDGES[idx],
                                                lastAngle=elements.LAST_ANGLES[idx],

            )
            curveWeights.create()


            stack = weightStack.WeightStack(name=self.name + "WeightStack",
                                            geoToWeight=self.base,
                                            ctrlNode=self.control,
                                            inputWeightAttrs=curveWeights.newKDoubleArrayOutputPlugs,
                                            addNewElem=isAddingNewElems[idx],
                                            outputAttrs = outputAttrs,
                                            outputAttrs_LR = outputAttrs_LR,
                                            autoCreate=True,
                                            controlPositionWeightsThreshold=self.ctrlAutoPositionThreshold,
                                            controlPositionOffset=slideCtrlPosOffsets[idx],
                                            controlRivetMesh = self.controlRivetMesh,
                                            controlAutoOrientMesh=self.controlAutoOrientMesh,
                                            controlRivetAimMesh=self.slidePatch,
                                            controlSpeedDefaults = self.slideControlSpeedDefaults,
                                            controlParent = self.controlParent,
                                            connectFalloff = connectFalloffs[idx],
                                            isOutputKDoubleArray=True,
                                            falloffCurveWeightNode=falloffCurveWeightNodes[idx], # If a weight node already exists, use it
                                            # falloffCurveWeightNode="TestCurveWeights",
                                            autoCreateName=self.ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                            controlSize = slideCtrlSizes[idx],
                                            controlShapeOffset = slideCtrlShapeOffsets[idx],
                                            controlShape = self.slideIconShapeDict,
                                            repositionRivetCtrls = self.repositionRivetCtrls,
                                            controlLockAttrs=["ry", "rz", "sx", "sz"],
                                            )
            stack.create()

            # Add controls to the container and connect to visibility

            for ctrl in stack.controls:
                cmds.container(container, edit=True, addNode=[ctrl])
                shape = misc.getShape(ctrl)
                cmds.connectAttr(slideContainerAttrNames[idx], shape + ".visibility", f=True)


            ################################## MATRIX DEFORMER #####################################################################
            curveWeights = weightStack.AnimCurveWeight(name=self.name + "MatDef",
                                                        baseGeo=self.base,
                                                        ctrlNode=self.control,
                                                        projectionGeo=self.projectionMesh,
                                                        weightCurveNames=[],
                                                        addNewElem=isAddingNewElems[idx],
                                                        autoCreateAnimCurves = True,
                                                        autoCreateName = self.ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                                        singleFalloffName = self.falloffMatrixDeformerName,
                                                        autoCreateNum = tierCounts[idx],
                                                        falloffDefaults=self.falloffMatrixDefaults,
                                                        falloffItts=self.falloffIttsMatDef,
                                                        falloffOtts=self.falloffOttsMatDef,
                                                        falloffCurveDict = self.matDefFalloffCurve,
                                                        startElem = tierAddAtIndex[idx],
                                                        centerWeight = elements.CENTER_WEIGHTS[idx],
                                                        outerWeight = elements.OUTER_WEIGHTS[idx],
                                                        angle = elements.ANGLES[idx],
                                                        nudge = elements.NUDGES[idx],
                                                        lastAngle=elements.LAST_ANGLES[idx],
            )
            curveWeights.create()
            


            # Create a single matrix deformer (rotation order issues)
            matDef = matrixDeformer.MatrixDeformer(name=self.name + "_MatDefTranslate",
                                    geoToDeform=self.deformMesh,
                                    ctrlName=self.ctrlName + matDefNames[idx],
                                    centerToParent=True,
                                    addAtIndex=tierAddAtIndex[idx],
                                    numToAdd=tierCounts[idx],
                                    # offset=[0,0,1],
                                    reverseDeformerOrder = True,
                                    locatorName=self.name + tierNames[idx] + "Trans", # Primary, Secondary, Or Tertiatry
                                    # rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    geoToConstrainMesh=self.deformMesh,
                                    curveWeightsConnectionIdx=tierAddAtIndex[idx],
                                    translations = stack.positionsFromWeights,
                                    rotations = stack.rotationsFromWeights,
                                    controlParent = stack.controls,
                                    rigParent = self.rigParent,
                                    offset = matDefCtrlShapeOffsets[idx],
                                    size = matDefCtrlSizes[idx],
                                    # locatorName = self.name + "MatDefTranslateLocator",
                                    # locations=[position],
                                    hide = True,
                                    connectTranslate = True,
                                    connectRotate = False,
                                    connectScale = False,
                                    controlShapeDict=self.matDefIconShapeDicts[idx],
                                    
                                    )
            matDef.create()

            matDef = matrixDeformer.MatrixDeformer(name=self.name + "_MatDefRotate",
                                    geoToDeform=self.deformMesh,
                                    ctrlName=self.ctrlName + matDefNames[idx],
                                    centerToParent=True,
                                    addAtIndex=tierAddAtIndex[idx],
                                    numToAdd=tierCounts[idx],
                                    # offset=[0,0,1],
                                    reverseDeformerOrder = True,
                                    locatorName=self.name + tierNames[idx] + "ROT", # Primary, Secondary, Or Tertiatry
                                    # rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    geoToConstrainMesh=self.deformMesh,
                                    curveWeightsConnectionIdx=tierAddAtIndex[idx],
                                    translations = stack.positionsFromWeights,
                                    rotations = stack.rotationsFromWeights,
                                    controlParent = stack.controls,
                                    rigParent = self.rigParent,
                                    offset = matDefCtrlShapeOffsets[idx],
                                    size = matDefCtrlSizes[idx],
                                    # locatorName = self.name + "MatDefRotateLocator",
                                    # locations=[position],
                                    hide = True,
                                    connectTranslate = False,
                                    connectRotate = True,
                                    connectScale = True,
                                    controlShapeDict=self.matDefIconShapeDicts[idx],
                                    
                                    
                                    )
            matDef.create()


            for ctrl in matDef.controls:
                cmds.container(container, edit=True, addNode=[ctrl])
                shape = misc.getShape(ctrl)

                cmds.connectAttr(matDefContainerAttrNames[idx], shape + ".visibility", f=True)

            ################################## LIP THICK DEFORMER #####################################################################
            vectorDeformer = None
            if self.doLipThick:
                curveWeights = weightStack.AnimCurveWeight(name=self.name + "ThickDef",
                                                baseGeo=self.base,
                                                ctrlNode=self.control,
                                                projectionGeo=self.projectionMesh,
                                                weightCurveNames=[],
                                                addNewElem=isAddingNewElems[idx],
                                                autoCreateAnimCurves = True,
                                                autoCreateName = self.ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                                singleFalloffName = self.falloffLipThickName,
                                                autoCreateNum = tierCounts[idx],
                                                falloffCurveDict = self.thickFalloffCurve,
                                                falloffDefaults=self.falloffThickDefaults,
                                                falloffItts=["linear","linear","linear","linear"],
                                                falloffOtts=["linear","linear","linear","linear"],
                                                startElem = tierAddAtIndex[idx],
                                                centerWeight = elements.CENTER_WEIGHTS[idx],
                                                outerWeight = elements.OUTER_WEIGHTS[idx],
                                                angle = elements.ANGLES[idx],
                                                nudge = elements.NUDGES[idx],
                                                lastAngle=elements.LAST_ANGLES[idx],


                )
                curveWeights.create()

                syAttrs = []
                for ctrl in stack.controls:
                    # Make plus minus average to 0 out scales
                    syAttr = ctrl + ".sy"
                    PMA = cmds.createNode("plusMinusAverage", n=ctrl + "ThickDefSy_PMA")
                    cmds.connectAttr(syAttr, PMA + ".input1D[0]")
                    cmds.setAttr(PMA + ".input1D[1]", -1)
                    syAttrs.append(PMA + ".output1D")
                thickShape = elements.upArrow
                if not self.upperLip:
                    thickShape = elements.downArrow
                stack = weightStack.WeightStack(name=self.name + "WeightStackThick",
                                                geoToWeight=self.deformMesh,
                                                ctrlNode=self.control,
                                                inputWeightAttrs=curveWeights.newKDoubleArrayOutputPlugs,
                                                addNewElem=isAddingNewElems[idx],
                                                UDLR = False,
                                                autoCreate=True,
                                                controlPositionWeightsThreshold=.1,
                                                controlRivetMesh = self.controlRivetMesh,
                                                controlAutoOrientMesh=self.controlAutoOrientMesh,
                                                controlRivetAimMesh=self.slidePatch,
                                                controlParent = self.controlParent,
                                                # controlShape=thickShape,
                                                connectFalloff = connectFalloffs[idx],
                                                isOutputKDoubleArray=True,
                                                autoCreateName=self.ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry

                                                # autoCreateName=self.ctrlName + tierNames[idx] + "THICK", # Primary, Secondary, Or Tertiatry
                                                controlSize = thickCtrlSizes[idx],
                                                controlShapeOffset = thickCtrlShapeOffsets[idx],
                                                # self.repositionRivetCtrls = self.repositionRivetCtrls,
                                                repositionRivetCtrls = False,

                                                controlSyConnectionAttrs = syAttrs,
                                                controlSpeedDefaults = [1,1,1],
                                                controlShapeOrient=[0,0,0],
                                                # controlLockAttrs=["tx", "tz", "ry", "rz", "sx", "sy", "sz"],
                                                controlLockAttrs=["tx", "tz", "ry", "rz", "sx", "sz"],
                                                )
                stack.create()

                vectorDeformer = vectorDeformerSimple.VectorDeformerSimple(name = self.name + "THICKTEST", geoToDeform=self.deformMesh, weightStackNode=stack.node, toPoint = self.thickToPoint)
                vectorDeformer.create() 

            
            ################################## LIP ROLL DEFORMER #####################################################################    
            if self.doLipRoll:
                curveWeights = weightStack.AnimCurveWeight(name=self.name + "CurveWeightsROLL",
                                                baseGeo=self.base,
                                                ctrlNode=self.control,
                                                projectionGeo=self.projectionMesh,
                                                weightCurveNames=[],
                                                addNewElem=isAddingNewElems[idx],
                                                autoCreateAnimCurves = True,
                                                autoCreateName = self.ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                                singleFalloffName = self.falloffLipRollName,
                                                autoCreateNum = tierCounts[idx],
                                                falloffCurveDict = self.rollFalloffCurve,
                                                falloffDefaults=self.falloffThickDefaults,
                                                falloffItts=["linear","linear","linear","linear"],
                                                falloffOtts=["linear","linear","linear","linear"],
                                                startElem = tierAddAtIndex[idx],
                                                centerWeight = elements.CENTER_WEIGHTS[idx],
                                                outerWeight = elements.OUTER_WEIGHTS[idx],
                                                angle = elements.ANGLES[idx],
                                                nudge = elements.NUDGES[idx],
                                                lastAngle=elements.LAST_ANGLES[idx],


                )
                curveWeights.create()

                rxAttrs = []
                for ctrl in stack.controls:
                    rxAttrs.append(ctrl + ".rx")
                thickShape = elements.upArrow
                if not self.upperLip:
                    thickShape = elements.downArrow

                stack = weightStack.WeightStack(name=self.name + "WeightStackRoll",
                                                geoToWeight=self.deformMesh,
                                                ctrlNode=self.control,
                                                inputWeightAttrs=curveWeights.newKDoubleArrayOutputPlugs,
                                                addNewElem=isAddingNewElems[idx],
                                                UDLR = False,
                                                #outputAttrs = thickOutputattrs,
                                                autoCreate=True,
                                                controlPositionWeightsThreshold=self.ctrlAutoPositionThreshold,
                                                # controlPositionOffset=self.slideCtrlPosOffset1,
                                                controlRivetMesh = self.controlRivetMesh,
                                                controlAutoOrientMesh=self.controlAutoOrientMesh,
                                                controlRivetAimMesh=self.slidePatch,
                                                #controlSpeedDefaults = self.slideControlSpeedDefaults,
                                                controlParent = self.controlParent,
                                                controlShape=thickShape,
                                                connectFalloff = connectFalloffs[idx],
                                                isOutputKDoubleArray=True,
                                                # falloffCurveWeightNode="TestCurveWeights",
                                                # autoCreateName=self.ctrlName + tierNames[idx] + "ROLL", # Primary, Secondary, Or Tertiatry
                                                autoCreateName=self.ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                                controlSize = thickCtrlSizes[idx],
                                                controlShapeOffset = thickCtrlShapeOffsets[idx],
                                                repositionRivetCtrls = False,
                                                controlRxConnectionAttrs = rxAttrs,
                                                # controlRxConnectionAttrs= True,
                                                controlSpeedDefaults = [1,1,1],
                                                controlShapeOrient=[0,0,0],
                                                controlLockAttrs=["tx", "tz", "ty", "ry", "rz", "sx", "sy", "sz"],
                                                )
                stack.create()
                # rollDeformer = vectorDeformerSimple.VectorDeformerSimple(self.name = self.name + "THICKTEST", geoToDeform=self.deformMesh, weightStackNode=stack.node, toPoint = self.thickToPoint)
                # rollDeformer.create()

                curveRoll = curveRollSimple.CurveRollSimple(
                                                            name=self.name + "ROLLTEST",
                                                            deformerType="LHCurveRollSimple",
                                                            membershipWeightsAttr = "",
                                                            rollWeightsAttr = "",
                                                            geoToDeform=self.deformMesh,
                                                            baseGeoToDeform=self.base,
                                                            rollCurve=self.rollCurveName,
                                                            duplicateCurve=True,
                                                            simplifyCurve=True,
                                                            cvCount = 6,
                                                            weightStackNode=stack.node,

                )
                curveRoll.create()
            
        vecDef = None
        if vectorDeformer:
            vecDef = vectorDeformer.deformer
            if type(self.deformMesh) == list:
                for mesh in self.deformMesh:
                    cmds.reorderDeformers(slideUD.deformer, vectorDeformer.deformer, misc.getShape(mesh))
            else:
                cmds.reorderDeformers(slideUD.deformer, vectorDeformer.deformer, misc.getShape(self.deformMesh))

        return slideUD.deformer, vecDef