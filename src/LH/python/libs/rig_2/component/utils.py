import itertools
from maya import cmds
from rig_2.manipulator import elements as manip_elements

from rig_2.mirror import utils as mirror_utils
import importlib
importlib.reload(mirror_utils)
from rig_2.name import utils as name_utils
importlib.reload(name_utils)
from rig.rigComponents import simpleton
importlib.reload(simpleton)
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)

from rig.deformers import utils as deformerUtils
importlib.reload(deformerUtils)

from rig.rigComponents import meshRivetCtrl
importlib.reload(meshRivetCtrl)

from rig.utils import misc
importlib.reload(misc)

def safe_parent(objects_to_parent, parent):
    if not cmds.objExists(parent):
        return
    for maya_object in objects_to_parent:
        if not cmds.objExists(maya_object):
            continue
        rel = cmds.listRelatives(maya_object, parent=True)
        if rel and rel[0] == parent:
            continue
        cmds.parent(maya_object, parent)


def get_projection_geo(mesh,
                       parent,
                       x_divisions=10,
                       y_divisions=10,
                       split_suffix="_GEO",
                       x_mult=1,
                       y_mult=1,
                       flip=False,
                       # If you give a list of meshes you need to give a name!!
                       name=None):
    proj_name=""
    if type(mesh) == str or type(mesh) == str:
        proj_name = mesh
    if split_suffix in mesh:
        proj_name = mesh.split(split_suffix)[0]
    proj_name += "_PRJ"
    if name:
        proj_name=name
    x, y, z, center = get_projection_dimensions(mesh)
    x = x*x_mult
    y = y*y_mult
    if cmds.objExists(proj_name):
        return proj_name
    plane = cmds.polyPlane( name = proj_name,
                           subdivisionsX = x_divisions,
                           subdivisionsY = y_divisions,
                           width = x,
                           height = y,
                           ax=[0,0,1])
    cmds.parent(plane, parent)
    cmds.move(center[0], center[1], center[2], plane)
    
    if flip:
        cmds.DeleteHistory(plane[0])
        cmds.scale(-1, plane[0], x=True)
        cmds.makeIdentity(plane[0], apply=True, t=1, r=1, s=1, n=0, pn=1)
        # make sure to flip the normals
        cmds.polyNormal(plane[0], normalMode=2, userNormalMode=1, ch=False)
    cmds.DeleteHistory(plane[0])
    cmds.makeIdentity(plane[0], apply=True, t=1, r=1, s=1, n=0, pn=1)
    tag_utils.tag_projection_mesh(plane[0])
    return plane[0]


def get_projection_dimensions(meshes, z_at_origin=True):
    # xmin, ymin, zmin, xmax, ymax, zmax
    bb = cmds.exactWorldBoundingBox(meshes)
    x = bb[0] - bb[3]
    y = bb[1] - bb[4]
    z = bb[2] - bb[5]
    center = get_bb_center(bb)
    # Put projection in front
    if z_at_origin:
        center[2] = 0
    return abs(x), abs(y), abs(z), center

def get_bb_center(bb):
    x = (bb[0] + bb[3]) / 2.0
    y = (bb[1] + bb[4]) / 2.0
    z = (bb[2] + bb[5]) / 2.0
    return [x, y, z]


def cluster_lattice_sheet(lattice_name,
                          s_count,
                          t_count,
                          control_parent,
                          handle_parent,
                          component_name,
                          side="C",
                          is_symmetric=True,
                          do_dynamic_connections=True):
    return_controls = []
    bb = cmds.exactWorldBoundingBox(lattice_name)
    x = bb[0] - bb[3]
    y = bb[1] - bb[4]
    z = bb[2] - bb[5]
    center = cmds.objectCenter(lattice_name)
    offset = [center[0], bb[1], center[2]]

    full_root_control_name = "{0}_{1}_CTL".format(side,"{0}Root".format(component_name))
    if cmds.objExists(full_root_control_name):
        root_control = full_root_control_name
    else:
        root_control = simpleton.Component( side=side,
                                            name="{0}Root".format(component_name),
                                            parent=control_parent,
                                            translate = center,
                                            rotate = [0,0,0],
                                            scale = [1,1,1],
                                            offset = offset,
                                            size=10,
                                            curveData = manip_elements.circle,
                                            component_name=component_name,
                                            null_transform = False,
                                            is_ctrl_guide = True,
                                            numBuffer=1,
                                            )
        root_control.create()
        root_control=root_control.ctrl
    sides, range_names = name_utils.name_based_on_range(count=s_count, name=component_name + "Shaper",
                                                 suffixSeperator="",
                                                 suffix="",
                                                 side_name=False,
                                                 reverse_side=True,
                                                 do_return_side=True)
    controls = []
    clusters = []
    for s, t in itertools.product(list(range(s_count)), list(range(t_count))):
        exists = False
        
        if is_symmetric:
            maya_object_name = "{0}_{1}Handle".format(sides[s], range_names[s] + "Row{0:02}".format(t))
            cluster_format_name = "{0}_{1}".format(sides[s], range_names[s] + "Row{0:02}".format(t))
            full_control_name = "{0}_{1}_CTL".format(sides[s],range_names[s] + "Row{0:02}".format(t))
            simpleton_name = range_names[s] + "Row{0:02}".format(t)
            loop_side = sides[s]
        else:
            maya_object_name = "{0}_{1}Shaper{2:02}Row{3:02}Handle".format(side, component_name, s, t)
            cluster_format_name = "{0}_{1}Shaper{2:02}Row{3:02}".format(side, component_name, s, t)
            full_control_name =  "{0}_{1}Shaper{2:02}Row{3:02}_CTL".format(side, component_name, s, t)
            simpleton_name = "{0}Shaper{1:02}Row{2:02}".format(component_name, s, t)
            loop_side = side

        if cmds.objExists(maya_object_name):
            cluster = maya_object_name
            exists = True
        else:
            cluster = cmds.cluster("{0}.pt[{1}][{2}][0:1]".format(lattice_name, s, t), n=cluster_format_name)[1]
        clusters.append(cluster)
        position = cmds.pointPosition("{0}.pt[{1}][{2}][1]".format(lattice_name, s, t), w=True)
        if cmds.objExists(full_control_name):
            control = full_control_name
            controls.append(full_control_name)
        else:
            control = simpleton.Component( side=loop_side,
                                        name=simpleton_name,
                                        parent=root_control,
                                        translate = position,
                                        rotate = [0,0,0],
                                        scale = [1,1,1],
                                        offset = [0,0,0],
                                        size=1,
                                        curveData = manip_elements.sphere_medium,
                                        component_name=component_name,
                                        null_transform = False,
                                        gimbal=False,
                                        is_ctrl_guide = True,
                                        numBuffer=1,
                                        )
            control.create()
            control = control.ctrl
            controls.append(control)
        if not exists:
            cmds.parentConstraint(control, cluster, mo=True)
            cmds.setAttr(cluster + ".v", 0)
    # After everything has been created make it dynamic symmetric
    if do_dynamic_connections:
        for control in controls:
            if "L_" in control:
                mirror_utils.add_dynamic_mirror_connection([control])
    return root_control, controls, clusters



def autoposition_matrix_deformer_controls(matrix_deformer_node, threshold=.09, is_mesh_rivet_control=False, orientation_mesh="", project_to_curve=None):
    # This will reposition matrix deformer
    # Rivets
    # Guides
    
    numElements = cmds.getAttr("{0}.inputs".format(matrix_deformer_node), mi=True)
    weighted_mesh = cmds.deformer(matrix_deformer_node, q=True, geometry=True)
    if not weighted_mesh:
        return
    weighted_mesh = weighted_mesh[0]
    print(weighted_mesh)
    for idx in range(len(numElements)):
        matrix_attr =  "{0}.inputs[{1}].matrix".format(matrix_deformer_node, idx)
        position = getPositionsFromMatrixWeightsByIndex(matrix_deformer_node, weighted_mesh, idx, threshold)
        if project_to_curve:
            position = misc.getClosestPointOnCurve(project_to_curve, position)
        
        connection = cmds.listConnections(matrix_attr)
        if not connection:
            continue
        connection = connection[0]
        # maya_object_type = str(cmds.objectType(connection))
        # if maya_object_type != "nullTransform" and maya_object_type != "transform":
        #     continue
        
        node_to_position = misc.getParent(connection)
        rotation=None
        if orientation_mesh:
            rotation=get_rotation_from_nurbs()
        if is_mesh_rivet_control:
            position_mesh_rivet(node_to_position, position, rotation)
            continue
        misc.move(node_to_position, position, rotation)

def autoposition_weight_stack_controls(weight_stack_node, threshold=.09, is_mesh_rivet_control=True, orientation_mesh="", project_to_curve=None):
    # THIS WILL NOT WORK if a transform is not connected to the factor, so be VERY CAREFUL when using this
    numElements = cmds.getAttr("{0}.inputs".format(weight_stack_node), mi=True)
    weighted_mesh = cmds.listConnections(weight_stack_node + ".weightedMesh")
    if not weighted_mesh:
        return
    weighted_mesh = weighted_mesh[0]
    for idx in range(len(numElements)):
        factor_attr =  "{0}.inputs[{1}].factor".format(weight_stack_node, idx)
        position = getPositionsFromWeightsByIndex(weight_stack_node, weighted_mesh, idx, threshold)
        if project_to_curve:
            position = misc.getClosestPointOnCurve(project_to_curve, position)
        
        connection = cmds.listConnections(factor_attr)
        if not connection:
            continue
        connection = connection[0]
        maya_object_type = str(cmds.objectType(connection))
        if maya_object_type != "nullTransform" and maya_object_type != "transform":
            continue
        node_to_position = connection
        rotation=None
        if orientation_mesh:
            rotation=get_rotation_from_nurbs()
        if is_mesh_rivet_control:
            position_mesh_rivet(node_to_position, position, rotation)
            continue
        misc.move(node_to_position, position, rotation)
            

def getPositionsFromMatrixWeightsByIndex(weight_stack_node, weighted_mesh, index=0, threshold=.09):
    weightList =  "{0}.inputs[{1}].matrixWeight".format(weight_stack_node, index)
    weightList = cmds.getAttr(weightList)
    height, width, depth, center = deformerUtils.getPointPositionByWeights(weightList, weighted_mesh, threshold=threshold)
    return [center.x, center.y, center.z]


def getPositionsFromWeightsByIndex(weight_stack_node, weighted_mesh, index=0, threshold=.09):
    weightList =  "{0}.inputs[{1}].inputWeights".format(weight_stack_node, index)
    weightList = cmds.getAttr(weightList)
    height, width, depth, center = deformerUtils.getPointPositionByWeights(weightList, weighted_mesh, threshold=threshold)
    return [center.x, center.y, center.z]

def get_rotation_from_nurbs(position, nurbs, aimVector = [0,0,1], up_vector=[0,1,0], up_vec_mult=100):
    # Based on a location, get an orientation from a nurbsSurface
    tempLocation = position
    temp_driven = cmds.createNode("transform")
    cmds.xform(temp_driven, ws=True, t=tempLocation)
    up_vector_object = cmds.createNode("transform")
    normalCons = cmds.normalConstraint(nurbs, temp_driven, aimVector=aimVector, u=up_vector, wuo=up_vector_object, worldUpType="object")
    misc.reorient_normal_constraint_up_vector_object(up_vector_object, temp_driven, up_vector, up_vec_mult=up_vec_mult)
    rotate = cmds.xform(temp_driven, q=True, ws=True, ro=True)
    cmds.delete(temp_driven, up_vector_object)
    return rotate

def position_mesh_rivet(rivet_control, position=None, rotation=None, do_auto_rotation=True, aimVector = [0,0,1]):
    buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo = meshRivetCtrl.getRivetParts(rivet_control)
    if not rotation and do_auto_rotation:
       rotation =  get_rotation_from_nurbs(position, normalConstraintGeo, aimVector)
    misc.move(buffer2, position, rotation)
    misc.updateGeoConstraint(offsetBuffer = buffer2, geoConstraint=geoConstraint)

