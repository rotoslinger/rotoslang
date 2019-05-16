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

from rig.rigComponents import brow
reload(brow)

def test(old_man=True):
    cmds.file( new=True, f=True )

    # Linux
    # cmds.unloadPlugin("collision")
    # cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")
    # model_package = "/scratch/levih/dev/rotoslang/src/scenes/presentation/FaceModelPackage/browTweaks.ma"
   
    # Windows
    cmds.unloadPlugin("LHDeformerNodes")
    cmds.loadPlugin("C:/Users/harri/Desktop/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/src/Debug/LHDeformerNodes")

    model_package = "C:/Users/harri/Desktop/dev/rotoslang/src/scenes/presentation/FaceModelPackage/browTweaks.ma"

    slidePatch="browModelPackage:slide"
    slidePatchBase="browModelPackage:slideBase"
    controlAutoOrientMesh ="browModelPackage:slide"
    leftBrowMesh = "browModelPackage:brow"
    leftBrowBaseMesh = "browModelPackage:browBase"
    rightBrowMesh = "browModelPackage:brow"
    rightBrowBaseMesh = "browModelPackage:browBase"
    L_projectionMesh="browModelPackage:L_projectionPatch"
    R_projectionMesh="browModelPackage:R_projectionPatch"
    
    if old_man:

        model_package = "C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/rigFiles/brow.ma"
        asset="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/oldMan.ma"

        slidePatch="C_browSlide_SURF"
        slidePatchBase="C_browSlideBase_SURF"
        controlAutoOrientMesh ="C_browSlide_SURF"
        leftBrowMesh = "C_brow_GEO"
        leftBrowBaseMesh = "C_browBase_GEO"
        rightBrowMesh = "C_brow_GEO"
        rightBrowBaseMesh = "C_browBase_GEO"
        L_projectionMesh="L_browProjection_MESH"
        R_projectionMesh="R_browProjection_MESH"
        cmds.file( asset, i=True, f=True )

    cmds.file( model_package, i=True, f=True, preserveReferences=True, loadReferenceDepth="none" )



    # delete history
    if not old_man:
        for i in [slidePatch, slidePatchBase, controlAutoOrientMesh, leftBrowMesh, leftBrowBaseMesh, rightBrowMesh, rightBrowBaseMesh,
                L_projectionMesh, R_projectionMesh]:
            cmds.select(i, r=True)
            cmds.DeleteHistory(i)

    browClass = brow.Brow(
                        tierCounts=[1,3,5],
                        side="L",
                        nameBrows="Brow",
                        ctrlName = "BROW",  # this will be used as a way to reuse controls between different components and deformers
                        leftBrowMesh = leftBrowMesh,
                        leftBrowBaseMesh = leftBrowBaseMesh,
                        rightBrowMesh = rightBrowMesh,
                        rightBrowBaseMesh = rightBrowBaseMesh,
                        slidePatch=slidePatch,
                        slidePatchBase=slidePatchBase,
                        L_projectionMesh=L_projectionMesh,
                        R_projectionMesh=R_projectionMesh,
                        ctrlAutoPositionThreshold=.09,
                        containerName = "BROW",
                        slideControlSpeedDefaults = [.1,.1,.1],
                        slideCtrlSizes = [1, .65, .35],
                        slideCtrlShapeOffset1=[0,0.0, 3.5],
                        slideCtrlShapeOffset2=[0,0.0, 3.5],
                        slideCtrlShapeOffset3=[0,0.0, 3.5],
                        matDefCtrlShapeOffset1=[0,-2.0, 3.5],
                        matDefCtrlShapeOffset2=[0,-2.0, 3.5],
                        matDefCtrlShapeOffset3=[0,-2.0, 3.5],
                        )
    browClass.create()
