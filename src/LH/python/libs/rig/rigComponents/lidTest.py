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

importlib.reload(elements)

from rig.utils import lhExport
importlib.reload(lhExport)

from rig.rigComponents import line
importlib.reload(line)
from rig.rigComponents import lid
importlib.reload(lid)

def test(old_man=False, auto_load=True):
    if auto_load:
        cmds.file( new=True, f=True)
        # Linux
        # cmds.unloadPlugin("collision")
        # cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")
        # rig_model_package = "/scratch/levih/dev/rotoslang/src/scenes/presentation/FaceModelPackage/eyeLidTweaks.ma"
        # rig_model_package = "/scratch/levih/dev/rotoslang/src/scenes/presentation/FaceModelPackage/eyeLidTweaksOblongEye.ma"
        # Windows
        cmds.unloadPlugin("LHDeformerNodes")
        cmds.loadPlugin("C:/Users/harri/Desktop/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/src/Debug/LHDeformerNodes")

    rig_model_package="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/presentation/FaceModelPackage/eyeLidTweaksOblongEye.ma"
    rig_model_package="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/rigFiles/eyeLidModelPackage.ma"

    if old_man==True:
        rig_model_package="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/rigFiles/eyeLidModelPackage.ma"
        asset="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/oldMan.ma"
        rig_model_package = "C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/rigFiles/lids.ma"
    # cmds.file( rig_model_package, i=True, f=True, )
    # This removes the reference from the file
    cmds.file( rig_model_package, i=True, f=True, preserveReferences=True, loadReferenceDepth="none" )

    L_slidePatch="L_lidSlide"
    L_slidePatchBase="L_lidSlideBase"
    L_controlAutoOrientMesh ="L_lidSlide"
    L_projectionMeshUpper="L_upLidProjection"
    L_projectionMeshLower="L_lowLidProjection"

    R_slidePatch="R_lidSlide"
    R_slidePatchBase="R_lidSlideBase"
    R_controlAutoOrientMesh ="R_lidSlide"
    R_projectionMeshUpper="R_upLidProjection"
    R_projectionMeshLower="R_lowLidProjection"

    slide_speed = [.5,.5,.5]

    if old_man==True:
        L_upperLipMesh = "L_upperLid"
        L_upperLipBaseMesh = "L_upperLidBase"
        L_lowerLidMesh = "L_lowerLid"
        L_lowerLidBaseMesh = "L_lowerLidbase"

        R_upperLipMesh = "R_upperLid"
        R_upperLipBaseMesh = "R_upperLidBase"
        R_lowerLidMesh = "R_lowerLid"
        R_lowerLidBaseMesh = "R_lowerLidBase"

        if auto_load:
            cmds.file( asset, i=True, f=True )

    left_eye_grp = "L_eyeRigPackage_GRP"
    right_eye_grp = cmds.duplicate(left_eye_grp, n=left_eye_grp.replace("L_", "R_"),rc=True)
    cmds.setAttr(right_eye_grp[0] + ".sx", -1)
    for node in right_eye_grp:
        node = cmds.rename(node, node.replace("L_", "R_"))
        if "1" in node:
            node = cmds.rename(node, node.replace("1", ""))
        cmds.select(node, r=True)
        cmds.DeleteHistory(node)
        cmds.makeIdentity(node, apply=True, t=1, r=1, s=1, n=0, pn=1)
        print(node)
        if cmds.listRelatives(node, s=True) and cmds.objectType(cmds.listRelatives(node, s=True)[0]) == "nurbsSurface":
            cmds.reverseSurface(node,d=0, ch=1, rpo=1)

    # return
    # delete history
    # for i in [L_slidePatch, L_slidePatchBase, L_controlAutoOrientMesh, L_upperLipMesh, L_upperLipBaseMesh, L_lowerLidMesh, L_lowerLidBaseMesh,
    #           L_projectionMeshUpper, L_projectionMeshLower]:
    #     cmds.select(i, r=True)
    #     cmds.DeleteHistory(i)

    left_lids = lid.Lid(
                    tierCounts=[1,3,5],
                    side="L",
                    nameLids="leftLid",
                    ctrlName = "lid",  # this will be used as a way to reuse controls between different components and deformers
                    upperLipMesh = L_upperLipMesh,
                    upperLipBaseMesh = L_upperLipBaseMesh,
                    lowerLidMesh = L_lowerLidMesh,
                    lowerLidBaseMesh = L_lowerLidBaseMesh,
                    slidePatch=L_slidePatch,
                    slidePatchBase=L_slidePatchBase,
                    projectionMeshUpper=L_projectionMeshUpper,
                    projectionMeshLower=L_projectionMeshLower,
                    ctrlAutoPositionThreshold=.09,
                    containerName = "L_lids",
                    slideControlSpeedDefaults = slide_speed,
                    slideCtrlSizes = [1, .65, .35],
                    slideCtrlShapeOffset1=[0,0.0,2],
                    slideCtrlShapeOffset2=[0,0.0,2],
                    slideCtrlShapeOffset3=[0,0.0,2],
                    component_name="L_lids"
                    )

    left_lids.create()
    cmds.select(left_lids.matDeformersTranslate["Upper"].controls)
    cmds.viewFit()

    right_lids = lid.Lid(
                    tierCounts=[1,3,5],
                    side="R",
                    nameLids="rightLid",
                    ctrlName = "lid",  # this will be used as a way to reuse controls between different components and deformers
                    upperLipMesh = R_upperLipMesh,
                    upperLipBaseMesh = R_upperLipBaseMesh,
                    lowerLidMesh = R_lowerLidMesh,
                    lowerLidBaseMesh = R_lowerLidBaseMesh,
                    slidePatch=R_slidePatch,
                    slidePatchBase=R_slidePatchBase,
                    projectionMeshUpper=R_projectionMeshUpper,
                    projectionMeshLower=R_projectionMeshLower,
                    ctrlAutoPositionThreshold=.09,
                    containerName = "R_lids",
                    slideControlSpeedDefaults = slide_speed,
                    slideCtrlSizes = [1, .65, .35],
                    slideCtrlShapeOffset1=[0,0.0,2],
                    slideCtrlShapeOffset2=[0,0.0,2],
                    slideCtrlShapeOffset3=[0,0.0,2],
                    component_name="R_lids"
                    )
    right_lids.create()



