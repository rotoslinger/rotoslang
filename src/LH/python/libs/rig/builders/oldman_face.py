from rig.deformers import multiWrap
import importlib
importlib.reload(multiWrap)

def build_face_pieces():
    driven_mesh = "C_bodyBind"
    driver_meshes = ['C_upperLip', 'C_lowerLip', 'jawMouth', 'brow', 'eyes', 'L_upperLid', 'R_upperLid', 'R_lowerLid', 'L_lowerLid']
    # driver_meshes = ['C_upperLip']
    wrap_class = multiWrap.Multiwrap(geoToDeform="C_bodyBind", driver_meshes=driver_meshes, driver_mesh_base="C_bodyBindBase")
    wrap_class.create()



def build_face_pieces_new():
    driven_mesh = "C_bodyBind_GEO"
    driver_meshes = [ 'jawMouth', 'C_brow_GEO']


    wrap_class = multiWrap.Multiwrap(name="MouthBrow", geoToDeform=driven_mesh, driver_meshes=driver_meshes, driver_mesh_base="C_bodyBindMultiWrapBase_GEO")
    wrap_class.create()
    
    driver_meshes = ['C_upperLip', 'C_lowerLip', 'L_upperLid', 'R_upperLid', 'R_lowerLid', 'L_lowerLid']
    
    wrap_class = multiWrap.Multiwrap(name="lidsLips", geoToDeform=driven_mesh, driver_meshes=driver_meshes, driver_mesh_base="C_bodyBindMultiWrapBase_GEO")
    wrap_class.create()
