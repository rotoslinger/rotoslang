#====================================================================================
#====================================================================================
#
# ka_weightPainting
#
# DESCRIPTION:
#   tools for weight painting, and general weight editing on deformers, especially skinClusters.
#   many commands intended to be accessed through the ka_menu
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
import math
from . import ka_math

from traceback import format_exc as printError

from . import ka_selection as ka_selection             #;reload(ka_skinCluster)
from . import ka_skinCluster as ka_skinCluster             #;reload(ka_skinCluster)
from . import ka_preference as ka_preference             #;reload(ka_preference)


###################################################################################################################################
# GET PARALLEL WEIGHT BLENDER GLOBAL DATA
###################################################################################################################################
# parallel data
previousSelection = []

vertDict = {}    # key=vertIndex, Value=MeshVertex <pymelNode>
parallelRelationshipDict = {}    # key=vertIndex, Value={top:topVertIndex, bottom:bottomVertIndex, right:rightVertIndex, left:leftVertIndex}
vertPositionDict = {}    # key=vertIndex, Value=(worldPositionX, worldPositionY, worldPositionZ)
selectionIndices = []    # key=vertIndex, Value=MeshVertex <pymelNode>

# pair sequence
vertPairSequence = []    # key=vertIndex, Value=List of Tuples, with each tuple containing vertIndices
currentVertPairSequenceIndex = 0    # index
previousVertPairSequenceIndex = None    # index

# sphere data
rightColoredVertexSpheres = []
leftColoredVertexSpheres = []
lambertA = None
lambertB = None
lambertAIsBlack = True
lambertBIsBlack = True

# weight data
skinCluster = None
influenceDict = {} #key=vertIndex, Value={<index>:<influence>}
weightsDict = {}    #key=vertIndex, Value={<index>:<weight value>}
appliedWeightsDict = {}    #key=vertIndex, Value={<index>:<weight value>}

# weight blend undo
weightBlend_maxUndos = 10
weightBlend_weightsDictHistory = []    #[(weightDict, skinCluster), (weightDict, skinCluster)...]
weightBlend_weightsDictHistoryIndex = 0    #current position in weight dict


###################################################################################################################################
# ARTISAN PAINT FUNCTIONS
###################################################################################################################################

def paint(influence):
    oldInfluence = pymel.artAttrSkinPaintCtx('artAttrSkinContext', query=True, influence=True)
    pymel.optionVar( stringValue=("ka_weightPaintTool_oldPaintingInfluence", oldInfluence))

    mel.eval('setSmoothSkinInfluence '+influence)
    pymel.setAttr(influence+".lockInfluenceWeights", 0)

    applyJointColors()
    #refreshMayaPaintUI()

def paintAndHoldAllOthers(influence):
    holdAllInfluences()
    paint(influence)


def togglePaint():
    oldInfluence = mel.eval('artAttrSkinPaintCtx -q -influence artAttrSkinContext')

    mel.eval('setSmoothSkinInfluence `optionVar -q ka_weightPaintTool_oldPaintingInfluence`;')

    pymel.setAttr(pymel.optionVar(query='ka_weightPaintTool_oldPaintingInfluence',)+'.lockInfluenceWeights', 0)
    pymel.optionVar(stringValue = ['ka_weightPaintTool_oldPaintingInfluence', oldInfluence])

    applyJointColors()
    #refreshMayaPaintUI()


def holdInfluence(influence):
    pymel.setAttr(influence+'.lockInfluenceWeights', 1)

    applyJointColors()
    #refreshMayaPaintUI()

def unholdInfluence(influence):
    pymel.setAttr(influence+'.lockInfluenceWeights', 0)

    applyJointColors()
    #refreshMayaPaintUI()

def holdAllInfluences():
    influenceList = getInfluences()
    for influence in influenceList:
        pymel.setAttr(influence+'.lockInfluenceWeights', 1)

def unholdAllInfluences():
    influenceList = getInfluences()
    for influence in influenceList:
        pymel.setAttr(influence+'.lockInfluenceWeights', 0)

def mirrorWeights(inverse=False):
    selection = pymel.ls(selection=True, objectsOnly=True, transforms=True, int=True)

    if len(selection) == 1:
        #raise NameError('Too many objects selected')
        skinCluster = findRelatedSkinCluster(selection[0])
        skinCluster.envelope.set(0)

        pymel.copySkinWeights(mirrorMode='YZ', surfaceAssociation='closestPoint', influenceAssociation=['label', 'oneToOne', 'closestBone', 'name'], mirrorInverse=inverse,)

        skinCluster.envelope.set(1)

    else:
        skinClusterA = findRelatedSkinCluster(selection[0])
        skinClusterB = findRelatedSkinCluster(selection[1])
        skinClusterA.envelope.set(0)
        skinClusterB.envelope.set(0)

        pymel.copySkinWeights(sourceSkin=skinClusterA, destinationSkin=skinClusterB, mirrorMode='YZ', surfaceAssociation='closestPoint', influenceAssociation=['label', 'oneToOne', 'closestBone', 'name'], mirrorInverse=inverse,)

        skinClusterA.envelope.set(1)
        skinClusterB.envelope.set(1)

    refreshMayaPaintUI()
#cmds.select(['adam_body_HI.f[4481:4496]', 'adam_body_HI.f[4519:4540]', 'adam_body_HI.f[4559:4593]', 'adam_body_HI.f[4606:4647]', 'adam_body_HI.f[4655:4702]', 'adam_body_HI.f[4704:5753]', 'adam_body_HI.f[5765:5774]', 'adam_body_HI.f[6133:6159]', 'adam_body_HI.f[6162:7997]', 'adam_body_HI.f[8367]', 'adam_body_HI.f[8380]', 'adam_body_HI.f[8383:8396]', 'adam_body_HI.f[8401:15789]',])



def toggleAddReplace():

    toolContext = pymel.currentCtx()
    if toolContext == "artAttrSkinContext":

        oldPaintTool = pymel.artAttrSkinPaintCtx(toolContext,  query=True, selectedattroper=True)
        oldPaintToolValue = pymel.artAttrSkinPaintCtx(toolContext,  query=True, value=True,)
        oldPaintToolOpacity = pymel.artAttrSkinPaintCtx(toolContext,  query=True, opacity=True,)

        #defaults

        if not pymel.optionVar(query="ka_weightPaint_oldPaintToolValue", exists=True):
                pymel.optionVar(floatValue=("ka_weightPaint_oldPaintToolValue", 1))

        if not pymel.optionVar(query="ka_weightPaint_oldPaintToolOpacity", exists=True):
                pymel.optionVar(floatValue=("ka_weightPaint_oldPaintToolOpacity", 1))

        if oldPaintTool == "smooth":
            toggleSmooth()
        else:

            if oldPaintTool == "absolute":
                pymel.artAttrSkinPaintCtx(toolContext, edit=True, selectedattroper="additive", )
                pymel.artAttrSkinPaintCtx(toolContext, edit=True, value=pymel.optionVar(query="ka_weightPaint_oldPaintToolValue",) )
                pymel.artAttrSkinPaintCtx(toolContext, edit=True, opacity=pymel.optionVar(query="ka_weightPaint_oldPaintToolOpacity",) )
                mel.eval('toolPropertyShow;')

#            elif oldPaintTool == "scale":
#                pymel.artAttrSkinPaintCtx(toolContext, edit=True, selectedattroper="additive", )
#                pymel.artAttrSkinPaintCtx(toolContext, edit=True, value=pymel.optionVar(query="ka_weightPaint_oldPaintToolValue",) )
#                pymel.artAttrSkinPaintCtx(toolContext, edit=True, opacity=pymel.optionVar(query="ka_weightPaint_oldPaintToolOpacity",) )
#                mel.eval('toolPropertyShow;')

            else:
                pymel.artAttrSkinPaintCtx(toolContext, edit=True, selectedattroper=pymel.optionVar(query="ka_weightPaint_oldPaintTool",) )
                pymel.artAttrSkinPaintCtx(toolContext, edit=True, value=pymel.optionVar(query="ka_weightPaint_oldPaintToolValue",) )
                pymel.artAttrSkinPaintCtx(toolContext, edit=True, opacity=pymel.optionVar(query="ka_weightPaint_oldPaintToolOpacity",) )
                mel.eval('toolPropertyShow;')


            if oldPaintTool in ['absolute', 'additive', 'scale']:
                pymel.optionVar(stringValue=("ka_weightPaint_oldPaintTool", oldPaintTool))
                pymel.optionVar(floatValue=("ka_weightPaint_oldPaintToolValue", oldPaintToolValue))
                pymel.optionVar(floatValue=("ka_weightPaint_oldPaintToolOpacity", oldPaintToolOpacity))

            mel.eval('artAttrSkinToolScript 4;')
            pymel.artAttrSkinPaintCtx(pymel.currentCtx(), edit=True, showactive=True)

def toggleSmooth():

    toolContext = pymel.currentCtx()
    if toolContext == "artAttrSkinContext":

        preSmoothPaintTool = pymel.artAttrSkinPaintCtx(toolContext, query=True, selectedattroper=True)
        preSmoothPaintToolValue = pymel.artAttrSkinPaintCtx(toolContext,  query=True, value=True,)
        preSmoothPaintToolOpacity = pymel.artAttrSkinPaintCtx(toolContext,  query=True, opacity=True,)

        #defaults
        if not pymel.optionVar(query="ka_weightPaint_preSmoothPaintTool", exists=True):
            pymel.optionVar(stringValue=("ka_weightPaint_preSmoothPaintTool", 'smooth'))

        if not pymel.optionVar(query="ka_weightPaint_preSmoothPaintToolValue", exists=True):
            pymel.optionVar(floatValue=("ka_weightPaint_preSmoothPaintToolValue", 1))

        if not pymel.optionVar(query="ka_weightPaint_preSmoothPaintToolOpacity", exists=True):
            pymel.optionVar(floatValue=("ka_weightPaint_preSmoothPaintToolOpacity", 1))


        if preSmoothPaintTool == "smooth":
            pymel.artAttrSkinPaintCtx(toolContext, edit=True, selectedattroper=pymel.optionVar(query="ka_weightPaint_preSmoothPaintTool",) )
            pymel.artAttrSkinPaintCtx(toolContext, edit=True, value=pymel.optionVar(query="ka_weightPaint_preSmoothPaintToolValue",) )
            pymel.artAttrSkinPaintCtx(toolContext, edit=True, opacity=pymel.optionVar(query="ka_weightPaint_preSmoothPaintToolOpacity",) )
            mel.eval('toolPropertyShow;')

        else:
            pymel.artAttrSkinPaintCtx(toolContext, edit=True, selectedattroper="smooth", )
            pymel.artAttrSkinPaintCtx(toolContext, edit=True, value=pymel.optionVar(query="ka_weightPaint_preSmoothPaintToolValue",) )
            pymel.artAttrSkinPaintCtx(toolContext, edit=True, opacity=pymel.optionVar(query="ka_weightPaint_preSmoothPaintToolOpacity",) )
            mel.eval('toolPropertyShow;')


        pymel.optionVar(stringValue=("ka_weightPaint_preSmoothPaintTool", preSmoothPaintTool))
        pymel.optionVar(floatValue=("ka_weightPaint_preSmoothPaintToolValue", preSmoothPaintToolValue))
        pymel.optionVar(floatValue=("ka_weightPaint_preSmoothPaintToolOpacity", preSmoothPaintToolOpacity))

        mel.eval('artAttrSkinToolScript 4;')
        pymel.artAttrSkinPaintCtx(pymel.currentCtx(), edit=True, showactive=True)


def resetSkin(mode):
    '''rebinds the mesh with the same weights, and without the history of the previous skin cluster'''

    oldInfluence = pymel.artAttrSkinPaintCtx('artAttrSkinContext', query=True, influence=True)

    deleteAllBindPoses()

    selections = pymel.ls(selection=True, objectsOnly=True, transforms=True, int=True)
    for selection in selections:

        skinCluster = findRelatedSkinCluster(selection)
        if skinCluster:
            influenceList = getInfluences(skinCluster)
            objectHistory = pymel.listHistory(selection, interestLevel=2, pruneDagObjects=True)
            if skinCluster not in objectHistory:    pymel.error('skin cluster: '+skinCluster+'was not found in '+selection+'\'s history: '+str(objectHistory))
            skinClusterIndexInHistory = objectHistory.index(skinCluster)

            obeyMaxInfluences = pymel.skinCluster(skinCluster, query=True, obeyMaxInfluences=True)
            maximumInfluences = pymel.skinCluster(skinCluster, query=True, maximumInfluences=True)

            historyParent = None
            if not skinCluster == objectHistory[0]:
                historyParent = objectHistory[skinClusterIndexInHistory-1]

            #rebind to new joint positions, no change to original geometry
            if mode == 'reset':
                pymel.setAttr(skinCluster+".envelope", 0)
                duplicateSkin = pymel.duplicate( selection, returnRootsOnly=True,)[0]

                pymel.select(influenceList, duplicateSkin, replace=True,)
                duplicateSkinCluster = pymel.skinCluster(ignoreBindPose=True, toSelectedBones=True, obeyMaxInfluences=obeyMaxInfluences, maximumInfluences=maximumInfluences)

                pymel.copySkinWeights(sourceSkin=skinCluster, destinationSkin=duplicateSkinCluster, noMirror=True, influenceAssociation="oneToOne",)

                pymel.delete(skinCluster)

                pymel.select(influenceList, selection, replace=True,)
                newSkinCluster = pymel.skinCluster(name=skinCluster, ignoreBindPose=True, toSelectedBones=True, obeyMaxInfluences=obeyMaxInfluences, maximumInfluences=maximumInfluences)

                pymel.copySkinWeights(sourceSkin=duplicateSkinCluster, destinationSkin=newSkinCluster, noMirror=True, influenceAssociation="oneToOne",)

                pymel.delete(duplicateSkin)

                objectHistory[skinClusterIndexInHistory] = newSkinCluster
                if historyParent:
                    pymel.reorderDeformers( historyParent, newSkinCluster, selection )

            #bake the skin deformed mesh, and reskin as new original geometry
            elif mode == 'bake':

                duplicateSkin = pymel.duplicate( selection, returnRootsOnly=True,)[0]

                pymel.select(influenceList, duplicateSkin, replace=True,)
                duplicateSkinCluster = pymel.skinCluster(ignoreBindPose=True, toSelectedBones=True, obeyMaxInfluences=obeyMaxInfluences, maximumInfluences=maximumInfluences)

                pymel.copySkinWeights(sourceSkin=skinCluster, destinationSkin=duplicateSkinCluster, noMirror=True, influenceAssociation="oneToOne",)

                print('bakeTime')
                pymel.delete(selection, constructionHistory=True,)

                pymel.select(influenceList, selection, replace=True,)
                newSkinCluster = pymel.skinCluster(ignoreBindPose=True, toSelectedBones=True, obeyMaxInfluences=obeyMaxInfluences, maximumInfluences=maximumInfluences)

                pymel.copySkinWeights(sourceSkin=duplicateSkinCluster, destinationSkin=newSkinCluster, noMirror=True, influenceAssociation="oneToOne",)

                pymel.delete(duplicateSkin)

    pymel.select(selections)
    if oldInfluence:
        paint(oldInfluence)


###################################################################################################################################
# COPY PASTE WEIGHTS FUNCTIONS
###################################################################################################################################


def copySkinWeights(verts=None, copySpecificInfluence=None):
    '''copys skin weights from 1 or more components, if more than 1, then the weight copy is an average'''

    if not verts:
        verts = pymel.ls(selection=True, flatten=True)

    skinCluster = findRelatedSkinCluster(verts[0])


    if copySpecificInfluence:
        influences = pymel.skinCluster(skinCluster, query=True, influence=True,)

        if copySpecificInfluence in influences:

            weights = []
            for i, influence in enumerate(influences):

                if influence == copySpecificInfluence:
                    weights.append(1)
                else:
                    weights.append(0)

            weights1 = weights
            weights2 = weights
        else:
            pymel.error(copySpecificInfluence+'is not an influence of the skin cluster of the verts')

    elif len(verts) == 1:

        influences = pymel.skinCluster(skinCluster, query=True, influence=True,)
        weights1 = pymel.skinPercent(skinCluster, query=True, value=True,)
        weights2 = pymel.skinPercent(skinCluster, query=True, value=True,)

    elif len(verts) == 2:

        influences = pymel.skinCluster(skinCluster, query=True, influence=True,)
        weights1 = pymel.skinPercent(skinCluster, verts[0], query=True, value=True,)
        weights2 = pymel.skinPercent(skinCluster, verts[1],  query=True, value=True,)

    elif len(verts) > 2:

        listOfListOfValues = []
        for vert in verts:

            listOfValues = pymel.skinPercent(skinCluster, vert, query=True, value=True)
            listOfListOfValues.append(listOfValues)

        averagedList = []
        for index in range(len(listOfListOfValues[0])):

            listOfValuesToAverage = []
            for listOfValues in listOfListOfValues:
                listOfValuesToAverage.append(listOfValues[index])

            value = (math.fsum(listOfValuesToAverage) / len(listOfValuesToAverage))

            averagedList.append(value)

        influences = pymel.skinCluster(skinCluster, query=True, influence=True,)
        weights1 = averagedList
        weights2 = averagedList

    pymel.optionVar( clearArray='copySkinWeights_clipBoard_1')
    pymel.optionVar( clearArray='copySkinInfluences_clipBoard_1')
    pymel.optionVar( clearArray='copySkinWeights_clipBoard_2')

    for i, weight in enumerate(weights1):
        if weights1[i] == 0 and weights2[i] == 0:
            pass

        else:

            pymel.optionVar( floatValueAppend=['copySkinWeights_clipBoard_1', weights1[i] ])
            pymel.optionVar( floatValueAppend=['copySkinWeights_clipBoard_2', weights2[i] ])
            pymel.optionVar( stringValueAppend=['copySkinInfluences_clipBoard_1', influences[i] ])



def pasteSkinWeights(verts=None, weightedAverage=100):

    if not verts:
        verts = pymel.ls(selection=True)

    skinClusters = []
    for vert in verts:
        skinCluster = findRelatedSkinCluster(vert)
        skinClusters.append(skinCluster)

    influences = pymel.optionVar(query='copySkinInfluences_clipBoard_1')
    weights1 =  pymel.optionVar(query='copySkinWeights_clipBoard_1')
    weights2 =  pymel.optionVar(query='copySkinWeights_clipBoard_2')

    lenOfInfluences = len(influences)

    averagedWeights = []
    for index in range(lenOfInfluences):

        weightsA = weights2[index] * (0.01 * ((200 - weightedAverage) * 1))
        weightsB = weights1[index] * ((weightedAverage * 1) * 0.01)

        value = ((weightsA+weightsB) / 2)

        averagedWeights.append(value)


    listOfTuples = []
    for i in range(lenOfInfluences):
        listOfTuples.append((influences[i], averagedWeights[i]))

    for skinCluster in skinClusters:
        pymel.skinPercent(skinCluster, verts, normalize=False, zeroRemainingInfluences=True, transformValue=listOfTuples)

def getSkinClusterData(vertIndex):
    global skinCluster
    global vertDict
    global influenceDict
    global weightsDict

    if vertIndex not in weightsDict:
        strVertIndex = str(vertIndex)
        strSkinCluster = str(skinCluster)
        usedWeightIndices = cmds.getAttr('%s.wl[%s].weights' % (strSkinCluster, strVertIndex,), multiIndices=True)
        weightsDict[vertIndex] = {}
        for usedWeightIndex in usedWeightIndices:
            unusedWeight = False
            weight = cmds.getAttr('%s.wl[%s].weights[%s]' % (strSkinCluster, strVertIndex, str(usedWeightIndex)))

            # get influence if not already in dict
            if not usedWeightIndex in influenceDict:
                influence = skinCluster.matrix[usedWeightIndex].inputs()
                if influence:
                    influenceDict[usedWeightIndex] = influence[0]
                else:
                    unusedWeight = True

            if not unusedWeight:
                weightsDict[vertIndex][usedWeightIndex] = weight

def copyWeightsFromNeighbors():

    global ka_pasteWeightsFromNeighbors_copyWeightsSucceeded        ;ka_pasteWeightsFromNeighbors_copyWeightsSucceeded=False
    global ka_weightBlender_ignoreInfluenceHolding
    ka_weightBlender_ignoreInfluenceHolding = ka_preference.get('weightBlender_ignoreInfluenceHolding', True)
    #if not pymel.optionVar( exists='ka_weightBlender_ignoreInfluenceHolding' ):
        #pymel.optionVar( iv=('ka_weightBlender_ignoreInfluenceHolding', 1))
    #ka_weightBlender_ignoreInfluenceHolding = pymel.optionVar( query='ka_weightBlender_ignoreInfluenceHolding' )

    getParallelVertData()

    global vertDict
    global parallelRelationshipDict
    global vertPositionDict
    global selectionIndices

    global weightBlend_weightsDictHistory
    global weightBlend_maxUndos

    global skinCluster
    global influenceDict
    global weightsDict
    global appliedWeightsDict

    global vertPairSequence

    skinCluster = None
    influenceDict = {}
    weightsDict = {}

    selection = pymel.ls(selection=True, flatten=True)
    skinCluster = findRelatedSkinCluster(selection[0])

 # Get skin weights (they will be stored into global variables)
    for sequence in vertPairSequence:
        for vertPair in sequence:
            for vert in vertPair:
                getSkinClusterData(vert)


    for vertIndex in parallelRelationshipDict:

        #vertTopIndex = parallelRelationshipDict[vertIndex]['top']
        #vertBottomIndex = parallelRelationshipDict[vertIndex]['bottom']
        #vertRightIndex = parallelRelationshipDict[vertIndex]['right']
        #vertLeftIndex = parallelRelationshipDict[vertIndex]['left']

        #vert = vertDict[vertIndex]
        #vertUpperNeighbor = vertDict[vertTopIndex]
        #vertLowerNeighbor = vertDict[vertBottomIndex]
        #vertRightNeighbor = vertDict[vertRightIndex]
        #vertLeftNeighbor = vertDict[vertLeftIndex]

        # Get skin weights (they will be stored into global variables)
        getSkinClusterData(vertIndex)
        #getSkinClusterData(vertTopIndex)
        #getSkinClusterData(vertBottomIndex)
        #getSkinClusterData(vertRightIndex)
        #getSkinClusterData(vertLeftIndex)

        #vertWeights = weightsDict[vertIndex]
        #topWeights = weightsDict[vertTopIndex]
        #bottomWeights = weightsDict[vertBottomIndex]
        #rightWeights = weightsDict[vertRightIndex]
        #leftWeights = weightsDict[vertLeftIndex]

        #come up with a factor that will allow normalized blending if the ignore
        #unheld influences mode is not set.
        if not ka_weightBlender_ignoreInfluenceHolding:
            totalHeld_vertWeight = 0
            totalUnheld_vertWeight = 0

            totalHeld_topWeight = 0
            totalUnheld_topWeight = 0

            totalHeld_bottomWeight = 0
            totalUnheld_bottomWeight = 0

            totalHeld_rightWeight = 0
            totalUnheld_rightWeight = 0

            totalHeld_leftWeight = 0
            totalUnheld_leftWeight = 0

            for weightIndex in vertWeights:

                if influenceDict[weightIndex].lockInfluenceWeights.get():
                    totalHeld_vertWeight += vertWeights.get(weightIndex, 0.0)
                    totalHeld_topWeight += topWeights.get(weightIndex, 0.0)
                    totalHeld_bottomWeight += bottomWeights.get(weightIndex, 0.0)
                    totalHeld_rightWeight += rightWeights.get(weightIndex, 0.0)
                    totalHeld_leftWeight += leftWeights.get(weightIndex, 0.0)

                else:
                    totalUnheld_vertWeight += vertWeights.get(weightIndex, 0.0)
                    totalUnheld_topWeight += topWeights.get(weightIndex, 0.0)
                    totalUnheld_bottomWeight += bottomWeights.get(weightIndex, 0.0)
                    totalUnheld_rightWeight += rightWeights.get(weightIndex, 0.0)
                    totalUnheld_leftWeight += leftWeights.get(weightIndex, 0.0)


            #figure out the multiply factor if none or either of the totals equals zero
            unheldNormalizeFactor_topWeight = 0
            unheldNormalizeFactor_bottomWeight = 0
            unheldNormalizeFactor_rightWeight = 0
            unheldNormalizeFactor_leftWeight = 0

            if not totalUnheld_vertWeight == 0: #if its zero, your not going to do much...
                if totalUnheld_topWeight:    unheldNormalizeFactor_topWeight = totalUnheld_vertWeight / totalUnheld_topWeight
                if totalUnheld_bottomWeight: unheldNormalizeFactor_bottomWeight = totalUnheld_vertWeight / totalUnheld_bottomWeight
                if totalUnheld_rightWeight:  unheldNormalizeFactor_rightWeight = totalUnheld_vertWeight / totalUnheld_rightWeight
                if totalUnheld_leftWeight:   unheldNormalizeFactor_leftWeight = totalUnheld_vertWeight / totalUnheld_leftWeight


            for weightIndex in vertWeights:
                if not vertWeights.get(weightIndex, 0.0) and not topWeights.get(weightIndex, 0.0) and not bottomWeights.get(weightIndex, 0.0) and not rightWeights.get(weightIndex, 0.0) and not leftWeights.get(weightIndex, 0.0):
                    pass
                else:
                    if influenceDict[weightIndex].lockInfluenceWeights.get():
                        # If the influence is locked, manipulate the data for the top, bottom, right, and left
                        # weights to be the same as the original vert, so that blending has no effect for those
                        # influences

                        weightsDict[vertTopIndex][weightIndex] = weightsDict[vertIndex][weightIndex]
                        weightsDict[vertBottomIndex][weightIndex] = weightsDict[vertIndex][weightIndex]
                        weightsDict[vertRightIndex][weightIndex] = weightsDict[vertIndex][weightIndex]
                        weightsDict[vertLeftIndex][weightIndex] = weightsDict[vertIndex][weightIndex]

                    else:
                        # manipulate the data for the top, bottom, right, and left weights so that blending
                        # 100% to their unheld influences would leave you with a weight total of 1. This will
                        # also allow a smooth transitioning with a value of less than 1.

                        if unheldNormalizeFactor_topWeight:
                            weightsDict[vertTopIndex][weightIndex] *= unheldNormalizeFactor_topWeight
                        else: weightsDict[vertTopIndex][weightIndex] = weightsDict[vertIndex][weightIndex] #use the vert weight

                        if unheldNormalizeFactor_bottomWeight:
                            weightsDict[vertBottomIndex][weightIndex] *= unheldNormalizeFactor_bottomWeight
                        else: weightsDict[vertBottomIndex][weightIndex] = weightsDict[vertIndex][weightIndex]  #use the vert weight

                        if unheldNormalizeFactor_rightWeight:
                            weightsDict[vertRightIndex][weightIndex] *= unheldNormalizeFactor_rightWeight
                        else: weightsDict[vertRightIndex][weightIndex] = weightsDict[vertIndex][weightIndex]  #use the vert weight

                        if unheldNormalizeFactor_leftWeight:
                            weightsDict[vertLeftIndex][weightIndex] *= unheldNormalizeFactor_leftWeight
                        else: weightsDict[vertLeftIndex][weightIndex] = weightsDict[vertIndex][weightIndex]  #use the vert weight

    appliedWeightsDict = weightsDict.copy()
    addToUndoStack('weightsDict')
    ka_pasteWeightsFromNeighbors_copyWeightsSucceeded = True

def pasteWeightsFromNeighbors_changeNeighbors(reverse=False):
    global vertPairSequence
    global currentVertPairSequenceIndex
    global previousVertPairSequenceIndex

    sequenceLength = len(vertPairSequence)
    sequenceIndex = currentVertPairSequenceIndex

    if reverse:
        if sequenceIndex != 0 and sequenceLength >= 1: # not the last item in sequence or a sequence of 1
            previousVertPairSequenceIndex = currentVertPairSequenceIndex
            currentVertPairSequenceIndex = currentVertPairSequenceIndex - 1

        else:
            previousVertPairSequenceIndex = currentVertPairSequenceIndex
            currentVertPairSequenceIndex = sequenceLength - 1

    else:
        if sequenceIndex != sequenceLength-1 and sequenceLength >= 1: # not the last item in sequence or a sequence of 1
            previousVertPairSequenceIndex = currentVertPairSequenceIndex
            currentVertPairSequenceIndex = currentVertPairSequenceIndex + 1

        else:
            previousVertPairSequenceIndex = currentVertPairSequenceIndex
            currentVertPairSequenceIndex = 0

    pasteWeightsFromNeighbors_positionSpheres()

def pasteWeightsFromNeighbors_positionSpheres():
    global rightColoredVertexSpheres
    global leftColoredVertexSpheres

    global vertPositionDict

    global vertPairSequence
    global currentVertPairSequenceIndex

    OOOOOOO = 'vertPairSequence';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
    OOOOOOO = 'currentVertPairSequenceIndex';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
    OOOOOOO = 'rightColoredVertexSpheres';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
    sequenceIndex = currentVertPairSequenceIndex
    currentVertPairList = vertPairSequence[sequenceIndex]

    for i, each in enumerate(rightColoredVertexSpheres):
        vertA = currentVertPairList[i][0]
        vertB = currentVertPairList[i][1]
        pymel.xform(leftColoredVertexSpheres[i], translation=vertPositionDict[vertA], worldSpace=True)
        pymel.xform(rightColoredVertexSpheres[i], translation=vertPositionDict[vertB], worldSpace=True)

        setSpherePairScale_fromCameraSpace(vertPositionDict[vertB], rightColoredVertexSpheres[i], vertPositionDict[vertA], leftColoredVertexSpheres[i])

def pasteWeightsFromNeighbors(weightedAverage=100):
    #pymel.undoInfo(stateWithoutFlush=False)

    global ka_pasteWeightsFromNeighbors_copyWeightsSucceeded
    if ka_pasteWeightsFromNeighbors_copyWeightsSucceeded:
        global ka_weightBlender_ignoreInfluenceHolding

        global skinCluster
        global influenceDict
        global weightsDict
        global appliedWeightsDict
        global parallelRelationshipDict
        global vertPositionDict

        global rightColoredVertexSpheres
        global leftColoredVertexSpheres
        global lambertA
        global lambertB
        global lambertAIsBlack
        global lambertBIsBlack

        global previousSelection
        global selectionIndices

        global ka_pasteWeightsFromNeighbors_previousShiftState


        global vertPairSequence
        global currentVertPairSequenceIndex
        global previousVertPairSequenceIndex

        appliedWeightsDict = {}

        selection = previousSelection
        lenOfSelection = len(selectionIndices)
        strSkinCluster = str(skinCluster)

        #shiftState = False
        #if (cmds.getModifiers() & 1) > 0:
            #shiftState = True #Shift is down

        for i, vertIndex in enumerate(selectionIndices):
            vertLeftIndex = vertPairSequence[currentVertPairSequenceIndex][i][0]
            vertRightIndex = vertPairSequence[currentVertPairSequenceIndex][i][1]

            ## get index of our two blend verts
            #if lenOfSelection == 1:
                ##if shiftState:
                #if pasteWeightsFromNeighbors_pairIndex:
                    #vertRightIndex = parallelRelationshipDict[vertIndex]['top']
                    #vertLeftIndex = parallelRelationshipDict[vertIndex]['bottom']
                #else:
                    #vertRightIndex = parallelRelationshipDict[vertIndex]['right']
                    #vertLeftIndex = parallelRelationshipDict[vertIndex]['left']

                # is pairIndex different then its previous value? if so do not repeat the work
                #if not shiftState == ka_pasteWeightsFromNeighbors_previousShiftState:
                #if not pasteWeightsFromNeighbors_pairIndex == pasteWeightsFromNeighbors_previousPairIndex:
                    #ka_pasteWeightsFromNeighbors_previousShiftState = shiftState
                    #pasteWeightsFromNeighbors_previousPairIndex = pasteWeightsFromNeighbors_pairIndex
                    #pymel.xform(rightColoredVertexSpheres[0], translation=vertPositionDict[vertRightIndex], worldSpace=True)
                    #pymel.xform(leftColoredVertexSpheres[0], translation=vertPositionDict[vertLeftIndex], worldSpace=True)
                    #setSpherePairScale_fromCameraSpace(vertPositionDict[vertRightIndex], rightColoredVertexSpheres[0], vertPositionDict[vertLeftIndex], leftColoredVertexSpheres[0])

            #else:
                #vertRightIndex = parallelRelationshipDict[vertIndex]['right']
                #vertLeftIndex = parallelRelationshipDict[vertIndex]['left']

            # are we blending to the left or right?
            finalWeights = {}
            weightsA = weightsDict[vertIndex].copy()
            if weightedAverage < 100:
                blend = (100 - weightedAverage)
                weightsB = weightsDict[vertRightIndex].copy()

            elif weightedAverage > 100:
                blend = (weightedAverage - 100)
                weightsB = weightsDict[vertLeftIndex].copy()

            else: # is at 100, ie: inital position, with no blending
                blend = (100 - weightedAverage)
                weightsB = None
                finalWeights = weightsA

            if weightsB:
                # any indices in one list and not the other? if so, their value is 0.0
                for weightIndex in weightsB:
                    if weightIndex not in weightsA:
                        weightsA[weightIndex] = 0.0

                for weightIndex in weightsA:
                    if weightIndex not in weightsB:
                        weightsB[weightIndex] = 0.0

                # do the averaging math
                for weightIndex in weightsA:
                    weightA = weightsA[weightIndex] * (0.01 * ((100 - blend) * 2))
                    weightB = weightsB[weightIndex] * ((blend * 2) * 0.01)

                    value = ((weightA+weightB) / 2)
                    if value:
                        finalWeights[weightIndex] = value

            strVertIndex = str(vertIndex)
            cmds.removeMultiInstance('%s.wl[%s]' % (strSkinCluster, strVertIndex,))
            for weightIndex in finalWeights:
                cmds.setAttr('%s.wl[%s].w[%s]' % (strSkinCluster, strVertIndex, str(weightIndex)), finalWeights[weightIndex])

            # store final applied weight
            appliedWeightsDict[vertIndex] = finalWeights

            ###########################
            # color Spheres
            if weightedAverage < 100:
                if weightedAverage == 0: lambertA.incandescence.set( [ 1, 1, 1 ] )
                else:                    lambertA.incandescence.set( [ blend*0.01, 0.25+(blend*0.0075), blend*0.0015 ] )
                lambertAIsBlack = False

                if not lambertBIsBlack:
                    lambertB.incandescence.set( [0, 0, 0] )
                    lambertBIsBlack = True

            elif weightedAverage > 100:
                if weightedAverage == 200: lambertB.incandescence.set( [ 1, 1, 1 ] )
                else:                      lambertB.incandescence.set( [ blend*0.01, 0.25+(blend*0.0075), blend*0.0015 ] )
                lambertBIsBlack = False

                if not lambertAIsBlack:
                    lambertA.incandescence.set( [0, 0, 0] )
                    lambertAIsBlack = True

            else: #is 100 (50%)
                if not lambertBIsBlack:
                    lambertB.incandescence.set( [0, 0, 0] )
                    lambertBIsBlack = True

                if not lambertAIsBlack:
                    lambertA.incandescence.set( [0, 0, 0] )
                    lambertAIsBlack = True


            #
            ###########################

def addToUndoStack(dictToAdd):
    if dictToAdd == 'weightsDict':
        global weightsDict
        inputWeightDict = weightsDict

    if dictToAdd == 'appliedWeightsDict':
        global appliedWeightsDict
        inputWeightDict = appliedWeightsDict

    global selectionIndices
    global skinCluster
    global weightBlend_maxUndos
    global weightBlend_weightsDictHistory
    global weightBlend_weightsDictHistoryIndex

    # Does given weight data differ from the last undo?
    weightsDifferFromLastUndo = False
    if weightBlend_weightsDictHistory:
        historicalWeightDict, historicalSkinCluster = weightBlend_weightsDictHistory[weightBlend_weightsDictHistoryIndex]
        if historicalSkinCluster == skinCluster:
            for vertIndex in selectionIndices:
                if vertIndex in inputWeightDict and vertIndex in historicalWeightDict:
                    for weightIndex in inputWeightDict[vertIndex]:
                        if weightsDifferFromLastUndo:
                            break
                        else:

                            if weightIndex in historicalWeightDict[vertIndex] and weightIndex in inputWeightDict[vertIndex]:
                                if round(inputWeightDict[vertIndex][weightIndex], 3) != round(historicalWeightDict[vertIndex][weightIndex], 3):
                                    weightsDifferFromLastUndo = True
                                    break


                            else:weightsDifferFromLastUndo = True ;
                else:weightsDifferFromLastUndo = True ;
        else:weightsDifferFromLastUndo = True ;
    else:weightsDifferFromLastUndo = True ;


    # store to undo stack
    if weightsDifferFromLastUndo:

        weightsAreValid = True # are they valid (totaling 1.0)?
        for vertIndex in selectionIndices:
            weightTotal = 0.0
            for weightIndex in inputWeightDict[vertIndex]:
                weightTotal += inputWeightDict[vertIndex][weightIndex]
            if not round(weightTotal, 2) == 1.0:# > 1.001 or weightTotal < 0.999:
                weightsAreValid = False

        if weightsAreValid:
            # is current undo 0? if not this is the result of redos
            while weightBlend_weightsDictHistoryIndex != 0:
                if weightBlend_weightsDictHistoryIndex < 0:
                    pymel.error('how did that happen?')
                weightBlend_weightsDictHistoryIndex -= 1
                weightBlend_weightsDictHistory.pop(0)

            if len(weightBlend_weightsDictHistory) >= weightBlend_maxUndos:
                weightBlend_weightsDictHistory.pop(-1)

            outputWeightDict={}
            for vertIndex in selectionIndices:
                outputWeightDict[vertIndex] = {}
                weightTotal = 0.0
                for weightIndex in inputWeightDict[vertIndex]:
                    outputWeightDict[vertIndex][weightIndex] = inputWeightDict[vertIndex][weightIndex]
                    weightTotal += outputWeightDict[vertIndex][weightIndex]

            weightBlend_weightsDictHistory.insert(0, (outputWeightDict, skinCluster))


def undoWeightBlend():
    global weightsDict
    global weightBlend_weightsDictHistory
    global weightBlend_weightsDictHistoryIndex

    ## if there is something to undo
    if not len(weightBlend_weightsDictHistory)-1  <  weightBlend_weightsDictHistoryIndex+1:
        weightBlend_weightsDictHistoryIndex += 1
        historicalWeightDict, historicalSkinCluster = weightBlend_weightsDictHistory[weightBlend_weightsDictHistoryIndex]

        strSkinCluster = str(historicalSkinCluster)
        for vertIndex in historicalWeightDict:
            strVertIndex = str(vertIndex)

            cmds.removeMultiInstance('%s.wl[%s]' % (strSkinCluster, strVertIndex,))
            for weightIndex in historicalWeightDict[vertIndex]:
                cmds.setAttr('%s.wl[%s].w[%s]' % (strSkinCluster, strVertIndex, str(weightIndex)), historicalWeightDict[vertIndex][weightIndex])
    else:
        pymel.warning('weightBlender has nothing left to redo')


def redoWeightBlend():
    global weightBlend_weightsDictHistory
    global weightBlend_weightsDictHistoryIndex

    if not weightBlend_weightsDictHistoryIndex-1 < 0:
        weightBlend_weightsDictHistoryIndex -= 1
        historicalWeightDict, historicalSkinCluster = weightBlend_weightsDictHistory[weightBlend_weightsDictHistoryIndex]

        strSkinCluster = str(historicalSkinCluster)
        for vertIndex in historicalWeightDict:
            strVertIndex = str(vertIndex)

            cmds.removeMultiInstance('%s.wl[%s]' % (strSkinCluster, strVertIndex,))
            for weightIndex in historicalWeightDict[vertIndex]:
                cmds.setAttr('%s.wl[%s].w[%s]' % (strSkinCluster, strVertIndex, str(weightIndex)), historicalWeightDict[vertIndex][weightIndex])
    else:
        pymel.warning('weightBlender has nothing left to undo')


def blendWeights(weightedAverage=100):
    #pymel.undoInfo(stateWithoutFlush=False)
    global ka_pasteWeightsFromNeighbors_copyWeightsSucceeded

    if ka_pasteWeightsFromNeighbors_copyWeightsSucceeded:
        global ka_pasteWeightsFromNeighbors_pasteInfoList                 ;pasteInfoList = ka_pasteWeightsFromNeighbors_pasteInfoList
        global ka_pasteWeightsFromNeighbors_skinCluster                 ;skinCluster = ka_pasteWeightsFromNeighbors_skinCluster
        global ka_pasteWeightsFromNeighbors_influences                  ;influences = ka_pasteWeightsFromNeighbors_influences


        selection = pymel.ls(selection=True, flatten=True)

        copiedInfluences = pymel.optionVar(query='copySkinInfluences_clipBoard_1')
        copiedWeights =  pymel.optionVar(query='copySkinWeights_clipBoard_1')
        averagedWeights = []
        listOfTuples = []
        listOfListOfTuples = []
        listOfVertsPerListOfTuples = []

        for list in pasteInfoList:

            vert, vertWeight, vertUpperNeighborWeight, vertLowerNeighborWeight, vertRightNeighborWeight, vertLeftNeighborWeight, vertInfluences = list

            localCopiedWeights = []
            pasteInfluences = []
            listOfTuples = []

            for copiedWeight in copiedWeights:
                localCopiedWeights.append(copiedWeight)

            for vertInfluence in vertInfluences:
                pasteInfluences.append(vertInfluence)

            for copiedInfluence in copiedInfluences:
                if not copiedInfluence in vertInfluences:
                    pasteInfluences.append(copiedInfluence)
                    vertWeight.append(0)


            for vertInfluence in vertInfluences:
                if not vertInfluence in copiedInfluences:
                    localCopiedWeights.insert(0, 0)

            listOfTuples = []
            for i, influence in enumerate(pasteInfluences):
                weightsA = vertWeight[i]            * (0.01 * (200 - weightedAverage) * 1)
                weightsB = localCopiedWeights[i]    * ((weightedAverage * 1) * 0.01)

                value = ((weightsA+weightsB) / 2)
                listOfTuples.append((str(influence), value))

            listOfListOfTuples.append(listOfTuples)
            listOfVertsPerListOfTuples.append(vert)


            pymel.undoInfo(stateWithoutFlush=True)
            for i, listOfTuples in enumerate(listOfListOfTuples):
                #must be cmds to allow clean undo
                pymel.skinPercent(str(skinCluster), str(listOfVertsPerListOfTuples[i]), normalize=False, zeroRemainingInfluences=True, transformValue=listOfTuples)
#                print 'setting',
#                print listOfTuples
#                print 'on vert: ',
#                print str(listOfVertsPerListOfTuples[i])
    else:
        pass


def setSpherePairScale_fromCameraSpace(vertAPosition, sphereA, vertBPosition, sphereB):

    vertAPositionInCameraSpace = getInCameraSpace(vertAPosition)
    sphereScaleA = vertAPositionInCameraSpace[2]*-0.01

    vertBPositionInCameraSpace = getInCameraSpace(vertBPosition)
    sphereScaleB = vertBPositionInCameraSpace[2]*-0.01

    distanceBetweenPoints = ka_math.distanceBetween(vertAPositionInCameraSpace, vertBPositionInCameraSpace)

    if sphereScaleA > (distanceBetweenPoints / 5) or sphereScaleB > (distanceBetweenPoints / 5):
        sphereScaleA = (distanceBetweenPoints / 5)
        sphereScaleB = (distanceBetweenPoints / 5)

    if sphereScaleA < (distanceBetweenPoints / 30) or sphereScaleB < (distanceBetweenPoints / 30):
        sphereScaleA = (distanceBetweenPoints / 30)
        sphereScaleB = (distanceBetweenPoints / 30)

    sphereA.scale.set(sphereScaleA, sphereScaleA, sphereScaleA)
    sphereB.scale.set(sphereScaleB, sphereScaleB, sphereScaleB)



def createColoredVertexSpheres():

    global vertDict
    global parallelRelationshipDict
    global vertPositionDict
    global selectionIndices

    global rightColoredVertexSpheres
    global leftColoredVertexSpheres
    global lambertA
    global lambertB

    panel = pymel.getPanel(underPointer=True)
    panel = panel.split('|')[-1]
    selection = pymel.ls(selection=True)

    radius = 1

    rightColoredVertexSpheres = []
    leftColoredVertexSpheres = []

    # make lambert for A spheres
    lambertA = pymel.shadingNode('lambert', asShader=True, name='DELETE_ME__TEMP_rightLambert')
    lambertA.addAttr('createColoredVertexSpheres_tempType', dt='string')
    lambertA.color.set( [0,0,0] )
    lambertA.transparency.set( [0.5,0.5,0.5] )
    shadingEngineR = pymel.sets(renderable=True, noSurfaceShader=True, empty=True, name='DELETE_ME__TEMP_rightshadingEngine')
    shadingEngineR.addAttr('createColoredVertexSpheres_tempType', dt='string')
    pymel.connectAttr(lambertA+".outColor", shadingEngineR+".surfaceShader", force=True)

    # make lambert for B spheres
    lambertB = pymel.shadingNode('lambert', asShader=True, name='DELETE_ME__TEMP_rightLambert')
    lambertB.addAttr('createColoredVertexSpheres_tempType', dt='string')
    lambertB.color.set( [0,0,0] )
    lambertB.transparency.set( [0.5,0.5,0.5] )
    shadingEngineL = pymel.sets(renderable=True, noSurfaceShader=True, empty=True, name='DELETE_ME__TEMP_rightshadingEngine')
    shadingEngineL.addAttr('createColoredVertexSpheres_tempType', dt='string')
    pymel.connectAttr(lambertB+".outColor", shadingEngineL+".surfaceShader", force=True)

    isolateState = pymel.isolateSelect(panel, query=True, state=True)
    firstvertexSphereA = None
    firstvertexSphereB = None
    for i, vertIndex in enumerate(parallelRelationshipDict):
        topIndex = parallelRelationshipDict[vertIndex]['top']
        bottomIndex = parallelRelationshipDict[vertIndex]['bottom']
        rightIndex = parallelRelationshipDict[vertIndex]['right']
        leftIndex = parallelRelationshipDict[vertIndex]['left']

        if i == 0:
            vertexSphereA = pymel.sphere(name='DELETE_ME__vertexSpheres', radius=radius, sections=1, spans=2)[0]
            vertexSphereA.overrideEnabled.set(1)
            vertexSphereA.drawOverride.overrideColor.set(2)

            vertexSphereB = pymel.sphere(name='DELETE_ME__vertexSpheres', radius=radius, sections=1, spans=2)[0]
            vertexSphereB.overrideEnabled.set(1)
            vertexSphereB.drawOverride.overrideColor.set(2)
            OOOOOOO = 'leftColoredVertexSpheres';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))

            vertexSphereA.addAttr('createColoredVertexSpheres_tempType', dt='string')
            vertexSphereB.addAttr('createColoredVertexSpheres_tempType', dt='string')

            pymel.sets( shadingEngineR, forceElement=vertexSphereA, )
            pymel.sets( shadingEngineL, forceElement=vertexSphereB, )

            firstvertexSphereA = vertexSphereA
            firstvertexSphereB = vertexSphereB
        else:
            vertexSphereA = pymel.instance(firstvertexSphereA, name='DELETE_ME__vertexSpheres',)[0]
            vertexSphereB = pymel.instance(firstvertexSphereB, name='DELETE_ME__vertexSpheres',)[0]

        rightColoredVertexSpheres.append(vertexSphereA)
        leftColoredVertexSpheres.append(vertexSphereB)

        shapeObj = selection[0].node()
        mel.eval( 'hilite '+shapeObj.name() )
        pymel.select(shapeObj)
        pymel.select(selection)



        #if len(parallelRelationshipDict) == 1:
            #vertRightNeighborPosition = vertPositionDict[rightIndex]
            #vertLeftNeighborPosition = vertPositionDict[leftIndex]
            #vertUpperNeighborPosition = vertPositionDict[topIndex]
            #vertLowerNeighborPosition = vertPositionDict[bottomIndex]
        #else:
            #vertLeftNeighborPosition = vertPositionDict[topIndex]
            #vertRightNeighborPosition = vertPositionDict[bottomIndex]

        #pymel.xform(vertexSphereA, translation=vertRightNeighborPosition, worldSpace=True)
        #pymel.xform(vertexSphereB, translation=vertLeftNeighborPosition, worldSpace=True)

        #setSpherePairScale_fromCameraSpace(vertRightNeighborPosition, vertexSphereA, vertLeftNeighborPosition, vertexSphereB)

        if isolateState:
            pymel.isolateSelect(panel, addDagObject=vertexSphereA)
            pymel.isolateSelect(panel, addDagObject=vertexSphereB)

    pasteWeightsFromNeighbors_positionSpheres()


rightColoredVertexSpheres
def colorVertexSpheres(objectList, color):

    lambert = None
    lambertMatch = pymel.ls(type='lambert')
    if lambertMatch:
        for each in lambertMatch:
            if '_'+color+'_TEMP_lambert' in each.name():
                lambert=each
                break
            elif ':'+color+'_TEMP_lambert' in each.name():
                lambert=each
                break

    if not lambert:
        lambert = pymel.shadingNode('lambert', asShader=True, name='DELETE_ME__TEMP_lambert')
        lambert.addAttr('createColoredVertexSpheres_tempType', dt='string')


    shadingEngine = None
    shadingEngineMatch = pymel.ls(type='shadingEngine')
    if shadingEngineMatch:
        for each in shadingEngineMatch:
            if '_'+color+'_TEMP_shadingEngine' in each.name():
                shadingEngine=each
                break
            elif ':'+color+'_TEMP_shadingEngine' in each.name():
                shadingEngine=each
                break

    if not shadingEngine:
        shadingEngine = pymel.sets(renderable=True, noSurfaceShader=True, empty=True, name='DELETE_ME__TEMP_shadingEngine')
        shadingEngine.addAttr('createColoredVertexSpheres_tempType', dt='string')
        pymel.connectAttr(lambert+".outColor", shadingEngine+".surfaceShader", force=True)


    colorValues = [0, 0, 0]
    if color == 'black': colorValues =          [0, 0, 0]
    if color == 'red': colorValues =            [1, 0, 0]
    if color == 'darkerRed': colorValues =      [0.75, 0, 0]
    if color == 'blue': colorValues =           [0, 0.2, 1]
    if color == 'darkBlue': colorValues =       [0, 0, .25]
    if color == 'lightBlue': colorValues =      [0.25, 0.25, 1]
    if color == 'green': colorValues =          [0, 1, 0]
    if color == 'darkGreen': colorValues =      [0, .45, 0]
    if color == 'lightGreen': colorValues =     [0.25, 1, 0.25]
    if color == 'teal': colorValues =           [0, 1, 1]

    lambert.colorR.set(colorValues[0])
    lambert.colorG.set(colorValues[1])
    lambert.colorB.set(colorValues[2])
    lambert.diffuse.set(1)

    #add color the object this color
    pymel.sets( shadingEngine, forceElement=object, )


def deleteColoredVertexSpheres():
    deleteMeObjects = pymel.ls('DELETE_ME__*')
    deleteList = []

    for each in deleteMeObjects:
        if pymel.attributeQuery('createColoredVertexSpheres_tempType', node=each, exists=True):
            deleteList.append(each)

    if deleteList:
        pymel.delete(deleteList)

def blendColoredVertexSpheres():
    pass

def averageWeights_forIslandInSelection():
    selection = pymel.ls(selection=True, flatten=True)


previousParallelSelection = []
previousDirection = None
def selectParallelVertsDict(selectGroup='top'):
    global previousParallelSelection
    global previousDirection

    mods = pymel.getModifiers()
    perpendicularMode = False
    if (mods & 1) > 0: #Shift is down
       perpendicularMode = True

    oposites = {'top':'bottom', 'bottom':'top', 'right':'left', 'left':'right', }
    parallelVertDict = getParallelVertsDict(perpendicularMode=perpendicularMode)
    previouslySelected = False

    selectList = []
    for key in parallelVertDict:
        vert, vertUpperNeighbor, vertLowerNeighbor, vertRightNeighbor, vertLeftNeighbor = parallelVertDict[key]

        if selectGroup == 'top':
            firstChoice = vertUpperNeighbor
            secondChoice = vertLowerNeighbor

        elif selectGroup == 'bottom':
            firstChoice = vertLowerNeighbor
            secondChoice = vertUpperNeighbor

        elif selectGroup == 'right':
            firstChoice = vertRightNeighbor
            secondChoice = vertLeftNeighbor

        elif selectGroup == 'left':
            firstChoice = vertLeftNeighbor
            secondChoice = vertRightNeighbor

        # has the first choice been selected immediatly before the current one?
        if previousDirection:
            if previousDirection == selectGroup:
                if firstChoice in previousParallelSelection:
                    previouslySelected = True

            #if switching direction
            elif oposites[selectGroup] == previousDirection:
                    if firstChoice not in previousParallelSelection:
                        previouslySelected = True

        # if selecting our first choice would be repeating the last selection, go for the
        # second choice instead. This will keep us pickwalking in a consistant way
        if not previouslySelected:
            selectList.append(firstChoice)
        else:
            selectList.append(secondChoice)


    previousParallelSelection = pymel.ls(selection=True, flatten=True)
    previousDirection = selectGroup
    pymel.select(selectList)


def getMMatrix(object, matrixType='worldMatrix'):
    matrix = pymel.getAttr(object+".%s" % matrixType)
    matrixList = []
    for row in matrix:
        for n in row:
            matrixList.append(n)

    mMatrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList(matrixList, mMatrix)
    return mMatrix

def transformPoint(transformObject, point):

    objMat = getMMatrix(transformObject, matrixType='worldInverseMatrix')
    aPoint = OpenMaya.MPoint(point[0], point[1], point[2])
    result = aPoint * objMat

    return result.x, result.y, result.z

def getInCameraSpace(inputValue):
    camera = getCurrentCamera()
    if isinstance(inputValue, pymel.general.MeshVertex):
        point = inputValue.getPosition(space='world')
    else:
        point = inputValue
    cameraSpacePositionOfPoint = transformPoint(camera, point)
    return cameraSpacePositionOfPoint

def getCurrentCamera():
    panelUnderPointer = pymel.getPanel( underPointer=True )
    camera = 'persp'
    if panelUnderPointer:
        if 'modelPanel' in panelUnderPointer:
            currentPanel = pymel.getPanel(withFocus=True)
            currentPanel = currentPanel.split('|')[-1]
            camera = pymel.modelPanel(currentPanel, query=True, camera=True)

    return camera


def getParallelVertData(perpendicularMode=False):
    '''returns the verts that are parralel (like an edge ring) to the selected verts.
    returns a list of lists with each list being [selectedPoint, aboveSelectedPoint, belowSelectedPoint]'''

    global previousSelection

    selection = pymel.ls(selection=True, flatten=True)

    previousSelection = selection

    if len(selection) == 1:
        getSingleParallelVertDict(selection)
    else:
        getLineParallelVertsDict(selection)

def getSingleParallelVertDict(selection):

    global vertDict
    global parallelRelationshipDict
    global vertPositionDict
    global selectionIndices
    global vertPairSequence

    vertDict = {}    #key=vertIndex, Value=MeshVertex <pymelNode>
    parallelRelationshipDict = {}    #key=vertIndex, Value={upper:upperVertIndex, lower:lowerVertIndex, right:rightVertIndex, left:leftVertIndex}
    vertPositionDict = {}    #key=vertIndex, Value=(worldPositionX, worldPositionY, worldPositionZ)
    selectionIndices = []    #key=vertIndex, Value=MeshVertex <pymelNode>

    faceDict = {}    #key=vertIndex, Value=MeshFace <pymelNode>
    edgeDict = {}    #key=vertIndex, Value=MeshEdge <pymelNode>

    facesOfVertDict = {}    #key=vertIndex, Value=[connectedFaceIndex[0], connectedFaceIndex[1]...]
    vertsOfFaceDict = {}    #key=faceIndex, Value=[connectedVertIndex[0], connectedVertIndex[1]...]

    edgesOfVertDict = {}    #key=edgeIndex, Value=[connectedVertIndex[0], connectedVertIndex[1]...]
    vertsOfEdgeDict = {}    #key=vertIndex, Value=[connectedEdgeIndex[0], connectedEdgeIndex[1]...]

    node = selection[0].node()

    # finds nessisary component relationship data one, to prevent redundancy
    mapComponentRelationships(selection[0], node=node, faceDict=faceDict, edgeDict=edgeDict, facesOfVertDict=facesOfVertDict,
                              vertsOfFaceDict=vertsOfFaceDict,  edgesOfVertDict=edgesOfVertDict, vertsOfEdgeDict=vertsOfEdgeDict,)

    # values we are trying to find
    rightVert = None
    leftVert = None
    topVert = None
    bottomVert = None

    # the ordered pairs of verts that will be availible to blend from
    vertPairSequence = []

    # find the connected Verts
    connectedVerts = []
    for edgeIndex in edgesOfVertDict[selectionIndices[0]]:
        vertIndices = vertsOfEdgeDict[edgeIndex]
        for vertIndex in vertIndices:
            if vertIndex != selectionIndices[0]:
                connectedVerts.append(vertIndex)
    lenOfConnectedPoints = len(connectedVerts)

    # populate the dict that has the worldSpace postion of each vert
    for vertIndex in connectedVerts:
        vertPositionDict[vertIndex] = vertDict[vertIndex].getPosition(space='world')

    # make a dict that has the cameraspace position of each vert
    cameraSpaceDict = {}
    for vertIndex in connectedVerts:
        cameraSpaceDict[vertIndex] = getInCameraSpace(vertPositionDict[vertIndex])

    # Find Right
    rightVert = connectedVerts[0]
    for vertIndex in connectedVerts:
        if cameraSpaceDict[vertIndex][0] < cameraSpaceDict[rightVert][0]:
            rightVert = vertIndex


    # if there are more than 4 connected points
    if lenOfConnectedPoints > 4:
        orderedPoints = [rightVert]

        count = 0
        while len(orderedPoints) != len(connectedVerts):

            for faceIndex in facesOfVertDict[orderedPoints[-1]]:
                for vertIndex in vertsOfFaceDict[faceIndex]:
                    if vertIndex in connectedVerts:
                        if vertIndex not in orderedPoints:
                            orderedPoints.append(vertIndex)
                            break
                            break

            count += 1
            if count > 9000:
                OOOOOOO = 'orderedPoints';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
                pymel.error('way to big son')


        vertPairSequence = []
        # populate vertPairSequence
        for iA, indexA in enumerate(orderedPoints):
            for iB, indexB in enumerate(orderedPoints):
                if not iA == iB:
                    vertPairSequence.append([(orderedPoints[iA], orderedPoints[iB])])

        OOOOOOO = 'vertPairSequence';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
        OOOOOOO = 'orderedPoints';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
        OOOOOOO = 'connectedVerts';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))

    # if there are exactly 4 connected points
    elif lenOfConnectedPoints == 4:

        # Find Left
        facesConnectedToRight = facesOfVertDict[rightVert]
        possibleLeftVerts = []
        for vertIndex in connectedVerts:
            if vertIndex != rightVert:
                connectedFaces = facesOfVertDict[vertIndex]
                connectedToRight = False
                for faceIndex in connectedFaces:
                    if faceIndex in facesConnectedToRight:
                        connectedToRight = True
                        break
                if not connectedToRight:
                    possibleLeftVerts.append(vertIndex)

        leftVert = possibleLeftVerts[0]
        for vertIndex in possibleLeftVerts:
            if cameraSpaceDict[vertIndex][0] < cameraSpaceDict[leftVert][0]:
                leftVert = int(vertIndex)

        # Find Top
        possibleTopVerts = []
        for vertIndex in connectedVerts:
            if vertIndex not in [rightVert, leftVert]:
                possibleTopVerts.append(vertIndex)

        topVert = possibleTopVerts[0]
        for vertIndex in possibleTopVerts:
            if cameraSpaceDict[vertIndex][1] > cameraSpaceDict[topVert][1]:
                topVert = int(vertIndex)

        # Find Bottom
        possibleBottomVerts = []
        for vertIndex in connectedVerts:
            if vertIndex not in [rightVert, leftVert, topVert]:
                possibleBottomVerts.append(vertIndex)

        bottomVert = possibleBottomVerts[0]
        for vertIndex in possibleBottomVerts:
            if cameraSpaceDict[vertIndex][1] <= cameraSpaceDict[bottomVert][1]:
                bottomVert = int(vertIndex)

        # populate vertPairSequence
        vertPairSequence = [[(leftVert, rightVert)], [(topVert, bottomVert)],]


    # if there exactly 3 connected points
    elif lenOfConnectedPoints == 3:
        # Find Left
        possibleLeftVerts = []
        for vertIndex in connectedVerts:
            if vertIndex != rightVert:
                possibleLeftVerts.append(vertIndex)

        leftVert = possibleLeftVerts[0]
        for vertIndex in possibleLeftVerts:
            if cameraSpaceDict[vertIndex][0] <= cameraSpaceDict[leftVert][0]:
                leftVert = vertIndex

        # Find Top
        possibleTopVerts = []
        for vertIndex in connectedVerts:
            possibleTopVerts.append(vertIndex)

        topVert = possibleTopVerts[0]
        for vertIndex in possibleTopVerts:
            if cameraSpaceDict[vertIndex][1] >= cameraSpaceDict[topVert][1]:
                topVert = vertIndex

        # Find Bottom
        possibleBottomVerts = []
        for vertIndex in connectedVerts:
            if vertIndex != topVert:
                possibleBottomVerts.append(vertIndex)

        bottomVert = possibleBottomVerts[0]
        for vertIndex in possibleBottomVerts:
            if cameraSpaceDict[vertIndex][1] <= cameraSpaceDict[bottomVert][1]:
                bottomVert = vertIndex

        for vertIndex in possibleLeftVerts:
            if vertIndex != rightVert and vertIndex != leftVert:
                thirdVert = vertIndex
                break

        # populate vertPairSequence
        vertPairSequence = [[(leftVert, rightVert)], [(leftVert, thirdVert)], [(thirdVert, rightVert)], ]


    # if there exactly 2 connected points
    elif lenOfConnectedPoints == 2:
        # Find Left
        for vertIndex in connectedVerts:
            if vertIndex != rightVert:
                leftVert = vertIndex

        # Find Top
        topVert = connectedVerts[0]
        for vertIndex in connectedVerts:
            if cameraSpaceDict[vertIndex][1] >= cameraSpaceDict[topVert][1]:
                topVert = vertIndex

        # Find Bottom
        for vertIndex in connectedVerts:
            if vertIndex != topVert:
                bottomVert = vertIndex

        vertPairSequence = [[(leftVert, rightVert)]]


    else:
        pymel.error('how did you manage to find a point with 0 connected edges?!')



    parallelVertDict = {
        'top' :topVert,
        'bottom' :bottomVert,
        'right' :rightVert,
        'left'  :leftVert,
        }

    if topVert:
        rangeOfX = abs(cameraSpaceDict[topVert][0] - cameraSpaceDict[bottomVert][0])
        rangeOfY = abs(cameraSpaceDict[topVert][1] - cameraSpaceDict[bottomVert][1])
        if rangeOfX > rangeOfY:
            parallelVertDict['top'] = bottomVert
            parallelVertDict['bottom'] = topVert

    parallelRelationshipDict[selectionIndices[0]] = parallelVertDict


def getLineParallelVertsDict(selection):
    '''returns the verts that are parralel (like an edge ring) to the selected line of verts.
    '''

    global vertDict
    global parallelRelationshipDict
    global vertPositionDict
    global selectionIndices
    global vertPairSequence

    vertDict = {}    #key=vertIndex, Value=MeshVertex <pymelNode>
    parallelRelationshipDict = {}    #key=vertIndex, Value={upper:upperVertIndex, lower:lowerVertIndex, right:rightVertIndex, left:leftVertIndex}
    vertPositionDict = {}    #key=vertIndex, Value=(worldPositionX, worldPositionY, worldPositionZ)
    selectionIndices = []    #key=vertIndex, Value=MeshVertex <pymelNode>

    faceDict = {}    #key=vertIndex, Value=MeshFace <pymelNode>
    facesOfVertDict = {}    #key=vertIndex, Value=[connectedFaceIndex[0], connectedFaceIndex[1]...]
    vertsOfFaceDict = {}    #key=faceIndex, Value=[connectedVertIndex[0], connectedVertIndex[1]...]

    node = selection[0].node()

    for eachVert in selection:
        mapComponentRelationships(eachVert, node=node, faceDict=faceDict, facesOfVertDict=facesOfVertDict, vertsOfFaceDict=vertsOfFaceDict)

    # find an end point to use as a starting point
    endPoint = None
    for vertIndex in selectionIndices:

        connectedSelectionVerts = []
        for connectedFaceIndex in facesOfVertDict[vertIndex]:
            for connectedVertIndex in vertsOfFaceDict[connectedFaceIndex]:
                if connectedVertIndex != vertIndex:
                    if connectedVertIndex in selectionIndices:
                        if connectedVertIndex not in connectedSelectionVerts:
                            connectedSelectionVerts.append(connectedVertIndex)

        if len(connectedSelectionVerts) == 1:
            endPoint = vertIndex
            break

    if not endPoint: # selectin is continus loop
        endPoint = vertIndex

    # get ordered Selection
    orderedSelection = [endPoint]
    selectionStack = [endPoint]
    while selectionStack:
        selectionVertIndex = selectionStack.pop(0)
        selectionVert = vertDict[selectionVertIndex]

        for faceIndex in facesOfVertDict[selectionVertIndex]:
            vertIndices = vertsOfFaceDict[faceIndex]
            for vertIndex in vertIndices:
                if vertIndex != selectionVertIndex:
                    if vertIndex in selectionIndices:
                        if vertIndex not in orderedSelection:
                            orderedSelection.append(vertIndex)
                            selectionStack.append(vertIndex)
                            break
            if selectionStack:
                break

    last = len(orderedSelection)-1
    parallelSetA = []
    parallelSetB = []
    for i, vertIndex in enumerate(orderedSelection):

        requiredMatches = 2
        if i == last:
            matchIndices = [vertIndex, orderedSelection[i-1]]
        else:
            matchIndices = [vertIndex, orderedSelection[i+1]]


        # find connected faces who contain both the matchIndices
        matchingFaces = []
        faceIndices = facesOfVertDict[vertIndex]
        for faceIndex in faceIndices:

            faceVertIndices = vertsOfFaceDict[faceIndex]
            matchingFacePoints = 0
            for faceVertIndex in faceVertIndices:
                if faceVertIndex in matchIndices:
                    matchingFacePoints += 1

            if matchingFacePoints == requiredMatches:
                matchingFaces.append(faceIndex)

        for matchingFaceIndex in matchingFaces:
            facePoints = vertsOfFaceDict[matchingFaceIndex]
            lenOfFacePoints = len(facePoints)
            indexOfSelf = facePoints.index(vertIndex)

            if facePoints[indexOfSelf-1] == matchIndices[1]:
                if indexOfSelf+1 == lenOfFacePoints:
                    parallelVertIndex = facePoints[0]
                else:
                    parallelVertIndex = facePoints[indexOfSelf+1]
            else:
                parallelVertIndex = facePoints[indexOfSelf-1]

            if not parallelSetA: # if first item
                parallelSetA.append(parallelVertIndex)

            else:
                isConnectedToA = False

                # is the parallel vert connected to the last point in parallelSetA?
                for connectedFaceIndex in facesOfVertDict[parallelVertIndex]:
                    for connectedFaceVertexIndex in vertsOfFaceDict[connectedFaceIndex]:
                        if connectedFaceVertexIndex == parallelSetA[-1]:
                            parallelSetA.append(parallelVertIndex)
                            isConnectedToA = True
                            break
                    if isConnectedToA:
                        break

                if not isConnectedToA:
                    parallelSetB.append(parallelVertIndex)

    # determin which is top and which is bottom of the parallel sets
    for vertIndex in parallelSetA+parallelSetB:
        vertPositionDict[vertIndex] = vertDict[vertIndex].getPosition(space='world')

    parallelSetA_xSum = 0
    parallelSetA_ySum = 0
    parallelSetB_xSum = 0
    parallelSetB_ySum = 0

    for vertIndex in parallelSetA:
        x, y, z = getInCameraSpace(vertPositionDict[vertIndex])
        parallelSetA_xSum += x
        parallelSetA_ySum += y

    for vertIndex in parallelSetB:
        x, y, z = getInCameraSpace(vertPositionDict[vertIndex])
        parallelSetB_xSum += x
        parallelSetB_ySum += y

    rangeOfX = abs(parallelSetA_ySum - parallelSetB_ySum)
    rangeOfY = abs(parallelSetA_xSum - parallelSetB_xSum)

    verticalHorizontal = 'vertical'
    if rangeOfX > rangeOfY:
        verticalHorizontal = 'horizontal'

    if verticalHorizontal == 'vertical':
        if parallelSetA_xSum > parallelSetB_xSum:
            topVerts = parallelSetA
            bottomVerts = parallelSetB
        else:
            topVerts = parallelSetB
            bottomVerts = parallelSetA

    elif verticalHorizontal == 'horizontal':
        if parallelSetA_ySum > parallelSetB_ySum:
            topVerts = parallelSetA
            bottomVerts = parallelSetB

        else:
            topVerts = parallelSetB
            bottomVerts = parallelSetA

    vertPairSequence = []
    vertPairSequenceA = []
    for i, vertIndex in enumerate(orderedSelection):
        vertPairSequenceA.append((bottomVerts[i], topVerts[i]))
        parallelVertDict = {
        'top' :topVerts[i],
        'bottom' :bottomVerts[i],
        'right' :topVerts[i],
        'left'  :bottomVerts[i],
        }

        parallelRelationshipDict[vertIndex] = parallelVertDict
    vertPairSequence.append(vertPairSequenceA)

def mapComponentRelationships(vert, node=None, faceDict=None, edgeDict=None, facesOfVertDict=None,
                              vertsOfFaceDict=None, edgesOfVertDict=None, vertsOfEdgeDict=None,):
    global vertDict
    global selectionIndices

    vertIndex = vert.currentItemIndex()
    if not node:
        node = vert.node()

    selectionIndices.append(vertIndex)
    if vertIndex not in vertDict:
        vertDict[vertIndex] = vert

    # map connected faces
    if facesOfVertDict != None:
        connectedFaces = vert.connectedFaces()
        for connectedFace in connectedFaces:
            faceIndex = connectedFace.currentItemIndex()

            if faceIndex not in vertsOfFaceDict:
                connectedVertIndices = connectedFace.getVertices()

                vertsOfFaceDict[faceIndex] = []
                for connectedVertIndex in connectedVertIndices:

                    # add to vertsOfFaceDict
                    vertsOfFaceDict[faceIndex].append(connectedVertIndex)

                    # add to facesOfVertDict
                    if connectedVertIndex not in facesOfVertDict:
                        facesOfVertDict[connectedVertIndex] = [faceIndex]

                    if faceIndex not in facesOfVertDict[connectedVertIndex]:
                        facesOfVertDict[connectedVertIndex].append(faceIndex)

                    # add to vertDict
                    if connectedVertIndex not in vertDict:
                        vertDict[connectedVertIndex] = node.vtx[connectedVertIndex]

                # add to faceDict
                if faceIndex not in faceDict:
                    faceDict[faceIndex] = connectedFace

    # map connected edges
    if edgesOfVertDict != None:
        connectedEdges = vert.connectedEdges()
        for connectedEdge in connectedEdges:
            edgeIndex = connectedEdge.currentItemIndex()
            #if edgeIndex not in facesOfVertDict:

            connectedVertIndices = []
            for vertex in connectedEdge.connectedVertices():
                vertIndex = vertex.currentItemIndex()
                connectedVertIndices.append(vertIndex)

                # add to vertDict
                if vertIndex not in vertDict:
                    vertDict[vertIndex] = vertex

            vertsOfEdgeDict[edgeIndex] = []
            for connectedVertIndex in connectedVertIndices:

                # add to vertsOfEdgeDict
                vertsOfEdgeDict[edgeIndex].append(connectedVertIndex)

                # add to edgesOfVertDict
                if connectedVertIndex not in edgesOfVertDict:
                    edgesOfVertDict[connectedVertIndex] = [edgeIndex]

                if edgeIndex not in edgesOfVertDict[connectedVertIndex]:
                    edgesOfVertDict[connectedVertIndex].append(edgeIndex)

            # add to edgeDict
            if edgeIndex not in edgeDict:
                edgeDict[edgeIndex] = connectedEdge


def pasteSkinWeights_fromStrandStartToEnd(verts=None):

    if not verts:
        verts = pymel.ls(selection=True, flatten=True)

    strandStart = None
    strandEnd = None
    strandRelationDict = {}
    vertStrand = []

    for vert in verts:
        connectedVerts = []

        for connectedVert in vert.connectedVertices():
            if connectedVert in verts:
                connectedVerts.append(connectedVert)

        lenOfconnectedVerts = len(connectedVerts)
        if lenOfconnectedVerts > 1:
            pass

        elif lenOfconnectedVerts == 1:
            if not strandStart:
                strandStart = vert

            else:
                strandEnd = vert

        else:
            pymel.error('strand is incomplete')

        strandRelationDict[vert] = connectedVerts

    currentVert = strandStart
    previousVert = None
    for i, each, in enumerate(verts):
        vertStrand.append(currentVert)
        if currentVert != strandEnd:
            for connectedVert in strandRelationDict[currentVert]:
                if connectedVert != previousVert:
                    previousVert = currentVert
                    currentVert = connectedVert
                    break

    copySkinWeights(verts=[strandEnd, strandStart])

    ratioSegments = 200.0/(len(vertStrand)-1.0)
    for i, vert in enumerate(vertStrand):
        print('ratioSegments*i:', end=' ')
        print(ratioSegments*i)
        pasteSkinWeights(verts=[vert], weightedAverage=(ratioSegments*i))



def xferSkin(sourceObject="", targetObjects=""):
    selectedObjects = pymel.ls(selection=True, int=True)
    if len(selectedObjects) < 2:
        pymel.error("must be at least 2 skinnable objects selected")

    if sourceObject == "":
        sourceObject = selectedObjects[0]

    if targetObjects == "":
        targetObjects = selectedObjects[1:]

    sourceSkinClusterNode = findRelatedSkinCluster(sourceObject)
    sourceSkinInfluenceList = getInfluences(sourceObject)

    for each in targetObjects:
        pymel.select(sourceSkinInfluenceList)
        pymel.select(each, add=True)

        targetSkinClusterNode = pymel.skinCluster(maximumInfluences=5, obeyMaxInfluences=True, removeUnusedInfluence=False, toSelectedBones=True)
#        targetSkinClusterNode = findRelatedSkinCluster(each)
        print('targetSkinClusterNode:', end=' ')
        print(targetSkinClusterNode)

        pymel.copySkinWeights( sourceSkin=sourceSkinClusterNode, destinationSkin=targetSkinClusterNode, noMirror=True, influenceAssociation = 'oneToOne', surfaceAssociation = 'closestPoint')

    pymel.select(targetObjects, replace=True)

def xferComponentWeights_fromStoredSelection():
    targetComponents = pymel.ls(selection=True, int=True)
    selectedObjects = ka_selection.getStoredSelection()
    xferComponentWeights(selectedObjects[0], targetComponents)


def xferComponentWeights(sourceObject=None, targetComponents=None):
    """selection A should be a point set, and it will transfer its weights to the nearest point for
    all other selected verts"""

    selectedObjects = pymel.ls(selection=True, int=True)

    if not sourceObject:
        sourceObject = selectedObjects[0].node()

    sourceSkinClusterNode = findRelatedSkinCluster(sourceObject)
    sourceSkinInfluenceList = getInfluences(sourceObject)

    destinationObjects = []
    sourceComponents = []
    targetComponents = []

    for each in selectedObjects:
        if each.node() == sourceObject:
            sourceComponents.append(each)

        else:
            if each.node() not in destinationObjects:
                destinationObjects.append(each.node())
            targetComponents.append(each)


    #find all influences that are in one skin, but not the other
    for destinationObject in destinationObjects:
        destinationSkinClusterNode = findRelatedSkinCluster(destinationObject)
        destinationSkinInfluenceList = getInfluences(destinationObject)

        missingInfuences = []
        for influence in sourceSkinInfluenceList:
            if influence not in destinationSkinInfluenceList:
                missingInfuences.append(influence)

        pymel.skinCluster(destinationSkinClusterNode, edit=True, addInfluence=missingInfuences, weight=0.0)


    #oneToOne
    for destinationObject in destinationObjects:
        pymel.select(clear=True)
        pymel.select(destinationObject, add=True)
        mel.eval('changeSelectMode -component;')
        mel.eval('setComponentPickMask "Point" true;')
        pymel.select(targetComponents, add=True)
        pymel.select(sourceObject, add=True)
        pymel.select(targetComponents, add=True)

        pymel.copySkinWeights(noMirror=True, surfaceAssociation='closestPoint', influenceAssociation=['label', 'closestBone', 'closestJoint',] )

    pymel.select(selectedObjects)
    mel.eval('changeSelectMode -component;')
    mel.eval('setComponentPickMask "Point" true;')

def _pruneSmallWeights(skinCluster, pruneMax, **kwArgs):
    verbose = kwArgs.get('verbose', False)
    influences = self.getSkinInfluences(self.mesh)
    lenOfInfluences = str(len(influences))

    #get point weights
    cmdGetString = 'cmds.getAttr(".weightList['+i+'].weights[0:'+lenOfInfluences+']")'
    values = cmds.getAttr('.weightList['+i+'].weights[0:'+lenOfInfluences+']')

def pruneSmallWeights(**kwArgs):
    kwArgs['verbose'] = True
    selection = pymel.ls(selection=True)

    for geo in selection:
        skinCluster = findRelatedSkinCluster(geo, silent=True)
        if skinCluster:
            _pruneSmallWeights(skinCluster, 0.0001 **kwArgs)


#UTILITYS#############################################################################################################################################################################
def findRelatedSkinCluster(*args, **kwArgs):
    '''return the skinCluster for the input, which will be a user selection'''
    return ka_skinCluster.findRelatedSkinCluster(*args, **kwArgs)

def getInfluences(*args, **kwArgs):
    '''return the influences attached to the skinCluster'''
    return ka_skinCluster.getInfluences(*args, **kwArgs)


def deleteAllBindPoses():
    pass

def refreshMayaPaintUI():
    mel.eval('refreshAE')
    mel.eval('artAttrSkinToolScript 4')
    mel.eval('artAttrSkinPaintCtx -e -showactive true `currentCtx`;')

def applyJointColors():
    selection = pymel.ls(selection=True, flatten=True)
    influenceList = getInfluences()
    skinCluster = findRelatedSkinCluster(selection[0])

    locked = []
    unlocked = []

    for each in influenceList:
        if pymel.getAttr(each+'.lockInfluenceWeights'):
            #pymel.color( each, userDefined=8 )
            locked.append(each)
        else:
            unlocked.append(each)

    if locked:
        pymel.color( locked, userDefined=8 )
    if unlocked:
        pymel.color( unlocked, userDefined=7 )


def createSkinCluster():
    pymel.skinCluster(obeyMaxInfluences=False, maximumInfluences=5, toSelectedBones=True, ignoreHierarchy=False, skinMethod=0, normalizeWeights=1, removeUnusedInfluence=False)

def addInfluence():
    selection = pymel.ls(selection=True)

    skinClusters = []
    influencesToAdd = []
    for item in selection:
        skinCluster = findRelatedSkinCluster(item)
        if skinCluster:
            if skinCluster not in skinClusters:
                skinClusters.append(skinCluster)

        else:
            if item.nodeType() == 'joint':
                influencesToAdd.append(item)

    for skinCluster in skinClusters:
        for influence in influencesToAdd:
            skinClusterInfluences = getInfluences(skinCluster)
            if influence not in skinClusterInfluences:
                pymel.skinCluster(skinCluster, edit=True, addInfluence=influence, useGeometry=False, lockWeights=True, dropoffRate=4.0, weight=0.0)
