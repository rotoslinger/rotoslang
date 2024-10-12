import maya.cmds as cmds
#===============================================================================
#CLASS:         slideDeformerCmd
#DESCRIPTION:   Creates an LHSlideDeformer
#USAGE:         Select driverSurface and geometry[] or set args
#RETURN:        LHSlideDeformer
#AUTHOR:        Levi Harrison
#DATE:          August 1st, 2014
#Version        1.0.0
#===============================================================================

class vectorDeformerCmd():
    def __init__(self,
                 weightGeo = '',
                 geoms = [],
                 weightBase = [],
                 control = "",
                 ihi = 0,
                 side='C',
                 name='',
                 lockAttrs = 1,
                 tNames = [],
                 rNames = [],
                 tPivots = [],
                 rPivots = [],
                 animCurveSuffix="ACV",
                 deformerSuffix="VCD"
                 ):
        """
                                     
        type  weightGeo:            string (mesh)
        param weightGeo:            the name of the geo that will be used to
                                     raycast weighting

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

        
        type  tNames:               string array
        param tNames:               the names of the t channels you want
                                     the size of this array will determine how
                                     many value attributes, weight channels, and
                                     animation curve values are created
                                     example ['L_mouth', 'R_mouth']
                                     
        type  rNames:               string array
        param rNames:               the names of the r channels you want
                                     the size of this array will determine how
                                     many value attributes, weight channels, and
                                     animation curve values are created
                                     example ['L_mouth', 'R_mouth']
                                     
        type  tPivots:              string array
        param tPivots:              OPTIONAL if you have already created 
                                     translation pivots you can specify them 
                                     here.  If you leave this blank new curves
                                     will be created for you.
                                     
        type  rPivots:              string array
        param rPivots:              OPTIONAL if you have already created 
                                     rotaional pivots you can specify them 
                                     here.  If you leave this blank new curves
                                     will be created for you.

        type  weightBase:           string array
        param weightBase:           Optional.  A copy of the geometry that will
                                     be deformed.  This allows weights to be 
                                     projected to a non moving geometry.  Very 
                                     important when you have multiple weight
                                     projecting deformers on the same mesh.
        """
        #----args
        self.geoms                   = geoms
        self.weightGeo               = weightGeo
        self.control                 = control
        self.tPivots                 = tPivots
        self.rPivots                 = rPivots
        self.weightBase              = weightBase
        self.animCurveSuffix         = animCurveSuffix
        self.deformerSuffix          = deformerSuffix

        self.lockAttrs               = lockAttrs
        self.ihi                     = ihi
        self.side                    = side
        self.name                    = name
        self.tNames                  = tNames
        self.rNames                  = rNames
        #----vars
        self.weightGeoShape          = ''
        self.geomShapes              = []
        self.weightBaseShapes        = []
        self.returnDeformer          = ''
        self.deformerName            = ''
        self.tValAttrs               = []
        self.rValAttrs               = []
        self.tWeights                = []
        self.rWeights                = []
        self.tAnimCurvesU            = []
        self.tAnimCurvesV            = []
        self.rAnimCurvesU            = []
        self.rAnimCurvesV            = []
        self.tPivotCurves            = []
        self.tPivotCurveShapes       = []
        self.rPivotCurves            = []
        self.rPivotCurveShapes       = []
        #----created attrs
        #----deformer attr default values
        #----procedures
        self.__create()

    def __getPivotShapes(self):
        """gets pivot shapes"""
        try:
            if self.tPivots:
                for i in self.tPivots:
                    self.tPivotCurves.append(i)
                    self.tPivotCurveShapes.append(cmds.listRelatives(i, 
                                                                     shapes = True)[0])
            if self.rPivots:
                for i in self.rPivots:
                    self.rPivotCurves.append(i)
                    self.rPivotCurveShapes.append(cmds.listRelatives(i, 
                                                                     shapes = True)[0])
        except:
            raise Exception("one or curves either did not exist or did not"
            + "have a shape")
            quit()

    def __getTypeArg(self):
        """get argument type (user defined or selected)"""
        if (self.weightGeo and self.geoms):
            return
        else:
            self.__getSelectedArgs()

    def __getSelectedArgs(self):
        """gets selected args if you are selecting, you must use the weight
           geo, if you do not want weight geo you must specify in the args"""
        try:
            sel = cmds.ls(sl=True)
            self.weightGeo = sel[0]
            self.geoms = sel[1:]
        except:
            raise Exception('''please give arguments (driverCurve, geoms) or select 1 driver geo and at least 1 piece of geometry \n' ''')
            quit()
    def __getShape(self):
        """gets shape"""
        try:
            self.weightGeoShape = cmds.listRelatives(self.weightGeo, shapes = True)[0]
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




    def __checkArgs(self):
        """checks the args to make sure they are the right type"""
        if (cmds.objectType(self.weightGeoShape, isType='mesh') == True):
            return
        else:
            raise Exception('''arguments are not of required type 'nurbsSurface, mesh, geometry \n' ''')
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
                
    def __createSlideDeformer(self):
        """creates the wrap deformer"""
        self.returnDeformer = cmds.deformer(self.geoms, 
                                            type = 'LHVectorDeformer',
                                            name= self.side + "_" +
                                                  self.name + "_" + self.deformerSuffix)[0]

    def __createAttrs(self):
        """add u and v attrs to control"""
        
        if not self.control:
            self.control = self.returnDeformer
        #----uValAttr
        for i in self.tNames:
            cmds.addAttr(self.control, longName= i,
                                at='float', keyable=True)
            self.tValAttrs.append(self.control + '.' + i)
        #----rValAttr
        for i in self.rNames:
            cmds.addAttr(self.control, longName= i,
                                at='float', keyable=True)
            self.rValAttrs.append(self.control + '.' + i)
    def __createWeights(self):
        """add u and v weights to deformer"""


        #----Weights
        for i in self.tNames:
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
            cmds.makePaintable('LHVectorDeformer', i + "Weight", attrType='doubleArray', shapeMode='deformer')
            self.tWeights.append(self.returnDeformer + "." + i +'Weights')


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
            cmds.makePaintable('LHVectorDeformer', i + "Weight", attrType='doubleArray', shapeMode='deformer')
            self.rWeights.append(self.returnDeformer + "." + i +'Weights')

    def __createAnimCurves(self):
        """add anim curves"""

        #----tAnimCurves
        for i in range(len(self.tNames)):
            self.tAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                    name = self.tNames[i]
                                                    + "_" + self.animCurveSuffix))
            self.tAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                    name = self.tNames[i]
                                                    + "Falloff_" + self.animCurveSuffix))

        #----rAnimCurves
        for i in range(len(self.rNames)):
            self.rAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                    name = self.rNames[i]
                                                    + self.animCurveSuffix))
            self.rAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                    name = self.rNames[i]
                                                    + "Falloff_" + self.animCurveSuffix))

    def __setAnimCurveShapes(self):
        """set anim curve shapes default is a straight line with a value of 1"""

        #----V
        for i in range(len(self.tAnimCurvesU)):
            cmds.setKeyframe(self.tAnimCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, t = 0)
        for i in range(len(self.tAnimCurvesV)):
            cmds.setKeyframe(self.tAnimCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, t = 0)

        #----R
        for i in range(len(self.rAnimCurvesU)):
            cmds.setKeyframe(self.rAnimCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, t = 0)
        for i in range(len(self.rAnimCurvesV)):
            cmds.setKeyframe(self.rAnimCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, t = 0)

    def __createPivots(self):
        """createNurbsCurves that are used for pivots """

        if not (self.tPivots):
            for i in range(len(self.tNames)):
                    tmp = cmds.curve(name= self.tNames[i] + 'Pivot_CRV',
                                          d=1, p=[(0,0,0),(0,0,1)],
                                          k=[0,1])
                    self.tPivotCurveShapes.append(cmds.listRelatives(tmp, shapes = True)[0])
                    self.tPivotCurves.append(tmp)

        if not (self.rPivots):
            for i in range(len(self.rNames)):
                    tmp = cmds.curve(name= self.rNames[i] + 'Pivot_CRV',
                                          d=1, p=[(0,0,0),(0,0,1)],
                                          k=[0,1])
                    self.rPivotCurveShapes.append(cmds.listRelatives(tmp, shapes = True)[0])
                    self.rPivotCurves.append(tmp)

    def __connectSlideDeformer(self):
        """makes all connections into the slide deformer"""
        #----connect shapes
        cmds.connectAttr(self.weightGeoShape + '.worldMesh',
                         self.returnDeformer + '.weightPatch',
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
        #----connect values

        #----v
        for i in range(len(self.tValAttrs)):
            cmds.connectAttr(self.tValAttrs[i], 
                             self.returnDeformer + '.tValueParentArray['
                             + str(i) + '].tValue', 
                             force=True)
        #----r
        for i in range(len(self.rValAttrs)):
            cmds.connectAttr(self.rValAttrs[i], 
                             self.returnDeformer + '.rValueParentArray['
                             + str(i) + '].rValue', 
                             force=True)

        #----connect weights
        #----v
        for i in range(len(self.tWeights)):
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.tWeights[i] + '[' + str(j) + ']',
                                 self.returnDeformer+'.tWeightsParentArray['+
                                 str(i) +'].tWeightsParent[' + str(j) + ']',
                                 force=True)
        #----r
        for i in range(len(self.rWeights)):
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.rWeights[i] + '[' + str(j) + ']',
                                 self.returnDeformer+'.rWeightsParentArray['+
                                 str(i) +'].rWeightsParent[' + str(j) + ']',
                                 force=True)

        #----connect anim curves

        # U Anim Curves

        #----vu
        for i in range(len(self.tAnimCurvesU)):
            cmds.connectAttr(self.tAnimCurvesU[i] + '.output',
                             self.returnDeformer + '.tAnimCurveUArray[' + str(i) +
                             '].tAnimCurveU', 
                             force=True)
        #----vv
        for i in range(len(self.tAnimCurvesV)):
            cmds.connectAttr(self.tAnimCurvesV[i] + '.output',
                             self.returnDeformer + '.tAnimCurveVArray[' + str(i) +
                             '].tAnimCurveV', 
                             force=True)

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

        #----connect nurbs curves

        #----nPivot
        for i in range(len(self.tPivotCurveShapes)):
            cmds.connectAttr(self.tPivotCurveShapes[i] + '.worldSpace',
                             self.returnDeformer + '.tPivotCurveArray['
                             + str(i) + '].tPivotCurve',
                             force=True)
        
        
        #----rPivot
        for i in range(len(self.rPivotCurveShapes)):
            cmds.connectAttr(self.rPivotCurveShapes[i] + '.worldSpace',
                             self.returnDeformer + '.rPivotCurveArray['
                             + str(i) + '].rPivotCurve',
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
        self.__getPivotShapes()
        self.__getTypeArg()
        self.__getShape()
        self.__checkArgs()
        self.__checkGeomArgs()
        self.__createSlideDeformer()
        self.__createAttrs()
        self.__createWeights()
        self.__createAnimCurves()
        self.__createPivots()
        self.__setAnimCurveShapes()
        self.__connectSlideDeformer()
        self.__cleanup()
# vectorDeformerCmd(
#                 weightGeo = 'L_weight_EX',
#                 geoms = ['L_geo1_HI','L_geo_HI'],
#                 control = '',
#                 ihi = 1,
#                 side='C',
#                 name='testFace',
#                 lockAttrs = 0,
#                  tNames = ['tTest1','tTest2','tTest3'],
#                  rNames = ['rTest1','rTest2','rTest3'],
#                  )
#---lips
# def refresh_paintable_attrs(vector_deformer):
#     "if paintable attrs do not exist, remove them"
#     cmds.makePaintable('LHVectorDeformer', ca = True, attrType = "doubleArray", shapeMode='deformer')
#     # get all double array attributes
#     attrs = cmds.listAttr(vector_deformer, ud = True, a = True)
#     for i in attrs:
#         paint = i.split(".")[1]
#         cmds.makePaintable('LHVectorDeformer', paint, attrType='doubleArray', shapeMode='deformer')
# #     cmds.makePaintable('LHVectorDeformer', "weights", attrType='multiFloat', shapeMode='deformer')
# refresh_paintable_attrs("C_testFace_V")