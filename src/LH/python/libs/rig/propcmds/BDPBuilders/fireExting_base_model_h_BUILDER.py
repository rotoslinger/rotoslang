import importlib
from rig.utils import misc
from rig.propcmds import stdavars
from src.LH.python.libs.rig.propcmds.OLD_components import prop_singleton
from rig_2.tag import utils as tag_utils
importlib.reload(misc)
importlib.reload(stdavars)
importlib.reload(prop_singleton)
importlib.reload(tag_utils)

def create_std_rig(name = ):
    misc.create_rig_hier(name = "prop")
    std_avars = stdavars.create_stdavar_ctrl(side = "C",
                                            skel_parent = "C_skeleton_GRP",
                                            rig_parent = "C_rig_GRP",
                                            ctrl_sizes = [12,((12)*.9),((11)*.9)],
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
                                         ctrl_names = ["ControlA"],
                                         colors = [(1.0, 1.0, 0.0)], # RGB Yellow by default
                                         ctl_sizes = [8.0],
                                         parent=std_avars.ctrls[2],   # by default this will go in the root
                                         ctrls_with_bones = [True],
                                         null_transform=False)
    child_001.create()
    child_002 = prop_singleton.Component(numBuffer=1,
                                         gimbal=False,
                                         ctrl_names = ["ControlB", "ControlC"],
                                         colors = [(1.0, 1.0, 0.0), (1.0, 1.0, 0.0)], # RGB Yellow by default
                                         ctl_sizes = [8.0, 8.0],
                                         parent=std_avars.ctrls[2],   # by default this will go in the root
                                         ctrls_with_bones = [True, True],
                                         null_transform=False)
    child_002.create()




    
    #print(child_001.ctrl)
                            
#tag_utils.get_tag_dict("tag_filter=["CONTROL"]")