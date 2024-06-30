from maya import cmds

from rig_2.name import utils as name_utils
import importlib
importlib.reload(name_utils)
from rig_2.node import utils as node_utils
importlib.reload(node_utils)
from rig_2.attr import utils as attr_utils
importlib.reload(attr_utils)


from rig_2.message import utils as message_utils
importlib.reload(message_utils)
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)

from rig.utils import weightMapUtils, misc
importlib.reload(weightMapUtils)
importlib.reload(misc)
from rig.deformers import utils as deformerUtils
importlib.reload(deformerUtils)
from rig.deformers import base
importlib.reload(base)
from rig.rigComponents import simpleton
importlib.reload(simpleton)
from rig.rigComponents import meshRivetCtrl
importlib.reload(meshRivetCtrl)
from rig.utils import exportUtils
importlib.reload(exportUtils)
from rig.rigComponents import elements
importlib.reload(elements)
from rig_2.shape import nurbscurve

importlib.reload(nurbscurve)
from rig_2.manipulator import elements as manipulator_elements
importlib.reload(manipulator_elements)

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
                 control_rivet_mesh ="",
                 ctrlName = "",
                 position = "",
                 manualLocatorNames=[],
                 manual_weights = False,
                 manual_no_rivet_names = [],
                 manual_constraint_dict = {},
                 type_name = "Trans",
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
                 # name side is when you want to have the ctrls mirrored
                 # for example you have a left eye and a right eye
                 # controls will not be able to be named "L_eye", "C_eye", "R_eye" because you have to make them twice once for each eye
                 # instead they will be named L_leftEye, L_centerEye, L_rightEye and the right controls will be named R_leftEye, R_centerEye, R_rightEye
                 auto_create_name_side=False,
                 auto_create_reverse = False,
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
        self.manual_weights = manual_weights
        self.manual_no_rivet_names = manual_no_rivet_names
        self.manual_constraint_dict = manual_constraint_dict
        self.deformerType = deformerType
        self.control_rivet_mesh = control_rivet_mesh
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
        self.position = position
        self.offset = offset
        self.posOffset = posOffset
        self.size = size
        self.numToAdd = numToAdd
        self.locatorName = locatorName
        self.curveWeightsNode = curveWeightsNode
        self.curveWeightsConnectionIdx = curveWeightsConnectionIdx
        self.autoNameWithSide = autoNameWithSide
        self.auto_create_name_side = auto_create_name_side
        self.auto_create_reverse = auto_create_reverse
        self.type_name = type_name


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

        if not self.control_rivet_mesh:
            self.control_rivet_mesh = self.geoToDeform
        self.weight_map_attrs = []
        


    def getNodes(self):
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.deformerParent = node_utils.get_node_agnostic("transform", name = self.position + self.component_name + self.type_name + "_DEFORM", parent = self.rigParent)
        self.locatorNames = self.manualLocatorNames
        if not self.manualLocatorNames:
            self.locatorNames = name_utils.name_based_on_range(count=self.numToAdd,
                                                               name=self.locatorName,
                                                               suffixSeperator="",
                                                               side_name=self.auto_create_name_side,
                                                               reverse_side=self.auto_create_reverse,
                                                               )
        for idx in range(self.numToAdd):
            locatorName = self.locatorNames[idx]
            if not self.autoNameWithSide and not self.manualLocatorNames:
                locatorName = self.locatorName
            currParent = self.deformerParent
            # if type(self.controlParent) == list:
            #     currParent = self.deformerParent[idx]
            idx = idx + self.addAtIndex

            bufferFormatName = "{0}_BUF"
            if self.manualLocatorNames:
                bufferFormatName = "{0}_BUF"


            bufferName = bufferFormatName.format(locatorName)

            if not bufferName in self.matrixBuffers:
                self.matrixBuffers.append(bufferName)

            if not cmds.objExists(bufferName):
                cmds.createNode("transform", n=bufferName, p=currParent)

            # Sometimes the name has to be numbered, but sometimes you have an individual name for every node...
            locatorFormatName ="{0}_LOC"
            locatorBaseFormatName = "{0}Base_LOC"
            if self.manualLocatorNames:
                locatorFormatName ="{0}_LOC"
                locatorBaseFormatName = "{0}Base_LOC"


            matrixNodeName = locatorFormatName.format(locatorName)
            matrixBaseNodeName = locatorBaseFormatName.format(locatorName)


            if not cmds.objExists(matrixNodeName):
                loc = cmds.spaceLocator(name=locatorFormatName.format(locatorName))[0]
                self.matrixNodes.append(loc)
                if cmds.objExists(bufferName):
                    cmds.parent(loc, bufferName)
            else:
                self.matrixNodes.append(matrixNodeName)
            if not cmds.objExists(matrixBaseNodeName):
                loc = cmds.spaceLocator(name=locatorBaseFormatName.format(locatorName))[0]
                self.matrixBaseNodes.append(loc)
                if cmds.objExists(bufferName):
                    cmds.parent(loc, bufferName)
            else:
                self.matrixBaseNodes.append(matrixBaseNodeName)
        self.create_guides()


    def getAttrs(self):
        if not self.manual_weights or not self.manualLocatorNames:
            return
        self.weight_map_attrs = []
        for name in self.manualLocatorNames:
            self.weight_map_attrs.append(attr_utils.get_attr(node=self.geoToDeform,
                                                             attr=name + "Weights",
                                                             weightmap=True))

        
    def create_guides(self):
        self.guide_shapes = []
        for buffer in self.matrixBuffers:
            guide_name = "{0}_SHP".format(buffer)
            # if it exists get it
            if cmds.objExists(guide_name):
                self.guide_shapes.append(guide_name)
                continue
            # if it does not exist, create it
            # sphere_medium
            # guideShape = exportUtils.create_curve_2(elements.sphereSmall, guide_name, buffer)
            # guideShape = exportUtils.create_curve_2(elements.sphereSmall, guide_name, buffer)
            guide_transform, guideShape = nurbscurve.create_curve(manipulator_elements.sphere_medium,
                                                                  buffer,
                                                                  buffer,
                                                                  transform_suffix=None,
                                                                  check_existing=False,
                                                                  outliner_color = False,
                                                                  color = False,
                                                                  shape_name = buffer)


            self.guide_shapes.append(guideShape[0])
            tag_utils.tag_guide(guide_transform)
            tag_utils.tag_guide_shape(guideShape[0])
            tag_utils.create_component_tag(guide_transform, self.component_name)
            tag_utils.create_component_tag(guideShape[0], self.component_name)
            # Set the default visibility of the guide
            if not self.guide:
                cmds.setAttr(guideShape[0] + ".v", 0)




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
        self.connect_manual_name_weights()

    def connect_manual_name_weights(self):
        if not self.manual_weights or not self.manualLocatorNames:
            return
        for idx, attr in enumerate(self.weight_map_attrs):
            cmds.connectAttr(attr, "{0}.inputs[{1}].matrixWeight".format(self.deformer, idx))



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
            locatorNames = name_utils.name_based_on_range(count=self.numToAdd,
                                                          name=self.ctrlName,
                                                          suffixSeperator="",
                                                          side_name=self.auto_create_name_side,
                                                          reverse_side=self.auto_create_reverse,
                                                          )

        if type(self.ctrlName) == list:
            locatorNames = self.ctrlName


        # if there is only 1 control parent, make that the parent for every item in the array
        if type(self.controlParent) != list:
            self.controlParent = [self.controlParent for x in range(len(self.matrixNodes))]

        for idx, node in enumerate(self.matrixNodes):
            locatorName = locatorNames[idx]
            manual_name = None
            component_type = self.controlType
                    
            if self.manualLocatorNames:
                manual_name = self.ctrlName[idx]
                if manual_name in self.manual_no_rivet_names:
                    component_type = 2
            
            if not self.autoNameWithSide and not self.manualLocatorNames:
                locatorName = self.locatorName
            side, name = misc.getNameSide(locatorName)
            controlName = "{0}_{1}MatrixDef_CTL".format(side, name)
            
            controlShape = self.controlShapeDict
            if self.customControlShapes and len(self.customControlShapes) == len(self.matrixNodes):
                controlShape = self.customControlShapes[controlName]
            # if a name exists in self.customControlShapes exract it now and use that control shape dict instead of the default
            # customControlShapes
            # manual_no_rivet_names = self.manual_no_rivet_names,
            # manual_constraint_dict = self.manual_constraint_dict,

            if not cmds.objExists(controlName):
                if component_type == 0:
                    ctrl = simpleton.Component(side=side,
                                            name=name+"MatrixDef", 
                                            parent=self.controlParent[idx],
                                            translate = translations[idx],
                                            rotate = rotations[idx],
                                            scale = scales[idx],
                                            offset = self.offset,
                                            size=self.size,
                                            curveData = controlShape,
                                            component_name=self.component_name

                                            )
                elif component_type == 1:
                    ctrl = meshRivetCtrl.Component(name = name+"MatrixDef", 
                                                        side=side,
                                                        speedTxDefault=1,
                                                        speedTyDefault=1,
                                                        speedTzDefault=1,
                                                        parent=self.controlParent[idx],
                                                        curveData=controlShape,
                                                        mesh = self.control_rivet_mesh,
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
                                                        component_name=self.component_name
                                                        )
                elif component_type == 2:
                    ctrl = simpleton.Component(side=side,
                                            name=name+"MatrixDef", 
                                            parent=self.controlParent[idx],
                                            translate = translations[idx],
                                            rotate = rotations[idx],
                                            scale = scales[idx],
                                            offset = self.offset,
                                            size=self.size,
                                            curveData = controlShape,
                                            component_name=self.component_name,
                                            null_transform = False,
                                            do_guide=True
                                            )
                ctrl.create()
                controlName = ctrl.ctrl

            if not controlName in self.controls:
                self.controls.append(controlName)

    def connectCtrls(self):
        if not self.doCreateCtrls:
            return
        for idx, ctrl in enumerate(self.controls):
            if self.connectTranslate and cmds.objExists(ctrl + ".tOut"):
                cmds.connectAttr(ctrl + ".tOut", self.matrixNodes[idx] + ".translate", f=True)
            elif self.connectTranslate:
                cmds.connectAttr(ctrl + ".translate", self.matrixNodes[idx] + ".translate", f=True)

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
        for idx, current_ctrl in enumerate(self.controls):
        # for idx, guide in enumerate(self.guide_shapes):
            guide_shape = self.guide_shapes[idx]
            guide = misc.getParent(guide_shape)
            message_utils.create_message_attr_setup(current_ctrl, "guide", guide, "ctrl")
            message_utils.create_message_attr_setup(current_ctrl, "guide_shape", guide_shape, "ctrl")
            tag_utils.tag_guide(guide)
            tag_utils.tag_guide_shape(guide_shape)
            if self.component_name:
                tag_utils.create_component_tag(guide, self.component_name)
            if "Rot" in guide:
                message_utils.create_message_attr_setup(current_ctrl, "rotation_guide", guide, "rotation_ctrl")
                tag_utils.create_tag(guide, "ROTATION_GUIDE")
            if "Trans" in guide:
                message_utils.create_message_attr_setup(current_ctrl, "translation_guide", guide, "translation_ctrl")
                tag_utils.create_tag(guide, "TRANSLATION_GUIDE")
                



    def cleanup(self):
        for node in self.matrixNodes + self.matrixBaseNodes:
            if self.hide:
                cmds.setAttr(node + ".visibility", 0)
            if not self.centerToParent:
                continue
            if cmds.listRelatives(node, p=True):
                cmds.xform(node, os=True, t=[0,0,0], ro=[0,0,0])



