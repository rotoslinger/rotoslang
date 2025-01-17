
#====================================================================================
#====================================================================================
#
# ka_menu
#
# DESCRIPTION:
#   sets up a context sensitive popup menu while a specified hotkey is held down
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


import os
import re
from functools import partial

import maya.cmds as cmds
import maya.mel as mel

import sip
import PyQt4
from PyQt4 import QtGui, QtCore, uic

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as OpenMayaUI

from . import ka_menu_modelEditor                                      #;reload(ka_menu_modelEditor)
from . import ka_menu_hyperShade                                       #;reload(ka_menu_hyperShade)
from . import ka_menu_paintPallet                                      #;reload(ka_menu_paintPallet)
from .. import ka_util                                          #;reload(ka_util)
from .. import ka_qtWidgets                                     #;reload(ka_qtWidgets)
from .. import ka_preference                               #;reload(ka_preference)

repeatable = ka_util.repeatable
undoable = ka_util.undoable
iconFolder = os.path.abspath( os.path.join( os.path.join( os.path.dirname(__file__), "..",), 'icons') )


def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(int(ptr), QtCore.QObject)



class Menu(ka_menu_modelEditor.Menu, ka_menu_hyperShade.Menu, ka_menu_paintPallet.Menu):
    iconFolder = iconFolder

    def __init__(self):
        self.mayaWindow = getMayaWindow()

        #the menu object
        #self.menu = QtGui.QMenu(self.mayaWindow)
        self.menu = ka_qtWidgets.kaQMenu(self.mayaWindow)

        self.currentMenu = self.menu
        self.currentMenuClass = None
        self.menuHierarchy = [self.menu]

        # Turn the undo queue back on if it has been left off
        if not cmds.undoInfo( query=True, state=True,):
            cmds.undoInfo( state=True,)


    def buildMenu(self, buildMenuOverride=None, **kwargs):
        '''clears contents of the previous menu, and sets the new menu to show (which will later be populated with items'''
        self.menu.clear()
        self.cursorPos = QtGui.QCursor.pos()
#        self.menu.show()

        self.setCurrentMenuClass(buildMenuOverride=buildMenuOverride)

        if self.currentMenuClass:
            self.currentMenuClass.populateMenu(**kwargs)
#        if buildMenuOverride:
#            self.populateMenu(buildMenuOverride=buildMenuOverride, **kwargs)
#
#        else:
#            self.populateMenu()


        self.showMenu()



    def setCurrentMenuClass(self, buildMenuOverride=None, **kwargs):
        panelName = cmds.getPanel( underPointer=True )
        cursorPos = QtGui.QCursor.pos()

        if not panelName:
            cursorPosX = cursorPos.x()
            cursorPosY = cursorPos.x()
            panelName = cmds.getPanel( atPosition=[cursorPosX, cursorPosY] )

            if not panelName:
                cursorPosX = cursorPosX - 3
                panelName = cmds.getPanel( atPosition=[cursorPosX, cursorPosY] )

                if not panelName:
                    panelName = cmds.getPanel( withFocus=True )



        if panelName:

            if buildMenuOverride:
                if buildMenuOverride == 'paintPallet':
                    self.currentMenuClass = ka_menu_paintPallet.Menu(self)

                if buildMenuOverride == 'hyperConnector':
                    self.currentMenuClass = ka_menu_hyperConnector.Menu(self)

            elif 'modelPanel' in panelName:
#                self.build_menu_modelEditor()
                self.currentMenuClass = ka_menu_modelEditor.Menu(self)

            elif 'hyperShadePanel' in panelName:
#                self.build_menu_hyperShade()
                self.currentMenuClass = ka_menu_hyperShade.Menu(self)

    def showMenu(self, **kwargs):
        if hasattr(self.currentMenu, 'showMenu'):
            self.currentMenu.showMenu(**kwargs)
        else:
            self.menu.popup(self.cursorPos)


    def press(self, buildMenuOverride=None, **kwargs):
        self.buildMenu(buildMenuOverride=buildMenuOverride, **kwargs)

        if hasattr(self.currentMenuClass, 'press'):
            self.currentMenuClass.press(**kwargs)


    def release(self, **kwargs):
        if hasattr(self.currentMenuClass, 'release'):
            self.currentMenuClass.release(**kwargs)



    #helper functions

    def addMenuItem(self, label, icon=None, command=None, menu=None, colorIcon=None):
        '''adds QAction to the menu and assigns the command (which is defined 1 line above the creation of each QAction as cmd) to be the
        result of clicking the menu item'''

        if not menu:
            menu = self.currentMenu

        newQAction = ka_qtWidgets.addMenuItem(label, menu, icon=icon, command=command, colorIcon=colorIcon)

        return newQAction


    def addWidgetMenuItem(self, widget, parent=None):
        '''adds QWidgetAction to the menu'''

        if not parent:
            menu = self.currentMenu
        else:
            menu = parent

        QWidgetAction = ka_qtWidgets.addWidgetMenuItem(widget, menu)

        return QWidgetAction


    def prefMenuItem_radioButtons(self, preferenceName, labelList, defaultIndex, parent=None, command=None):
        '''adds QWidgetAction to the menu'''

        if not parent:
            menu = self.currentMenu
        else:
            menu = parent

        actionGroup = ka_qtWidgets.prefMenuItem_radioButtons(preferenceName, labelList, defaultIndex, menu, command=command)

        return actionGroup


    def prefMenuItem_checkbox(self, label, preferenceName, defaultState, parent=None, command=None):
        '''adds QWidgetAction to the menu'''

        if not parent:
            menu = self.currentMenu
        else:
            menu = parent

        QWidgetAction = ka_qtWidgets.addPrefMenuItem_bool(label, preferenceName, defaultState, menu, command=command)

        return QWidgetAction


    def addSeparatorItem(self, label=''):
        separator = ka_qtWidgets.addSeparatorItem(self.currentMenu, label=label)
        return separator


    def addSubmenuItem(self, subMenuName, **kwargs):

        if self.currentMenu:
            kwargs['parentMenu'] = self.currentMenu
        else:
            kwargs['parentMenu'] = self.menu

        subMenu = ka_qtWidgets.addSubmenuItem(subMenuName, **kwargs)

        self.currentMenu = subMenu
        self.menuHierarchy.append(subMenu)

        return True

    def endSubmenuItem(self,):
        currentMenu = self.menuHierarchy.pop()
        ka_qtWidgets.endSubmenuItem(currentMenu)
        self.currentMenu = self.menuHierarchy[-1]





###################################################################################
global ka_menu
ka_menu = Menu()
ka_menu.activated = False

def press(buildMenuOverride=None, **kwargs):
#    print 'open'
    mel.eval('global int $gKa_menu = 1')

    if ka_menu.menu.isVisible():
        try:
            ka_menu.menu.hide()
            mel.eval('global int $gKa_menu = 0')

        except:
            pass

    else:
        ka_menu.press(buildMenuOverride=buildMenuOverride, **kwargs)


def release(**kwargs):
    mel.eval('global int $gKa_menu = 0')
    ka_menu.release(**kwargs)
    pass










