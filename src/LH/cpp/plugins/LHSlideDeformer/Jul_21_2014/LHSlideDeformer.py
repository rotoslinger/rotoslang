            #if (itGeo.index() == 0):
            #    print slideUVec[0], slideUVec[1], slideUVec[2],
'''2-d rotation
def rotatePoint(centerPoint,point,angle):
    """Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point

print rotatePoint((1,1),(2,2),45)
'''
import math, sys
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.OpenMayaAnim as OpenMayaAnim

class LHSlideDeformer(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00004005)

    # tAttrs    
    aSurface = OpenMaya.MObject()
    aSurfaceBase = OpenMaya.MObject()
    # curve weights
    aWeightPatch = OpenMaya.MObject()
    aRotationAmount = OpenMaya.MObject()
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



    #OLD OBJECTS
    aInputMatrix = OpenMaya.MObject()

    aUSlideOLD = OpenMaya.MObject()
    aVSlideOLD = OpenMaya.MObject()
    # nAttrWeights
    aUWeightsOLD = OpenMaya.MObject()
    aVWeightsOLD = OpenMaya.MObject()
    # cAttrWeights
    aUWeightsOLDParent = OpenMaya.MObject()
    aVWeightsOLDParent = OpenMaya.MObject()






    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)

    def getConnectedDagNode( self, attrArg ):
        plugArg = OpenMaya.MPlug( self.thisMObject(), attrArg )
        dagPath = OpenMaya.MDagPath()
        if( plugArg.isConnected() ):
            plugArr = OpenMaya.MPlugArray()
            plugArg.connectedTo( plugArr, True, False )
            plugDag = OpenMaya.MPlug( plugArr[0] )
            oDagNode = plugDag.node()
            fnDagNode = OpenMaya.MFnDagNode( oDagNode )
            fnDagNode.getPath( dagPath )
            return dagPath
        else:
            return None
        
    def getCurveArrayDagNode( self, attrArg ):
        plugArg = attrArg
        dagPath = OpenMaya.MDagPath()
        if( plugArg.isConnected() ):
            plugArr = OpenMaya.MPlugArray()
            plugArg.connectedTo( plugArr, True, False )
            plugDag = OpenMaya.MPlug( plugArr[0] )
            oDagNode = plugDag.node()
            fnDagNode = OpenMaya.MFnDagNode( oDagNode )
            fnDagNode.getPath( dagPath )
            return dagPath
        else:
            return None

        
####################################################
######## get mfnNurbsCurves ##########################
####################################################

    ''' get anim curves for weighting '''
    def getMfnNurbsCurves(self, data, thisNode, curveParent, curveChild):
#         try:
        returnPoints= OpenMaya.MPointArray()
#         thisNode = self.thisMObject()
        parentPlug = OpenMaya.MPlug(thisNode, curveParent )
        count = parentPlug.numConnectedChildren()
        
        curveIndex = OpenMaya.MIntArray()
        parentPlug.getExistingArrayAttributeIndices(curveIndex)
        for i in curveIndex:
            childPlug = parentPlug.connectionByPhysicalIndex(i)
            oChild = childPlug.child(0)
            char = oChild.asFloat()
            fnCurvePath = self.getCurveArrayDagNode( oChild )
            dagPathCurve = OpenMaya.MDagPath()
            fnCurvePath.getPath(dagPathCurve)
            dagPathCurve.extendToShape()
            ### get Cvs from Curve
            fnNurbsCurve = OpenMaya.MFnNurbsCurve( dagPathCurve )
            curvePoints = OpenMaya.MPointArray()
            fnNurbsCurve.getCVs(curvePoints,OpenMaya.MSpace.kWorld)
            point = curvePoints[0]
            returnPoints.append(point)
        return returnPoints

####################################################
######## get anim curves ##########################
####################################################

    ''' get anim curves for weighting '''
    def getAnimCurves(self, data, thisNode, animCurveParent, animCurveChild):
#         try:
        returnAnimCurve= []
        returnTimeOffset= []
        returnTimeLength= []
#         thisNode = self.thisMObject()
        parentPlug = OpenMaya.MPlug(thisNode, animCurveParent )
        count = parentPlug.numConnectedChildren()
        
        curveIndex = OpenMaya.MIntArray()
        parentPlug.getExistingArrayAttributeIndices(curveIndex)
        for i in curveIndex:
            childPlug = parentPlug.connectionByPhysicalIndex(i)
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
#             print "ITER"
#         print "returnAnimCurve", len(returnAnimCurve)

        return returnTimeOffset, returnTimeLength, returnAnimCurve

####################################################
######## get Values ################################
####################################################

    def getValues(self, data, valueParent, valueChild, returnValuelist):
        try:
            arrayHandle = OpenMaya.MArrayDataHandle(data.inputArrayValue( valueParent ))
            count = arrayHandle.elementCount()
            temp= dict()
            for i in range(count):
                arrayHandle.jumpToElement(i)
                val = arrayHandle.inputValue().child( valueChild ).asFloat()
                temp[i] = val
            returnValuelist = temp.items()
        except:
            pass
            

                #uWeightArray = weightDict.items()
                #returnValuelist = OpenMaya.MFnDoubleArrayData(arrayHandle.data())
                #returnValuelist[i] = OpenMaya.MFnDoubleArrayData(child.data()).array()
                #print i, val

        #returnWeightlist = OpenMaya.MFnDoubleArrayData(handle.data()).array()
        return returnValuelist

####################################################
######## Weights ###################################
####################################################

    def getWeightValues(self, data, weightParent, weightChild, mIndex, returnWeightlist):
        
	arrayHandle = OpenMaya.MArrayDataHandle(data.inputArrayValue( weightParent ))
	count = arrayHandle.elementCount()
	result = 0.0
        if count and mIndex <= mIndex:
            try:
	        arrayHandle.jumpToElement(mIndex)

	        handle = OpenMaya.MDataHandle(arrayHandle.inputValue() )
	        child = OpenMaya.MDataHandle(handle.child( weightChild ) )
                newData = OpenMaya.MFnDoubleArrayData(child.data())
                returnWeightlist = OpenMaya.MFnDoubleArrayData(child.data()).array()
            except:
                pass

        #returnWeightlist = OpenMaya.MFnDoubleArrayData(handle.data()).array()
        return returnWeightlist
        
        
        
    def getWeightParentValues(self, data, weightParent, weightParentParent, weightChild, parentIndex, mIndex, returnWeightlist):
        result = 0.0
        try:
            #parentArray
            arrayHandleParentParent = OpenMaya.MArrayDataHandle(data.inputArrayValue( weightParentParent ))
            countParentParent = arrayHandleParentParent.elementCount()
            arrayHandleParentParent.jumpToArrayElement(parentIndex)
            
            
            #parent
            hArrayHandleParent = arrayHandleParentParent.inputValue().child(weightParent)
            hArrayHandleParentArray = OpenMaya.MArrayDataHandle(hArrayHandleParent)
            countParent = hArrayHandleParentArray.elementCount()
            
            #child
            hArrayHandleParentArray.jumpToElement(mIndex)
            handle = OpenMaya.MDataHandle(hArrayHandleParentArray.inputValue() )
            child = OpenMaya.MDataHandle(handle.child( weightChild ) )
            newData = OpenMaya.MFnDoubleArrayData(child.data())
            returnWeightlist = OpenMaya.MFnDoubleArrayData(child.data()).array()
        except:
            pass               

                
        return returnWeightlist
        
####################################################
######## Weights End ###############################
####################################################

####################################################
######## Deform ###################################
####################################################

    def deform(self, data, itGeo, localToWorldMatrix, mIndex):
        thisNode = self.thisMObject()
        Envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
        envelope = data.inputValue(Envelope).asFloat()

        USlide = data.inputValue(LHSlideDeformer.aUSlideOLD).asFloat()
        VSlide = data.inputValue(LHSlideDeformer.aVSlideOLD).asFloat()
        rotationAmount = data.inputValue(LHSlideDeformer.aRotationAmount).asFloat()

        try:
            oSurface = data.inputValue(LHSlideDeformer.aSurface).asNurbsSurface()
            oSurfaceBase = data.inputValue(LHSlideDeformer.aSurfaceBase).asNurbsSurface()
            oWeightPatch = data.inputValue(LHSlideDeformer.aWeightPatch).asMesh()
            oInputMatrix = data.inputValue(LHSlideDeformer.aInputMatrix).asMatrix()

        except:
            pass

        if oSurface.isNull() or oSurfaceBase.isNull() or oWeightPatch.isNull():
            return
        plugInputMatrix = OpenMaya.MPlug( thisNode, LHSlideDeformer.aInputMatrix )

        # AnimCURVE BLAHHHHHH
        # they idea here is to fine the time range of all the keys and convert that to  0-1 range
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
        # well, you simply subtract 98.3, then, then do the steps above.
        # simple. sweet. easy

        # get dag path Surface
        dhSurface = data.inputValue( self.aSurface )
        fnSurfacePath = self.getConnectedDagNode( self.aSurface )
        dagPathSurface = OpenMaya.MDagPath()
	fnSurfacePath.getPath(dagPathSurface)
	dagPathSurface.extendToShape()
        #Surface
        fnSurface = OpenMaya.MFnNurbsSurface( dagPathSurface )

        # get dag path Surface Base
        dhSurfaceBase = data.inputValue( self.aSurfaceBase )
        fnSurfaceBasePath = self.getConnectedDagNode( self.aSurfaceBase )
        dagPathSurfaceBase = OpenMaya.MDagPath()
	fnSurfaceBasePath.getPath(dagPathSurfaceBase)
	dagPathSurfaceBase.extendToShape()
        #Surface Base
        fnSurfaceBase = OpenMaya.MFnNurbsSurface( dagPathSurfaceBase )
 

        # get dag path Surface Base
        dhWeightPatch = data.inputValue( self.aWeightPatch )
        fnWeightPatchPath = self.getConnectedDagNode( self.aWeightPatch )
        dagPathWeightPatch = OpenMaya.MDagPath()
	fnWeightPatchPath.getPath(dagPathWeightPatch)
	dagPathWeightPatch.extendToShape()
        fnWeightPatch = OpenMaya.MFnMesh( dagPathWeightPatch )



        # get weights

        uWeightsOld = []
        uWeightsOld = self.getWeightValues(data, LHSlideDeformer.aUWeightsOLDParent, LHSlideDeformer.aUWeightsOLD, mIndex, uWeightsOld )

        vWeightsOld = []
        vWeightsOld = self.getWeightValues(data, LHSlideDeformer.aVWeightsOLDParent, LHSlideDeformer.aVWeightsOLD, mIndex, vWeightsOld )
        



        
        
        ##################################
        #get multiValues and multi weights
        ##################################
        ################
        #####  U  ######
        ################
        uValsArray = []
        uWeightArray = []
        # Values
        try:
            uValsArray = self.getValues(data, LHSlideDeformer.aUValueParent, LHSlideDeformer.aUValue, uValsArray )
        except:
            pass
        weightDict= dict()
        numValues = len(uValsArray)
        # Weights
        try:
            for i in range(numValues):
            # a loop that goes through every childIndex of aUWeightsParentArray and gets weights for it at the mIndex
                uWeightArray = self.getWeightParentValues(data, LHSlideDeformer.aUWeightsParent, LHSlideDeformer.aUWeightsParentArray, LHSlideDeformer.aUWeights,i, mIndex, uWeightArray )
                weightDict[i] = uWeightArray
        except:
            pass
        uWeightArray = weightDict.items()
        
        
        ################
        #####  V  ######
        ################
        vValsArray = []
        vWeightArray = []
        # Values
        try:
            vValsArray = self.getValues(data, LHSlideDeformer.aVValueParent, LHSlideDeformer.aVValue, vValsArray )
        except:
            pass
        weightDict= dict()
        numValues = len(vValsArray)
        # Weights
        try:
            for i in range(numValues):
            # a loop that goes through every childIndex of aVWeightsParentArray and gets weights for it at the mIndex
                vWeightArray = self.getWeightParentValues(data, LHSlideDeformer.aVWeightsParent, LHSlideDeformer.aVWeightsParentArray, LHSlideDeformer.aVWeights,i, mIndex, vWeightArray )
                weightDict[i] = vWeightArray
        except:
            pass
        vWeightArray = weightDict.items()

        ################
        #####  N  ######
        ################
        nValsArray = []
        nWeightArray = []
        # Values
        try:
            nValsArray = self.getValues(data, LHSlideDeformer.aNValueParent, LHSlideDeformer.aNValue, nValsArray )
        except:
            pass
        weightDict= dict()
        numValues = len(nValsArray)
        # Weights
        try:
            for i in range(numValues):
            # a loop that goes through every childIndex of aNWeightsParentArray and gets weights for it at the mIndex
                nWeightArray = self.getWeightParentValues(data, LHSlideDeformer.aNWeightsParent, LHSlideDeformer.aNWeightsParentArray, LHSlideDeformer.aNWeights,i, mIndex, nWeightArray )
                weightDict[i] = nWeightArray
        except:
            pass
        nWeightArray = weightDict.items()

        ################
        #####  R  ######
        ################
        rValsArray = []
        rWeightArray = []
        # Values
        try:
            rValsArray = self.getValues(data, LHSlideDeformer.aRValueParent, LHSlideDeformer.aRValue, rValsArray )
        except:
            pass
        weightDict= dict()
        numValues = len(rValsArray)
        # Weights
        try:
            for i in range(numValues):
            # a loop that goes through every childIndex of aRWeightsParentArray and gets weights for it at the mIndex
                rWeightArray = self.getWeightParentValues(data, LHSlideDeformer.aRWeightsParent, LHSlideDeformer.aRWeightsParentArray, LHSlideDeformer.aRWeights,i, mIndex, rWeightArray )
                weightDict[i] = rWeightArray
        except:
            pass
        rWeightArray = weightDict.items()



        ##################################
        #########     ends     ###########
        ##################################


        ##################################
        ####   get multiAnimCurves    ####
        ##################################
        returnVals = []
        ################
        #####  UU  ######
        ################
        #retrieve u curves
        uUFnCurvesArray = []
        uUTimeLengthArray = []
        uUTimeOffsetArray = []
        try:
            returnVals = self.getAnimCurves(data, thisNode,
                                            LHSlideDeformer.aUAnimCurveUParent,
                                            LHSlideDeformer.aUAnimCurveU)
            
            uUTimeOffsetArray = returnVals[0]
            uUTimeLengthArray = returnVals[1]
            uUFnCurvesArray = returnVals[2]
        except:
            pass
        
        if len(uUFnCurvesArray) == 0:
            uUTimeOffsetArray = [0]
            uUTimeLengthArray = [0]
            uUFnCurvesArray = [0]
            
        ################
        #####  UV  ######
        ################
        #retrieve v curves
        uVFnCurvesArray = []
        uVTimeLengthArray = []
        uVTimeOffsetArray = []
        try:
            returnVals = self.getAnimCurves(data, thisNode,
                                            LHSlideDeformer.aUAnimCurveVParent,
                                            LHSlideDeformer.aUAnimCurveV)
            uVTimeOffsetArray = returnVals[0]
            uVTimeLengthArray = returnVals[1]
            uVFnCurvesArray = returnVals[2]
#             uVFnCurvesArray.append(returnVals[2])
        except:
            pass
        if len(uVFnCurvesArray) == 0:
            uVTimeOffsetArray = [0]
            uVTimeLengthArray = [0]
            uVFnCurvesArray = [0]
        ################
        #####  VU  ######
        ################
        #retrieve u curves
        vUFnCurvesArray = []
        vUTimeLengthArray = []
        vUTimeOffsetArray = []
        try:
            returnVals = self.getAnimCurves(data, thisNode,
                                            LHSlideDeformer.aVAnimCurveUParent,
                                            LHSlideDeformer.aVAnimCurveU)
            
            vUTimeOffsetArray = returnVals[0]
            vUTimeLengthArray = returnVals[1]
            vUFnCurvesArray = returnVals[2]
        except:
            pass
        
        if len(vUFnCurvesArray) == 0:
            vUTimeOffsetArray = [0]
            vUTimeLengthArray = [0]
            vUFnCurvesArray = [0]
            
        ################
        #####  VV  ######
        ################
        #retrieve v curves
        vVFnCurvesArray = []
        vVTimeLengthArray = []
        vVTimeOffsetArray = []
        try:
            returnVals = self.getAnimCurves(data, thisNode,
                                            LHSlideDeformer.aVAnimCurveVParent,
                                            LHSlideDeformer.aVAnimCurveV)
            vVTimeOffsetArray = returnVals[0]
            vVTimeLengthArray = returnVals[1]
            vVFnCurvesArray = returnVals[2]
        except:
            pass
        if len(vVFnCurvesArray) == 0:
            vVTimeOffsetArray = [0]
            vVTimeLengthArray = [0]
            vVFnCurvesArray = [0]
            
            
        ################
        #####  NU  ######
        ################
        #retrieve u curves
        nUFnCurvesArray = []
        nUTimeLengthArray = []
        nUTimeOffsetArray = []
        try:
            returnVals = self.getAnimCurves(data, thisNode,
                                            LHSlideDeformer.aNAnimCurveUParent,
                                            LHSlideDeformer.aNAnimCurveU)
            
            nUTimeOffsetArray = returnVals[0]
            nUTimeLengthArray = returnVals[1]
            nUFnCurvesArray = returnVals[2]
        except:
            pass
        
        if len(nUFnCurvesArray) == 0:
            nUTimeOffsetArray = [0]
            nUTimeLengthArray = [0]
            nUFnCurvesArray = [0]
            
        ################
        #####  NV  ######
        ################
        #retrieve v curves
        nVFnCurvesArray = []
        nVTimeLengthArray = []
        nVTimeOffsetArray = []
        try:
            returnVals = self.getAnimCurves(data, thisNode,
                                            LHSlideDeformer.aNAnimCurveVParent,
                                            LHSlideDeformer.aNAnimCurveV)
            nVTimeOffsetArray = returnVals[0]
            nVTimeLengthArray = returnVals[1]
            nVFnCurvesArray = returnVals[2]
        except:
            pass
        if len(nVFnCurvesArray) == 0:
            nVTimeOffsetArray = 0
            nVTimeLengthArray = 0
            nVFnCurvesArray = 0

        ################
        #####  RU  ######
        ################
        #retrieve u curves
        rUFnCurvesArray = []
        rUTimeLengthArray = []
        rUTimeOffsetArray = []
        try:
            returnVals = self.getAnimCurves(data, thisNode,
                                            LHSlideDeformer.aRAnimCurveUParent,
                                            LHSlideDeformer.aRAnimCurveU)
            
            rUTimeOffsetArray = returnVals[0]
            rUTimeLengthArray = returnVals[1]
            rUFnCurvesArray = returnVals[2]
        except:
            pass
        
        if len(rUFnCurvesArray) == 0:
            rUTimeOffsetArray = [0]
            rUTimeLengthArray = [0]
            rUFnCurvesArray = [0]
            
        ################
        #####  RV  ######
        ################
        #retrieve v curves
        rVFnCurvesArray = []
        rVTimeLengthArray = []
        rVTimeOffsetArray = []
        try:
            returnVals = self.getAnimCurves(data, thisNode,
                                            LHSlideDeformer.aRAnimCurveVParent,
                                            LHSlideDeformer.aRAnimCurveV)
            rVTimeOffsetArray = returnVals[0]
            rVTimeLengthArray = returnVals[1]
            rVFnCurvesArray = returnVals[2]
        except:
            pass
        if len(rVFnCurvesArray) == 0:
            rVTimeOffsetArray = 0
            rVTimeLengthArray = 0
            rVFnCurvesArray = 0

        
        # get r pivots
        ##################################
        ####   get rotate pivots    ####
        ##################################
        rotPoints = []
        ################
        #####  UU  ######
        ################
        #retrieve u curves
        rotPoints = self.getMfnNurbsCurves(data, thisNode,
                                        LHSlideDeformer.aRPivotArray,
                                        LHSlideDeformer.aRPivot)
        
        '''
        rotPoints= []
#         thisNode = self.thisMObject()
        parentPlug = OpenMaya.MPlug(thisNode, LHSlideDeformer.aRPivotArray )
        count = parentPlug.numConnectedChildren()
        
        curveIndex = OpenMaya.MIntArray()
        parentPlug.getExistingArrayAttributeIndices(curveIndex)
        for i in curveIndex:
            childPlug = parentPlug.connectionByPhysicalIndex(i)
            oChild = childPlug.child(0)
            
            fnCurvePath = self.getCurveArrayDagNode( oChild )
            
            
            
            dagPathCurve = OpenMaya.MDagPath()
            fnCurvePath.getPath(dagPathCurve)
            dagPathCurve.extendToShape()
            ### get Cvs from Curve
            fnNurbsCurve = OpenMaya.MFnNurbsCurve( dagPathCurve )
            curvePoints = OpenMaya.MPointArray()
            fnNurbsCurve.getCVs(curvePoints,OpenMaya.MSpace.kWorld)
            rotPoints.append(curvePoints[0])
            '''
#         print rotPoints[0].x
        ##############################################        ##############################################
        # uParam
        fnRUDouble = OpenMaya.MScriptUtil()
        fnRUDouble.createFromDouble(0.0)
        fnRUParam = fnRUDouble.asDoublePtr()
        # vParam
        fnRVDouble = OpenMaya.MScriptUtil()
        fnRVDouble.createFromDouble(0.0)
        fnRVParam = fnRVDouble.asDoublePtr()

        rotUParams = []
        rotVParams = []
#         rotUOffset = []
#         rotVOffset = []
#         try:
        #in order to get the rotate pivot when it falls outside the patch you can find the 
        for i in range(rotPoints.length()):
            fnSurfaceBase.closestPoint( rotPoints[i], fnRUParam, fnRVParam, False, 0.00001, OpenMaya.MSpace.kWorld )
            #curveBasePtParam
            uParam = OpenMaya.MScriptUtil.getDouble( fnRUParam )
            vParam = OpenMaya.MScriptUtil.getDouble( fnRVParam )
#             uParam = uParam + uValsArray[i][1]
#             vParam = vParam + vValsArray[i][1]
            rotUParams.append(uParam)
            rotVParams.append(vParam)
            
#         except:
#             pass
#         print rotUParams





        ##################################
        #############  end   #############
        ##################################


        #variables to be used with the loop
        # curve Param
        fnDouble = OpenMaya.MScriptUtil()
        fnDouble.createFromDouble(0.0)
        fnParam = fnDouble.asDoublePtr()

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
        rotUVPoint = OpenMaya.MPoint()

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
        weightIntersect = OpenMaya.MMeshIntersector()
        weightIntersect.create(oWeightPatch, weightMatrix)
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
        while not itGeo.isDone():
            pt = itGeo.position()
            w = self.weightValue(data, mIndex, itGeo.index())
            w = w * envelope
            #pt *= localToWorldMatrix
            #neutralPt = pt
            if w <= 0:
                itGeo.next()
                continue
            ######################
            # uWeights
            try:
                oldUW = uWeightsOld[itGeo.index()]
            except:
                oldUW = 1.0
            # vWeights
            #try:
            #    oldVW = vWeightsOld[itGeo.index()]
            #except:
            #    oldVW = 1.0
            try:
                oldVW = vWeightsOld[itGeo.index()]
            except:
                oldVW = 0.0
            # TxParam
                
                
            ##########################
            #### painted Weights U ###
            ##########################
            allUVals = dict()
            rotUVals = dict()

            
            #help(allUVals)
            for i in range(numValues):
                try:
                    tempUW = uWeightArray[i][1][itGeo.index()]
                    tempUVal = uValsArray[i][1]
                except:
                    tempUW = 0.0
                    tempUVal = 0.0
                #uW is equal to the sum of all uweights and uvalues
                
                allUVals[i] = tempUW * tempUVal
                rotUVals[i] = tempUVal
            allUVals = allUVals.values()
            rotUVals = rotUVals.values()
#             uW = sum(allUVals)
            
            ##########################
            #### painted Weights V ###
            ##########################
            
            allVVals = dict()
            rotVVals = dict()
            
            #help(allUVals)
            for i in range(numValues):
                try:
                    tempVW = vWeightArray[i][1][itGeo.index()]
                    tempVVal = vValsArray[i][1]
                except:
                    tempVW = 0.0
                    tempVVal = 0.0
                #uW is equal to the sum of all uweights and uvalues
                
                allVVals[i] = tempVW * tempVVal
                rotVVals[i] = tempUVal
                    
            allVVals = allVVals.values()
            rotVVals = rotVVals.values()
            
            ##########################
            #### painted Weights N ###
            ##########################
            allNVals = dict()
            
            #help(allUVals)
            for i in range(numValues):
                try:
                    tempNW = nWeightArray[i][1][itGeo.index()]
                    tempNVal = nValsArray[i][1]
                except:
                    tempNW = 0.0
                    tempNVal = 0.0
                #uW is equal to the sum of all uweights and uvalues
                
                allNVals[i] = tempNW * tempNVal
                    
            allNVals = allNVals.values()
            
            ##########################
            #### painted Weights R ###
            ##########################
            allRVals = dict()
            
            #help(allUVals)
            for i in range(numValues):
                try:
                    tempRW = rWeightArray[i][1][itGeo.index()]
                    tempRVal = rValsArray[i][1]
                except:
                    tempRW = 0.0
                    tempRVal = 0.0
                #uW is equal to the sum of all uweights and uvalues
                
                allRVals[i] = tempRW * tempRVal
                    
            allRVals = allRVals.values()
            
            
            ###################### 
            #### curveWeights #### 
            ###################### 

            #project weights based on Nurbs Patch
            #weightPt = OpenMaya.MPoint(0.0,0.0,0.0)
            fnWeightPatch.getClosestPoint( pt, weightPt, OpenMaya.MSpace.kWorld )

            rayDirection = OpenMaya.MVector(0.0,0.0,0.0)
            fnWeightPatch.getClosestNormal( pt, rayDirection, OpenMaya.MSpace.kWorld )
            rayFloatDirection = OpenMaya.MFloatVector(rayDirection[0], rayDirection[1], rayDirection[2])
            rayFloatPt= OpenMaya.MFloatPoint(pt.x, pt.y, pt.z)

            hitPt = OpenMaya.MFloatPoint(0.0,0.0,0.0)
            intersectYN = fnWeightPatch.anyIntersection( rayFloatPt, rayFloatDirection, None, None, False, OpenMaya.MSpace.kWorld, 100.0, True, None, hitPt, None, None, None, None, None, 0.00001)

            # we need to chart each point to the weight patch and find determine how much influence it has based on how much of an arc it has
            #getUCurveWeight Find nearest point on curve
            fnWeightPatch.getUVAtPoint( weightPt, uvCoord, OpenMaya.MSpace.kWorld )

            uCoord = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvCoord, 0, 0 )
            vCoord = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvCoord, 0, 1 )
            uCoord = round(uCoord, 3)
            vCoord = round(vCoord, 3)
            
            #get closest point to uv parameter
            
            
            
            
            ################
            #####  U  ######
            ################

            ########################
            # get uvAnimCurveWeights#
            ########################
            allUVAnimCurveWeights = dict()
            for i in range(len(uVTimeLengthArray)):
                uVRemap = OpenMaya.MTime(vCoord * uVTimeLengthArray[i])
                uVRemap = uVRemap - uVTimeOffsetArray[i]
                uVWeight = uVFnCurvesArray[i].evaluate(uVRemap)
                allUVAnimCurveWeights[i] = uVWeight 
            allUVAnimCurveWeights = allUVAnimCurveWeights.values()
            
            ########################
            # get uuAnimCurveWeights#
            ########################
            allUUAnimCurveWeights = dict()
            for i in range(len(uUTimeLengthArray)):
                uURemap = OpenMaya.MTime(uCoord * uUTimeLengthArray[i])
                uURemap = uURemap - uUTimeOffsetArray[i]
                uUWeight = uUFnCurvesArray[i].evaluate(uURemap)
                allUUAnimCurveWeights[i] = uUWeight 
            allUUAnimCurveWeights = allUUAnimCurveWeights.values()

            ################
            #####  V  ######
            ################

            ########################
            # get vVAnimCurveWeights#
            ########################
                       
            allVVAnimCurveWeights = dict()
            for i in range(len(vVTimeLengthArray)):
                vVRemap = OpenMaya.MTime(vCoord * vVTimeLengthArray[i])
                vVRemap = vVRemap - vVTimeOffsetArray[i]
                vVWeight = vVFnCurvesArray[i].evaluate(vVRemap)
                allVVAnimCurveWeights[i] = vVWeight 
            allVVAnimCurveWeights = allVVAnimCurveWeights.values()

            ########################
            # get vUAnimCurveWeights#
            ########################
                       
            allVUAnimCurveWeights = dict()
            for i in range(len(vUTimeLengthArray)):
                vURemap = OpenMaya.MTime(uCoord * vUTimeLengthArray[i])
                vURemap = vURemap - vUTimeOffsetArray[i]
                vUWeight = vUFnCurvesArray[i].evaluate(vURemap)
                allVUAnimCurveWeights[i] = vUWeight 
            allVUAnimCurveWeights = allVUAnimCurveWeights.values()

            ################
            #####  N  ######
            ################

            ########################
            # get nVAnimCurveWeights#
            ########################
            if nVFnCurvesArray == 0:
                allNVAnimCurveWeights = 1
            elif len(nVFnCurvesArray) > 0:
                allNVAnimCurveWeights = dict()
                for i in range(len(nVTimeLengthArray)):
                    nVRemap = OpenMaya.MTime(vCoord * nVTimeLengthArray[i])
                    nVRemap = nVRemap - nVTimeOffsetArray[i]
                    nVWeight = nVFnCurvesArray[i].evaluate(nVRemap)
                    allNVAnimCurveWeights[i] = nVWeight 
                allNVAnimCurveWeights = allNVAnimCurveWeights.values()

            ########################
            # get nUAnimCurveWeights#
            ########################
            if nVFnCurvesArray == 0:
                allNVAnimCurveWeights = 1
            elif len(nVFnCurvesArray) > 0:
                allNUAnimCurveWeights = dict()
                for i in range(len(nUTimeLengthArray)):
                    nURemap = OpenMaya.MTime(uCoord * nUTimeLengthArray[i])
                    nURemap = nURemap - nUTimeOffsetArray[i]
                    nUWeight = nUFnCurvesArray[i].evaluate(nURemap)
                    allNUAnimCurveWeights[i] = nUWeight 
                allNUAnimCurveWeights = allNUAnimCurveWeights.values()
                
            ################
            #####  R  ######
            ################

            ########################
            # get rVAnimCurveWeights#
            ########################
            if rVFnCurvesArray == 0:
                allRVAnimCurveWeights = 1
            elif len(rVFnCurvesArray) > 0:
                allRVAnimCurveWeights = dict()
                for i in range(len(rVTimeLengthArray)):
                    rVRemap = OpenMaya.MTime(vCoord * rVTimeLengthArray[i])
                    rVRemap = rVRemap - rVTimeOffsetArray[i]
                    rVWeight = rVFnCurvesArray[i].evaluate(rVRemap)
                    allRVAnimCurveWeights[i] = rVWeight 
                allRVAnimCurveWeights = allRVAnimCurveWeights.values()

            ########################
            # get rUAnimCurveWeights#
            ########################
            if rVFnCurvesArray == 0:
                allRVAnimCurveWeights = 1
            elif len(rVFnCurvesArray) > 0:
                allRUAnimCurveWeights = dict()
                for i in range(len(rUTimeLengthArray)):
                    rURemap = OpenMaya.MTime(uCoord * rUTimeLengthArray[i])
                    rURemap = rURemap - rUTimeOffsetArray[i]
                    rUWeight = rUFnCurvesArray[i].evaluate(rURemap)
                    allRUAnimCurveWeights[i] = rUWeight 
                allRUAnimCurveWeights = allRUAnimCurveWeights.values()

            ############################
            ###### U V N R combine #####
            ############################

            #---Multiply painted weights by curve weights
            # the length of all arrays should be the same
            # this is currently up to the user
            # but I should write a failsafe
            for i in range(len(allUVals)):
                allUVals[i] = (allUVals[i] *
                               allUVAnimCurveWeights[i] *
                               allUUAnimCurveWeights[i])
                allVVals[i] = (allVVals[i] *
                               allVVAnimCurveWeights[i] *
                               allVUAnimCurveWeights[i])
                if nVFnCurvesArray == 0:
                    pass
                elif len(nVFnCurvesArray) > 0:
                    allNVals[i] = (allNVals[i] *
                                   allNVAnimCurveWeights[i] *
                                   allNUAnimCurveWeights[i])
                if rVFnCurvesArray == 0:
                    pass
                elif len(rVFnCurvesArray) > 0:
                    allRVals[i] = (allRVals[i] *
                                   allRVAnimCurveWeights[i] *
                                   allRUAnimCurveWeights[i])
                    


                    

            uW = sum(allUVals)
            vW = sum(allVVals)
            nW = sum(allNVals)
            rW = sum(allRVals)

            ######################
            ######## rotUV #######
            ######################
#             pivotU = .5
#             pivotV = .5
#             
#             surfaceRot = uW-pivotU , vW-pivotV
#             surfaceRot = ( surfaceRot[0]*math.cos(rW)-surfaceRot[1]*math.sin(rW) , surfaceRot[0]*math.sin(rW)+surfaceRot[1]*math.cos(rW))
#             surfaceRot = surfaceRot[0]+pivotU , surfaceRot[1]+pivotV
#             
#             uW = surfaceRot[0]
#             vW = surfaceRot[1]
# 
#             if uW < 0:
#                 uW = 0
#             if uW > 1:
#                 uW = 1
#             if vW < 0:
#                 vW = 0
#             if vW > 1:
#                 vW = 1
            


#             if intersectYN == True:
#                 uW = uW
#                 vW = vW

            if intersectYN == False:
                uW = 0.0
                vW = 0.0
                nW = 0.0
            #if (itGeo.index() == 3):
            #    print 'UV', uCoord, vCoord

            #######################################################
            slideUBasePtParam = 0.0
            slideVBasePtParam = 0.0



            #curveBasePt
            slideUVBasePt = fnSurfaceBase.closestPoint( pt, fnUParam, fnVParam, False, 0.00001, OpenMaya.MSpace.kWorld )
            #curveBasePtParam
            slideUBasePtParam = OpenMaya.MScriptUtil.getDouble( fnUParam )
            slideVBasePtParam = OpenMaya.MScriptUtil.getDouble( fnVParam )
            # get min and max parameter
            fnSurfaceBase.getKnotDomain(fnUMinParam,fnUMaxParam,fnVMinParam,fnVMaxParam)
            # get normal
            slideBaseNormal = fnSurfaceBase.normal( slideUBasePtParam, slideVBasePtParam, OpenMaya.MSpace.kWorld )
            slideNormal = fnSurfaceBase.normal( slideUBasePtParam, slideVBasePtParam, OpenMaya.MSpace.kWorld )
            uMinParam = 0.0
            uMaxParam = 0.0
            vMinParam = 0.0
            vMaxParam = 0.0

            uMinParam = OpenMaya.MScriptUtil.getDouble( fnUMinParam )
            uMaxParam = OpenMaya.MScriptUtil.getDouble( fnUMaxParam )

            vMinParam = OpenMaya.MScriptUtil.getDouble( fnVMinParam )
            vMaxParam = OpenMaya.MScriptUtil.getDouble( fnVMaxParam )
            
            slideUValue = uW
            slideUCheck = slideUBasePtParam + slideUValue
            slideUBasePtParamValue = None

            slideVValue = vW
            slideVCheck = slideVBasePtParam + slideVValue
            slideVBasePtParamValue = None

            '''
            ######################
            ######## rotUVOLD #######
            ######################
            
            pivotU = rotUParams[2]
            pivotV = rotVParams[2]
            surfaceRot = slideUCheck-pivotU , slideVCheck-pivotV
            surfaceRot = ( surfaceRot[0]*math.cos(rW)-surfaceRot[1]*math.sin(rW) , surfaceRot[0]*math.sin(rW)+surfaceRot[1]*math.cos(rW))
            surfaceRot = surfaceRot[0]+pivotU , surfaceRot[1]+pivotV
               
            slideUCheck = surfaceRot[0]
            slideVCheck = surfaceRot[1]
            
            rotSlideUValue = surfaceRot[0]
            rotSlideVValue = surfaceRot[1]


            '''
            ######################
            ######## slideUV #######
            ######################
            

            allURotVals = []
            allVRotVals = []
#             print "SlideUCheckBefore",slideUCheck
            for i in range(len(rotUParams)):
                pivotU = rotUParams[i]
                pivotV = rotVParams[i]
                surfaceRot = slideUCheck-pivotU , slideVCheck-pivotV
                surfaceRot = ( surfaceRot[0]*math.cos(allRVals[i])-surfaceRot[1]*math.sin(allRVals[i]) , surfaceRot[0]*math.sin(allRVals[i])+surfaceRot[1]*math.cos(allRVals[i]))
                surfaceRot = surfaceRot[0]+pivotU , surfaceRot[1]+pivotV
                    
#                 slideUCheck = surfaceRot[0]
#                 slideVCheck = surfaceRot[1]
                 
                rotSlideU = surfaceRot[0]
                rotSlideV = surfaceRot[1]
                 
                allURotVals.append(rotSlideU)
                allVRotVals.append(rotSlideV)
                 
#                 allSlideUCheckVals.append(slideUCheck)
#                 allSlideVCheckVals.append(slideVCheck)
# 
#             rotSlideUValue = allURotVals[2]
#             rotSlideVValue = allVRotVals[2]
#             slideUCheck = rotSlideUValue
#             slideVCheck = rotSlideVValue
#             print allURotVals
            rotSlideUValue = sum(allURotVals)+ (-1.0 * (2 * slideUCheck))
            rotSlideVValue = sum(allVRotVals)+ (-1.0 * (2 * slideVCheck))
            slideUCheck = rotSlideUValue
            slideVCheck = rotSlideVValue
#             print "SlideUCheckAfter",slideUCheck

#             uCheckOffset = -1 * 
            
#             slideUCheck = rotSlideUValue + (-1.0 * (2 * slideUCheck))
#             slideVCheck = rotSlideVValue + (-1.0 * (2 * slideVCheck))
#             print "SlideUCheckAfter",slideUCheck
#             if len(allURotVals) > 0:
#                 rotSlideUValue = sum(allURotVals)- (slideUCheck * (len(allURotVals)-1))
#                 slideUCheck = rotSlideUValue
#             else :
#                 rotSlideUValue = 0
#             
#             if len(allVRotVals) > 0:
#                 rotSlideVValue = sum(allVRotVals)- (slideUCheck * (len(allURotVals)-1))
#                 slideVCheck = rotSlideVValue
#             else :
#                 rotSlideUValue = 0
                        

            
            
            
            
            
#             if slideUCheck < 0:
#                 slideUCheck = 0
#             if slideUCheck > 1:
#                 slideUCheck = 1
#             if slideVCheck < 0:
#                 slideVCheck = 0
#             if slideVCheck > 1:
#                 slideVCheck = 1

            # UCheck
            if (slideUCheck > uMinParam) or (slideUCheck < uMaxParam):
                slideUBasePtParamValue = rotSlideUValue
            if (slideUCheck <= uMinParam):
                slideUBasePtParamValue = uMinParam
            if (slideUCheck >= uMaxParam):
                slideUBasePtParamValue = uMaxParam

            # VCheck
            if (slideVCheck > vMinParam) or (slideVCheck < vMaxParam):
                slideVBasePtParamValue = rotSlideVValue
            if (slideVCheck <= vMinParam):
                slideVBasePtParamValue = vMinParam
            if (slideVCheck >= vMaxParam):
                slideVBasePtParamValue = vMaxParam
    
            # use U and V attributes to drive sliding on a surface
            # if surface goes further than the surface, find the last point traveled over, get the tangent in that direction, and have the pt travel on in that vector forever

            ## U and V on surface
            if (slideUCheck > uMinParam) or (slideUCheck < uMaxParam) and (slideVCheck > vMinParam) or (slideVCheck < vMaxParam):
                fnSurface.getPointAtParam( slideUBasePtParamValue, slideVBasePtParamValue, slideUVPoint, OpenMaya.MSpace.kWorld )
            # V Min
            if (slideVCheck <= vMinParam) :
                #fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kWorld, fakePt2, fakeVecU, fakeVecV)
                slideVVec = fnVVec
                slideVValue = rotSlideVValue + slideVBasePtParam
                slideUVPoint -= -slideVVec * rotSlideVValue

            # V Max
            if (slideVCheck >= vMaxParam) :
                #fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kWorld, fakePt2, fakeVecU, fakeVecV)
                slideVVec = fnVVec
                rotSlideVValue = rotSlideVValue -1
                slideVValue = rotSlideVValue + (slideVBasePtParam - vMaxParam)
                slideUVPoint -= -slideVVec * rotSlideVValue

            # U Min
            if (slideUCheck <= uMinParam) :
                #fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kWorld, fakePt2, fakeVecU, fakeVecV)
                slideUVec = fnUVec
#                 rotSlideUValue = rotSlideUValue -pivotU

                slideUValue = rotSlideUValue + slideUBasePtParam
                slideUVPoint -= -slideUVec * rotSlideUValue

            # U Max
            if (slideUCheck >= uMaxParam) :
            #fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kWorld, fakePt2, fakeVecU, fakeVecV)
                slideUVec = fnUVec
                rotSlideUValue = rotSlideUValue -1
                slideUValue = rotSlideUValue + (slideUBasePtParam - uMaxParam)
                slideUVPoint -= -slideUVec * rotSlideUValue

##################################################################################################
############# Slide Ends #########################################################################
##################################################################################################

############ BaseVec for RotationCompensation #######################
            # get the closest point to base point, and then find rotation for it.
#             if slideUBasePtParam < 0:
#                 slideUBasePtParam = slideUBasePtParam * -slideUBasePtParam
#             if slideVBasePtParam < 0:
#                 slideVBasePtParam = slideVBasePtParam * -slideVBasePtParam
                
            ######################
            ######## rotUV #######
            ######################
#             pivotU = .5
#             pivotV = .5
#             rotUBasePtParam = slideUValue   
#             rotVBasePtParam = slideVValue           
#             surfaceRot = rotUBasePtParam-pivotU , rotVBasePtParam-pivotV
#             surfaceRot = ( surfaceRot[0]*math.cos(rW)-surfaceRot[1]*math.sin(rW) , surfaceRot[0]*math.sin(rW)+surfaceRot[1]*math.cos(rW))
#             surfaceRot = surfaceRot[0]+pivotU , surfaceRot[1]+pivotV
#                
#             rotUBasePtParam = abs(surfaceRot[0])
#             rotVBasePtParam = abs(surfaceRot[1])
#    
#             if rotUBasePtParam < 0:
#                 rotUBasePtParam = 0
#             if rotUBasePtParam > 1:
#                 rotUBasePtParam = 1
#             if rotVBasePtParam < 0:
#                 rotVBasePtParam = 0
#             if rotVBasePtParam > 1:
#                 rotVBasePtParam = 1
#             fnSurfaceBase.getPointAtParam( rotUBasePtParam, rotVBasePtParam, rotUVPoint, OpenMaya.MSpace.kWorld )
#             pt +=(rotUVPoint - slideUVBasePt) * w
                
                
                
                
            fnSurfaceBase.getTangents( slideUBasePtParam, slideVBasePtParam, xVecBase, yVecBase, OpenMaya.MSpace.kWorld )

            xBaseVector = xVecBase
            yBaseVector = yVecBase
            zBaseVector = xVecBase ^ yVecBase

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

#############################################################################################
            fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, xVec, yVec, OpenMaya.MSpace.kWorld )

            xAxisVec = xVec
            yAxisVec = yVec
            zAxisVec = xVec ^  yVec
            

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
            DriveMatrixEuler = OpenMaya.MEulerRotation( DriveMatrixEuler[0] * rotationAmount, DriveMatrixEuler[1] * rotationAmount, DriveMatrixEuler[2] * rotationAmount)
            DriveMatrix = DriveMatrixEuler.asMatrix()
            ### apply normal translation before anything else
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

            '''2-d rotation
            def rotatePoint(centerPoint,point,angle):
                """Rotates a point around another centerPoint. Angle is in degrees.
                Rotation is counter-clockwise"""
                angle = math.radians(angle)
                temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
                temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
                temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
                return temp_point
            
            print rotatePoint((1,1),(2,2),45)
            '''
            
#             pivotUV = []
#             UVCoords = []
#             angle = rw
#             pivotU = .5
#             pivotV = .5
# 
#             
#             surfaceRot = slideUBasePtParam-pivotU , slideVBasePtParam-pivotV
#             surfaceRot = ( surfaceRot[0]*math.cos(rW)-surfaceRot[1]*math.sin(rW) , surfaceRot[0]*math.sin(rW)+surfaceRot[1]*math.cos(rW))
#             surfaceRot = surfaceRot[0]+pivotU , surfaceRot[1]+pivotV
#             
#             fnSurface.getPointAtParam( surfaceRot[0], surfaceRot[1], rotUVPoint, OpenMaya.MSpace.kWorld )
            #pt +=(rotUVPoint - slideUVBasePt) * w
            
            '''
            ######################
            ######## rotUVNEW #######
            ######################

            
            #curveBasePt
            slideUVBasePt = fnSurfaceBase.closestPoint( pt, fnUParam, fnVParam, False, 0.00001, OpenMaya.MSpace.kWorld )
            #curveBasePtParam
            slideUBasePtParam = OpenMaya.MScriptUtil.getDouble( fnUParam )
            slideVBasePtParam = OpenMaya.MScriptUtil.getDouble( fnVParam )
            # get min and max parameter
             
            ######################
            ######## rotUV #######
            ######################
            pivotU = .5
            pivotV = .5
            rotUBasePtParam = slideUBasePtParam   
            rotVBasePtParam = slideVBasePtParam           
            surfaceRot = rotUBasePtParam-pivotU , rotVBasePtParam-pivotV
            surfaceRot = ( surfaceRot[0]*math.cos(rW)-surfaceRot[1]*math.sin(rW) , surfaceRot[0]*math.sin(rW)+surfaceRot[1]*math.cos(rW))
            surfaceRot = surfaceRot[0]+pivotU , surfaceRot[1]+pivotV
              
            rotUBasePtParam = abs(surfaceRot[0])
            rotVBasePtParam = abs(surfaceRot[1])
  
            if rotUBasePtParam < 0:
                rotUBasePtParam = 0
            if rotUBasePtParam > 1:
                rotUBasePtParam = 1
            if rotVBasePtParam < 0:
                rotVBasePtParam = 0
            if rotVBasePtParam > 1:
                rotVBasePtParam = 1
            fnSurfaceBase.getPointAtParam( rotUBasePtParam, rotVBasePtParam, rotUVPoint, OpenMaya.MSpace.kWorld )
            pt +=(rotUVPoint - slideUVBasePt) * w
            '''


            itGeo.setPosition(pt)
            itGeo.next()

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
    mAttr = OpenMaya.MFnMatrixAttribute()
    ##### typed attributes ######


    # aInputMatrix
    LHSlideDeformer.aInputMatrix = mAttr.create( "inputMatrix", "inputMatrix", OpenMaya.MFnData.kMatrix)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aInputMatrix )

    # surface
    LHSlideDeformer.aSurface = tAttr.create('surface', 'surf', OpenMaya.MFnData.kNurbsSurface)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aSurface )
    # base
    LHSlideDeformer.aSurfaceBase = tAttr.create('surfaceBase', 'surfbase', OpenMaya.MFnData.kNurbsSurface)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aSurfaceBase )

    # weight patch
    LHSlideDeformer.aWeightPatch = tAttr.create('weightPatch', 'wpatch', OpenMaya.MFnData.kMesh)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aWeightPatch )

    # numeric attributes

    LHSlideDeformer.aRotationAmount = nAttr.create('RotationAmount', 'rotamount', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aRotationAmount)
    
    
    ######### UATTRS ###########################

    ############ VALUE ##########################
    LHSlideDeformer.aUValue = nAttr.create('uValue', 'uvalue', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(0.0)
#     LHSlideDeformer.addAttribute(LHSlideDeformer.aUValue)

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
#     LHSlideDeformer.addAttribute(LHSlideDeformer.aUWeights)

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
    #LHSlideDeformer.addAttribute(LHSlideDeformer.aUAnimCurveV)

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
#     LHSlideDeformer.addAttribute(LHSlideDeformer.aNValue)

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
#     LHSlideDeformer.addAttribute(LHSlideDeformer.aNWeights)

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
    #LHSlideDeformer.addAttribute(LHSlideDeformer.aNAnimCurveU)

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
#     LHSlideDeformer.addAttribute(LHSlideDeformer.aRValue)

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
#     LHSlideDeformer.addAttribute(LHSlideDeformer.aRWeights)

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
    #LHSlideDeformer.addAttribute(LHSlideDeformer.aRAnimCurveU)

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
    #LHSlideDeformer.addAttribute(LHSlideDeformer.aRAnimCurveV)

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


    ######################
    ######## OLD #########
    ######################
    # USlide
    LHSlideDeformer.aUSlideOLD = nAttr.create('USlide', 'uslide', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(0.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUSlideOLD)

    # VSlide
    LHSlideDeformer.aVSlideOLD = nAttr.create('VSlide', 'vslide', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(0.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVSlideOLD)

    # uWeightsOld 
    LHSlideDeformer.aUWeightsOLD = tAttr.create('uWeightsOLD', 'uweightsold', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUWeightsOLD)
    # vWeightsOld 
    LHSlideDeformer.aVWeightsOLD = tAttr.create('vWeightsOLD', 'vweightsold', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVWeightsOLD)

    ####### weight compound attributes ########

    # uWeightsParent 
    LHSlideDeformer.aUWeightsOLDParent = cAttr.create("uWeightsParentOLD", "uweightspold")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aUWeightsOLD )
    cAttr.setReadable(True); 
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUWeightsOLDParent);

    # vWeightsParent 
    LHSlideDeformer.aVWeightsOLDParent = cAttr.create("vWeightsParentOLD", "vweightspold")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aVWeightsOLD )
    cAttr.setReadable(True); 
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVWeightsOLDParent);




    ###Affects outputs and inputs

    outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom


    # output


    # mAttrs

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aInputMatrix, outputGeom)

    # tAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aSurface, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aSurfaceBase, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aWeightPatch, outputGeom)

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

    # OLD


    # nAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUSlideOLD, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVSlideOLD, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRotationAmount, outputGeom)
    # weightAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUWeightsOLD, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVWeightsOLD, outputGeom)

    # weightParentAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUWeightsOLDParent, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVWeightsOLDParent, outputGeom)


    # Make deformer weights paintable
    cmds.makePaintable('LHSlideDeformer', 'weights', attrType='multiFloat', shapeMode='deformer')
    cmds.makePaintable('LHSlideDeformer', 'uWeightsOLD', attrType='doubleArray', shapeMode='deformer')
    cmds.makePaintable('LHSlideDeformer', 'vWeightsOLD', attrType='doubleArray', shapeMode='deformer')
    
    cmds.makePaintable('LHSlideDeformer', 'uWeights', attrType='doubleArray', shapeMode='deformer')
    
    # turn off cycle check for rotate pivots
    
####################################################
######## Initialize End ############################
####################################################



def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Levi Harrison', '1.0', 'Any')
    try:
        plugin.registerNode('LHSlideDeformer', LHSlideDeformer.kPluginNodeId, creator, initialize, OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise RuntimeError, 'Failed to register node'
 
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(LHSlideDeformer.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to deregister node'
    
'''cmds.addAttr('LHSlideDeformer1', longName = 'uWeights003Parent', shortName = 'uweights003parent', numberOfChildren = 1, attributeType = 'compound',multi = True, indexMatters=True)
cmds.addAttr('LHSlideDeformer1', longName = 'uWeights003', shortName = 'uweights003', dataType = 'doubleArray', parent = 'uWeights003Parent')
cmds.makePaintable('LHSlideDeformer', 'uWeights003', attrType='doubleArray', shapeMode='deformer')

nurbsPlaneShape1

cmds.connectAttr('LHSlideDeformer1.uWeights001Parent[4]', 'LHSlideDeformer1.uWeightsParentArray[0].uWeightsParent[4]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights001Parent[5]', 'LHSlideDeformer1.uWeightsParentArray[0].uWeightsParent[5]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights001Parent[6]', 'LHSlideDeformer1.uWeightsParentArray[0].uWeightsParent[6]', force=True)

cmds.connectAttr('LHSlideDeformer1.uWeights002Parent[4]', 'LHSlideDeformer1.uWeightsParentArray[1].uWeightsParent[4]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights002Parent[5]', 'LHSlideDeformer1.uWeightsParentArray[1].uWeightsParent[5]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights002Parent[6]', 'LHSlideDeformer1.uWeightsParentArray[1].uWeightsParent[6]', force=True)


cmds.connectAttr('LHSlideDeformer1.uWeights003Parent[4]', 'LHSlideDeformer1.uWeightsParentArray[2].uWeightsParent[4]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights003Parent[5]', 'LHSlideDeformer1.uWeightsParentArray[2].uWeightsParent[5]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights003Parent[6]', 'LHSlideDeformer1.uWeightsParentArray[2].uWeightsParent[6]', force=True)




cmds.connectAttr('LHSlideDeformer1.uWeights001Parent[4]', 'LHSlideDeformer1.vWeightsParentArray[0].vWeightsParent[4]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights001Parent[5]', 'LHSlideDeformer1.vWeightsParentArray[0].vWeightsParent[5]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights001Parent[6]', 'LHSlideDeformer1.vWeightsParentArray[0].vWeightsParent[6]', force=True)

cmds.connectAttr('LHSlideDeformer1.uWeights002Parent[4]', 'LHSlideDeformer1.vWeightsParentArray[1].vWeightsParent[4]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights002Parent[5]', 'LHSlideDeformer1.vWeightsParentArray[1].vWeightsParent[5]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights002Parent[6]', 'LHSlideDeformer1.vWeightsParentArray[1].vWeightsParent[6]', force=True)


cmds.connectAttr('LHSlideDeformer1.uWeights003Parent[4]', 'LHSlideDeformer1.vWeightsParentArray[2].vWeightsParent[4]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights003Parent[5]', 'LHSlideDeformer1.vWeightsParentArray[2].vWeightsParent[5]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights003Parent[6]', 'LHSlideDeformer1.vWeightsParentArray[2].vWeightsParent[6]', force=True)
















cmds.connectAttr('LHSlideDeformer1.uWeights001Parent[4]', 'LHSlideDeformer1.nWeightsParentArray[0].nWeightsParent[4]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights001Parent[5]', 'LHSlideDeformer1.nWeightsParentArray[0].nWeightsParent[5]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights001Parent[6]', 'LHSlideDeformer1.nWeightsParentArray[0].nWeightsParent[6]', force=True)

cmds.connectAttr('LHSlideDeformer1.uWeights002Parent[4]', 'LHSlideDeformer1.nWeightsParentArray[1].nWeightsParent[4]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights002Parent[5]', 'LHSlideDeformer1.nWeightsParentArray[1].nWeightsParent[5]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights002Parent[6]', 'LHSlideDeformer1.nWeightsParentArray[1].nWeightsParent[6]', force=True)


cmds.connectAttr('LHSlideDeformer1.uWeights003Parent[4]', 'LHSlideDeformer1.nWeightsParentArray[2].nWeightsParent[4]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights003Parent[5]', 'LHSlideDeformer1.nWeightsParentArray[2].nWeightsParent[5]', force=True)
cmds.connectAttr('LHSlideDeformer1.uWeights003Parent[6]', 'LHSlideDeformer1.nWeightsParentArray[2].nWeightsParent[6]', force=True)










cmds.connectAttr('A_LMouthLRVSlideU_0.output', 'LHSlideDeformer1.vAnimCurveUArray[0].vAnimCurveU', force=True)
cmds.connectAttr('B_RMouthLRVSlideU_1.output', 'LHSlideDeformer1.vAnimCurveUArray[1].vAnimCurveU', force=True)
cmds.connectAttr('C_MouthLRVSlideU_2.output', 'LHSlideDeformer1.vAnimCurveUArray[2].vAnimCurveU', force=True)

cmds.connectAttr('ZA_LMouthUDUSlideU_0.output', 'LHSlideDeformer1.uAnimCurveUArray[0].uAnimCurveU', force=True)
cmds.connectAttr('ZB_RMouthUDUSlideU_1.output', 'LHSlideDeformer1.uAnimCurveUArray[1].uAnimCurveU', force=True)
cmds.connectAttr('ZC_MouthUDUSlideU_2.output', 'LHSlideDeformer1.uAnimCurveUArray[2].uAnimCurveU', force=True)

cmds.connectAttr('D_MouthLRFalloffVSlideV.output', 'LHSlideDeformer1.vAnimCurveVArray[0].vAnimCurveV', force=True)
cmds.connectAttr('D_MouthLRFalloffVSlideV.output', 'LHSlideDeformer1.vAnimCurveVArray[1].vAnimCurveV', force=True)
cmds.connectAttr('D_MouthLRFalloffVSlideV.output', 'LHSlideDeformer1.vAnimCurveVArray[2].vAnimCurveV', force=True)

cmds.connectAttr('ZD_MouthUDFalloffUSlideV.output', 'LHSlideDeformer1.uAnimCurveVArray[0].uAnimCurveV', force=True)
cmds.connectAttr('ZD_MouthUDFalloffUSlideV.output', 'LHSlideDeformer1.uAnimCurveVArray[1].uAnimCurveV', force=True)
cmds.connectAttr('ZD_MouthUDFalloffUSlideV.output', 'LHSlideDeformer1.uAnimCurveVArray[2].uAnimCurveV', force=True)
'''