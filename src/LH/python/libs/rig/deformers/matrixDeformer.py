from maya import cmds
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
from rig.deformers import utils as deformerUtils
from rig.deformers import base
reload(base)
from rig.rigComponents import simpleton
reload(simpleton)

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
                    ctrlName = "",
                    geoToDeform="",
                    controlParent=[],
                    rigParent="",
                    centerToParent=False,
                    doCreateCtrls=True,
                    controlShapeDict=None,
                    rotationTranforms=[],
                    translations = [],
                    rotations = [],
                    scales = [],
                    offset = [0,0,0],
                    posOffset = [0,0,0],
                    size = 1,
                    addAtIndex=0,
                    numToAdd=1,
                    locatorName="test",
                    curveWeightsNode="",
                    curveWeightsConnectionIdx=0,
                    autoNameWithSide=True,
                    hide=True,
                 **kw):
        super(MatrixDeformer, self).__init__(**kw)
        self.name = name
        self.addAtIndex = addAtIndex
        self.ctrlName = ctrlName
        self.deformerType = deformerType
        self.geoToDeform = geoToDeform
        self.controlParent = controlParent
        self.rigParent = rigParent
        self.doCreateCtrls = doCreateCtrls
        self.controlShapeDict = controlShapeDict
        self.centerToParent = centerToParent
        self.rotationTranforms = rotationTranforms
        self.translations = translations
        self.rotations = rotations
        self.scales = scales
        self.offset = offset
        self.posOffset = posOffset
        self.size = size
        self.numToAdd = numToAdd
        self.locatorName = locatorName
        self.curveWeightsNode = curveWeightsNode
        self.curveWeightsConnectionIdx = curveWeightsConnectionIdx
        self.autoNameWithSide = autoNameWithSide
        self.hide = hide
        self.deformer = ""
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.matrixBuffers = []
        self.controls = []

    def getDeformer(self):
        if cmds.objExists(self.name):
            self.deformer = self.name
            return
        self.deformer = cmds.deformer(self.geoToDeform, type=self.deformerType, n=self.name, foc=True)[0]

    def getNodes(self):
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.deformerParent = cmds.createNode("transform", name = self.name + "_DEFORM", parent = self.rigParent)
        self.locatorNames = deformerUtils.nameBasedOnRange(count=self.numToAdd, name=self.locatorName, suffixSeperator="")
        for idx in range(self.numToAdd):
            locatorName = self.locatorNames[idx]
            if not self.autoNameWithSide:
                locatorName = self.locatorName
            currParent = self.deformerParent
            # if type(self.controlParent) == list:
            #     currParent = self.deformerParent[idx]
            idx = idx + self.addAtIndex

            bufferName = "{0}{1:02}_BUF".format(locatorName, idx)

            if not bufferName in self.matrixBuffers:
                self.matrixBuffers.append(bufferName)

            if not cmds.objExists(bufferName):
                cmds.createNode("transform", n=bufferName, p=currParent)

            matrixNodeName = "{0}{1:02}_LOC".format(locatorName, idx)
            matrixBaseNodeName = "{0}Base{1:02}_LOC".format(locatorName, idx)
            if not cmds.objExists(matrixNodeName):
                loc = cmds.spaceLocator(name="{0}{1:02}_LOC".format(locatorName, idx))[0]
                self.matrixNodes.append(loc)
                if cmds.objExists(bufferName):
                    cmds.parent(loc, bufferName)
            else:
                self.matrixNodes.append(matrixNodeName)
            if not cmds.objExists(matrixBaseNodeName):
                loc = cmds.spaceLocator(name="{0}Base{1:02}_LOC".format(locatorName, idx))[0]
                self.matrixBaseNodes.append(loc)
                if cmds.objExists(bufferName):
                    cmds.parent(loc, bufferName)
            else:
                self.matrixBaseNodes.append(matrixBaseNodeName)

    def setDefaults(self):
        for idx in range(len(self.matrixBuffers)):
            if len(self.translations)-1 >= idx:
                misc.move(self.matrixBuffers[idx], translate=self.translations[idx])
            if len(self.rotations)-1 >= idx:
                misc.move(self.matrixBuffers[idx], rotate=self.rotations[idx])
            if len(self.scales)-1 >= idx:
                misc.move(self.matrixBuffers[idx], scale=self.scales[idx])
        
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

    def createCtrls(self):
        if not self.doCreateCtrls:
            return

        translations = [[0,0,0] for x in range(len(self.matrixNodes))]
        rotations = [[0,0,0] for x in range(len(self.matrixNodes))]
        scales = [[1,1,1] for x in range(len(self.matrixNodes))]
        
        if len(self.translations) == len(self.matrixNodes):
            translations = self.translations
        if len(self.rotations) == len(self.matrixNodes):
            rotations = self.rotations
        if len(self.scales) == len(self.matrixNodes):
            scales = self.scales

        locatorNames = self.locatorNames
        if self.ctrlName:
            locatorNames = deformerUtils.nameBasedOnRange(count=self.numToAdd, name=self.ctrlName, suffixSeperator="")

        for idx, node in enumerate(self.matrixNodes):
            locatorName = locatorNames[idx]
            if not self.autoNameWithSide:
                locatorName = self.locatorName
            side, name = misc.getNameSide(locatorName)
            controlName = "{0}_{1}MatrixDef_CTL".format(side, name)
            if not cmds.objExists(controlName):
                ctrl = simpleton.Component(side=side,
                                        name=name+"MatrixDef",
                                        parent=self.controlParent[idx],
                                        translate = translations[idx],
                                        rotate = rotations[idx],
                                        scale = scales[idx],
                                        offset = self.offset,
                                        size=self.size,
                                        curveData = self.controlShapeDict,
                                        )  
                ctrl.create()
                controlName = ctrl.ctrl           
            if not controlName in self.controls:
                self.controls.append(controlName)

    def connectCtrls(self):
        if not self.doCreateCtrls:
            return
        for idx, ctrl in enumerate(self.controls):
            cmds.connectAttr(ctrl + ".translate", self.matrixNodes[idx] + ".translate", f=True)
            cmds.connectAttr(ctrl + ".rotate", self.matrixNodes[idx] + ".rotate", f=True)
            cmds.connectAttr(ctrl + ".scale", self.matrixNodes[idx] + ".scale", f=True)

    def cleanup(self):
        for node in self.matrixNodes + self.matrixBaseNodes:
            if self.hide:
                cmds.setAttr(node + ".visibility", 0)
            if not self.centerToParent:
                continue
            if cmds.listRelatives(node, p=True):
                cmds.xform(node, os=True, t=[0,0,0], ro=[0,0,0])



