from maya import cmds
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
# from rig.utils import weightMapUtils
# from rig.deformers import base
from rig_2.component.subcomponent import weightStack

importlib.reload(weightStack)
# from rig.deformers import utils as deformerUtils
from rig.deformers import matrixDeformer
importlib.reload(matrixDeformer)
from rig.deformers import slideSimple
importlib.reload(slideSimple)
from rig.deformers import blendshapeSimple
importlib.reload(blendshapeSimple)
from rig.deformers import vectorDeformerSimple
importlib.reload(vectorDeformerSimple)
from rig.deformers import curveRollSimple
importlib.reload(curveRollSimple)
from rig.deformers import utils as deformerUtils
importlib.reload(deformerUtils)
# reload(deformerUtils)
# reload(base)
from rig.utils import misc
importlib.reload(misc)
from rig.utils import LHCurveDeformerCmds
importlib.reload(LHCurveDeformerCmds)
from rig.rigComponents import meshRivetCtrl 
importlib.reload(meshRivetCtrl)
from rig.rigComponents import elements
importlib.reload(elements)
from rig.rigComponents import mouthJaw
importlib.reload(mouthJaw)

importlib.reload(elements)

def test():
    cmds.file( new=True, f=True )
    # Linux
    # cmds.unloadPlugin("collision")
    # cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")
    # fileName="/scratch/levih/dev/rotoslang/src/scenes/presentation/FaceModelPackage/facePackageTweaks.ma"
   
    # Windows
    cmds.unloadPlugin("LHDeformerNodes")
    cmds.loadPlugin("C:/Users/harri/Desktop/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/src/Debug/LHDeformerNodes")
    fileName="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/presentation/FaceModelPackage/mouthJawPackageTweaks.ma"




    dog=False
    superman=False
    old_man=True




    slidePatch="faceModelPackage:slide"
    slidePatchBase="faceModelPackage:slideBase"
    controlAutoOrientMesh ="faceModelPackage:slide"

    # Lower Mesh Defaults
    deformMesh="faceModelPackage:humanJaw"
    baseMesh="faceModelPackage:humanJawBase"
    baseMeshprojectionMesh="faceModelPackage:mouthProjection"

    if old_man:
        deformMesh="FullBody:jawMouth"
        baseMesh="FullBody:jawMouthBase"
        fileName = "C:/Users/harri/Desktop/dev/rotoslang/src/scenes/oldMan/faceRigPackage/lipsPackage.ma"

    cmds.file( fileName, i=True, f=True )
    # delete history
    for i in [slidePatch, slidePatchBase, controlAutoOrientMesh, deformMesh, baseMesh, baseMeshprojectionMesh]:
        cmds.select(i, r=True)
        cmds.DeleteHistory(i)
        cmds.makeIdentity(i, apply=True, t=1, r=1, s=1, n=0, pn=1);

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
                #  matDefTranslations = elements.JAW_MOUTH_MATDEF_TRANSLATIONS,
                #  matDefRotations = elements.JAW_MOUTH_MATDEF_ROTATIONS,
                #  matDefScales = elements.JAW_MOUTH_MATDEF_SCALES,
                #  matDefHandWeightsDictionary = elements.JAW_MOUTH_MATDEF_WEIGHT_DICT,
                #  slideHandWeightsDictionary = elements.JAW_MOUTH_SLIDE_WEIGHT_DICT,
    )
    MouthJawClass.create() 
    cmds.select(MouthJawClass.mat_def_translate.controls)
    cmds.viewFit()
    # MouthJawClass.setPositions() 
    # MouthJawClass.setHandWeights()
