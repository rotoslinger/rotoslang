#====================================================================================
#====================================================================================
#
# ka_controls
#
# DESCRIPTION:
#   A module for creating and manipulating animaiton controls
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

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_pymel as ka_pymel
import ka_rigTools.ka_shapes as ka_shapes
import ka_rigTools.ka_naming as ka_naming
import ka_rigTools.ka_transforms as ka_transforms
import ka_rigTools.ka_attr as ka_attr
import ka_rigTools.ka_math as ka_math

SPACE_LABEL = 'Space'

def createControlStack(name, sizeOfStack=2, shape='peg', index='', side='', size=[1,1,1], lengthAxis='y',
                       length=None, rotateOffset=[], pointAt='y'):
    """returns a list of transforms, with the last being the main control, and the
    first being it's zero out group"""

    if not isinstance(size, list):
        size = [size, size, size]

    controlerStack = []

    if sizeOfStack > 1:
        zroGroup = pymel.createNode('transform')
        ka_naming.setName(zroGroup, name, index=index, side=side, nodePurpose='zeroOutGroup')
        controlerStack.append(zroGroup)

    if sizeOfStack > 2:
        for i in range(sizeOfStack-2):
            offsetGroup = pymel.createNode('transform')
            ka_naming.setName(offsetGroup, name, index=index, side=side, nodePurpose='offsetGroup')
            controlerStack.append(offsetGroup)


    controlShape = ka_shapes.createNurbsCurve(shape=shape, scale=size, pointAt=pointAt)
    control = pymel.createNode('joint')
    ka_shapes.shapeParent(controlShape, control)
    #control.drawStyle.set(2)
    control.radius.set(0)
    control.radius.set(channelBox=False)
    ka_naming.setName(control, name, index=index, side=side, nodePurpose='control')
    controlerStack.append(control)

    for i, node in enumerate(controlerStack):
        if i != 0:
            node.setParent(controlerStack[i-1])

    if side == 'l':
        controlerStack[-1].overrideEnabled.set(1)
        controlerStack[-1].overrideColor.set(6)

    elif side == 'r':
        controlerStack[-1].overrideEnabled.set(1)
        controlerStack[-1].overrideColor.set(13)

    else:
        controlerStack[-1].overrideEnabled.set(1)
        controlerStack[-1].overrideColor.set(17)

    return controlerStack

def resizeControlShape(control, size, length=None, nextControl=None, lengthAxis='x'):

    control = ka_pymel.getAsPyNodes(control)

    if 'transform' in pymel.nodeType(control, inherits=True):
        controlShapes = control.getShapes()
        control = control

    else:
        controlShapes = control
        control = control.getParent()

    laticeDeformer, lattice, latticeBase = pymel.lattice(controlShapes)
    latticeShape = lattice.getShape()
    latticeBase.uDivisions.set(2)
    latticeBase.sDivisions.set(2)
    latticeBase.tDivisions.set(2)

    laticeDeformer.outsideLattice.set(1)


def addSpace(controlStack, spaceParent=None, label=None, t=1, r=1):
    spaceXform = None
    indexOfSpaceXform = None

    for i, xForm in enumerate(controlStack):
        if hasattr(xForm, 'isSpaceXform'):
            spaceXform = xForm
            indexOfSpaceXform = i
            break

    if not spaceXform:
        indexOfSpaceXform, controlStack = _createSpaceXform(controlStack)
        spaceXform = controlStack[indexOfSpaceXform]

    else:
        spaceSwitchXform = controlStack[-1] # the node with the switch attributes

        ka_attr.addEnumValue(spaceSwitchXform.attr('t%sA' % SPACE_LABEL), label)
        ka_attr.addEnumValue(spaceSwitchXform.attr('t%sB' % SPACE_LABEL), label)
        ka_attr.addEnumValue(spaceSwitchXform.attr('r%sA' % SPACE_LABEL), label)
        ka_attr.addEnumValue(spaceSwitchXform.attr('r%sB' % SPACE_LABEL), label)

        nextIndex = int(pymel.attributeQuery('t%sA' % SPACE_LABEL, node=spaceSwitchXform, maximum=True)[0])
        _createSpaceBlenderForInput(nextIndex, spaceParent, spaceXform, controlStack)


def _createSpaceXform(controlStack):
    spaceXform = pymel.createNode('transform')
    spaceXform.rename(controlStack[-1].nodeName()+'_spaceXForm')
    spaceXform.addAttr('isSpaceXform', at='message')

    ka_transforms.snap(spaceXform, controlStack[0], t=1, r=1, s=1)

    spaceXform.setParent(controlStack[0])
    controlStack[1].setParent(spaceXform)
    indexOfSpaceXform = 1
    controlStack.insert(1, spaceXform)

    ka_transforms.snap(spaceXform, controlStack[0], t=1, r=1, s=1)


    # orientConstraint
    if 1:
        orientConstraint = pymel.createNode('orientConstraint')
        orientConstraint.rename(spaceXform.nodeName()+'_spaceSwitch_orientConstraint')
        orientConstraint.setParent(spaceXform)

        spaceXform.parentInverseMatrix[0] >> orientConstraint.constraintParentInverseMatrix
        spaceXform.rotateOrder >> orientConstraint.constraintRotateOrder

        orientConstraint.constraintRotateX >> spaceXform.rx
        orientConstraint.constraintRotateY >> spaceXform.ry
        orientConstraint.constraintRotateZ >> spaceXform.rz


    # pointConstraint
    if 1:
        pointConstraint = pymel.createNode('pointConstraint')
        orientConstraint.rename(spaceXform.nodeName()+'_spaceSwitch_pointConstraint')
        pointConstraint.setParent(spaceXform)
        spaceXform.parentInverseMatrix[0] >> pointConstraint.constraintParentInverseMatrix

        pointConstraint.constraintTranslateX >> spaceXform.tx
        pointConstraint.constraintTranslateY >> spaceXform.ty
        pointConstraint.constraintTranslateZ >> spaceXform.tz


    # space attr
    enumString = 'local:world'
    ka_attr.addHeaderAttr(controlStack[-1], '%s_SWITCHS' % SPACE_LABEL.upper())
    controlStack[-1].addAttr('t%sA' % SPACE_LABEL, at='enum', enumName=enumString, keyable=True)
    controlStack[-1].addAttr('t%sB' % SPACE_LABEL, at='enum', enumName=enumString, defaultValue=1, keyable=True)
    controlStack[-1].addAttr('t%sBlend' % SPACE_LABEL, maxValue=1.0, minValue=0.0, keyable=True)

    ka_attr.addSeparatorAttr(controlStack[-1])

    controlStack[-1].addAttr('r%sA' % SPACE_LABEL, at='enum', enumName=enumString, keyable=True)
    controlStack[-1].addAttr('r%sB' % SPACE_LABEL, at='enum', enumName=enumString, defaultValue=1, keyable=True)
    controlStack[-1].addAttr('r%sBlend' % SPACE_LABEL, maxValue=1.0, minValue=0.0, keyable=True)

    spaceBlenderT, spaceBlenderR = _createSpaceBlenderForInput(0, 'local', spaceXform, controlStack)
    #if spaceBlenderT:
        #spaceBlenderT.outputR >> pointConstraint.target[0].targetWeight

    #if spaceBlenderR:
        #spaceBlenderR.outputR >> orientConstraint.target[0].targetWeight


    spaceBlenderT, spaceBlenderR = _createSpaceBlenderForInput(1, 'world', spaceXform, controlStack)
    #if spaceBlenderT:
        #spaceBlenderT.outputR >> pointConstraint.target[1].targetWeight

    #if spaceBlenderR:
        #spaceBlenderR.outputR >> orientConstraint.target[1].targetWeight

    return indexOfSpaceXform, controlStack

def _getSpaceBlenderForInput(spaceXform, inputIndex):
    attrName = 'spaceBlender_'+str(inputIndex)
    if hasattr(spaceXform, attrName):
        return spaceXform.attr(attrName).inputs()[0]

    else:
        return _createSpaceBlenderForInput(inputIndex)

def _createSpaceBlenderForInput(inputIndex, targetXform, spaceXform, controlStack):
    spaceBlenderT = None
    spaceBlenderR = None
    t = 1
    if t:
        spaceBlenderT = pymel.createNode('blendColors')
        attrName = 'spaceBlenderT_'+str(inputIndex)
        spaceXform.addAttr(attrName, at='message')
        spaceBlenderT.message >> spaceXform.attr(attrName)

        spaceACondition = pymel.createNode('condition')
        spaceACondition.secondTerm.set(inputIndex)
        spaceACondition.colorIfTrueR.set(1.0)
        spaceACondition.colorIfFalseR.set(0.0)
        controlStack[-1].attr('t%sA' % SPACE_LABEL) >> spaceACondition.firstTerm

        spaceBCondition = pymel.createNode('condition')
        spaceBCondition.secondTerm.set(inputIndex)
        spaceBCondition.colorIfTrueR.set(1.0)
        spaceBCondition.colorIfFalseR.set(0.0)
        controlStack[-1].attr('t%sB' % SPACE_LABEL) >> spaceBCondition.firstTerm

        spaceACondition.outColorR >> spaceBlenderT.color2R
        spaceBCondition.outColorR >> spaceBlenderT.color1R
        controlStack[-1].attr('t%sBlend' % SPACE_LABEL) >> spaceBlenderT.blender

        pointConstraint = None
        pointConstraints = spaceXform.tx.inputs(type='pointConstraint')

    r = 1
    if r:
        spaceBlenderR = pymel.createNode('blendColors')
        attrName = 'spaceBlenderR_'+str(inputIndex)
        spaceXform.addAttr(attrName, at='message')
        spaceBlenderR.message >> spaceXform.attr(attrName)

        spaceACondition = pymel.createNode('condition')
        spaceACondition.secondTerm.set(inputIndex)
        spaceACondition.colorIfTrueR.set(1.0)
        spaceACondition.colorIfFalseR.set(0.0)
        controlStack[-1].attr('r%sA' % SPACE_LABEL) >> spaceACondition.firstTerm

        spaceBCondition = pymel.createNode('condition')
        spaceBCondition.secondTerm.set(inputIndex)
        spaceBCondition.colorIfTrueR.set(1.0)
        spaceBCondition.colorIfFalseR.set(0.0)
        controlStack[-1].attr('r%sB' % SPACE_LABEL) >> spaceBCondition.firstTerm

        spaceACondition.outColorR >> spaceBlenderR.color2R
        spaceBCondition.outColorR >> spaceBlenderR.color1R
        controlStack[-1].attr('r%sBlend' % SPACE_LABEL) >> spaceBlenderR.blender

        orientConstraint = None
        orientConstraints = spaceXform.rx.inputs(type='orientConstraint')


    if orientConstraints:
        orientConstraint = orientConstraints[0]
    if pointConstraints:
        pointConstraint = pointConstraints[0]


    # local space
    if targetXform == 'local':
        if t:
            controlStack[0].parentMatrix[0] >> pointConstraint.target[inputIndex].targetParentMatrix

        if r:
            controlStack[0].parentMatrix[0] >> orientConstraint.target[inputIndex].targetParentMatrix


    # world space
    elif targetXform == 'world':
        parentMatrix = ka_transforms.getListFromMMatrix(spaceXform.parentMatrix[0].get())
        worldSpacePosition = pymel.xform(controlStack[0], query=True, translation=True, worldSpace=True)
        worldSpaceRotation = pymel.xform(controlStack[0], query=True, rotation=True, worldSpace=True)


        if t:
            pointConstraint.target[inputIndex].targetTranslate.set(worldSpacePosition)


        if r:
            controlStack[0].inverseMatrix >> orientConstraint.target[inputIndex].targetParentMatrix
            pass
    # target object space
    else:
        if t:
            worldSpacePoint = pymel.xform(spaceXform, query=True, worldSpace=True, translation=True)
            translate = ka_transforms.getInForienSpace_point(worldSpacePoint, targetXform)

            pointConstraint.target[inputIndex].targetTranslate.set(translate)
            targetXform.worldMatrix[0] >> pointConstraint.target[inputIndex].targetParentMatrix

        if r:
            rotate = ka_transforms.getInForienSpace_eularRotation(spaceXform, targetXform)

            orientConstraint.target[inputIndex].targetRotate.set(rotate)

            targetXform.worldMatrix[0] >> orientConstraint.target[inputIndex].targetParentMatrix


    if spaceBlenderT:
        spaceBlenderT.outputR >> pointConstraint.target[inputIndex].targetWeight

    if spaceBlenderR:
        spaceBlenderR.outputR >> orientConstraint.target[inputIndex].targetWeight


    return spaceBlenderT, spaceBlenderR