#====================================================================================
#====================================================================================
#
# ka_hyperShade
#
# DESCRIPTION:
#   tools for filtering current selection based on UI inputs
#
# DEPENDENCEYS:
#   None
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


import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pymel
import maya.OpenMayaUI as mui

from PyQt4 import QtGui, QtCore, uic

import re


def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(int(ptr), QtCore.QObject)

uiFile= os.path.dirname(__file__)+'/ka_filterSelectionUI.ui'
form_class, base_class = uic.loadUiType(uiFile)

scriptJobDummyWindow = 'ka_filterSelection_scriptJobWindow'
class UI(base_class, form_class):
    title = 'ka selection filter tool'



    def __init__(self, parent=getMayaWindow()):
        '''A custom window with a demo set of ui widgets'''
        #init our ui using the MayaWindow as parent
        super(base_class, self).__init__(parent)
        #uic adds a function to our class called setupUi, calling this creates all the widgets from the .ui file
        self.setupUi(self)
        self.setObjectName('ka_renameUIWindow')
        self.setWindowTitle(self.title)

        self.selectionNodeTypes = {}
        self.selection = {}

        ##name and number
        self.connect(self.search_lineEdit, QtCore.SIGNAL('returnPressed(const QString&)'), self.update)
        self.connect(self.searchCaseSensitive_comboBox, QtCore.SIGNAL('currentIndexChanged (int)'), self.loadPreviewResults)
        self.connect(self.scopeKeepPrune_comboBox, QtCore.SIGNAL('currentIndexChanged (int)'), self.loadPreviewResults)
        self.connect(self.searchScope_comboBox, QtCore.SIGNAL('currentIndexChanged (int)'), self.loadPreviewResults)
        self.connect(self.type1_comboBoxKeepPrune_comboBox, QtCore.SIGNAL('currentIndexChanged (int)'), self.loadPreviewResults)
        self.connect(self.type1_comboBox, QtCore.SIGNAL('currentIndexChanged (int)'), self.loadPreviewResults)
        self.connect(self.type2_comboBoxKeepPrune_comboBox, QtCore.SIGNAL('currentIndexChanged (int)'), self.loadPreviewResults)
        self.connect(self.type2_comboBox, QtCore.SIGNAL('currentIndexChanged (int)'), self.loadPreviewResults)

        self.connect(self.filter_button, QtCore.SIGNAL('clicked()'), self.filter)


        self.update()
        self.search_lineEdit.setFocus()

        #script job
        if cmds.window(scriptJobDummyWindow, exists=True):
            cmds.deleteUI(scriptJobDummyWindow)
        cmds.window(scriptJobDummyWindow)

        def selectionChanged():
            '''run if maya selection is changed, destroys self if called while window is not visisble'''
            #import maya.cmds as cmds

            if self.isVisible():
                self.update()

            else:    #self destruct
                cmds.deleteUI(scriptJobDummyWindow)

        jobId = cmds.scriptJob(event=['SelectionChanged', selectionChanged], parent=scriptJobDummyWindow)

    def storeSelectionInfo(self):
        self.selection = pymel.ls(selection=True)
        hashesUsed = {}
        for each in selection:
            hashNum = each.__hash__
            if hashNum not in self.nodeTypeDict:
                self.nodeTypeDict[hashNum] = each.nodeType()
                hashesUsed.append(hashNum)
            else:
                hashesUsed[hashNum] = True

        for hashNum in self.nodeTypeDict:
            if hashNum not in hashesUsed:
                hashesUsed.pop(hashNum)


    def update(self):
        self.loadSelection()
        self.storeSelectionInfo()
        #self.loadPreviewResults()
        pass
    def closeEvent(self, event):
        if cmds.window(scriptJobDummyWindow, exists=True):
            cmds.deleteUI(scriptJobDummyWindow)
        event.accept() # let the window close


    #################################################################################
    ##
    ##    01: Filter
    ##
    #################################################################################
    def filter(self):
        selection = pymel.ls(selection=True, dependencyNodes=True)
        filteredList = self.processFilter(selection)
        pymel.select(filteredList)


    def loadSelection(self):
        selection = pymel.ls(selection=True, dependencyNodes=True)
        selectionNames = []

        nodeTypes = []
        givenType1 = str(self.type1_comboBox.currentText())
        givenType2 = str(self.type2_comboBox.currentText())

        #clear type comboBoxs and add the '' Value
        self.type1_comboBox.clear()
        self.type2_comboBox.clear()
        self.type1_comboBox.addItem('')
        self.type2_comboBox.addItem('')

        #if there was a value selected before for either type, preserve it
        if givenType1:
            nodeTypes.append(givenType1)
        if givenType2:
            nodeTypes.append(givenType2)

        #iterate through selection
        for each in selection:
            if hasattr(each, 'nodeName'):
                selectionNames.append(each.nodeName())

            # add objects type to the list of types to filter comboBox
            nodeType = str(pymel.nodeType(each))
            if nodeType not in nodeTypes:
                nodeTypes.append(nodeType)

            # do the same for its shapes
            if 'transform' in pymel.nodeType(each, inherited=True):
                for shape in each.getShapes():
                    nodeType = str(pymel.nodeType(shape))
                    if nodeType not in nodeTypes:
                        nodeTypes.append(nodeType)


        if selectionNames:
            self.selection_listWidget.clear()
            self.selection_listWidget.addItems(selectionNames)

        for nodeType in sorted(nodeTypes):
            self.type1_comboBox.addItem(nodeType)
            self.type2_comboBox.addItem(nodeType)

        #if there was a value selected before, set it as current value
        if givenType1 in nodeTypes:
            index = self.type1_comboBox.findText(givenType1)
            self.type1_comboBox.setCurrentIndex(index)

        if givenType2 in nodeTypes:
            index = self.type2_comboBox.findText(givenType2)
            self.type2_comboBox.setCurrentIndex(index)



    def loadPreviewResults(self):
        selection = pymel.ls(selection=True, dependencyNodes=True)
        previewList = []
        nameList = []

        previewList = self.processFilter(selection)
        self.previewResults_listWidget.clear()
        for each in previewList:
            self.previewResults_listWidget.addItem(each.nodeName())

    def processFilter(self, itemList):
        returnList = []

        searchText = str(self.search_lineEdit.displayText())
        scopeKeepPrune = str(self.scopeKeepPrune_comboBox.currentText())
        scopeMode = str(self.searchScope_comboBox.currentText())

        type1KeepPrune = str(self.type1_comboBoxKeepPrune_comboBox.currentText())
        type1 = str(self.type1_comboBox.currentText())

        type2KeepPrune = str(self.type2_comboBoxKeepPrune_comboBox.currentText())
        type2 = str(self.type2_comboBox.currentText())

        returnList = list(itemList)


        #filter by search text
        if searchText:

            matches = []
            for each in itemList:
                if scopeMode == 'Only those with Occurrence':
                    if searchText in each.nodeName():
                        matches.append(each)

                elif scopeMode == 'Only those Starting with':
                    if each.nodeName().startswith(searchText):
                        matches.append(each)

                elif scopeMode == 'Only those Ending with':
                    if each.nodeName().endswith(searchText):
                        matches.append(each)


            for each in itemList:
                if each in returnList:
                    if scopeKeepPrune == 'keep':
                        if each not in matches:
                            returnList.remove(each)

                    elif scopeKeepPrune == 'prune':
                        if each in matches:
                            returnList.remove(each)

        #Filter by Type1
        if type1:
            matches = []
            for each in itemList:
                if each in returnList:
                    if pymel.nodeType(each) == type1:
                        matches.append(each)

                    #if it didnt match, check if any of its shapes matach
                    elif 'transform' in pymel.nodeType(each, inherited=True):
                        for shape in pymel.listRelatives(each, shapes=True):
                            if pymel.nodeType(shape) == type1:
                                matches.append(each)


            for each in itemList:
                if each in returnList:
                    if type1KeepPrune == 'keep':
                        if each not in matches:
                            returnList.remove(each)

                    elif type1KeepPrune == 'prune':
                        if each in matches:
                            returnList.remove(each)

        #Filter by Type2
        if type2:
            matches = []
            for each in itemList:
                if each in returnList:
                    if pymel.nodeType(each) == type2:
                        matches.append(each)

                    #if it didnt match, check if any of its shapes matach
                    elif 'transform' in pymel.nodeType(each, inherited=True):
                        for shape in pymel.listRelatives(each, shapes=True):
                            if pymel.nodeType(shape) == type1:
                                matches.append(each)


            for each in itemList:
                if each in returnList:
                    if type2KeepPrune == 'keep':
                        if each not in matches:
                            returnList.remove(each)

                    elif type2KeepPrune == 'prune':
                        if each in matches:
                            returnList.remove(each)


        return returnList



def open():
    global ka_renameUIWindow
    try:
        ka_renameUIWindow.close()
    except:
        pass

    ka_renameUIWindow = UI()
    ka_renameUIWindow.show()
