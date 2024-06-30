from maya import cmds
from . import base
import importlib
importlib.reload(base)
from rig.utils import weightMapUtils, misc
importlib.reload(weightMapUtils)
importlib.reload(misc)

def createTestVectorDeformerRaw():
    deformMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2, sx=100, sy=100,  n="deformMesh")[0]
    deformer = cmds.deformer(deformMesh, type="LHVectorDeformerSimple")[0]
    testVectorCurve = cmds.curve(name= "testVectorCurve",
                        d=1, p=[(0,0,0),(0,0,-1)],
                        k=[0,1])
    testVectorCurveShape = misc.getShape(testVectorCurve)
    cmds.connectAttr(testVectorCurveShape+ ".worldSpace", "{0}.vectorCurve".format(deformer))
    weightMap = weightMapUtils.createWeightMapOnSingleObject(deformMesh, "testWeights", defaultValue=1.0, addAttr=True)
    cmds.connectAttr(weightMap, "{0}.vectorWeights".format(deformer))

def createTestVectorDeformerClass():
    deformMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2, sx=100, sy=100,  n="deformMesh")[0]
    deformer = VectorDeformerSimple(geoToDeform=deformMesh)
    deformer.create()

class VectorDeformerSimple(base.Deformer):
    def __init__(self,
                    name="testVectorDeformerSimple",
                    membershipWeightsAttr = "",
                    geoToDeform=[],
                    vectorCurve=None,
                    toPoint=(0,0,-1),
                    parent="",
                    weightStackNode="",
                    location=None,
                 **kw):
        super(VectorDeformerSimple, self).__init__(**kw)
        self.name = name
        self.membershipWeightsAttr = membershipWeightsAttr
        self.geoToDeform = geoToDeform
        self.vectorCurve = vectorCurve
        self.toPoint = toPoint
        self.parent = parent
        self.weightStackNode = weightStackNode
        self.location = location
        self.deformer = ""
        self.deformerType = "LHVectorDeformerSimple"
        self.weightMap = ""


    def getDeformer(self):
        if cmds.objExists(self.name):
            self.deformer = self.name
            return
        self.deformer = cmds.deformer(self.geoToDeform, type=self.deformerType, n=self.name, par=True)[0]



    def getNodes(self):
        if not self.vectorCurve:
            if cmds.objExists(self.name + "Curve"):
                self.vectorCurve = self.name + "Curve"
            else:
                self.vectorCurve = cmds.curve(name= self.name + "Curve",
                                    d=1, p=[(0,0,0),self.toPoint],
                                    k=[0,1])
                print(self.vectorCurve,self.parent)
                print(self.vectorCurve,self.parent)
                print(self.vectorCurve)
                print(self.vectorCurve)
                print(self.vectorCurve)
                cmds.parent(self.vectorCurve, self.parent)
        self.vectorCurve = misc.getShape(self.vectorCurve)

    def setDefaults(self):

        if type(self.geoToDeform) != list:
            self.geoToDeform = [self.geoToDeform]

        if not self.weightStackNode:
            self.weightMap = weightMapUtils.createWeightMapOnSingleObject(self.geoToDeform[0], self.name + "Weights", defaultValue=1.0, addAttr=True)
        else:
            self.weightMap = "{0}.outWeightsDoubleArray".format(self.weightStackNode)


    def connectDeformer(self):
        cmds.connectAttr(self.vectorCurve + ".worldSpace", self.deformer + ".vectorCurve", f=True)
        cmds.connectAttr(self.weightMap, "{0}.vectorWeights".format(self.deformer), f=True)
