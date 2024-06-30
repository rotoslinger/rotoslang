import random, ast

from rig.utils import misc
import importlib
importlib.reload(misc)

from maya import cmds, OpenMaya

from rig_2.animcurve import utils as animcurve_utils
importlib.reload(animcurve_utils)
from rig_2.attr import utils as attr_utils
importlib.reload(animcurve_utils)

from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)

from rig_2.message import utils as message_utils
importlib.reload(message_utils)


def mirrorSelectedLocatorLToR(ctrls=None):
    if not ctrls:
        ctrls = cmds.ls(sl=True, typ="transform")
    for ctrl in ctrls:
        mirrorSelectedLocatorLToRSingle(ctrl=ctrl)

def mirror_selected_transforms(translation=True,
                               rotate=True,
                               scale=True,
                               auto_all=True,
                               standard=False,
                               behavior=False,
                                mirrorXY=True,
                                mirrorYZ=False,
                                mirrorXZ=False,

                               ):
    selected = cmds.ls(sl=True)
    for sel in selected:
        mirror_transform(sel,
                         translation=translation,
                         rotate=rotate,
                         scale=scale,
                         auto_all=auto_all,
                         standard=standard,
                         behavior=behavior,
                         mirrorXY=mirrorXY,
                         mirrorYZ=mirrorYZ,
                         mirrorXZ=mirrorXZ,

                         )
    misc.update_all_geo_constraints()
    cmds.select(selected)

def mirror_transform(maya_object,
                     translation=True,
                     rotate=True,
                     scale=False,
                     auto_all=True,
                     standard=False,
                     behavior=False,
                    mirrorXY=True,
                    mirrorYZ=False,
                    mirrorXZ=False,
                     ):

    opposite_rotate=None
    opposite_translate=None
    opposite_scale=None


    opposite_object = get_opposite_side(maya_object)
    if not opposite_object:
        return
    # current translation, if not translating
    opposite_translate = cmds.xform(opposite_object, q=True, ws = True, t=True)

    maya_object_translate = cmds.xform(maya_object, q=True, ws = True, t=True)
    maya_object_rotate = cmds.xform(maya_object, q=True, ws = True, ro=True)
    mirrorBehavior = False
    if auto_all:
        mirrorBehavior = get_auto_mirror_behavior(opposite_object)
        
    if standard:
        mirrorBehavior = False

    if behavior:
        mirrorBehavior = True

    if translation:
        opposite_translate = [maya_object_translate[0] *-1, maya_object_translate[1], maya_object_translate[2] ]

    if not mirrorBehavior:
        opposite_rotate, opposite_scale = standard_mirror(maya_object)
    else:
        opposite_rotate, opposite_scale = getMirroredTransform(maya_object_translate,
                                                            maya_object_rotate,
                                                            mirrorBehavior,
                                                                mirrorXY=mirrorXY,
                                                                mirrorYZ=mirrorYZ,
                                                                mirrorXZ=mirrorXZ,
                                                            
                                                            )

    # Set back to current if not rotating
    if not rotate:
        opposite_rotate=cmds.xform(opposite_object, q=True, ws = True, ro=True)

    # Set back to current if not rotating
    if not scale:
        opposite_scale=cmds.xform(opposite_object, q=True, ws = True, s=True)

    cmds.xform(opposite_object, ws=True, ro=opposite_rotate, t=opposite_translate, s=opposite_scale)

def get_auto_mirror_behavior(maya_object):
    if cmds.objExists(maya_object+".RIVET_GUIDE"):
        return False
    if cmds.objExists(maya_object+".ROTATION_GUIDE"):
        return True
    if cmds.objExists(maya_object+".TRANSLATION_GUIDE"):
        return False
    return False


def mirror_rivet(maya_object):
    opposite_object = get_opposite_side(maya_object)
    maya_object_translate = cmds.xform(maya_object, q=True, t=True, ws=True)
    maya_object_rotate = cmds.xform(maya_object, q=True, ro=True, ws=True)
    maya_object_scale = cmds.xform(maya_object, q=True, s=True,ws=True)
    opposite_translate = [maya_object_translate[0] *-1, maya_object_translate[1], maya_object_translate[2] ]

    cmds.xform(opposite_object, ws=True, t=opposite_translate)
    misc.update_all_geo_constraints(maintainOffsetT=True)


def standard_mirror(maya_object):
    opposite_object = get_opposite_side(maya_object)
    maya_object_translate = cmds.xform(maya_object, q=True, t=True, ws=True,a=True)
    maya_object_rotate = cmds.xform(maya_object, q=True, ro=True, ws=True,a=True)
    maya_object_scale = cmds.xform(maya_object, q=True, s=True, ws=True, a=True)

    dummy_parent = cmds.createNode("joint", n="dummyParent{0:02}".format(random.randint(1,10000001)))
    dummy_origin_parent = cmds.createNode("joint", n="dummy{0:02}".format(random.randint(1,10000001)), p=dummy_parent)
    # cmds.xform(dummy_origin_parent, ws=True, ro=maya_object_rotate, t=maya_object_translate, s=maya_object_scale)

    dummy_origin = cmds.createNode("joint", n="dummy_origin{0:02}".format(random.randint(1,10000001)))
    dummy_aim_target = cmds.createNode("joint", n="dummy_aim_target{0:02}".format(random.randint(1,10000001)), )
    dummy_aim_up_target = cmds.createNode("joint", n="dummy_aim_up_target{0:02}".format(random.randint(1,10000001)), )

    cmds.xform(dummy_origin, ws=True, ro=maya_object_rotate, t=maya_object_translate, s=maya_object_scale)
    cmds.xform(dummy_aim_target, ws=True, ro=maya_object_rotate, t=maya_object_translate, s=maya_object_scale)
    cmds.xform(dummy_aim_up_target, ws=True, ro=maya_object_rotate, t=maya_object_translate, s=maya_object_scale)

    cmds.move(1, dummy_aim_target, z=True, r=True, os=True)
    cmds.move(1, dummy_aim_up_target, y=True, r=True, os=True)
    
    opposite_origin = cmds.xform(dummy_origin, q=True, t=True, ws=True,a=True)
    opposite_aim = cmds.xform(dummy_aim_target, q=True, t=True, ws=True,a=True)
    opposite_aim_up = cmds.xform(dummy_aim_up_target, q=True, t=True, ws=True,a=True)
    

    cmds.xform(dummy_origin, ws=True, t= [opposite_origin[0] *-1, opposite_origin[1], opposite_origin[2] ])
    cmds.xform(dummy_aim_target, ws=True, t= [opposite_aim[0] *-1, opposite_aim[1], opposite_aim[2] ])
    cmds.xform(dummy_aim_up_target, ws=True, t= [opposite_aim_up[0] *-1, opposite_aim_up[1], opposite_aim_up[2] ])

    # opposite_origin = [opposite_origin[0] *-1, opposite_origin[1], opposite_origin[2] ]
    # opposite_aim = [opposite_aim[0] *-1, opposite_aim[1], opposite_aim[2] ]
    # opposite_aim_up = [opposite_aim_up[0] *-1, opposite_aim_up[1], opposite_aim_up[2] ]
    


    # cmds.scale(-1, dummy_parent, x=True, r=True, os=True)
    cmds.makeIdentity(dummy_parent, apply=True, t=1, r=1, s=1, n=0, pn=1);
    # cmds.xform(dummy_parent, ws=True,  s=[-1,0,0])
    cmds.aimConstraint(dummy_aim_target, dummy_origin, aimVector=[0,0,1], worldUpObject=dummy_aim_up_target, worldUpType="object")

    # return
    opposite_translate = cmds.xform(dummy_origin, q=True, t=True, ws=True)
    opposite_rotate = cmds.xform(dummy_origin, q=True, ro=True, ws=True)
    opposite_scale = cmds.xform(dummy_origin, q=True, s=True, ws=True)

    # cmds.xform(opposite_object, ws=True, t=opposite_translate, ro=opposite_rotate)
    cmds.delete( dummy_origin, dummy_aim_target, dummy_parent, dummy_aim_up_target)
    return opposite_rotate, opposite_scale

def getMirroredTransform(position,
                         rotation,
                         mirrorBehavior=True,
                         mirrorXY=True,
                         mirrorYZ=False,
                         mirrorXZ=False,
                         
                         
                         ):
    rootGrp  = cmds.createNode("transform", n="TEMP_ROOT_GRP")
    tmpRootJnt = cmds.joint(rootGrp, name = "ROOT", o=[0,0,0], p=[0,0,0])
    tmpJnt = cmds.joint(tmpRootJnt, name = "TEMPO", o=rotation, p=position)
    tmpFinal = cmds.mirrorJoint(tmpJnt,
                                mirrorBehavior=mirrorBehavior,
                                mirrorXY=mirrorXY,
                                mirrorYZ=mirrorYZ,
                                mirrorXZ=mirrorXZ,
                                sr = ["L_", "R_"])[0]
    rotate = cmds.xform(tmpFinal, q=True, ws=True, ro=True)
    scale = cmds.xform(tmpFinal, q=True, ws=True, s=True)
    cmds.delete([rootGrp, tmpRootJnt, tmpJnt, tmpFinal])
    return rotate, scale

##################################################################################################################################################
########################################################## WEIGHTS ###############################################################################
##################################################################################################################################################

def get_symmetry_dict(maya_object, retrieve_if_exists=True, retrieve_L_dict=False, retrieve_R_dict=False):
    # Creates a dictionary of the opposite point for every point in a mesh, then sets this dictionary as a string attribute on the transform of the object
    # If the attribute exists and retrieve_if_exists is True running the function will retrieve the attribute as a dictionary
    # If the mesh changes you will need to run with retrieve_if_exists false one time
    # This should only be slow the first time it is run
    if retrieve_if_exists and cmds.objExists(maya_object + ".symmetry_dict"):
        if retrieve_L_dict:
            return ast.literal_eval(str(cmds.getAttr(maya_object + ".left_dict")))
        if retrieve_R_dict:
            return ast.literal_eval(str(cmds.getAttr(maya_object + ".right_dict")))
        return ast.literal_eval(str(cmds.getAttr(maya_object + ".symmetry_dict")))
    regular_idx = []
    flipped_idx = []
    left_ids = []
    right_ids = []
    fnMesh = misc.getOMMesh(maya_object)
    points = OpenMaya.MPointArray()
    fnMesh.getPoints(points)
    dummy_point = OpenMaya.MPoint()
    for i in range(points.length()):
        l_side = True
        if points[i].x < 0.0:
            l_side = False
        
        if l_side:
            left_ids.append(i)
        else:
            right_ids.append(i)
        opposite_point = OpenMaya.MPoint(points[i].x*-1,
                                            points[i].y,
                                            points[i].z)
        util = OpenMaya.MScriptUtil()
        util.createFromInt(0)
        face_id = util.asIntPtr()
        fnMesh.getClosestPoint(opposite_point,
                                dummy_point,
                                OpenMaya.MSpace.kObject,
                                face_id)
        face_id = OpenMaya.MScriptUtil(face_id).asInt()
        point_ids = OpenMaya.MIntArray()
        fnMesh.getPolygonVertices(face_id,point_ids)
        closest_lengths = []
        for j in point_ids:
            fnMesh.getPoint(j,dummy_point)
            vector_to = OpenMaya.MVector(dummy_point.x,
                                            dummy_point.y,
                                            dummy_point.z)
            vector_from = OpenMaya.MVector(opposite_point.x,
                                            opposite_point.y,
                                            opposite_point.z)
            vector_from = vector_from - vector_to
            closest_lengths.append(vector_from.length())
        #make dictionary
        id_dict = dict(list(zip(closest_lengths,point_ids)))
        smallest_id = min(closest_lengths)
        regular_idx.append(i)
        flipped_idx.append(id_dict.get(smallest_id))
    symmetry_dict = dict(list(zip(regular_idx,flipped_idx)))
    left_dict = {i:symmetry_dict[i] for i in left_ids }
    right_dict = {i:symmetry_dict[i] for i in right_ids }
    attr_utils.get_attr(maya_object, "symmetry_dict", dataType="string")
    attr_utils.get_attr(maya_object, "left_dict", dataType="string")
    attr_utils.get_attr(maya_object, "right_dict", dataType="string")
    cmds.setAttr(maya_object + ".symmetry_dict", str(symmetry_dict), type="string")
    cmds.setAttr(maya_object + ".left_dict", str(left_dict), type="string")
    cmds.setAttr(maya_object + ".right_dict", str(right_dict), type="string")
    if retrieve_L_dict:
        return left_dict
    if retrieve_R_dict:
        return right_dict
    return symmetry_dict

def mirror_double_array_attrs_OLD(full_attr_name, geo, side="L"):
    #----vars
    weights = cmds.getAttr(full_attr_name)
    cluster = cmds.cluster(geo, name = "temporaryCluster")
    cmds.percent( cluster[0], geo, v = 0)
    cluster_weight_attr = cluster[0] + '.weightList[0].weights'
    for i in range(len(weights)):
        cmds.setAttr(cluster_weight_attr+"["+str(i)+"]", 
                        weights[i],)
    if side == "L":
        cmds.copyDeformerWeights( ss=geo, ds=geo, sd=cluster[0], 
                                    mirrorMode='YZ')
    if side == "R":
        cmds.copyDeformerWeights( ss=geo, ds=geo, sd=cluster[0], 
                                    mirrorMode='YZ', mi = True)
    mirrored_weights = cmds.getAttr(cluster_weight_attr)[0]
    cmds.setAttr(full_attr_name, mirrored_weights, typ='doubleArray')
    cmds.delete(cluster)


def mirror_double_array_attrs(full_attr_name, geo, side="L"):
    #----vars
    retrieve_side = True, False
    if side == "R":
        retrieve_side = False, True

    symmetry_dict = get_symmetry_dict(geo, retrieve_L_dict=retrieve_side[0], retrieve_R_dict=retrieve_side[1])
    weights = cmds.getAttr(full_attr_name)
    for key in list(symmetry_dict.keys()):
        weights[symmetry_dict[key]] = weights[key]
    cmds.setAttr(full_attr_name,weights, type="doubleArray")

def smart_mirror_anim_curve(maya_object, center_name="C_", left_name="L_", right_name="R_"):
    if maya_object.startswith(center_name):
        animcurve_utils.mirror_anim_curves(anim_curve=maya_object,
                           side="L",
                           flip=False)
    elif maya_object.startswith(left_name) or maya_object.startswith(right_name):
        mirror_flip_curve(maya_object, left_name=left_name, right_name=right_name)

def get_opposite_side(maya_object, left_name = "L_", right_name = "R_"):
    if left_name in maya_object:
        return maya_object.replace(left_name, right_name,1)
    elif right_name in maya_object:
        return maya_object.replace(right_name, left_name,1)

def mirror_flip_curve(maya_object, left_name="L_", right_name="R_"):
    side = get_mirror_side_name(maya_object, left_name=left_name, right_name=right_name)
    if side=="C":
        return
    opposite_curve = get_opposite_side(maya_object, left_name = left_name, right_name = right_name)
    if not opposite_curve:
        return
    animcurve_utils.copy_flip_anim_curves(side=side,
                          source = maya_object,
                          target = opposite_curve,
                          flip=True)

def get_opposite_mirror_side(maya_object, center_name="C_", left_name="L_", right_name="R_"):
    if maya_object.startswith(center_name):
        return
    if maya_object.startswith(left_name):
        return "R"
    if maya_object.startswith(right_name):
        return "L"

def get_mirror_side_name(maya_object, center_name="C_", left_name="L_", right_name="R_"):
    if maya_object.startswith(center_name):
        return "C"
    if maya_object.startswith(left_name):
        return "L"
    if maya_object.startswith(right_name):
        return "R"

def copy_double_array_weights(
                              source_attr,
                              target_attr,
                              invert = False,
                              geo=None,
                              flip = False):
        weights = cmds.getAttr(source_attr)
        if invert == True:
            for i in range(len(weights)):
                weights[i] = weights[i] * -1
        if flip == True:
            symmetry_dict = get_symmetry_dict(geo)
            flip_weights = list(weights)
            if symmetry_dict:
                for i in range(len(flip_weights)):
                    try:
                        flip_weights[i] = weights[symmetry_dict.get(i)]
                    except:
                        pass
                weights =  flip_weights
        if type(target_attr) != list:
            target_attr = [target_attr]
        for i in range(len(target_attr)):
            cmds.setAttr(target_attr[i], weights, typ='doubleArray')

def smart_mirror_hand_weights(geo, weight_attr, center_mirror_side="L", symmetric_sides=False, center_name="C_", left_name="L_", right_name="R_"):
    simple_attr_name = weight_attr.split(".")[1]
    if simple_attr_name.startswith(center_name) or (not simple_attr_name.startswith(left_name) and not simple_attr_name.startswith(right_name)) :
        mirror_double_array_attrs(weight_attr, geo, side=center_mirror_side)

    elif simple_attr_name.startswith(left_name) or simple_attr_name.startswith(right_name):
        side = get_mirror_side_name(weight_attr, left_name=left_name, right_name=right_name)
        if symmetric_sides:
            mirror_double_array_attrs(weight_attr, geo, side=center_mirror_side)

            return
        target_attr = get_opposite_side(simple_attr_name)
        if not target_attr:

            return
        target_attr = geo + "." + target_attr
        copy_double_array_weights(source_attr=weight_attr,
                                  target_attr=target_attr,
                                  geo=geo,
                                  flip = True)

def mirror_all_geo_weights(mesh, side_to_mirror="L", center_name="C_", left_name="L_", right_name="R_"):
    all_attrs = cmds.listAttr(mesh, userDefined=True, a=True)
    if not all_attrs:
        return
    sorted_attrs = []
    for attr in all_attrs:
        full_attr_name = mesh + "." + attr
        attr_type = cmds.addAttr(full_attr_name, q=True, dt=True)[0]
        if attr_type != "doubleArray":
            continue
        smart_mirror_single_attr(mesh=mesh, attr=attr, side_to_mirror=side_to_mirror, center_name=center_name, left_name=left_name, right_name=right_name)

def smart_mirror_single_attr(mesh, attr, side_to_mirror="L", center_name="C_", left_name="L_", right_name="R_"):
    mesh_transform = misc.getParent(mesh)
    side = get_mirror_side_name(attr)
    if side == "C" or not side:
        mirror_double_array_attrs(mesh_transform + "." + attr, mesh_transform, side=side_to_mirror)
    if side != side_to_mirror:
        return
    side = get_mirror_side_name(attr, left_name=left_name, right_name=right_name)
    target_attr = get_opposite_side(attr)
    if not target_attr:
        return
    target_attr = mesh_transform + "." + target_attr
    copy_double_array_weights(source_attr=mesh_transform + "." + attr,
                            target_attr=target_attr,
                            geo=mesh_transform,
                            flip = True)

def add_dynamic_mirror_connection(maya_objects=None, hide_connected=True, translate=True, rotate=True, scale=True):
    if not maya_objects: maya_objects = cmds.ls(sl=True)
    for maya_object in maya_objects:
        # In case it already exists
        remove_dynamic_mirror_connection(maya_objects=[maya_object])
        dynamic_mirror_connection(maya_object, hide_connected=hide_connected, translate=translate, rotate=rotate, scale=scale)
        

def dynamic_mirror_connection(maya_object, hide_connected=True, translate=True, rotate=True, scale=True):
    # Finds the opposite side and makes a mirror connection (IN OBJECT SPACE) should do a global version option...
    opposite_object = get_opposite_side(maya_object)
    if not opposite_object:
        return
    if hide_connected:
        cmds.setAttr(opposite_object + ".v", 0)
    
    if translate:
        translate = cmds.createNode("multiplyDivide", n=maya_object+"OppositeTranslate_MTD")
        cmds.setAttr(translate + ".input2X", -1)
        cmds.connectAttr(maya_object + ".translate",  translate + ".input1")
        cmds.connectAttr(translate + ".output",  opposite_object + ".translate")
        
    if rotate:
        rotate = cmds.createNode("multiplyDivide", n=maya_object+"OppositeRotate_MTD")
        cmds.setAttr(rotate + ".input2Y", -1)
        cmds.setAttr(rotate + ".input2Z", -1)
        cmds.connectAttr(maya_object + ".rotate",  rotate + ".input1")
        cmds.connectAttr(rotate + ".output",  opposite_object + ".rotate")

    if scale:
        scale = cmds.createNode("multiplyDivide", n=maya_object+"OppositeScale_MTD")
        cmds.setAttr(scale + ".input2X", 1)
        cmds.connectAttr(maya_object + ".scale",  scale + ".input1")
        cmds.connectAttr(scale + ".output",  opposite_object + ".scale")

    # Tag for easy removal
    for node in [maya_object, opposite_object]:
        if translate:
            message_utils.create_message_attr_setup(node, "opposite_translate", translate, "control" )
        if rotate:
            message_utils.create_message_attr_setup(node, "opposite_rotate", rotate, "control" )
        if scale:
            message_utils.create_message_attr_setup(node, "opposite_scale", scale, "control" )
    tag_utils.tag_dynamic_mirrored(opposite_object)
    
def remove_dynamic_mirror_connection(maya_objects=None, unhide=True):
    if not maya_objects: maya_objects = cmds.ls(sl=True)
    for node in maya_objects:
        opposite_object = get_opposite_side(node)
        if not opposite_object:
            continue
        for side_node in [opposite_object, node]:
            if cmds.objExists(node + ".opposite_translate"):
                translate = message_utils.get_node_from_message(side_node + ".opposite_translate", from_output = True, get_single=True)
                cmds.delete(translate)
                cmds.deleteAttr(side_node + ".opposite_translate")
            if cmds.objExists(node + ".opposite_translate"):
                rotate = message_utils.get_node_from_message(side_node + ".opposite_rotate", from_output = True, get_single=True)
                cmds.delete(rotate)
                cmds.deleteAttr(side_node + ".opposite_rotate")
            if cmds.objExists(node + ".opposite_scale"):
                scale = message_utils.get_node_from_message(side_node + ".opposite_scale", from_output = True, get_single=True)
                cmds.delete(scale)
                cmds.deleteAttr(side_node + ".opposite_scale")
            if unhide:
                cmds.setAttr(side_node + ".v", 1)
            if cmds.objExists(side_node + ".DYNAMIC_MIRRORED"):
                cmds.deleteAttr(side_node + ".DYNAMIC_MIRRORED")

    