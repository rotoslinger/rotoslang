from rig.deformers import multiWrap
reload(multiWrap)

def build_face_pieces():
    driven_mesh = "C_bodyBind"
    driven_meshes = ['C_upperLip', 'C_lowerLip', 'jawMouth', 'brow', 'eyes', 'L_upperLid', 'R_upperLid', 'R_lowerLid', 'L_lowerLid']
    # driven_meshes = ['C_upperLip']
    wrap_class = multiWrap.Multiwrap(geoToDeform="C_bodyBind", driven_meshes=driven_meshes, driver_mesh_base="C_bodyBindBase")
    wrap_class.create()
