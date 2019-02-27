from maya import cmds
import base

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

class collisionDeformerCmd(base.Deformer):

        def checkArgs(self):
            # setup default suffix if user hasn't changed from base
            if self.suffix == "NUL":
                self.suffix = "COL"
            
            if not self.drivers and not self.drivens:
                sel = cmds.ls(sl=True)
                self.drivers = sel[0:-1]
                # Only get the last one if selected, there is no way to determine more that one if using selection
                self.drivens = [sel[-1]]

        def getShapes(self):
            self.driverShapes = []
            self.drivenShapes = []
            for i in self.drivers:
                self.driverShapes.append(self.getShape(i))
            for i in self.drivens:
                self.drivenShapes.append(self.getShape(i))
        
        def createGeo(self):
            self.baseGeoShapes = []
            self.baseGeoTransform = []
            for i in self.drivenShapes:
                transform, shape = self.duplicateMeshClean(i)
                self.baseGeoShapes.append(shape)
                self.baseGeoTransform.append(transform)

        def getTransformData(self):
            self.driverWorldMatrices = []
            self.drivenWorldMatrices = []
            self.driverBBoxMin = []
            self.drivenBBoxMin = []
            self.driverBBoxMax = []
            self.drivenBBoxMax = []
            for i in self.drivers:
                self.driverWorldMatrices.append(i + ".worldMatrix[0]")
            for i in self.drivens:
                self.drivenWorldMatrices.append(i + ".worldMatrix[0]")
            for i in self.driverShapes:
                self.driverBBoxMin.append(i + ".boundingBoxMin")
                self.driverBBoxMin.append(i + ".boundingBoxMax")
            # We get the bounds from the static base geo to avoid cycles.  Otherwise the deformed geo is driving itself...
            for i in self.baseGeoShapes:
                self.drivenBBoxMin.append(i + ".boundingBoxMin")
                self.drivenBBoxMin.append(i + ".boundingBoxMax")

        def createDeformer(self):
            self.deformer = cmds.deformer(self.drivens, type="LHCollisionDeformer")[0]

        def connectDeformer(self):
            # Drivers
            for i, shape in enumerate(self.driverShapes):
                cmds.connectAttr(shape + ".outMesh", self.deformer + ".colliderInputArray[{0}].inputGeo".format(i))
                cmds.connectAttr(shape + ".boundingBox.boundingBoxMin", self.deformer  + ".colliderInputArray[{0}].colBBMin".format(i))
                cmds.connectAttr(shape + ".boundingBox.boundingBoxMax", self.deformer  + ".colliderInputArray[{0}].colBBMax".format(i))
            for i, matrix in enumerate(self.driverWorldMatrices):
                cmds.connectAttr(matrix, self.deformer + ".colliderInputArray[{0}].colWorldMatrix".format(i))








            # ============ TEMP
            # Driven
            # for i, shape in enumerate(self.baseGeoShapes):
            #     cmds.connectAttr(shape + ".outMesh", self.deformer + ".inputGeoArray[{0}].inputGeo".format(i))

            for i, shape in enumerate(self.baseGeoShapes):
                cmds.connectAttr(shape + ".boundingBox.boundingBoxMin", self.deformer  + ".deformInputArray[{0}].mainBBMax".format(i))
                cmds.connectAttr(shape + ".boundingBox.boundingBoxMax", self.deformer  + ".deformInputArray[{0}].mainBBMin".format(i))
            for i, matrix in enumerate(self.drivenWorldMatrices):
                cmds.connectAttr(matrix, self.deformer + ".deformInputArray[{0}].mainWorldMatrix".format(i))
