from maya import cmds, OpenMaya

from rig_2.shape import mesh
import importlib
importlib.reload(mesh)
from rig_2.shape import nurbscurve
importlib.reload(nurbscurve)
from rig_2.shape import nurbsurface
importlib.reload(nurbsurface)
from rig.utils import misc
def get_shapes(transform):
    return cmds.listRelatives(transform, s=True)

def create_agnostic_point_position_dict(transforms):
    # reguardless of the type of the shape, get the point positions
    position_shape_dict = {}
    for transform in transforms:
        shapes = get_shapes(transform)
        if not shapes:
            continue
        for idx, shape in enumerate(shapes):
            position_shape_dict[shape] = get_points(shape, idx)
    return position_shape_dict

def set_agnostic_point_position(shape, point_array):
    if not cmds.objExists(shape) or not point_array:
        return
    set_points(shape, 0, point_array)


def deserialize_point_array(point_array):
    json_point_array = []
    for i in range(point_array.length()):
        json_point_array.append([point_array[i].x, point_array[i].y, point_array[i].z])
    return json_point_array

def serialize_json_point_array(json_point_array):
    point_array = OpenMaya.MPointArray()
    for i in range(len(json_point_array)):
        point_array.append(OpenMaya.MPoint(json_point_array[i][0],
                                           json_point_array[i][1],
                                           json_point_array[i][2],
                                           ))
    return point_array



    # geo_type = cmds.objectType(misc.getShape(sel))
def get_points(shape, idx):
    point_count = misc.getOMItergeo(shape).count()
    point_positions = []
    geo_type = cmds.objectType(shape)
    tweak_node = cmds.listConnections(shape + ".tweakLocation")
    if not tweak_node:
        return
    tweak_node=tweak_node[0]
    if geo_type == "nurbsCurve" or geo_type == "nurbsSurface":
        point_positions_attr_name = "{0}.plist[{1}].controlPoints[0:{2}]".format(tweak_node, idx, point_count)
        point_positions = cmds.getAttr(point_positions_attr_name)
    if geo_type == "mesh":
        point_positions_attr_name = "{0}.vlist[{1}].vertex[0:{2}]".format(tweak_node, idx, point_count)
        point_positions = cmds.getAttr(point_positions_attr_name)
    return point_positions


def set_points(shape, idx, point_positions):
    point_count = misc.getOMItergeo(shape).count()
    geo_type = cmds.objectType(shape)
    tweak_node = cmds.listConnections(shape + ".tweakLocation")
    if not tweak_node:
        return
    tweak_node=tweak_node[0]
    if geo_type == "nurbsCurve" or geo_type == "nurbsSurface":
        for i in range(point_count):
            cmds.setAttr("{0}.plist[{1}].controlPoints[{2}]".format(tweak_node, idx, i), *point_positions[i], typ="double3")
    if geo_type == "mesh":
        for i in range(point_count):
            cmds.setAttr("{0}.vlist[{1}].vertex[{2}]".format(tweak_node, idx, i), *point_positions[i], typ="double3")

def get_point_positions(formatted_shape_string):
    point_positions = []
    for point in cmds.ls(formatted_shape_string, fl=True):
        point_positions.append(cmds.xform(point, os=True, q=True, t=True))
    return point_positions

def format_nurbs_shape_string(nurbs_shape):
        spans_u = cmds.getAttr(nurbs_shape + ".spansU")
        degree_u = cmds.getAttr(nurbs_shape + ".degreeU")
        spans_v = cmds.getAttr(nurbs_shape + ".spansV")
        degree_v = cmds.getAttr(nurbs_shape + ".degreeV")
        u_cv_idx = spans_u + degree_u -1
        v_cv_idx = spans_v + degree_v -1
        return "{0}.cv[0:{1}][0:{2}]".format(nurbs_shape, u_cv_idx, v_cv_idx)
