import inspect
from collections import OrderedDict

from maya import cmds
from rig.deformers import matrixDeformer
import importlib
importlib.reload(matrixDeformer)

from rig.deformers import slideSimple
importlib.reload(slideSimple)

from rig.deformers import blendshapeSimple
importlib.reload(blendshapeSimple)

from rig.deformers import vectorDeformerSimple
importlib.reload(vectorDeformerSimple)

from rig.deformers import curveRollSimple
importlib.reload(curveRollSimple)

from rig.utils import misc
importlib.reload(misc)

from rig.utils import LHCurveDeformerCmds
importlib.reload(LHCurveDeformerCmds)

from rig.rigComponents import elements, meshRivetCtrl
importlib.reload(meshRivetCtrl)

from rig.deformers import utils as deformer_utils
importlib.reload(deformer_utils)

from rig_2.manipulator import elements as manipulator_elements
importlib.reload(manipulator_elements)

from rig_2.component.subcomponent import weightStack
importlib.reload(weightStack)

from rig_2.component import base as component_base
importlib.reload(component_base)


class Lip(component_base.Component):
    def __init__(
                self,
                component_name="lip",
                name="lowerLip",
                position_name="lower",
                characterName = "character",
                order_before_deformer=None,
                upperLip = False,
                ctrlName = None,  # this will be used as a way to reuse controls between different components and deformers
                containerName = "lip_container",
                multiSlideForBaseCurve=False,
                component_type="LIP",
                tierCount1=1,
                tierCount2=3,
                tierCount3=9,
                falloffDefaults=(-10, -9.9, -4, 10.0),
                ################# Slides ########################
                falloffSlideName = None,
                slideCtrlSize1=1,
                slideCtrlSize2=.65,
                slideCtrlSize3=.35,
                slideCtrlShapeOffset1=[0, 2, 0],
                slideCtrlShapeOffset2=[0, 2, 0],
                slideCtrlShapeOffset3=[0, 2, 0],
                slideCtrlPosOffset1=[0, 0.0, 0],
                slideCtrlPosOffset2=[0, 0.0, 0],
                slideCtrlPosOffset3=[0, 0.0, 0],
                slideFalloffDefaults=(-10, -9.9, -4, 10.0),
                slideFalloffDefaultCurve = None,
                slideIconShapeDict = manipulator_elements.circle,
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
                matDefIconShapeDicts = [manipulator_elements.primary_plus,
                                        manipulator_elements.secondary_plus,
                                        manipulator_elements.tertiary_plus],
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
                slidePatchBase="slideBase",
                ):
        super(Lip, self).__init__(component_name=component_name)
        # weight node is a subcomponent so it will not have any exposed args...
        self.ordered_args = OrderedDict()
        
        # args
        self.name=name
        self.characterName = characterName
        self.order_before_deformer=order_before_deformer
        self.upperLip = upperLip
        self.position_name = position_name
        self.ctrlName =ctrlName
        self.containerName = containerName
        self.multiSlideForBaseCurve=multiSlideForBaseCurve
        self.component_type=component_type
        self.tierCount1=tierCount1
        self.tierCount2=tierCount2
        self.tierCount3=tierCount3
        self.falloffDefaults=falloffDefaults
        self.falloffSlideName =falloffSlideName
        self.slideCtrlSize1=slideCtrlSize1
        self.slideCtrlSize2=slideCtrlSize2
        self.slideCtrlSize3=slideCtrlSize3
        self.slideCtrlShapeOffset1=slideCtrlShapeOffset1
        self.slideCtrlShapeOffset2=slideCtrlShapeOffset2
        self.slideCtrlShapeOffset3=slideCtrlShapeOffset3
        self.slideCtrlPosOffset1=slideCtrlPosOffset1
        self.slideCtrlPosOffset2=slideCtrlPosOffset2
        self.slideCtrlPosOffset3=slideCtrlPosOffset3
        self.slideFalloffDefaults=slideFalloffDefaults
        self.slideFalloffDefaultCurve = slideFalloffDefaultCurve
        self.slideIconShapeDict = slideIconShapeDict
        self.slideControlSpeedDefaults = slideControlSpeedDefaults
        self.falloffMatrixDeformerName =falloffMatrixDeformerName
        self.matDefCtrlSize1=matDefCtrlSize1
        self.matDefCtrlSize2=matDefCtrlSize2
        self.matDefCtrlSize3=matDefCtrlSize3
        self.matDefCtrlShapeOffset1=matDefCtrlShapeOffset1
        self.matDefCtrlShapeOffset2=matDefCtrlShapeOffset2
        self.matDefCtrlShapeOffset3=matDefCtrlShapeOffset3
        self.matDefFalloffCurve=matDefFalloffCurve
        self.falloffMatrixDefaults=falloffMatrixDefaults
        self.falloffIttsMatDef=falloffIttsMatDef
        self.falloffOttsMatDef=falloffOttsMatDef
        self.matDefIconShapeDicts =matDefIconShapeDicts
        self.doLipThick =doLipThick
        self.falloffLipThickName = falloffLipThickName
        self.thickCtrlSize1=thickCtrlSize1
        self.thickCtrlSize2=thickCtrlSize2
        self.thickCtrlSize3=thickCtrlSize3
        self.thickCtrlShapeOffset1 = thickCtrlShapeOffset1
        self.thickCtrlShapeOffset2 = thickCtrlShapeOffset2
        self.thickCtrlShapeOffset3 = thickCtrlShapeOffset3
        self.thickToPoint = thickToPoint
        self.falloffThickDefaults=falloffThickDefaults
        self.thickFalloffCurve = thickFalloffCurve
        self.rollCurveName = rollCurveName
        self.doLipRoll = doLipRoll
        self.falloffLipRollName = falloffLipRollName
        self.falloffRollDefaults=falloffRollDefaults
        self.controlRivetMesh =controlRivetMesh
        self.ctrlAutoPositionThreshold = ctrlAutoPositionThreshold
        self.rollFalloffCurve = rollFalloffCurve
        self.controlAutoOrientMesh=controlAutoOrientMesh
        self.repositionRivetCtrls=repositionRivetCtrls
        self.fileName=fileName
        self.deformMesh=deformMesh
        self.base=base
        self.projectionMesh=projectionMesh
        self.slidePatch=slidePatch
        self.slidePatchBase=slidePatchBase
        self.component_name=component_name

    def create_lip(self):

        # if you want to share falloffs between all deformers leave the falloff names None, but more self.control_parent is better...
        if not self.ctrlName:
            self.ctrlName = self.name

        if not self.falloffSlideName: # Falloff for lip slide should have a much more broad falloff compared to the rest
            self.falloffSlideName = self.ctrlName

        if not self.falloffMatrixDeformerName: # Falloff for lip the matrix deformer is going to be minimal because it is used for tweaks and puckers
            self.falloffMatrixDeformerName = self.ctrlName + "MatDef"

        if not self.falloffLipThickName: # Falloff for lip thick should be minimal
            self.falloffLipThickName = self.ctrlName + "Thick"

        if not self.falloffLipRollName: # Falloff for lip roll may be more broad, but not as broad as the slide falloff
            self.falloffLipRollName = self.ctrlName + "Roll"

        if self.fileName:
            cmds.file( self.fileName, i=True, f=True )

        # if not self.controlRivetMesh:

        #     self.controlRivetMesh = self.deformMesh

        # # Temporary, create character hierarchy
        # if not (cmds.objExists("C_{0}_GRP".format(self.characterName))):
        #     misc.create_rig_hier(name=self.characterName)

        # self.control_node = cmds.circle(n=self.name + "Control", nr=[0, 1, 0])[0]
        if cmds.objExists(self.ctrlName + "Control"):
            self.control_node = self.ctrlName + "Control"
        else:
            self.control_node = cmds.circle(n=self.ctrlName + "Control", nr=[0, 1, 0])[0]
            cmds.parent(self.control_node, self.control_parent)
            
            
        self.slide_ud = slideSimple.SlideSimple(self.name + "_SlideDef",
                                          geoToDeform=self.deformMesh,
                                          slidePatch=self.slidePatch,
                                          slidePatchBase=self.slidePatchBase,
                                          baseGeoToDeform=self.base,
                                          component_name=self.component_name, 
                                            # orderFrontOfChain=False,
                                            # orderParallel=False,
                                            # orderBefore=True,
                                            # orderAfter=False,
                                            # orderSplit=False,
                                            # orderExclusive=False,
                                          )
        self.slide_ud.create()


        outputAttrs = [self.slide_ud.deformer + ".weightArrays[0].vWeights"]
        outputAttrs_LR = [self.slide_ud.deformer + ".weightArrays[0].uWeights"]
        # super crappy implementation, this should be made more elegant ASAP
        if self.multiSlideForBaseCurve:
            outputAttrs = [self.slide_ud.deformer + ".weightArrays[0].vWeights", self.slide_ud.deformer + ".weightArrays[1].vWeights"]
            outputAttrs_LR = [self.slide_ud.deformer + ".weightArrays[0].uWeights", self.slide_ud.deformer + ".weightArrays[1].uWeights"]
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

            self.slide_curve_weights = weightStack.AnimCurveWeight(name=self.name + "Slide_CurveWeights",
                                                       baseGeo=self.base,
                                                       ctrlNode=self.control_node,
                                                       projectionGeo=self.projectionMesh,
                                                       weightCurveNames=[],
                                                       addNewElem=isAddingNewElems[idx],
                                                       autoCreateAnimCurves = True,
                                                       autoCreateName = self.ctrlName + tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                       singleFalloffName = self.ctrlName,
                                                       autoCreateNum = tierCounts[idx],
                                                       falloffDefaults=self.falloffDefaults,
                                                       centerWeight = elements.CENTER_WEIGHTS[idx],
                                                       outerWeight = elements.OUTER_WEIGHTS[idx],
                                                       angle = elements.ANGLES[idx],
                                                       nudge = elements.NUDGES[idx],
                                                       lastAngle=elements.LAST_ANGLES[idx],
                                                       component_name=self.component_name,


                                                       )
            self.slide_curve_weights.create()

            self.slide_weight_stack = weightStack.WeightStack(name=self.name + "Slide_WeightStack",
                                            geoToWeight=self.base,
                                            ctrlNode=self.control_node,
                                            inputWeightAttrs=self.slide_curve_weights.newKDoubleArrayOutputPlugs,
                                            addNewElem=isAddingNewElems[idx],
                                            outputAttrs = outputAttrs,
                                            outputAttrs_LR = outputAttrs_LR,
                                            autoCreate=True,
                                            controlPositionWeightsThreshold=self.ctrlAutoPositionThreshold,
                                            controlPositionOffset=slideCtrlPosOffsets[idx],
                                            controlRivetMesh = self.controlRivetMesh,
                                            controlAutoOrientMesh=self.controlAutoOrientMesh,
                                            controlRivetAimMesh=self.controlAutoOrientMesh,
                                            controlSpeedDefaults = self.slideControlSpeedDefaults,
                                            controlParent = self.control_parent,
                                            connectFalloff = connectFalloffs[idx],
                                            isOutputKDoubleArray=True,
                                            falloffCurveWeightNode=falloffCurveWeightNodes[idx],  # If a weight node already exists, use it
                                            # falloffCurveWeightNode="TestCurveWeights",
                                            autoCreateName=self.ctrlName + tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                            controlSize = slideCtrlSizes[idx],
                                            controlShapeOffset = slideCtrlShapeOffsets[idx],
                                            controlShape = self.slideIconShapeDict,
                                            repositionRivetCtrls = self.repositionRivetCtrls,
                                            controlLockAttrs=["ry", "rz", "sx", "sz"],
                                            component_name=self.component_name,
                                            )
            self.slide_weight_stack.create()
            
            weightStack.connect_weight_stack_anim_curve(self.slide_weight_stack, self.slide_curve_weights)
            ################################## MATRIX DEFORMER #####################################################################
            curveWeights = weightStack.AnimCurveWeight(name=self.name + "MatDef_AnimCurveWeight",
                                                       baseGeo=self.base,
                                                       ctrlNode=self.control_node,
                                                       projectionGeo=self.projectionMesh,
                                                       weightCurveNames=[],
                                                       addNewElem=isAddingNewElems[idx],
                                                       autoCreateAnimCurves = True,
                                                       autoCreateName = self.ctrlName + tierNames[idx],  # Primary, Secondary, Or Tertiatry
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
                                                       component_name=self.component_name,
                                                       )
            curveWeights.create()
            


            # Create a single matrix deformer (rotation order issues)
            self.mat_def_translate = matrixDeformer.MatrixDeformer(name=self.name + "Translate_MatrixDef",
                                                                   geoToDeform=self.deformMesh,
                                                                   ctrlName=self.ctrlName + matDefNames[idx],
                                                                   centerToParent=True,
                                                                    position=self.position_name,
                                                                   addAtIndex=tierAddAtIndex[idx],
                                                                   numToAdd=tierCounts[idx],
                                                                   type_name="Trans",
                                                                   # offset=[0,0,1],
                                                                   reverseDeformerOrder = True,
                                                                   locatorName= self.position_name + self.component_name + tierNames[idx] + "Trans",  # Primary, Secondary, Or Tertiatry
                                                                   curveWeightsNode=curveWeights.node,
                                                                   control_rivet_mesh=self.deformMesh,
                                                                   curveWeightsConnectionIdx=tierAddAtIndex[idx],
                                                                   translations = self.slide_weight_stack.positionsFromWeights,
                                                                   rotations = self.slide_weight_stack.rotationsFromWeights,
                                                                   controlParent = self.slide_weight_stack.controls,
                                                                   rigParent = self.rig,
                                                                   offset = matDefCtrlShapeOffsets[idx],
                                                                   size = matDefCtrlSizes[idx],
                                                                   # locatorName = self.name + "MatDefTranslateLocator",
                                                                   # locations=[position],
                                                                   hide = True,
                                                                   connectTranslate = True,
                                                                   connectRotate = False,
                                                                   connectScale = False,
                                                                   controlShapeDict=self.matDefIconShapeDicts[idx],
                                                                   component_name=self.component_name,
                                                                   )
            self.mat_def_translate.create()
            
            
                
                
            self.mat_def_rotate = matrixDeformer.MatrixDeformer(name=self.name + "Rotate_MatrixDef",
                                                                geoToDeform=self.deformMesh,
                                                                ctrlName=self.ctrlName + matDefNames[idx],
                                                                centerToParent=True,
                                                                addAtIndex=tierAddAtIndex[idx],
                                                                numToAdd=tierCounts[idx],
                                                                # offset=[0,0,1],
                                                                type_name="Rot",
                                                                reverseDeformerOrder = True,
                                                                position=self.position_name,
                                                                locatorName=self.position_name + self.component_name + tierNames[idx] + "Rot",  # Primary, Secondary, Or Tertiatry
                                                                # rotationTranforms=self.slide_weight_stack.controls,
                                                                curveWeightsNode=curveWeights.node,
                                                                control_rivet_mesh=self.deformMesh,
                                                                curveWeightsConnectionIdx=tierAddAtIndex[idx],
                                                                translations = self.slide_weight_stack.positionsFromWeights,
                                                                rotations = self.slide_weight_stack.rotationsFromWeights,
                                                                controlParent = self.slide_weight_stack.controls,
                                                                rigParent = self.rig,
                                                                offset = matDefCtrlShapeOffsets[idx],
                                                                size = matDefCtrlSizes[idx],
                                                                # locatorName = self.name + "MatDefRotateLocator",
                                                                # locations=[position],
                                                                hide = True,
                                                                connectTranslate = False,
                                                                connectRotate = True,
                                                                connectScale = True,
                                                                controlShapeDict=self.matDefIconShapeDicts[idx],
                                                                component_name=self.component_name,


                                                                )
            self.mat_def_rotate.create()
            
            weightStack.connect_weight_stack_anim_curve(self.mat_def_rotate, curveWeights)

            # for ctrl in matDef.controls:
            #     cmds.container(container, edit=True, addNode=[ctrl])
            #     shape = misc.getShape(ctrl)

            #     cmds.connectAttr(matDefContainerAttrNames[idx], shape + ".visibility", f=True)

            ################################## LIP THICK DEFORMER #####################################################################
            vectorDeformer = None
            if self.doLipThick:
                curveWeights = weightStack.AnimCurveWeight(name=self.name + "Thick_AnimCurveWeight",
                                                           baseGeo=self.base,
                                                           ctrlNode=self.control_node,
                                                           projectionGeo=self.projectionMesh,
                                                           weightCurveNames=[],
                                                           addNewElem=isAddingNewElems[idx],
                                                           autoCreateAnimCurves = True,
                                                           autoCreateName = self.ctrlName + tierNames[idx],  # Primary, Secondary, Or Tertiatry
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
                                                           component_name=self.component_name,

                                                           )
                curveWeights.create()

                syAttrs = []
                for ctrl in self.slide_weight_stack.controls:
                    # Make plus minus average to 0 out scales
                    syAttr = ctrl + ".sy"
                    PMA = cmds.createNode("plusMinusAverage", n=ctrl + "ThickDefSy_PMA")
                    cmds.connectAttr(syAttr, PMA + ".input1D[0]")
                    cmds.setAttr(PMA + ".input1D[1]", -1)
                    syAttrs.append(PMA + ".output1D")
                thickShape = manipulator_elements.up_arrow
                if not self.upperLip:
                    thickShape = manipulator_elements.down_arrow
                stack = weightStack.WeightStack(name=self.name + "Thick_WeightStack",
                                                geoToWeight=self.deformMesh,
                                                ctrlNode=self.control_node,
                                                inputWeightAttrs=curveWeights.newKDoubleArrayOutputPlugs,
                                                addNewElem=isAddingNewElems[idx],
                                                UDLR = False,
                                                autoCreate=True,
                                                controlPositionWeightsThreshold=.1,
                                                controlRivetMesh = self.controlRivetMesh,
                                                controlAutoOrientMesh=self.controlAutoOrientMesh,
                                                controlRivetAimMesh=self.controlAutoOrientMesh,
                                                controlParent = self.control_parent,
                                                # controlShape=thickShape,
                                                connectFalloff = connectFalloffs[idx],
                                                isOutputKDoubleArray=True,
                                                autoCreateName=self.ctrlName + tierNames[idx],  # Primary, Secondary, Or Tertiatry

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
                                                component_name=self.component_name,
                                                )
                stack.create()

                vectorDeformer = vectorDeformerSimple.VectorDeformerSimple(name = self.name + "_ThickDef",
                                                                           geoToDeform=self.deformMesh,
                                                                           weightStackNode=stack.node,
                                                                           toPoint = self.thickToPoint,
                                                                           parent = self.geo)
                vectorDeformer.create() 

                weightStack.connect_weight_stack_anim_curve(stack, curveWeights)

            ################################## LIP ROLL DEFORMER #####################################################################    
            if self.doLipRoll:
                curveWeights = weightStack.AnimCurveWeight(name=self.name + "Roll_AnimCurveWeights",
                                                           baseGeo=self.base,
                                                           ctrlNode=self.control_node,
                                                           projectionGeo=self.projectionMesh,
                                                           weightCurveNames=[],
                                                           addNewElem=isAddingNewElems[idx],
                                                           autoCreateAnimCurves = True,
                                                           autoCreateName = self.ctrlName + tierNames[idx],  # Primary, Secondary, Or Tertiatry
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
                                                           component_name=self.component_name,

                                                           )
                curveWeights.create()

                rxAttrs = []
                for ctrl in stack.controls:
                    rxAttrs.append(ctrl + ".rx")
                thickShape = manipulator_elements.up_arrow
                if not self.upperLip:
                    thickShape = manipulator_elements.down_arrow

                stack = weightStack.WeightStack(name=self.name + "Roll_WeightStack",
                                                geoToWeight=self.deformMesh,
                                                ctrlNode=self.control_node,
                                                inputWeightAttrs=curveWeights.newKDoubleArrayOutputPlugs,
                                                addNewElem=isAddingNewElems[idx],
                                                UDLR = False,
                                                #outputAttrs = thickOutputattrs,
                                                autoCreate=True,
                                                controlPositionWeightsThreshold=self.ctrlAutoPositionThreshold,
                                                # controlPositionOffset=self.slideCtrlPosOffset1,
                                                controlRivetMesh = self.controlRivetMesh,
                                                controlAutoOrientMesh=self.controlAutoOrientMesh,
                                                controlRivetAimMesh=self.controlAutoOrientMesh,
                                                #controlSpeedDefaults = self.slideControlSpeedDefaults,
                                                controlParent = self.control_parent,
                                                controlShape=thickShape,
                                                connectFalloff = connectFalloffs[idx],
                                                isOutputKDoubleArray=True,
                                                # falloffCurveWeightNode="TestCurveWeights",
                                                # autoCreateName=self.ctrlName + tierNames[idx] + "ROLL", # Primary, Secondary, Or Tertiatry
                                                autoCreateName=self.ctrlName + tierNames[idx],  # Primary, Secondary, Or Tertiatry
                                                controlSize = thickCtrlSizes[idx],
                                                controlShapeOffset = thickCtrlShapeOffsets[idx],
                                                repositionRivetCtrls = False,
                                                controlRxConnectionAttrs = rxAttrs,
                                                # controlRxConnectionAttrs= True,
                                                controlSpeedDefaults = [1,1,1],
                                                controlShapeOrient=[0,0,0],
                                                controlLockAttrs=["tx", "tz", "ty", "ry", "rz", "sx", "sy", "sz"],
                                                component_name=self.component_name,
                                                )
                stack.create()
                weightStack.connect_weight_stack_anim_curve(stack, curveWeights)

                curveRoll = curveRollSimple.CurveRollSimple(
                                                            name=self.name + "_RollDef",
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
                                                            component_name=self.component_name,

                )
                curveRoll.create()
            
        vecDef = None
        if vectorDeformer:
            vecDef = vectorDeformer.deformer
            if type(self.deformMesh) == list:
                for mesh in self.deformMesh:
                    cmds.reorderDeformers(self.slide_ud.deformer, vectorDeformer.deformer, misc.getShape(mesh))
            else:
                cmds.reorderDeformers(self.slide_ud.deformer, vectorDeformer.deformer, misc.getShape(self.deformMesh))

        self.slide_deformer = self.slide_ud.deformer
        self.vector_deformer = vecDef


        if self.order_before_deformer:
            cmds.reorderDeformers( self.slide_ud.deformer,self.order_before_deformer, misc.getShape(self.deformMesh))
            cmds.reorderDeformers( self.mat_def_translate.deformer, self.order_before_deformer, misc.getShape(self.deformMesh))
            cmds.reorderDeformers( self.mat_def_rotate.deformer,self.order_before_deformer, misc.getShape(self.deformMesh))


        return self.slide_ud.deformer, vecDef

    def post_create(self):
        cmds.refresh()
        deformer_utils.cacheOutAllSlideDeformers()

    def create(self):
        self.create_lip()
        self.post_create()
        
def lipCurveDeformSplit(name="C_UpperLipWire",
                        curve="lipCurve",
                        curveAim="lipCurveAim",
                        deformedGeometry="humanLipsUpper",
                        projectionPatch="upLipProjection",
                        deformedGeometryBase="humanLipsUpperBase",
                        addWeightStack=["upperLipWeightStack_LR", "upperLipWeightStack_UD"],
                        addAtIndex=9,
                        handPaint=False,
                        upperLip=True,
                        falloffDefaults = "",
                        falloffItts = "",
                        falloffOtts = "",
                        removePointIndicies=[],
                        reorderInFrontOfDeformer="",
                        curveDeformerAlgorithm=0,
                        curve_base=None,
                        component_name=None,
):

    if not falloffDefaults and upperLip:
        falloffDefaults = (-10, -9, -5, 20.0)
        falloffItts=["linear","linear","spline","linear"]
        falloffOtts=["linear","linear","linear","linear"]
    if not falloffDefaults and not upperLip:
        falloffDefaults = (20, 3.4, -1, -10)
        falloffItts=["linear","linear","linear","linear"]
        falloffOtts=["linear","linear","spline","linear"]
    blendshapeGeo = cmds.duplicate(deformedGeometry, n=name+"BlendshapeGeo")[0]
    cmds.setAttr(blendshapeGeo + ".visibility", 0)
    blendshape = blendshapeSimple.BlendshapeSimple(name = name + "ReverseBlendshape",
                                                   geoToDeform=deformedGeometry,
                                                   targetGeom=blendshapeGeo,
                                                    # orderFrontOfChain=False,
                                                    # orderParallel=True,
                                                    # orderBefore=False,
                                                    # orderAfter=False,
                                                    component_name=component_name
                                                   )
    blendshape.create()
    # Turn on Blending
    cmds.setAttr(blendshape.amountAttr, 1)
    blendshape = blendshape.deformer

    geoToWeight = deformedGeometryBase
    curveWeights = None
    inputWeightAttrs=[]
    if not handPaint:
        curveWeights = weightStack.AnimCurveWeight(name=name + "ReverseCurveDeformerAnimCurveWeights",
                                                   baseGeo=deformedGeometryBase,
                                                   ctrlNode=blendshapeGeo,
                                                   projectionGeo=projectionPatch,
                                                   weightCurveNames=[name + "CurveDeformerNormalize"],
                                                   addNewElem=False,
                                                   autoCreateAnimCurves = False,
                                                   autoCreateName = '',
                                                   singleFalloffName = '',
                                                   autoCreateNum = None,
                                                   falloffDefaults = falloffDefaults,
                                                   uKeyframesAllOnes=True,
                                                   falloffItts=falloffItts,
                                                   falloffOtts=falloffOtts,
                                                   component_name=component_name

                                                   )
        curveWeights.create()
        cmds.getAttr(curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray")

        inputWeightAttrs=[curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray", curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray"]
    factorAttrNames = ["reverse", "dummy"]
    inputWeightAttrs=["reverseWeights", "dummyWeights"]


    stack = weightStack.WeightStack(name=name + "NormalizeCurveDeformerWeights",
                                    geoToWeight=geoToWeight,
                                    ctrlNode=blendshapeGeo,
                                    inputWeightAttrs=inputWeightAttrs,
                                    factorAttrNames = factorAttrNames,
                                    operationVals=[0,6],
                                    addNewElem=False,
                                    outputAttrs = [blendshape + ".targetWeights"],
                                    autoCreate=False,
                                    UDLR = False,
                                    createControl=False,
                                    isOutputKDoubleArray=True,
                                    component_name=component_name
                                    )
    stack.create()

    cmds.setAttr(stack.ctrlNode + ".reverse", 1)
    cmds.setAttr(stack.ctrlNode + ".dummy", 1)

    geoToWeightShape = misc.getShape(stack.geoToWeight)

    cmds.connectAttr(curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray", stack.node+".inputs[0].inputWeights", f=True)
    cmds.connectAttr(curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray", stack.node+".inputs[1].inputWeights", f=True)

    for idx, attr in enumerate(addWeightStack):
        weightAttr = geoToWeightShape + ".reverseWeights"
        if not handPaint:
            weightAttr = curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray"
        cmds.connectAttr(weightAttr, attr + ".inputs[{0}].inputWeights".format(addAtIndex))
        cmds.setAttr(attr + ".inputs[{0}].factor".format(addAtIndex), 1)
        cmds.setAttr(attr + ".inputs[{0}].operation".format(addAtIndex), 2)
    # Create curve deformer (TEMP)
    if curveDeformerAlgorithm == 0:
        wire = cmds.wire(blendshapeGeo, wire=curve, dds=[(0),(100000)] , name=name + "WireDeformer")[0]
        if curve_base:
            curve_base = misc.getShape(curve_base)
            cmds.connectAttr(curve_base + ".worldSpace[0]", wire + ".baseWire[0]", f=True)
    if curveDeformerAlgorithm == 1:
        wire = LHCurveDeformerCmds.curveDeformerCmd( driverCurve = curve,
                                            aimCurve = curveAim,
                                            geom = [blendshapeGeo],
                                            ihi = 1,
                                            lockAttrs = 0,
                                            side='C',
                                            name=name + "CurveDeformer").returnDeformer
        
    if removePointIndicies:
        # first make sure to set the weights on the wire
        iterGeo = misc.getOMItergeo(blendshapeGeo)
        polyCount = iterGeo.count()
        defaultVals = [1.0 for x in range(polyCount)]
        #cmds.setAttr(wire + ".", defaultVals, type=dataType)
        for idx in range(polyCount):
            cmds.setAttr('{0}.weightList[0].weights[{1}]'.format(wire, polyCount), 1.0)
        for idx in removePointIndicies:
            cmds.setAttr('{0}.weightList[0].weights[{1}]'.format(wire, idx), 0.0)


    if reorderInFrontOfDeformer:
        cmds.reorderDeformers(reorderInFrontOfDeformer, blendshape, misc.getShape(deformedGeometry))

    return blendshape

