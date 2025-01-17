#====================================================================================
#====================================================================================
#
# ka_utils_skinCluster
#
# DESCRIPTION:
#   library of commands for querying skinClusters
#
# DEPENDENCEYS:
#   ka_menus
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


import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pymel
import maya.OpenMaya as OpenMaya

from . import ka_rigQuery #;reload(ka_rigQuery)



def findRelatedSkinCluster(*args, **kwArgs):
    '''return the skinCluster for the input, which will be a user selection

    kwArgs:
        silent - True/False if True, then no error will occure if no skinCluster is found
    '''

    silent = kwArgs.get('silent', True)

    log = 0 #log debug messages or not

    if args:
        node = args[0]
    else:
        if 'input' in kwArgs:
            node = kwArgs['input']
        else: #then use selection
            node = pymel.ls(selection=True)[0]

    node = node.node()
    #components = input.split('.')
    transform = None
    skinCluster = None

    if log:print("input", input)


    #if len(components) > 1:
        #input = components[0]

    if 'transform' in node.nodeType(inherited=True):
        transform = node

    #elif pymel.objectType(input) == 'joint':
        #transform = input

    if pymel.objectType(node) == 'skinCluster':
        return node

    elif 'deformableShape' in pymel.nodeType(node, inherited=True):
        transform = pymel.listRelatives(node, parent=True)


    if not skinCluster and transform:
        shapes = pymel.listRelatives(transform, shapes=True)
        if shapes:
            if 'deformableShape' in pymel.nodeType(shapes[0], inherited=True):
                history = pymel.listHistory(transform)

                if history:
                    for each in history:
                        if pymel.nodeType(each) == 'skinCluster':
                            shapes = pymel.listRelatives(transform, noIntermediate=True, shapes=True)
                            if shapes:
                                geos = pymel.skinCluster(each, query=True, geometry=True)
                                for geo in geos:
                                    if geo in shapes:
                                        skinCluster = each
                                        break
                                        break

                if not skinCluster:
                    if history:
                        for each in history:
                            if pymel.nodeType(each) == 'skinCluster':
                                skinCluster = each
                                break


    #if not skinCluster:
        #if not silent:
            ##raise NameError('-- A skinCluster could not be found for: '+input)
            #print '-- A skinCluster could not be found for: ', input

    return skinCluster



def getInfluences(skinCluster=''):
    '''return the influences attached to the skinCluster'''
    influences = []

    if skinCluster == '': #then use selection
        selection = pymel.ls(selection=True)
        if selection:
            skinCluster = findRelatedSkinCluster(selection[0])

    elif not pymel.nodeType(skinCluster) == 'skinCluster':
        skinCluster = findRelatedSkinCluster(skinCluster)

    if skinCluster:
        influences = pymel.listConnections(skinCluster+'.matrix', destination=False, source=True, skipConversionNodes=True)

    return influences


def removeUnusedForSkin(skinCluster, **kwArgs):
    verbose = kwArgs.get('verbose', False)

    influences = getInfluences(skinCluster)
    weightedInfluences = pymel.skinCluster(skinCluster, query=True, weightedInfluence=True)
    unweightedInfluences = []
    nodeState = skinCluster.nodeState.get()

    skinCluster.nodeState.set(1)
    for influence in influences:
        if influence not in weightedInfluences:
            #unweightedInfluences.append(influence)

            pymel.skinCluster(skinCluster, edit=True, removeInfluence=influence)

    if verbose:
        print('removed %s influences from skinCluster: %s' % (str(len(unweightedInfluences)), skinCluster.name()))

def removeUnusedInfluences(**kwArgs):
    kwArgs['verbose'] = True
    selection = pymel.ls(selection=True)

    for geo in selection:
        skinCluster = findRelatedSkinCluster(geo, silent=True)
        if skinCluster:
            removeUnusedForSkin(skinCluster, **kwArgs)


def setSetJointLabelFromName():
    selection = pymel.ls(selection=True)

    for sel in selection:
        _setSetJointLabelFromName(sel)

def setSetJointLabelFromNameOnAll():
    skinClusters = pymel.ls(type='skinCluster')
    jointInfluences = {}
    for skinCluster in skinClusters:
        influences = getInfluences(skinCluster)
        for influence in influences:
            if influence not in jointInfluences:
                jointInfluences[influence] = None

    for jointInfluence in jointInfluences:
        _setSetJointLabelFromName(jointInfluence)

def _setSetJointLabelFromName(node):

    if pymel.nodeType(node) == 'joint':
        #baseName = None
        #side = 0
        #left = 1
        #right = 2
        #currentName = node.nodeName(stripNamespace=True)

        #if currentName[0:2] == 'r_':
            #side = right
            #baseName = currentName[2:]
        #elif currentName[0:2] == 'l_':
            #side = left
            #baseName = currentName[2:]
        #elif currentName[0:2] == 'R_':
            #side = right
            #baseName = currentName[2:]
        #elif currentName[0:2] == 'L_':
            #side = left
            #baseName = currentName[2:]

        #elif '_r_' in currentName:
            #side = right
            #baseName = currentName.replace('_r_', '', 1)

        #elif '_l_' in currentName:
            #side = left
            #baseName = currentName.replace('_l_', '', 1)

        #elif '_R_' in currentName:
            #side = right
            #baseName = currentName.replace('_R_', '', 1)

        #elif '_L_' in currentName:
            #side = left
            #baseName = currentName.replace('_L_', '', 1)

        #else:
            #baseName = currentName

        #node.attr('type').set(18)
        #node.side.set(side)
        #node.otherType.set(baseName, type='string')
        sideInfo = ka_rigQuery._getSideInfo(node.nodeName())

        if not sideInfo:
            node.side.set(0)
            node.attr('type').set(18)
            node.otherType.set(node.nodeName(), type='string')

        else:
            if sideInfo['side'] == 'l':
                node.side.set(1)
            elif sideInfo['side'] == 'r':
                node.side.set(2)
            else:
                node.side.set(0)

                nameWithoutSide = node.nodeName().replace(sideInfo['sideString'], '', 1)

                node.attr('type').set(18)
                node.otherType.set(nameWithoutSide, type='string')


