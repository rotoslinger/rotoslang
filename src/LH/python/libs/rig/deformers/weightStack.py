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
                 animCurveSuffix="ACV",
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
        print self.weightNames, self.weightNamesFalloff


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

        self.isKDoubleArrayOutputWeights = True
        self.nodeType = "LHWeightNode"

    def check(self):
        listsToCheck = [self.weightMapAttrNames, self.factorAttrNames, self.operationVals]
        if any(len(listArray) != len(self.weightMapAttrNames) for listArray in listsToCheck):
            raise Exception("weightMapAttrs, factorAttrs, and operationVals all need to be the same length, " +
                            "if you want multiple maps to be connected to multiple factor attrs, use the same " + 
                            "weightMapAttrs multiple times")
            quit()

    def getAttrs(self):
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
        dv = 1
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



