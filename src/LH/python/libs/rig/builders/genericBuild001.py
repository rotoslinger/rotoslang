########### FOR DEBUG PURPOSES #####################
# #---paths
mac_file = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig/scenes/insomniac_body_test.ma"
linux_file = '/scratch/levih/dev/rotoslang/src/scenes/bodyJnts.ma'
scene_path = linux_file
weights_path = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig/insomniacWeights"
 
import sys
import importlib
linux = '/corp/projects/eng/lharrison/workspace/levi_harrison_test'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"
#---determine operating system
os = sys.platform

if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

import maya.cmds as cmds
from rig.utils import misc, weights

from rig.bodycmds import arm, leg, foot, finger, neck, head, eye, main, shoulder, torso, holster, rivet
importlib.reload(arm)
importlib.reload(leg)
importlib.reload(foot)
importlib.reload(finger)
importlib.reload(neck)
importlib.reload(head)
importlib.reload(eye)
importlib.reload(main)
importlib.reload(shoulder)
importlib.reload(torso)
importlib.reload(holster)
importlib.reload(misc)
importlib.reload(weights)
importlib.reload(rivet)

# build insomniac test
def build_it(scene_path = "", weights_path = "", debug = False, radius=1.0, geo=None, cape=True, hair=False):

    if scene_path:
        cmds.file(
                  f=True ,
                  new = True)
        cmds.file(scene_path, 
                  f=True ,
                  i = True,
                  options="v=0;",  
                  typ = "mayaAscii")

    misc.create_rig_hier()

    global_ctl = main.create_global_ctl(side = "C", 
                                        skel_parent = "C_skeleton_GRP", 
                                        rig_parent = "C_rig_GRP", 
                                        ctl_sizes = [4.0,3.0], 
                                        debug = debug )

    global_hook = global_ctl.ctl_gimbals[1]

    torso_hook = torso.create_torso(side = "C",
                                    name = "torso",
                                    root_joint = 'root_bind',
                                    torso_joints = ["spinea_bind",
                                                    "spineb_bind",
                                                    "spinec_bind",
                                                    "spined_bind"],
                                    hip_joint = 'pelvis_bind',
                                    driver = global_hook,
                                    global_scale = global_hook,
                                    skel_parent = "C_skeleton_GRP",
                                    rig_parent = "C_rig_GRP",
                                    fwd_ctl_sizes   = [2.5, 
                                                       1.6, 
                                                       1.6,
                                                       2.0, 
                                                       2.3,
                                                       1.5, 
                                                       ],
                                    rev_ctl_sizes   = [2.0, 
                                                       2.0, 
                                                       2.0,
                                                       2.0, 
                                                       3.0,
                                                       2.0, 
                                                       ],
                                    ctl_orients = [[0,0,0],
                                                   [0,0,0],
                                                   [0,0,0],
                                                   [0,0,0],
                                                   [0,0,0],
                                                   [0,0,0]],
                                    ctl_offsets = [[0,-.03,0],
                                                   [0,-.03,0],
                                                   [0,-.03,0],
                                                   [0,-.03,0],
                                                   [0,-.03,0],
                                                   [1.0,-.03,0],
                                                   ],
                                    switch_size = 3,
                                    switch_offset = [0,-.12,.05],
                                    switch_orient = [0,0,0],
                                    debug = debug)

    neck_hook = neck.create_neck( joint = "neck_bind", 
                                  driver = torso_hook.chest_anchor, 
                                  global_scale = global_hook,
                                  ctl_size = 1.0,
                                  orient = [0,0,-20],
                                  offset = [.3,0,0],
                                  debug = debug)
    
    head_hook = head.create_head( joint = "head_bind", 
                                  driver = neck_hook.skel_joint, 
                                  global_scale = global_hook,
                                  ctl_size = .8,
                                  orient = [0,0,-20],
                                  offset = [-.3,0,0],
                                  debug = debug)

    l_eye_hook = eye.create_eye( joints = ["l_eye_bind", "r_eye_bind"], 
                                 jointEnds = ["l_eyeEnd_bind", "r_eyeEnd_bind"], 
                                 sides=["L","R"],
                                  driver = head_hook.skel_joint, 
                                #   upVecDriver = head_hook.skel_joint, 
                                  global_scale = global_hook,
                                  ctl_size = .3,
                                  master_size = 1,
                                  orient = [0,90,0],
                                  offset = [0,0,0],
                                  space_names = ["world", "head"],
                                  space_parents= [global_ctl.ctl_gimbals[0], head_hook.skel_joint],
                                  debug = debug)

    l_shoulder = shoulder.create_shoulder(side = "L", 
                                          name = "shoulder",
                                          joint = "l_clavicle_bind", 
                                          driver = torso_hook.chest_anchor, 
                                          global_scale = global_hook, 
                                          ctl_size = 2.5, 
                                          orient = [0,0,0], 
                                          offset = [1.0,.7,-1.0], 
                                          debug = debug, 
                                          helper_chains = ["l_neckClav_bind",
                                                           "l_pec_bind",
                                                           "l_scapula_bind",
                                                           "l_clav_bind"],
                                          helper_names = ["neckClav",
                                                          "pec",
                                                          "scapula",
                                                          "clav"])

    r_shoulder = shoulder.create_shoulder(side = "R", 
                                          name = "shoulder",
                                          joint = "r_clavicle_bind", 
                                          driver = torso_hook.chest_anchor, 
                                          global_scale = global_hook, 
                                          ctl_size = 2.5, 
                                          orient = [0,0,0], 
                                          offset = [1.0,-.7,1.0], 
                                          debug = debug, 
                                          helper_chains = ["r_neckClav_bind",
                                                           "r_pec_bind",
                                                           "r_scapula_bind",
                                                           "r_clav_bind"],
                                          helper_names = ["neckClav",
                                                          "pec",
                                                          "scapula",
                                                          "clav"])

    l_arm = arm.create_arm(joints = ['l_shoulder_bind', 'l_elbow_bind', 'l_wrist_bind'], 
                           side = "L",
                           arm_splits = 4,
                           twist_axis="z",
                           elbow_splits = 6,
                           fk_ctl_size = [1.2,.8,.8],
                           ik_ctl_size = [1.0,.3,.5],
                           driver = l_shoulder.skel_joint,
                           debug = debug,
                           ik_space_names = ["world", "shoulder", "neck", "hip"],
                           ik_space_parents =  [global_hook, 
                                                l_shoulder.skel_joint,
                                                neck_hook.skel_joint,
                                                torso_hook.fwd_ctls[len(torso_hook.fwd_ctls)-1] ],
                           switch_ctl_size = .3,
                           switch_offset = 1.5,
                           global_scale= global_ctl.ctls[0])

    r_arm = arm.create_arm(joints = ['r_shoulder_bind', 'r_elbow_bind', 'r_wrist_bind'], 
                           side = "R",
                           arm_splits = 4,
                           elbow_splits = 6,
                           fk_ctl_size = [1.2,.8,.8],
                           ik_ctl_size = [1.0,.3,.5],
                           driver = r_shoulder.skel_joint,
                           debug = debug,
                           ik_space_names = ["world", "shoulder", "neck", "hip"],
                           ik_space_parents =  [global_hook, 
                                                r_shoulder.skel_joint,
                                                neck_hook.skel_joint,
                                                torso_hook.fwd_ctls[len(torso_hook.fwd_ctls)-1] ],
                           switch_ctl_size = .3,
                           switch_offset = 1.5,
                           global_scale= global_hook)

    finger.create_finger(side = "L", 
                         joint_roots = ["l_thumba_bind",
                                        "l_indexa_bind",
                                        "l_middlea_bind",
                                        "l_ringa_bind",
                                        "l_pinkya_bind"], 
                         driver = l_arm.bind_jnts[3],
                         ctl_size = [
                                     [.4,.3,.2],
                                     [.2,.15,.15,],
                                     [.2,.15,.15,],
                                     [.2,.15,.15,],
                                     [.3,2,.15,.15],
                                     ],
                         global_scale= global_hook)
            
    finger.create_finger(side = "R", 
                         joint_roots = ["r_thumba_bind",
                                        "r_indexa_bind",
                                        "r_middlea_bind",
                                        "r_ringa_bind",
                                        "r_pinkya_bind"], 
                         driver = r_arm.bind_jnts[3],
                         ctl_size = [
                                     [.4,.3,.2],
                                     [.2,.15,.15,],
                                     [.2,.15,.15,],
                                     [.2,.15,.15,],
                                     [.3,2,.15,.15],
                                     ],
                         global_scale= global_hook)
    if cape:
        finger.create_finger(side = "C",
                            names = ["cape1"
                                ],

                            joint_roots = ["cape1",
                                        ], 
                            driver = torso_hook.chest_anchor,
                            ctl_size = [
                                        [.4,.3,.2],
                                        [.4,.3,.2],
                                        [.4,.3,.2],
                                        [.4,.3,.2],
                                        [.4,.3,.2],
                                        [.4,.3,.2],
                                        [.4,.3,.2],
                                        ],
                            global_scale= global_hook,
                            infinite_digits=True,
                            debug = debug,
                            worldAlign=True)
    if hair:
        finger.create_finger(side = "C",
                            names = ["hair1"],
                            joint_roots = ["hair1",
                                        ], 
                            driver = head_hook.skel_joint,
                            ctl_size = [
                                        [.4,.3,.2],
                                        [.4,.3,.2],
                                        [.4,.3,.2],
                                        [.4,.3,.2],
                                        [.4,.3,.2]
                                        ],
                            global_scale= global_hook,
                            infinite_digits=True,
                            debug = debug,
                            ignore_end_joints = False,

                            worldAlign=True)


    l_leg = leg.create_leg(joints = ['l_leg_bind', 'l_knee_bind', 'l_ankle_bind'], 
                           side = "L",
                           leg_splits = 4,
                           twist_axis="z",
                           knee_splits = 6,
                           fk_ctl_size = [1.0,.9,.8],
                           ik_ctl_size = [1.0,.3,.5],
                           ik_ctl_scale = [.33,.1,.1],
                           ik_ctl_offset = [.03,0,-.06],
                           driver = torso_hook.hip_joint,
                           debug = debug,
                           ik_space_names = ["world", "hip"],
                           ik_space_parents =  [global_hook, 
                                                torso_hook.fwd_ctls[0] ],
                           switch_ctl_size = .3,
                           switch_offset = 1.5,
                           global_scale= global_ctl.ctls[0])
    
    r_leg = leg.create_leg(joints = ['r_leg_bind', 'r_knee_bind', 'r_ankle_bind'], 
                           side = "R",
                           leg_splits = 4,
                           twist_axis="z",
                           knee_splits = 6,
                           fk_ctl_size = [1.0,.9,.8],
                           ik_ctl_size = [1.0,.3,.5],
                           ik_ctl_scale = [.33,.1,.1],
                           ik_ctl_offset = [.03,0,-.06],
                           driver = torso_hook.hip_joint,
                           debug = debug,
                           ik_space_names = ["world", "hip"],
                           ik_space_parents =  [global_hook, 
                                                torso_hook.fwd_ctls[0] ],
                           switch_ctl_size = .3,
                           switch_offset = 1.5,
                           global_scale= global_ctl.ctls[0])
    l_foot = foot.create_foot(driver = l_leg.bind_jnts[3],
                              side = "L",
                              global_scale = global_hook,
                              toe_joint = "l_toe_bind",
                              tip_joint = "l_toeTipFront_bind",
                              left_joint = "l_toeTipLeft_bind",
                              right_joint = "l_toeTipRight_bind",
                              heel_joint = "l_toeTipBack_bind",
                              toe_end_joint = "l_toe_bind_end",
                              ankle_joint = "l_ankle_bind",
                              ik_control = l_leg.ik_ctls[0],
                              ik_switch = l_leg.ik_fk_switch,
                              ik_root = l_leg.ik_jnts[3],
                              foot_groups = l_leg.gimbal_buffers,
                              fk_ctl_size = 1.0,
                              orient = [0,0,0],
                              offset = [.009,0,0],
                              debug = debug)
    
    r_foot = foot.create_foot(driver = r_leg.bind_jnts[3],
                              side = "R",
                              global_scale = global_hook,
                              toe_joint = "r_toe_bind",
                              tip_joint = "r_toeTipFront_bind",
                              left_joint = "r_toeTipLeft_bind",
                              right_joint = "r_toeTipRight_bind",
                              heel_joint = "r_toeTipBack_bind",
                              toe_end_joint = "r_toe_bind_end",
                              ankle_joint = "r_ankle_bind",
                              ik_control = r_leg.ik_ctls[0],
                              ik_switch = r_leg.ik_fk_switch,
                              ik_root = r_leg.ik_jnts[3],
                              foot_groups = r_leg.gimbal_buffers,
                              fk_ctl_size = 1.0,
                              orient = [0,0,0],
                              offset = [.009,0,0],
                              debug = debug)

#     
#     rivet_hook = rivet.create_rivet_rig(joints = [
#                                          "L_legDetail_bind",
#                                          "L_waistPouch_bind",
#                                          "R_waistPouch_bind",
#                                          "R_legHolster_bind",
#                                          ],
# 
#                        num_buffer = 1,
#                        rig_parent = "C_rig_GRP", 
#                        skel_parent = "C_skeleton_GRP",
#                        sizes = [
#                                 3,
#                                 3,
#                                 3,
#                                 3
#                                 ],
#                        global_scale = global_hook,
#                        debug = debug)
    misc.create_bind_skel(parents = ["L_hand_JNT_FIX",
                                     "L_hand_JNT_FIX",
                                     "L_hand_JNT_FIX",
                                     "L_hand_JNT_FIX",
                                     "L_hand_JNT_FIX",
                                     "L_arm5_JNT_FIX",
                                     "L_shoulder_JNT_FIX",
                                     "C_chest_JNT_FIX",
                                     "C_torso3_JNT_FIX",
                                     "C_chest_JNT_FIX",
                                     "C_chest_JNT_FIX",
                                     "C_torso3_JNT_FIX",
                                     "C_torso3_JNT_FIX",
                                     "C_chest_JNT_FIX",
                                     "C_chest_JNT_FIX",
                                     "C_chest_JNT_FIX",
                                     "R_hand_JNT_FIX",
                                     "R_hand_JNT_FIX",
                                     "R_hand_JNT_FIX",
                                     "R_hand_JNT_FIX",
                                     "R_hand_JNT_FIX",
                                     "R_arm5_JNT_FIX",
                                     "R_shoulder_JNT_FIX",
                                     "C_chest_JNT_FIX",
                                     "C_torso3_JNT_FIX",
                                     "C_hip_JNT_FIX",
                                     "L_leg5_JNT_FIX",
                                     "L_toe_JNT_FIX",
                                     "C_hip_JNT_FIX",
                                     "R_leg5_JNT_FIX",
                                     "R_toe_JNT_FIX",
                                     "C_neck_JNT_FIX"
                                     ],
                          children = ["L_thumb3_JNT_FIX",
                                     "L_index3_JNT_FIX",
                                     "L_middle3_JNT_FIX",
                                     "L_ring3_JNT_FIX",
                                     "L_pinkyMetacarpal0_JNT_FIX",
                                     "L_elbow1_JNT_FIX",
                                     "L_arm_JNT_FIX",
                                     "L_shoulder_JNT_FIX",
                                     "L_clav0_JNT_FIX",
                                     "L_scapula0_JNT_FIX",
                                     "L_pec0_JNT_FIX",
                                     "R_scapula0_JNT_FIX",
                                     "R_pec0_JNT_FIX",
                                     "C_neck_JNT_FIX",
                                     "L_neckClav0_JNT_FIX",
                                     "R_neckClav0_JNT_FIX",
                                     "R_thumb3_JNT_FIX",
                                     "R_index3_JNT_FIX",
                                     "R_middle3_JNT_FIX",
                                     "R_ring3_JNT_FIX",
                                     "R_pinkyMetacarpal0_JNT_FIX",
                                     "R_elbow1_JNT_FIX",
                                     "R_arm_JNT_FIX",
                                     "R_shoulder_JNT_FIX",
                                     "R_clav0_JNT_FIX",
                                     "L_leg_JNT_FIX",
                                     "L_knee1_JNT_FIX",
                                     "L_foot_JNT_FIX",
                                     "R_leg_JNT_FIX",
                                     "R_knee1_JNT_FIX",
                                     "R_foot_JNT_FIX",
                                     "C_head_JNT_FIX"
                                     ])

    misc.non_bind_jnt_invis()
    misc.skin_jnt_vis()
#     misc.sec_bind_jnt_vis()
#     misc.select_bind_jnts()
    if weights_path:
        #---weights
        #---bind BIND jnts
        geo_list = ["L_InsomniacRigTest_GEO",
                    "C_headProxy_GEO",
                    "L_footProxy_GEO",
                    "C_pantsProxy_GEO",
                    "C_torsoProxy_GEO",
                    "R_bootProxy_GEO"]
        #get all rivets
#         for i in range(len(rivet_hook.geo)):
#             geo_list.append(rivet_hook.geo[i][0])
            
        weights.skin_to_weight_jnts(geo_list, max_influences = 4)
        #"L_InsomniacRigTest_GEO",
        #---bind SEC_BIND jnts
        #weights.skin_to_bind_sec_jnts(["C_holster_GEO"])
        #import weights
        weights.import_skins(weights_path)
        
        
        
    #OVERRIDES
    cmds.setAttr("L_armIkFkSwitch_CTL.ik_fk_switch", 1)
    cmds.setAttr("R_armIkFkSwitch_CTL.ik_fk_switch", 1)
    if cmds.objExists("C_torsoSwitch_CTL"):
        misc.lock_attrs(node="C_torsoSwitch_CTL",
                        attr=["v"],
                        unhide = False,
                        l = False,
                        k = False,
                        cb = False)
        cmds.setAttr("C_torsoSwitch_CTL.v",0)
        misc.lock_attrs(node="C_torsoSwitch_CTL",
                        attr=["v"],
                        unhide = False,
                        l = True,
                        k = False,
                        cb = False)
        
        
        
    #character fixes
    if debug == False:
        """"""
#---lock After for Leg
        #OVERRIDES
        cmds.setAttr("C_bindSkeleton_GRP.visibility", 0)
        misc.lock_all(hierarchy = l_leg.rig_parent,
                      filter = ["*_CTL", "*_JNT"])
        misc.lock_all(hierarchy = r_leg.rig_parent,
                      filter = ["*_CTL", "*_JNT"])
        misc.cleanup_skel()
    misc.set_global_jnt_radius(radius)
    # Rename cape metacarples.....
    if cape:
        for i in cmds.ls(typ="transform"):
            if "Metacarpal" in i and "cape" in i:
                cmds.rename(i, i.replace("Metacarpal", ""))
    for i in cmds.ls(typ="nurbsCurve"):
        parent = cmds.listRelatives(i, p=True)[0]
        cmds.rename(i, parent + "SHAPE")
    
    for ctrl in ["L_fingerRig_GRP", "R_fingerRig_GRP"]:
        cmds.setAttr(ctrl + ".v", lock = False)
        cmds.setAttr(ctrl + ".v", 0)
        cmds.setAttr(ctrl + ".v", lock = True)

    shape = cmds.listRelatives("C_rootFwd0_CTL", s=True)[0]
    cmds.setAttr(shape + ".v", lock = False)
    cmds.setAttr(shape + ".v", 0)
    cmds.setAttr(shape + ".v", lock = True)
    cmds.delete("group1")
    if geo:
        cmds.parent(geo, "C_geo_GRP")
    # for i in cmds.ls(typ="joint"):
    #     cmds.setAttr(i+".drawStyle", "bone")

######################################
#---Example
# build_it(scene_path = scene_path, 
#          weights_path = False,
#          debug = False,
#          radius=.1)
#########################################