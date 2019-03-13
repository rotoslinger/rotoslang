from maya import cmds
import base
reload(base)
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)
reload(misc)

class SlideSimple(object):
    def __init__(self,
                    name="testSlideSimple",
                    deformerType="LHSlideSimple",
                    geoToDeform="",
                    baseGeoToDeform="",
                    slidePatch="",
                    slidePatchBase="",
                    parent="",
                    centerToParent=True,
                    rotationTranforms=[],
                    addAtIndex=0,
                    numToAdd=1,
                    locatorName="test",
                    curveWeightsNode="",
                    curveWeightsConnectionIdx=0,
                    locations=[],
                    hide=True,
                 **kw):
        super(SlideSimple, self).__init__(**kw)
        self.name = name
        self.addAtIndex = addAtIndex
        self.deformerType = deformerType
        self.geoToDeform = geoToDeform
        self.baseGeoToDeform = baseGeoToDeform
        self.slidePatch = slidePatch
        self.slidePatchBase = slidePatchBase
        self.parent = parent
        self.centerToParent = centerToParent
        self.rotationTranforms = rotationTranforms
        self.numToAdd = numToAdd
        self.locatorName = locatorName
        self.curveWeightsNode = curveWeightsNode
        self.curveWeightsConnectionIdx = curveWeightsConnectionIdx
        self.locations = locations
        self.hide = hide
        self.deformer = ""
        self.matrixNodes = []
        self.matrixBaseNodes = []
        self.deformerType = "LHSlideSimple"

    def getDeformer(self):
        if cmds.objExists(self.name):
            self.deformer = self.name
            return
        self.deformer = cmds.deformer(self.geoToDeform, type=self.deformerType, n=self.name, foc=True)[0]

    def getNodes(self):
        self.slidePatch = misc.getShape(self.slidePatch)
        self.slidePatchBase = misc.getShape(self.slidePatchBase)
        self.baseGeoToDeform = misc.getShape(self.baseGeoToDeform)

    def setDefaultLocations(self):
        # weightMapUtils.setDefaultMultiWeightsWithDeformer(meshName, deformerName, attrName, multiAttrName, dataType, defaultValue=1.0):
        polyCount = cmds.polyEvaluate(self.geoToDeform, v=True)
        defaultVals = [1.0 for x in range(polyCount)]
        finalAttrName = "{0}.{1}[0].{2}".format(self.deformer, "weightArrays", "membershipWeight")
        cmds.getAttr(finalAttrName)
        cmds.setAttr(finalAttrName, defaultVals, type="doubleArray")


        
    def connectDeformer(self):
        cmds.connectAttr(self.slidePatch + ".worldSpace", self.deformer + ".surface")
        cmds.connectAttr(self.slidePatchBase + ".worldSpace", self.deformer + ".surfaceBase")
        cmds.connectAttr(self.baseGeoToDeform + ".worldMesh", self.deformer + ".weightArrays[0].baseGeo")

    def cleanup(self):
        return
        # for node in self.matrixNodes + self.matrixBaseNodes:
        #     if self.hide:
        #         cmds.setAttr(node + ".visibility", 0)
        #     if not self.centerToParent:
        #         continue
        #     if cmds.listRelatives(node, p=True):
        #         cmds.xform(node, os=True, t=[0,0,0], ro=[0,0,0])



    def create(self):
        self.getDeformer()
        self.getNodes()
        self.setDefaultLocations()
        self.connectDeformer()
        self.cleanup()

# cmds.reload(DeformerCmdsBase)
#===============================================================================
#CLASS:         returnDeformerCmd
#DESCRIPTION:   Creates an lhCollisionDeformer
#USAGE:         Select transform of collision objects, then the transform of the object that will collide, or set args in this order
#               Must be meshes
#RETURN:        lhCollisionDeformer
#AUTHOR:        Levi Harrison
#DATE:          January 5th, 2019
#Version        1.0.0
#===============================================================================




# class SlideSimple(base.Deformer):
#     def __init__(self,
#                  driverSurface = '',
#                  weightGeo = '',
#                  weightBase = [],
#                  geoms = [],
#                  control = "",
#                  ihi = 0,
#                  side='C',
#                  name='',
#                  lockAttrs = 1,
#                  uNames = [],
#                  vNames = [],
#                  animCurveSuffix = "ACV",
#                  deformerSuffix="SDS"
#                  ):
#         self.driverSurface           = driverSurface
#         self.geoms                   = geoms
#         self.weightGeo               = weightGeo
#         self.control                 = control
#         self.weightBase              = weightBase
#         self.lockAttrs               = lockAttrs
#         self.ihi                     = ihi
#         self.side                    = side
#         self.name                    = name
#         self.uNames                  = uNames
#         self.vNames                  = vNames
#         self.animCurveSuffix         = animCurveSuffix
#         self.deformerSuffix          = deformerSuffix
#         #----vars
#         self.driverShape             = ''
#         self.weightGeoShape          = ''
#         self.geomShapes              = []
#         self.weightBaseShapes        = []
#         self.returnDeformer          = ''
#         self.deformerName            = ''
#         self.baseGeo                 = ''
#         self.baseShape               = ''
#         self.baseName                = ''
#         self.driverType              = ''
#         self.uValAttrs               = []
#         self.vValAttrs               = []
#         self.uWeights                = []
#         self.vWeights                = []
#         self.uAnimCurvesU            = []
#         self.uAnimCurvesV            = []
#         self.vAnimCurvesU            = []
#         self.vAnimCurvesV            = []
#         self.create()

#     def checkArgs(self):
#         # setup default suffix if user hasn't changed from base
#         # if self.suffix == "NUL":
#         #     self.suffix = "SDS"

#         # if not self.drivers and not self.drivens:
#         #     sel = cmds.ls(sl=True)
#         #     self.drivers = sel[0:-1]
#         #     # Only get the last one if selected, there is no way to determine more that one if using selection
#         #     self.drivens = [sel[-1]]
#         if (self.driverSurface and self.weightGeo and self.geoms):
#             return
#         else:
#             self.getArgsBySelection()

#     def getArgsBySelection(self):
#         try:
#             sel = cmds.ls(sl=True)
#             self.driverSurface = sel[0]
#             self.weightGeo = sel[1]
#             self.geoms = sel[2:]
#         except:
#             raise Exception('''please give arguments (driverCurve, geoms) or select 1 driver geo and at least 1 piece of geometry \n' ''')
#             quit()

#     def getShapes(self):
#         self.driverShape = self.getShape(self.driverSurface)
#         self.weightGeoShape = self.getShape(self.weightGeo)
#         # Geos 
#         for geom in self.geoms:
#             self.geomShapes.append(self.getShape(geom))
#         # Weight bases
#         for base in self.weightBase:
#             self.weightBaseShapes.append(self.getShape(base))
    
#     def createGeo(self):
#         self.baseName = self.getBaseName(self.driverSurface)
#         if cmds.objExists(self.baseName):
#             self.baseShape = self.baseName + "Shape"
#             self.baseGeo = self.baseName
#             return
#         self.baseGeo,self.baseShape = self.duplicateMeshClean(self.driverSurface, self.baseName)

#     def getTransformData(self):
#         return

#     def createDeformer(self):
#         self.returnDeformer = cmds.deformer(self.geoms, 
#                                             type = 'LHSlideSimple',
#                                             name= self.side + "_" +
#                                                   self.name + "_" + self.deformerSuffix)[0]

#     def createAttributes(self):
#         """add u and v attrs to control"""
        
#         if not self.control:
#             self.control = self.returnDeformer
#         #----uValAttr
#         if self.uNames:
#             for i in self.uNames:
#                 cmds.addAttr(self.control, longName= i,
#                                     at='float', keyable=True)
#                 self.uValAttrs.append(self.control + '.' + i)
#         #----vValAttr
#         if self.vNames:
#             for i in self.vNames:
#                 cmds.addAttr(self.control, longName= i,
#                                     at='float', keyable=True)
#                 self.vValAttrs.append(self.control + '.' + i)
#         #----nValAttr
#         if self.nNames:
#             for i in self.nNames:
#                 cmds.addAttr(self.control, longName= i,
#                                     at='float', keyable=True)
#                 self.nValAttrs.append(self.control + '.' + i)

#     def connectDeformer(self):
#         return
#         # Drivers
#         # for i, shape in enumerate(self.driverShapes):
#         #     cmds.connectAttr(shape + ".outMesh", self.deformer + ".colliderInputArray[{0}].inputGeo".format(i))
#         #     cmds.connectAttr(shape + ".boundingBox.boundingBoxMin", self.deformer  + ".colliderInputArray[{0}].colBBMin".format(i))
#         #     cmds.connectAttr(shape + ".boundingBox.boundingBoxMax", self.deformer  + ".colliderInputArray[{0}].colBBMax".format(i))
#         # for i, matrix in enumerate(self.driverWorldMatrices):
#         #     cmds.connectAttr(matrix, self.deformer + ".colliderInputArray[{0}].colWorldMatrix".format(i))








#         # ============ TEMP
#         # Driven
#         # for i, shape in enumerate(self.baseGeoShapes):
#         #     cmds.connectAttr(shape + ".outMesh", self.deformer + ".inputGeoArray[{0}].inputGeo".format(i))

#         # for i, shape in enumerate(self.baseGeoShapes):
#         #     cmds.connectAttr(shape + ".boundingBox.boundingBoxMin", self.deformer  + ".deformInputArray[{0}].mainBBMax".format(i))
#         #     cmds.connectAttr(shape + ".boundingBox.boundingBoxMax", self.deformer  + ".deformInputArray[{0}].mainBBMin".format(i))
#         # for i, matrix in enumerate(self.drivenWorldMatrices):
#         #     cmds.connectAttr(matrix, self.deformer + ".deformInputArray[{0}].mainWorldMatrix".format(i))
