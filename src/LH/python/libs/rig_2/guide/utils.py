from maya import cmds
import maya.OpenMaya as OpenMaya

from rig_2.message import utils as message_utils
reload(message_utils)

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
from rig_2.shape import nurbscurve

reload(nurbscurve)
from rig_2.mirror import utils as mirror_utils
reload(nurbscurve)

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
    position_preservation_nodes = []
    constraints = []
    for node in guide_position_dict.keys():
        if not cmds.objExists(node):
            continue
        if node in no_export_tag_dict.keys():
            continue
        position_preservation_node = cmds.createNode("transform")
        cmds.xform(position_preservation_node, ws=True, a=True, r=False, p=True, t=guide_position_dict[node]["translation"])
        cmds.xform(position_preservation_node, ws=True, a=True, r=False, p=True, ro=guide_position_dict[node]["rotation"])
        cmds.xform(position_preservation_node, ws=True, a=True, r=False, p=True, s=guide_position_dict[node]["scale"])
        constraints.append(cmds.parentConstraint(position_preservation_node, node, mo=False)[0])
        constraints.append(cmds.scaleConstraint(position_preservation_node, node, mo=False)[0])
        position_preservation_nodes.append(position_preservation_node)
    cmds.refresh()
    cmds.delete(constraints)
    cmds.refresh()
    cmds.delete(position_preservation_nodes)
        # translate = guide_position_dict[node]["translation"]
        # rotation = guide_position_dict[node]["rotation"]
        # scale = guide_position_dict[node]["scale"]
        # cmds.move(translate[0], translate[1], translate[2],node,  ws=True, a=True, r=False, pcp=True, )
        # cmds.move(translate[0], translate[1], translate[2],node,  ws=True)
        # cmds.rotate(rotation[0], rotation[1], rotation[2], node, ws=True, a=True, r=False, pcp=True, )
        # cmds.scale(scale[0], scale[1], scale[2], node, ws=True, a=True, r=False, pcp=True, )



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
        nurbscurve.create_curve(shape_dict[transform],
                                name=shape_dict[transform]["name"],
                                parent=shape_dict[transform]["parent"],
                                transform_suffix=None,
                                check_existing = True
                                )



###############################################################################
################################# TAGGING #####################################
###############################################################################

def gimbal_tag_no_export(add=True, checkbox_on=False):
    return tag_utils.tag_no_export_from_control_message("gimbal", add, checkbox_on)

def guide_tag_no_export(add=True, checkbox_on=False):
    return tag_utils.tag_no_export_from_control_message("guide", add, checkbox_on)

def guide_shape_tag_no_export(add=True, checkbox_on=False):
    return tag_utils.tag_no_export_from_control_message("guide_shape", add, checkbox_on)

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
    tag_utils.no_export_add_remove_selector(return_nodes, add)
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
    gimbal_nodes = message_utils.get_nodes_from_message(control_nodes, "gimbal")
    guide_nodes = message_utils.get_nodes_from_message(control_nodes, "guide")
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

