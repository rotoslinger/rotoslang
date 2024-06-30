import math, sys
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.OpenMayaAnim as OpenMayaAnim

class LHSlideDeformer(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00004005)

    # tAttrs    
    aSurfaceBase = OpenMaya.MObject()
    aSurface = OpenMaya.MObject()
    aWeightMesh = OpenMaya.MObject()
    # nAttrs
    aRotationAmount = OpenMaya.MObject()
    aScaleAmount = OpenMaya.MObject()
    #### cache attrs #######
    aCachePivots = OpenMaya.MObject() 
    aCacheWeights = OpenMaya.MObject()
    aCacheParams = OpenMaya.MObject()
    aCacheWeightMesh = OpenMaya.MObject()
    aCacheWeightCurves = OpenMaya.MObject()
    aCacheBase = OpenMaya.MObject()
    ######## U ##############
    #U Values
    aUValue = OpenMaya.MObject()
    aUValueParent = OpenMaya.MObject()
    # UWeights
    aUWeights = OpenMaya.MObject()
    aUWeightsParent = OpenMaya.MObject()
    aUWeightsParentArray = OpenMaya.MObject()
    # UAnimCurves
    #UU
    aUAnimCurveU = OpenMaya.MObject()
    aUAnimCurveUParent = OpenMaya.MObject()
    #UV
    aUAnimCurveV = OpenMaya.MObject()
    aUAnimCurveVParent = OpenMaya.MObject()
    
    ######## V ##############
    #U Values
    aVValue = OpenMaya.MObject()
    aVValueParent = OpenMaya.MObject()
    # UWeights
    aVWeights = OpenMaya.MObject()
    aVWeightsParent = OpenMaya.MObject()
    aVWeightsParentArray = OpenMaya.MObject()
    # UAnimCurves
    #UU
    aVAnimCurveU = OpenMaya.MObject()
    aVAnimCurveUParent = OpenMaya.MObject()
    #UV
    aVAnimCurveV = OpenMaya.MObject()
    aVAnimCurveVParent = OpenMaya.MObject()
    
    ######## N ##############
    #N Values
    aNValue = OpenMaya.MObject()
    aNValueParent = OpenMaya.MObject()
    # NWeights
    aNWeights = OpenMaya.MObject()
    aNWeightsParent = OpenMaya.MObject()
    aNWeightsParentArray = OpenMaya.MObject()
    # NAnimCurves
    #NU
    aNAnimCurveU = OpenMaya.MObject()
    aNAnimCurveUParent = OpenMaya.MObject()
    #NV
    aNAnimCurveV = OpenMaya.MObject()
    aNAnimCurveVParent = OpenMaya.MObject()

    ######## R ##############
    #R Values
    aRValue = OpenMaya.MObject()
    aRValueParent = OpenMaya.MObject()
    # RWeights
    aRWeights = OpenMaya.MObject()
    aRWeightsParent = OpenMaya.MObject()
    aRWeightsParentArray = OpenMaya.MObject()
    # RAnimCurves
    #RU
    aRAnimCurveU = OpenMaya.MObject()
    aRAnimCurveUParent = OpenMaya.MObject()
    #RV
    aRAnimCurveV = OpenMaya.MObject()
    aRAnimCurveVParent = OpenMaya.MObject()
    #R Pivots
    aRPivot = OpenMaya.MObject()
    aRPivotArray = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)
        #----No Cache
        self.allValsArray = []
        #----Cache vars
        # rot cache
        self.rotatePivots = []
        self.rotUParams = []
        self.rotVParams = []
        # weight cache
        self.allWeightsArray = [0.0]
        # cache weight mesh
        self.uCoord = []
        self.vCoord = []
        self.intersectYN = []
        self.weightMeshCheck = 0
        # cache anim curves
        self.allUFnCurvesArray = []
        self.allUTimeOffsetArray = []
        self.allUTimeLengthArray = []
        self.allVFnCurvesArray = []
        self.allVTimeOffsetArray = []
        self.allVTimeLengthArray = []
        self.allUAnimCurveWeights = []
        self.allVAnimCurveWeights = []
        # cache params
        self.slideUVBasePt = []
        self.slideUBasePtParam = []
        self.slideVBasePtParam = []
        # cache base surface
        self.uMinParam = 0.0
        self.uMaxParam = 0.0
        self.vMinParam = 0.0
        self.vMaxParam = 0.0
        self.rotMatrix = []

####################################################
######## get anim curves ##########################
####################################################

    ''' get anim curves for weighting '''
    def getAnimCurves(self, animCurveParent, animCurveChild):
        thisNode = self.thisMObject();
        returnAnimCurve= []
        returnTimeOffset= []
        returnTimeLength= []
        parentPlug = OpenMaya.MPlug(thisNode, animCurveParent )
        count = parentPlug.numConnectedChildren()
        
        curveIndex = OpenMaya.MIntArray()
        parentPlug.getExistingArrayAttributeIndices(curveIndex)
        for i in curveIndex:
            childPlug = parentPlug.connectionByPhysicalIndex(curveIndex[i])
            oChild = childPlug.child(0)
            oChild.asFloat()
            fnAnimCurve = OpenMayaAnim.MFnAnimCurve(oChild)
            numKeys = fnAnimCurve.numKeys()
            timeAtFirstKey = fnAnimCurve.time(0)
            timeAtLastKey = fnAnimCurve.time(numKeys-1)
            timeStart = timeAtFirstKey.value() 
            timeEnd = timeAtLastKey.value()
            tTimeOff = timeStart * -1
            tTimeLength = timeEnd + tTimeOff
            tCurve = fnAnimCurve
            returnAnimCurve.append(tCurve)
            returnTimeOffset.append(tTimeOff)
            returnTimeLength.append(tTimeLength)

        return returnAnimCurve, returnTimeOffset, returnTimeLength

####################################################
######## Deform ###################################
####################################################

    def deform(self, data, itGeo, localToWorldMatrix, mIndex):
        thisNode = self.thisMObject()
        Envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
        envelope = data.inputValue(Envelope).asFloat()
        if envelope == 0:
            return
        # get number of geoms being deformed and specific index
        # this is important because indices may get scrambled or reordered,
        # if geometry is deleted.
        # also important for caching, without this information, only the first
        # geom will cache
        
        geomPlug = OpenMaya.MPlug(thisNode, OpenMayaMPx.cvar.MPxDeformerNode_input )
        geomIndices = OpenMaya.MIntArray()
        geomPlug.getExistingArrayAttributeIndices(geomIndices)
        # geomCount = geomIndices.length()
        
        # we want to get the highest index of connected geometry plus 1
        
        # this is will be the size of all cache arrays
        # for example if we have 4 pieces of geo all cache arrays
        # will have a length of 4
        
        # even if geometry indexes 1-3 is deleted, and index 4 still exists,
        # the cache arrays will still have a length of 4, but index 1-3 will
        # contain no information
        
        # this is hacky, but it keeps the deformer stable, and the performance
        # hit is miniscule so it doesn't even matter

        # the reason to take this precaution is because the Maya Api mpxdeformer
        # iterates over multiple pieces of geometry based on input connection
        # indices which are represented by the mIndex argument
        # you can think of the mIndex as a sort of geometry ID 
        # it is how maya determines which piece of geomtry it is deforming
        # (if a deformer has multiple geometry connections) and it is also
        # how I determine the order of weight connections, so it is very
        # important that the mIndex never gets reordered, even if existing
        # geometry gets deleted.
        
        # highest index + 1
        numIndex = max(geomIndices) + 1
#                 
        # get attrs
        rotationAmount = data.inputValue(LHSlideDeformer.aRotationAmount).asFloat()
        scaleAmount = data.inputValue(LHSlideDeformer.aScaleAmount).asFloat()
        # cache attrs
        cachePivotsAmt = data.inputValue(LHSlideDeformer.aCachePivots).asFloat()
        cacheWeightsAmt = data.inputValue(LHSlideDeformer.aCacheWeights).asFloat()
        cacheWeightMeshAmt = data.inputValue(LHSlideDeformer.aCacheWeightMesh).asFloat()
        cacheWeightCurvesAmt = data.inputValue(LHSlideDeformer.aCacheWeightCurves).asFloat()
        cacheParamsAmt = data.inputValue(LHSlideDeformer.aCacheParams).asFloat()
        cacheBaseAmt = data.inputValue(LHSlideDeformer.aCacheBase).asFloat()
        # try to get surface connections
        try:
            oSurface = data.inputValue(LHSlideDeformer.aSurface).asNurbsSurfaceTransformed()
            oSurfaceBase = data.inputValue(LHSlideDeformer.aSurfaceBase).asNurbsSurfaceTransformed()
        except:
            pass
        if oSurface.isNull() or oSurfaceBase.isNull():
            return
        
        #Surface Base
        fnSurfaceBase = OpenMaya.MFnNurbsSurface( oSurfaceBase )
    
        # get Surface
        fnSurface = OpenMaya.MFnNurbsSurface( oSurface )
        #############################################
        ####   get all attrVals (can't cache)    ####
        #############################################
        allValParents = [LHSlideDeformer.aUValueParent,
                         LHSlideDeformer.aVValueParent,
                         LHSlideDeformer.aNValueParent,
                         LHSlideDeformer.aRValueParent]
        allValChildren = [LHSlideDeformer.aUValue,
                          LHSlideDeformer.aVValue,
                          LHSlideDeformer.aNValue,
                          LHSlideDeformer.aRValue]
        allValsArray = []
        for i in range(len(allValParents)):
            arrayHandle = OpenMaya.MArrayDataHandle(data.inputArrayValue( allValParents[i] ))
            count = arrayHandle.elementCount()
            tmpValArray = []
            for i in range(count):
                arrayHandle.jumpToElement(i)
                tmpValArray.append(arrayHandle.inputValue().child( allValChildren[i] ).asFloat())
            allValsArray.append(tmpValArray)

        ##################################
        ####       loop variables     ####
        ##################################
    
#         # curve Param
#         fnDouble = OpenMaya.MScriptUtil()
#         fnDouble.createFromDouble(0.0)
#         fnParam = fnDouble.asDoublePtr()

        # uParam
        fnUDouble = OpenMaya.MScriptUtil()
        fnUDouble.createFromDouble(0.0)
        fnUParam = fnUDouble.asDoublePtr()
        # vParam
        fnVDouble = OpenMaya.MScriptUtil()
        fnVDouble.createFromDouble(0.0)
        fnVParam = fnVDouble.asDoublePtr()
        #uMin
        fnUMinDouble = OpenMaya.MScriptUtil()
        fnUMinDouble.createFromDouble(0.0)
        fnUMinParam = fnUMinDouble.asDoublePtr()
        #uMax
        fnUMaxDouble = OpenMaya.MScriptUtil()
        fnUMaxDouble.createFromDouble(0.0)
        fnUMaxParam = fnUMaxDouble.asDoublePtr()
        #vMin
        fnVMinDouble = OpenMaya.MScriptUtil()
        fnVMinDouble.createFromDouble(0.0)
        fnVMinParam = fnVMinDouble.asDoublePtr()
        #vMax
        fnVMaxDouble = OpenMaya.MScriptUtil()
        fnVMaxDouble.createFromDouble(0.0)
        fnVMaxParam = fnVMaxDouble.asDoublePtr()
        #UV pt
        slideUVPoint = OpenMaya.MPoint()
#         rotUVPoint = OpenMaya.MPoint()

        fakePt = OpenMaya.MPoint()
        fakePt2 = OpenMaya.MVector(0.0,0.0,0.0)
        fnUVec = OpenMaya.MVector(0.0,0.0,0.0)
        fnVVec = OpenMaya.MVector(0.0,0.0,0.0)
        fakeVecU = OpenMaya.MVector(0.0,0.0,0.0)
        fakeVecV = OpenMaya.MVector(0.0,0.0,0.0)
        xVec = OpenMaya.MVector(0.0,0.0,0.0)
        yVec = OpenMaya.MVector(0.0,0.0,0.0)
        zVec = OpenMaya.MVector(0.0,0.0,0.0)
        xVecBase = OpenMaya.MVector(0.0,0.0,0.0)
        yVecBase = OpenMaya.MVector(0.0,0.0,0.0)
        zVecBase = OpenMaya.MVector(0.0,0.0,0.0)
        BaseMatrix = OpenMaya.MMatrix()
        DriveMatrix = OpenMaya.MMatrix()

        weightMatrix = OpenMaya.MMatrix()

        UDouble = OpenMaya.MScriptUtil()
        UDouble.createFromDouble(0)
        U = UDouble.asDoublePtr()

        VDouble = OpenMaya.MScriptUtil()
        VDouble.createFromDouble(0)
        V = VDouble.asDoublePtr()
        u = 0
        v = 0
        fakeDouble3 = 0
        hitYN = None
        resultPt = OpenMaya.MPoint()
        curveW = 0.0
        weightPt = OpenMaya.MPoint(0.0,0.0,0.0)
        intersectPoint =  OpenMaya.MPoint()

        pArray = [0,0]
        x1 = OpenMaya.MScriptUtil()
        x1.createFromList( pArray, 2 )
        uvCoord = x1.asFloat2Ptr()

        fnMinDouble = OpenMaya.MScriptUtil()
        fnMinDouble.createFromDouble(0.0)
        fnMinParam = fnMinDouble.asDoublePtr()

        fnMaxDouble = OpenMaya.MScriptUtil()
        fnMaxDouble.createFromDouble(0.0)
        fnMaxParam = fnMaxDouble.asDoublePtr()
        paramPoint = OpenMaya.MPoint(0.0,0.0,0.0)


        geomArrayHandle = data.inputArrayValue(geomPlug)
                
        # cache weight Mesh----
        # only worry about the weight mesh at scene load/mesh connection,
        # or if weight mesh caching is off
        oWeightMesh = data.inputValue(LHSlideDeformer.aWeightMesh).asMeshTransformed()
        self.weightMeshCheck = OpenMaya.MPlug(thisNode, LHSlideDeformer.aWeightMesh )
        if (self.weightMeshCheck.isConnected()):
            self.weightMeshCheck = 1
        else:
            self.weightMeshCheck = 0    
        
        # Weight Mesh
        if self.weightMeshCheck == 1:
            self.fnWeightMesh = OpenMaya.MFnMesh( oWeightMesh )
        
        if len(self.uCoord) < numIndex or cacheWeightMeshAmt == 0:
        # try to get weight mesh connections
            # cache weight Mesh
            if self.weightMeshCheck == 1:
                weightIntersect = OpenMaya.MMeshIntersector()
                weightIntersect.create(oWeightMesh, weightMatrix)
                #----dump any prexisting info
                self.uCoord = []
                self.vCoord = []
                self.intersectYN = []
                
#                 geomArrayHandle = data.inputArrayValue(geomPlug)
                for i in range(numIndex):
                    try:
                        geomArrayHandle.jumpToElement( i )
                        success = 1
                    except:
                        success = 0
                    # if you find a connection, get the geometry
                    if (success == 1):
                        dhInput = geomArrayHandle.inputValue()
                        dhWeightChild = dhInput.child( OpenMayaMPx.cvar.MPxDeformerNode_inputGeom ) 
                        iter = OpenMaya.MItGeometry(dhWeightChild, True )
                        iterGeoCount = iter.count()
                        
                        if iterGeoCount > 0:
                            tmpUCoord = []
                            tmpVCoord = []
                            tmpIntersectYN = []
                            while not iter.isDone():
                                pt = iter.position()
                                #project weights based on Mesh
                                self.fnWeightMesh.getClosestPoint( pt, weightPt, 
                                                              OpenMaya.MSpace.kObject )
                    
                                rayDirection = OpenMaya.MVector(0.0,0.0,0.0)
                                self.fnWeightMesh.getClosestNormal( pt, rayDirection, 
                                                               OpenMaya.MSpace.kObject )
                                rayFloatDirection = OpenMaya.MFloatVector(rayDirection[0], 
                                                                          rayDirection[1], 
                                                                          rayDirection[2])
                                rayFloatPt= OpenMaya.MFloatPoint(pt.x, pt.y, pt.z)
                                # find out if point falls within the coverage of the mesh
                                hitPt = OpenMaya.MFloatPoint(0.0,0.0,0.0)
                                intersectYN = self.fnWeightMesh.anyIntersection( rayFloatPt, 
                                                                            rayFloatDirection, 
                                                                            None, None, False, 
                                                                            OpenMaya.MSpace.kObject, 
                                                                            100.0, True, None, 
                                                                            hitPt, None, None, 
                                                                            None, None, None, 
                                                                            0.00001)
                                # we need to chart each point to the weight mesh's uvs
                                # it is important for the mesh to have clean nurbs-like 0-1 uvs
                                self.fnWeightMesh.getUVAtPoint( weightPt, uvCoord, 
                                                           OpenMaya.MSpace.kObject )
                    
                                uCoord = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvCoord, 0, 0 )
                                vCoord = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvCoord, 0, 1 )
                                uCoord = round(uCoord, 3)
                                vCoord = round(vCoord, 3)
                                
                                tmpUCoord.append(uCoord)
                                tmpVCoord.append(vCoord)
                                tmpIntersectYN.append(intersectYN)
    
                                next(iter)
    
                            self.uCoord.append(tmpUCoord)
                            self.vCoord.append(tmpVCoord)
                            self.intersectYN.append(tmpIntersectYN)
                        else:
                            self.uCoord.append( [ 0.0 ] )
                            self.vCoord.append( [ 0.0 ] )
                            self.intersectYN.append( [ False ] )
                    else:
                        self.uCoord.append( [ 0.0 ] )
                        self.vCoord.append( [ 0.0 ] )
                        self.intersectYN.append( [ False ] )
            else:
                pass
        else:
            pass
        # cache r pivots
        ##################################
        ####   get rotate pivots    ####
        ##################################
#         self.rotatePivots = OpenMaya.MPointArray()
        pivotCheck = 0
        pivArrayHandle = OpenMaya.MArrayDataHandle(data.inputArrayValue( LHSlideDeformer.aRPivotArray ))
        pivCount = pivArrayHandle.elementCount()
        pivCheck = OpenMaya.MPlug(thisNode, LHSlideDeformer.aRPivotArray )
        if pivCheck.numConnectedChildren() > 0:
            pivCheck = 1
        else:
            pivCheck = 0
        if pivCheck > 0:
            if(len(self.rotatePivots) < numIndex or cachePivotsAmt == 0):
#                 geomArrayHandle = data.inputArrayValue(geomPlug)
                self.rotatePivots = []
                self.rotUParams = []
                self.rotVParams = []
                for i in range(numIndex):
                    tmpRotatePivots = OpenMaya.MPointArray()
                    try:
                        geomArrayHandle.jumpToElement( i )
                        success = 1
                    except:
                        success = 0
                    # if you find a connection, get the geometry
                    if (success == 1):
                        for j in range(pivCount):
                            pivArrayHandle.jumpToElement(j)
                            oTempCurve = pivArrayHandle.inputValue().child( LHSlideDeformer.aRPivot ).asNurbsCurveTransformed()
                            fnNurbsCurve = OpenMaya.MFnNurbsCurve( oTempCurve )
                            curvePoints = OpenMaya.MPointArray()
                            fnNurbsCurve.getCVs(curvePoints,OpenMaya.MSpace.kObject)
                            point = curvePoints[0]
                            
                            tmpRotatePivots.append(point)
                        self.rotatePivots.append(tmpRotatePivots)
                        ########################################
                        ####   get closest rotate pivots    ####
                        ########################################
                        # uParam
                        fnRUDouble = OpenMaya.MScriptUtil()
                        fnRUDouble.createFromDouble(0.0)
                        fnRUParam = fnRUDouble.asDoublePtr()
                        # vParam
                        fnRVDouble = OpenMaya.MScriptUtil()
                        fnRVDouble.createFromDouble(0.0)
                        fnRVParam = fnRVDouble.asDoublePtr()
                        
                        tmpRotUParams = []
                        tmpRotVParams = []

#                         self.rotUParams = []
#                         self.rotVParams = []
                        
                        #in order to get the rotate pivot when it falls outside the mesh you can find the 
                        for j in range(self.rotatePivots[i].length()):
                            fnSurfaceBase.closestPoint( self.rotatePivots[i][j], fnRUParam, 
                                                        fnRVParam, False, 0.00001, 
                                                        OpenMaya.MSpace.kObject )
                            #curveBasePtParam
                            uParam = OpenMaya.MScriptUtil.getDouble( fnRUParam )
                            vParam = OpenMaya.MScriptUtil.getDouble( fnRVParam )
                            tmpRotUParams.append(uParam)
                            tmpRotVParams.append(vParam)
                        self.rotUParams.append(tmpRotUParams)
                        self.rotVParams.append(tmpRotVParams)
                    else:
                        self.rotatePivots.append( [ OpenMaya.MPointArray() ] )
                        self.rotUParams.append( [ 0.0 ] )
                        self.rotVParams.append( [ 0.0 ] )
        rotatePivotsLength = self.rotatePivots[mIndex].length()
        iterGeoCount = itGeo.count()
        ##################################
        #get multiValues and multi weights
        ##################################
        # to keep the size of code small, 
        # we will put all u,v,n,r values into an array
        # the same for weights
        # indexes are as follows:
        # 0 = u vals/weights
        # 1 = v vals/weights
        # 2 = n vals/weights
        # 3 = r vals/weights
        
            
        #####################################################
        ####   get all weights (cache if specified)      ####
        #####################################################
        weightCheck = OpenMaya.MPlug(thisNode, LHSlideDeformer.aUWeightsParentArray )
        weightSize = weightCheck.numConnectedChildren()

        if len(self.allWeightsArray) < numIndex or cacheWeightsAmt == 0:
            allWeightParentArrays = [LHSlideDeformer.aUWeightsParentArray,
                                     LHSlideDeformer.aVWeightsParentArray,
                                     LHSlideDeformer.aNWeightsParentArray,
                                     LHSlideDeformer.aRWeightsParentArray]
            allWeightParents = [LHSlideDeformer.aUWeightsParent,
                                LHSlideDeformer.aVWeightsParent,
                                LHSlideDeformer.aNWeightsParent,
                                LHSlideDeformer.aRWeightsParent]
            allWeightChildren = [LHSlideDeformer.aUWeights,
                                 LHSlideDeformer.aVWeights,
                                 LHSlideDeformer.aNWeights,
                                 LHSlideDeformer.aRWeights]
#             geomArrayHandle = data.inputArrayValue(geomPlug)
            #dump old weights
            self.allWeightsArray = []
            for i in range(numIndex):
                
                try:
                    geomArrayHandle.jumpToElement( i )
                    success = 1
                except:
                    success = 0
                # if you find a connection, get the weights
                if (success == 1):
                    tmpAllWeightsArray = []
                    for j in range(len(allWeightParentArrays)):
                        tempWeights = []
                        weightArrayCheck = OpenMaya.MPlug(thisNode, allWeightParentArrays[i] )
                        connectedArray = OpenMaya.MIntArray()
                        weightArrayCheck.getExistingArrayAttributeIndices(connectedArray)
                        if weightArrayCheck.numConnectedChildren() > 0:
                            for k in range(connectedArray.length()):
                                tmp = [1.0]
                                try:
                                    #parentArray
                                    arrayHandleParentParent = OpenMaya.MArrayDataHandle(data.inputArrayValue( allWeightParentArrays[j] ))
                                    countParentParent = arrayHandleParentParent.elementCount()
                                    arrayHandleParentParent.jumpToArrayElement(connectedArray[k])
                                    
                                    
                                    #parent
                                    hArrayHandleParent = arrayHandleParentParent.inputValue().child(allWeightParents[j])
                                    hArrayHandleParentArray = OpenMaya.MArrayDataHandle(hArrayHandleParent)
                                    countParent = hArrayHandleParentArray.elementCount()
                                    
                                    #child
                                    hArrayHandleParentArray.jumpToElement(i)
                                    handle = OpenMaya.MDataHandle(hArrayHandleParentArray.inputValue() )
                                    child = OpenMaya.MDataHandle(handle.child( allWeightChildren[j] ) )
                                    newData = OpenMaya.MFnDoubleArrayData(child.data())
                                    tmp = OpenMaya.MFnDoubleArrayData(child.data()).array()

                                except:
                                    weight=[]
                                    for ii in range(iterGeoCount):
                                        weight.append(1.0)
                                    tmp = weight
                                tempWeights.append(tmp)
                            tmpAllWeightsArray.append(tempWeights)
                        else:
                            pass
                    self.allWeightsArray.append(tmpAllWeightsArray)
                else:
                    self.allWeightsArray.append([[[0.0]]])
        else:
            pass
        
        #######################################################
        ####   get multiAnimCurves (cache if specified)    ####
        #######################################################
        # to keep the size of code small, 
        # we will put all u,v,n,r anim curve info into an array
        # indexes are as follows:
        # 0 = u anim stuff
        # 1 = v anim stuff
        # 2 = n anim stuff
        # 3 = r anim stuff
        
        
        
        if len(self.allUAnimCurveWeights) < numIndex or cacheWeightCurvesAmt == 0:
            if self.weightMeshCheck == 1:
                #----dump all old info
                self.allUFnCurvesArray = []
                self.allUTimeOffsetArray = []
                self.allUTimeLengthArray = []
                self.allVFnCurvesArray = []
                self.allVTimeOffsetArray = []
                self.allVTimeLengthArray = []
                self.allUAnimCurveWeights = []
                self.allVAnimCurveWeights = []
                
                tmpUAnimCurvesArray = []
                tmpUTimeOffsetArray = []
                tmpUTimeLengthArray = []
                
                tmpVAnimCurvesArray = []
                tmpVTimeOffsetArray = []
                tmpVTimeLengthArray = []
                ##########################
                #####  all U Curves  #####
                ##########################
                
                allAnimCurveUParents = [LHSlideDeformer.aUAnimCurveUParent,
                                        LHSlideDeformer.aVAnimCurveUParent,
                                        LHSlideDeformer.aNAnimCurveUParent,
                                        LHSlideDeformer.aRAnimCurveUParent]
                allAnimCurveUChildren = [LHSlideDeformer.aUAnimCurveU,
                                         LHSlideDeformer.aVAnimCurveU,
                                         LHSlideDeformer.aNAnimCurveU,
                                         LHSlideDeformer.aRAnimCurveU]
                allAnimCurveVParents = [LHSlideDeformer.aUAnimCurveVParent,
                                        LHSlideDeformer.aVAnimCurveVParent,
                                        LHSlideDeformer.aNAnimCurveVParent,
                                        LHSlideDeformer.aRAnimCurveVParent]
                allAnimCurveVChildren = [LHSlideDeformer.aUAnimCurveV,
                                         LHSlideDeformer.aVAnimCurveV,
                                         LHSlideDeformer.aNAnimCurveV,
                                         LHSlideDeformer.aRAnimCurveV]
                for i in range(numIndex):
                    try:
                        geomArrayHandle.jumpToElement( i )
                        success = 1
                    except:
                        success = 0
                    # if you find a connection, get the weights
                    if (success == 1):
                        tmpUAnimCurves = None
                        tmpUTimeOffset = None
                        tmpUTimeLength = None
                        tmpVAnimCurves = None
                        tmpVTimeOffset = None
                        tmpVTimeLength = None
                        for j in range(len(allAnimCurveUParents)):
                            try:
                                tmp = self.getAnimCurves(allAnimCurveUParents[j],
                                                         allAnimCurveUChildren[j])
                                tmpUAnimCurves,tmpUTimeOffset,tmpUTimeLength = tmp[0],tmp[1],tmp[2]
                                
                                tmp = self.getAnimCurves(allAnimCurveVParents[j],
                                                         allAnimCurveVChildren[j])
                                tmpVAnimCurves,tmpVTimeOffset,tmpVTimeLength = tmp[0],tmp[1],tmp[2]
                            except:
                                pass
                            
                            if not tmpUAnimCurves:
                                tmpUAnimCurves, tmpUTimeOffset, tmpUTimeLength = [0], [0], [0]
                            
                            if not tmpVAnimCurves:
                                tmpVAnimCurves, tmpVTimeOffset, tmpVTimeLength = [0], [0], [0]

                            tmpUAnimCurvesArray.append(tmpUAnimCurves)
                            tmpUTimeOffsetArray.append(tmpUTimeOffset)
                            tmpUTimeLengthArray.append(tmpUTimeLength)

                            tmpVAnimCurvesArray.append(tmpVAnimCurves)
                            tmpVTimeOffsetArray.append(tmpVTimeOffset)
                            tmpVTimeLengthArray.append(tmpVTimeLength)
                            
                        self.allUFnCurvesArray.append(tmpUAnimCurvesArray)
                        self.allUTimeOffsetArray.append(tmpUTimeOffsetArray)
                        self.allUTimeLengthArray.append(tmpUTimeLengthArray)
                        
                        self.allVFnCurvesArray.append(tmpVAnimCurvesArray)
                        self.allVTimeOffsetArray.append(tmpVTimeOffsetArray)
                        self.allVTimeLengthArray.append(tmpVTimeLengthArray)
                    else:
                        self.allUFnCurvesArray.append([[0.0]])
                        self.allUTimeOffsetArray.append([[0.0]])
                        self.allUTimeLengthArray.append([[0.0]])
                        self.allVFnCurvesArray.append([[0.0]])
                        self.allVTimeOffsetArray.append([[0.0]])
                        self.allVTimeLengthArray.append([[0.0]])
    
                
                # AnimCURVE
                # the idea here is to fine the time range of all the keys and convert that to  0-1 range
                # in a perfect world the time would only range 0-1
                # but because we might want to be remotely accurate
                # a larger range will be needed
                # therefore, a time range of seven means that we will have to divide by 7
                # in order to get back in the 0-1 range
                # this means that later, when charting the anim curve to a nurbsSurface,
                # we will have to multiply the (0-1) parameter of the nearest point by 7
                # say the parameter is .8 * 7 = 5.6
                # this means we will get the value of the anim curve at 5.6
                
                # of course this only works if the frame range starts at 0 and goes to 6
                # what happens when someone decides to start on frame 98.3 and ends 7 frames later?
                # you simply subtract 98.3, then, then do the steps above.
                self.allUAnimCurveWeights = []
                self.allVAnimCurveWeights = []
                for i in range(numIndex):
                    tempU = []
                    tempV = []
                    try:
                        geomArrayHandle.jumpToElement( i )
                        success = 1
                    except:
                        success = 0
                    # if you find a connection, get the geometry
                    if (success == 1):
#                         geomArrayHandle = data.inputArrayValue(geomPlug)
                        dhInput = geomArrayHandle.inputValue()
                        dhWeightChild = dhInput.child( OpenMayaMPx.cvar.MPxDeformerNode_inputGeom ) 
                        iter = OpenMaya.MItGeometry(dhWeightChild, True )
                        iterGeoCount = iter.count()
                        if iterGeoCount > 0:

                            for j in range(len(self.allUFnCurvesArray[i])):
                                tempUVals = []
                                for k in range(len(self.allUFnCurvesArray[i][j])):
                                    tempUPointVals = []
                                    while not iter.isDone():
                                        pt = iter.position()
                                        try:
                                            remap = self.uCoord[i][iter.index()] * self.allUTimeLengthArray[i][j][k]
                                            remap = remap - self.allUTimeOffsetArray[i][j][k] 
                                            remap = OpenMaya.MTime(remap)
                                            weight = self.allUFnCurvesArray[i][j][k].evaluate(remap)
                                            tempUPointVals.append(weight)
                                        except:
                                            tempUPointVals.append(1.0)
                                        next(iter)
                                    iter.reset()
                                    tempUVals.append(tempUPointVals)
                                tempU.append(tempUVals)
                            self.allUAnimCurveWeights.append(tempU)
                            
                            for j in range(len(self.allVFnCurvesArray[i])):
                                tempVVals = []
                                for k in range(len(self.allVFnCurvesArray[i][j])):
                                    tempVPointVals = []
                                    while not iter.isDone():
                                        pt = iter.position()
                                        try:
                                            remap = OpenMaya.MTime(self.vCoord[i][iter.index()] * self.allVTimeLengthArray[i][j][k])
                                            remap = remap - self.allVTimeOffsetArray[i][j][k]
                                            weight = self.allVFnCurvesArray[i][j][k].evaluate(remap)
                                            tempVPointVals.append(weight)
                                        except:
                                            tempVPointVals.append(1.0)
                                        next(iter)
                                    iter.reset()
                                    tempVVals.append(tempVPointVals)
                                tempV.append(tempVVals)
                            self.allVAnimCurveWeights.append(tempV)
                            
                        else:
                            self.allUAnimCurveWeights.append([[[0.0]]])
                            self.allVAnimCurveWeights.append([[[0.0]]])
                    else:
                        self.allUAnimCurveWeights.append([[[0.0]]])
                        self.allVAnimCurveWeights.append([[[0.0]]])
            else:
                pass
        else:
            pass
        #############################################################
        ####   get closest param infos (cache if specified)    ######
        #############################################################
        """ Caches out closest point functions for sliding """
        if len(self.slideUVBasePt) < numIndex or cacheParamsAmt == 0:
            # dump existing infos
            self.slideUVBasePt = []
            self.slideUBasePtParam = []
            self.slideVBasePtParam = []
            for i in range(numIndex):
                try:
                    geomArrayHandle.jumpToElement( i )
                    success = 1
                except:
                    success = 0
                # if you find a connection, get the geometry
                if (success == 1):
                    tmpPoint = []
                    tmpUParam = []
                    tmpVParam = []
                    dhInput = geomArrayHandle.inputValue()
                    dhWeightChild = dhInput.child( OpenMayaMPx.cvar.MPxDeformerNode_inputGeom ) 
                    iter = OpenMaya.MItGeometry(dhWeightChild, True )
                    iterGeoCount = iter.count()
                    if iterGeoCount > 0:
                        while not iter.isDone():
                            pt = iter.position()
                            #curveBasePt
                            slideUVBasePt = fnSurfaceBase.closestPoint( pt, fnUParam, fnVParam, False, 0.00001, OpenMaya.MSpace.kObject )
                            #curveBasePtParam
                            slideUBasePtParam = OpenMaya.MScriptUtil.getDouble( fnUParam )
                            slideVBasePtParam = OpenMaya.MScriptUtil.getDouble( fnVParam )
                            tmpPoint.append(slideUVBasePt)
                            tmpUParam.append(slideUBasePtParam)
                            tmpVParam.append(slideVBasePtParam)
                            next(iter)
                        iter.reset()
                        self.slideUVBasePt.append(tmpPoint)
                        self.slideUBasePtParam.append(tmpUParam)
                        self.slideVBasePtParam.append(tmpVParam)

                    else:
                        self.slideUVBasePt.append( [ 0.0, 0.0, 0.0 ] )
                        self.slideUBasePtParam.append( [ 0.0 ] )
                        self.slideVBasePtParam.append( [ 0.0 ] )
                else:
                    self.slideUVBasePt.append( [ 0.0, 0.0, 0.0 ] )
                    self.slideUBasePtParam.append( [ 0.0 ] )
                    self.slideVBasePtParam.append( [ 0.0 ] )
                
                    
#             self.slideUVBasePt.append(tmpPoint)
#             self.slideUBasePtParam.append(tmpUParam)
#             self.slideVBasePtParam.append(tmpVParam)
            
        
        ##########################################################
        ####   get surface base infos (cache if specified)    ####
        ##########################################################
        """ In most situations you can cache the surface base """

        if len(self.rotMatrix) < numIndex or cacheBaseAmt == 0:
            
            
            #----get parameter range
            fnSurfaceBase.getKnotDomain(fnUMinParam,fnUMaxParam,fnVMinParam,fnVMaxParam)

            self.uMinParam = OpenMaya.MScriptUtil.getDouble( fnUMinParam )
            self.uMaxParam = OpenMaya.MScriptUtil.getDouble( fnUMaxParam )

            self.vMinParam = OpenMaya.MScriptUtil.getDouble( fnVMinParam )
            self.vMaxParam = OpenMaya.MScriptUtil.getDouble( fnVMaxParam )
            self.rotMatrix = []
            for i in range(numIndex):
                try:
                    geomArrayHandle.jumpToElement( i )
                    success = 1
                except:
                    success = 0
                # if you find a connection, get the geometry
                if (success == 1):
                    dhInput = geomArrayHandle.inputValue()
                    dhWeightChild = dhInput.child( OpenMayaMPx.cvar.MPxDeformerNode_inputGeom ) 
                    iter = OpenMaya.MItGeometry(dhWeightChild, True )
                    iterGeoCount = iter.count()
                    if iterGeoCount > 0:
                        tmpRotMatrix = []
                        #----dump old info
                        while not iter.isDone():
                            idx = iter.index()
                            fnSurfaceBase.getTangents( self.slideUBasePtParam[i][idx], self.slideVBasePtParam[i][idx], xVecBase, yVecBase, OpenMaya.MSpace.kObject )
                
                            xBaseVector = xVecBase
                            xBaseVector.normalize()
                            
                            yBaseVector = yVecBase
                            yBaseVector.normalize()
                            
                            zBaseVector = xBaseVector ^ yBaseVector
                            zBaseVector.normalize
                
                            # x
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[0], 0, xBaseVector[0])
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[0], 1, xBaseVector[1])
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[0], 2, xBaseVector[2])
                            # y
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[1], 0, yBaseVector[0])
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[1], 1, yBaseVector[1])
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[1], 2, yBaseVector[2])
                            # z
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[2], 0, zBaseVector[0])
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[2], 1, zBaseVector[1])
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[2], 2, zBaseVector[2])
                            # translate
                            OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[3], 3, 1.0)
                            
                            # find the rotation offset, then apply later
                            rotMatrix = OpenMaya.MEulerRotation()
                            #### 0 = XYZ rotation order, check maya api doc for other rotation orders
                            rotMatrix = rotMatrix.decompose(BaseMatrix,0)   
                            tmpRotMatrix.append(rotMatrix.asMatrix())
                            next(iter)
                        iter.reset()
                        self.rotMatrix.append(tmpRotMatrix)
                    else:
                        self.rotMatrix.append([OpenMaya.MMatrix()])
                else:
                    self.rotMatrix.append([OpenMaya.MMatrix()])
        else:
            pass
        
        
        ####################################################
        ####################################################
        ######    geometry iteration/main algorithm    #####
        ####################################################
        ####################################################


        #self.allValsArray
#         print len(self.rotatePivots)
        
        
        
        
        
        
        
        
        
        
        #rotatePivots MPointArray
        #rotUParams floatArray
        #rotVParams floatArray
        
        
        
        
        
        
        
        
        
        
#         #----Cache vars
#         # rot cache
#         self.rotatePivots = []
#         self.rotUParams = []
#         self.rotVParams = []
#         # weight cache
#         self.allWeightsArray = [0.0]
#         # cache weight mesh
#         self.uCoord = []
#         self.vCoord = []
#         self.intersectYN = []
#         self.weightMeshCheck = 0
#         # cache anim curves
#         self.allUFnCurvesArray = []
#         self.allUTimeOffsetArray = []
#         self.allUTimeLengthArray = []
#         self.allVFnCurvesArray = []
#         self.allVTimeOffsetArray = []
#         self.allVTimeLengthArray = []
#         self.allUAnimCurveWeights = []
#         self.allVAnimCurveWeights = []
#         # cache params
#         self.slideUVBasePt = []
#         self.slideUBasePtParam = []
#         self.slideVBasePtParam = []
#         # cache base surface
#         self.uMinParam = 0.0
#         self.uMaxParam = 0.0
#         self.vMinParam = 0.0
#         self.vMaxParam = 0.0
#         self.rotMatrix = []















        while not itGeo.isDone():
            pt = itGeo.position()
            w = self.weightValue(data, mIndex, itGeo.index())
            idx = itGeo.index()
            w = w * envelope
            if w <= 0:
                next(itGeo)
                continue
            ######################  

            #########################################
            #### all user defined painted weights ###
            #########################################

            
            allVals = []
            for i in range(len(allValsArray)):
                tempVals = []
                for j in range(len(allValsArray[i])):
                    try:
                        tempW = self.allWeightsArray[mIndex][i][j][idx]
                        tempVal = allValsArray[i][j]
                    except:
                        tempW = 1.0
                        tempVal = allValsArray[i][j]
                    tempVals.append(tempW * tempVal)
                allVals.append(tempVals)
            
            
            ###################### 
            #### curveWeights #### 
            ######################
            if self.weightMeshCheck == 1:
                        
                ############################
                ###### U V N R combine #####
                ############################
                uW = 0.0
                vW = 0.0
                nW = 0.0
                rW = 0.0
                #---Multiply painted weights by curve weights
                # the length of all arrays should be the same
                # this is currently up to the user
                # but I should write a failsafe
                for i in range(len(allVals[0])):
                    try:
                        allVals[0][i] = (allVals[0][i] *
                                         self.allUAnimCurveWeights[mIndex][0][i][idx] *
                                         self.allVAnimCurveWeights[mIndex][0][i][idx])
                    except:
                        allVals[0][i] = allVals[0][i] * 1.0
                for i in range(len(allVals[1])):
                    try:
                        allVals[1][i] = (allVals[1][i] *
                                         self.allUAnimCurveWeights[mIndex][1][i][idx] *
                                         self.allVAnimCurveWeights[mIndex][1][i][idx])
                    except:
                        allVals[1][i] = allVals[1][i] * 1.0
                for i in range(len(allVals[2])):
                    try:
                        allVals[2][i] = (allVals[2][i] *
                                         self.allUAnimCurveWeights[mIndex][2][i][idx] *
                                         self.allVAnimCurveWeights[mIndex][2][i][idx])
                    except:
                        allVals[2][i] = allVals[2][i] * 1.0
                for i in range(len(allVals[3])):
                    try:
                        allVals[3][i] = (allVals[3][i] *
                                         self.allUAnimCurveWeights[mIndex][3][i][idx] *
                                         self.allVAnimCurveWeights[mIndex][3][i][idx])
                    except:
                        allVals[3][i] = allVals[3][i] * 1.0
                
                uW = sum(allVals[0])
                vW = sum(allVals[1])
                nW = sum(allVals[2])
                rW = sum(allVals[3])
    
    
                if self.intersectYN[mIndex][idx] == False:
                    uW = 0.0
                    vW = 0.0
                    nW = 0.0
                    rW = 0.0
                    
            if self.weightMeshCheck == 0:
                uW = sum(allVals[0])
                vW = sum(allVals[1])
                nW = sum(allVals[2])
                rW = sum(allVals[3])
            #######################################################
            slideUBasePtParam = 0.0
            slideVBasePtParam = 0.0


            #curveBasePt
            slideUVBasePt = self.slideUVBasePt[mIndex][idx]
            #curveBasePtParam
            slideUBasePtParam = self.slideUBasePtParam[mIndex][idx]
            slideVBasePtParam = self.slideVBasePtParam[mIndex][idx]

            # get min and max parameter
            
            slideUValue = uW
            slideUCheck = slideUBasePtParam + slideUValue
            slideUBasePtParamValue = None

            slideVValue = vW
            slideVCheck = slideVBasePtParam + slideVValue
            slideVBasePtParamValue = None

            ######################
            ######## slideUV #######
            ######################
            

            allURotVals = 0.0
            allVRotVals = 0.0
            rotSlideUValue = 0.0
            rotSlideVValue = 0.0
            ######## rotateUV #######
            uPivOffset = 0.0
            vPivOffset = 0.0
            if pivCheck > 0:
                for i in range(rotatePivotsLength):
                    
                    pivotU = self.rotUParams[mIndex][i]
                    pivotV = self.rotVParams[mIndex][i]
                    
                    surfaceRot = slideUCheck-pivotU , slideVCheck-pivotV
                    surfaceRot = ( surfaceRot[0]*math.cos(rW*allVals[3][i])-surfaceRot[1]*math.sin(rW*allVals[3][i]) , surfaceRot[0]*math.sin(rW*allVals[3][i])+surfaceRot[1]*math.cos(rW*allVals[3][i]))
                    surfaceRot = surfaceRot[0]+pivotU , surfaceRot[1]+pivotV
                                          
                    slideUCheck,slideVCheck=surfaceRot

                rotSlideUValue = slideUCheck
                rotSlideVValue = slideVCheck
            if pivCheck == 0:
                rotSlideUValue = slideUCheck
                rotSlideVValue = slideVCheck
            
            # UCheck
            if (slideUCheck > self.uMinParam) or (slideUCheck < self.uMaxParam):
                slideUBasePtParamValue = rotSlideUValue
            if (slideUCheck <= self.uMinParam):
                slideUBasePtParamValue = self.uMinParam
            if (slideUCheck >= self.uMaxParam):
                slideUBasePtParamValue = self.uMaxParam

            # VCheck
            if (slideVCheck > self.vMinParam) or (slideVCheck < self.vMaxParam):
                slideVBasePtParamValue = rotSlideVValue
            if (slideVCheck <= self.vMinParam):
                slideVBasePtParamValue = self.vMinParam
            if (slideVCheck >= self.vMaxParam):
                slideVBasePtParamValue = self.vMaxParam
    
            # use U and V attributes to drive sliding on a surface
            # if surface goes further than the surface, find the last point traveled over, get the tangent in that direction, and have the pt travel on in that vector forever

            ## U and V on surface
            if (slideUCheck > self.uMinParam) or (slideUCheck < self.uMaxParam) and (slideVCheck > self.vMinParam) or (slideVCheck < self.vMaxParam):
                fnSurface.getPointAtParam( slideUBasePtParamValue, slideVBasePtParamValue, slideUVPoint, OpenMaya.MSpace.kObject )
            # V Min
            if (slideVCheck <= self.vMinParam) :
                #fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kObject )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kObject, fakePt2, fakeVecU, fakeVecV)
                slideVVec = fnVVec
                slideVValue = rotSlideVValue + slideVBasePtParam
                slideUVPoint -= -slideVVec * rotSlideVValue

            # V Max
            if (slideVCheck >= self.vMaxParam) :
                #fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kObject )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kObject, fakePt2, fakeVecU, fakeVecV)
                slideVVec = fnVVec
                rotSlideVValue = rotSlideVValue -1
                slideVValue = rotSlideVValue + (slideVBasePtParam - self.vMaxParam)
                slideUVPoint -= -slideVVec * rotSlideVValue

            # U Min
            if (slideUCheck <= self.uMinParam) :
                #fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kObject )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kObject, fakePt2, fakeVecU, fakeVecV)
                slideUVec = fnUVec
#                 rotSlideUValue = rotSlideUValue -pivotU

                slideUValue = rotSlideUValue + slideUBasePtParam
                slideUVPoint -= -slideUVec * rotSlideUValue

            # U Max
            if (slideUCheck >= self.uMaxParam) :
            #fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kObject )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kObject, fakePt2, fakeVecU, fakeVecV)
                slideUVec = fnUVec
                rotSlideUValue = rotSlideUValue -1
                slideUValue = rotSlideUValue + (slideUBasePtParam - self.uMaxParam)
                slideUVPoint -= -slideUVec * rotSlideUValue
            
##################################################################################################
############# Slide Ends #########################################################################
##################################################################################################
# 
#             fnSurfaceBase.getTangents( slideUBasePtParam, slideVBasePtParam, xVecBase, yVecBase, OpenMaya.MSpace.kObject )
# 
#             xBaseVector = xVecBase
#             xBaseVector.normalize()
#             
#             yBaseVector = yVecBase
#             yBaseVector.normalize()
#             
#             zBaseVector = xBaseVector ^ yBaseVector
#             zBaseVector.normalize
# 
#             # x
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[0], 0, xBaseVector[0])
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[0], 1, xBaseVector[1])
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[0], 2, xBaseVector[2])
#             # y
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[1], 0, yBaseVector[0])
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[1], 1, yBaseVector[1])
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[1], 2, yBaseVector[2])
#             # z
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[2], 0, zBaseVector[0])
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[2], 1, zBaseVector[1])
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[2], 2, zBaseVector[2])
#             # translate
#             OpenMaya.MScriptUtil.setDoubleArray(BaseMatrix[3], 3, 1.0)
#             
#             # find the rotation offset, then apply later
#             rotMatrix = OpenMaya.MEulerRotation()
#             #### 0 = XYZ rotation order, check maya api doc for other rotation orders
#             rotMatrix = rotMatrix.decompose(BaseMatrix,0)  
            rotMatrix = self.rotMatrix[mIndex][idx]      

#############################################################################################

            fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, xVec, yVec, OpenMaya.MSpace.kObject )

            xAxisVec = xVec
            xAxisVec.normalize()
            
            yAxisVec = yVec
            yAxisVec.normalize()
            
            zAxisVec = xAxisVec ^ yAxisVec
            zAxisVec.normalize()


            # apply rotate offset
            rotateX = OpenMaya.MQuaternion(-rotMatrix[0],xAxisVec)
            rotateMatrixX = rotateX.asMatrix()
            yAxisVec = yAxisVec * rotateMatrixX
            zAxisVec = zAxisVec * rotateMatrixX

            rotateY = OpenMaya.MQuaternion(-rotMatrix[1],yAxisVec)
            rotateMatrixY = rotateY.asMatrix()
            xAxisVec = xAxisVec * rotateMatrixY
            zAxisVec = zAxisVec * rotateMatrixY

            rotateZ = OpenMaya.MQuaternion(-rotMatrix[2],zAxisVec)
            rotateMatrixZ = rotateZ.asMatrix()
            xAxisVec = xAxisVec * rotateMatrixZ
            yAxisVec = yAxisVec * rotateMatrixZ
            

            # x
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[0], 0, xAxisVec[0])
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[0], 1, xAxisVec[1])
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[0], 2, xAxisVec[2])
            # y
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[1], 0, yAxisVec[0])
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[1], 1, yAxisVec[1])
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[1], 2, yAxisVec[2])
            # z
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[2], 0, zAxisVec[0])
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[2], 1, zAxisVec[1])
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[2], 2, zAxisVec[2])
            # translate
            OpenMaya.MScriptUtil.setDoubleArray(DriveMatrix[3], 3, 1.0)
            # apply rotation amount
            DriveMatrixEuler = OpenMaya.MEulerRotation()
            DriveMatrixEuler = DriveMatrixEuler.decompose(DriveMatrix,0)
            DriveMatrixEuler = OpenMaya.MEulerRotation( DriveMatrixEuler[0] * rotationAmount,
                                                        DriveMatrixEuler[1] * rotationAmount,
                                                        DriveMatrixEuler[2] * rotationAmount)
            DriveMatrix = DriveMatrixEuler.asMatrix()
            ### apply normal translation before anything else
            slideNormal = fnSurfaceBase.normal( slideUBasePtParamValue, slideVBasePtParamValue, OpenMaya.MSpace.kObject )
            pt -=(slideNormal) * nW * w

            ### ApplyRotation Amount
            toCenterBase = OpenMaya.MVector(-slideUVBasePt.x, -slideUVBasePt.y, -slideUVBasePt.z)
            pt = pt + toCenterBase
            
            # do rotationAmount, then put pts back
            pt = ( pt * DriveMatrix ) - toCenterBase

            ### apply slide
            pt.x +=(slideUVPoint.x - slideUVBasePt.x) * w
            pt.y +=(slideUVPoint.y - slideUVBasePt.y) * w
            pt.z +=(slideUVPoint.z - slideUVBasePt.z) * w
            
            
            if scaleAmount != 1.0:
                pt = pt - (slideUVPoint - pt) * (scaleAmount - 1.0) * w
            

            itGeo.setPosition(pt)
            next(itGeo)
        return

####################################################
######## Deform End ################################
####################################################



def creator():
    return OpenMayaMPx.asMPxPtr(LHSlideDeformer())



####################################################
######## Initialize ################################
####################################################


def initialize():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()
    cAttr = OpenMaya.MFnCompoundAttribute()
    ##### typed attributes ######

    # base
    LHSlideDeformer.aSurfaceBase = tAttr.create('surfaceBase', 'surfbase', OpenMaya.MFnData.kNurbsSurface)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aSurfaceBase )
    # surface
    LHSlideDeformer.aSurface = tAttr.create('surface', 'surf', OpenMaya.MFnData.kNurbsSurface)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aSurface )
    # weight mesh
    LHSlideDeformer.aWeightMesh = tAttr.create('weightMesh', 'wmesh', OpenMaya.MFnData.kMesh)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aWeightMesh )

    # numeric attributes

    LHSlideDeformer.aRotationAmount = nAttr.create('rotationAmount', 'rotamount', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aRotationAmount)

    LHSlideDeformer.aScaleAmount = nAttr.create('scaleAmount', 'scl', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aScaleAmount)
    
    # cache numeric attributes
    
    LHSlideDeformer.aCachePivots = nAttr.create('cacheRotPivots', 'crp', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aCachePivots)
    
    LHSlideDeformer.aCacheWeights = nAttr.create('cacheWeights', 'cw', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aCacheWeights)

    LHSlideDeformer.aCacheParams = nAttr.create('cacheParams', 'cp', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aCacheParams)

    LHSlideDeformer.aCacheWeightMesh = nAttr.create('cacheWeightMesh', 'cwm', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aCacheWeightMesh)

    LHSlideDeformer.aCacheWeightCurves = nAttr.create('cacheWeightCurves', 'cwc', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aCacheWeightCurves)


    LHSlideDeformer.aCacheBase = nAttr.create('cacheBase', 'cb', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aCacheBase)
    
    ######### UATTRS ###########################

    ############ VALUE ##########################
    LHSlideDeformer.aUValue = nAttr.create('uValue', 'uvalue', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(0.0)

    LHSlideDeformer.aUValueParent = cAttr.create("uValueParentArray", "uValueParentArray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aUValue )
    cAttr.setReadable(True);
    cAttr.setWritable(True);
    cAttr.setConnectable(True);
    cAttr.setChannelBox(True);
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUValueParent);


    #child
    LHSlideDeformer.aUWeights = tAttr.create('uWeights', 'uweights', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)

    #Parent
    LHSlideDeformer.aUWeightsParent = cAttr.create("uWeightsParent", "uweightsparent")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aUWeights )
    cAttr.setReadable(True);
    cAttr.setWritable(True);
    cAttr.setConnectable(True);
    cAttr.setChannelBox(True);
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUWeightsParent);

    #ParentParent
    LHSlideDeformer.aUWeightsParentArray = cAttr.create("uWeightsParentArray", "uweightsparentarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aUWeightsParent )
    cAttr.setReadable(True);
    cAttr.setWritable(True);
    cAttr.setConnectable(True);
    cAttr.setChannelBox(True);
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUWeightsParentArray);


    LHSlideDeformer.aUAnimCurveU = nAttr.create('uAnimCurveU', 'uanimcurveu', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    #LHSlideDeformer.addAttribute(LHSlideDeformer.aUAnimCurveU)

    LHSlideDeformer.aUAnimCurveUParent = cAttr.create("uAnimCurveUArray", "uanimcurveuarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aUAnimCurveU )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True);
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUAnimCurveUParent)

    LHSlideDeformer.aUAnimCurveV = nAttr.create('uAnimCurveV', 'uanimcurvev', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)

    LHSlideDeformer.aUAnimCurveVParent = cAttr.create("uAnimCurveVArray", "uanimcurvevarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aUAnimCurveV )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUAnimCurveVParent)
    
    ############################################
    ######### VATTRS ###########################
    ############################################
    
    ############ VALUE ##########################
    LHSlideDeformer.aVValue = nAttr.create('vValue', 'vvalue', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(0.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVValue)

    LHSlideDeformer.aVValueParent = cAttr.create("vValueParentArray", "vValueParentArray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aVValue )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVValueParent)


    #child
    LHSlideDeformer.aVWeights = tAttr.create('vWeights', 'vweights', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVWeights)

    #Parent
    LHSlideDeformer.aVWeightsParent = cAttr.create("vWeightsParent", "vweightsparent")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aVWeights )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVWeightsParent)

    #ParentParent
    LHSlideDeformer.aVWeightsParentArray = cAttr.create("vWeightsParentArray", "vweightsparentarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aVWeightsParent )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVWeightsParentArray)


    LHSlideDeformer.aVAnimCurveU = nAttr.create('vAnimCurveU', 'vanimcurveu', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    #LHSlideDeformer.addAttribute(LHSlideDeformer.aVAnimCurveU)

    LHSlideDeformer.aVAnimCurveUParent = cAttr.create("vAnimCurveUArray", "vanimcurveuarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aVAnimCurveU )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVAnimCurveUParent)

    LHSlideDeformer.aVAnimCurveV = nAttr.create('vAnimCurveV', 'vanimcurvev', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    #LHSlideDeformer.addAttribute(LHSlideDeformer.aVAnimCurveV)

    LHSlideDeformer.aVAnimCurveVParent = cAttr.create("vAnimCurveVArray", "vanimcurvevarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aVAnimCurveV )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVAnimCurveVParent)
    
    ###############################################
    ############ N Attrs ##########################
    ###############################################

    LHSlideDeformer.aNValue = nAttr.create('nValue', 'nvalue', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(0.0)

    LHSlideDeformer.aNValueParent = cAttr.create("nValueParentArray", "nValueParentArray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aNValue )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aNValueParent)


    #child
    LHSlideDeformer.aNWeights = tAttr.create('nWeights', 'nweights', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)

    #Parent
    LHSlideDeformer.aNWeightsParent = cAttr.create("nWeightsParent", "nweightsparent")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aNWeights )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aNWeightsParent);

    #ParentParent
    LHSlideDeformer.aNWeightsParentArray = cAttr.create("nWeightsParentArray", "nweightsparentarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aNWeightsParent )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aNWeightsParentArray)


    LHSlideDeformer.aNAnimCurveU = nAttr.create('nAnimCurveU', 'nanimcurveu', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)

    LHSlideDeformer.aNAnimCurveUParent = cAttr.create("nAnimCurveUArray", "nanimcurveuarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aNAnimCurveU )
    cAttr.setReadable(True);
    cAttr.setWritable(True);
    cAttr.setConnectable(True);
    cAttr.setChannelBox(True);
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aNAnimCurveUParent);

    LHSlideDeformer.aNAnimCurveV = nAttr.create('nAnimCurveV', 'nanimcurvev', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    #LHSlideDeformer.addAttribute(LHSlideDeformer.aNAnimCurveV)

    LHSlideDeformer.aNAnimCurveVParent = cAttr.create("nAnimCurveVArray", "nanimcurvevarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aNAnimCurveV )
    cAttr.setReadable(True);
    cAttr.setWritable(True);
    cAttr.setConnectable(True);
    cAttr.setChannelBox(True);
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aNAnimCurveVParent);


    ###############################################
    ############ R Attrs ##########################
    ###############################################

    LHSlideDeformer.aRValue = nAttr.create('rValue', 'rvalue', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(0.0)

    LHSlideDeformer.aRValueParent = cAttr.create("rValueParentArray", "rValueParentArray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aRValue )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aRValueParent)


    #child
    LHSlideDeformer.aRWeights = tAttr.create('rWeights', 'rweights', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)

    #Parent
    LHSlideDeformer.aRWeightsParent = cAttr.create("rWeightsParent", "rweightsparent")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aRWeights )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aRWeightsParent);

    #ParentParent
    LHSlideDeformer.aRWeightsParentArray = cAttr.create("rWeightsParentArray", "rweightsparentarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aRWeightsParent )
    cAttr.setReadable(True)
    cAttr.setWritable(True)
    cAttr.setConnectable(True)
    cAttr.setChannelBox(True)
    cAttr.setUsesArrayDataBuilder(True)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aRWeightsParentArray)


    LHSlideDeformer.aRAnimCurveU = nAttr.create('rAnimCurveU', 'ranimcurveu', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)

    LHSlideDeformer.aRAnimCurveUParent = cAttr.create("rAnimCurveUArray", "ranimcurveuarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aRAnimCurveU )
    cAttr.setReadable(True);
    cAttr.setWritable(True);
    cAttr.setConnectable(True);
    cAttr.setChannelBox(True);
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aRAnimCurveUParent);

    LHSlideDeformer.aRAnimCurveV = nAttr.create('rAnimCurveV', 'ranimcurvev', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)

    LHSlideDeformer.aRAnimCurveVParent = cAttr.create("rAnimCurveVArray", "ranimcurvevarray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aRAnimCurveV )
    cAttr.setReadable(True);
    cAttr.setWritable(True);
    cAttr.setConnectable(True);
    cAttr.setChannelBox(True);
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aRAnimCurveVParent);


    #R Pivot Curves
    LHSlideDeformer.aRPivot = tAttr.create('rPivotCurve', 'rpivotcurve', OpenMaya.MFnData.kNurbsCurve)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aRPivot )

    LHSlideDeformer.aRPivotArray = cAttr.create("rPivotCurveArray", "rpivotcurvearray")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aRPivot )
    cAttr.setReadable(True);
    cAttr.setWritable(True);
    cAttr.setConnectable(True);
    cAttr.setChannelBox(True);
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aRPivotArray);



    # Affects outputs and inputs

    outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
    
    # nAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRotationAmount, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aScaleAmount, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aCachePivots, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aCacheWeights, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aCacheParams, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aCacheWeightMesh, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aCacheWeightCurves, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aCacheBase, outputGeom)

    # tAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aSurfaceBase, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aSurface, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aWeightMesh, outputGeom)

    # U ATTRS
    
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUValue, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUValueParent, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUWeights, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUWeightsParent, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUWeightsParentArray, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVValue, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUAnimCurveU, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUAnimCurveUParent, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUAnimCurveV, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUAnimCurveVParent, outputGeom)

    # V ATTRS
    
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVValue, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVValueParent, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVWeights, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVWeightsParent, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVWeightsParentArray, outputGeom)
    
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVAnimCurveU, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVAnimCurveUParent, outputGeom)
    
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVAnimCurveV, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVAnimCurveVParent, outputGeom)

    # N ATTRS
    
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aNValue, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aNValueParent, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aNWeights, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aNWeightsParent, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aNWeightsParentArray, outputGeom)
    
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aNAnimCurveU, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aNAnimCurveUParent, outputGeom)
    
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aNAnimCurveV, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aNAnimCurveVParent, outputGeom)

    # R ATTRS
    
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRValue, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRValueParent, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRWeights, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRWeightsParent, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRWeightsParentArray, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRAnimCurveU, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRAnimCurveUParent, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRAnimCurveV, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRAnimCurveVParent, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRPivot, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRPivotArray, outputGeom)

    # Make deformer weights paintable
    cmds.makePaintable('LHSlideDeformer', 'weights', attrType='multiFloat', shapeMode='deformer')

####################################################
######## Initialize End ############################
####################################################

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Levi Harrison', '1.0', 'Any')
    try:
        plugin.registerNode('LHSlideDeformer', LHSlideDeformer.kPluginNodeId, creator, initialize, OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise RuntimeError('Failed to register node')
 
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(LHSlideDeformer.kPluginNodeId)
    except:
        raise RuntimeError('Failed to deregister node')
    
