from maya import cmds
import maya.OpenMaya as OpenMaya

import maya.mel as mel





class weightValueDragger(object):
    # You will want to set add cmds.setToolTo("weightValueDragger") in your hotkeys to be able to use this feature
    CONTEXTNAME = "weightValueDragger"
    def __init__(self):
        self.weightAttr = ""

    def clickAndMoveCommand(self):

        Context = "weightValueDragger"
        # self.currentContext = cmds.currentCtx(q=True)
        #
        # self.weightAttr=cmds.artAttrCtx(self.currentContext, attrSelected=True, q=True)

        def getFirstClick():
            vec = tuple(cmds.draggerContext(Context, query=1, anchorPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])
            print "Weight attr", self.weightAttr

        def getCursorPosition():
            vec = tuple(cmds.draggerContext(Context, query=1, dragPoint=1))
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])
            dotProd = OpenMaya.MVector(self.vectorStart- self.vectorEnd).normal()*(OpenMaya.MVector(-1.0, 0.0, 0.0))
            length = OpenMaya.MVector(self.vectorStart- self.vectorEnd).length()
            posNeg = -1

            if dotProd >= 0:
                posNeg = 1
            self.wt = (length*.001)*posNeg
            # self.setWeights()
            setWeightsOnSelectedAcculmulative(self.weightAttr, self.wt)

            vec = tuple(cmds.draggerContext(Context, query=1, dragPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])

        def releaseClick():
            self.vectorStart = OpenMaya.MVector(0.0, 0.0, 0.0)
            self.wt = 0.0
            cmds.setToolTo("selectSuperContext")
            #cmds.setToolTo(self.currentContext)

            # mel.eval('artSetToolAndSelectAttr( "'+ self.currentContext +'", "' + self.weightAttr + '" );')

        def holdCommand():
            vec = tuple(cmds.draggerContext(Context, query=1, anchorPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])

        if cmds.draggerContext(Context, exists=True):
            cmds.deleteUI(Context)

        cmds.draggerContext(Context, um="all", pressCommand=getFirstClick, dragCommand=getCursorPosition, name=Context,
                            cursor='crossHair', sp="screen", pr="viewPlane", hc= holdCommand, rc=releaseClick)
        cmds.setToolTo(Context)


def setWeightsOnSelectedAcculmulative(weightAttr, weightValue):
    """
    Accumulates a weight on selected points.  Adds or subtracts weight to the currently selected point(s)
    :param self:
    :param weightAttr:
    :param weightValue:
    :return:
    """
    print weightAttr
    # curr = cmds.currentCtx(q=True)
    # weightAttr=cmds.artAttrCtx(curr, attrSelected=True, q=True)
    weightAttrSplit = weightAttr.split(".")
    # ---get deformer
    deformer = weightAttr.split(".")[1]
    geo = cmds.deformer(deformer, q=True, g=True)
    geoTransform = [cmds.listRelatives(i, parent=True)[0] for i in geo]
    # ---make sure selected are points, and are in the deformer
    selected = cmds.ls(sl=True, fl=True)
    vtx = [i for i in selected if ".vtx[" in i]
    cv = [i for i in selected if ".cv[" in i]
    points = vtx + cv
    finalPoints = []

    weightAttrs = []
    allWeightValues = []
    for i in range(len(geoTransform)):
        weightAttrs.append(
            weightAttrSplit[1] + "." + weightAttrSplit[2] + "s[" + str(i) + "]." + weightAttrSplit[2])
        allWeightValues.append(cmds.getAttr(weightAttrs[i]))

    final_points_indexes = []
    initial_values = []
    for i in range(len(geoTransform)):
        tmp_final_idx = []
        tmp_value = []
        for j in range(len(points)):
            if geoTransform[i] in points[j]:
                finalPoints.append(points[j])
                idx = points[j].split("[")[1]
                idx = int(idx.split("]")[0])
                tmp_final_idx.append(idx)
                tmp_value.append(allWeightValues[i][idx])
        final_points_indexes.append(tmp_final_idx)
        initial_values.append(tmp_value)
    for i in range(len(geoTransform)):
        for j in range(len(final_points_indexes[i])):
            clampedWeight = initial_values[i][j] + weightValue
            if clampedWeight > 1.0:
                clampedWeight = 1.0
            if clampedWeight < 0.0:
                clampedWeight = 0.0
            allWeightValues[i][final_points_indexes[i][j]] = clampedWeight
    for i in range(len(allWeightValues)):
        cmds.setAttr(weightAttrs[i], allWeightValues[i], typ='doubleArray')
    cmds.refresh(force=True)


def weightAverage(weightAttribute="LHWeightDeformer.C_testFace_SLD.lMouthUDWeight", between=True):
    if not cmds.selectPref(q=True, trackSelectionOrder=True):
        print "turning on tracking selection order"
        cmds.selectPref(trackSelectionOrder=True)

    # def weightAverage(weightAttribute="LHWeightDeformer.C_testFace_SLD.lSideWeight"):
    """ Please only select points from one mesh at a time for now"""

    weightAtrSplit = weightAttribute.split(".")
    weightAttrName = weightAtrSplit[1] + "." + weightAtrSplit[2] + "s[" + str(0) + "]." + weightAtrSplit[2]
    currentWeights = cmds.getAttr(weightAttrName)
    selected = cmds.ls(orderedSelection=True, fl=True)

    # Get Mesh
    mesh = selected[0].split(".")[0]
    meshNode = OpenMaya.MSelectionList()
    meshNode.add(mesh)
    meshPath = OpenMaya.MDagPath()
    meshNode.getDagPath(0, meshPath)
    iterVerts = OpenMaya.MItMeshVertex(meshPath)

    # Get Points
    vtx = [i for i in selected if ".vtx[" in i]
    cv = [i for i in selected if ".cv[" in i]
    points = vtx + cv

    # if between anchor the start and end point by removing from list
    # get neighbours
    indexes = [int(x.split("]")[0].split("[")[1]) for x in points]


    # print indexes
    if between:
        # indexes = [indexes[i] for i in range(len(indexes)) if i != 0 and i < len(indexes)-1]
        print indexes
        indexes = indexes[1:-1]
        print indexes

    dag = OpenMaya.MDagPath()
    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    currentIndex = util.asIntPtr()
    connectedVertIDs = OpenMaya.MIntArray()

    for idx in indexes:
        # print idx
        # Get neighbors, first set to
        iterVerts.setIndex(idx, currentIndex)

        iterVerts.getConnectedVertices(connectedVertIDs)
        # print "BEFOREE!!!", idx
        # remove any selected verts from the connectedVerts
        cleanConnected = [x for x in connectedVertIDs if x not in indexes]
        util.createFromInt(idx)
        currentIndex = util.asIntPtr()
        try:
            connectedWeights = [currentWeights[i] for i in cleanConnected]
            w = sum(connectedWeights)/len(connectedWeights)
            currentWeights[idx] = w
            # print idx
            # print idx
        except:
            continue

        print w

    currentWeights = cmds.setAttr(weightAttrName, currentWeights, typ='doubleArray')


        # get connected, then remove any from current


    #print [x.split("]")[0] + x.split("]")[0].split("[")[1] for x in points]
# ##############################
def weightAverageAll(weightAttribute="LHWeightDeformer.C_testFace_SLD.lMouthUDWeight", iterAmount = 4):
    if not cmds.selectPref(q=True, trackSelectionOrder=True):
        print "turning on tracking selection order"
        cmds.selectPref(trackSelectionOrder=True)
    # def weightAverage(weightAttribute="LHWeightDeformer.C_testFace_SLD.lSideWeight"):
    """ Please only select points from one mesh at a time for now"""
    weightAtrSplit = weightAttribute.split(".")
    weightAttrName = weightAtrSplit[1] + "." + weightAtrSplit[2] + "s[" + str(0) + "]." + weightAtrSplit[2]
    currentWeights = cmds.getAttr(weightAttrName)
    selected = cmds.ls(sl=True, fl=True)

    # Get Mesh
    mesh = selected[0].split(".")[0]
    meshNode = OpenMaya.MSelectionList()
    meshNode.add(mesh)
    meshPath = OpenMaya.MDagPath()
    meshNode.getDagPath(0, meshPath)
    iterVerts = OpenMaya.MItMeshVertex(meshPath)

    # Get Points
    vtx = [i for i in selected if ".vtx[" in i]
    cv = [i for i in selected if ".cv[" in i]
    points = vtx + cv

    # if between anchor the start and end point by removing from list
    # get neighbours
    indexes = [int(x.split("]")[0].split("[")[1]) for x in points]


    dag = OpenMaya.MDagPath()
    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    currentIndex = util.asIntPtr()
    connectedVertIDs = OpenMaya.MIntArray()
    for i in range(iterAmount):
        for idx in indexes:
            # print idx
            # Get neighbors, first set to
            iterVerts.setIndex(idx, currentIndex)

            iterVerts.getConnectedVertices(connectedVertIDs)
            # print "BEFOREE!!!", idx
            # remove any selected verts from the connectedVerts
            cleanConnected = [x for x in connectedVertIDs if x not in indexes]
            util.createFromInt(idx)
            currentIndex = util.asIntPtr()
            try:
                connectedWeights = [currentWeights[i] for i in connectedVertIDs]
                w = sum(connectedWeights)/len(connectedWeights)
                currentWeights[idx] = w
                # print idx
                # print idx
            except:
                continue

            print w
        try:
            currentWeights = cmds.setAttr(weightAttrName, currentWeights, typ='doubleArray')
        except:
            pass

        # get connected, then remove any from current


    #print [x.split("]")[0] + x.split("]")[0].split("[")[1] for x in points]
def getPointBoundingBox():
    "Get a bounding box based on points, gets the 2 furthest points"
    points = cmds.ls(sl=True, fl=True)
    startPos = ""
    startPoint =""
    endPos = ""
    endPoint=""
    for p in range(len(points)):
        if p == 0:
            startPos = cmds.pointPosition(points[p], w=True)
            startPoint = points[p]
            continue
        if p == 1:
            endPos = cmds.pointPosition(points[p], w=True)
            endPoint = points[p]
        currentLength = OpenMaya.MVector(OpenMaya.MVector(startPos[0], startPos[1], startPos[2])
                                         - OpenMaya.MVector(endPos[0], endPos[1], endPos[2])).length()

        currentPos = cmds.pointPosition(points[p], w=True)
        currentPoint = points[p]
        # test start
        if (currentLength < OpenMaya.MVector(OpenMaya.MVector(currentPos[0],currentPos[1],currentPos[2])
                                         -OpenMaya.MVector(endPos[0],endPos[1],endPos[2])).length()):
            startPos = cmds.pointPosition(points[p], w=True)
            startPoint = points[p]
            continue
        if (currentLength < OpenMaya.MVector(OpenMaya.MVector(startPos[0], startPos[1], startPos[2])
                                                 - OpenMaya.MVector(currentPos[0], currentPos[1], currentPos[2])).length()):
            endPos = cmds.pointPosition(points[p], w=True)
            endPoint = points[p]
            continue

    return startPoint, endPoint
