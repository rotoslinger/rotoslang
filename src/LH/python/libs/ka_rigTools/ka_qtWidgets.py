
#====================================================================================
#====================================================================================
#
# ka_menu_weightLib
#
# DESCRIPTION:
#   contains custom widgets
#
# DEPENDENCEYS:
#   PyQt4
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

from . import ka_preference                               #;reload(ka_preference)
from . import ka_skinCluster                             #;reload(ka_skinCluster)
from . import ka_weightPainting                          #;reload(ka_weightPainting)
from . import ka_util                                          #;reload(ka_util)

currentFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".",))
iconFolder = os.path.abspath(os.path.join(currentFolder, "icons",))

## FUNCTIONS

def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(int(ptr), QtCore.QObject)


def addSeparatorItem(parent, label=''):
    separator = QtGui.QAction(label, parent)
    separator.setSeparator(True)
    parent.addAction(separator)

    return separator


def addSubmenuItem(subMenuName, parentMenu, icon=None, tearOff=True, command=None, font=None):
    """Add a submenu to a menu item, this submenu can also trigger a command on left click
    if one is passed in"""

    subMenu = kaQMenu(parent=parentMenu)
    subMenuAction = QtGui.QAction(subMenuName, parentMenu)
    subMenuAction.setMenu(subMenu)

    if icon:
        subMenuAction.setIcon(QtGui.QIcon(os.path.join(iconFolder, icon)))

    if font:
        subMenuAction.setFont(font)

    parentMenu.addAction(subMenuAction)

    if command:
        parentMenu.connect(subMenuAction, QtCore.SIGNAL('triggered()'), command)

    if tearOff:
        subMenu.setTearOffEnabled(True)

    return subMenu


def endSubmenuItem(subMenu):
    """Finishes a subMenu"""

    actions = subMenu.actions()
    hasQWidgetAction = False
    for action in actions:
        if action.__class__.__name__ == 'QWidgetAction':
            hasQWidgetAction = True
            break

    if hasQWidgetAction:

        tearOffWidgetAction =  TearOffWidgetAction(subMenu)
        subMenu.insertAction(actions[0], tearOffWidgetAction)
    else:
        subMenu.setTearOffEnabled(True)


def addWidgetMenuItem(widget, parentMenu, font=None):
    """Makes a widget into a QMenuWidgetItem and adds it to the menu"""

    QWidgetAction = QtGui.QWidgetAction(parentMenu)
    QWidgetAction.setDefaultWidget(widget)
    parentMenu.addAction(QWidgetAction)

    return QWidgetAction


def addMenuItem(label, menu, icon=None, command=None, colorIcon=None, font=None,):
    """adds QAction to the menu and assigns the command (which is defined 1 line above the creation of each QAction as cmd) to be the
    result of clicking the menu item
    Args:
        label - string - the label of the menu item
        menu - QMenu - the menu to add the item to
    Kwargs:
        icon - string - the file name of the icon to use for the item, must be a file existing
               in the icons directory
        command - function - the command to trigger when the item is l-clicked
        colorIcon - list - uses given rbg 0.0-1.0 values to generates an icon of solid
                    color
    """

    if colorIcon:
        pixMap = QtGui.QPixmap(100, 100)
        pixMap.fill(QtGui.QColor(255*colorIcon[0], 255*colorIcon[1], 255*colorIcon[2],))
        icon = QtGui.QIcon(pixMap)
        newQAction = QtGui.QAction(icon, label, menu)

    elif icon:
        newQAction = QtGui.QAction(QtGui.QIcon(os.path.join(iconFolder, icon)), label, menu)
    else:
        newQAction = QtGui.QAction(label, menu)

    if font:
        newQAction.setFont(font)

    if command:
        menu.connect(newQAction, QtCore.SIGNAL('triggered()'), command)

    menu.addAction(newQAction)

    return newQAction


## PREFRENCE MENU ITEMS

def prefMenuItem_radioButtons(preferenceName, labelList, defaultIndex, menu, command=None, font=None):
    """Adds a set of radio buttons to the menu, who's value selection gets stored as
    a preference"""

    actionGroup = QtGui.QActionGroup(menu)
    actionGroup.setExclusive(True)
    defaultIndex = ka_preference.get(preferenceName, defaultIndex)

    for i, label in enumerate(labelList):
        action = actionGroup.addAction(label)
        action.setCheckable(True)
        if font:
            action.setFont(font)

        if i == defaultIndex:
            action.setChecked(True)

        def cmd(i=i, preferenceName=preferenceName, command=command):
            ka_preference.set(preferenceName, i)
            if command != None:
                command()

        menu.connect(action, QtCore.SIGNAL('triggered()'), cmd)
        menu.addAction(action)

    return actionGroup


def addPrefMenuItem_bool(label, preferenceKey, defaultPreferenceValue, menu, command=None, font=None):
    action = QtGui.QAction(label, menu)
    if font:
        action.setFont(font)

    action.setCheckable(True)

    value = ka_preference.get(preferenceKey, defaultPreferenceValue)
    if value: action.setChecked(True)
    else: action.setChecked(False)

    def cmd(action=action, preferenceKey=preferenceKey, command=command):
        checkboxState = action.isChecked()
        if checkboxState:
            action.setChecked(2)
            ka_preference.add(preferenceKey, True)

        else:
            action.setChecked(0)
            ka_preference.add(preferenceKey, False)

        if command:
            command()

    menu.connect(action, QtCore.SIGNAL('triggered()'), cmd)
    menu.addAction(action)


## CLASSES
class kaQMenu(QtGui.QMenu):
    """A widget similar to QMenu, with the exception that the menu can also function as a button"""

    def __init__(self, *args, **kwArgs):
        QtGui.QMenu.__init__(self, *args, **kwArgs)

    def mousePressEvent(self, event):

        QActionClicked = self.actionAt(event.pos())
        if QActionClicked:
            QMenuOfAction = QActionClicked.menu()
            if QMenuOfAction:
                QActionClicked.trigger()

        # Do regular stuff
        QtGui.QMenu.mousePressEvent(self, event)

    #def setTearOffEnabled(self, bool_):
        #actions = self.actions()
        #hasQWidgetAction = False
        #for action in actions:
            #print action.__class__()
        ## TearOffWidgetAction(subMenu)
            ##subMenu.addAction(tearOffWidgetAction )


class StaticQMenu(QtGui.QMenu):

    def __init__(self, *args, **kwArgs):
        QtGui.QMenu.__init__(self, *args, **kwArgs)

    def hideEvent(self, event):
        pass



class TearOffWidgetAction(QtGui.QWidgetAction):

    def __init__(self, *args, **kwArgs):
        QtGui.QWidgetAction.__init__(self, *args, **kwArgs)
        menuParent = args[0]

        backgroundButton = QtGui.QPushButton('', menuParent )
        tearOffWidget = QtGui.QPushButton('------', menuParent )

        font = tearOffWidget.font()
        font.setPointSize(10)
        tearOffWidget.setFont(font)

        menuParentPalette = menuParent.palette()
        backgroundColor = menuParentPalette.window().color()

        QPalette = QtGui.QPalette()
        QPalette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor())
        grey = QtGui.QColor(255 * 0.5, 255 * 0.5, 255 * 0.5, 255)
        QPalette.setColor(QtGui.QPalette.Button, grey)
        QPalette.setColor(QtGui.QPalette.Shadow, grey)
        tearOffWidget.setPalette(QPalette)


        transparentPallete = QtGui.QPalette()
        backgroundColor = QtGui.QColor(255 * 0.3, 255 * 0.3, 255 * 0.3, 255)
        transparentPallete.setColor(QtGui.QPalette.Button, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.Shadow, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.Background, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.Window, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.Base, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.Dark, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.Mid, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.Midlight, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.Light, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.Highlight, backgroundColor)
        transparentPallete.setColor(QtGui.QPalette.AlternateBase, backgroundColor)

        backgroundButton.setPalette(transparentPallete)
        backgroundButton.setFixedSize(222, 21,)
        tearOffWidget.setFixedSize(222, 11,)

        self.createWidget(backgroundButton)
        self.createWidget(tearOffWidget)

        def resizeTearAwayButtonCmd(tearOffWidget=tearOffWidget, backgroundButton=backgroundButton, menuParent=menuParent):
            widthHint = menuParent.sizeHint().width()
            tearOffWidget.setFixedWidth(widthHint)
            tearOffWidget.setText('-'*(widthHint))
            backgroundButton.setFixedWidth(widthHint)
        menuParent.connect(menuParent, QtCore.SIGNAL('aboutToShow()'), resizeTearAwayButtonCmd)

        def tearMenuCmd(menuParent=menuParent,):
            globalPos = menuParent.mapToGlobal(menuParent.pos())
            globalPos = menuParent.pos()
            sizeHint = menuParent.sizeHint()
            sizeX = sizeHint.width()
            sizeY = sizeHint.height()-20
            newWindow = QtGui.QMainWindow(getMayaWindow())
            newWindow.setFixedSize(sizeX, sizeY)
            newWindow.move(globalPos)
            newWindow.setWindowTitle(menuParent.title())

            layout = QtGui.QFrame(newWindow)
            layout.setFixedSize(sizeX, sizeY) # -20 is to compensate for loss of tearOff button

            transparentPallete = QtGui.QPalette()
            backgroundColor = QtGui.QColor(255 * 0.3, 255 * 0.3, 255 * 0.3, 255)
            transparentPallete.setColor(QtGui.QPalette.Button, backgroundColor)
            transparentPallete.setColor(QtGui.QPalette.Shadow, backgroundColor)
            transparentPallete.setColor(QtGui.QPalette.Background, backgroundColor)
            transparentPallete.setColor(QtGui.QPalette.Window, backgroundColor)
            transparentPallete.setColor(QtGui.QPalette.Base, backgroundColor)
            transparentPallete.setColor(QtGui.QPalette.Dark, backgroundColor)
            transparentPallete.setColor(QtGui.QPalette.Mid, backgroundColor)
            transparentPallete.setColor(QtGui.QPalette.Midlight, backgroundColor)
            transparentPallete.setColor(QtGui.QPalette.Light, backgroundColor)
            transparentPallete.setColor(QtGui.QPalette.AlternateBase, backgroundColor)

            menuContents = menuParent.actions()
            yPos = 0
            for QAction in menuContents[1:]: # all except the tear off widget
                newWindow.addAction(QAction)
                if hasattr(QAction, 'defaultWidget'):
                    defaultWidget = QAction.defaultWidget()
                    size = defaultWidget.frameSize()
                    newWidget = defaultWidget.__class__(newWindow)
                    newWidget.setFixedSize(size)
                    newWidget.move(0, yPos)
                    yPos += size.height()

                else:
                    button = QtGui.QPushButton(QAction.text(), newWindow)
                    button.setFixedSize(sizeHint.width(), 21)
                    button.move(0, yPos)
                    yPos += 18
                    button.setPalette(transparentPallete)
                    menuParent.connect(button, QtCore.SIGNAL('pressed()'), QAction.trigger)


            newWindow.show()
            newWindow.releaseKeyboard()
            #newWindow.show()
            #pressEvent = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, QtCore.QPoint(-10, -10), QtCore.Qt.LeftButton, QtCore.Qt.MouseButtons(), QtCore.Qt.KeyboardModifiers())
            #menuParent.mousePressEvent(pressEvent)
            menuParent.hide()
            print('hide')
        menuParent.connect(tearOffWidget, QtCore.SIGNAL('pressed()'), tearMenuCmd)

class WeightBlenderWidget(QtGui.QGroupBox):

    def __init__(self, *args, **kwArgs):
        QtGui.QGroupBox.__init__(self, *args, **kwArgs)
        self.setFixedSize(405,75)
        menuParent = args[0]

        # ignore influence holding checkbox
        QCheckBox = QtGui.QCheckBox ('ignore influence holding:', self)
        QCheckBox.move(5, 2)
        QCheckBox.setFixedSize(200, 18)
        ignoreInfluenceHolding = ka_preference.get('weightBlender_ignoreInfluenceHolding', 1)
        QCheckBox.setCheckState(ignoreInfluenceHolding)
        def cmd(i): ka_preference.set('weightBlender_ignoreInfluenceHolding', i)
        self.connect(QCheckBox, QtCore.SIGNAL('stateChanged(int)'), cmd)

        # blend mode comboBox
        self.QComboBox = QtGui.QComboBox (self)
        self.QComboBox.move(175, 2)
        self.QComboBox.setFixedSize(225, 18)
        self.QComboBox.addItems(['Blend: Copied Weights', 'Blend: Horizontal Neighbors Weights',] )
        defaultIndex = ka_preference.get('WeightBlenderWidget_blendMode', 0)
        self.QComboBox.setCurrentIndex(defaultIndex)
        def cmd(index): ka_preference.set('WeightBlenderWidget_blendMode', index)
        self.connect(self.QComboBox, QtCore.SIGNAL('currentIndexChanged(int)'), cmd)

        # weight slider
        self.sliderStarted = False

        self.weightSlider = QtGui.QSlider(self)
        self.weightSlider.setOrientation(QtCore.Qt.Horizontal)
        self.weightSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.weightSlider.setMaximum(200)
        self.weightSlider.setMinimum(0)
        self.weightSlider.setValue (100)
        self.weightSlider.setTickInterval(25)
        self.weightSlider.setSingleStep(1)
        self.weightSlider.move(5, 20)
        self.weightSlider.setFixedSize(395, 30)

        # Value Changed Cmd
        def cmd(value, self=self):
           index = self.QComboBox.currentIndex()

           if index == 0:
               ka_weightPainting.pasteSkinWeights(weightedAverage=value)
           elif index == 1:
               ka_weightPainting.pasteWeightsFromNeighbors(weightedAverage=value)
           else:
               ka_weightPainting.pasteWeightsFromNeighbors(weightedAverage=value)

        self.connect(self.weightSlider, QtCore.SIGNAL('valueChanged(int)'), self.sliderChanged)
        self.connect(self.weightSlider, QtCore.SIGNAL('sliderPressed ()'), self.sliderPress)
        self.connect(self.weightSlider, QtCore.SIGNAL('sliderReleased ()'), self.sliderRelease)


        # copy weights button
        QPushButton = QtGui.QPushButton('Copy Weights', self)
        QPushButton.move(5,50)
        QPushButton.setFixedSize(95, 25)
        self.connect(QPushButton, QtCore.SIGNAL('pressed()'), ka_weightPainting.copySkinWeights)

        # paste weights button
        QPushButton = QtGui.QPushButton('Paste Weights', self)
        QPushButton.move(105,50)
        QPushButton.setFixedSize(95, 25)
        self.connect(QPushButton, QtCore.SIGNAL('pressed()'), ka_weightPainting.pasteSkinWeights)

        # Undo Blend button
        QPushButton = QtGui.QPushButton('Undo Blend', self)
        QPushButton.move(205,50)
        QPushButton.setFixedSize(95, 25)
        self.connect(QPushButton, QtCore.SIGNAL('pressed()'), ka_weightPainting.undoWeightBlend)

        # Redo Blend button
        QPushButton = QtGui.QPushButton('Redo Blend', self)
        QPushButton.move(305,50)
        QPushButton.setFixedSize(95, 25)
        self.connect(QPushButton, QtCore.SIGNAL('pressed()'), ka_weightPainting.redoWeightBlend)


    def sliderChanged(self, value):
        if self.sliderStarted:
           index = self.QComboBox.currentIndex()

           if index == 0:
               ka_weightPainting.pasteSkinWeights(weightedAverage=value)

           elif index == 1:
               ka_weightPainting.pasteWeightsFromNeighbors(weightedAverage=value)

           else:
               ka_weightPainting.pasteWeightsFromNeighbors(weightedAverage=value)

    def sliderPress(self):
        self.sliderStarted = True
        index = self.QComboBox.currentIndex()

        if index != 0:
             ka_weightPainting.copyWeightsFromNeighbors()
             ka_weightPainting.createColoredVertexSpheres()

    def sliderRelease(self):
        self.sliderStarted = False
        index = self.QComboBox.currentIndex()

        if index != 0:
             ka_weightPainting.addToUndoStack('appliedWeightsDict')
             ka_weightPainting.deleteColoredVertexSpheres()











#def pk_makePolyPlane(width=10.0,length=10.0,subX=15,subZ=15):
    #'''pk_makePolyPlane(width=10.0,length=10.0,subX=15,subZ=15)
    #is a python script in the file
    #C:\Documents and Settings\Paul\My Documents\maya\2008\python\pythonlearning.py
    #Creates a poly plane centered at the origin of the world space. '''

    #outputMesh = maya.OpenMaya.MObject()

    #nRows = subX + 1
    #nCols = subZ + 1

    #numFaces = subX * subZ
    #numVertices = nRows * nCols
    ## point array of plane vertex local positions
    #points = maya.OpenMaya.MFloatPointArray()
    #for x in range(0,nRows,1):
        #for z in range(0,nCols,1):
            #px = width*(x/float(subX)) - width/2.0
            #py = 0.0
            #pz = length*(z/float(subZ)) - length/2.0
            #p = maya.OpenMaya.MFloatPoint( px, py, pz )
            ##print 'point:: %f, %f, %f' % (p.x, p.y, p.z)
            #points.append(p)

    ## vertex connections per poly face in one array of indexs into point array given above
    #faceConnects = maya.OpenMaya.MIntArray()
    #for row in range(0,subX,1):
        #for col in range(0,subZ,1):
            ##fID = (row * subX) + (col % subZ)
            ##print 'row:%i, col:%i, polyFaceID:%i' % (row,col,fID)
            #index0 = ((row % nRows) * nCols) + (col % nCols)
            #faceConnects.append(index0)
            #index1 = ((row % nRows) * nCols) + ((col+1) % nCols)
            #faceConnects.append(index1)
            #index2 = (((row+1) % nRows) * nCols) + ((col+1) % nCols)
            #faceConnects.append(index2)
            #index3 = (((row+1) % nRows) * nCols) + (col % nCols)
            #faceConnects.append(index3)
            ##print 'face vertex ID: %i, %i, %i, %i' % (index0,index1,index2,index3)

    ## an array to hold the total number of vertices that each face has
    #faceCounts = maya.OpenMaya.MIntArray()
    #for c in range(0,numFaces,1):
        #faceCounts.append(4)

    ##create mesh object using arrays above and get name of new mesh
    #meshFS = maya.OpenMaya.MFnMesh()
    #newMesh = meshFS.create(numVertices, numFaces, points, faceCounts, faceConnects, outputMesh)
    #meshFS.updateSurface()
    #nodeName = meshFS.name()
    #print 'Mesh node name is: %s' % nodeName

    ##assign new mesh to default shading group
    #maya.cmds.sets (nodeName, e=True, fe='initialShadingGroup')
    #return nodeName



#def printMeshRecreateCmd(inMeshs=None):
    #if not inMeshs:
        #inMeshs = pymel.ls(selection)
    #elif not isinstance(inMeshs, list):
        #inMeshs = [inMeshs]

    #for inMesh in inMeshs:
        #meshKwargs = {}

        #meshKwargs['points'] = []
        #for point in inMesh.getPoints():
            #meshKwargs['points'].append([point[0], point[1], point[2]])

        #meshKwargs['numVertices'] = len(meshKwargs['points'])

        #meshKwargs['numFaces'] = len(inMesh.f.indices())

        #meshKwargs['faceCounts'] = []
        #meshKwargs['faceConnects'] = []
        #for i, face in enumerate(inMesh.f):
            #verts = face.getVertices()
            #meshKwargs['faceCounts'].append(len(verts))
            #meshKwargs['faceConnects'].extend(verts)

        ##meshKwargs['outputMesh'] = maya.OpenMaya.MObject()

        #print 'kwArgs = {}'
        #for kwarg in meshKwargs:
            #print "kwArgs['%s'] = " % (kwarg),
            #print meshKwargs[kwarg]

#printMeshRecreateCmd(a)




#import maya.OpenMaya
#def createMesh(**kwargs):
    #points = kwargs.get('points')
    #numFaces = kwargs.get('numFaces')
    #numVertices = kwargs.get('numVertices')
    #faceCounts = maya.OpenMaya.MIntArray()
    #faceConnects = maya.OpenMaya.MIntArray()
    #outputMesh = maya.OpenMaya.MObject()

    #for i in kwargs.get('faceCounts'):
        #faceCounts.append(i)

    #for i in kwargs.get('faceConnects'):
        #faceConnects.append(i)

    #apiPoints = maya.OpenMaya.MFloatPointArray()
    #for point in points:
        #apiPoints.append(maya.OpenMaya.MFloatPoint( *point ))

    ##create mesh object using arrays above and get name of new mesh
    #meshFS = maya.OpenMaya.MFnMesh()

    #newMesh = meshFS.create(numVertices, numFaces, apiPoints, faceCounts, faceConnects, outputMesh)
    #meshFS.updateSurface()
    #nodeName = meshFS.name()
    #print 'Mesh node name is: %s' % nodeName

    #maya.cmds.sets (nodeName, e=True, fe='initialShadingGroup')
    #return nodeName

#createMesh(**kwArgs)
