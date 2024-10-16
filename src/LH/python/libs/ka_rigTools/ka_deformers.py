#====================================================================================
#====================================================================================
#
# ka_deformers
#
# DESCRIPTION:
#   tools related to deformers
#
# DEPENDENCEYS:
#   Maya
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


from . import ka_skinCluster as ka_skinCluster #;reload(ka_skinCluster)

def renameAllDeformers():
    """renames all deformers to be <shapeName>_<deformerNodeType>
    this allows file names to be more likely to be uniquely named and
    guessable"""

    allDeformers = getAllDeformers()
    for deformer in allDeformers:
        componentsDeformed = getComponentsOfDeformersSet(deformer)
        deformedObjects = getDeformedObjects(componentsDeformed)
        if len(deformedObjects) == 1:
            if not deformer.isReferenced():
                newName = deformedObjects[0] +'_'+ pymel.nodeType(deformer)
                deformer.rename(newName)

def getDeformers(shapes):
    """returns all deformers of the given shape or shapes

    args:

        shapes: shape-pymelNode or list of shape-pymelNodes
            the shape or shapes to get deformers from
    """

    deformers = []

    if not isinstance(shapes, list):
        shapes = [shapes]

    for shape in shapes:
        history = pymel.listHistory(shape)
        for each in history:
            if 'geometryFilter' in pymel.nodeType(each, inherited=True):
                if not each in deformers:
                    deformers.append(each)

    return deformers

def getAllDeformers():
    """returns all deformers in Scene"""
    return pymel.ls(type='geometryFilter')


def getDeformedObjects(deformedComponentSlices):
    '''returns all shapes deformed by the given deformer
    '''

def getDeformerSet(deformerNode):
    possibleDeformerSets = deformerNode.message.outputs()
    for each in possibleDeformerSets:
        if pymel.nodeType(each) == 'objectSet':
            if pymel.isConnected(deformerNode.message, each.usedBy[0]):
                return each


def getComponentsOfDeformersSet(deformerNode, flatten=False):

    deformerSet = getDeformerSet(deformerNode)
    components = pymel.sets(deformerSet, q=True,)

    if flatten:
        components = pymel.ls(components, flatten=True)

    return components


def getRange_fromString(componentString,):

    start = componentString.index('[')+1
    end = componentString.index(']')
    colon = componentString.index(':')

    start = int(componentString[start:mid])
    end = int(componentString[mid+1:end+1])

    return (start, end)


def setComponentsOfDeformersSet(deformerNode, componentSet):
    deformerSet = getDeformerSet(deformerNode)
    pymel.sets(deformerSet, clear=True,)
    pymel.sets(deformerSet, addElement=componentSet,)



def getWeightSlices(weightList):
    '''this function will take (a potentially long) list of weight values, and break it into slices
    representing the non zero values. This step will have a dramatic speed increase when it comes
    to importing them

    returns - a dictionary where the slice is the key
              ie: {'32:33' : (0.7, 0.3),}
    '''

    weightSlicesDict = {}
    sliceStart = None
    sliceEnd = None
    sliceValues = []
    lastIndex = len(weightList)-1

    for i, weightValue in enumerate(weightList):

        if weightValue:
            sliceValues.append(weightValue)

            if sliceStart == None:
                sliceStart = i
                sliceEnd = i

            else:
                sliceEnd += 1

            if i == lastIndex:
                if sliceStart == sliceEnd:
                    key = str(sliceStart)

                else:
                    key = '%s:%s' % (str(sliceStart), str(sliceEnd))

                weightSlicesDict[key] = tuple(sliceValues)
                sliceStart = None
                sliceEnd = None
                sliceValues = []

        else:
            if sliceStart != None:
                if sliceStart == sliceEnd:
                    key = str(sliceStart)

                else:
                    key = '%s:%s' % (str(sliceStart), str(sliceEnd))

                weightSlicesDict[key] = tuple(sliceValues)
                sliceStart = None
                sliceEnd = None
                sliceValues = []

    return weightSlicesDict