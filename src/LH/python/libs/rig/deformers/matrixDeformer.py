from maya import cmds
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
from rig.deformers import utils as deformerUtils
from rig.deformers import base
reload(base)

def createTestMatrixDeformer():
    deformMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2, sx=100, sy=100,  n="deformMesh")[0]
    deformer = cmds.deformer(deformMesh, type="LHMatrixDeformer")[0]
    for idx in range(20):
        locator = cmds.spaceLocator(n="test_{0:02}".format(idx))[0]
        locatorBase = cmds.spaceLocator(n="testBase_{0:02}".format(idx))[0]
        cmds.connectAttr("{0}.worldMatrix".format(locator), "{0}.inputs[{1}].matrix".format(deformer, idx))
        cmds.connectAttr("{0}.worldMatrix".format(locatorBase), "{0}.inputs[{1}].matrixBase".format(deformer, idx))
        weightMap = weightMapUtils.createWeightMapOnSingleObject(deformMesh, "testWeights_{0:02}".format(idx), defaultValue=1.0, addAttr=True)
        cmds.connectAttr(weightMap, "{0}.inputs[{1}].matrixWeight".format(deformer, idx))

class MatrixDeformer(base.Deformer):
    def __init__(self,
                    name="testMatrixDeformer",
                    deformerType="LHMatrixDeformer",
                    geoToDeform="",
                    parent="",
                    centerToParent=False,
                    rotationTranforms=[],
                    translations = [],
                    rotations = [],
                    scales = [],
                    addAtIndex=0,
                    numToAdd=1,
                    locatorName="test",
                    curveWeightsNode="",
                    curveWeightsConnectionIdx=0,
                    # locations=[],
                    hide=True,
                 **kw):
        super(MatrixDeformer, self).__init__(**kw)
        self.name = name
        self.addAtIndex = addAtIndex
        self.deformerType = deformerType
        self.geoToDeform = geoToDeform
        self.parent = parent
        self.centerToParent = centerToParent
        self.rotationTranforms = rotationTranforms
        self.translations = translations
        self.rotations = rotations
        self.scales = scales
        self.numToAdd = numToAdd
        self.locatorName = locatorName
        self.curveWeightsNode = curveWeightsNode
        self.curveWeightsConnectionIdx = curveWeightsConnectionIdx
        # self.locations = locations
        self.hide = hide
        self.deformer = ""
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.matrixBuffers = []
        self.deformerType = "LHMatrixDeformer"

    def getDeformer(self):
        if cmds.objExists(self.name):
            self.deformer = self.name
            return
        self.deformer = cmds.deformer(self.geoToDeform, type=self.deformerType, n=self.name, foc=True)[0]

    def getNodes(self):
        self.matrixNodes = []
        self.matrixBaseNodes = []
        for idx in range(self.numToAdd):
            currParent = self.parent
            if type(self.parent) == list:
                currParent = self.parent[idx]
            idx = idx + self.addAtIndex

            bufferName = "{0}{1:02}_BUF".format(self.locatorName, idx)

            if not bufferName in self.matrixBuffers:
                self.matrixBuffers.append(bufferName)

            if not cmds.objExists(bufferName):
                cmds.createNode("transform", n=bufferName, p=currParent)

            matrixNodeName = "{0}{1:02}_LOC".format(self.locatorName, idx)
            matrixBaseNodeName = "{0}Base{1:02}_LOC".format(self.locatorName, idx)
            if not cmds.objExists(matrixNodeName):
                loc = cmds.spaceLocator(name="{0}{1:02}_LOC".format(self.locatorName, idx))[0]
                self.matrixNodes.append(loc)
                if cmds.objExists(bufferName):
                    cmds.parent(loc, bufferName)
            else:
                self.matrixNodes.append(matrixNodeName)
            if not cmds.objExists(matrixBaseNodeName):
                loc = cmds.spaceLocator(name="{0}Base{1:02}_LOC".format(self.locatorName, idx))[0]
                self.matrixBaseNodes.append(loc)
                if cmds.objExists(bufferName):
                    cmds.parent(loc, bufferName)
            else:
                self.matrixBaseNodes.append(matrixBaseNodeName)



    def setDefaultLocations(self):
        for idx in range(len(self.matrixBuffers)):
            if len(self.translations)-1 >= idx:
                misc.move(self.matrixBuffers[idx], translate=self.translations[idx])
                # misc.move(self.matrixBaseNodes[idx], translate=self.translations[idx])
            if len(self.rotations)-1 >= idx:
                misc.move(self.matrixBuffers[idx], rotate=self.rotations[idx])
                # misc.move(self.matrixBaseNodes[idx], rotate=self.rotations[idx])
            if len(self.scales)-1 >= idx:
                misc.move(self.matrixBuffers[idx], scale=self.scales[idx])
                # misc.move(self.matrixBaseNodes[idx], scale=self.scales[idx])

        # if not self.locations:
        #     return
        # for idx, location in enumerate(self.locations):
        #     idx = idx + self.addAtIndex
        #     locator = "{0}{1:02}_LOC".format(self.locatorName, idx)
        #     # cmds.xform(locator,  ws=True,  t=location)
        #     misc.move(locator, location)
        #     locatorBase = "{0}Base{1:02}_LOC".format(self.locatorName, idx)
        #     misc.move(locatorBase, location)

            # cmds.xform(locatorBase,  ws=True,  t=location)

        
    def connectDeformer(self):
        for idx in range(self.numToAdd):
            elemIndex = idx + self.addAtIndex
            cmds.connectAttr("{0}.worldMatrix".format(self.matrixNodes[idx]), "{0}.inputs[{1}].matrix".format(self.deformer, elemIndex))
            cmds.connectAttr("{0}.worldMatrix".format(self.matrixBaseNodes[idx]), "{0}.inputs[{1}].matrixBase".format(self.deformer, elemIndex))
            if cmds.objExists(self.curveWeightsNode):
                curveWeightsIndex = idx + self.curveWeightsConnectionIdx
                weightMap = "{0}.outDoubleWeights[{1}].outWeightsDoubleArray".format(self.curveWeightsNode, curveWeightsIndex)
                cmds.connectAttr(weightMap, "{0}.inputs[{1}].matrixWeight".format(self.deformer, elemIndex))
            if self.rotationTranforms:
                cmds.connectAttr("{0}.rotate".format(self.rotationTranforms[idx]), "{0}.rotate".format(self.matrixNodes[idx]))
                # cmds.connectAttr( "{0}.rotate".format(self.rotationTranforms[idx]), "{0}.rotate".format(self.matrixBaseNodes[idx]))

    def cleanup(self):
        for node in self.matrixNodes + self.matrixBaseNodes:
            if self.hide:
                cmds.setAttr(node + ".visibility", 0)
            if not self.centerToParent:
                continue
            if cmds.listRelatives(node, p=True):
                cmds.xform(node, os=True, t=[0,0,0], ro=[0,0,0])
        # for idx in range(len(self.matrixNodes)):
        #     if len(self.translations)-1 >= idx:
        #         misc.move(self.matrixNodes[idx], translate=self.translations[idx])
        #         misc.move(self.matrixBaseNodes[idx], translate=self.translations[idx])
        #     if len(self.rotations)-1 >= idx:
        #         misc.move(self.matrixNodes[idx], rotate=self.rotations[idx])
        #         misc.move(self.matrixBaseNodes[idx], rotate=self.rotations[idx])
        #     if len(self.scales)-1 >= idx:
        #         misc.move(self.matrixNodes[idx], scale=self.scales[idx])
        #         misc.move(self.matrixBaseNodes[idx], scale=self.scales[idx])

# def move(transform=None, translate=None, rotate=None, scale=None):



    def create(self):
        self.getDeformer()
        self.getNodes()
        self.setDefaultLocations()
        self.connectDeformer()
        self.cleanup()




