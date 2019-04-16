from maya import cmds
import maya.OpenMaya as OpenMaya
import sys
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
# from rig.utils import weightMapUtils
# from rig.deformers import base
from rig.deformers import weightStack
reload(weightStack)
# from rig.deformers import utils as deformerUtils
from rig.deformers import matrixDeformer
reload(matrixDeformer)
from rig.deformers import slideSimple
reload(slideSimple)
from rig.deformers import blendshapeSimple
reload(blendshapeSimple)
from rig.deformers import vectorDeformerSimple
reload(vectorDeformerSimple)
from rig.deformers import curveRollSimple
reload(curveRollSimple)
from rig.deformers import utils as deformerUtils
reload(deformerUtils)
# reload(deformerUtils)
# reload(base)
from rig.utils import weightMapUtils, misc
reload(misc)
from rig.utils import LHCurveDeformerCmds
reload(LHCurveDeformerCmds)
from rig.rigComponents import meshRivetCtrl 
reload(meshRivetCtrl)
from rig.rigComponents import elements
reload(elements)

from decorators import initialize
reload(elements)

from rig.utils import lhExport
reload(lhExport)

from rig.rigComponents import line
reload(line)
from rig.rigComponents import lid
reload(lid)

def test():
    cmds.file( new=True, f=True )

    cmds.unloadPlugin("collision")

    cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")

    fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/FaceModelPackage/eyeLidTweaks.ma"
    fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/FaceModelPackage/eyeLidTweaksOblongEye.ma"

    cmds.file( fileName, i=True, f=True )

    slidePatch="eyeLidModelPackage:L_lidSlide"
    slidePatchBase="eyeLidModelPackage:L_lidSlideBase"
    controlAutoOrientMesh ="eyeLidModelPackage:L_lidSlide"
    upperLipMesh = "eyeLidModelPackage:L_humanLidsUpper"
    upperLipBaseMesh = "eyeLidModelPackage:L_humanLidsUpperBase"
    lowerLidMesh = "eyeLidModelPackage:L_humanLidsLower"
    lowerLidBaseMesh = "eyeLidModelPackage:L_humanLidsLowerBase"
    projectionMeshUpper="eyeLidModelPackage:L_upLidProjection"
    projectionMeshLower="eyeLidModelPackage:L_lowLidProjection"

    # delete history
    for i in [slidePatch, slidePatchBase, controlAutoOrientMesh, upperLipMesh, upperLipBaseMesh, lowerLidMesh, lowerLidBaseMesh,
              projectionMeshUpper, projectionMeshLower]:
        cmds.select(i, r=True)
        cmds.DeleteHistory(i)

    left_lids = lid.Lid(
                        tierCounts=[1,3,5],
                        side="L",
                        nameLids="Lid",
                        ctrlName = "LID",  # this will be used as a way to reuse controls between different components and deformers
                        upperLipMesh = upperLipMesh,
                        upperLipBaseMesh = upperLipBaseMesh,
                        lowerLidMesh = lowerLidMesh,
                        lowerLidBaseMesh = lowerLidBaseMesh,
                        slidePatch=slidePatch,
                        slidePatchBase=slidePatchBase,
                        projectionMeshUpper=projectionMeshUpper,
                        projectionMeshLower=projectionMeshLower,
                        ctrlAutoPositionThreshold=.09,
                        containerName = "L_lids",
                        slideControlSpeedDefaults = [.1,.1,.1],
                        slideCtrlSizes = [1, .65, .35],
                        slideCtrlShapeOffset1=[0,0.0,2],
                        slideCtrlShapeOffset2=[0,0.0,2],
                        slideCtrlShapeOffset3=[0,0.0,2],
                        )
    left_lids.create()
