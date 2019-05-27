import ast
from maya import cmds
from rig.utils import misc
reload(misc)
from rig_2.message import utils as message_utils
reload(message_utils)

def get_no_exports():
    return get_tag_dict(tag_filter=["NO_EXPORT"])

def get_tag_dict(tag_filter=["NO_EXPORT"]):
    tag_dict = {}
    for tag in tag_filter:
        for node in get_all_with_tag(tag):
            # Instantiate empty list if the key does not yet exist
            if node not in tag_dict.keys():
                tag_dict[node] = []
            tag_dict[node].append(tag)
    return tag_dict

# Temp, for testing, REMOVE ME
TAG_DICT = {u'C_upperLipPrimaryGimbal_CTL': ['NO_EXPORT'], u'C_upperLipPrimary01_BUF': ['NO_EXPORT'], u'C_upperLipPrimary_CTL': ['NO_EXPORT'], u'C_upperLipPrimary_GUIDE': ['NO_EXPORT']}

def set_tags_from_dict(tag_dict = TAG_DICT):
    for node in tag_dict.keys():
        for tag in tag_dict[node]:
            create_tag(node, tag)

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
    cmds.setAttr(node_to_tag +"." + tag_name,
                    l = True,
                    k=False)

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


def tag_gimbal(node_to_tag):
    create_tag(node_to_tag, "GIMBAL")


def tag_control(node_to_tag):
    create_tag(node_to_tag, "CONTROL")


def tag_guide(node_to_tag):
    create_tag(node_to_tag, "GUIDE")

def tag_guide_shape(node_to_tag):
    create_tag(node_to_tag, "GUIDE_SHAPE")


def tag_bind_joint(node_to_tag):
    create_tag(node_to_tag, "BIND")


def tag_weight_curve(node_to_tag):
    create_tag(node_to_tag, "WEIGHT_CURVE")

def tag_falloff_weight_curve(node_to_tag):
    create_tag(node_to_tag, "FALLOFF_WEIGHT_CURVE")


def get_all_with_tag(tag):
    return [x for x in cmds.ls() if cmds.objExists(x + "." + tag)]


def get_all_shape_with_tag(tag):
    return [x for x in cmds.ls(shapes=True) if cmds.objExists(x + "." + tag)]


def vis_all_with_tag(tag, vis=True):
    nodes = get_all_with_tag(tag)
    for node in nodes:
        cmds.setAttr(node + ".v", vis)


def vis_all_shape_with_tag(tag, vis=True):
    nodes = get_all_shape_with_tag(tag)
    for node in nodes:
        cmds.setAttr(node + ".v", vis)


def get_all_gimbals():
    return get_all_with_tag("GIMBAL")


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
    for node in nodes:
        tag_no_export(node)


def remove_no_export_tag(nodes):
    # if set to be tagged NO_EXPORT attr is added,
    # this is then exported along with whatever else and recreated on build
    # if it is removed, it will export
    for node in nodes:
        remove_tag_no_export(node)


def no_export_add_remove_selector(nodes, add=True):
    if add:
        add_no_export_tag(nodes)
    else:
        remove_no_export_tag(nodes)

def control_from_selected():
    return [control for control in cmds.ls(sl=True) if cmds.objExists(control + ".CONTROL")]

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
        controls.append(curve_dict["control_node"])
        curve_names.append(curve_dict["curve_name"])
        curve_weights_nodes.append(curve_dict["curve_weights_node"])
        nodes.append(curve_dict["node"])
        output_indices.append(curve_dict["output_idx"])
        if "hand_weights" in curve_dict.keys():
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
