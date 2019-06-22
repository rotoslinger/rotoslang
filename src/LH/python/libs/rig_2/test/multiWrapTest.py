from maya import cmds
from rig.deformers import multiWrap
reload(multiWrap)

def build_face_pieces():
    driven_mesh = "C_bodyBind_GEO"
    driver_meshes = ['C_upperLip', 'C_lowerLip', 'jawMouth', 'brow', 'eyes', 'L_upperLid', 'R_upperLid', 'R_lowerLid', 'L_lowerLid']
    # driver_meshes = ['C_upperLip']
    wrap_class = multiWrap.Multiwrap(geoToDeform="C_bodyBind", driver_meshes=driver_meshes, driver_mesh_base="C_bodyBindBase")
    wrap_class.create()

def build_mult_wrap():
    
    subdivisions = 5
    driven_mesh = cmds.polySphere(n="C_bodyBind_GEO",
                                  radius=1,
                                  subdivisionsX=subdivisions,
                                  subdivisionsY=subdivisions,
                                  axis=[0, 1, 0],
                                  createUVs=2,
                                  constructionHistory=0)[0]
    # cmds.polyTriangulate(driven_mesh, ch=False)
    driven_mesh_base = cmds.polySphere(n="C_bodyBind_GEOBase",
                                  radius=1,
                                  subdivisionsX=subdivisions,
                                  subdivisionsY=subdivisions,
                                  axis=[0, 1, 0],
                                  createUVs=2,
                                  constructionHistory=0)[0]
    cmds.setAttr(driven_mesh_base + ".v", 0)
    # cmds.polyTriangulate(driven_mesh_base, ch=False)
    driver_meshes = []
    for idx in range(5):
        driver_meshes.append(cmds.polySphere(n="C_bodyDriverGeo{0:02}_GEO".format(idx),
                                    radius=1,
                                    subdivisionsX=subdivisions,
                                    subdivisionsY=subdivisions,
                                    axis=[0, 1, 0],
                                    createUVs=2,
                                    constructionHistory=0)[0])
        # cmds.polyTriangulate(driver_meshes[idx], ch=False)
    
    

    wrap_class = multiWrap.Multiwrap(name="multiWrapTest", geoToDeform=driven_mesh, driver_meshes=driver_meshes, driver_mesh_base=driven_mesh_base)
    wrap_class.create()
    # cmds.setAttr(self.deformer + ".cacheClosestPoint", 0)
    # cmds.refresh()
    # cmds.setAttr(self.deformer + ".cacheClosestPoint", 1)
    wrap_class.post_create()
