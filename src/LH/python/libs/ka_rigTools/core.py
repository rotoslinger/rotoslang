
#====================================================================================
#====================================================================================
#
# ka_rigTools.core
#
# DESCRIPTION:
#   An accsess point for commands in the ka_rigTools package
#
# DEPENDENCEYS:
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

import types
import os
import sip
import PyQt4
from PyQt4 import QtGui, QtCore, uic
from traceback import print_exc as printError

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as OpenMayaUI

from . import ka_preference

import ka_rigTools.ka_util as ka_util    #;reload(ka_util)
import ka_rigTools.ka_transforms as ka_transforms    #;reload(ka_transforms)

import ka_rigTools.ka_rigSetups.ka_advancedFK as ka_advancedFK    #;reload(ka_advancedFK)


import ka_rigTools.ka_python as ka_python    #;reload(ka_animation)
import ka_rigTools.ka_psd as ka_psd    #;reload(ka_animation)
import ka_rigTools.ka_rigAerobics as ka_rigAerobics    #;reload(ka_animation)
import ka_rigTools.ka_weightBlender as ka_weightBlender    #;reload(ka_animation)
import ka_rigTools.ka_animation as ka_animation    #;reload(ka_animation)
import ka_rigTools.ka_shapes as ka_shapes    #;reload(ka_shapes)
import ka_rigTools.ka_math as ka_math    #;reload(ka_pymel)
import ka_rigTools.ka_pymel as ka_pymel    #;reload(ka_pymel)
import ka_rigTools.ka_advancedJoints as ka_advancedJoints    #;reload(ka_advancedJoints)
import ka_rigTools.ka_display as ka_display    #;reload(ka_display)
import ka_rigTools.ka_weightPainting as ka_weightPainting    #;reload(ka_weightPainting)
import ka_rigTools.ka_hyperShade as ka_hyperShade    #;reload(ka_hyperShade)
import ka_rigTools.ka_skinCluster as ka_skinCluster    #;reload(ka_skinCluster)
import ka_rigTools.ka_context as ka_context    #;reload(ka_context)
import ka_rigTools.ka_selection as ka_selection    #;reload(ka_selection)
import ka_rigTools.ka_constraints as ka_constraints    #;reload(ka_constraints)
import ka_rigTools.ka_attrTool.attrCommands as attrCommands    #;reload(attrCommands)
import ka_rigTools.ka_advancedJoints.ka_advancedJoints_volumeRotator as ka_advancedJoints_volumeRotator    #;reload(ka_advancedJoints_volumeRotator)

import ka_rigTools.ka_rename as ka_rename
import ka_rigTools.ka_filterSelection as ka_filterSelection
import ka_rigTools.ka_attrTool.ka_attrTool_UI as ka_attrTool_UI    #;reload(ka_attrTool_UI)
import importlib

ALWAYS_RELOAD = True

class ToolObject(object):
    """And Object that represents a function and allows high level functionality to be added to all tools.
    It can also be queryied by UI generators (ie KMenu)"""

    def __init__(self, label='', function=None, icon=None, docFunc=None, context=None):
        self.label = label
        self.settings = []

        self.icon = icon
        self.context = context
        self._function = function

        if docFunc:
            self.__doc__ = docFunc.__doc__
        else:
            self.__doc__ = function.__doc__

        # get args and kwargs for the funcs
        self.toolArgs = []
        self.toolKwargs = {}
        if function.__defaults__:
            lenOfArgs = function.__code__.co_argcount - len(function.__defaults__)
        else:
            lenOfArgs = function.__code__.co_argcount

        for i in range(function.__code__.co_argcount):
            if i < lenOfArgs:
                self.toolArgs.append(function.__code__.co_varnames[i])

            else:
                self.toolKwargs[function.__code__.co_varnames[i]] = function.__defaults__[i-lenOfArgs]
        self.toolArgs = tuple(self.toolArgs)

        # make a list of all modules used by the function
        self.dependentModules = []
        self.ka_dependentModules = []
        globalVars = globals()
        for localVar in self._function.__code__.co_names:
            if localVar in globalVars:
                if isinstance(globalVars[localVar], types.ModuleType):
                    self.dependentModules.append(globalVars[localVar])
                    if 'ka_rigTools' in globalVars[localVar].__package__:
                        self.ka_dependentModules.append(globalVars[localVar])

    def __call__(self, *args, **kwargs):
        # use settings to modify args, and kwargs
        for settingObject in self.settings:
            settingValue = ka_preference.get(settingObject.settingLongName, None)
            if settingObject.settingName not in kwargs: # if not passed in explicitly
                if settingValue != None:
                    kwargs[settingObject.settingName] = settingValue

        # do nessisary reloads
        if ALWAYS_RELOAD:
            for module in self.ka_dependentModules:
                importlib.reload(module)

        # make repeatable
        argString = ''
        if args:
            for each in args:
                argString += str(each)+', '

        if kwargs:
            for key, item in kwargs.items():
                argString += str(key)+'='+str(item)+', '

        commandToRepeat = 'python("import ka_rigTools.core as ka_rigTools; ka_rigTools.'+self._function.__name__+'('+argString+')")'
        OOOOOOO = 'commandToRepeat';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))

        try:
            cmds.repeatLast(ac=commandToRepeat, acl=self._function.__name__)
        except:
            ka_python.printError()

        # call original function
        return self._function(*args, **kwargs)


class SettingObject(object):
    """And Object that represents a setting, of a tool, that can be queryied by UI generators"""

    def __init__(self, *args, **kwargs):
        self.settingName = args[0]
        self.toolObject = kwargs.get('toolObject', None)

        self.settingLongName = '%s__%s__setting' % (self.toolObject._function.__name__, self.settingName)
        self.valueType = kwargs.get('valueType', 'float')
        self.enumValues = kwargs.get('enumValues', None)
        self.minValue = kwargs.get('minValue', None)
        self.maxValue = kwargs.get('maxValue', None)

        self.defaultValue = self.toolObject.toolKwargs[self.settingName]

class Tool(object):
    """A decorator that creates a ToolObject from a function"""
    def __init__(self, label='', icon=None, docFunc=None, context=None):
        self.label = label
        self.icon = icon
        self.docFunc = docFunc
        self.context = context

    def __call__(self, f):
        #print 'tool __call__'

        toolObject = ToolObject(label=self.label, function=f, icon=self.icon, docFunc=self.docFunc, context=self.context)
        return toolObject


class Setting(object):
    """A decorator that creates a SettingObject and assosiates it to
    a ToolObject"""

    def __init__(self, *args, **kwargs ):
        self.args = args
        self.kwargs = kwargs


    def __call__(self, toolObject):
        self.kwargs['toolObject'] = toolObject
        settingObject = SettingObject(*self.args, **self.kwargs)
        toolObject.settings.insert(0, settingObject)

        return toolObject




# Create Nurbs Curves -------------------------------------------------------------------
@Tool(label='Cube')
def createShape_cube():
    """Creates a simple Nurbs Cube
    """
    return ka_shapes.createNurbsCurve('cube')


@Tool(label='Circle')
def createShape_circle():
    """Creates a simple Nurbs Circle
    """
    return ka_shapes.createNurbsCurve('circle')


@Tool(label='Square')
def createShape_square():
    """Creates a simple Nurbs Square
    """
    return ka_shapes.createNurbsCurve('square')

@Tool(label='Pyramid Pointer')
def createShape_pyramidPointer():
    """Creates a nurbs curve shaped like a Pyramid, which points at the transform
    """
    return ka_shapes.createNurbsCurve('pyramidPointer')




# Create Advance Joints -------------------------------------------------------------------
@Tool(label='Create Piston Joint Setup')
def createAdvanceJoint_pistonJoint():
    """Creates a joint setup that stretchs and twists between two locators.
    There is also an option to make the joint setup squash and strech
    """
    return ka_advancedJoints.muscleJoint()


@Tool(label='Create Ligament Joint Setup')
def createAdvanceJoint_ligamentJoint():
    """Creates a joint setup that stretchs and twists between two locators, while
    colliding with a central half sphere
    """
    return ka_advancedJoints.createBendMuscle()


@Tool(label='Create Advanced IK Spline Setup')
def createAdvanceJoint_advancedIkSpline():
    """Creates an ikSpline setup between each selected joint in a continues joint chain.
    Selection must be at least 2 joints long and include the first and last joint
    """
    return ka_advancedJoints.makeAdvancedIkSplineUI()


# Create RIG SETUP -------------------------------------------------------------------
@Tool(label='Create Advanced FK Setup')
def rigSetup_advancedFK():
    """DO NOT USE, WILL OPEN NEW SCENE WITHOUT SAVE
    Creates an advanced fk setup from the selected (positioned) controls.
    """
    return ka_advancedFK.createFromSelection()



# SELECTION TOOLS -------------------------------------------------------------------
@Tool(label='Reverse Selection Order')
def invertSelectionOrder():
    """Reverse the order of the current selection
    """
    return ka_selection.invertSelectionOrder()


@Tool(label='Island Select Components')
def islandSelectComponents():
    """Grows component selection until there are no more connected
    components to select
    """
    return ka_selection.islandSelectComponents()

@Tool(label='Store Selection')
def storeSelection():
    """Stores selection for to be used by tools that use
    this functionality
    """
    return ka_selection.storeSelection()


# DISPLAY TOOLS -------------------------------------------------------------------
@Tool(label='Hide Rotation Axis on All')
def hideRotationAxisForAll():
    """Hides the rotation axis display for all transforms in the scene
    """
    return ka_display.hideAllRotationAxis()


@Tool(label='Set IsolateSet', icon='isolateSelection.png')
def setIsolateSet():
    """Creates a set that the ka_display.isolateSelection will isolate instead
    of the current selection if it exists
    """
    return ka_display.setIsolateSet()


@Tool(label='Add Skinning Set From Viewport', icon='add.png')
def skinningDisplaySet_createFromScene():
    return ka_display.skinningDisplaySet_createFromScene()


@Tool(label='Create Skinning Display Set')
def skinningDisplaySet_create(*args, **kwargs):
    return ka_display.skinningDisplaySet_create(*args, **kwargs)

@Tool(label='Print recreate command for Skinning Display Set')
def skinningDisplaySet_printAll(*args, **kwargs):
    return ka_display.skinningDisplaySet_printAll(*args, **kwargs)


@Tool(label='Set Skinning Set in Viewport')
def setSkinningDisplaySet(skiningSet):
    return ka_display.setSkinningDisplaySet(skiningSet)


@Tool(label='Clear IsolateSet', icon='clear.png')
def clearIsolateSet():
    """clears the isolate select set, created by the setIsolateSet command
    """
    return ka_display.clearIsolateSet()


@Tool(label='Isolate Selection + Influences', icon='isolateSelection.png')
def isolateSelection_skinningMode():
    """Isolates the selected geometry and all the influences if that geometry has
    a skin cluster
    """
    return ka_display.isolateSelection(mode='skinning')


@Tool(label='Toggle Colored Wireframe on Effected Geo')
def toggleColorWireframeOnSelected():
    """Toggles the coloring of geometry wireframes if they are
    some how effected by the current selection
    """
    return ka_display.toggleColorWireframeOnSelected()


@Tool(label='Disable Draw Overrides on Selection')
def disableDrawOverrides_onSelection():
    """Disables the draw overrides on selected nodes and their related
    transform or shape.
    """
    return ka_display.ka_disableDrawingOverideOnSelection(enable=False)


@Tool(label='Enable Draw Overrides on Selection')
def enableDrawOverrides_onSelection():
    """Enables the draw overrides on selected nodes and their related
    transform or shape.
    """
    return ka_display.ka_disableDrawingOverideOnSelection(enable=True)




# DEFORMER TOOLS -------------------------------------------------------------------
@Tool(label='Hold All', icon='lock.png')
def holdInfluences():
    """Hold All Influences for the selected geo
    """
    return ka_weightPainting.holdAllInfluences()


@Tool(label='Unhold All', icon='unlock.png')
def unholdInfluences():
    """Unhold All Influences for the selected geo
    """
    return ka_weightPainting.unholdAllInfluences()


@Tool(label='Mirror Weights', icon='symmetry.png')
def mirrorWeights():
    """Mirrors skinCluster weights from one side of a geometry to the other.
    Also sets the joint labels for influences according to their name so the
    mirror operation will have less mistakes
    """
    ka_skinCluster.setSetJointLabelFromNameOnAll()
    return ka_weightPainting.mirrorWeights()


@Tool(label='Mirror Weights on Frame 1', icon='symmetry.png')
def mirrorWeights_onFrame1():
    """Same as mirror weights, but set the current time to 1 before,
    and set it back after.
    """
    currentTime = pymel.currentTime( query=True )
    pymel.currentTime( 1 )

    ka_skinCluster.setSetJointLabelFromNameOnAll()
    ka_weightPainting.mirrorWeights()

    pymel.currentTime( currentTime )


@Tool(label='Reset Skin Cluster',)
def resetSkinCluster():
    """Rebuilds the skin cluster with the same influences and weights, but using
    the current position of the influences. Also Fixes many issues stemming from
    empty array items in old skinClusters, and it creates a new deformer node with
    no empty array items.

    RESET - unlike bakeSkinCluster, this puts the envelope to 0 before doing anything
    so that the original mesh is not effected
    """
    return ka_weightPainting.resetSkin("reset")

@Tool(label='Reset Skin Cluster On Frame 1',)
def resetSkinCluster_onFrame1():
    """Same as reset skin cluster except that it will occure at frame 1 and then
    set the time back to the current frame
    """
    currentTime = pymel.currentTime( query=True )
    pymel.currentTime( 1 )
    ka_weightPainting.resetSkin("reset")
    pymel.currentTime( currentTime )


@Tool(label='Bake Skin Cluster',)
def bakeSkinCluster():
    """Rebuilds the skin cluster with the same influences and weights, but using
    the current position of the influences. Also Fixes many issues stemming from
    empty array items in old skinClusters, and it creates a new deformer node with
    no empty array items.

    BAKE - unlike resetSkinCluster, this freezes the skinCluster deformation into
    the original mesh
    """
    return ka_weightPainting.resetSkin("bake")


@Tool(label='Copy Skin Weights',)
def copySkinWeights():
    """Copies the skin weights for the selected points. If more than 1 is selected
    than the average of all the points weights will be the value copied. If two
    points are selected, it will be possible to blend between them with the paste
    weights slider

    """
    ka_weightPainting.copySkinWeights()

@Tool(label='Paste Skin Weights',)
def pasteSkinWeights():
    """pastes skin weights copied earlier using the Copy Skin Weights Command"""
    ka_weightPainting.pasteSkinWeights()


@Tool(label='Delete All Bind Pose Nodes',)
def deleteAllBindPoses():
    """Deletes all bind pose nodes in the scene, as they are not used in modern
    rigging, and block certain maya functions
    """
    return ka_weightPainting.deleteAllBindPoses()


@Tool(label='Paste Skin Weights Along Strand',)
def pasteSkinWeightsAlongStrand():
    """pastes a mix of the skin weights belonging to the start and end point in your strand
    selection. The mix each point will recieve is based to the pre-deformed length of the edges
    between it, and the start/end. This will result in the first point being 100% of its own
    weight, and 0% of the end points weight"""

    return ka_weightPainting.pasteSkinWeights()


@Tool(label='Paste Skin Weights Along Strand',)
def pasteSkinWeightsAlongStrand():
    """pastes a mix of the skin weights belonging to the start and end point in your strand
    selection. The mix each point will recieve is based to the pre-deformed length of the edges
    between it, and the start/end. This will result in the first point being 100% of its own
    weight, and 0% of the end points weight"""

    return ka_weightPainting.pasteSkinWeights_fromStrandStartToEnd()


@Tool(label='Average Skin Weights with BOTH Strand Neighbores',)
def pasteSkinWeightsFromStrandNeighbores():
    """will paste weights that consist 1/3 from its original weight, and 1/3 from each of its 2
    perpendicular neighbors. If you can not imagine why this would be useful, think of the center
    line on a symmetrical character"""

    return ka_weightBlender.blendWithBothNeighbors()



@Tool(label='Cluster Deform Components',)
def clusterDeform_eachInSelection():
    """For each component in selection, create a cluster for
    it
    """
    return ka_util.clusterDeformSelection()


@Tool(label='abSymMesh Mirror',)
def mirrorMesh():
    """Without changing topology, mirrors changes made to the left side of the mesh
    to the right
    """
    return mel.eval('mel.eval("abSymCtl(\"msBn\")")')


@Tool(label='abSymMesh Flip',)
def flipMesh():
    """Without changing topology, flips changes made to the left side of the mesh to the right
    and visa versa.
    """
    return mel.eval('mel.eval("abSymCtl(\"msBn\")")')



# TRANSFORM TOOLS -------------------------------------------------------------------
@Tool(label='Remove non-Standard transform values',)
def removeNonStandardTransformValues():
    """Resets to default all non-standard transform (ie: not translate
    rotate or scale). This includes all pivot and shear attrs
    """
    return ka_transforms.removeNonStandardTransformValues()


@Tool(label='Translate Snap',)
def snap_translate():
    """Snaps all but the last selected transform, the the last selected transform's
    position
    """
    return ka_transforms.snap(t=1)

@Tool(label='Rotate Snap',)
def snap_rotate():
    """Snaps all but the last selected transform, the the last selected transform's
    orientation
    """
    return ka_transforms.snap(r=1)

@Tool(label='Scale Snap',)
def snap_scale():
    """Snaps all but the last selected transform, the the last selected transform's
    scale
    """
    return ka_transforms.snap(s=1)

@Tool(label='Aim Snap',)
def snap_aim():
    """Rotates the primary axis of all but the last selected transform, to point at the
    last transform in the selection. The secondary axis will point as close as possible
    to the direction it was facing initially (while still aiming the primary axis at it's
    target).
    """
    return ka_transforms.snap(a=1)

@Tool(label='Aim Snap',)
def snap_mirror():
    """Snaps a transform (position and orientation) to the other side of the designated axis (x).
    """
    return ka_transforms.snap(m=1)


@Tool(label='Un-Orient Joint',)
def removeJointOrients():
    """Resets the joint orient for the selected joints, while preserving the
    world space pose of the joint
    """
    return ka_transforms.removeJointOrients()


@Tool(label='Lock Translates',)
def lock_translates():
    """locks the translate attribute for the selcted items
    """
    return ka_transforms.lockTranslates()

@Tool(label='Unlock Translates',)
def unlock_translates():
    """unlocks the translate attribute for the selcted items
    """
    return ka_transforms.unlockTranslates()


@Tool(label='Lock Rotates',)
def lock_rotates():
    """locks the rotate attribute for the selcted items
    """
    return ka_transforms.lockRotates()

@Tool(label='Unlock Rotates',)
def unlock_rotates():
    """unlock the rotate attribute for the selcted items
    """
    return ka_transforms.unlockRotates()


@Tool(label='Lock Scales',)
def lock_scales():
    """locks the scale attribute for the selcted items
    """
    return ka_transforms.lockScales()

@Tool(label='Unlock Scales',)
def unlock_scales():
    """unlock the scale attribute for the selcted items
    """
    return ka_transforms.unlockScales()


@Tool(label='Lock Visibility',)
def lock_visibility():
    """locks the visibility attribute for the selcted items
    """
    return ka_transforms.lockVisibility()

@Tool(label='Unlock Visibility',)
def unlock_visibility():
    """unlock the visibility attribute for the selcted items
    """
    return ka_transforms.unlockVisibility()


@Tool(label='Lock ALL',)
def lockAllTransformAttrs():
    """locks all translate, rotate, scale and visibility attributes for the selcted items
    """
    return ka_transforms.lockVisibility()

@Tool(label='Unlock ALL',)
def unlockAllTransformAttrs():
    """unlocks all translate, rotate, scale and visibility attributes for the selcted items
    """
    return ka_transforms.unlockVisibility()




# TRANSFER and COPY / PASTE TOOLS -------------------------------------------------------------------
@Tool(label='Transfer Skin',)
def transferSkin():
    """Creates a skinCluster on all selected objects, except the first; who's skinCluster
    uses identical influences, and who's weight values are as close as possible to the first
    selected object.
    """
    return ka_weightPainting.xferSkin()

@Tool(label='Transfer Weights to Selected Components',)
def transferSelectedWeights():
    """Transfers the weights from the first selected geometry (or geometry points)
    to the second set of selected geometry points.
    """
    return ka_weightPainting.xferComponentWeights()

@Tool(label='Transfer Weights to Stored Component Selection',)
def xferComponentWeights_fromStoredSelection():
    """Transfers the weights from the first stored geometry (or geometry points)
    to the second set of selected geometry points.
    """
    return ka_weightPainting.xferComponentWeights_fromStoredSelection()

@Tool(label='Transfer Weights to Stored Component Selection on Frame 1',)
def xferComponentWeights_fromStoredSelection_onFrame1():
    """Transfers the weights from the first stored geometry (or geometry points)
    to the second set of selected geometry points.
    """
    currentTime = pymel.currentTime( query=True )
    pymel.currentTime( 1 )
    ka_weightPainting.xferComponentWeights_fromStoredSelection()
    pymel.currentTime( currentTime )


@Tool(label='Copy Shape',)
def copyShape():
    """Copys the value of the cvs on a nurbs curve into the clipBoard.
    """
    return mel.eval('ka_copyShape')


@Tool(label='Paste Shape',)
def pasteShape():
    """Pastes the value of the cvs from the clip board to the selected nurbs curves.
    """
    return mel.eval('ka_pasteShape("")')


@Tool(label='Paste Shape Flipped',)
def pasteShapeFlipped():
    """Pastes the flipped value of the cvs from the clip board to the selected nurbs curves.

    *flipped would be appropriate if the transformes where world space, but on opposite sides
    of the axis of symmetry

    """
    return mel.eval('ka_pasteShape("flipped")')


@Tool(label='Paste Shape Reversed',)
def pasteShapeReversed():
    """Pastes the *reversed value of the cvs from the clip board to the selected nurbs curves.

    *reversed would be appropriate if the source and destination where behaviourly mirrored
    from each other
    """
    return mel.eval('ka_pasteShape("reversed")')


# HIERARCHY TOOLS -------------------------------------------------------------------
@Tool(label='Create Zero Out Group',)
def createZero():
    """Creates a parent for the selected transforms in the exact same position,
    so that the given node's transforms will be 0,0,0.
    The first group created will be named the same and the original node, but with
    the suffix '_zro'. All nodes after that will be named with the suffix '_ofsA', '_ofsB',
   '_ofsC'...
    """
    return ka_transforms.makeZroGroup()




# CONSTRAINT TOOLS -------------------------------------------------------------------
@Tool(label='Surface Constraint',)
def constrain_surface(maintainOffset=False):
    """Constrains the all but the first selected transform to the Nurbs Surface of the first
    selected node. The constraint fully solves for position and rotation, and does not use
    any plug-ins
    """
    return ka_constraints.constrain(pointOnSurface=True)


@Tool(label='Curve Constraint',)
def constrain_curve(maintainOffset=False):
    """Constrains the all but the first selected transform to the Nurbs Curve of the first
    selected node. The constraint fully solves for position, and does not use any plug-ins
    """
    return mel.eval('ka_pointOnCurveConstraint')


@Tool(label='Point and Orient Constraint')
def constrain_pointOrient(maintainOffset=False):
    """A Shortcut command to do both a Point and Orient Constraint. This is a time saver because
    this command is repeatable
    """
    return ka_constraints.constrain(t=True, r=True)


@Tool(label='Point, Orient and Scale Constraint')
def constrain_pointOrientScale(maintainOffset=False):
    """A Shortcut command to do a Point, Orient and Scale Constraint. This is a time saver because
    this command is repeatable
    """
    return ka_constraints.constrain(t=True, r=True, s=True)


@Tool(label='Joint Orient Constraint')
def constrain_jointOrient(maintainOffset=False):
    """Same as an orient constraint, except that the rotate values are plugged into the jointOrient
    attribute.
    """
    return ka_util.jointOrientContraint()




# MISC TOOLS -------------------------------------------------------------------
@Tool(label='Print Selection as List')
def print_selection_asPythonList():
    """Prints the current selection as a formated python list of strings
    """
    return ka_util.printSelection_asPythonList()


@Tool(label='Print Curve Recreate Command')
def printSelectedCurveCreationCommand():
    """Prints the the command to recreate the selected nurbs curve
    """
    return ka_util.printSelectedCurveCreationCommand()


@Tool(label='Print Mesh Recreate Command')
def printSelectedCurveCreationCommand():
    """Prints the the command to recreate the selected mesh
    """
    return ka_util.printMeshCreateCmd()



# LOCK UNLOCK COMMANDS -------------------------------------------------------------------
@Tool(label='Lock Translate', docFunc=ka_transforms.lockTransformAttrs)
def lockTranslate():
    return ka_transforms.lockTransformAttrs(t=1)

@Tool(label='Unlock Translate', docFunc=ka_transforms.unlockTransformAttrs)
def unlockTranslate():
    return ka_transforms.unlockTransformAttrs(t=1)


@Tool(label='Lock Rotate', docFunc=ka_transforms.lockTransformAttrs)
def lockRotate():
    return ka_transforms.lockTransformAttrs(r=1)

@Tool(label='Unlock Rotate', docFunc=ka_transforms.unlockTransformAttrs)
def unlockRotate():
    return ka_transforms.unlockTransformAttrs(r=1)


@Tool(label='Lock Scale', docFunc=ka_transforms.lockTransformAttrs)
def lockScale():
    return ka_transforms.lockTransformAttrs(s=1)

@Tool(label='Unlock Scale', docFunc=ka_transforms.unlockTransformAttrs)
def unlockScale():
    return ka_transforms.unlockTransformAttrs(s=1)

@Tool(label='Lock Vis', docFunc=ka_transforms.lockTransformAttrs)
def lockVis():
    return ka_transforms.lockTransformAttrs(v=1)

@Tool(label='Unlock Vis', docFunc=ka_transforms.unlockTransformAttrs)
def unlockVis():
    return ka_transforms.unlockTransformAttrs(v=1)


@Tool(label='Lock Radius', docFunc=ka_transforms.lockTransformAttrs)
def lockRadius():
    return ka_transforms.lockTransformAttrs(radius=1)

@Tool(label='Unlock Radius', docFunc=ka_transforms.unlockTransformAttrs)
def unlockRadius():
    return ka_transforms.unlockTransformAttrs(radius=1)


@Tool(label='Lock All', docFunc=ka_transforms.lockTransformAttrs)
def lockAll():
    return ka_transforms.lockTransformAttrs(t=1, r=1, s=1, v=1, radius=1)

@Tool(label='Unlock All', docFunc=ka_transforms.unlockTransformAttrs)
def unlockAll():
    return ka_transforms.unlockTransformAttrs(t=1, r=1, s=1, v=1, radius=1)



# HIERARCHY COMMANDS -------------------------------------------------------------------
@Tool(label='Add Zero out group')
def addZeroOutGroup():
    """Addes a Zero out group as a parent of the selected transforms. It will
    be named with the suffix '_zro', unless a parent of that name already exists,
    in which case it will be named with '_ofsA', '_ofsB'...
    """

    return ka_transforms.makeZroGroup()


@Tool(label='Parent Shape')
def parentShape():
    """Will parent the shapes of all but the last selected transform, to the
    last selected transform. The former parents of those shapes will then be
    deleted.
    """

    return ka_util.shapeParent()


# CONSTRAINT COMMANDS -------------------------------------------------------------------
@Setting('maintainOffset', valueType='bool')
@Tool(label='Surface Constraint')
def constrain_surfaceConstraint(maintainOffset=False):
    """Will constrain all but the last selected node to the last selected Nurbs Surface.
    Those objects will be driven positionally and orientationally to closest point on the
    nurbs surface when it was constrained.

    -maintainOffset - <bool> - if True, that the offset of the node to the closest point on
                               the surface will be maintained
    """
    return ka_constraints.constrain(pointOnSurface=True)

@Tool(label='Non Twist Aim')
def constrain_nonTwistAim(maintainOffset=False):
    """creates an aim that will try to roll the same as it's parent
    """

    return ka_constraints.nonTwistAim()


@Tool(label='Curve Constraint')
def constrain_curveConstraint():
    """Will constrain the first selected object to the second selected Curve
    """

    mel.eval('ka_pointOnCurveConstraint')


@Tool(label='Aim Between Constraint')
def constrain_aimBetweenConstraint():
    """orients the first selected object's to be an average orientation of aiming its +x axis
    at the second selected object, and aiming its -x at the third selected object
    """
    ka_constraints.constrain(aimBetween=True)


@Setting('maintainOffset', valueType='bool')
@Tool(label='Point and Orient Constraint')
def constrain_pointAndOrient(maintainOffset=False):
    """Will apply a point and orient constraint on the second object
    constraining it to the first. (handy because it is repeatable)

    -maintainOffset - <bool> - if True, that the offset of the node to the closest point on
                           the surface will be maintained
    """
    return ka_constraints.constrain(t=True, r=True, withOffset=maintainOffset)


@Setting('maintainOffset', valueType='bool')
@Tool(label='Point, Orient, and Scale Constraint')
def constrain_pointOrientAndScale(maintainOffset=False):
    """Will apply a point and orient constraint on the second object
    constraining it to the first. (handy because it is repeatable)

    -maintainOffset - <bool> - if True, that the offset of the node to the closest point on
                           the surface will be maintained
    """
    return ka_constraints.constrain(t=True, r=True, s=True, withOffset=maintainOffset)

@Tool(label='Joint Orient Constraint')
def constrain_jointOrientContraint():
    """Similar to an orient constraint, but effecting the joint orients instead of the rotation
    """
    return ka_util.jointOrientContraint()

@Tool(label='Distance Between, to Translate X')
def constrain_distanceBetween():
    """connects the translate x of the last selected object, to equal the distance
    between the first 2 selected objects
    """
    return ka_util.distanceBetweenToTranslateX()

@Tool(label='Direct Connect Translates')
def directConnect_translates():
    """connects the translates of the first selected object, every other objects translate
    """
    selection = pymel.ls(selection=True)
    for i, node in enumerate(selection):
        if i != 0:
            selection[0].tx >> node.tx
            selection[0].ty >> node.ty
            selection[0].tz >> node.tz

@Tool(label='Direct Connect Rotates')
def directConnect_rotates():
    """connects the rotates of the first selected object, every other objects rotates
    """
    selection = pymel.ls(selection=True)
    for i, node in enumerate(selection):
        if i != 0:
            selection[0].rx >> node.rx
            selection[0].ry >> node.ry
            selection[0].rz >> node.rz

@Tool(label='Direct Connect Scales')
def directConnect_scales():
    """connects the scales of the first selected object, every other objects scales
    """
    selection = pymel.ls(selection=True)
    for i, node in enumerate(selection):
        if i != 0:
            selection[0].sx >> node.sx
            selection[0].sy >> node.sy
            selection[0].sz >> node.sz


# SNAP COMMANDS -------------------------------------------------------------------
@Tool(label='Snap Translate')
def snap_translate():
    """moves the all but the last selected object to the last selected object's world
    space position
    """
    return ka_transforms.snap(t=1)


@Tool(label='Snap Rotate')
def snap_rotate():
    """rotates the all but the last selected object to be the have the same world space
    rotation as the last selected object
    """
    return ka_transforms.snap(r=1)


@Tool(label='Snap Scale')
def snap_scale():
    """scales the all but the last selected object to the last selected object's world
    space scale
    """
    return ka_transforms.snap(s=1)

@Setting('primaryAxis', valueType='enum', enumValues=['  x', ' -x', '  y', ' -y', '  z', ' -z'])
@Setting('secondaryAxis', valueType='enum', enumValues=['  x', ' -x', '  y', ' -y', '  z', ' -z'])
@Tool(label='Snap Aim')
def snap_aim(primaryAxis=0, secondaryAxis=2):
    """rotates the all but the last selected object to aim their "pimary axis" at the world space
    position of the last selected object. The "secondary axis" will roll to point as near as possible
    to the direction it was initially pointing in world space.
    """
    return ka_transforms.snap(a=1)


@Tool(label='Snap Mirror')
def snap_mirror():
    """moves the all but the last selected object to the last selected objects world
    space position
    """
    return ka_transforms.snap(m=1)

# PRINT COMMANDS
@Tool(label='Print SELECTION as Python List')
def print_selection():
    """Print's current Selection as a formated python list:
    ie: ['pSphere1', 'pSphere2', 'pSphere1',]
    """
    return ka_util.printSelection_asPythonList()

@Tool(label='Print CURVE Create Command')
def print_curve():
    """Print's code that will recreate the selected nurbsCurve
    """
    return ka_util.printSelectedCurveCreationCommand()

@Tool(label='Print MESH Create Command')
def print_mesh():
    """Print's code that will recreate the selected mesh
    """
    return ka_util.printMeshCreateCmd()

# MISC COMMANDS -------------------------------------------------------------------
@Tool(label='Delete All Bind Pose Nodes')
def deleteAllBindPoseNodes():
    """Deletes all Bind Pose Nodes in the scene, as they are
    usually not used in modern rigging"""
    return ka_util.deleteAllBindPoseNodes()


@Tool(label='Find Lattice Cage From Lattice Deformer')
def findLatticeCageFromLatticeDeformer():
    """Finds the Lattice Cage that is deforming the given lattice
    deformer
    """
    return mel.eval("findLatticeDeformersLatticeCage;")


@Tool(label='Delete All Time based Keyframes')
def deleteAllKeyframes():
    """Deletes all Keyframes with time as the input. This will not
    delete set driven keys
    """
    return ka_util.deleteAllKeyframes()


@Tool(label='Set Joint Label From Name')
def setJointLabel():
    """will set the joint label of the joint based on the name. This
    will make the side attribute of the joint center right or left, and
    the label attribute of the joint the same as the name without the side
    indication (ie: if the name was "R_arm", the label would be "arm"). This
    allows mirroring and weight copy to be done more reliably, using joint labels.
    """
    return ka_skinCluster.setSetJointLabelFromName()


@Tool(label='Set Joint Label On ALL Influences')
def setJointLabel_allInfluences():
    """same as Set Joint Label from Name, but for all the Influences
    on the selected skinned mesh.
    """
    return ka_skinCluster.setSetJointLabelFromNameOnAll()


@Tool(label='Reorder all Shapes to Top of Hierchy')
def reorderAllShapesToTopOfTheirHierchy():
    """Reorders the Hierchy so that the first child of any transform
    (with a shape) is it's shape
    """
    return ka_util.reorderAllShapesToTopOfTheirHierchy()


@Tool(label='Make Surface Constraint Use Tanget V as upVector (default)')
def makeSurfaceConstraint_useTangetV():
    """Make Surface Constraint Use Tanget V as upVector (default)
    """
    return ka_util.makeSurfaceConstraint_useTangetV()


@Tool(label='Make Surface Constraint Use Tanget U as upVector')
def makeSurfaceConstraint_useTangetU():
    """Make Surface Constraint Use Tanget U as upVector
    """
    return ka_util.makeSurfaceConstraint_useTangetU()


# TOOL UIs -------------------------------------------------------------------
@Tool(label='Open Rename Tool')
def renameTool():
    """A UI for renaming nodes
    """
    return ka_rename.openUI()


@Tool(label='Filter Selection Tool')
def filterTool():
    """A UI for filtering selection based on selection type
    """
    return ka_filterSelection.openUI()


@Tool(label='Attribute Tool')
def attrTool():
    """A UI for manipulating attribute values and connections
    """
    return ka_attrTool_UI.openUI()


# HYPERSHADE COMMANDS -------------------------------------------------------------------
@Tool(label='Align Nodes Vertical', icon='alignVertical.png')
def hyperShade_alignNodesVertical():
    """Move (in hypershade) all selected nodes into a vertical column
    """
    return ka_hyperShade.alignNodes('vertical')


@Tool(label='Align Nodes Horizontal', icon='alignHorizontal.png')
def hyperShade_alignNodesHorizontal():
    """Move (in hypershade) all selected nodes into a horizontal row
    """
    return ka_hyperShade.alignNodes('horizontal')


@Tool(label='Clear Graph', icon='clear.png')
def hyperShade_clear():
    """Clears the hyphershade
    """
    return ka_hyperShade.clear()


@Tool(label='isolate In Graph',)
def hyperShade_isolateSelection():
    """Clears hypershade and addes back in the selected nodes
    """
    return ka_hyperShade.isolateInGraph()


@Tool(label='Add Selected to Graph', icon='add.png')
def hyperShade_add():
    """Add selected node to the hyphershade
    """
    return ka_hyperShade.add()


@Tool(label='Duplicate (with connections)', icon='duplicate.png')
def hyperShade_duplicate():
    """Duplicates the selected nodes, the heirchy relationships,
    and the connections between them
    """
    return attrCommands.duplicateSelection()


@Tool(label='Echo re-Create Commands')
def hyperShade_echoRecreateCommands():
    """Prints commands that will recreate the selected nodes,
    the hierchy, and connections between them
    """
    return attrCommands.eccoAttrsPymelObjectOriented()


@Setting('depthLimit', valueType='int')
@Tool(label='Graph Inputs', icon='graphIn.png')
def hyperShade_graphInputs(depthLimit=2):
    """graphs input nodes of the selected nodes in the hypershade.
    This command graphs without containers
    """
    return ka_hyperShade.graphInputOutput(mode='inputs', depthLimit=depthLimit)

@Setting('depthLimit', valueType='int')
@Tool(label='Graph Outputs', icon='graphOut.png')
def hyperShade_graphOutputs(depthLimit=2):
    """graphs output nodes of the selected nodes in the hypershade.
    This command graphs without containers
    """
    return ka_hyperShade.graphInputOutput(mode='outputs', depthLimit=depthLimit)

@Setting('depthLimit', valueType='int')
@Tool(label='Graph Inputs and Outputs', icon='graphInOut.png')
def hyperShade_graphInputsAndOutputs(depthLimit=2):
    """graphs input and output nodes of the selected nodes in the hypershade.
    This command graphs without containers
    """
    return ka_hyperShade.graphInputOutput(mode='all', depthLimit=depthLimit)


@Tool(label='Select Inputs', icon='Selection.png')
def hyperShade_selectInputs():
    """selects input nodes of the selected nodes in the hypershade.
    """
    return ka_hyperShade.selectInputOutput(mode='inputs')

@Tool(label='Select Outputs', icon='Selection.png')
def hyperShade_selectOutputs():
    """selects output nodes of the selected nodes in the hypershade.
    """
    return ka_hyperShade.selectInputOutput(mode='outputs')

@Tool(label='Select Inputs and Outputs', icon='Selection.png')
def hyperShade_selectInputsAndOutputs():
    """selects input and output nodes of the selected nodes in the hypershade.
    """
    return ka_hyperShade.selectInputOutput()


@Tool(label='Add Keys To AnimCurve Node', icon='key.png')
def hyperShade_addKeysToAnimCurveNode():
    """Adds two keys to the selected animCurve node.
    """
    return ka_hyperShade.addKeysToAnimCurveNode()


@Tool(label='Convert Anim Curve to Type animCurveUA', icon='transfer.png')
def hyperShade_addKeysToAnimCurveNodeUA(targetType='animCurveUA'):
    """Convert animCurve to another Type
    """
    return ka_util.convertSelectedAnimCurveTo(targetType=targetType)

@Tool(label='Convert Anim Curve to Type animCurveUU', icon='transfer.png')
def hyperShade_addKeysToAnimCurveNodeUU(targetType='animCurveUI'):
    """Convert animCurve to another Type
    """
    return ka_util.convertSelectedAnimCurveTo(targetType=targetType)

@Tool(label='Convert Anim Curve to Type animCurveUL', icon='transfer.png')
def hyperShade_addKeysToAnimCurveNodeUL(targetType='animCurveUL'):
    """Convert animCurve to another Type
    """
    return ka_util.convertSelectedAnimCurveTo(targetType=targetType)

@Tool(label='Convert Anim Curve to Type animCurveUT', icon='transfer.png')
def hyperShade_addKeysToAnimCurveNodeUT(targetType='animCurveUT'):
    """Convert animCurve to another Type
    """
    return ka_util.convertSelectedAnimCurveTo(targetType=targetType)


@Tool(label='Apply SkinCluster', context=ka_context.createSkinClusterContext)
def skinCluster():
    """applies a new skinCluster from selection with proper
    defaults
    """
    return ka_weightPainting.createSkinCluster()


@Tool(label='Add Influence', context=ka_context.addInfluenceContext, icon='add.png')
def addInfluence():
    return ka_weightPainting.addInfluence()


@Tool(label='Add Influence')
def addInfluenceToSkinCluster():
    """adds the selected influence to the skinCluster with proper
    defaults
    """
    selection = pymel.ls(selection=True)
    skinCluster = ka_skinCluster.findRelatedSkinCluster(selection[0])
    return pymel.skinCluster(skinCluster, edit=True, addInfluence=selection[0:-1])

@Tool(label='Find Related Skin Cluster')
def findRelatedSkinCluster(selection=None):
    """returns the related skin cluster
    """
    if selection == None:
        selection = pymel.ls(selection=True)
    else:
        selection = pymel.ls(selection)

    return ka_skinCluster.findRelatedSkinCluster(selection[0])


# SET CURRENT INFLUENCE ------------------------------------------------------
def paintInfluenceUnderMouse_label():
    """Returns string for a UI item that will read:

    'Paint: joint1'
    <or>
    'joint1 IS NOT an Influence in the skinCluster!'

    depending on whether the joint is part of the skinCluster
    """
    context = ka_context.getCurrentContext()

    selection = context.getSelection()
    nodeUnderMouse = context.getTransformUnderMouse()

    #if selection:
    skinCluster = ka_skinCluster.findRelatedSkinCluster(selection[-1])
    if skinCluster:
        influences = ka_skinCluster.getInfluences(skinCluster)
        nodeName = nodeUnderMouse.nodeName()
        if len(nodeName) > 25:
            nodeName = nodeName[:22]+'...'

        if nodeUnderMouse in influences:
            return 'Paint: %s' % nodeName

        else:
            return '%s IS NOT an Influence in the skinCluster!' % nodeName

    return ''

@Tool(label=paintInfluenceUnderMouse_label, context=ka_context.paintableInfluenceUnderMouse_context, icon='paint.png')
def paintInfluenceUnderMouse():
    context = ka_context.getCurrentContext()
    nodeUnderMouse = context.getTransformUnderMouse()
    return ka_weightPainting.paint(nodeUnderMouse)


def pasteWeightsFromInfluence_label():
    """Returns string for a UI item that will read:

    'Paint: joint1'
    <or>
    'joint1 IS NOT an Influence in the skinCluster!'

    depending on whether the joint is part of the skinCluster
    """
    context = ka_context.getCurrentContext()

    selection = context.getSelection()
    nodeUnderMouse = context.getTransformUnderMouse()

    #if selection:
    skinCluster = ka_skinCluster.findRelatedSkinCluster(selection[-1])
    if skinCluster:
        influences = ka_skinCluster.getInfluences(skinCluster)
        if nodeUnderMouse in influences:
            return 'Copy AND Paste weights form: %s' % nodeUnderMouse.nodeName()

        else:
            return '%s IS NOT an Influence in the skinCluster!' % nodeUnderMouse.nodeName()

    return ''


@Tool(label=pasteWeightsFromInfluence_label, context=ka_context.paintableInfluenceUnderMouse_context, icon='paint.png')
def pasteWeightsFromInfluence():
    context = ka_context.getCurrentContext()

    if context.selectionIncludesComponents():
        ka_weightPainting.copySkinWeights(copySpecificInfluence=context.getTransformUnderMouse())
        ka_weightPainting.pasteSkinWeights()


@Tool(label='Paint Influence and Hold All Others', context=ka_context.paintableInfluenceUnderMouse_context, icon='paint.png')
def paintInfluenceUnderMouse_andHoldAllOthers():
    context = ka_context.getCurrentContext()
    nodeUnderMouse = context.getTransformUnderMouse()
    return ka_weightPainting.paintAndHoldAllOthers(nodeUnderMouse)


@Tool(label='Copy Weights', context=ka_context.paintableInfluenceUnderMouse_context, icon='paint.png')
def copyVertWeights():
    return ka_weightPainting.copySkinWeights()


@Tool(label='Paste Weights', context=ka_context.paintableInfluenceUnderMouse_context, icon='paint.png')
def pasteVertWeights():
    return ka_weightPainting.pasteSkinWeights()


@Tool(label='>> 20 frames',)
def advance20Frames():
    return ka_animation.advanceNFrames(numberOfFrames=20)

@Tool(label='>> 10 frames',)
def advance10Frames():
    return ka_animation.advanceNFrames(numberOfFrames=10)

@Tool(label='Key All Controls')
def keyAllControls():
    return ka_animation.keyAllControls()


@Tool(label='Apply A Pose')
def applyTPose():
    return ka_animation.applyTPose()

@Tool(label='Apply T Pose')
def applyTPose():
    return ka_animation.applyTPose()


@Tool(label='Store A Pose')
def applyTPose():
    return ka_animation.storeTPose()

@Tool(label='Store T Pose')
def storeTPose():
    return ka_animation.storeTPose()


@Tool(label='Store Selection As Controls')
def storeSelectionAsAllControls():
    return ka_animation.storeAllControls()


@Tool(label='Select All Controls')
def selectAllControls():
    return ka_animation.selectAllControls()


@Tool(label='Select All Influences of skinCluster')
def selectAllSkinClusterInfluences():
    """selects all influences that are part of the skin cluster on
    the selected object"""
    influences = ka_skinCluster.getInfluences()
    return pymel.select(influences)


@Tool(label='Convert Selected Anim Curve to animCurveUU')
def convertAnimCurveTo_UU():
    """Converts the selected animation curve to type animCurveUU"""
    ka_util.convertSelectedAnimCurveTo(targetType='animCurveUU')

@Tool(label='Convert Selected Anim Curve to animCurveUA')
def convertAnimCurveTo_UA():
    """Converts the selected animation curve to type animCurveUA"""
    ka_util.convertSelectedAnimCurveTo(targetType='animCurveUA')

@Tool(label='Convert Selected Anim Curve to animCurveUL')
def convertAnimCurveTo_UL():
    """Converts the selected animation curve to type animCurveUL"""
    ka_util.convertSelectedAnimCurveTo(targetType='animCurveUL')

@Tool(label='Convert Selected Anim Curve to animCurveUT')
def convertAnimCurveTo_UT():
    """Converts the selected animation curve to type animCurveUT"""
    ka_util.convertSelectedAnimCurveTo(targetType='animCurveUT')


@Tool(label='Create volumeRotator')
def createVolumeRotator():
    """Creates a volume rotator"""
    ka_advancedJoints_volumeRotator.create()

@Tool(label='Print All VolumeRotators')
def printAllVolumeRotators():
    """Creates a volume rotator"""
    ka_advancedJoints_volumeRotator.printAllVolumeRotators()



# IRS ------------------------------------------------------
@Tool(label='Create Human')
def createHuman():
    """make a fellow"""
    import ka_rigTools.ka_irs.core as ka_irs #;reload(ka_irs)
    ka_irs.createHuman()


@Tool(label='add rig aerobics')
def rigAerobics_add():
    return ka_rigAerobics.rnkBipiedAnimation()




# TEST ------------------------------------------------------
@Tool(label='Test Command A')
def testCommandA():
    return ka_math.testA()

@Tool(label='Test Command B')
def testCommandB():
    selection = pymel.ls(selection=True)
    positions = []
    for node in selection[:4]:
        positions.append(node.t.get())

    print(ka_math.getBarycentricCoordinates(positions, selection[-1].t.get()))


@Tool(label='Test Command C')
def testCommandC():
    return ka_psd.makeTetraSphere()

