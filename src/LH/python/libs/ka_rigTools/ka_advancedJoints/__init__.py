#====================================================================================
#====================================================================================
#
# ka_advancedJoints
#
# DESCRIPTION:
#   A module for creating complex joint setups
#
# DEPENDENCEYS:
#   Maya
#
#
# AUTHOR:
#   Kris Andrews (3dkris@3dkris.com)
#
#====================================================================================
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are
#met:

    #(1) Redistributions of source code must retain the above copyright
    #notice, this list of conditions and the following disclaimer.

    #(2) Redistributions in binary form must reproduce the above copyright
    #notice, this list of conditions and the following disclaimer in
    #the documentation and/or other materials provided with the
    #distribution.

    #(3)The name of the author may not be used to
    #endorse or promote products derived from this software without
    #specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
#INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#POSSIBILITY OF SUCH DAMAGE.
#====================================================================================

import math

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_math as ka_math; importlib.reload(ka_math)
import ka_rigTools.ka_util as ka_util; importlib.reload(ka_util)
import ka_rigTools.ka_pymel as ka_pymel; importlib.reload(ka_pymel)
import ka_rigTools.ka_shapes as ka_shapes; importlib.reload(ka_shapes)
import ka_rigTools.ka_transforms as ka_transforms; importlib.reload(ka_transforms)
import ka_rigTools.ka_constraints as ka_constraints; importlib.reload(ka_constraints)
import ka_rigTools.ka_attrTool.attrCommands as attrCommands; importlib.reload(attrCommands)
import importlib




def createVolumeRotator():
    selection = pymel.ls(selection=True)
    _createVolumeRotator(selection[0], selection[1])


def printVolumeRotators():
    outputCode = ['import ka_rigTools.ka_advancedJoints as ka_advancedJoints; reload(ka_advancedJoints)']
    volumeRotatorGroups = []
    for node in pymel.ls(type='transform'):
	if hasattr(node, 'rigType'):
	    if 'volumeRotatorGroup' in getRigTypes(node):
		volumeRotatorGroups.append(node)

    for volumeRotatorGroup in volumeRotatorGroups:
	rootJoint = volumeRotatorGroup.rootJoint.inputs()[0]
	childJoint = volumeRotatorGroup.childJoint.inputs()[0]

	volumeRotatorGroup_diameterAdjustsDict = {}
	for child in volumeRotatorGroup.getChildren(allDescendents=True, type='transform'):
	    if hasattr(child, 'rigType'):
		rigTypes = getRigTypes(child)
		if 'volumeRotatorGroup_diameterAdjust' in rigTypes:
		    for key in ['positiveY', 'negativeY', 'positiveZ', 'negitiveZ']:
			if key in rigTypes:
			    volumeRotatorGroup_diameterAdjustsDict[key] = child

	valuesDict = {}
	for key in volumeRotatorGroup_diameterAdjustsDict:
	    diameterAdjust = volumeRotatorGroup_diameterAdjustsDict[key]
	    value = None
	    for attr in ['tx', 'ty', 'tz']:
		if not diameterAdjust.attr(attr).isLocked():
		    value = diameterAdjust.attr(attr).get()
		    valuesDict[key] = value
		    break
	OOOOOOO = 'volumeRotatorGroup_diameterAdjustsDict';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
	values = []
	for key in ['positiveY', 'negativeY', 'positiveZ', 'negitiveZ']:
	    if key in valuesDict:
		values.append(valuesDict[key])


	outputCode.append("ka_advancedJoints._createVolumeRotator('%s', '%s', diameterAdjustDefaults=%s)" % (str(rootJoint), str(childJoint), str(values)))

    for line in outputCode:
	print(line)


def _createVolumeRotator(rootJoint, childJoint, diameterAdjustDefaults=[1.0, -1.0, 1.0, -1.0]):
    rootJoint = ka_pymel.getAsPyNodes(rootJoint)
    childJoint = ka_pymel.getAsPyNodes(childJoint)

    basename = childJoint.nodeName()
    childJointTx = childJoint.tx.get()
    side = childJointTx/abs(childJointTx)

    # rotatorGroupZro
    rotatorGroupZro = pymel.createNode('transform')
    rotatorGroupZro.rename(basename+'_rotatorGroupZro')
    pymel.parent(rotatorGroupZro, childJoint)
    ka_transforms.snap(rotatorGroupZro, childJoint, t=1, r=1)


    # rotatorGroupZro Aim
    aimConstraint = pymel.aimConstraint(rootJoint, rotatorGroupZro, worldUpType='objectrotation', worldUpObject=childJoint, aimVector=[side*-1, 0, 0], worldUpVector=[0,0,1], upVector=[0,0,1], maintainOffset=False)

    #rootPos_vectorProduct = pymel.createNode('vectorProduct')
    #rootPos_vectorProduct.operation.set(4)
    #rootJoint.worldMatrix[0] >> rootPos_vectorProduct.matrix

    #childPos_vectorProduct = pymel.createNode('vectorProduct')
    #childPos_vectorProduct.operation.set(4)
    #childJoint.worldMatrix[0] >> childPos_vectorProduct.matrix

    #vectorOfRoot_plusMinus = pymel.createNode('plusMinusAverage')
    #childPos_vectorProduct.operation.set(2)
    #rootPos_vectorProduct.output >> vectorOfRoot_plusMinus.input3D[0]
    #childPos_vectorProduct.output >> vectorOfRoot_plusMinus.input3D[1]

    childVectorY_vectorProduct = pymel.createNode('vectorProduct')
    childVectorY_vectorProduct.operation.set(3)
    childVectorY_vectorProduct.input1.set(0,1,0)
    childJoint.worldMatrix[0] >> childVectorY_vectorProduct.matrix

    childVectorZ_vectorProduct = pymel.createNode('vectorProduct')
    childVectorZ_vectorProduct.operation.set(3)
    childVectorZ_vectorProduct.input1.set(0,0,1)
    childJoint.worldMatrix[0] >> childVectorZ_vectorProduct.matrix

    rootVectorX_vectorProduct = pymel.createNode('vectorProduct')
    rootVectorX_vectorProduct.operation.set(3)
    rootVectorX_vectorProduct.input1.set(1,0,0)
    rootJoint.worldMatrix[0] >> rootVectorX_vectorProduct.matrix


    dotOfvectorXY_vectorProduct = pymel.createNode('vectorProduct')
    childVectorY_vectorProduct.output >> dotOfvectorXY_vectorProduct.input1
    #vectorOfRoot_plusMinus.output3D >> dotOfvectorXY_vectorProduct.input2
    rootVectorX_vectorProduct.output >> dotOfvectorXY_vectorProduct.input2

    dotOfvectorXZ_vectorProduct = pymel.createNode('vectorProduct')
    childVectorZ_vectorProduct.output >> dotOfvectorXZ_vectorProduct.input1
    #vectorOfRoot_plusMinus.output3D >> dotOfvectorXZ_vectorProduct.input2
    rootVectorX_vectorProduct.output >> dotOfvectorXZ_vectorProduct.input2

    #invertY_plusMinus = pymel.createNode('plusMinusAverage')
    #invertY_plusMinus.operation.set(2)
    #invertY_plusMinus.input1D[0].set(1)
    #dotOfvectorXY_vectorProduct.outputX >> invertY_plusMinus.input1D[1]

    #invertZ_plusMinus = pymel.createNode('plusMinusAverage')
    #invertZ_plusMinus.operation.set(2)
    #invertZ_plusMinus.input1D[0].set(1)
    #dotOfvectorXZ_vectorProduct.outputX >> invertZ_plusMinus.input1D[1]

    invertZ_setDriven = pymel.createNode('animCurveUU', )
    invertZ_setDriven.keyTanInType[0].set(2, keyable=False, channelBox=False, lock=False, )
    invertZ_setDriven.keyTanInType[1].set(2, keyable=False, channelBox=False, lock=False, )
    invertZ_setDriven.keyTanInType[2].set(2, keyable=False, channelBox=False, lock=False, )
    invertZ_setDriven.keyTanOutType[0].set(2, keyable=False, channelBox=False, lock=False, )
    invertZ_setDriven.keyTanOutType[1].set(2, keyable=False, channelBox=False, lock=False, )
    invertZ_setDriven.keyTanOutType[2].set(2, keyable=False, channelBox=False, lock=False, )
    pymel.setKeyframe(invertZ_setDriven, value=0.0, float=-1.0)
    pymel.setKeyframe(invertZ_setDriven, value=1.0, float=0.0)
    pymel.setKeyframe(invertZ_setDriven, value=0.0, float=1.0)
    invertZ_setDriven.tangentType.set(2, keyable=False, channelBox=False, lock=False, )
    invertZ_setDriven.weightedTangents.set(False, keyable=False, channelBox=False, lock=False, )

    invertY_setDriven = pymel.createNode('animCurveUU', )
    invertY_setDriven.keyTanInType[0].set(2, keyable=False, channelBox=False, lock=False, )
    invertY_setDriven.keyTanInType[1].set(2, keyable=False, channelBox=False, lock=False, )
    invertY_setDriven.keyTanInType[2].set(2, keyable=False, channelBox=False, lock=False, )
    invertY_setDriven.keyTanOutType[0].set(2, keyable=False, channelBox=False, lock=False, )
    invertY_setDriven.keyTanOutType[1].set(2, keyable=False, channelBox=False, lock=False, )
    invertY_setDriven.keyTanOutType[2].set(2, keyable=False, channelBox=False, lock=False, )
    pymel.setKeyframe(invertY_setDriven, value=0.0, float=-1.0)
    pymel.setKeyframe(invertY_setDriven, value=1.0, float=0.0)
    pymel.setKeyframe(invertY_setDriven, value=0.0, float=1.0)
    invertY_setDriven.tangentType.set(2, keyable=False, channelBox=False, lock=False, )
    invertY_setDriven.weightedTangents.set(False, keyable=False, channelBox=False, lock=False, )

    dotOfvectorXY_vectorProduct.outputX >> invertY_setDriven.input
    dotOfvectorXZ_vectorProduct.outputX >> invertZ_setDriven.input



    invertY_setDriven.output >> aimConstraint.upVectorY
    invertY_setDriven.output >> aimConstraint.worldUpVectorY

    invertZ_setDriven.output >> aimConstraint.upVectorZ
    invertZ_setDriven.output >> aimConstraint.worldUpVectorZ

    # rotatorGroup
    rotatorGroup = pymel.createNode('transform')
    rotatorGroup.rename(basename+'_rotatorGroup')
    pymel.parent(rotatorGroup, rotatorGroupZro)
    ka_transforms.snap(rotatorGroup, rootJoint, t=1, r=1)
    setRigTypes(rotatorGroup, 'volumeRotatorGroup')
    pymel.addAttr(rotatorGroup, longName='rootJoint', attributeType='message', keyable=True)
    pymel.addAttr(rotatorGroup, longName='childJoint', attributeType='message', keyable=True)
    rootJoint.message >> rotatorGroup.rootJoint
    childJoint.message >> rotatorGroup.childJoint


    # childJointRotateSpaceGroup
    childJointRotateSpaceGroup = pymel.createNode('transform')
    childJointRotateSpaceGroup.rename(basename+'_rotatorChildSpace')
    pymel.parent(childJointRotateSpaceGroup, rotatorGroup)
    orientConstraint = pymel.orientConstraint(childJoint, childJointRotateSpaceGroup)
    ka_transforms.snap(childJointRotateSpaceGroup, childJoint, t=1,)


    # halfRotateJoint
    halfRotateJoint = pymel.createNode('joint')
    halfRotateJoint.rename('%s_halfRotateJnt'% basename)
    halfRotateJoint.radius.set(childJoint.radius.get()*2)
    pymel.parent(halfRotateJoint, rotatorGroup)
    halfRotateJoint.jointOrient.set(0,0,0)
    orientConstraint = pymel.orientConstraint(rotatorGroup, childJointRotateSpaceGroup, halfRotateJoint)
    #orientConstraint = ka_constraints.localizeConstraint(orientConstraint)
    orientConstraint.interpType.set(2)
    ka_transforms.snap(halfRotateJoint, childJoint, t=1)


    axisDict = {'positiveY':{'vector':[0,1,0,],
                             'attr':'ty',
                             'unusedAttr':'tz',
                             'axisName':'Y',
                             'unusedAxisName':'Z',
                             'index':1,
                             'niceName':'negY',
                             'diameterAdjustDefault':diameterAdjustDefaults[0],
                            },

                'negativeY':{'vector':[0,-1,0,],
                             'attr':'ty',
                             'unusedAttr':'tz',
                             'axisName':'Y',
                             'unusedAxisName':'Z',
                             'index':1,
                             'niceName':'negY',
                             'diameterAdjustDefault':diameterAdjustDefaults[1],
                            },

                'positiveZ':{'vector':[0,0,1,],
                             'attr':'tz',
                             'unusedAttr':'ty',
                             'axisName':'Z',
                             'unusedAxisName':'Y',
                             'index':2,
                             'niceName':'Z',
                             'diameterAdjustDefault':diameterAdjustDefaults[2],
                            },

                'negitiveZ':{'vector':[0,0,-1,],
                             'attr':'tz',
                             'unusedAttr':'ty',
                             'axisName':'Z',
                             'unusedAxisName':'Y',
                             'index':2,
                             'niceName':'negZ',
                             'diameterAdjustDefault':diameterAdjustDefaults[3],
                            },
               }

    # attributes used by all push joints
    RGB = 'RGB'
    pushJointRadius = childJoint.radius.get()
    rootLength = ka_transforms.distanceBetween(rootJoint, childJoint)
    childLength = 1*side
    childrenOfChildJoint = childJoint.getChildren(type='joint')
    for child in childrenOfChildJoint:
	tx = child.tx.get()
	if abs(tx) > abs(childLength):
	    childLength = tx


    # Create push joints
    for axis in sorted(axisDict):
	axisVector = axisDict[axis]['vector']
	axisindex = axisDict[axis]['index']
	attrName = axisDict[axis]['attr']
	unusedAttrName = axisDict[axis]['unusedAttr']
	axisName = axisDict[axis]['axisName']
	unusedAxisName = axisDict[axis]['unusedAxisName']
	axisNiceName = axisDict[axis]['niceName']
	vectorProductAttr = axisDict[axis]['axisName']
	diameterAdjustDefault = axisVector[axisindex]*abs(axisDict[axis]['diameterAdjustDefault'])


	negativeAxisVector = []
	for i in axisVector:
	    negativeAxisVector.append(-1*i)

	axisValue = axisVector[axisindex]

	diameterAdjust = ka_shapes.createNurbsCurve('pyramidPointer', pointAt=negativeAxisVector, size=pushJointRadius*0.2)
	diameterAdjust.rename('%s_%s_diameterAdjust' % (basename, axisNiceName))
	pymel.parent(diameterAdjust, halfRotateJoint)
	diameterAdjust.t.set(axisVector)
	diameterAdjust.r.set(0,0,0)
	for attr in ['tx', 'ty', 'tz']:
	    if attr != attrName:
		diameterAdjust.attr(attr).lock()
	    else:
		diameterAdjust.attr(attr).set(diameterAdjustDefault)
	setRigTypes(diameterAdjust, ['volumeRotatorGroup_diameterAdjust', axis])


	# Root Push
	rootPushJoint = pymel.createNode('joint')
	rootPushJoint.rename('%s_%s_rootPush' % (childJoint.nodeName(), axis))
	rootPushJoint.radius.set(pushJointRadius*0.3)
	pymel.parent(rootPushJoint, rotatorGroup)

	rootPushJointEnd = pymel.createNode('joint')
	rootPushJointEnd.rename('%s_%s_rootPushEnd' % (childJoint.nodeName(), axis))
	pymel.parent(rootPushJointEnd, rootPushJoint)
	rootPushJointEnd.tx.set(-0.25*childLength)
	rootPushJointEnd.v.set(0)

	ka_transforms.snap(rootPushJoint, rotatorGroup, r=1)
	rootPushJoint.t.set(axisVector)
	diameterAdjust.attr(attrName) >> rootPushJoint.attr(attrName)


	# Child Push
	childPushJoint = pymel.createNode('joint')
	childPushJoint.rename('%s_%s_childPush' % (childJoint.nodeName(), axis))
	childPushJoint.radius.set(pushJointRadius*0.3)
	pymel.parent(childPushJoint, childJointRotateSpaceGroup)

	childPushJointEnd = pymel.createNode('joint')
	childPushJointEnd.rename('%s_%s_childPushEnd' % (childJoint.nodeName(), axis))
	pymel.parent(childPushJointEnd, childPushJoint)
	childPushJointEnd.tx.set(0.25*childLength)
	childPushJointEnd.v.set(0)

	ka_transforms.snap(childPushJoint, childJoint, r=1)
	childPushJoint.t.set(axisVector)
	diameterAdjust.attr(attrName) >> childPushJoint.attr(attrName)

	# child outer edge vp
	childOuterEdge_vectorProduct = pymel.createNode('vectorProduct')
	childOuterEdge_vectorProduct.operation.set(4)
	childJointRotateSpaceGroup.matrix >> childOuterEdge_vectorProduct.matrix
	diameterAdjust.attr(attrName) >> childOuterEdge_vectorProduct.attr('input1'+axisName)
	#childOuterEdgeX_multiplyDivide.outputX >> childOuterEdge_vectorProduct.input1X
	childOuterEdge_vectorProduct.input1X.set(childLength*10)

	# condition rounding multiplier
	conditionRoundingMultiplier = pymel.createNode('multiplyDivide')
	conditionRoundingMultiplier.input2X.set(1.001)
	diameterAdjust.attr(attrName) >> conditionRoundingMultiplier.input1X

	# concave bend condition
	concaveBendOperationCondition = pymel.createNode('condition')
	if axisValue == 1:
	    concaveBendOperationCondition.operation.set(2) # greater than
	else:
	    concaveBendOperationCondition.operation.set(4) # less than

	childOuterEdge_vectorProduct.attr('output'+axisName) >> concaveBendOperationCondition.firstTerm
	conditionRoundingMultiplier.outputX >> concaveBendOperationCondition.secondTerm
	concaveBendOperationCondition.colorIfTrueR.set(2)
	concaveBendOperationCondition.colorIfTrueG.set(1)
	concaveBendOperationCondition.colorIfTrueB.set(4)
	concaveBendOperationCondition.colorIfFalseR.set(0)
	concaveBendOperationCondition.colorIfFalseG.set(0)
	concaveBendOperationCondition.colorIfFalseB.set(0)

	# convex bend condition
	convexBendOperationCondition = pymel.createNode('condition')
	if axisValue == 1:
	    convexBendOperationCondition.operation.set(5) # equal or greater than
	else:
	    convexBendOperationCondition.operation.set(3) # equal or less than
	childOuterEdge_vectorProduct.attr('output'+axisName) >> convexBendOperationCondition.firstTerm
	conditionRoundingMultiplier.outputX >> convexBendOperationCondition.secondTerm
	convexBendOperationCondition.colorIfTrueR.set(2)
	convexBendOperationCondition.colorIfTrueG.set(1)
	convexBendOperationCondition.colorIfTrueB.set(4)
	convexBendOperationCondition.colorIfFalseR.set(0)
	convexBendOperationCondition.colorIfFalseG.set(0)
	convexBendOperationCondition.colorIfFalseB.set(0)


	# child near edge vp
	childNearEdge_vectorProduct = pymel.createNode('vectorProduct')
	childJointRotateSpaceGroup.matrix >> childNearEdge_vectorProduct.matrix
	diameterAdjust.attr(attrName) >> childNearEdge_vectorProduct.attr('input1'+axisName)
	concaveBendOperationCondition.outColorB >> childNearEdge_vectorProduct.operation


	# intersect nodes
	# child outer edge root outer edge height difference
	childOuterRootOuterHeightDiff = pymel.createNode('plusMinusAverage')
	childOuterEdge_vectorProduct.attr('output'+axisName) >> childOuterRootOuterHeightDiff.input1D[0]
	diameterAdjust.attr(attrName) >> childOuterRootOuterHeightDiff.input1D[1]
	concaveBendOperationCondition.outColorR >> childOuterRootOuterHeightDiff.operation

	# slope plus minus average
	slopePlusMinusAverage = pymel.createNode('plusMinusAverage')
	childOuterEdge_vectorProduct.outputX >> slopePlusMinusAverage.input2D[0].input2Dx
	childOuterEdge_vectorProduct.attr('output'+axisName) >> slopePlusMinusAverage.input2D[0].input2Dy
	childNearEdge_vectorProduct.outputX >> slopePlusMinusAverage.input2D[1].input2Dx
	childNearEdge_vectorProduct.attr('output'+axisName) >> slopePlusMinusAverage.input2D[1].input2Dy
	concaveBendOperationCondition.outColorR >> slopePlusMinusAverage.operation

	# slope ratio divider
	slopeRatioDivider = pymel.createNode('multiplyDivide')
	slopePlusMinusAverage.output2Dx >> slopeRatioDivider.input1X
	slopePlusMinusAverage.output2Dy >> slopeRatioDivider.input2X
	concaveBendOperationCondition.outColorR >> slopeRatioDivider.operation

	# slope ratio multiplier
	slopeRatioMultiplier = pymel.createNode('multiplyDivide')
	slopeRatioDivider.outputX >> slopeRatioMultiplier.input1X
	childOuterRootOuterHeightDiff.output1D >> slopeRatioMultiplier.input2X
	concaveBendOperationCondition.outColorG >> slopeRatioMultiplier.operation


	# child outer edge subtractor
	childOuterSubtractor = pymel.createNode('plusMinusAverage')
	childOuterEdge_vectorProduct.outputX >> childOuterSubtractor.input1D[0]
	slopeRatioMultiplier.outputX >> childOuterSubtractor.input1D[1]
	concaveBendOperationCondition.outColorR >> childOuterSubtractor.operation

	# child push space switch vector product
	childPushSpaceSwitch_vectorProduct = pymel.createNode('vectorProduct')
	diameterAdjust.attr(attrName) >> childPushSpaceSwitch_vectorProduct.attr('input1'+axisName)
	childOuterSubtractor.output1D  >> childPushSpaceSwitch_vectorProduct.input1X
	childJointRotateSpaceGroup.inverseMatrix >> childPushSpaceSwitch_vectorProduct.matrix
	concaveBendOperationCondition.outColorB >> childPushSpaceSwitch_vectorProduct.operation

	# midJoint to root space VP
	halfRotateJointToRootSpace_vectorProduct = pymel.createNode('vectorProduct')
	halfRotateJoint.matrix >> halfRotateJointToRootSpace_vectorProduct.matrix
	diameterAdjust.attr(attrName) >> halfRotateJointToRootSpace_vectorProduct.attr('input1'+axisName)
	#convexBendOperationCondition.outColorB >> halfRotateJointToRootSpace_vectorProduct.operation
	halfRotateJointToRootSpace_vectorProduct.operation.set(4)

	# midJoint to child space VP
	halfRotateJointToChildSpace_vectorProduct = pymel.createNode('vectorProduct')
	childJointRotateSpaceGroup.inverseMatrix >> halfRotateJointToChildSpace_vectorProduct.matrix
	halfRotateJointToRootSpace_vectorProduct.output >> halfRotateJointToChildSpace_vectorProduct.input1
	#convexBendOperationCondition.outColorB >> halfRotateJointToChildSpace_vectorProduct.operation
	halfRotateJointToChildSpace_vectorProduct.operation.set(4)

	#BLENDER
	# slope dotProduct
	slopeDotProduct = pymel.createNode('vectorProduct')
	slopeDotProduct.input2.set(1,0,0)
	slopeDotProduct.normalizeOutput.set(1)
	slopePlusMinusAverage.output2Dx >> slopeDotProduct.input1X
	slopePlusMinusAverage.output2Dy >> slopeDotProduct.input1Y
	concaveBendOperationCondition.outColorG >> slopeDotProduct.operation

	# inputBlendCurve
	inputBlendCurve = pymel.createNode('animCurveUU', )
	inputBlendCurve.keyTanInType[0].set(18, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.keyTanInType[1].set(1, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.keyTanInType[2].set(2, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.keyTanInX[1].set(0.0, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.keyTanInY[1].set(0.0, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.keyTanOutType[0].set(18, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.keyTanOutType[1].set(1, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.keyTanOutType[2].set(2, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.keyTanOutX[1].set(1.0, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.keyTanOutY[1].set(0.0, keyable=False, channelBox=False, lock=False, )
	pymel.setKeyframe(inputBlendCurve, value=1.0, float=-1.0)
	pymel.setKeyframe(inputBlendCurve, value=1.0, float=0.75)
	pymel.setKeyframe(inputBlendCurve, value=0.0, float=1.0)
	inputBlendCurve.tangentType.set(18, keyable=False, channelBox=False, lock=False, )
	inputBlendCurve.weightedTangents.set(False, keyable=False, channelBox=False, lock=False, )
	slopeDotProduct.outputX >> inputBlendCurve.input


	# outputX condition
	outputXCondition = pymel.createNode('condition')
	if axisValue == 1:
	    outputXCondition.operation.set(2) # greater than
	else:
	    outputXCondition.operation.set(4) # less than
	outputXCondition.colorIfFalseR.set(0)
	childOuterEdge_vectorProduct.attr('output'+axisName) >> outputXCondition.firstTerm
	conditionRoundingMultiplier.outputX >> outputXCondition.secondTerm
	inputBlendCurve.output >> outputXCondition.colorIfTrueR


	# inputBlendColor
	inputBlendColor = pymel.createNode('blendColors',)
	outputXCondition.outColorR >> inputBlendColor.blender



	# final connects
	#childOuterSubtractor.output1D >> outputXCondition.colorIfTrueR
	#childPushSpaceSwitch_vectorProduct.outputX >> outputXCondition.colorIfTrueG

	#halfRotateJointToRootSpace_vectorProduct.outputX >> outputXCondition.colorIfFalseR
	#halfRotateJointToChildSpace_vectorProduct.outputX >> outputXCondition.colorIfFalseG

	#outputXCondition.outColorR >> rootPushJoint.tx
	#outputXCondition.outColorG >> childPushJoint.tx

	childOuterSubtractor.output1D >> inputBlendColor.color1R
	childPushSpaceSwitch_vectorProduct.outputX >> inputBlendColor.color1G

	halfRotateJointToRootSpace_vectorProduct.outputX >> inputBlendColor.color2R
	halfRotateJointToChildSpace_vectorProduct.outputX >> inputBlendColor.color2G

	inputBlendColor.outputR >> rootPushJoint.tx
	inputBlendColor.outputG >> childPushJoint.tx

	halfRotateJointToRootSpace_vectorProduct.attr('output'+unusedAxisName) >> rootPushJoint.attr(unusedAttrName)
	halfRotateJointToChildSpace_vectorProduct.attr('output'+unusedAxisName) >> childPushJoint.attr(unusedAttrName)


def createTwistMuscle():
    text=None
    result = cmds.promptDialog(
                    title='Name Muscle',
                    message='Enter a Base Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)

        if text:
            _createBendMuscle(name=text)
        else:
            _createBendMuscle()

def _createTwistMuscle(baseName):
    pass

def distanceBetween(pointA, pointB):
    '''returns distance between a list of 2d or 3d coordinates'''
    sum = 0
    for i, each in enumerate(pointA):
        sum += (pointA[i] - pointB[i])**2

    return math.sqrt( sum )

def shapeParent(objectA, objectB):

    shapeObj = pymel.parent(objectA, objectB)
    pymel.makeIdentity(shapeObj[0], apply=True, t=1, r=1, s=1, n=1)
    shapes = pymel.listRelatives(shapeObj[0], shapes=True)

    for shape in shapes:
        pymel.parent(shape, objectB, shape=True, add=True)

    pymel.delete(shapeObj)
    pymel.select(objectB)



def create_pistonMuscle():
    text=None
    result = cmds.promptDialog(
                    title='Name Muscle',
                    message='Enter a Base Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)

        if text:
            _createBendMuscle(baseName)
        else:
            _createBendMuscle()




def makeRibonFromTransforms(transformList=None, secondaryAxis=1):
    if not transformList:
        transformList = pymel.ls(selection=True)
    if not hasattr(transformList, '__iter__'):
        list(transformList)

    lenOfTransformList = len(transformList)
    if lenOfTransformList < len(transformList):
        pymel.error('must select at least 4 transforms to build ribon')

    ribon, makeNurbPlane = pymel.nurbsPlane( d=3, u=1, v=lenOfTransformList-3 )
    ribonShape = ribon.getShape()

    for i, transform in enumerate(transformList):
        cvRow = ribonShape.cv[0:3][i]
        ribonVector = [0.0, 0.0, 0.0]

        for ib, cv in enumerate(cvRow):
            if ib == 0: ribonVector[secondaryAxis] = 1.0
            if ib == 1: ribonVector[secondaryAxis] = 0.0
            if ib == 2: ribonVector[secondaryAxis] = -1.0
            ka_transforms.translate_inTargetObjectsSpace([ribonShape.cv[ib][i]], ribonVector, transform)

        # create a control locator for row
        controlLocatorShape = pymel.createNode('locator')
        controlLocator = controlLocatorShape.getParent()

        guideLocatorWorldMatrix = pymel.xform(transform, query=True, matrix=True, worldSpace=True)
        pymel.xform(controlLocator, matrix=guideLocatorWorldMatrix, worldSpace=True)


    pymel.delete(ribonShape, constructionHistory=True)
            ##transform cvRow i*0.333 in transforms y-axis
            #utils
            #pass



def makeAdvancedIkSplineUI():
    '''Simple UI to create an ik spline with strech and upvectors from the start and end joint (selected in that order.
    The strech will preserve the ratio of the inital joint lengths, though the scale of the chain may change to fit the
    newly created chain. If more than 2 joints are selected, the joints inbetween the first and last will be an additional twist point,
    and also be the connecting point between the multiple overlapping ik splines'''

    if cmds.windowPref( 'makeAdvancedIkSplineWindow', exists=True ):
        cmds.windowPref( 'makeAdvancedIkSplineWindow', remove=True )


    if cmds.window('makeAdvancedIkSplineWindow', exists=True):
        cmds.deleteUI('makeAdvancedIkSplineWindow', window=True)

    windowH = 100
    windowW = 350
    windowUI = cmds.window('makeAdvancedIkSplineWindow', title="makeAdvancedIkSplineWindow", iconName='make Advanced Ik Spline', widthHeight=(windowW, windowH,) )
    cmds.rowColumnLayout(columnWidth=[1, windowW])
    cmds.text("Rig IK Spline")

    cmds.separator(vis=0, h=5)
    cmds.separator()
    cmds.separator(vis=0, h=5)

    cmds.text("Base Name:")
    nameField = cmds.textField()

    cmds.separator(vis=0, h=5)
    cmds.separator()
    cmds.separator(vis=0, h=5)

    cmds.text("Number Of Spans")
    numbOfSpansField = cmds.intField(v=2, minValue=1, width=50)

    cmds.separator(vis=0, h=5)
    cmds.separator()
    cmds.separator(vis=0, h=5)

    def cmd(*args, **kwargs):
        baseName = cmds.textField(nameField, q=True, text=True)
        numbOfSpans = cmds.intField(numbOfSpansField, q=True, value=True)
        makeAdvancedIkSplineFromSelection(baseName, numbOfSpans)

    cmds.button( label='Create', command=cmd)

    cmds.setParent( '..' )
    cmds.window(windowUI, edit=True, width=windowW, height=windowH )
    cmds.showWindow( windowUI )


def makeAdvancedIkSplineFromSelection(baseName, numbOfCvs):
    '''makes an ikSpline from selection'''

    selection = pymel.ls(selection=True)



    if len(selection) > 2:
        twistControlJoints = selection[1:-1]

    else:
        twistControlJoints = []

    rootJoint = selection[0]
    endJoint = selection[-1]


    makeAdvancedIkSpline(baseName, rootJoint, endJoint, numbOfCvs=numbOfCvs, twistControlJoints=twistControlJoints)


def makeAdvancedIkSpline(baseName, rootJoint, endJoint, numbOfCvs=2, twistControlJoints=[], closedCurve=False):

    #make a list of the points of the joints so we can make a linear point per joint curve with it later
    #this will serve as the curve we can build our iks on to start
    chainWorldSpacePointList = []
    jointList = []
    parent = [endJoint]


    while parent:

        joint = parent
        position = tuple(pymel.xform(joint, query=True, translation=True, worldSpace=True))
        jointList.append(joint)
        chainWorldSpacePointList.append(position)

        if parent[0] != rootJoint:
            parent = pymel.listRelatives(parent, parent=True)

        else:
            parent = []

    chainWorldSpacePointList.reverse()
    totalJointLength = 0
    for i, point in enumerate(chainWorldSpacePointList):
        if i != 0:
            totalJointLength += ka_math.distanceBetween( chainWorldSpacePointList[i-1], chainWorldSpacePointList[i] )


    jointLinearCurve = pymel.curve( p=chainWorldSpacePointList, degree=1)
    curveInfo = pymel.createNode('curveInfo')
    multiplyDivideLength = pymel.createNode('multiplyDivide',)
    curveInfo.arcLength >> multiplyDivideLength.input1X

    jointLinearCurve.getShape().worldSpace[0] >> curveInfo.inputCurve

    #numbOfSpans = (len(twistControlJoints)*(numbOfCvs+1))+1
    numbOfSpans = ( (len(twistControlJoints)+1) * numbOfCvs ) + len(twistControlJoints) -1

    if closedCurve:
        numbOfSpans -= 1
    niceCurve = pymel.rebuildCurve(jointLinearCurve, replaceOriginal=False, degree=3, spans=numbOfSpans, constructionHistory=False)[0]
    niceCurve.rename(baseName+'_ikCurve')
    niceCurve.inheritsTransform.set(0)
    niceCurveCvs = list(niceCurve.getShape().cv)

    if closedCurve:
        pymel.closeCurve(niceCurve, replaceOriginal=True)


    chainStartEnds = []
    if twistControlJoints:
        #rootParent = rootJoint.getParent()

        twistControlJoints.append(endJoint)
        localStartJoint = rootJoint
        for twistControlJoint in twistControlJoints:
            if twistControlJoint == twistControlJoints[-1]:
                localEndJoint = endJoint

            else:
                twistControlJointName = twistControlJoint.nodeName()
                localEndJoint = pymel.duplicate(twistControlJoint,)[0]
                localEndJoint.rename(twistControlJointName+'EndJoint')
                endJointChildren = pymel.listRelatives(localEndJoint)
                pymel.delete(endJointChildren)
                pymel.parent(twistControlJoint, localEndJoint)
                localEndJoint.radius.set(0)

            chainStartEnds.append((localStartJoint, localEndJoint))
            localStartJoint = twistControlJoint


    else:
        chainStartEnds.append((rootJoint, endJoint))


    ikHandles = []
    locators = []
    firstControlBuilt = True
    for chain_i, chainStartEnd in enumerate(chainStartEnds):

        chainStart, chainEnd = chainStartEnd

        ikHandle = pymel.ikHandle(startJoint=chainStart, endEffector=chainEnd, solver='ikSplineSolver', rootOnCurve=False)[0]

        ikHandles.append(ikHandle)
        jointChain = pymel.ikHandle(ikHandle, query=True, jointList=True)
        jointChain.append(chainEnd)


        if chain_i == 0:
            ikHandle.rootOnCurve.set(1)

        ikHandle.rename(baseName+'_ikHandle'+str(chain_i))

        pymel.delete(ikHandle.inCurve.inputs(plugs=True)[0].node().getParent())
        ikCurveShape = jointLinearCurve.getShape()
        ikCurveShape.worldSpace[0] >> ikHandle.inCurve

        #ikCurveShape = ikHandle.inCurve.inputs(plugs=True)[0].node()


        ikCurve = pymel.listRelatives(ikCurveShape, parent=True)[0]
        ikCurve.rename(baseName+'_unSmoothedIkSplineCurve')
        ikCurve.inheritsTransform.set(0)
        ikCurve.translate.lock()
        ikCurve.rotate.lock()
        ikCurve.scale.lock()
        ikEndEffector = pymel.ikHandle(ikHandle, query=True, endEffector=True)
        ikEndEffector.rename(baseName+'_ikEndEffector'+str(chain_i))

        #if chain_i != 0:
            #multiplyDivide = pymel.createNode('multiplyDivide')
            #curveInfoNode.arcLength >> multiplyDivide.input1X
            #multiplyDivide.input2X.set(ChainLengthCount / jointLinearCurve.getShape().length())
            #multiplyDivide.outputX >> ikHandle.offset
            ##multiplyDivide.operation.set(2)

        if chain_i == 0:
            controllersToMake = numbOfCvs+2
        else:
            controllersToMake = numbOfCvs+1

        chain_midLocators = []
        for i in range(controllersToMake):

            #if last twist control in the closed curve ikChain
            if closedCurve and chain_i == len(chainStartEnds)-1 and i == controllersToMake-1:
                locators.append(locators[0])

            else:
                curveCv = niceCurveCvs.pop(0)
                isATwistControl = False
                if firstControlBuilt or i == controllersToMake-1:
                    locator = pymel.curve( p=[(0.0, 2.2204460492503131e-16, 3.0000000000000009), (0.0, 0.0, 0.0), (0.0, 1.0, -1.6653345369377348e-16), (3.3306690738754696e-16, 3.3306690738754696e-16, 2.0), (0.0, -1.0, 1.6653345369377348e-16), (0.0, 0.0, 0.0)], degree=1)
                    isATwistControl = True
                else:
                    locator = pymel.spaceLocator()

                locator.rename(baseName+'_ikCluster'+str(curveCv.currentItemIndex()))
                locatorShape = locator.getShapes()[0]
                locator.translate.set(curveCv.getPosition())
                cluster = pymel.cluster(curveCv, wn=(locator, locator), bindState=True )[0]
		cluster.rename(baseName+'_cluster'+str(curveCv.currentItemIndex()))
		clusterHandel = locator.listRelatives(shapes=True, type='clusterHandle')[0]
		clusterHandel.rename(baseName+'_clusterHandel'+str(curveCv.currentItemIndex()))

		OOOOOOO = 'cluster';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
                locators.append(locator)

                if isATwistControl:
                    if firstControlBuilt:
                        chainStartPosition = pymel.xform(chainStart, query=True, translation=True, worldSpace=True)
                        pymel.xform(locator, translation=chainStartPosition, worldSpace=True)
                        firstControlBuilt=False
                    else:
                        chainEndPosition = pymel.xform(chainEnd, query=True, translation=True, worldSpace=True)
                        pymel.xform(locator, translation=chainEndPosition, worldSpace=True)

                else:
                    chain_midLocators.append(locator)




        if chain_i == 0:
            chain_startLocatorIndex = 0
            chain_endLocatorIndex = -1

        else:
            chain_startLocatorIndex = (controllersToMake*-1)-1
            chain_endLocatorIndex = -1

        chain_startLocator = locators[chain_startLocatorIndex]
        chain_endLocator = locators[chain_endLocatorIndex]


        for locator in chain_midLocators:
            ka_math.distanceBetween(chain_startLocator.translate.get(), chain_endLocator.translate.get())

        pymel.parent(ikHandle, locators[0])


        ikHandle.dTwistControlEnable.set(1)
        ikHandle.dWorldUpType.set(4)
        ikHandle.dWorldUpAxis.set(3)
        ikHandle.dWorldUpVector.set([0,0,1])
        ikHandle.dWorldUpVectorEnd.set([0,0,1])

        chain_startLocator.worldMatrix >> ikHandle.dWorldUpMatrix
        chain_endLocator.worldMatrix >> ikHandle.dWorldUpMatrixEnd

        if chain_i == 0:
            ikHandle.addAttr('currentLength', keyable=True, defaultValue=1)
            ikHandle.addAttr('currentScale', keyable=True, defaultValue=1)
            ikHandle.addAttr('goalLength', keyable=True, defaultValue=1)
            ikHandle.addAttr('percentLength', keyable=True, defaultValue=1)
            ikHandle.addAttr('goalPercentBlend', keyable=True, defaultValue=1, maxValue=1, minValue=0)

        jointList = pymel.ikHandle(ikHandle, query=True, jointList=True,)
        jointList.append(endJoint)
        for i, joint in enumerate(jointList):
            if not i == 0:
                distance = ka_math.distanceBetween( [0,0,0], joint.translate.get() )
                joint.jointOrient.set(0,0,0)
                joint.translateX.set(distance)
                joint.translateY.set(0)
                joint.translateZ.set(0)

            else:
                joint.jointOrient.set(0,0,0)




        #curveInfo = pymel.createNode('curveInfo',)
        #ikCurveShape.worldSpace[0] >> curveInfo.inputCurve

        curveLength = curveInfo.arcLength.get()
        numberOfJoints = len(chainWorldSpacePointList)
        curveLengthEqualSegment = curveLength / ( numberOfJoints-1 )

        if chain_i == 0:
            ikHandle.goalLength >> multiplyDivideLength.input1Y
            ikHandle.percentLength >> multiplyDivideLength.input2X
            ikHandle.currentScale >> multiplyDivideLength.input2Y
            multiplyDivideLength.outputX >> ikHandle.currentLength
            ikHandle.goalLength.set( ikHandle.currentLength.get() )

            blendColorGoalPercentBlend = pymel.createNode('blendColors',)
            blendColorGoalPercentBlend.rename('blendColorGoalPercentBlend')
            multiplyDivideLength.outputX >> blendColorGoalPercentBlend.color1R
            multiplyDivideLength.outputY >> blendColorGoalPercentBlend.color2R
            ikHandle.goalPercentBlend >> blendColorGoalPercentBlend.blender

            multiplyDivideLengthPerJoint = pymel.createNode('multiplyDivide')
            multiplyDivideLengthPerJoint.rename('multiplyDivideLengthPerJoint')
            blendColorGoalPercentBlend.outputR >> multiplyDivideLengthPerJoint.input1X
            multiplyDivideLengthPerJoint.input2X.set(1.0 / ( numberOfJoints-1 ))

            curveInfo.arcLength >> ikHandle.currentLength

            multiplyDivideScale = pymel.createNode('multiplyDivide')
            multiplyDivideScale.rename('multiplyDivideScale')
            multiplyDivideLengthPerJoint.outputX >> multiplyDivideScale.input1X
            multiplyDivideScale.operation.set(2)
            ikHandle.currentScale >> multiplyDivideScale.input2X


        for i, joint in enumerate(jointChain):
            if i != 0:
                initialJointLength = ka_math.distanceBetween( [0,0,0], joint.translate.get() )
                percentOfJointTotal = initialJointLength / totalJointLength

                lengthOfCurveSegmanet = percentOfJointTotal * curveLength
                percentOfEqualSegment = lengthOfCurveSegmanet / curveLengthEqualSegment

                multiplyDivide = pymel.createNode('multiplyDivide')
                multiplyDivide.rename('multiplyDivideJointLengthRatio')
                multiplyDivide.input2X.set(percentOfEqualSegment)
                multiplyDivideScale.outputX >> multiplyDivide.input1X
                multiplyDivide.outputX >> joint.tx

        if chain_i == 0:
            scaleConstraint = pymel.createNode('scaleConstraint')
            pymel.parent(scaleConstraint, ikHandle)
            ikHandle.scale >> scaleConstraint.target[0].targetScale
            ikHandle.parentMatrix >> scaleConstraint.target[0].targetParentMatrix
            scaleConstraint.constraintScaleX >> ikHandle.currentScale

            ikHandle.currentLength.lock()
            ikHandle.currentScale.lock()
        ikHandle.visibility.set(0)
        ikCurve.template.set(1)

    connectionPlugs = jointLinearCurve.getShape().worldSpace[0].outputs(plugs=True)
    for plug in connectionPlugs:
        niceCurve.worldSpace[0] >> plug

    pymel.delete(jointLinearCurve)

    OOOOOOO = 'ikCurve';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
    infoDict = {'ikCurve':niceCurve,
                'jointList':jointList,
                'locators':locators,
    }

    return infoDict

def createBendMuscle():
    text=None
    result = cmds.promptDialog(
                    title='Name Muscle',
                    message='Enter a Base Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)

        if text:
            _createBendMuscle(name=text)
        else:
            _createBendMuscle()


def procedurallyCreateBendMuscle(baseName=None, numberOfJoints=[3,3], radius=1, insertionParent=None, originParent=None, pivotIndicatorParent=None, pullWeight=0.0, insertionMatrix=[], originMatrix=[], pivotIndicatorZroMatrix=[], pivotPositionMatrix=[], jointPercents=[]):

#    pivotIndicator = _createBendMuscle(name=baseName, numberOfInbetweenJoints=numberOfJoints, radius=radius)
    pivotIndicator = _createBendMuscle(name=baseName, numberOfInbetweenJoints=[3,3], radius=radius)

    if pullWeight < 0.0: pullWeight = 0.0
    if pullWeight > 1.0: pullWeight = 1.0

    pivotIndicator.pullWeight.set(pullWeight)
    #pivotIndicatorZro = pymel.listRelatives(pivotIndicator, parent=True)[0]
    insertionNull = pivotIndicator.insertion.inputs()[0]
    originNull = pivotIndicator.origin.inputs()[0]

    if originParent:
        pymel.parent(originNull, originParent)

    if insertionParent:
        pymel.parent(insertionNull, insertionParent)

    if pivotIndicatorParent:
        pymel.parent(pivotIndicator, pivotIndicatorParent)

    if originMatrix:
        pymel.xform(originNull, ws=True, m=originMatrix)
    if insertionMatrix:
        pymel.xform(insertionNull, ws=True, m=insertionMatrix)
    #if pivotIndicatorZroMatrix:
        #pymel.xform(pivotIndicatorZro, ws=True, m=pivotIndicatorZroMatrix)
    if pivotPositionMatrix:
        pymel.xform(pivotIndicator, ws=True, m=pivotPositionMatrix)

    bendyJoints = getBendyJoints(pivotIndicator)
    for iA, listOfJoints in enumerate(bendyJoints):
        for iB, joint in enumerate(listOfJoints):
            joint.constraintPercent.set(float(jointPercents[iA][iB]))

    return pivotIndicator

def getBendyJoints(pivotIndicator):
    muscleMidPointJoint = []

    originJointsDict = {}
    originJointsList = []

    insertionJointsDict = {}
    insertionJointsList = []

    joints = pymel.listRelatives(pivotIndicator, type='joint', children=True)

    if not joints:
        transforms = pymel.listRelatives(pivotIndicator, type='transform', children=True)
        for transform in transforms:
            if pymel.attributeQuery('rigType', node=transform, exists=True):
                rigType = transform.rigType.get()
                if rigType == 'jointsGroup':
                    joints = pymel.listRelatives(transform, type='joint', children=True)


    if joints:
        for joint in joints:
            if pymel.attributeQuery('baseName', node=joint, exists=True):
                jointBaseName = joint.baseName.get()

                if 'muscleOriginInbetweenJoint' in jointBaseName:
                    originJointsDict[jointBaseName] = joint

                if 'muscleInsertionInbetweenJoint' in jointBaseName:
                    insertionJointsDict[jointBaseName] = joint

                if jointBaseName == 'muscleMidPointJoint':
                    muscleMidPointJoint = [joint]


    for key in sorted(originJointsDict):
        originJointsList.append(originJointsDict[key])

    for key in sorted(insertionJointsDict):
        insertionJointsList.append(insertionJointsDict[key])

    return [originJointsList, insertionJointsList, muscleMidPointJoint]



def printCommand_procedurallyCreateBendMuscleJoint():
    allBendMuscleJoints = getAllBendMuscleJoints()

    #print 'import %s' % __module__


    print('## Create BendJoints\n')
    for pivotIndicator in allBendMuscleJoints:
        #pivotIndicatorZro = pymel.listRelatives(pivotIndicator, parent=True)[0]
	pullWeight = pivotIndicator.pullWeight.get()
        baseName = pivotIndicator.nodeName()
        baseName = baseName.replace('_pivotPosition', '', 1)

        #radius = str(pivotIndicator.radius.get())

        insertionNull = pivotIndicator.insertion.inputs()[0]
        originNull = pivotIndicator.origin.inputs()[0]

        insertionParent = insertionNull.getParent()
        if insertionParent:
            insertionParent = str(insertionParent)
        else:
            insertionParent = ''

        originParent = originNull.getParent()
        if originParent:
            originParent = str(originParent)
        else:
            originParent = ''

        pivotIndicatorParent = pivotIndicator.getParent()
        if pivotIndicatorParent:
            pivotIndicatorParent = str(pivotIndicatorParent)
        else:
            pivotIndicatorParent = ''


        insertionMatrix = str( pymel.xform(insertionNull, query=True, ws=True, m=True) )
        originMatrix = str( pymel.xform(originNull, query=True, ws=True, m=True) )
        #pivotIndicatorMatrix = str( pymel.xform(pivotIndicatorZro, query=True, ws=True, m=True) )
        pivotPositionMatrix = str( pymel.xform(pivotIndicator, query=True, ws=True, m=True) )


        muscleOriginInbetweenJoints = []
        muscleInsertionInbetweenJoints = []

        newListOfJointLists = []
        listOfJointLists = getBendyJoints(pivotIndicator)

        for list in listOfJointLists:

            newList = []
            for joint in list:
                newList.append( joint.constraintPercent.get() )

            newListOfJointLists.append(newList)


        jointPercents = str(newListOfJointLists)

        numberOfJoints = '['+str(len(newListOfJointLists[0]))+','+str(len(newListOfJointLists[1]))+']'
        print('userMethods.procedurallyCreateBendMuscle(baseName="'+baseName+'", numberOfJoints='+numberOfJoints+', insertionParent="'+insertionParent+'", originParent="'+originParent+'", pivotIndicatorParent="'+pivotIndicatorParent+'", pullWeight='+str(pullWeight)+', insertionMatrix='+insertionMatrix+', originMatrix='+originMatrix+', pivotPositionMatrix='+pivotPositionMatrix+', jointPercents='+str(jointPercents)+')')


    print('\n\n## Create Constraints inputs')
    constraints = []
    for pivotIndicator in allBendMuscleJoints:
        insertionNull = pivotIndicator.insertion.inputs()[0]
        originNull = pivotIndicator.origin.inputs()[0]

	# get a dict on unique inputs
	inputDict = {}
	inputs = pivotIndicator.inputs()
	inputs.extend(insertionNull.inputs())
	inputs.extend(originNull.inputs())
	for inputNode in inputs:
	    if inputNode not in inputDict:
		inputDict[inputNode] = inputNode

	# if they are constraints, generate the recreate commands
	for inputNode in inputDict:
	    if 'Constraint' in inputNode.nodeType():
		constraints.append(inputNode)

    attrCommands.eccoAttrsPymelObjectOriented(nodes=constraints, skipExternalConnections=False)



def modifyBendMuscle(position, mode):
    '''
    position - tuple of 2 ints - first number is 0 or 1, indicating it is effecting the origin or insertion joints
    mode - string - either 'add' or 'delete' are appropriate flags
    '''
    selection = pymel.ls(selection=True)
    pivotIndicator = selection[0]
    if pymel.attributeQuery('rigType', node=pivotIndicator, exists=True):
        rigType = pivotIndicator.rigType.get()
        if rigType != 'muscleBendPivotPosition':
            pymel.error('selection must be a single pivotPosition of a bend muscle')
    else:
        pymel.error('selection must be a single pivotPosition of a bend muscle')

    pivotIndicatorChildren = pymel.listRelatives(pivotIndicator, shapes=False)

#    jointsGroup = None
    muscleOriginInbetweenLocators = []
    muscleInsertionInbetweenLocators = []
    muscleOriginInbetweenJoints = []
    muscleInsertionInbetweenJoints = []

    for child in pivotIndicatorChildren:
       if pymel.attributeQuery('rigType', node=child, exists=True):
           rigType = child.rigType.get()

#           if rigType == 'jointsGroup':
#               jointsGroup = child

           if rigType == 'muscleMidPointLocatorB':
               muscleMidPointLocatorB = child

           if rigType == 'muscleOriginInbetweenLocator':
               muscleOriginInbetweenLocators.append(child)

           if rigType == 'muscleInsertionInbetweenLocator':
               muscleInsertionInbetweenLocators.append(child)

           if rigType == 'muscleMidPointLocatorB':
               muscleMidPointLocatorB = child

           if 'muscleOriginInbetweenJoint' in baseName:
               muscleOriginInbetweenJoints.append(joint)

           if 'muscleInsertionInbetweenJoint' in baseName:
               muscleInsertionInbetweenJoints.append(joint)

#    muscleOriginInbetweenJoints = []
#    muscleInsertionInbetweenJoints = []
#    if jointsGroup:
#        joints = pymel.listRelatives(jointsGroup, shapes=False, type='joint')
#        if joints:
#            for joint in joints:
#                if pymel.attributeQuery('baseName', node=joint, exists=True):
#                    print 'chea!'
#                    baseName = joint.baseName.get()
#
#                    if 'muscleOriginInbetweenJoint' in baseName:
#                        muscleOriginInbetweenJoints.append(joint)
#
#                    if 'muscleInsertionInbetweenJoint' in baseName:
#                        muscleInsertionInbetweenJoints.append(joint)

    baseName = pivotIndicator.baseName.get()
    userDefinedName = pivotIndicator.nodeName()[0:(-1*(len(baseName)+1))]

    if position[0] == 0:
        numberOfOriginJoints = len(muscleOriginInbetweenJoints)
        muscleInbetweenJoints = muscleOriginInbetweenJoints
        muscleInbetweenLocators = muscleOriginInbetweenLocators
        type = 'origin'
        muscleEndLocator = pivotIndicator.origin.inputs()[0]

    elif position[0] == 1:
        numberOfOriginJoints = len(muscleInsertionInbetweenJoints)
        muscleInbetweenJoints = muscleInsertionInbetweenJoints
        muscleInbetweenLocators = muscleInsertionInbetweenLocators
        type = 'insertion'
        muscleEndLocator = pivotIndicator.insertion.inputs()[0]

    print('muscleOriginInbetweenJoints: ', end=' ')
    print(muscleOriginInbetweenJoints)
    print('muscleInsertionInbetweenJoints: ', end=' ')
    print(muscleInsertionInbetweenJoints)
    print('userDefinedName: ', end=' ')
    print(userDefinedName)
    print('numberOfOriginJoints: ', end=' ')
    print(numberOfOriginJoints)
    print('pivotIndicator: ', end=' ')
    print(pivotIndicator)
    print('jointsGroup: ', end=' ')
    print(jointsGroup)
    print('muscleInbetweenJoints: ', end=' ')
    print(muscleInbetweenJoints)
    print('muscleEndLocator: ', end=' ')
    print(muscleEndLocator)

    _addJointToBendOriginMuscle(type, userDefinedName, numberOfOriginJoints, pivotIndicator, muscleInbetweenJoints, muscleInbetweenLocators, muscleMidPointLocatorB, muscleEndLocator,)

    pymel.select(selection)

def _modifyBendMuscle(bendMuscle, position, mode):
    pass

def _addJointToBendOriginMuscle(type, name, numberOfInbetweenJoints, pivotIndicator, muscleInbetweenJointsA, muscleInbetweenLocatorsA, muscleMidPointLocatorB, muscleOriginLocator, jointPercents=[]):
    total = numberOfInbetweenJoints+2
    i = numberOfInbetweenJoints
    Type = type[0].upper() + type[1:] #uppercased first letter
#    muscleInbetweenLocatorsA = []
#    muscleInbetweenJointsA = []
#    for i in range(numberOfInbetweenJoints[0]):

    muscleInbetweenLocator = pymel.spaceLocator(name=name+'muscle'+Type+'InbetweenLocator'+str(chain_i))
    muscleInbetweenLocatorShape = pymel.listRelatives(muscleInbetweenLocator, shapes=True)[0]
    pymel.addAttr(muscleInbetweenLocator, longName='rigType', dataType='string', keyable=True)
    muscleInbetweenLocator.rigType.set('muscle'+Type+'InbetweenLocator', lock=True)
    muscleInbetweenLocatorShape.localScale.set([0.2,0.2,0.2])
    pymel.parent(muscleInbetweenLocator, pivotIndicator)
    muscleInbetweenLocator.visibility.set(0)

#    if not muscleInbetweenLocatorsA:
#        muscleInbetweenLocatorPointConstraint = pymel.pointConstraint(muscleOriginLocator, muscleMidPointLocatorB, muscleInbetweenLocator)
#        muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleOriginLocator, muscleMidPointLocatorB, muscleInbetweenLocator)
#        muscleInbetweenLocatorOrientConstraint.interpType.set(2)
#    else:
    muscleInbetweenLocatorPointConstraint = pymel.pointConstraint(muscleOriginLocator, muscleInbetweenJointsA[-1], muscleInbetweenLocator)
    muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleOriginLocator, muscleInbetweenLocatorsA[-1], muscleInbetweenLocator)
    muscleInbetweenLocatorOrientConstraint.interpType.set(2)

    muscleInbetweenLocatorPointConstraint.w0.set(1)
    muscleInbetweenLocatorPointConstraint.w1.set(total-2)

    muscleInbetweenLocatorOrientConstraint.w0.set(1)
    muscleInbetweenLocatorOrientConstraint.w1.set(total-2)

    muscleInbetweenLocatorsA.append(muscleInbetweenLocator)


    muscleInbetweenJoint = pymel.createNode('joint', name=name+'muscle'+Type+'InbetweenJoint'+str(i))
    muscleInbetweenJoint.radius.set(0.2)
    muscleInbetweenJoint.addAttr('constraintPercent', defaultValue=1.0/(total-1.0), keyable=True)
    muscleInbetweenJointsA.append(muscleInbetweenJoint)
    pymel.addAttr(muscleInbetweenJoint, longName='rigType', dataType='string', keyable=True)
    muscleInbetweenJoint.rigType.set('muscleBendJoint', lock=True)
    pymel.addAttr(muscleInbetweenJoint, longName='baseName', dataType='string', keyable=True)
    muscleInbetweenJoint.baseName.set('muscle'+Type+'InbetweenJoint'+str(i), lock=True)
    pymel.parent(muscleInbetweenJoint, jointsGroup)


    plusMinusAverage = pymel.createNode('plusMinusAverage', name=name+'muscle'+Type+'InbetweenJoint'+str(i)+'_plusMinusAverage')
    plusMinusAverage.input1D[0].set(1)
    plusMinusAverage.operation.set(2)
    muscleInbetweenJoint.constraintPercent >> plusMinusAverage.input1D[1]

    muscleInbetweenJoint.constraintPercent >> muscleInbetweenLocatorPointConstraint.w0
    plusMinusAverage.output1D >> muscleInbetweenLocatorPointConstraint.w1

    muscleInbetweenJoint.constraintPercent >> muscleInbetweenLocatorOrientConstraint.w0
    plusMinusAverage.output1D >> muscleInbetweenLocatorOrientConstraint.w1

    muscleOriginInbetweenJoint_vectorProductA = pymel.createNode('vectorProduct', name=name+'muscle'+Type+'InbetweenJoint'+str(i)+'_vectorProductA')
    muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input1
    muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input2

    muscleOriginInbetweenJoint_vectorProductB = pymel.createNode('vectorProduct', name=name+'muscle'+Type+'InbetweenJoint'+str(i)+'_vectorProductB')
    muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input1
    muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input2
    muscleOriginInbetweenJoint_vectorProductB.normalizeOutput.set(1)
    muscleOriginInbetweenJoint_vectorProductB.operation.set(3)

    condition = pymel.createNode('condition', name=name+'muscle'+Type+'InbetweenJoint'+str(i)+'_condition')
    muscleOriginInbetweenJoint_vectorProductA.outputX >> condition.firstTerm
    condition.operation.set(2)
    condition.secondTerm.set(1)
    muscleInbetweenLocator.translate >> condition.colorIfTrue
    muscleOriginInbetweenJoint_vectorProductB.output >> condition.colorIfFalse
    condition.outColor >> muscleInbetweenJoint.translate

    total -= 1

    jointBefore = muscleInbetweenJointsA[-1]
    jointAfter = muscleInbetweenJointsA[0]

    aimConstraint = pymel.listRelatives(jointAfter, type='aimConstraint')[0]
    muscleUpVector_vectorProductC = aimConstraint.worldUpVectorY.inputs()[0]
    muscleUpVector_animCurveUU = aimConstraint.worldUpVectorZ.inputs()[0]
#    muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
#    muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
#    muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
#    muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ

    if type == 'origin':
        aimVector = [1,0,0]
    else:
        aimVector = [-1,0,0]
    aimConstraint = pymel.aimConstraint(jointAfter, muscleInbetweenJoint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocator, aimVector=aimVector, worldUpVector=[0,0,1], upVector=[0,0,1])
    muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
    muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
    muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
    muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ

#    for i, joint in enumerate(muscleInbetweenJointsA):
#        if joint == muscleInbetweenJointsA[0]:
#            pymel.aimConstraint(muscleMidPointLocatorB, joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsA[i], aimVector=[1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])
#        else:
#            pymel.aimConstraint(muscleInbetweenJointsA[i-1], joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsA[i], aimVector=[1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])

    colorAllMuscleJoints()

#----------------------------------------------------------------------
def globalizeConstraint(constraint):
    """replace constraint with a simplified version of itself that uses globalSpace"""

    if pymel.objectType(constraint) == 'orientConstraint':
        newConstraint = pymel.createNode('orientConstraint', name='local_'+constraint.nodeName())

        for i in range(constraint.target.get(size=True)):
            target = constraint.target[i].targetRotate.inputs()[0]
            target.worldMatrix[0] >> newConstraint.target[i].targetParentMatrix
            newConstraint.target[i].targetWeight.set(constraint.target[i].targetWeight.get())

        destination = constraint.constraintRotateX.outputs()
        if not destination:
            destination = constraint.constraintRotateY.outputs()
        if not destination:
            destination = constraint.constraintRotateZ.outputs()
        destination = destination[0]

        newConstraint.constraintRotate >> destination.rotate
        destination.parentInverseMatrix[0] >> newConstraint.constraintParentInverseMatrix
        destination.rotateOrder >> newConstraint.constraintRotateOrder
        pymel.delete(constraint)
        pymel.parent(newConstraint, destination)
        newConstraint.translate.set(0,0,0)
        newConstraint.rotate.set(0,0,0)

    return newConstraint



def _createBendMuscle(name='', radius=1, numberOfInbetweenJoints=[3,3]):

    if name:
        name = name+'_'

    ## create pivotIndicatorZro control
    #pivotIndicatorZro = pymel.circle(sweep=180, radius=1, name=name+'pivotPosition_zro')[0]
    #pivotIndicatorZro.rotateZ.set(-90)
    #pymel.delete(pivotIndicatorZro, constructionHistory=True)
    #pymel.makeIdentity(pivotIndicatorZro, apply=True, rotate=True)
    #pymel.addAttr(pivotIndicatorZro, longName='rigType', dataType='string', keyable=True)
    #pivotIndicatorZro.rigType.set('muscleBendPivotPositionZro', lock=True)


    ## create pivotIndicatorOri
    #pivotIndicatorOri = pymel.group(world=True, empty=True, name=name+'pivotIndicatorOri')
    #pymel.addAttr(pivotIndicatorOri, longName='rigType', dataType='string', keyable=True)
    #pivotIndicatorOri.rigType.set('muscleBendPivotPositionOri', lock=True)
    #pymel.parent(pivotIndicatorOri, pivotIndicatorZro)
    #pivotIndicatorOri.translate.lock()
    #pivotIndicatorOri.scale.lock()

    ## create pivotIndicatorAimTarget control
    #pivotIndicatorAimTargetShape = pymel.createNode('locator')
    #pivotIndicatorAimTarget = pivotIndicatorAimTargetShape.getParent()
    #pivotIndicatorAimTarget.rename(name+'pivotIndicatorAimTarget')
    #pymel.addAttr(pivotIndicatorAimTarget, longName='rigType', dataType='string', keyable=True)
    #pivotIndicatorAimTarget.rigType.set('muscleBendPivotPositionOri', lock=True)
    #pymel.parent(pivotIndicatorAimTarget, pivotIndicatorOri)
    #pivotIndicatorAimTarget.translate.set(0,1,0)
    #pivotIndicatorAimTargetShape.localScale.set([0.2,0.5,0.2])
    #pivotIndicatorAimTargetShape.visibility.set(0)
    #pivotIndicatorAimTarget.translateZ.lock()

    # create shape of pivotIndicator
    pivotIndicator = pymel.circle(sweep=180, radius=1, name=name+'pivotPosition')[0]
    pivotIndicator.rotateZ.set(-90)
    pymel.makeIdentity(pivotIndicator, apply=True, rotate=True)
    pivotIndicator.rotateY.set(-90)
    pymel.makeIdentity(pivotIndicator, apply=True, rotate=True)
    pymel.delete(pivotIndicator, constructionHistory=True)
    #pivotIndicator.translate.lock()

    pivotIndicatorShapeC = pymel.circle(sweep=360, radius=1,)[0]
    pivotIndicatorShapeC.rotateX.set(-90)
    pymel.makeIdentity(pivotIndicatorShapeC, apply=True, rotate=True)
    pymel.delete(pivotIndicatorShapeC, constructionHistory=True)
    shapeParent(pivotIndicatorShapeC, pivotIndicator)

    curveShape = pymel.curve( p=[(0.0, 0.0, 0.0), (0.0, 1.2, 0.0)], degree=1,)
    shapeParent(curveShape, pivotIndicator)
    #pymel.parent(pivotIndicator, pivotIndicatorZro)

    pivotIndicatorShapes = pymel.listRelatives(pivotIndicator, shapes=True)
    for i, shape in enumerate(pivotIndicatorShapes):
        if i == 0:
            shape.rename(pivotIndicator.name()+'Shape')
        else:
            shape.rename(pivotIndicator.name()+'Shape'+str(i))

    pivotIndicator.addAttr('pullWeight', defaultValue=0, keyable=True, minValue=0, maxValue=1)
    #pivotIndicator.addAttr('radius', defaultValue=radius, keyable=True)
    pymel.addAttr(pivotIndicator, longName='rigType', dataType='string', keyable=True)
    pivotIndicator.rigType.set('muscleBendPivotPosition', lock=True)
    pymel.addAttr(pivotIndicator, longName='baseName', dataType='string', keyable=True)
    pivotIndicator.baseName.set('pivotPosition', lock=True)
    pymel.addAttr(pivotIndicator, longName='origin', attributeType='message', keyable=True)
    pymel.addAttr(pivotIndicator, longName='insertion', attributeType='message', keyable=True)

    #jointsGroup = pivotIndicator
    jointsGroup = pymel.createNode('transform')
    jointsGroup.rename(name+'jointsGroup')
    pymel.parent(jointsGroup, pivotIndicator)

    pivotIndicatorOriCounterScale_multiplyDivide = pymel.createNode('multiplyDivide')
    #pivotIndicatorAimTarget.rename(name+'pivotIndicatorOriCounterScale_multiplyDivide')
    pivotIndicatorOriCounterScale_multiplyDivide.input1.set(1.0, 1.0, 1.0,)

    pivotIndicator.s >> pivotIndicatorOriCounterScale_multiplyDivide.input2
    pivotIndicatorOriCounterScale_multiplyDivide.operation.set(2)



    # create muscleOriginLocator
    muscleOriginLocator = pymel.spaceLocator(name=name+'muscleOriginLocator')
    muscleOriginLocatorShape = pymel.listRelatives(muscleOriginLocator, shapes=True)[0]
    muscleOriginLocatorShape.localScale.set([0.2,0.5,0.2])
    muscleOriginLocator.translateX.set(-2)
    pymel.addAttr(muscleOriginLocator, longName='rigType', dataType='string', keyable=True)
    muscleOriginLocator.rigType.set('muscleBendOrigin', lock=True)
    muscleOriginLocator.message >> pivotIndicator.origin

    muscleOriginLocatorShdw = pymel.group(name=name+'muscleOriginLocatorShdw', empty=True, world=True)
    pymel.addAttr(muscleOriginLocatorShdw, longName='rigType', dataType='string', keyable=True)
    muscleOriginLocatorShdw.rigType.set('muscleBendOriginShdw', lock=True)
    pymel.parent(muscleOriginLocatorShdw, pivotIndicator)
    pointConstraint = pymel.pointConstraint(muscleOriginLocator, muscleOriginLocatorShdw)
    orientConstraint = pymel.orientConstraint(muscleOriginLocator, muscleOriginLocatorShdw,)


    # create muscleInsertLocator
    muscleInsertLocator = pymel.spaceLocator(name=name+'muscleInsertLocator')
    muscleInsertLocatorShape = pymel.listRelatives(muscleInsertLocator, shapes=True)[0]
    muscleInsertLocatorShape.localScale.set([0.2,0.5,0.2])
    muscleInsertLocator.translateX.set(2)
    pymel.addAttr(muscleInsertLocator, longName='rigType', dataType='string', keyable=True)
    muscleInsertLocator.rigType.set('muscleBendInsertion', lock=True)
    muscleInsertLocator.message >> pivotIndicator.insertion

    muscleInsertLocatorShdw = pymel.group(name=name+'muscleInsertLocatorShdw', empty=True, world=True)
    pymel.addAttr(muscleInsertLocatorShdw, longName='rigType', dataType='string', keyable=True)
    muscleInsertLocatorShdw.rigType.set('muscleInsertLocatorShdw', lock=True)
    pymel.parent(muscleInsertLocatorShdw, pivotIndicator)
    pointConstraint = pymel.pointConstraint(muscleInsertLocator, muscleInsertLocatorShdw)
    orientConstraint = pymel.orientConstraint(muscleInsertLocator, muscleInsertLocatorShdw,)


    # constrain pivotIndicatorAimTarget between origin and insertion locators
    #pointConstraint = pymel.pointConstraint(muscleOriginLocator, muscleInsertLocator, pivotIndicatorAimTarget, skip=['z',])
    #pivotIndicatorAimTargetPointConstraint = pointConstraint
    #yInput = pivotIndicatorAimTarget.translateY.inputs()[0]
    #condition = pymel.createNode('condition')
    #pointConstraint.constraintTranslateY >> condition.firstTerm
    #pointConstraint.constraintTranslateY >> condition.colorIfTrueR
    #condition.outColorR >> pivotIndicatorAimTarget.translateY
    #condition.secondTerm.set(1)
    #condition.colorIfFalseR.set(1)
    #condition.operation.set(2)

    #orientConstraint = pymel.orientConstraint(muscleOriginLocator, muscleInsertLocator, pivotIndicatorOri)
    #orientConstraint = globalizeConstraint(orientConstraint)
    #orientConstraint.interpType.set(2)
    #aimConstraint = pymel.aimConstraint(pivotIndicatorAimTarget, pivotIndicator, worldUpType='objectrotation', worldUpObject=pivotIndicatorOri, aimVector=[0,1,0], worldUpVector=[0,0,1], upVector=[0,0,1])


    # create mid point locators
    muscleMidPointLocator = pymel.spaceLocator(name=name+'muscleMidPointLocator')
    muscleMidPointLocatorShape = pymel.listRelatives(muscleMidPointLocator, shapes=True)[0]
    muscleMidPointLocatorShape.localScale.set([0.2,0.2,0.2])
    pymel.parent(muscleMidPointLocator, pivotIndicator)
    pymel.addAttr(muscleMidPointLocator, longName='rigType', dataType='string', keyable=True)
    muscleMidPointLocator.rigType.set('muscleMidPointLocator', lock=True)

    muscleMidPointLocator_blendPosition = pymel.createNode('blendColors', name=name+'muscleMidPointLocator_blendPosition')
    muscleMidPointLocator_blendPosition.blender.set(0.5)
    muscleOriginLocatorShdw.translate >> muscleMidPointLocator_blendPosition.color1
    muscleInsertLocatorShdw.translate >> muscleMidPointLocator_blendPosition.color2
    muscleMidPointLocator.visibility.set(0)

    #muscleMidPointLocator_blendPositionY = pymel.createNode('blendColors', name=name+'muscleMidPointLocator_blendPositionY')
    #muscleMidPointLocator_blendPositionY.blender.set(0.5)
    #muscleOriginLocatorShdw.translateY >> muscleMidPointLocator_blendPositionY.color1G
    #muscleInsertLocatorShdw.translateY >> muscleMidPointLocator_blendPositionY.color2G
    #muscleMidPointLocator.visibility.set(0)

    #muscleMidPointLocator_blendPositionZ = pymel.createNode('blendColors', name=name+'muscleMidPointLocator_blendPositionZ')
    #muscleMidPointLocator_blendPositionZ.blender.set(0.5)
    #muscleOriginLocatorShdw.translateZ >> muscleMidPointLocator_blendPositionZ.color1B
    #muscleInsertLocatorShdw.translateZ >> muscleMidPointLocator_blendPositionZ.color2B
    #muscleMidPointLocator.visibility.set(0)

    blendColor = pymel.createNode('blendColors', name=name+'muscleMidPointLocator')
    pivotIndicator.pullWeight >> blendColor.blender
    muscleMidPointLocator_blendPosition.output >> blendColor.color2
    #muscleMidPointLocator_blendPositionY.outputG >> blendColor.color2G
    #muscleMidPointLocator_blendPositionZ.outputB >> blendColor.color2B
    blendColor.color1.set(0,1,0)
    #blendColor.outputG >> muscleMidPointLocator.translateY
    blendColor.output >> muscleMidPointLocator.translate


    muscleMidPointLocatorB = pymel.spaceLocator(name=name+'muscleMidPointLocatorB')
    muscleMidPointLocatorBShape = pymel.listRelatives(muscleMidPointLocatorB, shapes=True)[0]
    muscleMidPointLocatorBShape.localScale.set([0.2,0.2,0.2])
    pymel.parent(muscleMidPointLocatorB, pivotIndicator)
    pymel.addAttr(muscleMidPointLocatorB, longName='rigType', dataType='string', keyable=True)
    muscleMidPointLocatorB.rigType.set('muscleMidPointLocatorB', lock=True)
    muscleMidPointLocatorB.visibility.set(0)

    muscleMidPointLocatorC = pymel.spaceLocator(name=name+'muscleMidPointLocatorC')
    muscleMidPointLocatorCShape = pymel.listRelatives(muscleMidPointLocatorC, shapes=True)[0]
    muscleMidPointLocatorCShape.localScale.set([0.2,0.2,0.2])
    pymel.parent(muscleMidPointLocatorC, pivotIndicator)
    pymel.addAttr(muscleMidPointLocatorC, longName='rigType', dataType='string', keyable=True)
    muscleMidPointLocatorC.rigType.set('muscleMidPointLocatorC', lock=True)
    muscleMidPointLocatorC.visibility.set(0)
    condition = pymel.createNode('condition', name=name+'midPointCollide_condition')
    muscleMidPointLocator.translateY >> condition.firstTerm
    condition.secondTerm.set(1)
    condition.operation.set(2)
    muscleMidPointLocator.translateY >> condition.colorIfTrueG
    condition.colorIfFalseR.set(0)
    condition.colorIfFalseB.set(0)
    condition.outColor >> muscleMidPointLocatorB.translate




    vectorProductA = pymel.createNode('vectorProduct', name=name+'vectorProductA')

    vectorProductB = pymel.createNode('vectorProduct', name=name+'vectorProductB')
    muscleMidPointLocatorC.translate >> vectorProductB.input1
    muscleMidPointLocatorC.translate >> vectorProductB.input2

    vectorProductC = pymel.createNode('vectorProduct', name=name+'vectorProductC')
    muscleMidPointLocatorC.translate >> vectorProductC.input1
    vectorProductC.normalizeOutput.set(1)
    vectorProductC.operation.set(3)



    joints = []

    muscleOriginJoint = pymel.createNode('joint', name=name+'muscleOriginJoint')
    muscleOriginJoint.radius.set(0.2)
    muscleOriginLocatorShdw.translate >> muscleOriginJoint.translate
    pymel.parent(muscleOriginJoint, jointsGroup)
    pymel.addAttr(muscleOriginJoint, longName='rigType', dataType='string', keyable=True)
    muscleOriginJoint.rigType.set('muscleBendJoint', lock=True)
    pymel.addAttr(muscleOriginJoint, longName='indexNum', dataType='string', keyable=True)
    muscleOriginJoint.indexNum.set(str(0), lock=True)

    muscleMidPointJoint = pymel.createNode('joint', name=name+'muscleMidPointJoint')
    muscleMidPointJoint.radius.set(0.2)
    muscleMidPointJoint.addAttr('constraintPercent', defaultValue=0.5, keyable=True, maxValue=1, minValue=0)
    #muscleMidPointJoint.addAttr('constraintPercentY', defaultValue=0.5, keyable=True, maxValue=1, minValue=0)
    #muscleMidPointJoint.addAttr('constraintPercentZ', defaultValue=0.0, keyable=True, maxValue=1, minValue=0)
    pymel.parent(muscleMidPointJoint, jointsGroup)
    pymel.addAttr(muscleMidPointJoint, longName='rigType', dataType='string', keyable=True)
    muscleMidPointJoint.rigType.set('muscleBendJoint', lock=True)
    pymel.addAttr(muscleMidPointJoint, longName='baseName', dataType='string', keyable=True)
    muscleMidPointJoint.baseName.set('muscleMidPointJoint', lock=True)

    #hook up the percent blend of the mid joint to the point constraint of the pivotIndicatorAimTarget
    plusMinusAverage = pymel.createNode('plusMinusAverage')
    plusMinusAverage.input1D[0].set(1)
    plusMinusAverage.operation.set(2)
    muscleMidPointJoint.constraintPercent >> plusMinusAverage.input1D[1]
    #muscleMidPointJoint.constraintPercent >> pivotIndicatorAimTargetPointConstraint.w0
    #plusMinusAverage.output1D >> pivotIndicatorAimTargetPointConstraint.w1
    muscleMidPointJoint.constraintPercent >> muscleMidPointLocator_blendPosition.blender
    #muscleMidPointJoint.constraintPercentY >> muscleMidPointLocator_blendPositionY.blender
    #muscleMidPointJoint.constraintPercentZ >> muscleMidPointLocator_blendPositionZ.blender
    pivotIndicatorOriCounterScale_multiplyDivide.output >> muscleMidPointJoint.s

    muscleInsertJoint = pymel.createNode('joint', name=name+'muscleInsertJoint')
    muscleInsertJoint.radius.set(0.2)
    muscleInsertLocatorShdw.translate >> muscleInsertJoint.translate
    pymel.parent(muscleInsertJoint, jointsGroup)
    pymel.addAttr(muscleInsertJoint, longName='rigType', dataType='string', keyable=True)
    muscleInsertJoint.rigType.set('muscleBendJoint', lock=True)
    pymel.addAttr(muscleInsertJoint, longName='indexNum', dataType='string', keyable=True)
    muscleInsertJoint.indexNum.set(str(numberOfInbetweenJoints[0]+numberOfInbetweenJoints[1]+2), lock=True)

    conditionB = pymel.createNode('condition', name=name+'midPointCollide_conditionB')
    vectorProductB.outputX >> conditionB.firstTerm
    conditionB.secondTerm.set(1)
    conditionB.operation.set(2)
    muscleMidPointLocatorC.translate >> conditionB.colorIfTrue
    vectorProductC.output >> conditionB.colorIfFalse
    conditionB.outColor >> muscleMidPointJoint.translate


    total = numberOfInbetweenJoints[0]+2
    muscleInbetweenLocatorsA = []
    muscleInbetweenJointsA = []
    for i in range(numberOfInbetweenJoints[0]):
        muscleInbetweenLocator = pymel.spaceLocator(name=name+'muscleOriginInbetweenLocator'+str(i))
        muscleInbetweenLocatorShape = pymel.listRelatives(muscleInbetweenLocator, shapes=True)[0]
        muscleInbetweenLocatorShape.localScale.set([0.2,0.2,0.2])
        pymel.addAttr(muscleInbetweenLocator, longName='rigType', dataType='string', keyable=True)
        muscleInbetweenLocator.rigType.set('muscleOriginInbetweenLocator', lock=True)
        pymel.parent(muscleInbetweenLocator, pivotIndicator)
        muscleInbetweenLocatorShape.visibility.set(0)

        if not muscleInbetweenLocatorsA:
            muscleInbetweenJoint_blendPosition = pymel.createNode('blendColors', name=name+'muscleInbetweenJoint_blendPosition'+str(i))
            muscleOriginLocatorShdw.translate >> muscleInbetweenJoint_blendPosition.color1
            muscleMidPointLocatorB.translate >> muscleInbetweenJoint_blendPosition.color2


            muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleOriginLocatorShdw, muscleMidPointLocatorB, muscleInbetweenLocator)
            muscleInbetweenLocatorOrientConstraint.interpType.set(2)
        else:
            muscleInbetweenJoint_blendPosition = pymel.createNode('blendColors', name=name+'muscleInbetweenJoint_blendPosition'+str(i))
            muscleOriginLocatorShdw.translate >> muscleInbetweenJoint_blendPosition.color1
            muscleInbetweenJointsA[-1].translate >> muscleInbetweenJoint_blendPosition.color2

            muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleOriginLocatorShdw, muscleInbetweenLocatorsA[-1], muscleInbetweenLocator)
            muscleInbetweenLocatorOrientConstraint.interpType.set(2)

        muscleInbetweenJoint_blendPosition.output >> muscleInbetweenLocator.translate
        muscleInbetweenLocatorOrientConstraint = ka_constraints.localizeConstraint(muscleInbetweenLocatorOrientConstraint)
        muscleInbetweenLocatorOrientConstraint.interpType.set(2)

        muscleInbetweenLocatorOrientConstraint.target[0].targetWeight.set(1)
        muscleInbetweenLocatorOrientConstraint.target[0].targetWeight.set(total-2)

        muscleInbetweenLocatorsA.append(muscleInbetweenLocator)


        muscleInbetweenJoint = pymel.createNode('joint', name=name+'muscleOriginInbetweenJoint'+str(i))
        pymel.parent(muscleInbetweenJoint, jointsGroup)
        muscleInbetweenJoint.radius.set(0.2)
        muscleInbetweenJoint.addAttr('constraintPercent', defaultValue=1.0/(total-1.0), keyable=True, maxValue=1, minValue=0)
        muscleInbetweenJointsA.append(muscleInbetweenJoint)
        pymel.addAttr(muscleInbetweenJoint, longName='rigType', dataType='string', keyable=True)
        muscleInbetweenJoint.rigType.set('muscleBendJoint', lock=True)
        pymel.addAttr(muscleInbetweenJoint, longName='baseName', dataType='string', keyable=True)
        muscleInbetweenJoint.baseName.set('muscleOriginInbetweenJoint'+str(i), lock=True)


        plusMinusAverage = pymel.createNode('plusMinusAverage', name=name+'muscleOriginInbetweenJoint'+str(i)+'_plusMinusAverage')
        plusMinusAverage.input1D[0].set(1)
        plusMinusAverage.operation.set(2)
        muscleInbetweenJoint.constraintPercent >> plusMinusAverage.input1D[1]

        muscleInbetweenJoint.constraintPercent >> muscleInbetweenJoint_blendPosition.blender

        muscleInbetweenJoint.constraintPercent >> muscleInbetweenLocatorOrientConstraint.target[0].targetWeight
        plusMinusAverage.output1D >> muscleInbetweenLocatorOrientConstraint.target[1].targetWeight

        muscleOriginInbetweenJoint_vectorProductA = pymel.createNode('vectorProduct', name=name+'muscleOriginInbetweenJoint'+str(i)+'_vectorProductA')
        muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input1
        muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input2

        muscleOriginInbetweenJoint_vectorProductB = pymel.createNode('vectorProduct', name=name+'muscleOriginInbetweenJoint'+str(i)+'_vectorProductB')
        muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input1
        muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input2
        muscleOriginInbetweenJoint_vectorProductB.normalizeOutput.set(1)
        muscleOriginInbetweenJoint_vectorProductB.operation.set(3)

        condition = pymel.createNode('condition', name=name+'muscleOriginInbetweenJoint'+str(i)+'_condition')
        muscleOriginInbetweenJoint_vectorProductA.outputX >> condition.firstTerm
        condition.operation.set(2)
        condition.secondTerm.set(1)
        muscleInbetweenLocator.translate >> condition.colorIfTrue
        muscleOriginInbetweenJoint_vectorProductB.output >> condition.colorIfFalse
        condition.outColor >> muscleInbetweenJoint.translate
        pivotIndicatorOriCounterScale_multiplyDivide.output >> muscleInbetweenJoint.s
        total -= 1


    muscleUpVector_vectorProductC = pymel.createNode('vectorProduct', name=name+'muscleUpVector_vectorProductC')
    muscleUpVector_vectorProductC.operation.set(1)
    muscleUpVector_vectorProductC.normalizeOutput.set(1)
    muscleOriginLocatorShdw.translate >> muscleUpVector_vectorProductC.input1
    muscleUpVector_vectorProductC.input2.set(0,0,1)

    muscleUpVector_animCurveUU = pymel.createNode('animCurveUU', name=name+'muscleUpVector_plusMinusAverage')
    muscleUpVector_vectorProductC.outputX >> muscleUpVector_animCurveUU.input
    pymel.setKeyframe(muscleUpVector_animCurveUU, float=1, value=0, inTangentType='linear', outTangentType='linear',)
    pymel.setKeyframe(muscleUpVector_animCurveUU, float=0, value=1, inTangentType='linear', outTangentType='linear',)
    pymel.setKeyframe(muscleUpVector_animCurveUU, float=-1, value=0, inTangentType='linear', outTangentType='linear',)

    aimConstraint = pymel.aimConstraint(muscleInbetweenJointsA[-1], muscleOriginJoint, worldUpType='objectrotation', worldUpObject=muscleOriginLocatorShdw, aimVector=[1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])
    aimConstraint = ka_constraints.localizeConstraint(aimConstraint)
    muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
    muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
    muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
    muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ
    for i, joint in enumerate(muscleInbetweenJointsA):
        if joint == muscleInbetweenJointsA[0]:
            aimConstraint = pymel.aimConstraint(muscleMidPointLocatorB, joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsA[i], aimVector=[1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])
        else:
            aimConstraint = pymel.aimConstraint(muscleInbetweenJointsA[i-1], joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsA[i], aimVector=[1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])

        aimConstraint = ka_constraints.localizeConstraint(aimConstraint)
        muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
        muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
        muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
        muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ


    total = numberOfInbetweenJoints[1]+2
    muscleInbetweenLocatorsB = []
    muscleInbetweenJointsB = []
    for i in range(numberOfInbetweenJoints[1]):
        muscleInbetweenLocator = pymel.spaceLocator(name=name+'muscleInsertionInbetweenLocator'+str(i))
        muscleInbetweenLocatorShape = pymel.listRelatives(muscleInbetweenLocator, shapes=True)[0]
        muscleInbetweenLocatorShape.localScale.set([0.2,0.2,0.2])
        pymel.addAttr(muscleInbetweenLocator, longName='rigType', dataType='string', keyable=True)
        muscleInbetweenLocator.rigType.set('muscleInsertionInbetweenLocator', lock=True)
        pymel.parent(muscleInbetweenLocator, pivotIndicator)
        muscleInbetweenLocatorShape.visibility.set(0)

        if not muscleInbetweenLocatorsB:
            muscleInbetweenJoint_blendPosition = pymel.createNode('blendColors', name=name+'muscleInbetweenJoint_blendPosition'+str(i))
            muscleInsertLocatorShdw.translate >> muscleInbetweenJoint_blendPosition.color1
            muscleMidPointLocatorB.translate >> muscleInbetweenJoint_blendPosition.color2

            muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleInsertLocatorShdw, muscleMidPointLocatorB, muscleInbetweenLocator)
            muscleInbetweenLocatorOrientConstraint.interpType.set(2)
        else:
            muscleInbetweenJoint_blendPosition = pymel.createNode('blendColors', name=name+'muscleInbetweenJoint_blendPosition'+str(i))
            muscleInsertLocatorShdw.translate >> muscleInbetweenJoint_blendPosition.color1
            muscleInbetweenJointsB[-1].translate >> muscleInbetweenJoint_blendPosition.color2

            muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleInsertLocatorShdw, muscleInbetweenLocatorsB[-1], muscleInbetweenLocator)
            muscleInbetweenLocatorOrientConstraint.interpType.set(2)

        muscleInbetweenJoint_blendPosition.output >> muscleInbetweenLocator.translate
        muscleInbetweenLocatorOrientConstraint = ka_constraints.localizeConstraint(muscleInbetweenLocatorOrientConstraint)
        muscleInbetweenLocatorOrientConstraint.interpType.set(2)

        muscleInbetweenJoint = pymel.createNode('joint', name=name+'muscleInsertionInbetweenJoint'+str(i))
        pymel.parent(muscleInbetweenJoint, jointsGroup)
        muscleInbetweenJoint.radius.set(0.2)
        muscleInbetweenJoint.addAttr('constraintPercent', defaultValue=1.0/(total-1.0), keyable=True, maxValue=1, minValue=0)
        muscleInbetweenJointsB.append(muscleInbetweenJoint)
        pymel.addAttr(muscleInbetweenJoint, longName='rigType', dataType='string', keyable=True)
        muscleInbetweenJoint.rigType.set('muscleBendJoint', lock=True)
        pymel.addAttr(muscleInbetweenJoint, longName='baseName', dataType='string', keyable=True)
        muscleInbetweenJoint.baseName.set('muscleInsertionInbetweenJoint'+str(i), lock=True)
        muscleInbetweenLocatorsB.append(muscleInbetweenLocator)
        pymel.addAttr(muscleInbetweenJoint, longName='indexNum', dataType='string', keyable=True)
        muscleInbetweenJoint.indexNum.set(str(numberOfInbetweenJoints[0]+i+2), lock=True)

        plusMinusAverage = pymel.createNode('plusMinusAverage', name=name+'muscleInsertionInbetweenJoint'+str(i)+'_plusMinusAverage')
        plusMinusAverage.input1D[0].set(1)
        plusMinusAverage.operation.set(2)
        muscleInbetweenJoint.constraintPercent >> plusMinusAverage.input1D[1]

        muscleInbetweenJoint.constraintPercent >> muscleInbetweenJoint_blendPosition.blender

        muscleInbetweenJoint.constraintPercent >> muscleInbetweenLocatorOrientConstraint.target[0].targetWeight
        plusMinusAverage.output1D >> muscleInbetweenLocatorOrientConstraint.target[1].targetWeight

        muscleOriginInbetweenJoint_vectorProductA = pymel.createNode('vectorProduct', name=name+'muscleInsertionInbetweenJoint'+str(i)+'_vectorProductA')
        muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input1
        muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input2

        muscleOriginInbetweenJoint_vectorProductB = pymel.createNode('vectorProduct', name=name+'muscleInsertionInbetweenJoint'+str(i)+'_vectorProductB')
        muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input1
        muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input2
        muscleOriginInbetweenJoint_vectorProductB.normalizeOutput.set(1)
        muscleOriginInbetweenJoint_vectorProductB.operation.set(3)

        condition = pymel.createNode('condition', name=name+'muscleInsertionInbetweenJoint'+str(i)+'_condition')
        muscleOriginInbetweenJoint_vectorProductA.outputX >> condition.firstTerm
        condition.secondTerm.set(1)
        condition.operation.set(2)
        muscleInbetweenLocator.translate >> condition.colorIfTrue
        muscleOriginInbetweenJoint_vectorProductB.output >> condition.colorIfFalse
        condition.outColor >> muscleInbetweenJoint.translate
        pivotIndicatorOriCounterScale_multiplyDivide.output >> muscleInbetweenJoint.s

        total -= 1


    muscleUpVector_vectorProductC = pymel.createNode('vectorProduct', name=name+'muscleUpVector_vectorProductC')
    muscleUpVector_vectorProductC.operation.set(1)
    muscleUpVector_vectorProductC.normalizeOutput.set(1)
    muscleInsertLocatorShdw.translate >> muscleUpVector_vectorProductC.input1
    muscleUpVector_vectorProductC.input2.set(0,0,1)

    muscleUpVector_animCurveUU = pymel.createNode('animCurveUU', name=name+'muscleUpVector_plusMinusAverage')
    muscleUpVector_vectorProductC.outputX >> muscleUpVector_animCurveUU.input
    pymel.setKeyframe(muscleUpVector_animCurveUU, float=1, value=0, inTangentType='linear', outTangentType='linear',)
    pymel.setKeyframe(muscleUpVector_animCurveUU, float=0, value=1, inTangentType='linear', outTangentType='linear',)
    pymel.setKeyframe(muscleUpVector_animCurveUU, float=-1, value=0, inTangentType='linear', outTangentType='linear',)


    aimConstraint = pymel.aimConstraint(muscleInbetweenJointsB[-1], muscleInsertJoint, worldUpType='objectrotation', worldUpObject=muscleInsertLocatorShdw, aimVector=[-1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])
    aimConstraint = ka_constraints.localizeConstraint(aimConstraint)
    muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
    muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
    muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
    muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ
    for i, joint in enumerate(muscleInbetweenJointsB):
        if joint == muscleInbetweenJointsB[0]:
            aimConstraint = pymel.aimConstraint(muscleMidPointLocatorB, joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsB[i], aimVector=[-1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])
        else:
            aimConstraint = pymel.aimConstraint(muscleInbetweenJointsB[i-1], joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsB[i], aimVector=[-1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])

        aimConstraint = ka_constraints.localizeConstraint(aimConstraint)
        muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
        muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
        muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
        muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ

    muscleMidPointLocatorC_averagePosition = pymel.createNode('plusMinusAverage', name=name+'muscleMidPointLocatorC_averagePosition')
    muscleMidPointLocatorC_averagePosition.operation.set(3)
    muscleInbetweenJointsB[0].translate >> muscleMidPointLocatorC_averagePosition.input3D[0]
    muscleInbetweenJointsA[0].translate >> muscleMidPointLocatorC_averagePosition.input3D[1]
    muscleMidPointLocatorB.translate >> muscleMidPointLocatorC_averagePosition.input3D[2]
    muscleMidPointLocatorC_averagePosition.output3D >> muscleMidPointLocatorC.translate

    muscleMidPointJointC_orientConstraint = pymel.orientConstraint(muscleInbetweenJointsB[0], muscleInbetweenJointsA[0], muscleMidPointJoint)
    muscleMidPointJointC_orientConstraint = ka_constraints.localizeConstraint(muscleMidPointJointC_orientConstraint)
    muscleMidPointJointC_orientConstraint.interpType.set(2)

    #pivotIndicator.radius >> pivotIndicatorZro.scaleX
    #pivotIndicator.radius >> pivotIndicatorZro.scaleY
    #pivotIndicator.radius >> pivotIndicatorZro.scaleZ


    ## RIG PIVOT POSITION TO ROTATE
    ## -----------------------------

    ## GET RELATED NODES:
    #pivotIndicator = pymel.ls('asdf_pivotPosition')[0]
    #muscleOriginLocator = pymel.ls('asdf_muscleOriginLocator')[0]
    #muscleInsertLocator = pymel.ls('asdf_muscleInsertLocator')[0]


    ## CREATE NODES: ##
    asdf_pivotPosition_orientConstraint1__4jj5wo__ = pymel.createNode('orientConstraint', parent=pivotIndicator,  )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.rename('asdf_pivotPosition_orientConstraint1')
    asdf_pivotPosition_aimConstraint1__4jj4s0__ = pymel.createNode('aimConstraint', parent=pivotIndicator,  )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.rename('asdf_pivotPosition_aimConstraint1')
    plusMinusAverage5__1lt6chs__ = pymel.createNode('plusMinusAverage', )
    plusMinusAverage5__1lt6chs__.rename('plusMinusAverage5')
    vectorProduct6__1lt6b4g__ = pymel.createNode('vectorProduct', )
    vectorProduct6__1lt6b4g__.rename('vectorProduct6')
    vectorProduct7__1lt6btc__ = pymel.createNode('vectorProduct', )
    vectorProduct7__1lt6btc__.rename('vectorProduct7')
    condition1__1lwls00__ = pymel.createNode('condition', )
    condition1__1lwls00__.rename('condition1')
    vectorProduct11__1lwlrbk__ = pymel.createNode('vectorProduct', )
    vectorProduct11__1lwlrbk__.rename('vectorProduct11')
    plusMinusAverage6__1lwlqs0__ = pymel.createNode('plusMinusAverage', )
    plusMinusAverage6__1lwlqs0__.rename('plusMinusAverage6')
    vectorProduct9__1lwlpgw__ = pymel.createNode('vectorProduct', )
    vectorProduct9__1lwlpgw__.rename('vectorProduct9')
    vectorProduct10__1lwlq3k__ = pymel.createNode('vectorProduct', )
    vectorProduct10__1lwlq3k__.rename('vectorProduct10')
    animCurveUU2__1lwlt8w__ = pymel.createNode('animCurveUU', )
    animCurveUU2__1lwlt8w__.rename('animCurveUU2')
    vectorProduct12__1lwlsmo__ = pymel.createNode('vectorProduct', )
    vectorProduct12__1lwlsmo__.rename('vectorProduct12')
    asdf_pivotPosition_orientConstraint2__4jgk5c__ = pymel.createNode('orientConstraint', parent=pivotIndicator,  )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.rename('asdf_pivotPosition_orientConstraint2')
    animCurveUU3__1jkm34w__ = pymel.createNode('animCurveUU', )
    animCurveUU3__1jkm34w__.rename('animCurveUU3')



    ## ADD ATTRS: ##
    asdf_pivotPosition_orientConstraint1__4jj5wo__.addAttr('asdf_muscleInsertLocatorW0', attributeType='double', shortName='w0', hasMinValue=True, minValue=0.0, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.addAttr('asdf_muscleOriginLocatorW1', attributeType='double', shortName='w1', hasMinValue=True, minValue=0.0, )

    asdf_pivotPosition_orientConstraint2__4jgk5c__.addAttr('asdf_muscleInsertLocatorW0', attributeType='double', shortName='w0', hasMinValue=True, minValue=0.0, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.addAttr('asdf_muscleOriginLocatorW1', attributeType='double', shortName='w1', hasMinValue=True, minValue=0.0, )




    ## SET ATTRS: ##
    asdf_pivotPosition_orientConstraint1__4jj5wo__.nodeState.set(0, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.visibility.set(True, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.translate.translateX.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.translate.translateY.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.translate.translateZ.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.rotate.rotateX.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.rotate.rotateY.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.rotate.rotateZ.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.scale.scaleX.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.scale.scaleY.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.scale.scaleZ.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.enableRestPosition.set(True, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.restRotate.restRotateZ.set(6.95195208022, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.interpType.set(2, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.asdf_muscleInsertLocatorW0.set(1.0, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.asdf_muscleOriginLocatorW1.set(1.0, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.asdf_muscleInsertLocatorW0.set(1.0, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint1__4jj5wo__.asdf_muscleOriginLocatorW1.set(1.0, keyable=True, channelBox=False, )

    asdf_pivotPosition_aimConstraint1__4jj4s0__.nodeState.set(0, keyable=True, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.visibility.set(True, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.translate.translateX.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.translate.translateY.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.translate.translateZ.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.rotate.rotateX.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.rotate.rotateY.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.rotate.rotateZ.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.scale.scaleX.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.scale.scaleY.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.scale.scaleZ.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.enableRestPosition.set(True, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.target[0].targetTranslate.targetTranslateX.set(3.50696161767e-15, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.target[0].targetTranslate.targetTranslateY.set(3.24136137962, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.target[0].targetTranslate.targetTranslateZ.set(12.7939519882, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.aimVector.aimVectorX.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.upVector.upVectorY.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.upVector.upVectorZ.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.worldUpVector.worldUpVectorX.set(-1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.worldUpVector.worldUpVectorY.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.worldUpVector.worldUpVectorZ.set(2.22044604925e-16, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintTranslate.constraintTranslateX.set(8.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintTranslate.constraintTranslateY.set(0.979946428075, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintTranslate.constraintTranslateZ.set(1.7763568394e-15, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintRotate.constraintRotateX.set(-8.71855165607e-15, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintRotate.constraintRotateY.set(-4.92234270002e-15, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintRotate.constraintRotateZ.set(-58.8966349154, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintVector.constraintVectorX.set(1.4984217641e-15, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintVector.constraintVectorY.set(2.26141495155, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintVector.constraintVectorZ.set(3.74829265214, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.restRotate.restRotateX.set(3.22666125386e-16, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.restRotate.restRotateY.set(-3.29053531035e-15, keyable=False, channelBox=False, )
    asdf_pivotPosition_aimConstraint1__4jj4s0__.restRotate.restRotateZ.set(-11.200907761, keyable=False, channelBox=False, )

    plusMinusAverage5__1lt6chs__.operation.set(3, keyable=False, channelBox=False, )
    plusMinusAverage5__1lt6chs__.input3D[0].input3Dx.set(2.00853979343e-15, keyable=True, channelBox=False, )
    plusMinusAverage5__1lt6chs__.input3D[0].input3Dy.set(3.24136137962, keyable=True, channelBox=False, )
    plusMinusAverage5__1lt6chs__.input3D[0].input3Dz.set(1.04565930367, keyable=True, channelBox=False, )
    plusMinusAverage5__1lt6chs__.input3D[1].input3Dx.set(5.00538365367e-15, keyable=True, channelBox=False, )
    plusMinusAverage5__1lt6chs__.input3D[1].input3Dy.set(3.24136137962, keyable=True, channelBox=False, )
    plusMinusAverage5__1lt6chs__.input3D[1].input3Dz.set(24.5422439575, keyable=True, channelBox=False, )
    plusMinusAverage5__1lt6chs__.output3D.output3Dx.set(3.50696161767e-15, keyable=False, channelBox=False, )
    plusMinusAverage5__1lt6chs__.output3D.output3Dy.set(3.24136137962, keyable=False, channelBox=False, )
    plusMinusAverage5__1lt6chs__.output3D.output3Dz.set(12.7939519882, keyable=False, channelBox=False, )

    vectorProduct6__1lt6b4g__.operation.set(4, keyable=False, channelBox=False, )

    vectorProduct7__1lt6btc__.operation.set(4, keyable=False, channelBox=False, )

    condition1__1lwls00__.operation.set(3, keyable=False, channelBox=False, )
    condition1__1lwls00__.colorIfTrue.colorIfTrueR.set(1.0, keyable=True, channelBox=False, )
    condition1__1lwls00__.colorIfFalse.colorIfFalseR.set(-1.0, keyable=True, channelBox=False, )
    condition1__1lwls00__.outColor.outColorR.set(1.0, keyable=False, channelBox=False, )

    vectorProduct11__1lwlrbk__.operation.set(4, keyable=False, channelBox=False, )
    vectorProduct11__1lwlrbk__.input1.input1X.set(5.00538365367e-15, keyable=True, channelBox=False, )
    vectorProduct11__1lwlrbk__.input1.input1Y.set(3.24136137962, keyable=True, channelBox=False, )
    vectorProduct11__1lwlrbk__.input1.input1Z.set(24.5422439575, keyable=True, channelBox=False, )

    plusMinusAverage6__1lwlqs0__.operation.set(3, keyable=False, channelBox=False, )
    plusMinusAverage6__1lwlqs0__.input3D[0].input3Dx.set(-1.0, keyable=True, channelBox=False, )
    plusMinusAverage6__1lwlqs0__.input3D[0].input3Dy.set(0.0, keyable=True, channelBox=False, )
    plusMinusAverage6__1lwlqs0__.input3D[0].input3Dz.set(2.22044604925e-16, keyable=True, channelBox=False, )
    plusMinusAverage6__1lwlqs0__.input3D[1].input3Dx.set(-1.0, keyable=True, channelBox=False, )
    plusMinusAverage6__1lwlqs0__.input3D[1].input3Dy.set(0.0, keyable=True, channelBox=False, )
    plusMinusAverage6__1lwlqs0__.input3D[1].input3Dz.set(2.22044604925e-16, keyable=True, channelBox=False, )
    plusMinusAverage6__1lwlqs0__.output3D.output3Dx.set(-1.0, keyable=False, channelBox=False, )
    plusMinusAverage6__1lwlqs0__.output3D.output3Dz.set(2.22044604925e-16, keyable=False, channelBox=False, )

    vectorProduct9__1lwlpgw__.operation.set(3, keyable=False, channelBox=False, )
    vectorProduct9__1lwlpgw__.input1.input1Z.set(1.0, keyable=True, channelBox=False, )

    vectorProduct10__1lwlq3k__.operation.set(3, keyable=False, channelBox=False, )
    vectorProduct10__1lwlq3k__.input1.input1Z.set(1.0, keyable=True, channelBox=False, )

    animCurveUU2__1lwlt8w__.tangentType.set(18, keyable=False, channelBox=False, )
    animCurveUU2__1lwlt8w__.weightedTangents.set(False, keyable=False, channelBox=False, )
    animCurveUU2__1lwlt8w__.keyTanInX[1].set(0.0, keyable=False, channelBox=False, )
    animCurveUU2__1lwlt8w__.keyTanInY[1].set(0.0, keyable=False, channelBox=False, )
    animCurveUU2__1lwlt8w__.keyTanOutX[1].set(1.0, keyable=False, channelBox=False, )
    animCurveUU2__1lwlt8w__.keyTanOutY[1].set(0.0, keyable=False, channelBox=False, )
    animCurveUU2__1lwlt8w__.keyTanInType[1].set(1, keyable=False, channelBox=False, )
    animCurveUU2__1lwlt8w__.keyTanOutType[1].set(1, keyable=False, channelBox=False, )
    pymel.setKeyframe(animCurveUU2__1lwlt8w__, value=1.0, float=-1.0)
    pymel.setKeyframe(animCurveUU2__1lwlt8w__, value=0.0, float=0.0)
    pymel.setKeyframe(animCurveUU2__1lwlt8w__, value=1.0, float=1.0)

    vectorProduct12__1lwlsmo__.input1.input1X.set(23.4965839386, keyable=True, channelBox=False, )
    vectorProduct12__1lwlsmo__.input1.input1Z.set(2.22044604925e-15, keyable=True, channelBox=False, )
    vectorProduct12__1lwlsmo__.input2.input2Y.set(1.0, keyable=True, channelBox=False, )
    vectorProduct12__1lwlsmo__.normalizeOutput.set(True, keyable=True, channelBox=False, )

    asdf_pivotPosition_orientConstraint2__4jgk5c__.nodeState.set(0, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.visibility.set(True, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.translate.translateX.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.translate.translateY.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.translate.translateZ.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.rotate.rotateX.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.rotate.rotateY.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.rotate.rotateZ.set(0.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.scale.scaleX.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.scale.scaleY.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.scale.scaleZ.set(1.0, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.enableRestPosition.set(True, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.target[0].targetRotate.targetRotateX.set(-8.71855165607e-15, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.target[0].targetRotate.targetRotateY.set(-4.92234270002e-15, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.target[0].targetRotate.targetRotateZ.set(-58.8966349154, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.restRotate.restRotateZ.set(6.95195208022, keyable=False, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.interpType.set(2, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.asdf_muscleInsertLocatorW0.set(0.0, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.asdf_muscleOriginLocatorW1.set(1.0, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.asdf_muscleInsertLocatorW0.set(0.0, keyable=True, channelBox=False, )
    asdf_pivotPosition_orientConstraint2__4jgk5c__.asdf_muscleOriginLocatorW1.set(1.0, keyable=True, channelBox=False, )

    animCurveUU3__1jkm34w__.tangentType.set(18, keyable=False, channelBox=False, )
    animCurveUU3__1jkm34w__.weightedTangents.set(False, keyable=False, channelBox=False, )
    animCurveUU3__1jkm34w__.keyTanInX[1].set(0.0, keyable=False, channelBox=False, )
    animCurveUU3__1jkm34w__.keyTanInY[1].set(0.0, keyable=False, channelBox=False, )
    animCurveUU3__1jkm34w__.keyTanOutX[1].set(1.0, keyable=False, channelBox=False, )
    animCurveUU3__1jkm34w__.keyTanOutY[1].set(0.0, keyable=False, channelBox=False, )
    animCurveUU3__1jkm34w__.keyTanInType[1].set(1, keyable=False, channelBox=False, )
    animCurveUU3__1jkm34w__.keyTanOutType[1].set(1, keyable=False, channelBox=False, )
    animCurveUU3__1jkm34w__.output.set(1.0, keyable=False, channelBox=False, )
    pymel.setKeyframe(animCurveUU3__1jkm34w__, value=0.0, float=-1.0)
    pymel.setKeyframe(animCurveUU3__1jkm34w__, value=1.0, float=0.0)
    pymel.setKeyframe(animCurveUU3__1jkm34w__, value=0.0, float=1.0)




    ## CONNECT ATTRS: ##
    vectorProduct6__1lt6b4g__.output >> plusMinusAverage5__1lt6chs__.input3D[0]
    vectorProduct7__1lt6btc__.output >> plusMinusAverage5__1lt6chs__.input3D[1]

    muscleOriginLocator.worldMatrix[0] >> vectorProduct7__1lt6btc__.matrix

    vectorProduct11__1lwlrbk__.output >> vectorProduct12__1lwlsmo__.input1

    muscleInsertLocator.worldMatrix[0] >> vectorProduct9__1lwlpgw__.matrix

    muscleInsertLocator.parentMatrix[0]                        >> asdf_pivotPosition_orientConstraint1__4jj5wo__.target[0].targetParentMatrix
    asdf_pivotPosition_orientConstraint1__4jj5wo__.asdf_muscleOriginLocatorW1 >> asdf_pivotPosition_orientConstraint1__4jj5wo__.target[1].targetWeight
    pivotIndicator.rotateOrder                                  >> asdf_pivotPosition_orientConstraint1__4jj5wo__.constraintRotateOrder
    muscleOriginLocator.rotate                                 >> asdf_pivotPosition_orientConstraint1__4jj5wo__.target[1].targetRotate
    pivotIndicator.parentInverseMatrix[0]                       >> asdf_pivotPosition_orientConstraint1__4jj5wo__.constraintParentInverseMatrix
    muscleOriginLocator.rotateOrder                            >> asdf_pivotPosition_orientConstraint1__4jj5wo__.target[1].targetRotateOrder
    muscleInsertLocator.rotate                                 >> asdf_pivotPosition_orientConstraint1__4jj5wo__.target[0].targetRotate
    asdf_pivotPosition_orientConstraint1__4jj5wo__.asdf_muscleInsertLocatorW0 >> asdf_pivotPosition_orientConstraint1__4jj5wo__.target[0].targetWeight
    muscleOriginLocator.parentMatrix[0]                        >> asdf_pivotPosition_orientConstraint1__4jj5wo__.target[1].targetParentMatrix
    muscleInsertLocator.rotateOrder                            >> asdf_pivotPosition_orientConstraint1__4jj5wo__.target[0].targetRotateOrder

    vectorProduct12__1lwlsmo__.output.outputX >> animCurveUU2__1lwlt8w__.input

    muscleOriginLocator.worldMatrix[0] >> vectorProduct10__1lwlq3k__.matrix

    vectorProduct11__1lwlrbk__.output.outputY >> condition1__1lwls00__.firstTerm

    condition1__1lwls00__.outColor.outColorR            >> asdf_pivotPosition_aimConstraint1__4jj4s0__.aimVector.aimVectorY
    plusMinusAverage6__1lwlqs0__.output3D               >> asdf_pivotPosition_aimConstraint1__4jj4s0__.worldUpVector
    pivotIndicator.rotatePivotTranslate   >> asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintRotateTranslate
    pivotIndicator.rotateOrder            >> asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintRotateOrder
    pivotIndicator.parentInverseMatrix[0] >> asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintParentInverseMatrix
    plusMinusAverage5__1lt6chs__.output3D               >> asdf_pivotPosition_aimConstraint1__4jj4s0__.target[0].targetTranslate
    pivotIndicator.translate              >> asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintTranslate
    pivotIndicator.rotatePivot            >> asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintRotatePivot

    vectorProduct12__1lwlsmo__.output.outputX >> animCurveUU3__1jkm34w__.input

    vectorProduct7__1lt6btc__.output                         >> vectorProduct11__1lwlrbk__.input1
    muscleInsertLocator.worldInverseMatrix[0] >> vectorProduct11__1lwlrbk__.matrix

    vectorProduct9__1lwlpgw__.output  >> plusMinusAverage6__1lwlqs0__.input3D[0]
    vectorProduct10__1lwlq3k__.output >> plusMinusAverage6__1lwlqs0__.input3D[1]

    pivotIndicator.rotateOrder                                  >> asdf_pivotPosition_orientConstraint2__4jgk5c__.constraintRotateOrder
    asdf_pivotPosition_orientConstraint1__4jj5wo__.constraintRotate           >> asdf_pivotPosition_orientConstraint2__4jgk5c__.target[1].targetRotate
    pivotIndicator.parentInverseMatrix[0]                       >> asdf_pivotPosition_orientConstraint2__4jgk5c__.constraintParentInverseMatrix
    animCurveUU2__1lwlt8w__.output                                            >> asdf_pivotPosition_orientConstraint2__4jgk5c__.asdf_muscleInsertLocatorW0
    asdf_pivotPosition_orientConstraint2__4jgk5c__.asdf_muscleInsertLocatorW0 >> asdf_pivotPosition_orientConstraint2__4jgk5c__.target[0].targetWeight
    pivotIndicator.parentMatrix[0]                              >> asdf_pivotPosition_orientConstraint2__4jgk5c__.target[1].targetParentMatrix
    asdf_pivotPosition_aimConstraint1__4jj4s0__.constraintRotate              >> asdf_pivotPosition_orientConstraint2__4jgk5c__.target[0].targetRotate
    animCurveUU3__1jkm34w__.output                                            >> asdf_pivotPosition_orientConstraint2__4jgk5c__.asdf_muscleOriginLocatorW1
    pivotIndicator.parentMatrix[0]                              >> asdf_pivotPosition_orientConstraint2__4jgk5c__.target[0].targetParentMatrix
    asdf_pivotPosition_orientConstraint2__4jgk5c__.asdf_muscleOriginLocatorW1 >> asdf_pivotPosition_orientConstraint2__4jgk5c__.target[1].targetWeight

    muscleInsertLocator.worldMatrix[0] >> vectorProduct6__1lt6b4g__.matrix

    asdf_pivotPosition_orientConstraint2__4jgk5c__.constraintRotate >> pivotIndicator.rotate

    colorAllMuscleJoints()
    return pivotIndicator

#def _createBendMuscle(name='', radius=1, numberOfInbetweenJoints=[3,3]):

    #if name:
        #name = name+'_'

    ## create pivotIndicatorZro control
    #pivotIndicatorZro = pymel.circle(sweep=180, radius=1, name=name+'pivotPosition_zro')[0]
    #pivotIndicatorZro.rotateZ.set(-90)
    #pymel.delete(pivotIndicatorZro, constructionHistory=True)
    #pymel.makeIdentity(pivotIndicatorZro, apply=True, rotate=True)
    #pymel.addAttr(pivotIndicatorZro, longName='rigType', dataType='string', keyable=True)
    #pivotIndicatorZro.rigType.set('muscleBendPivotPositionZro', lock=True)


    ## create pivotIndicatorOri
    #pivotIndicatorOri = pymel.group(world=True, empty=True, name=name+'pivotIndicatorOri')
    #pymel.addAttr(pivotIndicatorOri, longName='rigType', dataType='string', keyable=True)
    #pivotIndicatorOri.rigType.set('muscleBendPivotPositionOri', lock=True)
    #pymel.parent(pivotIndicatorOri, pivotIndicatorZro)
    #pivotIndicatorOri.translate.lock()
    #pivotIndicatorOri.scale.lock()

    ## create pivotIndicatorAimTarget control
    #pivotIndicatorAimTargetShape = pymel.createNode('locator')
    #pivotIndicatorAimTarget = pivotIndicatorAimTargetShape.getParent()
    #pivotIndicatorAimTarget.rename(name+'pivotIndicatorAimTarget')
    #pymel.addAttr(pivotIndicatorAimTarget, longName='rigType', dataType='string', keyable=True)
    #pivotIndicatorAimTarget.rigType.set('muscleBendPivotPositionOri', lock=True)
    #pymel.parent(pivotIndicatorAimTarget, pivotIndicatorOri)
    #pivotIndicatorAimTarget.translate.set(0,1,0)
    #pivotIndicatorAimTargetShape.localScale.set([0.2,0.5,0.2])
    #pivotIndicatorAimTargetShape.visibility.set(0)
    #pivotIndicatorAimTarget.translateZ.lock()

    ## create shape of pivotIndicator
    #pivotIndicator = pymel.circle(sweep=180, radius=1, name=name+'pivotPosition')[0]
    #pivotIndicator.rotateZ.set(-90)
    #pymel.makeIdentity(pivotIndicator, apply=True, rotate=True)
    #pivotIndicator.rotateY.set(-90)
    #pymel.makeIdentity(pivotIndicator, apply=True, rotate=True)
    #pymel.delete(pivotIndicator, constructionHistory=True)
    #pivotIndicator.translate.lock()

    #pivotIndicatorShapeC = pymel.circle(sweep=360, radius=1,)[0]
    #pivotIndicatorShapeC.rotateX.set(-90)
    #pymel.makeIdentity(pivotIndicatorShapeC, apply=True, rotate=True)
    #pymel.delete(pivotIndicatorShapeC, constructionHistory=True)
    #shapeParent(pivotIndicatorShapeC, pivotIndicator)

    #curveShape = pymel.curve( p=[(0.0, 0.0, 0.0), (0.0, 1.2, 0.0)], degree=1,)
    #shapeParent(curveShape, pivotIndicator)
    #pymel.parent(pivotIndicator, pivotIndicatorZro)

    #pivotIndicatorShapes = pymel.listRelatives(pivotIndicator, shapes=True)
    #for i, shape in enumerate(pivotIndicatorShapes):
        #if i == 0:
            #shape.rename(pivotIndicator.name()+'Shape')
        #else:
            #shape.rename(pivotIndicator.name()+'Shape'+str(i))

    #pivotIndicator.addAttr('pullWeight', defaultValue=0, keyable=True, minValue=0)
    #pivotIndicator.addAttr('radius', defaultValue=radius, keyable=True)
    #pymel.addAttr(pivotIndicator, longName='rigType', dataType='string', keyable=True)
    #pivotIndicator.rigType.set('muscleBendPivotPosition', lock=True)
    #pymel.addAttr(pivotIndicator, longName='baseName', dataType='string', keyable=True)
    #pivotIndicator.baseName.set('pivotPosition', lock=True)
    #pymel.addAttr(pivotIndicator, longName='origin', attributeType='message', keyable=True)
    #pymel.addAttr(pivotIndicator, longName='insertion', attributeType='message', keyable=True)

    #jointsGroup = pivotIndicator

    #pivotIndicatorOriCounterScale_multiplyDivide = pymel.createNode('multiplyDivide')
    #pivotIndicatorAimTarget.rename(name+'pivotIndicatorOriCounterScale_multiplyDivide')
    #pivotIndicatorOriCounterScale_multiplyDivide.input1.set(1.0, 1.0, 1.0,)

    #pivotIndicator.s >> pivotIndicatorOriCounterScale_multiplyDivide.input2
    #pivotIndicatorOriCounterScale_multiplyDivide.operation.set(2)



    ## create muscleOriginLocator
    #muscleOriginLocator = pymel.spaceLocator(name=name+'muscleOriginLocator')
    #muscleOriginLocatorShape = pymel.listRelatives(muscleOriginLocator, shapes=True)[0]
    #muscleOriginLocatorShape.localScale.set([0.2,0.5,0.2])
    #muscleOriginLocator.translateX.set(-2)
    #pymel.addAttr(muscleOriginLocator, longName='rigType', dataType='string', keyable=True)
    #muscleOriginLocator.rigType.set('muscleBendOrigin', lock=True)
    #muscleOriginLocator.message >> pivotIndicator.origin

    #muscleOriginLocatorShdw = pymel.group(name=name+'muscleOriginLocatorShdw', empty=True, world=True)
    #pymel.addAttr(muscleOriginLocatorShdw, longName='rigType', dataType='string', keyable=True)
    #muscleOriginLocatorShdw.rigType.set('muscleBendOriginShdw', lock=True)
    #pymel.parent(muscleOriginLocatorShdw, pivotIndicator)
    #pointConstraint = pymel.pointConstraint(muscleOriginLocator, muscleOriginLocatorShdw)
    #orientConstraint = pymel.orientConstraint(muscleOriginLocator, muscleOriginLocatorShdw,)


    ## create muscleInsertLocator
    #muscleInsertLocator = pymel.spaceLocator(name=name+'muscleInsertLocator')
    #muscleInsertLocatorShape = pymel.listRelatives(muscleInsertLocator, shapes=True)[0]
    #muscleInsertLocatorShape.localScale.set([0.2,0.5,0.2])
    #muscleInsertLocator.translateX.set(2)
    #pymel.addAttr(muscleInsertLocator, longName='rigType', dataType='string', keyable=True)
    #muscleInsertLocator.rigType.set('muscleBendInsertion', lock=True)
    #muscleInsertLocator.message >> pivotIndicator.insertion

    #muscleInsertLocatorShdw = pymel.group(name=name+'muscleInsertLocatorShdw', empty=True, world=True)
    #pymel.addAttr(muscleInsertLocatorShdw, longName='rigType', dataType='string', keyable=True)
    #muscleInsertLocatorShdw.rigType.set('muscleInsertLocatorShdw', lock=True)
    #pymel.parent(muscleInsertLocatorShdw, pivotIndicator)
    #pointConstraint = pymel.pointConstraint(muscleInsertLocator, muscleInsertLocatorShdw)
    #orientConstraint = pymel.orientConstraint(muscleInsertLocator, muscleInsertLocatorShdw,)


    ## constrain pivotIndicatorAimTarget between origin and insertion locators
    #pointConstraint = pymel.pointConstraint(muscleOriginLocator, muscleInsertLocator, pivotIndicatorAimTarget, skip=['z',])
    #pivotIndicatorAimTargetPointConstraint = pointConstraint
    #yInput = pivotIndicatorAimTarget.translateY.inputs()[0]
    #condition = pymel.createNode('condition')
    #pointConstraint.constraintTranslateY >> condition.firstTerm
    #pointConstraint.constraintTranslateY >> condition.colorIfTrueR
    #condition.outColorR >> pivotIndicatorAimTarget.translateY
    #condition.secondTerm.set(1)
    #condition.colorIfFalseR.set(1)
    #condition.operation.set(2)

    #orientConstraint = pymel.orientConstraint(muscleOriginLocator, muscleInsertLocator, pivotIndicatorOri)
    #orientConstraint = globalizeConstraint(orientConstraint)
    #orientConstraint.interpType.set(2)
    #aimConstraint = pymel.aimConstraint(pivotIndicatorAimTarget, pivotIndicator, worldUpType='objectrotation', worldUpObject=pivotIndicatorOri, aimVector=[0,1,0], worldUpVector=[0,0,1], upVector=[0,0,1])


    ## create mid point locators
    #muscleMidPointLocator = pymel.spaceLocator(name=name+'muscleMidPointLocator')
    #muscleMidPointLocatorShape = pymel.listRelatives(muscleMidPointLocator, shapes=True)[0]
    #muscleMidPointLocatorShape.localScale.set([0.2,0.2,0.2])
    #pymel.parent(muscleMidPointLocator, pivotIndicator)
    #pymel.addAttr(muscleMidPointLocator, longName='rigType', dataType='string', keyable=True)
    #muscleMidPointLocator.rigType.set('muscleMidPointLocator', lock=True)
    #muscleMidPointLocator_blendPosition = pymel.createNode('blendColors', name=name+'muscleMidPointLocator_blendPosition')
    #muscleMidPointLocator_blendPosition.blender.set(0.5)
    #muscleOriginLocatorShdw.translateY >> muscleMidPointLocator_blendPosition.color1G
    #muscleInsertLocatorShdw.translateY >> muscleMidPointLocator_blendPosition.color2G
    #muscleMidPointLocator.visibility.set(0)

    #blendColor = pymel.createNode('blendColors', name=name+'muscleMidPointLocator')
    #pivotIndicator.pullWeight >> blendColor.blender
    #muscleMidPointLocator_blendPosition.outputG >> blendColor.color2G
    #blendColor.color1.set(0,1,0)
    #blendColor.outputG >> muscleMidPointLocator.translateY


    #muscleMidPointLocatorB = pymel.spaceLocator(name=name+'muscleMidPointLocatorB')
    #muscleMidPointLocatorBShape = pymel.listRelatives(muscleMidPointLocatorB, shapes=True)[0]
    #muscleMidPointLocatorBShape.localScale.set([0.2,0.2,0.2])
    #pymel.parent(muscleMidPointLocatorB, pivotIndicator)
    #pymel.addAttr(muscleMidPointLocatorB, longName='rigType', dataType='string', keyable=True)
    #muscleMidPointLocatorB.rigType.set('muscleMidPointLocatorB', lock=True)
    #muscleMidPointLocatorB.visibility.set(0)

    #muscleMidPointLocatorC = pymel.spaceLocator(name=name+'muscleMidPointLocatorC')
    #muscleMidPointLocatorCShape = pymel.listRelatives(muscleMidPointLocatorC, shapes=True)[0]
    #muscleMidPointLocatorCShape.localScale.set([0.2,0.2,0.2])
    #pymel.parent(muscleMidPointLocatorC, pivotIndicator)
    #pymel.addAttr(muscleMidPointLocatorC, longName='rigType', dataType='string', keyable=True)
    #muscleMidPointLocatorC.rigType.set('muscleMidPointLocatorC', lock=True)
    #muscleMidPointLocatorC.visibility.set(0)
    #condition = pymel.createNode('condition', name=name+'midPointCollide_condition')
    #muscleMidPointLocator.translateY >> condition.firstTerm
    #condition.secondTerm.set(1)
    #condition.operation.set(2)
    #muscleMidPointLocator.translateY >> condition.colorIfTrueG
    #condition.colorIfFalseR.set(0)
    #condition.colorIfFalseB.set(0)
    #condition.outColor >> muscleMidPointLocatorB.translate




    #vectorProductA = pymel.createNode('vectorProduct', name=name+'vectorProductA')

    #vectorProductB = pymel.createNode('vectorProduct', name=name+'vectorProductB')
    #muscleMidPointLocatorC.translate >> vectorProductB.input1
    #muscleMidPointLocatorC.translate >> vectorProductB.input2

    #vectorProductC = pymel.createNode('vectorProduct', name=name+'vectorProductC')
    #muscleMidPointLocatorC.translate >> vectorProductC.input1
    #vectorProductC.normalizeOutput.set(1)
    #vectorProductC.operation.set(3)



    #joints = []

    #muscleOriginJoint = pymel.createNode('joint', name=name+'muscleOriginJoint')
    #muscleOriginJoint.radius.set(0.2)
    #muscleOriginLocatorShdw.translate >> muscleOriginJoint.translate
    #pymel.parent(muscleOriginJoint, jointsGroup)
    #pymel.addAttr(muscleOriginJoint, longName='rigType', dataType='string', keyable=True)
    #muscleOriginJoint.rigType.set('muscleBendJoint', lock=True)
    #pymel.addAttr(muscleOriginJoint, longName='indexNum', dataType='string', keyable=True)
    #muscleOriginJoint.indexNum.set(str(0), lock=True)

    #muscleMidPointJoint = pymel.createNode('joint', name=name+'muscleMidPointJoint')
    #muscleMidPointJoint.radius.set(0.2)
    #muscleMidPointJoint.addAttr('constraintPercent', defaultValue=0.5, keyable=True, maxValue=1, minValue=0)
    #pymel.parent(muscleMidPointJoint, jointsGroup)
    #pymel.addAttr(muscleMidPointJoint, longName='rigType', dataType='string', keyable=True)
    #muscleMidPointJoint.rigType.set('muscleBendJoint', lock=True)
    #pymel.addAttr(muscleMidPointJoint, longName='baseName', dataType='string', keyable=True)
    #muscleMidPointJoint.baseName.set('muscleMidPointJoint', lock=True)

    ##hook up the percent blend of the mid joint to the point constraint of the pivotIndicatorAimTarget
    #plusMinusAverage = pymel.createNode('plusMinusAverage')
    #plusMinusAverage.input1D[0].set(1)
    #plusMinusAverage.operation.set(2)
    #muscleMidPointJoint.constraintPercent >> plusMinusAverage.input1D[1]
    #muscleMidPointJoint.constraintPercent >> pivotIndicatorAimTargetPointConstraint.w0
    #plusMinusAverage.output1D >> pivotIndicatorAimTargetPointConstraint.w1
    #muscleMidPointJoint.constraintPercent >> muscleMidPointLocator_blendPosition.blender
    #pivotIndicatorOriCounterScale_multiplyDivide.output >> muscleMidPointJoint.s

    #muscleInsertJoint = pymel.createNode('joint', name=name+'muscleInsertJoint')
    #muscleInsertJoint.radius.set(0.2)
    #muscleInsertLocatorShdw.translate >> muscleInsertJoint.translate
    #pymel.parent(muscleInsertJoint, jointsGroup)
    #pymel.addAttr(muscleInsertJoint, longName='rigType', dataType='string', keyable=True)
    #muscleInsertJoint.rigType.set('muscleBendJoint', lock=True)
    #pymel.addAttr(muscleInsertJoint, longName='indexNum', dataType='string', keyable=True)
    #muscleInsertJoint.indexNum.set(str(numberOfInbetweenJoints[0]+numberOfInbetweenJoints[1]+2), lock=True)

    #conditionB = pymel.createNode('condition', name=name+'midPointCollide_conditionB')
    #vectorProductB.outputX >> conditionB.firstTerm
    #conditionB.secondTerm.set(1)
    #conditionB.operation.set(2)
    #muscleMidPointLocatorC.translate >> conditionB.colorIfTrue
    #vectorProductC.output >> conditionB.colorIfFalse
    #conditionB.outColor >> muscleMidPointJoint.translate


    #total = numberOfInbetweenJoints[0]+2
    #muscleInbetweenLocatorsA = []
    #muscleInbetweenJointsA = []
    #for i in range(numberOfInbetweenJoints[0]):
        #muscleInbetweenLocator = pymel.spaceLocator(name=name+'muscleOriginInbetweenLocator'+str(i))
        #muscleInbetweenLocatorShape = pymel.listRelatives(muscleInbetweenLocator, shapes=True)[0]
        #muscleInbetweenLocatorShape.localScale.set([0.2,0.2,0.2])
        #pymel.addAttr(muscleInbetweenLocator, longName='rigType', dataType='string', keyable=True)
        #muscleInbetweenLocator.rigType.set('muscleOriginInbetweenLocator', lock=True)
        #pymel.parent(muscleInbetweenLocator, pivotIndicator)
        #muscleInbetweenLocatorShape.visibility.set(0)

        #if not muscleInbetweenLocatorsA:
            #muscleInbetweenJoint_blendPosition = pymel.createNode('blendColors', name=name+'muscleInbetweenJoint_blendPosition'+str(i))
            #muscleOriginLocatorShdw.translate >> muscleInbetweenJoint_blendPosition.color1
            #muscleMidPointLocatorB.translate >> muscleInbetweenJoint_blendPosition.color2


            #muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleOriginLocatorShdw, muscleMidPointLocatorB, muscleInbetweenLocator)
            #muscleInbetweenLocatorOrientConstraint.interpType.set(2)
        #else:
            #muscleInbetweenJoint_blendPosition = pymel.createNode('blendColors', name=name+'muscleInbetweenJoint_blendPosition'+str(i))
            #muscleOriginLocatorShdw.translate >> muscleInbetweenJoint_blendPosition.color1
            #muscleInbetweenJointsA[-1].translate >> muscleInbetweenJoint_blendPosition.color2

            #muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleOriginLocatorShdw, muscleInbetweenLocatorsA[-1], muscleInbetweenLocator)
            #muscleInbetweenLocatorOrientConstraint.interpType.set(2)

        #muscleInbetweenJoint_blendPosition.output >> muscleInbetweenLocator.translate
        #muscleInbetweenLocatorOrientConstraint = ka_constraints.localizeConstraint(muscleInbetweenLocatorOrientConstraint)
        #muscleInbetweenLocatorOrientConstraint.interpType.set(2)

        #muscleInbetweenLocatorOrientConstraint.target[0].targetWeight.set(1)
        #muscleInbetweenLocatorOrientConstraint.target[0].targetWeight.set(total-2)

        #muscleInbetweenLocatorsA.append(muscleInbetweenLocator)


        #muscleInbetweenJoint = pymel.createNode('joint', name=name+'muscleOriginInbetweenJoint'+str(i))
        #pymel.parent(muscleInbetweenJoint, jointsGroup)
        #muscleInbetweenJoint.radius.set(0.2)
        #muscleInbetweenJoint.addAttr('constraintPercent', defaultValue=1.0/(total-1.0), keyable=True, maxValue=1, minValue=0)
        #muscleInbetweenJointsA.append(muscleInbetweenJoint)
        #pymel.addAttr(muscleInbetweenJoint, longName='rigType', dataType='string', keyable=True)
        #muscleInbetweenJoint.rigType.set('muscleBendJoint', lock=True)
        #pymel.addAttr(muscleInbetweenJoint, longName='baseName', dataType='string', keyable=True)
        #muscleInbetweenJoint.baseName.set('muscleOriginInbetweenJoint'+str(i), lock=True)


        #plusMinusAverage = pymel.createNode('plusMinusAverage', name=name+'muscleOriginInbetweenJoint'+str(i)+'_plusMinusAverage')
        #plusMinusAverage.input1D[0].set(1)
        #plusMinusAverage.operation.set(2)
        #muscleInbetweenJoint.constraintPercent >> plusMinusAverage.input1D[1]

        #muscleInbetweenJoint.constraintPercent >> muscleInbetweenJoint_blendPosition.blender

        #muscleInbetweenJoint.constraintPercent >> muscleInbetweenLocatorOrientConstraint.target[0].targetWeight
        #plusMinusAverage.output1D >> muscleInbetweenLocatorOrientConstraint.target[1].targetWeight

        #muscleOriginInbetweenJoint_vectorProductA = pymel.createNode('vectorProduct', name=name+'muscleOriginInbetweenJoint'+str(i)+'_vectorProductA')
        #muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input1
        #muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input2

        #muscleOriginInbetweenJoint_vectorProductB = pymel.createNode('vectorProduct', name=name+'muscleOriginInbetweenJoint'+str(i)+'_vectorProductB')
        #muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input1
        #muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input2
        #muscleOriginInbetweenJoint_vectorProductB.normalizeOutput.set(1)
        #muscleOriginInbetweenJoint_vectorProductB.operation.set(3)

        #condition = pymel.createNode('condition', name=name+'muscleOriginInbetweenJoint'+str(i)+'_condition')
        #muscleOriginInbetweenJoint_vectorProductA.outputX >> condition.firstTerm
        #condition.operation.set(2)
        #condition.secondTerm.set(1)
        #muscleInbetweenLocator.translate >> condition.colorIfTrue
        #muscleOriginInbetweenJoint_vectorProductB.output >> condition.colorIfFalse
        #condition.outColor >> muscleInbetweenJoint.translate
        #pivotIndicatorOriCounterScale_multiplyDivide.output >> muscleInbetweenJoint.s
        #total -= 1


    #muscleUpVector_vectorProductC = pymel.createNode('vectorProduct', name=name+'muscleUpVector_vectorProductC')
    #muscleUpVector_vectorProductC.operation.set(1)
    #muscleUpVector_vectorProductC.normalizeOutput.set(1)
    #muscleOriginLocatorShdw.translate >> muscleUpVector_vectorProductC.input1
    #muscleUpVector_vectorProductC.input2.set(0,0,1)

    #muscleUpVector_animCurveUU = pymel.createNode('animCurveUU', name=name+'muscleUpVector_plusMinusAverage')
    #muscleUpVector_vectorProductC.outputX >> muscleUpVector_animCurveUU.input
    #pymel.setKeyframe(muscleUpVector_animCurveUU, float=1, value=0, inTangentType='linear', outTangentType='linear',)
    #pymel.setKeyframe(muscleUpVector_animCurveUU, float=0, value=1, inTangentType='linear', outTangentType='linear',)
    #pymel.setKeyframe(muscleUpVector_animCurveUU, float=-1, value=0, inTangentType='linear', outTangentType='linear',)

    #aimConstraint = pymel.aimConstraint(muscleInbetweenJointsA[-1], muscleOriginJoint, worldUpType='objectrotation', worldUpObject=muscleOriginLocatorShdw, aimVector=[1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])
    #aimConstraint = ka_constraints.localizeConstraint(aimConstraint)
    #muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
    #muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
    #muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
    #muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ
    #for i, joint in enumerate(muscleInbetweenJointsA):
        #if joint == muscleInbetweenJointsA[0]:
            #aimConstraint = pymel.aimConstraint(muscleMidPointLocatorB, joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsA[i], aimVector=[1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])
        #else:
            #aimConstraint = pymel.aimConstraint(muscleInbetweenJointsA[i-1], joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsA[i], aimVector=[1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])

        #aimConstraint = ka_constraints.localizeConstraint(aimConstraint)
        #muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
        #muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
        #muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
        #muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ


    #total = numberOfInbetweenJoints[1]+2
    #muscleInbetweenLocatorsB = []
    #muscleInbetweenJointsB = []
    #for i in range(numberOfInbetweenJoints[1]):
        #muscleInbetweenLocator = pymel.spaceLocator(name=name+'muscleInsertionInbetweenLocator'+str(i))
        #muscleInbetweenLocatorShape = pymel.listRelatives(muscleInbetweenLocator, shapes=True)[0]
        #muscleInbetweenLocatorShape.localScale.set([0.2,0.2,0.2])
        #pymel.addAttr(muscleInbetweenLocator, longName='rigType', dataType='string', keyable=True)
        #muscleInbetweenLocator.rigType.set('muscleInsertionInbetweenLocator', lock=True)
        #pymel.parent(muscleInbetweenLocator, pivotIndicator)
        #muscleInbetweenLocatorShape.visibility.set(0)

        #if not muscleInbetweenLocatorsB:
            #muscleInbetweenJoint_blendPosition = pymel.createNode('blendColors', name=name+'muscleInbetweenJoint_blendPosition'+str(i))
            #muscleInsertLocatorShdw.translate >> muscleInbetweenJoint_blendPosition.color1
            #muscleMidPointLocatorB.translate >> muscleInbetweenJoint_blendPosition.color2

            #muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleInsertLocatorShdw, muscleMidPointLocatorB, muscleInbetweenLocator)
            #muscleInbetweenLocatorOrientConstraint.interpType.set(2)
        #else:
            #muscleInbetweenJoint_blendPosition = pymel.createNode('blendColors', name=name+'muscleInbetweenJoint_blendPosition'+str(i))
            #muscleInsertLocatorShdw.translate >> muscleInbetweenJoint_blendPosition.color1
            #muscleInbetweenJointsB[-1].translate >> muscleInbetweenJoint_blendPosition.color2

            #muscleInbetweenLocatorOrientConstraint = pymel.orientConstraint(muscleInsertLocatorShdw, muscleInbetweenLocatorsB[-1], muscleInbetweenLocator)
            #muscleInbetweenLocatorOrientConstraint.interpType.set(2)

        #muscleInbetweenJoint_blendPosition.output >> muscleInbetweenLocator.translate
        #muscleInbetweenLocatorOrientConstraint = ka_constraints.localizeConstraint(muscleInbetweenLocatorOrientConstraint)
        #muscleInbetweenLocatorOrientConstraint.interpType.set(2)

        #muscleInbetweenJoint = pymel.createNode('joint', name=name+'muscleInsertionInbetweenJoint'+str(i))
        #pymel.parent(muscleInbetweenJoint, jointsGroup)
        #muscleInbetweenJoint.radius.set(0.2)
        #muscleInbetweenJoint.addAttr('constraintPercent', defaultValue=1.0/(total-1.0), keyable=True, maxValue=1, minValue=0)
        #muscleInbetweenJointsB.append(muscleInbetweenJoint)
        #pymel.addAttr(muscleInbetweenJoint, longName='rigType', dataType='string', keyable=True)
        #muscleInbetweenJoint.rigType.set('muscleBendJoint', lock=True)
        #pymel.addAttr(muscleInbetweenJoint, longName='baseName', dataType='string', keyable=True)
        #muscleInbetweenJoint.baseName.set('muscleInsertionInbetweenJoint'+str(i), lock=True)
        #muscleInbetweenLocatorsB.append(muscleInbetweenLocator)
        #pymel.addAttr(muscleInbetweenJoint, longName='indexNum', dataType='string', keyable=True)
        #muscleInbetweenJoint.indexNum.set(str(numberOfInbetweenJoints[0]+i+2), lock=True)

        #plusMinusAverage = pymel.createNode('plusMinusAverage', name=name+'muscleInsertionInbetweenJoint'+str(i)+'_plusMinusAverage')
        #plusMinusAverage.input1D[0].set(1)
        #plusMinusAverage.operation.set(2)
        #muscleInbetweenJoint.constraintPercent >> plusMinusAverage.input1D[1]

        #muscleInbetweenJoint.constraintPercent >> muscleInbetweenJoint_blendPosition.blender

        #muscleInbetweenJoint.constraintPercent >> muscleInbetweenLocatorOrientConstraint.target[0].targetWeight
        #plusMinusAverage.output1D >> muscleInbetweenLocatorOrientConstraint.target[1].targetWeight

        #muscleOriginInbetweenJoint_vectorProductA = pymel.createNode('vectorProduct', name=name+'muscleInsertionInbetweenJoint'+str(i)+'_vectorProductA')
        #muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input1
        #muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductA.input2

        #muscleOriginInbetweenJoint_vectorProductB = pymel.createNode('vectorProduct', name=name+'muscleInsertionInbetweenJoint'+str(i)+'_vectorProductB')
        #muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input1
        #muscleInbetweenLocator.translate >> muscleOriginInbetweenJoint_vectorProductB.input2
        #muscleOriginInbetweenJoint_vectorProductB.normalizeOutput.set(1)
        #muscleOriginInbetweenJoint_vectorProductB.operation.set(3)

        #condition = pymel.createNode('condition', name=name+'muscleInsertionInbetweenJoint'+str(i)+'_condition')
        #muscleOriginInbetweenJoint_vectorProductA.outputX >> condition.firstTerm
        #condition.secondTerm.set(1)
        #condition.operation.set(2)
        #muscleInbetweenLocator.translate >> condition.colorIfTrue
        #muscleOriginInbetweenJoint_vectorProductB.output >> condition.colorIfFalse
        #condition.outColor >> muscleInbetweenJoint.translate
        #pivotIndicatorOriCounterScale_multiplyDivide.output >> muscleInbetweenJoint.s

        #total -= 1


    #muscleUpVector_vectorProductC = pymel.createNode('vectorProduct', name=name+'muscleUpVector_vectorProductC')
    #muscleUpVector_vectorProductC.operation.set(1)
    #muscleUpVector_vectorProductC.normalizeOutput.set(1)
    #muscleInsertLocatorShdw.translate >> muscleUpVector_vectorProductC.input1
    #muscleUpVector_vectorProductC.input2.set(0,0,1)

    #muscleUpVector_animCurveUU = pymel.createNode('animCurveUU', name=name+'muscleUpVector_plusMinusAverage')
    #muscleUpVector_vectorProductC.outputX >> muscleUpVector_animCurveUU.input
    #pymel.setKeyframe(muscleUpVector_animCurveUU, float=1, value=0, inTangentType='linear', outTangentType='linear',)
    #pymel.setKeyframe(muscleUpVector_animCurveUU, float=0, value=1, inTangentType='linear', outTangentType='linear',)
    #pymel.setKeyframe(muscleUpVector_animCurveUU, float=-1, value=0, inTangentType='linear', outTangentType='linear',)


    #aimConstraint = pymel.aimConstraint(muscleInbetweenJointsB[-1], muscleInsertJoint, worldUpType='objectrotation', worldUpObject=muscleInsertLocatorShdw, aimVector=[-1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])
    #aimConstraint = ka_constraints.localizeConstraint(aimConstraint)
    #muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
    #muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
    #muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
    #muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ
    #for i, joint in enumerate(muscleInbetweenJointsB):
        #if joint == muscleInbetweenJointsB[0]:
            #aimConstraint = pymel.aimConstraint(muscleMidPointLocatorB, joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsB[i], aimVector=[-1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])
        #else:
            #aimConstraint = pymel.aimConstraint(muscleInbetweenJointsB[i-1], joint, worldUpType='objectrotation', worldUpObject=muscleInbetweenLocatorsB[i], aimVector=[-1,0,0], worldUpVector=[0,0,1], upVector=[0,0,1])

        #aimConstraint = ka_constraints.localizeConstraint(aimConstraint)
        #muscleUpVector_vectorProductC.outputX >> aimConstraint.worldUpVectorY
        #muscleUpVector_vectorProductC.outputX >> aimConstraint.upVectorY
        #muscleUpVector_animCurveUU.output >> aimConstraint.worldUpVectorZ
        #muscleUpVector_animCurveUU.output >> aimConstraint.upVectorZ

    #muscleMidPointLocatorC_averagePosition = pymel.createNode('plusMinusAverage', name=name+'muscleMidPointLocatorC_averagePosition')
    #muscleMidPointLocatorC_averagePosition.operation.set(3)
    #muscleInbetweenJointsB[0].translate >> muscleMidPointLocatorC_averagePosition.input3D[0]
    #muscleInbetweenJointsA[0].translate >> muscleMidPointLocatorC_averagePosition.input3D[1]
    #muscleMidPointLocatorB.translate >> muscleMidPointLocatorC_averagePosition.input3D[2]
    #muscleMidPointLocatorC_averagePosition.output3D >> muscleMidPointLocatorC.translate

    #muscleMidPointJointC_orientConstraint = pymel.orientConstraint(muscleInbetweenJointsB[0], muscleInbetweenJointsA[0], muscleMidPointJoint)
    #muscleMidPointJointC_orientConstraint = ka_constraints.localizeConstraint(muscleMidPointJointC_orientConstraint)
    #muscleMidPointJointC_orientConstraint.interpType.set(2)

    #pivotIndicator.radius >> pivotIndicatorZro.scaleX
    #pivotIndicator.radius >> pivotIndicatorZro.scaleY
    #pivotIndicator.radius >> pivotIndicatorZro.scaleZ

    #colorAllMuscleJoints()
    #return pivotIndicator

def muscleJoint():
    text=None
    result = cmds.promptDialog(
                    title='Name Muscle',
                    message='Enter a Base Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)

        if text:
            _muscleJoint(name=text)
        else:
            _muscleJoint

def printCommand_procedurallyCreateMuscleJoint():
    allMuscleJoints = getAllMuscleJoints()
    print('## Create Piston Joints\n')

    for muscleJoint in allMuscleJoints:
        baseName = muscleJoint.nodeName()
        baseName = baseName.replace('_muscleJoint', '', 1)

        initialLength = str(muscleJoint.initialLength.get())
        radius = str(muscleJoint.radius.get())
        if pymel.attributeQuery('squashAndStretchStrength', node=muscleJoint, exists=True):
            squashAndStretchStrength = str(muscleJoint.squashAndStretchStrength.get())
        else: #attribute has been spelt wrong initially by kris (me)
            squashAndStretchStrength = str(muscleJoint.squashAndStrechStrength.get())

        insertionNull = muscleJoint.insertion.inputs()[0]
        originNull = muscleJoint.origin.inputs()[0]

        insertionParent = str(insertionNull.getParent())
        originParent = str(originNull.getParent())

        insertionMatrix = str( pymel.xform(insertionNull, query=True, ws=True, m=True) )
        originMatrix = str( pymel.xform(originNull, query=True, ws=True, m=True) )

        print('userMethods.procedurallyCreateMuscleJoint("'+baseName+'", '+initialLength+', '+radius+', '+squashAndStretchStrength+', "'+insertionParent+'", "'+originParent+'", '+insertionMatrix+', '+originMatrix+')')

    print('\n\n## Create Constraints inputs')
    constraints = []
    for muscleJoint in allMuscleJoints:
        insertionNull = muscleJoint.insertion.inputs()[0]
        originNull = muscleJoint.origin.inputs()[0]

	# get a dict on unique inputs
	inputDict = {}

	inputs = muscleJoint.inputs()
	inputs.extend(insertionNull.inputs())
	inputs.extend(originNull.inputs())
	for inputNode in inputs:
	    if inputNode not in inputDict:
		inputDict[inputNode] = inputNode

	# if they are constraints, generate the recreate commands
	for inputNode in inputDict:
	    if 'Constraint' in inputNode.nodeType():
		constraints.append(inputNode)

    attrCommands.eccoAttrsPymelObjectOriented(nodes=constraints, skipExternalConnections=False)


def procedurallyCreateMuscleJoint(baseName, initialLength, radius, squashAndStretchStrength, insertionParent, originParent, insertionMatrix, originMatrix):

    muscleJoint = _muscleJoint(name=baseName, initialLength=initialLength, radius=radius, squashAndStretchStrength=squashAndStretchStrength)
    insertionNull = muscleJoint.insertion.inputs()[0]
    originNull = muscleJoint.origin.inputs()[0]

    pymel.parent(originNull, originParent)
    pymel.parent(insertionNull, insertionParent)

    pymel.xform(originNull, ws=True, m=originMatrix)
    pymel.xform(insertionNull, ws=True, m=insertionMatrix)


def _muscleJoint(name='', initialLength=1.5, radius=0.4, squashAndStretchStrength=0):

    if name:
        name = name+'_'
    rootLocatorShape = pymel.createNode('locator',)
    rootLocator = pymel.listRelatives(rootLocatorShape, parent=True)[0]
    pymel.rename(rootLocator, name+'muscleOrigin')
    pymel.addAttr(rootLocator, longName='rigType', dataType='string', keyable=True)
    rootLocator.rigType.set('muscleOrigin')

    rootLocator.translateX.set(1)
    rootLocator.localScaleX.set(0.3)
    rootLocator.localScaleY.set(0.5)
    rootLocator.localScaleZ.set(0.3)

    endLocatorShape = pymel.createNode('locator',)
    endLocator = pymel.listRelatives(endLocatorShape, parent=True)[0]
    pymel.rename(endLocator, name+'muscleInsertion')
    pymel.addAttr(endLocator, longName='rigType', dataType='string', keyable=True)
    endLocator.rigType.set('muscleInsertion')

    endLocator.translateX.set(3)
    endLocator.localScaleX.set(0.3)
    endLocator.localScaleY.set(0.5)
    endLocator.localScaleZ.set(0.3)

    midPositionGroup = pymel.group( empty=True, name=name+'muscleMidPoint')
    pymel.parent(midPositionGroup, rootLocator)
    pymel.pointConstraint(rootLocator, endLocator, midPositionGroup)

    muscleJoint = pymel.joint(name=name+'muscleJoint', position=(2, 0, 0))
    pymel.addAttr(muscleJoint, longName='currentLength', defaultValue=initialLength, minValue=0.001, keyable=True)
    pymel.addAttr(muscleJoint, longName='initialLength', defaultValue=initialLength, minValue=0.001, keyable=True)
    pymel.addAttr(muscleJoint, longName='squashAndStretchStrength', defaultValue=squashAndStretchStrength, minValue=0., keyable=True)
    pymel.addAttr(muscleJoint, longName='rigType', dataType='string', keyable=True)
    pymel.addAttr(muscleJoint, longName='origin', attributeType='message', keyable=True)
    pymel.addAttr(muscleJoint, longName='insertion', attributeType='message', keyable=True)
    muscleJoint.rigType.set('muscleJoint')
    muscleJoint.rigType.lock()
    rootLocator.message >> muscleJoint.origin
    endLocator.message >> muscleJoint.insertion
    muscleJoint.radius.set(radius)
    muscleJoint.translateX.set(0)

    pymel.select(clear=True)

    muscleEnd = pymel.joint(name=name+'muscleInsertionJoint', position=(3, 0, 0))
    pymel.parent(muscleEnd, muscleJoint)
    muscleEnd.radius.set(radius*0.75)
    pymel.select(clear=True)
    pymel.addAttr(muscleEnd, longName='rigType', dataType='string', keyable=True)
    muscleEnd.rigType.set('muscleInsertionJoint')
    muscleEnd.rigType.lock()

    muscleStart = pymel.joint(name=name+'muscleOriginJoint', position=(1, 0, 0))
    pymel.parent(muscleStart, muscleJoint)
    muscleStart.radius.set(radius*0.75)
    pymel.select(clear=True)
    pymel.addAttr(muscleStart, longName='rigType', dataType='string', keyable=True)
    muscleStart.rigType.set('muscleOriginJoint')
    muscleEnd.rigType.lock()

    pymel.pointConstraint(rootLocator, endLocator, midPositionGroup)
    pymel.pointConstraint(rootLocator, muscleStart)
    pymel.pointConstraint(endLocator, muscleEnd)
    pymel.aimConstraint(rootLocator, midPositionGroup, worldUpObject=endLocator, worldUpType='objectrotation', aimVector=[-1,0,0], upVector=[0,0,1], worldUpVector=[0,0,1])

    worldSpaceToLocalSpace_vectorProduct2 = pymel.createNode('vectorProduct', name=name+'worldSpaceToLocalSpace')
    worldSpaceToLocalSpace_vectorProduct2.operation.set(4)
    endLocatorShape.worldPosition >> worldSpaceToLocalSpace_vectorProduct2.input1
    midPositionGroup.worldInverseMatrix >> worldSpaceToLocalSpace_vectorProduct2.matrix

    scale_multiplyDivide = pymel.createNode('multiplyDivide', name=name+'scale_multiplyDivide')
    scale_multiplyDivide.operation.set(2)

    worldSpaceToLocalSpace_vectorProduct2.outputX >> scale_multiplyDivide.input1X
    worldSpaceToLocalSpace_vectorProduct2.outputX >> scale_multiplyDivide.input2Y
    muscleJoint.initialLength >> scale_multiplyDivide.input2X
    muscleJoint.initialLength >> scale_multiplyDivide.input1Y

    scaleFactor_blendColor = pymel.createNode('blendColors', name=name+'scale_blendColors')
    scaleFactor_blendColor.color2.set(1,1,1)

    scale_multiplyDivide.output >> scaleFactor_blendColor.color1

    muscleJoint.squashAndStretchStrength >> scaleFactor_blendColor.blender

    scaleFactor_blendColor.outputR >> muscleJoint.scaleX
    scaleFactor_blendColor.outputG >> muscleJoint.scaleY
    scaleFactor_blendColor.outputG >> muscleJoint.scaleZ

    currentlength_multiplyDivide = pymel.createNode('multiplyDivide')
    currentlength_multiplyDivide.rename(name+'scale_multiplyDivide')
    currentlength_multiplyDivideB = pymel.createNode('multiplyDivide')
    currentlength_multiplyDivideB.rename(name+'scale_multiplyDivideB')

    muscleEnd.tx >> currentlength_multiplyDivide.input1X
    currentlength_multiplyDivide.input2X.set(2)
    currentlength_multiplyDivide.outputX >> currentlength_multiplyDivideB.input1X
    scale_multiplyDivide.outputX >> currentlength_multiplyDivideB.input2X
    currentlength_multiplyDivide.outputX >> muscleJoint.currentLength

    twist_multiplyDivide = pymel.createNode('multiplyDivide')
    twist_multiplyDivide.rename(name+'scale_multiplyDivide')
    midPositionGroup.rx >> twist_multiplyDivide.input1X
    midPositionGroup.rx >> twist_multiplyDivide.input1Y
    midPositionGroup.rx >> twist_multiplyDivide.input1Z
    twist_multiplyDivide.input2X.set(-0.5)
    twist_multiplyDivide.input2Y.set(-0.5)
    twist_multiplyDivide.input2Z.set(0.5)
    twist_multiplyDivide.outputX >> muscleStart.rx
    twist_multiplyDivide.outputY >> muscleJoint.rx
    twist_multiplyDivide.outputZ >> muscleEnd.rx

    pymel.select(rootLocator)

    colorAllMuscleJoints()

    return muscleJoint

def getRelatedMuscleJoint(input):
    muscleJoint = None
    if pymel.attributeQuery('rigType', node=input, exists=True):
        rigType = input.rigType.get()
        possibleMuscleJoint = None
        possibleBendMuscle = None

        if rigType == 'muscleJoint':
            muscleJoint = input
        elif rigType == 'muscleOriginJoint':
            possibleMuscleJoint = input.inverseScale.inputs()[0]
        elif rigType == 'muscleInsertionJoint':
            possibleMuscleJoint = input.inverseScale.inputs()[0]

        if rigType == 'muscleBendPivotPosition':
            muscleJoint = input

        elif rigType == 'muscleBendPivotPositionZro':
            for child in pymel.listRelatives(input, children=True):
                if pymel.attributeQuery('rigType', node=child, exists=True):
                    childRigType = child.rigType.get()
                    if childRigType == 'muscleBendPivotPosition':
                        muscleJoint = child

        elif rigType == 'muscleBendJoint':
            possibleBendMuscle = pymel.listRelatives(input, parent=True)[0]
            possibleBendMuscle = pymel.listRelatives(possibleBendMuscle, parent=True)[0]

        elif rigType == 'muscleBendOrigin':
            outputs = input.message.outputs()
            for each in outputs:
                if pymel.attributeQuery('rigType', node=each, exists=True):
                    eachRigType = each.rigType.get()
                    if rigType == 'muscleBendPivotPosition':
                        muscleJoint = input

        elif rigType == 'muscleBendInsertion':
            outputs = input.message.outputs()
            for each in outputs:
                if pymel.attributeQuery('rigType', node=each, exists=True):
                    eachRigType = each.rigType.get()
                    if rigType == 'muscleBendPivotPosition':
                        muscleJoint = input


        if possibleMuscleJoint:
            if pymel.attributeQuery('rigType', node=possibleMuscleJoint, exists=True):
                rigType = possibleMuscleJoint.rigType.get()
                if rigType == 'muscleJoint':
                    muscleJoint = possibleMuscleJoint

    return muscleJoint

def getRelatedBendMuscleJoint(input):
    muscleJoint = None
    if pymel.attributeQuery('rigType', node=input, exists=True):
        rigType = input.rigType.get()
        possibleMuscleJoint = None
        possibleBendMuscle = None

        if rigType == 'muscleBendPivotPosition':
            muscleJoint = input
        #elif rigType == 'muscleOriginJoint':
            #possibleMuscleJoint = input.inverseScale.inputs()[0]
        #elif rigType == 'muscleInsertionJoint':
            #possibleMuscleJoint = input.inverseScale.inputs()[0]

        #if rigType == 'muscleBendPivotPosition':
            #muscleJoint = input

        #elif rigType == 'muscleBendJoint':
            #possibleBendMuscle = pymel.listRelatives(input, parent=True)[0]
            #possibleBendMuscle = pymel.listRelatives(possibleBendMuscle, parent=True)[0]

        #elif rigType == 'muscleBendOrigin':
            #outputs = input.message.outputs()
            #for each in outputs:
                #if pymel.attributeQuery('rigType', node=each, exists=True):
                    #eachRigType = each.rigType.get()
                    #if rigType == 'muscleBendPivotPosition':
                        #muscleJoint = input

        #elif rigType == 'muscleBendInsertion':
            #outputs = input.message.outputs()
            #for each in outputs:
                #if pymel.attributeQuery('rigType', node=each, exists=True):
                    #eachRigType = each.rigType.get()
                    #if rigType == 'muscleBendPivotPosition':
                        #muscleJoint = input

        #if possibleMuscleJoint:
            #if pymel.attributeQuery('rigType', node=possibleMuscleJoint, exists=True):
                #rigType = possibleMuscleJoint.rigType.get()
                #if rigType == 'muscleJoint':
                    #muscleJoint = possibleMuscleJoint

    return muscleJoint

def getAllMuscleJoints():
    muscleJoints = []
    selection = pymel.ls(selection=True)
    joints = pymel.ls(type='joint')

    for joint in joints:
       if pymel.attributeQuery('rigType', node=joint, exists=True):
           rigType = joint.rigType.get()

           if rigType == 'muscleJoint':
               muscleJoints.append(joint)

    return muscleJoints

def getAllBendMuscleJoints():
    muscleBendJoints = []
    selection = pymel.ls(selection=True)
    curves = pymel.ls(type='nurbsCurve')

    for curve in curves:
        curve = pymel.listRelatives(curve, parent=True)[0]
        if pymel.attributeQuery('rigType', node=curve, exists=True):
           rigType = curve.rigType.get()
           if rigType == 'muscleBendPivotPosition':
               if curve not in muscleBendJoints:
                   muscleBendJoints.append(curve)

    return muscleBendJoints

def getAllMuscleSkinningJoints():
    muscleJoints = []
    selection = pymel.ls(selection=True)
    joints = pymel.ls(type='joint')

    for joint in joints:
       if pymel.attributeQuery('rigType', node=joint, exists=True):
           rigType = joint.rigType.get()
           if rigType == 'muscleJoint':
               muscleJoints.append(joint)
           elif rigType == 'muscleOriginJoint':
               muscleJoints.append(joint)
           elif rigType == 'muscleInsertionJoint':
               muscleJoints.append(joint)
           elif rigType == 'muscleBendJoint':
               muscleJoints.append(joint)

    return muscleJoints

def selectAllMuscleJoints():
    pymel.select(getAllMuscleSkinningJoints() )

def colorAllMuscleJoints():
    muscleJoints = []
    selection = pymel.ls(selection=True)
    joints = pymel.ls(type='joint')
    curves = pymel.ls(type='nurbsCurve')
    curves.extend(pymel.ls(type='locator'))

    for joint in joints:
       if pymel.attributeQuery('rigType', node=joint, exists=True):
           rigType = joint.rigType.get()

           if rigType == 'muscleBendJoint':
               joint.overrideEnabled.set(1)
               joint.overrideColor.set(29)

               if pymel.attributeQuery('baseName', node=joint, exists=True):
                   baseName = joint.baseName.get()
                   if baseName == 'muscleMidPointJoint':
                       joint.overrideEnabled.set(1)
                       joint.overrideColor.set(15)

           elif rigType == 'muscleOriginJoint':
               joint.overrideEnabled.set(1)
               joint.overrideColor.set(20)

           elif rigType in ['muscleJoint','muscleInsertionJoint']:
               joint.overrideEnabled.set(1)
               joint.overrideColor.set(4)



    for curve in curves:
        curve = pymel.listRelatives(curve, parent=True)[0]
        if pymel.attributeQuery('rigType', node=curve, exists=True):
           rigType = curve.rigType.get()
           if rigType in ['muscleBendPivotPosition','muscleBendOrigin','muscleBendInsertion','muscleInsertion','muscleOrigin']:
               curve.overrideEnabled.set(1)
               curve.overrideColor.set(22)

           elif rigType in ['muscleBendPivotPositionZro',]:
               curve.overrideEnabled.set(1)
               curve.overrideColor.set(26)


    return muscleJoints


def getMirroredObject(object):

        newName = None
        currentName = object.nodeName()
        if currentName[0:2] == 'r_':
            newName = 'l_'+ currentName[2:]
        elif currentName[0:2] == 'l_':
            newName = 'r_'+ currentName[2:]
        elif currentName[0:2] == 'R_':
            nameName = 'L_'+ currentName[2:]
        elif currentName[0:2] == 'L_':
            newName = 'R_'+ currentName[2:]

        elif '_r_' in currentName:
            newName = currentName.replace('_r_', '_l_', 1)
        elif '_l_' in currentName:
            newName = currentName.replace('_l_', '_r_', 1)
        elif '_R_' in currentName:
            newName = currentName.replace('R_', '_L_', 1)
        elif '_L_' in currentName:
            newName = currentName.replace('_L_', '_R_', 1)

        else:
            newName = currentName

        if pymel.objExists(newName):
            newObject = pymel.ls(newName)[0]
            return newObject


def mirrorMuscleJoint():
    selection = pymel.ls(selection=True)
    selectedMuscleJoints = [getRelatedMuscleJoint(each) for each in selection]
    fails = 0
    failStrings = []

    for originalMuscleJoint in selectedMuscleJoints:

#        try:
        newName = None
        currentName = originalMuscleJoint.nodeName()

        if currentName[0:2] == 'r_':
            newName = 'l_'+ currentName[2:]
        elif currentName[0:2] == 'l_':
            newName = 'r_'+ currentName[2:]
        elif currentName[0:2] == 'R_':
            nameName = 'L_'+ currentName[2:]
        elif currentName[0:2] == 'L_':
            newName = 'R_'+ currentName[2:]
        else:
            failStrings.append('%s naming prefix does not indicate side, So mirroring was skipped' % (str(originalMuscleJoint)))

        if newName:
           if pymel.attributeQuery('rigType', node=originalMuscleJoint, exists=True):
               rigType = originalMuscleJoint.rigType.get()

               if rigType == 'muscleJoint':
                   newbaseName = newName.split('_muscleJoint')[0]
                   initialLength = originalMuscleJoint.initialLength.get()
                   radius = originalMuscleJoint.radius.get()
                #            squashAndStretchStrength = originalMuscleJoint.squashAndStretchStrength.get()
                   if pymel.attributeQuery('squashAndStretchStrength', node=originalMuscleJoint, exists=True):
                       squashAndStretchStrength = originalMuscleJoint.squashAndStretchStrength.get()
                   else: #attribute has been spelt wrong initially by kris (me)
                       squashAndStretchStrength = originalMuscleJoint.squashAndStrechStrength.get()

                   mirroredJoint = _muscleJoint(name=newbaseName, initialLength=1.5, radius=0.4, squashAndStretchStrength=0)

                   originalMuscleOrigin = originalMuscleJoint.origin.inputs()[0]
                   originalMuscleOriginParent = pymel.listRelatives(originalMuscleOrigin, parent=True)[0]
                   originalMuscleInsertion = originalMuscleJoint.insertion.inputs()[0]
                   originalMuscleInsertionParent = pymel.listRelatives(originalMuscleInsertion, parent=True)[0]

                   newMuscleOrigin = mirroredJoint.origin.inputs()[0]
                   newMuscleOriginParent = getMirroredObject(originalMuscleOriginParent)
                   pymel.parent(newMuscleOrigin, newMuscleOriginParent)

                   newMuscleInsertion = mirroredJoint.insertion.inputs()[0]
                   newMuscleInsertionParent = getMirroredObject(originalMuscleInsertionParent)
                   pymel.parent(newMuscleInsertion, newMuscleInsertionParent)

                   snapMirrored(snapTarget=originalMuscleOrigin, snapObjects=[newMuscleOrigin])
                   snapMirrored(snapTarget=originalMuscleInsertion, snapObjects=[newMuscleInsertion])

               elif rigType == 'muscleBendPivotPosition':
                   newbaseName = newName.split('_pivotPosition')[0]
                   radius = originalMuscleJoint.radius.get()

                   newListOfJointLists = []
                   listOfJointLists = getBendyJoints(originalMuscleJoint)

                   for list in listOfJointLists:

                       newList = []
                       for joint in list:
                           newList.append( joint.constraintPercent.get() )

                       newListOfJointLists.append(newList)


                   jointPercents = newListOfJointLists

                   numberOfJoints = [len(newListOfJointLists[0]), len(newListOfJointLists[1])]


                   originalMuscleOrigin = originalMuscleJoint.origin.inputs()[0]
                   originalMuscleOriginParent = pymel.listRelatives(originalMuscleOrigin, parent=True)[0]
                   originalMuscleInsertion = originalMuscleJoint.insertion.inputs()[0]
                   originalMuscleInsertionParent = pymel.listRelatives(originalMuscleInsertion, parent=True)[0]
                   originalPivotPosition = originalMuscleJoint
                   originalPivotPositionZro = pymel.listRelatives(originalPivotPosition, parent=True)[0]
                   originalPivotPositionZroParent = pymel.listRelatives(originalPivotPositionZro, parent=True)[0]

                   #mirroredJoint = procedurallyCreateBendMuscle(baseName=newbaseName, radius=radius, jointPercents=jointPercents)
                   mirroredJoint = procedurallyCreateBendMuscle(baseName=newbaseName, numberOfJoints=numberOfJoints, radius=radius, insertionParent=None, originParent=None, pivotIndicatorZroParent=None, insertionMatrix=[], originMatrix=[], pivotIndicatorZroMatrix=[], jointPercents=jointPercents)



                   newMuscleOrigin = mirroredJoint.origin.inputs()[0]
                   newMuscleOriginParent = getMirroredObject(originalMuscleOriginParent)
                   pymel.parent(newMuscleOrigin, newMuscleOriginParent)

                   newMuscleInsertion = mirroredJoint.insertion.inputs()[0]
                   newMuscleInsertionParent = getMirroredObject(originalMuscleInsertionParent)
                   pymel.parent(newMuscleInsertion, newMuscleInsertionParent)

                   newPivotPosition = mirroredJoint
                   newPivotPositionZro = pymel.listRelatives(newPivotPosition, parent=True)[0]
                   newPivotPositionZroParent = getMirroredObject(originalPivotPositionZroParent)
                   pymel.parent(newPivotPositionZro, newPivotPositionZroParent)


                   snapMirrored(snapTarget=originalMuscleOrigin, snapObjects=[newMuscleOrigin])
                   snapMirrored(snapTarget=originalMuscleInsertion, snapObjects=[newMuscleInsertion])
                   snapMirrored(snapTarget=originalPivotPositionZro, snapObjects=[newPivotPositionZro])

                   pymel.xform(newMuscleOrigin, rotation=[0,180,0], relative=True, objectSpace=True)
                   pymel.xform(newMuscleInsertion, rotation=[0,180,0], relative=True, objectSpace=True)
                   pymel.xform(newPivotPositionZro, rotation=[0,180,0], relative=True, objectSpace=True)



def mirrorBendMuscleJoint():
    selection = pymel.ls(selection=True)
    selectedMuscleJoints = [getRelatedBendMuscleJoint(each) for each in selection]
    fails = 0
    failStrings = []

    for originalMuscleJoint in selectedMuscleJoints:

#        try:
        newName = None
        currentName = originalMuscleJoint.nodeName()

        if currentName[0:2] == 'r_':
            newName = 'l_'+ currentName[2:]
        elif currentName[0:2] == 'l_':
            newName = 'r_'+ currentName[2:]
        elif currentName[0:2] == 'R_':
            nameName = 'L_'+ currentName[2:]
        elif currentName[0:2] == 'L_':
            newName = 'R_'+ currentName[2:]
        else:
            failStrings.append('%s naming prefix does not indicate side, So mirroring was skipped' % (str(originalMuscleJoint)))

        if newName:
            if pymel.attributeQuery('rigType', node=originalMuscleJoint, exists=True):
                rigType = originalMuscleJoint.rigType.get()

               #if rigType == 'muscleJoint':
                   #newbaseName = newName.split('_muscleJoint')[0]
                   #initialLength = originalMuscleJoint.initialLength.get()
                   #radius = originalMuscleJoint.radius.get()
                ##            squashAndStretchStrength = originalMuscleJoint.squashAndStretchStrength.get()
                   #if pymel.attributeQuery('squashAndStretchStrength', node=originalMuscleJoint, exists=True):
                       #squashAndStretchStrength = originalMuscleJoint.squashAndStretchStrength.get()
                   #else: #attribute has been spelt wrong initially by kris (me)
                       #squashAndStretchStrength = originalMuscleJoint.squashAndStrechStrength.get()
                       #mirroredJoint = _muscleJoint(name=newbaseName, initialLength=1.5, radius=0.4, squashAndStretchStrength=0)

                   #originalMuscleOrigin = originalMuscleJoint.origin.inputs()[0]
                   #originalMuscleOriginParent = pymel.listRelatives(originalMuscleOrigin, parent=True)[0]
                   #originalMuscleInsertion = originalMuscleJoint.insertion.inputs()[0]
                   #originalMuscleInsertionParent = pymel.listRelatives(originalMuscleInsertion, parent=True)[0]

                   #newMuscleOrigin = mirroredJoint.origin.inputs()[0]
                   #newMuscleOriginParent = getMirroredObject(originalMuscleOriginParent)
                   #pymel.parent(newMuscleOrigin, newMuscleOriginParent)

                   #newMuscleInsertion = mirroredJoint.insertion.inputs()[0]
                   #newMuscleInsertionParent = getMirroredObject(originalMuscleInsertionParent)
                   #pymel.parent(newMuscleInsertion, newMuscleInsertionParent)

                   #snapMirrored(snapTarget=originalMuscleOrigin, snapObjects=[newMuscleOrigin])
                   #snapMirrored(snapTarget=originalMuscleInsertion, snapObjects=[newMuscleInsertion])

               #elif rigType == 'muscleBendPivotPosition':
                   #newbaseName = newName.split('_pivotPosition')[0]
                   #radius = originalMuscleJoint.radius.get()

                   #mirroredJoint = _createBendMuscle(name=newbaseName, radius=radius)

                   #originalMuscleOrigin = originalMuscleJoint.origin.inputs()[0]
                   #originalMuscleOriginParent = pymel.listRelatives(originalMuscleOrigin, parent=True)[0]
                   #originalMuscleInsertion = originalMuscleJoint.insertion.inputs()[0]
                   #originalMuscleInsertionParent = pymel.listRelatives(originalMuscleInsertion, parent=True)[0]
                   #originalPivotPosition = originalMuscleJoint
                   #originalPivotPositionParent = pymel.listRelatives(originalPivotPosition, parent=True)[0]

                   #newMuscleOrigin = mirroredJoint.origin.inputs()[0]
                   #newMuscleOriginParent = getMirroredObject(originalMuscleOriginParent)
                   #pymel.parent(newMuscleOrigin, newMuscleOriginParent)

                   #newMuscleInsertion = mirroredJoint.insertion.inputs()[0]
                   #newMuscleInsertionParent = getMirroredObject(originalMuscleInsertionParent)
                   #pymel.parent(newMuscleInsertion, newMuscleInsertionParent)

                   #newPivotPosition = mirroredJoint
                   #newPivotPositionParent = getMirroredObject(originalPivotPositionParent)
                   #pymel.parent(newPivotPosition, newPivotPositionParent)

                   #snapMirrored(snapTarget=originalMuscleOrigin, snapObjects=[newMuscleOrigin])
                   #snapMirrored(snapTarget=originalMuscleInsertion, snapObjects=[newMuscleInsertion])
                   #snapMirrored(snapTarget=originalPivotPosition, snapObjects=[newPivotPosition])



def alignAllMuscleOrigin():
    muscleOrigins = []
    selection = pymel.ls(selection=True)
    joints = pymel.ls(type='joint')

    for joint in joints:
       if pymel.attributeQuery('rigType', node=joint, exists=True):
           rigType = joint.rigType.get()
           if rigType == 'muscleJoint':
               muscleOrigins.append(joint)

    if muscleOrigins:
        for muscleOrigin in muscleOrigins:
            alignMuscleOrigin(muscleJoints=[muscleOrigin])

    pymel.select(selection)

def alignMuscleOrigin(muscleJoints=None):

    muscleJoints = []
    muscleBendJoints = []
    selection = pymel.ls(selection=True)
    joints = pymel.ls(type='joint')
    curves = pymel.ls(type='nurbsCurve')
    curves.extend(pymel.ls(type='locator'))

    for joint in joints:
       if pymel.attributeQuery('rigType', node=joint, exists=True):
           rigType = joint.rigType.get()

           if rigType == 'muscleJoint':
               muscleJoints.append(joint)

    for curve in curves:
       if pymel.attributeQuery('rigType', node=joint, exists=True):
           rigType = joint.rigType.get()

           if rigType == 'muscleBendJoint':
               muscleBendJoints.append(each)

#    if muscleJoints == None:
#        muscleJoints = []
#        for each in selection:
#            if pymel.attributeQuery('rigType', node=each, exists=True):
#                rigType = each.rigType.get()
#                if rigType == 'muscleJoint':
#                    muscleJoints.append(each)
#
#        muscleJoints = pymel.ls(selection=True)

    if muscleJoints:
        for muscleJoint in muscleJoints:
            originLocator = muscleJoint.origin.inputs()[0]
            insertionLocator = muscleJoint.insertion.inputs()[0]
            insertionMatrix = pymel.xform(insertionLocator, q=True, ws=True, m=True)
            snap(r=True, snapTarget=muscleJoint.name(), snapObjects=[originLocator.name()])
            pymel.xform(insertionLocator, ws=True, m=insertionMatrix)
            snap(r=True, snapTarget=muscleJoint.name(), snapObjects=[insertionLocator.name()])

            pointA = pymel.xform(originLocator, query=True, ws=True, translation=True)
            pointB = pymel.xform(insertionLocator, query=True, ws=True, translation=True)
            initialDistance = distanceBetween(pointA, pointB)
            muscleJoint.initialLength.set(initialDistance*0.5)

    if muscleBendJoints:
        for muscleBendJoint in muscleBendJoints:
            originLocator = muscleBendJoint.origin.inputs()[0]
            insertionLocator = muscleBendJoint.insertion.inputs()[0]

            insertionMatrix = pymel.xform(insertionLocator, q=True, ws=True, m=True)
            snap(r=True, snapTarget=muscleJoint.name(), snapObjects=[originLocator.name()])
            pymel.xform(insertionLocator, ws=True, m=insertionMatrix)
            snap(r=True, snapTarget=muscleJoint.name(), snapObjects=[insertionLocator.name()])

#            pointA = pymel.xform(originLocator, query=True, ws=True, translation=True)
#            pointB = pymel.xform(insertionLocator, query=True, ws=True, translation=True)
#            initialDistance = distanceBetween(pointA, pointB)
#            muscleJoint.initialLength.set(initialDistance*0.5)

    pymel.select(selection)


def snap(t=0, s=0, r=0, snapTarget=None, snapObjects=None):
    '''snaps objects to A to object B based on translate rotate or scale'''
    sel = cmds.ls(selection=True)

    if not snapObjects:
        snapObjects = sel[:-1]

    if not snapTarget:
        snapTarget = sel[-1:]

    if t == 1:
        for each in snapObjects:
#            tempConstraint = pointConstraint(snapTarget, each)
#            delete(tempConstraint)

#            matrix = cmds.xform(snapTarget, q=True, ws=True, m=True)
#            origMatrix = cmds.xform(each, q=True, ws=True, m=True)
#
#            origMatrix[12] = matrix[12]
#            origMatrix[13] = matrix[13]
#            origMatrix[14] = matrix[14]
#
#            cmds.xform(each, ws=True, m=origMatrix)
#
            worldTrans = cmds.xform(snapTarget, q=True, ws=True, translation=True)
            cmds.xform(each, ws=True, translation=worldTrans)

    if s == 1:
        for each in snapObjects:
            tempConstraint = cmds.scaleConstraint(snapTarget, each)
            delete(tempConstraint)
#            worldScale = cmds.xform(snapTarget, q=True, scale=True)
#            cmds.xform(each, ws=True, scale=worldScale)

    if r == 1:
        for each in snapObjects:

            worldRot = cmds.xform(snapTarget, q=True, ws=True, rotation=True)
            cmds.xform(each, ws=True, rotation=worldRot)

    cmds.select(snapObjects)

def snapMirrored(snapTarget=None, snapObjects=None):

    sel = pymel.ls(sl=True)
    if not snapObjects:
        snapObjects = sel[:-1]

    if not snapTarget:
        snapTarget = sel[-1]

    for each in snapObjects:
	snap(m=True)


    cmds.select(snapObjects)

def updateClosestPose():

    selection = pymel.ls(selection=True)
    for node in selection:

	poseDriver = _getPoseDriver(node)
	if poseDriver:
	    poseTranslate = node.t.get()
	    poseRotate = node.r.get()
	    keyableAttrs = poseDriver.listAttr(keyable=True)

	    poseAngleAttrs = []
	    poseAngleAttrsByValue = {}
	    largestAttr = None
	    largestAttrValue = 180.0

	    for attr in keyableAttrs:
		if attr.name(includeNode=False).startswith('pAngleFrom_'):
		    #poseAngleAttrs.append(attr)
		    #poseAngleAttrsByValue[attr.get()] = attr

		    attrValue = attr.get()
		    if attrValue < largestAttrValue:
			largestAttrValue = attrValue
			largestAttr = attr

	    largestAngleFromAttrName = largestAttr.name(includeNode=False)
	    largestWeightAttrName = largestAngleFromAttrName.replace('pAngleFrom_', 'pWt_')
	    largestAttrName = largestAngleFromAttrName.replace('pAngleFrom_', '')

	    targetWeightAttr = poseDriver.attr(largestWeightAttrName).outputs(plugs=True)[0]
	    targetAttr = targetWeightAttr.getParent()

	    targetAttr.targetTranslate.set(poseTranslate)
	    targetAttr.targetRotate.set(poseRotate)

	    print('updated pose:%s on %s' % (largestAttrName, poseDriver.nodeName()))


def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def vectorLength(v):
    return math.sqrt(dotproduct(v, v))

def angleBetween(v1, v2):
    return math.acos(dotproduct(v1, v2) / (vectorLength(v1) * vectorLength(v2)))

def setRigTypes(nodes, rigTypes):

    # excepts args as list or single item
    if not isinstance(nodes, list):
	nodes = [nodes]
    if not isinstance(rigTypes, list):
	rigTypes = [rigTypes]

    for node in nodes:
	if not hasattr(node, 'rigType'):
	    node.addAttr('rigType', dataType='string', shortName='rigType')
	else:
	    node.rigType.set(lock=False)

	node.rigType.set(str(rigTypes))
	node.rigType.set(lock=True)

def getRigTypes(node):
    if hasattr(node, 'rigType'):
	rigTypes = eval(node.rigType.get())
	if isinstance(rigTypes, list):
	    if rigTypes:
		if isinstance(rigTypes[0], str):
		    return rigTypes

    return []

def setPoseDriverPose(nodes=None, driver=None, driverType=None):

    selection = pymel.ls(selection=True)


    selectionIsPoseDriven = True
    for node in selection:
	poseDriver = _getPoseDriver(node)
	if not poseDriver:
	    if selectionIsPoseDriven:
		selectionIsPoseDriven = False

	else:
	    if not selectionIsPoseDriven:
		pymel.error('selection contains a mix of poseDriven, and non poseDriven items')


    defaultText = ''
    if not selectionIsPoseDriven:
	defaultText = 'defautPose'

    poseName = ''
    result = cmds.promptDialog(
                    title='Set Pose Name',
                    message='Enter a Pose Name:',
                    text=defaultText,
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')


    if result == 'OK':
	poseName = cmds.promptDialog(query=True, text=True)

	if selectionIsPoseDriven:
	    nodes = selection

	    for node in nodes:
		_setPoseDriverPose(node, poseName=poseName, driverType='pose')
		print('poseDriven')
	else:
	    nodes = selection[1:]
	    driver = selection[0]

	    for node in nodes:
		_setPoseDriverPose(node, poseName=poseName, driver=driver, driverType='pose')


	pymel.select(nodes)


def _setPoseDriverPose(node, poseName=None, driver=None, driverType=None):

    poseTranslate = node.t.get()
    poseRotate = node.r.get()

    isDefaultPose = False
    poseDriver = _getPoseDriver(node)
    if not poseDriver:
	poseDriver = _createPoseDriver(node)
    	poseName = 'defaultPose'
	isDefaultPose = True

    poseIndex = 0
    for index in poseDriver.target.getArrayIndices():
	poseIndex = index + 1


    if not poseName:
	poseName = 'pose_'+str(poseIndex)


    poseDriver.addAttr(poseName, attributeType='enum', shortName=poseName, hasMinValue=True, minValue=0.0, hasMaxValue=True, maxValue=0.0, enumName='--------', )
    poseDriver.attr(poseName).set(lock=True, keyable=True, channelBox=True, )

    # make weight attribute
    poseWeightAttrName = 'pWt_'+poseName
    poseDriver.addAttr(poseWeightAttrName, attributeType='double', shortName=poseWeightAttrName, hasSoftMinValue=True, softMinValue=0.0, hasSoftMaxValue=True, softMaxValue=1.0, )
    poseDriver.attr(poseWeightAttrName).set(1.0, keyable=True,)
    poseDriver.attr(poseWeightAttrName) >> poseDriver.target[poseIndex].targetWeight

    poseDriver.target[poseIndex].targetTranslate.set(poseTranslate)
    poseDriver.target[poseIndex].targetRotate.set(poseRotate)


    #poseAngleAttrName = 'pAng_'+poseName
    #poseDriver.addAttr(poseAngleAttrName, attributeType='double', shortName=poseAngleAttrName, hasSoftMinValue=True, softMinValue=0.0, hasSoftMaxValue=True, softMaxValue=180.0, )
    #poseDriver.attr(poseAngleAttrName).set(45.0, keyable=True, channelBox=True, )

    # get pose reader vector product
    poseReader = None
    if not driver:
	inputs = poseDriver.previousInput.inputs()
	if inputs:
	    poseReader = inputs[0]

    if not poseReader:
	poseReader = _createPoseReader(driver)

    poseReader.message >> poseDriver.previousInput

    if isDefaultPose:
	nonDefaultPoseWeightsTotal = pymel.createNode('plusMinusAverage')
	setRigTypes(nonDefaultPoseWeightsTotal, 'nonDefaultPoseWeightsTotal')
	nonDefaultPoseWeightsTotal.message >> poseDriver.nonDefaultPoseWeightsTotal
	poseDriver.addAttr('defaultPoseVector', attributeType='float3' )
	poseDriver.addAttr('defaultPoseVectorX', attributeType='float', parent='defaultPoseVector')
	poseDriver.addAttr('defaultPoseVectorY', attributeType='float', parent='defaultPoseVector' )
	poseDriver.addAttr('defaultPoseVectorZ', attributeType='float', parent='defaultPoseVector' )
	poseDriver.defaultPoseVector.set(poseReader.output.get())

	plusMinusAverageSubtract = pymel.createNode('plusMinusAverage')
	plusMinusAverageSubtract.operation.set(2)
	plusMinusAverageSubtract.input1D[0].set(1)

	condition = pymel.createNode('condition', )
	condition.operation.set(2)
	condition.colorIfFalse.colorIfFalseR.set(0.0)

	nonDefaultPoseWeightsTotal.output1D >> plusMinusAverageSubtract.input1D[1]
	plusMinusAverageSubtract.output1D >> condition.firstTerm
	plusMinusAverageSubtract.output1D >> condition.colorIfTrue.colorIfTrueR
	condition.outColorR >> poseDriver.attr(poseWeightAttrName)



    else:
	nonDefaultPoseWeightsTotal = _getNonDefaultPoseWeightsTotalNode(poseDriver)

	# make angleFromPose Attr
	angleFromPoseAttrName = 'pAngleFrom_'+poseName
	poseDriver.addAttr(angleFromPoseAttrName, attributeType='double', shortName=angleFromPoseAttrName, hasSoftMinValue=True, softMinValue=0.0, hasSoftMaxValue=True, softMaxValue=1.0, )
	poseDriver.attr(angleFromPoseAttrName).set(keyable=True,)

	## set Range
	#setRange = pymel.createNode('setRange')
	#setRange.oldMinX.set(-1)
	#setRange.oldMaxX.set(1)
	#setRange.maxX.set(0)
	#setRange.minX.set(180)

	## dot product
	#poseCompareVectorProduct = pymel.createNode('vectorProduct')
	#poseCompareVectorProduct.rename(poseName+'_poseCompare')
	#poseCompareVectorProduct.operation.set(1)
	#poseCompareVectorProduct.input2.set(poseReader.output.get())

	## dot product
	angleBetweenNode = pymel.createNode('angleBetween')
	angleBetweenNode.rename(poseName+'_poseCompare')
	angleBetweenNode.vector2.set(poseReader.output.get())

	# pose driver set driven key
	poseKeyframe = pymel.createNode('animCurveUU')
	pymel.setKeyframe(poseKeyframe, insert=True, float=0.0)
	pymel.keyframe(poseKeyframe, index=0, absolute=True, valueChange=1.0)

	# make connections
	poseReader.output >> angleBetweenNode.vector1
	angleBetweenNode.axisAngle.angle >> poseKeyframe.input
	angleBetweenOutConversion = poseKeyframe.input.inputs()[0]

	poseKeyframe.output >> poseDriver.attr(poseWeightAttrName)
	angleBetweenOutConversion.output >> poseDriver.attr(angleFromPoseAttrName)
	poseKeyframe.output >> nonDefaultPoseWeightsTotal.input1D[poseIndex]

	#poseReader.output >> poseCompareVectorProduct.input1
	#poseCompareVectorProduct.outputX >> setRange.valueX
	#setRange.outValueX >> poseKeyframe.input
	#poseKeyframe.output >> poseDriver.attr(poseWeightAttrName)
	#setRange.outValueX >> poseDriver.attr(angleFromPoseAttrName)
	#poseKeyframe.output >> nonDefaultPoseWeightsTotal.input1D[poseIndex]

	defaultVector = poseDriver.defaultPoseVector.get()
	currentVector = poseReader.output.get()
	angleFromDefault = angleBetween(defaultVector, currentVector)
	angleFromDefault = 180 * angleFromDefault / math.pi # radians to degrees

	pymel.setKeyframe(poseKeyframe, insert=True, float=angleFromDefault)
	pymel.keyframe(poseKeyframe, index=1, absolute=True, valueChange=0.0)
	pymel.keyTangent( poseKeyframe, edit=True, index=[0, 1], inTangentType='linear', outTangentType='linear')

def _getNonDefaultPoseWeightsTotalNode(poseDriver):
    inputs = poseDriver.nonDefaultPoseWeightsTotal.inputs()
    if inputs:
	return inputs[0]


def _getPoseDriver(node):
    for inputNode in node.tx.inputs():
	if 'poseDriver' in getRigTypes(inputNode):
	    return inputNode

def _getPoseReader(node):
    for outputNode in node.matrix.outputs():
	if 'poseReader' in getRigTypes(outputNode):
	    return outputNode

def _createPoseReader(node):
    poseReader_mainAxis = pymel.createNode('vectorProduct')
    poseReader_mainAxis.rename(node.nodeName()+'_poseReaderMain')
    setRigTypes(poseReader_mainAxis, 'poseReader')
    poseReader_mainAxis.operation.set(3)
    poseReader_mainAxis.input1.set(1.0, 0.0, 0.0)

    poseReader_secondaryAxis = pymel.createNode('vectorProduct')
    poseReader_secondaryAxis.rename(node.nodeName()+'_poseReaderSecondary')
    setRigTypes(poseReader_secondaryAxis, 'poseReaderSecondary')
    poseReader_secondaryAxis.operation.set(3)
    poseReader_secondaryAxis.input1.set(0.0, 0.0, 1.0)

    node.matrix >> poseReader_mainAxis.matrix
    node.matrix >> poseReader_secondaryAxis.matrix

    return poseReader_mainAxis

def _createPoseDriver(node):
    if not 'dagNode' in node.nodeType(inherited=True):
	pymel.error('cannot create a pose for non transforms')

    poseDriver = pymel.createNode('parentConstraint', parent=node)
    poseDriver.rename(node.nodeName()+'_poseDriver')
    setRigTypes(poseDriver, 'poseDriver')
    poseDriver.addAttr('previousInput', attributeType='message', shortName='previousInput')
    poseDriver.addAttr('nonDefaultPoseWeightsTotal', attributeType='message', shortName='ndpwt')
    poseDriver.interpType.set(2)
    poseDriver.tx.set(keyable=False)
    poseDriver.ty.set(keyable=False)
    poseDriver.tz.set(keyable=False)
    poseDriver.rx.set(keyable=False)
    poseDriver.ry.set(keyable=False)
    poseDriver.rz.set(keyable=False)
    poseDriver.sx.set(keyable=False)
    poseDriver.sy.set(keyable=False)
    poseDriver.sz.set(keyable=False)
    poseDriver.v.set(keyable=False)

    node.rotatePivotTranslate            >> poseDriver.constraintRotateTranslate
    #node.parentInverseMatrix[0]          >> poseDriver.constraintParentInverseMatrix
    node.rotateOrder                     >> poseDriver.constraintRotateOrder
    node.rotatePivot                     >> poseDriver.constraintRotatePivot

    poseDriver.constraintRotate.constraintRotateX       >> node.rotate.rotateX
    poseDriver.constraintRotate.constraintRotateY       >> node.rotate.rotateY
    poseDriver.constraintRotate.constraintRotateZ       >> node.rotate.rotateZ
    poseDriver.constraintTranslate.constraintTranslateZ >> node.translate.translateZ
    poseDriver.constraintTranslate.constraintTranslateY >> node.translate.translateY
    poseDriver.constraintTranslate.constraintTranslateX >> node.translate.translateX

    return poseDriver


def setKeyframes(nodes=None):
    """Same as setting a keyframe regularly, but works on set driven keys as well"""

    if not nodes:
        nodes = pymel.ls(selection=True)

    setDrivenFound = False
    for node in nodes:
        for inputNode in node.inputs():
            if 'animCurveU' in inputNode.nodeType():
                outputPlugs = inputNode.output.outputs(skipConversionNodes=True, plugs=True)
                if outputPlugs:
                    keyTime = inputNode.input.get()
                    keyValue = outputPlugs[0].get()

                    pymel.setKeyframe(inputNode, insert=True, float=keyTime)
                    index = pymel.keyframe(inputNode, query=True, float=[keyTime], indexValue=True,)

                    pymel.keyframe(inputNode, index=index, absolute=True, valueChange=keyValue)

                    setDrivenFound = True

            elif 'poseDriver' in getRigTypes(inputNode):
		updateClosestPose()

		setDrivenFound = True
		break



    if not setDrivenFound:
        mel.eval('performSetKeyframeArgList 1 {"0", "animationList"}')



def createJointNet():
    text=None
    result = cmds.promptDialog(
                    title='Name Muscle',
                    message='Enter a Base Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)

        if text:
            _createJointNet(text)

def _getJointNet_worldPositionVP(joint):
    pass

def _createJointNet(baseName, jointsU=10, jointsV=10):
    joints = {}
    lastU = jointsU-1
    lastV = jointsV-1
    elementDict = {}

    for iU in range(jointsU):
	joints[iU] = {}
	for iV in range(jointsV):
	    if iU == 0 and iV == 0: pass
	    elif iU == lastU and iV == lastV: pass
	    elif iU == 0 and iV == lastV: pass
	    elif iU == lastU and iV == 0: pass
	    else:
		isJoint = True
		if iU == 0 or iU == lastU or iV == 0 or iV == lastV:
		    transform = pymel.createNode('locator', parent=None)
		    transform.localScale.set(0.1, 0.1, 0.1, )
		    transform = transform.getParent()
		    isJoint = False

		else:
		    transform = pymel.createNode('joint', parent=None)
		    transform.radius.set(0.1)

		elementDict[transform] = {}

		transform.rename('%s_transformNet_%s_%s' % (baseName, str(iU), str(iV)))
		transform.tx.set((5.0/jointsU)*iU)
		transform.tz.set((5.0/jointsV)*iV)
		joints[iU][iV] = transform

		vectorProduct = pymel.createNode('vectorProduct')
		vectorProduct.rename('%s_transformNet_%s_%s_vectorProduct' % (baseName, str(iU), str(iV)))
		vectorProduct.operation.set(4)
		setRigTypes(vectorProduct, ['transformNet_worldSpaceVectorProduct'])
		elementDict[transform]['vectorProduct'] = vectorProduct

		transform.parentMatrix[0] >> vectorProduct.matrix
		transform.t >> vectorProduct.input1

		if isJoint:
		    aimConstraint = pymel.createNode('aimConstraint', parent=transform)
		    aimConstraint.rename('%s_transformNet_%s_%s_aimConstraint' % (baseName, str(iU), str(iV)))
		    aimConstraint.upVector.set(0.0, 0.0, 1.0, )
		    setRigTypes(vectorProduct, ['transformNet_aimConstraint'])
		    elementDict[transform]['aimConstraint'] = aimConstraint

		    transform.t >> aimConstraint.constraintTranslate
		    transform.rotateOrder >> aimConstraint.constraintRotateOrder
		    transform.parentInverseMatrix >> aimConstraint.constraintParentInverseMatrix
		    aimConstraint.constraintRotateX >> transform.rotateX
		    aimConstraint.constraintRotateY >> transform.rotateY
		    aimConstraint.constraintRotateZ >> transform.rotateZ



    for iU in range(jointsU):
	for iV in range(jointsV):
	    if iU == 0 and iV == 0: pass
	    elif iU == lastU and iV == lastV: pass
	    elif iU == 0 and iV == lastV: pass
	    elif iU == lastU and iV == 0: pass
	    else:
		if iU == 0 or iU == lastU or iV == 0 or iV == lastV:
		    pass
		else:
		    isJoint = True

		    joint = joints[iU][iV]

		    nextUJoint = joints[iU+1][iV]
		    previousUJoint = joints[iU-1][iV]

		    nextVJoint = joints[iU][iV+1]
		    previousVJoint = joints[iU][iV-1]

		    # U aim
		    subtract = pymel.createNode('plusMinusAverage')
		    subtract.operation.set(2)

		    invert = pymel.createNode('multiplyDivide')
		    invert.input2.set(-1,-1,-1)

		    add = pymel.createNode('plusMinusAverage')

		    average = pymel.createNode('plusMinusAverage')
		    average.operation.set(3)

		    elementDict[previousUJoint]['vectorProduct'].output >> subtract.input3D[0]
		    elementDict[joint]['vectorProduct'].output >> subtract.input3D[1]

		    subtract.output3D >> invert.input1

		    elementDict[joint]['vectorProduct'].output >> add.input3D[0]
		    invert.output >> add.input3D[1]

		    add.output3D >> average.input3D[0]
		    elementDict[nextUJoint]['vectorProduct'].output >> average.input3D[1]

		    average.output3D >> elementDict[joint]['aimConstraint'].target[0].targetTranslate


		    # V aim
		    subtractA = pymel.createNode('plusMinusAverage')
		    subtractA.operation.set(2)

		    subtractB = pymel.createNode('plusMinusAverage')
		    subtractB.operation.set(2)

		    invert = pymel.createNode('multiplyDivide')
		    invert.input2.set(-1,-1,-1)

		    #add = pymel.createNode('plusMinusAverage')

		    average = pymel.createNode('plusMinusAverage')
		    average.operation.set(3)

		    elementDict[previousVJoint]['vectorProduct'].output >> subtractA.input3D[0]
		    elementDict[joint]['vectorProduct'].output >> subtractA.input3D[1]

		    subtractA.output3D >> invert.input1

		    elementDict[nextVJoint]['vectorProduct'].output >> subtractB.input3D[0]
		    elementDict[joint]['vectorProduct'].output >> subtractB.input3D[1]

		    invert.output >> average.input3D[0]
		    subtractB.output3D >> average.input3D[1]

		    average.output3D >> elementDict[joint]['aimConstraint'].worldUpVector


def getWorldSpaceVectorProduct(transform):
    for node in a.worldMatrix.outputs():
	if node.nodeType() == 'vectorProduct':
	    if node.operation.get() == 4:
		if node.input1.get() == (0.0, 0.0, 0.0):
		    return node

    vectorProduct = pymel.createNode('vectorProduct')
    vectorProduct.rename('%s_worldSpaceVectorProduct' % transform.nodeName())
    vectorProduct.operation.set(4)
    transform.worldMatrix >> vectorProduct.matrix
    return ectorProduct

def transformNetConstraint():
    selection = pymel.ls(selection=True)
    contrainedObject = selection[-1]
    contraintTargets = selection[0:-1]

    # get world space vector product for all involved transforms
    contrainedObject_worldSpaceVectorProduct = getWorldSpaceVectorProduct(contrainedObject)
    worldSpaceVectorProducts = []
    for contraintTarget in contraintTargets:
	worldSpaceVectorProducts.append(getWorldSpaceVectorProduct(contraintTarget))

    # get the vectors from each target to the constrained object
    vectorsToConstrainedObject = []
    for i, contraintTarget in enumerate(contraintTargets):
	vectorToConstrainedObject = pymel.createNode('plusMinusAverage')
	vectorToConstrainedObject.rename('vectorFrom_%s_to_%s' % (contraintTarget.nodeName(), contrainedObject.nodeName()))
	vectorToConstrainedObject.operation.set(2)

	worldSpaceVectorProducts[i].ouput >> vectorToConstrainedObject.input3D[0]
	contrainedObject_worldSpaceVectorProduct.output >> vectorToConstrainedObject.input3D[1]

	vectorsToConstrainedObject.append(vectorToConstrainedObject)

    # create a cross product between each of the constraintTargets
    crossProducts = []
    for i, contraintTarget in enumerate(contraintTargets):
	currentVector = vectorsToConstrainedObject[i]

	if contraintTarget == contraintTargets[-1]: # is last
	    nextVector = vectorsToConstrainedObject[0]
	else:
	    nextVector = vectorsToConstrainedObject[i+1]

	crossProduct = pymel.createNode('vectorProduct')
	crossProduct.rename('crossProductOf_%s_and_%s' % (contraintTarget.nodeName(), contraintTargets[i+1].nodeName()))
	crossProduct.operation.set(2)

	nextVector.output3D >> crossProduct.input1
	currentVector.output3D >> crossProduct.input2


    # get and averaged vector for all cross products
    crossProductAverage = vectorToConstrainedObject = pymel.createNode('plusMinusAverage')
    crossProductAverage.rename('crossProductAverage')
    crossProductAverage.operation.set(3)
    for i, crossProduct in enumerate(crossProducts):
	crossProduct.output >> crossProductAverage.input3D[i]




    # make aim constraint
    aimConstaint = pymel.createNode('aimConstraint')
    aimConstaint.rename('%s_balancedAimConstraint' % contrainedObject.nodeName())

    crossProductAverage.output3D >> aimConstaint.target[0].targetTranslate

    if contrainedObject.nodeType() == 'joint':
	contrainedObject.jointOrient >> aimConstaint.constraintJointOrient

    contrainedObject.parentInverseMatrix >> aimConstaint.constraintParentInverseMatrix
    contrainedObject.rotateOrder >> aimConstaint.constraintRotateOrder
    contrainedObject.rotatePivot >> aimConstaint.constraintRotatePivot
    contrainedObject.rotateTranslate >> aimConstaint.constraintRotateTranslate
    contrainedObject.translate >> aimConstaint.constraintTranslate

    aimConstaint.constraintRotateX >> contrainedObject.rotateX
    aimConstaint.constraintRotateY >> contrainedObject.rotateY
    aimConstaint.constraintRotateZ >> contrainedObject.rotateZ





#

