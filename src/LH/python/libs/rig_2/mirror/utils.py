import random
from rig.utils import misc
from maya import cmds

def get_opposite_side(maya_object, l_side_name = "L_", r_side_name = "R_"):
    if not l_side_name and not r_side_name in maya_object:
        return
    if l_side_name in maya_object:
        return maya_object.replace(l_side_name, r_side_name)
    elif r_side_name in maya_object:
        return maya_object.replace(r_side_name, l_side_name)
    return


def mirrorSelectedLocatorLToR(ctrls=None):
    if not ctrls:
        ctrls = cmds.ls(sl=True, typ="transform")
    for ctrl in ctrls:
        mirrorSelectedLocatorLToRSingle(ctrl=ctrl)


# def mirrorSelectedLocatorLToRSingle(ctrl=None):
#     locator = cmds.listConnections(ctrl + ".rotate")
#     if not locator:
#         return
#     lParent = cmds.listRelatives(locator, p=True)[0]
#     if not "L_" in lParent:
#         return
#     rParent = lParent.replace("L_", "R_")
#     if not cmds.objExists(rParent):
#         return
#     lParentTranslate = cmds.xform(lParent, q=True, ws = True, t=True)
#     rParentTranslate = [lParentTranslate[0] *-1, lParentTranslate[1], lParentTranslate[2] ]
#     lParentRotate = cmds.xform(lParent, q=True, ws = True, ro=True)
#     rParentRotate,rParentScale = getMirroredTransform(lParentTranslate, lParentRotate)
#     cmds.xform(rParent, ws=True, ro=rParentRotate, t=rParentTranslate, s=rParentScale)

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
        opposite_rotate, opposite_scale = standard_mirror_new(maya_object)
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
    maya_object_translate = cmds.xform(maya_object, q=True, t=True, ws=True)
    maya_object_rotate = cmds.xform(maya_object, q=True, ro=True, ws=True)
    maya_object_scale = cmds.xform(maya_object, q=True, s=True,ws=True)

    dummy_parent = cmds.createNode("transform", n="dummyParent{0:02}".format(random.randint(1,10000001)))
    dummy = cmds.createNode("transform", n="dummy{0:02}".format(random.randint(1,10000001)), p=dummy_parent)
    cmds.xform(dummy, ws=True, ro=maya_object_rotate, t=maya_object_translate, s=maya_object_scale)
    cmds.xform(dummy_parent, ws=True,  s=[-1,0,0])

    opposite_translate = cmds.xform(dummy, q=True, t=True, ws=True)
    opposite_rotate = cmds.xform(dummy, q=True, ro=True, ws=True)
    opposite_scale = cmds.xform(dummy, q=True, s=True, ws=True)

    # cmds.xform(opposite_object, ws=True, t=opposite_translate, ro=opposite_rotate)
    cmds.delete(dummy, dummy_parent)
    return opposite_rotate, opposite_scale


def standard_mirror_new(maya_object):
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


def mirror_rivet_new(maya_object):
    opposite_object = get_opposite_side(maya_object)
    maya_object_translate = cmds.xform(maya_object, q=True, t=True, ws=True)
    maya_object_rotate = cmds.xform(maya_object, q=True, ro=True, ws=True)
    maya_object_scale = cmds.xform(maya_object, q=True, s=True,ws=True)

    dummy_parent = cmds.createNode("transform", n="dummyParent{0:02}".format(random.randint(1,10000001)))
    dummy = cmds.createNode("transform", n="dummy{0:02}".format(random.randint(1,10000001)), p=dummy_parent)
    cmds.xform(dummy, ws=True, ro=maya_object_rotate, t=maya_object_translate, s=maya_object_scale)
    cmds.xform(dummy_parent, ws=True,  s=[-1,0,0])

    opposite_translate = cmds.xform(dummy, q=True, t=True, ws=True)
    opposite_rotate = cmds.xform(dummy, q=True, ro=True, ws=True)

    cmds.xform(opposite_object, ws=True, t=opposite_translate, ro=opposite_rotate)
    cmds.delete(dummy, dummy_parent)
    


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