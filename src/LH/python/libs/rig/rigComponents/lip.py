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
# reload(deformerUtils)
# reload(base)
from rig.utils import weightMapUtils, misc
reload(misc)
from rig.utils import LHCurveDeformerCmds
reload(LHCurveDeformerCmds)
from rig.rigComponents import meshRivetCtrl 
reload(meshRivetCtrl)

def Lip(name="lowerLip",
        characterName = "character",
        controlParent="C_control_GRP",
        rigParent="C_rig_GRP",
        ctrlName = None, # this will be used as a way to reuse controls between different components and deformers
        multiSlideForBaseCurve=False,
        tierCount1=1,
        tierCount2=3,
        tierCount3=9,
        ctrlSize1=1,
        ctrlSize2=.65,
        ctrlSize3=.35,

        ctrlShapeOffset1=[0,0.0,2],
        ctrlShapeOffset2=[0,0.0,2],
        ctrlShapeOffset3=[0,0.0,2],

        controlRivetMesh = None,

        ctrlAutoPositionThreshold = .9,

        ctrlPosOffset1=[0, 0.0, 0],
        ctrlPosOffset2=[0, 0.0, 0],
        ctrlPosOffset3=[0, 0.0, 0],

        controlSpeedDefaults = [.1,.1,.1],

        controlAutoOrientMesh="slide",
        repositionRivetCtrls=False,

        falloffDefaults=(-10, -9.9, -4, 10.0),
        fileName="/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/humanLipTest.ma",
        deformMesh="humanLipsLower",
        base="humanLipsLowerBase",
        projectionMesh="lowLipProjection",
        slidePatch="slide",
        slidePatchBase="slideBase"):
    if not ctrlName:
        ctrlName = name
    if fileName:
        cmds.file( fileName, i=True, f=True )

    if not controlRivetMesh:
        controlRivetMesh = deformMesh

    # Temporary, create character hierarchy
    if not (cmds.objExists("C_{0}_GRP".format(characterName))):
        misc.create_rig_hier(char_name=characterName)

    control = cmds.circle(n= name + "Control", nr=[0,1,0])[0]
    cmds.parent(control, controlParent)

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

    curveWeights = weightStack.AnimCurveWeight(name=name + "CurveWeights",
                                        baseGeo=base,
                                        ctrlNode=control,
                                        projectionGeo=projectionMesh,
                                        weightAttrNames=[],
                                        addNewElem=False,
                                        autoCreateAnimCurves = True,
                                        autoCreateName = ctrlName + "Primary",
                                        singleFalloffName = ctrlName,
                                        autoCreateNum = tierCount1,
                                        falloffDefaults=falloffDefaults,
                                        autoCreateTimeRange = autoCreateTimeRange, offset=offset, centerWeight = centerWeight, outerWeight = outerWeight, angle = angle, nudge = nudge, intermediateVal=intermediateVal,lastAngle=lastAngle, lastIntermediateVal=lastIntermediateVal, intermediateAngle=intermediateAngle, lastIntermediateAngle=lastIntermediateAngle,

    )
    curveWeights.create()

    outputAttrs = [slideUD.deformer + ".weightArrays[0].vWeights"]
    outputAttrs_LR = [slideUD.deformer + ".weightArrays[0].uWeights"]
    # super crappy implementation, this should be made more elegant ASAP
    if multiSlideForBaseCurve:
        outputAttrs = [slideUD.deformer + ".weightArrays[0].vWeights", slideUD.deformer + ".weightArrays[1].vWeights"]
        outputAttrs_LR = [slideUD.deformer + ".weightArrays[0].uWeights", slideUD.deformer + ".weightArrays[1].uWeights"]

    stack = weightStack.WeightStack(name=name + "WeightStack",
                                    geoToWeight=base,
                                    ctrlNode=control,
                                    weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                    addNewElem=False,
                                    # outputAttrs = ["cluster1.weightList[0]"],
                                    # outputAttrs_LR = ["cluster2.weightList[0]"],
                                    outputAttrs = outputAttrs,
                                    outputAttrs_LR = outputAttrs_LR,
                                    autoCreate=True,
                                    controlPositionWeightsThreshold=ctrlAutoPositionThreshold,
                                    controlPositionOffset=ctrlPosOffset1,
                                    controlRivetMesh = controlRivetMesh,
                                    controlAutoOrientMesh=controlAutoOrientMesh,
                                    controlRivetAimMesh=slidePatch,
                                    controlSpeedDefaults = controlSpeedDefaults,
                                    controlParent = controlParent,
                                    connectFalloff = False,
                                    isOutputKDoubleArray=True,
                                    # falloffCurveWeightNode="TestCurveWeights",
                                    autoCreateName=ctrlName + "Primary",
                                    controlSize = ctrlSize1,
                                    controlOffset = ctrlShapeOffset1,
                                    repositionRivetCtrls = repositionRivetCtrls,
                                    )
    stack.create()
    #position = cmds.xform(stack.controls[0], q=True, t=True)
    # curveWeights.setFalloffDefaults()
    matDef = matrixDeformer.MatrixDeformer(name=name + "MatrixDeformer1",
                                    geoToDeform=deformMesh,
                                    ctrlName=ctrlName + "MatrixDeformer1",
                                    centerToParent=True,
                                    addAtIndex=0,
                                    numToAdd=1,
                                    # offset=[0,0,1],
                                    locatorName=name + "Primary",
                                    rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    curveWeightsConnectionIdx=0,
                                    translations = stack.positionsFromWeights,
                                    rotations = stack.rotationsFromWeights,
                                    controlParent = stack.controls,
                                    rigParent = rigParent,

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
                                        autoCreateName = ctrlName + "Secondary",
                                        singleFalloffName = ctrlName,
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
                                    outputAttrs = outputAttrs,
                                    outputAttrs_LR = outputAttrs_LR,
                                    autoCreate=True,
                                    controlPositionWeightsThreshold=ctrlAutoPositionThreshold,
                                    controlPositionOffset=ctrlPosOffset2,
                                    controlRivetMesh = controlRivetMesh,
                                    controlAutoOrientMesh=controlAutoOrientMesh,
                                    controlRivetAimMesh=slidePatch,
                                    controlSpeedDefaults = controlSpeedDefaults,
                                    controlParent = controlParent,
                                    falloffCurveWeightNode=name + "CurveWeights",
                                    autoCreateName = ctrlName + "Secondary",
                                    isOutputKDoubleArray=True,
                                    controlSize = ctrlSize2,
                                    controlOffset = ctrlShapeOffset2,
                                    falloffElemStart = tierCount1,
                                    repositionRivetCtrls = repositionRivetCtrls,
                                    )
    stack.create()
    # curveWeights.setFalloffDefaults()

    matDef = matrixDeformer.MatrixDeformer(name=name + "MatrixDeformer2",
                                    geoToDeform=deformMesh,
                                    ctrlName=ctrlName + "MatrixDeformer2",
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
                                    controlParent = stack.controls,
                                    rigParent = rigParent,
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
                                        autoCreateName = ctrlName + "Tertiary",
                                        singleFalloffName = ctrlName,
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
                                    outputAttrs = outputAttrs,
                                    outputAttrs_LR = outputAttrs_LR,
                                    autoCreate=True,
                                    controlPositionWeightsThreshold=ctrlAutoPositionThreshold,
                                    controlPositionOffset=ctrlPosOffset3,
                                    controlRivetMesh = controlRivetMesh,
                                    controlAutoOrientMesh=controlAutoOrientMesh,
                                    controlRivetAimMesh=slidePatch,
                                    controlSpeedDefaults = controlSpeedDefaults,
                                    controlParent = controlParent,
                                    falloffCurveWeightNode=name + "CurveWeights",
                                    autoCreateName=ctrlName + "Tertiary",
                                    isOutputKDoubleArray=True,
                                    controlSize = ctrlSize3,
                                    controlOffset = ctrlShapeOffset3,
                                    falloffElemStart = tierCount2 + tierCount1,
                                    repositionRivetCtrls = repositionRivetCtrls,
                                    )
    stack.create()
    # curveWeights.setFalloffDefaults()

    matDef = matrixDeformer.MatrixDeformer(name=name + "MatrixDeformer3",
                                    geoToDeform=deformMesh,
                                    ctrlName=ctrlName + "MatrixDeformer3",
                                    centerToParent=True,
                                    addAtIndex=0,
                                    numToAdd=tierCount3,
                                    locatorName=name + "Tertiary",
                                    #rotationTranforms=stack.controls,
                                    curveWeightsNode=curveWeights.node,
                                    curveWeightsConnectionIdx=tierCount2 + tierCount1,
                                    translations = stack.positionsFromWeights,
                                    rotations = stack.rotationsFromWeights,
                                    controlParent = stack.controls,
                                    rigParent = rigParent,
                                    hide = True)
    matDef.create()
    cmds.setAttr(slideUD.deformer + ".cacheBind",1)
    return slideUD.deformer


def lipCurveDeformSplit(name="C_UpperLipWire",
                        curve="lipCurve",
                        curveAim="lipCurveAim",
                        deformedGeometry="humanLipsUpper",
                        projectionPatch="upLipProjection",
                        deformedGeometryBase="humanLipsUpperBase",
                        addWeightStack=["upperLipWeightStack_LR", "upperLipWeightStack_UD"],
                        addAtIndex=9,
                        handPaint=False,
                        upperLip=True,
                        falloffDefaults = "",
                        falloffItts = "",
                        falloffOtts = "",
                        removePointIndicies=[],
                        reorderInFrontOfDeformer="",
):

    if not falloffDefaults and upperLip:
        falloffDefaults = (-10, -9, -5, 20.0)
        falloffItts=["linear","linear","spline","linear"]
        falloffOtts=["linear","linear","linear","linear"]
    if not falloffDefaults and not upperLip:
        falloffDefaults = (20, 3.4, -1, -10)
        falloffItts=["linear","linear","linear","linear"]
        falloffOtts=["linear","linear","spline","linear"]
    blendshapeGeo = cmds.duplicate(deformedGeometry, n=name+"BlendshapeGeo")[0]
    cmds.setAttr(blendshapeGeo + ".visibility", 0)
    blendshape = blendshapeSimple.BlendshapeSimple(name = name + "ReverseBlendshape", geoToDeform=deformedGeometry, targetGeom=blendshapeGeo)
    blendshape.create()
    # Turn on Blending
    cmds.setAttr(blendshape.amountAttr, 1)
    blendshape = blendshape.deformer

    geoToWeight = deformedGeometryBase
    curveWeights = None
    weightMapAttrNames=[]
    if not handPaint:
        curveWeights = weightStack.AnimCurveWeight(name=name + "ReverseCurveDeformerAnimCurveWeights",
                                    baseGeo=deformedGeometryBase,
                                    ctrlNode=blendshapeGeo,
                                    projectionGeo=projectionPatch,
                                    weightAttrNames=[name + "CurveDeformerNormalize"],
                                    addNewElem=False,
                                    autoCreateAnimCurves = False,
                                    autoCreateName = '',
                                    singleFalloffName = '',
                                    autoCreateNum = None,
                                    falloffDefaults = falloffDefaults,
                                    uKeyframesAllOnes=True,
                                    falloffItts=falloffItts,
                                    falloffOtts=falloffOtts
        )
        curveWeights.create()
        cmds.getAttr(curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray")

        weightMapAttrNames=[curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray", curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray"]
    factorAttrNames = ["reverse", "dummy"]
    weightMapAttrNames=["reverseWeights", "dummyWeights"]


    stack = weightStack.WeightStack(name=name + "NormalizeCurveDeformerWeights",
                                    geoToWeight=geoToWeight,
                                    ctrlNode=blendshapeGeo,
                                    weightMapAttrNames=weightMapAttrNames,
                                    factorAttrNames = factorAttrNames,
                                    operationVals=[0,6],
                                    addNewElem=False,
                                    outputAttrs = [blendshape + ".targetWeights"],
                                    autoCreate=False,
                                    UDLR = False,
                                    createControl=False,
                                    isOutputKDoubleArray=True,
                                    )
    stack.create()

    cmds.setAttr(stack.ctrlNode + ".reverse", 1)
    cmds.setAttr(stack.ctrlNode + ".dummy", 1)

    geoToWeightShape = misc.getShape(stack.geoToWeight)

    cmds.connectAttr(curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray", stack.node+".inputs[0].inputWeights", f=True)
    cmds.connectAttr(curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray", stack.node+".inputs[1].inputWeights", f=True)

    for idx, attr in enumerate(addWeightStack):
        weightAttr = geoToWeightShape + ".reverseWeights"
        if not handPaint:
            weightAttr = curveWeights.node + ".outDoubleWeights[0].outWeightsDoubleArray"
        cmds.connectAttr(weightAttr, attr + ".inputs[{0}].inputWeights".format(addAtIndex))
        cmds.setAttr(attr + ".inputs[{0}].factor".format(addAtIndex), 1)
        cmds.setAttr(attr + ".inputs[{0}].operation".format(addAtIndex), 2)
    # Create curve deformer (TEMP)
    wire = cmds.wire(blendshapeGeo, wire=curve, dds=[(0),(100000)] , name=name + "WireDeformer")[0]
    if removePointIndicies:
        # first make sure to set the weights on the wire
        iterGeo = misc.getOMItergeo(blendshapeGeo)
        polyCount = iterGeo.count()
        defaultVals = [1.0 for x in range(polyCount)]
        #cmds.setAttr(wire + ".", defaultVals, type=dataType)
        for idx in range(polyCount):
            cmds.setAttr('{0}.weightList[0].weights[{1}]'.format(wire, polyCount), 1.0)
        for idx in removePointIndicies:
            cmds.setAttr('{0}.weightList[0].weights[{1}]'.format(wire, idx), 0.0)


    if reorderInFrontOfDeformer:
        cmds.reorderDeformers(reorderInFrontOfDeformer, blendshape, misc.getShape(deformedGeometry))
    # LHCurveDeformerCmds.curveDeformerCmd(
    #                                     driverCurve = curve,
    #                                     aimCurve = curveAim,
    #                                     geom = [blendshapeGeo],
    #                                     ihi = 1,
    #                                     lockAttrs = 0,
    #                                     side='C',
    #                                     name=name + "CurveDeformer")




    #if removePointIndicies:

 