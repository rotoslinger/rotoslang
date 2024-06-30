
#====================================================================================
#====================================================================================
#
# kMenu_menus
#
# DESCRIPTION:
#   a list of all the different menus created for kMenu
#
# DEPENDENCEYS:
#   kMenu
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


import os
import sip
import PyQt4
from PyQt4 import QtGui, QtCore, uic

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as OpenMayaUI

import ka_rigTools.kMenu as kMenu                                             #;reload(kMenu)
import ka_rigTools.ka_util as ka_util                                         #;reload(ka_util)
import ka_rigTools.core as ka_rigTools                                        #;reload(ka_rigTools)
import ka_rigTools.ka_context as ka_context                                   #;reload(ka_context)
import ka_rigTools.ka_display as ka_display                                   #;reload(ka_context)
import ka_rigTools.ka_rigSetups.ka_lengthBasedRibon as ka_lengthBasedRibon    #;reload(ka_lengthBasedRibon)
import ka_rigTools.ka_attrTool.attrCommands as attrCommands                   #;reload(attrCommands)
import ka_rigTools.ka_rigAerobics as ka_rigAerobics    #;reload(ka_rigAerobics)
import ka_rigTools.ka_advancedJoints as ka_advancedJoints                     #;reload(ka_advancedJoints)
import ka_rigTools.ka_shapes as ka_shapes                     #;reload(ka_advancedJoints)

context = ka_context.newContext()

# CREATE MENU
MENU_CREATE = kMenu.KMenu(label='Create', icon='create.png')
if MENU_CREATE:
    with MENU_CREATE.addSubMenu(label='Nurbs Curve'):
        for shapeName in ka_shapes.NURBSCURVE_SHAPES:
            def cmds(shapeName=shapeName):
                ka_shapes.createNurbsCurve(shapeName)
            MENU_CREATE.add(cmds, label=shapeName,)

        #MENU_CREATE.add(ka_rigTools.createShape_cube)
        #MENU_CREATE.add(ka_rigTools.createShape_circle)
        #MENU_CREATE.add(ka_rigTools.createShape_square)
        #MENU_CREATE.add(ka_rigTools.createShape_pyramidPointer)

    with MENU_CREATE.addSubMenu(label='Advanced Joints'):
        MENU_CREATE.add(ka_rigTools.createAdvanceJoint_pistonJoint)
        MENU_CREATE.add(ka_rigTools.createAdvanceJoint_ligamentJoint)
        MENU_CREATE.add(ka_rigTools.createAdvanceJoint_advancedIkSpline)
        MENU_CREATE.add(ka_lengthBasedRibon.create)
        #MENU_CREATE.add(ka_advancedJoints.createVolumeRotator)
        #MENU_CREATE.add(ka_advancedJoints.printVolumeRotators)
        MENU_CREATE.add(ka_rigTools.createVolumeRotator)
        #MENU_CREATE.add(ka_rigTools.printSelectedVolumeRotators)
        MENU_CREATE.add(ka_rigTools.printAllVolumeRotators)

    with MENU_CREATE.addSubMenu(label='Rig Setups'):
        MENU_CREATE.add(ka_rigTools.rigSetup_advancedFK)


# SELECTION MENU
MENU_SELECTION = kMenu.KMenu(label='Selection', icon='Selection.png')
if MENU_SELECTION:
    MENU_SELECTION.add(ka_rigTools.filterTool)
    MENU_SELECTION.add(ka_rigTools.invertSelectionOrder)
    MENU_SELECTION.add(ka_rigTools.islandSelectComponents)
    MENU_SELECTION.add(ka_rigTools.selectAllSkinClusterInfluences)


# DISPLAY MENU
MENU_DISPLAY = kMenu.KMenu(label='Display', icon='visibility.png')
if MENU_DISPLAY:
    with MENU_DISPLAY.addSubMenu(label='Skinning Sets'):
        MENU_DISPLAY.add(ka_rigTools.skinningDisplaySet_createFromScene)
        #with MENU_DISPLAY.addSubMenu(label='Remove Skinning Set'):
            #pass
        #with MENU_DISPLAY.addSubMenu(label='Update Skinning Set'):
            #pass

        MENU_DISPLAY.add(ka_rigTools.skinningDisplaySet_printAll)

        for eachSet in ka_display.skinningDisplaySet_getAll():
            #MENU_DISPLAY.add(ka_rigTools.setSkinningDisplaySet(str(eachSet)), label=eachSet.nodeName())

            def cmd(skinningSet=eachSet): ka_rigTools.setSkinningDisplaySet(str(skinningSet))
            MENU_DISPLAY.add(cmd, label=eachSet.nodeName(), icon='isolateSelection.png')


    #for skinningSet in pymel.about:
    MENU_DISPLAY.add(ka_rigTools.setIsolateSet)
    MENU_DISPLAY.add(ka_rigTools.clearIsolateSet)
    MENU_DISPLAY.add(ka_rigTools.hideRotationAxisForAll)
    MENU_DISPLAY.add(ka_rigTools.isolateSelection_skinningMode)
    MENU_DISPLAY.add(ka_rigTools.toggleColorWireframeOnSelected)
    MENU_DISPLAY.add(ka_rigTools.disableDrawOverrides_onSelection)
    MENU_DISPLAY.add(ka_rigTools.enableDrawOverrides_onSelection)


# ANIMATION MENU
MENU_ANIMATION = kMenu.KMenu(label='Animation', icon='key.png')
if MENU_ANIMATION:
    MENU_ANIMATION.addSeparator(label='Set Keys:')
    MENU_ANIMATION.add(ka_rigTools.keyAllControls)
    MENU_ANIMATION.add(ka_rigTools.advance20Frames)
    MENU_ANIMATION.add(ka_rigTools.advance10Frames)
    MENU_ANIMATION.add(ka_rigTools.applyTPose)

    MENU_ANIMATION.addSeparator(label='Store Pose and Controls')
    MENU_ANIMATION.add(ka_rigTools.storeTPose)
    MENU_ANIMATION.add(ka_rigTools.storeSelectionAsAllControls)
    MENU_ANIMATION.add(ka_rigTools.selectAllControls)

    if context.getStudioEnv() == 'rnk':
        MENU_ANIMATION.addSeparator(label='Apply RNK Bipied Rig Aerobics')
        MENU_ANIMATION.add(ka_rigAerobics.rnkBipiedAnimation)


# BLENDSHAPE MENU
MENU_BLENDSHAPES = kMenu.KMenu(label='Blendshapes')
if MENU_BLENDSHAPES:
    MENU_BLENDSHAPES.add(ka_rigTools.mirrorMesh)
    MENU_BLENDSHAPES.add(ka_rigTools.flipMesh)


# SKINNING MENU
MENU_SKINNING = kMenu.KMenu(label='Skinning: ')
if MENU_SKINNING:

    #MENU_SKINNING.add(ka_rigTools.pasteWeightsFromInfluence)

    MENU_SKINNING.addSeparator(label='Joint under mouse', context=ka_context.paintableInfluenceUnderMouse_context)
    MENU_SKINNING.add(ka_rigTools.paintInfluenceUnderMouse)
    MENU_SKINNING.add(ka_rigTools.paintInfluenceUnderMouse_andHoldAllOthers)

    MENU_SKINNING.addSeparator(label='Influence Holding')
    MENU_SKINNING.add(ka_rigTools.holdInfluences)
    MENU_SKINNING.add(ka_rigTools.unholdInfluences)

    MENU_SKINNING.addSeparator(label='Skinning Commands')
    MENU_SKINNING.add(ka_rigTools.mirrorWeights)
    MENU_SKINNING.add(ka_rigTools.mirrorWeights_onFrame1)
    MENU_SKINNING.add(ka_rigTools.isolateSelection_skinningMode)

    MENU_SKINNING.addSeparator(label='skinCluster Resets')
    MENU_SKINNING.add(ka_rigTools.resetSkinCluster)
    MENU_SKINNING.add(ka_rigTools.resetSkinCluster_onFrame1)
    MENU_SKINNING.add(ka_rigTools.bakeSkinCluster)

    with MENU_SKINNING.addSubMenu(label='Copy / Paste Weights'):

        #MENU_SKINNING.addSeparator(label='Copy Paste Weights')
        MENU_SKINNING.add(ka_rigTools.copySkinWeights)
        MENU_SKINNING.add(ka_rigTools.pasteSkinWeights)


    MENU_SKINNING.addSeparator(label='Misc')
    MENU_SKINNING.add(ka_rigTools.deleteAllBindPoseNodes)


# DEFORMERS MENU
MENU_DEFORMERS = kMenu.KMenu(label='Deformers', icon='deformers.png')
if MENU_DEFORMERS:
    MENU_DEFORMERS.add(ka_rigTools.skinCluster)
    MENU_DEFORMERS.add(MENU_SKINNING)
    MENU_DEFORMERS.add(MENU_BLENDSHAPES)
    MENU_DEFORMERS.add(ka_rigTools.clusterDeform_eachInSelection)


# TRANSFORMS MENU
MENU_TRANSFORMS = kMenu.KMenu(label='Transforms', icon='xyz.png')
if MENU_TRANSFORMS:
    MENU_TRANSFORMS.add(ka_rigTools.removeNonStandardTransformValues)
    MENU_TRANSFORMS.add(ka_rigTools.removeJointOrients)


# COPY PASTE MENU
MENU_COPYPASTE = kMenu.KMenu(label='Copy & Paste', icon='clipboard.png')
if MENU_COPYPASTE:
    MENU_COPYPASTE.add(ka_rigTools.copyShape)
    MENU_COPYPASTE.add(ka_rigTools.pasteShape)
    MENU_COPYPASTE.add(ka_rigTools.pasteShapeFlipped)
    MENU_COPYPASTE.add(ka_rigTools.pasteShapeReversed)


# TRANSFER MENU
MENU_TRANSFER = kMenu.KMenu(label='Transfer Tools', icon='transfer.png')
if MENU_TRANSFER:
    MENU_TRANSFER.add(MENU_COPYPASTE)
    MENU_TRANSFER.add(ka_rigTools.transferSkin)
    MENU_TRANSFER.add(ka_rigTools.transferSelectedWeights)
    MENU_TRANSFER.add(ka_rigTools.storeSelection)
    MENU_TRANSFER.add(ka_rigTools.xferComponentWeights_fromStoredSelection)
    MENU_TRANSFER.add(ka_rigTools.xferComponentWeights_fromStoredSelection_onFrame1)

# COLOR MENU
MENU_COLOR = kMenu.KMenu(label='Color', icon='colorPallet.png')
if MENU_COLOR:
    favoriteColors = [([1.0, 0.0, 0.0], 'Red'),
                      ([0.66, 0.0, 0.0], '%66 Red'),
                      ([0.0, 0.0, 1.0], 'Blue'),
                      ([0.0, 0.0, 0.66], '%66 Blue'),
                      ([1.0, 1.0, 0.0], 'Yellow'),
                      ([0.66, 0.66, 0.0], '%66 Yellow'),
                      ([0.3919999897480011, 0.86299997568130493, 1.0], 'Baby Blue'),
                      ([0.25871999323368072, 0.56957998394966125, 0.66], '%66 Baby Blue'),
                      ([1.0, 0.5, 0.0], 'Orange'),
                      ([0.5, 0.25, 0.0], '%66 Orange'),
                      ]

    # CUSTOME Colors
    for rgbColor, label in favoriteColors:
        r, g, b = rgbColor

        def cmd(rgbColor=rgbColor): ka_util.colorObjects(color=rgbColor)
        MENU_COLOR.add(cmd, label=label, icon=rgbColor)


    # MAYA Colors
    for i in range(32):
        if i == 0:
            def cmd(): mel.eval("kaRig_colourSelection \"black\";")
            MENU_COLOR.add(cmd, label='#%s None' % str(i))
        else:
            rgb = pymel.colorIndex( i, q=True )

            def cmd(i=i): ka_util.colorObjects(index=i)
            MENU_COLOR.add(cmd, label='#%s' % str(i), icon=rgb)


# LOCK / UNLOCK MENU
MENU_LOCK_UNLOCK = kMenu.KMenu(label='Lock / Unlock', icon='lock.png')
if MENU_LOCK_UNLOCK:
    with MENU_LOCK_UNLOCK.addSubMenu(label='Lock', icon='lock.png'):
        MENU_LOCK_UNLOCK.add(ka_rigTools.lockTranslate)
        MENU_LOCK_UNLOCK.add(ka_rigTools.lockRotate)
        MENU_LOCK_UNLOCK.add(ka_rigTools.lockScale)
        MENU_LOCK_UNLOCK.add(ka_rigTools.lockVis)
        MENU_LOCK_UNLOCK.add(ka_rigTools.lockRadius)
        MENU_LOCK_UNLOCK.add(ka_rigTools.lockAll)

    with MENU_LOCK_UNLOCK.addSubMenu(label='Unlock', icon='unlock.png'):
        MENU_LOCK_UNLOCK.add(ka_rigTools.unlockTranslate)
        MENU_LOCK_UNLOCK.add(ka_rigTools.unlockRotate)
        MENU_LOCK_UNLOCK.add(ka_rigTools.unlockScale)
        MENU_LOCK_UNLOCK.add(ka_rigTools.unlockVis)
        MENU_LOCK_UNLOCK.add(ka_rigTools.unlockRadius)
        MENU_LOCK_UNLOCK.add(ka_rigTools.unlockAll)


# HIERARCHY MENU
MENU_HIERARCHY = kMenu.KMenu(label='Hierarchy', icon='groups.png')
if MENU_HIERARCHY:
    MENU_HIERARCHY.add(ka_rigTools.addZeroOutGroup)
    MENU_HIERARCHY.add(ka_rigTools.parentShape)


# CONSTRAINT MENU
MENU_CONSTRAINT = kMenu.KMenu(label='Constrain', icon='pointConstraint.png')
if MENU_CONSTRAINT:
    MENU_CONSTRAINT.add(ka_rigTools.constrain_surfaceConstraint)
    MENU_CONSTRAINT.add(ka_rigTools.constrain_curveConstraint)
    MENU_CONSTRAINT.add(ka_rigTools.constrain_aimBetweenConstraint)
    MENU_CONSTRAINT.add(ka_rigTools.constrain_pointAndOrient)
    MENU_CONSTRAINT.add(ka_rigTools.constrain_pointOrientAndScale)
    MENU_CONSTRAINT.add(ka_rigTools.constrain_jointOrientContraint)
    MENU_CONSTRAINT.add(ka_rigTools.constrain_distanceBetween)
    MENU_CONSTRAINT.add(ka_rigTools.constrain_nonTwistAim)
    with MENU_CONSTRAINT.addSubMenu(label='Direct Connects'):
        MENU_CONSTRAINT.add(ka_rigTools.directConnect_translates)
        MENU_CONSTRAINT.add(ka_rigTools.directConnect_rotates)
        MENU_CONSTRAINT.add(ka_rigTools.directConnect_scales)



# CONSTRAINT MENU
MENU_SNAP = kMenu.KMenu(label='Snap', icon='magnet.png')
if MENU_SNAP:
    MENU_SNAP.add(ka_rigTools.snap_translate)
    MENU_SNAP.add(ka_rigTools.snap_rotate)
    MENU_SNAP.add(ka_rigTools.snap_scale)
    MENU_SNAP.add(ka_rigTools.snap_aim)
    MENU_SNAP.add(ka_rigTools.snap_mirror)


# MISC MENU
MENU_MISC = kMenu.KMenu(label='Misc', icon='misc.png')
if MENU_MISC:
    with MENU_MISC.addSubMenu(label='Print Commands'):
        MENU_MISC.add(ka_rigTools.print_selection)
        MENU_MISC.add(ka_rigTools.print_curve)
        MENU_MISC.add(ka_rigTools.print_mesh)

    MENU_MISC.add(ka_rigTools.deleteAllKeyframes)
    MENU_MISC.add(ka_rigTools.deleteAllBindPoseNodes)
    MENU_MISC.add(ka_rigTools.findLatticeCageFromLatticeDeformer)
    MENU_MISC.add(ka_rigTools.setJointLabel)
    MENU_MISC.add(ka_rigTools.setJointLabel_allInfluences)
    MENU_MISC.add(ka_rigTools.reorderAllShapesToTopOfTheirHierchy)
    MENU_MISC.add(ka_rigTools.makeSurfaceConstraint_useTangetV)
    MENU_MISC.add(ka_rigTools.makeSurfaceConstraint_useTangetU)


# TOOL MENU
MENU_TOOL = kMenu.KMenu(label='Tools: ', icon='tools.png')
if MENU_TOOL:
    MENU_TOOL.add(ka_rigTools.renameTool)
    MENU_TOOL.add(ka_rigTools.filterTool)
    MENU_TOOL.add(ka_rigTools.attrTool)


# COMPONENT_SELECTION_MENU
MENU_COMPONENT = kMenu.KMenu(label='Component Selection: ')
if MENU_COMPONENT:
    MENU_COMPONENT.add(ka_rigTools.pasteWeightsFromInfluence)


# HYPERSHADE MENU
MENU_HYPERSHADE = kMenu.KMenu(label='HyperShade: ')
if MENU_HYPERSHADE:
    MENU_HYPERSHADE.add(ka_rigTools.attrTool)

    MENU_HYPERSHADE.addSeparator('') #---------------------------------------------------------

    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_alignNodesVertical)
    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_alignNodesHorizontal)
    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_clear)
    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_isolateSelection)
    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_add)

    MENU_HYPERSHADE.addSeparator('') #---------------------------------------------------------

    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_duplicate)
    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_echoRecreateCommands)
    with MENU_HYPERSHADE.addSubMenu(label='Create Node', icon='create.png'):
        createNodeTypesList = ['choice', 'multiplyDivide', 'blendColors', 'condition', 'setRange', 'plusMinusAverage', 'blendTwoAttr', 'distanceBetween', 'pointOnCurveInfo', 'curveInfo', 'pointOnSurfaceInfo', 'surfaceInfo', 'closestPointOnSurface', 'angleBetween', 'vectorProduct', 'arrayMapper', 'bump2d', 'bump3d', 'heightField', 'lightInfo', 'place2dTexture', 'place3dTexture', 'projection', 'reverse', 'samplerInfo', 'stencil', 'uvChooser', 'animCurveUU', 'animCurveUA', 'animCurveUL', 'animCurveUT', 'closestPointOnMesh', 'remapValue',]
        for eachNodeType in sorted(createNodeTypesList):
            if 'animCurve' in eachNodeType:
                def cmd(nodeType=eachNodeType):
                    node = pymel.createNode(nodeType)
                    ka_hyperShade.addKeysToAnimCurveNode(node)
                    return node
            else:
                def cmd(nodeType=eachNodeType):
                    pymel.createNode(nodeType)
                    return node

            MENU_HYPERSHADE.add(cmd, label=eachNodeType)

    MENU_HYPERSHADE.addSeparator('') #---------------------------------------------------------

    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_graphInputs)
    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_graphOutputs)
    MENU_HYPERSHADE.add(ka_rigTools.hyperShade_graphInputsAndOutputs)

    MENU_HYPERSHADE.addSeparator('') #---------------------------------------------------------

    with MENU_HYPERSHADE.addSubMenu(label='Misc', icon='misc.png'):
        MENU_HYPERSHADE.add(ka_rigTools.hyperShade_selectInputs)
        MENU_HYPERSHADE.add(ka_rigTools.hyperShade_selectOutputs)
        MENU_HYPERSHADE.add(ka_rigTools.hyperShade_selectInputsAndOutputs)

        MENU_HYPERSHADE.addSeparator('') #---------------------------------------------------------

        MENU_HYPERSHADE.add(ka_rigTools.hyperShade_addKeysToAnimCurveNode)

        with MENU_HYPERSHADE.addSubMenu(label='convertAnimCurvesTo:', icon='transfer.png'):
            MENU_HYPERSHADE.add(ka_rigTools.convertAnimCurveTo_UU)
            MENU_HYPERSHADE.add(ka_rigTools.convertAnimCurveTo_UA)
            MENU_HYPERSHADE.add(ka_rigTools.convertAnimCurveTo_UL)
            MENU_HYPERSHADE.add(ka_rigTools.convertAnimCurveTo_UT)




MENU_ATTR_TOOL = kMenu.KMenu()
MENU_ATTR_TOOL.add(kMenu.KMenuItem_attrTool)


# ROOT MENU
MENU_ROOT = kMenu.KMenu()
if MENU_ROOT:

    MENU_ROOT.addSeparator(label='Context Actions')

    #if ka_context.weightedComponentsSelected(context=context):
    MENU_ROOT.add(ka_rigTools.pasteSkinWeightsAlongStrand, showContext=ka_context.weightedComponentsSelected)
    MENU_ROOT.add(ka_rigTools.pasteSkinWeightsFromStrandNeighbores, showContext=ka_context.weightedComponentsSelected)



    if context.userIsK():
        MENU_ROOT.add(ka_rigTools.createHuman)
        MENU_ROOT.add(ka_rigTools.testCommandA)
        MENU_ROOT.add(ka_rigTools.testCommandB)
        MENU_ROOT.add(ka_rigTools.testCommandC)


    MENU_ROOT.add(ka_rigTools.skinCluster)
    MENU_ROOT.add(ka_rigTools.addInfluence)
    if context.getStudioEnv() == 'rnk':
        pass


    MENU_ROOT.addSeparator(label='Root Menu')
    MENU_ROOT.add(MENU_CREATE)
    MENU_ROOT.add(MENU_SELECTION)
    MENU_ROOT.add(MENU_DISPLAY)


    MENU_ROOT.add(MENU_DEFORMERS)
    MENU_ROOT.add(MENU_ANIMATION)
    MENU_ROOT.add(MENU_TRANSFORMS)
    MENU_ROOT.add(MENU_TRANSFER)
    MENU_ROOT.add(MENU_COLOR)
    MENU_ROOT.add(MENU_LOCK_UNLOCK)
    MENU_ROOT.add(MENU_HIERARCHY)
    MENU_ROOT.add(MENU_CONSTRAINT)
    MENU_ROOT.add(MENU_SNAP)
    MENU_ROOT.add(MENU_MISC)
    MENU_ROOT.add(MENU_TOOL)

    MENU_ROOT.addSeparator(label='Context Menus')
    MENU_ROOT.add(MENU_SKINNING)
    MENU_ROOT.add(MENU_HYPERSHADE)






def popMenu(clearFirst=False):
    global MENU_ROOT

    context = ka_context.newContext()


    if kMenu.getAllKMenuWidgets() and clearFirst:
        kMenu.clearUnpinnedKMenus(onlyNonPinned=False)

    else:

        if kMenu.getAllUnpinnedKMenuWidgets():
            kMenu.clearUnpinnedKMenus()

        else:
            kMenu.clearUnpinnedKMenus()
            kMenu.raise_MenuWidgets()

            if context.getUiTypeUnderMouse() == 'hyperShade':
                if context.getHypershade_nodeUnderMouse():
                    MENU_ATTR_TOOL.pop()

                else:
                    MENU_HYPERSHADE.pop()


            elif context.getUiTypeUnderMouse() == 'model':

                if context.getCurrentTool() == 'artAttrSkinContext':
                    MENU_SKINNING.pop()

                elif ka_context.paintableInfluenceUnderMouse_and_componentsSelected_context(context=context):
                    MENU_COMPONENT.pop()

                else:
                    #skinningDisplaySets = ka_display.skinningDisplaySet_getAll()
                    #if skinningDisplaySets:
                        #skinningDisplaySetsMenu = kMenu.KMenu(label='Skinning Sets: ')
                        #for eachSet in skinningDisplaySets:
                            #def cmd(skinningSet=eachSet): ka_rigTools.setSkinningDisplaySet(str(skinningSet))
                            #MENU_DISPLAY.add(cmd, label=eachSet.nodeName(), icon='isolateSelection.png')

                        #MENU_ROOT.add(skinningDisplaySetsMenu)

                    MENU_ROOT.pop()


            else:
                MENU_ROOT.pop()

