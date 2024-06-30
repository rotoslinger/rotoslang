import inspect
from collections import OrderedDict

from maya import cmds
from rig.utils import weightMapUtils, misc
import importlib
importlib.reload(weightMapUtils)
importlib.reload(misc)
import copy
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)

from rig_2.component import base as component_base
importlib.reload(component_base)


class Deformer(object):
    def __init__(self,
                    name="testDeformer",
                    deformerType="",
                    geoToDeform="",
                    parent="",
                    centerToParent=True,
                    rotationTranforms=[],
                    addAtIndex=0,
                    numToAdd=1,
                    locatorName="test",
                    curveWeightsNode="",
                    curveWeightsConnectionIdx=0,
                    locations=[],
                    hide=True,
                    orderFrontOfChain=True,
                    orderParallel=False,
                    orderBefore=False,
                    orderAfter=False,
                    orderSplit=False,
                    orderExclusive=False,
                    component_name="",
                 ):
        # args
        self.component_name=component_name
        self.name = name
        self.addAtIndex = addAtIndex
        self.deformerType = deformerType
        self.geoToDeform = geoToDeform
        self.parent = parent
        self.centerToParent = centerToParent
        self.rotationTranforms = rotationTranforms
        self.numToAdd = numToAdd
        self.locatorName = locatorName
        self.curveWeightsNode = curveWeightsNode
        self.curveWeightsConnectionIdx = curveWeightsConnectionIdx
        self.locations = locations
        self.hide = hide
        self.orderFrontOfChain = orderFrontOfChain
        self.orderParallel = orderParallel
        self.orderBefore = orderBefore
        self.orderAfter = orderAfter
        self.orderSplit = orderSplit
        self.orderExclusive = orderExclusive

        # attrs
        self.deformer = ""
        self.matrixNodes = []
        self.matrixBaseNodes = []


    # def initialize(self):
    #     self.check()
    #     self.getDeformer()
    #     self.getNodes()

    def check(self):
        return

    def getDeformer(self):
        if cmds.objExists(self.name):
            self.deformer = self.name
            return
        print(self.deformerType, "DEFORMER TYPE")
        print(self.geoToDeform, "GEO TO DEFORM")
        self.deformer = cmds.deformer(self.geoToDeform, type=self.deformerType, n=self.name,
                                      foc=self.orderFrontOfChain,
                                      bf=self.orderBefore,
                                      af=self.orderAfter, 
                                      par=self.orderParallel,
                                    #   sp = self.orderSplit,
                                    #   ex = self.orderExclusive,
                                      
                                      )[0]
        tag_utils.create_component_tag(self.deformer, self.component_name)
        tag_utils.create_component_tag(self.geoToDeform, self.component_name)


    def getNodes(self):
        return

    def getAttrs(self):
        return

    def setDefaults(self):
        return
        
    def connectDeformer(self):
        return

    def createCtrls(self):
        return

    def connectCtrls(self):
        return

    def cleanup(self):
        return

    def duplicateMeshClean(self, mesh, vis=False):
        """ Makes sure to duplicate a mesh cleanly, you still need to be careful of deformations """
        meshShape = cmds.ls(mesh, dag = 1, g = 1)[0]
        newTransform = cmds.createNode("transform", n = mesh + "Base")
        newMesh = cmds.createNode("mesh", n = mesh + "BaseShape", p = newTransform)
        cmds.connectAttr(meshShape + ".outMesh", newMesh + ".inMesh")
        cmds.refresh()
        cmds.disconnectAttr(meshShape + ".outMesh", newMesh + ".inMesh")
        if self.parent:
            cmds.parent(newTransform, self.parent)
        if not vis:
            cmds.setAttr(newTransform + ".visibility", 0)
        return newTransform, newMesh


    def post_create(self):
        return

    def create(self):
        self.check()
        self.getDeformer()
        self.getNodes()
        self.getAttrs()
        self.setDefaults()
        self.connectDeformer()
        self.createCtrls()
        self.connectCtrls()
        self.cleanup()
        self.post_create()
        