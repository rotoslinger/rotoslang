import importlib
from rig.utils import misc
from rig.propcmds import stdavars
from rig_2.tag import utils as tag_utils
from rig.propcmds import prop_base
importlib.reload(prop_base)
importlib.reload(misc)
importlib.reload(stdavars)
importlib.reload(tag_utils)

def create_std_rig(name = "mask_tubing_rig"):
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
    mask_tubing = prop_base.simple_component(side = "",
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
                                    create_wire_deformer=True,

                                    debug = True)
    counter = 1 
    mask_pouch = prop_base.simple_component(side = "",
                                parent_hook=mask_tubing.ctrls[5],
                                joint_parent=mask_tubing.joints[5],
                                rig_parent=rig_root.rig_grp,
                                # Not adding a joint parent, because Oxy mask won't have joints, it is a wire
                                # This automatically makes the parent the root joint.
                                ctrl_sizes = [5],
                                ctrl_names = ["_pouchBase",
                                              "_pouchMid",
                                              "_pouchEnd"],
                                create_joints = True,
                                create_buffer_shape = True,
                                colors = [(.35, 0, 1)],
                                chained_pos_offset=(0, -2, 0),
                                root_pos_offset=(0, -10 ,0),
                                # ctrl_shape_orient = [0, 0, 0],
                                ctrl_rotation = [0,0,0],
                                debug = True)
    oxygen_mask = prop_base.simple_component(side = "",
                        parent_hook=mask_pouch.ctrls[2],
                        joint_parent=mask_pouch.joints[2],
                        rig_parent=rig_root.rig_grp,
                        # Not adding a joint parent, because Oxy mask won't have joints, it is a wire
                        # This automatically makes the parent the root joint.
                        ctrl_sizes = [5],
                        ctrl_names = ["_mask"],
                        create_joints = True,
                        create_buffer_shape = True,
                        colors = [(.5, 0, 1)],
                        chained_pos_offset=(0, -2, 0),
                        root_pos_offset=(0, -16 ,0),
                        # ctrl_shape_orient = [0, 0, 0],
                        ctrl_rotation = [0,0,0],
                        debug = True)
    carabiner = prop_base.simple_component(side = "",
                    parent_hook=oxygen_mask.ctrls[0],
                    joint_parent=oxygen_mask.joints[0],
                    rig_parent=rig_root.rig_grp,
                    # Not adding a joint parent, because Oxy mask won't have joints, it is a wire
                    # This automatically makes the parent the root joint.
                    ctrl_sizes = [2],
                    ctrl_names = ["_carabiner"],
                    create_joints = True,
                    create_buffer_shape = True,
                    colors = [(0, 1, 0)],
                    chained_pos_offset=(0, 0, 2),
                    root_pos_offset=(0, -20 ,0),
                    # ctrl_shape_orient = [0, 0, 0],
                    ctrl_rotation = [0,0,90],
                    debug = True)

    strap_straight = prop_base.simple_component(side = "C",
                    parent_hook=carabiner.ctrls[0],
                    joint_parent=carabiner.joints[0],
                    rig_parent=rig_root.rig_grp,
                    # Not adding a joint parent, because Oxy mask won't have joints, it is a wire
                    # This automatically makes the parent the root joint.
                    ctrl_sizes = [1],
                    ctrl_names = ["_strapStraightBase","_strapStraight1","_strapStraight2","_strapStraightEnd",],
                    create_joints = True,
                    create_buffer_shape = True,
                    colors = [(1, 1, 0)],
                    chained_pos_offset=(0, 0, 2),
                    root_pos_offset=(0, -20 ,2),
                    # ctrl_shape_orient = [0, 0, 0],
                    create_wire_deformer=True,
                    ctrl_rotation = [0,0,0],
                    debug = True)
    strap_straight_end = prop_base.simple_component(side = "",
                        parent_hook=strap_straight.ctrls[3],
                        joint_parent=strap_straight.joints[3],
                        rig_parent=rig_root.rig_grp,
                        # Not adding a joint parent, because Oxy mask won't have joints, it is a wire
                        # This automatically makes the parent the root joint.
                        ctrl_sizes = [2],
                        ctrl_names = ["_strapStraightRigidEnd"],
                        create_joints = True,
                        create_buffer_shape = True,
                        colors = [(.5, .5, 0.0)],
                        chained_pos_offset=(0, 0, 2),
                        root_pos_offset=(0, -20 ,10),
                        # ctrl_shape_orient = [0, 0, 0],
                        ctrl_rotation = [0,0,0],
                        debug = True)

    l_strap = prop_base.simple_component(side = "L",
                        parent_hook=oxygen_mask.ctrls[0],
                        joint_parent=oxygen_mask.joints[0],
                        rig_parent=rig_root.rig_grp,
                        # Not adding a joint parent, because Oxy mask won't have joints, it is a wire
                        # This automatically makes the parent the root joint.
                        ctrl_sizes = [1],
                        ctrl_names = ["_strapBase","_strapMid1","_strapMid2","_strapEnd",],
                        create_joints = True,
                        create_buffer_shape = True,
                        colors = [(1, 0, 0)],
                        chained_pos_offset=(0, -2, 0),
                        root_pos_offset=(3, -20 ,0),
                        # ctrl_shape_orient = [0, 0, 0],
                        create_wire_deformer=True,

                        ctrl_rotation = [0,0,0],
                        debug = True)

    r_strap = prop_base.simple_component(side = "R",
                        parent_hook=oxygen_mask.ctrls[0],
                        joint_parent=oxygen_mask.joints[0],
                        rig_parent=rig_root.rig_grp,
                        # Not adding a joint parent, because Oxy mask won't have joints, it is a wire
                        # This automatically makes the parent the root joint.
                        ctrl_sizes = [1],
                        ctrl_names = ["_strapBase","_strapMid1","_strapMid2","_strapEnd",],
                        create_joints = True,
                        create_buffer_shape = True,
                        colors = [(0, 0, 1)],
                        chained_pos_offset=(0, -2, 0),
                        root_pos_offset=(-3, -20 ,0),
                        # ctrl_shape_orient = [0, 0, 0],
                        create_wire_deformer=True,
                        ctrl_rotation = [0,0,0],
                        debug = True)
    strap_loop = prop_base.simple_component(side = "",
                    parent_hook=oxygen_mask.ctrls[0],
                    joint_parent=oxygen_mask.joints[0],
                    rig_parent=rig_root.rig_grp,
                    # Not adding a joint parent, because Oxy mask won't have joints, it is a wire
                    # This automatically makes the parent the root joint.
                    ctrl_sizes = [2],
                    ctrl_names = ["_loopAttachA","_LLoop","_CLoop", "_RLoop","_loopAttachB"],
                    create_joints = True,
                    create_buffer_shape = True,
                    colors = [(0, 1, 1)],
                    chained_pos_offset=(0, -2, 0),
                    root_pos_offset=(0, -20 ,0),
                    # ctrl_shape_orient = [0, 0, 0],
                    ctrl_rotation = [0,0,0],
                    floating_ctrls=True,
                    create_wire_deformer=True,

                    debug = True)



    
        # prop_base.simple_component(side = "R",
        #                             parent_hook=mask_tubing.ctrls[2],
        #                             joint_parent=mask_tubing.joints[2],
        #                             rig_parent=rig_root.rig_grp,
        #                             ctrl_sizes = [2],
        #                             ty_offsets = [0,0,0],
        #                             ctrl_names = ["arm"],
        #                             colors = [(0, 0, 1)],
        #                             create_joints = True,
        #                             create_buffer_shape = True,

        #                             debug = True)
