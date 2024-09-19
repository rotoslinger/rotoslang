import importlib
from rig.utils import misc
from rig.propcmds import stdavars
# from src.LH.python.libs.rig.propcmds.OLD_components import prop_singleton
from rig_2.tag import utils as tag_utils
from rig.propcmds import prop_base
importlib.reload(prop_base)
importlib.reload(misc)
importlib.reload(stdavars)
# importlib.reload(prop_singleton)
importlib.reload(tag_utils)

def create_std_rig(name = "glove_rig"):
    rig_root = misc.create_rig_hier(name=name)
    std_avars = stdavars.create_stdavar_ctrl(side = "C",
                                            skel_parent = rig_root.skeleton_grp,
                                            rig_parent = rig_root.rig_grp,
                                            ctrl_sizes = [12,((12)*.9),((11)*.9)],
                                            colors = [ 
                                                        (.8, 0, 0.0),
                                                        (0.4, 0, 0.0),
                                                        (0.4, 0, 0.0)],
                                            ctrl_names = ["World", "Layout", "Root"],
                                            ctrls_with_bones = [False, False, True],
                                            create_buffer_shape = True,
                                            debug = True)
    glove = prop_base.simple_component(side = "",
                                    parent_hook = std_avars.root_ctrl,
                                    rig_parent = rig_root.rig_grp,
                                    ctrl_sizes = [8,8],
                                    colors = [(1, 0, 0),(1, 1, 0)],
                                    ctrl_names = ["glove_base", "glove_mid", "glove_base_knuckle"],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    chained_pos_offset=(0,0,-2),
                                    ctrl_rotation = [0,90,0],
                                    ctrl_shape_orient = [0,0,0],
                                    root_pos_offset=(0, 2 ,0),
                                    debug = True)
    counter = 1 
    finger_names = ["pinky", "ring", "midddle", "index", "thumb"]
    finger_x_offsets = [4,2,0,-2,-4]
    for idx, finger in enumerate(finger_names):
        prop_base.simple_component(side = "",
                                    parent_hook=glove.ctrls[2],
                                    joint_parent=glove.joints[2],
                                    rig_parent=rig_root.rig_grp,
                                    ctrl_sizes = [2],
                                    ctrl_names = [finger + "_digit_1",
                                                  finger + "_digit_2",
                                                  finger + "_digit_3"],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    colors = [(0, 1, 0)],
                                    chained_pos_offset=(0, 0 , -2),
                                    root_pos_offset=(finger_x_offsets[idx], 2 ,0),
                                    ctrl_shape_orient = [0, 0, 0],
                                    # ctrl_rotation = [0,90,0],
                                    debug = True)
        
    
        # prop_base.simple_component(side = "R",
        #                             parent_hook=glove.ctrls[2],
        #                             joint_parent=glove.joints[2],
        #                             rig_parent=rig_root.rig_grp,
        #                             ctrl_sizes = [2],
        #                             ty_offsets = [0,0,0],
        #                             ctrl_names = ["arm"],
        #                             colors = [(0, 0, 1)],
        #                             create_joints = True,
        #                             create_buffer_shape = True,

        #                             debug = True)
