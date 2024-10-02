
import sys
from maya import cmds
import importlib

from rig_2.tag import utils as tag_utils
from rig_2.tag import constants as tag_constants
from rig_2.message import utils as message_utils

importlib.reload(tag_utils)
importlib.reload(tag_constants)
importlib.reload(message_utils)

def finalize_maintenence(model_grp=None):
    # model_grp arg.  Optional.  Use if you want to provide the function with a model group to parent to the rig hier geo group
    rig_hier = tag_utils.RigHierarchy()
    print("RIG HIER " + str(rig_hier.hier))
    print("RIG PIECES " + str(rig_hier.pieces))
    # if cmds.objExists(rig_hier.maintenance_grp))
    root_grp, maintenance_grp, rig_grp, rig_control_grp, skeleton_grp, geo_grp = rig_hier.get_hier()
    groups = maintenance_grp, rig_grp, rig_control_grp, skeleton_grp, geo_grp 

    if model_grp:
        cmds.parent(model_grp, geo_grp)
        
    for grp in groups:
        cmds.setAttr(grp+".overrideEnabled",
                keyable = False, 
                channelBox = True,)





    print(cmds.objExists("C_crrOxyMask_rig_GRP.v"))
    # all_controls = tag_utils.get_all_with_tag(tag_constants.WILDCARD______CONTROL)
    # all_controls_shapes = tag_utils.get_all_with_tag(tag_constants.WILDCARD______CONTROL_SHAPE)
    # all_buffers = tag_utils.get_all_with_tag(tag_constants.WILDCARD______BUFFER)
    # all_buffer_shapes = tag_utils.get_all_with_tag(tag_constants.WILDCARD______BUFFER_SHAPE)
    
    # root_group = tag_utils.get_all_with_tag(tag_constants.HIER_____ROOT_GRP)[0]
    # maintenance_group = tag_utils.get_all_with_tag(tag_constants.HIER_____MAINTENANCE_GRP, hint_list=root_group)[0]
    # rig_group = tag_utils.get_all_with_tag(tag_constants.HIER_____RIG_GRP, hint_list=root_group)[0]
    # rig_control_group = tag_utils.get_all_with_tag(tag_constants.HIER_____RIG_CONTROL_GRP, hint_list=root_group)[0]
    # skeleton_group = tag_utils.get_all_with_tag(tag_constants.HIER_____SKELETON_GRP, hint_list=root_group)[0]
    # geo_group = tag_utils.get_all_with_tag(tag_constants.HIER_____GEO_GRP, hint_list=root_group)[0]


    # meant to be used after the entire rig has finished building
    # creates all neccesary attributes.
    # wires up the maintenence group
    # turns on drawing overrides
    # Adds visibility switches for the rig groups
    # Adds override display types for each rig group

    pass



'''
# cleans up the rig to make it cleaner for animation to see.

either use blackboxing or hidden in outliner
if hidden in outliner wire it up to a single debug control we can flip on and off when debugging the rig.
set ihi for all meshes
set reference and drawing overrides for the top level geom.  Also connect drawing overrides to the debug control.
make sure all fitting shapes on buffers are turned off. 




Have a button that you can use to set up scaling of the control. It adds a cluster to scale a curve and then later delete history...



Fitting guides.  Line_Width
setAttr "nurbsCircleShape1.alwaysDrawOnTop" 1;


'''