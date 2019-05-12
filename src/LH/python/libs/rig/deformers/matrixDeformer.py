from maya import cmds
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
from rig.deformers import utils as deformerUtils
from rig.deformers import base
reload(base)
from rig.rigComponents import simpleton
reload(simpleton)
from rig.rigComponents import meshRivetCtrl
reload(meshRivetCtrl)
from rig.utils import exportUtils
reload(exportUtils)
from rig.rigComponents import elements
reload(elements)

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
                    geoToConstrainMesh = "",
                    ctrlName = "",
                    manualLocatorNames=[],
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
                    reverseDeformerOrder = False,
                    connectTranslate=True,
                    connectRotate=True,
                    connectScale=True,
                    # 0 is simpleton, 1 is rivet control
                    controlType = 0,
                    controlAutoOrientMesh="",
                    customControlShapes = [],
                    guide = False,
                    # inherited args
                    # orderFrontOfChain=True,
                    # orderParallel=False,
                    # orderBefore=False,
                    # orderAfter=False,

                 **kw):
        super(MatrixDeformer, self).__init__(**kw)
        self.name = name
        self.addAtIndex = addAtIndex
        self.ctrlName = ctrlName
        self.manualLocatorNames = manualLocatorNames
        self.deformerType = deformerType
        self.geoToConstrainMesh = geoToConstrainMesh
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
        self.reverseDeformerOrder = reverseDeformerOrder
        self.connectTranslate = connectTranslate
        self.connectRotate = connectRotate
        self.connectScale = connectScale
        self.controlType = controlType
        self.controlAutoOrientMesh = controlAutoOrientMesh
        self.customControlShapes = customControlShapes
        self.guide = guide

        if not self.numToAdd and self.manualLocatorNames:
            self.numToAdd = len(self.manualLocatorNames)

        self.deformer = ""
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.matrixBuffers = []
        self.controls = []

    # def getDeformer(self):
    #     if cmds.objExists(self.name):
    #         self.deformer = self.name
    #         return
    #     self.deformer = cmds.deformer(self.geoToDeform, type=self.deformerType, n=self.name, foc=True)[0]

    def getNodes(self):
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.deformerParent = cmds.createNode("transform", name = self.name + "_DEFORM", parent = self.rigParent)
        self.locatorNames = self.manualLocatorNames
        if not self.manualLocatorNames:
            self.locatorNames = deformerUtils.nameBasedOnRange(count=self.numToAdd, name=self.locatorName, suffixSeperator="")
        for idx in range(self.numToAdd):
            locatorName = self.locatorNames[idx]
            if not self.autoNameWithSide and not self.manualLocatorNames:
                locatorName = self.locatorName
            currParent = self.deformerParent
            # if type(self.controlParent) == list:
            #     currParent = self.deformerParent[idx]
            idx = idx + self.addAtIndex

            bufferFormatName = "{0}{1:02}_BUF"
            if self.manualLocatorNames:
                bufferFormatName = "{0}_BUF"


            bufferName = bufferFormatName.format(locatorName, idx)

            if not bufferName in self.matrixBuffers:
                self.matrixBuffers.append(bufferName)

            if not cmds.objExists(bufferName):
                cmds.createNode("transform", n=bufferName, p=currParent)

            # Sometimes the name has to be numbered, but sometimes you have an individual name for every node...
            locatorFormatName ="{0}{1:02}_LOC"
            locatorBaseFormatName = "{0}Base{1:02}_LOC"
            if self.manualLocatorNames:
                locatorFormatName ="{0}_LOC"
                locatorBaseFormatName = "{0}Base_LOC"


            matrixNodeName = locatorFormatName.format(locatorName, idx)
            matrixBaseNodeName = locatorBaseFormatName.format(locatorName, idx)


            if not cmds.objExists(matrixNodeName):
                loc = cmds.spaceLocator(name=locatorFormatName.format(locatorName, idx))[0]
                self.matrixNodes.append(loc)
                if cmds.objExists(bufferName):
                    cmds.parent(loc, bufferName)
            else:
                self.matrixNodes.append(matrixNodeName)
            if not cmds.objExists(matrixBaseNodeName):
                loc = cmds.spaceLocator(name=locatorBaseFormatName.format(locatorName, idx))[0]
                self.matrixBaseNodes.append(loc)
                if cmds.objExists(bufferName):
                    cmds.parent(loc, bufferName)
            else:
                self.matrixBaseNodes.append(matrixBaseNodeName)
        self.create_guides()

    def create_guides(self):
        self.guide_shapes = []
        for buffer in self.matrixBuffers:
            guide_name = "{0}_SHP".format(buffer)
            # if it exists get it
            if cmds.objExists(guide_name):
                self.guide_shapes.append(guide_name)
                continue
            # if it does not exist, create it
            guideShape = exportUtils.create_curve_2(elements.sphereSmall, guide_name, buffer)
            self.guide_shapes.append(guide_name)
            misc.tag_guide(guide_name)
            # Set the default visibility of the guide
            if not self.guide:
                cmds.setAttr(guide_name + ".v", 0)


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
        if self.reverseDeformerOrder:
            cmds.setAttr(self.deformer + ".reverseDeformationOrder", 1)

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

        if self.ctrlName and not self.manualLocatorNames and not type(self.ctrlName) == list:
            locatorNames = deformerUtils.nameBasedOnRange(count=self.numToAdd, name=self.ctrlName, suffixSeperator="")

        if type(self.ctrlName) == list:
            locatorNames = self.ctrlName


        # if there is only 1 control parent, make that the parent for every item in the array
        if type(self.controlParent) != list:
            self.controlParent = [self.controlParent for x in range(len(self.matrixNodes))]

        for idx, node in enumerate(self.matrixNodes):
            locatorName = locatorNames[idx]
            if not self.autoNameWithSide and not self.manualLocatorNames:
                locatorName = self.locatorName
            side, name = misc.getNameSide(locatorName)
            controlName = "{0}_{1}MatrixDef_CTL".format(side, name)
            
            controlShape = self.controlShapeDict
            if self.customControlShapes and len(self.customControlShapes) == len(self.matrixNodes):
                controlShape = self.customControlShapes[controlName]
            # if a name exists in self.customControlShapes exract it now and use that control shape dict instead of the default
            # customControlShapes

            if not cmds.objExists(controlName):
                if self.controlType == 0:
                    ctrl = simpleton.Component(side=side,
                                            name=name+"MatrixDef", 
                                            parent=self.controlParent[idx],
                                            translate = translations[idx],
                                            rotate = rotations[idx],
                                            scale = scales[idx],
                                            offset = self.offset,
                                            size=self.size,
                                            curveData = controlShape,
                                            )
                elif self.controlType == 1:
                    ctrl = meshRivetCtrl.Component(name = name+"MatrixDef", 
                                                        side=side,
                                                        speedTxDefault=1,
                                                        speedTyDefault=1,
                                                        speedTzDefault=1,
                                                        parent=self.controlParent[idx],
                                                        curveData=controlShape,
                                                        mesh = self.geoToDeform,
                                                        translate = translations[idx],
                                                        rotate = rotations[idx],
                                                        normalConstraintPatch=self.controlAutoOrientMesh,
                                                        selection=False,
                                                        mirror=False,
                                                        size=self.size,
                                                        offset = self.offset,
                                                        # orient = self.controlShapeOrient,
                                                        # shapeScale = self.controlShapeScale,
                                                        lockAttrs = [],
                                                        )
                ctrl.create()
                controlName = ctrl.ctrl

            if not controlName in self.controls:
                self.controls.append(controlName)

    def connectCtrls(self):
        if not self.doCreateCtrls:
            return
        for idx, ctrl in enumerate(self.controls):
            if self.connectTranslate:
                cmds.connectAttr(ctrl + ".tOut", self.matrixNodes[idx] + ".translate", f=True)
            if self.connectRotate:
                cmds.connectAttr(ctrl + ".rotate", self.matrixNodes[idx] + ".rotate", f=True)
            if self.connectScale:
                cmds.connectAttr(ctrl + ".scale", self.matrixNodes[idx] + ".scale", f=True)
        self.connect_control_guides()
        # Geo constraint
        # if not self.geoToConstrainMesh:
        #     return
        # for idx in range(len(self.matrixBuffers)):
        #     side, name = misc.getNameSide(self.matrixBuffers[idx])
        #     misc.geoConstraint(driverMesh = self.geoToConstrainMesh,
        #                        driven = self.matrixBuffers[idx],
        #                        parent = self.rigParent,
        #                        name = "{0}_{1}_GCS".format(side, name),
        #                        translate=True,
        #                        rotate=True,
        #                        scale=False,
        #                        offsetBuffer =None,
        #                        maintainOffsetT=False,
        #                        maintainOffsetR=False, maintainOffsetS=True)

    def connect_control_guides(self):
        # Connect guides
        for idx, guide in enumerate(self.guide_shapes):
            current_ctrl = self.controls[idx]
            if not cmds.objExists(current_ctrl + ".guide" ):
                cmds.addAttr(current_ctrl, ln = "guide", at = "message")
                cmds.connectAttr(guide + ".message", current_ctrl + ".guide")

    def cleanup(self):
        for node in self.matrixNodes + self.matrixBaseNodes:
            if self.hide:
                cmds.setAttr(node + ".visibility", 0)
            if not self.centerToParent:
                continue
            if cmds.listRelatives(node, p=True):
                cmds.xform(node, os=True, t=[0,0,0], ro=[0,0,0])



