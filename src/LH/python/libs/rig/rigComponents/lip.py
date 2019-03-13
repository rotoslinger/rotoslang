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
# reload(deformerUtils)
# reload(base)

def Lip(name="lowerLip",
             tierCount1=1,
             tierCount2=3,
             tierCount3=9,

             ctrlSize1=1,
             ctrlSize2=.65,
             ctrlSize3=.35,

             ctrlShapeOffset1=[0,0.0,2],
             ctrlShapeOffset2=[0,0.0,2],
             ctrlShapeOffset3=[0,0.0,2],

             ctrlAutoPositionThreshold = .9,

             ctrlPosOffset1=[0, 0.0, 0],
             ctrlPosOffset2=[0, 0.0, 0],
             ctrlPosOffset3=[0, 0.0, 0],

             controlSpeedDefaults = [.1,.1,.1],

             controlAutoOrientMesh="slide",

             falloffDefaults=(-10, -9.9, -4, 10.0),
             fileName="/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/humanLipTest.ma",
             deformMesh="humanLipsLower",
             base="humanLipsLowerBase",
             projectionMesh="lowLipProjection",
             slidePatch="slide",
             slidePatchBase="slideBase"):
    if fileName:
        cmds.file( fileName, o=True, f=True )


    control = cmds.circle(n= name + "Control", nr=[0,1,0])[0]

    slideUD = slideSimple.SlideSimple(name + "LipSlide", geoToDeform=deformMesh, slidePatch=slidePatch, slidePatchBase=slidePatchBase, baseGeoToDeform=base)
    slideUD.create()

    autoCreateTimeRange = 20.0
    offset=0
    centerWeight = .6
    outerWeight = .0
    angle = 50
    nudge = -0.0
    intermediateVal = .0
    intermediateAngle=0

    lastAngle = 50
    lastIntermediateVal=.8
    lastIntermediateAngle=30

    # createNum1 = 3
    # createNum2 = 9
    # createNum3 = 7
    curveWeights = weightStack.AnimCurveWeight(name=name + "CurveWeights",
                                        baseGeo=base,
                                        ctrlNode=control,
                                        projectionGeo=projectionMesh,
                                        weightAttrNames=[],
                                        addNewElem=False,
                                        autoCreateAnimCurves = True,
                                        autoCreateName = name + "Primary",
                                        singleFalloffName = name,
                                        autoCreateNum = tierCount1,
                                        falloffDefaults=falloffDefaults,
                                        autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal,lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,
                                        #autoCreateTimeRange = 20.0, offset=.0, centerWeight = .4, outerWeight = .6, angle = 0, nudge = -0.03

    )
    curveWeights.create()


    stack = weightStack.WeightStack(name=name + "WeightStack",
                                    geoToWeight=base,
                                    ctrlNode=control,
                                    weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                    addNewElem=False,
                                    # outputAttrs = ["cluster1.weightList[0]"],
                                    # outputAttrs_LR = ["cluster2.weightList[0]"],
                                    outputAttrs = [slideUD.deformer + ".weightArrays[0].vWeights"],
                                    outputAttrs_LR = [slideUD.deformer + ".weightArrays[0].uWeights"],
                                    autoCreate=True,
                                    controlPositionByWeightsThreshold=ctrlAutoPositionThreshold,
                                    controlPositionOffset=ctrlPosOffset1,
                                    controlRivetMesh = deformMesh,
                                    controlAutoOrientMesh=controlAutoOrientMesh,
                                    controlRivetAimMesh=slidePatch,
                                    controlSpeedDefaults = controlSpeedDefaults,
                                    connectFalloff = False,
                                    isOutputKDoubleArray=True,
                                    # falloffCurveWeightNode="TestCurveWeights",
                                    autoCreateName=name + "Primary",
                                    controlSize = ctrlSize1,
                                    controlOffset = ctrlShapeOffset1,
                                    )
    stack.create()
    position = cmds.xform(stack.controls[0], q=True, t=True)
    curveWeights.setFalloffDefaults()
    matDef = matrixDeformer.MatrixDeformer(name=name + "MatrixDeformer1",
                                    geoToDeform=deformMesh,
                                    # parent=stack.controls,
                                    centerToParent=True,
                                    addAtIndex=0,
                                    numToAdd=1,
                                    locatorName=name + "Primary",
                                    rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    curveWeightsConnectionIdx=0,
                                    translations = stack.positionsFromWeights,
                                    rotations = stack.rotationsFromWeights,

                                    # locations=[position],
                                    hide = True)
    matDef.create()
#######################################################################################################################################
    autoCreateTimeRange = 20.0
    offset=0
    centerWeight = .3
    outerWeight = .5
    angle = 0
    nudge = -0.14
    intermediateVal = .0
    intermediateAngle=0

    lastAngle = 60
    lastIntermediateVal=.8
    lastIntermediateAngle=30

    curveWeights = weightStack.AnimCurveWeight(name=name + "CurveWeights",
                                        baseGeo=base,
                                        ctrlNode=control,
                                        projectionGeo=projectionMesh,
                                        weightAttrNames=[],
                                        addNewElem=True,
                                        autoCreateAnimCurves = True,
                                        autoCreateName = name + "Secondary",
                                        singleFalloffName = name,
                                        autoCreateNum = tierCount2,
                                        autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal,lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,
                                        #autoCreateTimeRange = 20.0, offset=.0, centerWeight = .4, outerWeight = .6, angle = 0, nudge = -0.03
                                        startElem = tierCount1,

    )
    curveWeights.create()


    stack = weightStack.WeightStack(name=name + "WeightStack",
                                    geoToWeight=base,
                                    ctrlNode=control,
                                    weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                    addNewElem=True,
                                    outputAttrs = [slideUD.deformer + ".weightArrays[0].vWeights"],
                                    outputAttrs_LR = [slideUD.deformer + ".weightArrays[0].uWeights"],
                                    autoCreate=True,
                                    controlPositionByWeightsThreshold=ctrlAutoPositionThreshold,
                                    controlPositionOffset=ctrlPosOffset2,
                                    controlRivetMesh = deformMesh,
                                    controlAutoOrientMesh=controlAutoOrientMesh,
                                    controlRivetAimMesh=slidePatch,
                                    controlSpeedDefaults = controlSpeedDefaults,
                                    falloffCurveWeightNode=name + "CurveWeights",
                                    autoCreateName = name + "Secondary",
                                    isOutputKDoubleArray=True,
                                    controlSize = ctrlSize2,
                                    controlOffset = ctrlShapeOffset2,
                                    falloffElemStart = tierCount1
                                    )
    stack.create()
    curveWeights.setFalloffDefaults()

    matDef = matrixDeformer.MatrixDeformer(name=name + "MatrixDeformer2",
                                    geoToDeform=deformMesh,
                                    # parent=stack.controls,
                                    # parent=stack.controls,
                                    centerToParent=True,
                                    addAtIndex=0,
                                    numToAdd=tierCount2,
                                    locatorName= name + "Secondary",
                                    rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    curveWeightsConnectionIdx=tierCount1,
                                    translations = stack.positionsFromWeights,
                                    rotations = stack.rotationsFromWeights,
                                    hide = True)
    matDef.create()
    # quit()
    #############################################################################################################################
    curveWeights = weightStack.AnimCurveWeight(name=name + "CurveWeights",
                                        baseGeo=base,
                                        ctrlNode=control,
                                        projectionGeo=projectionMesh,
                                        weightAttrNames=[],
                                        addNewElem=True,
                                        autoCreateAnimCurves = True,
                                        autoCreateName = name + "Tertiary",
                                        singleFalloffName = name,
                                        autoCreateNum = tierCount3,
                                        autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal,lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,
                                        #autoCreateTimeRange = 20.0, offset=.0, centerWeight = .4, outerWeight = .6, angle = 0, nudge = -0.03
                                        startElem = tierCount2 + tierCount1,

    )
    curveWeights.create()


    stack = weightStack.WeightStack(name=name + "WeightStack",
                                    geoToWeight=base,
                                    ctrlNode=control,
                                    weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                    addNewElem=True,
                                    outputAttrs = [slideUD.deformer + ".weightArrays[0].vWeights"],
                                    outputAttrs_LR = [slideUD.deformer + ".weightArrays[0].uWeights"],
                                    autoCreate=True,
                                    controlPositionByWeightsThreshold=ctrlAutoPositionThreshold,
                                    controlPositionOffset=ctrlPosOffset3,
                                    controlRivetMesh = deformMesh,
                                    controlAutoOrientMesh=controlAutoOrientMesh,
                                    controlRivetAimMesh=slidePatch,
                                    controlSpeedDefaults = controlSpeedDefaults,
                                    falloffCurveWeightNode=name + "CurveWeights",
                                    autoCreateName=name + "Tertiary",
                                    isOutputKDoubleArray=True,
                                    controlSize = ctrlSize3,
                                    controlOffset = ctrlShapeOffset3,
                                    falloffElemStart = tierCount2 + tierCount1
                                    )
    stack.create()
    curveWeights.setFalloffDefaults()

    matDef = matrixDeformer.MatrixDeformer(name=name + "MatrixDeformer3",
                                    geoToDeform=deformMesh,
                                    # parent=stack.controls,
                                    centerToParent=True,
                                    addAtIndex=0,
                                    numToAdd=tierCount3,
                                    locatorName=name + "Tertiary",
                                    rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    curveWeightsConnectionIdx=tierCount2 + tierCount1,
                                    translations = stack.positionsFromWeights,
                                    rotations = stack.rotationsFromWeights,
                                    hide = True)
    matDef.create()
    cmds.setAttr(slideUD.deformer + ".cacheBind",1)