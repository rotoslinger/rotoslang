from maya import cmds
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
from rig.deformers import utils as deformerUtils

def createTestMatrixDeformer():
    deformMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2, sx=30, sy=30,  n="deformMesh")[0]
    deformer = cmds.deformer(deformMesh, type="LHMatrixDeformer")[0]
    for idx in range(2):
        locator = cmds.spaceLocator(n="test_{0:02}".format(idx))[0]
        locatorBase = cmds.spaceLocator(n="testBase_{0:02}".format(idx))[0]
        cmds.connectAttr("{0}.worldMatrix".format(locator), "{0}.inputs[{1}].matrix".format(deformer, idx))
        cmds.connectAttr("{0}.worldMatrix".format(locatorBase), "{0}.inputs[{1}].matrixBase".format(deformer, idx))
        weightMap = weightMapUtils.createWeightMapOnSingleObject(deformMesh, "testWeights_{0:02}".format(idx), defaultValue=1.0, addAttr=True)
        cmds.connectAttr(weightMap, "{0}.inputs[{1}].matrixWeight".format(deformer, idx))

class MatrixDeformer(object):
    def __init__(self,
                    name="testMatrixDeformer",
                    deformerType="LHMatrixDeformer",
                    geoToDeform="",
                    parent="",
                    addAtIndex=0,
                    numToAdd=1,
                    locatorName="test",
                    curveWeightsNode="",
                    curveWeightsConnectionIdx=0,
                    locations=[],
                 **kw):
        super(MatrixDeformer, self).__init__(**kw)
        self.name = name
        self.addAtIndex = addAtIndex
        self.deformerType = deformerType
        self.geoToDeform = geoToDeform
        self.parent = parent
        self.numToAdd = numToAdd
        self.locatorName = locatorName
        self.curveWeightsNode = curveWeightsNode
        self.curveWeightsConnectionIdx = curveWeightsConnectionIdx
        self.locations = locations
        self.deformer = ""
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.deformerType = "LHMatrixDeformer"

    def getDeformer(self):
        if cmds.objExists(self.name):
            self.deformer = self.name
            return
        self.deformer = cmds.deformer(self.geoToDeform, type=self.deformerType, n=self.name)[0]

    def getNodes(self):
        self.matrixNodes = []
        self.matrixBaseNodes = []
        for idx in range(self.numToAdd):
            idx = idx + self.addAtIndex
            matrixNodeName = "{0}{1:02}_LOC".format(self.locatorName, idx)
            matrixBaseNodeName = "{0}Base{1:02}_LOC".format(self.locatorName, idx)
            if not cmds.objExists(matrixNodeName):
                loc = cmds.spaceLocator(name="{0}{1:02}_LOC".format(self.locatorName, idx))[0]
                self.matrixNodes.append(loc)
                if cmds.objExists(self.parent):
                    cmds.parent(loc, self.parent)
            else:
                self.matrixNodes.append(matrixNodeName)
            if not cmds.objExists(matrixBaseNodeName):
                loc = cmds.spaceLocator(name="{0}Base{1:02}_LOC".format(self.locatorName, idx))[0]
                self.matrixBaseNodes.append(loc)
                if cmds.objExists(self.parent):
                    cmds.parent(loc, self.parent)
            else:
                self.matrixBaseNodes.append(matrixBaseNodeName)

    def setDefaultLocations(self):
        if not self.locations:
            return
        for idx, location in enumerate(self.locations):
            idx = idx + self.addAtIndex
            locator = "{0}{1:02}_LOC".format(self.locatorName, idx)
            cmds.xform(locator,  ws=True,  t=location)
            locatorBase = "{0}Base{1:02}_LOC".format(self.locatorName, idx)
            cmds.xform(locatorBase,  ws=True,  t=location)

        
    def connectDeformer(self):
        for idx in range(self.numToAdd):
            elemIndex = idx + self.addAtIndex
            cmds.connectAttr("{0}.worldMatrix".format(self.matrixNodes[idx]), "{0}.inputs[{1}].matrix".format(self.deformer, elemIndex))
            cmds.connectAttr("{0}.worldMatrix".format(self.matrixBaseNodes[idx]), "{0}.inputs[{1}].matrixBase".format(self.deformer, elemIndex))
            if cmds.objExists(self.curveWeightsNode):
                curveWeightsIndex = idx + self.curveWeightsConnectionIdx
                weightMap = "{0}.outDoubleWeights[{1}].outWeightsDoubleArray".format(self.curveWeightsNode, curveWeightsIndex)
                cmds.connectAttr(weightMap, "{0}.inputs[{1}].matrixWeight".format(self.deformer, elemIndex))

    def create(self):
        self.getDeformer()
        self.getNodes()
        self.setDefaultLocations()
        self.connectDeformer()




        # def createMatrixDeformer(name="test", addAtIndex=0):
    # deformMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2, sx=30, sy=30,  n="deformMesh")[0]
    # deformer = cmds.deformer(deformMesh, type="LHMatrixDeformer")[0]
    # for idx in range(2):
    #     locator = cmds.spaceLocator(n="test_{0:02}".format(idx))[0]
    #     locatorBase = cmds.spaceLocator(n="testBase_{0:02}".format(idx))[0]
    #     cmds.connectAttr("{0}.worldMatrix".format(locator), "{0}.inputs[{1}].matrix".format(deformer, idx))
    #     cmds.connectAttr("{0}.worldMatrix".format(locatorBase), "{0}.inputs[{1}].matrixBase".format(deformer, idx))
    #     weightMap = weightMapUtils.createWeightMapOnSingleObject(deformMesh, "testWeights_{0:02}".format(idx), defaultValue=1.0, addAttr=True)
    #     cmds.connectAttr(weightMap, "{0}.inputs[{1}].matrixWeight".format(deformer, idx))
