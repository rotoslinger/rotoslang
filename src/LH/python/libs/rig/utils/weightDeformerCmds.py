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

class weightDeformerCmd():
    def __init__(self,
                 weightGeo = '',
                 geoms = [],
                 control = "",
                 ihi = 0,
                 side='C',
                 name='',
                 lockAttrs = 1,
                 names = [],
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
        param tNames:               the names of the v channels you want
                                     the size of this array will determine how
                                     many value attributes, weight channels, and
                                     animation curve values are created
                                     example ['L_mouth', 'R_mouth']
                                     
        """
        #----args
        self.geoms                   = geoms
        self.weightGeo               = weightGeo
        self.control                 = control

        self.lockAttrs               = lockAttrs
        self.ihi                     = ihi
        self.side                    = side
        self.name                    = name
        self.names                  = names
        #----vars
        self.weightGeoShape          = ''
        self.geomShapes              = []
        self.returnDeformer          = ''
        self.deformerName            = ''
        self.tWeights                = []
        self.rWeights                = []
        self.tAnimCurvesU            = []
        self.tAnimCurvesV            = []
        self.rAnimCurvesU            = []
        self.rAnimCurvesV            = []
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
                
    def __createWeightDeformer(self):
        """creates the wrap deformer"""
        self.returnDeformer = cmds.deformer(self.geoms, 
                                            type = 'LHWeightDeformer',
                                            name= self.side + "_" +
                                                  self.name + "_WTD")[0]

    def __createWeights(self):
        """add u and v weights to deformer"""


        #----pWeights
        for i in self.names:
            cmds.addAttr(self.returnDeformer,
                         longName = i + 'pWeights',
                         numberOfChildren = 1, 
                         attributeType = 'compound',
                         multi = True, 
                         indexMatters=True)
            cmds.addAttr(self.returnDeformer, 
                         longName = i + "pWeight",
                         dataType = 'doubleArray',
                         parent = i + 'pWeights')
            cmds.makePaintable('LHVectorDeformer', i + "pWeight", attrType='doubleArray', shapeMode='deformer')
            self.tWeights.append(self.returnDeformer + "." + i +'pWeights')

    def __createAnimCurves(self):
        """add anim curves"""

        #----tAnimCurves
        for i in range(len(self.names)):
            self.tAnimCurvesU.append(cmds.createNode("animCurveTU",
                                                    name = self.names[i]
                                                    + "_ACV"))
            self.tAnimCurvesV.append(cmds.createNode("animCurveTU",
                                                    name = self.names[i]
                                                    + "Falloff_ACV"))

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





    def __connectWeightDeformer(self):
        """makes all connections into the slide deformer"""
        #----connect shapes
        cmds.connectAttr(self.weightGeoShape + '.worldMesh',
                         self.returnDeformer + '.weightPatch',
                         force=True)

        #----connect weights
        #----v
        for i in range(len(self.tWeights)):
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.tWeights[i] + '[' + str(j) + ']',
                                 self.returnDeformer+'.weightsParentArray['+
                                 str(i) +'].weightsParent[' + str(j) + ']',
                                 force=True)

        #----connect anim curves

        # U Anim Curves

        #----vu
        for i in range(len(self.tAnimCurvesU)):
            cmds.connectAttr(self.tAnimCurvesU[i] + '.output',
                             self.returnDeformer + '.uAnimCurveArray[' + str(i) +
                             '].uAnimCurve', 
                             force=True)
        #----vv
        for i in range(len(self.tAnimCurvesV)):
            cmds.connectAttr(self.tAnimCurvesV[i] + '.output',
                             self.returnDeformer + '.vAnimCurveArray[' + str(i) +
                             '].vAnimCurve', 
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
        self.__createWeightDeformer()
        self.__createWeights()
        self.__createAnimCurves()
        self.__setAnimCurveShapes()
        self.__connectWeightDeformer()
        self.__cleanup()
        
#---lips
# weightDeformerCmd(
#                  weightGeo = 'C_mouthWeightPatch_EX',
#                  geoms = ['C_body_HI'],
#                  control = '',
#                  ihi = 1,
#                  side='C',
#                  name='testFace',
#                  lockAttrs = 0,
#                  names = ["testA", "testB", "testC"
#                            ],
#                  )

def refresh_paintable_attrs(slide_deformer):
    "if paintable attrs do not exist, remove them"
    cmds.makePaintable('LHWeightDeformer', ca = True, attrType = "doubleArray", shapeMode='deformer')
    # get all double array attributes
    attrs = cmds.listAttr(slide_deformer, ud = True, a = True)
    for i in attrs:
        paint = i.split(".")[1]
        cmds.makePaintable('LHWeightDeformer', paint, attrType='doubleArray', shapeMode='deformer')
#     cmds.makePaintable('LHWeightDeformer', "weights", attrType='multiFloat', shapeMode='deformer')

refresh_paintable_attrs("C_testFace_WTD")

'''
import maya.OpenMaya as OpenMaya
parentArray = OpenMaya.MSelectionList()
parentArray.add("C_testFace_WTD.outWeightsParentArray")

parentArrayPlug = OpenMaya.MPlug()

parentArray.getPlug(0, parentArrayPlug)

# help(plug)


parentArrayDataHandle = parentArrayPlug.asMDataHandle()

FinalArrayDataHandle = OpenMaya.MArrayDataHandle(parentArrayDataHandle)
# help(arrayDataHandle)
# print arrayDataHandle.elementCount()
FinalArrayDataHandle.jumpToElement(0)
# help(FinalArrayDataHandle)
array = OpenMaya.MDoubleArray()
# FinalArrayDataHandle.set(array)




this = OpenMaya.MObject()
help(FinalArrayDataHandle)

# childData = OpenMaya.MDataHandle(FinalArrayDataHandle.outputValue().child(  ));

# plug.getPlug(0, dataHandle)
# connectedArray = OpenMaya.MIntArray()
# plug.getExistingArrayAttributeIndices(connectedArray);

# dataArrayHandle =  OpenMaya.MArrayDataHandle(plug.outputArrayValue( plug))




# print plug.elementCount()

# pPath = OpenMaya.MDagPath()
# node.getDagPath(0,pPath)
# fnCurve = OpenMaya.MFnNurbsCurve(pPath)

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
'''