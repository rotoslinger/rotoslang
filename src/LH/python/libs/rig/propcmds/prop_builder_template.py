import importlib
from rig.utils import misc
from rig.propcmds import stdavars
from rig_2.tag import utils as tag_utils
importlib.reload(misc)
importlib.reload(stdavars)

def create_std_rig():
    misc.create_rig_hier(name = "prop")
    controls = stdavars.create_stdavar_ctrl(side = "C",
                    skel_parent = "C_skeleton_GRP",
                    rig_parent = "C_rig_GRP",
                    ctl_sizes = [12,((12)*.9),((11)*.9)],
                    colors = [ 
                                (.8, 0, 0.0),
                                (0.4, 0, 0.0),
                                (0.4, 0, 0.0)],
                    ty_offsets = [0,0,0],
                    create_bone = True,
                    debug = True)
#tag_utils.get_tag_dict("tag_filter=["CONTROL"]")