
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
    tierCount2 = 3
    tierCount3 = 5

    ctrlSize1=2
    ctrlSize2=1
    ctrlSize3=.5
    controlSpeedDefaults = [.1,.1,.1]

    ctrlAutoPositionThreshold = 0.9


    ctrlShapeOffset1=[0,0.0,2]
    ctrlShapeOffset2=[0,0.0,1]
    ctrlShapeOffset3=[0,0.0,1]

    ctrlPosOffset1=[0, 0.0, 0]
    ctrlPosOffset2=[0, 0.0, 0]
    ctrlPosOffset3=[0, 0.0, 0]


    falloffDefaults=(-10, -9.9, -3, 10.0)
    lowerRemovePointIndicies=[10, 11, 23, 35, 47, 48, 71, 73, 85, 97, 98, 121, 133, 145, 146, 158, 170, 193, 205, 206, 229, 239, 240, 251, 262, 273, 274, 295, 297, 308, 319, 320, 341, 352, 363, 364, 375, 386, 407, 418, 419, 440]
    upperRemovePointIndicies=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 34, 46, 58, 59, 160, 172, 217, 218, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 262, 273, 284, 285, 377, 388, 429, 430]

    if dog:
        fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/dogLipTest.ma"
        tierCount1 = 1
        tierCount2 = 5
        tierCount3 = 9

        ctrlSize1=2.3
        ctrlSize2=1.2
        ctrlSize3=.6
        ctrlAutoPositionThreshold = 0.9

        ctrlShapeOffset1=[0,0.0,2]
        ctrlShapeOffset2=[0,0.0,2]
        ctrlShapeOffset3=[0,0.0,2]
        
        falloffDefaults=(-10, -9.9, -4, 10.0)
        
        ctrlPosOffset1=[0, 0.0, 3]
        ctrlPosOffset2=[0, 0.0, 0]
        ctrlPosOffset3=[0, 0.0, 0]
        
        controlSpeedDefaults = [.025,.05,.05]
        lowerRemovePointIndicies=[]
        upperRemovePointIndicies=[]

    lowerLipSlide = lip.Lip(name="lowerLip",
                tierCount1=tierCount1,
                tierCount2=tierCount2,
                tierCount3=tierCount3,

                ctrlSize1=ctrlSize1,
                ctrlSize2=ctrlSize2,
                ctrlSize3=ctrlSize3,

                ctrlShapeOffset1=ctrlShapeOffset1,
                ctrlShapeOffset2=ctrlShapeOffset2,
                ctrlShapeOffset3=ctrlShapeOffset3,
                
                ctrlPosOffset1=ctrlPosOffset1,
                ctrlPosOffset2=ctrlPosOffset2,
                ctrlPosOffset3=ctrlPosOffset3,
                
                controlSpeedDefaults=controlSpeedDefaults,
                
                ctrlAutoPositionThreshold = ctrlAutoPositionThreshold,

                falloffDefaults=falloffDefaults,
                fileName=fileName,
                deformMesh="humanLipsLower",
                base="humanLipsLowerBase",
                projectionMesh="lowLipProjection",
                slidePatch="slide",
                slidePatchBase="slideBase")

    lip.Lip(name="lowerLipCurve",
            ctrlName = "lowerLip",
            #fileName=fileName,
            controlRivetMesh = "humanLipsLower",
            multiSlideForBaseCurve=False,
            repositionRivetCtrls=True,
            tierCount1=tierCount1,
            tierCount2=tierCount2,
            tierCount3=tierCount3,

            ctrlSize1=ctrlSize1,
            ctrlSize2=ctrlSize2,
            ctrlSize3=ctrlSize3,

            ctrlShapeOffset1=ctrlShapeOffset1,
            ctrlShapeOffset2=ctrlShapeOffset2,
            ctrlShapeOffset3=ctrlShapeOffset3,
            
            ctrlPosOffset1=ctrlPosOffset1,
            ctrlPosOffset2=ctrlPosOffset2,
            ctrlPosOffset3=ctrlPosOffset3,
            
            controlSpeedDefaults=controlSpeedDefaults,
            
            ctrlAutoPositionThreshold = .01,

            falloffDefaults=falloffDefaults,
            fileName=None,
            deformMesh="lowerLipCurve",
            base="lowerLipCurveBase",
            projectionMesh="lowLipProjection",
            slidePatch="slide",
            slidePatchBase="slideBase")

    lip.lipCurveDeformSplit(name="C_LowerLipWire",
                            curve="lowerLipCurve",
                            curveAim="lowerLipCurveAim",
                            deformedGeometry="humanLipsLower",
                            projectionPatch="lowLipProjection",
                            deformedGeometryBase="humanLipsLowerBase",
                            addWeightStack=["lowerLipWeightStack_LR", "lowerLipWeightStack_UD"],
                            addAtIndex=tierCount1+tierCount2+tierCount3,
                            handPaint=False,
                            upperLip=False,
                            reorderInFrontOfDeformer=lowerLipSlide,
                            removePointIndicies=lowerRemovePointIndicies,
                            falloffDefaults = "")



    falloffDefaults=(10, -1, -7, -10.0)


    upperLipSlide = lip.Lip(name="upperLip",
                tierCount1=tierCount1,
                tierCount2=tierCount2,
                tierCount3=tierCount3,

                ctrlSize1=ctrlSize1,
                ctrlSize2=ctrlSize2,
                ctrlSize3=ctrlSize3,

                ctrlShapeOffset1=ctrlShapeOffset1,
                ctrlShapeOffset2=ctrlShapeOffset2,
                ctrlShapeOffset3=ctrlShapeOffset3,
                
                ctrlPosOffset1=ctrlPosOffset1,
                ctrlPosOffset2=ctrlPosOffset2,
                ctrlPosOffset3=ctrlPosOffset3,
                
                controlSpeedDefaults=controlSpeedDefaults,
                
                ctrlAutoPositionThreshold = ctrlAutoPositionThreshold,

                falloffDefaults=falloffDefaults,
                fileName=None,
                deformMesh="humanLipsUpper",
                base="humanLipsUpperBase",
                projectionMesh="upLipProjection",
                slidePatch="slide",
                slidePatchBase="slideBase")

    lip.Lip(name="upperLipCurve",
            ctrlName = "upperLip",
            #fileName=fileName,
            controlRivetMesh = "humanLipsUpper",
            multiSlideForBaseCurve=False,
            repositionRivetCtrls=True,
            tierCount1=tierCount1,
            tierCount2=tierCount2,
            tierCount3=tierCount3,

            ctrlSize1=ctrlSize1,
            ctrlSize2=ctrlSize2,
            ctrlSize3=ctrlSize3,

            ctrlShapeOffset1=ctrlShapeOffset1,
            ctrlShapeOffset2=ctrlShapeOffset2,
            ctrlShapeOffset3=ctrlShapeOffset3,
            
            ctrlPosOffset1=ctrlPosOffset1,
            ctrlPosOffset2=ctrlPosOffset2,
            ctrlPosOffset3=ctrlPosOffset3,
            
            controlSpeedDefaults=controlSpeedDefaults,
            
            ctrlAutoPositionThreshold = .01,

            falloffDefaults=falloffDefaults,
            fileName=None,
            deformMesh="upperLipCurve",
            base="upperLipCurveBase",
            projectionMesh="upLipProjection",
            slidePatch="slide",
            slidePatchBase="slideBase")

    lip.lipCurveDeformSplit(name="C_UpperLipWire",
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
                            reorderInFrontOfDeformer=upperLipSlide,
                            falloffDefaults = "")

