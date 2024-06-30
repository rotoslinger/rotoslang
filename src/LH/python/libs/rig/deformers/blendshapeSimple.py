from maya import cmds
import maya.OpenMaya as OpenMaya
import sys
import importlib
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)
from rig.deformers import base

from rig.deformers import utils as deformerUtils
importlib.reload(deformerUtils)
from rig.deformers import utils as deformerUtils
importlib.reload(deformerUtils)
from rig.utils import weightMapUtils, misc
importlib.reload(misc)

class BlendshapeSimple(base.Deformer):
    def __init__(self,
                    sourceGeom="",
                    targetGeom="",
                 **kw):
        super(BlendshapeSimple, self).__init__(**kw)
        self.targetGeom = targetGeom
        # to make the args easier to read
        if not self.geoToDeform:
            self.geoToDeform = sourceGeom
        self.deformerType="LHBlendshapeSimple"


    def check(self):
        self.geomTypeAttr = misc.getGeomTypeAttr(self.geoToDeform)
        targetGeomTypeAttr = misc.getGeomTypeAttr(self.targetGeom)
        if not self.geomTypeAttr == targetGeomTypeAttr:
            raise Exception('The target and source geometries are not the same time, make sure you only blendshape geometries of the same type')
            quit()

    def getAttrs(self):
        self.amountAttr = self.deformer + ".amount"

    def getNodes(self):
        self.geoToDeform = misc.getShape(self.geoToDeform)
        self.targetGeom = misc.getShape(self.targetGeom)

    # def setDefaults(self):
    #     # Set membership weights to be all 1 by default, unless otherwise specified
    #     iterGeo = misc.getOMItergeo(self.geoToDeform)
    #     polyCount = iterGeo.count()
    #     defaultVals = [1.0 for x in range(polyCount)]
    #     cmds.setAttr(self.deformer + "." + "membershipWeights", defaultVals, type="doubleArray")

    def connectDeformer(self):
        cmds.connectAttr(self.targetGeom + self.geomTypeAttr, self.deformer + ".targetGeo")

    def cleanup(self):
        return
