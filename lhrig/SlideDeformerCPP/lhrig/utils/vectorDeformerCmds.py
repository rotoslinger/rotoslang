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
                 control = "",
                 ihi = 0,
                 side='C',
                 name='',
                 lockAttrs = 1,
                 tNames = [],
                 rNames = [],
                 tUseAnimCurves = [1],
                 rUseAnimCurves = [1],
                 ):
        """
                                     
        @type  weightGeo:            string (mesh)
        @param weightGeo:            the name of the geo that will be used to
                                     raycast weighting

        @type  geoms:                string array
        @param geoms:                the names of the geometry the will be deformed,
                                     or the second selection and beyond 
                                     can be mesh, nurbsSurface, or nurbsCurve

        @type  control:              string
        @param control:              where to put attributes, usually a control
                                     if unset attributes will be created on 
                                     the returned deformer

        @type  ihi:                  int
        @param ihi:                  sets the deformer isHistoricallyIntersting to 0

        @type  lockAttrs:            int
        @param lockAttrs:            if set to 1 all attributes in return 
                                     deformer are locked and hidden

        @type  side:                 string
        @param side:                 defaults to C but L and R are also acceptable

        
        @type  tNames:               string array
        @param tNames:               the names of the v channels you want
                                     the size of this array will determine how
                                     many value attributes, weight channels, and
                                     animation curve values are created
                                     example ['L_mouth', 'R_mouth']
                                     
        @type  uUseAnimCurves:       unsigned int array
        @param uUseAnimCurves:       determine whether you would like animation
                                     curves to be created for weighting in each 
                                     u channel if a single int [1] is given, all 
                                     anim curves are created for all u names
                                     if a single int [0] is given no anim curves
                                     will be created
                                     if some channels need anim curves and some
                                     don't [0,1,1,0], ints for every u name can
                                     be given to determine if it does or doesn't
                                     need anim curves
                                     
        @type  tUseAnimCurves:       unsigned int array
        @param tUseAnimCurves:       determine whether you would like animation
                                     curves to be created for weighting in each 
                                     v channel if a single int [1] is given, all 
                                     anim curves are created for all v names
                                     if a single int [0] is given no anim curves
                                     will be created
                                     if some channels need anim curves and some
                                     don't [0,1,1,0], ints for every v name can
                                     be given to determine if it does or doesn't
                                     need anim curves
        """
        #----args
        self.geoms                   = geoms
        self.weightGeo               = weightGeo
        self.control                 = control

        self.lockAttrs               = lockAttrs
        self.ihi                     = ihi
        self.side                    = side
        self.name                    = name
        self.tNames                  = tNames
        self.rNames                  = rNames
        self.tUseAnimCurves          = tUseAnimCurves
        self.rUseAnimCurves          = rUseAnimCurves
        #----vars
        self.weightGeoShape          = ''
        self.geomShapes              = []
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
                                                  self.name + "_V")[0]

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


        #----TWeights
        for i in self.tNames:
            cmds.addAttr(self.returnDeformer,
                         longName = i + 'TWeights',
                         numberOfChildren = 1, 
                         attributeType = 'compound',
                         multi = True, 
                         indexMatters=True)
            cmds.addAttr(self.returnDeformer, 
                         longName = i + "TWeight",
                         dataType = 'doubleArray',
                         parent = i + 'TWeights')
            cmds.makePaintable('LHVectorDeformer', i + "TWeight", attrType='doubleArray', shapeMode='deformer')
            self.tWeights.append(self.returnDeformer + "." + i +'TWeights')


        #----rWeights
        for i in self.rNames:
            cmds.addAttr(self.returnDeformer,
                         longName = i + 'RWeights',
                         numberOfChildren = 1, 
                         attributeType = 'compound',
                         multi = True, 
                         indexMatters=True)
            cmds.addAttr(self.returnDeformer,
                         longName = i + "RWeight",
                         dataType = 'doubleArray',
                         parent = i + 'RWeights')
            cmds.makePaintable('LHVectorDeformer', i + "RWeight", attrType='doubleArray', shapeMode='deformer')
            self.rWeights.append(self.returnDeformer + "." + i +'RWeights')

    def __createAnimCurves(self):
        """add anim curves"""

        #----tAnimCurves
        if len(self.tUseAnimCurves) <= 0:
            return
        if len(self.tUseAnimCurves) == 1:
            if self.tUseAnimCurves[0] == 0:
                return
            elif self.tUseAnimCurves[0] == 1:
                for i in range(len(self.tNames)):
                    self.tAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                            name = self.tNames[i]
                                                            + "_ACV"))
                    self.tAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                            name = self.tNames[i]
                                                            + "_ACV"))
        elif len(self.tUseAnimCurves) > 1:
            for i in range(len(self.tNames)):
                if len(self.tUseAnimCurves) >= i:
                    if self.tUseAnimCurves[i] <= 0:
                        self.tAnimCurvesU.append('')
                        self.tAnimCurvesV.append('')
                    if self.tUseAnimCurves[i] >= 1:
                        self.tAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                                name = self.tNames[i]
                                                                + "_ACV"))
                        self.tAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                                name = self.tNames[i]
                                                                + "_ACV"))

        #----rAnimCurves
        if len(self.rUseAnimCurves) <= 0:
            return
        if len(self.rUseAnimCurves) == 1:
            if self.rUseAnimCurves[0] == 0:
                return
            elif self.rUseAnimCurves[0] == 1:
                for i in range(len(self.rNames)):
                    self.rAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                            name = self.rNames[i]
                                                            + "_ACV"))
                    self.rAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                            name = self.rNames[i]
                                                            + "_ACV"))
        elif len(self.rUseAnimCurves) > 1:
            for i in range(len(self.rNames)):
                if len(self.rUseAnimCurves) >= i:
                    if self.rUseAnimCurves[i] <= 0:
                        self.rAnimCurvesU.append('')
                        self.rAnimCurvesV.append('')
                    if self.rUseAnimCurves[i] >= 1:
                        self.rAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                                name = self.rNames[i]
                                                                + "_ACV"))
                        self.rAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                                name = self.rNames[i]
                                                                + "_ACV"))

    def __setDefaultWeights(self):
        """set all weights to 1"""
#         for i in self.geoms:
#             for j in self.uWeights:
#                 cmds.setAttr(self.returnDeformer + '.' + self.uWeights[j], type = 'doubleArray', [1])
#                 cmds.percent(i, self.returnDeformer + '.' + self.uWeights[j], 
#                              v=1)
#         cmds.percent -v 0 C_testFace_SLD c_geo_HI.vtx[0:2] ;


    def __setAnimCurveShapes(self):
        """set anim curve shapes default is a straight line with a value of 1"""

        #----V
        for i in range(len(self.tAnimCurvesU)):
            cmds.setKeyframe(self.tAnimCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0)
        for i in range(len(self.tAnimCurvesV)):
            cmds.setKeyframe(self.tAnimCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0)

        #----R
        for i in range(len(self.rAnimCurvesU)):
            cmds.setKeyframe(self.rAnimCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0)
        for i in range(len(self.rAnimCurvesV)):
            cmds.setKeyframe(self.rAnimCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0)

    def __createRotationPivots(self):
        """createNurbsCurves that are used for pivots """
        for i in range(len(self.tNames)):
                tmp = cmds.curve(name= self.tNames[i] + 'Pivot_CRV',
                                      d=1, p=[(0,0,0),(0,0,1)],
                                      k=[0,1])
                self.tPivotCurveShapes.append(cmds.listRelatives(tmp, shapes = True)[0])
                self.tPivotCurves.append(tmp)

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

    def __create(self):
        """ This method creates the curveDeformer setup """
        self.__getTypeArg()
        self.__getShape()
        self.__checkArgs()
        self.__checkGeomArgs()
        self.__createSlideDeformer()
        self.__createAttrs()
        self.__createWeights()
        self.__createAnimCurves()
        self.__createRotationPivots()
        self.__setAnimCurveShapes()
        self.__connectSlideDeformer()
        
        self.__cleanup()
        
#---lips
vectorDeformerCmd(
                 weightGeo = 'C_weightPatch_EX',
                 geoms = ['c_geo_HI'],
                 control = '',
                 ihi = 1,
                 side='C',
                 name='testFace',
                 lockAttrs = 0,
                 tNames = ['vtTest1','tTest2','tTest3','tTest4'],
                 rNames = ['rTest1','rTest2','rTest3','rTest4'],
                 )
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