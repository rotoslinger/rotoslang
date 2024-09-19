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

def create_std_rig(name = "noodle_rig"):
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
    noodle_container = prop_base.simple_component(side = "",
                                    parent_hook = std_avars.root_ctrl,
                                    rig_parent = rig_root.rig_grp,
                                    ctrl_sizes = [8,8],
                                    colors = [(1, 0, 0),(1, 1, 0)],
                                    ctrl_names = ["noodleBox"],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    chained_pos_offset=(0,0,0),
                                    ctrl_rotation = [0,0,0],
                                    ctrl_shape_orient = [0,0,90],
                                    root_pos_offset=(0, 2 ,0),
                                    debug = True)
    for idx in range(10):
        noodle_name = "noodle" + str(idx + 1)
        finger_x_offset = idx-5
        noodle_base = prop_base.simple_component(side = "",
                            parent_hook=noodle_container.ctrls[0],
                            joint_parent=noodle_container.joints[0],
                            rig_parent=rig_root.rig_grp,
                            ctrl_sizes = [1],
                            ctrl_names = [noodle_name + "Base"],
                            create_joints = True,
                            create_buffer_shape = True,
                            colors = [(0, 1, 0)],
                            chained_pos_offset=(0, -2 , 0),
                            root_pos_offset=(0, 0 ,finger_x_offset),
                            ctrl_shape_orient = [0, 0, 0],
                            ctrl_rotation = (90,0,-90),
                            debug = True)

        prop_base.simple_component(side = "",
                                    parent_hook=noodle_base.ctrls[0],
                                    joint_parent=noodle_base.joints[0],
                                    rig_parent=rig_root.rig_grp,
                                    ctrl_sizes = [.5],
                                    ctrl_names = [noodle_name + "start",
                                                  noodle_name + "01",
                                                  noodle_name + "02",
                                                  noodle_name + "03",
                                                  noodle_name + "end"],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    colors = [(0, 1, 0)],
                                    chained_pos_offset=(0, -2 , 0),
                                    root_pos_offset=(0, 0 ,finger_x_offset),
                                    ctrl_shape_orient = [0, 0, 0],
                                    ctrl_rotation = (0,0,0),
                                    debug = True)
        
    for idx in range(6):
        onion_name = "onion" + str(idx + 1)
        finger_x_offset = idx-2.5
        prop_base.simple_component(side = "",
                                    parent_hook=noodle_container.ctrls[0],
                                    joint_parent=noodle_container.joints[0],
                                    rig_parent=rig_root.rig_grp,
                                    ctrl_sizes = [1],
                                    ctrl_names = [onion_name],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    colors = [(0, 1, 0)],
                                    chained_pos_offset=(0, 0 , -2),
                                    root_pos_offset=(finger_x_offset, 0 ,0),
                                    ctrl_shape_orient = [0, 0, 0],
                                    # ctrl_rotation = [0,90,0],
                                    debug = True)
    for idx in range(3):
        spring_onion_name = "springOnion" + str(idx + 1)
        finger_x_offset = idx-1
        prop_base.simple_component(side = "",
                                    parent_hook=noodle_container.ctrls[0],
                                    joint_parent=noodle_container.joints[0],
                                    rig_parent=rig_root.rig_grp,
                                    ctrl_sizes = [1],
                                    ctrl_names = [spring_onion_name],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    colors = [(0, 1, 0)],
                                    chained_pos_offset=(0, 0 , -2),
                                    root_pos_offset=(finger_x_offset, 2 ,0),
                                    ctrl_shape_orient = [0, 0, 0],
                                    # ctrl_rotation = [0,90,0],
                                    debug = True)

        # prop_base.simple_component(side = "R",
        #                             parent_hook=noodle.ctrls[2],
        #                             joint_parent=noodle.joints[2],
        #                             rig_parent=rig_root.rig_grp,
        #                             ctrl_sizes = [2],
        #                             ty_offsets = [0,0,0],
        #                             ctrl_names = ["arm"],
        #                             colors = [(0, 0, 1)],
        #                             create_joints = True,
        #                             create_buffer_shape = True,

        #                             debug = True)
