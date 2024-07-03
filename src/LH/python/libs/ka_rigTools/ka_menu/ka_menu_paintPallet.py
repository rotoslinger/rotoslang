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
import traceback #import print_exc #as printError
import sys
def printError():
    traceback.print_exc(limit=20)

import sip
import PyQt4
from PyQt4 import QtGui, QtCore, uic
#from PyQt4 import *

import maya.cmds as cmds
import pymel.core as pymel
import maya.mel as mel

from .. import ka_weightPainting                          #;reload(ka_weightPainting)
from .. import ka_util                                          #;reload(ka_util)


class Menu():
    '''menu items specific to actions in the maya viewport'''
    def __init__(self, menu):
        self.menu = menu

    def populateMenu(self, **kwargs):
        '''more or less acting as the __init__'''

        if 'sliderMode' in kwargs:
            sliderMode = kwargs['sliderMode']

        else:
            sliderMode = 'parallelBlend'

        #Create Widget
        newQAction = QtGui.QWidgetAction(self.menu.currentMenu)
        self.spinBox = None

        width = 400

        QGroupBox = QtGui.QGroupBox('Paint Pallet', self.menu.currentMenu)

        def setPaintWeight(value, addMode=False):
            if not addMode:
                cmds.artAttrSkinPaintCtx('artAttrSkinContext', value=value, edit=True,)
                self.spinBox.setValue(value)
            else:
                previousValue = cmds.artAttrSkinPaintCtx('artAttrSkinContext', value=True, query=True,)
                value = previousValue + value
                cmds.artAttrSkinPaintCtx('artAttrSkinContext', value=value, edit=True,)

            self.spinBox.setValue(value)
            colorWidget(self.spinBox, value=[value, value, value])

        def colorWidget(widget, value=None, color=None):
            if color or value:
                textColor = []
                if value:
                    color = [225*value[0], 225*value[1], 225*value[2], ]

                    if value[0]+value[1]+value[2] <= 1.5:
                        textColor = [225, 225, 225]
                    else:
                        textColor = [0, 0, 0]

                    textColor = QtGui.QColor(textColor[0], textColor[1], textColor[2],)
                color = QtGui.QColor(color[0], color[1], color[2],)


                palette = QtGui.QPalette()
                palette.setColor(QtGui.QPalette.Button, color)
                palette.setColor(QtGui.QPalette.Base, color)

                if textColor:
                    palette.setColor(QtGui.QPalette.ButtonText, textColor)
                    palette.setColor(QtGui.QPalette.Text, textColor)
                    palette.setColor(QtGui.QPalette.Shadow, textColor)

                widget.setPalette(palette)
                widget.setAutoFillBackground(True)

        def addToRow(widget, posy, width, height, icon='', color=[], value=[], weightValue=None, weightAdd=None, cmd=None):
            widget.move(self.currentXPos, posy)
            widget.setFixedSize(width, height)
            self.currentXPos = self.currentXPos + width

            if not weightValue == None:
                value = [weightValue, weightValue, weightValue]
                def cmd(): setPaintWeight(weightValue)
                #self.menu.currentMenu.connect(widget, QtCore.SIGNAL('clicked()'), cmd)

            elif not weightAdd == None:
                def cmd(): setPaintWeight(weightAdd, addMode=True)
                if weightAdd < 0:
                    color = [0, 25, 100]
                else:
                    color = [100, 25, 0]

            if cmd:
                self.menu.currentMenu.connect(widget, QtCore.SIGNAL('clicked()'), cmd)



            if icon:
                button.setIcon(QtGui.QIcon(self.iconFolder+icon))
                button.setIconSize(QtCore.QSize(width*1.5, height*1.5))
                #button.setIconSize(QtCore.QSize(1000, 1000))


            if color or value:
                colorWidget(widget, color=color, value=value)


        #new row
        rowPosY = 13
        rowHeight = 20
        self.currentXPos = 5

        button = QtGui.QLabel ('paste weights averager:', QGroupBox)
        addToRow(button, rowPosY, width-200, rowHeight,)


        if not pymel.optionVar( exists='ka_weightBlender_ignoreInfluenceHolding' ):
            pymel.optionVar( iv=('ka_weightBlender_ignoreInfluenceHolding', 1))
        ignoreInfluenceHolding = pymel.optionVar( query='ka_weightBlender_ignoreInfluenceHolding' )
        def cmd(i):
            pymel.optionVar( iv=('ka_weightBlender_ignoreInfluenceHolding', i))
        button = QtGui.QCheckBox ('ignore influence holding:', QGroupBox)
        button.setChecked(ignoreInfluenceHolding)
        self.menu.currentMenu.connect(button, QtCore.SIGNAL('stateChanged(int)'), cmd)
        addToRow(button, rowPosY, 200, rowHeight,)

        #new row
        rowPosY = rowPosY+rowHeight
        rowHeight = 20
        self.currentXPos = 5


        button = QtGui.QPushButton('UNDO weightBlend', QGroupBox)
        addToRow(button, rowPosY, (width-10)/2, rowHeight, color=[90, 90, 90, ], cmd=ka_weightPainting.undoWeightBlend)

        button = QtGui.QPushButton('REDO weightBlend', QGroupBox)
        addToRow(button, rowPosY, (width-10)/2, rowHeight, color=[90, 90, 90, ], cmd=ka_weightPainting.redoWeightBlend)

        #new row
        rowPosY = rowPosY+rowHeight
        rowHeight = 25
        self.currentXPos = 5

        self.weightSlider = QtGui.QSlider(QGroupBox)
        self.weightSlider.setOrientation(QtCore.Qt.Horizontal)
        self.weightSlider.setTickPosition(QtGui.QSlider.TicksBelow)

        #button.TicksBothSides
        self.weightSlider.setMaximum(200)
        self.weightSlider.setMinimum(0)
        self.weightSlider.setValue (100)
        self.weightSlider.setTickInterval(25)
        self.weightSlider.setSingleStep(1)
        addToRow(self.weightSlider, rowPosY, width-10, rowHeight,)

        #new row
        rowPosY = rowPosY+rowHeight
        rowHeight = 20
        self.currentXPos = 5


        button = QtGui.QPushButton('-025', QGroupBox)
        addToRow(button, rowPosY, (width-10)/5, rowHeight, weightAdd= -0.025)

        button = QtGui.QPushButton('-05', QGroupBox)
        addToRow(button, rowPosY, (width-10)/5, rowHeight, weightAdd= -0.05)


        self.spinBox = QtGui.QDoubleSpinBox(QGroupBox)
        addToRow(self.spinBox, rowPosY-10, (width-10)/5, rowHeight+10,)
        self.spinBox.setRange(0, 1)
        self.spinBox.setSingleStep(0.05)
        self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox.setDecimals(3)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold (1)
        font.setFamily('ORC A Std')
        self.spinBox.setFont(font)
        try:
            value = cmds.artAttrSkinPaintCtx('artAttrSkinContext', value=True, query=True,)
        except:
            value = 1
        self.spinBox.setValue(value)
        colorWidget(self.spinBox, value=[value, value, value])


        button = QtGui.QPushButton('+025', QGroupBox)
        addToRow(button, rowPosY, (width-10)/5, rowHeight, weightAdd=0.025)

        button = QtGui.QPushButton('+05', QGroupBox)
        addToRow(button, rowPosY, (width-10)/5, rowHeight, weightAdd=0.05)


        #new row
        rowPosY = rowPosY+rowHeight
        rowHeight = 30
        self.currentXPos = 5

        button = QtGui.QPushButton('0', QGroupBox)
        addToRow(button, rowPosY, (width-10)/5, rowHeight*2, weightValue=0)

        button = QtGui.QPushButton('25', QGroupBox)
        addToRow(button, rowPosY, (width-10)/5, rowHeight, weightValue=0.25)

        button = QtGui.QPushButton('50', QGroupBox)
        addToRow(button, rowPosY, (width-10)/5, rowHeight, weightValue=0.5)

        button = QtGui.QPushButton('75', QGroupBox)
        addToRow(button, rowPosY, (width-10)/5, rowHeight, weightValue=0.75)

        button = QtGui.QPushButton('100', QGroupBox)#100
        addToRow(button, rowPosY, (width-10)/5, rowHeight*2, weightValue=1)

        #new row
        rowPosY = rowPosY+rowHeight
        rowHeight = 30
        self.currentXPos = 5+((width-10)/5)

        button = QtGui.QPushButton('33', QGroupBox)
        addToRow(button, rowPosY, (((width-10)/5)*3)/2, rowHeight, weightValue=0.33)


        button = QtGui.QPushButton('66', QGroupBox)#66
        addToRow(button, rowPosY, (((width-10)/5)*3)/2, rowHeight, weightValue=0.66)

        #new row
        rowPosY = rowPosY+rowHeight
        rowHeight = 25
        self.currentXPos = 5

        button = QtGui.QPushButton('10', QGroupBox)#10
        addToRow(button, rowPosY, (width-10)/9, rowHeight, weightValue=0.1)

        button = QtGui.QPushButton('20', QGroupBox)
        addToRow(button, rowPosY, (width-10)/9, rowHeight, weightValue=0.2)

        button = QtGui.QPushButton('30', QGroupBox)
        addToRow(button, rowPosY, (width-10)/9, rowHeight, weightValue=0.3)

        button = QtGui.QPushButton('40', QGroupBox)
        addToRow(button, rowPosY, (width-10)/9, rowHeight, weightValue=0.4)

        button = QtGui.QPushButton('50', QGroupBox)
        addToRow(button, rowPosY, (width-10)/9, rowHeight, weightValue=0.5)

        button = QtGui.QPushButton('60', QGroupBox)
        addToRow(button, rowPosY, (width-10)/9, rowHeight, weightValue=0.6)

        button = QtGui.QPushButton('70', QGroupBox)
        addToRow(button, rowPosY, (width-10)/9, rowHeight, weightValue=0.7)

        button = QtGui.QPushButton('80', QGroupBox)
        addToRow(button, rowPosY, (width-10)/9, rowHeight, weightValue=0.8)

        button = QtGui.QPushButton('90', QGroupBox)
        addToRow(button, rowPosY, (width-10)/9, rowHeight, weightValue=0.9)

        height = rowPosY+rowHeight
        QGroupBox.setFixedSize(width, height);


        #Weight Slider Functionality
        self.virtualSliderActive = False

#        def cmd(value):
#            ka_weightPainting.pasteSkinWeights(weightedAverage=value)
#            self.virtualSliderActive = True


        if sliderMode == 'parallelBlend':
            def cmd(value):
                ka_weightPainting.pasteWeightsFromNeighbors(weightedAverage=value)
                if not self.virtualSliderActive:
                    self.virtualSliderActive = True

            self.menu.currentMenu.connect(self.weightSlider, QtCore.SIGNAL('valueChanged(int)'), cmd)

        if sliderMode == 'pasteWeights':
            def cmd(value):
                ka_weightPainting.pasteSkinWeights(weightedAverage=value)
                if not self.virtualSliderActive:
                    self.virtualSliderActive = True
#                    cmds.undoInfo(openChunk=True)
            self.menu.currentMenu.connect(self.weightSlider, QtCore.SIGNAL('valueChanged(int)'), cmd)

        if sliderMode == 'blendWeights':
            def cmd(value):
                ka_weightPainting.blendWeights(weightedAverage=value)
                if not self.virtualSliderActive:
                    self.virtualSliderActive = True
#                    cmds.undoInfo(openChunk=True)
            self.menu.currentMenu.connect(self.weightSlider, QtCore.SIGNAL('valueChanged(int)'), cmd)


#        def cmd(): cmds.undoInfo(openChunk=True);
#        self.menu.currentMenu.connect(self.weightSlider, QtCore.SIGNAL('self.weightSliderPressed()'), cmd)
#
#        def cmd(): cmds.undoInfo(closeChunk=True);
#        self.menu.currentMenu.connect(self.weightSlider, QtCore.SIGNAL('self.weightSliderReleased()'), cmd)


        self.weightSlider.setTracking(True)
        self.weightSlider = self.weightSlider
        QGroupBox.setMouseTracking(True)

        newQAction.setDefaultWidget(QGroupBox)
        self.menu.currentMenu.addAction(newQAction)

        if sliderMode in ['blendWeights', 'pasteWeights']:
            #self.menu.cursorPos.setX(self.menu.cursorPos.x() - (width/2))
            self.menu.cursorPos.setY(self.menu.cursorPos.y() + 35)

        else:
            self.menu.cursorPos.setX(self.menu.cursorPos.x() - (width/2))
            self.menu.cursorPos.setY(self.menu.cursorPos.y() + 35)

    def press(self,**kwargs):

        ka_weightPainting.deleteColoredVertexSpheres()

        if 'sliderMode' in kwargs:
            sliderMode = kwargs['sliderMode']

            if sliderMode == 'parallelBlend':
                ka_weightPainting.copyWeightsFromNeighbors()
                ka_weightPainting.createColoredVertexSpheres()
                self.weightSlider.grabMouse()
                self.menu.menu.hide()
#                cmds.undoInfo(openChunk=True)
                #cmds.undoInfo(stateWithoutFlush=False)

            elif sliderMode == 'pasteWeights':
                self.weightSlider.grabMouse()
                self.menu.menu.hide()
#                cmds.undoInfo(openChunk=True)
                #cmds.undoInfo(stateWithoutFlush=False)

            elif sliderMode == 'blendWeights':
                ka_weightPainting.copyWeightsFromNeighbors()
                self.weightSlider.grabMouse()
                self.menu.menu.hide()
                #cmds.undoInfo(openChunk=True)
                #cmds.undoInfo(stateWithoutFlush=False)


    def release(self, **kwargs):
        self.weightSlider.releaseMouse()
        sliderMode = None
        if 'sliderMode' in kwargs:
            sliderMode = kwargs['sliderMode']

            if sliderMode == 'parallelBlend':
#
#                ka_weightPainting.ka_pasteWeightsFromNeighbors_undoStarted = False
                self.weightSlider.releaseMouse()
                ka_weightPainting.addToUndoStack('appliedWeightsDict')
                ka_weightPainting.deleteColoredVertexSpheres()
                #cmds.undoInfo(stateWithoutFlush=True)
                #cmds.undoInfo(closeChunk=True)

            elif sliderMode == 'pasteWeights':
#
#                ka_weightPainting.ka_pasteWeightsFromNeighbors_undoStarted = False
                self.weightSlider.releaseMouse()
                ka_weightPainting.deleteColoredVertexSpheres()
                #cmds.undoInfo(stateWithoutFlush=True)
#                cmds.undoInfo(closeChunk=True)
            elif sliderMode == 'blendWeights':
                self.weightSlider.releaseMouse()
                self.menu.menu.hide()
#                cmds.undoInfo(openChunk=True)
                #cmds.undoInfo(stateWithoutFlush=True)

        #if self.virtualSliderActive == False:
            #if sliderMode == 'pasteWeights':
                #ka_weightPainting.pasteSkinWeights()
            #else:
                #self.menu.menu.popup(self.menu.cursorPos)












    def showMenu(self, **kwargs):
        pass













