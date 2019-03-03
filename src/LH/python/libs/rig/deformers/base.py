from maya import cmds
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
reload(misc)
import copy

"""
sld = cmds.ls(typ="LHSlideDeformer")
vec = cmds.ls(typ="LHVectorDeformer")
crd = cmds.ls(typ="LHCurveRollDeformer")
for i in sld+vec+crd:
    print i
    print weightMapUtils.createMultiWeightMapOnDeformer(deformer=i, mesh="C_body_HI", weightName="membership",addAttr=True,dataType="doubleArray")
"""

def createMeshPlane():
    return

def createNurbsPlane():
    return

class Node(object):
    def __init__(self,
                 name,
                 nodeType = None,
                 parent = None,
                 attrNode = None,
                 kDoubleArrayNode = None,
                 floatNode = None,
                 enumNode = None,
                 inKDoubleArrayAttrs = [],
                 inFloatAttrs = [],
                 inEnumAttrs = [],
                 inKDoubleArrayVals=[],
                 inFloatVals=[],
                 inEnumVals=[],
                 enumNames = [],
                 nodeKDoublePlugMap="",
                 nodeFloatPlugMap="",
                 nodeEnumPlugMap="",
                 outKDoubleArrayAttr ="",
                 inputMultiAttrToAddTo="",
                 outputMultiAttrToAddTo=""):

        self.inputMultiAttrToAddTo = inputMultiAttrToAddTo
        self.inputMultiTestAttrs = []
        self.outputMultiAttrToAddTo = outputMultiAttrToAddTo
        self.outputMultiTestAttrs = []

        self.availableInputElem = 0
        self.availableOutputElem = 0

        # This index will be used to offset the element connections
        # This is used when elements already exist, so new ones need to be created
        self.inputMultiElementOffset = 0
        self.nodeType = nodeType
        self.name = name
        self.parent = parent

        self.attrNode = attrNode
        self.floatNode = floatNode
        self.enumNode = enumNode
        self.kDoubleArrayNode = kDoubleArrayNode

        # Where to put all of the new attributes.  If you want them all on one node just use the attrNode arg
        for node in ["floatNode", "enumNode"]:
            if self.attrNode and not getattr(self, node):
                setattr(self, node, self.attrNode)

        self.inKDoubleArrayAttrs = inKDoubleArrayAttrs
        self.inFloatAttrs = inFloatAttrs
        self.inEnumAttrs = inEnumAttrs

        self.inKDoubleArrayVals = inKDoubleArrayVals
        self.inFloatVals = inFloatVals
        self.inEnumVals = inEnumVals

        self.enumNames = enumNames

        self.outKDoubleArrayAttr = outKDoubleArrayAttr

        self.floatPlugNames = []
        self.kDoubleArrayPlugNames = []
        self.enumPlugNames = []

        self.inputConnectionMap = {}
        self.inputConnectionMap = {}
        self.setAttrMap = {}
        self.outputConnectionMap = {}
        self.doubleArrayAttrs = []
        self.floatAttrs = []
        self.enumAttrs = []
        self.nodeKDoublePlugMap = nodeKDoublePlugMap
        self.nodeFloatPlugMap = nodeFloatPlugMap
        self.nodeEnumPlugMap = nodeEnumPlugMap
        self.outputConnectionMapMulti = {}
        # super(Node, self).__init__(**kw)

    def getNode(self):
        if cmds.objExists(self.name):
            self.node = self.name
            return
        self.node = cmds.createNode(self.nodeType, n=self.name, p=self.parent)

    def availableElemCheck(self, multiAttrToCheck):
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
            node, attr = self.extractNodeAttr(multiAttrToCheck)
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

    def inputElemCheck(self):
        self.availableInputElem = self.availableElemCheck(self.inputMultiAttrToAddTo)

    def outputElemCheck(self):
        self.availableOutputElem = self.availableElemCheck(self.outputMultiAttrToAddTo)

    @staticmethod
    def getNodeAgnostic(nodeType, name, parent):
        if cmds.objExists(name):
            return name
        return cmds.createNode(nodeType, n=name, p=parent)

    def getNodeAgnosticMultiple(self, nodeType=None, names=[], parent=None):
        retNodes = []
        for name in names:
            retNodes.append(self.getNodeAgnostic(nodeType, name, parent))
        return retNodes

    def initDriverNodes(self):
        return

    def getDriverNodes(self):
        return

    @staticmethod
    def initKeyframes(animCurves):
        for animCurve in animCurves:
            oCurve = misc.getOMAnimCurve(animCurve)
            if not oCurve.numKeys():
                cmds.setKeyframe(animCurve, v=1, breakdown=0,
                                 hierarchy="none", controlPoints=0,
                                 shape=0, time=0)

    def attrCheck(self, node, attrs, attrType=None, enumName=None, k=False, weightmap=False, defaultVals=[]):
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

    def getAttrs(self):
        # For each inWeightAttrs check if the attribute exists on the geometry
        self.doubleArrayAttrs = self.attrCheck(node=self.kDoubleArrayNode,
                                               attrs=self.inKDoubleArrayAttrs,
                                               attrType=None,
                                               weightmap=True,
                                               defaultVals=self.inKDoubleArrayVals)
        self.floatAttrs = self.attrCheck(node=self.floatNode,
                                         attrs=self.inFloatAttrs,
                                         attrType="float",
                                         k=True,
                                         defaultVals=self.inFloatVals)
        self.enumAttrs = self.attrCheck(node=self.enumNode,
                                        attrs=self.inEnumAttrs,
                                        attrType="enum",
                                        enumName=self.enumNames,
                                        k=True,
                                        defaultVals=self.inEnumVals)

    @staticmethod
    def extractNodeAttr(fullAttrName):
        names = fullAttrName.split(".")
        node, attr = names[0], names[-1]
        return node, attr

    def initSetMultiAttrs(self):
        if not self.doubleArrayAttrs:
            self.setAttrMap[self.nodeKDoublePlugMap] = self.inKDoubleArrayVals
        if not self.floatAttrs:
            self.setAttrMap[self.nodeFloatPlugMap] = self.inFloatVals
        if not self.enumAttrs:
            self.setAttrMap[self.nodeEnumPlugMap] = self.inEnumVals

    def setMultiAttrs(self):
        for attributeMap in self.setAttrMap.keys():
            if not self.setAttrMap[attributeMap]:
                continue
            for idx, val in enumerate(self.setAttrMap[attributeMap]):
                # Get the attr first in order to create the element if it doesn't already exist
                cmds.getAttr(attributeMap.format(self.node, idx))
                cmds.setAttr(attributeMap.format(self.node, idx), val)

    @staticmethod
    def connectionCheck(srcAttr, destAttr):
        connections = cmds.listConnections(destAttr, d=True, p=True)
        # make case insensitive, because of short names
        if connections and srcAttr.lower() in [x.lower() for x in connections]:
            return True
        return False

    def connectMultiInputViaMap(self, attr, inputAttrMap, idx):
        # Check outputs, make sure connections don't already exist.
        destAttr = inputAttrMap.format(self.node, idx)
        if self.connectionCheck(attr, destAttr):
            return
        cmds.connectAttr(attr, inputAttrMap.format(self.node, idx), f=False)


    def connectOutputViaMap(self, outputAttrMap, attr):
        destAttr = outputAttrMap.format(self.node)
        if self.connectionCheck(attr, destAttr):
            return
        cmds.connectAttr(destAttr, attr, f=False)

    def initInputConnections(self):
        self.inputConnectionMap = {self.nodeKDoublePlugMap: self.doubleArrayAttrs,
                                   self.nodeFloatPlugMap: self.floatAttrs,
                                   self.nodeEnumPlugMap: self.enumAttrs}
        # self.inputConnectionMap = {self.nodeKDoublePlugMap: self.doubleArrayAttrs,
        #                            self.nodeFloatPlugMap: self.floatAttrs,
        #                            self.nodeEnumPlugMap: self.enumAttrs}

    # def elementCheck(self):


    def inputElementCheck(self):
        # return
        # Create a copy of the input connections to iterate over
        inputConnectionMapCopy = copy.deepcopy(self.inputConnectionMap)
        firstEmptyElement=0
        for attributeMap in inputConnectionMapCopy.keys():
            if not inputConnectionMapCopy[attributeMap]:
                continue
            if not "[" in attributeMap and not "]" in attributeMap:
                continue
            print "WEIGHT SEARCH ", self.nodeKDoublePlugMap, self.doubleArrayAttrs, "attrMap", attributeMap
            for idx, sourceAttr in enumerate(inputConnectionMapCopy[attributeMap]):
                dstAttr = attributeMap.format(self.node, idx)
                # if already connected remove from dictionary
                if self.connectionCheck(dstAttr, sourceAttr):
                    self.inputConnectionMap[attributeMap].remove(sourceAttr)
                    continue 
                connections = cmds.listConnections(sourceAttr, s=True, p=True)
                if connections:
                    if sourceAttr in self.inputConnectionMap[attributeMap]:
                        self.inputConnectionMap[attributeMap].remove(sourceAttr)
                    continue
        
    def inputConnections(self):
        """
        For multi index connections only
        """
        for attributeMap in self.inputConnectionMap.keys():
            if not self.inputConnectionMap[attributeMap]:
                continue
            for idx, attr in enumerate(self.inputConnectionMap[attributeMap]):
                self.connectMultiInputViaMap(attr, attributeMap, idx + self.availableInputElem)

    def initOutputConnections(self):
        return

    def outputElementCheck(self):
        return
        # for outputAttrMap in self.outputConnectionMap.keys():
        # for outputAttrMap in self.outputConnectionMapMulti.keys():

    def outputConnections(self):
        for outputAttrMap in self.outputConnectionMap.keys():
            self.connectOutputViaMap(outputAttrMap, self.outputConnectionMap[outputAttrMap])

    def outputConnectionsMulti(self):
        for outputAttrMap in self.outputConnectionMapMulti.keys():
            # in case the attributes don't exist yet
            destAttr = self.outputConnectionMapMulti[outputAttrMap]
            cmds.getAttr(outputAttrMap)
            cmds.getAttr(self.outputConnectionMapMulti[outputAttrMap])
            if self.connectionCheck(outputAttrMap, destAttr):
                return
            cmds.connectAttr(outputAttrMap, destAttr, f=False)

    def create(self):
        self.getNode()
        self.inputElemCheck()
        self.outputElemCheck()
        self.initDriverNodes()
        self.getDriverNodes()
        self.getAttrs()
        self.initSetMultiAttrs()
        self.setMultiAttrs()
        self.initInputConnections()
        self.inputElementCheck()
        self.inputConnections()
        self.initOutputConnections()
        self.outputElementCheck()
        self.outputConnections()
        self.outputConnectionsMulti()

    @staticmethod
    def findCompoundAttr(attributeName):
        if "." in attributeName and "[" in attributeName:
            attributeName = attributeName.split("[")[0]
            attributeName = attributeName.split(".")[1]
            return attributeName

    def getMultiInputAttrs(self, inputAttrMap):
        retAttrs = []
        attrName = self.findCompoundAttr(inputAttrMap)
        numElements = len(cmds.getAttr(self.node + "." + attrName, mi=True))
        for idx in range(numElements):
            fullAttrName = inputAttrMap.format(self.node, idx)
            tmpAttr = cmds.listConnections(fullAttrName, s=True, p=True)
            if tmpAttr:
                retAttrs.append(tmpAttr[0])
        return retAttrs

    def findInputAttrsMulti(self):
        self.doubleArrayAttrs = self.getMultiInputAttrs(self.nodeKDoublePlugMap)
        self.floatAttrs = self.getMultiInputAttrs(self.nodeFloatPlugMap)
        self.enumAttrs = self.getMultiInputAttrs(self.nodeEnumPlugMap)

    def findOutputConnections(self):
        return

    def findOther(self):
        return

    def find(self):
        self.getNode()
        self.findInputAttrsMulti()
        self.findOutputConnections()
        self.findOther()

class WeightStack(Node):
    def __init__(self,
                 geomNode=None,
                 inWeightAttrs=None,
                 inFactorAttrs=None,
                 inOperationAttrs=None,
                 outWeightAttr="",
                 inOperationVals=None,
                 **kw):
        super(WeightStack, self).__init__(**kw)

        # This is just to make the args more readable for this class.  It is fine to fallback on the Node version
        if not self.inKDoubleArrayAttrs:
            self.inKDoubleArrayAttrs = inWeightAttrs
        if not self.inFloatAttrs:
            self.inFloatAttrs = inFactorAttrs
        if not self.inEnumAttrs:
            self.inEnumAttrs = inOperationAttrs
        if not self.outKDoubleArrayAttr:
            self.outKDoubleArrayAttr = outWeightAttr
        if not self.inEnumVals:
            self.inEnumVals = inOperationVals
        self.enumNames = "add=0:subtract=1:multiply=2:divide=3:clampStack=4:clampPainted=5"
        self.nodeType = "LHWeightNode"
        self.geomNode = geomNode
        # This is where we put the weights
        self.kDoubleArrayNode = self.geomNode
        self.outWeightAttr = outWeightAttr
        self.nodeKDoublePlugMap = "{0}.inputs[{1}].inputWeights"
        self.nodeFloatPlugMap = "{0}.inputs[{1}].factor"
        self.nodeEnumPlugMap = "{0}.inputs[{1}].operation"
        self.inputConnectionMap = {self.nodeKDoublePlugMap: [],
                                   self.nodeFloatPlugMap: [],
                                   self.nodeEnumPlugMap: []}
        self.outputWeightsDoubleMap = "{0}.outWeightsDoubleArray"
        # Weight map stack is only ever meant to be used with 1 piece of geometry,
        # therefore the outWeightsFloatArray should never rise above the 0 index
        # If you need to weight another geometry, you should create another weight map stack
        self.outputWeightsFloatMap = "{0}.outWeightsFloatArray[0]"

        self.inputMultiAttrToAddTo = self.name + ".inputs"
        self.inputMultiTestAttrs = ["inputWeights", "factor", "operation"]


    # def initInputConnections(self):
    #     self.inputConnectionMap = {self.nodeKDoublePlugMap: self.doubleArrayAttrs,
    #                                self.nodeFloatPlugMap: self.floatAttrs,
    #                                self.nodeEnumPlugMap: self.enumAttrs}

    def initOutputConnections(self):
        testAttr = self.outKDoubleArrayAttr
        if "[" in self.outKDoubleArrayAttr:
            testAttr = self.outKDoubleArrayAttr.split("[")[0]
        node, attr = self.extractNodeAttr(testAttr)
        isMulti = cmds.attributeQuery(attr, node=node, multi=True)
        outputAttrMap = self.outputWeightsDoubleMap
        if isMulti:
            outputAttrMap = self.outputWeightsFloatMap
        self.outputConnectionMap = {outputAttrMap: self.outKDoubleArrayAttr}


# stack = base.WeightStack(name="TestWeights", geomNode="BASE", attrNode = "pSphere1",inWeightAttrs=["test1", "test2"], inFactorAttrs=["fTest1", "fTest2"], inOperationAttrs = [], outWeightAttr="cluster1.weightList[0]")
# stack.create()


class CurveWeights(Node):
    def __init__(self,
                 geomNode=None,
                 projectionMesh=None,
                 weightNames = [],
                 # vNames = [],
                 outWeightStackNode="",
                 outAttrs=[],
                 animCurveSuffix="ACV",
                 **kw):
        super(CurveWeights, self).__init__(**kw)
        self.nodeType = "LHCurveWeightNode"

        self.geomNode = misc.getShape(geomNode)
        self.kDoubleArrayNode = self.geomNode

        self.projectionMesh = projectionMesh
        self.membershipWeightsAttr = self.name + "_MembershipWeights"
        self.inKDoubleArrayAttrs = [self.membershipWeightsAttr]
        self.animCurveSuffix = animCurveSuffix

        # Sort the names
        self.weightNames = ["{0}_{1}".format(x, self.animCurveSuffix) for x in weightNames]
        self.weightNamesFalloff = ["{0}Falloff_{1}".format(x, self.animCurveSuffix) for x in weightNames]
        # self.vNames = ["{0}_{1}".format(x, self.animCurveSuffix) for x in vNames]
        # self.vNamesFalloff = ["{0}Falloff_{1}".format(x, self.animCurveSuffix) for x in vNames]

        self.outWeightStackNode = outWeightStackNode
        self.outAttrs = outAttrs
        self.uAnimCurves=[]
        self.uAnimCurvesFalloff = []
        self.vAnimCurves=[]
        self.vAnimCurvesFalloff = []
        self.outputMap = "{0}.outDoubleWeights[{1}].outWeightsDoubleArray"

        self.inputMultiAttrToAddTo = self.name + ".inputs"
        self.inputMultiTestAttrs = ["inputWeights", "factor", "operation"]

        self.outputMultiAttrToAddTo = outWeightStackNode + ".inputs"
        self.outputMultiTestAttrs = ["inputWeights", "factor", "operation"]
        self.numOutGoingElements = 0
        self.outgoingElements = []


    def getDriverNodes(self):
        self.projectionMesh = misc.getShape(self.projectionMesh)
        self.geomNode = misc.getShape(self.geomNode)
        self.weightCurves = self.getNodeAgnosticMultiple(nodeType="animCurveTU", names=self.weightNames, parent=None)
        self.weightCurvesFalloff = self.getNodeAgnosticMultiple(nodeType="animCurveTU", names=self.weightNamesFalloff, parent=None)
        # self.vCurves = self.getNodeAgnosticMultiple(nodeType="animCurveTU", names=self.vNames, parent=None)
        # self.vCurvesFalloff = self.getNodeAgnosticMultiple(nodeType="animCurveTU", names=self.vNamesFalloff, parent=None)
        # Make sure there is at least 1 key on the curves.  Will do nothing if keyframes already exist.
        self.initKeyframes(self.weightCurves + self.weightCurvesFalloff)

    def initInputConnections(self):
        super(CurveWeights, self).initInputConnections()
        self.inputConnectionMap["{0}.membershipWeights"] = [self.kDoubleArrayNode + "." + self.membershipWeightsAttr]
        self.inputConnectionMap["{0}.projectionMesh"] = [self.projectionMesh + ".worldMesh"]
        self.inputConnectionMap["{0}.inMesh"] = [self.geomNode + ".worldMesh"]

        self.uCurveOutAttrs = ["{0}.output".format(x) for x in self.weightCurves]
        self.vCurveOutAttrs = ["{0}.output".format(x) for x in self.weightCurvesFalloff]

        self.inputConnectionMap["{0}.inputs[{1}].AnimCurveU"] = self.uCurveOutAttrs
        self.inputConnectionMap["{0}.inputs[{1}].AnimCurveV"] = self.vCurveOutAttrs

    def findWeightStackElements(self):
        if not cmds.objExists(self.outWeightStackNode):
            # return
            # self.outWeightStackNode = cmds.createNode("LHWeightNode", n=self.outWeightStackNode)
        numOutGoingElements = cmds.getAttr(self.node + ".inputs", mi=True)
        if numOutGoingElements:
            numOutGoingElements = len(numOutGoingElements)
        else:
            numOutGoingElements = 0
        numInputElements = cmds.getAttr(self.outWeightStackNode + ".inputs", mi=True)
        if numInputElements:
            numInputElements = len(numInputElements)
        else:
            numInputElements = 0
        return numOutGoingElements, numInputElements

    def getOutgoingElems(self):
        numOutGoingElements = cmds.getAttr(self.node + ".inputs", mi=True)
        if numOutGoingElements:
            self.numOutGoingElements = len(numOutGoingElements)
        for elem in range(self.numOutGoingElements):
            print "OUTGOING", self.outputConnectionMapMulti


    def initOutputConnections(self):
        # Check inputs to determing outputs
        self.getOutgoingElems()
        if self.outWeightStackNode:
            numOutGoingElements, numInputElements = self.findWeightStackElements()
            print numOutGoingElements, numInputElements
            # return
            for idx in range(numOutGoingElements):
                outputMap = self.outputMap.format(self.node, idx + self.availableInputElem)
                # print outputMap
                self.outputConnectionMapMulti[outputMap] = "{0}.inputs[{1}].inputWeights".format(self.outWeightStackNode, idx + self.availableOutputElem)
        # print self.outputConnectionMapMulti

        # testAttr = self.outKDoubleArrayAttr
        # if "[" in self.outKDoubleArrayAttr:
        #     testAttr = self.outKDoubleArrayAttr.split("[")[0]
        # print testAttr
        # node, attr = self.extractNodeAttr(testAttr)
        # print node, attr
        # isMulti = cmds.attributeQuery(attr, node=node, multi=True)
        # outputAttrMap = self.outputWeightsDoubleMap
        # if isMulti:
        #     outputAttrMap = self.outputWeightsFloatMap
        #
        # print outputAttrMap, self.outKDoubleArrayAttr
        # self.outputConnectionMap = {outputAttrMap: self.outKDoubleArrayAttr}

    def outputConnections(self):
        return

# curveWeights = base.CurveWeights(name="TestCurveWeights", geomNode="BASE", attrNode = "pSphere1", projectionMesh="pPlane1", weightNames=["L_innerLR", "L_outerLR"], outWeightStackNode="TestWeights")
# curveWeights.create()


def createBoth():
    return

#==================Base Class for Creating Custom Deformers============
#===============================================================================
#CLASS:         DeformerCommand
#DESCRIPTION:   Creates a deformer
#USAGE:         Select all drivers, then drivens, and run, or set args in this order
#RETURN:        deformer the self.deformer object will be the created deformer
#AUTHOR:        Levi Harrison
#DATE:          January 5th, 2019
#Version        1.0.0
#===============================================================================

class Deformer(object):
    def __init__(self,
                 drivers = [],
                 drivens = [],
                 side = "C",
                 name = "deformer",
                 suffix = "NUL",
                 ihi = False,
                 parentOfNewObjects=""
                 ):
        # Args
        self.drivers = drivers
        self.drivens = drivens
        self.side = side
        self.name = name
        self.suffix = suffix
        self.ihi = ihi
        self.parentOfNewObjects = ihi

        self.create()

    def checkArgs(self):
        return
    
    def getShapes(self):
        return

    def getArgsBySelection(self):
        return

    def getShape(self, mayaObject):
        """ Assumes you only have 1 shape per transform """
        return cmds.listRelatives(mayaObject, shapes = True)[0]

    def getBaseName(self, name):
        """
        based on "L_name_TYP" naming config, but works if not
        """
        if "_" in name:
            name = self.driverSurface.split("_")
            if len(name) >= 3:
                return name[0] + '_' + name[1] + 'Base_' + name[2]
        return name + 'Base'

    def createGeo(self):
        return

    def duplicateMeshClean(self, mesh, vis=False):
        """ Makes sure to duplicate a mesh cleanly, you still need to be careful of deformations """
        meshShape = cmds.ls(mesh, dag = 1, g = 1)[0]
        newTransform = cmds.createNode("transform", n = mesh + "Base")
        newMesh = cmds.createNode("mesh", n = mesh + "BaseShape", p = newTransform)
        cmds.connectAttr(meshShape + ".outMesh", newMesh + ".inMesh")
        cmds.refresh()
        cmds.disconnectAttr(meshShape + ".outMesh", newMesh + ".inMesh")
        if self.parentOfNewObjects:
            cmds.parent(newTransform, self.parentOfNewObjects)
        if not vis:
            cmds.setAttr(newTransform + ".visibility", 0)
        return newTransform, newMesh

    def getTransformData(self):
        return

    def createDeformer(self):
        return
    
    def createAttributes(self):
        return

    def connectDeformer(self):
        return
    
    def cleanup(self):
        return

    def create(self):
        self.checkArgs()
        self.getShapes()
        self.createGeo()
        self.getTransformData()
        self.createDeformer()
        self.createAttributes()
        self.connectDeformer()
        self.cleanup()
