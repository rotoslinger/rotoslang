#====================================================================================
#====================================================================================
#
# ka_menu_modelEditor
#
# DESCRIPTION:
#   loads items to the menu build by ka_menu, these items relate to a menu build in the modelEditor (maya 3d veiwport)
#
# DEPENDENCEYS:
#   -a hotkey to build menu must use ka_rigTools.ka_menu.press()as the command
#   -ka_menu
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

from functools import partial

import sip
import PyQt4
from PyQt4 import QtGui, QtCore, uic
#from PyQt4 import *

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_shapes as ka_shapes                           #;reload(ka_shapes)
import ka_rigTools.ka_display as ka_display                         #;reload(ka_display)
import ka_rigTools.ka_skinCluster as ka_skinCluster                 #;reload(ka_skinCluster)
import ka_rigTools.ka_weightPainting as ka_weightPainting           #;reload(ka_weightPainting)
import ka_rigTools.ka_util as ka_util                               #;reload(ka_util)
import ka_rigTools.ka_transforms as ka_transforms                   #;reload(ka_transforms)
import ka_rigTools.ka_advancedJoints as ka_advancedJoints           #;reload(ka_advancedJoints)
import ka_rigTools.ka_attrTool.ka_attrTool_UI as ka_attrTool_UI     #;reload(ka_attrTool_UI)
import ka_rigTools.ka_qtWidgets as ka_qtWidgets                     #;reload(ka_qtWidgets)
import ka_rigTools.ka_constraints as ka_constraints                 #;reload(ka_constraints)
import importlib


class Menu():
    '''menu items specific to actions in the maya viewport'''

    def __init__(self, menu):
        self.menu = menu

#    def build_menu_modelEditor(self):
    def populateMenu(self, **kwargs):
        '''more or less acting as the __init__'''

        #dagHit Vars...
        dagObjectHit = mel.eval('dagObjectHit -mn %s' % 'fakeName')

        dagObjectHit_objectHit = None
        dagObjectHit_type = None
        dagObjectHit_objectHitShape = None
        dagObjectHit_shapeType = None
        if dagObjectHit:
            dagObjectHit_objectHit = mel.eval('$gDagObjectHit_objectHit=$gDagObjectHit_objectHit')
            if pymel.objExists(dagObjectHit_objectHit):
                dagObjectHit_objectHit = pymel.ls(dagObjectHit_objectHit)[0]
                dagObjectHit_type = pymel.nodeType(dagObjectHit_objectHit)
                dagObjectHit_objectHitShape = pymel.listRelatives(dagObjectHit_objectHit, shapes=True)
                if dagObjectHit_objectHitShape:
                    dagObjectHit_objectHitShape = dagObjectHit_objectHit+'|'+dagObjectHit_objectHitShape[0] #nessisary to conver var from list to item here, to prevent error if None
                    dagObjectHit_shapeType = pymel.nodeType(dagObjectHit_objectHitShape)
            else:
                dagObjectHit_objectHit = None

        #Selection Vars...
        selection = pymel.ls(selection=True)
        if len(selection) > 1:
            multiSelect = True
        else:
            multiSelect = False

        selectionMain_object = ''
        selectionMain_objectType = ''
        selectionMain_shape = ''
        selectionMain_shapeType = ''
        if selection:
            selection0Split = selection[0].split('.')
            if len(selection0Split) > 1:
                selectionMain_object = selection0Split[0]
            else:
                selectionMain_object = selection[0]

            selectionMain_objectType = pymel.nodeType(selectionMain_object)
            selectionMain_shape = pymel.listRelatives(selectionMain_object, shapes=True)
            if selectionMain_shape:
                selectionMain_shape = selectionMain_object+'|'+selectionMain_shape[0]
                selectionMain_shapeType = pymel.nodeType(selectionMain_shape)

            else: #was selectionMain_object a shape?...
                parentOf_selectionMain_object = pymel.listRelatives(selectionMain_object, parent=True)
                if parentOf_selectionMain_object:
                    parentOf_selectionMain_object = parentOf_selectionMain_object[0]
                    shapesOf_parentOf_selectionMain_object = pymel.listRelatives( parentOf_selectionMain_object, shapes=True)
                    if shapesOf_parentOf_selectionMain_object:
                        if selectionMain_object in shapesOf_parentOf_selectionMain_object: #...Guess it was, lets set them as the shape
                            selectionMain_shape = selectionMain_object
                            selectionMain_shapeType = pymel.nodeType(selectionMain_shape)
                            #all that just to figure out if selectionMain was a shape or not...


        toolContext = pymel.currentCtx();

## SKIN WEIGHTING -------------------------------------------------------------------------------------------------------------------------------
        if toolContext == 'artAttrSkinContext':  #
            lenOfInfluenceList = 'N/A'

            if selectionMain_object:
                influenceList = ka_weightPainting.getInfluences(selectionMain_object)
                if influenceList:
                    lenOfInfluenceList = str(len(influenceList))

            if dagObjectHit:

                if influenceList:
                    if dagObjectHit_objectHit in influenceList:

                        def cmd(): ka_weightPainting.paint(dagObjectHit_objectHit)
                        self.menu.addMenuItem( 'Paint:    '+dagObjectHit_objectHit.nodeName(), icon='paint.png', command=cmd )

                        def cmd(): ka_weightPainting.paintAndHoldAllOthers(dagObjectHit_objectHit)
                        self.menu.addMenuItem( 'Paint and Hold All Others: ', icon='paintAndLock.png', command=cmd )

                        self.menu.addSeparatorItem()  #---------------------------------------------------------

                        def cmd(): ka_weightPainting.paintAndHoldAllOthers(dagObjectHit_objectHit)
                        self.menu.addMenuItem( 'Hold Influence: ', icon='lock.png', command=cmd )

                        def cmd(): ka_weightPainting.paintAndHoldAllOthers(dagObjectHit_objectHit)
                        self.menu.addMenuItem( 'Unhold Influence: ', icon='unlock.png', command=cmd )

                        self.menu.addSeparatorItem()  #---------------------------------------------------------

                    elif dagObjectHit_type == 'joint':
                        self.menu.addMenuItem( 'JOINT IS NOT PART OF SKIN    ('+dagObjectHit_objectHit+')')


            def cmd(): ka_weightPainting.holdAllInfluences()
            self.menu.addMenuItem( 'Hold All: ', icon='lock.png', command=cmd )

            def cmd(): ka_weightPainting.unholdAllInfluences()
            self.menu.addMenuItem( 'Unhold All: ', icon='unlock.png', command=cmd )

            self.menu.addSeparatorItem()  #---------------------------------------------------------

            def cmd():
                ka_skinCluster.setSetJointLabelFromNameOnAll()
                ka_weightPainting.mirrorWeights()
            self.menu.addMenuItem( 'Mirror Weights: ', command=cmd, icon='symmetry.png')

            def cmd(): ka_display.isolateSelection(mode='skinning')
            self.menu.addMenuItem( 'Isolate Selection + Influences: ', command=cmd, icon='isolateSelection.png')

            self.menu.addSeparatorItem()  #---------------------------------------------------------

            def cmd(): ka_weightPainting.resetSkin("reset")
            self.menu.addMenuItem( 'Reset Bind Pose: ', command=cmd )

            def cmd(): ka_weightPainting.resetSkin("bake")
            self.menu.addMenuItem( 'Bake as Bind Pose: ', command=cmd )

            def cmd(): ka_weightPainting.deleteAllBindPoses()
            self.menu.addMenuItem( 'Delete All Bind Pose Nodes: ', command=cmd )

            self.menu.addSeparatorItem()  #---------------------------------------------------------

            if self.menu.addSubmenuItem('Copy Paste Weights: ', icon='clipboard.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[
                weightBlenderWidget = ka_qtWidgets.WeightBlenderWidget(self.menu.menu)
                self.menu.addWidgetMenuItem(weightBlenderWidget)

                self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

            #def cmd():
                #reload(ka_util)
                #ka_util.getListOfComponentShells()
            #self.menu.addMenuItem( 'Hard Weight By Shell: ', command=cmd )

            #def cmd(): ka_skinCluster.cleanSkinCluster()
            #self.menu.addMenuItem( 'Clean skinCluster ', command=cmd )

            self.menu.addSeparatorItem()  #---------------------------------------------------------

            if self.menu.addSubmenuItem('Info: ', icon='info.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                def cmd(): pass
                self.menu.addMenuItem( 'number of influences: %s' % str(lenOfInfluenceList), command=cmd )

                self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

## NO TOOL CONTEXTS ARE ON -------------------------------------------------------------------------------------------------------------------------------
        else:
            if dagObjectHit_objectHit:

                def cmd():
                    if ka_util.selectionIsComponent():
                        ka_weightPainting.copySkinWeights(copySpecificInfluence=dagObjectHit_objectHit)
                        ka_weightPainting.pasteSkinWeights()
                self.menu.addMenuItem( 'copy AND paste'+dagObjectHit_objectHit+'\'s influence', icon='paint.png', command=cmd )

                def cmd(): ka_weightPainting.copySkinWeights(copySpecificInfluence=dagObjectHit_objectHit)
                self.menu.addMenuItem( 'copy '+dagObjectHit_objectHit+'\'s influence', icon='paint.png', command=cmd )

                def cmd():
                    import ka_rigTools.ka_selection as ka_selection; importlib.reload(ka_selection)

                    ka_selection.islandSelectComponents()
                    ka_weightPainting.copySkinWeights()
                    ka_weightPainting.pasteSkinWeights()
                self.menu.addMenuItem( 'island select and averageWeights', command=cmd )

                def cmd(): ka_weightPainting.paint(dagObjectHit_objectHit)
                self.menu.addMenuItem( 'Paint:    '+dagObjectHit_objectHit, icon='paint.png', command=cmd )

            else:

                # Create
                if self.menu.addSubmenuItem('Create: ', icon='create.png',): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                    if self.menu.addSubmenuItem('Nurbs Curve Shapes: ',): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        def cmd(): ka_shapes.createNurbsCurve("cube")
                        self.menu.addMenuItem( 'Cube: ', command=cmd )

                        def cmd(): ka_shapes.createNurbsCurve("circle")
                        self.menu.addMenuItem( 'Circle: ', command=cmd )

                        def cmd(): ka_shapes.createNurbsCurve("square")
                        self.menu.addMenuItem( 'Square: ', command=cmd )

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                    # Advanced Joints
                    if self.menu.addSubmenuItem('Advanced Joints: '): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        def cmd(): importlib.reload(ka_advancedJoints) ;ka_advancedJoints.muscleJoint()
                        self.menu.addMenuItem( 'make piston JointMuscle', command=cmd )

                        def cmd(): importlib.reload(ka_advancedJoints) ;ka_advancedJoints.createBendMuscle()
                        self.menu.addMenuItem( 'make ligament JointMuscle', command=cmd )

                        def cmd(): importlib.reload(ka_advancedJoints)     ;ka_advancedJoints.makeAdvancedIkSplineUI()
                        self.menu.addMenuItem( 'advanced ik Spline', command=cmd )

                        self.menu.addSeparatorItem(label='print recreate command')

                        def cmd(): importlib.reload(ka_advancedJoints) ;ka_advancedJoints.printCommand_procedurallyCreateMuscleJoint()
                        self.menu.addMenuItem( 'print piston JointMuscle', command=cmd )

                        def cmd(): importlib.reload(ka_advancedJoints) ;ka_advancedJoints.printCommand_procedurallyCreateBendMuscleJoint()
                        self.menu.addMenuItem( 'print ligament JointMuscle', command=cmd )

                        self.menu.addSeparatorItem(label='edit existing')

                        def cmd(): importlib.reload(ka_advancedJoints) ;ka_advancedJoints.makeAdvancedIkSplineUI()
                        self.menu.addMenuItem( 'pistonJointMuscle: set inital length', command=cmd )

                        #def cmd(): reload(ka_advancedJoints); ka_advancedJoints.makeRibonFromTransforms()
                        #self.menu.addMenuItem( 'Make Ribon From Transforms', command=cmd )



                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                # Selection
                if selection:
                    if self.menu.addSubmenuItem('Selection: ', icon='Selection.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        def cmd(): from .. import ka_filterSelection  #;reload(ka_filterSelection)  ;ka_filterSelection.openUI();
                        self.menu.addMenuItem( 'Selection Filter Tool', command=cmd )

                        def cmd(): mel.eval('ka_invertSelectionOrder')
                        self.menu.addMenuItem( 'Inverse Selection Order', command=cmd )

                        def cmd(): ka_util.filterSelection()
                        self.menu.addMenuItem( 'Filter Selection', command=cmd )

                        def cmd():
                            import ka_rigTools.ka_selection as ka_selection; importlib.reload(ka_selection)
                            ka_selection.islandSelectComponents()
                        self.menu.addMenuItem( 'Island Select Component', command=cmd )

                        def cmd(): ka_weightPainting.selectParallelVertsDict(selectGroup='top')
                        self.menu.addMenuItem( 'select upper paralell vert loop', command=cmd )

                        def cmd(): ka_weightPainting.selectParallelVertsDict(selectGroup='bottom')
                        self.menu.addMenuItem( 'select lower paralell vert loop', command=cmd )

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                # Display
                if self.menu.addSubmenuItem('Display: ', icon='visibility'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                    def cmd(): ka_display.hideAllRotationAxis()
                    self.menu.addMenuItem( 'Rotation Axis Off on ALL', command=cmd )

                    def cmd(): ka_display.isolateSelection(mode='skinning')
                    self.menu.addMenuItem( 'Isolate Selection + Influences: ', command=cmd )

                    def cmd(): ka_display.toggleColorWireframeOnSelected()
                    self.menu.addMenuItem( 'Colored Wireframe on Effected', command=cmd )

                    def cmd(): ka_display.ka_disableDrawingOverideOnSelection(enable=False)
                    self.menu.addMenuItem( 'disable Drawing Overide on Selection', command=cmd )

                    def cmd(): ka_display.ka_disableDrawingOverideOnSelection(enable=True)
                    self.menu.addMenuItem( 'enable Drawing Overide on Selection', command=cmd )

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]



                # Deformers
                if selection:
                    if self.menu.addSubmenuItem('deformers: ', icon='deformers.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        if self.menu.addSubmenuItem('skinning: '): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                            def cmd():
                                ka_skinCluster.setSetJointLabelFromNameOnAll()
                                ka_weightPainting.mirrorWeights()
                            self.menu.addMenuItem( 'Mirror Weights: ', command=cmd, icon='symmetry.png')

                            def cmd(): ka_display.isolateSelection(mode='skinning')
                            self.menu.addMenuItem( 'Isolate Selection + Influences: ', command=cmd, icon='isolateSelection.png')

                            self.menu.addSeparatorItem()  #---------------------------------------------------------

                            def cmd(): ka_weightPainting.resetSkin("reset")
                            self.menu.addMenuItem( 'Reset Bind Pose: ', command=cmd )

                            def cmd(): ka_weightPainting.resetSkin("bake")
                            self.menu.addMenuItem( 'Bake as Bind Pose: ', command=cmd )

                            def cmd(): ka_weightPainting.deleteAllBindPoses()
                            self.menu.addMenuItem( 'Delete All Bind Pose Nodes: ', command=cmd )

                            self.menu.addSeparatorItem()  #---------------------------------------------------------

                            self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                        def cmd(): ka_util.clusterDeformSelection()
                        self.menu.addMenuItem( 'cluster deform selection[1:] to selection[0]', command=cmd )

                        def cmd(): ka_util.helixCluster()
                        self.menu.addMenuItem( 'cluster on helix selection', command=cmd )

                        # Blend Shapes
                        if selectionMain_shapeType == 'mesh':
                            if self.menu.addSubmenuItem('Blend Shapes: '): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                                def cmd(): mel.eval('Copy over Flipped Shape;')
                                self.menu.addMenuItem( 'Copy over Flipped Shape', command=cmd )

                                def cmd(): mel.eval('mel.eval("abSymCtl(\"msBn\")")')
                                self.menu.addMenuItem( 'abSymMesh Mirror', command=cmd )

                                def cmd(): mel.eval('abSymCtl(\"fsBn\");')
                                self.menu.addMenuItem( 'abSymMesh Flip', command=cmd )

                                self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]




                # Transforms
                if selection:
                    if self.menu.addSubmenuItem('Transforms: ', icon='xyz.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        # Freeze
                        if selection:
                            if self.menu.addSubmenuItem('Freeze: ', icon='Snowflake.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                                def cmd(): mel.eval("makeIdentity -apply true -t 1 -r 0 -s 0 -n 0;")
                                self.menu.addMenuItem( 'Translate', command=cmd )

                                def cmd(): mel.eval("makeIdentity -apply true -t 0 -r 1 -s 0 -n 0;")
                                self.menu.addMenuItem( 'Rotate', command=cmd )

                                def cmd(): mel.eval("makeIdentity -apply true -t 0 -r 0 -s 1 -n 0;")
                                self.menu.addMenuItem( 'Scale', command=cmd )

                                def cmd(): mel.eval("makeIdentity -apply true -t 1 -r 1 -s 1 -n 0;")
                                self.menu.addMenuItem( 'All', command=cmd )

                                def cmd(): mel.eval("makeIdentity -apply true -t 1 -r 0 -s 0 -n 1;")
                                self.menu.addMenuItem( 'Joint Rotation', command=cmd )

                                def cmd(): ka_util.freezePivotPosition()
                                self.menu.addMenuItem( 'Local Pivot', command=cmd )

                                self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                        def cmd(): ka_util.removeNonStandardTransformValues()
                        self.menu.addMenuItem( 'remove non-standard transform values', command=cmd )

                        # joints
                        if selectionMain_objectType == 'joint':

                            def cmd(): mel.eval("OrientJointOptions;")
                            self.menu.addMenuItem( 'Orient Joint', command=cmd )

                            #def cmd(): mel.eval("ka_removeJointOrientation;")
                            def cmd(): ka_util.removeJointOrients()
                            self.menu.addMenuItem( 'Unorient Joint', command=cmd )

                            def cmd(): mel.eval("MirrorJointOptions;")
                            self.menu.addMenuItem( 'Mircror Joint', command=cmd )

                            def cmd(): mel.eval("makeIdentity -apply true -t 0 -r 1 -s 0 -n 0;")
                            self.menu.addMenuItem( 'Freeze Joint Rotations', command=cmd )

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                # Transfer Tools
                if multiSelect:
                    if self.menu.addSubmenuItem('Transfer Tools: ', icon='transfer.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        def cmd(): ka_weightPainting.xferSkin()
                        self.menu.addMenuItem( 'Transfer Skin', command=cmd )

                        def cmd(): ka_weightPainting.xferComponentWeights()
                        self.menu.addMenuItem( 'Transfer Skin to Skinned Component Selection', command=cmd )

                        def cmd(): mel.eval('print \"no command yet\"')
                        self.menu.addMenuItem( 'Transfer UVs (component)', command=cmd )

                        def cmd(): mel.eval('print \"no command yet\"')
                        self.menu.addMenuItem( 'Transfer UVs (worldSpace)', command=cmd )

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                # Copy / Paste
                if selection:
                    if self.menu.addSubmenuItem('Copy / Paste: ', icon='clipboard.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        if self.menu.addSubmenuItem('Weights: '): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                            #widget = QtGui.QPushButton('hi', self.menu.menu)
                            #self.menu.addWidgetMenuItem(widget)

                            weightBlenderWidget = ka_qtWidgets.WeightBlenderWidget(self.menu.menu)
                            self.menu.addWidgetMenuItem(weightBlenderWidget)

                            self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                        if self.menu.addSubmenuItem('Shapes: '): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                            def cmd(): mel.eval('ka_copyShape')
                            self.menu.addMenuItem( 'Copy Shape', command=cmd )

                            def cmd(): mel.eval('ka_pasteShape("")')
                            self.menu.addMenuItem( 'Paste Shape', command=cmd )

                            def cmd(): mel.eval('ka_pasteShape("flipped")')
                            self.menu.addMenuItem( 'Paste Shape Flipped', command=cmd )

                            def cmd(): mel.eval('ka_pasteShape("reversed")')
                            self.menu.addMenuItem( 'Paste Shape Reversed', command=cmd )

                            self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]



                # Color
                if selection:
                    if self.menu.addSubmenuItem('Color: ', icon='colorPallet.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[


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

                        # my Colors
                        for rgbColor, label in favoriteColors:
                            r, g, b = rgbColor
                            #r, g, b = pymel.colorIndex( i, q=True )

                            def cmd(rgbColor=rgbColor): ka_util.colorObjects(color=rgbColor)
                            self.menu.addMenuItem( '%s' % label, command=cmd, colorIcon=[r,g,b])

                        self.menu.addSeparatorItem()  #---------------------------------------------------------

                        # All Colors
                        for i in range(32):
                            if i == 0:
                                def cmd(): mel.eval("kaRig_colourSelection \"black\";")
                                self.menu.addMenuItem( '#%s None' % str(i), command=cmd,)

                            else:
                                rgb = pymel.colorIndex( i, q=True )

                                def cmd(i=i): ka_util.colorObjects(index=i)
                                self.menu.addMenuItem( '#%s' % str(i), command=cmd, colorIcon=rgb)

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                # Lock / Unlock
                if selection:
                    if self.menu.addSubmenuItem('Lock / Unlock: ', icon='lock.png',): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        # Lock
                        if self.menu.addSubmenuItem('Lock: ', icon='lock.png',): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                            def cmd(): mel.eval("kaRig_AttrLock \"\" \"t\"")
                            self.menu.addMenuItem( 'Translate', command=cmd, icon='lock.png', )

                            def cmd(): mel.eval("kaRig_AttrLock \"\" \"r\"")
                            self.menu.addMenuItem( 'Rotate', command=cmd, icon='lock.png', )

                            def cmd(): mel.eval("kaRig_AttrLock \"\" \"s\"")
                            self.menu.addMenuItem( 'Scale', command=cmd, icon='lock.png', )

                            def cmd(): mel.eval("kaRig_AttrLock \"\" \"v\"")
                            self.menu.addMenuItem( 'Visibility', command=cmd, icon='lock.png', )

                            def cmd(): mel.eval("kaRig_AttrLock \"\" \"\"")
                            self.menu.addMenuItem( 'All', command=cmd, icon='lock.png', )

                            self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                            # Unlock
                            if self.menu.addSubmenuItem('Unlock: ', icon='unlock.png',): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                                def cmd(): mel.eval("kaRig_AttrUnlock \"\" \"t\"")
                                self.menu.addMenuItem( 'Translate', command=cmd, icon='unlock.png' )

                                def cmd(): mel.eval("kaRig_AttrUnlock \"\" \"r\"")
                                self.menu.addMenuItem( 'Rotate', command=cmd, icon='unlock.png' )

                                def cmd(): mel.eval("kaRig_AttrUnlock \"\" \"s\"")
                                self.menu.addMenuItem( 'Scale', command=cmd, icon='unlock.png' )

                                def cmd(): mel.eval("kaRig_AttrUnlock \"\" \"v\"")
                                self.menu.addMenuItem( 'Visibility', command=cmd, icon='unlock.png' )

                                def cmd(): mel.eval("kaRig_AttrUnlock \"\" \"\"")
                                self.menu.addMenuItem( 'All', command=cmd, icon='unlock.png' )

                                self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]




                # Hierarchy
                if selection:
                    if self.menu.addSubmenuItem('Hierarchy: ', icon='groups.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        def cmd(): mel.eval("ka_zeroOutGroup")
                        self.menu.addMenuItem( 'Adjust Group', command=cmd )

                        def cmd(): ka_transforms.makeZroGroup()
                        self.menu.addMenuItem( 'Zro/Buffer Group', command=cmd )

                        def cmd(): mel.eval("ka_shadowGroup")
                        self.menu.addMenuItem( 'Shadow Group', command=cmd )

                        def cmd(): ka_util.shapeParent()
                        self.menu.addMenuItem( 'Parent Shape', command=cmd )

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                # Constrain
                if multiSelect:
                    if self.menu.addSubmenuItem('Constrain: ', icon='pointConstraint.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        #def cmd(): mel.eval("ka_constrain(\"pointAndOrient\", \"normal\", \"\")")
                        #self.menu.addMenuItem( 'Point, Orient', command=cmd )

                        #def cmd(): mel.eval("ka_constrain(\"pointAndOrient\", \"normal\", \"\")")
                        #self.menu.addMenuItem( 'Point, Orient, Scale', command=cmd )

                        #def cmd(): mel.eval("ka_constrain(\"pointAndOrient\", \"normal\", \"\")")
                        #self.menu.addMenuItem( 'Point, Orient (with offset)', command=cmd )

                        #def cmd(): mel.eval("ka_constrain(\"pointAndOrientAndScale\", \"normal\", \"\")")
                        #self.menu.addMenuItem( 'Point, Orient, Scale (with offset)', command=cmd )

                        #def cmd(): mel.eval("ka_constrain(\"pointOnSurface\", \"normal\", \"\")")
                        #self.menu.addMenuItem( 'Point on Surface', command=cmd )

                        #def cmd(): mel.eval("ka_constrain(\"pointOnSurface\", \"normal\", \"\")")

                        def cmd():
                            importlib.reload(ka_util)
                            ka_constraints.constrain(pointOnSurface=True)
                        self.menu.addMenuItem( 'Surface Constraint', command=cmd )

                        def cmd():
                            importlib.reload(ka_util)
                            ka_constraints.constrain(aimBetween=True)
                        self.menu.addMenuItem( 'Aim Between', command=cmd )

                        def cmd(): ka_constraints.constrain(t=True, r=True)
                        self.menu.addMenuItem( 'Point, Orient', command=cmd )

                        def cmd(): ka_constraints.constrain(t=True, r=True, s=True)
                        self.menu.addMenuItem( 'Point, Orient, Scale', command=cmd )

                        def cmd(): ka_constraints.constrain(t=True, r=True, withOffset=True)
                        self.menu.addMenuItem( 'Point, Orient (with offset)', command=cmd )

                        def cmd(): ka_constraints.constrain(t=True, r=True, s=True, withOffset=True)
                        self.menu.addMenuItem( 'Point, Orient, Scale (with offset)', command=cmd )

                        def cmd():
                            importlib.reload(ka_util)
                            ka_constraints.constrain(pointOnSurface=True, withOffset=True)
                        self.menu.addMenuItem( 'Point to Surface (with offset)', command=cmd )

                        #def cmd(): ka_constraints.constrain(t=True, r=True)
                        #self.menu.addMenuItem( 'Point on Surface', command=cmd )

                        #def cmd(): ka_constraints.constrain(t=True, r=True)
                        #self.menu.addMenuItem( 'Orient to Surface', command=cmd )

                        if selectionMain_shapeType == 'nurbsCurve':
                            def cmd(): mel.eval('ka_pointOnCurveConstraint')
                            self.menu.addMenuItem( 'Point on Curve Constraint', command=cmd )


                        def cmd(): ka_util.jointOrientContraint()
                        self.menu.addMenuItem( 'constrain jointOrient', command=cmd )

                        def cmd(): ka_util.distanceBetweenToTranslateX()
                        self.menu.addMenuItem( 'connect translate X to distanceBetween sel 1&2', command=cmd )

                        def cmd():
                            importlib.reload(ka_advancedJoints)
                            ka_advancedJoints.distanceBetweenToTranslateX()
                        self.menu.addMenuItem( 'Transform Net Constraint', command=cmd )

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                # Snap
                if multiSelect:
                    if self.menu.addSubmenuItem('Snap: ', icon='magnet'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        def cmd(): ka_transforms.snap(t=1)
                        self.menu.addMenuItem( 'snap translate', command=cmd )

                        def cmd(): ka_transforms.snap(r=1)
                        self.menu.addMenuItem( 'snap rotate', command=cmd )

                        def cmd(): ka_transforms.snap(s=1)
                        self.menu.addMenuItem( 'snap scale', command=cmd )

                        def cmd(): ka_transforms.snap(a=1)
                        if self.menu.addSubmenuItem( 'snap aim', command=cmd ):

                            self.menu.addSeparatorItem(label='Command Options:')
                            self.menu.addMenuItem('Primary Axis:')
                            self.menu.prefMenuItem_radioButtons('snapToolPrimaryAxis', ['  x', ' -x', '  y', ' -y', '  z', ' -z'], 0)

                            self.menu.addMenuItem('secondary Axis:')
                            self.menu.prefMenuItem_radioButtons('snapToolSecondaryAxis', ['  x', ' -x', '  y', ' -y', '  z', ' -z'], 0)

                            self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                        def cmd(): ka_transforms.snap(m=1)
                        self.menu.addMenuItem( 'snap mirror', command=cmd )


                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                # Misc
                if self.menu.addSubmenuItem('Misc: ', icon='misc.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                    if self.menu.addSubmenuItem('Print Commands: '): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        def cmd(): ka_util.printSelection_asPythonList()
                        self.menu.addMenuItem( 'Print SELECTION as Python List', command=cmd )

                        def cmd(): ka_util.printSelectedCurveCreationCommand()
                        self.menu.addMenuItem( 'Print CURVE Create Command', command=cmd )

                        def cmd(): ka_util.printMeshCreateCmd()
                        self.menu.addMenuItem( 'Print MESH Create Command', command=cmd )

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                    def cmd(): mel.eval("ka_deleteBindPoses;")
                    self.menu.addMenuItem( 'delete all bindPose nodes', command=cmd )

                    def cmd(): mel.eval("findLatticeDeformersLatticeCage;")
                    self.menu.addMenuItem( 'find Lattice Deformers Lattice Cage', command=cmd )

                    def cmd(): ka_util.deleteAllKeyframes()
                    self.menu.addMenuItem( 'Delete All Time based Keyframes', command=cmd )


                    def cmd(): ka_skinCluster.setSetJointLabelFromName()
                    self.menu.addMenuItem( 'Set Joint Label From Name', command=cmd )

                    def cmd(): ka_skinCluster.setSetJointLabelFromNameOnAll()
                    self.menu.addMenuItem( 'Set Joint On ALL Influences', command=cmd )

                    def cmd(): ka_util.reorderAllShapesToTopOfTheirHierchy()
                    self.menu.addMenuItem( 'reorder All Shapes To Top Of Their Hierchy', command=cmd )

                    def cmd(): ka_util.makeSurfaceConstraint_useTangetV()
                    self.menu.addMenuItem( 'make Suface Constraints use tangetV as upVector', command=cmd )

                    def cmd(): ka_util.makeSurfaceConstraint_useTangetU()
                    self.menu.addMenuItem( 'make Suface Constraints use tangetU as upVector', command=cmd )

                    def cmd(): ka_util.helixParent()
                    self.menu.addMenuItem( 'helixParent', command=cmd )

                    def cmd(): ka_util.renameAllShapes()
                    self.menu.addMenuItem( 'auto-name all shapes', command=cmd )

                    def cmd(): importlib.reload(ka_util); ka_util.aimSnap()
                    self.menu.addMenuItem( 'Aim snap', command=cmd )

                    def cmd(): importlib.reload(ka_advancedJoints); ka_advancedJoints.setPoseDriverPose()
                    self.menu.addMenuItem( 'Set Pose', command=cmd )

                    def cmd(): importlib.reload(ka_advancedJoints); ka_advancedJoints.updateClosestPose()
                    self.menu.addMenuItem( 'Update Pose', command=cmd )

                    def cmd(): importlib.reload(ka_advancedJoints); ka_advancedJoints.createJointNet()
                    self.menu.addMenuItem( 'create Joint Net', command=cmd )

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                # Tools
                if self.menu.addSubmenuItem('Tools: ', icon='tools.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                    def cmd(): from .. import ka_rename  #;reload(ka_rename)  ;ka_rename.openUI()
                    self.menu.addMenuItem( 'Rename Tool', command=cmd )

                    def cmd(): from .. import ka_filterSelection  #;reload(ka_filterSelection)  ;ka_filterSelection.openUI();
                    self.menu.addMenuItem( 'Filter Selection Tool', command=cmd )

                    def cmd(): importlib.reload(ka_attrTool);  ka_attrTool.openUI()
                    self.menu.addMenuItem( 'Attr Tool', command=cmd )

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                # Info
                if self.menu.addSubmenuItem('Info: ', icon='info.png',): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                    if self.menu.addSubmenuItem('%s items selected: ' % str(len(selection))): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        for item in selection:
                            if self.menu.addSubmenuItem('%s ' % item,): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                                self.menu.addMenuItem( 'nodeType: %s' % pymel.nodeType(item), )

                                self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                # Options
                if self.menu.addSubmenuItem('Options: ', icon='settings.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                    if self.menu.addSubmenuItem('scrubSlider Tool Options: '): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        self.menu.addSeparatorItem(label='scrubSlider Options:')
                        self.menu.addMenuItem('scrubSlider Mode:')
                        self.menu.prefMenuItem_radioButtons('scrubSliderMode', ['  toggle', ' clickDrag',], 0)

                        self.menu.addMenuItem('scrubSlider Indicators:')

                        self.menu.prefMenuItem_checkbox('Slider Vis', 'scrubSlider_sliderVisable', 1)
                        self.menu.prefMenuItem_checkbox('Slider Value Box Vis', 'scrubSlider_sliderValueVisable', 1)

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                    if self.menu.addSubmenuItem('Snap Aim Options: '): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        self.menu.addSeparatorItem(label='Command Options:')
                        self.menu.addMenuItem('Primary Axis:')
                        self.menu.prefMenuItem_radioButtons('snapToolPrimaryAxis', ['  x', ' -x', '  y', ' -y', '  z', ' -z'], 0)

                        self.menu.addMenuItem('secondary Axis:')
                        self.menu.prefMenuItem_radioButtons('snapToolSecondaryAxis', ['  x', ' -x', '  y', ' -y', '  z', ' -z'], 0)

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


