import importlib
from maya import cmds
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
                                    joint_parent=std_avars.root_joint,
                                    rig_parent = rig_root.rig_grp,
                                    ctrl_sizes = [8,8],
                                    colors = [(1, 0, 0),(1, 1, 0)],
                                    ctrl_names = ["noodleBox"],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    chained_pos_offset=(0,0,0),
                                    ctrl_rotation = [0,0,0],
                                    ctrl_shape_orient = [0,0,90],
                                    root_pos_offset=(0, 0 ,0),
                                    debug = True)
    noodle_container_hinges = prop_base.simple_component(side = "",
                                parent_hook = noodle_container.ctrls[0],
                                joint_parent=noodle_container.joints[0],

                                rig_parent = rig_root.rig_grp,
                                ctrl_sizes = [3,3],
                                colors = [(1, 0, 0),(1, 1, 0)],
                                ctrl_names = ["flapA",
                                              "flapB",
                                              "flapC",
                                              "flapD",],
                                create_joints = True,
                                create_buffer_shape = True,
                                chained_pos_offset=(0,0,0),
                                ctrl_rotation = [0,0,0],
                                ctrl_shape_orient = [0,0,90],
                                root_pos_offset=(0, 0 ,0),
                                debug = True)

    yVal = (50.480194 + 24.24) +0.952
    root_positions = [(-0.07074814289808273, yVal, 1.2604942321777344), (-0.07074814289808273, yVal, -2.3326282501220703), (-0.07074814289808273, yVal, -1.9153881072998047), (-0.07074814289808273, yVal, -1.545572280883789), (-0.07074814289808273, yVal, -1.1283330917358398), (-0.07074814289808273, yVal, -0.746757984161377), (-0.07074814289808273, yVal, -0.32951831817626953), (-0.07074814289808273, yVal, 0.044440269470214844), (-0.07074814289808273, yVal, 0.46167945861816406), (-0.07074814289808273, yVal, 0.8432550430297852)]
    
    noodles = []
    noodle_geom_forward = ['noodle_base_noodle_a_e_food_sub', 'noodle_base_noodle_a_j_food_sub', 'noodle_base_noodle_a_d_food_sub', 'noodle_base_noodle_a_c_food_sub', 'noodle_base_noodle_a_b_food_sub', 'noodle_base_noodle_a_f_food_sub', 'noodle_base_noodle_a_h_food_sub', 'noodle_base_noodle_a_g_food_sub', 'noodle_base_noodle_a_i_food_sub', 'noodle_base_noodle_a_a_food_sub']
    noodle_geom_backward =['noodle_base_noodle_a_j_food_sub', 'noodle_base_noodle_a_i_food_sub', 'noodle_base_noodle_a_h_food_sub', 'noodle_base_noodle_a_g_food_sub', 'noodle_base_noodle_a_f_food_sub', 'noodle_base_noodle_a_e_food_sub', 'noodle_base_noodle_a_d_food_sub', 'noodle_base_noodle_a_c_food_sub', 'noodle_base_noodle_a_b_food_sub', 'noodle_base_noodle_a_a_food_sub']
    noodle_geom= noodle_geom_forward
    for idx in range(10):
        noodle_name = "noodle" + str(idx + 1)
        geom=noodle_geom[idx]
        finger_x_offset = idx-5
        # noodle_base = prop_base.simple_component(side = "",
        #                     parent_hook=noodle_container.ctrls[0],
        #                     joint_parent=noodle_container.joints[0],
        #                     rig_parent=rig_root.rig_grp,
        #                     ctrl_sizes = [1],
        #                     ctrl_names = [noodle_name + "Base"],
        #                     create_joints = True,
        #                     create_buffer_shape = True,
        #                     colors = [(0, 1, 0)],
        #                     chained_pos_offset=(0, -2 , 0),
        #                     root_pos_offset=(0, 0 ,finger_x_offset),
        #                     ctrl_shape_orient = [0, 0, 0],
        #                     ctrl_rotation = (90,0,-90),
        #                     create_wire_deformer=True,
        #                     debug = True)
        num_ctrls = 7
        offset_all = ((50.384)/num_ctrls+1)
        print("OFFSET ALL " + str(offset_all))
        remainder = 50.384-offset_all
        print("REMAINDER  " + str(remainder))
        offset = ((50.384-offset_all)/(num_ctrls+1))
        offset = offset_all
        print("FINAL OFFSET " +str(offset))
        offset_offset_all = (offset-offset_all)*.5

        translate_ctrls_amt = remainder - offset
        print("Remainder-offset " +str(translate_ctrls_amt))
        print("DIF OFFSET AND OFFSET ALL ", offset_offset_all)

        noodles.append(prop_base.simple_component(side = "",
                                    parent_hook=noodle_container.ctrls[0],
                                    joint_parent=noodle_container.joints[0],
                                    rig_parent=rig_root.rig_grp,
                                    ctrl_sizes = [.5],
                                    ctrl_names = [noodle_name + "WireStart",
                                                  noodle_name + "Wire01",
                                                  noodle_name + "Wire02",
                                                  noodle_name + "Wire03",
                                                  noodle_name + "Wire04",
                                                  noodle_name + "Wire05",
                                                  noodle_name + "WireEnd"],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    colors = [(0, 1, 0)],
                                    chained_pos_offset=(0,-offset, 0),
                                    root_pos_offset=(root_positions[idx][0], 0, root_positions[idx][2]),
                                    ctrl_shape_orient = [0, 0, 0],
                                    ctrl_rotation = (90,0,-90),
                                    create_wire_deformer=True,
                                    floating_ctrls=True,
                                    wire_deformer_geom=geom,
                                    debug = True))
    for idx in range(10):
        # buffer_len = len(noodles[idx].ctrl_buffers)
        # buffer_root = noodles[idx].ctrl_buffers[-1]
        ctrls_buffers = noodles[idx].ctrl_buffers
        buffer_root=ctrls_buffers.pop(0)
        half_offset = (24.24)
        # cmds.move( 0,(half_offset * 2),0 , buffer_root, r=True)
        for ctrl in ctrls_buffers:
            cmds.move( 0,round(translate_ctrls_amt,5),0 , ctrl, r=True)
        cmds.move( 0,24.24,0 , buffer_root, r=True)
        # cmds.select(geom,noodles[idx].wire_curve)
        # wire_deformer=cmds.wire()




    onion_list = []
    for idx in range(6):
        onion_name = "onion" + str(idx + 1)
        finger_x_offset = idx-2.5
        onion_list.append(prop_base.simple_component(side = "",
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
                                    debug = True))
    
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

