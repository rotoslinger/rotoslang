
from maya import cmds
from rig.utils import weightMapUtils, misc
reload(weightMapUtils)

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

