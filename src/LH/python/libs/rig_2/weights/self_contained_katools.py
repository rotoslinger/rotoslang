

# import time

import maya.cmds as cmds
import pymel.core as pymel
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import math
import traceback
import maya.api.OpenMaya as om2


# import ka_rigTools.ka_math as ka_math #;reload(ka_math)
# import ka_rigTools.ka_python as ka_python #;reload(ka_python)
# import ka_rigTools.ka_preference as ka_preference #;reload(ka_preference)
# import ka_rigTools.ka_skinCluster as ka_skinCluster #;reload(ka_skinCluster)


def printError():
    print('\nSCRIPT STACK------------------------------------------')
    traceback.print_stack()

    print('ERROR ------------------------------------------------')
    traceback.print_exc()
    print('\n')


def dotProduct(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def distanceBetween(pointA, pointB):
    '''returns distance between a list of 2d or 3d coordinates'''
    sum = 0
    for i, each in enumerate(pointA):
        sum += (pointA[i] - pointB[i])**2

    return math.sqrt( sum )



class WeightBlenderInfo(object):

    def __init__(self, components=None):

        self.selection = components
        self.selectedNodes = []

        # sequence info
        self.currentSequence = 0
        self.lastSequence = -1

        # point info
        self.pntDict = {}    # populated by _getComponentID
        self.selectedPointIDs = {}
        self.pnt_typeDict = {}    # populated by _getNode method
        self.pnt_worldSpacePostionDict = {}
        self.pnt_cameraSpacePostionDict = {}
        self.pnt_complexIndexDict = {}    # may be represented by multiple numbers ie: nurbs / lattice
        self.pnt_simpleIndexDict = {}    # corrispnds to components index in the skin cluster

        # node info
        self.nodeOfpointDict = {}    # populated by _getNode method
        self.pointsInNodesDict = {}

        ## other componentInfo
        self.faceDict = {}
        self.edgeDict = {}

        self.pointsOfFace = {}
        self.pointsOfEdge = {}

        self.facesOfPoint = {}
        self.facesOfEdge = {}

        self.edgesOfPoint = {}
        self.edgesOfFace = {}
        self.edgesOfFace = {}

        # mesh relationship Dicts
        self.connectedPointsDict = {}

        # strand info
        # self.strandTargetSequencesA/B_dict:
        #     A dictionary (key=pointID, value=List of lists) the value is a list of possible combinations of blend targets
        #     that can be selected from, and each of those combinations may be one or more points. If blending to multiple points
        #     you will infact be blending to the average of their weights.
        self.strandTargetSequencesA_dict = {}
        self.strandTargetSequencesB_dict = {}


        # other info
        self.currentCamera = getCurrentCamera()
        self.currentCameraMMatrix = getMMatrix(self.currentCamera, matrixType='worldInverseMatrix')

        # target icons
        self.deleteTargetIcons()

        self.iconPointsA = {}
        self.iconPointsB = {}

        self.targetIconsA = []
        self.targetIconsB = []

        self.targetIconsShaderA = None    # (lambertA, shadingEngineA)
        self.targetIconsShaderB = None    # (lambertB, shadingEngineB)
        self.lambertAIsBlack = True
        self.lambertBIsBlack = True

        # weight info
        self.weightDict = {}                # (key=pointID, value=dictionary (key=influenceIndex, value=weightValue))
        self.skinClusterDict = {}           # (key=node, value=skinCluster)
        self.influenceDict = {}             # (key=skinCluster, value=listOfInfluences)
        self.influenceArrayIndexDict = {}   # (key=skinCluster, value=dict(key=influence, value=arrayIndex))

        # targetA/B WeightDict contains the pre averaged weights of the targetsA and B for given selected points
        # (as a point may have multiple targetsA or B)
        self.targetAWeightDict = {}    # (key=pointID(of original point, not target), value=dictionary (key=influenceIndex, value=weightValue))
        self.targetBWeightDict = {}    # (key=pointID(of original point, not target), value=dictionary (key=influenceIndex, value=weightValue))



        if not self.selection:
            self.selection = pymel.ls(selection=True, flatten=True)

        if not self.selection:
            print("Error: nothing selected")
            # cmds.error('## WeightBlender Failure, no valid points selected')


        # populate info dictionaries
        for i, point in enumerate(self.selection):
            # basic info
            pointID = self._getComponentID(point)
            node = self._getNode(pointID)

            self.selectedPointIDs[pointID] = point

            self.nodeOfpointDict[pointID] = node
            if node not in self.pointsInNodesDict:
                self.pointsInNodesDict[node] = [pointID]
            else:
                self.pointsInNodesDict[node].append(pointID)

            # worldSpace dict
            self._getWorldSpacePosition(pointID)

            # cameraSpace dict
            self._getCameraSpacePosition(pointID)

            # connected points dict
            self._getConnectedPoints(pointID)


        # get list of point strands with each strand ordered from camera left to right
        self.strands = []
        pointIdStack = list(self.selectedPointIDs)
        while pointIdStack:
            pointID = pointIdStack.pop()

            strand = [pointID]
            strandPointIDStack = [pointID]
            while strandPointIDStack:
                strandPointID = strandPointIDStack.pop()

                connectedPointsFound = 0
                connectedPoints = []
                for connectedPointID in self.connectedPointsDict[strandPointID]:
                    if connectedPointID in self.selectedPointIDs:
                        connectedPointsFound += 1
                        if connectedPointsFound == 3:
                            cmds.error('Selection is invalid. Selections can either be unconnected points, or points connected in strands')

                        if connectedPointID not in strand:
                            connectedPoints.append(connectedPointID)

                for connectedPointID in connectedPoints:

                    if connectedPointID in pointIdStack:
                        connectedPoint = pointIdStack.remove(connectedPointID) # remove from main stack

                    # should point be added to start or end of the strand
                    if len(strand) == 1: # second point in strand
                        direction = 1

                    else:
                        if strand[-1] in self.connectedPointsDict[connectedPointID]:
                            direction = 1
                        else:
                            direction = -1

                    # add to strand
                    if direction == 1:
                        strand.append(connectedPointID)
                        strandPointIDStack.append(connectedPointID)

                    else:
                        strand.insert(0, connectedPointID)
                        strandPointIDStack.insert(0, connectedPointID)

            # make sure the strand is ordered camera left to right
            self.firstPoint_cameraSpaceX = self.pnt_cameraSpacePostionDict[strand[0]][0]
            self.lastPoint_cameraSpaceX = self.pnt_cameraSpacePostionDict[strand[-1]][0]

            if self.firstPoint_cameraSpaceX > self.lastPoint_cameraSpaceX:
                strand.reverse()
            self.strands.append(strand)


        # gather possible variations of target combinations, so we can form a list
        # from that
        for i, strand in enumerate(self.strands):

            # Single point
            if len(strand) == 1:
                pointID = strand[0]
                if self.pnt_typeDict[strand[0]] == 'mesh':
                    orderedVertTargets = self._orderConnectedVertsClockwise(pointID)

                self.strandTargetSequencesA_dict[pointID] = []
                self.strandTargetSequencesB_dict[pointID] = []

                listA = self.strandTargetSequencesA_dict[pointID]
                listB = self.strandTargetSequencesB_dict[pointID]

                leftMostPoint = orderedVertTargets[0]
                for iA, orderedVertTarget in enumerate(orderedVertTargets):
                    for iB, orderedVertTarget in enumerate(orderedVertTargets):
                        if iB != 0:
                            if iA != iB:
                                listA.append([orderedVertTargets[iA]])
                                listB.append([orderedVertTargets[iB]])
                                self.lastSequence += 1

                    if self.pnt_cameraSpacePostionDict[orderedVertTargets[iA]][0] < self.pnt_cameraSpacePostionDict[leftMostPoint][0]:
                        leftMostPoint = orderedVertTargets[iA]

                rightMostPoint = self._getMostParallelPoint(pointID, leftMostPoint, orderedVertTargets)
                leftAndRightPoints = [leftMostPoint, rightMostPoint]

                upperMostPoint = None
                for orderedVertTarget in orderedVertTargets:
                    if orderedVertTarget not in leftAndRightPoints:
                        if not upperMostPoint:
                            upperMostPoint = orderedVertTarget

                        elif self.pnt_cameraSpacePostionDict[orderedVertTarget][1] > self.pnt_cameraSpacePostionDict[upperMostPoint][1]:
                            upperMostPoint = orderedVertTarget

                lowerMostPoint = self._getMostParallelPoint(pointID, upperMostPoint, orderedVertTargets, [upperMostPoint, rightMostPoint, leftMostPoint])

                if upperMostPoint and lowerMostPoint:
                    listA.insert(0, [upperMostPoint])
                    listB.insert(0, [lowerMostPoint])

                if rightMostPoint and leftMostPoint:
                    listA.insert(0, [leftMostPoint])
                    listB.insert(0, [rightMostPoint])

            # Multi Point
            else:
                if self.pnt_typeDict[strand[0]] == 'mesh':
                    strandTargetsA, strandTargetsB = self._getVertStrandTargets(strand)
                    # print('goob')
                    # OOOOOOO = 'strandTargetsA';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
                    # OOOOOOO = 'strandTargetsB';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
                    for i, pointID in enumerate(strand):
                        # OOOOOOO = 'i';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
                        self.strandTargetSequencesA_dict[pointID] = [strandTargetsA[i]]
                        self.strandTargetSequencesB_dict[pointID] = [strandTargetsB[i]]

        self.iconPointsA = {}
        self.iconPointsB = {}

        # populate iconPointsA&B list, this list eliminates having 2 icons for points used multiple times
        for pointID in self.selectedPointIDs:
            targetsSequenceA = self.strandTargetSequencesA_dict[pointID][self.currentSequence]
            for targetA in targetsSequenceA:
                    self.iconPointsA[targetA] = None

            targetsSequenceB = self.strandTargetSequencesB_dict[pointID][self.currentSequence]
            for targetB in targetsSequenceB:
                    self.iconPointsB[targetB] = None

    def start(self, createTargetIcons=True):
        if createTargetIcons:
            self.createTargetIcons()
        self.storeWeights()



    def averageWithBothNeighbors(self):
        #self.targetAWeightDict = {}    # (key=pointID(of original point, not target), value=dictionary (key=influenceIndex, value=weightValue))


        for i, pointID in enumerate(self.selectedPointIDs):
            originalWeightDict = self.weightDict[pointID]
            targetWeightA = self.targetAWeightDict[pointID]
            targetWeightB = self.targetBWeightDict[pointID]

            finalWeightDict = {}

            for influenceIndex in originalWeightDict:
                finalWeightDict[influenceIndex] = None

            for influenceIndex in targetWeightA:
                finalWeightDict[influenceIndex] = None

            for influenceIndex in targetWeightB:
                finalWeightDict[influenceIndex] = None

            for influenceIndex in finalWeightDict:
                weightOrig = originalWeightDict.get(influenceIndex, 0.0)
                weightA = targetWeightA.get(influenceIndex, 0.0)
                weightB = targetWeightB.get(influenceIndex, 0.0)

                value = ((weightOrig+weightA+weightB) / 3.0)

                finalWeightDict[influenceIndex] = value


            #skinCluster = self.skinClusterDict[self.nodeOfpointDict[pointID]]
            #skinPercentTupleList = []
            #for influenceIndex in finalWeightDict:
                #skinPercentTupleList.append((self.influenceDict[skinCluster][influenceIndex], finalWeightDict[influenceIndex]))

            self._applyWeights(pointID, finalWeightDict)

    def blend(self, blend=100):
        """main function, usually called by a change in a slider value (so potentially called often in succession)

        kwargs:
            percent - int 0-200 - a value representing the value to blend. if 100, then the weights will be the same as
                                  they started, if they are 0, then they will be 100% blended to targetA, if the value
                                  is 200, then the value will be blended 100% to targetB.
        """
        # print("AHHHHHHHHHHHHHH")

        # for key, value in self.weightDict.items():
        #     print("AHHHHHHHHHHHHHH")
        #     print(str(key) + "->" + str(value))
        # self.strands
        # print(self.strands[-1])
        strand0 = self.pnt_cameraSpacePostionDict

        # self.firstPoint_cameraSpaceX = self.pnt_cameraSpacePostionDict[strand[0]][0]
        # self.lastPoint_cameraSpaceX = self.pnt_cameraSpacePostionDict[strand[-1]][0]

        # if self.firstPoint_cameraSpaceX > self.lastPoint_cameraSpaceX:
        # strand.reverse()
        # x for x in self.strands if x == 0
        # print(strand0)
        # print(self.strands)


        ''' 
        x = [p[0] for p in self.strands[0]]
        y = [p[1] for p in self.strands[0]]
        z = [p[2] for p in self.strands[0]]

        centroid = (sum(x) / len(self.strands[0]), sum(y) / len(self.strands[0]), sum(z) / len(self.strands[0]))
        '''


        # firstPoint_cameraSpaceX = self.pnt_cameraSpacePostionDict[self.strands[0]][0]
        # lastPoint_cameraSpaceX = self.pnt_cameraSpacePostionDict[self.strands[-1]][0]

        # if firstPoint_cameraSpaceX > lastPoint_cameraSpaceX:
        #     self.strands.reverse()
        # print(self.firstPoint_cameraSpaceX)

        #### you need to get a list of point positions at rest 


        if self.firstPoint_cameraSpaceX > self.lastPoint_cameraSpaceX:
            self.strands.reverse()


        for i, pointID in enumerate(self.selectedPointIDs):
            
            originalWeightDict = self.weightDict[pointID]
            targetWeightA = self.targetAWeightDict[pointID]
            targetWeightB = self.targetBWeightDict[pointID]

            if not targetWeightA:
                targetWeightA = originalWeightDict

            if not targetWeightB:
                targetWeightB = originalWeightDict


            targetWeightDict = None
            finalWeightDict = {}

            if blend < 100:
                percent = (100 - blend)
                targetWeightDict = targetWeightA

            elif blend > 100:
                percent = (blend - 100)
                targetWeightDict = targetWeightB

            else: # is at 100, ie: inital position, with no blending
                finalWeightDict = originalWeightDict

            if targetWeightDict:
                finalWeightDict = self._getWeightedAveragedWeights(originalWeightDict, targetWeightDict, weightValue=percent)

            #skinCluster = self.skinClusterDict[self.nodeOfpointDict[pointID]]
            #skinPercentTupleList = []
            #for influenceIndex in finalWeightDict:
                #skinPercentTupleList.append((self.influenceDict[skinCluster][influenceIndex], finalWeightDict[influenceIndex]))

            self._applyWeights(pointID, finalWeightDict)



        ###########################
        # color Spheres
        if blend < 100:
            if blend == 0: self.targetIconsShaderA[0].incandescence.set( [ 1, 1, 1 ] )
            else:            self.targetIconsShaderA[0].incandescence.set( [ percent*0.01, 0.25+(percent*0.0075), percent*0.0015 ] )
            self.lambertAIsBlack = False

            if not self.lambertBIsBlack:
                self.targetIconsShaderB[0].incandescence.set( [0, 0, 0] )
                self.lambertBIsBlack = True

        elif blend > 100:
            if blend == 200: self.targetIconsShaderB[0].incandescence.set( [ 1, 1, 1 ] )
            else:              self.targetIconsShaderB[0].incandescence.set( [ percent*0.01, 0.25+(percent*0.0075), percent*0.0015 ] )
            self.lambertBIsBlack = False

            if not self.lambertAIsBlack:
                self.targetIconsShaderA[0].incandescence.set( [0, 0, 0] )
                self.lambertAIsBlack = True

        else: #is 100 (50%)
            if not self.lambertBIsBlack:
                self.targetIconsShaderB[0].incandescence.set( [0, 0, 0] )
                self.lambertBIsBlack = True

            if not self.lambertAIsBlack:
                self.targetIconsShaderA[0].incandescence.set( [0, 0, 0] )
                self.lambertAIsBlack = True


    def _applyWeights(self, pointID, weightDict):
        skinCluster = self.skinClusterDict[self.nodeOfpointDict[pointID]]

        if self.pnt_typeDict[pointID] == 'mesh':
            strSkinCluster = str(skinCluster)
            strVertIndex = str(self._getComplexPointIndices(pointID)[0])

            cmds.removeMultiInstance('%s.wl[%s]' % (strSkinCluster, strVertIndex,))
            for influenceIndex in weightDict:
                influence = self.influenceDict[skinCluster][influenceIndex]
                arrayIndex = self.influenceArrayIndexDict[skinCluster][influence]
                cmds.setAttr('%s.wl[%s].w[%s]' % (strSkinCluster, strVertIndex, str(arrayIndex)), weightDict[influenceIndex])


        else:
            skinPercentTupleList = []
            for influenceIndex in weightDict:
                skinPercentTupleList.append((self.influenceDict[skinCluster][influenceIndex], weightDict[influenceIndex]))

            pymel.skinPercent(skinCluster, self.pntDict[pointID], transformValue=skinPercentTupleList )



    def storeWeights(self, refresh=False):
        if refresh:
            self.weightDict = {}
            self.skinClusterDict = {}
            self.influenceDict = {}
            self.targetAWeightDict = {}
            self.targetBWeightDict = {}

        for targetA in self.iconPointsA:
            self._getSkinWeights(targetA)

        for targetB in self.iconPointsB:
            self._getSkinWeights(targetB)

        for pointID in self.selectedPointIDs:
            self._getSkinWeights(pointID)

            targetsPointIDsA = self.strandTargetSequencesA_dict[pointID][self.currentSequence]
            targetsPointIDsB = self.strandTargetSequencesB_dict[pointID][self.currentSequence]

            for targetsPoint in targetsPointIDsA:
                self._getSkinWeights(targetsPoint)

            for targetsPoint in targetsPointIDsB:
                self._getSkinWeights(targetsPoint)


            # average weight targets if there are more than 1
            if len(targetsPointIDsA) == 1:
                weightedAverage_ofA = self.weightDict[targetsPointIDsA[0]]
            else:
                weightedAverage_ofA = self._getAveragedWeights(targetsPointIDsA)

            if len(targetsPointIDsB) == 1:
                weightedAverage_ofB = self.weightDict[targetsPointIDsB[0]]
            else:
                weightedAverage_ofB = self._getAveragedWeights(targetsPointIDsB)


            # store to the weightTarget Dict
            self.targetAWeightDict[pointID] = weightedAverage_ofA
            self.targetBWeightDict[pointID] = weightedAverage_ofB

    def _getEdgeFromPoints(self, pointA, pointB):
        connectingEdge = None

        # store component info
        for pointID in [pointA, pointB]:
            if pointID not in self.edgesOfPoint:
                for connectedEdge in self.pntDict[pointID].connectedEdges():
                    connectedEdgeID = self._getComponentID(connectedEdge)

                    if not pointID in self.edgesOfPoint:
                        self.edgesOfPoint[pointID] = [connectedEdgeID]

                    elif connectedEdgeID not in self.edgesOfPoint[pointID]:
                        self.edgesOfPoint[pointID].append(connectedEdgeID)

                    if connectedEdgeID not in self.pointsOfEdge:
                        self.pointsOfEdge[connectedEdgeID] = []

                        for connectedVert in self.edgeDict[connectedEdgeID].connectedVertices():
                            connectedVertID = self._getComponentID(connectedVert)

                            if connectedVertID not in self.pointsOfEdge[connectedEdgeID]:
                                self.pointsOfEdge[connectedEdgeID].append(connectedVertID)

        for connectedEdge in self.edgesOfPoint[pointA]:
            for connectedVert in self.pointsOfEdge[connectedEdge]:
                if connectedVert == pointB:
                    return connectedEdge

    #def _getWeightedAveragedWeights(self, *weightDicts, weightValue=50.0):

        #finalWeightDict = {}

        ## make sure list [0] has all influences in the other lists, so we can use it to itterate
        #for weightDic in weightDicts[1:]:
            #for influenceIndex in weightDictB:
                #if influenceIndex not in weightDictA:
                    #weightDicts[0][influenceIndex] = 0.0

        ## do the averaging math
        #for influenceIndex in weightDicts[0]:
            #weightA = weightDictA[influenceIndex] * (0.01 * ((100 - weightValue) * 2))
            #weightB = weightDictB.get(influenceIndex, 0.0) * ((weightValue * 2) * 0.01)

            #value = ((weightA+weightB) / 2)
            #if value:
                #finalWeightDict[influenceIndex] = value

        #return finalWeightDict

    def _getWeightedAveragedWeights(self, weightDictA, weightDictB, weightValue):

        finalWeightDict = {}

        # make sure list A has all influences in list B, so we can use it to itterate
        for influenceIndex in weightDictB:
            if influenceIndex not in weightDictA:
                weightDictA[influenceIndex] = 0.0

        # do the averaging math
        for influenceIndex in weightDictA:
            weightA = weightDictA[influenceIndex] * (0.01 * ((100 - weightValue) * 2))
            weightB = weightDictB.get(influenceIndex, 0.0) * ((weightValue * 2) * 0.01)

            value = ((weightA+weightB) / 2)
            if value:
                finalWeightDict[influenceIndex] = value

        return finalWeightDict


    def _getAveragedWeights(self, pointIDs):
        averagedValues = []

        influenceIndices = {}
        for pointID in pointIDs:
            self._getSkinWeights(pointID)
            for influenceIndex in self.weightDict[pointID]:
                if influenceIndex not in influenceIndices:
                    influenceIndices[influenceIndex] = None

        finalValues = {}
        for influenceIndex in influenceIndices:
            listOfValuesToAverage = []
            for pointID in pointIDs:
                value = self.weightDict[pointID].get(influenceIndex, 0.0) # 0.0 if no key value exists
                listOfValuesToAverage.append(value)

            averagedValue = (math.fsum(listOfValuesToAverage) / len(listOfValuesToAverage))
            finalValues[influenceIndex] = averagedValue

        return finalValues

    def _getSkinWeights(self, pointID, refresh=False):

        if pointID not in self.weightDict:
            node = self._getNode(pointID)
            skinCluster = self.skinClusterDict.get(node, None)
            if not skinCluster or refresh == True:
                skinCluster =  findRelatedSkinCluster(self.pntDict[pointID])
                self.skinClusterDict[node] = skinCluster

                influences = self._getInfluences(skinCluster)

            weights = pymel.skinPercent(skinCluster, self.pntDict[pointID], query=True, value=True )
            self.weightDict[pointID] = {}

            for i, weight in enumerate(weights):
                if weight:
                    self.weightDict[pointID][i] = weight


    def _getInfluences(self, skinCluster):

        if skinCluster not in self.influenceDict:
            usedIndices = skinCluster.matrix.getArrayIndices()
            self.influenceDict[skinCluster] = []
            self.influenceArrayIndexDict[skinCluster] = {}

            for index in usedIndices:
                inputs = skinCluster.matrix[index].inputs()
                if inputs:
                    influence = inputs[0]
                    self.influenceDict[skinCluster].append(influence)
                    self.influenceArrayIndexDict[skinCluster][influence] = index

        return self.influenceDict[skinCluster]


    def _getMostParallelPoint(self, pointOfOriginID, pointOfReferenceId, inclusionList, exclusionList=[]):
        reverseOriginVectorX = self.pnt_cameraSpacePostionDict[pointOfReferenceId][0] - self.pnt_cameraSpacePostionDict[pointOfOriginID][0]
        reverseOriginVectorY = self.pnt_cameraSpacePostionDict[pointOfReferenceId][1] - self.pnt_cameraSpacePostionDict[pointOfOriginID][1]
        reverseOriginVector = normalizeVector([reverseOriginVectorX, reverseOriginVectorY])

        mostParallelPoint = None
        strongestDot = -1
        for i, pointID in enumerate(inclusionList):
            if pointID not in exclusionList:
                vectorX = self.pnt_cameraSpacePostionDict[pointOfOriginID][0] - self.pnt_cameraSpacePostionDict[pointID][0]
                vectorY = self.pnt_cameraSpacePostionDict[pointOfOriginID][1] - self.pnt_cameraSpacePostionDict[pointID][1]
                vector = normalizeVector([vectorX, vectorY])

                #dotValue = numpy.dot(reverseOriginVector, vector)
                dotValue = dotProduct(reverseOriginVector, vector)

                if dotValue > strongestDot:
                    mostParallelPoint = pointID
                    strongestDot = dotValue

        return mostParallelPoint


    def _getPointsConnectedByFace(self, inputPointID, pointInclusionList=[], pointExclusionList=[], firstOnly=False):

        returnList = []
        shape = self._getNode(inputPointID)

        if inputPointID not in self.facesOfPoint:
            self.facesOfPoint[inputPointID] = []
            connectedFaces  = self.pntDict[inputPointID].connectedFaces()
            for connectedFace in connectedFaces:
                faceID = self._getComponentID(connectedFace)
                self.facesOfPoint[inputPointID].append(faceID)

                if faceID not in self.pointsOfFace:
                    self.pointsOfFace[faceID] = []

                    for vertIndex in connectedFace.getVertices():
                        vert = shape.vtx[vertIndex]
                        vertID = self._getComponentID(vert)

                        if vertID not in self.pointsOfFace[faceID]:
                            self.pointsOfFace[faceID].append(vertID)


        for connectedFace in self.facesOfPoint[inputPointID]:
            for pointOfFace in self.pointsOfFace[connectedFace]:

                continueFlag = True
                if pointInclusionList:
                    if pointOfFace not in pointInclusionList:
                        continueFlag = False

                if continueFlag:
                    if pointExclusionList:
                        if pointOfFace in pointExclusionList:
                            continueFlag = False

                if continueFlag:
                    if firstOnly:
                        return [pointOfFace]

                    else:
                        if pointOfFace not in returnList:
                            returnList.append(pointOfFace)

        return returnList

    def _getFacesConnectedByEdge(self, edgeID, inclusionList=[], exclusionList=[]):

        if edgeID not in self.facesOfEdge:
            self.facesOfEdge[edgeID] = []
            for connectedFace in self.edgeDict[edgeID].connectedFaces():
                connectedFaceID = self._getComponentID(connectedFace)
                self.facesOfEdge[edgeID].append(connectedFaceID)

        return self.facesOfEdge[edgeID]

    def _getVertsOfFace(self, faceID):
        if faceID not in self.pointsOfFace:
            self.pointsOfFace[faceID] = []
            for connectedVert in self.faceDict[faceID].connectedVertices():
                connectedVertID = self._getComponentID(connectedVert)
                self.pointsOfFace[faceID].append(connectedVertID)

        return self.pointsOfFace[faceID]

    def _getVertStrandTargets(self, strand):
        strandTargetsA = []
        strandTargetsB = []

        shape = self._getNode(strand[0])

        for pointID in strand:
            connectedPoints = self.connectedPointsDict[pointID]
            connectedFaces  = self.pntDict[pointID].connectedFaces()

            if pointID not in self.facesOfPoint:
                if pointID not in self.facesOfPoint:
                    self.facesOfPoint[pointID] = []

            for face in connectedFaces:
                faceID = self._getComponentID(face)
                self.faceDict[faceID] = face

                if faceID not in self.facesOfPoint[pointID]:
                    self.facesOfPoint[pointID].append(faceID)

                if faceID not in self.pointsOfFace:
                    self.pointsOfFace[faceID] = []

                for vertIndex in face.getVertices():
                    vert = shape.vtx[vertIndex]
                    vertID = self._getComponentID(vert)
                    self.pntDict[vertID] = vert

                    if vertID not in self.pointsOfFace[faceID]:
                        self.pointsOfFace[faceID].append(vertID)

                    if vertID not in self.facesOfPoint:
                        self.facesOfPoint[vertID] = [faceID]

                    elif faceID not in self.facesOfPoint[vertID]:
                        self.facesOfPoint[vertID].append(faceID)



        if len(strand) == 2:    #--------------------------------------------------------------------------------------
            strandTargetsA = []
            strandTargetsB = []

            connectingEdge = self._getEdgeFromPoints(strand[0], strand[1])

            pointPriorityDict = {}    # key=strandPointID, value=dict(key=pointID, value=int representing a points priority)
            pointsConnectedTo0 = self._getConnectedPoints(strand[0], exclusionList=strand)
            pointsConnectedTo1 = self._getConnectedPoints(strand[1], exclusionList=strand)
            connectedPoints = list(pointsConnectedTo0)


            for connectedPoint in pointsConnectedTo1:
                if connectedPoint not in connectedPoints:
                    connectedPoints.append(connectedPoint)

            # populate priority dict
            for strandVert in strand:
                pointPriorityDict[strandVert] = {}

                for connectedPoint in connectedPoints:
                    pointPriorityDict[strandVert][connectedPoint] = 0

            # +5 for each point connected by edge to the strand point
            for connectedPoint in connectedPoints:
               if connectedPoint in pointsConnectedTo0:
                   pointPriorityDict[strand[0]][connectedPoint] += 5

               if connectedPoint in pointsConnectedTo1:
                   pointPriorityDict[strand[1]][connectedPoint] += 5

            # +1 if it is connected by face to the edge between points
            for connectedFace in self._getFacesConnectedByEdge(connectingEdge):
                for vertOfFace in self._getVertsOfFace(connectedFace):
                    if vertOfFace in connectedPoints:
                        if vertOfFace not in strand:
                            for strandVert in strand:
                                pointPriorityDict[strandVert][vertOfFace] += 1


            # find 2 points for each strand point with the highest priority
            strand0Targets = []
            largetsPriority = 0
            for strandTarget in pointPriorityDict[strand[0]]:
                priorityValue = pointPriorityDict[strand[0]][strandTarget]
                if priorityValue >= largetsPriority:
                    if strand0Targets:
                        strand0Targets = [strandTarget, strand0Targets[0]]
                    else:
                        strand0Targets = [strandTarget]
                    largetsPriority = priorityValue

                # incase the first item IS the largest priority
                elif len(strand0Targets) != 2:
                    strand1Targets = [strand0Targets[0], strandTarget]

            strand1Targets = []
            largetsPriority = 0
            for strandTarget in pointPriorityDict[strand[1]]:
                priorityValue = pointPriorityDict[strand[1]][strandTarget]
                if priorityValue >= largetsPriority:
                    if strand1Targets:
                        strand1Targets = [strandTarget, strand1Targets[0]]
                    else:
                        strand1Targets = [strandTarget]
                    largetsPriority = priorityValue

                # incase the first item IS the largest priority
                elif len(strand1Targets) != 2:
                    strand1Targets = [strand1Targets[0], strandTarget]


            # add to targets A and B lists
            # find As
            strandTargetsA_firstTarget = strand0Targets.pop()
            strandTargetsA = [[strandTargetsA_firstTarget]]
            strandTargetsAShallowList = [strandTargetsA_firstTarget]

            pointsConnectedToFirstTarget = self._getPointsConnectedByFace(strandTargetsA_firstTarget)
            for strandTarget in strand1Targets:
                if strandTarget in pointsConnectedToFirstTarget:
                    strandTargetsA.append([strandTarget])
                    strandTargetsAShallowList.append(strandTarget)
                    break


            # find Bs
            for strandTarget in strand0Targets:
                if strandTarget not in strandTargetsAShallowList:
                    strandTargetsB.append([strandTarget])
                    break

            for strandTarget in strand1Targets:
                if strandTarget not in strandTargetsAShallowList:
                    strandTargetsB.append([strandTarget])
                    break


            strandTargetsA = strandTargetsA
            strandTargetsB = strandTargetsB


        if len(strand) > 2:    #--------------------------------------------------------------------------------------

            strandTargetsA = []
            strandTargetsB = []

            # MID POINTS
            lastStrandIndex = len(strand)-1
            # for all but the end points
            for i, pointID in enumerate(strand):

                # if not and end point
                if i != 0 and i != lastStrandIndex:

                    # a unique list of points connected by edges to the this point, excluding the original strand
                    connectedPoints = []
                    for connectedPoint in self.connectedPointsDict[pointID]:
                        if connectedPoint not in strand:
                            connectedPoints.append(connectedPoint)

                    if not connectedPoints:
                        pymel.error('what the heck did you select dude?')

                    # make listB contain all connected points, and move one into list A.
                    # we will move all connected points of that point to listA
                    targetListB = list(connectedPoints)
                    targetListA = [targetListB.pop(0)] # randomly take a point



                    #pointToAddToB = self._getPointsConnectedByFace(strandTargetB, pointInclusionList=unusedConnectedPoints, pointExclusionList=strandTargetsB[adjacentTargetIndex], firstOnly=False)

                    # itterate connected faces in search of connected points on the same side of the strand
                    faceStack = list(self.facesOfPoint[targetListA[0]])
                    iCheck = 0
                    while faceStack:
                        iCheck += 1
                        if iCheck == 99:
                            pymel.error('icheck failed')

                        currentFace = faceStack.pop(0)
                        pointsOfCurrentFace = self.pointsOfFace[currentFace]

                        for pointOfFace in pointsOfCurrentFace:
                           if pointOfFace in targetListB:
                              if pointOfFace in connectedPoints:
                                  if pointOfFace not in [connectedPoints[0], connectedPoints[-1]]:
                                      targetListB.remove(pointOfFace)
                                      targetListA.append(pointOfFace)

                              for connectedFaceID in self.facesOfPoint[pointOfFace]:
                                  if connectedFaceID != currentFace:
                                      faceStack.append(connectedFaceID)

                    # append targetList to the correct strand side (A or B)
                    if not strandTargetsA: # order doesn't matter on first one
                        strandTargetsA.append(targetListA)
                        strandTargetsB.append(targetListB)

                    else:
                        laststrandTargetA = strandTargetsA[-1]

                        A_to_A = False
                        for lastVert in laststrandTargetA:
                            for connectedFace in self.facesOfPoint[lastVert]:
                                for faceVert in self.pointsOfFace[connectedFace]:
                                    if faceVert in targetListA:
                                        strandTargetsA.append(targetListA)
                                        strandTargetsB.append(targetListB)
                                        A_to_A = True
                                        break
                                        break
                                        break

                        if not A_to_A:
                            strandTargetsA.append(targetListB)
                            strandTargetsB.append(targetListA)

            # END POINTS
            for i, pointID in enumerate(strand):

                # if it IS an  end point
                if i == 0 or i == lastStrandIndex:

                    if i == 0:
                        adjacentStrandIndex = 1
                        adjacentTargetIndex = 0

                    elif i == lastStrandIndex:
                        adjacentStrandIndex = -2
                        adjacentTargetIndex = -1

                    # a unique list of points connected by edges to the this point, excluding the original strand
                    connectedPoints = []
                    for connectedPoint in self.connectedPointsDict[pointID]+self.connectedPointsDict[strand[adjacentStrandIndex]]:
                        if connectedPoint not in strand:
                            connectedPoints.append(connectedPoint)


                    # a unique list of points connected by edges to the this point, that are being used as targets already
                    unusedConnectedPoints = []
                    for connectedPoint in self.connectedPointsDict[pointID]:
                        if connectedPoint not in strand:
                            unusedConnectedPoints.append(connectedPoint)

                    if not connectedPoints:
                        pymel.error('what the heck did you select dude?')


                    # make empty lists, we will vet points to see if they are appropriate before adding them
                    targetListA = []
                    targetListB = []

                    pointsToAddToA = []
                    pointsToAddToB = []


                    # find ideal pointA to add (closest face-connected point from the adjacent mid target)
                    for strandTargetA in strandTargetsA[adjacentTargetIndex]:
                        pointsToAddToA = self._getPointsConnectedByFace(strandTargetA, pointInclusionList=unusedConnectedPoints, pointExclusionList=strandTargetsA[adjacentTargetIndex], firstOnly=False)
                        if pointsToAddToA:
                            break


                    # find ideal pointB to add (closest face-connected point from the adjacent mid target)
                    for strandTargetB in strandTargetsB[adjacentTargetIndex]:
                        pointsToAddToB = self._getPointsConnectedByFace(strandTargetB, pointInclusionList=unusedConnectedPoints, pointExclusionList=strandTargetsB[adjacentTargetIndex], firstOnly=False)
                        if pointsToAddToB:
                            break


                    pointsToRemoveFromA = []
                    for pointToAddToA in pointsToAddToA:
                        faceConnectedPoints = self._getPointsConnectedByFace(pointToAddToA, pointInclusionList=strand)

                        if len(self.facesOfPoint[pointID]) <= 4:

                            # if there are only 4 connected faces to the end point, we will add a special check
                            # to make sure that the proposed point is connected to the adjacent strand point
                            if strand[adjacentStrandIndex] in faceConnectedPoints:
                               break
                            else:
                                pointsToRemoveFromA.append(pointToAddToA)

                        else:
                            for connectedPoint in faceConnectedPoints:
                                # is the propose point connected to both?
                                if connectedPoint in strandTargetsB[adjacentTargetIndex]:
                                    pointsToRemoveFromA.append(pointToAddToA)    # if so, it is no good
                                    break

                    for pointToRemove in pointsToRemoveFromA:
                        pointsToAddToA.remove(pointToRemove)




                    pointsToRemoveFromB = []
                    for pointToAddToB in pointsToAddToB:
                        if len(self.facesOfPoint[pointID]) <= 4:

                            # if there are only 4 connected faces to the end point, we will add a special check
                            # to make sure that the proposed point is connected to the adjacent strand point
                            faceConnectedPoints = self._getPointsConnectedByFace(pointToAddToB, pointInclusionList=strand)
                            if strand[adjacentStrandIndex] in faceConnectedPoints:
                               break
                            else:
                                pointsToRemoveFromB.append(pointToAddToB)

                        else:
                            for connectedPoint in faceConnectedPoints:
                                # is the propose point connected to both?
                                if connectedPoint in strandTargetsA[adjacentTargetIndex]:
                                    pointsToRemoveFromA.append(pointToAddToB)    # if so, it is no good
                                    break

                    for pointToRemove in pointsToRemoveFromB:
                        pointsToAddToB.remove(pointToRemove)



                    # None found?
                    if not pointsToAddToA:
                        for targetPoints in strandTargetsA[adjacentTargetIndex]:
                            for connectedFace in self.facesOfPoint[targetPoints]:
                                for pointOfFace in self.pointsOfFace[connectedFace]:
                                    if pointOfFace == pointID:
                                        if not pointsToAddToA:
                                            pointsToAddToA.append(targetPoints)
                                            break


                    if not pointsToAddToB:
                        for targetPoints in strandTargetsB[adjacentTargetIndex]:
                            for connectedFace in self.facesOfPoint[targetPoints]:
                                for pointOfFace in self.pointsOfFace[connectedFace]:
                                    if pointOfFace == pointID:
                                        if not pointsToAddToB:
                                            pointsToAddToB.append(targetPoints)
                                            break


                    # finnally add the two proposed points
                    if i == 0:
                        strandTargetsA.insert(0, pointsToAddToA)
                        strandTargetsB.insert(0, pointsToAddToB)
                    else:
                        strandTargetsA.append(pointsToAddToA)
                        strandTargetsB.append(pointsToAddToB)


        return strandTargetsA, strandTargetsB


    def nextSequence(self):
        if self.currentSequence == self.lastSequence:
            self.currentSequence = 0
        else:
            self.currentSequence += 1

        self.storeWeights()
        self.setTargetIconPositions()

    def previousSequence(self):
        if self.currentSequence == 0:
            self.currentSequence = self.lastSequence
        else:
            self.currentSequence -= 1

        self.storeWeights()
        self.setTargetIconPositions()

    def createTargetIcons(self):
        self.deleteTargetIcons()

        panel = getCurrentPannel()
        isolateState = pymel.isolateSelect(panel, query=True, state=True)
        radius = 1



        if not self.targetIconsShaderA:    # make lambert for A spheres
            lambertA = pymel.shadingNode('lambert', asShader=True, name='DELETE_ME__TEMP_rightLambert')
            lambertA.addAttr('createColoredVertexSpheres_tempType', dt='string')
            lambertA.color.set( [0,0,0] )
            lambertA.transparency.set( [0.5,0.5,0.5] )

            shadingEngineA = pymel.sets(renderable=True, noSurfaceShader=True, empty=True, name='DELETE_ME__TEMP_rightshadingEngine')
            shadingEngineA.addAttr('createColoredVertexSpheres_tempType', dt='string')
            pymel.connectAttr(lambertA+".outColor", shadingEngineA+".surfaceShader", force=True)
            self.targetIconsShaderA = (lambertA, shadingEngineA)


        if not self.targetIconsShaderB:    # make lambert for B spheres
            lambertB = pymel.shadingNode('lambert', asShader=True, name='DELETE_ME__TEMP_rightLambert')
            lambertB.addAttr('createColoredVertexSpheres_tempType', dt='string')
            lambertB.color.set( [0,0,0] )
            lambertB.transparency.set( [0.5,0.5,0.5] )

            shadingEngineB = pymel.sets(renderable=True, noSurfaceShader=True, empty=True, name='DELETE_ME__TEMP_rightshadingEngine')
            shadingEngineB.addAttr('createColoredVertexSpheres_tempType', dt='string')
            pymel.connectAttr(lambertB+".outColor", shadingEngineB+".surfaceShader", force=True)
            self.targetIconsShaderB = (lambertB, shadingEngineB)





        # Create Sphere A
        for i, targetA in enumerate(self.iconPointsA):
            if i == 0:
                targetIconA = pymel.sphere(name='DELETE_ME__vertexSpheres', radius=radius, sections=1, spans=2)[0]
                targetIconA.overrideEnabled.set(1)
                targetIconA.drawOverride.overrideColor.set(2)

                targetIconA.addAttr('createColoredVertexSpheres_tempType', dt='string')
                pymel.sets( shadingEngineA, forceElement=targetIconA, )

            else:
                targetIconA = pymel.instance(self.targetIconsA[0], name='DELETE_ME__vertexSpheres',)[0]


            self.targetIconsA.append(targetIconA)
            if isolateState:
                pymel.isolateSelect(panel, addDagObject=targetIconA)


        # Create Sphere B
        for i, targetB in enumerate(self.iconPointsB):
            if i == 0:
                targetIconB = pymel.sphere(name='DELETE_ME__vertexSpheres', radius=radius, sections=1, spans=2)[0]
                targetIconB.overrideEnabled.set(1)
                targetIconB.drawOverride.overrideColor.set(2)

                targetIconB.addAttr('createColoredVertexSpheres_tempType', dt='string')
                pymel.sets( shadingEngineB, forceElement=targetIconB, )

            else:
                targetIconB = pymel.instance(self.targetIconsB[0], name='DELETE_ME__vertexSpheres',)[0]

            self.targetIconsB.append(targetIconB)
            if isolateState:
                pymel.isolateSelect(panel, addDagObject=targetIconB)

        pymel.select(list(self.pointsInNodesDict.keys()))
        for node in self.pointsInNodesDict:
            print('hilight ' + str(node))
            #mel.eval( 'hilite '+node.name() )
        pymel.select(self.selection)

        self.setTargetIconPositions()


    def setTargetIconScales(self, pointID, target_pointID, targetIcon):
        pointID = pointID[0]

        target_cameraSpace = self._getCameraSpacePosition(target_pointID)
        targetIconScale = target_cameraSpace[2]*-0.01

        point_cameraSpace = self._getCameraSpacePosition(pointID)
        pointScale = point_cameraSpace[2]*-0.01

        distanceBetweenPoints = distanceBetween(target_cameraSpace, point_cameraSpace)

        if targetIconScale > (distanceBetweenPoints / 5) or pointScale > (distanceBetweenPoints / 5):
            targetIconScale = (distanceBetweenPoints / 5)

        if targetIconScale < (distanceBetweenPoints / 30) or pointScale < (distanceBetweenPoints / 30):
            targetIconScale = (distanceBetweenPoints / 30)

        targetIcon.scale.set(targetIconScale, targetIconScale, targetIconScale)

    def setTargetIconPositions(self):

        targetIconsAStack = list(self.targetIconsA)
        targetIconsBStack = list(self.targetIconsB)

        targetDictA = {}
        targetDictB = {}

        for pointID in self.selectedPointIDs:

            targetsPointIDsA = self.strandTargetSequencesA_dict[pointID][self.currentSequence]
            for targetPointA in targetsPointIDsA:
                if targetPointA not in targetDictA:
                    targetIcon = targetIconsAStack.pop()
                    worldPosition = self._getWorldSpacePosition(targetPointA)

                    targetDictA[targetPointA] = {'icon':targetIcon,
                                                 'position':worldPosition,
                                                 'blendingPoints':[pointID]
                                                }
                else:
                    if not pointID in targetDictA[targetPointA]['blendingPoints']:
                        targetDictA[targetPointA]['blendingPoints'].append(pointID)


            targetsPointIDsB = self.strandTargetSequencesB_dict[pointID][self.currentSequence]
            for targetPointB in targetsPointIDsB:
                if targetPointB not in targetDictB:
                    targetIcon = targetIconsBStack.pop()
                    worldPosition = self._getWorldSpacePosition(targetPointB)

                    targetDictB[targetPointB] = {'icon':targetIcon,
                                                 'position':worldPosition,
                                                 'blendingPoints':[pointID]
                                                }
                else:
                    if not pointID in targetDictB[targetPointB]['blendingPoints']:
                        targetDictB[targetPointB]['blendingPoints'].append(pointID)

        for targetID in targetDictA:
            subDict = targetDictA[targetID]
            pymel.xform(subDict['icon'], translation=subDict['position'], worldSpace=True)
            self.setTargetIconScales(subDict['blendingPoints'], targetID, subDict['icon'])

        for targetID in targetDictB:
            subDict = targetDictB[targetID]
            pymel.xform(subDict['icon'], translation=subDict['position'], worldSpace=True)
            self.setTargetIconScales(subDict['blendingPoints'], targetID, subDict['icon'])





    def deleteTargetIcons(self):
        deleteMeObjects = pymel.ls('DELETE_ME__*')
        deleteList = []

        for each in deleteMeObjects:
            if pymel.attributeQuery('createColoredVertexSpheres_tempType', node=each, exists=True):
                deleteList.append(each)

        if deleteList:
            pymel.delete(deleteList)

    def _getComponentID(self, component):
        """Returns a string for used to identify a component in all
        the various informational dictionarys
        """
        componentString  = str(component).split("[")[1]
        componentString = componentString.split("]")[0]
        
        # componentID = componentString.__hash__()

        componentID = int(componentString)


        # add to relevent dictionary
        if component.__class__.__name__ == 'MeshEdge':
            self.edgeDict[componentID] = component

        elif component.__class__.__name__ == 'MeshFace':
            self.faceDict[componentID] = component

        else:
            self.pntDict[componentID] = component

        return componentID


    def _getWorldSpacePosition(self, pointID, refresh=False):
        if not refresh:
            if pointID in self.pnt_worldSpacePostionDict:
                return self.pnt_worldSpacePostionDict[pointID]

        point = self.pntDict[pointID]
        worldPosition = pymel.xform(point, query=True, translation=True, worldSpace=True)
        self.pnt_worldSpacePostionDict[pointID] = worldPosition

        return worldPosition


    def _getCameraSpacePosition(self, pointID, refresh=False):
        if not refresh:
            if pointID in self.pnt_cameraSpacePostionDict:
                return self.pnt_cameraSpacePostionDict[pointID]

        if not refresh:
            if pointID in self.pnt_worldSpacePostionDict:
                pointWorldSpace = self.pnt_worldSpacePostionDict[pointID]
            else:
                pointWorldSpace = self._getWorldSpacePosition(pointID)

        camera = self.currentCamera


        # get point in camera space
        aPoint = OpenMaya.MPoint(pointWorldSpace[0], pointWorldSpace[1], pointWorldSpace[2])
        result = aPoint * self.currentCameraMMatrix

        self.pnt_cameraSpacePostionDict[pointID] = [result.x, result.y, result.z]
        return self.pnt_cameraSpacePostionDict[pointID]

    def _getNode(self, pointID):
        if pointID not in self.nodeOfpointDict:
            point = self.pntDict[pointID]
            node = point.node()
            self.nodeOfpointDict[pointID] = node

            # type dict
            if pointID not in self.pnt_typeDict:
                componentType = point.nodeType()
                self.pnt_typeDict[pointID] = componentType

        return self.nodeOfpointDict[pointID]


    def _getComplexPointIndices(self, pointID):
        """Return a list of intigers representing the index of the component."""
        if pointID not in self.pnt_complexIndexDict:
            componentString = str(self.pntDict[pointID])
            startOfStringIndex = componentString.find('[')
            indexStrings = componentString[startOfStringIndex+1:-1].split('][')
            indices = []
            for indexString in indexStrings:
                index = int(indexString)
                indices.append(index)

            self.pnt_complexIndexDict[pointID] = indices

        return self.pnt_complexIndexDict[pointID]

    def _getConnectedPoints(self, pointID, inclusionList=[], exclusionList=[]):

        # start empty list if none exists
        if pointID not in self.connectedPointsDict:
            self.connectedPointsDict[pointID] = []

        if self.pnt_typeDict[pointID] == 'mesh':

            connectedVertIDs = self.connectedPointsDict[pointID]

            # get connected vertIDs, if not already stored in dict
            if not connectedVertIDs:
                vert = self.pntDict[pointID]
                connectedVerts = vert.connectedVertices()
                for connectedVert in connectedVerts:
                    connectedVertID = self._getComponentID(connectedVert)
                    connectedVertIDs.append(connectedVertID)

                    #populate info dicts
                    if connectedVertID not in self.pntDict:
                        self.pntDict[connectedVertID] = connectedVert

                        if connectedVertID not in self.connectedPointsDict[pointID]:
                            self.connectedPointsDict[pointID].append(connectedVertID)


            returnList = []
            for connectedVertID in connectedVertIDs:

                # if it is not included/excluded, add it to list
                if connectedVertID not in exclusionList:
                    if not inclusionList or connectedVertID in inclusionList:
                        returnList.append(connectedVertID)

            return returnList

        elif self.pnt_typeDict[pointID] == 'nurbsSurface':
            pass

        elif self.pnt_typeDict[pointID] == 'nurbsCurve':
            pass

        elif self.pnt_typeDict[pointID] == 'bezierCurve':
            pass

        elif self.pnt_typeDict[pointID] == 'lattice':
            pass

    def _orderConnectedVertsClockwise(self, pointID):
        orderedVerts = []
        connectedPoints = self.connectedPointsDict[pointID]
        unOrderedVerts = list(connectedPoints)

        # find point that is fathest to camera left
        leftMostPoint = connectedPoints[0]
        for connectedPointID in connectedPoints[1:]:
            #leftMostX = self.pnt_cameraSpacePostionDict[leftMostPoint]
            leftMostX = self._getCameraSpacePosition(leftMostPoint)
            connectedPointX = self._getCameraSpacePosition(connectedPointID)

            if leftMostX > connectedPointX:
                leftMostPoint = connectedPointID

        orderedVerts.append(leftMostPoint)
        unOrderedVerts.remove(leftMostPoint)

        count = 0
        maxCount = 999
        direction = 1
        while len(orderedVerts) != len(connectedPoints):
            count += 1

            if direction == 1:
                faceConnectedPoints = self._getPointsConnectedByFace(orderedVerts[-1], pointInclusionList=connectedPoints, pointExclusionList=orderedVerts)

                if not faceConnectedPoints:
                    direction = -1

                else:
                    nextPoint = None
                    for faceConnectedPoint in faceConnectedPoints:
                        if faceConnectedPoint != pointID:
                            if not nextPoint:
                                nextPoint = faceConnectedPoint

                            else:
                                if self._getCameraSpacePosition(nextPoint)[1] < self._getCameraSpacePosition(faceConnectedPoint)[1]:
                                #if self.pnt_cameraSpacePostionDict[nextPoint][1] < self.pnt_cameraSpacePostionDict[faceConnectedPoint][1]:
                                    nextPoint = faceConnectedPoint

                    orderedVerts.append(nextPoint)
                    unOrderedVerts.remove(nextPoint)


            else:   # direction is reversed
                faceConnectedPoints = self._getPointsConnectedByFace(orderedVerts[0], pointInclusionList=connectedPoints, pointExclusionList=orderedVerts)

                if not faceConnectedPoints: # well, just grab a random left over then :S
                    nextPoint = unOrderedVerts.pop()
                    orderedVerts.append(nextPoint)

                else:
                    nextPoint = None
                    for faceConnectedPoint in faceConnectedPoints:
                        if faceConnectedPoint != pointID:
                            nextPoint = faceConnectedPoint
                            break

                    orderedVerts.append(nextPoint)
                    unOrderedVerts.remove(nextPoint)

        ## get more topology info
        ## populate 2 dictionarys, one with connected faces as the key, and the points of those faces as the
        ## value, and the second dictionary having connected verts as keys, and faces connected to those verts as values
        #facesOfPointsDict = {pointID:[]}
        #for connectedPointID in connectedPoints:
            #facesOfPointsDict[connectedPointID] = []

        #pointsOfFacesDict = {}
        #connectedFaces = self.pntDict[pointID].connectedFaces()
        #for face in connectedFaces:
            #faceID = self._getComponentID(face)
            #faceVertIndices = face.getVertices()
            #faceVertsList = []
            #for faceVertIndex in faceVertIndices:
                #faceVert = self.pntDict[pointID].node().vtx[faceVertIndex]
                #faceVertID = self._getComponentID(faceVert)
                #if faceVertID in connectedPoints:
                    #self.pntDict[faceVertID] = faceVert
                    #faceVertsList.append(faceVertID)

                    #if faceID not in facesOfPointsDict[faceVertID]:
                        #facesOfPointsDict[faceVertID].append(faceID)

            #pointsOfFacesDict[faceID] = faceVertsList

        #previousLen = 0
        #searchInOppositeDirection = False

        #while len(orderedVerts) != len(connectedPoints):
            ## infinite loop check

            #if len(orderedVerts) == previousLen:
                #pymel.error('unable to order connected verts')
            #previousLen = len(orderedVerts)

            #if searchInOppositeDirection:
                #previoiusVertID = orderedVerts[0]
            #else:
                #previoiusVertID = orderedVerts[-1]

            #connectedFaceIDs = facesOfPointsDict[previoiusVertID]

            #if not searchInOppositeDirection:
                #unorderedVerts = []
                #for connectedFaceID in connectedFaceIDs:
                    #for faceVertID in pointsOfFacesDict[connectedFaceID]:
                        #if faceVertID != pointID and faceVertID not in orderedVerts:
                            #unorderedVerts.append(faceVertID)

            #if not unorderedVerts:
                #searchInOppositeDirection = True

            #else:
                #OOOOOOO = 'unorderedVerts';  print '%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO))))
                ## If we have 2 unordered verts, then we are solving the first point, and must choose a
                ## direction to solve, preferably clockwise. Find the uppermost of the 2 vertex in camera Y
                ## and remove the other
                #if len(unorderedVerts) == 2:
                    #vertA_camY = self._getCameraSpacePosition(unorderedVerts[0])
                    #vertB_camY = self._getCameraSpacePosition(unorderedVerts[1])

                    #if vertA_camY < vertB_camY:
                        #unorderedVerts.remove(unorderedVerts[1])
                    #else:
                        #unorderedVerts.remove(unorderedVerts[0])

                #if searchInOppositeDirection:
                    #orderedVerts.insert(0, unorderedVerts[0])
                #else:
                    #orderedVerts.append(unorderedVerts[0])

        return orderedVerts


# MAIN FUNCTIONS ----------------------------------------------------------------------------------------------------------------
weightBlenderInfo = None
def start(points=None):
    global weightBlenderInfo
    store_selection_list()
    selection = cmds.ls(selection=True)
    print('start')
    weightBlenderInfo = WeightBlenderInfo()
    weightBlenderInfo.start()
    
def change(value=0.0):
    global weightBlenderInfo
    # weightBlenderInfo = WeightBlenderInfo()

    weightBlenderInfo.blend(value)

def finish():
    global weightBlenderInfo
    print('finished')
    if weightBlenderInfo:
        weightBlenderInfo.deleteTargetIcons()
    restore_selection()

import maya.api.OpenMaya as om2

# Initialize global variables
stored_selection = None
selection_context = None


def store_selection_list():
    global stored_selection, selection_context

    stored_selection = cmds.ls(sl=True, fl=True)
    if "vtx" in stored_selection[0]:
        selection_context = "vertex"
    elif ".e[" in stored_selection[0]:
        selection_context = "edge"

    # updateObjectSelectionMasks;
    # updateComponentSelectionMasks;


    vertices = cmds.polyListComponentConversion(toVertex=True)
    cmds.select(vertices)
    pass

def restore_selection():
    stored_selection, selection_context
    cmds.select(stored_selection)
    if selection_context == "vertex":
        cmds.selectMode(component=True )
        cmds.selectType(vertex=True)
        cmds.hilite(stored_selection[0].split(".")[0])

    if selection_context == "edge":
        cmds.selectMode(component=True )
        cmds.selectType(polymeshEdge=True)
        cmds.hilite(stored_selection[0].split(".")[0])
    ctx = cmds.currentCtx()
    print(cmds.contextInfo(ctx, escapeContext=True))




# cmds.select(all_target_curves, r=True)
# cmds.selectMode(component=True )
# cmds.selectType(controlVertex=True)


def cancel():
    global weightBlenderInfo

    finish()
    pass

def next():
    global weightBlenderInfo
    weightBlenderInfo.nextSequence()

def previous():
    global weightBlenderInfo
    weightBlenderInfo.previousSequence()


def blendWithBothNeighbors():
    global weightBlenderInfo
    selection = pymel.ls(selection=True)

    weightBlenderInfo = WeightBlenderInfo()
    weightBlenderInfo.start(createTargetIcons=False)

    weightBlenderInfo.averageWithBothNeighbors()


    pymel.select(selection)

    print('hiyea')


# MISC
def getCurrentPannel():
    try:
        panel = pymel.getPanel(underPointer=True)
        panel = panel.split('|')[-1]
        return panel

    except:
        printError()
        print('## Failed to find current panel, make sure you have a view port with focus')


# UNDOS ----------------------------------------------------------------------------------------------------------------

## weight blend undo
#weightBlend_maxUndos = 10
#weightBlend_weightsDictHistory = []    #[(weightDict, skinCluster), (weightDict, skinCluster)...]
#weightBlend_weightsDictHistoryIndex = 0    #current position in weight dict

#def addToUndoStack(dictToAdd):
    #global weightBlenderInfo

    #if dictToAdd == 'weightsDict':
        #global weightsDict
        #inputWeightDict = weightsDict

    #if dictToAdd == 'appliedWeightsDict':
        #global appliedWeightsDict
        #inputWeightDict = appliedWeightsDict

    #global selectionIndices
    #global skinCluster
    #global weightBlend_maxUndos
    #global weightBlend_weightsDictHistory
    #global weightBlend_weightsDictHistoryIndex

    ## Does given weight data differ from the last undo?
    #weightsDifferFromLastUndo = False
    #if weightBlend_weightsDictHistory:
        #historicalWeightDict, historicalSkinCluster = weightBlend_weightsDictHistory[weightBlend_weightsDictHistoryIndex]
        #if historicalSkinCluster == skinCluster:
            #for vertIndex in selectionIndices:
                #if vertIndex in inputWeightDict and vertIndex in historicalWeightDict:
                    #for weightIndex in inputWeightDict[vertIndex]:
                        #if weightsDifferFromLastUndo:
                            #break
                        #else:

                            #if weightIndex in historicalWeightDict[vertIndex] and weightIndex in inputWeightDict[vertIndex]:
                                #if round(inputWeightDict[vertIndex][weightIndex], 3) != round(historicalWeightDict[vertIndex][weightIndex], 3):
                                    #weightsDifferFromLastUndo = True
                                    #break


                            #else:weightsDifferFromLastUndo = True ;
                #else:weightsDifferFromLastUndo = True ;
        #else:weightsDifferFromLastUndo = True ;
    #else:weightsDifferFromLastUndo = True ;


    ## store to undo stack
    #if weightsDifferFromLastUndo:

        #weightsAreValid = True # are they valid (totaling 1.0)?
        #for vertIndex in selectionIndices:
            #weightTotal = 0.0
            #for weightIndex in inputWeightDict[vertIndex]:
                #weightTotal += inputWeightDict[vertIndex][weightIndex]
            #if not round(weightTotal, 2) == 1.0:# > 1.001 or weightTotal < 0.999:
                #weightsAreValid = False

        #if weightsAreValid:
            ## is current undo 0? if not this is the result of redos
            #while weightBlend_weightsDictHistoryIndex != 0:
                #if weightBlend_weightsDictHistoryIndex < 0:
                    #pymel.error('how did that happen?')
                #weightBlend_weightsDictHistoryIndex -= 1
                #weightBlend_weightsDictHistory.pop(0)

            #if len(weightBlend_weightsDictHistory) >= weightBlend_maxUndos:
                #weightBlend_weightsDictHistory.pop(-1)

            #outputWeightDict={}
            #for vertIndex in selectionIndices:
                #outputWeightDict[vertIndex] = {}
                #weightTotal = 0.0
                #for weightIndex in inputWeightDict[vertIndex]:
                    #outputWeightDict[vertIndex][weightIndex] = inputWeightDict[vertIndex][weightIndex]
                    #weightTotal += outputWeightDict[vertIndex][weightIndex]

            #weightBlend_weightsDictHistory.insert(0, (outputWeightDict, skinCluster))

#def undoWeightBlend():
    #global weightsDict
    #global weightBlend_weightsDictHistory
    #global weightBlend_weightsDictHistoryIndex

    ### if there is something to undo
    #if not len(weightBlend_weightsDictHistory)-1  <  weightBlend_weightsDictHistoryIndex+1:
        #weightBlend_weightsDictHistoryIndex += 1
        #historicalWeightDict, historicalSkinCluster = weightBlend_weightsDictHistory[weightBlend_weightsDictHistoryIndex]

        #strSkinCluster = str(historicalSkinCluster)
        #for vertIndex in historicalWeightDict:
            #strVertIndex = str(vertIndex)

            #cmds.removeMultiInstance('%s.wl[%s]' % (strSkinCluster, strVertIndex,))
            #for weightIndex in historicalWeightDict[vertIndex]:
                #cmds.setAttr('%s.wl[%s].w[%s]' % (strSkinCluster, strVertIndex, str(weightIndex)), historicalWeightDict[vertIndex][weightIndex])
    #else:
        #pymel.warning('weightBlender has nothing left to redo')


#def redoWeightBlend():
    #global weightBlend_weightsDictHistory
    #global weightBlend_weightsDictHistoryIndex

    #if not weightBlend_weightsDictHistoryIndex-1 < 0:
        #weightBlend_weightsDictHistoryIndex -= 1
        #historicalWeightDict, historicalSkinCluster = weightBlend_weightsDictHistory[weightBlend_weightsDictHistoryIndex]

        #strSkinCluster = str(historicalSkinCluster)
        #for vertIndex in historicalWeightDict:
            #strVertIndex = str(vertIndex)

            #cmds.removeMultiInstance('%s.wl[%s]' % (strSkinCluster, strVertIndex,))
            #for weightIndex in historicalWeightDict[vertIndex]:
                #cmds.setAttr('%s.wl[%s].w[%s]' % (strSkinCluster, strVertIndex, str(weightIndex)), historicalWeightDict[vertIndex][weightIndex])
    #else:
        #pymel.warning('weightBlender has nothing left to undo')

# ----------------------------------------------------------------------------------------------------------------

def getCurrentCamera():
    """Returns the current cammera with focus"""
    panelUnderPointer = pymel.getPanel( underPointer=True )
    camera = 'persp'
    if panelUnderPointer:
        if 'modelPanel' in panelUnderPointer:
            currentPanel = pymel.getPanel(withFocus=True)
            currentPanel = currentPanel.split('|')[-1]
            camera = pymel.modelPanel(currentPanel, query=True, camera=True)

    return camera


def getMMatrix(transform, matrixType='worldMatrix'):
    """Returns transform as MMatrix"""
    matrix = pymel.getAttr(transform+".%s" % matrixType)
    matrixList = []
    for row in matrix:
        for n in row:
            matrixList.append(n)

    mMatrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList(matrixList, mMatrix)
    return mMatrix




def normalizeVector(vector):
    return [ vector[i]/magnitudeOfVector(vector)  for i in range(len(vector)) ]


def magnitudeOfVector(vector):
    return math.sqrt( sum( vector[i]*vector[i] for i in range(len(vector)) ) )




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
    transform = None
    skinCluster = None

    if log:print("input", input)


    if 'transform' in node.nodeType(inherited=True):
        transform = node

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
    return skinCluster

