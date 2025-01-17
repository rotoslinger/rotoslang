#====================================================================================
#====================================================================================
#
# ka_menu_modelEditor
#
# DESCRIPTION:
#   sets up a context sesitive popup menu while a specified hotkey is held down
#
# DEPENDENCEYS:
#   a hotkey to build menu must use ka_rigTools.ka_menu.press()as the command and
#   be held down during left click. The release hotkey for this button must use
#   ka_rigTools.ka_menu.release()as the command
#
#   ka_weightPainting
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
import re
from traceback import format_exc as printError

import sip
import PyQt4
from PyQt4 import QtGui, QtCore, uic

import maya.cmds as cmds
import pymel.core as pymel
import maya.mel as mel

from .. import ka_util                                              #;reload(ka_util)
from .. import ka_hyperShade                                        #;reload(ka_hyperShade)
import ka_rigTools.ka_attrTool.ka_attrTool_UI as ka_attrTool_UI     #;reload(ka_attrTool_UI)
import ka_rigTools.ka_attrTool.attrCommands as attrCommands         #;reload(attrCommands)
from .. import ka_preference                                        #;reload(ka_preference)
import importlib
#from ..ka_attrTool import attrCommands                     #;reload(attrCommands)

#from ka_util import undoable, repeatable #decorators
undoable = ka_util.undoable
repeatable = ka_util.repeatable #decorators

class Menu():
    '''menu items specific to actions in the maya viewport'''
    def __init__(self, menu):
        self.menu = menu

        #def build_menu_hyperShade(self):
    def populateMenu(self, **kwargs):
        '''more or less acting as the __init__'''

        self.hyperShadeMenu()

    def hyperShadeMenu(self):###########################################################################################################################################################################################################################################################
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ####################################################################################################################################################################################################################################################################################
        hypergraph = "graph1HyperShadeEd"
        nodeUnderMouse = pymel.hyperGraph(hypergraph, query=True, feedbackNode=True,)

        if nodeUnderMouse:
            nodeUnderMouse = pymel.ls(nodeUnderMouse)[0] #return shortest unique name

            node = nodeUnderMouse
            node_type = None
            node_Shape = None
            node_shapeType = None

            node_type = pymel.nodeType(node)
            node_Shape = pymel.listRelatives(node, shapes=True)
            if node_Shape:
                node_Shape = node_Shape[0] #nessisary to convert var from list to item here, to prevent error if None
                node_shapeType = pymel.nodeType(node_Shape)


        else:
            node = pymel.ls(selection=True)
            if node:
                node = node[0]


        if nodeUnderMouse:

            importlib.reload(ka_attrTool_UI);
            pyNodeUnderMouse = pymel.ls(nodeUnderMouse)
            if pyNodeUnderMouse:
                if len(pyNodeUnderMouse) == 1:
                    attrTool_QWidgetAction = ka_attrTool_UI.AttrTool_quickConnectPopup(self.menu.menu, selection=pyNodeUnderMouse)
                    self.menu.menu.addAction(attrTool_QWidgetAction)

        else:
            if node:
                def cmd():
                    importlib.reload(ka_attrTool_UI);  ka_attrTool_UI.openUI()
                self.menu.addMenuItem('Attr Tool', icon='plug.png', command=cmd )

                self.menu.addSeparatorItem()  #---------------------------------------------------------

                def cmd(): ka_hyperShade.alignNodes('vertical')
                self.menu.addMenuItem( 'Align Nodes Vertical', icon='alignVertical.png', command=cmd )

                def cmd(): ka_hyperShade.alignNodes('horizontal')
                self.menu.addMenuItem( 'Align Nodes Horizontal', icon='alignHorizontal.png', command=cmd )

            def cmd(): ka_hyperShade.clear()
            self.menu.addMenuItem( 'Clear Graph', icon='clear.png', command=cmd )

            def cmd():
                importlib.reload(ka_hyperShade)
                ka_hyperShade.isolateInGraph()
            self.menu.addMenuItem( 'isolate In Graph', icon='clear.png', command=cmd )

            if node:
                def cmd(): mel.eval("ka_hgAdd")
                self.menu.addMenuItem( 'Add Selected to Graph', icon='add.png', command=cmd )

                self.menu.addSeparatorItem()  #---------------------------------------------------------

                def cmd(): importlib.reload(attrCommands) ;attrCommands.duplicateSelection()
                self.menu.addMenuItem( 'Duplicate (with connections)', icon='duplicate.png', command=cmd )

                def cmd(): importlib.reload(attrCommands) ;attrCommands.eccoAttrsPymelObjectOriented()
                self.menu.addMenuItem( 'Echo re-Create Commands', command=cmd )

                def cmd(): importlib.reload(attrCommands) ;attrCommands.eccoAttrsPymelObjectOriented()
                self.menu.addMenuItem( 'Substitute Node', command=cmd )

                self.menu.addSeparatorItem()  #---------------------------------------------------------

            if not nodeUnderMouse:
                if self.menu.addSubmenuItem('create Node: ', icon='create.png'): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                    createNodeTypesList = ['choice', 'multiplyDivide', 'blendColors', 'condition', 'setRange', 'plusMinusAverage', 'blendTwoAttr', 'distanceBetween', 'pointOnCurveInfo', 'curveInfo', 'pointOnSurfaceInfo', 'surfaceInfo', 'closestPointOnSurface', 'angleBetween', 'vectorProduct', 'arrayMapper', 'bump2d', 'bump3d', 'heightField', 'lightInfo', 'place2dTexture', 'place3dTexture', 'projection', 'reverse', 'samplerInfo', 'stencil', 'uvChooser', 'animCurveUU', 'animCurveUA', 'animCurveUL', 'animCurveUT', 'closestPointOnMesh', 'remapValue',]
                    for eachNodeType in sorted(createNodeTypesList):
                        if 'animCurve' in eachNodeType:
                            def cmd(nodeType=eachNodeType):
                                node = pymel.createNode(nodeType)
                                ka_hyperShade.addKeysToAnimCurveNode(node)

                        else:
                            def cmd(nodeType=eachNodeType):
                                node = pymel.createNode(nodeType)

                        self.menu.addMenuItem( eachNodeType, command=cmd )

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                #def cmd(): ka_hyperShade.contain('dag')
                #self.menu.addMenuItem( 'Contain', icon='contain.png', command=cmd )

                self.menu.addSeparatorItem()  #---------------------------------------------------------

                def cmd(): ka_hyperShade.graphInputOutput(mode='inputs', depthLimit=ka_preference.get('hypherShade_graphDepthInputs', 0)+3)
                if self.menu.addSubmenuItem( 'Graph Inputs', command=cmd, icon='graphIn.png'):

                    self.menu.addSeparatorItem(label='Command Options:')

                    self.menu.addMenuItem('Depth To Graph Inputs:')
                    self.menu.prefMenuItem_radioButtons('hypherShade_graphDepthInputs', ['  1', '  2', '  3', '  4', '  5', '  6',], 0)

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                def cmd(): ka_hyperShade.graphInputOutput(mode='outputs', depthLimit=ka_preference.get('hypherShade_graphDepthOutputs', 0)+3)
                if self.menu.addSubmenuItem( 'Graph Outputs', command=cmd, icon='graphOut.png' ):

                    self.menu.addSeparatorItem(label='Command Options:')

                    self.menu.addMenuItem('Depth To Graph Outputs:')
                    self.menu.prefMenuItem_radioButtons('hypherShade_graphDepthOutputs', ['  1', '  2', '  3', '  4', '  5', '  6',], 0)

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                def cmd(): ka_hyperShade.graphInputOutput(depthLimit=ka_preference.get('hypherShade_graphDepthInputsAndOutputs', 0)+3)
                if self.menu.addSubmenuItem( 'Graph Inputs & Outputs', command=cmd, icon='graphInOut.png' ):

                    self.menu.addSeparatorItem(label='Command Options:')

                    self.menu.addMenuItem('Depth To Graph Inputs & Outputs:')
                    self.menu.prefMenuItem_radioButtons('hypherShade_graphDepthInputsAndOutputs', ['  1', '  2', '  3', '  4', '  5', '  6',], 0)

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                if self.menu.addSubmenuItem( 'Max Number of Nodes to Graph',):
                    def cmd():
                        radioValues = [25, 50, 100, 250, 500, 1000]
                        ka_preference.add('hyperGraph_maxGraphSize', radioValues[ka_preference.get('hyperGraph_maxGraphSizeRadioValue')])
                        #OOOOOOO = 'ka_preference.get("hyperGraph_maxGraphSize")';  print '%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO))))
                    self.menu.prefMenuItem_radioButtons('hyperGraph_maxGraphSizeRadioValue', ['  25', '  50', '  100', '  250', '  500', '  1000',], 2, command=cmd)

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]


                self.menu.addSeparatorItem()  #---------------------------------------------------------

                if self.menu.addSubmenuItem('Misc: ',): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                    def cmd(): ka_hyperShade.selectInputOutput(mode='inputs')
                    self.menu.addMenuItem( 'Select Inputs', command=cmd )

                    def cmd(): ka_hyperShade.selectInputOutput(mode='outputs')
                    self.menu.addMenuItem( 'Select Outputs', command=cmd )

                    def cmd(): ka_hyperShade.selectInputOutput()
                    self.menu.addMenuItem( 'Select Inputs and Outputs', command=cmd )


                    def cmd(): ka_util.filterSelection()
                    self.menu.addMenuItem( 'Filter Selection', command=cmd )

                    def cmd(): ka_hyperShade.addKeysToAnimCurveNode()
                    self.menu.addMenuItem( 'addKeysToAnimCurveNode', command=cmd )

                    if self.menu.addSubmenuItem('convertAnimCurvesTo: ',): #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[

                        def cmd(): ka_util.convertSelectedAnimCurveTo(targetType='animCurveUA')
                        self.menu.addMenuItem( 'animCurveUA', command=cmd )

                        def cmd(): ka_util.convertSelectedAnimCurveTo(targetType='animCurveUU')
                        self.menu.addMenuItem( 'animCurveUA', command=cmd )

                        def cmd(): ka_util.convertSelectedAnimCurveTo(targetType='animCurveUU')
                        self.menu.addMenuItem( 'animCurveUL', command=cmd )

                        def cmd(): ka_util.convertSelectedAnimCurveTo(targetType='animCurveUU')
                        self.menu.addMenuItem( 'animCurveUT', command=cmd )

                        self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                    self.menu.endSubmenuItem()#]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

                if node:
                    if pymel.nodeType(node) == 'plusMinusAverage':
                        def cmd(): ka_hyperShade.addInputToPlusMinus(node)
                        self.menu.addMenuItem( 'add input to 1D inputs', command=cmd )










#global proc ka_hgMM_setAnimCurveDefaultKeys(string $animCurve)
#{
#    setKeyframe -insert -float 0 $animCurve;
#    setKeyframe -insert -float 1 $animCurve;
#}






## GET RELATED NODES:
#vectorProduct39__3ai83s__ = pymel.ls('vectorProduct39')[0]



### CREATE NODES: ##
#animCurveUU9__3c9f74__ = pymel.createNode('animCurveUU', )
#animCurveUU9__3c9f74__.rename('animCurveUU9')



### SET ATTRS: ##
#animCurveUU9__3c9f74__.keyTanInType[1].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[2].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[5].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[6].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[7].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[8].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[9].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[10].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[11].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[12].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[13].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[14].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[15].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[16].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[17].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[18].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[19].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[20].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[21].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[22].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[23].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[24].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[25].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[26].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanInType[27].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[0].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[1].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[2].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[5].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[6].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[7].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[8].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[9].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[10].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[11].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[12].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[13].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[14].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[15].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[16].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[17].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[18].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[19].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[20].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[21].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[22].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[23].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[24].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[25].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[26].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[27].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanLocked[28].set(False, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[1].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[2].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[5].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[6].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[7].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[8].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[9].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[10].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[11].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[12].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[13].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[14].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[15].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[16].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[17].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[18].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[19].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[20].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[21].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[22].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[23].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[24].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[25].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[26].set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.keyTanOutType[27].set(9, keyable=False, channelBox=False, lock=False, )
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=6.31375169754, float=-0.987688362598)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=3.57280226361, float=-0.962688326836)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=2.70518822872, float=-0.937688350677)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=1.42202978387, float=-0.81768989563)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=0.974567582953, float=-0.697691440582)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=0.514892541264, float=-0.457694470882)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=0.223051743041, float=-0.217697530985)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=0.0981848903144, float=-0.0976990610361)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=0.0377371079827, float=-0.0376998260617)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=0.00770401038631, float=-0.00770020857453)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-0.0223104187645, float=0.0222994089127)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-0.271920693514, float=0.262296378613)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-0.413900368347, float=0.382294863462)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-0.493372125415, float=0.442294120789)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-0.53604708554, float=0.47229373455)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-0.581100152223, float=0.502293348312)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-0.79542840161, float=0.62229180336)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-0.933484851289, float=0.682291030884)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-1.01538712763, float=0.712290644646)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-1.10861097144, float=0.742290258408)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-1.34528399166, float=0.802289485931)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-1.50295072776, float=0.832289099693)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-1.70363566728, float=0.862288713455)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-1.97768159794, float=0.892288327217)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-2.39188034094, float=0.922287940979)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-3.12623804911, float=0.952287554741)
#pymel.setKeyframe(animCurveUU9__3c9f74__, value=-5.2421836853, float=0.982287228107)
#animCurveUU9__3c9f74__.tangentType.set(9, keyable=False, channelBox=False, lock=False, )
#animCurveUU9__3c9f74__.weightedTangents.set(False, keyable=False, channelBox=False, lock=False, )




### CONNECT ATTRS: ##
#vectorProduct39__3ai83s__.output.outputX >> animCurveUU9__3c9f74__.input



