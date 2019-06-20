from maya import cmds
from rig.deformers import multiWrap
reload(multiWrap)


def build_mult_wrap():
    
    
    driven_mesh = cmds.polySphere(n="C_bodyBind_GEO",
                                  radius=1,
                                  subdivisionsX=5,
                                  subdivisionsY=5,
                                  axis=[0, 1, 0],
                                  createUVs=2,
                                  constructionHistory=0)[0]
    driven_mesh_base = cmds.polySphere(n="C_bodyBind_GEOBase",
                                  radius=1,
                                  subdivisionsX=5,
                                  subdivisionsY=5,
                                  axis=[0, 1, 0],
                                  createUVs=2,
                                  constructionHistory=0)[0]
    cmds.setAttr(driven_mesh_base + ".v", 0)
    driver_meshes = []
    for idx in range(3):
        driver_meshes.append(cmds.polySphere(n="C_bodyDriverGeo{0:02}_GEO".format(idx),
                                    radius=1,
                                    subdivisionsX=5,
                                    subdivisionsY=5,
                                    axis=[0, 1, 0],
                                    createUVs=2,
                                    constructionHistory=0)[0])
    
    

    wrap_class = multiWrap.Multiwrap(name="multiWrapTest", geoToDeform=driven_mesh, driver_meshes=driver_meshes, driver_mesh_base=driven_mesh_base)
    wrap_class.create()
    
