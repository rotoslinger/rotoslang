            #if (itGeo.index() == 0):
            #    print slideUVec[0], slideUVec[1], slideUVec[2],

import math, sys
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds


class LHSlideDeformer(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00004005)


    # tAttrs    
    aSurface = OpenMaya.MObject()
    aSurfaceBase = OpenMaya.MObject()
    # nAttrs
    aUSlide = OpenMaya.MObject()
    aVSlide = OpenMaya.MObject()
    aRotationAmount = OpenMaya.MObject()
    # nAttrWeights
    aUWeights = OpenMaya.MObject()
    aVWeights = OpenMaya.MObject()
    aTxParamWeight = OpenMaya.MObject()
    aTyParamWeight = OpenMaya.MObject()
    aTzParamWeight = OpenMaya.MObject()
    # cAttrWeights
    aUWeightsParent = OpenMaya.MObject()
    aVWeightsParent = OpenMaya.MObject()
    aTxParamWeightParent = OpenMaya.MObject()
    aTyParamWeightParent = OpenMaya.MObject()
    aTzParamWeightParent = OpenMaya.MObject()
    # curve weights
    aUCurve = OpenMaya.MObject()
    aVCurve = OpenMaya.MObject()
    aWeightPatch = OpenMaya.MObject()
    aInputMatrix = OpenMaya.MObject()
     
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

        USlide = data.inputValue(LHSlideDeformer.aUSlide).asFloat()
        VSlide = data.inputValue(LHSlideDeformer.aVSlide).asFloat()
        rotationAmount = data.inputValue(LHSlideDeformer.aRotationAmount).asFloat()

        try:
            oSurface = data.inputValue(LHSlideDeformer.aSurface).asNurbsSurface()
            oSurfaceBase = data.inputValue(LHSlideDeformer.aSurfaceBase).asNurbsSurface()
            oUCurve = data.inputValue(LHSlideDeformer.aUCurve).asNurbsCurve()
            oVCurve = data.inputValue(LHSlideDeformer.aVCurve).asNurbsCurve()
            oWeightPatch = data.inputValue(LHSlideDeformer.aWeightPatch).asMesh()
            oInputMatrix = data.inputValue(LHSlideDeformer.aInputMatrix).asMatrix()
        except:
            pass

        if oSurface.isNull() or oSurfaceBase.isNull() or oUCurve.isNull() or oVCurve.isNull() or oWeightPatch.isNull():
            return
        plugInputMatrix = OpenMaya.MPlug( thisNode, LHSlideDeformer.aInputMatrix )


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
 
        #Dag Path UCurve
        dhUCurve = data.inputValue( self.aUCurve )
        fnUCurvePath = self.getConnectedDagNode( self.aUCurve )
        dagPathUCurve = OpenMaya.MDagPath()
	fnUCurvePath.getPath(dagPathUCurve)
	dagPathUCurve.extendToShape()
        fnUCurve = OpenMaya.MFnNurbsCurve( dagPathUCurve )

        #Dag Path VCurve
        dhVCurve = data.inputValue( self.aVCurve )
        fnVCurvePath = self.getConnectedDagNode( self.aVCurve )
        dagPathVCurve = OpenMaya.MDagPath()
	fnVCurvePath.getPath(dagPathVCurve)
	dagPathVCurve.extendToShape()
        fnVCurve = OpenMaya.MFnNurbsCurve( dagPathVCurve )


        # get dag path Surface Base
        dhWeightPatch = data.inputValue( self.aWeightPatch )
        fnWeightPatchPath = self.getConnectedDagNode( self.aWeightPatch )
        dagPathWeightPatch = OpenMaya.MDagPath()
	fnWeightPatchPath.getPath(dagPathWeightPatch)
	dagPathWeightPatch.extendToShape()
        fnWeightPatch = OpenMaya.MFnMesh( dagPathWeightPatch )



        # get weights

        uWeights = []
        uWeights = self.getWeightValues(data, LHSlideDeformer.aUWeightsParent, LHSlideDeformer.aUWeights, mIndex, uWeights )

        vWeights = []
        vWeights = self.getWeightValues(data, LHSlideDeformer.aVWeightsParent, LHSlideDeformer.aVWeights, mIndex, vWeights )
        
        # ReParamWeights
        TxParamWeight = []
        TxParamWeight = self.getWeightValues(data, LHSlideDeformer.aTxParamWeightParent, LHSlideDeformer.aTxParamWeight, mIndex, TxParamWeight )

        TyParamWeight = []
        TyParamWeight = self.getWeightValues(data, LHSlideDeformer.aTyParamWeightParent, LHSlideDeformer.aTyParamWeight, mIndex, TyParamWeight )

        TzParamWeight = []
        TzParamWeight = self.getWeightValues(data, LHSlideDeformer.aTzParamWeightParent, LHSlideDeformer.aTzParamWeight, mIndex, TzParamWeight )

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
                next(itGeo)
                continue
            ######################
            # uWeights
            try:
                uW = uWeights[itGeo.index()]
            except:
                uW = 1.0
            # vWeights
            try:
                vW = vWeights[itGeo.index()]
            except:
                vW = 1.0
            # TxParam
            try:
                txW = TxParamWeight[itGeo.index()]
            except:
                txW = 0.0
            # TyParam
            try:
                tyW = TyParamWeight[itGeo.index()]
            except:
                tyW = 0.0
            # TxParam
            try:
                tzW = TzParamWeight[itGeo.index()]
            except:
                tzW = 0.0

            ###################### 

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
            #uCurveWeightPt = fnUCurve.closestPoint( weightPt, fnParam, 0.00001, OpenMaya.MSpace.kWorld )
            fnWeightPatch.getUVAtPoint( weightPt, uvCoord, OpenMaya.MSpace.kWorld )

            uCoord = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvCoord, 0, 0 )
            vCoord = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvCoord, 0, 1 )
            uCoord = round(uCoord, 3)
            vCoord = round(vCoord, 3)
            
            #get point at param
            fnUCurve.getPointAtParam( uCoord, paramPoint, OpenMaya.MSpace.kWorld )


            #fnUCurve.getKnotDomain(fnMinParam,fnMaxParam)
            #MaxParam = OpenMaya.MScriptUtil.getDouble( fnMaxParam )
            #MinParam = OpenMaya.MScriptUtil.getDouble( fnMinParam )


            fnWeightPatch.getUVAtPoint( paramPoint, uvCoord, OpenMaya.MSpace.kWorld )

            uCoord = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvCoord, 0, 0 )
            vCoord = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvCoord, 0, 1 )
            uCoord = round(uCoord, 3)
            vCoord = round(vCoord, 3)




            if intersectYN == True:
                curveW = vCoord 
            if intersectYN == False:
                curveW = 0.0

            if (itGeo.index() == 3):
                print('UV', uCoord, vCoord)

            #######################################################
            slideUBasePtParam = 0.0
            slideVBasePtParam = 0.0

            dummyPoint = OpenMaya.MPoint(pt.x + (txW*10.0), pt.y + (tyW*10.0), pt.z + (tzW*10.0))


            #curveBasePt
            slideUVBasePt = fnSurfaceBase.closestPoint( dummyPoint, fnUParam, fnVParam, False, 0.00001, OpenMaya.MSpace.kWorld )
            #curveBasePtParam
            slideUBasePtParam = OpenMaya.MScriptUtil.getDouble( fnUParam )
            slideVBasePtParam = OpenMaya.MScriptUtil.getDouble( fnVParam )
            # get min and max parameter
            fnSurfaceBase.getKnotDomain(fnUMinParam,fnUMaxParam,fnVMinParam,fnVMaxParam)

            uMinParam = 0.0
            uMaxParam = 0.0
            vMinParam = 0.0
            vMaxParam = 0.0

            uMinParam = OpenMaya.MScriptUtil.getDouble( fnUMinParam )
            uMaxParam = OpenMaya.MScriptUtil.getDouble( fnUMaxParam )

            vMinParam = OpenMaya.MScriptUtil.getDouble( fnVMinParam )
            vMaxParam = OpenMaya.MScriptUtil.getDouble( fnVMaxParam )

            ######################
            ######## slideUV #######
            ######################

            slideUValue = USlide * uW * curveW
	    slideUCheck = slideUBasePtParam + slideUValue
	    slideUBasePtParamValue = None

            slideVValue = VSlide * vW
	    slideVCheck = slideVBasePtParam + slideVValue
	    slideVBasePtParamValue = None

            # remap thepLengthdir to the Parameter max becausepLengthdir cannot exceed 1 or go below 0 you know it will not exceed the maximum or minimum parameters
            # insure you never go over the curves highest and lowest params

            # UCheck
	    if (slideUCheck > uMinParam) or (slideUCheck < uMaxParam):
		slideUBasePtParamValue = slideUBasePtParam + slideUValue
	    if (slideUCheck <= uMinParam):
		slideUBasePtParamValue = uMinParam
	    if (slideUCheck >= uMaxParam):
		slideUBasePtParamValue = uMaxParam

            # VCheck
	    if (slideVCheck > vMinParam) or (slideVCheck < vMaxParam):
		slideVBasePtParamValue = slideVBasePtParam + slideVValue
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

		slideVValue = slideVValue + slideVBasePtParam
		slideUVPoint -= -slideVVec * slideVValue

            # V Max
	    if (slideVCheck >= vMaxParam) :
		#fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kWorld, fakePt2, fakeVecU, fakeVecV)
                slideVVec = fnVVec

		slideVValue = slideVValue + (slideVBasePtParam - vMaxParam)
		slideUVPoint -= -slideVVec * slideVValue

            # U Min
	    if (slideUCheck <= uMinParam) :
		#fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kWorld, fakePt2, fakeVecU, fakeVecV)
                slideUVec = fnUVec

		slideUValue = slideUValue + slideUBasePtParam
		slideUVPoint -= -slideUVec * slideUValue

            # U Max
	    if (slideUCheck >= uMaxParam) :
		#fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                fnSurface.getDerivativesAtParm( slideUBasePtParamValue, slideVBasePtParamValue, fakePt, fnUVec, fnVVec, OpenMaya.MSpace.kWorld, fakePt2, fakeVecU, fakeVecV)
                slideUVec = fnUVec

		slideUValue = slideUValue + (slideUBasePtParam - uMaxParam)
		slideUVPoint -= -slideUVec * slideUValue

##################################################################################################
############# Slide Ends #########################################################################
##################################################################################################

############ BaseVec for RotationCompensation #######################
            # get the closest point to base point, and then find rotation for it.
            fnSurfaceBase.getTangents( slideUBasePtParam, slideVBasePtParam, xVecBase, yVecBase, OpenMaya.MSpace.kWorld )

            xBaseVector = xVecBase
            yBaseVector = yVecBase
            zBaseVector = xVecBase ^  yVecBase

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

            ### ApplyRotation
            toCenterBase = OpenMaya.MVector(-slideUVBasePt.x, -slideUVBasePt.y, -slideUVBasePt.z)
            pt = pt + toCenterBase

            # do rotation, then put pts back
	    pt = ( pt * DriveMatrix ) - toCenterBase

	    pt.x +=(slideUVPoint.x - slideUVBasePt.x) * w# * curveW
	    pt.y +=(slideUVPoint.y - slideUVBasePt.y) * w# * curveW
	    pt.z +=(slideUVPoint.z - slideUVBasePt.z) * w# * curveW

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

    LHSlideDeformer.aUCurve = tAttr.create('uCurve', 'ucurve', OpenMaya.MFnData.kNurbsCurve)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aUCurve )

    LHSlideDeformer.aVCurve = tAttr.create('vCurve', 'vcurve', OpenMaya.MFnData.kNurbsCurve)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aVCurve )



    # numeric attributes

    # USlide
    LHSlideDeformer.aUSlide = nAttr.create('USlide', 'uslide', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(0.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUSlide)

 
    # VSlide
    LHSlideDeformer.aVSlide = nAttr.create('VSlide', 'vslide', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setDefault(0.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVSlide)




    LHSlideDeformer.aRotationAmount = nAttr.create('RotationAmount', 'rotamount', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    nAttr.setDefault(1.0)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aRotationAmount)



    # uWeights 
    LHSlideDeformer.aUWeights = tAttr.create('uWeights', 'uweights', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUWeights)
    # vWeights 
    LHSlideDeformer.aVWeights = tAttr.create('vWeights', 'vweights', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVWeights)

    # txWeights 
    LHSlideDeformer.aTxParamWeight = tAttr.create('txWeights', 'txweights', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aTxParamWeight)

    LHSlideDeformer.aTyParamWeight = tAttr.create('tyWeights', 'tyweights', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aTyParamWeight)

    LHSlideDeformer.aTzParamWeight = tAttr.create('tzWeights', 'tzweights', OpenMaya.MFnNumericData.kDoubleArray)
    tAttr.setKeyable(True)
    tAttr.setArray(False)
    LHSlideDeformer.addAttribute(LHSlideDeformer.aTzParamWeight)


    ####### weight compound attributes ########

    # uWeightsParent 
    LHSlideDeformer.aUWeightsParent = cAttr.create("uWeightsParent", "uweightsp")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aUWeights )
    cAttr.setReadable(True); 
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aUWeightsParent);

    # vWeightsParent 
    LHSlideDeformer.aVWeightsParent = cAttr.create("vWeightsParent", "vweightsp")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aVWeights )
    cAttr.setReadable(True); 
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aVWeightsParent);

    # txWeightsParent 
    LHSlideDeformer.aTxParamWeightParent = cAttr.create("txWeightsParent", "txweightsp")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aTxParamWeight )
    cAttr.setReadable(True); 
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aTxParamWeightParent);

    LHSlideDeformer.aTyParamWeightParent = cAttr.create("tyWeightsParent", "tyweightsp")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aTyParamWeight )
    cAttr.setReadable(True); 
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aTyParamWeightParent);

    LHSlideDeformer.aTzParamWeightParent = cAttr.create("tzWeightsParent", "tzweightsp")
    cAttr.setKeyable(True)
    cAttr.setArray(True)
    cAttr.addChild( LHSlideDeformer.aTzParamWeight )
    cAttr.setReadable(True); 
    cAttr.setUsesArrayDataBuilder(True); 
    LHSlideDeformer.addAttribute(LHSlideDeformer.aTzParamWeightParent);


    ###Affects outputs and inputs

    outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom


    # output


    # mAttrs

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aInputMatrix, outputGeom)

    # tAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aSurface, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aSurfaceBase, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aWeightPatch, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUCurve, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVCurve, outputGeom)


    # nAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUSlide, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVSlide, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRotationAmount, outputGeom)
    # weightAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUWeights, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVWeights, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aTxParamWeight, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aTyParamWeight, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aTzParamWeight, outputGeom)

    # weightParentAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUWeightsParent, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVWeightsParent, outputGeom)

    LHSlideDeformer.attributeAffects(LHSlideDeformer.aTxParamWeightParent, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aTyParamWeightParent, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aTzParamWeightParent, outputGeom)

    # Make deformer weights paintable
    cmds.makePaintable('LHSlideDeformer', 'weights', attrType='multiFloat', shapeMode='deformer')
    cmds.makePaintable('LHSlideDeformer', 'uWeights', attrType='doubleArray', shapeMode='deformer')
    cmds.makePaintable('LHSlideDeformer', 'vWeights', attrType='doubleArray', shapeMode='deformer')

    cmds.makePaintable('LHSlideDeformer', 'txWeights', attrType='doubleArray', shapeMode='deformer')
    cmds.makePaintable('LHSlideDeformer', 'tyWeights', attrType='doubleArray', shapeMode='deformer')
    cmds.makePaintable('LHSlideDeformer', 'tzWeights', attrType='doubleArray', shapeMode='deformer')


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
