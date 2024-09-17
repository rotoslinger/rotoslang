import importlib
from rig.utils import misc
from rig.propcmds import stdavars
from rig.propcmds import prop_singleton
from rig_2.tag import utils as tag_utils
from rig.propcmds import prop_base
importlib.reload(prop_base)
importlib.reload(misc)
importlib.reload(stdavars)
importlib.reload(prop_singleton)
importlib.reload(tag_utils)

def create_std_rig(name = "Prop"):
    rig_root = misc.create_rig_hier(name=name)
    std_avars = stdavars.create_stdavar_ctrl(side = "C",
                                            skel_parent = rig_root.skeleton_grp,
                                            rig_parent = rig_root.rig_grp,
                                            ctrl_sizes = [12,((12)*.9),((11)*.9)],
                                            colors = [ 
                                                        (.8, 0, 0.0),
                                                        (0.4, 0, 0.0),
                                                        (0.4, 0, 0.0)],
                                            ty_offsets = [0,0,0],
                                            ctrl_names = ["World", "Layout", "Root"],
                                            ctrls_with_bones = [False, False, True],
                                            create_buffer_shape = True,
                                            debug = True)
    child_001 = prop_base.simple_component(side = "",
                                            parent_hook = std_avars.root_ctrl,
                                            skel_parent = rig_root.skeleton_grp,
                                            rig_parent = rig_root.rig_grp,
                                            ctrl_sizes = [8],
                                            colors = [(1, 1, 0.0)],
                                            ty_offsets = [0,0,0],
                                            ctrl_names = ["ControlA"],
                                            create_joints = True,
                                            create_buffer_shape = True,

                                            debug = True)
    child_002 = prop_base.simple_component(side = "",
                                            parent_hook = std_avars.root_ctrl,
                                            skel_parent = rig_root.skeleton_grp,
                                            rig_parent = rig_root.rig_grp,
                                            ctrl_sizes = [10, 10, 10],
                                            colors = [ 
                                                        (.8, 0, 0.0),
                                                        (0.4, 0, 0.0),
                                                        (0.4, 0, 0.0)],
                                            ty_offsets = [0,0,0],
                                            ctrl_names = ["ControlB", "ControlC", "ControlD"],
                                            create_joints = True,
                                            chained_pos_offset=(1,1,0),

                                            create_buffer_shape = True,
                                            debug = True)




    
                            

# # Original 
# def create_std_rigOLD(name = "Prop"):
#     std_avars = misc.create_rig_hier(name=name)
#     std_avars = stdavars.create_stdavar_ctrl(side = "C",
#                                             skel_parent = std_avars.skeleton_grp,
#                                             rig_parent = std_avars.rig_grp,
#                                             ctrl_sizes = [12,((12)*.9),((11)*.9)],
#                                             colors = [ 
#                                                         (.8, 0, 0.0),
#                                                         (0.4, 0, 0.0),
#                                                         (0.4, 0, 0.0)],
#                                             ty_offsets = [0,0,0],
#                                             ctrl_names = ["World", "Layout", "Root"],
#                                             ctrls_with_bones = [False, False, True],
#                                             debug = True)
#     child_001 = prop_singleton.Component(numBuffer=1,
#                                          gimbal=False,
#                                          ctrl_names = ["ControlA"],
#                                          colors = [(1.0, 1.0, 0.0)], # RGB Yellow by default
#                                          ctl_sizes = [8.0],
#                                          parent=std_avars.ctrls[2],   # by default this will go in the root
#                                          ctrls_with_bones = [True],
#                                          null_transform=False)
#     child_001.create()
#     child_002 = prop_singleton.Component(numBuffer=1,
#                                          gimbal=False,
#                                          ctrl_names = ["ControlB", "ControlC"],
#                                          colors = [(1.0, 1.0, 0.0), (1.0, 1.0, 0.0)], # RGB Yellow by default
#                                          ctl_sizes = [8.0, 8.0],
#                                          parent=std_avars.ctrls[2],   # by default this will go in the root
#                                          ctrls_with_bones = [True, True],
#                                          null_transform=False)
#     child_002.create()




    
    #print(child_001.ctrl)
                            
#tag_utils.get_tag_dict("tag_filter=["CONTROL"]")