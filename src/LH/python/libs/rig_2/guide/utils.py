from maya import cmds
import maya.OpenMaya as OpenMaya
from rig.utils import misc
reload(misc)
from rig.utils import exportUtils
reload(exportUtils)
from rig.utils import weightMapUtils
reload(weightMapUtils)

from rig.rigComponents import meshRivetCtrl
reload(meshRivetCtrl)

def get_node_from_message(nodes, message_name):
    return_nodes = []
    for sel in cmds.ls(sl=True):
        full_attr_name = sel + "." + message_name
        if not cmds.objExists(full_attr_name):
            continue
        connection = cmds.listConnections(full_attr_name, shapes=True)
        if not connection:
            continue
        return_nodes.append(connection[0])
    return return_nodes


def add_no_export_filter(nodes):
    # if set to be filtered NO_EXPORT attr is added,
    # this is then exported along with whatever else and recreated on build
    # if it is removed, it will export
    for node in nodes:
        misc.tag_no_export(node)

def remove_no_export_filter(nodes):
    # if set to be filtered NO_EXPORT attr is added,
    # this is then exported along with whatever else and recreated on build
    # if it is removed, it will export
    for node in nodes:
        misc.remove_tag_no_export(node)

def filter_add_remove_selector(nodes, add=True):
    if add:
        add_no_export_filter(nodes)
    else:
        remove_no_export_filter(nodes)

def gimbal_filter(add=True):
    # select controls to be filtered and run
    # Will filter gimbal shapes from being saved out
    nodes = get_node_from_message(cmds.ls(sl=True), "gimbal")
    filter_add_remove_selector(nodes, add)
    return nodes

def guide_filter(add=True):
    # select controls to be filtered and run
    # Will filter guide positions from being saved out
    nodes = get_node_from_message(cmds.ls(sl=True), "guide")
    filter_add_remove_selector(nodes, add)
    return nodes

def guide_shape_filter(add=True):
    # select controls to be filtered and run
    # Will filter guide positions from being saved out
    nodes = get_node_from_message(cmds.ls(sl=True), "guide_shape")
    filter_add_remove_selector(nodes, add)
    return nodes

def control_filter(add=True):
    # select controls to be filtered and run
    # Will filter control shapes from being saved out
    return_shapes = []
    for sel in cmds.ls(sl=True):
        shape = misc.getShape(sel)
        if shape and cmds.objectType(shape) == "nurbsCurve":
            return_shapes.append(shape)
    filter_add_remove_selector(return_shapes, add)
    return return_shapes

def filter_all(add=True):
    return gimbal_filter(add) + guide_filter(add) + control_filter(add) + guide_shape_filter(add)

def get_shape_dicts(shape_nodes, filter_names=None):
    shapeDict = {}
    elemLength = cmds.getAttr(matrixDeformer + ".inputs", s=True)
    for shape in shape_nodes:
        if shape in filter_names:
            continue
        shapeDict[shape] = exportUtils.nurbsCurveData(name = shape, space=OpenMaya.MSpace.kObject).nurbsCurve
    return shapeDict

def get_gimbal_shapes(filter_names=None):
    return
def get_guide_shapes(filter_names=None):
    return
def get_control_shapes(filter_names=None):
    return
def get_guide_positions(filter_names=None):
    return

def set_gimbal_shapes(filter_names=None):
    return
def set_guide_shapes(filter_names=None):
    return
def set_control_shapes(filter_names=None):
    return
def set_guide_positions(filter_names=None):

    # Make sure to update all constraints after guides are set
    cmds.refresh()
    update_geo_constraints()
    return

def update_geo_constraints():
    return

