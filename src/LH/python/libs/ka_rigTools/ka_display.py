 #====================================================================================
#====================================================================================
#
# ka_display
#
# DESCRIPTION:
#   Functions to manipulate maya display attributes
#
# DEPENDENCEYS:
#   -Maya
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

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_pymel as ka_pymel    #;reload(ka_python)
import ka_rigTools.ka_python as ka_python    #;reload(ka_python)
import ka_rigTools.ka_skinCluster as ka_skinCluster    #;reload(ka_skinCluster)
import ka_rigTools.ka_context as ka_context    #;reload(ka_context)

def hideAllRotationAxis():
    transforms = cmds.ls(type='transform')
    transforms = transforms + cmds.ls(type='joint')
    for each in transforms:
        try:
            cmds.setAttr(each+'.displayLocalAxis', 0)
        except:
            printError()


def setIsolateSet():
    context = ka_context.newContext()
    currentPanel = context.getPanelWithFocus()

    isolateSet = pymel.isolateSelect(currentPanel, query=True, viewObjects=True)
    isolatedObjects = pymel.sets(isolateSet, query=True)
    if pymel.objExists('isolateSelectionSet'):
        pymel.delete('isolateSelectionSet')
    pymel.sets( isolatedObjects, n="isolateSelectionSet")

def skinningDisplaySet_print(skinningDisplaySet):
    setObjects = pymel.sets(skinningDisplaySet, query=True)
    setObjects = ka_pymel.getAsStrings(setObjects)
    startFrame = skinningDisplaySet.startFrame.get()
    endFrame = skinningDisplaySet.endFrame.get()
    name = skinningDisplaySet.nodeName()

    print('ka_rigTools.skinningDisplaySet_create(%s, startFrame=%s, endFrame=%s, name="%s")' % (str(setObjects), str(startFrame), str(endFrame), name))


def skinningDisplaySet_printSelected():
    print('import ka_rigTools.core as ka_rigTools')
    for skinningDisplaySet in skinningDisplaySet_getSelected():
        skinningDisplaySet_print(skinningDisplaySet)

def skinningDisplaySet_printAll():
    print('import ka_rigTools.core as ka_rigTools')
    for skinningDisplaySet in skinningDisplaySet_getAll():
        skinningDisplaySet_print(skinningDisplaySet)


def skinningDisplaySet_create(setObjects, startFrame=1, endFrame=33, name='displaySet1'):
    skinningSet = pymel.sets( setObjects, n=name)

    skinningSet.addAttr('ka_type', dt='string')
    skinningSet.ka_type.set('skinningSet')

    skinningSet.addAttr('startFrame', at='long')
    skinningSet.addAttr('endFrame', at='long')
    skinningSet.startFrame.set(startFrame)
    skinningSet.endFrame.set(endFrame)

    return skinningSet

def skinningDisplaySet_createFromScene():
    context = ka_context.newContext()
    currentPanel = context.getPanelWithFocus()

    isolateSet = pymel.isolateSelect(currentPanel, query=True, viewObjects=True)
    isolatedObjects = pymel.sets(isolateSet, query=True)

    name = ka_python.getInput('setName:')
    startFrame = pymel.playbackOptions(query=True, min=True)
    endFrame = pymel.playbackOptions(query=True, max=True)

    skinningSet = skinningDisplaySet_create(isolatedObjects, startFrame=startFrame, endFrame=endFrame, name=name)
    #skinningSet = pymel.sets( isolatedObjects, n=name)
    #skinningSet.addAttr('ka_type', dt='string')
    #skinningSet.ka_type.set('skinningSet')

    #skinningSet.addAttr('startFrame', at='long')
    #skinningSet.addAttr('endFrame', at='long')
    #skinningSet.startFrame.set(pymel.playbackOptions(query=True, min=True))
    #skinningSet.endFrame.set(pymel.playbackOptions(query=True, max=True))

def setSkinningDisplaySet(skinningSet):
    context = ka_context.newContext()
    currentPanel = context.getPanelWithFocus()
    isolateState = pymel.isolateSelect(currentPanel, query=True, state=True)
    selection = pymel.ls(selection=True)


    skinningSet = pymel.ls(skinningSet)[0]

    pymel.isolateSelect(currentPanel, query=True, viewObjects=True)

    if isolateState:
        cmds.isolateSelect(currentPanel, state=0,)

    cmds.isolateSelect(currentPanel, state=1,)

    pymel.select(skinningSet)
    cmds.isolateSelect(currentPanel, addSelected=True,)

    cmds.playbackOptions(min=skinningSet.startFrame.get(), max=skinningSet.endFrame.get())
    pymel.select(selection)

def skinningDisplaySet_getAll():
    skinningSets = []
    for eachSet in pymel.ls(type='objectSet'):
        if hasattr(eachSet, 'ka_type'):
            if eachSet.ka_type.get() == 'skinningSet':
                skinningSets.append(eachSet)

    return skinningSets

def skinningDisplaySet_getSelected():
    skinningSets = []
    for eachSet in pymel.ls(selected=True, type='objectSet'):
        if hasattr(eachSet, 'ka_type'):
            if eachSet.ka_type.get() == 'skinningSet':
                skinningSets.append(eachSet)

    return skinningSets

def clearIsolateSet():
    if pymel.objExists('isolateSelectionSet'):
        pymel.delete('isolateSelectionSet')
    pymel.sets( isolatedObjects, n="isolateSelectionSet")


def addToIsolateSelect():
    context = ka_context.newContext()
    currentPanel = context.getPanelWithFocus()

    if pymel.isolateSelect(currentPanel, query=True, state=True):
        selection = pymel.ls(selection=True)
        cmds.isolateSelect(currentPanel, addSelected=True,)

        if pymel.objExists('isolateSelectionSet'):
            pymel.sets('isolateSelectionSet', addElement=selection)




def removeFromIsolateSelect():
    context = ka_context.newContext()
    currentPanel = context.getPanelWithFocus()

    if pymel.isolateSelect(currentPanel, query=True, state=True):
        selection = pymel.ls(selection=True)
        cmds.isolateSelect(currentPanel, removeSelected=True,)

        if pymel.objExists('isolateSelectionSet'):
            pymel.sets('isolateSelectionSet', remove=selection)


def isolateSelection(mode='default'):

    panelUnderPointer = pymel.getPanel( underPointer=True )
    if panelUnderPointer:
        if 'modelPanel' in panelUnderPointer:
            currentPanel = pymel.getPanel(withFocus=True)
            isolateState = pymel.isolateSelect(currentPanel, query=True, state=True)

            if pymel.objExists('isolateSelectionSet'):
                pymel.isolateSelect(currentPanel, state=(1 - isolateState),)
                for node in pymel.sets('isolateSelectionSet', query=True):
                    pymel.isolateSelect(currentPanel, addDagObject=node,)

            else:
                selection = pymel.ls(selection=True)
                if mode == 'default':
                    cmds.isolateSelect(currentPanel, state=(1 - isolateState),)
                    cmds.isolateSelect(currentPanel, addSelected=True,)
                    mel.eval('isoSelectAutoAddNewObjs %s 1;'%(currentPanel))

                if mode == 'skinning':
                    skinClusters = []
                    influences = []
                    for each in selection:
                        skinCluster = ka_skinCluster.findRelatedSkinCluster(each)
                        if skinCluster:
                            skinClusters.append(skinCluster)

                    for skinCluster in skinClusters:
                        for influence in ka_skinCluster.getInfluences(skinCluster):
                            if influence not in influences:
                                influences.append(influence)

                    cmds.isolateSelect(currentPanel, state=(1 - isolateState),)
                    cmds.isolateSelect(currentPanel, addSelected=True,)
                    for influence in influences:
                        pymel.isolateSelect(currentPanel, addDagObject=influence,)



def updateIsolateSelection():
    panelUnderPointer = pymel.getPanel( underPointer=True )
    if panelUnderPointer:
        if 'modelPanel' in panelUnderPointer:
            currentPanel = pymel.getPanel(withFocus=True)
            #currentPanel = 'modelPanel4'
            isolateState = pymel.isolateSelect(currentPanel, query=True, state=True)
            selection = pymel.ls(selection=True)
            #
            if isolateState:
                isolatedObjectSet = pymel.isolateSelect(currentPanel, query=True, viewObjects=True,)
                isolatedObjects = pymel.sets(isolatedObjectSet, query=True)
                pymel.isolateSelect(currentPanel, state=False,)

                mel.eval('changeSelectMode -object;')
                mel.eval('buildSelectObjectMM;')
                mel.eval('MarkingMenuPopDown;')
                mel.eval('artSelectToolScript 4')
                #mel.eval('artSelectToolScript 3')

                pymel.isolateSelect(currentPanel, state=True,)
                for item in isolatedObjects:
                    if not '.' in str(item):
                        pymel.isolateSelect(currentPanel, addDagObject=item,)

            pymel.select(selection)

def updateIsolateSelection():
    context = ka_context.newContext()

    panelUnderPointer = pymel.getPanel( underPointer=True )
    if panelUnderPointer:
        if context.getUiTypeUnderMouse() == 'model':
        #if 'modelPanel' in panelUnderPointer:
            currentPanel = context.getPanelUnderMouse()
            #currentPanel = pymel.getPanel(withFocus=True)
            #currentPanel = 'modelPanel4'
            isolateState = pymel.isolateSelect(currentPanel, query=True, state=True)
            selection = pymel.ls(selection=True)
            #
            if isolateState:
                isolatedObjectSet = pymel.isolateSelect(currentPanel, query=True, viewObjects=True,)
                isolatedObjects = pymel.sets(isolatedObjectSet, query=True)
                pymel.isolateSelect(currentPanel, state=False,)

                if context.getCurrentTool() == 'artSelectContext':
                    mel.eval('changeSelectMode -object;')
                    mel.eval('buildSelectObjectMM;')
                    mel.eval('MarkingMenuPopDown;')
                    mel.eval('artSelectToolScript 4')

                elif context.getCurrentTool() == 'artSelectContext':
                    mel.eval('changeSelectMode -object;')
                    mel.eval('buildSelectObjectMM;')
                    mel.eval('MarkingMenuPopDown;')
                    mel.eval('artAttrSkinToolScript 4')


                #mel.eval('artSelectToolScript 3')


                pymel.isolateSelect(currentPanel, state=True,)
                for item in isolatedObjects:
                    #if not '.' in str(item):
                    pymel.isolateSelect(currentPanel, addDagObject=item,)

            pymel.select(selection)

def toggleColorWireframeOnSelected():
    mel.eval("displayAffected (!`displayAffected -query`);")

def ka_disableDrawingOverideOnSelection(enable=False):
    for node in pymel.ls(selection=True):
        try:
            node.drawOverride.overrideEnabled.set(enable)
        except:
            pass


def jointXRayMode(state='toggle'):
    context = ka_context.newContext()
    currentModelEditor = context.getPanelWithFocus()

    if state == 'toggle':
        value = pymel.modelEditor(currentModelEditor, query=True, jointXray=True, )
        if value:
           state = False

        else:
            state = True

    pymel.modelEditor(currentModelEditor, edit=True, jointXray=state, )

def xRayMode(state='toggle'):
    context = ka_context.newContext()
    currentModelEditor = context.getPanelWithFocus()

    if state == 'toggle':
        value = pymel.modelEditor(currentModelEditor, query=True, xray=True, )
        if value:
           state = False
        else:
            state = True

    pymel.modelEditor(currentModelEditor, edit=True, xray=state, )




#global proc  ka_xRay()
#{//turn X-ray on for the current pannel
    #string $currentPanel = `getPanel -withFocus`;

    #modelEditor -e -xray 1 $currentPanel;
    #string $version = `about -version`;
    #if(`match "20" $version` == "20")
    #{
        #modelEditor -e -jointXray (!`modelEditor -q -jointXray $currentPanel`) $currentPanel;
    #}
    #if(`match "8.5" $version` == "8.5")
    #{
        #if(`currentCtx` == "artAttrSkinContext")
        #{
            #modelEditor -edit -displayAppearance "wireframe" -displayTextures off -displayLights "default" $currentPanel;
        #}
    #}
#}

