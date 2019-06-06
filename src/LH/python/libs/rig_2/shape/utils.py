from maya import cmds, OpenMaya

from rig_2.shape import mesh
reload(mesh)
from rig_2.shape import nurbscurve
reload(nurbscurve)
from rig_2.shape import nurbsurface
reload(nurbsurface)
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
        for shape in shapes:
            position_shape_dict[shape] = get_agnostic_point_position(shape)
    return position_shape_dict

def get_agnostic_point_position(shape):
    # iter_geo = misc.getOMItergeo(shape)
    # point_array = OpenMaya.MPointArray()
    # # Very important to get in kObject space as the geo will be deformed and transformed all over the place
    # # you want to store positioning as an additive layer
    # iter_geo.allPositions(point_array, OpenMaya.MSpace.kObject)
    
    # return deserialize_point_array(point_array)
    return get_points(shape)

def set_agnostic_point_position(shape, point_array, num_iterations=10):
    for i in range(num_iterations):
        set_points(shape, point_array)
    # point_array = serialize_json_point_array(point_array)
    # # print point_array
    # # for i in range(point_array.length()):
    # #     print point_array[i].x, point_array[i].y, point_array[i].z,
    # # Because Maya doesn't have a pre or post deform space we have to iterate over the setAllPosition method multiple times to approximate the setting of position
    # iter_geo = misc.getOMItergeo(shape)
    # for i in range(num_iterations):
    #     iter_geo.setAllPositions(point_array, OpenMaya.MSpace.kObject)

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
def get_points(shape):
    point_count = misc.getOMItergeo(shape).count()
    point_positions = []
    geo_type = cmds.objectType(shape)
    if geo_type == "nurbsCurve":
        # select -r C_upperLipVolume_CRV.cv[0:20] ;
        shape_string = "{0}.cv[0:{1}]".format(shape, point_count-1)
        point_positions = get_point_positions(shape_string)
    if geo_type == "mesh":
        shape_string = "{0}.vtx[0:{1}]".format(shape, point_count-1)
        point_positions = get_point_positions(shape_string)
    if geo_type == "nurbsSurface":
        shape_string = format_nurbs_shape_string(shape)
        point_positions = get_point_positions(shape_string)
    return point_positions


def set_points(shape, point_positions):
    geo_type = cmds.objectType(shape)
    if geo_type == "nurbsCurve":
        # select -r C_upperLipVolume_CRV.cv[0:20] ;
        shape_string = "{0}.cv[0:{1}]".format(shape, len(point_positions)-1)
        for idx, point in enumerate(cmds.ls(shape_string, fl=True)):
            cmds.xform(point, os=True, t=point_positions[idx])
    if geo_type == "mesh":
        shape_string = "{0}.vtx[0:{1}]".format(shape, len(point_positions)-1)
        for idx, point in enumerate(cmds.ls(shape_string, fl=True)):
            cmds.xform(point, os=True, t=point_positions[idx])
    if geo_type == "nurbsSurface":
        shape_string = format_nurbs_shape_string(shape)
        for idx, point in enumerate(cmds.ls(shape_string, fl=True)):
            cmds.xform(point, os=True, t=point_positions[idx])
    return point_positions


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
