
from maya import cmds
from rig.utils import weightMapUtils, misc
import importlib
importlib.reload(weightMapUtils)
from rig.deformers import base
importlib.reload(base)

def createTestMultiWrap(baseMesh="justHead_body_M_skin_geobody_M_hrcGEOBASE", driverMeshes = ["humanLipsUpper", "humanLipsLower"]):
    cmds.file( "/home/users/levih/Desktop/supermanFace/lipsMultiWrapTest.ma", i=True, f=True )
    multiWrap = cmds.deformer("justHead_body_M_skin_geobody_M_hrcGEO", typ="LHMultiWrap", n="TESTMULTIWRAP")[0]
    baseShape = misc.getShape(baseMesh)
    cmds.connectAttr( baseShape + ".worldMesh", multiWrap + ".baseMesh")
    for idx, driverMesh in enumerate(driverMeshes):
        driverMeshShape = misc.getShape(driverMesh)
        cmds.connectAttr( driverMeshShape + ".worldMesh", multiWrap + ".inputGeoArray[{0}].inputGeo".format(idx))
    cmds.setAttr(multiWrap + ".cacheClosestPoint", 0)
    cmds.refresh()
    cmds.setAttr(multiWrap + ".cacheClosestPoint", 1)

def test():
    driver = cmds.polyCube(n="driver", h=200, w=200, d=200)[0]
    driven = []
    for idx in range(4):
        driven.append(cmds.polyCube(n="driven{0:02}".format(idx), h=200, w=200, d=200)[0])
    wrap_class = Multiwrap(geoToDeform=driver, driver_meshes=driven)
    wrap_class.create()

class Multiwrap(base.Deformer):
    def __init__(self,
                    # inherited needed arg
                    # geoToDeform,
                    driver_meshes,
                    driver_mesh_base=None,
                    component_name="multiwrap",
                 **kw):
        super(Multiwrap, self).__init__(component_name=component_name,**kw)
        self.driver_meshes = driver_meshes
        self.driver_mesh_base = driver_mesh_base
        self.deformerType="LHMultiWrap"
        # Deformer base always uses geoToDeform, but to ma

    def check(self):
        if not type(self.driver_meshes) == list:
            raise Exception('driver_meshes arg type must be list')
            quit()

    def get_base_geo(self):
        
        # get it if it exists
        if not self.driver_mesh_base and cmds.objExists(self.geoToDeform + "Base") :
            self.driver_mesh_base = self.geoToDeform + "Base"

        # duplicate the driver if the base doesnt already exist
        if not self.driver_mesh_base:
            self.driver_mesh_base = cmds.duplicate(self.geoToDeform, n = self.geoToDeform + "Base")[0]
            cmds.setAttr(self.driver_mesh_base + ".vis", 0)

        self.driver_mesh_base_shape = misc.getShape(self.driver_mesh_base)


    def getNodes(self):
        # Get all the shapes
        self.geoToDeform_shape = misc.getShape(self.geoToDeform)

        self.get_base_geo()

        self.driven_mesh_shapes = []
        for node in self.driver_meshes:
            self.driven_mesh_shapes.append(misc.getShape(node))

    def connectDeformer(self):
        print(self.driver_mesh_base_shape, "BASE SHAPE", self.deformer, "DEFORMER")
        cmds.connectAttr( self.driver_mesh_base_shape + ".worldMesh", self.deformer + ".baseMesh")
        for idx, mesh_shape in enumerate(self.driven_mesh_shapes):
            cmds.connectAttr( mesh_shape + ".worldMesh", self.deformer + ".inputGeoArray[{0}].inputGeo".format(idx))

    def post_create(self):
        cmds.setAttr(self.deformer + ".cacheClosestPoint", 0)
        cmds.refresh()
        cmds.setAttr(self.deformer + ".cacheClosestPoint", 1)
