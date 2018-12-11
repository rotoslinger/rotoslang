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
    # cAttrWeights
    aUWeightsParent = OpenMaya.MObject()
    aVWeightsParent = OpenMaya.MObject()
     
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

        Envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
        envelope = data.inputValue(Envelope).asFloat()

        USlide = data.inputValue(LHSlideDeformer.aUSlide).asFloat()
        VSlide = data.inputValue(LHSlideDeformer.aVSlide).asFloat()
        rotationAmount = data.inputValue(LHSlideDeformer.aRotationAmount).asFloat()

        try:
            oSurface = data.inputValue(LHSlideDeformer.aSurface).asNurbsSurface()
            oSurfaceBase = data.inputValue(LHSlideDeformer.aSurfaceBase).asNurbsSurface()
        except:
            raise RuntimeError, "One or more surfaces are not connected"

        if oSurface.isNull() or oSurfaceBase.isNull():
            return


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
 
        # get weights

        uWeights = []
        uWeights = self.getWeightValues(data, LHSlideDeformer.aUWeightsParent, LHSlideDeformer.aUWeights, mIndex, uWeights )

        vWeights = []
        vWeights = self.getWeightValues(data, LHSlideDeformer.aVWeightsParent, LHSlideDeformer.aVWeights, mIndex, vWeights )

        #variables to be used with the loop

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

        #fnUVecThreeFloat = OpenMaya.MScriptUtil()
        #fnUVecThreeFloat.createFromList([1.0,1.0,1.0], 3)
        #fnUVec = fnUVecThreeFloat.asFloat3Ptr()
        # U vector

        fnUVec = OpenMaya.MVector(0.0,0.0,0.0)
        fnVVec = OpenMaya.MVector(0.0,0.0,0.0)

        xVec = OpenMaya.MVector(0.0,0.0,0.0)
        yVec = OpenMaya.MVector(0.0,0.0,0.0)
        zVec = OpenMaya.MVector(0.0,0.0,0.0)
        xVecBase = OpenMaya.MVector(0.0,0.0,0.0)
        yVecBase = OpenMaya.MVector(0.0,0.0,0.0)
        zVecBase = OpenMaya.MVector(0.0,0.0,0.0)
        #help(fnUVec)

        #f2_util = om.MScriptUtil()
        #f2_util.createFromList( [0.0, 0.0], 2)
        #f2_ptr = f2_util.asFloat2Ptr()
        BaseMatrix = OpenMaya.MMatrix()
        DriveMatrix = OpenMaya.MMatrix()
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
                uW = uWeights[itGeo.index()]
            except:
                uW = 1.0
            # vWeights
            try:
                vW = vWeights[itGeo.index()]
            except:
                vW = 1.0
            ###################### 
            slideUBasePtParam = 0.0
            slideVBasePtParam = 0.0

            #curveBasePt
            slideUVBasePt = fnSurfaceBase.closestPoint( pt, fnUParam, fnVParam, False, 0.00001, OpenMaya.MSpace.kWorld )
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

            #slideUVec = OpenMaya.MVector(0.0,0.0,0.0)
            #slideVVec = OpenMaya.MVector(0.0,0.0,0.0)


            #fnUVec = OpenMaya.MVector(0.0,0.0,0.0)
            #fnVVec = OpenMaya.MVector(0.0,0.0,0.0)


            ######################
            ######## slideUV #######
            ######################

            slideUValue = USlide * uW
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

            #if (itGeo.index() == 0):
            #    print slideUVec[0], slideUVec[1], slideUVec[2],

            # use U and V attributes to drive sliding on a surface
            # if surface goes further than the surface, find the last CV the point traveled over, get the tangent in that direction, and have the pt travel on in that vector forever
            # because this is a surface you will need to chart both the U and V point at the same time
            # this means you must find all of the possibilities of where the point could be
            # this is just like the curve deformer, only you have to find all of the different possibilities of where a point could be
            ## U and V on surface
            # U on V off in max
            # U on V off in min
            # U off in max V on
            # U off in min V on 
            # U and V off in max
            # U and V off in min
            # U off in max, V off in min
            # U off in min, V off in max

	    #### make vector or point on curve depending on slideUValue value
            ## U and V on surface
	    if (slideUCheck > uMinParam) or (slideUCheck < uMaxParam) and (slideVCheck > vMinParam) or (slideVCheck < vMaxParam):
		fnSurface.getPointAtParam( slideUBasePtParamValue, slideVBasePtParamValue, slideUVPoint, OpenMaya.MSpace.kWorld )



            # V Min
	    if (slideVCheck <= vMinParam) :
		fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                slideVVec = fnVVec

		slideVValue = slideVValue + slideVBasePtParam
		slideUVPoint -= -slideVVec * slideVValue

            # V Max
	    if (slideVCheck >= vMaxParam) :
		fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                slideVVec = fnVVec

		slideVValue = slideVValue + (slideVBasePtParam - vMaxParam)
		slideUVPoint -= -slideVVec * slideVValue




            # U Min
	    if (slideUCheck <= uMinParam) :
		fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                slideUVec = fnUVec

		slideUValue = slideUValue + slideUBasePtParam
		slideUVPoint -= -slideUVec * slideUValue



            # U Max
	    if (slideUCheck >= uMaxParam) :
		fnSurface.getTangents( slideUBasePtParamValue, slideVBasePtParamValue, fnUVec, fnVVec, OpenMaya.MSpace.kWorld )
                slideUVec = fnUVec

		slideUValue = slideUValue + (slideUBasePtParam - uMaxParam)
		slideUVPoint -= -slideUVec * slideUValue

##################################################################################################
############# Slide Ends #########################################################################
##################################################################################################





##################################################

############ BaseVec for RotationCompensation #######################
            # get the closest point to base point, and then find rotation for it.
            ##slideUVBasePt = fnSurfaceBase.closestPoint( pt, fnUParam, fnVParam, False, 0.00001, OpenMaya.MSpace.kWorld )
            fnSurfaceBase.getTangents( slideUBasePtParam, slideVBasePtParam, xVecBase, yVecBase, OpenMaya.MSpace.kWorld )

            xBaseVector = xVecBase
            yBaseVector = yVecBase
            zBaseVector = xVecBase ^  yVecBase

            #if (itGeo.index() == 0):
            #    print xBaseVector[0], xBaseVector[1], xBaseVector[2],
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

            DriveMatrixEuler = OpenMaya.MEulerRotation()
            DriveMatrixEuler = DriveMatrixEuler.decompose(DriveMatrix,0)
            DriveMatrixEuler = OpenMaya.MEulerRotation( DriveMatrixEuler[0] * rotationAmount, DriveMatrixEuler[1] * rotationAmount, DriveMatrixEuler[2] * rotationAmount)
            DriveMatrix = DriveMatrixEuler.asMatrix()




            ### ApplyRotation
            toCenterBase = OpenMaya.MVector(-slideUVBasePt.x, -slideUVBasePt.y, -slideUVBasePt.z)
            pt = pt + toCenterBase

            # do rotation, then put pts back
	    pt = ( pt * DriveMatrix ) - toCenterBase




            #pt = pt + (SlidePoints[itGeo.index()] - pt) * USlide * w
	    pt.x +=(slideUVPoint.x - slideUVBasePt.x) * w
	    pt.y +=(slideUVPoint.y - slideUVBasePt.y) * w
	    pt.z +=(slideUVPoint.z - slideUVBasePt.z) * w

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
 
    ##### typed attributes ######

    # surface
    LHSlideDeformer.aSurface = tAttr.create('surface', 'surf', OpenMaya.MFnData.kNurbsSurface)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aSurface )
    # base
    LHSlideDeformer.aSurfaceBase = tAttr.create('surfaceBase', 'surfbase', OpenMaya.MFnData.kNurbsSurface)
    LHSlideDeformer.addAttribute( LHSlideDeformer.aSurfaceBase )

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

    ###### weight numeric attributes ######


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

    ###Affects outputs and inputs

    outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom


    # output

    # tAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aSurface, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aSurfaceBase, outputGeom)
    # nAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUSlide, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVSlide, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aRotationAmount, outputGeom)
    # weightAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUWeights, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVWeights, outputGeom)
    # weightParentAttrs
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aUWeightsParent, outputGeom)
    LHSlideDeformer.attributeAffects(LHSlideDeformer.aVWeightsParent, outputGeom)

    # Make deformer weights paintable
    cmds.makePaintable('LHSlideDeformer', 'weights', attrType='multiFloat', shapeMode='deformer')

    cmds.makePaintable('LHSlideDeformer', 'uWeights', attrType='doubleArray', shapeMode='deformer')
    cmds.makePaintable('LHSlideDeformer', 'vWeights', attrType='doubleArray', shapeMode='deformer')

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
