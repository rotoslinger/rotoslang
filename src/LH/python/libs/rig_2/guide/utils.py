from maya import cmds
import maya.OpenMaya as OpenMaya
import json, os

from rig_2.tag import utils as tag_utils
reload(tag_utils)
from rig.utils import misc
reload(misc)
from rig.utils import exportUtils
reload(exportUtils)
from rig.utils import weightMapUtils
reload(weightMapUtils)

from rig.rigComponents import meshRivetCtrl
reload(meshRivetCtrl)
from rig_2.manipulator import nurbscurve
reload(nurbscurve)
from rig_2.mirror import utils as mirror_utils
reload(nurbscurve)

def get_no_exports():
    return tag_utils.get_tag_dict()

def get_control_shapes(no_export_tag_dict=None):
    all_controls = tag_utils.get_all_controls()
    return get_shape_dicts(all_controls, no_export_tag_dict=no_export_tag_dict)

def get_guide_positions(no_export_tag_dict=None):
    all_guide_transforms = tag_utils.get_all_guides()
    return get_guide_transforms(all_guide_transforms, no_export_tag_dict)

def get_guide_shapes(no_export_tag_dict=None):
    all_guide_transforms = tag_utils.get_all_guides()
    return get_shape_dicts(all_guide_transforms, no_export_tag_dict=no_export_tag_dict)

def get_gimbal_shapes(no_export_tag_dict=None):
    all_gimbal_transforms = tag_utils.get_all_gimbals()
    return get_shape_dicts(all_gimbal_transforms, no_export_tag_dict=no_export_tag_dict)

def set_no_exports(tag_dict):
    tag_utils.set_tags_from_dict(tag_dict)

def set_guide_positions(transform_dict, no_export_tag_dict=None):
    set_guide_transforms(transform_dict, no_export_tag_dict)
    # Make sure to update all constraints after guides are set
    cmds.refresh()
    misc.update_all_geo_constraints()
    return

def export_all(filename, ctrl_shape=True, guide=True, guide_shape=True, gimbal_shape=True):
    export_dict = {}
    no_export_tag_dict = get_no_exports()
    export_dict["no_export_tag_dict"] = no_export_tag_dict
    if ctrl_shape:
        export_dict["control_shapes"] = get_control_shapes(no_export_tag_dict)
    if guide:
        export_dict["guide_positions"] = get_guide_positions(no_export_tag_dict)
    if guide_shape:
        export_dict["guide_shapes"] = get_guide_shapes(no_export_tag_dict)
    if gimbal_shape:
        export_dict["gimbal_shapes"] = get_gimbal_shapes(no_export_tag_dict)

    # Make sure the path exists
    path= os.path.dirname(os.path.normpath(filename))
    if not os.path.exists(path):
        os.mkdir(path)

    file = open(filename, "wb")
    json.dump(export_dict, file, sort_keys = False, indent = 2)
    file.close()
    return export_dict

def import_all(filename, ctrl_shape=True, guide=True, guide_shape=True, gimbal_shape=True):
    file = open(filename, "rb")
    import_dict = json.load(file)
    file.close()

    no_export_tag_dict = import_dict["no_export_tag_dict"]

    # Set NO_EXPORT tags
    tag_utils.set_tags_from_dict(no_export_tag_dict)
    # Control Shapes
    if ctrl_shape:
        set_shapes_from_dict(import_dict["control_shapes"], no_export_tag_dict)
    # guidePositions
    if guide:
        set_guide_positions(import_dict["guide_positions"], no_export_tag_dict)
    # Guide Shapes
    if guide_shape:
        set_shapes_from_dict(import_dict["guide_shapes"], no_export_tag_dict)
    # Gimbal Shapes
    if gimbal_shape:
        set_shapes_from_dict(import_dict["gimbal_shapes"], no_export_tag_dict)


###############################################################################
############################### Guide Data ####################################
###############################################################################
def get_guide_custom_attrs(guide_nodes, no_export_tag_dict, specified_attrs):
    # This will export all user defined attributes on a guide node
    custom_attribute_dict = {}
    user_defined_attrs = []

    for node in guide_nodes:
        if node in no_export_tag_dict.keys():
            continue
        custom_attribute_dict[node]["user_defined_attrs"] = cmds.listAttr( node, cb=True)

        


def get_guide_transforms(guide_nodes, no_export_tag_dict, debug=False):
    guide_position_dict = {}
    translations = []
    rotations = []
    scales = []
    for node in guide_nodes:
        if node in no_export_tag_dict.keys():
            continue
        if cmds.objectType(node) != "transform":
            node = misc.getParent(node)
        guide_position_dict[node] = {}
        guide_position_dict[node]["translation"] = cmds.xform(node, q=True, ws=True, t=True)
        guide_position_dict[node]["rotation"] = cmds.xform(node, q=True, ws=True, ro=True)
        guide_position_dict[node]["scale"] = cmds.xform(node, q=True, ws=True, s=True)
    if debug:
        print guide_position_dict
    return guide_position_dict

def set_guide_transforms(guide_position_dict, no_export_tag_dict):
    for node in guide_position_dict.keys():
        if node in no_export_tag_dict.keys():
            continue
        cmds.xform(node, ws=True, t=guide_position_dict[node]["translation"])
        cmds.xform(node, ws=True, ro=guide_position_dict[node]["rotation"])
        cmds.xform(node, ws=True, s=guide_position_dict[node]["scale"])



###############################################################################
################################# SHAPES ######################################
###############################################################################

def get_shape_dicts(curve_transforms, no_export_tag_dict=None):
    shapeDict = {}
    for transform in curve_transforms:
        if cmds.objectType(transform) != "transform" and cmds.objectType(transform) != "nullTransform":
            transform = misc.getParent(transform)
        if no_export_tag_dict and transform in no_export_tag_dict.keys():
            continue
        shapeDict[transform] = nurbscurve.get_curve_shape_dict(mayaObject=transform, space=OpenMaya.MSpace.kObject)
    return shapeDict

def set_shapes_from_dict(shape_dict, no_export_tag_dict=None):
    for transform in shape_dict.keys():
        if no_export_tag_dict and transform in no_export_tag_dict.keys():
            continue
        # print shape_dict
        nurbscurve.create_curve(shape_dict[transform],
                                name=shape_dict[transform]["name"],
                                parent=shape_dict[transform]["parent"],
                                transform_suffix=None,
                                check_existing = True
                                )



###############################################################################
################################# TAGGING #####################################
###############################################################################

def add_no_export_tag(nodes):
    # if set to be tagged NO_EXPORT attr is added,
    # this is then exported along with whatever else and recreated on build
    # if it is removed, it will export
    for node in nodes:
        tag_utils.tag_no_export(node)

def remove_no_export_tag(nodes):
    # if set to be tagged NO_EXPORT attr is added,
    # this is then exported along with whatever else and recreated on build
    # if it is removed, it will export
    for node in nodes:
        tag_utils.remove_tag_no_export(node)

def no_export_add_remove_selector(nodes, add=True):
    if add:
        add_no_export_tag(nodes)
    else:
        remove_no_export_tag(nodes)

def gimbal_tag_no_export(add=True, checkbox_on=False):
    if not checkbox_on:
        return
    # select controls to be tagged and run
    # Will tag gimbal shapes from being saved out
    sorted_nodes = control_from_selected()
    nodes = misc.get_nodes_from_message(sorted_nodes, "gimbal")
    no_export_add_remove_selector(nodes, add)
    return nodes

def guide_tag_no_export(add=True, checkbox_on=False):
    if not checkbox_on:
        return
    # select controls to be tagged and run
    # Will tag guide positions from being saved out
    sorted_nodes = control_from_selected()
    nodes =  misc.get_nodes_from_message(sorted_nodes, "guide")
    no_export_add_remove_selector(nodes, add)
    return nodes

def guide_shape_tag_no_export(add=True, checkbox_on=False):
    if not checkbox_on:
        return
    # select controls to be tagged and run
    # Will tag guide positions from being saved out
    sorted_nodes = control_from_selected()
    nodes =  misc.get_nodes_from_message(sorted_nodes, "guide_shape")
    no_export_add_remove_selector(nodes, add)
    return nodes

def control_tag_no_export(add=True, checkbox_on=False):
    if not checkbox_on:
        return
    # select controls to be tagged and run
    # Will tag control shapes from being saved out
    return_nodes = []
    # You need to have controls selected for this to work
    nodes = control_from_selected()
    for sel in nodes:
        return_nodes.append(sel)
    no_export_add_remove_selector(return_nodes, add)
    return return_nodes

def control_from_selected():
    return [control for control in cmds.ls(sl=True) if cmds.objExists(control + ".CONTROL")]

def tag_all_no_export(ctrl_shape=True, guide=True, guide_shape=True, gimbal_shape=True):
    control_tag_no_export(checkbox_on=ctrl_shape)
    guide_tag_no_export(checkbox_on=guide)
    guide_shape_tag_no_export(checkbox_on=guide_shape)
    gimbal_tag_no_export(checkbox_on=gimbal_shape)

def remove_tag_all_no_export(ctrl_shape=True, guide=True, guide_shape=True, gimbal_shape=True):
    control_tag_no_export(add=False, checkbox_on=ctrl_shape)
    guide_tag_no_export(add=False, checkbox_on=guide)
    guide_shape_tag_no_export(add=False, checkbox_on=guide_shape)
    gimbal_tag_no_export(add=False, checkbox_on=gimbal_shape)

###########################################################################
###################### MIRRORING UTILS ####################################
###########################################################################

def mirror_all_shapes():
    control_nodes = control_from_selected()
    gimbal_nodes = misc.get_nodes_from_message(control_nodes, "gimbal")
    guide_nodes = misc.get_nodes_from_message(control_nodes, "guide")
    nodes_to_mirror = control_nodes + gimbal_nodes + guide_nodes
    for source_nodes in nodes_to_mirror:
        if type(source_nodes) is not list:
            source_nodes = [source_nodes]
        for source_node in source_nodes:
            target_node = mirror_utils.get_opposite_side(source_node)
            if not target_node or not cmds.objExists(target_node):
                continue
            nurbscurve.mirror_shape(source_node, target_node)

def mirror_selected_shape_transforms():
    # control_nodes = control_from_selected()
    # gimbal_nodes = misc.get_nodes_from_message(control_nodes, "gimbal")
    # guide_nodes = misc.get_nodes_from_message(control_nodes, "guide")
    # nodes_to_mirror = control_nodes + gimbal_nodes + guide_nodes
    nodes_to_mirror = cmds.ls(sl=True)
    for source_nodes in nodes_to_mirror:
        if type(source_nodes) is not list:
            source_nodes = [source_nodes]
        for source_node in source_nodes:
            target_node = mirror_utils.get_opposite_side(source_node)
            if not target_node or not cmds.objExists(target_node):
                continue
            nurbscurve.mirror_shape(source_node, target_node)

