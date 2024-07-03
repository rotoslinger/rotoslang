from maya import cmds
import maya.OpenMaya as OpenMaya
# from plugins import setVertexWeightColor
# import maya.mel as mel





class weightValueDragger(object):
    # You will want to set add cmds.setToolTo("weightValueDragger") in your hotkeys to be able to use this feature
    CONTEXTNAME = "weightValueDragger"
    print("NEW CONTEXT")
    def __init__(self):
        # self.weightAttr = "LHWeightDeformer.C_testFace_SLD.lSideWeight"
        self.weightAttr = ""
        self.vertexColorWeightVis= True
        self.toggleVisOnDrag= False
        self.originalWeightValues=""
        # self.vertexWeightVis= False

    def clickAndMoveCommand(self):

        Context = "weightValueDragger"
        def getFirstClick():
            vec = tuple(cmds.draggerContext(Context, query=1, anchorPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])

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
            allWeightValues = setWeightsOnSelectedAcculmulative(self.weightAttr, self.wt)
            if self.vertexColorWeightVis:
                setVertexColorsToWeightValue(allWeightValues, True)
            vec = tuple(cmds.draggerContext(Context, query=1, dragPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])

        def releaseClick():
            self.vectorStart = OpenMaya.MVector(0.0, 0.0, 0.0)
            self.wt = 0.0
            sel = cmds.ls(sl=True, fl=True)
            geo = sel[0].split(".")[0]
            if self.toggleVisOnDrag:
                cmds.setAttr(geo + '.displayColors', False)

        def holdCommand():
            vec = tuple(cmds.draggerContext(Context, query=1, anchorPoint=1 ))
            self.vectorStart = OpenMaya.MVector(vec[0], vec[1], vec[2])
            self.vectorEnd = OpenMaya.MVector(vec[0], vec[1], vec[2])

        if cmds.draggerContext(Context, exists=True):
            cmds.deleteUI(Context)

        cmds.draggerContext(Context, um="sequence", pressCommand=getFirstClick, dragCommand=getCursorPosition, name=Context,
                            cursor='crossHair', sp="screen", pr="viewPlane", rc=releaseClick)
        cmds.setToolTo(Context)
        if self.weightAttr and self.vertexColorWeightVis:
            allWeightValues = getAllWeightValues(self.weightAttr)[0]
            setVertexColorsToWeightValue(allWeightValues, True)

def turnOnVertexColor(weightAttr, *args):
    if weightAttr:
        allWeightValues = getAllWeightValues(weightAttr)[0]
        setVertexColorsToWeightValue(allWeightValues, True)
        sel = cmds.ls(sl=True, fl=True)
        geo = sel[0].split(".")[0]
        cmds.setAttr(geo + '.displayColors', True)

def turnOffVertexColor(*args):
    sel = cmds.ls(sl=True, fl=True)
    if not sel:
        return
    geo = sel[0].split(".")[0]
    cmds.setAttr(geo + '.displayColors', False)



def getMFnMesh(geo):
    meshNode = OpenMaya.MSelectionList()
    meshNode.add(geo)
    meshPath = OpenMaya.MDagPath()
    meshNode.getDagPath(0, meshPath)
    return OpenMaya.MFnMesh(meshPath)


def setWeightsOnSelectedAcculmulative(weightAttr="LHWeightDeformer.C_testFace_SLD.lSideWeight", weightValue=0.0):
    """
    Used for weight dragging
    Accumulates a weight on selected points.  Adds or subtracts weight to the currently selected point(s)
    :param self:
    :param weightAttr:
    :param weightValue:
    :return:
    """
    # curr = cmds.currentCtx(q=True)
    # weightAttr=cmds.artAttrCtx(curr, attrSelected=True, q=True)
    allWeightValues, finalPoints, geoTransform, points, weightAttrs = getAllWeightValues(weightAttr)

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
    return allWeightValues


def getAllWeightValues(weightAttr):
    weightAttrSplit = weightAttr.split(".")
    if len(weightAttrSplit) == 2:
        # ---get deformer
        geo = [weightAttrSplit[0]]

    elif not len(weightAttrSplit) > 2:
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
        if len(weightAttrSplit) == 2:
            weightAttrs.append( weightAttr)
        elif not len(weightAttrSplit) > 2:
            weightAttrs.append( weightAttrSplit[1] + "." + weightAttrSplit[2] + "s[" + str(i) + "]." + weightAttrSplit[2])
        allWeightValues.append(cmds.getAttr(weightAttrs[i]))
    return allWeightValues, finalPoints, geoTransform, points, weightAttrs


def weightAverageSelectionBorder(weightAttribute="LHWeightDeformer.C_testFace_SLD.lMouthUDWeight"):
    componentMode = cmds.selectMode(q=True, component=True)
    sel = cmds.ls(sl=True, fl=True)
    trackComponentSelectionOrder()

    # def weightAverage(weightAttribute="LHWeightDeformer.C_testFace_SLD.lSideWeight"):
    """ Please only select points from one mesh at a time for now"""

    currentWeights, indicies, iterVerts, weightAttrName = getWeightsFromAttribute(weightAttribute)

    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    currentIndex = util.asIntPtr()
    connectedVertIDs = OpenMaya.MIntArray()

    for idx in indicies:
        # Get neighbors, first set to
        iterVerts.setIndex(idx, currentIndex)

        iterVerts.getConnectedVertices(connectedVertIDs)
        # remove any selected verts from the connectedVerts
        cleanConnected = [x for x in connectedVertIDs if x not in indicies]
        util.createFromInt(idx)
        currentIndex = util.asIntPtr()
        try:
            currentWeights[idx] = averageWeightlist(cleanConnected, currentWeights, idx)
        except:
            continue

    cmds.setAttr(weightAttrName, currentWeights, typ='doubleArray')
    if componentMode:
        cmds.selectMode(component=True)
        cmds.hilite(sel[0].split(".")[0])


def averageWeightlist(weightListFilter, weightlist, currentPointIndex):
    """
    Takes a large number of weight values, averages them, and sets them to a single point.  You must give the entire
    list of points weights, and a list of indicies to get the information.  Returns the single point weight value.
    :param weightListFilter: a list of indicies to average (might gathering weights from points 1,4,5 only, or could be 0:-1 (the whole list))
    :param weightlist: an entire list of weights for an object (a value for every point in a mesh)
    :param currentPointIndex: the current point where the average weights will be set
    :return:
    """
    connectedWeights = [weightlist[i] for i in weightListFilter]
    w = sum(connectedWeights) / len(connectedWeights)
    weightlist[currentPointIndex] = w
    return weightlist[currentPointIndex]


def weightAverageAll(weightAttribute="LHWeightDeformer.C_testFace_SLD.lMouthUDWeight", iterAmount = 4):
    componentMode = cmds.selectMode(q=True, component=True)
    sel = cmds.ls(sl=True, fl=True)
    if not weightAttribute:
        return
    trackComponentSelectionOrder()
    # def weightAverage(weightAttribute="LHWeightDeformer.C_testFace_SLD.lSideWeight"):
    """ Please only select points from one mesh at a time for now"""
    currentWeights, indicies, iterVerts, weightAttrName = getWeightsFromAttribute(weightAttribute)

    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    currentIndex = util.asIntPtr()
    connectedVertIDs = OpenMaya.MIntArray()
    for i in range(iterAmount):
        for idx in indicies:
            # print idx
            # Get neighbors, first set to
            iterVerts.setIndex(idx, currentIndex)
            iterVerts.getConnectedVertices(connectedVertIDs)
            # remove any selected verts from the connectedVerts
            cleanConnected = [x for x in connectedVertIDs if x not in indicies]
            util.createFromInt(idx)
            currentIndex = util.asIntPtr()
            try:
                currentWeights[idx] = averageWeightlist(connectedVertIDs, currentWeights, idx)

                # connectedWeights = [currentWeights[i] for i in connectedVertIDs]
                # w = sum(connectedWeights)/len(connectedWeights)
                # currentWeights[idx] = w
            except:
                continue
        try:
            cmds.setAttr(weightAttrName, currentWeights, typ='doubleArray')
        except:
            pass
    if componentMode:
        cmds.selectMode(component=True)
        cmds.hilite(sel[0].split(".")[0])

                # get connected, then remove any from current





def gradientWeightsBetween2Points(weightAttribute="LHWeightDeformer.C_testFace_SLD.lMouthUDWeight",
                                  flattenTx=False, flattenTy=False, flattenTz=False, calcDeformed=False):

    # preserve selection
    if not weightAttribute:
        return

    componentMode = cmds.selectMode(q=True, component=True)

    if not calcDeformed:
        deformer = weightAttribute.split(".")[1]
        cmds.setAttr(deformer + ".envelope", 0)

    sel = cmds.ls(sl=True, fl=True)

    currentWeights, indicies, mesh, weightAttrName = getWeightsFromAttribute(weightAttribute, OMObjectType="MFnMesh")
    startPoint, endPoint = getPointBoundingBox(flattenTx, flattenTy, flattenTz)

    endPointidx, point1, point2, points, startPointIdx = sortPoints(currentWeights, endPoint, startPoint)



    # create curve between 2 points
    curve = cmds.curve(d=True, p=[point1, point2], k=[0, 1])

    curveNode = OpenMaya.MSelectionList()
    curveNode.add(curve)
    curvePath = OpenMaya.MDagPath()
    curveNode.getDagPath(0, curvePath)
    fnCurve = OpenMaya.MFnNurbsCurve(curvePath)


    indicies.remove(startPointIdx)
    indicies.remove(endPointidx)
    gttrPoint = OpenMaya.MPoint()
    util = OpenMaya.MScriptUtil()
    # util.createFromInt(0)
    param = util.asDoublePtr()
    for id in indicies:
        mesh.getPoint(id, gttrPoint, OpenMaya.MSpace.kWorld)
        fnCurve.closestPoint(gttrPoint, param, OpenMaya.MSpace.kWorld)
        percent = util.getDouble(param)
        # w = modulateBetween2ValuesByFactor(startPointWeightValue, endPointWeightValue, percent)
        w = modulateBetween2ValuesByFactor(points[1], points[0], percent)
        currentWeights[id] = w
    try:
        cmds.setAttr(weightAttrName, currentWeights, typ='doubleArray')
    except:
        pass


    cmds.delete(curve)
    if not calcDeformed:
        deformer = weightAttribute.split(".")[1]
        cmds.setAttr(deformer + ".envelope", 1)

    cmds.select(sel, r=True)
    if componentMode:
        cmds.selectMode(component=True)
        cmds.hilite(sel[0].split(".")[0])


def sortPoints(currentWeights, endPoint, startPoint):
    pointDataDict = {}
    startPointIdx = getPointIndicies(startPoint)
    endPointidx = getPointIndicies(endPoint)
    startPointWeightValue = currentWeights[startPointIdx]
    endPointWeightValue = currentWeights[endPointidx]
    points = sorted([startPointWeightValue, endPointWeightValue])
    pointDataDict[startPointWeightValue] = [startPointIdx, startPoint]
    pointDataDict[endPointWeightValue] = [endPointidx, endPoint]
    point1 = cmds.pointPosition(pointDataDict[points[0]][1])
    point2 = cmds.pointPosition(pointDataDict[points[1]][1])
    return endPointidx, point1, point2, points, startPointIdx


def modulateBetween2ValuesByFactor(value1, value2, factor):
    """
    A blend between value1 and value2.  Factor should be between 0-1
    if factor is 0 the result will be value 1 and if the factor is 1 the value would be equal to value2
    A factor of .5 would be right inbetween the two values
    :param value1: a numerical value
    :param value2: a numerical value
    :param factor: a numerical value, should at least  be a float if not a double, needs to be between 0-1
    :return: the output
    """
    return value2 + ((value1 - value2) * factor)

def getPointIndicies(point):
    return int(point.split("]")[0].split("[")[1])


def averageWeightsBetween2Points(weightAttribute="LHWeightDeformer.C_testFace_SLD.lMouthUDWeight",
                                 flattenTx=False, flattenTy=False, flattenTz=False):
    if not weightAttribute:
        return
    currentWeights, indicies, iterVerts, weightAttrName = getWeightsFromAttribute(weightAttribute)
    startPoint, endPoint = getPointBoundingBox(flattenTx, flattenTy, flattenTz)
    startPoint = getPointIndicies(startPoint)
    endPoint = getPointIndicies(endPoint)
    indicies.remove(startPoint)
    indicies.remove(endPoint)
    w = sum([currentWeights[startPoint], currentWeights[endPoint]]) / 2
    for idx in indicies:
        currentWeights[idx] = w
    try:
        cmds.setAttr(weightAttrName, currentWeights, typ='doubleArray')
    except:
        pass


def averageBetweenPoints(weightAttr = "LHWeightDeformer.C_testFace_SLD.lSideWeight"):
    """
    Averages weights between 2 points.  Works best when selecting points on the same edgeloop.
    :param weightAttr: the name of the weight attribute
    :return:
    """
    if not weightAttr:
        return
    returnData = getWeightsFromAttribute(weightAttr)
    currentWeights = returnData[0]
    weightAttrName = returnData[3]
    selEndPoints, points = getPointsBetween()
    startPoint = getPointIndicies(selEndPoints[0])
    endPoint = getPointIndicies(selEndPoints[1])
    indicies = [getPointIndicies(x) for x in points]
    w = sum([currentWeights[startPoint], currentWeights[endPoint]]) / 2
    for idx in indicies:
        currentWeights[idx] = w
    try:
        cmds.setAttr(weightAttrName, currentWeights, typ='doubleArray')
    except:
        pass


def gradientBetweenPoints(weightAttr = "LHWeightDeformer.C_testFace_SLD.lSideWeight", calcDeformed=False):
    """
    Averages weights between 2 points.  Works best when selecting points on the same edgeloop.
    :param weightAttr: the name of the weight attribute
    :return:
    """
    if not weightAttr:
        return

    if not calcDeformed:
        deformer = weightAttr.split(".")[1]
        cmds.setAttr(deformer + ".envelope", 0)


    currentWeights, indicies, mesh, weightAttrName = getWeightsFromAttribute(weightAttr, OMObjectType="MFnMesh")

    selEndPoints, pointsBetween = getPointsBetween()
    # startPointIdx = getPointIndicies(selEndPoints[0])
    # endPointIdx = getPointIndicies(selEndPoints[1])
    selEndPoints = cmds.ls(sl=True, fl=True)


    endPointidx, point1, point2, points, startPointIdx = sortPoints(currentWeights, selEndPoints[1], selEndPoints[0])


    indicies = [getPointIndicies(x) for x in pointsBetween]

    # create curve between 2 points
    curve = cmds.curve(d=True, p=[point1, point2], k=[0, 1])

    curveNode = OpenMaya.MSelectionList()
    curveNode.add(curve)
    curvePath = OpenMaya.MDagPath()
    curveNode.getDagPath(0, curvePath)
    fnCurve = OpenMaya.MFnNurbsCurve(curvePath)

    gttrPoint = OpenMaya.MPoint()
    util = OpenMaya.MScriptUtil()


    # util.createFromInt(0)
    param = util.asDoublePtr()
    for id in indicies:
        mesh.getPoint(id, gttrPoint, OpenMaya.MSpace.kWorld)
        fnCurve.closestPoint(gttrPoint, param, OpenMaya.MSpace.kWorld)
        percent = util.getDouble(param)
        # w = modulateBetween2ValuesByFactor(startPointWeightValue, endPointWeightValue, percent)
        w = modulateBetween2ValuesByFactor(points[1], points[0], percent)
        currentWeights[id] = w
    try:
        cmds.setAttr(weightAttrName, currentWeights, typ='doubleArray')
    except:
        pass


    cmds.delete(curve)
    if not calcDeformed:
        deformer = weightAttr.split(".")[1]
        cmds.setAttr(deformer + ".envelope", 1)

    cmds.select(selEndPoints, r=True)
    cmds.selectMode(component=True)
    cmds.hilite(selEndPoints[0].split(".")[0])



def getPointsBetween():
    selEndPoints = cmds.ls(sl=True, fl=True)
    startPoint = getPointIndicies(selEndPoints[0])
    endPoint = getPointIndicies(selEndPoints[1])
    list = cmds.polySelect('C_body_HI', shortestEdgePath=(startPoint, endPoint), q=True, asSelectString=True)
    points = cmds.polyListComponentConversion(list, toVertex=True)
    points = cmds.ls(points, fl=True)
    points.remove(str(selEndPoints[0]))
    points.remove(str(selEndPoints[1]))
    return selEndPoints, points

def trackComponentSelectionOrder():
    if not cmds.selectPref(q=True, trackSelectionOrder=True):
        print("turning on tracking selection order")
        cmds.selectPref(trackSelectionOrder=True)


def getWeightsFromAttribute(weightAttribute, OMObjectType="MItMeshVertex"):
    """
    :param weightAttribute:
    :return:
    currentWeights: a list of weight values at their current value
    indicies: the indices of the points selected in the viewport
    iterVerts: MItMeshVertex that will be used to find the vertex connections
    weightAttrName: the cleaned up name of the weight attribute
    """
    if not weightAttribute:
        return
    weightAtrSplit = weightAttribute.split(".")
    weightAttrName = weightAtrSplit[1] + "." + weightAtrSplit[2] + "s[" + str(0) + "]." + weightAtrSplit[2]
    currentWeights = cmds.getAttr(weightAttrName)
    selected = cmds.ls(sl=True, fl=True)
    # Get Mesh
    mesh = selected[0].split(".")[0]
    iterVerts = extractOMObject(mesh, OMObjectType)
    # Get Points
    vtx = [i for i in selected if ".vtx[" in i]
    cv = [i for i in selected if ".cv[" in i]
    points = vtx + cv
    # get neighbours
    indicies = [int(x.split("]")[0].split("[")[1]) for x in points]
    return currentWeights, indicies, iterVerts, weightAttrName


def extractOMObject(mayaObject, OMObjectType="MItMeshVertex"):
    meshNode = OpenMaya.MSelectionList()
    meshNode.add(mayaObject)
    meshPath = OpenMaya.MDagPath()
    meshNode.getDagPath(0, meshPath)

    # Getting attributes looks like this: OpenMaya.MItMeshVertex(meshPath)
    iterVerts = getattr(OpenMaya, OMObjectType)
    iterVerts = iterVerts(meshPath)


    return iterVerts


def getPointBoundingBox(flattenTx=False, flattenTy=False, flattenTz=False):
    """
    Get a bounding box based on points, gets the 2 furthest points
    :param flattenTy: If true, will not pay attention to the ty position
    :return:
    """
    print(flattenTx, flattenTy, flattenTz)
    points = cmds.ls(sl=True, fl=True)
    startPos = ""
    startPoint =""
    endPos = ""
    endPoint=""

    xMult = 0.0
    yMult = 0.0
    zMult = 0.0
    startX = 0.0
    endX = 0.0
    startY = 0.0
    endY = 0.0
    startZ = 0.0
    endZ = 0.0

    if not flattenTx:
        xMult = 1.0
    if not flattenTy:
        yMult = 1.0
    if not flattenTz:
        zMult = 1.0

    for p in range(len(points)):
        if p == 0:
            startPos = cmds.pointPosition(points[p], w=True)
            startPos = startPos[0]*xMult, startPos[1]*yMult, startPos[2]*zMult
            startPoint = points[p]
            continue
        if p == 1:
            endPos = cmds.pointPosition(points[p], w=True)
            endPos = endPos[0]*xMult, endPos[1]*yMult, endPos[2]*zMult
            endPoint = points[p]
            continue


        if not flattenTx:
            startX = startPos[0]
            endX = endPos[0]
        if not flattenTy:
            startY = startPos[1]
            endY = endPos[1]

        if not flattenTz:
            startZ = startPos[2]
            endZ = endPos[2]


        currentLength = OpenMaya.MVector(OpenMaya.MVector(startX, startY, startZ)
                                         - OpenMaya.MVector(endX, endY, endZ)).length()
        currentPos = cmds.pointPosition(points[p], w=True)
        currentPos = currentPos[0]*xMult, currentPos[1]*yMult, currentPos[2]*zMult

        # test start

        if not flattenTx:
            startX = currentPos[0]
            endX = endPos[0]
        if not flattenTy:
            startY = currentPos[1]
            endY = endPos[1]
        if not flattenTz:
            startZ = currentPos[2]
            endZ = endPos[2]


        if (currentLength < OpenMaya.MVector(OpenMaya.MVector(startX, startY, startZ)
                                         -OpenMaya.MVector(endX, endY, endZ)).length()):
            startPos = cmds.pointPosition(points[p], w=True)
            startPos = startPos[0]*xMult, startPos[1]*yMult, startPos[2]*zMult
            startPoint = points[p]
            continue

        if not flattenTx:
            startX = startPos[0]
            endX = currentPos[0]
        if not flattenTy:
            startY = startPos[1]
            endY = currentPos[1]
        if not flattenTz:
            startZ = startPos[2]
            endZ = currentPos[2]

        if (currentLength < OpenMaya.MVector(OpenMaya.MVector(startX, startY, startZ)
                                                 - OpenMaya.MVector(endX, endY, endZ)).length()):
            endPos = cmds.pointPosition(points[p], w=True)
            endPos = endPos[0]*xMult, endPos[1]*yMult, endPos[2]*zMult
            endPoint = points[p]
            continue

    return startPoint, endPoint

class stayInPointSelectionMode:
    """
    Assumes you have an active point selection before running
    """
    def __enter__(self):
        self.componentMode = cmds.selectMode(q=True, component=True)
    def __exit__(self):
        if self.componentMode:
            cmds.selectMode(component=True)
            sel = cmds.ls(sl=True, fl=True)
            cmds.hilite(sel[0].split(".")[0])

def setVertexColorsToWeightValue(allWeightValues, displayVertexColors):
    sel = cmds.ls(sl=True, fl=True)
    geo = sel[0].split(".")[0]
    fnMesh = getMFnMesh(geo)
    util = OpenMaya.MScriptUtil()

    # indexList = [util.createFromInt(x).asInPtr() for x in range(len(allWeightValues))]

    # vertexIndexList = OpenMaya.MIntArray(indexList)
    vertexColorList = OpenMaya.MColorArray()

    # Check to see if vertex colors exist
    colors = fnMesh.numColors()
    if not colors:
        fnMesh.createColorSetWithName("weightColors")

    fnMesh.getVertexColors(vertexColorList)

    lenVertexList = vertexColorList.length()
    fnComponent = OpenMaya.MFnSingleIndexedComponent()
    fnComponent.create(OpenMaya.MFn.kMeshVertComponent)
    fnComponent.setCompleteData(lenVertexList);
    vertexIndexList = OpenMaya.MIntArray()
    fnComponent.getElements(vertexIndexList)

    util.asDoublePtr()
    # percent = util.getDouble(param)

    setVertexColors(allWeightValues, fnMesh, vertexColorList, vertexIndexList)

    if displayVertexColors:
        cmds.setAttr(geo+'.displayColors', True)

def setVertexColors(allWeightValues, fnMesh, vertexColorList, vertexIndexList):
    for c in range(vertexColorList.length()):
        # print c
        # print allWeightValues[c]
        vertexColorList[c].r = float(allWeightValues[0][c])
        vertexColorList[c].g = float(allWeightValues[0][c])
        vertexColorList[c].b = float(allWeightValues[0][c])
        vertexColorList[c].a = float(1.0)
    fnMesh.setVertexColors(vertexColorList, vertexIndexList, None)
