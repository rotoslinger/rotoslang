from maya import cmds, OpenMaya
import maya.api.OpenMaya as OpenMaya2


from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
reload(misc)

from rig.rigComponents import meshRivetCtrl
reload(meshRivetCtrl)


import copy


class Node(object):
    def __init__(self,
                 name,
                 side=None,
                 suffix=None,
                 nodeType = None,
                 parent = None,
                 outputAttrs=[],
                 startAtElemIdx=-1,
                 addNewElem=False):
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
            self.startElem = availableElemCheck(multiAttrToCheck)
        elif self.startAtElemIdx == -1 and not self.addNewElem:
            self.startElem = 0
        elif self.startAtElemIdx > -1:
            self.startElem = self.startAtElemIdx

    def getNode(self):
        if cmds.objExists(self.name):
            self.node = self.name
            return
        self.node = cmds.createNode(self.nodeType, n=self.name, p=self.parent)

    def getDriverNodes(self):
        return


    def getAttrs(self):
        return

    def inputConnections(self):
        return

    def outputConnections(self):
        return

    def create(self):
        self.check()
        self.getNode()
        self.getDriverNodes()
        self.getAttrs()
        self.inputConnections()
        self.outputConnections()

class AnimCurveWeight(Node):
    def __init__(self,
                #  weightMapAttrNames = [],
                 baseGeo = "",
                 ctrlNode="",
                 projectionGeo = "",
                 weightAttrNames = [],
                 animCurveSuffix = "ACV",
                 autoCreateAnimCurves = False,
                 autoCreateName = "lip",
                 autoCreateNum = 11,
                 autoCreateTimeRange = 20.0,
                 createSingleFalloff = True,
                 singleFalloffName = "", # if you are not auto creating you need to give the single falloff name
                 addFalloff = True,
                 startElem = 0,
                 offset=.15, centerWeight = .35, outerWeight = .3, angle = 30, nudge = 1.0, intermediateVal = .2, lastAngle=0, lastIntermediateVal=.2, intermediateAngle=30, lastIntermediateAngle=0,
                 # Inherited args
                 # outputAttrs=[],
                 # name,
                 # nodeType = None,
                 # parent = None,
                 # startAtElemIdx=-1,
                 # addNewElem=False,
                 **kw):

        super(AnimCurveWeight, self).__init__(**kw)
        self.baseGeo = baseGeo
        self.ctrlNode = ctrlNode
        self.projectionGeo = projectionGeo
        self.weightAttrNames = weightAttrNames
        self.animCurveSuffix = animCurveSuffix
        self.startElem = startElem
        self.membershipWeights = ""
        self.projectionMesh = ""
        self.baseMesh = ""
        self.weightNames = ["{0}_{1}".format(x, self.animCurveSuffix) for x in self.weightAttrNames]
        self.weightNamesFalloff = ["{0}Falloff_{1}".format(x, self.animCurveSuffix) for x in self.weightAttrNames]
        self.autoCreateAnimCurves = autoCreateAnimCurves
        self.autoCreateNum = autoCreateNum
        self.autoCreateTimeRange = autoCreateTimeRange
        self.autoCreateName = autoCreateName
        self.kDoubleArrayOutputPlugs = []
        self.kFloatArrayOutputPlugs = []

        self.addFalloff=addFalloff
        self.offset=offset
        self.centerWeight =centerWeight
        self.outerWeight = outerWeight
        self.angle = angle
        self.nudge = nudge
        self.intermediateVal = intermediateVal
        self.lastAngle = lastAngle
        self.lastIntermediateVal = lastIntermediateVal
        self.intermediateAngle = intermediateAngle
        self.lastIntermediateAngle = lastIntermediateAngle
        self.createSingleFalloff = createSingleFalloff
        self.singleFalloffName = singleFalloffName


        # These attributes will be filled with the latest created plugs, if you want a list of all the plugs check the kDoubleArrayOutputPlugs
        self.newKDoubleArrayOutputPlugs = []
        self.newKFloatArrayOutputPlugs = []

        self.nodeType = "LHCurveWeightNode"


    def check(self):
        if not self.outputAttrs:
            return

        if len(self.outputAttrs) != len(self.weightAttrNames):
            raise Exception('Make sure the length of the outputAttrs arg matches the number of input arg elements')
            quit()

    def getAttrs(self):
        self.membershipWeights = attrCheck(node=self.baseGeo,
                                            attrs=["membershipWeights"],
                                            attrType=None,
                                            weightmap=True)[0]
        if self.autoCreateAnimCurves:
            self.factorAttrNames = nameBasedOnRange(count=self.autoCreateNum, name="falloff", suffixSeperator="")

            defaultVals = [0.0 for x in range(self.autoCreateNum)]

            self.floatAttrs = attrCheck(node=self.ctrlNode,
                                            attrs=self.factorAttrNames,
                                            attrType="float",
                                            defaultVals = defaultVals,
                                            k=True)

    def getDriverNodes(self):
        self.projectionMesh = misc.getShape(self.projectionGeo)
        self.baseMesh = misc.getShape(self.baseGeo)

        if self.autoCreateAnimCurves:
            self.weightCurves, self.weightCurvesFalloff = createNormalizedAnimWeights(name=self.autoCreateName, num=self.autoCreateNum,
                                                                                      timeRange=self.autoCreateTimeRange, suffix=self.animCurveSuffix,
                                                                                      offset=self.offset, centerWeight =self.centerWeight, outerWeight = self.outerWeight,
                                                                                      angle = self.angle, nudge=self.nudge, intermediateVal=self.intermediateVal,
                                                                                      lastAngle=self.lastAngle,
                                                                                      lastIntermediateVal=self.lastIntermediateVal,
                                                                                      intermediateAngle=self.intermediateAngle,
                                                                                      lastIntermediateAngle=self.lastIntermediateAngle,
                                                                                      createSingleFalloff=self.createSingleFalloff,
                                                                                      singleFalloffName = self.singleFalloffName)
            return
        
        self.weightCurves = getNodeAgnosticMultiple(nodeType="animCurveTU", names=self.weightNames, parent=None)

        if self.createSingleFalloff and self.singleFalloffName:
            self.weightNamesFalloff = [self.singleFalloffName + "_ACV" for x in range(self.weightNamesFalloff)]

        self.weightCurvesFalloff = getNodeAgnosticMultiple(nodeType="animCurveTU", names=self.weightNamesFalloff, parent=None)
        # Make sure there is at least 1 key on the curves.  Will do nothing if keyframes already exist.
        initUKeyframes(self.weightCurves)
        initVKeyframesLinear(self.weightCurvesFalloff)

    def inputConnections(self):
        cmds.connectAttr(self.membershipWeights, "{0}.membershipWeights".format(self.node), f=True)
        cmds.connectAttr("{0}.worldMesh".format(self.projectionMesh), "{0}.projectionMesh".format(self.node), f=True)
        cmds.connectAttr("{0}.worldMesh".format(self.baseMesh), "{0}.inMesh".format(self.node), f=True)

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
            cmds.connectAttr(self.floatAttrs[idx], "{0}.inputs[{1}].falloffU".format(self.node, elemIdx),f=True)

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
            attrType = checkOutputWeightType(attr)
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
            height, width, depth, center = getPointPositionByWeights(weightList, self.baseMesh)
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
stack = weightStack.AnimCurveWeight(name="TestCurveWeights", baseGeo=base, projectionGeo=projectionMesh, weightAttrNames=["test001"], addNewElem=False, outputAttrs = ["cluster1.weightList[0]"])
stack.create()
"""

class WeightStack(Node):
    def __init__(self,
                 ctrlNode="",
                 weightMapAttrNames = [],
                 factorAttrNames = [],
                 geoToWeight = "",
                 operationVals=[],
                 autoCreate = False,
                 autoCreateName = "lip",
                 autoCreateOperationVal = 0,
                 createControl = True,
                 controlSize = .05,
                 controlOffset = [0,0,.1],
                 controlRivetMesh = "",
                 UDLR = True,
                 outputAttrs_LR = [],
                 connectFalloff = True,
                 falloffCurveWeightNode = "",
                 falloffElemStart = 0,
                 # Inherited args
                 # outputAttrs=[],
                 # name,
                 # nodeType = None,
                 # parent = None,
                 # startAtElemIdx=-1,
                 # addNewElem=False,
                 **kw):

        super(WeightStack, self).__init__(**kw)
        self.ctrlNode = ctrlNode
        self.weightMapAttrNames = weightMapAttrNames
        self.factorAttrNames = factorAttrNames
        self.geoToWeight = geoToWeight
        self.operationVals = operationVals
        self.startElem = 0
        self.autoCreate = autoCreate
        self.autoCreateName = autoCreateName
        self.autoCreateOperationVal = autoCreateOperationVal
        self.createControl = createControl
        self.controlSize = controlSize
        self.controlOffset = controlOffset
        self.UDLR = UDLR
        self.factorAttrNamesLR = []
        self.floatAttrs_LR = []
        self.name_LR = ""
        if self.UDLR:
            self.name_LR = "{0}_LR".format(self.name)
            self.name = "{0}_UD".format(self.name)
        self.node_LR = ""
        self.isKDoubleArrayOutputWeights = True
        self.nodeType = "LHWeightNode"
        self.outputAttrs_LR = outputAttrs_LR
        self.controlRivetMesh = controlRivetMesh            
        self.connectFalloff = connectFalloff            
        self.falloffCurveWeightNode = falloffCurveWeightNode            
        self.falloffElemStart = falloffElemStart            
        self.controls = []
    def check(self):
        if self.autoCreate:
            return
        listsToCheck = [self.weightMapAttrNames, self.factorAttrNames, self.operationVals]
        if any(len(listArray) != len(self.weightMapAttrNames) for listArray in listsToCheck):
            raise Exception("weightMapAttrs, factorAttrs, and operationVals all need to be the same length, " +
                            "if you want multiple maps to be connected to multiple factor attrs, use the same " + 
                            "weightMapAttrs multiple times")
            quit()

    def getNode(self):
        super(WeightStack, self).getNode()
        if cmds.objExists(self.name_LR):
            self.node_LR = self.name_LR
            return
        self.node_LR = cmds.createNode(self.nodeType, n=self.name_LR, p=self.parent)

    def getAttrs(self):
        self.weightMapAttrs = []
        if self.autoCreate:
            self.weightMapAttrs = self.weightMapAttrNames
            self.factorAttrNames = nameBasedOnRange(count=len(self.weightMapAttrNames), name=self.autoCreateName, suffixSeperator="")
            self.operationVals = [self.autoCreateOperationVal for x in range(len(self.weightMapAttrNames))]
        if not self.weightMapAttrs:
            self.weightMapAttrs = attrCheck(node=self.geoToWeight,
                                                attrs=self.weightMapAttrNames,
                                                attrType=None,
                                                weightmap=True)

        # Add UD LR functionality
        if self.UDLR:
            UDNames = ["{0}_UD".format(x) for x in self.factorAttrNames]
            self.factorAttrNamesLR = ["{0}_LR".format(x) for x in self.factorAttrNames]
            self.factorAttrNames = UDNames
            # Create the extra LR attrs here
            self.floatAttrs_LR = attrCheck(node=self.ctrlNode,
                                            attrs=self.factorAttrNamesLR,
                                            attrType="float",
                                            k=True)

        # These are the primary attributes created by the user specified names
        self.floatAttrs = attrCheck(node=self.ctrlNode,
                                         attrs=self.factorAttrNames,
                                         attrType="float",
                                         k=True)
    
    def inputConnections(self):
        self.elemCheck("{0}.inputs".format(self.node))
        for idx in range(len(self.weightMapAttrs)):
            elemIdx = idx + self.startElem
            cmds.connectAttr(self.weightMapAttrs[idx], "{0}.inputs[{1}].inputWeights".format(self.node, elemIdx), f=True)
            cmds.connectAttr(self.floatAttrs[idx], "{0}.inputs[{1}].factor".format(self.node, elemIdx), f=True)
            cmds.setAttr("{0}.inputs[{1}].operation".format(self.node, elemIdx), self.operationVals[idx])
            if self.UDLR:
                # elemIdx = elemIdx + len(self.weightMapAttrs)
                cmds.connectAttr(self.weightMapAttrs[idx], "{0}.inputs[{1}].inputWeights".format(self.node_LR, elemIdx), f=True)
                cmds.connectAttr(self.floatAttrs_LR[idx], "{0}.inputs[{1}].factor".format(self.node_LR, elemIdx), f=True)
                cmds.setAttr("{0}.inputs[{1}].operation".format(self.node_LR, elemIdx), self.operationVals[idx])
            if self.createControl:
                txConnect = None
                if self.UDLR:
                    # txConnect = self.floatAttrs_LR[idx]
                    txConnect = "{0}.inputs[{1}].factor".format(self.node_LR, elemIdx)
                weightList =  "{0}.inputs[{1}].inputWeights".format(self.node, elemIdx)
                weightList = cmds.getAttr(weightList)
                height, width, depth, center = getPointPositionByWeights(weightList, "deformMesh")
                side, name = misc.getNameSide(self.factorAttrNames[idx])
                if cmds.objExists("{0}_{1}_MRC".format(side, name)):
                    continue
                sxConnect = None
                if self.connectFalloff and self.falloffCurveWeightNode:
                    sxConnect = "{0}.inputs[{1}].falloffU".format(self.falloffCurveWeightNode, idx + self.falloffElemStart)

                tmpCtrl = meshRivetCtrl.component(name = name,
                                                    side=side,
                                                    speedTxDefault=1,
                                                    speedTyDefault=1,
                                                    speedTzDefault=1,
                                                    # curveData=None,
                                                    mesh = self.controlRivetMesh,
                                                    translate = [center.x, center.y, center.z],
                                                    # rotate = None,
                                                    # scale = None,
                                                    # guide = False,
                                                    txConnectionAttr=txConnect,
                                                    # tyConnectionAttr=self.floatAttrs[idx],
                                                    tyConnectionAttr="{0}.inputs[{1}].factor".format(self.node, elemIdx),
                                                    # tzConnectionAttr=None,

                                                    # rxConnectionAttr=None,
                                                    # ryConnectionAttr=None,
                                                    # rzConnectionAttr=None,

                                                    sxConnectionAttr=sxConnect,
                                                    # syConnectionAttr=None,
                                                    # szConnectionAttr=None,

                                                    normalConstraintPatch=None,
                                                    selection=False,
                                                    mirror=False,
                                                    size=self.controlSize,
                                                    offset = self.controlOffset)

                if tmpCtrl.ctrl not in self.controls:
                    self.controls.append(tmpCtrl.ctrl)

    def outputConnections(self):
        # Checks if the output type is kDoubleArray or a multiFloat (maya native deformer weights type)
        if not self.outputAttrs:
            return
        for idx, attr in enumerate(self.outputAttrs):
            attrType = checkOutputWeightType(attr)
            if attrType:
                # If True, then this output attribute will get the kDoubleArray Output
                cmds.connectAttr("{0}.outWeightsDoubleArray".format(self.node), attr, f=True)
                if self.UDLR:
                    cmds.connectAttr("{0}.outWeightsDoubleArray".format(self.node_LR), self.outputAttrs_LR[idx], f=True)
            else:
                # If False, then this output attribute will get the outWeightsFloatArray
                cmds.connectAttr("{0}.outWeightsFloatArray[0]".format(self.node), attr, f=True)
                if self.UDLR:
                    cmds.connectAttr("{0}.outWeightsFloatArray[0]".format(self.node_LR), self.outputAttrs_LR[idx], f=True)

def getPointPositionByWeights(weightList, mesh, threshold = .9):
    fnMesh = misc.getOMMesh(mesh)
    meshDag = misc.getDag(mesh)
    allPoints = OpenMaya.MPointArray()
    fnMesh.getPoints(allPoints)
    bBox = OpenMaya.MBoundingBox()
    for idx in range(len(weightList)):
        if weightList[idx] >= threshold:
            bBox.expand(allPoints[idx])
    return bBox.height(), bBox.width(), bBox.depth(), bBox.center()


def nameBasedOnRange(count, name, suffixSeperator="_", suffix="", ):
    retNames = []
    midpoint = count/2
    for idx in range(count):
        current = idx
        side = "L"
        formatName = "{0}_{1}{2:02}{3}{4}"
        if idx == midpoint:
            side = "C"
            current = ""
            formatName = "{0}_{1}{2}{3}{4}"
        if idx > midpoint:
            side = "R"
            current = count -1 - idx
        # finalName = formatName.format(side, name, current, suffixSeperator, suffix)
        # if suffix is "None":
        #     finalName = finalName.replace("_None", "")
        retNames.append(formatName.format(side, name, current, suffixSeperator, suffix))
    return retNames

def createNormalizedAnimWeights(name="Temp", num=9, timeRange=20.0, suffix="ACV", offset=.15, centerWeight = .35, outerWeight = .3, angle = 50, nudge = 0,
                                intermediateVal=.2, lastAngle=0, lastIntermediateVal=.2, intermediateAngle=0, lastIntermediateAngle=0, createSingleFalloff=True, singleFalloffName="Single"):
    keyframes = []
    falloffKeyframes = []
    ratio = timeRange/num
    midpoint = num/2
    for idx in range(num):
        # print idx, "IDX !!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        # print num, "NUUUUUUUUM"
        count = idx
        side = "L"
        formatName = "{0}_{1}{2:02}_{3}"
        formatNameFalloff = "{0}_{1}Falloff{2:02}_{3}"
        if idx == midpoint:
            side = "C"
            count = ""
            formatName = "{0}_{1}{2}_{3}"
            formatNameFalloff = "{0}_{1}Falloff{2}_{3}"
        if idx > midpoint:
            side = "R"
            count = num -1 - idx
        weightCurve = getNodeAgnostic(nodeType="animCurveTU", name=formatName.format(side, name, count, suffix), parent=None)
        try:
            cmds.cutKey(weightCurve, cl=True, option="keys")
        except:
            pass
        keyframes.append(weightCurve)
        # Falloff V curve
        falloffName = formatNameFalloff.format(side, name, count, suffix)
        if not singleFalloffName:
            singleFalloffName = name
        if createSingleFalloff:
            falloffName = "{0}Falloff_{1}".format(singleFalloffName, suffix)
        falloffKeyframes.append(getNodeAgnostic(nodeType="animCurveTU", name=falloffName, parent=None))
        # Make sure there is at least 1 key on the curves.  Will do nothing if keyframes already exist.
        for key in range(3):
            fIdx = float(idx)
            val=1.0
            itt = "spline"
            ott = "spline"

            currLeftIntermediateVal = intermediateVal
            currRightIntermediateVal = intermediateVal

            currentLeftAngle = angle
            currentLeftIntermediateAngle = intermediateAngle
            currentRightAngle = -angle
            currentRightIntermediateAngle = -intermediateAngle

            if idx == 0:
                currentLeftAngle = lastAngle
                currentRightAngle = -angle
                currentLeftIntermediateAngle = lastIntermediateAngle
                currentRightIntermediateAngle = -intermediateAngle
                currLeftIntermediateVal = lastIntermediateVal
                currRightIntermediateVal = intermediateVal



            if idx == num-1:
                currentLeftAngle = angle
                currentRightAngle = -lastAngle
                currentLeftIntermediateAngle = intermediateAngle
                currentRightIntermediateAngle = -lastIntermediateAngle
                currLeftIntermediateVal = intermediateVal
                currRightIntermediateVal = lastIntermediateVal




            time=fIdx+key
            if key == 0:
                itt = "linear"
                ott = "slow"
                val=0.0
                time=fIdx+key + offset
                time=time+nudge
            # if key == 1:
            #     itt = "spline"
            #     ott = "spline"
            #     val=currLeftIntermediateVal
            #     time=fIdx+key + offset
            #     time=time+nudge
                
            # if key == 3:
            #     itt = "spline"
            #     ott = "spline"
            #     val=currRightIntermediateVal
            #     time=fIdx+key - offset
            #     time=time-nudge


            if key == 2:
                itt = "fast"
                ott = "linear"
                val=0.0 
                time=fIdx+key - offset
                time=time-nudge


            # inTangentType(itt)	string	create
            # The in tangent type for keyframes set by this command. Valid values are "spline," "linear," "fast," "slow," "flat," "step," and "clamped." Default is "keyTangent -q -g -inTangentType"
            # outTangentType(ott)	string	create
            # The out tangent type for keyframes set by this command. Valid values are "spline," "linear," "fast," "slow," "flat," "step," and "clamped." Default is "keyTangent -q -g -outTangentType"
            cmds.setKeyframe(weightCurve, v=val, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=time, itt=itt, ott=ott)
            # cmds.keyTangent( weightCurve, edit=True, time=(idx+key,idx+key), absolute=True, outAngle=100, outWeight=5,wl=False, weightedTangents=False)
            # cmds.keyTangent( weightCurve, edit=True, time=(idx+key,idx+key), absolute=True, outAngle=100, outWeight=5, l=False, weightedTangents=False)
            # angle = angle
            time = (time,time)



            # currentLeftAngle = angle
            # currentLeftIntermediateAngle = intermediateAngle

            # currentRightAngle = -angle
            # currentRightIntermediateAngle = -intermediateAngle

            # if idx == 0:
            #     currentLeftAngle = lastAngle
            #     currentRightAngle = -angle
            #     currentLeftIntermediateAngle = lastIntermediateAngle
            #     currentRightIntermediateAngle = -intermediateAngle

            # if idx == num-1:
            #     currentLeftAngle = angle
            #     currentRightAngle = -lastAngle
            #     currentLeftIntermediateAngle = intermediateAngle
            #     currentRightIntermediateAngle = -lastIntermediateAngle



            if key == 0:
                cmds.keyTangent( weightCurve, time=time, edit=True,  weightedTangents=True)
                cmds.keyTangent( weightCurve, time=time, edit=True,  lock=False)
                cmds.keyTangent( weightCurve, time=time, edit=True,  outWeight=outerWeight, inWeight=outerWeight, outAngle=currentLeftAngle,inAngle=0)

            # if key == 1:
            #     cmds.keyTangent( weightCurve, time=time, edit=True,  weightedTangents=True)
            #     cmds.keyTangent( weightCurve, time=time, edit=True,  lock=True)
            #     cmds.keyTangent( weightCurve, time=time, edit=True, outAngle=currentLeftIntermediateAngle)

            if key == 1:
                cmds.keyTangent( weightCurve, time=time, edit=True,  weightedTangents=True)
                cmds.keyTangent( weightCurve, time=time, edit=True,  outWeight=centerWeight, inWeight=centerWeight, outAngle=0,inAngle=0)

            # if key == 3:
            #     cmds.keyTangent( weightCurve, time=time, edit=True,  weightedTangents=True)
            #     cmds.keyTangent( weightCurve, time=time, edit=True,  lock=True)
            #     cmds.keyTangent( weightCurve, time=time, edit=True, outAngle=currentRightIntermediateAngle)

            if key == 2:
                cmds.keyTangent( weightCurve, time=time, edit=True,  weightedTangents=True)
                cmds.keyTangent( weightCurve, time=time, edit=True,  lock=False)
                cmds.keyTangent( weightCurve, time=time, edit=True,  outWeight=outerWeight, inWeight=outerWeight, outAngle=0,inAngle=currentRightAngle)
    # lastTime = cmds.findKeyframe(keyframes[-1], index=(4,4), time=True)
    # lastTime = (cmds.keyframe(keyframes[-1], indexValue=True, q=True))[-1]

    flatTime = int(time[0])
    # scaleAmt = float(timeRange)/(float(time[0])+1.0)
    scaleAmt = float(timeRange)/float(flatTime)
    cmds.scaleKey(keyframes, 
                scaleSpecifiedKeys = False,
                timeScale = scaleAmt,
                timePivot = 0.0,
                floatScale = 1, 
                floatPivot = 0.0,
                valueScale = 1,
                valuePivot = 0)

    # Center at 0
    for key in keyframes:
        cmds.keyframe(key, edit=True,relative=True,timeChange=-(timeRange/2),time=(-100,timeRange + 100))
        cmds.setKeyframe(key, breakdown=0,
                            hierarchy="none", controlPoints=2,
                            shape=0, time=-timeRange/2)
        cmds.setKeyframe(key, breakdown=0,
                            hierarchy="none", controlPoints=2,
                            shape=0, time=timeRange/2)

    cmds.select(keyframes)

    initVKeyframesLinear(falloffKeyframes)
    return keyframes, falloffKeyframes
        # weightCurvesFalloff = getNodeAgnosticMultiple(nodeType="animCurveTU", names=self.weightNamesFalloff, parent=None)
        # Make sure there is at least 1 key on the curves.  Will do nothing if keyframes already exist.
        # initUKeyframes(weightCurves)
        # initVKeyframes(weightCurvesFalloff)

def getNodeAgnostic(name, nodeType, parent):
    if cmds.objExists(name):
        return name
    return cmds.createNode(nodeType, n=name, p=parent)

def getNodeAgnosticMultiple(names=[], nodeType=None,  parent=None):
    retNodes = []
    for name in names:
        retNodes.append(getNodeAgnostic(name=name, nodeType=nodeType, parent=parent))
    return retNodes


def initUKeyframes(animCurves):
    for animCurve in animCurves:
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=-10)
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=0)
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=10)

def initVKeyframes(animCurves):
    for animCurve in animCurves:
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=-10)
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=10)

def initVKeyframesLinear(animCurves):
    for animCurve in animCurves:
        oCurve = misc.getOMAnimCurve(animCurve)
        if not oCurve.numKeys():
            cmds.setKeyframe(animCurve, v=0, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=-10, itt="linear")
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=9.7, itt="linear")
            cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                hierarchy="none", controlPoints=2,
                                shape=0, time=10, itt="linear")


def checkOutputWeightType(outputAttrToCheck):
    testAttr = outputAttrToCheck
    if "[" in outputAttrToCheck:
        testAttr = outputAttrToCheck.split("[")[0]
    node, attr = extractNodeAttr(testAttr)
    isMulti = cmds.attributeQuery(attr, node=node, multi=True)
    if isMulti:
        return False
    return True


def availableElemCheck(multiAttrToCheck):
    availableInputElem = 0
    if multiAttrToCheck:
        allElemsConnected = 0
        availableInputElem = -1
        if not cmds.objExists(multiAttrToCheck):
            return 0
        numElements = cmds.getAttr(multiAttrToCheck, mi=True)
        if not numElements:
            return 0
        numElements = len(numElements)
        
        node, attr = extractNodeAttr(multiAttrToCheck)
        if not node:
            return 0
        for elemIdx in range(numElements):
            isConnections = False
            for child in cmds.attributeQuery(attr, node=node, lc=True):
                connections = cmds.listConnections("{0}[{1}].{2}".format(multiAttrToCheck, elemIdx, child))
                if connections:
                    isConnections = True
            # If none of the children are connected, you know the element is free to be connected to
            if not isConnections:
                availableInputElem = elemIdx
                break
        if availableInputElem == -1:
            availableInputElem = numElements

    return availableInputElem


def extractNodeAttr(fullAttrName):
    names = fullAttrName.split(".")
    node, attr = names[0], names[-1]
    return node, attr

def attrCheck(node, attrs, attrType=None, enumName=None, k=False, weightmap=False, defaultVals=[]):
    if not node:
        return
    retAttrs = []
    for idx, attr in enumerate(attrs):
        dv = 0.0
        if defaultVals:
            dv = defaultVals[idx]
        fullName = node + "." + attr
        if cmds.objExists(fullName):
            retAttrs.append(fullName)
            # update dv
            if defaultVals:
                cmds.addAttr(fullName, e=True, dv=dv)
                cmds.setAttr(fullName, dv)
            continue
        if weightmap:
            weightMapUtils.createWeightMapOnObject(node, attr)
        else:
            if attrType == "enum":
                cmds.addAttr(node, at=attrType, ln=attr, enumName=enumName, k=k, dv=dv)
            else:
                cmds.addAttr(node, at=attrType, ln=attr, k=k, dv=dv)

        retAttrs.append(fullName)
    return retAttrs












'''
EXAMPLE

from maya import cmds
import maya.OpenMaya as OpenMaya
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)
from rig.utils import weightMapUtils
from rig.deformers import base
from rig.deformers import weightStack
reload(weightStack)
reload(base)
#weightStack.createNormalizedAnimWeights(name="Lip", num=5, timeRange=20.0, offset=.3)

cmds.file( new=True, f=True )

cmds.unloadPlugin("collision")

cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")




fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/TestCurveWeights.ma"
cmds.file( fileName, o=True, f=True )

#cmds.file(new=True, f=True)
control = cmds.circle(n="Control", nr=[0,1,0])[0]
subdivisions = 30
deformMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2, sx=subdivisions,  n="deformMesh")[0]
cluster = cmds.cluster(deformMesh)[1]
cmds.move(1, cluster, y=True)
base = cmds.polyPlane(ax=[0,0,1], h=2, w=2,sx=subdivisions, n="BASE")[0]
cmds.setAttr(base + ".v",0)
projectionMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2, sx=3)[0]
cmds.setAttr(projectionMesh + ".v",0)
cluster2 = cmds.cluster(deformMesh)[1]
cmds.move(1, cluster2, x=True)

cmds.move(2, projectionMesh, z=True)


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

createNum1 = 3
createNum2 = 9
createNum3 = 7

curveWeights = weightStack.AnimCurveWeight(name="TestCurveWeights",
                                    baseGeo=base,
                                    ctrlNode=control,
                                    projectionGeo=projectionMesh,
                                    weightAttrNames=[],
                                    addNewElem=False,
                                    autoCreateAnimCurves = True,
                                    autoCreateName = "lipSingle",
                                    autoCreateNum = 1,
                                    autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal,lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,

)
curveWeights.create()


stack = weightStack.WeightStack(name="TestWeights",
                                geoToWeight=base,
                                ctrlNode=control,
                                weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                addNewElem=False,
                                outputAttrs = ["cluster1.weightList[0]"],
                                outputAttrs_LR = ["cluster2.weightList[0]"],
                                autoCreate=True,
                                controlRivetMesh = deformMesh,
                                falloffCurveWeightNode="TestCurveWeights",
                                autoCreateName="lipSingle",
                                controlSize = .07,
                                controlOffset = [0,0.0,.1],
                                )
stack.create()
curveWeights.setFalloffDefaults()
cmds.setAttr("C_lipSingle_CTL.ty", -0.6)

autoCreateTimeRange = 20.0
offset=0
centerWeight = .3
outerWeight = .5
angle = 0
nudge = -0.14
intermediateVal = .0
intermediateAngle=0

lastAngle = 60
lastIntermediateVal=.8
lastIntermediateAngle=30

curveWeights = weightStack.AnimCurveWeight(name="TestCurveWeights",
                                    baseGeo=base,
                                    ctrlNode=control,
                                    projectionGeo=projectionMesh,
                                    weightAttrNames=[],
                                    addNewElem=True,
                                    autoCreateAnimCurves = True,
                                    autoCreateName = "lipPrime",
                                    autoCreateNum = createNum1,
                                    autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal,lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,
                                    #autoCreateTimeRange = 20.0, offset=.0, centerWeight = .4, outerWeight = .6, angle = 0, nudge = -0.03
                                    startElem = 1,

)
curveWeights.create()


stack = weightStack.WeightStack(name="TestWeights",
                                geoToWeight=base,
                                ctrlNode=control,
                                weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                addNewElem=True,
                                outputAttrs = ["cluster1.weightList[0]"],
                                outputAttrs_LR = ["cluster2.weightList[0]"],
                                autoCreate=True,
                                controlRivetMesh = deformMesh,
                                falloffCurveWeightNode="TestCurveWeights",
                                autoCreateName="lipPrime",
                                controlSize = .05,
                                controlOffset = [0,0.1,.1],
                                falloffElemStart = 1
                                )
stack.create()
curveWeights.setFalloffDefaults()


#############################################################################################################################

curveWeights = weightStack.AnimCurveWeight(name="TestCurveWeights",
                                    baseGeo=base,
                                    ctrlNode=control,
                                    projectionGeo=projectionMesh,
                                    weightAttrNames=[],
                                    addNewElem=True,
                                    autoCreateAnimCurves = True,
                                    autoCreateName = "lipSecondary",
                                    autoCreateNum = createNum2,
                                    autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal,lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,
                                    #autoCreateTimeRange = 20.0, offset=.0, centerWeight = .4, outerWeight = .6, angle = 0, nudge = -0.03
                                    startElem = 4,

)
curveWeights.create()


stack = weightStack.WeightStack(name="TestWeights",
                                geoToWeight=base,
                                ctrlNode=control,
                                weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                addNewElem=True,
                                outputAttrs = ["cluster1.weightList[0]"],
                                outputAttrs_LR = ["cluster2.weightList[0]"],
                                autoCreate=True,
                                controlRivetMesh = deformMesh,
                                falloffCurveWeightNode="TestCurveWeights",
                                autoCreateName="lipSecondary",
                                controlSize = .03,
                                controlOffset = [0,0.05,.1],
                                falloffElemStart = 4
                                )
stack.create()
curveWeights.setFalloffDefaults()

#############################################################################################################################

'''