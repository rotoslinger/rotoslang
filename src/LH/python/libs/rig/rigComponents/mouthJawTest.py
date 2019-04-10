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
from rig.rigComponents import mouthJaw
reload(mouthJaw)

from decorators import initialize
reload(elements)

def test():
    cmds.file( new=True, f=True )

    cmds.unloadPlugin("collision")

    cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")

    dog=False
    superman=False

    fileName="/scratch/levih/dev/rotoslang/src/scenes/presentation/FaceModelPackage/mouthJawPackageTweaks.ma"


    cmds.file( fileName, i=True, f=True )

    slidePatch="faceModelPackage:slide"
    slidePatchBase="faceModelPackage:slideBase"
    controlAutoOrientMesh ="faceModelPackage:slide"

    # Lower Mesh Defaults
    deformMesh="faceModelPackage:humanJaw"
    baseMesh="faceModelPackage:humanJawBase"
    baseMeshprojectionMesh="faceModelPackage:mouthProjection"

    # delete history
    for i in [slidePatch, slidePatchBase, controlAutoOrientMesh, deformMesh, baseMesh, baseMeshprojectionMesh]:
        cmds.select(i, r=True)
        cmds.DeleteHistory(i)
    MouthJawClass = mouthJaw.MouthJaw(
                 nameMouth="mouth",
                 nameJaw="jaw",
                 deformMesh=deformMesh,
                 baseGeoToDeform=baseMesh,
                 slidePatch=slidePatch,
                 slidePatchBase=slidePatchBase,
                 projectionMesh=baseMeshprojectionMesh,
                 characterName = "character",
                 controlParent="C_control_GRP",
                 rigParent="C_rig_GRP",
                 ctrlAutoPositionThreshold=.09,
                 matDefTranslations = elements.JAW_MOUTH_MATDEF_TRANSLATIONS,
                 matDefRotations = elements.JAW_MOUTH_MATDEF_ROTATIONS,
                 matDefScales = elements.JAW_MOUTH_MATDEF_SCALES,
                 matDefHandWeightsDictionary = elements.JAW_MOUTH_MATDEF_WEIGHT_DICT,
                 slideHandWeightsDictionary = elements.JAW_MOUTH_SLIDE_WEIGHT_DICT,
                

    )


    MouthJawClass.create() 
    MouthJawClass.setPositions() 
    MouthJawClass.setHandWeights() 
