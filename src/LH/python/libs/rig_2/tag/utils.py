import ast
from maya import cmds
from rig.utils import misc
import importlib
importlib.reload(misc)
from rig_2.message import utils as message_utils
importlib.reload(message_utils)
from rig_2.attr import utils as attr_utils
importlib.reload(attr_utils)

from rig_2.tag import constants as tag_constants
importlib.reload(tag_constants)


def get_no_exports(check_component_class_no_export=True):
    return get_tag_dict(tag_filter=["NO_EXPORT"],
                        check_component_class_no_export=check_component_class_no_export)

def get_tag_dict(tag_filter=["NO_EXPORT"], check_component_class_no_export=True):
    tag_dict = {}
    for tag in tag_filter:
        for node in get_all_with_tag(tag):
            # Make sure to remove from the dict if EXPORT_OVERRIDE exists
            if node in list(tag_dict.keys()) and cmds.objExists(node + ".EXPORT_OVERRIDE"):
                del tag_dict[node]
                # if node not in tag_dict.keys():
                #     tag_dict[node] = []
                # if "DELETE_NOEXPORT_IF_EXISTS" not in tag_dict[node]:
                #     tag_dict[node].append("DELETE_NOEXPORT_IF_EXISTS")
                continue
            if cmds.objExists(node + ".EXPORT_OVERRIDE"):
                continue
            # Create key entry if the key does not yet exist
            if node not in list(tag_dict.keys()):
                tag_dict[node] = []
            tag_dict[node].append(tag)
    if not check_component_class_no_export:
        return tag_dict
    # This is strictly for enforcing the class NO EXPORT NODES tag
    for component in get_all_component_names():
        component_class_node = get_class_node_from_component_name(component)
        if not cmds.objExists(component_class_node + ".NO_EXPORT"):
            # for node in get_nodes_by_component_name(component):
            #     if node not in tag_dict.keys():
            #         tag_dict[node] = []
            #     if "DELETE_NOEXPORT_IF_EXISTS" not in tag_dict[node]:
            #         tag_dict[node].append("DELETE_NOEXPORT_IF_EXISTS")
            continue
        for node in get_nodes_by_component_name(component):
            # Failsafe make sure to remove from the dict if EXPORT_OVERRIDE exists
            if node in list(tag_dict.keys()) and cmds.objExists(node + ".EXPORT_OVERRIDE"):
                # if "DELETE_NOEXPORT_IF_EXISTS" not in tag_dict[node]:
                #     tag_dict[node].append("DELETE_NOEXPORT_IF_EXISTS")
                del tag_dict[node]

            if cmds.objExists(node + ".EXPORT_OVERRIDE"):
                continue
            # Create key entry if the key does not yet exist
            if node not in list(tag_dict.keys()):
                tag_dict[node] = []
            tag_dict[node].append("NO_EXPORT")
            # Create the tag 
            create_tag(node, "NO_EXPORT")
    return tag_dict

# Temp, for testing, REMOVE ME
TAG_DICT = {'C_upperLipPrimaryGimbal_CTL': ['NO_EXPORT'], 'C_upperLipPrimary01_BUF': ['NO_EXPORT'], 'C_upperLipPrimary_CTL': ['NO_EXPORT'], 'C_upperLipPrimary_GUIDE': ['NO_EXPORT']}

def set_tags_from_dict(tag_dict = TAG_DICT, check_component_class_no_export=True):
    for node in list(tag_dict.keys()):
        for tag in tag_dict[node]:
            create_tag(node, tag)
    if not check_component_class_no_export:
        return
    # This is strictly for enforcing the class NO EXPORT NODES tag
    for component in get_all_component_names():
        component_class_node = get_class_node_from_component_name(component)
        if not cmds.objExists(component_class_node + ".NO_EXPORT"):
            continue
        for node in get_nodes_by_component_name(component):
            if cmds.objExists(node + ".EXPORT_OVERRIDE"):
                continue
            create_tag(node, "NO_EXPORT")
        # Create key entry if the key does not yet exist
            if node not in list(tag_dict.keys()):
                tag_dict[node] = []
            tag_dict[node].append("NO_EXPORT")
    return tag_dict

def create_tag(node_to_tag, tag_name="TAG", warn=False):
    if cmds.objExists(node_to_tag + "." + tag_name):
        if warn:
            cmds.warning( "The node {0} already has the tag {1}, not adding tag.".format(node_to_tag, tag_name) )
        return
    if not cmds.objExists(node_to_tag):
        if warn:
            cmds.warning( "The node {0} does not exist, not adding tag {1}.".format(node_to_tag, tag_name) )
        return
    cmds.addAttr(node_to_tag, ln = tag_name,
                    at = "bool",)
    cmds.setAttr(node_to_tag +"." + tag_name, True)
    cmds.setAttr(node_to_tag +"." + tag_name,
                    l = True,
                    k=False)

def get_class_node_from_component_name(component_name):
    return "{0}_CLASS".format(component_name)

def create_component_tag(node_to_tag, component_name, connect_to_class_node=True):
    class_node = "{0}_CLASS".format(component_name)
    if not cmds.objExists(class_node):
        return
    if type(node_to_tag) != list:
        node_to_tag = [node_to_tag]
    for node in node_to_tag:
        if connect_to_class_node:
            component_class_attr = attr_utils.get_attr(node, "component_class_" + component_name, attrType="message")
            cmds.connectAttr(class_node + ".membership_nodes", component_class_attr, f=True)

        attr = node + ".COMPONENT_MEMBERSHIP"
        if cmds.objExists(attr):
            return attr
        attr_utils.get_attr(node, "COMPONENT_MEMBERSHIP", dataType="string")
        cmds.setAttr(attr, component_name, type="string")
        
        return attr

def get_arg_node_by_component_name(component_name):
    nodes = get_nodes_by_component_name(component_name)
    for node in nodes:
        if not cmds.objExists(node + ".COMPONENT_ARG_NODE"):
            continue
        return node

def get_all_tags_in_component(component):
    nodes = get_nodes_by_component_name(component)
    all_tag_attrs = []
    for node in nodes:
        attrs = cmds.listAttr(node, userDefined=True)
        if not attrs:
            continue
        # Remove tags and message attrs
        attrs = [x for x in attrs if x.isupper() and not cmds.addAttr(node + "." + x, q=True, attributeType=True) == "message"]
        all_tag_attrs += attrs
    
    all_tag_attrs = list(dict.fromkeys(all_tag_attrs))
    all_tag_attrs = [str(x) for x in all_tag_attrs if x not in tag_constants.ARG_UI_FILTER]
    return all_tag_attrs
    
def get_all_component_names():
    component_pieces = get_all_with_tag("COMPONENT_MEMBERSHIP")
    component_names = [cmds.getAttr(x + ".COMPONENT_MEMBERSHIP") for x in component_pieces]
    # remove duplicate entries
    component_names = list(dict.fromkeys(component_names))
    return component_names

def get_all_component_tag_vals():
    component_pieces = get_all_with_tag("COMPONENT_MEMBERSHIP")
    component_names = [cmds.getAttr(x + ".COMPONENT_MEMBERSHIP") for x in component_pieces]
    return list(dict.fromkeys(component_names))

def get_nodes_by_component_name(component_name, message_connection=True):
    if message_connection:
        component_class_node = get_class_node_from_component_name(component_name)
        if not cmds.objExists(component_class_node + ".membership_nodes"):
            return []
        nodes = cmds.listConnections(component_class_node + ".membership_nodes")
        if nodes:
            # make sure no Null returns...
            nodes = [node for node in nodes if node]
            return nodes
    
    component_pieces = get_all_with_tag("COMPONENT_MEMBERSHIP")
    return_nodes = []
    for node in component_pieces:
        value = cmds.getAttr(node + ".COMPONENT_MEMBERSHIP")
        if component_name not in value:
            continue
        return_nodes.append(node)

    return return_nodes

def get_all_nodes_by_maya_component_class_name(component_class_node):
    nodes = cmds.listConnections(component_class_node + ".membership_nodes")
    if nodes:
        # make sure no Null returns...
        nodes = [node for node in nodes if node]
        return nodes
    

def remove_tag(tagged_node, tag_name="TAG"):
    attr_full_name = tagged_node + "." + tag_name
    if not cmds.objExists(attr_full_name):
        return
    cmds.setAttr(tagged_node + "." + tag_name,
                l = False)
    cmds.deleteAttr(attr_full_name)


def tag_no_export(node_to_tag):
    if not node_to_tag:
        return
    if type(node_to_tag) != list:
        node_to_tag = [node_to_tag]
    for node in node_to_tag:
        create_tag(node, "NO_EXPORT")


def remove_tag_no_export(tagged_node):
    if not tagged_node:
        return
    if type(tagged_node) != list:
        tagged_node = [tagged_node]
    for node in tagged_node:
        remove_tag(node, "NO_EXPORT")

def tag_weighted_mesh(node_to_tag):
    create_tag(node_to_tag, "WEIGHTED_MESH")
    
def tag_guide_class(node_to_tag):
    create_tag(node_to_tag, "GUIDE_CLASS")


def tag_arg_node(node_to_tag):
    create_tag(node_to_tag, "COMPONENT_ARG_NODE")
    
def tag_rivet_mesh(node_to_tag):
    create_tag(node_to_tag, "RIVET_MESH")

# ################# FACE GUIDES ################# #
def tag_slide_geo(node_to_tag):
    create_tag(node_to_tag, "SLIDE_GEO")

def tag_base_geo(node_to_tag):
    create_tag(node_to_tag, "BASE_GEO")
    
def tag_guide_curves(node_to_tag):
    create_tag(node_to_tag, "GUIDE_CURVES")
    
def tag_lid_curves(node_to_tag):
    create_tag(node_to_tag, "LID_CURVES")
    
def tag_brow_curves(node_to_tag):
    create_tag(node_to_tag, "BROW_CURVES")
    
def tag_lip_volume_curves(node_to_tag):
    create_tag(node_to_tag, "LIP_VOLUME_CURVES")
    
def tag_lip_roll_curves(node_to_tag):
    create_tag(node_to_tag, "LIP_ROLL_CURVES")
    
def tag_projection_mesh(node_to_tag):
    create_tag(node_to_tag, "PROJECTION_MESH")
    
def tag_reference_geo(node_to_tag):
    create_tag(node_to_tag, "REFERENCE_GEO")
    
def tag_guide_geo(node_to_tag):
    create_tag(node_to_tag, "GUIDE_GEO")

def tag_export_override(node_to_tag):
    create_tag(node_to_tag, "EXPORT_OVERRIDE")


def tag_rivet_orient_patch(node_to_tag):
    create_tag(node_to_tag, "RIVET_ORIENT_PATCH")
    
def tag_guide_cacheable(node_to_tag):
    create_tag(node_to_tag, "GUIDE_CACHEABLE")
#################################################

### RIG HIERARCHY TAGS
### These will be used for doing rig cleanup and locking before a publish
### They will also make it extremely easy to unlock the rig and work on it
### GEO_GROUP will have overrides turned on and will be set to reference

def tag_root_group(node_to_tag):
    create_tag(node_to_tag, "ROOT_GRP")
def tag_ctrl_group(node_to_tag):
    create_tag(node_to_tag, "CONTROL_GRP")
def tag_maintenance_group(node_to_tag):
    create_tag(node_to_tag, "MAINTENANCE_GRP")

def tag_rig_group(node_to_tag):
    create_tag(node_to_tag, "RIG_GRP")

# This is the place to add clusters that are used to scale controls
def tag_rig_ctrl_group(node_to_tag):
    create_tag(node_to_tag, "RIG_CONTROL_GRP")
def tag_rig_ctrlsize_group(node_to_tag):
    create_tag(node_to_tag, "RIG_CONTROL_SIZE_GRP")

def tag_skeleton_group(node_to_tag):
    create_tag(node_to_tag, "SKELETON_GRP")
def tag_bindjnt_group(node_to_tag):
    create_tag(node_to_tag, "BIND_JOINT_GRP")
def tag_rootskel_joint(node_to_tag):
    create_tag(node_to_tag, "ROOT_SKEL_JOINT")

def tag_helpjnt_group(node_to_tag):
    create_tag(node_to_tag, "HELPER_JOINT_GRP")

def tag_geo_group(node_to_tag):
    create_tag(node_to_tag, "GEO_GRP")

def tag_gimbal(node_to_tag):
    create_tag(node_to_tag, "GIMBAL")

def tag_control(node_to_tag):
    create_tag(node_to_tag, "CONTROL")

def tag_buffer(node_to_tag):
    create_tag(node_to_tag, "BUFFER")

def tag_buffer_shape(node_to_tag):
    create_tag(node_to_tag, "BUFFER_SHAPE")
    
def tag_control_shape(node_to_tag):
    create_tag(node_to_tag, "CONTROL_SHAPE")


def tag_guide(node_to_tag):
    create_tag(node_to_tag, "GUIDE")

def tag_delete_me(node_to_tag):
    create_tag(node_to_tag, "DELETE_ME")

def tag_guide_shape(node_to_tag):
    create_tag(node_to_tag, "GUIDE_SHAPE")


def tag_bind_joint(node_to_tag):
    create_tag(node_to_tag, "BIND_JNT")


def tag_weight_curve(node_to_tag):
    create_tag(node_to_tag, "WEIGHT_CURVE")

def tag_falloff_weight_curve(node_to_tag):
    create_tag(node_to_tag, "FALLOFF_WEIGHT_CURVE")

def tag_dynamic_mirrored(node_to_tag):
    create_tag(node_to_tag, "DYNAMIC_MIRRORED")

def get_all_with_tag(tag, hint_list=None):
    if not hint_list:
        hint_list = cmds.ls()
    if type(hint_list) != list:
        hint_list = cmds.listRelatives(hint_list, allDescendents = True)
    return [x for x in hint_list if cmds.objExists(x + "." + tag)]

class RigHierarchy():
    def __init__(self):
        self.hier = self.get_hier()
        self.pieces = self.get_pieces()
        
    def get_hier(self):
        self.root_grp = get_all_with_tag(tag_constants.HIER_____ROOT_GRP)[0]
        self.maintenance_grp = get_all_with_tag(tag_constants.HIER_____MAINTENANCE_GRP, hint_list=self.root_grp)[0]
        self.rig_grp = get_all_with_tag(tag_constants.HIER_____RIG_GRP, hint_list=self.root_grp)[0]
        self.rig_control_grp = get_all_with_tag(tag_constants.HIER_____RIG_CONTROL_GRP, hint_list=self.root_grp)[0]
        self.skeleton_grp = get_all_with_tag(tag_constants.HIER_____SKELETON_GRP, hint_list=self.root_grp)[0]
        self.geo_grp = get_all_with_tag(tag_constants.HIER_____GEO_GRP, hint_list=self.root_grp)[0]
        return self.root_grp, self.maintenance_grp, self.rig_grp, self.rig_control_grp, self.skeleton_grp, self.geo_grp
    
    def get_pieces(self):
        all_controls = get_all_with_tag(tag_constants.WILDCARD______CONTROL)
        all_controls_shapes = get_all_with_tag(tag_constants.WILDCARD______CONTROL_SHAPE)
        all_buffers = get_all_with_tag(tag_constants.WILDCARD______BUFFER)
        all_buffer_shapes = get_all_with_tag(tag_constants.WILDCARD______BUFFER_SHAPE)
        return all_controls, all_controls_shapes, all_buffers, all_buffer_shapes





def get_all_in_component_with_tag(tag, component_name):
    hint_list = get_nodes_by_component_name(component_name)
    return get_all_with_tag(tag, hint_list)

def get_all_shape_with_tag(tag):
    return [x for x in cmds.ls(shapes=True) if cmds.objExists(x + "." + tag)]


def vis_all_with_tag(tag, vis=True, component=None, vis_shape=True, vis_transform=False):
    # Is only going to set visibility for nodes that have a shape parented directly beneath them
    # By default only sets vis for the shape to avoid toggling visibility for entire hierarchies
    # Has option to hide by transform
    hint_list=None
    if component:
       hint_list = get_nodes_by_component_name(component)
    nodes = get_all_with_tag(tag, hint_list)
    for node in nodes:
        if not node:
            continue
        shapes = cmds.listRelatives(node, s=True)
        if not shapes:
            continue
        if vis_transform:
            safe_set_visibility(node, vis=vis)            

        if not vis_shape:
            continue
        
        for shape in shapes:
            safe_set_visibility(shape, vis=vis)            
            # if not cmds.objExists(shape + ".visibility"):
            #     continue
            # cmds.setAttr(shape + ".v", vis)
    return tag, vis

def safe_set_visibility(node, vis=True):
    try:
        cmds.setAttr(node + ".v", vis)
    except:
        # Either the attribute doesn't exist, or it is locked, or connected, okay to silently fail
        return

def make_selectable_all_with_tag(tag, selectable=True, component=None):
    hint_list=None
    if component:
       hint_list = get_nodes_by_component_name(component)
    nodes = get_all_with_tag(tag, hint_list)
    for node in nodes:
        if not node:
            continue
        shapes = cmds.listRelatives(node, s=True)
        if not shapes:
            continue
        for shape in shapes:
            try:
                if selectable:
                    cmds.setAttr(shape + ".overrideEnabled", 1)
                    cmds.setAttr(shape + ".overrideDisplayType", 0)
                else:
                    cmds.setAttr(shape + ".overrideEnabled", 1)
                    cmds.setAttr(shape + ".overrideDisplayType", 2)
            except:
                continue
    return tag, selectable

def refresh_all_component_vis_select():
    return

def vis_all_shape_with_tag(tag, vis=True):
    nodes = get_all_shape_with_tag(tag)
    for node in nodes:
        cmds.setAttr(node + ".v", vis)


def get_all_gimbals():
    return get_all_with_tag("GIMBAL")

def get_all_guide_geo():
    return get_all_with_tag("GUIDE_GEO")


def get_all_guides():
    return get_all_with_tag("GUIDE")


def get_all_controls():
    return get_all_with_tag("CONTROL")

def get_weight_curves():
    return get_all_with_tag("WEIGHT_CURVE")

def get_falloff_weight_curves():
    return get_all_with_tag("FALLOFF_WEIGHT_CURVE")

def select_all_with_tag(tag):
    cmds.select(get_all_with_tag(tag))


def get_transform_all_with_tag(tag):
    ret_transforms = []
    nodes = get_all_with_tag(tag)
    for node in nodes:
        # if the object's world location, rotation, scale can be queried, add it to the transforms
        if cmds.objectType(node) == "transform" or cmds.objectType(node) == "joint":
            ret_transforms.append(node)
            continue
        # If not it probably is a shape, so find the parent and add that
        ret_transforms.append(misc.getParent(node))
    return ret_transforms

def select_all_guides():
    select_all_with_tag("GUIDE")


def vis_all_guides():
    vis_all_shape_with_tag("GUIDE", True)
    vis_all_shape_with_tag("GUIDE_SHAPE", True)


def hide_all_guides():
    vis_all_shape_with_tag("GUIDE", False)
    vis_all_shape_with_tag("GUIDE_SHAPE", False)


def select_guide_from_selected():
    guides = []
    for sel in cmds.ls(sl=True):
        if not cmds.objExists(sel + ".guide"):
            continue
        guides.append(cmds.listConnections(sel + ".guide")[0])
    cmds.select(guides)


def add_no_export_tag(nodes):
    # if set to be tagged NO_EXPORT attr is added,
    # this is then exported along with whatever else and recreated on build
    # if it is removed, it will export
    if type(nodes) != list:
        nodes= [nodes]
    for node in nodes:
        tag_no_export(node)


def remove_no_export_tag(nodes):
    # if set to be tagged NO_EXPORT attr is added,
    # this is then exported along with whatever else and recreated on build
    # if it is removed, it will export
    if type(nodes) != list:
        nodes= [nodes]
    for node in nodes:
        remove_tag_no_export(node)


def no_export_add_remove_selector(nodes, add=True):
    if add:
        add_no_export_tag(nodes)
    else:
        remove_no_export_tag(nodes)

def control_from_selected():
    return [control for control in cmds.ls(sl=True) if cmds.objExists(control + ".CONTROL")]

def component_from_selected():
    return get_all_with_tag("COMPONENT_ARG_NODE", hint_list=cmds.ls(sl=True))

def tag_no_export_from_control_message(message_name, add=True, checkbox_on=False):
    # Finds a node from the specified control by the specified message name, tags it NO_EXPORT, or removes that tag
    if not checkbox_on:
        return
    sorted_nodes = control_from_selected()
    nodes =  message_utils.get_nodes_from_message(sorted_nodes, message_name)
    no_export_add_remove_selector(nodes, add)
    return nodes

def remove_nodes_with_tags_from_list(tag_name, node_list):
    for idx, curve in enumerate(node_list):
        if cmds.objExists(curve + "." + tag_name):
            node_list.pop(idx)
    return node_list

def tag_no_export_from_control_connection_dict(add=True,
                                               weight_curves=True,
                                               falloff_weight_curves=True,
                                               hand_painted_weights=True
                                               ):
    # Finds a node from the specified control by the specified message name, tags it NO_EXPORT, or removes that tag
    sorted_nodes = control_from_selected()
    nodes_to_tag = []
    for ctrl in sorted_nodes:
        controls, curve_names, curve_weights_nodes, nodes, output_indices, hand_weights = get_connection_weight_data(ctrl,
                                                                                                                     connection_attr_name="weight_curve_connection_dicts")
        if weight_curves:
            nodes_to_tag += curve_names
        if hand_painted_weights:
            nodes_to_tag += hand_weights
        controls, curve_names, curve_weights_nodes, nodes, output_indices, hand_weights = get_connection_weight_data(ctrl,
                                                                                                                     connection_attr_name="falloff_weight_curve_connection_dicts")
        if falloff_weight_curves:
            nodes_to_tag += curve_names
    no_export_add_remove_selector(nodes_to_tag, add)
    return nodes_to_tag

def get_connection_weight_data(ctrl, connection_attr_name="weight_curve_connection_dicts"):
    # attr_name Options are "weight_curve_connection_dicts" OR "falloff_weight_curve_connection_dicts"
    weights_string_dict = [ast.literal_eval(str(x)) for x in cmds.getAttr(ctrl + "." + connection_attr_name)]
    controls, curve_names, curve_weights_nodes, nodes, output_indices, hand_weights = get_data_from_connection_dict(weights_string_dict)
    return controls, curve_names, curve_weights_nodes, nodes, output_indices, hand_weights

def get_data_from_connection_dict(connection_dict_list):
    controls = []
    curve_names = []
    curve_weights_nodes = []
    nodes = []
    output_indices = []
    hand_weights = []
    for curve_dict in connection_dict_list:
        controls.append(curve_dict["control_parent"])
        curve_names.append(curve_dict["curve_name"])
        curve_weights_nodes.append(curve_dict["curve_weights_node"])
        nodes.append(curve_dict["node"])
        output_indices.append(curve_dict["output_idx"])
        if "hand_weights" in list(curve_dict.keys()):
            hand_weights.append(curve_dict["hand_weights"])
    return controls, curve_names, curve_weights_nodes, nodes, output_indices, hand_weights

def get_geo_weights_from_connection_dict(ctrl, connection_attr_name="weight_curve_connection_dicts"):
    weights_string_dict = [ast.literal_eval(str(x)) for x in cmds.getAttr(ctrl + "." + connection_attr_name)]
    geos = []
    hand_weights = []
    for curve_dict in weights_string_dict:
        geos.append(curve_dict["geo_shape"])
        hand_weights.append(curve_dict["hand_weights"])
    # Get rid of duplicates
    geos = list(dict.fromkeys(geos))
    # Currently multiple geos are not supported
    geo = geos[0]
    hand_weights = list(dict.fromkeys(hand_weights))
    return geo, hand_weights





WILDCARD_____ = "Rigging wildcard tags.  These are for getting common rig items."
# Commonly Used Wildcard
WILDCARD______ROOT_SKEL_JOINT = "ROOT_SKEL_JOINT"
WILDCARD______GIMBAL = "GIMBAL"
WILDCARD______CONTROL = "CONTROL"
WILDCARD______BUFFER = "BUFFER"
WILDCARD______BUFFER_SHAPE = "BUFFER_SHAPE"
WILDCARD______CONTROL_SHAPE = "CONTROL_SHAPE"
WILDCARD______GUIDE = "GUIDE"
WILDCARD______DELETE_ME = "DELETE_ME"

### RIG HIERARCHY TAGS
### These will be used for doing rig cleanup and locking before a publish
### They will also make it extremely easy to unlock the rig and work on it
### GEO_GROUP will have overrides turned on and will be set to reference
HIER_____ = "Rig hierarchy tags.  These are places to put things, and where to do general rig cleanup."
HIER_____ROOT_GRP = "ROOT_GRP"
HIER_____ROOT_GRP = "ROOT_GRP"
HIER_____MAINTENANCE_GRP = "MAINTENANCE_GRP"
HIER_____RIG_GRP = "RIG_GRP"
HIER_____RIG_CONTROL_GRP = "RIG_CONTROL_GRP"
HIER_____RIG_CONTROL_SIZE_GRP = "RIG_CONTROL_SIZE_GRP"

HIER_____SKELETON_GRP = "SKELETON_GRP"
HIER_____BIND_JOINT_GRP = "BIND_JOINT_GRP"
HIER_____HELPER_JOINT_GRP = "HELPER_JOINT_GRP"
HIER_____GEO_GRP = "GEO_GRP"
HIER_____GUIDE_SHAPE = "GUIDE_SHAPE"
HIER_____BIND = "BIND"


# ################# FACE RIG ################# #
FACE_____= "Face rig tags.  These all have to do with the creation of the face rig."
FACE_____SLIDE_GEO="SLIDE_GEO"
FACE_____BASE_GEO="BASE_GEO"
FACE_____GUIDE_CURVES="GUIDE_CURVES"
FACE_____LID_CURVES="LID_CURVES"
FACE_____BROW_CURVES="BROW_CURVES"
FACE_____LIP_VOLUME_CURVES="LIP_VOLUME_CURVES"
FACE_____LIP_ROLL_CURVES="LIP_ROLL_CURVES"
FACE_____PROJECTION_MESH="PROJECTION_MESH"
FACE_____REFERENCE_GEO="REFERENCE_GEO"
FACE_____GUIDE_GEO="GUIDE_GEO"
FACE_____EXPORT_OVERRIDE="EXPORT_OVERRIDE"
FACE_____RIVET_ORIENT_PATCH="RIVET_ORIENT_PATCH"
FACE_____GUIDE_CACHEABLE="GUIDE_CACHEABLE"
FACE_____DYNAMIC_MIRRORED="DYNAMIC_MIRRORED"
FACE_____WEIGHT_CURVE="WEIGHT_CURVE"
FACE_____FALLOFF_WEIGHT_CURVE="FALLOFF_WEIGHT_CURVE"

#################################################
LIB_DA = "These are tags without a category."
LIB_D_WEIGHTED_MESH = "WEIGHTED_MESH",
LIB_D_GUIDE_CLASS = "GUIDE_CLASS",
LIB_D_COMPONENT_ARG_NODE = "COMPONENT_ARG_NODE",
LIB_D_RIVET_MESH="RIVET_MESH",



TAG_LIBRARY = { "misc":
                        [
                        "WEIGHTED_MESH",
                        "GUIDE_CLASS",
                        "COMPONENT_ARG_NODE",
                        "RIVET_MESH",
                        ],
                # ################# FACE GUIDES ################# #
                "face_guide":
                            [
                            "SLIDE_GEO",
                            "BASE_GEO",
                            "GUIDE_CURVES",
                            "LID_CURVES",
                            "BROW_CURVES",
                            "LIP_VOLUME_CURVES",
                            "LIP_ROLL_CURVES",
                            "PROJECTION_MESH",
                            "REFERENCE_GEO",
                            "GUIDE_GEO",
                            "EXPORT_OVERRIDE",
                            "RIVET_ORIENT_PATCH",
                            "GUIDE_CACHEABLE",
                            ],
                #################################################

                ### RIG HIERARCHY TAGS
                ### These will be used for doing rig cleanup and locking before a publish
                ### They will also make it extremely easy to unlock the rig and work on it
                ### GEO_GROUP will have overrides turned on and will be set to reference
                "rig_hierarchy":
                                [
                                "ROOT_GRP",
                                "CONTROL_GRP",
                                "MAINTENANCE_GRP",
                                "RIG_GRP",
                                "CONTROL_RIG_GRP",
                                "SKELETON_GRP",
                                "BIND_JOINT_GRP",
                                "ROOT_SKEL_JOINT",
                                "HELPER_JOINT_GRP",
                                "GEO_GRP",
                                "GIMBAL",
                                "CONTROL",
                                "BUFFER",
                                "BUFFER_SHAPE",
                                "CONTROL_SHAPE",
                                "GUIDE",
                                "DELETE_ME",
                                "GUIDE_SHAPE",
                                "BIND",
                                "WEIGHT_CURVE",
                                "FALLOFF_WEIGHT_CURVE",
                                "DYNAMIC_MIRRORED",
                                ]

}