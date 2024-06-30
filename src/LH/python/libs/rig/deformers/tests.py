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
# reload(deformerUtils)
# reload(base)

def faceTest():
    print()
    weightStack
    fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/Prototype/LipPrototype.ma"

    # fileName = "/scratch/levih/dev/rotoslang/src/scenes/presentation/TestCurveWeights.ma"
    cmds.file( fileName, o=True, f=True )









    deformMesh="C_lowLips_HI"
    base="C_lowLipsBase_HI"
    projectionMesh="RigGeo_C_mouthWeightPatch_EX"
    slidePatch="RigGeo_C_mouthSurface_EX"
    slidePatchBase="RigGeo_C_mouthSurfaceBase_EX"





    #cmds.file(new=True, f=True)
    control = cmds.circle(n="Control", nr=[0,1,0])[0]
    subdivisions = 30
    # deformMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2, sx=subdivisions,  n="deformMesh")[0]
    cluster = cmds.cluster(deformMesh)[1]
    cmds.move(1, cluster, y=True)
    # base = cmds.polyPlane(ax=[0,0,1], h=2, w=2,sx=subdivisions, n="BASE")[0]
    cmds.setAttr(base + ".v",0)
    # projectionMesh = cmds.polyPlane(ax=[0,0,1], h=2, w=2, sx=1,sy=1, n="projectionMesh")[0]
    cmds.setAttr(projectionMesh + ".v",0)
    cluster2 = cmds.cluster(deformMesh)[1]
    cmds.move(1, cluster2, x=True)

    # cmds.move(2, projectionMesh, z=True)


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

    createNum1 = 3
    createNum2 = 9
    createNum3 = 7

    curveWeights = weightStack.AnimCurveWeight(name="TestCurveWeights",
                                               baseGeo=base,
                                               ctrlNode=control,
                                               projectionGeo=projectionMesh,
                                               weightAttrNames=[],
                                               addNewElem=False,
                                               autoCreateAnimCurves = True,
                                               autoCreateName = "lipSingle",
                                               singleFalloffName = "lip",
                                               autoCreateNum = 1,
                                               autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal, lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,
                                               #autoCreateTimeRange = 20.0, offset=.0, centerWeight = .4, outerWeight = .6, angle = 0, nudge = -0.03

                                               )
    curveWeights.create()


    stack = weightStack.WeightStack(name="TestWeights",
                                    geoToWeight=base,
                                    ctrlNode=control,
                                    weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                    addNewElem=False,
                                    outputAttrs = ["cluster1.weightList[0]"],
                                    outputAttrs_LR = ["cluster2.weightList[0]"],
                                    autoCreate=True,
                                    controlRivetMesh = deformMesh,
                                    connectFalloff = False,
                                    # falloffCurveWeightNode="TestCurveWeights",
                                    autoCreateName="lipSingle",
                                    controlSize = .4,
                                    controlOffset = [0,0.0,.7],
                                    )
    stack.create()
    position = cmds.xform(stack.controls[0], q=True, t=True)
    curveWeights.setFalloffDefaults()
    # cmds.refresh()
    # position = cmds.xform(stack.controls[0], q=True, t=True)
    
    # print "POSITION", position, stack.controls[0]
    # print "POSITION", position, stack.controls[0]

    # print "POSITION", position
    # print "POSITION", position
    # print "POSITION", position
    # print "POSITION", position
    matDef = matrixDeformer.MatrixDeformer(name="testMatrixDeformer",
                                    geoToDeform=deformMesh,
                                    # parent=stack.controls,
                                    centerToParent=True,
                                    addAtIndex=0,
                                    numToAdd=1,
                                    locatorName="test",
                                    rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    curveWeightsConnectionIdx=0,
                                    locations=stack.positionsFromWeights,
                                    # locations=[position],
                                    hide = True)
    matDef.create()
    

    # cmds.setAttr(matDef.deformer+".multiThread",0)


    #cmds.setAttr("C_lipSingle_CTL.ty", -0.6)
    #cmds.setAttr("C_lipPrime_CTL.ty", 0.30)

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

    #@createNum1 = 3
    #createNum2 = 15
    #createNum3 = 12


    curveWeights = weightStack.AnimCurveWeight(name="TestCurveWeights",
                                               baseGeo=base,
                                               ctrlNode=control,
                                               projectionGeo=projectionMesh,
                                               weightAttrNames=[],
                                               addNewElem=True,
                                               autoCreateAnimCurves = True,
                                               autoCreateName = "lipPrime",
                                               singleFalloffName = "lip",
                                               autoCreateNum = createNum1,
                                               autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal, lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,
                                               #autoCreateTimeRange = 20.0, offset=.0, centerWeight = .4, outerWeight = .6, angle = 0, nudge = -0.03
                                               startElem = 1,

                                               )
    curveWeights.create()


    stack = weightStack.WeightStack(name="TestWeights",
                                    geoToWeight=base,
                                    ctrlNode=control,
                                    weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                    addNewElem=True,
                                    outputAttrs = ["cluster1.weightList[0]"],
                                    outputAttrs_LR = ["cluster2.weightList[0]"],
                                    autoCreate=True,
                                    controlRivetMesh = deformMesh,
                                    falloffCurveWeightNode="TestCurveWeights",
                                    autoCreateName="lipPrime",
                                    controlSize = .3,
                                    controlOffset = [0,0.0,.7],
                                    falloffElemStart = 1
                                    )
    stack.create()
    curveWeights.setFalloffDefaults()

    matDef = matrixDeformer.MatrixDeformer(name="testMatrixDeformer",
                                    geoToDeform=deformMesh,
                                    # parent=stack.controls,
                                    # parent=stack.controls,
                                    centerToParent=True,
                                    addAtIndex=1,
                                    numToAdd=3,
                                    locatorName="test",
                                    rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    curveWeightsConnectionIdx=1,
                                    locations=stack.positionsFromWeights,
                                    hide = True)
    matDef.create()


    #cmds.setAttr("L_lipPrime00_CTL.ty", 0.6)
    #cmds.setAttr("C_lipPrime_CTL.ty", 0.30)

    #############################################################################################################################
    #autoCreateTimeRange = 20.0
    #offset=0
    #centerWeight = .3
    #outerWeight = .2
    #angle = 0
    #centerWeight = .6
    #outerWeight = .0
    #angle = 50
    #nudge = -0.0

    #lastAngle = 50



    curveWeights = weightStack.AnimCurveWeight(name="TestCurveWeights",
                                               baseGeo=base,
                                               ctrlNode=control,
                                               projectionGeo=projectionMesh,
                                               weightAttrNames=[],
                                               addNewElem=True,
                                               autoCreateAnimCurves = True,
                                               autoCreateName = "lipSecondary",
                                               singleFalloffName = "lip",
                                               autoCreateNum = createNum2,
                                               autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal, lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,
                                               #autoCreateTimeRange = 20.0, offset=.0, centerWeight = .4, outerWeight = .6, angle = 0, nudge = -0.03
                                               startElem = 4,

                                               )
    curveWeights.create()


    stack = weightStack.WeightStack(name="TestWeights",
                                    geoToWeight=base,
                                    ctrlNode=control,
                                    weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                    addNewElem=True,
                                    outputAttrs = ["cluster1.weightList[0]"],
                                    outputAttrs_LR = ["cluster2.weightList[0]"],
                                    autoCreate=True,
                                    controlRivetMesh = deformMesh,
                                    falloffCurveWeightNode="TestCurveWeights",
                                    autoCreateName="lipSecondary",
                                    controlSize = .1,
                                    controlOffset = [0,0.2,.7],
                                    falloffElemStart = 4
                                    )
    stack.create()
    curveWeights.setFalloffDefaults()

    matDef = matrixDeformer.MatrixDeformer(name="testMatrixDeformer",
                                    geoToDeform=deformMesh,
                                    # parent=stack.controls,
                                    centerToParent=True,
                                    addAtIndex=4,
                                    numToAdd=9,
                                    locatorName="test",
                                    rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    curveWeightsConnectionIdx=4,
                                    locations=stack.positionsFromWeights,
                                    hide = True)
    matDef.create()
