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





def Lip(name="lowerLip",
        characterName = "character",
        controlParent="C_control_GRP",
        rigParent="C_rig_GRP",
        upperLip = False,
        ctrlName = None,  # this will be used as a way to reuse controls between different components and deformers

        multiSlideForBaseCurve=False,

        tierCount1=1,
        tierCount2=3,
        tierCount3=9,

        falloffDefaults=(-10, -9.9, -4, 10.0),

        ################# Slides ########################

        falloffSlideName = None,
        slideCtrlSize1=1,
        slideCtrlSize2=.65,
        slideCtrlSize3=.35,

        slideCtrlShapeOffset1=[0,0.0,2],
        slideCtrlShapeOffset2=[0,0.0,2],
        slideCtrlShapeOffset3=[0,0.0,2],

        slideCtrlPosOffset1=[0, 0.0, 0],
        slideCtrlPosOffset2=[0, 0.0, 0],
        slideCtrlPosOffset3=[0, 0.0, 0],

        slideFalloffDefaults=(-10, -9.9, -4, 10.0),
        slideFalloffDefaultCurve = None,

        slideControlSpeedDefaults = [.1,.1,.1],

        ################# MatrixDeformers ###############
        falloffMatrixDeformerName = None,

        matDefCtrlSize1=1,
        matDefCtrlSize2=.65,
        matDefCtrlSize3=.35,

        matDefCtrlShapeOffset1=[0,0.0,2],
        matDefCtrlShapeOffset2=[0,0.0,2],
        matDefCtrlShapeOffset3=[0,0.0,2],

        matDefFalloffCurve=None,

        falloffMatrixDefaults=(-11, -7, -2, 10.0),
        falloffIttsMatDef=["linear","linear","linear","linear"],
        falloffOttsMatDef=["linear","spline","linear","linear"],

        ################# ThickDeformers ###############
        falloffLipThickName = None,
        thickCtrlSize1=.7,
        thickCtrlSize2=.65,
        thickCtrlSize3=.35,

        thickCtrlShapeOffset1 = [ 0, -2, 2],
        thickCtrlShapeOffset2 = [0,-2.0,1],
        thickCtrlShapeOffset3 = [0,-2.0,1],

        thickToPoint = (0, 0.978, -0.208),
        falloffThickDefaults=(10, -1, -4, 10.0),

        thickFalloffCurve = elements.LOWER_LIP_THICK_FALLOFF,

        ################ Pucker Deformer ####################
        falloffPuckerDefaults=(-10, -9.9, -4, 10.0),
        falloffLipPuckerName = None,


        ################ Curl Deformer ####################

        falloffLipCurlName = None,
        falloffCurlDefaults=(-10, -9.9, -4, 10.0),

        controlRivetMesh = None,
        ctrlAutoPositionThreshold = .9,


        controlAutoOrientMesh="slide",
        repositionRivetCtrls=False,

        fileName="/scratch/levih/dev/rotoslang/src/scenes/presentation/ForTransfer/humanLipTest.ma",
        deformMesh="humanLipsLower",
        base="humanLipsLowerBase",
        projectionMesh="lowLipProjection",
        slidePatch="slide",
        slidePatchBase="slideBase"):

    # if you want to share falloffs between all deformers leave the falloff names None, but more control is better...
    if not ctrlName:
        ctrlName = name

    if not falloffSlideName: # Falloff for lip slide should have a much more broad falloff compared to the rest
        falloffSlideName = ctrlName

    if not falloffMatrixDeformerName: # Falloff for lip the matrix deformer is going to be minimal because it is used for tweaks and puckers
        falloffMatrixDeformerName = ctrlName + "MATDEFTEST"

    if not falloffLipThickName: # Falloff for lip thick should be minimal
        falloffLipThickName = ctrlName + "LIPTHICK"

    if not falloffLipPuckerName: # Falloff for lip thick should be minimal
        falloffLipPuckerName = ctrlName

    if not falloffLipCurlName: # Falloff for lip curl may be more broad, but not as broad as the slide falloff
        falloffLipCurlName = ctrlName

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

    outputAttrs = [slideUD.deformer + ".weightArrays[0].vWeights"]
    outputAttrs_LR = [slideUD.deformer + ".weightArrays[0].uWeights"]
    # super crappy implementation, this should be made more elegant ASAP
    if multiSlideForBaseCurve:
        outputAttrs = [slideUD.deformer + ".weightArrays[0].vWeights", slideUD.deformer + ".weightArrays[1].vWeights"]
        outputAttrs_LR = [slideUD.deformer + ".weightArrays[0].uWeights", slideUD.deformer + ".weightArrays[1].uWeights"]
    # Loop Vars each divided into 3
    tierNames = ["Primary", "Secondary", "Tertiary"]
    tierCounts = [tierCount1, tierCount2, tierCount3]
    tierStartElemIdxs = [0, tierCount1, tierCount2 + tierCount1]
    tierAddAtIndex = [0, tierCount1, tierCount2 + tierCount1]
    isAddingNewElems = [False, True, True]
    slideCtrlShapeOffsets = [slideCtrlShapeOffset1, slideCtrlShapeOffset2, slideCtrlShapeOffset3]
    slideCtrlSizes = [slideCtrlSize1, slideCtrlSize2, slideCtrlSize3]
    matDefNames = ["MatrixDeformer1", "MatrixDeformer2", "MatrixDeformer3"]
    matDefCtrlShapeOffsets = [matDefCtrlShapeOffset1, matDefCtrlShapeOffset2, matDefCtrlShapeOffset3]
    matDefCtrlSizes = [matDefCtrlSize1, matDefCtrlSize2, matDefCtrlSize3]
    thickCtrlShapeOffsets = [thickCtrlShapeOffset1, thickCtrlShapeOffset2, thickCtrlShapeOffset3]
    thickCtrlSizes = [thickCtrlSize1, thickCtrlSize2, thickCtrlSize3 ]
    connectFalloffs = [False, True, True]
    falloffCurveWeightNodes= [None, name + "CurveWeights", name + "CurveWeights"]
    slideCtrlPosOffsets = [slideCtrlPosOffset1, slideCtrlPosOffset2, slideCtrlPosOffset3]
    centerWeights = [.6, .3, .3]
    outerWeights = [0, .5, .5]
    angles = [50, 0, 0]
    nudges = [0, -0.14, -0.14]
    lastAngles = [50, 60, 60]

    for idx in range(3):
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
                                            addNewElem=isAddingNewElems[idx],
                                            autoCreateAnimCurves = True,
                                            autoCreateName = ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                            singleFalloffName = ctrlName,
                                            autoCreateNum = tierCounts[idx],
                                            falloffDefaults=falloffDefaults,
                                            autoCreateTimeRange = autoCreateTimeRange,
                                            offset=offset,
                                            centerWeight = centerWeights[idx],
                                            outerWeight = outerWeights[idx],
                                            angle = angles[idx],
                                            nudge = nudges[idx],
                                            intermediateVal=intermediateVal,
                                            lastAngle=lastAngles[idx],
                                            lastIntermediateVal=lastIntermediateVal,
                                            intermediateAngle=intermediateAngle,
                                            lastIntermediateAngle=lastIntermediateAngle,

        )
        curveWeights.create()


        stack = weightStack.WeightStack(name=name + "WeightStack",
                                        geoToWeight=base,
                                        ctrlNode=control,
                                        weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                        addNewElem=isAddingNewElems[idx],
                                        outputAttrs = outputAttrs,
                                        outputAttrs_LR = outputAttrs_LR,
                                        autoCreate=True,
                                        controlPositionWeightsThreshold=ctrlAutoPositionThreshold,
                                        controlPositionOffset=slideCtrlPosOffsets[idx],
                                        controlRivetMesh = controlRivetMesh,
                                        controlAutoOrientMesh=controlAutoOrientMesh,
                                        controlRivetAimMesh=slidePatch,
                                        controlSpeedDefaults = slideControlSpeedDefaults,
                                        controlParent = controlParent,
                                        connectFalloff = connectFalloffs[idx],
                                        isOutputKDoubleArray=True,
                                        falloffCurveWeightNode=falloffCurveWeightNodes[idx], # If a weight node already exists, use it
                                        # falloffCurveWeightNode="TestCurveWeights",
                                        autoCreateName=ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                        controlSize = slideCtrlSizes[idx],
                                        controlShapeOffset = slideCtrlShapeOffsets[idx],
                                        repositionRivetCtrls = repositionRivetCtrls,
                                        )
        stack.create()

        ################################## MATRIX DEFORMER #####################################################################
        curveWeights = weightStack.AnimCurveWeight(name=name + "MatDef",
                                                    baseGeo=base,
                                                    ctrlNode=control,
                                                    projectionGeo=projectionMesh,
                                                    weightAttrNames=[],
                                                    addNewElem=isAddingNewElems[idx],
                                                    autoCreateAnimCurves = True,
                                                    autoCreateName = ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                                    singleFalloffName = falloffMatrixDeformerName,
                                                    autoCreateNum = tierCounts[idx],
                                                    falloffDefaults=falloffMatrixDefaults,
                                                    falloffItts=falloffIttsMatDef,
                                                    falloffOtts=falloffOttsMatDef,
                                                    autoCreateTimeRange = autoCreateTimeRange,
                                                    offset=offset,
                                                    centerWeight = centerWeights[idx],
                                                    outerWeight = outerWeights[idx],
                                                    angle = angles[idx],
                                                    nudge = nudges[idx],
                                                    intermediateVal=intermediateVal,
                                                    lastAngle=lastAngles[idx],
                                                    lastIntermediateVal=lastIntermediateVal,
                                                    intermediateAngle=intermediateAngle,
                                                    lastIntermediateAngle=lastIntermediateAngle,
                                                    startElem = tierAddAtIndex[idx],
        )
        curveWeights.create()

        print "ADD AT INDEX ", tierAddAtIndex[idx]
        print "TIER COUNT ", tierCounts[idx]

        matDef = matrixDeformer.MatrixDeformer(name=name + matDefNames[idx],
                                        geoToDeform=deformMesh,
                                        ctrlName=ctrlName + matDefNames[idx],
                                        centerToParent=True,
                                        addAtIndex=0,
                                        numToAdd=tierCounts[idx],
                                        # offset=[0,0,1],
                                        locatorName=name + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                        rotationTranforms=stack.controls,
                                        curveWeightsNode=curveWeights.node,
                                        
                                        curveWeightsConnectionIdx=tierAddAtIndex[idx],
                                        translations = stack.positionsFromWeights,
                                        rotations = stack.rotationsFromWeights,
                                        controlParent = stack.controls,
                                        rigParent = rigParent,
                                        offset = matDefCtrlShapeOffsets[idx],
                                        size = matDefCtrlSizes[idx],
                                        # locations=[position],
                                        hide = True)
        matDef.create()


    
        ################################## LIP THICK DEFORMER #####################################################################    
        curveWeights = weightStack.AnimCurveWeight(name=name + "ThickDef",
                                        baseGeo=base,
                                        ctrlNode=control,
                                        projectionGeo=projectionMesh,
                                        weightAttrNames=[],
                                        addNewElem=isAddingNewElems[idx],
                                        autoCreateAnimCurves = True,
                                        autoCreateName = ctrlName + tierNames[idx], # Primary, Secondary, Or Tertiatry
                                        singleFalloffName = falloffLipThickName,
                                        autoCreateNum = tierCounts[idx],
                                        falloffCurveDict = thickFalloffCurve,
                                        falloffDefaults=falloffThickDefaults,
                                        falloffItts=["linear","linear","linear","linear"],
                                        falloffOtts=["linear","linear","linear","linear"],
                                        autoCreateTimeRange = autoCreateTimeRange,
                                        offset=offset,
                                        centerWeight = centerWeights[idx],
                                        outerWeight = outerWeights[idx],
                                        angle = angles[idx],
                                        nudge = nudges[idx],
                                        intermediateVal=intermediateVal,
                                        lastAngle=lastAngles[idx],
                                        lastIntermediateVal=lastIntermediateVal,
                                        intermediateAngle=intermediateAngle,
                                        lastIntermediateAngle=lastIntermediateAngle,
                                        startElem = tierAddAtIndex[idx],


        )
        curveWeights.create()

        tyAttrs = []
        for ctrl in stack.controls:
            tyAttrs.append(ctrl + ".tyOut")
        thickShape = elements.upArrow
        if not upperLip:
            thickShape = elements.downArrow

        stack = weightStack.WeightStack(name=name + "WeightStackThick",
                                        geoToWeight=deformMesh,
                                        ctrlNode=control,
                                        weightMapAttrNames=curveWeights.newKDoubleArrayOutputPlugs,
                                        addNewElem=isAddingNewElems[idx],
                                        UDLR = False,
                                        #outputAttrs = thickOutputattrs,
                                        autoCreate=True,
                                        controlPositionWeightsThreshold=ctrlAutoPositionThreshold,
                                        # controlPositionOffset=slideCtrlPosOffset1,
                                        controlRivetMesh = controlRivetMesh,
                                        controlAutoOrientMesh=controlAutoOrientMesh,
                                        controlRivetAimMesh=slidePatch,
                                        #controlSpeedDefaults = slideControlSpeedDefaults,
                                        controlParent = controlParent,
                                        controlShape=thickShape,
                                        connectFalloff = connectFalloffs[idx],
                                        isOutputKDoubleArray=True,
                                        # falloffCurveWeightNode="TestCurveWeights",
                                        autoCreateName=ctrlName + tierNames[idx] + "THICK", # Primary, Secondary, Or Tertiatry
                                        controlSize = thickCtrlSizes[idx],
                                        controlShapeOffset = thickCtrlShapeOffsets[idx],
                                        repositionRivetCtrls = repositionRivetCtrls,
                                        controlTyConnectionAttrs = tyAttrs,
                                        controlSpeedDefaults = [1,1,1],
                                        controlShapeOrient=[0,0,0],
                                        controlLockAttrs=["tx", "tz", "rx", "ry", "rz", "sx", "sy", "sz"],
                                        )
        stack.create()
        vectorDeformer = vectorDeformerSimple.VectorDeformerSimple(name = name + "THICKTEST", geoToDeform=deformMesh, weightStackNode=stack.node, toPoint = thickToPoint)
        vectorDeformer.create() 
    return slideUD.deformer, vectorDeformer.deformer

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
                        curveDeformerAlgorithm=0,
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
    if curveDeformerAlgorithm == 0:
        wire = cmds.wire(blendshapeGeo, wire=curve, dds=[(0),(100000)] , name=name + "WireDeformer")[0]
    if curveDeformerAlgorithm == 1:
        wire = LHCurveDeformerCmds.curveDeformerCmd( driverCurve = curve,
                                            aimCurve = curveAim,
                                            geom = [blendshapeGeo],
                                            ihi = 1,
                                            lockAttrs = 0,
                                            side='C',
                                            name=name + "CurveDeformer").returnDeformer
        
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

    return blendshape
