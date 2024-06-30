from maya import cmds
from rig.deformers import multiWrap
import importlib
importlib.reload(multiWrap)

def build_face_pieces():
    driven_mesh = "C_bodyBind_GEO"
    driver_meshes = ['jawMouth', 'C_brow_GEO', 'eyes', 'L_upperLid', 'R_upperLid', 'R_lowerLid', 'L_lowerLid']
    # driver_meshes = ['C_upperLip']
    wrap_class = multiWrap.Multiwrap(name="jawMouth_DEFORMER",geoToDeform=driven_mesh, driver_meshes=driver_meshes, driver_mesh_base="C_bodyBindMultiWrapBase_GEO")
    wrap_class.create()
    
    driven_mesh = "jawMouth"
    driver_meshes = ['C_upperLip', 'C_lowerLip']
    # driver_meshes = ['C_upperLip']
    wrap_class_new = multiWrap.Multiwrap(name="lip_DEFORMER",geoToDeform=driven_mesh, driver_meshes=driver_meshes, driver_mesh_base="jawMouthBase")
    wrap_class_new.create()
    

     
    
    
    # driven_mesh = "C_bodyBind_GEO"
    # driver_meshes = ['C_upperLip']
    # # driver_meshes = ['C_upperLip']
    # wrap_class = multiWrap.Multiwrap(name="UpperLip", geoToDeform=driven_mesh, driver_meshes=driver_meshes, driver_mesh_base="C_bodyBindMultiWrapBase_GEO")
    # wrap_class.create()
    
    # driven_mesh = "C_bodyBind_GEO"
    # driver_meshes = ['C_lowerLip']
    # # driver_meshes = ['C_upperLip']
    # wrap_class = multiWrap.Multiwrap(name="LowerLip", geoToDeform=driven_mesh, driver_meshes=driver_meshes, driver_mesh_base="C_bodyBindMultiWrapBase_GEO")
    # wrap_class.create()

    
    # driven_mesh = "C_bodyBind_GEO"
    # driver_meshes = ['jawMouth']
    # # driver_meshes = ['C_upperLip']
    # wrap_class = multiWrap.Multiwrap(name="Body", geoToDeform=driven_mesh, driver_meshes=driver_meshes, driver_mesh_base="C_bodyBindMultiWrapBase_GEO")
    # wrap_class.create()
    
    # Lips Drive Jaw Mouth, Jaw Mouth drives body

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
    for idx in range(2):
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
