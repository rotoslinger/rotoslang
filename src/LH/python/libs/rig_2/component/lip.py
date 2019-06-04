
from maya import cmds
import maya.OpenMaya as OpenMaya
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"
win = "C:\\Users\\harri\\Desktop\\dev\\rotoslang\\src\\LH\\python\\libs"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win32" in os:
    os = win

if os not in sys.path:
    sys.path.append(os)

linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"
win = "C:\\Users\\harri\\Desktop\\dev\\rotoslang\\src\\LH\\python\\libs\\rig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win32" in os:
    os = win

if os not in sys.path:
    sys.path.append(os)
from rig.utils import weightMapUtils
from rig.utils import misc
from rig.deformers import base
from rig.deformers import weightStack
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
reload(weightStack)
reload(base)

def build(tierCount1=1,
              tierCount2=3,
              tierCount3=5,
              order_before_deformer=None):

    slidePatch="C_mouthGuide_SLDE"
    slidePatchBase="C_mouthGuide_SLDEBASE"
    controlAutoOrientMesh ="C_mouthGuide_SLDE"

    # Upper Mesh Defaults
    deformMeshUpper="C_upperLip"
    baseUpper="C_upperLipBase"
    
    projectionMeshUpper="C_upLipSimplePkg_PRJ"
    
    deformMeshUpperCurve="C_upperLipVolume_CRV"
    baseUpperCurve="C_upperLipVolume_CRVBASE"
    
    upperCurve ="C_upperLipVolume_CRV"
    upperCurveAim ="C_upperLipVolume_CRV"
    
    rollCurveNameUpper = "C_upperLipRoll_CRV"
    rollFalloffCurveUpper = elements.UPPER_LIP_ROLL_FALLOFF
    
    # Lower Mesh Defaults
    deformMeshLower="C_lowerLip"
    baseLower="C_lowerLipBase"
    
    projectionMeshLower="C_lowLipSimplePkg_PRJ"
    
    deformMeshLowerCurve="C_lowerLipVolume_CRV"
    baseLowerCurve="C_lowerLipVolume_CRVBASE"
    
    lowerCurve ="C_lowerLipVolume_CRV"
    lowerCurveAim ="C_lowerLipVolume_CRV"
    
    rollCurveNameLower = "C_lowerLipRoll_CRV"
    rollFalloffCurveLower = elements.LOWER_LIP_ROLL_FALLOFF


    
    lowerRemovePointIndicies=[8, 10, 15, 16, 17, 39, 44, 45, 70, 71, 78, 79, 80, 82, 84, 85, 86, 90, 92, 93, 94, 95, 96, 97, 98, 99, 106, 107, 116, 124, 125, 133, 134, 135, 157, 162, 163, 188, 189, 196, 197, 198, 200, 202, 203, 204, 208, 210, 211, 212, 213, 214, 215, 216, 217, 224, 225, 234, 242, 243]

    upperRemovePointIndicies=[11, 12, 29, 32, 40, 44, 45, 48, 71, 75, 76, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 123, 125, 133, 148, 161, 164, 172, 176, 177, 180, 203, 207, 208, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 255, 257, 265, 280]










    slideCtrlSize1=1
    slideCtrlSize2=.7
    slideCtrlSize3=.4
    slideControlSpeedDefaults = [.1,.1,.1]

    ctrlAutoPositionThreshold = 0.6

    thickToPoint = (0, -0.97, 0.244)

    slideCtrlShapeOffset1=[0,0.0,1]
    slideCtrlShapeOffset2=[0,0.0,1]
    slideCtrlShapeOffset3=[0,0.0,1]

    slideCtrlPosOffset1=[0, 0.0, 0]
    slideCtrlPosOffset2=[0, 0.0, 0]
    slideCtrlPosOffset3=[0, 0.0, 0]

    thickCtrlSize1=.7
    thickCtrlSize2=.65
    thickCtrlSize3=.35

    thickCtrlShapeOffset1 = [ 0, -2, 3]
    thickCtrlShapeOffset2 = [0,-2.0,1]
    thickCtrlShapeOffset3 = [0,-2.0,1]

    falloffDefaults=(-10, -9.9, -3, 10.0)
    falloffMatrixDefaults=(-11, -7, -2, 10.0)

    matDefCtrlSize1=.5
    matDefCtrlSize2=.5
    matDefCtrlSize3=.5

    matDefCtrlShapeOffset1=[0,-1.0,1]
    matDefCtrlShapeOffset2=[0,-1.0,1]
    matDefCtrlShapeOffset3=[0,-1.0,1]

    #Uppers
    falloffDefaultsUpper=(10, -1, -7, -10.0)
    falloffMatrixDefaultsUpper=(10, -1, -9, -10.0)

    matDefCtrlShapeOffset1Upper=[0,1.0,1]
    matDefCtrlShapeOffset2Upper=[0,1.0,1]
    matDefCtrlShapeOffset3Upper=[0,1.0,1]

    thickToPointUpper = (0, 0.953, 0.303)

    thickCtrlShapeOffset1Upper=[0, 2.0, 3]
    thickCtrlShapeOffset2Upper=[0, 2.0, 1]
    thickCtrlShapeOffset3Upper=[0, 2.0, 1]

    thickFalloffCurveUpper = elements.UPPER_LIP_THICK_FALLOFF
    matDefFalloffCurve = elements.LOWER_LIP_MATDEF_FALLOFF

    matDefFalloffCurveUpper = elements.UPPER_LIP_MATDEF_FALLOFF


    lowerLipClass = lip.Lip(name="lowerLip",
                upperLip=False,
                tierCount1=tierCount1,
                tierCount2=tierCount2,
                tierCount3=tierCount3,
                thickToPoint=thickToPoint,
                slideCtrlSize1=slideCtrlSize1,
                slideCtrlSize2=slideCtrlSize2,
                slideCtrlSize3=slideCtrlSize3,

                matDefCtrlSize1=matDefCtrlSize1,
                matDefCtrlSize2=matDefCtrlSize2,
                matDefCtrlSize3=matDefCtrlSize3,
                matDefFalloffCurve = matDefFalloffCurve,
                rollCurveName = rollCurveNameLower,

                rollFalloffCurve = rollFalloffCurveLower,


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

                thickCtrlSize1=thickCtrlSize1,
                thickCtrlSize2=thickCtrlSize2,
                thickCtrlSize3=thickCtrlSize3,


                thickCtrlShapeOffset1=thickCtrlShapeOffset1,
                thickCtrlShapeOffset2=thickCtrlShapeOffset2,
                thickCtrlShapeOffset3=thickCtrlShapeOffset3,
                
                falloffDefaults=falloffDefaults,
                falloffMatrixDefaults=falloffMatrixDefaults,
                fileName=None,
                deformMesh=deformMeshLower,
                controlAutoOrientMesh = controlAutoOrientMesh,
                base=baseLower,
                projectionMesh=projectionMeshLower,
                slidePatch=slidePatch,
                slidePatchBase=slidePatchBase)
    lowerLipClass.create()
    lowerLipSlide, lowerLipThick = lowerLipClass.slide_deformer, lowerLipClass.vector_deformer



    lowerLipCurveClass = lip.Lip(name="lowerLipCurve",
            ctrlName = "lowerLip",
            order_before_deformer=order_before_deformer,
            controlRivetMesh = deformMeshLower,
            doLipThick = False,
            doLipRoll = False,
            upperLip=False,
            # multiSlideForBaseCurve=False,
            multiSlideForBaseCurve=False,
            # repositionRivetCtrls=True,
            repositionRivetCtrls=True,
            tierCount1=tierCount1,
            tierCount2=tierCount2,
            tierCount3=tierCount3,

            slideCtrlSize1=slideCtrlSize1,
            slideCtrlSize2=slideCtrlSize2,
            slideCtrlSize3=slideCtrlSize3,
            matDefCtrlSize1=matDefCtrlSize1,
            matDefCtrlSize2=matDefCtrlSize2,
            matDefCtrlSize3=matDefCtrlSize3,

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

            falloffDefaults=falloffDefaults,
            falloffMatrixDefaults=falloffMatrixDefaults,
            fileName=None,
            deformMesh=deformMeshLowerCurve,
            base=baseLowerCurve,
            controlAutoOrientMesh = controlAutoOrientMesh,
            # deformMesh=lowerCurve,
            # base="lowerLipCurveBase",
            projectionMesh=projectionMeshLower,
            slidePatch=slidePatch,
            slidePatchBase=slidePatchBase)

    lowerLipCurveClass.create()
    # cmds.reorderDeformers(lowerLipSlide, lowerLipThick, misc.getShape(deformMeshLower))


    lip.lipCurveDeformSplit(name="C_LowerLipWire",
                            # curveDeformerAlgorithm=1,
                            curve=lowerCurve,
                            curveAim=lowerCurveAim,
                            deformedGeometry=deformMeshLower,
                            projectionPatch=projectionMeshLower,
                            deformedGeometryBase=baseLower,
                            addWeightStack=["lowerLipWeightStack_LR", "lowerLipWeightStack_UD"],
                            addAtIndex=tierCount1+tierCount2+tierCount3,
                            handPaint=False,
                            upperLip=False,
                            reorderInFrontOfDeformer=lowerLipSlide,
                            removePointIndicies=lowerRemovePointIndicies,
                            falloffDefaults = "",
                            curve_base=baseLowerCurve)
    


    # falloffDefaultsUpper=(10, -1, -7, -10.0)
    # falloffMatrixDefaultsUpper=(10, -1, -9, -10.0)

    # matDefCtrlShapeOffset1Upper=[0,1.0,2]
    # matDefCtrlShapeOffset2Upper=[0,1.0,1]
    # matDefCtrlShapeOffset3Upper=[0,1.0,1]

    # thickToPointUpper = (0, 0.978, -0.208)

    # thickCtrlShapeOffset1Upper=[0, 2.0, 2]
    # thickCtrlShapeOffset2Upper=[0, 2.0, 1]
    # thickCtrlShapeOffset3Upper=[0, 2.0, 1]


    # thickFalloffCurveUpper = elements.UPPER_LIP_THICK_FALLOFF

    # upperLipSlide, upperLipThick = lip.Lip(name="upperLip",
    upperLipClass = lip.Lip(name="upperLip",
                upperLip=True,
                tierCount1=tierCount1,
                tierCount2=tierCount2,
                tierCount3=tierCount3,
                thickToPoint=thickToPointUpper,
                slideCtrlSize1=slideCtrlSize1,
                slideCtrlSize2=slideCtrlSize2,
                slideCtrlSize3=slideCtrlSize3,
                matDefCtrlSize1=matDefCtrlSize1,
                matDefCtrlSize2=matDefCtrlSize2,
                matDefCtrlSize3=matDefCtrlSize3,
                matDefFalloffCurve = matDefFalloffCurveUpper,

                slideCtrlShapeOffset1=slideCtrlShapeOffset1,
                slideCtrlShapeOffset2=slideCtrlShapeOffset2,
                slideCtrlShapeOffset3=slideCtrlShapeOffset3,
                
                slideCtrlPosOffset1=slideCtrlPosOffset1,
                slideCtrlPosOffset2=slideCtrlPosOffset2,
                slideCtrlPosOffset3=slideCtrlPosOffset3,
                
                slideControlSpeedDefaults=slideControlSpeedDefaults,

                thickCtrlSize1=thickCtrlSize1,
                thickCtrlSize2=thickCtrlSize2,
                thickCtrlSize3=thickCtrlSize3,

                thickCtrlShapeOffset1=thickCtrlShapeOffset1Upper,
                thickCtrlShapeOffset2=thickCtrlShapeOffset2Upper,
                thickCtrlShapeOffset3=thickCtrlShapeOffset3Upper,
                thickFalloffCurve=thickFalloffCurveUpper,

                matDefCtrlShapeOffset1=matDefCtrlShapeOffset1Upper,
                matDefCtrlShapeOffset2=matDefCtrlShapeOffset2Upper,
                matDefCtrlShapeOffset3=matDefCtrlShapeOffset3Upper,

                rollCurveName = rollCurveNameUpper,
                rollFalloffCurve = rollFalloffCurveUpper,

                ctrlAutoPositionThreshold = ctrlAutoPositionThreshold,

                falloffDefaults=falloffDefaultsUpper,
                falloffMatrixDefaults=falloffMatrixDefaultsUpper,
                fileName=None,
                deformMesh=deformMeshUpper,
                base=baseUpper,
                controlAutoOrientMesh = controlAutoOrientMesh,
                projectionMesh=projectionMeshUpper,
                slidePatch=slidePatch,
                slidePatchBase=slidePatchBase)
                
    upperLipClass.create()
    upperLipSlide, upperLipThick = upperLipClass.slide_deformer, upperLipClass.vector_deformer

    upperLipCurveClass = lip.Lip(name="upperLipCurve",
            ctrlName = "upperLip",
            order_before_deformer=order_before_deformer,

            upperLip=True,
            doLipThick = False,
            doLipRoll = False,
            #fileName=fileName,
            controlRivetMesh = deformMeshUpper,
            multiSlideForBaseCurve=False,
            repositionRivetCtrls=True,
            tierCount1=tierCount1,
            tierCount2=tierCount2,
            tierCount3=tierCount3,

            slideCtrlSize1=slideCtrlSize1,
            slideCtrlSize2=slideCtrlSize2,
            slideCtrlSize3=slideCtrlSize3,
            matDefCtrlSize1=matDefCtrlSize1,
            matDefCtrlSize2=matDefCtrlSize2,
            matDefCtrlSize3=matDefCtrlSize3,

            slideCtrlShapeOffset1=slideCtrlShapeOffset1,
            slideCtrlShapeOffset2=slideCtrlShapeOffset2,
            slideCtrlShapeOffset3=slideCtrlShapeOffset3,
            
            slideCtrlPosOffset1=slideCtrlPosOffset1,
            slideCtrlPosOffset2=slideCtrlPosOffset2,
            slideCtrlPosOffset3=slideCtrlPosOffset3,
            
            slideControlSpeedDefaults=slideControlSpeedDefaults,

            matDefCtrlShapeOffset1=matDefCtrlShapeOffset1Upper,
            matDefCtrlShapeOffset2=matDefCtrlShapeOffset2Upper,
            matDefCtrlShapeOffset3=matDefCtrlShapeOffset3Upper,

            ctrlAutoPositionThreshold = ctrlAutoPositionThreshold,

            falloffDefaults=falloffDefaultsUpper,
            falloffMatrixDefaults=falloffMatrixDefaultsUpper,
            fileName=None,
            deformMesh=deformMeshUpperCurve,
            base=baseUpperCurve,
            projectionMesh=projectionMeshUpper,
            controlAutoOrientMesh = controlAutoOrientMesh,
            slidePatch=slidePatch,
            slidePatchBase=slidePatchBase)
    upperLipCurveClass.create()
    # cmds.reorderDeformers(upperLipSlide, upperLipThick, misc.getShape(deformMeshUpper))

    blendshape = lip.lipCurveDeformSplit(name="C_UpperLipWire",
                                         curve=upperCurve,
                                        curveAim=upperCurveAim,
                                        deformedGeometry=deformMeshUpper,
                                        projectionPatch=projectionMeshUpper,
                                        deformedGeometryBase=baseUpper,
                                        addWeightStack=["upperLipWeightStack_LR", "upperLipWeightStack_UD"],
                                        addAtIndex=tierCount1+tierCount2+tierCount3,
                                        handPaint=False,
                                        upperLip=True,
                                        removePointIndicies=upperRemovePointIndicies,
                                        reorderInFrontOfDeformer=upperLipSlide,
                                        falloffDefaults = "",
                                        curve_base=baseUpperCurve
)
    cmds.select(upperLipCurveClass.mat_def_translate.controls)
    cmds.viewFit()



