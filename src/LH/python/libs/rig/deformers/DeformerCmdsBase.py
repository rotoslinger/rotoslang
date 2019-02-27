from maya import cmds
#==================Base Class for Creating Custom Deformers============
#===============================================================================
#CLASS:         DeformerCommand
#DESCRIPTION:   Creates a deformer
#USAGE:         Select all drivers, then drivens, and run, or set args in this order
#RETURN:        deformer the self.deformer object will be the created deformer
#AUTHOR:        Levi Harrison
#DATE:          January 5th, 2019
#Version        1.0.0
#===============================================================================



class DeformerCommand(object):
    def __init__(self,
                 drivers = [],
                 drivens = [],
                 side = "C",
                 name = "deformer",
                 suffix = "NUL",
                 ihi = False,
                 parentOfNewObjects=""
                 ):
        # Args
        self.drivers = drivers
        self.drivens = drivens
        self.side = side
        self.name = name
        self.suffix = suffix
        self.ihi = ihi
        self.parentOfNewObjects = ihi

        self.create()

    def checkArgs(self):
        return
    
    def getShapes(self):
        return

    def getArgsBySelection(self):
        return

    def getShape(self, mayaObject):
        """ Assumes you only have 1 shape per transform """
        return cmds.listRelatives(mayaObject, shapes = True)[0]

    def getBaseName(self, name):
        """
        based on "L_name_TYP" naming config, but works if not
        """
        if "_" in name:
            name = self.driverSurface.split("_")
            if len(name) >= 3:
                return name[0] + '_' + name[1] + 'Base_' + name[2]
        return name + 'Base'

    def createGeo(self):
        return

    def duplicateMeshClean(self, mesh, vis=False):
        """ Makes sure to duplicate a mesh cleanly, you still need to be careful of deformations """
        meshShape = cmds.ls(mesh, dag = 1, g = 1)[0]
        newTransform = cmds.createNode("transform", n = mesh + "Base")
        newMesh = cmds.createNode("mesh", n = mesh + "BaseShape", p = newTransform)
        cmds.connectAttr(meshShape + ".outMesh", newMesh + ".inMesh")
        cmds.refresh()
        cmds.disconnectAttr(meshShape + ".outMesh", newMesh + ".inMesh")
        if self.parentOfNewObjects:
            cmds.parent(newTransform, self.parentOfNewObjects)
        if not vis:
            cmds.setAttr(newTransform + ".visibility", 0)
        return newTransform, newMesh

    def getTransformData(self):
        return

    def createDeformer(self):
        return
    
    def createAttributes(self):
        return

    def connectDeformer(self):
        return
    
    def cleanup(self):
        return

    def create(self):
        self.checkArgs()
        self.getShapes()
        self.createGeo()
        self.getTransformData()
        self.createDeformer()
        self.createAttributes()
        self.connectDeformer()
        self.cleanup()
