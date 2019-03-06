from maya import cmds
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
reload(misc)
import copy


class Node(object):
    def __init__(self,
                 name,
                 nodeType = None,
                 parent = None,
                 outputAttrs=[],
                 startAtElemIdx=-1,
                 addNewElem=False):
        self.name = name
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
                 projectionGeo = "",
                 weightAttrNames = [],
                 animCurveSuffix = "ACV",
                 autoCreateAnimCurves = False,
                 autoCreateName = "lip",
                 autoCreateNum = 11,
                 autoCreateTimeRange = 20.0,
                 offset=.15, centerWeight = .35, outerWeight = .3, angle = 30, nudge = 1.0,





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
        self.projectionGeo = projectionGeo
        self.weightAttrNames = weightAttrNames
        self.animCurveSuffix = animCurveSuffix
        self.startElem = 0
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


        self.offset=offset
        self.centerWeight =centerWeight
        self.outerWeight = outerWeight
        self.angle = angle
        self.nudge = nudge


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

    def getDriverNodes(self):
        self.projectionMesh = misc.getShape(self.projectionGeo)
        self.baseMesh = misc.getShape(self.baseGeo)

        if self.autoCreateAnimCurves:
            self.weightCurves, self.weightCurvesFalloff = createNormalizedAnimWeights(name=self.autoCreateName, num=self.autoCreateNum,
                                                                                      timeRange=self.autoCreateTimeRange, suffix=self.animCurveSuffix,
                                                                                      offset=self.offset, centerWeight =self.centerWeight, outerWeight = self.outerWeight,
                                                                                      angle = self.angle, nudge=self.nudge)
            return
        
        self.weightCurves = getNodeAgnosticMultiple(nodeType="animCurveTU", names=self.weightNames, parent=None)
        self.weightCurvesFalloff = getNodeAgnosticMultiple(nodeType="animCurveTU", names=self.weightNamesFalloff, parent=None)
        # Make sure there is at least 1 key on the curves.  Will do nothing if keyframes already exist.
        initUKeyframes(self.weightCurves)
        initVKeyframes(self.weightCurvesFalloff)

    def inputConnections(self):
        cmds.connectAttr(self.membershipWeights, "{0}.membershipWeights".format(self.node), f=True)
        cmds.connectAttr("{0}.worldMesh".format(self.projectionMesh), "{0}.projectionMesh".format(self.node), f=True)
        cmds.connectAttr("{0}.worldMesh".format(self.baseMesh), "{0}.inMesh".format(self.node), f=True)

        # format the output attribute for the anim curves so you don't have to do it in the loop
        self.uCurveOutAttrs = ["{0}.output".format(x) for x in self.weightCurves]
        self.vCurveOutAttrs = ["{0}.output".format(x) for x in self.weightCurvesFalloff]

        self.elemCheck("{0}.inputs".format(self.node))
        for idx in range(len(self.weightCurves)):
            elemIdx = idx + self.startElem
            cmds.connectAttr(self.uCurveOutAttrs[idx], "{0}.inputs[{1}].AnimCurveU".format(self.node, elemIdx),f=True)
            cmds.connectAttr(self.vCurveOutAttrs[idx], "{0}.inputs[{1}].AnimCurveV".format(self.node, elemIdx),f=True)
        
            kDoubleOut = "{0}.outDoubleWeights[{1}].outWeightsDoubleArray".format(self.node, idx)
            kFloatOut = "{0}.outDoubleWeights[{1}].outWeightsFloatArray[{1}]".format(self.node, idx)
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
                weightAttr = "{0}.outFloatWeights[{1}].outWeightsFloatArray[{1}]".format(self.node, elemIdx)                # Call getAttr to create an elem if it doesn't already exist
            # Call getAttr to create an elem if it doesn't already exist
            cmds.getAttr(weightAttr)
            cmds.connectAttr(weightAttr, attr, f=True)
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

        self.isKDoubleArrayOutputWeights = True
        self.nodeType = "LHWeightNode"

    def check(self):
        listsToCheck = [self.weightMapAttrNames, self.factorAttrNames, self.operationVals]
        if self.autoCreate:
            return
        if any(len(listArray) != len(self.weightMapAttrNames) for listArray in listsToCheck):
            raise Exception("weightMapAttrs, factorAttrs, and operationVals all need to be the same length, " +
                            "if you want multiple maps to be connected to multiple factor attrs, use the same " + 
                            "weightMapAttrs multiple times")
            quit()

    def getAttrs(self):
        if self.autoCreate:
            self.weightMapAttrs = self.weightMapAttrNames
            self.factorAttrNames = nameBasedOnRange(count=len(self.weightMapAttrNames), name=self.autoCreateName, suffix="")
            self.floatAttrs = attrCheck(node=self.ctrlNode,
                                            attrs=self.factorAttrNames,
                                            attrType="float",
                                            k=True)
            self.operationVals = [self.autoCreateOperationVal for x in range(len(self.weightMapAttrNames))]
            return
        self.weightMapAttrs = attrCheck(node=self.geoToWeight,
                                            attrs=self.weightMapAttrNames,
                                            attrType=None,
                                            weightmap=True)
        self.floatAttrs = attrCheck(node=self.ctrlNode,
                                         attrs=self.factorAttrNames,
                                         attrType="float",
                                         k=True)
    
    def inputConnections(self):
        self.elemCheck("{0}.inputs".format(self.node))
        for idx in range(len(self.weightMapAttrs)):
            elemIdx = idx + self.startElem
            # print "SOURCE ", self.weightMapAttrs[idx], "DESTINATION ", "{0}.inputs[{1}].inputWeights".format(self.node, elemIdx)
            cmds.connectAttr(self.weightMapAttrs[idx], "{0}.inputs[{1}].inputWeights".format(self.node, elemIdx), f=True)
            cmds.connectAttr(self.floatAttrs[idx], "{0}.inputs[{1}].factor".format(self.node, elemIdx), f=True)
            cmds.setAttr("{0}.inputs[{1}].operation".format(self.node, elemIdx), self.operationVals[idx])
    
    def outputConnections(self):
        # Checks if the output type is kDoubleArray or a multiFloat (maya native deformer weights type)
        if not self.outputAttrs:
            return
        for attr in self.outputAttrs:
            attrType = checkOutputWeightType(attr)
            if attrType:
                # If True, then this output attribute will get the kDoubleArray Output
                cmds.connectAttr("{0}.outWeightsDoubleArray".format(self.node), attr, f=True)
            else:
                # If False, then this output attribute will get the outWeightsFloatArray
                cmds.connectAttr("{0}.outWeightsFloatArray[0]".format(self.node), attr, f=True)

def nameBasedOnRange(count, name, suffix):
    retNames = []
    midpoint = count/2
    for idx in range(count):
        current = idx
        side = "L"
        formatName = "{0}_{1}{2:02}_{3}"
        if idx == midpoint:
            side = "C"
            current = ""
            formatName = "{0}_{1}{2}_{3}"
        if idx > midpoint:
            side = "R"
            current = count -1 - idx
        retNames.append(formatName.format(side, name, current, suffix))
    return retNames

def createNormalizedAnimWeights(name="Temp", num=9, timeRange=20.0, suffix="ACV", offset=.15, centerWeight = .35, outerWeight = .3, angle = 50, nudge = 0
):
    keyframes = []
    falloffKeyframes = []
    ratio = timeRange/num
    midpoint = num/2
    for idx in range(num):
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
        falloffKeyframes.append(getNodeAgnostic(nodeType="animCurveTU", name=formatNameFalloff.format(side, name, count, suffix), parent=None))
        # Make sure there is at least 1 key on the curves.  Will do nothing if keyframes already exist.
        for key in range(5):
            idx = float(idx)
            val=1.0
            itt = "spline"
            ott = "spline"
            time=idx+key
            if key == 0:
                itt = "linear"
                ott = "slow"
                val=0.0
                time=idx+key + offset
                time=time+nudge
            if key == 1:
                itt = "spline"
                ott = "spline"
                val=0.2
                time=idx+key + offset
                time=time+nudge
                
            if key == 3:
                itt = "spline"
                ott = "spline"
                val=0.2
                time=idx+key - offset
                time=time-nudge


            if key == 4:
                itt = "fast"
                ott = "linear"
                val=0.0 
                time=idx+key - offset
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
            time=(time,time)
            if key == 0:
                cmds.keyTangent( weightCurve,time=time, edit=True,  weightedTangents=True)
                cmds.keyTangent( weightCurve,time=time, edit=True,  lock=False)
                cmds.keyTangent( weightCurve,time=time, edit=True,  outWeight=outerWeight, inWeight=outerWeight, outAngle=angle,inAngle=0)
            if key == 2:
                cmds.keyTangent( weightCurve,time=time, edit=True,  weightedTangents=True)
                cmds.keyTangent( weightCurve,time=time, edit=True,  outWeight=centerWeight, inWeight=centerWeight, outAngle=0,inAngle=0)
            if key == 4:
                cmds.keyTangent( weightCurve,time=time, edit=True,  weightedTangents=True)
                cmds.keyTangent( weightCurve,time=time, edit=True,  lock=False)
                cmds.keyTangent( weightCurve,time=time, edit=True,  outWeight=outerWeight, inWeight=outerWeight, outAngle=0,inAngle=-angle)
    # lastTime = cmds.findKeyframe(keyframes[-1], index=(4,4), time=True)
    # lastTime = (cmds.keyframe(keyframes[-1], indexValue=True, q=True))[-1]
    print time

    print timeRange
    flatTime = int(time[0])
    # scaleAmt = float(timeRange)/(float(time[0])+1.0)
    scaleAmt = float(timeRange)/float(flatTime)
    print scaleAmt
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

    initVKeyframes(falloffKeyframes)
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



