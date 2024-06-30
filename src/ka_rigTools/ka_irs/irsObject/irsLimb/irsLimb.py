#====================================================================================
#====================================================================================
#
# irsLimb
#
# DESCRIPTION:
#   a limb object representing a limb of a creautre
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


import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_python as ka_python
import ka_rigTools.ka_controls as ka_controls
import ka_rigTools.ka_attr as ka_attr

import ka_rigTools.ka_irs.irsObject.irsObject as irsObject

MODE_LABEL = 'mode' # variable to change if you want the the attributes named diffrently
SPACE_LABEL = 'label' # variable to change if you want the the attributes named diffrently


class IrsLimb(irsObject.IrsObject):

    def __init__(self, root=None, **kwargs):
        return self.__init__IrsLimb__(root=root, **kwargs)

    def __init__IrsLimb__(self, root=None, **kwargs):

        # modify kwargs -----------------------------------
        kwargs['name'] = kwargs.get('name', 'defaultLimbName')

        # init superClass -----------------------------------
        self.__init__irsObject__(root, **kwargs)

        # set object variables -----------------------------------
        self.switchControl = None
        self.defaultTransforms = None
        self.outputTransforms = []
        self.outputTransformParentConstraints = None

        self.defaultXforms = []
        self.outputXforms = []
        self.drivingXforms = []

        self._lastLimbJointCreated = None

        # make feature dict
        self.featureDict = {}
        for featureClass in self.features:
            self.featureDict[featureClass.featureLabel] = {}
            self.featureDict[featureClass.featureLabel]['slot'] = featureClass.featureSlot
            self.featureDict[featureClass.featureLabel]['class'] = featureClass





    def addFeature(self, featureName):
        feature = self.featureDict[featureName]['class'](irsLimb=self, name=self.baseName, parent=self.root,
                                                         side=self.side)

    #def createLimbXforms(self, name, numberOfXforms, matrices=None, parentName=None, makeDrivingXform=True):
        #pass

    #def createLimbXform(self, name, index='', parentName=None, matrix=None, makeDrivingXform=True,):
        #"""
        #"""

        ## defaultXform --------------------------------------------------------------------------------------
        ##   choose parent
        #if parentName == None:
            #if self.defaultXforms:
                #parent = self.defaultXforms[-1]
            #else:
                #parent = self.root
        #else:
            #parent = getattr(self, 'defaultXform_%s' % parentName)

        #attrName = 'defaultXform_%s'% name
        #defaultXform = pymel.createNode('joint')
        #self.setName(defaultXform, attrName, side=self.side, index=index)
        #defaultXform.jointOrient.set([0,0,0], lock=True)
        #defaultXform.setParent(parent)
        #defaultXform.v.set(0)
        #self.defaultXforms.append(defaultXform)

        #if index != '':
            #if hasattr(self, attrName):
                #getattr(self, attrName).append(defaultXform)
            #else:
                #setattr(self, attrName, [defaultXform])
        #else:
            #setattr(self, attrName, defaultXform)

        #self.defaultXforms.append(defaultXform)

        ## outputXform --------------------------------------------------------------------------------------
        ##   choose parent
        #if parentName == None:
            #if self.defaultXforms:
                #parent = self.defaultXforms[-1]
            #else:
                #parent = self.root
        #else:
            #parent = getattr(self, 'outputXform_%s' % parentName)

        ## create node
        #attrName = 'outputXform_%s'% name
        #outputXform = pymel.createNode('joint')
        #self.setName(outputXform, attrName, side=self.side, index=index)
        #outputXform.jointOrient.set([0,0,0], lock=True)
        #outputXform.setParent(parent)
        #self.outputXforms.append(outputXform)


        #if index != '':
            #if hasattr(self, attrName):
                #getattr(self, attrName).append(outputXform)
            #else:
                #setattr(self, attrName, [outputXform])
        #else:
            #setattr(self, attrName, outputXform)

        #if matrix:
            #pymel.xform(outputXform, matrix=matrix, worldSpace=True)

        ## drivingXform --------------------------------------------------------------------------------------
        #if makeDrivingXform:
            ## choose parent
            #if parentName == None:
                #if self.defaultXforms:
                    #parent = self.defaultXforms[-1]
                #else:
                    #parent = self.root
            #else:
                #parent = getattr(self, 'drivingXform_%s' % parentName)

            ## create node
            #attrName = 'drivingXform_%s'% name
            #drivingXform = pymel.createNode('joint')
            #self.setName(drivingXform, attrName, side=self.side, index=index)
            #drivingXform.jointOrient.set([0,0,0], lock=True)
            #drivingXform.setParent(parent)
            #drivingXform.drawStyle.set(2)
            #self.drivingXforms.append(drivingXform)

            #if index != '':
                #if hasattr(self, attrName):
                    #getattr(self, attrName).append(drivingXform)
                #else:
                    #setattr(self, attrName, [drivingXform])
            #else:
                #setattr(self, attrName, drivingXform)
            #self.defaultXforms.append(drivingXform)

            #if matrix:
                #pymel.xform(drivingXform, matrix=matrix, worldSpace=True)


    def connectToOutputTransform(self, node, parentConstraint, index):
            node.rotate >> parentConstraint.target[index].targetRotate
            node.rotateOrder >> parentConstraint.target[index].targetRotateOrder
            node.parentMatrix[index] >> parentConstraint.target[index].targetParentMatrix
            node.rotatePivotTranslate >> parentConstraint.target[index].targetRotateTranslate
            node.rotatePivot >> parentConstraint.target[index].targetRotatePivot
            node.scale >> parentConstraint.target[index].targetScale
            node.translate >> parentConstraint.target[index].targetTranslate

            if hasattr(node, 'jointOrient'):
                node.jointOrient >> parentConstraint.target[index].targetJointOrient


    def createSwitchControl(self, modes=[], spaces=[]):
        self.switchControl = ka_controls.createControlStack('switches', sizeOfStack=1, shape='wrench', side=self.side)[0]

        # modes
        enumString = ':'.join(modes)
        ka_attr.addHeaderAttr(self.switchControl, 'MODE_SWITCHS')
        self.switchControl.addAttr('%sA' % MODE_LABEL, at='enum', enumName=enumString, keyable=True)
        self.switchControl.addAttr('%sB'% MODE_LABEL, at='enum', enumName=enumString, defaultValue=1, keyable=True)
        self.switchControl.addAttr('%sBlend' % MODE_LABEL, maxValue=1.0, minValue=0.0, keyable=True)

        ka_attr.addHeaderAttr(self.switchControl, 'MISC_SWITCHS')

        return self.switchControl

    def getModeIndex(self, mode):
        if isinstance(mode, int):
            return mode

        else:
            enumDict = self.switchControl.attr('%sA' % MODE_LABEL).getEnums()
            return enumDict[mode]


    def driveJoint(self, driverTransform, drivenTransform, mode):
        orientConstraints = drivenTransform.rx.inputs(type='orientConstraint')
        pointConstraints = drivenTransform.tx.inputs(type='pointConstraint')

        if orientConstraints:
            orientConstraint = orientConstraints[0]
            pointConstraint = pointConstraints[0]

        else:
            orientConstraint = pymel.createNode('orientConstraint')
            orientConstraint.rename(drivenTransform.nodeName()+'driving_orientConstraint')
            orientConstraint.setParent(drivenTransform)

            drivenTransform.parentInverseMatrix[0] >> orientConstraint.constraintParentInverseMatrix
            drivenTransform.rotateOrder >> orientConstraint.constraintRotateOrder

            orientConstraint.constraintRotateX >> drivenTransform.rx
            orientConstraint.constraintRotateY >> drivenTransform.ry
            orientConstraint.constraintRotateZ >> drivenTransform.rz

            pointConstraint = pymel.createNode('pointConstraint')
            pointConstraint.rename(drivenTransform.nodeName()+'driving_pointConstraint')
            pointConstraint.setParent(drivenTransform)

            pointConstraint.constraintTranslateX >> drivenTransform.tx
            pointConstraint.constraintTranslateY >> drivenTransform.ty
            pointConstraint.constraintTranslateZ >> drivenTransform.tz


        modeIndex = self.getModeIndex(mode)
        driverTransform.parentMatrix[0] >> orientConstraint.target[modeIndex].targetParentMatrix
        driverTransform.rotateOrder >> orientConstraint.target[modeIndex].targetRotateOrder
        driverTransform.rotate >> orientConstraint.target[modeIndex].targetRotate

        driverTransform.translate >> pointConstraint.target[modeIndex].targetTranslate

        modeBlender = self._getModeBlenderForInput(modeIndex)
        modeBlender.outputR >> orientConstraint.target[modeIndex].targetWeight
        modeBlender.outputR >> pointConstraint.target[modeIndex].targetWeight


    def driveVisibility(self, node, mode):
        modeIndex = self.getModeIndex(mode)

        visibilityCondition = self._getVisibilityConditionForMode(modeIndex)
        visibilityCondition.outColorR >> node.v

    def _getVisibilityConditionForMode(self, inputIndex):
        attrName = 'visibilityCondition_'+str(inputIndex)
        if hasattr(self.switchControl, attrName):
            return self.switchControl.attr(attrName).inputs()[0]

        else:
            return self._createVisibilityConditionForMode(inputIndex)

    def _createVisibilityConditionForMode(self, inputIndex):
        visibilityCondition = pymel.createNode('condition')
        visibilityCondition.operation.set(0)

        modeBlender = self._getModeBlenderForInput(inputIndex)
        modeBlender.outputR >> visibilityCondition.firstTerm

        return visibilityCondition

    def _getModeBlenderForInput(self, inputIndex):
        attrName = 'modeBlender_'+str(inputIndex)
        if hasattr(self.switchControl, attrName):
            return self.switchControl.attr(attrName).inputs()[0]

        else:
            return self._createModeBlenderForInput(inputIndex)

    def _createModeBlenderForInput(self, inputIndex):

        modeBlender = pymel.createNode('blendColors')
        attrName = 'modeBlender_'+str(inputIndex)
        self.switchControl.addAttr(attrName, at='message')
        modeBlender.message >> self.switchControl.attr(attrName)

        modeACondition = pymel.createNode('condition')
        modeACondition.secondTerm.set(inputIndex)
        modeACondition.colorIfTrueR.set(1.0)
        modeACondition.colorIfFalseR.set(0.0)
        self.switchControl.attr('%sA' % MODE_LABEL) >> modeACondition.firstTerm

        modeBCondition = pymel.createNode('condition')
        modeBCondition.secondTerm.set(inputIndex)
        modeBCondition.colorIfTrueR.set(1.0)
        modeBCondition.colorIfFalseR.set(0.0)
        self.switchControl.attr('%sB' % MODE_LABEL) >> modeBCondition.firstTerm

        modeACondition.outColorR >> modeBlender.color1R
        modeBCondition.outColorR >> modeBlender.color2R
        self.switchControl.attr('%sBlend' % MODE_LABEL) >> modeBlender.blender

        return modeBlender