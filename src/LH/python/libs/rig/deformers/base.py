from maya import cmds
from rig.utils import weightMapUtils
reload(weightMapUtils)

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
                 inEnumVals = [],
                 inEnumAttrs = [],
                 enumNames = [],
                 nodeKDoublePlugMap="",
                 nodeFloatPlugMap="",
                 nodeEnumPlugMap="",
                 outKDoubleArrayAttr =""):

        self.nodeType = nodeType
        self.name = name
        self.parent = parent

        self.attrNode = attrNode
        self.floatNode = floatNode
        self.enumNode = enumNode
        self.kDoubleArrayNode = kDoubleArrayNode
        for node in ["floatNode", "enumNode"]:
            if self.attrNode and not getattr(self, node):
                setattr(self, node, self.attrNode)

        self.inKDoubleArrayAttrs = inKDoubleArrayAttrs
        self.inFloatAttrs = inFloatAttrs
        self.inEnumAttrs = inEnumAttrs
        self.inEnumVals = inEnumVals
        self.enumNames = enumNames
        self.outKDoubleArrayAttr = outKDoubleArrayAttr
        self.floatPlugNames = []
        self.kDoubleArrayPlugNames = []
        self.enumPlugNames = []
        self.inputConnectionMap = {}
        self.outputConnectionMap = {}
        self.doubleArrayAttrs = []
        self.floatAttrs = []
        self.enumAttrs = []
        self.nodeKDoublePlugMap = nodeKDoublePlugMap
        self.nodeFloatPlugMap = nodeFloatPlugMap
        self.nodeEnumPlugMap = nodeEnumPlugMap
        # Where to put all of the new attributes.  If you want them all on one node just use the attrNode arg

        # super(Node, self).__init__(**kw)

    def getNode(self):
        if cmds.objExists(self.name):
            self.node = self.name
            return
        self.node = cmds.createNode(self.nodeType, n=self.name, p=self.parent)

    def attrCheck(self, node, attrs, attrType=None, enumName=None, k=False, weightmap=False):
        if not node:
            return
        retAttrs = []
        for attr in attrs:
            # print node, attr
            fullName = node + "." + attr
            if cmds.objExists(fullName):
                retAttrs.append(fullName)
                continue
            if weightmap:
                weightMapUtils.createWeightMapOnObject(node, attr)
            else:
                if attrType == "enum":
                    cmds.addAttr(node, at=attrType, ln=attr, enumName=enumName, k=k)
                else:
                    cmds.addAttr(node, at=attrType, ln=attr, k=k)

            retAttrs.append(fullName)
        return retAttrs

    def getAttrs(self):
        # For each inWeightAttrs check if the attribute exists on the geometry
        self.doubleArrayAttrs = self.attrCheck(node=self.kDoubleArrayNode,
                                               attrs=self.inKDoubleArrayAttrs,
                                               attrType=None,
                                               weightmap=True)
        self.floatAttrs = self.attrCheck(node=self.floatNode,
                                         attrs=self.inFloatAttrs,
                                         attrType="float",
                                         k=True)
        self.enumAttrs = self.attrCheck(node=self.enumNode,
                                        attrs=self.inEnumAttrs,
                                        attrType="enum",
                                        enumName=self.enumNames,
                                        k=True)
    @staticmethod
    def extractNodeAttr(fullAttrName):
        names = fullAttrName.split(".")
        node, attr = names[0], names[-1]
        return node, attr

    def setDefaultAttrs(self):
        return

    def initInputConnections(self):
        return

    def inputMultiConnections(self):
        """
        For multi index connections only
        """
        for attributeMap in self.inputConnectionMap.keys():
            for idx, attr in enumerate(self.inputConnectionMap[attributeMap]):
                self.connectMultiInputViaMap(attr, attributeMap, idx)

    def connectMultiInputViaMap(self, attr, inputAttrMap, idx):
        cmds.connectAttr(attr, inputAttrMap.format(self.node, idx), f=True)

    def connectOutputViaMap(self, outputAttrMap, attr):
        cmds.connectAttr(outputAttrMap.format(self.node), attr, f=True)

    def initOutputConnections(self):
        return

    def outputConnections(self):
        for outputAttrMap in self.outputConnectionMap.keys():
            self.connectOutputViaMap(outputAttrMap, self.outputConnectionMap[outputAttrMap])

    def create(self):
        self.getNode()
        self.getAttrs()
        self.setDefaultAttrs()
        self.initInputConnections()
        self.inputMultiConnections()
        self.initOutputConnections()
        self.outputConnections()

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

    def initInputConnections(self):
        self.inputConnectionMap = {"{0}.inputs[{1}].inputWeights": self.doubleArrayAttrs,
                                   "{0}.inputs[{1}].factor": self.floatAttrs,
                                   "{0}.inputs[{1}].operation": self.enumAttrs}

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

    # def find(self):
    #     pass
    #

class CurveWeights(Node):
    def __init__(self,
                 inMesh = None,
                 projectionMesh = None,
                 membershipWeights = None,
                 inUWeightCurves = [],
                 inUFalloffCurves=[],
                 inVWeightCurves = [],
                 inVFalloffCurves = [],
                 outWeightAttrs=[],
                 **kw):
        self.nodeType = "LHCurveWeightNode"
        super(CurveWeights, self).__init__(**kw)

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
