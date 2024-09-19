import importlib
from rig.utils import misc
from rig.propcmds import stdavars
from rig_2.tag import utils as tag_utils
from rig.propcmds import prop_base
importlib.reload(prop_base)
importlib.reload(misc)
importlib.reload(stdavars)
importlib.reload(tag_utils)

def create_std_rig(name = "oxygen_mask_rig"):
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
    oxygen_mask = prop_base.simple_component(side = "",
                                    parent_hook = std_avars.root_ctrl,
                                    rig_parent = rig_root.rig_grp,
                                    ctrl_sizes = [2],
                                    colors = [(1, 1, 0)],
                                    ctrl_names = ["tubeBase", "tube01", "tube02", "tube03", "tube04", "tube05"],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    chained_pos_offset=(0,-2,0),
                                    ctrl_rotation = (90,0,-90),
                                    # ctrl_rotation = (90,0,-90),
                                    ctrl_shape_orient = [0,0,0],
                                    root_pos_offset=(0, 2 ,0),
                                    debug = True)
    counter = 1 
    prop_base.simple_component(side = "",
                                parent_hook=oxygen_mask.ctrls[5],
                                joint_parent=oxygen_mask.joints[5],
                                rig_parent=rig_root.rig_grp,
                                # Not adding a joint parent, because Oxy mask won't have joints, it is a wire
                                # This automatically makes the parent the root joint.
                                ctrl_sizes = [5],
                                ctrl_names = ["_pouchBase",
                                              "_pouchMid",
                                              "_pouchEnd"],
                                create_joints = True,
                                create_buffer_shape = True,
                                colors = [(0, 1, 0)],
                                chained_pos_offset=(0, -2, 0),
                                root_pos_offset=(0, -10 ,0),
                                # ctrl_shape_orient = [0, 0, 0],
                                ctrl_rotation = [0,0,0],
                                debug = True)
        
    
        # prop_base.simple_component(side = "R",
        #                             parent_hook=oxygen_mask.ctrls[2],
        #                             joint_parent=oxygen_mask.joints[2],
        #                             rig_parent=rig_root.rig_grp,
        #                             ctrl_sizes = [2],
        #                             ty_offsets = [0,0,0],
        #                             ctrl_names = ["arm"],
        #                             colors = [(0, 0, 1)],
        #                             create_joints = True,
        #                             create_buffer_shape = True,

        #                             debug = True)
