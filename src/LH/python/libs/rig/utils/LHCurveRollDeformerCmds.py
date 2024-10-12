import maya.cmds as cmds
#===============================================================================
#CLASS:         curve rollDeformerCmd
#DESCRIPTION:   Creates an LHCurveRollDeformer
#USAGE:         Select driverSurface and geometry[] or set args
#RETURN:        LHCurveRollDeformer
#AUTHOR:        Levi Harrison
#DATE:          August 1st, 2014
#Version        1.0.0
#===============================================================================

class curveRollDeformerCmd():
    def __init__(self,
                 weightGeo = '',
                 weightBase = [],
                 inCurve = '',
                 outCurve = '',
                 geoms = [],
                 control = "",
                 ihi = 0,
                 side='C',
                 name='',
                 lockAttrs = 1,
                 rNames = [],
                 orientToCurve = True,
                 rollVector='',
                 animCurveSuffix="ACV",
                 deformerSuffix="CRD"
                 ):
        """
                                     
        type  weightGeo:            string (mesh)
        param weightGeo:            the name of the geo that will be used to
                                     raycast weighting
                                     
        type  inCurve:              string (curve)
        param inCurve:              the name of the curve that will be used as
                                     a pivot
        
        
        
        type  geoms:                string array
        param geoms:                the names of the geometry the will be deformed,
                                     or the second selection and beyond 
                                     can be mesh, nurbsSurface, or nurbsCurve

        type  control:              string
        param control:              where to put attributes, usually a control
                                     if unset attributes will be created on 
                                     the returned deformer

        type  ihi:                  int
        param ihi:                  sets the deformer isHistoricallyIntersting to 0

        type  lockAttrs:            int
        param lockAttrs:            if set to 1 all attributes in return 
                                     deformer are locked and hidden

        type  side:                 string
        param side:                 defaults to C but L and R are also acceptable
        
        type  rNames:               string array
        param rNames:               names of attributes
                                             
        type  orientToCurve:        bool
        param orientToCurve:        whether or not the roll is oriented to the
                                     curve.  If False a 2 point curve (rollVec)
                                     will be created that can be used to specify 
                                     a custom pivot.  The pivot position will
                                     remain on the closest point to the curve,
                                     but the rotation pivot will be inherited 
                                     from a vector that is created by
                                     subtracting the first and second points of
                                     the new curve.
                                             
        type  rollVec:              string
        param rollVec:              OPTIONAL: a specify a rollVec curve here.
                                     Should be a 2 point curve.   If specified
                                     a new curve will not be created.
                                     

        """
        #----args
        self.geoms                   = geoms
        self.inCurve                 = inCurve
        self.outCurve                = outCurve
        self.weightGeo               = weightGeo
        self.weightBase              = weightBase
        self.orientToCurve           = orientToCurve
        self.rollVector              = rollVector
        self.control                 = control

        self.lockAttrs               = lockAttrs
        self.ihi                     = ihi
        self.side                    = side
        self.name                    = name
        self.rNames                  = rNames
        self.animCurveSuffix         = animCurveSuffix
        self.deformerSuffix          = deformerSuffix
        #----vars
        self.inCurveShape            = ''
        self.outCurveShape           = ''
        self.weightGeoShape          = ''
        self.weightBaseShapes        = []
        self.geomShapes              = []
        self.returnDeformer          = ''
        self.deformerName            = ''
        self.rValAttrs               = []
        self.rWeights                = []
        self.rAnimCurvesU            = []
        self.rAnimCurvesV            = []
        self.rollVecShape            = ""
        #----created attrs
        #----deformer attr default values
        #----procedures
        self.__create()

    def __getTypeArg(self):
        """get argument type (user defined or selected)"""
        if (self.inCurve and self.outCurve and self.weightGeo and self.geoms):
            return
        else:
            self.__getSelectedArgs()

    def __getSelectedArgs(self):
        """gets selected args if you are selecting, you must use the weight
           geo, if you do not want weight geo you must specify in the args"""
        try:
            sel = cmds.ls(sl=True)
            self.inCurve = sel[0]
            self.outCurve = sel[1]

            self.weightGeo = sel[2]
            self.geoms = sel[3:]
        except:
            raise Exception('''please give arguments (inCurve, outCurve, weightMesh, and geoms) ''')
            quit()
    def __getShape(self):
        """gets shape"""
        try:
            self.weightGeoShape = cmds.listRelatives(self.weightGeo, shapes = True)[0]
            self.inCurveShape = cmds.listRelatives(self.inCurve, shapes = True)[0]
            self.outCurveShape = cmds.listRelatives(self.outCurve, shapes = True)[0]
            try:
                for i in range(len(self.geoms)):
                    temp = cmds.listRelatives(self.geoms[i], shapes = True)[0]
                    self.geomShapes.append(temp)
            except:
                self.geomShapes = self.geoms
                
            try:
                for i in range(len(self.weightBase)):
                    temp = cmds.listRelatives(self.weightBase[i], shapes = True)[0]
                    self.weightBaseShapes.append(temp)
            except:
                pass
                
        except:
            raise Exception('''one or more argument did not have a shape \n' ''')
            quit()
        print(self.weightBase)

    def __checkArgs(self):
        """checks the args to make sure they are the right type"""
        if (cmds.objectType(self.inCurveShape, isType='nurbsCurve') == True):
            if (cmds.objectType(self.weightGeoShape, isType='mesh') == True):
                return
            return
        else:
            raise Exception('''arguments curve and weightGeo are not of required type nurbsCurve and mesh ''')
            quit()

    def __checkGeomArgs(self):
        """checks the args to make sure they are the right type"""
        for i in self.geomShapes:
            if ((cmds.objectType(i, isType='nurbsSurface') == True) or
                (cmds.objectType(i, isType='nurbsCurve') == True) or
                (cmds.objectType(i, isType='mesh') == True)) :
                continue
            else:
                raise Exception( i + ' is not supported geometry \n')
                quit()
                
    def __createCurveRollDeformer(self):
        """creates the wrap deformer"""
        self.returnDeformer = cmds.deformer(self.geoms, 
                                            type = 'LHCurveRollDeformer',
                                            name= self.side + "_" +
                                                  self.name + "_" + self.deformerSuffix)[0]

    def __createRollVec(self):
        if self.orientToCurve == False:
            if not self.rollVector:
                self.rollVector = cmds.curve(name= self.name + 'Vector_CRV',
                              d=1, p=[(0,0,0),(0,0,1)],
                              k=[0,1])
                self.rollVecShape = cmds.listRelatives(self.rollVector, shapes = True)[0]
            else:
                self.rollVecShape = cmds.listRelatives(self.rollVector, shapes = True)[0]
    def __createAttrs(self):
        """add u and v attrs to control"""
        
        if not self.control:
            self.control = self.returnDeformer
        #----rValAttr
        for i in self.rNames:
            cmds.addAttr(self.control, longName= i,
                                at='float', keyable=True)
            self.rValAttrs.append(self.control + '.' + i)

    def __createWeights(self):
        """add u and v weights to deformer"""

        #----rWeights
        for i in self.rNames:
            cmds.addAttr(self.returnDeformer,
                         longName = i + 'Weights',
                         numberOfChildren = 1, 
                         attributeType = 'compound',
                         multi = True, 
                         indexMatters=True)
            cmds.addAttr(self.returnDeformer,
                         longName = i + "Weight",
                         dataType = 'doubleArray',
                         parent = i + 'Weights')
            cmds.makePaintable('LHCurveRollDeformer', i + "Weight", attrType='doubleArray', shapeMode='deformer')
            self.rWeights.append(self.returnDeformer + "." + i +'Weights')

    def __createAnimCurves(self):
        """add anim curves"""
        for i in range(len(self.rNames)):
                    self.rAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                            name = self.rNames[i]
                                                            + "_" + self.animCurveSuffix))
                    self.rAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                            name = self.rNames[i]
                                                            + "Falloff" + "_" + self.animCurveSuffix))

    def __setAnimCurveShapes(self):
        """set anim curve shapes default is a straight line with a value of 1"""
        #----R
        for i in range(len(self.rAnimCurvesU)):
            cmds.setKeyframe(self.rAnimCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, time = 0)
        for i in range(len(self.rAnimCurvesV)):
            cmds.setKeyframe(self.rAnimCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, time = 0)

    def __connectCurveRollDeformer(self):
        """makes all connections into the curve roll deformer"""
        #----connect shapes
        cmds.connectAttr(self.weightGeoShape + '.worldMesh',
                         self.returnDeformer + '.weightPatch',
                         force=True)
        
        if self.rollVector:
            cmds.connectAttr(self.rollVecShape + '.worldSpace',
                             self.returnDeformer + '.vectorCurve',
                             force=True)
        
        if self.weightBaseShapes:
            for i in range(len(self.weightBaseShapes)):
                if (cmds.objectType(self.weightBaseShapes[i], isType='nurbsSurface')) or (cmds.objectType(self.weightBaseShapes[i], isType='nurbsCurve')):
                    cmds.connectAttr(self.weightBaseShapes[i] + '.worldSpace', 
                                     self.returnDeformer + '.baseGeoArray['
                                     + str(i) + '].baseGeo', 
                                     force=True)
                if (cmds.objectType(self.weightBaseShapes[i], isType='mesh')):
                    cmds.connectAttr(self.weightBaseShapes[i] + '.worldMesh', 
                                     self.returnDeformer + '.baseGeoArray['
                                     + str(i) + '].baseGeo', 
                                     force=True)
        
        #----connect shapes
        cmds.connectAttr(self.inCurveShape + '.worldSpace',
                         self.returnDeformer + '.inCurve',
                         force=True)
        cmds.connectAttr(self.outCurveShape + '.worldSpace',
                         self.returnDeformer + '.outCurve',
                         force=True)
        #----r
        for i in range(len(self.rValAttrs)):
            cmds.connectAttr(self.rValAttrs[i], 
                             self.returnDeformer + '.rValueParentArray['
                             + str(i) + '].rValue', 
                             force=True)

        #----connect weights
        #----r
        for i in range(len(self.rWeights)):
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.rWeights[i] + '[' + str(j) + ']',
                                 self.returnDeformer+'.rWeightsParentArray['+
                                 str(i) +'].rWeightsParent[' + str(j) + ']',
                                 force=True)

        #----connect anim curves


        #----ru
        for i in range(len(self.rAnimCurvesU)):
            cmds.connectAttr(self.rAnimCurvesU[i] + '.output',
                             self.returnDeformer + '.rAnimCurveUArray[' + str(i) +
                             '].rAnimCurveU', 
                             force=True)
        #----rv
        for i in range(len(self.rAnimCurvesV)):
            cmds.connectAttr(self.rAnimCurvesV[i] + '.output',
                             self.returnDeformer + '.rAnimCurveVArray[' + str(i) +
                             '].rAnimCurveV', 
                             force=True)



    def __cleanup(self):
        "clean it up"
        if self.ihi == 0:
            cmds.setAttr(self.returnDeformer+".ihi",0)
            connections = cmds.listConnections(self.returnDeformer)
            if connections:
                for i in connections:
                    cmds.setAttr(i+".ihi",0)
        try:
            cmds.setAttr(self.baseGeo+'.v', 0)
        except:
            pass
        if self.weightBase:
            cmds.setAttr(self.returnDeformer+".useBaseGeo",1)

    def __create(self):
        """ This method creates the curveDeformer setup """
        self.__getTypeArg()
        self.__getShape()
        self.__checkArgs()
        self.__checkGeomArgs()
        self.__createCurveRollDeformer()
        self.__createRollVec()
        self.__createAttrs()
        self.__createWeights()
        self.__createAnimCurves()
        self.__setAnimCurveShapes()
        self.__connectCurveRollDeformer()
        self.__cleanup()
        
#---lips
# curveRollDeformerCmd(
#                  weightGeo = 'C_weightPatch_EX',
#                  geoms = ['C_body_HI'],
#                  inCurve = 'C_inCurve_EX',
#                  outCurve = 'C_outCurve_EX',
#                  control = '',
#                  orientToCurve = False,
#                  ihi = 1,
#                  side='C',
#                  name='bLipRoll',
#                  weightBase = ["C_bodyBase_HI"],
#                  rollVector = "C_inVEC_EX",
#                  lockAttrs = 0,
#                  rNames = ['C_rollCenter',
#                            'C_roll',
#                            'L_roll',
#                            'R_roll',
#                            'L_sneerRoll',
#                            'L_pinchRoll',
#                            'R_sneerRoll',
#                            'R_pinchRoll'],
#                  )


# def refresh_paintable_attrs(curveRoll_deformer):
#     "if paintable attrs do not exist, remove them"
#     cmds.makePaintable('LHCurveRollDeformer', ca = True, attrType = "doubleArray", shapeMode='deformer')
#     # get all double array attributes
#     attrs = cmds.listAttr(curveRoll_deformer, ud = True, a = True)
#     for i in attrs:
#         paint = i.split(".")[1]
#         cmds.makePaintable('LHCurveRollDeformer', paint, attrType='doubleArray', shapeMode='deformer')
# refresh_paintable_attrs("C_tLipRoll_CRD")