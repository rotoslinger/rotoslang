 #====================================================================================
#====================================================================================
#
# ka_menu_weightLib
#
# DESCRIPTION:
#   functions for manipulation and query of maya selection
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

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_clipBoard as ka_clipBoard
import ka_rigTools.ka_pymel as ka_pymel
import ka_rigTools.ka_weightBlender as ka_weightBlender
import ka_rigTools.ka_context as ka_context


def storeSelection():
    selection = cmds.ls(selection=True)
    ka_clipBoard.add('storedSelection', selection)

def getStoredSelection():
    selection = ka_clipBoard.get('storedSelection', [])
    selection = ka_pymel.getAsPyNodes(selection)
    return selection


def invertSelectionOrder(selection=None):
    if not selection:
        selection = pymel.ls(selection=True)

    selection.reverse()
    pymel.select(selection)

#def orderSelectionByHierchy(selection=None):
    #if not selection:
        #selection = pymel.ls(selection=True)

        #selection.reverse()
    #pymel.select(selection)


def islandSelectComponents():
    a = pymel.ls(selection=True, flatten=True)[0]
    island = []
    newFaces = pymel.ls(a.connectedVertices(), flatten=True)
    i = 0
    while i < 999 and newFaces:
        i += 1

        newFace = newFaces.pop(0)
        connectedFaces = pymel.ls(newFace.connectedVertices(), flatten=True)
        for connectedFace in iter(connectedFaces):
            if connectedFace not in island:
                island.append(connectedFace)
                newFaces.append(connectedFace)

    pymel.select(island)



def selectRight():
    if context.selectionIsComponents():
        pass
    #weightBlenderInfo = ka_weightBlender.WeightBlenderInfo()
    #selectionIsComponents

previousPointIDs = None
def pickWalk(direction, additive=False):
    context = ka_context.newContext()

    selection = cmds.ls(selection=True)
    if context.selectionIsComponents():
        global previousPointIDs

        weightBlenderInfo = ka_weightBlender.WeightBlenderInfo()
        rightPoints = []
        rightPointIds = []
        leftPoints = []
        leftPointsIds = []
        directionSwitch = False

        for pointID in weightBlenderInfo.iconPointsA:
            rightPoints.append(weightBlenderInfo.pntDict[pointID])
            rightPointIds.append(pointID)

        for pointID in weightBlenderInfo.iconPointsB:
            leftPoints.append(weightBlenderInfo.pntDict[pointID])
            leftPointsIds.append(pointID)

        if direction == 'right':
            nextPoints = rightPoints
            nextPointIds = rightPointIds

        elif direction == 'left':
            nextPoints = leftPoints
            nextPointIds = leftPointsIds

        elif direction == 'top':
            nextPoints = rightPoints
            nextPointIds = rightPointIds

        elif direction == 'bottom':
            nextPoints = leftPoints
            nextPointIds = leftPointsIds

        if previousPointIDs:
            for pointID in nextPointIds:
                if pointID in previousPointIDs:
                    directionSwitch = True
                    break

            if directionSwitch:
                if nextPoints[0] in rightPoints:
                    nextPoints = leftPoints
                    nextPoints = leftPointsIds

                else:
                    nextPoints = rightPoints
                    nextPoints = rightPointIds

        pymel.select(nextPoints)
        previousPointIDs = nextPointIds

    else:
        cmds.pickWalk( direction=direction )

    if additive:
        pickWalkedSelection = cmds.ls(selection=True)
        cmds.select(selection, replace=True)
        cmds.select(pickWalkedSelection, add=True)