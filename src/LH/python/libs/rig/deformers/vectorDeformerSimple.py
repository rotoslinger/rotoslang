from maya import cmds
import base
reload(base)
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
reload(misc)

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

    def getNodes(self):
        if not self.vectorCurve:
            self.vectorCurve = cmds.curve(name= self.name + "Curve",
                                d=1, p=[(0,0,0),self.toPoint],
                                k=[0,1])
        self.vectorCurve = misc.getShape(self.vectorCurve)

    def setDefaults(self):

        if type(self.geoToDeform) != list:
            self.geoToDeform = [self.geoToDeform]

        if not self.weightStackNode:
            self.weightMap = weightMapUtils.createWeightMapOnSingleObject(self.geoToDeform[0], self.name + "Weights", defaultValue=1.0, addAttr=True)
        else:
            self.weightMap = "{0}.outWeightsDoubleArray".format(self.weightStackNode)


    def connectDeformer(self):
        cmds.connectAttr(self.vectorCurve + ".worldSpace", self.deformer + ".vectorCurve")
        cmds.connectAttr(self.weightMap, "{0}.vectorWeights".format(self.deformer), f=True)
