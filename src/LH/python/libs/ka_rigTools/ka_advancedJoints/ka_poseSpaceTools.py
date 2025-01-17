 #====================================================================================
#====================================================================================
#
# ka_poseSpaceTools
#
# DESCRIPTION:
#   a series of tools to make pose drivers
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


import maya.cmds as cmds
import pymel.core as pymel
import maya.mel as mel
import maya.OpenMayaUI as OpenMayaUI



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
