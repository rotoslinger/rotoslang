import importlib
from rig.utils import misc
from rig.propcmds import stdavars
from rig.propcmds import prop_singleton
from rig_2.tag import utils as tag_utils
importlib.reload(misc)
importlib.reload(stdavars)
importlib.reload(prop_singleton)
importlib.reload(tag_utils)

def create_std_rig():
    misc.create_rig_hier(name = "prop")
    std_avars = stdavars.create_stdavar_ctrl(side = "C",
                                            skel_parent = "C_skeleton_GRP",
                                            rig_parent = "C_rig_GRP",
                                            ctl_sizes = [12,((12)*.9),((11)*.9)],
                                            colors = [ 
                                                        (.8, 0, 0.0),
                                                        (0.4, 0, 0.0),
                                                        (0.4, 0, 0.0)],
                                            ty_offsets = [0,0,0],
                                            ctrl_names = ["World", "Layout", "Root"],
                                            ctrls_with_bones = [False, False, True],
                                            debug = True)
    child_001 = prop_singleton.Component(numBuffer=1,
                                         gimbal=False,
                                         parent=std_avars.ctls[0],   # by default this will go in the root
                                         createJoint = True,
                                         null_transform=False)
    


    #create_rig_parts
    child_001.create()
                            
#tag_utils.get_tag_dict("tag_filter=["CONTROL"]")