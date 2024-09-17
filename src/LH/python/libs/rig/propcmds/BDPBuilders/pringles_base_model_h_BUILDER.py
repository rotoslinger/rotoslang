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
                                            ctrl_names = ["World", "Layout", "Root"],
                                            ctrls_with_bones = [False, False, True],
                                            create_buffer_shape = True,
                                            debug = True)
    contain = prop_base.simple_component(side = "",
                                    parent_hook = std_avars.root_ctrl,
                                    rig_parent = rig_root.rig_grp,
                                    ctrl_sizes = [8],
                                    colors = [(0, 0, 1)],
                                    ctrl_names = ["Container"],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    debug = True)
    counter = 1 

    for name in ["ChipA", "ChipB", "ChipC"]:
        counter += 1
        prop_base.simple_component(side = "",
                                    parent_hook = contain.ctrls[0],
                                    rig_parent = rig_root.rig_grp,
                                    ctrl_sizes = [8],
                                    colors = [(1, 1, 0.0)],
                                    ctrl_names = [name],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    joint_parent=contain.joints[0],
                                    chained_pos_offset=(0, counter ,0),

                                    debug = True)
