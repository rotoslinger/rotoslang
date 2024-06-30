import inspect
from collections import OrderedDict


from maya import cmds

from rig_2.name import utils as name_utils
import importlib
importlib.reload(name_utils)

from rig_2.weights import utils as weights_utils
importlib.reload(weights_utils)

from rig_2.animcurve import utils as animcurve_utils
importlib.reload(animcurve_utils)

from rig_2.node import utils as node_utils
importlib.reload(node_utils)

from rig.utils import misc
importlib.reload(misc)

from rig.deformers import utils as deformerUtils
importlib.reload(deformerUtils)

from rig.rigComponents import meshRivetCtrl
importlib.reload(meshRivetCtrl)

from rig_2.message import utils as message_utils
importlib.reload(message_utils)

from rig_2.manipulator import elements as manipulator_elements
importlib.reload(manipulator_elements)

from rig_2.attr import utils as attr_utils
importlib.reload(attr_utils)

from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)

from rig_2.component import base as component_base
importlib.reload(component_base)



class Weight_Node(component_base.Component):
    def __init__(self,
                 name,
                 side=None,
                 suffix=None,
                 nodeType = None,
                 parent = None,
                 outputAttrs=[],
                 startAtElemIdx=-1,
                 addNewElem=False,
                 component_name="",
                 ):
        super(Weight_Node, self).__init__(component_name=component_name)
        # weight node is a subcomponent so it will not have any exposed args...
        self.ordered_args = OrderedDict()
        self.component_name = component_name
        self.name = name
        self.side = side # WIP
        self.suffix = suffix # WIP
        self.nodeType = nodeType
        self.parent = parent
        self.startAtElemIdx = startAtElemIdx
        self.addNewElem = addNewElem
        self.startElem = 0
        self.outputAttrs = outputAttrs

    def elemCheck(self):
        return

    def check(self):
        return

    def elemCheck(self, multiAttrToCheck):
        if self.startAtElemIdx == -1 and self.addNewElem:
            self.startElem = deformerUtils.availableElemCheck(multiAttrToCheck)
        elif self.startAtElemIdx == -1 and not self.addNewElem:
            self.startElem = 0
        elif self.startAtElemIdx > -1:
            self.startElem = self.startAtElemIdx

    def getNode(self):
        if cmds.objExists(self.name):
            self.node = self.name
            return
        self.node = node_utils.get_node_agnostic(self.nodeType, name=self.name, parent=self.parent, component_name=self.component_name)
        # Node has cycle issues, will be deleted before giving to animators, so ignore cycles during setup...
        if self.nodeType == "LHCurveWeightNode_2":
            cmds.cycleCheck( self.node, e=False)

            
    def getDriverNodes(self):
        return


    def getAttrs(self):
        return

    def inputConnections(self):
        return

    def outputConnections(self):
        return
    
    def createControls(self):
        return

    def positionControls(self):
        return
    
    def getRotationOrientation(self, position, controlAutoOrientMesh):
            tempLocation = position
            temp = cmds.createNode("transform")
            cmds.xform(temp, ws=True, t=tempLocation)
            normalCons = cmds.normalConstraint(controlAutoOrientMesh, temp, aimVector=[0, 0, 1])
            rotate = cmds.xform(temp, q=True, ws=True, ro=True)
            cmds.delete(temp)
            return rotate

    def create(self):
        self.check()
        self.getNode()
        self.getDriverNodes()
        self.getAttrs()
        self.inputConnections()
        self.outputConnections()
        self.createControls()
        self.positionControls()

class AnimCurveWeight(Weight_Node):
    def __init__(self,
                 # Inherited args
                 # outputAttrs=[],
                 # name,
                 # nodeType = None,
                 # parent = None,
                 # startAtElemIdx=-1,
                 # addNewElem=False,
                 baseGeo = "",
                 ctrlNode="",
                 projectionGeo = "",
                 weightCurveNames = [],
                 animCurveSuffix = "ACV",
                 autoCreateAnimCurves = False,
                 autoCreateName = "lip",
                 auto_create_reverse=False,
                 # name side is when you want to have the ctrls mirrored
                 # for example you have a left eye and a right eye
                 # controls will not be able to be named "L_eye", "C_eye", "R_eye" because you have to make them twice once for each eye
                 # instead they will be named L_leftEye, L_centerEye, L_rightEye and the right controls will be named R_leftEye, R_centerEye, R_rightEye
                 auto_create_name_side=False,
                 autoCreateNum = 11,
                 autoCreateTimeRange = 20.0,
                 createSingleFalloff = True,
                 auto_create_single_falloff_handweights = False,
                 falloff_weight_mesh = "",
                 uKeyframesAllOnes = False,
                 falloffCurveDict = None,
                 curveOverrideDict = None,
                 falloffDefaults=(-10, -9, 9, 10),
                 falloffItts=["linear","linear","linear","linear"],
                 falloffOtts=["linear","linear","linear","linear"],
                 singleFalloffName = "",  # if you are not auto creating you need to give the single falloff name
                 addFalloff = True,
                 startElem = 0,
                 offset=0,
                 centerWeight = .6,
                 outerWeight = 0,
                 angle = 50,
                 nudge = 0,
                 intermediateVal = 0,
                 lastAngle=50,
                 lastIntermediateVal=.8,
                 intermediateAngle=0,
                 lastIntermediateAngle=30,
                 inputWeightCurvesDict=[],
                 inputWeightCurvesFalloffDict=[],
                 autoPositionThreshhold = .9,
                 controlAutoOrientMesh = "",
                 **kw):

        super(AnimCurveWeight, self).__init__(**kw)
        
        # args
        self.baseGeo=baseGeo
        self.ctrlNode=ctrlNode
        self.projectionGeo = projectionGeo
        self.weightCurveNames =weightCurveNames
        self.animCurveSuffix = animCurveSuffix
        self.autoCreateAnimCurves = autoCreateAnimCurves
        self.autoCreateName = autoCreateName
        self.auto_create_name_side=auto_create_name_side
        self.autoCreateNum = autoCreateNum
        self.autoCreateTimeRange =autoCreateTimeRange
        self.auto_create_reverse=auto_create_reverse
        self.createSingleFalloff =createSingleFalloff
        self.auto_create_single_falloff_handweights =auto_create_single_falloff_handweights
        self.falloff_weight_mesh = falloff_weight_mesh
        
        
        
        
        self.uKeyframesAllOnes =uKeyframesAllOnes
        self.falloffCurveDict =falloffCurveDict
        self.curveOverrideDict = curveOverrideDict
        self.falloffDefaults=falloffDefaults
        self.falloffItts=falloffItts
        self.falloffOtts=falloffOtts
        self.singleFalloffName = singleFalloffName
        self.addFalloff = addFalloff
        self.startElem = startElem
        self.offset=offset
        self.centerWeight = centerWeight
        self.outerWeight =outerWeight
        self.angle =angle
        self.nudge = nudge
        self.intermediateVal =intermediateVal
        self.lastAngle=lastAngle
        self.lastIntermediateVal=lastIntermediateVal
        self.intermediateAngle=intermediateAngle
        self.lastIntermediateAngle=lastIntermediateAngle
        self.inputWeightCurvesDict=inputWeightCurvesDict
        self.inputWeightCurvesFalloffDict=inputWeightCurvesFalloffDict
        self.autoPositionThreshhold = autoPositionThreshhold
        self.controlAutoOrientMesh =controlAutoOrientMesh 
        
        # attrs
        self.membershipWeights = ""
        self.projectionMesh = ""
        self.baseMesh = ""
        self.kDoubleArrayOutputPlugs = []
        self.kFloatArrayOutputPlugs = []
        # These attributes will be filled with the latest created plugs, if you want a list of all the plugs check the kDoubleArrayOutputPlugs
        self.newKDoubleArrayOutputPlugs = []
        self.newKFloatArrayOutputPlugs = []
        self.nodeType = "LHCurveWeightNode_2"

        # only support single base mesh for now
        if type(self.baseGeo) == list:
            self.baseGeo = self.baseGeo[0]
            
        self.weightNames = ["{0}_{1}".format(x, self.animCurveSuffix) for x in self.weightCurveNames]
        self.weightNamesFalloff = ["{0}Falloff_{1}".format(x, self.animCurveSuffix) for x in self.weightCurveNames]

        if not self.falloff_weight_mesh or not cmds.objExists(self.falloff_weight_mesh):
            self.auto_create_single_falloff_handweights = False


    def check(self):
        if not self.outputAttrs:
            return

        if len(self.outputAttrs) != len(self.weightCurveNames):
            raise Exception('Make sure the length of the outputAttrs arg matches the number of input arg elements')
            quit()


    def getDriverNodes(self):
        self.projectionMesh = misc.getShape(self.projectionGeo)
        self.baseMesh = misc.getShape(self.baseGeo)

        if self.inputWeightCurvesDict and self.inputWeightCurvesFalloffDict:
            self.weightCurves = animcurve_utils.create_set_anim_curves(self.inputWeightCurvesDict,
                                                                       component_name=self.component_name)
            self.weightCurvesFalloff = animcurve_utils.create_set_anim_curves(self.inputWeightCurvesFalloffDict,
                                                                              falloff=True,
                                                                              component_name=self.component_name)
            return

        if self.autoCreateAnimCurves:
            self.weightCurves, self.weightCurvesFalloff = weights_utils.createNormalizedAnimWeights(name=self.autoCreateName, num=self.autoCreateNum,
                                                                                                    timeRange=self.autoCreateTimeRange, suffix=self.animCurveSuffix,
                                                                                                    offset=self.offset, centerWeight =self.centerWeight, outerWeight = self.outerWeight,
                                                                                                    angle = self.angle, nudge=self.nudge, intermediateVal=self.intermediateVal,
                                                                                                    lastAngle=self.lastAngle,
                                                                                                    lastIntermediateVal=self.lastIntermediateVal,
                                                                                                    intermediateAngle=self.intermediateAngle,
                                                                                                    lastIntermediateAngle=self.lastIntermediateAngle,
                                                                                                    createSingleFalloff=self.createSingleFalloff,
                                                                                                    singleFalloffName = self.singleFalloffName,
                                                                                                    falloffStart=self.falloffDefaults[0],
                                                                                                    falloffStartInner=self.falloffDefaults[1],
                                                                                                    falloffEndInner=self.falloffDefaults[2],
                                                                                                    falloffEnd=self.falloffDefaults[3],
                                                                                                    itts=self.falloffItts,
                                                                                                    otts=self.falloffOtts,
                                                                                                    falloffCurveDict=self.falloffCurveDict,
                                                                                                    component_name=self.component_name,
                                                                                                    auto_create_reverse = self.auto_create_reverse,
                                                                                                    )
            self.overrideWeightCurves()
            return

        self.weightCurves = node_utils.get_node_agnostic_multiple(nodeType="animCurveTU", names=self.weightNames, parent=None, tag_name="WEIGHT_CURVE", component_name=self.component_name)

        if self.createSingleFalloff and self.singleFalloffName:
            self.weightNamesFalloff = [self.singleFalloffName + "_ACV" for x in range(self.weightNamesFalloff)]

        self.weightCurvesFalloff = node_utils.get_node_agnostic_multiple(nodeType="animCurveTU", names=self.weightNamesFalloff, parent=None, tag_name="FALLOFF_WEIGHT_CURVE", component_name=self.component_name)
        # Make sure there is at least 1 key on the curves.  Will do nothing if keyframes already exist.
        if self.uKeyframesAllOnes:
            animcurve_utils.initUKeyframeAllOnes(self.weightCurves)
        else:
            animcurve_utils.initUKeyframes(self.weightCurves)
        animcurve_utils.initVFalloff(self.weightCurvesFalloff,
                                     falloffCurveDict=self.falloffCurveDict,
                                     falloffStart=self.falloffDefaults[0],
                                     falloffStartInner=self.falloffDefaults[1],
                                     falloffEndInner=self.falloffDefaults[2],
                                     falloffEnd=self.falloffDefaults[3],
                                     itts=self.falloffItts,
                                     otts=self.falloffOtts
                                     )
        self.overrideWeightCurves()
        
    def getAttrs(self):
        self.membershipWeights = deformerUtils.attrCheck(node=self.baseGeo,
                                           attrs=["membershipWeights"],
                                           attrType=None,
                                           weightmap=True)[0]
        if self.autoCreateAnimCurves:
            self.factorAttrNames = name_utils.name_based_on_range(count=self.autoCreateNum,
                                                                  name="falloff",
                                                                  suffixSeperator="",
                                                                  side_name=self.auto_create_name_side,
                                                                  reverse_side=self.auto_create_reverse,
                                                                  )

            defaultVals = [0.0 for x in range(self.autoCreateNum)]

            self.floatAttrs = deformerUtils.attrCheck(node=self.ctrlNode,
                                        attrs=self.factorAttrNames,
                                        attrType="float",
                                        defaultVals = defaultVals,
                                        k=True)
            if self.auto_create_single_falloff_handweights:
                self.singleFalloffOverrideHandWeights = attr_utils.get_attr(node=self.falloff_weight_mesh,
                                                                            attr = self.singleFalloffName + "OverrideWeights",
                                                                            weightmap=True)
        

    def overrideWeightCurves(self):
        if not self.curveOverrideDict:
            return
        for curve in self.weightCurves:
            animcurve_utils.setAnimCurveShape(curve, self.curveOverrideDict)



    def inputConnections(self):
        cmds.connectAttr(self.membershipWeights, "{0}.membershipWeights".format(self.node), f=True)
        cmds.connectAttr("{0}.worldMesh".format(self.projectionMesh), "{0}.projectionMesh".format(self.node), f=True)
        geoAttrType = ".worldMesh"
        objectType = cmds.objectType(self.baseMesh)
        if objectType == "nurbsCurve" or objectType == "nurbsSurface":
            geoAttrType = ".worldSpace"
        if objectType == "lattice":
            geoAttrType = ".worldLattice"
        cmds.connectAttr("{0}{1}".format(self.baseMesh, geoAttrType), "{0}.inputGeo".format(self.node), f=True)

        # format the output attribute for the anim curves so you don't have to do it in the loop
        self.uCurveOutAttrs = ["{0}.output".format(x) for x in self.weightCurves]
        self.vCurveOutAttrs = ["{0}.output".format(x) for x in self.weightCurvesFalloff]

        self.elemCheck("{0}.inputs".format(self.node))

        self.newKDoubleArrayOutputPlugs = []
        self.newKFloatArrayOutputPlugs = []

        for idx in range(len(self.weightCurves)):
            elemIdx = idx + self.startElem
            cmds.connectAttr(self.uCurveOutAttrs[idx], "{0}.inputs[{1}].AnimCurveU".format(self.node, elemIdx),f=True)
            cmds.connectAttr(self.vCurveOutAttrs[idx], "{0}.inputs[{1}].AnimCurveV".format(self.node, elemIdx),f=True)
            if self.autoCreateAnimCurves and self.auto_create_single_falloff_handweights:
                cmds.connectAttr(self.singleFalloffOverrideHandWeights, "{0}.inputs[{1}].overrideWeights".format(self.node, elemIdx),f=True)

            kDoubleOut = "{0}.outDoubleWeights[{1}].outWeightsDoubleArray".format(self.node, elemIdx)
            kFloatOut = "{0}.outDoubleWeights[{1}].outWeightsFloatArray[{1}]".format(self.node, elemIdx)

            self.newKDoubleArrayOutputPlugs.append(kDoubleOut)
            self.newKFloatArrayOutputPlugs.append(kFloatOut)

            if kDoubleOut not in self.kDoubleArrayOutputPlugs:
                self.kDoubleArrayOutputPlugs.append(kDoubleOut)
            if kFloatOut not in self.kFloatArrayOutputPlugs:
                self.kFloatArrayOutputPlugs.append(kFloatOut)

    def outputConnections(self):
        if not self.outputAttrs:
            return
        self.elemCheck("{0}.inputs".format(self.node))
        for idx, attr in enumerate(self.outputAttrs):
            elemIdx = idx + self.startElem
            attrType = weights_utils.checkOutputWeightType(attr)
            weightAttr = ""
            if attrType:
                # If True, then this output attribute will get the kDoubleArray Output
                weightAttr = "{0}.outDoubleWeights[{1}].outWeightsDoubleArray".format(self.node, elemIdx)
            else:
                # If False, then this output attribute will get the outWeightsFloatArray
                weightAttr = "{0}.outFloatWeights[{1}].outWeightsFloatArray[{1}]".format(self.node, elemIdx)
            # Call getAttr to create an elem if it doesn't already exist
            cmds.getAttr(weightAttr)
            cmds.connectAttr(weightAttr, attr, f=True)

    def getPositionsAndRotationsFromWeights(self):
        self.positionsFromWeights = []
        self.rotationsFromWeights = []
        for idx, attr in enumerate(self.weightCurves):
            weightAttr = "{0}.outDoubleWeights[{1}].outWeightsDoubleArray".format(self.node, idx)
            weightlist = cmds.getAttr(weightAttr)
            # self.positionsFromWeights.append(deformerUtils.getPointPositionByWeights(weightlist, self.baseGeo, self.autoPositionThreshhold))
            height, width, depth, center = deformerUtils.getPointPositionByWeights(weightlist, self.baseGeo, self.autoPositionThreshhold)
            self.positionsFromWeights.append([center.x, center.y, center.z])

            
            if self.controlAutoOrientMesh:
                self.rotationsFromWeights.append(self.getRotationOrientation(self.positionsFromWeights[idx], self.controlAutoOrientMesh))

    # def getRotationOrientation(self, position, controlAutoOrientMesh):
    #         tempLocation = position
    #         temp = cmds.createNode("transform")
    #         cmds.xform(temp, ws=True, t=tempLocation)
    #         normalCons = cmds.normalConstraint(controlAutoOrientMesh, temp, aimVector=[0, 0, 1])
    #         rotate = cmds.xform(temp, q=True, ws=True, ro=True)
    #         cmds.delete(temp)
    #         return rotate

    def setFalloffDefaults(self):
        self.getWorldLocationBasedOnWeights()
        for idx in range(len(self.weightCurves)):
            cmds.setAttr("{0}.inputs[{1}].falloffUPivot".format(self.node, idx), self.closestU[idx])

    def getBaseMeshFromConnection(self):
        self.baseMesh = cmds.listConnections(self.node + ".inMesh", source=True, sh=True)[0]

    def getProjectionMeshFromConnection(self):
        self.projectionMesh = cmds.listConnections(self.node + ".projectionMesh", source=True, sh=True)[0]


    def getWorldLocationBasedOnWeights(self):
        self.getNode()
        numElements = cmds.getAttr("{0}.outDoubleWeights".format(self.node), mi=True)
        if not numElements:
            return 0
        numElements = len(numElements)
        # weightVals = []
        self.getBaseMeshFromConnection()
        self.getProjectionMeshFromConnection()
        self.closestU = []
        self.closestV = []
        for idx in range(numElements):
            weightList = cmds.getAttr("{0}.outDoubleWeights[{1}].outWeightsDoubleArray".format(self.node, idx))
            height, width, depth, center = deformerUtils.getPointPositionByWeights(weightList, self.baseMesh)
            u, v = misc.getClosestUVOnMesh(pointX=center.x, pointY=center.y, pointZ=center.z,  mesh=self.projectionMesh)
            self.closestU.append(u)
            self.closestV.append(v)





"""
# Test the module with a cluster deformer
cmds.file(new=True, f=True)
deformMesh = cmds.polySphere(n="deformMesh")[0]
cmds.cluster(deformMesh)
base = cmds.polySphere(n="BASE")[0]
cmds.setAttr(base + ".v",0)
projectionMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2)[0]
cmds.move(2, projectionMesh, z=True)
stack = weightStack.AnimCurveWeight(name="TestCurveWeights", baseGeo=base, projectionGeo=projectionMesh, weightCurveNames=["test001"], addNewElem=False, outputAttrs = ["cluster1.weightList[0]"])
stack.create()
"""

class WeightStack(Weight_Node):
    def __init__(self,
                 ctrlNode="",
                 inputWeightAttrs = [],
                 factorAttrNames = [],
                 geoToWeight = "",
                 operationVals=[],
                 autoCreate = False,
                 autoCreateName = "lip",
                 # name side is when you want to have the ctrls mirrored
                 # for example you have a left eye and a right eye
                 # controls will not be able to be named "L_eye", "C_eye", "R_eye" because you have to make them twice once for each eye
                 # instead they will be named L_leftEye, L_centerEye, L_rightEye and the right controls will be named R_leftEye, R_centerEye, R_rightEye
                 auto_create_name_side=False,
                 auto_create_reverse=False,
                 autoCreateOperationVal = 0,
                 createControl = True,
                 controlSize = 1,
                 controlTxConnectionAttrs=[],
                 controlTyConnectionAttrs=[],
                 controlTzConnectionAttrs=[],
                 controlRxConnectionAttrs=[],
                 controlRyConnectionAttrs=[],
                 controlRzConnectionAttrs=[],
                 controlSxConnectionAttrs=[],
                 controlSyConnectionAttrs=[],
                 controlSzConnectionAttrs=[],
                 controlShape = manipulator_elements.slide,
                 controlShapeOffset = [0,0,.1],
                 controlShapeOrient = [90, 0, 0],
                 controlShapeScale = [1, 1, 1],
                 controlLockAttrs = [],
                 controlPositionWeightsThreshold=.9,
                 controlPositionOffset=[0,0,0],
                 controlAutoOrientMesh="",
                 controlRivetMesh = "",
                 controlRivetAimMesh="",
                 controlParent="",
                 UDLR = True,
                 isOutputKDoubleArray=False,
                 outputAttrs_LR = [],
                 connectFalloff = True,
                 falloffCurveWeightNode = "",
                 falloffElemStart = 0,
                 controlSpeedDefaults = [.1,.1,.1],
                 repositionRivetCtrls=False,
                 inputWeightAttrs_UD=[],
                 inputWeightAttrs_LR=[],
                #  outputToBlendshape=False,
                 # Inherited args
                 # outputAttrs=[],
                 # name,
                 # nodeType = None,
                 # parent = None,
                 # startAtElemIdx=-1,
                 # addNewElem=False,
                 **kw):

        super(WeightStack, self).__init__(**kw)

        # args
        self.ctrlNode=ctrlNode
        self.inputWeightAttrs =inputWeightAttrs
        self.factorAttrNames =factorAttrNames
        self.geoToWeight = geoToWeight
        self.operationVals=operationVals
        self.autoCreate = autoCreate
        self.autoCreateName =autoCreateName
        self.auto_create_name_side=auto_create_name_side
        self.autoCreateOperationVal =autoCreateOperationVal
        self.createControl = createControl
        self.controlSize = controlSize
        self.controlTxConnectionAttrs=controlTxConnectionAttrs
        self.controlTyConnectionAttrs=controlTyConnectionAttrs
        self.controlTzConnectionAttrs=controlTzConnectionAttrs
        self.controlRxConnectionAttrs=controlRxConnectionAttrs
        self.controlRyConnectionAttrs=controlRyConnectionAttrs
        self.controlRzConnectionAttrs=controlRzConnectionAttrs
        self.controlSxConnectionAttrs=controlSxConnectionAttrs
        self.controlSyConnectionAttrs=controlSyConnectionAttrs
        self.controlSzConnectionAttrs=controlSzConnectionAttrs
        self.controlShape =controlShape
        self.controlShapeOffset = controlShapeOffset
        self.controlShapeOrient = controlShapeOrient
        self.controlShapeScale = controlShapeScale
        self.controlLockAttrs = controlLockAttrs
        self.controlPositionWeightsThreshold=controlPositionWeightsThreshold
        self.controlPositionOffset=controlPositionOffset
        self.controlAutoOrientMesh=controlAutoOrientMesh
        self.controlRivetMesh =controlRivetMesh
        self.controlRivetAimMesh=controlRivetAimMesh
        self.controlParent=controlParent
        self.UDLR =UDLR
        self.isOutputKDoubleArray=isOutputKDoubleArray
        self.outputAttrs_LR = outputAttrs_LR
        self.connectFalloff = connectFalloff
        self.falloffCurveWeightNode =falloffCurveWeightNode
        self.falloffElemStart =falloffElemStart
        self.controlSpeedDefaults = controlSpeedDefaults
        self.repositionRivetCtrls=repositionRivetCtrls
        self.inputWeightAttrs_UD=inputWeightAttrs_UD
        self.inputWeightAttrs_LR=inputWeightAttrs_LR
        self.auto_create_reverse=auto_create_reverse

        # instance attrs
        self.factorAttrNamesLR = []
        self.floatAttrs_LR = []
        self.name_LR = ""
        if self.UDLR:
            self.name_LR = "{0}_LR".format(self.name)
            self.name = "{0}_UD".format(self.name)
        self.node_LR = ""
        self.isKDoubleArrayOutputWeights = True
        self.nodeType = "LHWeightNode"
        self.controls = []
        self.positionsFromWeights = []
        self.rotationsFromWeights = []
        self.startElem = 0
        self.controls_weight_ordered = []
        # self.outputToBlendshape = outputToBlendshape
        # Don't support multiple geos right now
        if type(self.geoToWeight) == list:
            self.geoToWeight = self.geoToWeight[0]

    def check(self):
        if self.autoCreate:
            return

        # If specifying different UD and LR weights
        if self.inputWeightAttrs_UD and self.inputWeightAttrs_LR and not self.operationVals:
            for idx in range(len(self.inputWeightAttrs_UD)):
                self.operationVals.append(0)
            listsToCheck = [self.inputWeightAttrs_UD, self.inputWeightAttrs_LR, self.factorAttrNames, self.operationVals]
            if any(len(listArray) != len(self.inputWeightAttrs_UD) for listArray in listsToCheck):
                raise Exception("inputWeightAttrs_UD, inputWeightAttrs_LR, factorAttrs, and operationVals all need to be the same length, " +
                                "if you want multiple maps to be connected to multiple factor attrs, use the same " + 
                                "weightMapAttrs multiple times")
                quit()
            return

        # using only 1 set of weights for both UD and LR
        if not self.operationVals:
            for idx in range(len(self.inputWeightAttrs)):
                self.operationVals.append(0)
        listsToCheck = [self.inputWeightAttrs, self.factorAttrNames, self.operationVals]
        if any(len(listArray) != len(self.inputWeightAttrs) for listArray in listsToCheck):
            raise Exception("inputWeightAttrs, factorAttrs, and operationVals all need to be the same length, " +
                            "if you want multiple maps to be connected to multiple factor attrs, use the same " + 
                            "inputWeightAttrs multiple times")
            quit()

    def getNode(self):
        super(WeightStack, self).getNode()
        if not self.UDLR:
            return
        if cmds.objExists(self.name_LR):
            self.node_LR = self.name_LR
            return
        self.node_LR = node_utils.get_node_agnostic(self.nodeType, name=self.name_LR, parent=self.parent, component_name=self.component_name)

    def getAttrs(self):
        # We will always need to know what mesh the weight stack is weighting, this message attr does that
        if self.geoToWeight:
            for node in [self.node, self.node_LR]:
                if not node:
                    continue
                if not cmds.objExists(node + ".weightedMesh"):
                    cmds.addAttr(node, ln = "weightedMesh", at = "message")
                geo = self.geoToWeight
                if type(self.geoToWeight) == list:
                    geo = geo[0]
                shape = misc.getShape(geo)
                cmds.connectAttr(shape + ".message", node + ".weightedMesh", f=True)
                tag_utils.tag_weighted_mesh(geo)
                tag_utils.create_component_tag(geo, component_name=self.component_name)


        self.weightMapAttrs = []
        self.weightMapAttrs_LR = []

        if self.autoCreate:
            self.weightMapAttrs = self.inputWeightAttrs
            self.factorAttrNames = name_utils.name_based_on_range(count=len(self.inputWeightAttrs),
                                                                  name=self.autoCreateName,
                                                                  suffixSeperator="",
                                                                  side_name=self.auto_create_name_side,
                                                                  reverse_side=self.auto_create_reverse,
                                                                  
                                                                  )
            self.operationVals = [self.autoCreateOperationVal for x in range(len(self.inputWeightAttrs))]

        # If the given weight map already exists in maya
        if self.inputWeightAttrs and cmds.objExists(self.inputWeightAttrs[0]):
            self.weightMapAttrs = self.inputWeightAttrs
        
        
        # Create the weight map if it doesn't already exist
        if not self.weightMapAttrs:
            self.weightMapAttrs = deformerUtils.attrCheck(node=self.geoToWeight,
                                            attrs=self.inputWeightAttrs,
                                            attrType=None,
                                            weightmap=True)

        # Add UD LR functionality
        if self.UDLR:
            UDNames = ["{0}_UD".format(x) for x in self.factorAttrNames]
            self.factorAttrNamesLR = ["{0}_LR".format(x) for x in self.factorAttrNames]
            self.factorAttrNames = UDNames
            # Create the extra LR attrs here
            self.floatAttrs_LR = deformerUtils.attrCheck(node=self.ctrlNode,
                                           attrs=self.factorAttrNamesLR,
                                           attrType="float",
                                           k=True)

        # These are the primary attributes created by the user specified names
        self.floatAttrs = deformerUtils.attrCheck(node=self.ctrlNode,
                                    attrs=self.factorAttrNames,
                                    attrType="float",
                                    k=True)
        
        # 
        if not self.weightMapAttrs and self.inputWeightAttrs_UD and self.inputWeightAttrs_LR:
            self.weightMapAttrs = self.inputWeightAttrs_UD
            self.weightMapAttrs_LR = self.inputWeightAttrs_LR


    def inputConnections(self):
        self.elemCheck("{0}.inputs".format(self.node))
        self.positionsFromWeights = []
        
        for idx in range(len(self.weightMapAttrs)):
            elemIdx = idx + self.startElem
            cmds.connectAttr(self.weightMapAttrs[idx], "{0}.inputs[{1}].inputWeights".format(self.node, elemIdx), f=True)
            # if self.inputWeightAttrs_UD:
            #     cmds.connectAttr(self.inputWeightAttrs_UD[idx], "{0}.inputs[{1}].inputWeights".format(self.node, elemIdx), f=True)

            cmds.connectAttr(self.floatAttrs[idx], "{0}.inputs[{1}].factor".format(self.node, elemIdx), f=True)
            cmds.setAttr("{0}.inputs[{1}].operation".format(self.node, elemIdx), self.operationVals[idx])
            if self.UDLR:
                # elemIdx = elemIdx + len(self.weightMapAttrs)
                cmds.connectAttr(self.weightMapAttrs[idx], "{0}.inputs[{1}].inputWeights".format(self.node_LR, elemIdx), f=True)
                if self.weightMapAttrs_LR:
                    cmds.connectAttr(self.weightMapAttrs_LR[idx], "{0}.inputs[{1}].inputWeights".format(self.node_LR, elemIdx), f=True)
                cmds.connectAttr(self.floatAttrs_LR[idx], "{0}.inputs[{1}].factor".format(self.node_LR, elemIdx), f=True)
                cmds.setAttr("{0}.inputs[{1}].operation".format(self.node_LR, elemIdx), self.operationVals[idx])

    def getPositionsFromWeights(self):
        self.elemCheck("{0}.inputs".format(self.node))
        positionsFromWeights = []
        for idx in range(len(self.weightMapAttrs)):
            elemIdx = idx + self.startElem
            weightList =  "{0}.inputs[{1}].inputWeights".format(self.node, elemIdx)
            height, width, depth, center = deformerUtils.getPointPositionByWeights(weightList, self.geoToWeight, self.controlPositionWeightsThreshold)
            positionsFromWeights.append([center.x, center.y, center.z])
        return positionsFromWeights

    def getPositionsAndRotationsFromWeights(self):
        self.elemCheck("{0}.inputs".format(self.node))
        self.positionsFromWeights = []
        self.rotationsFromWeights = []
        numElements = cmds.getAttr("{0}.inputs".format(self.node), mi=True)
        for idx in range(len(numElements)):
            self.positionsFromWeights.append(self.getPositionsFromWeightsByIndex(idx))
            self.rotationsFromWeights.append(self.getRotationOrientation(self.positionsFromWeights[idx], self.controlAutoOrientMesh))
        return self.positionsFromWeights, self.rotationsFromWeights

    def getPositionsFromWeightsByIndex(self, index=0):
        weightList =  "{0}.inputs[{1}].inputWeights".format(self.node, index)
        weightList = cmds.getAttr(weightList)
        height, width, depth, center = deformerUtils.getPointPositionByWeights(weightList, self.geoToWeight, threshold=self.controlPositionWeightsThreshold)
        return [center.x, center.y, center.z]

    def reposition_controls(self):
        for idx, ctrl in enumerate(self.controls):
            buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo = meshRivetCtrl.getRivetParts(ctrl)
            misc.move(buffer2, self.positionsFromWeights[idx], self.rotationsFromWeights[idx])
            misc.updateGeoConstraint(offsetBuffer = buffer2, geoConstraint=geoConstraint)
            
    def outputConnections(self):
        # Checks if the output type is kDoubleArray or a multiFloat (maya native deformer weights type)
        if not self.outputAttrs:
            return
        for idx, attr in enumerate(self.outputAttrs):
            if self.isOutputKDoubleArray:
                # If True, then this output attribute will get the kDoubleArray Output
                cmds.connectAttr("{0}.outWeightsDoubleArray".format(self.node), attr, f=True)
                if self.UDLR:
                    cmds.connectAttr("{0}.outWeightsDoubleArray".format(self.node_LR), self.outputAttrs_LR[idx], f=True)
            else:
                # If False, then this output attribute will get the outWeightsFloatArray
                cmds.connectAttr("{0}.outWeightsFloatArray[0]".format(self.node), attr, f=True)
                if self.UDLR:
                    cmds.connectAttr("{0}.outWeightsFloatArray[0]".format(self.node_LR), self.outputAttrs_LR[idx], f=True)

    def createControls(self):
        if not self.createControl:
            return
        self.rotationsFromWeights = []
        for idx in range(len(self.weightMapAttrs)):
            elemIdx = idx + self.startElem
            txConnect = None
            if self.UDLR:
                # txConnect = self.floatAttrs_LR[idx]
                txConnect = "{0}.inputs[{1}].factor".format(self.node_LR, elemIdx)
            weightList =  "{0}.inputs[{1}].inputWeights".format(self.node, elemIdx)
            weightList = cmds.getAttr(weightList)
            height, width, depth, center = deformerUtils.getPointPositionByWeights(weightList, self.geoToWeight, self.controlPositionWeightsThreshold)
            self.positionsFromWeights.append([center.x + self.controlPositionOffset[0], center.y + self.controlPositionOffset[1], center.z + self.controlPositionOffset[2]])
            rotate = [0,0,0]
            if self.controlAutoOrientMesh:
                tempLocation = self.positionsFromWeights[idx]
                temp = cmds.createNode("transform")
                cmds.xform(temp, ws=True, t=tempLocation)
                normalCons = cmds.normalConstraint(self.controlAutoOrientMesh, temp, aimVector=[0, 0, 1])
                rotate = cmds.xform(temp, q=True, ws=True, ro=True)
                cmds.delete(temp)
                self.rotationsFromWeights.append(rotate)
            
            side, name = misc.getNameSide(self.factorAttrNames[idx])

            tyConnect = None
            tzConnect = None
            rxConnect = None
            ryConnect = None
            rzConnect = None
            sxConnect = None
            syConnect = None
            szConnect = None

            if self.controlTxConnectionAttrs:
                txConnect = self.controlTxConnectionAttrs[idx]
            if self.controlTyConnectionAttrs:
                tyConnect = self.controlTyConnectionAttrs[idx]
            if self.controlTzConnectionAttrs:
                tzConnect = self.controlTzConnectionAttrs[idx]
            if self.controlRxConnectionAttrs:
                rxConnect = self.controlRxConnectionAttrs[idx]
            if self.controlRyConnectionAttrs:
                ryConnect = self.controlRyConnectionAttrs[idx]

            if self.controlRzConnectionAttrs:
                rzConnect = self.controlRzConnectionAttrs[idx]

            if self.controlSxConnectionAttrs:
                sxConnect = self.controlSxConnectionAttrs[idx]

            if self.controlSyConnectionAttrs:
                syConnect = self.controlSyConnectionAttrs[idx]

            if self.controlSxConnectionAttrs:
                szConnect = self.controlSzConnectionAttrs[idx]

            if cmds.objExists("{0}_{1}_CPT".format(side, name)):
                ctrlName = "{0}_{1}_CTL".format(side, name)
                if ctrlName not in self.controls:
                    self.controls.append(ctrlName)
                    connectionAttr = "{0}.inputs[{1}].factor".format(self.node, elemIdx)
                    # "txOut", "tyOut", "tzOut"
                    if self.UDLR:
                        txConnectionAttr=txConnect
                        cmds.connectAttr(ctrlName + ".txOut", txConnect, f=True)
                        tyConnectionAttr="{0}.inputs[{1}].factor".format(self.node, elemIdx)
                        cmds.connectAttr(ctrlName + ".tyOut", tyConnectionAttr, f=True)


                    if self.controlRxConnectionAttrs:
                        cmds.connectAttr(rxConnect, connectionAttr, f=True)
                    if self.controlRyConnectionAttrs:
                        cmds.connectAttr(ryConnect, connectionAttr, f=True)
                    if self.controlRzConnectionAttrs:
                        cmds.connectAttr(rzConnect, connectionAttr, f=True)

                        
                    if self.controlSxConnectionAttrs:
                        cmds.connectAttr(sxConnect, connectionAttr, f=True)
                    if self.controlSyConnectionAttrs:
                        cmds.connectAttr(syConnect, connectionAttr, f=True)
                    if self.controlSzConnectionAttrs:
                        cmds.connectAttr(szConnect, connectionAttr, f=True)
                continue

            tyConnect = "{0}.inputs[{1}].factor".format(self.node, elemIdx)
            tmpCtrl = meshRivetCtrl.Component(name = name,
                                                side=side,
                                                speedTxDefault=self.controlSpeedDefaults[0],
                                                speedTyDefault=self.controlSpeedDefaults[1],
                                                speedTzDefault=self.controlSpeedDefaults[2],
                                                parent=self.controlParent,
                                                curveData=self.controlShape,
                                                mesh = self.controlRivetMesh,
                                                translate = self.positionsFromWeights[idx],
                                                rotate = rotate,
                                                # scale = None,
                                                # guide = False,
                                                txConnectionAttr=txConnect,
                                                # tyConnectionAttr=self.floatAttrs[idx],
                                                tyConnectionAttr=tyConnect,
                                                tzConnectionAttr=tzConnect,

                                                rxConnectionAttr=rxConnect,
                                                ryConnectionAttr=ryConnect,
                                                rzConnectionAttr=rzConnect,

                                                sxConnectionAttr=sxConnect,
                                                syConnectionAttr=syConnect,
                                                szConnectionAttr=szConnect,

                                                normalConstraintPatch=self.controlRivetAimMesh,
                                                selection=False,
                                                mirror=False,
                                                size=self.controlSize,
                                                offset = self.controlShapeOffset,
                                                orient = self.controlShapeOrient,
                                                shapeScale = self.controlShapeScale,
                                                lockAttrs = self.controlLockAttrs,
                                                component_name=self.component_name
                                                                                                
                                                
                                                )
            tmpCtrl.create()

            if tmpCtrl.ctrl not in self.controls:
                self.controls.append(tmpCtrl.ctrl)

    def positionControls(self):
        if not self.repositionRivetCtrls:
            return
        
        for idx, ctrl in enumerate(self.controls):
            buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo = meshRivetCtrl.getRivetParts(ctrl)
            misc.move(buffer2, self.positionsFromWeights[idx], self.rotationsFromWeights[idx])
            misc.updateGeoConstraint(offsetBuffer = buffer2, geoConstraint=geoConstraint)

        

def connect_controls_curves_message(weight_stack_controls, weight_curves, falloff_weight_curves, stack_node, curve_weights_node):
    # Creates a message attr connection between controls and their cooresponding weight curves.
    for idx, control in enumerate(weight_stack_controls):
        message_utils.create_message_attr_setup(control, "weight_curve", weight_curves[idx], "control")
        message_utils.create_message_attr_setup(control, "falloff_weigth_curve", falloff_weight_curves[idx], "control")
        create_anim_curve_connection_attr(control, "weight_curve_connection_dicts", weight_curves[idx], idx, stack_node, curve_weights_node)
        create_anim_curve_connection_attr(control, "falloff_weight_curve_connection_dicts", falloff_weight_curves[idx], idx, stack_node, curve_weights_node)

def connect_weight_stack_anim_curve(weight_stack_class, anim_curve_weights_class, is_node_LR=False):
    # As long as the weight stack and anim curves have been created in the proper order this will work
    node=None
    if hasattr(weight_stack_class, "node") and not is_node_LR:
        node = weight_stack_class.node
    elif hasattr(weight_stack_class, "node") and is_node_LR:
        node = weight_stack_class.node_LR
    else: 
        node = weight_stack_class.deformer
    connect_controls_curves_message(weight_stack_class.controls,
                                    anim_curve_weights_class.weightCurves,
                                    anim_curve_weights_class.weightCurvesFalloff,
                                    node,
                                    anim_curve_weights_class.node,
                                    
                                    
                                    )

def create_anim_curve_connection_attr(control_node, attr_name, curve_name, output_idx, stack_node, curve_weights_node):
    connection_info_dict = {}
    connection_info_dict["curve_name"] = curve_name
    connection_info_dict["output_idx"] = output_idx
    connection_info_dict["control_parent"] = control_node
    connection_info_dict["node"] = stack_node
    connection_info_dict["curve_weights_node"] = curve_weights_node
    connection_info_dict["hand_weights"] = None
    connection_info_dict["geo_shape"] = None
    string_array_attr = attr_utils.create_string_array(control_node, attr_name)
    attr_utils.add_string_to_string_array(string_array_attr, str(connection_info_dict))
