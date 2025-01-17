    #====================================================================================
#====================================================================================
#
# ka_advancedJoints_volumeRotator
#
# DESCRIPTION:
#   A joint set up that has helps create the effect of volume being preserved
#
# DEPENDENCEYS:
#   -Maya
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
import sys

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_math as ka_math; importlib.reload(ka_math)
import ka_rigTools.ka_util as ka_util; importlib.reload(ka_util)
import ka_rigTools.ka_pymel as ka_pymel; importlib.reload(ka_pymel)
import ka_rigTools.ka_shapes as ka_shapes; importlib.reload(ka_shapes)
import ka_rigTools.ka_naming as ka_naming; importlib.reload(ka_naming)
import ka_rigTools.ka_transforms as ka_transforms; importlib.reload(ka_transforms)
import ka_rigTools.ka_constraints as ka_constraints; importlib.reload(ka_constraints)
import ka_rigTools.ka_advancedJoints.ka_advancedJoints_commands as ka_advancedJoints_commands; importlib.reload(ka_advancedJoints_commands)
import importlib

#import ka_rigTools.ka_advancedJoints.ka_advancedJoints_volumeRotator as ka_advancedJoints_volumeRotator #;reload(ka_advancedJoints_volumeRotator)
#ka_advancedJoints_volumeRotator.printAllVolumeRotators()
#ka_advancedJoints_volumeRotator.printAllVolumeRotators()

MODULE_LONG_NAME = __name__
MODULE_SHORT_NAME = MODULE_LONG_NAME.split('.')[-1]

VOLUME_ROTATOR_ZRO_NAME_SUFFIX = '_volumeRotator_Zro'
VOLUME_ROTATOR_NAME_SUFFIX = '_volumeRotator'


def create():
    selection = pymel.ls(selection=True)
    for node in selection:
        volumeRotator = VolumeRotator(bendJoint=node)

def printAllVolumeRotators(skipMirrored=True):

    print('\nimport %s as %s    #;reload(%s)' % (MODULE_LONG_NAME, MODULE_SHORT_NAME, MODULE_SHORT_NAME))

    volumeRotatorNodes = getAllVolumeRotatorNodes()
    for node in volumeRotatorNodes:
	volumeRotator = VolumeRotator(node)
	if volumeRotator.oppositeVolumeRotator and skipMirrored:
	    pass

	else:
	    volumeRotator.printCreateCommand()

def printSelectedVolumeRotators():
    volumeRotatorNodes = getSelectedVolumeRotatorNodes()


def getSelectedVolumeRotatorNodes():
    selectedVolumeRotators = []
    selection = pymel.ls(selection=True)
    for node in selection:
	relatedVolumeRotator = getRelatedVolumeRotator(node)
	if relatedVolumeRotator:
	    selectedVolumeRotators.append(relatedVolumeRotator)

    return selectedVolumeRotators


def getAllVolumeRotatorNodes():
    allVolumeRotators = []
    for transform in pymel.ls(type='transform'):
	if 'volumeRotatorGrpZro' in ka_advancedJoints_commands.getRigTypes(transform):
	    allVolumeRotators.append(transform)
    return allVolumeRotators


def getRelatedVolumeRotatorNodes(node):
    if 'volumeRotatorGrpZro' in ka_advancedJoints_commands.getRigTypes(node):
	return node

    nodeParent = node.getParent()
    while nodeParent:
	if 'volumeRotatorGrpZro' in ka_advancedJoints_commands.getRigTypes(nodeParent):
	    return nodeParent

	nodeParent = nodeParent.getParent()


class VolumeRotator(object):


    #----------------------------------------------------------------------
    def __init__(self, volumeRotatorGrpZro=None, baseName=None, bendJoint=None, intersectPlaneDict=None,
                 rootTransform=None, rootTransformOffset=None, oppositeVolumeRotator=None, alsoCreateMirror=True):
        """"""

	self.volumeRotatePlaneDict = {}

        # volumeRotator is being created
        if not volumeRotatorGrpZro:

	    # oppositeVolumeRotator
	    self.oppositeVolumeRotator = oppositeVolumeRotator

            # baseName
            if baseName:
                self.baseName = baseName
            else:
                self.baseName = bendJoint.nodeName()

            # bendJoint
            if bendJoint:
                self.bendJoint = ka_pymel.getAsPyNodes(bendJoint)
                self.bendJointRadius = self.bendJoint.radius.get()
                self.pushJointRadius = self.bendJointRadius*0.3

		if self.bendJoint.tx.get() >= 0:
		    self.side = 1
		else:
		    self.side = -1

                self.bendJointLength = 1#*self.side
                bendJointChildren = self.bendJoint.getChildren(type='joint')
                for child in bendJointChildren:
                    childTx = child.tx.get()
                    if abs(childTx) > abs(self.bendJointLength):
                        self.bendJointLength = abs(childTx)


                self.pushJointLength = self.bendJointLength*0.25#*self.side

	    # rootTransform
	    if rootTransform:
		self.rootTransform = rootTransform

	    else:
		bendJointParent = self.bendJoint.getParent()
		self.rootTransform = bendJointParent

	    if rootTransformOffset:
		self.rootTransformOffset = rootTransformOffset

	    else:
		self.rootTransformOffset = [0,0,0,]

            # intersectPlaneDict
            self.intersectPlaneDict = intersectPlaneDict

            # create
            self.create()

	    if alsoCreateMirror:
		oppositeNode = ka_naming.getOppositeNode(self.bendJoint)
		if oppositeNode:
		    volumeRotator = VolumeRotator(bendJoint=oppositeNode, oppositeVolumeRotator=self, alsoCreateMirror=False)


	# volumeRotator is being passed in
	else:
	    self.volumeRotatorGrpZro = ka_pymel.getAsPyNodes(volumeRotatorGrpZro)
	    self.bendJoint = volumeRotatorGrpZro.getParent()

	    # oppositeVolumeRotator
	    if hasattr(self.volumeRotatorGrpZro, 'oppositeVolumeRotator'):
		for inputNode in self.volumeRotatorGrpZro.oppositeVolumeRotator.inputs():
		    self.oppositeVolumeRotator = VolumeRotator(inputNode)

	    else:
		self.oppositeVolumeRotator = None

	    # rootTransform
	    if rootTransform:
		self.rootTransform = rootTransform

	    else:
		bendJointParent = self.bendJoint.getParent()
		self.rootTransform = rootTransform

	    if rootTransformOffset:
		self.rootTransformOffset = rootTransformOffset

	    else:
		self.rootTransformOffset = [0,0,0,]

	    # volumeRotatePlanes
	    for child in volumeRotatorGrpZro.getChildren():
		childRigTypes = ka_advancedJoints_commands.getRigTypes(child)
		if 'volumeRotatorGrp' in childRigTypes:
		    planeName = child.baseName.get()

		    forwardPushJoint = None
		    backwardPushJoint = None
		    for subChild in child.getChildren(allDescendents=True):
			if hasattr(subChild, 'rigTypes'):
			    rigTypes = ka_advancedJoints_commands.getRigTypes(subChild)
			    if 'forwardPush_jnt' in rigTypes:
				forwardPushJoint = subChild

			    elif 'backwardPush_jnt' in rigTypes:
				backwardPushJoint = subChild

		    if planeName not in self.volumeRotatePlaneDict:
			self.volumeRotatePlaneDict[planeName] = {}
		    self.volumeRotatePlaneDict[planeName]['volumeRotatorGrp'] = child
		    self.volumeRotatePlaneDict[planeName]['forwardPush_jnt'] = forwardPushJoint
		    self.volumeRotatePlaneDict[planeName]['backwardPush_jnt'] = backwardPushJoint



		elif 'aimTargetGroup' in childRigTypes:
		    planeName = child.baseName.get()

		    if planeName not in self.volumeRotatePlaneDict:
			self.volumeRotatePlaneDict[planeName] = {}

		    self.volumeRotatePlaneDict[planeName]['aimTargetGroup'] = child


	    self.baseName = volumeRotatorGrpZro.nodeName().replace(VOLUME_ROTATOR_ZRO_NAME_SUFFIX, '')
            self.intersectPlaneDict = {}
	    for planeName in self.volumeRotatePlaneDict:
		volumeRotatePlane = self.volumeRotatePlaneDict[planeName]['volumeRotatorGrp']
		forwardPush_jnt = self.volumeRotatePlaneDict[planeName]['forwardPush_jnt']

		forwardPush_jnt = None
		for child in volumeRotatePlane.getChildren():
		    childRigTypes = ka_advancedJoints_commands.getRigTypes(child)
		    if 'forwardPush_jnt' in childRigTypes:
			forwardPush_jnt = child
			break

		offsetFromRoot = []
		for i, axis in enumerate('XYZ'):
		    offsetFromRoot.append(forwardPush_jnt.attr('backwardsOffsetT'+axis).get())

		self.intersectPlaneDict[planeName] = {}
		self.intersectPlaneDict[planeName]['planeMatrix'] = pymel.xform(volumeRotatePlane, query=True, matrix=True)
		self.intersectPlaneDict[planeName]['thickness'] = forwardPush_jnt.ty.get()
		self.intersectPlaneDict[planeName]['offsetFromRoot'] = offsetFromRoot





    #----------------------------------------------------------------------
    def printCreateCommand(self):
        """creates the volume rotator"""
	baseName = self.baseName
	bendJoint = ka_pymel.getAsStrings(self.bendJoint)

	print("%s.%s(baseName='%s', bendJoint='%s', intersectPlaneDict=%s)" % (MODULE_SHORT_NAME, self.__class__.__name__, self.baseName, bendJoint, str(self.intersectPlaneDict)))

    #----------------------------------------------------------------------
    def create(self):
        """creates the volume rotator"""

        # self.volumeRotatorGrpZro
        self.volumeRotatorGrpZro = pymel.createNode('transform')
        self.volumeRotatorGrpZro.rename(self.baseName+VOLUME_ROTATOR_ZRO_NAME_SUFFIX)
	ka_advancedJoints_commands.setRigTypes(self.volumeRotatorGrpZro, 'volumeRotatorGrpZro')
	self.volumeRotatorGrpZro.addAttr('baseName', dt='string')
	self.volumeRotatorGrpZro.baseName.set(self.baseName, lock=True)
	pymel.parent(self.volumeRotatorGrpZro, self.bendJoint)
        ka_transforms.snap(self.volumeRotatorGrpZro, self.bendJoint, t=1, r=1)


	if self.oppositeVolumeRotator:
	    self.volumeRotatorGrpZro.addAttr('oppositeVolumeRotator', at='message')
	    self.oppositeVolumeRotator.volumeRotatorGrpZro.message >> self.volumeRotatorGrpZro.oppositeVolumeRotator

        ## self.aimTargetGroup
        #self.aimTargetGroup = pymel.createNode('transform')
        #self.aimTargetGroup.rename(self.baseName+'_aimTarget_grp')
	#ka_advancedJoints_commands.setRigTypes(self.aimTargetGroup, 'aimTargetGroup')
        #pymel.parent(self.aimTargetGroup, self.volumeRotatorGrpZro)
        #if not rootTransform:
            #bendJointParent = self.bendJoint.getParent()
            #if bendJointParent:
                #if not rootTransformOffset:
                    #rootTransformOffset = [0,0,0]

                #parentConstraint = pymel.parentConstraint(bendJointParent, self.aimTargetGroup, maintainOffset=False)
                #parentConstraint.target[0].targetOffsetTranslate.set(rootTransformOffset)


        if not self.intersectPlaneDict:
	    defaultThickness = self.bendJoint.radius.get() * 1.33
            self.intersectPlaneDict = {'posY':{'planeMatrix':[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
	                                       'thickness': defaultThickness,
	                                       'offsetFromRoot':[0,0,0],
                                              },

                                       'negY':{'planeMatrix': [1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, -0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
	                                       'thickness': defaultThickness,
	                                       'offsetFromRoot':[0,0,0],

                                              },

                                       'posZ':{'planeMatrix':[1.0, 0.0, 0.0, 0.0, 0.0, -0.0, 1.0, 0.0, 0.0, -1.0, -0.0, 0.0, 0.0, 0.0,  0.0, 1.0],
	                                       'thickness': defaultThickness,
	                                       'offsetFromRoot':[0,0,0],
                                              },

                                       'negZ':{'planeMatrix':[ 1.0, 0.0, 0.0, 0.0, 0.0, -0.0, -1.0, 0.0, 0.0, 1.0, -0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
	                                       'thickness': defaultThickness,
	                                       'offsetFromRoot':[0,0,0],
                                              },
                                      }
	    #if self.side == -1:
		#posZMat = list(self.intersectPlaneDict['posZ']['planeMatrix'])
		#negZMat = list(self.intersectPlaneDict['negZ']['planeMatrix'])

		#self.intersectPlaneDict['posZ']['planeMatrix'] = negZMat
		#self.intersectPlaneDict['negZ']['planeMatrix'] = posZMat

        for planeName in self.intersectPlaneDict:
            self.createVolumeRotatePlane(planeName=planeName)


    def createVolumeRotatePlane(self, planeName='',):
	self.volumeRotatePlaneDict[planeName] = {}
        planeBaseName = self.baseName+'_'+planeName
	planeDict = self.intersectPlaneDict[planeName]

        # volumeRotatorGrp
        #volumeRotatorGrp = pymel.createNode('transform')
	volumeRotatorGrpShape = pymel.createNode('locator')
        volumeRotatorGrp = volumeRotatorGrpShape.getParent()
        volumeRotatorGrp.rename(planeBaseName+'_volumeRotator_grp')
	ka_advancedJoints_commands.setRigTypes(volumeRotatorGrp, 'volumeRotatorGrp')
	volumeRotatorGrp.addAttr('baseName', dt='string')
	volumeRotatorGrp.baseName.set(planeName, lock=True)
        pymel.parent(volumeRotatorGrp, self.volumeRotatorGrpZro)
	ka_transforms.snap(volumeRotatorGrp, self.volumeRotatorGrpZro, t=1, r=1)

	self.volumeRotatePlaneDict[planeName]['volumeRotatorGrp'] = volumeRotatorGrp

        # aimTargetGroup
        aimTargetGroup = pymel.createNode('transform')
        aimTargetGroup.rename(planeBaseName+'_aimTarget_grp')
	ka_advancedJoints_commands.setRigTypes(aimTargetGroup, 'aimTargetGroup')
	aimTargetGroup.addAttr('baseName', dt='string')
	aimTargetGroup.baseName.set(planeName, lock=True)
        pymel.parent(aimTargetGroup, self.volumeRotatorGrpZro)
	aimTargetGroup_parentConstraint = pymel.parentConstraint(self.rootTransform, aimTargetGroup, maintainOffset=False)

	self.volumeRotatePlaneDict[planeName]['aimTargetGroup'] = aimTargetGroup

        # aimGroup
        #aimGroup = pymel.createNode('transform')
	aimGroupShape = pymel.createNode('locator')
        aimGroup = aimGroupShape.getParent()
        aimGroup.rename(planeBaseName+'_aim_grp')
        pymel.parent(aimGroup, volumeRotatorGrp)
        ka_transforms.snap(aimGroup, self.volumeRotatorGrpZro, t=1)
        aimConstraint = pymel.aimConstraint(aimTargetGroup, aimGroup, worldUpType='objectrotation', worldUpObject=volumeRotatorGrp, aimVector=[-1*self.side, 0, 0], worldUpVector=[0,0,1], upVector=[0,0,1], maintainOffset=False)


        rootVectorX_vectorProduct = pymel.createNode('vectorProduct')
        volumeRotatorGrp.rename(planeBaseName+VOLUME_ROTATOR_NAME_SUFFIX)
        rootVectorX_vectorProduct.operation.set(3)
        rootVectorX_vectorProduct.normalizeOutput.set(1)
        rootVectorX_vectorProduct.input1.set(1,0,0)
        aimTargetGroup.translate >> rootVectorX_vectorProduct.input1
        volumeRotatorGrp.inverseMatrix >> rootVectorX_vectorProduct.matrix

        dotOfvectorXY_vectorProduct = pymel.createNode('vectorProduct')
        dotOfvectorXY_vectorProduct.operation.set(2)
        dotOfvectorXY_vectorProduct.input1.set(0,1,0)
        rootVectorX_vectorProduct.output >> dotOfvectorXY_vectorProduct.input2

        dotOfvectorXZ_vectorProduct = pymel.createNode('vectorProduct')
        dotOfvectorXZ_vectorProduct.operation.set(2)
        dotOfvectorXZ_vectorProduct.input1.set(0,0,1)
        rootVectorX_vectorProduct.output >> dotOfvectorXZ_vectorProduct.input2

	keyPairs = [
	[1.0, -1.0],
	[0.0, 0.0],
	[1.0, 1.0],
	]
        invertZ_setDriven = pymel.createNode('animCurveUU', )
	invertY_setDriven = pymel.createNode('animCurveUU', )

	for keyNode in [invertZ_setDriven, invertY_setDriven]:
	    for i, pair in enumerate(keyPairs):
		pymel.setKeyframe(keyNode, value=pair[0], float=pair[1])

		keyNode.keyTanInType[i].set(2)
		keyNode.keyTanOutType[i].set(2)
		keyNode.keyTanLocked[i].set(False)

	    keyNode.tangentType.set(2)
	    keyNode.weightedTangents.set(False)


        dotOfvectorXY_vectorProduct.outputX >> invertY_setDriven.input
        dotOfvectorXZ_vectorProduct.outputX >> invertZ_setDriven.input

	# connect to aim
        invertY_setDriven.output >> aimConstraint.upVectorY
        invertY_setDriven.output >> aimConstraint.worldUpVectorY

        invertZ_setDriven.output >> aimConstraint.upVectorZ
        invertZ_setDriven.output >> aimConstraint.worldUpVectorZ



        # halfRotateGrp
        halfRotateGrp = pymel.createNode('transform')
        halfRotateGrp.rename(planeBaseName+'_halfRotate_grp')
        pymel.parent(halfRotateGrp, volumeRotatorGrp)
        ka_transforms.snap(halfRotateGrp, self.volumeRotatorGrpZro, t=1)
        orientConstraint = pymel.orientConstraint(volumeRotatorGrp, aimGroup, halfRotateGrp)
        orientConstraint.interpType.set(2)


        # forward push joint
	forwardPushJoint = pymel.createNode('joint')
	forwardPushJoint.rename('%s_forwardPush_jnt' % planeBaseName)
	ka_advancedJoints_commands.setRigTypes(forwardPushJoint, 'forwardPush_jnt')
	self.volumeRotatePlaneDict[planeName]['forwardPush_jnt'] = forwardPushJoint

	pymel.parent(forwardPushJoint, volumeRotatorGrp)
	forwardPushJoint.radius.set(self.pushJointRadius)
	forwardPushJoint.overrideEnabled.set(1)
	forwardPushJoint.overrideColor.set(25)

	forwardPushJointEnd = pymel.createNode('joint')
	forwardPushJointEnd.rename('%s_forwardPushEnd_jnt' % planeBaseName)
	pymel.parent(forwardPushJointEnd, forwardPushJoint)
	forwardPushJointEnd.radius.set(self.pushJointRadius*0.275)
	forwardPushJointEnd.t.set(self.pushJointLength*self.side, 0, 0)
	forwardPushJointEnd.v.set(0)

	ka_transforms.snap(forwardPushJoint, self.volumeRotatorGrpZro, t=1, r=1)
	forwardPushJoint.r.set(0,0,0)
	forwardPushJoint.jointOrient.set(0,0,0)
	forwardPushJoint.t.set(0, planeDict['thickness'], 0)


	backwardPushJoint = pymel.createNode('joint')
	backwardPushJoint.rename('%s_backwardPush_jnt' % planeBaseName)
	ka_advancedJoints_commands.setRigTypes(backwardPushJoint, 'backwardPush_jnt')
	self.volumeRotatePlaneDict[planeName]['backwardPush_jnt'] = backwardPushJoint

	pymel.parent(backwardPushJoint, aimGroup)
	backwardPushJoint.radius.set(self.pushJointRadius)
	backwardPushJoint.overrideEnabled.set(1)
	backwardPushJoint.overrideColor.set(27)

	backwardPushJointEnd = pymel.createNode('joint')
	backwardPushJointEnd.rename('%s_backwardPushEnd_jnt' % planeBaseName)
	pymel.parent(backwardPushJointEnd, backwardPushJoint)
	backwardPushJointEnd.radius.set(self.pushJointRadius*0.25)
	backwardPushJointEnd.t.set(self.pushJointLength*self.side*-1, 0, 0)
	backwardPushJointEnd.v.set(0)

	ka_transforms.snap(backwardPushJoint, aimGroup, t=1, r=1)
	backwardPushJoint.r.set(0,0,0)
	backwardPushJoint.jointOrient.set(0,0,0)
	forwardPushJoint.ty >> backwardPushJoint.ty



	# lock attrs
	forwardPushJoint.tz.set(lock=True, keyable=False, channelBox=False)
	forwardPushJoint.rx.set(lock=True, keyable=False, channelBox=False)
	forwardPushJoint.ry.set(lock=True, keyable=False, channelBox=False)
	forwardPushJoint.rz.set(lock=True, keyable=False, channelBox=False)
	forwardPushJoint.sx.set(lock=True, keyable=False, channelBox=False)
	forwardPushJoint.sy.set(lock=True, keyable=False, channelBox=False)
	forwardPushJoint.sz.set(lock=True, keyable=False, channelBox=False)
	forwardPushJoint.v.set(lock=True, keyable=False, channelBox=False)

	backwardPushJoint.tz.set(lock=True, keyable=False, channelBox=False)
	backwardPushJoint.rx.set(lock=True, keyable=False, channelBox=False)
	backwardPushJoint.ry.set(lock=True, keyable=False, channelBox=False)
	backwardPushJoint.rz.set(lock=True, keyable=False, channelBox=False)
	backwardPushJoint.sx.set(lock=True, keyable=False, channelBox=False)
	backwardPushJoint.sy.set(lock=True, keyable=False, channelBox=False)
	backwardPushJoint.sz.set(lock=True, keyable=False, channelBox=False)
	backwardPushJoint.v.set(lock=True, keyable=False, channelBox=False)


	# Intersection Nodes ---------------------------------------------------------------
	#   aim group vector products
	outerConcaveEdge_vectorProduct = pymel.createNode('vectorProduct')
	outerConcaveEdge_vectorProduct.rename(planeBaseName+'outerConcaveEdge_vectorProduct')
	outerConcaveEdge_vectorProduct.input1.input1X.set(-1.0)
	outerConcaveEdge_vectorProduct.operation.set(3)
	forwardPushJoint.ty >> outerConcaveEdge_vectorProduct.input1Y
	aimGroup.matrix >> outerConcaveEdge_vectorProduct.matrix

	innerConcaveEdge_vectorProduct = pymel.createNode('vectorProduct', )
	innerConcaveEdge_vectorProduct.rename(planeBaseName+'innerConcaveEdge_vectorProduct')
	innerConcaveEdge_vectorProduct.input1.input1X.set(-1.0)
	innerConcaveEdge_vectorProduct.operation.set(3)
	aimGroup.matrix >> innerConcaveEdge_vectorProduct.matrix


	# offset_plusMinusAverageA
	offset_plusMinusAverageA = pymel.createNode('plusMinusAverage')
	offset_plusMinusAverageA.rename(planeBaseName+'offset_plusMinusAverageA')
	offset_plusMinusAverageA.operation.set(2)
	outerConcaveEdge_vectorProduct.outputY >> offset_plusMinusAverageA.input1D[0]
	forwardPushJoint.ty >> offset_plusMinusAverageA.input1D[1]


	# vectorXDotProduct
	vectorXDotProduct = pymel.createNode('vectorProduct', )
	vectorXDotProduct.rename(planeBaseName+'vectorXDotProduct')
	vectorXDotProduct.input2.set(1, 0, 0,)
	innerConcaveEdge_vectorProduct.output >> vectorXDotProduct.input1

	# slopeRatioKeyframe
	slopeRatioKeyframe = pymel.createNode('animCurveUU', )
	slopeRatioKeyframe.rename(planeBaseName+'slopeRatioKeyframe')

	keyPairs = [
	[0.00066144208469, -1.0],
	[-6.31309055792, -0.987688362598],
	[-3.57214055792, -0.962688326836],
	[-2.705, -0.938],
	[-2.166, -0.908],
	[-1.83183855792, -0.877689123154],
	[-1.42136855792, -0.81768989563],
	[-0.973906557915, -0.697691440582],
	[-0.514893, -0.457694470882],
	[-0.223052, -0.217697530985],
	[-0.0981849, -0.0976990610361],
	[-0.0377371, -0.0376998260617],
	[-0.00770401, -0.00770020857453],
	[0.0223104, 0.0222994089127],
	[0.271921, 0.262296378613],
	[0.4139, 0.382294863462],
	[0.493372, 0.442294120789],
	[0.536047, 0.47229373455],
	[0.5811, 0.502293348312],
	[0.795428, 0.62229180336],
	[0.933485, 0.682291030884],
	[1.015387, 0.712290644646],
	[1.108611, 0.742290258408],
	[1.345284, 0.802289485931],
	[1.502951, 0.832289099693],
	[1.703636, 0.862288713455],
	[1.977682, 0.892288327217],
	[2.39188, 0.922287940979],
	[3.126238, 0.952287554741],
	[4.55, 0.982],
	[10.325, 1.0],
	]

	for i, pair in enumerate(keyPairs):
	    pymel.setKeyframe(slopeRatioKeyframe, value=pair[0], float=pair[1])

	    slopeRatioKeyframe.keyTanInType[i].set(2)
	    slopeRatioKeyframe.keyTanOutType[i].set(2)
	    slopeRatioKeyframe.keyTanLocked[i].set(False)

	slopeRatioKeyframe.tangentType.set(2)
	slopeRatioKeyframe.weightedTangents.set(False)

	vectorXDotProduct.outputX >> slopeRatioKeyframe.input


	# slopeMultiplier
	slopeMultiplier = pymel.createNode('multiplyDivide', )
	slopeMultiplier.rename(planeBaseName+'slopeMultiplier')
	slopeRatioKeyframe.output >> slopeMultiplier.input1X
	offset_plusMinusAverageA.output1D >> slopeMultiplier.input2X

	#  offset_plusMinusAverageB
	offset_plusMinusAverageB = pymel.createNode('plusMinusAverage', )
	offset_plusMinusAverageB.rename(planeBaseName+'offset_plusMinusAverageB')
	offset_plusMinusAverageB.operation.set(2)
	outerConcaveEdge_vectorProduct.outputX >> offset_plusMinusAverageB.input1D[0]
	slopeMultiplier.outputX >> offset_plusMinusAverageB.input1D[1]

	# aimSpace_vectorProduct
	aimSpace_vectorProduct = pymel.createNode('vectorProduct', )
	aimSpace_vectorProduct.rename(planeBaseName+'aimSpace_vectorProduct')
	aimSpace_vectorProduct.operation.set(4)
	forwardPushJoint.ty >> aimSpace_vectorProduct.input1.input1Y
	offset_plusMinusAverageB.output1D >> aimSpace_vectorProduct.input1.input1X
	aimGroup.inverseMatrix >> aimSpace_vectorProduct.matrix

	# concaveConvexBlend_keyframeY
	concaveConvexBlend_keyframeY = pymel.createNode('animCurveUU', )
	concaveConvexBlend_keyframeY.rename(planeBaseName+'concaveConvexBlend_keyframeY')
	keyPairs = [
	[0.0, -1.0],
	[0.0, 0.0],
	[1.0, 0.2],
	[1.0, 1.0],
	]

	for i, pair in enumerate(keyPairs):
	    pymel.setKeyframe(concaveConvexBlend_keyframeY, value=pair[0], float=pair[1])

	    concaveConvexBlend_keyframeY.keyTanInType[i].set(2)
	    concaveConvexBlend_keyframeY.keyTanOutType[i].set(2)
	    concaveConvexBlend_keyframeY.keyTanLocked[i].set(False)

	concaveConvexBlend_keyframeY.tangentType.set(2)
	concaveConvexBlend_keyframeY.weightedTangents.set(False)

	innerConcaveEdge_vectorProduct.outputY >> concaveConvexBlend_keyframeY.input


	# concaveConvexBlend_keyframeX
	concaveConvexBlend_keyframeX = pymel.createNode('animCurveUU', )
	concaveConvexBlend_keyframeX.rename(planeBaseName+'concaveConvexBlend_keyframeX')
	keyPairs = [
	[0.0, -1.0],
	[1.0, -0.8],
	[1.0, 0.8],
	[0.0, 1.0],
	]

	for i, pair in enumerate(keyPairs):
	    pymel.setKeyframe(concaveConvexBlend_keyframeX, value=pair[0], float=pair[1])

	    concaveConvexBlend_keyframeX.keyTanInType[i].set(2)
	    concaveConvexBlend_keyframeX.keyTanOutType[i].set(2)
	    concaveConvexBlend_keyframeX.keyTanLocked[i].set(False)

	concaveConvexBlend_keyframeX.tangentType.set(2)
	concaveConvexBlend_keyframeX.weightedTangents.set(False)

	innerConcaveEdge_vectorProduct.outputX >> concaveConvexBlend_keyframeX.input


	# convexConcaveBlendY
	convexConcaveBlendY = pymel.createNode('blendColors', )
	convexConcaveBlendY.rename(planeBaseName+'convexConcaveBlendY')
	convexConcaveBlendY.color1R.set(1.0)
	convexConcaveBlendY.color2R.set(0.0)
	concaveConvexBlend_keyframeY.output >> convexConcaveBlendY.blender

	# convexConcaveBlendX
	convexConcaveBlendX = pymel.createNode('blendColors', )
	convexConcaveBlendX.rename(planeBaseName+'convexConcaveBlendX')
	convexConcaveBlendX.color2R.set(0.0)
	concaveConvexBlend_keyframeX.output >> convexConcaveBlendX.blender
	convexConcaveBlendY.outputR >> convexConcaveBlendX.color1R


	## convexConcaveBlendConditionA
	#convexConcaveBlendConditionA = pymel.createNode('condition', )
	#convexConcaveBlendConditionA.rename(planeBaseName+'convexConcaveBlendConditionA')
	#convexConcaveBlendConditionA.operation.set(4)
	#convexConcaveBlendConditionA.colorIfFalseR.set(1.0)
	#concaveConvexBlend_keyframe.output >> convexConcaveBlendConditionA.colorIfTrueR
	#innerConcaveEdge_vectorProduct.outputX >> convexConcaveBlendConditionA.firstTerm

	## convexConcaveBlendConditionB
	#convexConcaveBlendConditionB = pymel.createNode('condition', )
	#convexConcaveBlendConditionB.rename(planeBaseName+'convexConcaveBlendConditionB')
	#convexConcaveBlendConditionB.operation.set(2)
	#convexConcaveBlendConditionB.colorIfFalseR.set(0.0)
	#convexConcaveBlendConditionA.outColorR >> convexConcaveBlendConditionB.colorIfTrueR
	#innerConcaveEdge_vectorProduct.outputY >> convexConcaveBlendConditionB.firstTerm


	# concaveInputTxInverter
	concaveInputTxInverter = pymel.createNode('multiplyDivide', )
	concaveInputTxInverter.rename(planeBaseName+'concaveInputTxInverter')
	concaveInputTxInverter.input2X.set(-1)
	aimSpace_vectorProduct.outputX >> concaveInputTxInverter.input1X


	# Convex Bend Nodes ---------------------------------------------------------------
	#   halfRotateGrpInLocalSpace_vectorProduct
	halfRotateGrpInLocalSpace_vectorProduct = pymel.createNode('vectorProduct', )
	halfRotateGrpInLocalSpace_vectorProduct.rename(planeBaseName+'halfRotateGrpInLocalSpace_vectorProduct')
	halfRotateGrpInLocalSpace_vectorProduct.operation.set(4)
	halfRotateGrp.matrix >> halfRotateGrpInLocalSpace_vectorProduct.matrix
	forwardPushJoint.ty >> halfRotateGrpInLocalSpace_vectorProduct.input1Y


	# Convex Concave BendColors Node ---------------------------------------------------------------
	#   convexConcaveBlendColor
	convexConcaveBlendColor = pymel.createNode('blendColors', )
	convexConcaveBlendColor.rename(planeBaseName+'convexConcaveBlendColor')

	concaveInputTxInverter.outputX >> convexConcaveBlendColor.color1R
	halfRotateGrpInLocalSpace_vectorProduct.outputX >> convexConcaveBlendColor.color2R
	#convexConcaveBlendConditionB.outColorR >> convexConcaveBlendColor.blender
	convexConcaveBlendX.outputR >> convexConcaveBlendColor.blender

	convexConcaveBlendColor.outputR >> forwardPushJoint.tx

	# inputTxInverter
	inputTxInverter = pymel.createNode('multiplyDivide', )
	inputTxInverter.rename(planeBaseName+'concaveInputTxInverter')
	inputTxInverter.input2X.set(-1)
	convexConcaveBlendColor.outputR >> inputTxInverter.input1X

	inputTxInverter.outputX >> backwardPushJoint.tx

	# position rotate group
	pymel.xform(volumeRotatorGrp, matrix=planeDict['planeMatrix'], objectSpace=True)


	# create offset attributes
	for i, attrName in enumerate(['backwardsOffsetTX', 'backwardsOffsetTY', 'backwardsOffsetTZ',]):
	    forwardPushJoint.addAttr(attrName, keyable=False)
	    forwardPushJoint.attr(attrName).set(self.intersectPlaneDict[planeName]['offsetFromRoot'][i], channelBox=True)


	for i, attrName in enumerate(['forwardsOffsetRX', 'forwardsOffsetRY', 'forwardsOffsetRZ', ]):
	    forwardPushJoint.addAttr(attrName, at='doubleAngle', keyable=False)
	    forwardPushJoint.attr(attrName).set(volumeRotatorGrp.attr('r'+'xyz'[i]).get(), channelBox=True)

	forwardPushJoint.backwardsOffsetTX >> aimTargetGroup_parentConstraint.target[0].targetOffsetTranslate.targetOffsetTranslateX
	forwardPushJoint.backwardsOffsetTY >> aimTargetGroup_parentConstraint.target[0].targetOffsetTranslate.targetOffsetTranslateY
	forwardPushJoint.backwardsOffsetTZ >> aimTargetGroup_parentConstraint.target[0].targetOffsetTranslate.targetOffsetTranslateZ

	forwardPushJoint.forwardsOffsetRX >> volumeRotatorGrp.rx
	forwardPushJoint.forwardsOffsetRY >> volumeRotatorGrp.ry
	forwardPushJoint.forwardsOffsetRZ >> volumeRotatorGrp.rz

	# hook up visualizer locators
	visualiserLocator_mutliplyDivide = pymel.createNode('multiplyDivide', )
	visualiserLocator_mutliplyDivide.rename(planeBaseName+'visualiserLocator_mutliplyDivide')
	visualiserLocator_mutliplyDivide.input2X.set(0.8)
	visualiserLocator_mutliplyDivide.input2Y.set(0.8)

	volumeRotatorGrpShape.localScaleY.set(0)
	volumeRotatorGrpShape.localScaleZ.set(0)
	volumeRotatorGrpShape.overrideEnabled.set(1)
	volumeRotatorGrpShape.overrideDisplayType.set(2)

	aimGroupShape.localScaleY.set(0)
	aimGroupShape.localScaleZ.set(0)
	aimGroupShape.overrideEnabled.set(1)
	aimGroupShape.overrideDisplayType.set(2)

	forwardPushJoint.addAttr('offsetLocatorVis', at='bool', keyable=False)
	forwardPushJoint.offsetLocatorVis.set(0.0, channelBox=True)
	forwardPushJoint.offsetLocatorVis >> volumeRotatorGrpShape.v
	forwardPushJoint.offsetLocatorVis >> aimGroupShape.v

	forwardPushJointEnd.tx >> visualiserLocator_mutliplyDivide.input1X
	visualiserLocator_mutliplyDivide.outputX >> volumeRotatorGrpShape.localPositionX
	visualiserLocator_mutliplyDivide.outputX >> volumeRotatorGrpShape.localScaleX

	backwardPushJointEnd.tx >> visualiserLocator_mutliplyDivide.input1Y
	visualiserLocator_mutliplyDivide.outputY >> aimGroupShape.localPositionX
	visualiserLocator_mutliplyDivide.outputY >> aimGroupShape.localScaleX

	forwardPushJoint.ty >> volumeRotatorGrpShape.localPositionY
	forwardPushJoint.ty >> aimGroupShape.localPositionY



	# connect mirrored to opposite if this node is a mirror
	if self.oppositeVolumeRotator:

	    # inputTyInverterA
	    inputTyInverterA = pymel.createNode('multiplyDivide', )
	    inputTyInverterA.rename(planeBaseName+'inputTyInverterA')
	    inputTyInverterA.input2X.set(-1)

	    # inputbackwardOffsetInverter
	    inputBackwardOffsetInverter = pymel.createNode('multiplyDivide', )
	    inputBackwardOffsetInverter.rename(planeBaseName+'inputTyInverterB')
	    inputBackwardOffsetInverter.input2.set(-1,-1,-1)

	    # inputForwardOffsetInverter
	    inputForwardOffsetInverter = pymel.createNode('multiplyDivide', )
	    inputForwardOffsetInverter.rename(planeBaseName+'inputTyInverterC')
	    inputForwardOffsetInverter.input2.set(1,1,1)


	    oppositeVolumeRotatorGrp = self.oppositeVolumeRotator.volumeRotatePlaneDict[planeName]['volumeRotatorGrp']
	    oppositeForwardPushJoint = self.oppositeVolumeRotator.volumeRotatePlaneDict[planeName]['forwardPush_jnt']
	    oppositeBackwardPushJoint = self.oppositeVolumeRotator.volumeRotatePlaneDict[planeName]['backwardPush_jnt']
	    oppositeAimTargetGroup = self.oppositeVolumeRotator.volumeRotatePlaneDict[planeName]['aimTargetGroup']

	    # mirror forwardPushJointTY
	    oppositeForwardPushJoint.ty >> inputTyInverterA.input1X
	    inputTyInverterA.outputX >> forwardPushJoint.ty

	    # mirror backwardsOffsetT
	    oppositeForwardPushJoint.backwardsOffsetTX >> inputBackwardOffsetInverter.input1X
	    oppositeForwardPushJoint.backwardsOffsetTY >> inputBackwardOffsetInverter.input1Y
	    oppositeForwardPushJoint.backwardsOffsetTZ >> inputBackwardOffsetInverter.input1Z

	    inputBackwardOffsetInverter.outputX >> forwardPushJoint.backwardsOffsetTX
	    inputBackwardOffsetInverter.outputY >> forwardPushJoint.backwardsOffsetTY
	    inputBackwardOffsetInverter.outputZ >> forwardPushJoint.backwardsOffsetTZ

	    # mirror forwardsOffsetR
	    oppositeForwardPushJoint.forwardsOffsetRX >> inputForwardOffsetInverter.input1X
	    oppositeForwardPushJoint.forwardsOffsetRY >> inputForwardOffsetInverter.input1Y
	    oppositeForwardPushJoint.forwardsOffsetRZ >> inputForwardOffsetInverter.input1Z

	    inputForwardOffsetInverter.outputX >> forwardPushJoint.forwardsOffsetRX
	    inputForwardOffsetInverter.outputY >> forwardPushJoint.forwardsOffsetRY
	    inputForwardOffsetInverter.outputZ >> forwardPushJoint.forwardsOffsetRZ


	    #oppositeVolumeRotatorGrp.t >> inputAimTranslateOffsetInverter.input1
	    #inputAimTranslateOffsetInverter.output >> volumeRotatorGrp.t
	    #oppositeVolumeRotatorGrp.r >> volumeRotatorGrp.r

	    #oppositeAimTargetGroup.t >> inputTyInverterC.input1

	    ##inputTyInverterC.output >> aimTargetGroup.t
	    ##oppositeAimTargetGroup.r >> aimTargetGroup.r

	    #inputTyInverterC.output >> aimTargetGroup.t

