
from maya import cmds
import maya.OpenMaya as OpenMaya
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

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
from rig.utils import weightMapUtils
from rig.utils import misc
from rig.deformers import base
from rig.deformers import weightStack
from rig.deformers import tests 
from rig.deformers import test2
from rig.deformers import test3
from rig.deformers import test4
from rig.deformers import matrixDeformer 
from rig.deformers import utils 
from rig.rigComponents import lip 
from rig.rigComponents import meshRivetCtrl
from rig.rigComponents import elements 
reload(elements)
reload(meshRivetCtrl)
reload(misc)
reload(weightMapUtils)
reload(lip)
reload(utils)
reload(matrixDeformer)
reload(tests)
reload(test2)
reload(test3)
reload(test4)
reload(weightStack)
reload(base)

def test():
    cmds.file( new=True, f=True )

    cmds.unloadPlugin("collision")

    cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")

    dog=False

    fileName="/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/humanLipTest.ma"
    tierCount1 = 1
    tierCount2 = 9
    tierCount3 = 11

    slideCtrlSize1=2
    slideCtrlSize2=1
    slideCtrlSize3=.5
    slideControlSpeedDefaults = [.1,.1,.1]

    ctrlAutoPositionThreshold = 0.9

    thickToPoint = (0, 0.978, -0.208)


    slideCtrlShapeOffset1=[0,0.0,2]
    slideCtrlShapeOffset2=[0,0.0,1]
    slideCtrlShapeOffset3=[0,0.0,1]

    slideCtrlPosOffset1=[0, 0.0, 0]
    slideCtrlPosOffset2=[0, 0.0, 0]
    slideCtrlPosOffset3=[0, 0.0, 0]

    # thickCtrlShapeOffset1=[0,-4.0,2]
    # thickCtrlShapeOffset2=[0,-4.0,1]
    # thickCtrlShapeOffset3=[0,-4.0,1]

    # falloffMatrixDeformerName = ctrlName + "MATDEFTEST"

    falloffDefaults=(-10, -9.9, -3, 10.0)
    falloffMatrixDefaults=(-11, -7, -2, 10.0)
    lowerRemovePointIndicies=[10, 11, 23, 35, 47, 48, 71, 73, 85, 97, 98, 121, 133, 145, 146, 158, 170, 193, 205, 206, 229, 239, 240, 251, 262, 273, 274, 295, 297, 308, 319, 320, 341, 352, 363, 364, 375, 386, 407, 418, 419, 440]
    upperRemovePointIndicies=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 34, 46, 58, 59, 160, 172, 217, 218, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 262, 273, 284, 285, 377, 388, 429, 430]

    matDefCtrlSize1=1
    matDefCtrlSize2=.65
    matDefCtrlSize3=.35

    matDefCtrlShapeOffset1=[0,-1.0,2]
    matDefCtrlShapeOffset2=[0,-1.0,1]
    matDefCtrlShapeOffset3=[0,-1.0,1]




    if dog:
        fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/dogLipTest.ma"
        tierCount1 = 1
        tierCount2 = 5
        tierCount3 = 7

        slideCtrlSize1=2.3
        slideCtrlSize2=1.2
        slideCtrlSize3=.6
        ctrlAutoPositionThreshold = 0.9

        slideCtrlShapeOffset1=[0,0.0,2]
        slideCtrlShapeOffset2=[0,0.0,2]
        slideCtrlShapeOffset3=[0,0.0,2]
        
        falloffDefaults=(-10, -9.9, -4, 10.0)
        
        slideCtrlPosOffset1=[0, 0.0, 3]
        slideCtrlPosOffset2=[0, 0.0, 0]
        slideCtrlPosOffset3=[0, 0.0, 0]
        
        slideControlSpeedDefaults = [.025,.05,.05]
        lowerRemovePointIndicies=[]
        upperRemovePointIndicies=[]

    lowerLipSlide, lowerLipThick = lip.Lip(name="lowerLip",
                upperLip=False,
                tierCount1=tierCount1,
                tierCount2=tierCount2,
                tierCount3=tierCount3,
                thickToPoint=thickToPoint,
                slideCtrlSize1=slideCtrlSize1,
                slideCtrlSize2=slideCtrlSize2,
                slideCtrlSize3=slideCtrlSize3,

                slideCtrlShapeOffset1=slideCtrlShapeOffset1,
                slideCtrlShapeOffset2=slideCtrlShapeOffset2,
                slideCtrlShapeOffset3=slideCtrlShapeOffset3,
                
                slideCtrlPosOffset1=slideCtrlPosOffset1,
                slideCtrlPosOffset2=slideCtrlPosOffset2,
                slideCtrlPosOffset3=slideCtrlPosOffset3,
                
                slideControlSpeedDefaults=slideControlSpeedDefaults,

                matDefCtrlShapeOffset1=matDefCtrlShapeOffset1,
                matDefCtrlShapeOffset2=matDefCtrlShapeOffset2,
                matDefCtrlShapeOffset3=matDefCtrlShapeOffset3,

                ctrlAutoPositionThreshold = ctrlAutoPositionThreshold,

                # thickCtrlShapeOffset1=thickCtrlShapeOffset1,
                # thickCtrlShapeOffset2=thickCtrlShapeOffset2,
                # thickCtrlShapeOffset3=thickCtrlShapeOffset3,
                
                falloffDefaults=falloffDefaults,
                falloffMatrixDefaults=falloffMatrixDefaults,
                fileName=fileName,
                deformMesh="humanLipsLower",
                base="humanLipsLowerBase",
                projectionMesh="lowLipProjection",
                slidePatch="slide",
                slidePatchBase="slideBase")

    lip.Lip(name="lowerLipCurve",
            ctrlName = "lowerLip",
            controlRivetMesh = "humanLipsLower",
            upperLip=False,
            # multiSlideForBaseCurve=False,
            multiSlideForBaseCurve=True,
            repositionRivetCtrls=True,
            tierCount1=tierCount1,
            tierCount2=tierCount2,
            tierCount3=tierCount3,

            slideCtrlSize1=slideCtrlSize1,
            slideCtrlSize2=slideCtrlSize2,
            slideCtrlSize3=slideCtrlSize3,

            slideCtrlShapeOffset1=slideCtrlShapeOffset1,
            slideCtrlShapeOffset2=slideCtrlShapeOffset2,
            slideCtrlShapeOffset3=slideCtrlShapeOffset3,
            
            slideCtrlPosOffset1=slideCtrlPosOffset1,
            slideCtrlPosOffset2=slideCtrlPosOffset2,
            slideCtrlPosOffset3=slideCtrlPosOffset3,
            
            slideControlSpeedDefaults=slideControlSpeedDefaults,

            matDefCtrlShapeOffset1=matDefCtrlShapeOffset1,
            matDefCtrlShapeOffset2=matDefCtrlShapeOffset2,
            matDefCtrlShapeOffset3=matDefCtrlShapeOffset3,

            ctrlAutoPositionThreshold = .01,

            falloffDefaults=falloffDefaults,
            falloffMatrixDefaults=falloffMatrixDefaults,
            fileName=None,
            deformMesh=["lowerLipCurve", "lowerLipCurveAim"],
            base=["lowerLipCurveBase", "lowerLipCurveAimBase"],
            # deformMesh="lowerLipCurve",
            # base="lowerLipCurveBase",
            projectionMesh="lowLipProjection",
            slidePatch="slide",
            slidePatchBase="slideBase")

    cmds.reorderDeformers(lowerLipSlide, lowerLipThick, misc.getShape("humanLipsLower"))


    lip.lipCurveDeformSplit(name="C_LowerLipWire",
                            curveDeformerAlgorithm=1,
                            curve="lowerLipCurve",
                            curveAim="lowerLipCurveAim",
                            deformedGeometry="humanLipsLower",
                            projectionPatch="lowLipProjection",
                            deformedGeometryBase="humanLipsLowerBase",
                            addWeightStack=["lowerLipWeightStack_LR", "lowerLipWeightStack_UD"],
                            addAtIndex=tierCount1+tierCount2+tierCount3,
                            handPaint=False,
                            upperLip=False,
                            reorderInFrontOfDeformer=lowerLipThick,
                            removePointIndicies=lowerRemovePointIndicies,
                            falloffDefaults = "")



    falloffDefaults=(10, -1, -7, -10.0)
    falloffMatrixDefaults=(10, -1, -9, -10.0)

    matDefCtrlShapeOffset1=[0,1.0,2]
    matDefCtrlShapeOffset2=[0,1.0,1]
    matDefCtrlShapeOffset3=[0,1.0,1]

    # thickToPoint = (0, -0.978, 0.208)

    thickToPoint = (0, 0.978, -0.208)

    thickCtrlShapeOffset1=[0, 2.0, 2]
    thickCtrlShapeOffset2=[0, 2.0, 1]
    thickCtrlShapeOffset3=[0, 2.0, 1]


    thickFalloffCurve = elements.UPPER_LIP_THICK_FALLOFF

    upperLipSlide, upperLipThick = lip.Lip(name="upperLip",
                upperLip=True,
                tierCount1=tierCount1,
                tierCount2=tierCount2,
                tierCount3=tierCount3,
                thickToPoint=thickToPoint,
                slideCtrlSize1=slideCtrlSize1,
                slideCtrlSize2=slideCtrlSize2,
                slideCtrlSize3=slideCtrlSize3,

                slideCtrlShapeOffset1=slideCtrlShapeOffset1,
                slideCtrlShapeOffset2=slideCtrlShapeOffset2,
                slideCtrlShapeOffset3=slideCtrlShapeOffset3,
                
                slideCtrlPosOffset1=slideCtrlPosOffset1,
                slideCtrlPosOffset2=slideCtrlPosOffset2,
                slideCtrlPosOffset3=slideCtrlPosOffset3,
                
                slideControlSpeedDefaults=slideControlSpeedDefaults,

                thickCtrlShapeOffset1=thickCtrlShapeOffset1,
                thickCtrlShapeOffset2=thickCtrlShapeOffset2,
                thickCtrlShapeOffset3=thickCtrlShapeOffset3,
                thickFalloffCurve=thickFalloffCurve,

                matDefCtrlShapeOffset1=matDefCtrlShapeOffset1,
                matDefCtrlShapeOffset2=matDefCtrlShapeOffset2,
                matDefCtrlShapeOffset3=matDefCtrlShapeOffset3,




                ctrlAutoPositionThreshold = ctrlAutoPositionThreshold,

                falloffDefaults=falloffDefaults,
                falloffMatrixDefaults=falloffMatrixDefaults,
                fileName=None,
                deformMesh="humanLipsUpper",
                base="humanLipsUpperBase",
                projectionMesh="upLipProjection",
                slidePatch="slide",
                slidePatchBase="slideBase")

    lip.Lip(name="upperLipCurve",
            ctrlName = "upperLip",
            upperLip=True,

            #fileName=fileName,
            controlRivetMesh = "humanLipsUpper",
            multiSlideForBaseCurve=False,
            repositionRivetCtrls=True,
            tierCount1=tierCount1,
            tierCount2=tierCount2,
            tierCount3=tierCount3,

            slideCtrlSize1=slideCtrlSize1,
            slideCtrlSize2=slideCtrlSize2,
            slideCtrlSize3=slideCtrlSize3,

            slideCtrlShapeOffset1=slideCtrlShapeOffset1,
            slideCtrlShapeOffset2=slideCtrlShapeOffset2,
            slideCtrlShapeOffset3=slideCtrlShapeOffset3,
            
            slideCtrlPosOffset1=slideCtrlPosOffset1,
            slideCtrlPosOffset2=slideCtrlPosOffset2,
            slideCtrlPosOffset3=slideCtrlPosOffset3,
            
            slideControlSpeedDefaults=slideControlSpeedDefaults,

            matDefCtrlShapeOffset1=matDefCtrlShapeOffset1,
            matDefCtrlShapeOffset2=matDefCtrlShapeOffset2,
            matDefCtrlShapeOffset3=matDefCtrlShapeOffset3,

            ctrlAutoPositionThreshold = .01,

            falloffDefaults=falloffDefaults,
            falloffMatrixDefaults=falloffMatrixDefaults,
            fileName=None,
            deformMesh="upperLipCurve",
            base="upperLipCurveBase",
            projectionMesh="upLipProjection",
            slidePatch="slide",
            slidePatchBase="slideBase")

    cmds.reorderDeformers(upperLipSlide, upperLipThick, misc.getShape("humanLipsUpper"))

    blendshape = lip.lipCurveDeformSplit(name="C_UpperLipWire",
                                         curve="upperLipCurve",
                                        curveAim="upperLipCurveAim",
                                        deformedGeometry="humanLipsUpper",
                                        projectionPatch="upLipProjection",
                                        deformedGeometryBase="humanLipsUpperBase",
                                        addWeightStack=["upperLipWeightStack_LR", "upperLipWeightStack_UD"],
                                        addAtIndex=tierCount1+tierCount2+tierCount3,
                                        handPaint=False,
                                        upperLip=True,
                                        removePointIndicies=upperRemovePointIndicies,
                                        reorderInFrontOfDeformer=upperLipThick,
                                        falloffDefaults = "")



