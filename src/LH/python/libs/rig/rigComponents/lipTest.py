
from maya import cmds
import sys
import importlib
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
from rig_2.component.subcomponent import weightStack
from rig.deformers import matrixDeformer 
from rig.deformers import utils
from rig_2.component.subcomponent import lip_sub
from rig.rigComponents import line 
from rig.rigComponents import meshRivetCtrl
from rig.rigComponents import elements 
importlib.reload(line)
importlib.reload(elements)
importlib.reload(meshRivetCtrl)
importlib.reload(misc)
importlib.reload(weightMapUtils)
importlib.reload(lip_sub)
importlib.reload(utils)
importlib.reload(matrixDeformer)
importlib.reload(weightStack)
importlib.reload(base)

def test(reloadPlugin = False, auto_load=True):
    if reloadPlugin:
        cmds.file( new=True, f=True )

        # Linux
        # cmds.unloadPlugin("collision")
        # cmds.loadPlugin("/scratch/levih/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/CentOS-6.6_thru_8/mayaDevKit-2018.0/collision.so")
        # fileName="/scratch/levih/dev/rotoslang/src/scenes/presentation/FaceModelPackage/facePackageTweaks.ma"
    
        # Windows
        cmds.unloadPlugin("LHDeformerNodes")
        cmds.loadPlugin("C:/Users/harri/Desktop/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/src/Debug/LHDeformerNodes")
    fileName="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/presentation/FaceModelPackage/facePackageTweaks.ma"

    dog=False
    superman=False
    oldman=True

    tierCount1 = 1
    tierCount2 = 3
    tierCount3 = 5

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

    lowerRemovePointIndicies=[10, 11, 23, 35, 47, 48, 71, 73, 85, 97, 98, 121, 133, 145, 146, 158, 170, 193, 205, 206, 229, 239, 240, 251, 262, 273, 274, 295, 297, 308, 319, 320, 341, 352, 363, 364, 375, 386, 407, 418, 419, 440]
    upperRemovePointIndicies=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 34, 46, 58, 59, 160, 172, 217, 218, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 262, 273, 284, 285, 377, 388, 429, 430]

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




    slidePatch="faceModelPackage:slide"
    slidePatchBase="faceModelPackage:slideBase"
    controlAutoOrientMesh ="faceModelPackage:slide"


    # Lower Mesh Defaults
    deformMeshLower="faceModelPackage:humanLipsLower"
    baseLower="faceModelPackage:humanLipsLowerBase"
    projectionMeshLower="faceModelPackage:lowLipProjection"
    deformMeshLowerCurve=["faceModelPackage:lowerLipCurve", "faceModelPackage:lowerLipCurveAim"]
    baseLowerCurve=["faceModelPackage:lowerLipCurveBase", "faceModelPackage:lowerLipCurveAimBase"]
    lowerCurve ="faceModelPackage:lowerLipCurve"
    lowerCurveAim ="faceModelPackage:lowerLipCurveAim"
    rollCurveNameLower = "faceModelPackage:lowerLipCurveRollOuter"
    rollFalloffCurveLower = elements.LOWER_LIP_ROLL_FALLOFF

    # Upper Mesh Defaults
    deformMeshUpper="faceModelPackage:humanLipsUpper"
    baseUpper="faceModelPackage:humanLipsUpperBase"
    projectionMeshUpper="faceModelPackage:upLipProjection"
    deformMeshUpperCurve="faceModelPackage:upperLipCurve"
    baseUpperCurve="faceModelPackage:upperLipCurveBase"
    upperCurve ="faceModelPackage:upperLipCurve"
    upperCurveAim ="faceModelPackage:upperLipCurveAim"
    rollCurveNameUpper = "faceModelPackage:upperLipCurveRollOuter"
    rollFalloffCurveUpper = elements.UPPER_LIP_ROLL_FALLOFF

    rigGeo = "faceModelPackage:rigGeo"
    if dog:
        fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/dogLipTest.ma"
        tierCount1 = 1
        tierCount2 = 5
        tierCount3 = 11

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

    if superman:
        fileName = "/home/users/levih/Desktop/supermanFace/prototype/supermanLips.ma"
        tierCount1 = 1
        tierCount2 = 9
        tierCount3 = 5

        slideCtrlSize1=.1
        slideCtrlSize2=.07
        slideCtrlSize3=.04
        ctrlAutoPositionThreshold = 0.8

        slideCtrlShapeOffset1=[0,0.0,.07]
        slideCtrlShapeOffset2=[0,0.0,.07]
        slideCtrlShapeOffset3=[0,0.0,.07]
        
        falloffDefaults=(-10, -9.9, -4, 10.0)
        
        slideCtrlPosOffset1=[0, 0.0, 0]
        slideCtrlPosOffset2=[0, 0.0, 0]
        slideCtrlPosOffset3=[0, 0.0, 0]
        
        slideControlSpeedDefaults = [1,1,1]

        matDefCtrlSize1=.05
        matDefCtrlSize2=.05
        matDefCtrlSize3=.05

        matDefCtrlShapeOffset1=[0,-.1,.07]
        matDefCtrlShapeOffset2=[0,-.1,.07]
        matDefCtrlShapeOffset3=[0,-.1,.07]

        thickToPointUpper = (0, 0.913, 0.409)

        thickFalloffCurveUpper = elements.UPPER_LIP_THICK_FALLOFF

        #Uppers
        falloffDefaultsUpper=(10, -1, -7, -10.0)
        falloffMatrixDefaultsUpper=(10, -1, -9, -10.0)

        matDefCtrlShapeOffset1Upper=[0,.1,.07]
        matDefCtrlShapeOffset2Upper=[0,.1,.07]
        matDefCtrlShapeOffset3Upper=[0,.1,.07]


        #lowerRemovePointIndicies=[94, 95, 96, 98, 99, 100, 101, 102, 133, 135, 137, 153, 181, 238, 239, 240, 242, 243, 266, 288, 290, 292, 307, 322, 323, 324, 326, 327, 328, 329, 330, 332, 333, 334, 335, 337, 338, 339, 343, 367, 388, 389, 390, 527, 577, 588, 589, 590, 591, 593, 605, 606, 607, 608, 609, 732, 786, 787, 788, 789, 790, 791, 793, 795, 796, 797, 798, 799, 800, 826, 848, 849, 850, 987, 1034, 1045, 1046, 1048, 1049, 1050, 1062, 1063, 1064, 1065, 1066, 1185]

        #upperRemovePointIndicies=[1, 2, 74, 75, 76, 77, 81, 96, 97, 98, 101, 102, 105, 106, 108, 109, 110, 114, 122, 126, 127, 145, 147, 149, 153, 154, 155, 156, 158, 159, 160, 161, 163, 169, 170, 171, 176, 178, 179, 180, 200, 201, 244, 245, 254, 255, 259, 266, 267, 268, 271, 272, 275, 276, 278, 279, 280, 284, 292, 296, 297, 311, 316, 318, 324, 325, 326, 331, 333, 334, 335, 339, 341, 345, 346, 347, 348, 350, 351, 352, 361, 363, 364, 429, 430, 431, 432, 433, 434, 435, 436, 438, 439, 440, 441, 442, 443, 452, 453, 454, 455, 456, 457, 459, 460, 462, 463, 472, 473, 474, 475, 476, 477, 479, 480, 482, 483, 484, 507, 508, 576, 577, 579, 588, 590, 591, 592, 593, 595, 603, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 646, 647, 648, 658, 659, 660, 661, 662, 663, 664, 665, 667, 675, 676, 677, 697, 698, 699, 701, 702, 703, 704, 715, 716, 717, 718, 719, 720, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 752, 753, 754, 756, 757, 763, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 846, 847, 849, 851, 909, 910, 911, 912, 913, 914, 915, 917, 918, 919, 920, 921, 922, 923, 932, 933, 934, 936, 937, 938, 939, 940, 942, 943, 952, 953, 954, 955, 956, 957, 959, 960, 962, 963, 964, 987, 988, 1056, 1057, 1059, 1068, 1069, 1071, 1073, 1074, 1075, 1083, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1128, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1146, 1147, 1155, 1156, 1157, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1195, 1196, 1197, 1198, 1199, 1200, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1232, 1233, 1234, 1236, 1237, 1243, 1303, 1304, 1305, 1306, 1307, 1308, 1309, 1310, 1311, 1312, 1325, 1326]

        # Lower Mesh Defaults
        projectionMeshLower="supermanLips_lipModelPackage_lowLipProjection"
        deformMeshLowerCurve=["supermanLips_lowerLipCurve", "supermanLips_lowerLipCurveAim"]
        baseLowerCurve=["supermanLips_lowerLipCurveBase", "supermanLips_lowerLipCurveAimBase"]
        lowerCurve = "supermanLips_lowerLipCurve"
        lowerCurveAim = "supermanLips_lowerLipCurveAim"
        deformMeshLower="humanLipsLower"
        baseLower="humanLipsLowerBase"
        rollCurveNameLower = "supermanLips_lowerLipCurveRollOuter"

        # Upper Mesh Defaults
        projectionMeshUpper="supermanLips_lipModelPackage_upLipProjection"
        deformMeshUpperCurve="supermanLips_upperLipCurve"
        baseUpperCurve="supermanLips_upperLipCurveBase"
        upperCurve = "supermanLips_upperLipCurve"
        upperCurveAim = "supermanLips_upperLipCurveAim"
        deformMeshUpper="humanLipsUpper"
        baseUpper="humanLipsUpperBase"

        slidePatch="supermanLips_lipModelPackage_slide"
        slidePatchBase="supermanLips_lipModelPackage_slideBase"
        controlAutoOrientMesh = "supermanLips_lipModelPackage_slide"
        rollCurveNameUpper = "supermanLips_upperLipCurveRollOuter"

        lowerRemovePointIndicies=[]
        upperRemovePointIndicies=[]

    if oldman:
        fileName = "C:/Users/harri/Desktop/dev/rotoslang/src/scenes/oldMan/faceRigPackage/lipsPackage.ma"

        deformMeshLower="FullBody:C_lowerLip"
        baseLower="FullBody:C_lowerLipBase"

        deformMeshUpper="FullBody:C_upperLip"
        baseUpper="FullBody:C_upperLipBase"
        lowerRemovePointIndicies=[8, 10, 15, 16, 17, 39, 44, 45, 70, 71, 78, 79, 80, 82, 84, 85, 86, 90, 92, 93, 94, 95, 96, 97, 98, 99, 106, 107, 116, 124, 125, 133, 134, 135, 157, 162, 163, 188, 189, 196, 197, 198, 200, 202, 203, 204, 208, 210, 211, 212, 213, 214, 215, 216, 217, 224, 225, 234, 242, 243]

        upperRemovePointIndicies=[11, 12, 29, 32, 40, 44, 45, 48, 71, 75, 76, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 123, 125, 133, 148, 161, 164, 172, 176, 177, 180, 203, 207, 208, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 255, 257, 265, 280]


    if auto_load:
        cmds.file( new=True, f=True )
        cmds.file( fileName, i=True, f=True )
        # rigGeo = "faceModelPackage:rigGeo"

        # delete history
        for i in [rigGeo, projectionMeshLower, deformMeshLowerCurve, baseLowerCurve, lowerCurve,
                    lowerCurveAim, deformMeshLower, baseLower, projectionMeshUpper,
                    deformMeshUpperCurve, baseUpperCurve, upperCurve, upperCurveAim,
                    deformMeshUpper, baseUpper, slidePatch, slidePatchBase, controlAutoOrientMesh]:
            if not type(i) == list and cmds.objExists(i):
                cmds.select(i, r=True)
                cmds.DeleteHistory(i)
                cmds.makeIdentity(i, apply=True, t=1, r=1, s=1, n=0, pn=1);

            elif type(i) == list:
                for x in i:
                    if cmds.objExists(x):
                        cmds.select(x, r=True)
                        cmds.DeleteHistory(i)
                        cmds.makeIdentity(x, apply=True, t=1, r=1, s=1, n=0, pn=1);


        # for i in [deformMeshLower,
        #             deformMeshUpper]:
        #     cmds.select(i, r=True)
        #     cmds.DeleteHistory(i)

    # lowerLipSlide, lowerLipThick = line.Line(name="lowerLip",
    lowerLipClass = line.Line(name="lowerLip",
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



    lowerLipCurveClass = line.Line(name="lowerLipCurve",
            ctrlName = "lowerLip",
            controlRivetMesh = deformMeshLower,
            doLipThick = False,
            doLipRoll = False,
            upperLip=False,
            # multiSlideForBaseCurve=False,
            multiSlideForBaseCurve=True,
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


    lip_sub.lipCurveDeformSplit(name="C_LowerLipWire",
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
                                falloffDefaults = "")
    


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
    upperLipClass = line.Line(name="upperLip",
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

    upperLipCurveClass = line.Line(name="upperLipCurve",
            ctrlName = "upperLip",
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

    blendshape = lip_sub.lipCurveDeformSplit(name="C_UpperLipWire",
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
                                             falloffDefaults = "")
    cmds.select(upperLipCurveClass.mat_def.controls)
    cmds.viewFit()



