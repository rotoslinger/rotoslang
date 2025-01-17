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
import os
import pprint

import sip
import PyQt4
from PyQt4 import QtGui, QtCore, uic

import maya.cmds as cmds
import pymel.core as pymel
import maya.mel as mel

from .. import ka_util                      #;reload(ka_util)
from .. import ka_hyperShade          #;reload(ka_hyperShade)
#from ka_util import undoable, repeatable #decorators
undoable = ka_util.undoable
repeatable = ka_util.repeatable #decorators

class Menu():
    '''menu items specific to actions in the maya viewport'''
    def __init__(self, menu):
        self.menu = menu

#    def build_menu_hyperShade(self):
    def populateMenu(self, **kwargs):
        '''more or less acting as the __init__'''
        #print "kwargs[node]:",
        #print kwargs['node']
        #print 'kwargs[mode]:',
        #print kwargs['mode']
        self.hyperConnector_widget(node=kwargs['node'], mode=kwargs['mode'])

    def addNodeAttrToFavorites(self, nodeType, attributeName, mode):
        path = os.path.dirname(__file__)
        filePath = path+'/'+'ka_menu_hyperConnector_favoritesDictionary.py'
        f = open(filePath, 'r')
        fileText = f.read()
        f.close()

        favoritesDict = eval(fileText)
        if not isinstance(favoritesDict, dict):
            favoritesDict = {}

        if not nodeType in favoritesDict:
            favoritesDict[nodeType] = {'source':{}, 'destination':{},}

        if mode == 'source':
            attrDict = favoritesDict[nodeType]['source']

        elif mode == 'destination':
            attrDict = favoritesDict[nodeType]['destination']

        if not attributeName in attrDict:
            attrDict[attributeName] = True

        print('favoritesDict:', end=' ')
        print(favoritesDict)

        pp = pprint.PrettyPrinter(indent=4)
        writeText = pp.pformat(favoritesDict)
        print('writeText:', end=' ')
        print(writeText)
        print('type(writeText):', end=' ')
        print(type(writeText))

        f = open(filePath, 'w')
        f.write(writeText)
        f.close()
    def getNodeAttrsFromFavorites(self,):
        path = os.path.dirname(__file__)
        filePath = path+'/'+'ka_menu_hyperConnector_favoritesDictionary.py'
        f = open(filePath, 'r')
        fileText = f.read()
        f.close()

        return eval(fileText)

    def hyperConnector_widget(self, node=None, mode=None,):
        node = node
        nodeType = pymel.nodeType(node)
        attrs = sorted(pymel.listAttr(node, connectable=True,))
        hypergraph = "graph1HyperShadeEd"

        #set mode specific attributes
        if mode == 'source':
            QGroupBox_title = 'Source Attribute'

        elif mode == 'destination':
            QGroupBox_title = 'Destination Attribute'

        #Create Widget
        newQAction = QtGui.QWidgetAction(self.menu.currentMenu)

        width = 600
        height = 600
        maxHeight = 700

        QGroupBox = QtGui.QGroupBox(QGroupBox_title, self.menu.currentMenu)
        QGroupBox.setFixedSize(width, height);
        QGroupBox,set
        menuLineEdit = QtGui.QLineEdit(QGroupBox)
        menuLineEdit.move(5, 15)
        menuLineEdit.setFixedSize((width-10)*0.5, 20);

        listFilter_comboBox = QtGui.QComboBox(QGroupBox)
        listFilter_comboBox.move((width*0.5), 15)
        listFilter_comboBox.setFixedSize((width-10)*0.5, 20);
        listFilter_comboBox.addItems(['favorites', 'no filter', 'userDefined', 'keyable'])

        menuTreeWidget = QtGui.QTreeWidget(QGroupBox)
        menuTreeWidget.move(5, 40)
        menuTreeWidget.setFixedSize(width-10, height-45)
        menuTreeWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        font = QtGui.QFont('Sans Serif', 9.5)
        menuTreeWidget.setFont(font)
        menuTreeWidget.setColumnCount(3)
        menuTreeWidget.setIndentation(15)
        attrInQTreeWidget = {}


        menuTreeWidget.setHeaderLabels(['attributes', 'input', 'output'])
        menuTreeWidget.setColumnWidth (1, 150)
        menuTreeWidget.setColumnWidth (2, 100)
        menuTreeWidget.setColumnWidth (0, 300)

        #
        contextMenu = QtGui.QMenu(self.menu.currentMenu)
        menuTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        def popCmd(point):
            point.setY(point.y() - 50)
            contextMenu.exec_(menuTreeWidget.mapToGlobal(point))

        self.menu.currentMenu.connect(menuTreeWidget, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), popCmd)

        def cmd(widget=menuTreeWidget):
            selectedItems =  menuTreeWidget.selectedItems()
            for item in selectedItems:
                nodeType = str(pymel.nodeType(node))
                attrName = str(item.text(0))
                self.addNodeAttrToFavorites(nodeType, attrName, mode)
        self.menu.addMenuItem('add to favorites22', command=cmd, menu=contextMenu)


        #Add Widget
        newQAction.setDefaultWidget(QGroupBox)
        self.menu.currentMenu.addAction(newQAction)

        attrParent = None



        #Setup connections
        def updateList(**kwargs):
            searchText = str(menuLineEdit.displayText())
            menuTreeWidget.clear()
            comboBoxText = str(listFilter_comboBox.currentText())
            listAttrArgs = {}

            #use favorites IF there are any for this node
            if comboBoxText == 'favorites':
                favoritesDict = self.getNodeAttrsFromFavorites()
                if nodeType not in favoritesDict:
                    comboBoxText = 'no filter'
                    listFilter_comboBox.setCurrentIndex(1)

                elif not favoritesDict[nodeType]:
                    comboBoxText = 'no filter'
                    listFilter_comboBox.setCurrentIndex(1)

                else:
                    attrs = []

                    if mode == 'source':
                        attrList = favoritesDict[nodeType]['source']
                        if not attrList:
                            comboBoxText = 'no filter'
                            listFilter_comboBox.setCurrentIndex(1)
                        else:
                            for attr in attrList:
                                if node.attr(attr).isMulti():
                                    usedIndices = node.attr(attr).getArrayIndices()
                                    if usedIndices:
                                        for i in range(usedIndices[-1]+2):
                                            attrs.append('%s[%s]' % (attr, str(i)) )

                                #if pymel.attributeQuery('output1D', node=node, exists=True):
                                    #if pymel.attributeQuery('output1D', node=node, writable=True):
                                        #attrs.append(key)
                                        #childAttrs = pymel.attributeQuery(key, node=node, listChildren=True)
                                        #if childAttrs:
                                            #for childAttr in childAttrs:
                                                #attrs.append(childAttr)

                                        #attrParent = pymel.attributeQuery(key, node=node, listParent=True)
                                        #while attrParent:
                                            #if attrParent not in attrs:
                                                #attrs.append(attrParent[0])
                                                #attrParent = pymel.attributeQuery(attrParent, node=node, listParent=True)

                                else:
                                    attrs.append(attr)
                            attrs.extend(pymel.listAttr(node, connectable=True, hasData=True, userDefined=True))

                    elif mode == 'destination':
                        attrList = favoritesDict[nodeType]['destination']
                        if not attrList:
                            comboBoxText = 'no filter'
                            listFilter_comboBox.setCurrentIndex(1)
                        else:
                            for attr in attrList:
                                if node.attr(attr).isMulti():
                                    usedIndices = node.attr(attr).getArrayIndices()
                                    if usedIndices:
                                        for i in range(usedIndices[-1]+2):
                                            attrs.append('%s[%s]' % (attr, str(i)) )


                                #if pymel.attributeQuery('output1D', node=node, readable=True):
                                    #attrs.append(key)
                                    #childAttrs = pymel.attributeQuery(key, node=node, listChildren=True)
                                    #if childAttrs:
                                        #for childAttr in childAttrs:
                                            #attrs.append(childAttr)

                                    #attrParent = pymel.attributeQuery(key, node=node, listParent=True)
                                    #if attrParent:
                                        #if attrParent not in attrs:
                                            #attrs.append(attrParent[0])
                                            #attrParent = pymel.attributeQuery(attrParent, node=node, listParent=True)

                                else:
                                    attrs.append(attr)
                            attrs.extend(pymel.listAttr(node, connectable=True, hasData=True, userDefined=True))

            if comboBoxText == 'no filter':
                attrs = pymel.listAttr(node, connectable=True, hasData=True,)

            elif comboBoxText != 'favorites':
                listAttrArgs = {comboBoxText: True,}
                attrs = pymel.listAttr(node, connectable=True, hasData=True, **listAttrArgs)

            #dictionary to assosiate attribute names (used as the text label) with the QTreeWidgetItem objects
            OOOOOOO = 'attrs';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
            if attrs:
                for i, attr in enumerate(sorted(attrs)):
                    if re.search(searchText, attr, re.IGNORECASE):
                        if pymel.attributeQuery(attr, node = node, exists=True):

                            # determin if attr is source or destination
                            invalidAttr = False
                            if mode == 'source':
                                if not pymel.attributeQuery(attr, node = node, connectable=True, readable=True):
                                    invalidAttr=True

                            elif mode == 'destination':
                                if not pymel.attributeQuery(attr, node = node, connectable=True, writable=True):
                                    invalidAttr=True

                            # add each attr
                            if not invalidAttr:
                                attr = node.attr(attr)
                                attrName = attr.attrName(longName=True, includeNode=False)

                                attrIsArray = attr.isMulti()
                                attrParent =  attr.getParent(arrays=True)
                                attrChildren = []
                                if pymel.attributeQuery(attrName, node=node, listChildren=True):
                                    attrChildren = attr.getChildren()

                                #use ONLY top level attributes, the children attributes will be delt with per parent
                                if not attrParent:
                                    addAttrToTree(attr)

                                    itemHeight = 15
                                    if not menuTreeWidget.height()+itemHeight > maxHeight:
                                        menuTreeWidget.setFixedHeight(menuTreeWidget.height()+itemHeight)
                                        QGroupBox.setFixedHeight(QGroupBox.height()+itemHeight)

                                    if attrChildren:
                                        OOOOOOO = 'attrChildren';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
                                        attrChildren = list(zip(attrChildren, [1 for each in attrChildren]))

                                        while attrChildren:
                                            childAttr, indent = attrChildren.pop(0)
                                            OOOOOOO = 'indent';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
                                            OOOOOOO = 'childAttr';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
                                            childAttrName = childAttr.attrName(longName=True, includeNode=False)

                                            childAttrParent = childAttr.getParent()
                                            childAttrParentName = childAttrParent.attrName(longName=True, includeNode=False)

                                            ## Add child Item to tree
                                            addAttrToTree(childAttr, parentAttrWidget=attrInQTreeWidget[childAttrParentName])

                                            # Deal with array items, if attr is array
                                            #childAttrIsArray = pymel.attributeQuery(childAttr, node=node, isMulti=True)
                                            #childAttrIsArray = childAttr.isMulti()
                                            #if childAttrIsArray:
                                                #usedIndices = childAttr.getArrayIndices()

                                                #if usedIndices:
                                                    #for i in range(usedIndices[-1]+2):
                                                        #arrayAttr = '%s[%s]' % (childAttr, str(i))

                                                        #ChildQTreeWidgetItem = QtGui.QTreeWidgetItem(attrInQTreeWidget[childAttr])#menuListWidget)
                                                        #ChildQTreeWidgetItem.setText(0, arrayAttr)
                                                        #attrInQTreeWidget[arrayAttr] = ChildQTreeWidgetItem
                                                        #updateMenuTreeWidget(ChildQTreeWidgetItem)
                                                        #if searchText:
                                                            #menuTreeWidget.expandItem(attrInQTreeWidget[childAttrParent])

                                            # Add Children's children to stack
                                            childrenOfChildAttr = pymel.attributeQuery(childAttrName, node=node, listChildren=True)
                                            if childrenOfChildAttr:
                                                for each in childrenOfChildAttr:
                                                    attrChildren.insert(0, (each, indent+1))


        def addAttrToTree(attr, indent=0, parentAttrWidget=None, expanded=True):
            """Adds the tree widget representing the attribute to the tree. Also adds array
            items if the attribute has any"""

            attrName = attr.attrName(longName=True, includeNode=False)

            if parentAttrWidget:
                QTreeWidgetItem = QtGui.QTreeWidgetItem(parentAttrWidget,)#menuListWidget)
            else:
                QTreeWidgetItem = QtGui.QTreeWidgetItem(menuTreeWidget,)#menuListWidget)
            QTreeWidgetItem.setText(0, attrName)

            QTreeWidgetItem.pymelAttr = attr
            QTreeWidgetItem.pymelAttrName = attrName

            attrInQTreeWidget[attrName] = QTreeWidgetItem
            updateMenuTreeWidget(QTreeWidgetItem, indent=indent)

            if expanded and parentAttrWidget:
                menuTreeWidget.expandItem(parentAttrWidget)

            if attr.isMulti():
                if not attr.isCompound():

                    usedIndices = attr.getArrayIndices()
                    if usedIndices:
                        r = usedIndices[-1]+2
                    else:
                        r = 2

                    for i in range(r):

                        #arrayAttr = attr[i]
                        arrayAttrName = '%s[%s]' % (attrName, str(i))
                        #arrayAttr = attr.attr(arrayAttrName)
                        #print attr

                        arrayQTreeWidgetItem = QtGui.QTreeWidgetItem(QTreeWidgetItem)#menuListWidget)
                        arrayQTreeWidgetItem.setText(0, arrayAttrName)
                        attrInQTreeWidget[arrayAttrName] = arrayQTreeWidgetItem

                        #arrayQTreeWidgetItem.pymelAttr = arrayAttr
                        arrayQTreeWidgetItem.pymelAttrName = arrayAttrName

                        updateMenuTreeWidget(arrayQTreeWidgetItem)

                        if expanded:
                            menuTreeWidget.expandItem(QTreeWidgetItem)

        def colorTreeWidgetItem(widget, color=None, fade=False, bold=True, italic=False):
            if fade:
                color.setAlpha(75)
            elif color:
                widget.setTextColor(0, QtGui.QColor(0, 0, 0,))
                widget.setTextColor(1, QtGui.QColor(0, 0, 0,))

            altFont = font
            altFont.setBold(bold)
            altFont.setItalic(italic)
            widget.setFont(0, altFont)
            widget.setFont(1, altFont)

            if color:
                widget.setBackgroundColor(0, QtGui.QColor(color))
                widget.setBackgroundColor(1, QtGui.QColor(color))

        def updateMenuTreeWidget(QTreeWidgetItem, indent=0):
            #DEFINE THE NAME OF EACH ITEM in a way that indicates if
            #it has incomming connections or not
            #attr = QTreeWidgetItem.pymelAttr

            attrName = QTreeWidgetItem.pymelAttrName
            attrDisplay = re.sub('[>\-\- ]', '', attrName) #strip out all "-->>" connection indicators and spaces

            nodeAttr = node+'.'+attrName

            hasIncomming = False

            bold=True
            italic=False
            greyText=False
            OOOOOOO = 'attrName';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
            OOOOOOO = 'node';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))

            if pymel.attributeQuery(attrName, node=node, exists=True):
                if node.attr(attrName).exists():
                    if pymel.connectionInfo(nodeAttr, isSource=True):
                        destination = pymel.connectionInfo(nodeAttr, destinationFromSource=True)
                        if destination:
                            QTreeWidgetItem.setText(2, destination[0])

                    if pymel.connectionInfo(nodeAttr, isDestination=True):
                        source = pymel.connectionInfo(nodeAttr, sourceFromDestination=True)
                        if source:
                            QTreeWidgetItem.setText(1, source[0])

                        hasIncomming = True

            else:
                bold=False
                italic=True
                greyText=True

            if hasIncomming:

                attrParents = []
                attrParent = pymel.attributeQuery(attrDisplay, node=node, listParent=True)
                while attrParent:
                    attrParents.append(attrParent[0])
                    attrParent = pymel.attributeQuery(attrParent[0], node=node, listParent=True)

                connectionSource = pymel.connectionInfo(nodeAttr, sourceFromDestination=True)
                connectionSourceType = pymel.nodeType(connectionSource)

                if 'Constraint' in connectionSourceType:
                    color = QtGui.QColor(163, 203, 240, 255)
                    colorTreeWidgetItem(QTreeWidgetItem, color, bold=bold, italic=italic)
                    for each in attrParents:
                        colorTreeWidgetItem(attrInQTreeWidget[each], color, fade=True, bold=bold, italic=italic)

                elif 'animCurve' in connectionSourceType:
                    color = QtGui.QColor(222, 114, 122, 255)
                    colorTreeWidgetItem(QTreeWidgetItem, color, bold=bold, italic=italic)
                    for each in attrParents:
                        colorTreeWidgetItem(attrInQTreeWidget[each], color, fade=True, bold=bold, italic=italic)
                else:
                    color = QtGui.QColor(241, 241, 165, 255)
                    colorTreeWidgetItem(QTreeWidgetItem, color, bold=bold, italic=italic)
                    for each in attrParents:
                        colorTreeWidgetItem(attrInQTreeWidget[each], color, fade=True, bold=bold, italic=italic)

            else:
                QTreeWidgetItem.setBackgroundColor(0, QtGui.QColor(0, 0, 0, 0))
                QTreeWidgetItem.setBackgroundColor(1, QtGui.QColor(0, 0, 0, 0))

                if greyText:
                    QTreeWidgetItem.setTextColor(0, QtGui.QColor(205, 205, 205,))
                    QTreeWidgetItem.setTextColor(1, QtGui.QColor(205, 205, 205,))
                else:
                    QTreeWidgetItem.setTextColor(0, QtGui.QColor(255, 255, 255,))
                    QTreeWidgetItem.setTextColor(1, QtGui.QColor(255, 255, 255,))
                colorTreeWidgetItem(QTreeWidgetItem, bold=bold, italic=italic)

        updateList()


        def addAttrTofDictionary(node, attribute):
            path = os.path.dirname(__file__)
            f = open(path+'/'+'ka_menu_hyperConnector_attributePopularity.py', 'w')
            f.write('pooop')
            f.close()
            print(path+'/'+'ka_menu_hyperConnector_attributePopularity.py')
            print('WOORD')

        def toggleConnect(sourceAttr, destinationAttr):
            attrIsConnected = pymel.isConnected( sourceAttr, destinationAttr, ignoreUnitConversion=True,)
            attrIsLocked = pymel.getAttr(destinationAttr, lock=True)

            if attrIsLocked:
                pymel.setAttr(destinationAttr, lock=False)


            if attrIsConnected:
                pymel.disconnectAttr(sourceAttr, destinationAttr,)
            else:
                try:
                    pymel.connectAttr(sourceAttr, destinationAttr, force=True)
                except:
                    printError()

            if attrIsLocked:
                pymel.setAttr(destinationAttr, lock=True)

            #addAttrToPopularityDictionary(sourceAttr)

        @undoable
        def storeAttrSelection(*args, **kwArgs):
            selectedItems =  menuTreeWidget.selectedItems()
            selectedAttrs = []
            if selectedItems:
                for item in selectedItems:
                    attr = str(item.text(0))
                    selectedAttrs.append(attr)

                #if mode is 'source', store the attr selection into and option var
                if mode == 'source':
                    pymel.optionVar(stringValue=('ka_menu_hyperConnector_sourceNode', node))

                    pymel.optionVar(clearArray='ka_menu_hyperConnector_sourceAttrs')
                    for attr in selectedAttrs:
                        pymel.optionVar(stringValueAppend=('ka_menu_hyperConnector_sourceAttrs', attr))

                #if mode is 'source', store the attr selection into and option var
                if mode == 'destination':
                    sourceNode = pymel.optionVar(query='ka_menu_hyperConnector_sourceNode')
                    sourceAttrs = pymel.optionVar(query='ka_menu_hyperConnector_sourceAttrs')
                    numberOfAttrs = len(sourceAttrs)

                    destinationNodes = []
                    sourceNodes = []
                    mayaSelection = pymel.ls(selection=True)

                    if mayaSelection:
                        #connect doubleHelix first half to second
                        if sourceNode in mayaSelection:
                            print('mode: connect double helix')
                            #if len(mayaSelection)%2==0:

                            halfOf_mayaSelection = len(mayaSelection)/2

                            sourceNodes = mayaSelection[0:halfOf_mayaSelection]
                            destinationNodes =mayaSelection[halfOf_mayaSelection:]

                        else:
                            print('mode: connect [0] to [1:]')
                            sourceNodes = [sourceNode]
                            destinationNodes = mayaSelection

                    #connect 2 nodes
                    else:
                        print('mode: connect 2')
                        sourceNodes = [sourceNode]
                        destinationNodes = [node]



                    #LETS CONNECT FINALLY
                    if len(sourceNodes) > 1:

                        sourceNodes = doubleHelix_sort(sourceNodes)
                        destinationNodes = doubleHelix_sort(destinationNodes)

                        for i, destinationNode in enumerate(destinationNodes):
                            toggleConnect(sourceNodes[i]+'.'+sourceAttrs[0], destinationNodes[i]+'.'+selectedAttrs[0])


                    else:
                        for destinationNode in destinationNodes:
                            toggleConnect(sourceNode+'.'+sourceAttrs[0], destinationNode+'.'+selectedAttrs[0])
                            menuTreeWidget.setItemSelected(selectedItems[-1], 0)


                    updateMenuTreeWidget(selectedItems[-1])

        def increaseAttrPopularity(attr):
            pass

        def doubleHelix_sort(nodeList,):

            xDict = {}
            yDict = {}
            for each in nodeList:
                x, y = pymel.hyperGraph(hypergraph, getNodePosition=each, query=True, )
                xDict[x] = each
                yDict[y] = each

            sortedX = sorted(xDict)
            sortedY = sorted(yDict)
            nodeList_width = sortedX[-1]-sortedX[0]
            nodeList_height = sortedY[-1]-sortedY[0]

            if nodeList_width > nodeList_height:
                dictOfChoice = xDict
            else:
                dictOfChoice = yDict

            nodeList = []
            for key in sorted(dictOfChoice):
                nodeList.append(dictOfChoice[key])

            return nodeList


        self.menu.currentMenu.connect(menuLineEdit, QtCore.SIGNAL('textChanged(const QString&)'), updateList)
        self.menu.currentMenu.connect(listFilter_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), updateList)
        self.menu.currentMenu.connect(menuTreeWidget, QtCore.SIGNAL('clicked(const QModelIndex&)'), storeAttrSelection)

        menuLineEdit.setFocus()





