import importlib
from rig.utils import misc
from rig.propcmds import stdavars
from src.LH.python.libs.rig.propcmds.OLD_components import prop_singleton
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
    glasses = prop_base.simple_component(side = "",
                                    parent_hook = std_avars.root_ctrl,
                                    rig_parent = rig_root.rig_grp,
                                    ctrl_sizes = [8,8],
                                    colors = [(1, 1, 0),(0, 1, 0)],
                                    ctrl_names = ["glasses_base", "glasses_bridge"],
                                    create_joints = True,
                                    create_buffer_shape = True,
                                    chained_pos_offset=(0, 0 ,0),

                                    debug = True)
    counter = 1 

    prop_base.simple_component(side = "L",
                                parent_hook = glasses.ctrls[1],
                                rig_parent = rig_root.rig_grp,
                                ctrl_sizes = [2],
                                ctrl_names = ["arm"],
                                create_joints = True,
                                create_buffer_shape = True,
                                joint_parent=glasses.joints[0],
                                colors = [(1, 0, 0)],

                                debug = True)
    prop_base.simple_component(side = "R",
                                parent_hook = glasses.ctrls[1],
                                rig_parent = rig_root.rig_grp,
                                ctrl_sizes = [2],
                                ctrl_names = ["arm"],
                                colors = [(0, 0, 1)],
                                create_joints = True,
                                create_buffer_shape = True,
                                joint_parent=glasses.joints[0],

                                debug = True)
