#====================================================================================
#====================================================================================
#
# ka_reload
#
# DESCRIPTION:
#   reloads all ka_ modules
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

import ka_rigTools.ka_psd as ka_psd
import ka_rigTools.kMenu as kMenu
import ka_rigTools.ka_advancedJoints as ka_advancedJoints
import ka_rigTools.ka_advancedJoints.ka_advancedJoints_commands as ka_advancedJoints_commands
import ka_rigTools.ka_advancedJoints.ka_advancedJoints_volumeRotator as ka_advancedJoints_volumeRotator
import ka_rigTools.ka_animation as ka_animation
import ka_rigTools.ka_attr as ka_attr
import ka_rigTools.ka_attrTool.attrCommands as attrCommands
import ka_rigTools.ka_attrTool.attrFavorites as attrFavorites
import ka_rigTools.ka_attrTool.attributeObj as attributeObj
import ka_rigTools.ka_attrTool.ka_attrTool_UI as ka_attrTool_UI
import ka_rigTools.ka_clipBoard as ka_clipBoard
import ka_rigTools.ka_constraints as ka_constraints
import ka_rigTools.ka_context as ka_context
import ka_rigTools.ka_controls as ka_controls
import ka_rigTools.ka_display as ka_display
import ka_rigTools.ka_filterSelection as ka_filterSelection
import ka_rigTools.ka_hyperShade as ka_hyperShade


import ka_rigTools.ka_irs.core as irsCore
import ka_rigTools.ka_irs.irsObject.irsFeature as irsFeature
import ka_rigTools.ka_irs.irsObject.irsLimb as irsLimb
import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb as irsLimb

import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_bipedLeg.irsLimb_bipedLeg as irsLimb_bipedLeg
import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_bipedLeg.features.irsLimb_bipedLegFeature_fk as irsLimb_bipedLegFeature_fk
import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_bipedLeg.features.irsLimb_bipedLegFeature_ik as irsLimb_bipedLegFeature_ik

import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_spine.irsLimb_spine as irsLimb_spine
import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_spine.features.irsLimb_spineFeature_fk as irsLimb_spineFeature_fk
import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_spine.features.irsLimb_spineFeature_ik as irsLimb_spineFeature_ik

import ka_rigTools.ka_irs.irsObject.irsObject as irsObject
import ka_rigTools.ka_irs.irsObject.irsRig.irsRig as irsRig
import ka_rigTools.ka_irs.irsObject.irsRig.irsRig_animation as irsRig_animation


import ka_rigTools.ka_naming as ka_naming
import ka_rigTools.ka_math as ka_math
import ka_rigTools.ka_mayaCommandOverrides as ka_mayaCommandOverrides
import ka_rigTools.ka_menu as ka_menu
import ka_rigTools.ka_menu.ka_menu_hyperShade as ka_menu_hyperShade
import ka_rigTools.ka_menu.ka_menu_modelEditor as ka_menu_modelEditor
import ka_rigTools.ka_menu.ka_menu_paintPallet as ka_menu_paintPallet
import ka_rigTools.ka_naming as ka_naming
import ka_rigTools.ka_preference as ka_preference
import ka_rigTools.ka_pymel as ka_pymel
import ka_rigTools.ka_python as ka_python
import ka_rigTools.ka_qtWidgets as ka_qtWidgets
import ka_rigTools.ka_rename as ka_rename
import ka_rigTools.ka_rigAerobics as ka_rigAerobics
import ka_rigTools.ka_rigQuery as ka_rigQuery
import ka_rigTools.ka_rigSetups.ka_advancedFK as ka_advancedFK
import ka_rigTools.ka_scrubSlider as ka_scrubSlider
import ka_rigTools.ka_selection as ka_selection
import ka_rigTools.ka_shapes as ka_shapes
import ka_rigTools.ka_skinCluster as ka_skinCluster
import ka_rigTools.ka_transforms as ka_transforms
import ka_rigTools.ka_util as ka_util
import ka_rigTools.ka_weightBlender as ka_weightBlender
import ka_rigTools.ka_weightPainting as ka_weightPainting
import ka_rigTools.core as core
import ka_rigTools.kMenu.kMenu_menus as kMenu_menus
import importlib

LOW_LEVEL_MODULES = [
ka_python,
ka_pymel,
ka_mayaCommandOverrides,
ka_preference,
ka_context,
]

MID_LEVEL_MODULES = [
ka_math,
ka_naming,
]

STANDARD_MODULES = [
ka_advancedJoints,
ka_advancedJoints_commands,
ka_advancedJoints_volumeRotator,
ka_animation,
attrCommands,
attrFavorites,
attributeObj,
ka_attr,

ka_clipBoard,
ka_constraints,
ka_controls,
ka_display,
ka_filterSelection,
ka_hyperShade,
ka_qtWidgets,
ka_rigAerobics,
ka_rigQuery,
ka_advancedFK,
ka_selection,
ka_shapes,
ka_skinCluster,
ka_transforms,
ka_util,
ka_weightBlender,
ka_weightPainting,
]

IRS_MODULES = [
irsCore,
irsObject,
irsRig,
irsRig_animation,
irsFeature,
irsLimb,
irsLimb_bipedLeg,
irsLimb_bipedLegFeature_fk,
irsLimb_bipedLegFeature_ik,
irsLimb_spine,
irsLimb_spineFeature_fk,
irsLimb_spineFeature_ik,

]


UI_MODULES = [
ka_attrTool_UI,
ka_scrubSlider,

ka_menu,
ka_menu_hyperShade,
ka_menu_modelEditor,
ka_menu_paintPallet,

kMenu,
kMenu_menus,
]

ALL_MODULES = LOW_LEVEL_MODULES
ALL_MODULES += MID_LEVEL_MODULES
ALL_MODULES += STANDARD_MODULES
ALL_MODULES += IRS_MODULES
ALL_MODULES += UI_MODULES

def reloadIrsModules():
    for module in IRS_MODULES:
        if module != core:
            if module not in UI_MODULES:
                importlib.reload(module)

    print('fart')



def reloadModules():
    for module in ALL_MODULES:
        importlib.reload(module)


    ## low level
    #reload(ka_python)
    #reload(ka_pymel)
    #reload(ka_mayaCommandOverrides)
    #reload(ka_preference)
    #reload(ka_context)

    ## mid level
    #reload(ka_math)
    #reload(ka_rename)


    ## standard modules
    #reload(ka_advancedJoints)
    #reload(ka_advancedJoints_commands)
    #reload(ka_advancedJoints_volumeRotator)
    #reload(ka_animation)
    #reload(attrCommands)
    #reload(attrFavorites)
    #reload(attributeObj)
    #reload(ka_attrTool_UI)
    #reload(ka_clipBoard)
    #reload(ka_constraints)
    #reload(ka_controls)
    #reload(ka_display)
    #reload(ka_filterSelection)
    #reload(ka_hyperShade)
    #reload(ka_qtWidgets)
    #reload(ka_rigAerobics)
    #reload(ka_rigQuery)
    #reload(ka_advancedFK)
    #reload(ka_selection)
    #reload(ka_shapes)
    #reload(ka_skinCluster)
    #reload(ka_transforms)
    #reload(ka_util)
    #reload(ka_weightBlender)
    #reload(ka_weightPainting)

    ## irs
    #reload(irsObject)
    #reload(irsRig)
    #reload(irsRig_animation)
    #reload(irsFeature)
    #reload(irsLimb)
    #reload(irsLimb_bipedLegFeature_fk)
    #reload(irsLimb_bipedLegFeature_ik)
    #reload(irsLimb_bipedLeg)


    ## main entry point
    #reload(core)

    ## UIs
    #reload(ka_scrubSlider)

    #reload(ka_menu)
    #reload(ka_menu_hyperShade)
    #reload(ka_menu_modelEditor)
    #reload(ka_menu_paintPallet)

    #reload(kMenu)
    #reload(kMenu_menus)


def printImportString():

    keys = []
    for key in sys.modules:
        if key.startswith('ka_rigTools'):
            keys.append(key)

    modules = []
    modulesKeys = []
    for key in sorted(keys):
        module = sys.modules[key]
        if hasattr(module, '__package__'):
            if module.__package__:
                if module.__package__.startswith('ka_rigTools'):
                    if 'ka_reload' not in modulesKey:
                        if 'ka_hotkeys' not in modulesKey:
                            if 'ka_hotkeys' != modulesKey:
                                modules.append(module)
                                modulesKeys.append(key)

    for modulesKey in sorted(modulesKeys):
        if 'ka_reload' not in modulesKey:
            modulesKeyEnd = modulesKey.split('.')[-1]
            print('import %s as %s' % (modulesKey, modulesKeyEnd))

    print('\n')
    for modulesKey in sorted(modulesKeys):
        if 'ka_reload' not in modulesKey:
            modulesKeyEnd = modulesKey.split('.')[-1]
            print('reload(%s)' % (modulesKeyEnd))
