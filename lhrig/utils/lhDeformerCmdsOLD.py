import maya.cmds as cmds
#===============================================================================
#CLASS:         add_weights
#DESCRIPTION:   adds weights to specified LHDeformer
#USAGE:         set args and run
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          November 17th, 2014
#Version        1.0.0
#===============================================================================

class add_weights():
    def __init__(self,
                 deformer_type = "",
                 deformer = "",
                 names=[],
                 geoms = [],
                 uWeights = False,
                 vWeights = False,
                 nWeights = False,
                 tWeights = False,
                 rWeights = False,
                 rollWeights = False,
                 ):
        """
                                     
        @type  deformer_type:        string
        @param deformer_type:        supported types: "LHSlideDeformer",
                                     "LHVectorDeformer","LHCurveRollDeformer"
                                     
        @type  names:                string array
        @param names:                the names of the weights you will be adding
        
        @type  geoms:                string array
        @param geoms:                the names of the geometry that will be
                                     affected
        @type  geoms:                string array
        @param geoms:                the names of the geometry that will be
                                     affected
        """
        #----args
        self.deformer_type           = deformer_type
        self.deformer                = deformer
        self.names                   = names
        self.geoms                   = geoms
        self.uWeights                = uWeights
        self.vWeights                = vWeights
        self.nWeights                = nWeights
        self.tWeights                = tWeights
        self.rWeights                = rWeights
        self.rollWeights             = rollWeights

        #----vars
        self.valArray                = []
        self.valAttrs                = []

        self.animCurvesU             = []
        self.animCurvesV             = []
        self.weights                 = []
        self.geomShapes              = []
        self.pivotCurves             = []
        self.pivotCurveShapes        = []
        self.__create()
#     def __check(self):
#         """makes sure everything exists"""
    def __check(self):
        """make sure only one weight type option is set"""
        count = 0
        if self.uWeights>0:
            count += 1
        if self.vWeights>0:
            count += 1
        if self.nWeights>0:
            count += 1
        if self.tWeights>0:
            count += 1
        if self.rWeights>0:
            count += 1
        if self.rollWeights>0:
            count += 1
        if count != 1:
            raise Exception('''more than 1 weight type has been set, please only set 1 weight type to True''')
            quit()
    def __getShape(self):
        """gets shape"""
        try:
            try:
                for i in range(len(self.geoms)):
                    temp = cmds.listRelatives(self.geoms[i], shapes = True)[0]
                    self.geomShapes.append(temp)
            except:
                self.geomShapes = self.geoms
        except:
            raise Exception('''one or more argument either did not exist or did not have a shape''')
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

    def __createAttrs(self):
        """add u and v attrs to control"""
        
        #----uValAttr
        for i in self.names:
            cmds.addAttr(self.deformer, longName= i,
                                at='float', keyable=True)
            self.valAttrs.append(self.deformer + '.' + i)
    def __createWeights(self):
        """add u and v weights to deformer"""

        #----UWeights
        for i in self.names:
            cmds.addAttr(self.deformer, 
                         longName = i + 'Weights',
                         numberOfChildren = 1, 
                         attributeType = 'compound',
                         multi = True, 
                         indexMatters=True)
            cmds.addAttr(self.deformer, 
                         longName = i + "Weight",
                         dataType = 'doubleArray',
                         parent = i + 'Weights')
            cmds.makePaintable('LHSlideDeformer', i + "Weight", attrType='doubleArray', shapeMode='deformer')
            self.weights.append(self.deformer + "." + i +'Weights')


    def __createAnimCurves(self):
        """add anim curves"""
        #----uAnimCurves
        for i in range(len(self.names)):
            self.animCurvesU.append(cmds.createNode("animCurveTU",
                                                    name = self.names[i]+"_ACV"))
            self.animCurvesV.append(cmds.createNode("animCurveTU",
                                                    name = self.names[i]+"Falloff_ACV"))

    def __createPivots(self):
        """createNurbsCurves that are used for pivots """
        if self.deformer_type == "LHVectorDeformer":
            for i in range(len(self.names)):
                    tmp = cmds.curve(name= self.names[i] + 'Pivot_CRV',
                                          d=1, p=[(0,0,0),(0,0,1)],
                                          k=[0,1])
                    self.pivotCurveShapes.append(cmds.listRelatives(tmp, shapes = True)[0])
                    self.pivotCurves.append(tmp)
    

    def __setAnimCurveShapes(self):
        """set anim curve shapes default is a straight line with a value of 1"""

        #----U
        for i in range(len(self.animCurvesU)):
            cmds.setKeyframe(self.animCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, t = 0)
        for i in range(len(self.animCurvesV)):
            cmds.setKeyframe(self.animCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, t = 0)

    def __connect(self):
        """makes all connections into the slide deformer"""
        #----get attr names based on arguments
        if self.uWeights>0:
            prefix = "u"
        if self.vWeights>0:
            prefix = "v"
        if self.nWeights>0:
            prefix = "n"
        if self.tWeights>0:
            prefix = "t"
        if self.rWeights>0 or self.rollWeights>0:
            prefix = "r"
            
            
        #####################################
        ###########     pivots    ###########
        #####################################
        if self.deformer_type == "LHVectorDeformer":
            # find out what the next available value parent array is
            connects = cmds.listConnections(self.deformer + '.' + prefix+ 'PivotCurveArray', c = True)
            connects = [x.split("[")[1] for x in connects if "[" in x]
            connects = [x.split("]")[0] for x in connects if "]" in x]
            connects = [int(x) for x in connects]
            idx = max(connects)
            for i in range(len(self.valAttrs)):
                idx +=1
                cmds.connectAttr(self.pivotCurveShapes[i]+".worldSpace", 
                                 self.deformer + '.' + prefix+ 'PivotCurveArray['
                                 + str(idx) + '].'+ prefix+'PivotCurve', 
                                 force=True)


        #####################################
        ###########     value    ############
        #####################################
        # find out what the next available value parent array is
        connects = cmds.listConnections(self.deformer + '.' + prefix+ 'ValueParentArray', c = True)
        connects = [x.split("[")[1] for x in connects if "[" in x]
        connects = [x.split("]")[0] for x in connects if "]" in x]
        connects = [int(x) for x in connects]        
        idx = max(connects)
        for i in range(len(self.valAttrs)):
            idx +=1
            cmds.connectAttr(self.valAttrs[i], 
                             self.deformer + '.' + prefix+ 'ValueParentArray['
                             + str(idx) + '].'+ prefix+'Value', 
                             force=True)
            
        #####################################
        ###########     weights    ##########
        #####################################
        # find out what the next available value parent array is
        connects = cmds.listConnections(self.deformer + '.' + prefix+ 'WeightsParentArray', c = True)
        connects = [x.split("[")[1] for x in connects if "[" in x]
        connects = [x.split("]")[0] for x in connects if "]" in x]
        connects = [int(x) for x in connects]        
        idx = max(connects)
        #----u
        for i in range(len(self.weights)):
            idx +=1
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.weights[i] + '[' + str(j) + ']',
                                 self.deformer+'.'+ prefix+ 'WeightsParentArray['+
                                 str(idx) +'].' + prefix+'WeightsParent[' + str(j) + ']',
                                 force=True)
                
        #####################################
        ########     uAnimCurves    #########
        #####################################
        # find out what the next available value parent array is
        connects = cmds.listConnections(self.deformer + '.' + prefix+ 'AnimCurveUArray', c = True)
        connects = [x.split("[")[1] for x in connects if "[" in x]
        connects = [x.split("]")[0] for x in connects if "]" in x]
        connects = [int(x) for x in connects]        
        idx = max(connects)
        #----uu
        for i in range(len(self.animCurvesU)):
            idx +=1
            cmds.connectAttr(self.animCurvesU[i] + '.output', 
                             self.deformer + '.'+ prefix+'AnimCurveUArray[' + str(idx) + 
                             '].'+ prefix+'AnimCurveU', 
                             force=True)
            
        #####################################
        ########     vAnimCurves    #########
        #####################################
        # find out what the next available value parent array is
        connects = cmds.listConnections(self.deformer + '.' + prefix+ 'AnimCurveVArray', c = True)
        connects = [x.split("[")[1] for x in connects if "[" in x]
        connects = [x.split("]")[0] for x in connects if "]" in x]
        connects = [int(x) for x in connects]        
        idx = max(connects)
        #----uv
        for i in range(len(self.animCurvesV)):
            idx +=1
            cmds.connectAttr(self.animCurvesV[i] + '.output',
                             self.deformer + '.'+ prefix+'AnimCurveVArray[' + str(idx) +
                             '].'+ prefix+'AnimCurveV', 
                             force=True)
            
            
    def __create(self):
        """ This method creates the curveDeformer setup """
        self.__check()
        self.__getShape()
        self.__checkGeomArgs()
        self.__createAttrs()
        self.__createPivots()
        self.__createWeights()
        self.__createAnimCurves()
        self.__setAnimCurveShapes()
        self.__connect()

# add_weights(deformer_type = "LHCurveRollDeformer",
#             deformer = "C_testFace_CRD",
#             names = ["thisV","thatV"],
#             geoms = ["c_geo_HI"],
#             uWeights = False,
#             vWeights = False,
#             nWeights = False,
#             tWeights = False,
#             rWeights = False,
#             rollWeights = True)

def refresh_paintable_attrs(deformer_name, deformer_type ):
    "if paintable attrs do not exist, remove them"
    cmds.makePaintable(deformer_type, ca = True, attrType = "doubleArray", shapeMode='deformer')
    # get all double array attributes
    attrs = cmds.listAttr(deformer_name, ud = True, a = True)
    for i in attrs:
        paint = i.split(".")[1]
        cmds.makePaintable(deformer_type, paint, attrType='doubleArray', shapeMode='deformer')
#===============================================================================
#CLASS:         slideDeformerCmd
#DESCRIPTION:   Creates an LHSlideDeformer
#USAGE:         Select driverSurface and geometry[] or set args
#RETURN:        LHSlideDeformer
#AUTHOR:        Levi Harrison
#DATE:          August 1st, 2014
#Version        1.0.0
#===============================================================================

class slideDeformerCmd():
    def __init__(self,
                 driverSurface = '',
                 weightGeo = '',
                 geoms = [],
                 control = "",
                 ihi = 0,
                 side='C',
                 name='',
                 lockAttrs = 1,
                 uNames = [],
                 vNames = [],
                 nNames = [],
                 rNames = [],
                 ):
        """
        @type  driverSurface:        string (nurbsSurface)
        @param driverSurface:        the name of the geo that will drive the
                                     geometry, or the first selection
                                     
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

        @type  uNames:               string array
        @param uNames:               the names of the u channels you want
                                     the size of this array will determine how
                                     many value attributes, weight channels, and
                                     animation curve values are created
                                     example ['L_mouth', 'R_mouth']
        
        @type  vNames:               string array
        @param vNames:               the names of the v channels you want
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
                                     
        @type  vUseAnimCurves:       unsigned int array
        @param vUseAnimCurves:       determine whether you would like animation
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
        self.driverSurface           = driverSurface
        self.geoms                   = geoms
        self.weightGeo               = weightGeo
        self.control                 = control

        self.lockAttrs               = lockAttrs
        self.ihi                     = ihi
        self.side                    = side
        self.name                    = name
        self.uNames                  = uNames
        self.vNames                  = vNames
        self.rNames                  = rNames
        self.nNames                  = nNames
        #----vars
        self.driverShape             = ''
        self.weightGeoShape          = ''
        self.geomShapes              = []
        self.returnDeformer          = ''
        self.returnWeightDeformer    = ''
        self.deformerName            = ''
        self.baseGeo                 = ''
        self.baseShape               = ''
        self.baseName                = ''
        self.driverType              = ''
        self.uValAttrs               = []
        self.vValAttrs               = []
        self.nValAttrs               = []
        self.rValAttrs               = []
        self.uWeights                = []
        self.vWeights                = []
        self.nWeights                = []
        self.rWeights                = []
        self.uAnimCurvesU            = []
        self.uAnimCurvesV            = []
        self.vAnimCurvesU            = []
        self.vAnimCurvesV            = []
        self.nAnimCurvesU            = []
        self.nAnimCurvesV            = []
        self.rAnimCurvesU            = []
        self.rAnimCurvesV            = []
        self.rPivotCurves            = []
        self.rPivotCurveShapes       = []
        #----created attrs
        #----deformer attr default values
        #----procedures
        self.__create()

    def __getTypeArg(self):
        """get argument type (user defined or selected)"""
        if (self.driverSurface and self.weightGeo and self.geoms):
            return
        else:
            self.__getSelectedArgs()

    def __getSelectedArgs(self):
        """gets selected args if you are selecting, you must use the weight
           geo, if you do not want weight geo you must specify in the args"""
        try:
            sel = cmds.ls(sl=True)
            self.driverSurface = sel[0]
            self.weightGeo = sel[1]
            self.geoms = sel[2:]
        except:
            raise Exception('''please give arguments (driverCurve, geoms) or select 1 driver geo and at least 1 piece of geometry \n' ''')
            quit()
    def __getShape(self):
        """gets shape"""
        try:
            self.driverShape = cmds.listRelatives(self.driverSurface, shapes = True)[0]
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
        if (cmds.objectType(self.driverShape, isType='nurbsSurface') == True
            and cmds.objectType(self.weightGeoShape, isType='mesh') == True):
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
        self.returnWeightDeformer = cmds.deformer(self.geoms, 
                                            type = 'LHWeightDeformer',
                                            name= self.side + "_" +
                                                  self.name + "_WTD",
                                            foc = True)[0]
        self.returnDeformer = cmds.deformer(self.geoms, 
                                            type = 'LHSlideDeformer',
                                            name= self.side + "_" +
                                                  self.name + "_SLD")[0]
    def __createBase(self):
        """creates base geo"""
        self.baseName = self.__nameBase()
        self.baseGeo,self.baseShape = self.__duplicateMeshClean(self.driverSurface, self.baseName)

    def __nameBase(self):
        """returns name of base"""
        try:
            name = self.driverSurface.split("_")
            return name[0] + '_' + name[1] + 'Base_' + name[2]
        except:
            return name[0] + 'Base'

    def __createAttrs(self):
        """add u and v attrs to control"""
        
        if not self.control:
            self.control = self.returnDeformer
        #----uValAttr
        for i in self.uNames:
            cmds.addAttr(self.control, longName= i,
                                at='float', keyable=True)
            self.uValAttrs.append(self.control + '.' + i)
        #----vValAttr
        for i in self.vNames:
            cmds.addAttr(self.control, longName= i,
                                at='float', keyable=True)
            self.vValAttrs.append(self.control + '.' + i)
        #----nValAttr
        for i in self.nNames:
            cmds.addAttr(self.control, longName= i,
                                at='float', keyable=True)
            self.nValAttrs.append(self.control + '.' + i)
    def __createWeights(self):
        """add u and v weights to deformer"""

        #----UWeights
        for i in self.uNames:
            cmds.addAttr(self.returnWeightDeformer, 
                         longName = i + 'UWeights',
                         numberOfChildren = 1, 
                         attributeType = 'compound',
                         multi = True, 
                         indexMatters=True)
            cmds.addAttr(self.returnWeightDeformer, 
                         longName = i + "UWeight",
                         dataType = 'doubleArray',
                         parent = i + 'UWeights')
            cmds.makePaintable('LHWeightDeformer', i + "UWeight", attrType='doubleArray', shapeMode='deformer')
            self.uWeights.append(self.returnWeightDeformer + "." + i +'UWeights')

        #----VWeights
        for i in self.vNames:
            cmds.addAttr(self.returnWeightDeformer,
                         longName = i + 'VWeights',
                         numberOfChildren = 1, 
                         attributeType = 'compound',
                         multi = True, 
                         indexMatters=True)
            cmds.addAttr(self.returnWeightDeformer, 
                         longName = i + "VWeight",
                         dataType = 'doubleArray',
                         parent = i + 'VWeights')
            cmds.makePaintable('LHWeightDeformer', i + "VWeight", attrType='doubleArray', shapeMode='deformer')
            self.vWeights.append(self.returnWeightDeformer + "." + i +'VWeights')

        #----nWeights
        for i in self.nNames:
            cmds.addAttr(self.returnWeightDeformer, 
                         longName = i + 'NWeights',
                         numberOfChildren = 1, 
                         attributeType = 'compound',
                         multi = True, 
                         indexMatters=True)
            cmds.addAttr(self.returnWeightDeformer,
                         longName = i + "NWeight",
                         dataType = 'doubleArray',
                         parent = i + 'NWeights')
            cmds.makePaintable('LHWeightDeformer', i + "NWeight", attrType='doubleArray', shapeMode='deformer')
            self.nWeights.append(self.returnWeightDeformer + "." + i +'NWeights')


    def __createAnimCurves(self):
        """add anim curves"""
        #----uAnimCurves
        for i in range(len(self.uNames)):
            self.uAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                    name = self.uNames[i]+"_ACV"))
            self.uAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                            name = self.uNames[i]+"Falloff_ACV"))
        #----vAnimCurves
        for i in range(len(self.vNames)):
            self.vAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                    name = self.vNames[i]
                                                    + "_ACV"))
            self.vAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                    name = self.vNames[i]
                                                    + "Falloff_ACV"))
        #----nAnimCurves
        for i in range(len(self.nNames)):
            self.nAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                    name = self.nNames[i]
                                                    + "_ACV"))
            self.nAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                    name = self.nNames[i]
                                                    + "Falloff_ACV"))

    def __setAnimCurveShapes(self):
        """set anim curve shapes default is a straight line with a value of 1"""

        #----U
        for i in range(len(self.uAnimCurvesU)):
            cmds.setKeyframe(self.uAnimCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, time = 0)
        for i in range(len(self.uAnimCurvesV)):
            cmds.setKeyframe(self.uAnimCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, time = 0)

        #----V
        for i in range(len(self.vAnimCurvesU)):
            cmds.setKeyframe(self.vAnimCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, time = 0)
        for i in range(len(self.vAnimCurvesV)):
            cmds.setKeyframe(self.vAnimCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, time = 0)

        #----N
        for i in range(len(self.nAnimCurvesU)):
            cmds.setKeyframe(self.nAnimCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, time = 0)
        for i in range(len(self.nAnimCurvesV)):
            cmds.setKeyframe(self.nAnimCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, time = 0)


    def __connectSlideDeformer(self):
        """makes all connections into the slide deformer"""
        #----connect shapes
        cmds.connectAttr(self.driverShape + '.worldSpace',
                         self.returnDeformer + '.surface',
                         force=True)
        cmds.connectAttr(self.baseShape + '.worldSpace',
                         self.returnDeformer + '.surfaceBase',
                         force=True)
        cmds.connectAttr(self.weightGeoShape + '.worldMesh',
                         self.returnWeightDeformer + '.weightPatch',
                         force=True)
        #---connects weight deformers
        #----connect anim curves
        uAnimCurvesIdx = -1
        # U Anim Curves
        #----uu
        for i in range(len(self.uAnimCurvesU)):
            uAnimCurvesIdx = uAnimCurvesIdx + 1
            cmds.connectAttr(self.uAnimCurvesU[i] + '.output', 
                             self.returnWeightDeformer + '.uAnimCurveArray[' + str(uAnimCurvesIdx) + 
                             '].uAnimCurve',
                             force=True)
        #----vu
        for i in range(len(self.vAnimCurvesU)):
            uAnimCurvesIdx = uAnimCurvesIdx + 1
            cmds.connectAttr(self.vAnimCurvesU[i] + '.output',
                             self.returnWeightDeformer + '.uAnimCurveArray[' + str(uAnimCurvesIdx) +
                             '].uAnimCurve',
                             force=True)
        # V Anim Curves
        #----nu
        for i in range(len(self.nAnimCurvesU)):
            uAnimCurvesIdx = uAnimCurvesIdx + 1
            cmds.connectAttr(self.nAnimCurvesU[i] + '.output',
                             self.returnWeightDeformer + '.uAnimCurveArray[' + str(uAnimCurvesIdx) +
                             '].uAnimCurve',
                             force=True)


        vAnimCurvesIdx = -1
        #----uv
        for i in range(len(self.uAnimCurvesV)):
            vAnimCurvesIdx = vAnimCurvesIdx + 1
            cmds.connectAttr(self.uAnimCurvesV[i] + '.output',
                             self.returnWeightDeformer + '.vAnimCurveArray[' + str(vAnimCurvesIdx) +
                             '].vAnimCurve',
                             force=True)
        
        #----vv
        for i in range(len(self.vAnimCurvesV)):
            vAnimCurvesIdx = vAnimCurvesIdx + 1
            cmds.connectAttr(self.vAnimCurvesV[i] + '.output',
                             self.returnWeightDeformer + '.vAnimCurveArray[' + str(vAnimCurvesIdx) +
                             '].vAnimCurve',
                             force=True)
        #----nv
        for i in range(len(self.nAnimCurvesV)):
            vAnimCurvesIdx = vAnimCurvesIdx + 1
            cmds.connectAttr(self.nAnimCurvesV[i] + '.output',
                             self.returnWeightDeformer + '.vAnimCurveArray[' + str(vAnimCurvesIdx) +
                             '].vAnimCurve',
                             force=True)
        
        #---connects weight deformer weights
        weightIdx = -1
        #----u
        for i in range(len(self.uWeights)):
            weightIdx = weightIdx + 1
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.uWeights[i] + '[' + str(j) + ']',
                                 self.returnWeightDeformer+'.weightsParentArray['+
                                 str(weightIdx) +'].weightsParent[' + str(j) + ']',
                                 force=True)
        #----v
        for i in range(len(self.vWeights)):
            weightIdx = weightIdx + 1
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.vWeights[i] + '[' + str(j) + ']',
                                 self.returnWeightDeformer+'.weightsParentArray['+
                                 str(weightIdx) +'].weightsParent[' + str(j) + ']',
                                 force=True)
        #----n
        for i in range(len(self.nWeights)):
            weightIdx = weightIdx + 1
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.nWeights[i] + '[' + str(j) + ']',
                                 self.returnWeightDeformer+'.weightsParentArray['+
                                 str(weightIdx) +'].weightsParent[' + str(j) + ']',
                                 force=True)
        
        
        
        #----connect values

        #----u
        for i in range(len(self.uValAttrs)):
            cmds.connectAttr(self.uValAttrs[i], 
                             self.returnDeformer + '.uValueParentArray['
                             + str(i) + '].uValue', 
                             force=True)
        #----v
        for i in range(len(self.vValAttrs)):
            cmds.connectAttr(self.vValAttrs[i], 
                             self.returnDeformer + '.vValueParentArray['
                             + str(i) + '].vValue', 
                             force=True)
        #----n
        for i in range(len(self.nValAttrs)):
            cmds.connectAttr(self.nValAttrs[i], 
                             self.returnDeformer + '.nValueParentArray['
                             + str(i) + '].nValue', 
                             force=True)

        #----connect weights
        #----u
        weightIdx = -1
        for i in range(len(self.uWeights)):
            weightIdx = weightIdx + 1
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.returnWeightDeformer+'.outWeightsParentArray['+
                                 str(weightIdx) +'].outWeightsParent[' + str(j) + ']',
                                 self.returnDeformer+'.uWeightsParentArray['+
                                 str(i) +'].uWeightsParent[' + str(j) + ']',
                                 force=True)
        #----v
        for i in range(len(self.vWeights)):
            weightIdx = weightIdx + 1
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.returnWeightDeformer+'.outWeightsParentArray['+
                                 str(weightIdx) +'].outWeightsParent[' + str(j) + ']',
                                 self.returnDeformer+'.vWeightsParentArray['+
                                 str(i) +'].vWeightsParent[' + str(j) + ']',
                                 force=True)
        #----n
        for i in range(len(self.nWeights)):
            weightIdx = weightIdx + 1
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.returnWeightDeformer+'.outWeightsParentArray['+
                                 str(weightIdx) +'].outWeightsParent[' + str(j) + ']',
                                 self.returnDeformer+'.nWeightsParentArray['+
                                 str(i) +'].nWeightsParent[' + str(j) + ']',
                                 force=True)

    def __duplicateMeshClean(self, mesh, name):
        "duplicates a nurbs curve cleanly"
        parent = ""
        try:
            parent = cmds.listRelatives(mesh, p = 1)[0]
        except:
            pass
        meshShape = cmds.ls(mesh, dag = 1, g = 1)[0]
        newTransform = cmds.createNode("transform", n = name)
        newMesh = cmds.createNode("nurbsSurface", n = name+"Shape", p = newTransform)
        cmds.connectAttr(meshShape + ".worldSpace", newMesh + ".create")
        cmds.refresh()
        cmds.disconnectAttr(meshShape + ".worldSpace", newMesh + ".create")
        if parent:
            cmds.parent(newTransform, parent)
        return newTransform,newMesh

    def __cleanup(self):
        "clean it up"
#         cmds.setAttr(self.returnDeformer + ".envelope", 1)
#         cmds.setAttr(self.returnWeightDeformer + ".envelope", 1)
        
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
        self.__createBase()
        self.__createAttrs()
        self.__createWeights()
        self.__createAnimCurves()
        self.__setAnimCurveShapes()
        self.__connectSlideDeformer()
        self.__cleanup()
# slideDeformerCmd(driverSurface = "L_slide_EX",
#                  weightGeo = "L_weight_EX",
#                  geoms = ["L_geo_HI","L_geo1_HI"],
#                  ihi = 1,
#                  name = "testSlide",
#                  uNames = ["uSlide1","uSlide2","uSlide3"],
#                  vNames = ["vSlide1","vSlide2","vSlide3"],
#                  nNames = ["nSlide1","nSlide2","nSlide3"])
