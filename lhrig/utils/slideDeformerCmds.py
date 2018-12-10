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

class slideDeformerCmd():
    def __init__(self,
                 driverSurface = '',
                 weightGeo = '',
                 weightBase = [],
                 geoms = [],
                 control = "",
                 ihi = 0,
                 side='C',
                 name='',
                 lockAttrs = 1,
                 uNames = [],
                 vNames = [],
                 nNames = [],
                 ):
        """
        @type  driverSurface:        string (nurbsSurface)
        @param driverSurface:        the name of the geo that will drive the
                                     geometry, or the first selection
                                     
        @type  weightGeo:            string (mesh)
        @param weightGeo:            the name of the geo that will be used to
                                     raycast weighting

        @type  weightBase:           string array
        @param weightBase:           Optional.  A copy of the geometry that will
                                     be deformed.  This allows weights to be 
                                     projected to a non moving geometry.  Very 
                                     important when you have multiple weight
                                     projecting deformers on the same mesh.

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
        self.weightBase              = weightBase
        self.lockAttrs               = lockAttrs
        self.ihi                     = ihi
        self.side                    = side
        self.name                    = name
        self.uNames                  = uNames
        self.vNames                  = vNames
        self.nNames                  = nNames
        #----vars
        self.driverShape             = ''
        self.weightGeoShape          = ''
        self.geomShapes              = []
        self.weightBaseShapes        = []
        self.returnDeformer          = ''
        self.deformerName            = ''
        self.baseGeo                 = ''
        self.baseShape               = ''
        self.baseName                = ''
        self.driverType              = ''
        self.uValAttrs               = []
        self.vValAttrs               = []
        self.nValAttrs               = []
        self.uWeights                = []
        self.vWeights                = []
        self.nWeights                = []
        self.uAnimCurvesU            = []
        self.uAnimCurvesV            = []
        self.vAnimCurvesU            = []
        self.vAnimCurvesV            = []
        self.nAnimCurvesU            = []
        self.nAnimCurvesV            = []
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
        if self.uNames:
            for i in self.uNames:
                cmds.addAttr(self.control, longName= i,
                                    at='float', keyable=True)
                self.uValAttrs.append(self.control + '.' + i)
        #----vValAttr
        if self.vNames:
            for i in self.vNames:
                cmds.addAttr(self.control, longName= i,
                                    at='float', keyable=True)
                self.vValAttrs.append(self.control + '.' + i)
        #----nValAttr
        if self.nNames:
            for i in self.nNames:
                cmds.addAttr(self.control, longName= i,
                                    at='float', keyable=True)
                self.nValAttrs.append(self.control + '.' + i)
    def __createWeights(self):
        """add u and v weights to deformer"""

        #----Weights
        if self.uNames:
            for i in self.uNames:
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
                cmds.makePaintable('LHSlideDeformer', i + "Weight", attrType='doubleArray', shapeMode='deformer')
                self.uWeights.append(self.returnDeformer + "." + i +'Weights')

        #----Weights
        if self.vNames:
            for i in self.vNames:
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
                cmds.makePaintable('LHSlideDeformer', i + "Weight", attrType='doubleArray', shapeMode='deformer')
                self.vWeights.append(self.returnDeformer + "." + i +'Weights')

        #----nWeights
        if self.nNames:
            for i in self.nNames:
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
                cmds.makePaintable('LHSlideDeformer', i + "Weight", attrType='doubleArray', shapeMode='deformer')
                self.nWeights.append(self.returnDeformer + "." + i +'Weights')


    def __createAnimCurves(self):
        """add anim curves"""
        #----uAnimCurves
        if self.uNames:
            for i in range(len(self.uNames)):
                self.uAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                        name = self.uNames[i] 
                                                        + "_ACV"))
                self.uAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                        name = self.uNames[i] 
                                                        + "Falloff_ACV"))
        #----vAnimCurves
        if self.vNames:
            for i in range(len(self.vNames)):
                self.vAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                        name = self.vNames[i]
                                                        + "_ACV"))
                self.vAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                        name = self.vNames[i]
                                                        + "Falloff_ACV"))
        #----nAnimCurves
        if self.nNames:
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
        if self.uNames:
            for i in range(len(self.uAnimCurvesU)):
                cmds.setKeyframe(self.uAnimCurvesU[i], v = 1, breakdown = 0,
                                 hierarchy="none", controlPoints = 0, 
                                 shape = 0, time = 0)
            for i in range(len(self.uAnimCurvesV)):
                cmds.setKeyframe(self.uAnimCurvesV[i], v = 1, breakdown = 0,
                                 hierarchy="none", controlPoints = 0, 
                                 shape = 0, time = 0)

        #----V
        if self.vNames:
            for i in range(len(self.vAnimCurvesU)):
                cmds.setKeyframe(self.vAnimCurvesU[i], v = 1, breakdown = 0,
                                 hierarchy="none", controlPoints = 0, 
                                 shape = 0, time = 0)
            for i in range(len(self.vAnimCurvesV)):
                cmds.setKeyframe(self.vAnimCurvesV[i], v = 1, breakdown = 0,
                                 hierarchy="none", controlPoints = 0, 
                                 shape = 0, time = 0)

        #----N
        if self.nNames:
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

        #----u
        if self.uNames:
            for i in range(len(self.uValAttrs)):
                cmds.connectAttr(self.uValAttrs[i], 
                                 self.returnDeformer + '.uValueParentArray['
                                 + str(i) + '].uValue', 
                                 force=True)
        #----v
        if self.vNames:
            for i in range(len(self.vValAttrs)):
                cmds.connectAttr(self.vValAttrs[i], 
                                 self.returnDeformer + '.vValueParentArray['
                                 + str(i) + '].vValue', 
                                 force=True)
        #----n
        if self.nNames:
            for i in range(len(self.nValAttrs)):
                cmds.connectAttr(self.nValAttrs[i], 
                                 self.returnDeformer + '.nValueParentArray['
                                 + str(i) + '].nValue', 
                                 force=True)

        #----connect weights
        #----u
        if self.uNames:
            for i in range(len(self.uWeights)):
                for j in range(len(self.geoms)):
                    cmds.connectAttr(self.uWeights[i] + '[' + str(j) + ']',
                                     self.returnDeformer+'.uWeightsParentArray['+
                                     str(i) +'].uWeightsParent[' + str(j) + ']',
                                     force=True)
        #----v
        if self.vNames:
            for i in range(len(self.vWeights)):
                for j in range(len(self.geoms)):
                    cmds.connectAttr(self.vWeights[i] + '[' + str(j) + ']',
                                     self.returnDeformer+'.vWeightsParentArray['+
                                     str(i) +'].vWeightsParent[' + str(j) + ']',
                                     force=True)
        #----n
        if self.nNames:
            for i in range(len(self.nWeights)):
                for j in range(len(self.geoms)):
                    cmds.connectAttr(self.nWeights[i] + '[' + str(j) + ']',
                                     self.returnDeformer+'.nWeightsParentArray['+
                                     str(i) +'].nWeightsParent[' + str(j) + ']',
                                     force=True)
    
        #----connect anim curves

        # U Anim Curves
        #----uu
        if self.uNames:
            for i in range(len(self.uAnimCurvesU)):
                cmds.connectAttr(self.uAnimCurvesU[i] + '.output', 
                                 self.returnDeformer + '.uAnimCurveUArray[' + str(i) + 
                                 '].uAnimCurveU', 
                                 force=True)
            #----uv
            for i in range(len(self.uAnimCurvesV)):
                cmds.connectAttr(self.uAnimCurvesV[i] + '.output',
                                 self.returnDeformer + '.uAnimCurveVArray[' + str(i) +
                                 '].uAnimCurveV', 
                                 force=True)
        #----vu
        if self.vNames:
            for i in range(len(self.vAnimCurvesU)):
                cmds.connectAttr(self.vAnimCurvesU[i] + '.output',
                                 self.returnDeformer + '.vAnimCurveUArray[' + str(i) +
                                 '].vAnimCurveU', 
                                 force=True)
            #----vv
            for i in range(len(self.vAnimCurvesV)):
                cmds.connectAttr(self.vAnimCurvesV[i] + '.output',
                                 self.returnDeformer + '.vAnimCurveVArray[' + str(i) +
                                 '].vAnimCurveV', 
                                 force=True)

        # N Anim Curves
        #----nu
        if self.nNames:
            for i in range(len(self.nAnimCurvesU)):
                cmds.connectAttr(self.nAnimCurvesU[i] + '.output',
                                 self.returnDeformer + '.nAnimCurveUArray[' + str(i) +
                                 '].nAnimCurveU', 
                                 force=True)
            #----nv
            for i in range(len(self.nAnimCurvesV)):
                cmds.connectAttr(self.nAnimCurvesV[i] + '.output',
                                 self.returnDeformer + '.nAnimCurveVArray[' + str(i) +
                                 '].nAnimCurveV', 
                                 force=True)
    
        #----connect nurbs curves

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
        
        
        
# slideDeformerCmd(
#                  weightGeo = 'C_weightPatch_EX',
#                  geoms = ['c_geo_HI'],
#                  driverSurface = "nurbsPlane1",
#                  control = '',
#                  ihi = 1,
#                  side='C',
#                  name='NEWSLIDE',
#                  lockAttrs = 0,
#                  uNames = ['vtTest1','tTest2','tTest3','tTest4'],
#                  vNames = ['rTest1','rTest2','rTest3','rTest4'],
#                  nNames = ['teste'],
#                  rNames = ['testd'],
#                  )
#---lips
# slideDeformerCmd(
#                  driverSurface = 'C_slidePatch_EX',
#                  weightGeo = 'C_weightPatch_EX',
#                  geoms = ['C_body_HI'],
#                  weightBase=["C_bodyBase_HI"],
#                  control = '',
#                  ihi = 1,
#                  side='C',
#                  name='testFace',
#                  lockAttrs = 0,
#                  #---Mouth
# #                 uNames = ['mouthLR','lSide','rSide'],
# #                 vNames = ['mouthUD','lMouthUD','rMouthUD',],
#                 vNames = ['mouthUD',
#                           'lMouthUD',
#                           'rMouthUD',
#                           'C_TLipUD',
#                           'C_TLipLeftUD',
#                           'C_TLipMidUD',
#                           'C_TLipRightUD',
#                           'C_TLipCenterUD',
#                           'C_TLipSneerUD',
#                           'C_TLipPinchUD',
#                           'C_BLipUD',
#                           'C_BLipLeftUD',
#                           'C_BLipMidUD',
#                           'C_BLipRightUD',
#                           'C_BLipCenterUD',
#                           'L_BLipSneerUD',
#                           'L_BLipPinchUD',
#                           'R_BLipSneerUD',
#                           'R_BLipPinchUD',
#                           ],
#                 uNames = ["mouthLR",
#                           "lSide",
#                           "rSide",
#                           'C_TLipLR',
#                           'C_TLipLeftLR',
#                           'C_TLipMidLR',
#                           'C_TLipRightLR',
#                           'C_TLipCenterLR',
#                           'C_TLipSneerLR',
#                           'C_TLipPinchLR',
#                           'C_BLipLR',
#                           'C_BLipLeftLR',
#                           'C_BLipMidLR',
#                           'C_BLipRightLR',
#                           'C_BLipCenterLR',
#                           'L_BLipSneerLR',
#                           'L_BLipPinchLR',
#                           'R_BLipSneerLR',
#                           'R_BLipPinchLR',
#                           ],
#                  #---Test
#                  nNames = ['nTest1'],
#                  )
#---Mouth
# slideDeformerCmd(
#                  driverSurface = 'C_mouthPlane_EX',
#                  weightGeo = 'C_dummyWeightPatch_EX',
#                  geoms = ['C_body_HI'],
#                  control = '',
#                  ihi = 1,
#                  side='C',
#                  name='testFace',
#                  lockAttrs = 0,
#                  #---Mouth
#                 uNames = ['mouthLR','lSide','rSide'],
#                 vNames = ['mouthUD','lMouthUD','rMouthUD',],
#                  #---Test
#                  rNames = ['rTest1'],
#                  nNames = ['nTest1'],
#                  )

#---LLids
# slideDeformerCmd(
#                  driverSurface = 'L_lidPatch_EX',
#                  weightGeo = 'L_lidWeightPatch_EX',
#                  geoms = ['C_body_HI'],
#                  control = '',
#                  ihi = 1,
#                  side='L',
#                  name='lids',
#                  lockAttrs = 0,
#                  #---Lids
#                  uNames = ['L_ULidInnLR_ACV','L_ULidMidLR_ACV','L_ULidOutLR_ACV','L_ULidLR_ACV','L_BLidInnLR_ACV','L_BLidMidLR_ACV','L_BLidOutLR_ACV','L_BLidLR_ACV'],
#                  vNames = ['L_ULidInnUD_ACV','L_ULidMidUD_ACV','L_ULidOutUD_ACV','L_ULidUD_ACV','L_BLidInnUD_ACV','L_BLidMidUD_ACV','L_BLidOutUD_ACV','L_BLidUD_ACV'],
#                  #---Test
#                  rNames = ['rTest1'],
#                  nNames = ['nTest1'],
#                  )


#---CBrows
# slideDeformerCmd(
#                  driverSurface = 'C_browPatch_EX',
#                  weightGeo = 'C_browWeightPatch_EX',
#                  geoms = ['C_body_HI'],
#                  control = '',
#                  ihi = 1,
#                  side='',
#                  name='brows',
#                  lockAttrs = 0,
#                  #---Lids
#                  uNames = ['L_LR','R_LR','C_LR','L_innLR','L_midLR','L_outLR','R_innLR','R_midLR','R_outLR'],
#                  vNames = ['L_UD','R_UD','C_UD','L_innUD','L_midUD','L_outUD','R_innUD','R_midUD','R_outUD'],
#                  #---Test
#                  rNames = ['rTest1'],
#                  nNames = ['L_N','R_N','C_N','L_innN','L_midN','L_outN','R_innN','R_midN','R_outN'],
#                  )




# cmds.NewScene,'uTest33','uTest34','uTest35','uTest36','uTest37','uTest38','uTest39'
# cmds.file(f=True, new=True)
# cmds.unloadPlugin( 'LHSlideDeformer.so' )
# cmds.loadPlugin( 'LHSlideDeformer.so' )
# cmds.file("/corp/home/lharrison/Desktop/forSlideMid.ma", f=True ,options="v=0;",  typ = "mayaAscii", o = True)
# slideDeformerCmd(
#                  driverSurface = 'C_drive_EX',
#                  weightGeo = 'C_weightPatch_EX',
#                  geoms = ['c_geo_HI'],
#                  control = '',
#                  ihi = 1,
#                  side='C',
#                  name='testFace',
#                  lockAttrs = 0,
# #                  uNames = ['uTest1','uTest2','uTest3','uTest4',"l5",'l6', 'k',"p"],
#                  uNames = ['uTest1','uTest2','uTest3','uTest4','uTest5','uTest6','uTest7','uTest8','uTest10','uTest11','uTest12','uTest13','uTest14','uTest15','uTest16','uTest17','uTest18','uTest19','uTest20','uTest21','uTest22','uTest23','uTest24','uTest25','uTest26','uTest27','uTest28','uTest29','uTest30','uTest31','uTest32','uTest33','uTest34','uTest35','uTest36','uTest37','uTest38','uTest39'],
#                  vNames = ['vTest1','vTest2','vTest3',"v4","v9","v10","v11","v12","v14"],
#                  rNames = ['rTest1','rTest2','rTest3',"r4"],
#                  nNames = ['nTest1','nTest2','nTest3',"n4"],
#                  )






# slideDeformerCmd(
#                  driverSurface = 'C_drive_EX',
#                  weightGeo = 'C_weightPatch_EX',
#                  geoms = ['c_geo_HI'],
#                  control = '',
#                  ihi = 1,
#                  side='C',
#                  name='testFace',
#                  lockAttrs = 0,
#                  uNames = ['uTest1','uTest2','uTest3','uTest4'],
#                  vNames = ['vTest1','vTest2','vTest3','vTest4'],
#                  rNames = ['rTest1','rTest2','rTest3','rTest4'],
#                  nNames = ['nTest1','nTest2','nTest3','nTest4'],
#                  )
# ModObjectsMenu MayaWindow|mainModifyMenu;
# ArtPaintAttrTool;
# artAttrToolScript 4 "";
# artAttrInitPaintableAttr;
# // Result: 1 // 
# artAttrPaintMenu( "artAttrListPopupMenu" );
# // Result: artAttrContext // 
# artAttrValues artAttrContext;
# toolPropertyShow;
# editMenuUpdate MayaWindow|mainEditMenu;
# changeToolIcon;
# dR_contextChanged;
# currentCtx;
# // Result: artAttrContext // 
# moduleDetectionLogic;
# loadModule -scan;
# artAttrCtx -e -clear `currentCtx`;

def refresh_paintable_attrs(slide_deformer):
    "if paintable attrs do not exist, remove them"
    cmds.makePaintable('LHSlideDeformer', ca = True, attrType = "doubleArray", shapeMode='deformer')
    # get all double array attributes
    attrs = cmds.listAttr(slide_deformer, ud = True, a = True)
    for i in attrs:
        paint = i.split(".")[1]
        cmds.makePaintable('LHSlideDeformer', paint, attrType='doubleArray', shapeMode='deformer')
    cmds.makePaintable('LHSlideDeformer', "weights", attrType='multiFloat', shapeMode='deformer')

# refresh_paintable_attrs("_brows_SLD")