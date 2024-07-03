#====================================================================================
#====================================================================================
#
# ka_hotkeys
#
# DESCRIPTION:
#   sets up named commands and hotkeys based on the classes in the class "Hotkeys"
#
# DEPENDENCEYS:
#   none
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
import inspect
import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel


#import ka_menu.ka_menu_hyperShade as ka_menu_hyperShade                 #;reload(ka_menu_hyperShade)
#print 'C'

#import ka_menu.ka_menu_modelEditor as ka_menu_modelEditor               #;reload(ka_menu_modelEditor)
#print 'D'
from . import ka_menu    #;reload(ka_menu)

from . import ka_util    #;reload(ka_util)
from . import ka_transforms    #;reload(ka_transforms)
from . import ka_weightPainting    #;reload(ka_weightPainting)

import ka_rigTools.ka_reload as ka_reload; importlib.reload(ka_reload)

import ka_rigTools.core ;importlib.reload(ka_rigTools.core)
import ka_rigTools.kMenu as kMenu ;importlib.reload(kMenu)
import ka_rigTools.kMenu.kMenu_menus as kMenu_menus ;importlib.reload(kMenu_menus)
import ka_rigTools.ka_attrTool.ka_attrTool_UI as ka_attrTool_UI   #;reload(ka_attrTool_UI)
import ka_rigTools.ka_advancedJoints as ka_advancedJoints    #;reload(ka_advancedJoints)
import ka_rigTools.ka_scrubSlider as ka_scrubSlider    #;reload(ka_scrubSlider)
import ka_rigTools.ka_display as ka_display    #;reload(ka_display)
import ka_rigTools.ka_selection as ka_selection    #;reload(ka_selection)
import ka_rigTools.ka_context as ka_context    #;reload(ka_context)
import importlib

oneThirdWeightPasteToggle = True



#def echo(func):
    #pass

class echo(object):

    def __init__(self, function):
        self.function = function

    def __call__(self):
        print("Entering", self.function.__name__)
        self.function()
        print("Exited", self.function.__name__)


def activateHotkey(hotkeyList):
    """sets given hotkey to use the assosiated command from the Hotkeys class

    hotkeyList -- a list of class names to activate. ie: ['v', 'tilda']
    """

    HotkeysClassObject = Hotkeys()
    listOfKeyBinds = HotkeysClassObject.listOfKeyBinds
    keyBindsToActivate = []

    if hotkeyList == 'all':
        keyBindsToActivate = HotkeysClassObject.listOfKeyBinds

    elif isinstance(hotkeyList, list):
        for each in listOfKeyBinds:
            if each.__name__ in hotkeyList:
                keyBindsToActivate.append(each)

    elif isinstance(hotkeyList, str):
        for each in listOfKeyBinds:
            if each.__name__ == hotkeyList:
                keyBindsToActivate = [each]

    verionScriptsDir = pymel.internalVar(userScriptDir=True)
    #scriptsDir = '/'.join(pymel.internalVar(userScriptDir=True).split('/')[:-3])+'/scripts/'
    scriptsDir = os.path.abspath(os.path.join(cmds.internalVar(userScriptDir=True), '..', '..', 'scripts'))
    #currentPackageDir = os.path.abspath(os.path.join(cmds.internalVar(userScriptDir=True), '..', '..', 'scripts'))
    currentPackageDir = '/'.join(__file__.split('/')[:-2])+'/'

    possiblePackageLocations = [verionScriptsDir, scriptsDir, currentPackageDir]

    for keybind in keyBindsToActivate:

        cmdName = 'ka_nameCommand_'+keybind.__name__
        #cmdString =  r'''python('''
        #cmdString += r'''"import sys \n"+'''

        ##add a sys path append to the name commands so the self import can find itself
        #for directory in possiblePackageLocations:
            #if os.path.isdir(directory):
                ##if os.path.exists(directory+'/ka_rigTools'):
                #cmdString += r'''"if not '%s' in sys.path: sys.path.insert(0, '%s') \n"+''' % (directory, directory)
                ##break

        #cmdString += r'''"import ka_rigTools.ka_hotkeys \n"+'''
        #cmdString += r'''"ka_rigTools.ka_hotkeys.Hotkeys.%s.command() \n"'''%(keybind.__name__)
        #cmdString += r''')'''

        cmdString = """python("import sys, os; import pymel.core as pymel;\\ndirectory = os.path.abspath(os.path.join(cmds.internalVar(userScriptDir=True), '..', '..', 'scripts'))\\nif sys.path[0] != directory: sys.path.insert(0, directory)\\nimport ka_rigTools.ka_hotkeys\\nka_rigTools.ka_hotkeys.Hotkeys.%s.command()")""" % (keybind.__name__)

        cmdReleaseName = 'ka_nameCommand_'+keybind.__name__+'_release'
        cmdReleaseString = r'python("import ka_rigTools.ka_hotkeys ;ka_rigTools.ka_hotkeys.Hotkeys.%s.release_command()")' % (keybind.__name__)

        #create the nameCommands for push and release...
        cmds.nameCommand( cmdName, command=cmdString , annotation=cmdName, default=0,)
        cmds.nameCommand( cmdReleaseName, command=cmdReleaseString  , annotation=cmdReleaseName, default=0,)

        #assign the name commands to hotkeys based on the variables in their corresponding method
        if cmds.hotkeyCheck( keyString = keybind.pushKey, altModifier = keybind.alt, ctrlModifier = keybind.ctrl, ):
            cmds.hotkey(keyShortcut=keybind.pushKey, name='', altModifier=keybind.alt, ctrlModifier=keybind.ctrl, )
        else:
            cmds.hotkey(keyShortcut = keybind.pushKey, name = cmdName, altModifier = keybind.alt, ctrlModifier = keybind.ctrl, )
        cmds.hotkey( keyShortcut = keybind.pushKey, releaseName = cmdReleaseName, altModifier = keybind.alt, ctrlModifier = keybind.ctrl, )





class Hotkeys():

    """A collection of Classes, where each represents a hotkey and the command it should preform"""

    def __init__(self):
        """ sets up all sub classes of self as named commands and hotkeys"""


        #create list of classes within the current class "that do not start with '_'
        membersOfClass = inspect.getmembers(self)
        self.listOfKeyBinds = []
        for member in membersOfClass:
            #if class does not start with a '_', member is a tuple ie: ('a', <class ka_rigTools.hotkeys.a at 0x00000000321292B0>)
            if not member[0][0] == '_':
                self.listOfKeyBinds.append(member[1])    #store the acual method


# A ######################################################################################################################
    class a():#keybind--------------------------------------------------------------------------
        pushKey='a';  ctrl=False;  alt=False;


        @staticmethod
        def command():
            context = ka_context.newContext()

            if cmds.currentCtx() == 'artAttrSkinContext':
                ka_weightPainting.toggleAddReplace()

            elif context.getUiTypeUnderMouse() == 'model':
                ka_display.addToIsolateSelect()

            elif context.getUiTypeUnderMouse() == 'hyperShade':
                mel.eval('ka_hgAdd();')

        @staticmethod
        def release_command():
            pass

    class a_alt():#keybind--------------------------------------------------------------------------
        pushKey='a';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            import ka_rigTools.ka_display as ka_display    #;reload(ka_display)

            panelUnderPointer = cmds.getPanel( underPointer=True )
            toolContext = cmds.currentCtx()

            if toolContext == 'artAttrSkinContext':
                ka_display.isolateSelection(mode='skinning')

            else:
                ka_display.isolateSelection()
        @staticmethod
        def release_command():
            pass


    class A():#keybind--------------------------------------------------------------------------
        pushKey='A';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            context = ka_context.newContext()

            if context.getUiTypeUnderMouse() == 'model':
                ka_display.removeFromIsolateSelect()

            elif context.getUiTypeUnderMouse() == 'hyperShade':
                mel.eval('ka_hgRemove();')

        @staticmethod
        def release_command():
            pass


    class a_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='a';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            ka_util.cycleAttributeEditorChannelBox()

        @staticmethod
        def release_command():
            pass

    class A_ctrl_alt():#keybind--------------------------------------------------------------------------
        pushKey='A';  ctrl=True;  alt=True;

        @staticmethod
        def command():
            cmds.evalDeferred('''import pymel.core as pymel \na = pymel.ls(selection=True)[0]\ns=pymel.ls(selection=True)''')

        @staticmethod
        def release_command():
            pass

# B ######################################################################################################################
    class b():#keybind--------------------------------------------------------------------------
        pushKey='b';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            from PyQt4 import QtGui, QtCore, uic

            mel.eval('''artActivateScreenSlider "upper_radius"''')
            print('b')
            OOOOOOO = 'QtGui.qApp.focusWidget()';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))

        @staticmethod
        def release_command():
            mel.eval('''artDeactivateScreenSlider''')


# C ######################################################################################################################
    class c():#keybind--------------------------------------------------------------------------
        pushKey='c';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            if ka_util.selectionIsComponent():
                ka_weightPainting.copySkinWeights()

            else:
                mel.eval('snapMode -curve 1')
            #if ka_util.selectionIsComponent():
                #ka_weightPainting.copySkinWeights()

        @staticmethod
        def release_command():
            mel.eval('snapMode -curve 0')

    class C():#keybind--------------------------------------------------------------------------
        pushKey='C';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            if ka_util.selectionIsComponent():
                ka_weightPainting.pasteSkinWeights()
        @staticmethod
        def release_command():
            pass

    class c_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='c';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            if ka_util.selectionIsComponent():
                ka_weightPainting.copySkinWeights()
                #mel.eval('ka_copyAttrValues;')
                print('I copied! RAWR')
            else:
                pass
        @staticmethod
        def release_command():
            pass

    class c_alt():#keybind--------------------------------------------------------------------------
        pushKey='c';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            ka_transforms.snap(r=1)
#            if ka_util.selectionIsComponent():
#                ka_weightPainting.copySkinWeights()

        @staticmethod
        def release_command():
            pass

# D ######################################################################################################################
    class d_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='d';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            importlib.reload(ka_util)
            ka_util.contextDuplicate()

        @staticmethod
        def release_command():
            pass

    class D_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='D';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            print('delete history')
            cmds.delete(constructionHistory=True,)

        @staticmethod
        def release_command():
            pass


# E ######################################################################################################################
    class e():#keybind--------------------------------------------------------------------------
        pushKey='e';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            mel.eval('buildRotateMM')

        @staticmethod
        def release_command():
            mel.eval('destroySTRSMarkingMenu RotateTool')


    class e_alt():#keybind--------------------------------------------------------------------------
        pushKey='e';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            try:
                mel.eval('deleteUI -window "componentEditorPanel1Window";')
            except:
                pass
            mel.eval('tearOffPanel "Component Editor" "componentEditorPanel" true;')

        @staticmethod
        def release_command():
            pass

    class E():#keybind--------------------------------------------------------------------------
        pushKey='E';  ctrl=False;  alt=False;

        @staticmethod
        def command():
#            ka_util.selectEdgeLoopFromVertSelection()
            mel.eval('SelectEdgeLoopSp;')

        @staticmethod
        def release_command():
            pass
# F ######################################################################################################################
    class f():#keybind--------------------------------------------------------------------------
        pushKey='f';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            if cmds.currentCtx() == 'artAttrSkinContext':
                ka_weightPainting.focusOnInfluence()
            else:
                mel.eval('fitPanel -selected')

        @staticmethod
        def release_command():
            pass

    class f_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='f';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            from . import ka_filterSelection as ka_filterSelection #;reload(ka_filterSelection)
            ka_filterSelection.openUI()

        @staticmethod
        def release_command():
            pass

# G ######################################################################################################################
    class g_alt():#keybind--------------------------------------------------------------------------
        pushKey='g';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            ka_util.modelFilterGeoOnly(filterList=['nurbsSurfaces', 'polymeshes'])


        @staticmethod
        def release_command():
            pass


# H ######################################################################################################################
    class h():#keybind--------------------------------------------------------------------------
        pushKey='h';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            if ka_util.selectionIsComponent():

                ka_weightPainting.copySkinWeights()
                ka_menu.press(buildMenuOverride='paintPallet', sliderMode='pasteWeights')


        @staticmethod
        def release_command():
            ka_menu.release(sliderMode='pasteWeights')

    class h_alt():#keybind--------------------------------------------------------------------------
        pushKey='h';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            mel.eval('hotkeyEditor')

        @staticmethod
        def release_command():
            pass
# I ######################################################################################################################
    class i_alt():#keybind--------------------------------------------------------------------------
        pushKey='i';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            #mel.eval('ka_invertSelectionOrder')
            ka_util.reverseSelectionOrder()
        @staticmethod
        def release_command():
            pass

# K ######################################################################################################################
    class k():#keybind--------------------------------------------------------------------------
        pushKey='k';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            #mel.eval('performSetKeyframeArgList 1 {"0", "animationList"}')
            importlib.reload(ka_advancedJoints)
            ka_advancedJoints.setKeyframes()

        @staticmethod
        def release_command():
            pass

    class K():#keybind--------------------------------------------------------------------------
        pushKey='K';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            importlib.reload(ka_util)
            ka_util.setKeyframes()

        @staticmethod
        def release_command():
            pass

    class k_alt():#keybind--------------------------------------------------------------------------
        pushKey='k';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            mel.eval('tearOffPanel "Graph Editor" "graphEditor" true;')

        @staticmethod
        def release_command():
            pass

# N ######################################################################################################################
    class n():#keybind--------------------------------------------------------------------------
        pushKey='n';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_util.toggleRotationAxis()


        @staticmethod
        def release_command():
            ka_util.objectSelectMode(release=True)

    class n_alt():#keybind--------------------------------------------------------------------------
        pushKey='n';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            selection = cmds.ls(selection=True)
            shapes = cmds.listRelatives( shapes=True, path=True)

            if shapes:
                shapeType = cmds.nodeType(shapes[0])
                if shapeType == 'mesh':
                    mel.eval('ToggleFaceNormalDisplay;')


        @staticmethod
        def release_command():
            ka_util.objectSelectMode(release=True)

# M ######################################################################################################################
    class m_alt():#keybind--------------------------------------------------------------------------
        pushKey='m';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            if ka_util.selectionIsComponent():
                mel.eval('polyMergeToCenter')
            else:
                importlib.reload(ka_util)
                ka_transforms.snap(m=1)

        @staticmethod
        def release_command():
            pass

# O ######################################################################################################################
    class o_alt():#keybind--------------------------------------------------------------------------
        pushKey='o';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            mel.eval('tearOffPanel "Outliner" "outlinerPanel" false;')

        @staticmethod
        def release_command():
            pass

# P ######################################################################################################################
    class p_alt():#keybind--------------------------------------------------------------------------
        pushKey='p';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            mel.eval('_uoff(); togglePlayback; _uon()')

        @staticmethod
        def release_command():
            pass




# Q ######################################################################################################################
    class q():#keybind--------------------------------------------------------------------------
        pushKey='q';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_util.objectSelectMode()

        @staticmethod
        def release_command():
            ka_util.objectSelectMode(release=True)

    class q_alt():#keybind--------------------------------------------------------------------------
        pushKey='q';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            ka_util.componentSelectMode()
            mel.eval('global string $gSelect; setToolTo $gSelect;')
        @staticmethod
        def release_command():
            pass

    class Q_alt():#keybind--------------------------------------------------------------------------
        pushKey='Q';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            selection = pymel.ls(selection=True)
            ka_util.componentSelectMode()
            mel.eval('global string $gSelect; setToolTo $gSelect;')
            pymel.select(selection)

        @staticmethod
        def release_command():
            pass

    class q_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='q';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            mel.eval('artSelectToolScript 4')

        @staticmethod
        def release_command():
            mel.eval('artSelectToolScript 3')

    class Q():#keybind--------------------------------------------------------------------------
        pushKey='Q';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            mel.eval('artSelectToolScript 4')
            ka_display.updateIsolateSelection()

        @staticmethod
        def release_command():
            #mel.eval('artSelectToolScript 3')
            pass
# R ######################################################################################################################
    class r_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='r';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            import ka_rigTools.ka_rename; importlib.reload(ka_rigTools.ka_rename)
            ka_rigTools.ka_rename.openUI()

        @staticmethod
        def release_command():
            pass

    class r_alt():#keybind--------------------------------------------------------------------------
        pushKey='r';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            mel.eval('ReferenceEditor;')

        @staticmethod
        def release_command():
            pass

    class R_ctrlAlt():#keybind--------------------------------------------------------------------------
        pushKey='R';  ctrl=True;  alt=True;

        @staticmethod
        def command():
            ka_util.openLastScene()

        @staticmethod
        def release_command():
            pass

# S ######################################################################################################################
    class s():#keybind--------------------------------------------------------------------------
        pushKey='s';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            panelUnderPointer = cmds.getPanel( underPointer=True )

            #reload(ka_menu_modelEditor)
            #ka_menu.press()
            if cmds.currentCtx() == 'artAttrSkinContext':
                ka_weightPainting.toggleSmooth()
                #mel.eval('ka_MM_toggleSmooth;')

            #elif 'modelPanel' in panelUnderPointer and ka_util.selectionIsComponent():
                #ka_weightPainting.pasteSkinWeights()

            else:
                mel.eval('ka_snapScaleAndRotate();')
                mel.eval('ka_hgInputsOutputs();')

        @staticmethod
        def release_command():
            ka_menu.release()
            mel.eval('ka_snapScaleAndRotate_release();')


    class s_alt():#keybind--------------------------------------------------------------------------
        pushKey='s';  ctrl=False;  alt=True;

        @staticmethod
        def command():

            mel.eval('tearOffPanel "Hypershade" "hyperShadePanel" true;')
            mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "showBottomTabsOnly");')
            mel.eval('ka_hyperGraphMM();')

        @staticmethod
        def release_command():
            pass

    class S_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='S';  ctrl=True;  alt=False;

        @staticmethod
        def command():

            mel.eval('checkForUnknownNodes(); projectViewer SaveAs')

        @staticmethod
        def release_command():
            pass

# T ######################################################################################################################
    class t():#keybind--------------------------------------------------------------------------
        pushKey='t';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            importlib.reload(ka_scrubSlider)
            ka_scrubSlider.timeSliderScrub()

        @staticmethod
        def release_command():
            #ka_scrubSlider.release()
            pass

    class T():#keybind--------------------------------------------------------------------------
        pushKey='T';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            mel.eval('''string $sel[] = `ls -sl`; if ( size($sel) > 0 ) {
string $nodesInDAG[] = `ls -dag -shapes $sel[0]`;
if ( size($nodesInDAG) > 0 ) {
if ( `nodeType $nodesInDAG[0]` == "rnkLight" ) { select $nodesInDAG[0]; }
}
}
setToolTo ShowManips''')

        @staticmethod
        def release_command():
            pass


    class t_alt():#keybind--------------------------------------------------------------------------
        pushKey='t';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            mel.eval('if (`scriptedPanel -q -exists scriptEditorPanel1`) { scriptedPanel -e -to scriptEditorPanel1; showWindow scriptEditorPanel1Window; selectCurrentExecuterControl; }else { CommandWindow; };')

        @staticmethod
        def release_command():
            pass


# V ######################################################################################################################
    class v():#keybind--------------------------------------------------------------------------
        pushKey='v';  ctrl=False;  alt=False;

        #@echo
        @staticmethod
        def command():
            if not 'moveSuperContext' == cmds.currentCtx():
                if cmds.currentCtx() == 'artAttrSkinContext':
                    ka_menu.press(buildMenuOverride='paintPallet',)

                elif ka_util.selectionIsComponent():
                    #ka_menu.press(buildMenuOverride='paintPallet', sliderMode='parallelBlend')
                    #ka_scrubSlider.toggleSlider('weight_parallelBlend_Scrub')
                    importlib.reload(ka_scrubSlider)
                    ka_scrubSlider.weight_parallelBlend_Scrub()

                else:
                    mel.eval('snapMode -point 1;')
            else:
                mel.eval('snapMode -point 1;')

        @staticmethod
        def release_command():
            mel.eval('snapMode -point 0;')
            #ka_menu.release(sliderMode='parallelBlend')

    class V():#keybind--------------------------------------------------------------------------
        pushKey='V';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            pass
            ka_menu.press(buildMenuOverride='paintPallet', sliderMode='pasteWeights')

        @staticmethod
        def release_command():
            pass
            ka_menu.release(sliderMode='pasteWeights')


    class v_alt():#keybind--------------------------------------------------------------------------
        pushKey='v';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            if ka_util.selectionIsComponent() or cmds.currentCtx() == 'artAttrSkinContext':
#                ka_menu.press(buildMenuOverride='paintPallet', sliderMode='blendWeights')
                ka_menu.press(buildMenuOverride='paintPallet', sliderMode='pasteWeights')

            else:
                print('snap')
                ka_transforms.snap(t=1)

        @staticmethod
        def release_command():
#            ka_menu.release(sliderMode='blendWeights')
            ka_menu.release(sliderMode='pasteWeights')


    class v_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='v';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            ka_menu.press(buildMenuOverride='paintPallet', sliderMode='pasteWeights')
            ka_weightPainting.pasteSkinWeights()

        @staticmethod
        def release_command():
            ka_menu.release(sliderMode='pasteWeights')

    class V_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='V';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            #reload(ka_weightPainting)
            #ka_weightPainting.pasteSkinWeights_fromStrandStartToEnd()
            ka_rigTools.core.pasteSkinWeightsAlongStrand()
            #global oneThirdWeightPasteToggle
            #if oneThirdWeightPasteToggle:
                #ka_weightPainting.pasteSkinWeights(weightedAverage=66.666)
                #oneThirdWeightPasteToggle = False
            #else:
                #ka_weightPainting.pasteSkinWeights(weightedAverage=133.334)
                #oneThirdWeightPasteToggle = True


        @staticmethod
        def release_command():
            pass

# W ######################################################################################################################


    class W():#keybind--------------------------------------------------------------------------
        pushKey='W';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            mel.eval('ka_wireframeOnShaded();')

        @staticmethod
        def release_command():
            pass

    class w_alt():#keybind--------------------------------------------------------------------------
        pushKey='w';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            mel.eval('artAttrSkinToolScript 4')
            ka_display.updateIsolateSelection()

        @staticmethod
        def release_command():
            #mel.eval('artAttrSkinToolScript 3')
            pass

# X ######################################################################################################################
    class x():#keybind--------------------------------------------------------------------------
        pushKey='x';  ctrl=False;  alt=False;

        @staticmethod
        def command():

            if cmds.currentCtx() == 'artAttrSkinContext':
                ka_weightPainting.togglePaint()
            else:
                ka_display.xRayMode()
                mel.eval('snapMode -grid 1;')
                #mel.eval('ka_xRay();')
            #ka_transforms.snap(t=1)


            #mel.eval('ka_MM_toggleAddReplace;')

        @staticmethod
        def release_command():
            if not cmds.currentCtx() == 'artAttrSkinContext':
                ka_display.xRayMode(False)
                ka_display.jointXRayMode(False)

            #mel.eval('ka_xRay_release();')
            mel.eval('snapMode -grid 0;')

    class X():#keybind--------------------------------------------------------------------------
        pushKey='X';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_display.jointXRayMode()
            #mel.eval('string $currentPanel = `getPanel -withFocus`; modelEditor -e -jointXray (!`modelEditor -q -jointXray $currentPanel`) $currentPanel;')

        @staticmethod
        def release_command():
            pass

    class X_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='X';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            pass
        @staticmethod
        def release_command():
            pass

    class x_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='x';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            ka_display.xRayMode()


        @staticmethod
        def release_command():
            pass

    class x_alt():#keybind--------------------------------------------------------------------------
        pushKey='x';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            ka_transforms.snap(s=1)

        @staticmethod
        def release_command():
            pass
# Z ######################################################################################################################
    class Z_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='Z';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            ka_util.resetAttrs()

        @staticmethod
        def release_command():
            pass

    class z_alt():#keybind--------------------------------------------------------------------------
        pushKey='z';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            importlib.reload(ka_util)
            print('yaaa')
            ka_transforms.snap(a=1)

        @staticmethod
        def release_command():
            pass
# DOWN ######################################################################################################################
    class DOWN():#keybind--------------------------------------------------------------------------
        pushKey='DOWN';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_selection.pickWalk('down')

        @staticmethod
        def release_command():
            pass

    class DOWN_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='DOWN';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            ka_selection.pickWalk('down', additive=True)

        @staticmethod
        def release_command():
            pass

    class DOWN_alt():#keybind--------------------------------------------------------------------------
        pushKey='DOWN';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            cmds.select(hierarchy=True)

        @staticmethod
        def release_command():
            pass
# UP ######################################################################################################################
    class UP():#keybind--------------------------------------------------------------------------
        pushKey='UP';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_selection.pickWalk('up' )

        @staticmethod
        def release_command():
            pass

    class UP_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='UP';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            ka_selection.pickWalk('up', additive=True)

        @staticmethod
        def release_command():
            pass
# RIGHT ######################################################################################################################
    class RIGHT():#keybind--------------------------------------------------------------------------
        pushKey='RIGHT';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_selection.pickWalk('right' )

        @staticmethod
        def release_command():
            pass

    class RIGHT_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='RIGHT';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            ka_selection.pickWalk('right', additive=True)

        @staticmethod
        def release_command():
            pass

# LEFT ######################################################################################################################
    class LEFT():#keybind--------------------------------------------------------------------------
        pushKey='LEFT';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_selection.pickWalk('left' )

        @staticmethod
        def release_command():
            pass

    class LEFT_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='LEFT';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            ka_selection.pickWalk('left', additive=True)


        @staticmethod
        def release_command():
            pass

# insert ######################################################################################################################
    class insert_alt():#keybind--------------------------------------------------------------------------
        pushKey='insert';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            ka_util.editRotationAxis()

        @staticmethod
        def release_command():
            pass

# tilda(`) ######################################################################################################################
    class tilda():#keybind--------------------------------------------------------------------------
        pushKey='`';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            #ka_menu.press()
            print('go')
            ka_reload.reloadIrsModules()

            kMenu_menus.popMenu()
        @staticmethod
        def release_command():
            ka_menu.release()

    class tilda_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='`';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            importlib.reload(ka_attrTool_UI)
            ka_attrTool_UI.press()

        @staticmethod
        def release_command():
            #ka_attrTool_UI.release()
            pass

    class tilda_alt():#keybind--------------------------------------------------------------------------
        pushKey='`';  ctrl=False;  alt=True;

        @staticmethod
        def command():
            print('__ KA RELOAD __')
            #import kMenu.kMenu_menus
            #reload(kMenu.kMenu_menus)
            ##kMenu.kMenu_menus.popMenu(clearFirst=True)
            ka_reload.reloadModules()
            kMenu.clearUnpinnedKMenus(onlyNonPinned=False)

        @staticmethod
        def release_command():
            #import ka_qtWidgets
            #ka_qtWidgets.remove_kaQMenu22()
            pass

# \ ######################################################################################################################
    class forwardslash_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='\\';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            mel.eval('setToolTo polySplitContext')

        @staticmethod
        def release_command():
            mel.eval('setToolTo polySplitContext ; toolPropertyWindow')

    class forwardslash():#keybind--------------------------------------------------------------------------
        pushKey='\\';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            mel.eval('polySelectEditCtx -e -mode 1 polySelectEditContext; setToolTo polySelectEditContext')

        @staticmethod
        def release_command():
            mel.eval('polySelectEditCtx -e -mode 1 polySelectEditContext; setToolTo polySelectEditContext; toolPropertyWindow')

# 1 ######################################################################################################################
    class one():#keybind--------------------------------------------------------------------------
        pushKey='1';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_util.setTransformManipulatorMode('world')

        @staticmethod
        def release_command():
            pass


# 2 ######################################################################################################################
    class two():#keybind--------------------------------------------------------------------------
        pushKey='2';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_util.setTransformManipulatorMode('local')

        @staticmethod
        def release_command():
            pass

# 3 ######################################################################################################################
    class three():#keybind--------------------------------------------------------------------------
        pushKey='3';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            ka_util.setTransformManipulatorMode('trueValues')

        @staticmethod
        def release_command():
            pass

# ! ######################################################################################################################
    class exclamation():#keybind--------------------------------------------------------------------------
        pushKey='!';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            mel.eval('setDisplaySmoothness 1')

        @staticmethod
        def release_command():
            pass


# @ ######################################################################################################################
    class addressSign():#keybind--------------------------------------------------------------------------
        pushKey='@';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            mel.eval('setDisplaySmoothness 2')

        @staticmethod
        def release_command():
            pass

# # ######################################################################################################################
    class pound():#keybind--------------------------------------------------------------------------
        pushKey='#';  ctrl=False;  alt=False;

        @staticmethod
        def command():
            mel.eval('setDisplaySmoothness 3')

        @staticmethod
        def release_command():
            pass

# = ######################################################################################################################
    class equals():#keybind--------------------------------------------------------------------------
        pushKey='=';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            mel.eval('PolySelectTraverse 1')

        @staticmethod
        def release_command():
            pass


    class equals_ctrl():#keybind--------------------------------------------------------------------------
        pushKey='+';  ctrl=True;  alt=False;

        @staticmethod
        def command():
            import ka_rigTools.ka_selection as ka_selection; importlib.reload(ka_selection)
            ka_selection.islandSelectComponents()

        @staticmethod
        def release_command():
            pass






