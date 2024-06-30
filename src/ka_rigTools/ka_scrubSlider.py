#====================================================================================
#====================================================================================
#
# ka_scrubUtils
#
# DESCRIPTION:
#   a series of fuctions triggered by dragging the mouse
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

import sip
import PyQt4
from PyQt4 import QtGui, QtCore, uic
#from PyQt4 import *
from traceback import print_exc as printError


import maya.cmds as cmds
import pymel.core as pymel
import maya.mel as mel
import maya.OpenMayaUI as OpenMayaUI

from . import ka_weightPainting   #;reload(ka_weightPainting)
from . import ka_preference        #;reload(ka_preference)
from . import ka_weightBlender          #;reload(ka_weightBlender)


def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(int(ptr), QtCore.QObject)

class ScrubSlider(QtGui.QSlider):

    def __init__(self, sliderRange=[0, 100], defaultValue=0, width=500, step=1.0, shiftStep=25, mode='toggle',
                 startCommand=None, changeCommand=None, finishCommand=None, hotkeyDict={}, rightClickCommand=None):
        """
        constructor of scrubSlider.

        Kwargs:
            sliderRange (start int, end int): The slider range

            defaultValue (int): the value to start the slider at

            width (int in pixels): the width of the slider (this also effects the sensitivity of it indirectly)

            step (int): not yet impimented

            mode (string): acceptable values are "clickDrag", and "toggle".

            startCommand (function): a passed in function to run at the start of the scrub

            changeCommand (function): a passed in function to run when the slider changes. The current Value of the slider will be
                                      the first argument passed to the function

            finishCommand (function): a passed in function to run at the end of the scrub (right before the mouse is released
                                       back to the user)

            hotkeyDict (dictionary of string(key) function(value) pairs): This dictionary gives the slider functions to assign to
                                                                          keypresses that will override maya hotkeys while the slider
                                                                          is in use.

        """
        self.mayaWindow = getMayaWindow()
        super(ScrubSlider, self).__init__(self.mayaWindow)


        self.mode = mode
        cursorPos = QtGui.QCursor().pos()
        cursorPos = self.mayaWindow.mapFromGlobal(cursorPos)
        self.extraWidgets = []
        self.finished = False

        # slider setup math
        self.defaultValue = float(defaultValue)
        self.previousValue = float(defaultValue)
        self.mouseInitialPositionX = cursorPos.x()
        self.mouseGrabOffset = 0.0
        self.step = step
        self.shiftStep = shiftStep

        self.sliderMax = float(sliderRange[1])
        self.sliderMin = float(sliderRange[0])
        self.sliderRange = float(self.sliderMax - self.sliderMin)

        defaultPercentOfSliderRange = (float(defaultValue) - self.sliderMin) / float(self.sliderRange)

        #self.pixelMin = self.mouseInitialPositionX - (width * defaultPercentOfSliderRange)
        self.pixelMin = self.mouseInitialPositionX - (width * defaultPercentOfSliderRange)
        self.pixelMax = self.pixelMin + width
        self.pixelRange = self.pixelMax - self.pixelMin


        # QSlider
        sliderOffset = 105
        self.move(self.pixelMin, cursorPos.y()+sliderOffset)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setSingleStep(1)
        self.setFixedSize(width, 4)
        self.setValue(defaultValue)
        self.setMaximum(self.sliderMax)
        self.setMinimum(self.sliderMin)

        # value spin box
        valueBoxWidth = 40
        self.sliderValueBox = QtGui.QSpinBox(self.mayaWindow)
        self.sliderValueBox.move(((self.pixelMin+((self.pixelMax-self.pixelMin)*0.5) - (valueBoxWidth*0.5))),
                                   cursorPos.y()+sliderOffset+6)
        self.sliderValueBox.setFixedSize(valueBoxWidth, 15)
        self.sliderValueBox.setButtonSymbols(2)
        self.sliderValueBox.setRange(self.sliderMin, self.sliderMax)
        self.extraWidgets.append(self.sliderValueBox)


        # passed commandeds
        self.startCommand = startCommand
        self.changeCommand = changeCommand
        self.finishCommand = finishCommand

        if mode == "clickDrag":
            self.startScrub = False

        if mode == "toggle":
            self.startScrub = True

        self.connect(self, QtCore.SIGNAL('sliderReleased()'), self.finish)

        self.hotkeyDict = hotkeyDict
        self.lastPressedKeyID = None


        #self.hotkeyActions = []
        #for key in hotkeyDict:
            #if isinstance(key, basestring):
                #keySequence = QtGui.QKeySequence(key)

            #elif isinstance(key, QtGui.QKeySequence):
                #keySequence = key

            #else:
                #keySequence = QtGui.QKeySequence(key)

            ##action = QtGui.QAction(self.mayaWindow)
            #action = QtGui.QAction(self)
            #action.setShortcut(keySequence)
            #action.setShortcutContext(QtCore.Qt.WidgetShortcut)
            ##action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
            #action.triggered.connect(hotkeyDict[key])
            #self.addAction(action)
            ##self.mayaWindow.addAction(action)
            #self.hotkeyActions.append(action)

        #def printHi():
            #print 'reverseTab'
        #self.action222 = QtGui.QAction(self)
        #self.action222.setShortcut(QtGui.QKeySequence('Shift,Shift+X'))
        #self.action222.setShortcutContext(QtCore.Qt.WidgetShortcut)
        #self.action222.triggered.connect(printHi)
        #self.addAction(self.action222)
        #self.hotkeyActions.append(self.action222)

    #def event(self, event):
        #if (event.type()== QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Tab):
            #self.keyPressEvent(event)

        #return QtGui.QSlider.event(self, event)

    def mousePressEvent(self, QMouseEvent):
        print('clickity')
        print(QMouseEvent.button())

        if QMouseEvent == QtCore.Qt.LeftButton:
            self.finish()

        elif QMouseEvent == QtCore.Qt.RightButton:
            print('righty')

        QtGui.QSlider.mousePressEvent(self, QMouseEvent)


    def mouseMoveEvent(self, mouseEvent):
        mouseX = self.mayaWindow.mapFromGlobal(mouseEvent.globalPos()).x()
        scrubValue = int(round(self.getScrubValue(mouseX)))
        if (scrubValue - self.previousValue):
            self.scubValueChanged(scrubValue)
        mouseEvent.accept()

    def keyPressEvent(self, keyEvent):
        keyID = keyEvent.key()
        if keyID in self.hotkeyDict:
            subDict = self.hotkeyDict[keyID]
            if subDict['press']:

                modifiers = int(keyEvent.modifiers())
                modifierDown = True
                if subDict['shift'] and modifiers not in [33554432, 100663296, 369098752, 301989888]:
                    modifierDown = False
                    print('not shift')

                if subDict['alt'] and modifiers not in [134217728, 201326592, 167772160, 234881024]:
                    modifierDown = False
                    print('not alt')

                if subDict['ctrl'] and modifiers not in [67108864, 100663296, 201326592, 234881024]:
                    modifierDown = False
                    print('not ctrl')

                if modifierDown:
                    if subDict['hold']:
                        if not keyEvent.isAutoRepeat():
                            subDict['command']()
                            keyEvent.accept()

                    else:
                        subDict['command']()
                        keyEvent.accept()
                        return None

        QtGui.QSlider.keyPressEvent(self, keyEvent)


    def keyReleaseEvent(self, keyEvent):

        if not keyEvent.isAutoRepeat():
            keyID = keyEvent.key()
            if keyID in self.hotkeyDict:
                subDict = self.hotkeyDict[keyID]
                if subDict['release']:
                    subDict['command']()
                    keyEvent.accept()

        QtGui.QSlider.keyReleaseEvent(self, keyEvent)


    def getScrubValue(self, mouseX):

        if mouseX <= self.pixelMin:
            return self.sliderMin
        elif mouseX >= self.pixelMax:
            return self.sliderMax
        else:
            relativeX = float(mouseX-self.pixelMin)
            percent = relativeX / float(self.pixelRange)
            return self.sliderMin + (self.sliderRange * percent)


    def getSteppedValue(self, x, base=1):
        return int(base * round(float(x)/base))


    def scubValueChanged(self, value):
        self.previousValue = value

        # check if modifier should change step value
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            value = self.getSteppedValue(value, self.shiftStep)

        self.setValue(value)
        self.setFocus(QtCore.Qt.MouseFocusReason)

        if self.sliderValueBox.isVisible:
            self.sliderValueBox.setValue(value)

        if self.changeCommand:
            self.changeCommand(value)


    def start(self):

        sliderVis = ka_preference.get('scrubSlider_sliderVisable', True)
        sliderValueVis = ka_preference.get('scrubSlider_sliderValueVisable', True)
        if self.startCommand:
            self.startCommand()

        self.setTracking(True)
        self.setFocus(QtCore.Qt.MouseFocusReason)
        self.show()
        self.grabMouse()
        self.setMouseTracking(True)
        self.setSliderDown(True)
        self.grabKeyboard()

        #if not sliderVis:
            #self.hide()

        if sliderValueVis:
            self.sliderValueBox.show()

        self.setFocus(QtCore.Qt.MouseFocusReason)

    def finish(self):
        if not self.finished: # only finish once
            if self.finishCommand:
                self.finishCommand()

            self.releaseMouse()
            self.releaseKeyboard()
            self.deleteLater()

            for extraWidget in self.extraWidgets:
                extraWidget.deleteLater()

            self.sliderValueBox.deleteLater()
            self.finished = True




def getScrubSlider():
    mayaWindow = getMayaWindow()
    for child in mayaWindow.children():
        if child.objectName() == 'ka_scrubSlider':
            return child

scrubSlider = getScrubSlider()
if scrubSlider:
    scrubSlider.finish()

def createScrubSlider(*args, **kwargs):
    """Returns scrubSlider. This is the main function to create the scrub slider"""

    # get mode
    mode = ka_preference.get('snapToolPrimaryAxis', 0)
    if mode == 1: mode = 'clickDrag'
    else:         mode = 'toggle'
    kwargs['mode'] = mode

    if mode == 'toggle':
        scrubSlider = getScrubSlider()
        if scrubSlider:
            count = 0
            while scrubSlider and count < 25:
                count += 1

                try:
                    scrubSlider.finish()
                except:
                    printError()
                    if hasattr(scrubSlider, 'extraWidgets'):
                        for extraWidget in scrubSlider.extraWidgets:
                            extraWidget.deleteLater()

                        scrubSlider.deleteLater()

                scrubSlider = getScrubSlider()

        else:
            scrubSlider = ScrubSlider(*args, **kwargs)
            scrubSlider.setObjectName('ka_scrubSlider')
            scrubSlider.start()


    elif mode == 'clickDrag':
        scrubSlider = ScrubSlider(*args, **kwargs)
        scrubSlider.setObjectName('ka_scrubSlider')
        scrubSlider.start()


    return scrubSlider

def addHotkeyToDict(keyString, command, hotkeyDict, press=True, release=False, hold=False):
    keyString = keyString.upper()
    keyString.replace('ALT', 'Alt')
    keyString.replace('SHIFT', 'Shift')
    keyString.replace('CTRL', 'Ctrl')

    QKeySeq = QtGui.QKeySequence(keyString)

    keyID = int(QKeySeq)
    hotkeyDict[keyID] = {}
    subDict = hotkeyDict[keyID]
    subDict['QKeySequence'] = QKeySeq
    subDict['command'] = command
    subDict['press'] = press
    subDict['release'] = release
    subDict['hold'] = hold

    if 'Shift' in keyString:
        subDict['shift'] = True
    else:
        subDict['shift'] = False

    if 'Alt'   in keyString:
        subDict['alt']   = True
    else:
        subDict['alt']   = False

    if 'Ctrl'  in keyString:
        subDict['ctrl']  = True
    else:
        subDict['ctrl']   = False

#def release():
    #scrubSlider = getScrubSlider()
    #if scrubSlider:
        #scrubSlider.finish()


#def toggleSlider(sliderCommandName):
    ##sliderCmd = getattr(__thismodule__, sliderCommandName)
    #sliderCmd = globals()[sliderCommandName]
    #scrubSlider = getScrubSlider()

    #if not scrubSlider:
        #scrubSlider = sliderCmd()

    #else:
        #scrubSlider.finish()

def timeSliderScrub():
    rangeMin = pymel.floatField('MayaWindow|toolBar5|MainPlaybackRangeLayout|formLayout10|floatField3', query=True, value=True)
    rangeMax = pymel.floatField('MayaWindow|toolBar5|MainPlaybackRangeLayout|formLayout10|floatField4', query=True, value=True)
    currentTime = pymel.currentTime(query=True)

    def sliderCmd(time):
        pymel.currentTime(time)

    scrubSlider = createScrubSlider(sliderRange=[rangeMin, rangeMax], changeCommand=sliderCmd, defaultValue=currentTime)

# 's pressed'

def weight_parallelBlend_Scrub():
    hotkeyDict = {}

    def startCommand():
        ka_weightPainting.copyWeightsFromNeighbors()
        ka_weightPainting.createColoredVertexSpheres()

    def changeCommand(value):
        ka_weightPainting.pasteWeightsFromNeighbors(weightedAverage=value)

    def finishCommand():
        ka_weightPainting.addToUndoStack('appliedWeightsDict')
        ka_weightPainting.deleteColoredVertexSpheres()

    def s_pressed():
        ka_weightPainting.pasteWeightsFromNeighbors_changeNeighbors()
    addHotkeyToDict('s', s_pressed, hotkeyDict, press=True, release=False, hold=False)

    def a_pressed():
        ka_weightPainting.pasteWeightsFromNeighbors_changeNeighbors(reverse=True)
    addHotkeyToDict('a', a_pressed, hotkeyDict, press=True, release=False, hold=False)

    #hotkeyDict = {QtGui.QKeySequence('S'):tabPressed,
                  ##QtGui.QKeySequence(QtCore.Qt.Key_S):tabPressed,
                  ##QtCore.Qt.Key_Tab:tabPressed,
                  ##QtGui.QKeySequence(QtCore.Qt.Key_Tab):tabPressed,
                  ##[Qt.ShiftModifier, QtCore.Qt.Key_Tab]:shiftTabPressed,
                  #}

    scrubSlider = createScrubSlider(sliderRange=[0, 200], startCommand=startCommand, changeCommand=changeCommand, finishCommand=finishCommand,
                                    defaultValue=100, hotkeyDict=hotkeyDict)



def weight_parallelBlend_Scrub():
    hotkeyDict = {}

    def startCommand():
        ka_weightBlender.start()

    def changeCommand(value):
        ka_weightBlender.change(value=value)

    def finishCommand():
        ka_weightBlender.finish()


    def c_pressed():
        next(ka_weightBlender)
    addHotkeyToDict('c', c_pressed, hotkeyDict, press=True, release=False, hold=False)

    def b_pressed():
        ka_weightBlender.previous()
    addHotkeyToDict('b', b_pressed, hotkeyDict, press=True, release=False, hold=False)


    scrubSlider = createScrubSlider(sliderRange=[0, 200], startCommand=startCommand, changeCommand=changeCommand, finishCommand=finishCommand,
                                    defaultValue=100, hotkeyDict=hotkeyDict)



    #hotkeyDict = {QtGui.QKeySequence('S'):tabPressed,
                  ##QtGui.QKeySequence(QtCore.Qt.Key_S):tabPressed,
                  ##QtCore.Qt.Key_Tab:tabPressed,
                  ##QtGui.QKeySequence(QtCore.Qt.Key_Tab):tabPressed,
                  ##[Qt.ShiftModifier, QtCore.Qt.Key_Tab]:shiftTabPressed,
                  #}









#import pymel.core as pymel
#import ka_rigTools.ka_weightPainting as ka_weightPainting; reload(ka_weightPainting)

#q
#pymel.ls(selection=True, flatten=True)


#import ka_rigTools.ka_scrubUtils as ka_scrubUtils; reload(ka_scrubUtils)

#def asimIsFatSlider():
    #maxFat = 100
    #minFat = 300
    #currentFat = 173

    #def howFat(fatAmoumt):
        #print 'asim gained %s lbs of fat' % str(fatAmount)

    #scrubSlider = createScrubSlider(sliderRange=[maxFat, minFat], changeCommand=sliderCmd, defaultValue=currentFat)
