########### FOR DEBUG PURPOSES #####################
# #---paths
mac_file = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig/scenes/nd_body_test.ma"
linux_file = '/corp/projects/eng/lharrison/workspace/levi_harrison_test/lhrig/scenes/nd_body_test.ma'
scene_path = linux_file
weights_path = "/corp/projects/eng/lharrison/workspace/levi_harrison_test/lhrig/weights"
 
import sys
import importlib
linux = '/corp/projects/eng/lharrison/workspace/levi_harrison_test'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
sys.path.append(os)

import maya.cmds as cmds
from utils import misc, weights

from bodycmds import arm, finger, neck, main, shoulder, torso, holster
importlib.reload(arm)
importlib.reload(finger)
importlib.reload(neck)
importlib.reload(main)
importlib.reload(shoulder)
importlib.reload(torso)
importlib.reload(holster)
importlib.reload(misc)
importlib.reload(weights)

# build naughty dog test
def build_it(scene_path = "", weights_path = "", debug = False):

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
                                        ctl_sizes = [.4,.3], 
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
                                    fwd_ctl_sizes   = [.3, 
                                                       .2, 
                                                       .2,
                                                       .2, 
                                                       .23,
                                                       .2, 
                                                       ],
                                    rev_ctl_sizes   = [.2, 
                                                       .2, 
                                                       .2,
                                                       .2, 
                                                       .3,
                                                       .2, 
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
                                                   [.05,-.03,0],
                                                   ],
                                    switch_size = .03,
                                    switch_offset = [0.4,-.12,.05],
                                    switch_orient = [0,0,0],
                                    debug = debug)

    neck_hook = neck.create_neck( joint = "neck_bind", 
                                  driver = torso_hook.chest_anchor, 
                                  global_scale = global_hook,
                                  ctl_size = 0.1,
                                  orient = [0,0,0],
                                  offset = [.09,0,0],
                                  debug = debug)

    l_shoulder = shoulder.create_shoulder(side = "L", 
                                          name = "shoulder",
                                          joint = "l_clavicle_bind", 
                                          driver = torso_hook.chest_anchor, 
                                          global_scale = global_hook, 
                                          ctl_size = 0.25, 
                                          orient = [0,0,0], 
                                          offset = [.15,.05,0], 
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
                                          ctl_size = 0.25, 
                                          orient = [0,0,0], 
                                          offset = [.15,-.05,0], 
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
                           fk_ctl_size = [.1,.08,.05],
                           ik_ctl_size = [.1,.03,.05],
                           driver = l_shoulder.skel_joint,
                           debug = debug,
                           ik_space_names = ["world", "shoulder", "neck", "hip"],
                           ik_space_parents =  [global_hook, 
                                                l_shoulder.skel_joint,
                                                neck_hook.skel_joint,
                                                torso_hook.fwd_ctls[len(torso_hook.fwd_ctls)-1] ],
                           switch_ctl_size = .01,
                           global_scale= global_ctl.ctls[0])

    r_arm = arm.create_arm(joints = ['r_shoulder_bind', 'r_elbow_bind', 'r_wrist_bind'], 
                           side = "R",
                           arm_splits = 4,
                           elbow_splits = 6,
                           fk_ctl_size = [.1,.08,.05],
                           ik_ctl_size = [.1,.03,.05],
                           driver = r_shoulder.skel_joint,
                           debug = debug,
                           ik_space_names = ["world", "shoulder", "neck", "hip"],
                           ik_space_parents =  [global_hook, 
                                                r_shoulder.skel_joint,
                                                neck_hook.skel_joint,
                                                torso_hook.fwd_ctls[len(torso_hook.fwd_ctls)-1] ],
                           switch_ctl_size = .01,
                           global_scale= global_hook)

    finger.create_finger(side = "L", 
                         joint_roots = ["l_thumba_bind",
                                        "l_indexa_bind",
                                        "l_middlea_bind",
                                        "l_ringa_bind",
                                        "l_pinkya_bind"], 
                         driver = l_arm.bind_jnts[3],
                         ctl_size = [
                                     [.03,.015,.015,],
                                     [.015,.015,.015,],
                                     [.015,.015,.015,],
                                     [.015,.015,.015,],
                                     [.03,.015,.015,.015],
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
                                     [.03,.015,.015,],
                                     [.015,.015,.015,],
                                     [.015,.015,.015,],
                                     [.015,.015,.015,],
                                     [.03,.015,.015,.015],
                                     ],
                         global_scale= global_hook)
    holster.create_holster_rig(sides = ["L",
                                "L",
                                "L",
                                "L",
                                "L",
                                "L",
                                "L",
                                "L",
                                "R",
                                "R",
                                "R",
                                "R",
                                "R",
                                "R",
                                "R",
                                ],
                       names = ["holster00",
                                "holster01",
                                "holster02",
                                "holster03",
                                "holster04",
                                "holster05",
                                "holster06",
                                "holster07",
                                "holster00",
                                "holster01",
                                "holster02",
                                "holster03",
                                "holster04",
                                "holster05",
                                "holster06",
                                ],
                                   translates = 
                                                 [(0.1313270249253715, 1.6098569303159314, -0.02813489531987654),
                                                  (0.14, 1.506, 0.097),
                                                  (0.13409266136991232, 1.5651956572799437, 0.048120271819026596),
                                                  (0.1563488186795067, 1.424705478048368, 0.14144159407821502),
                                                  (0.161533587466745, 1.3222108327840236, 0.12123224127311401),
                                                  (0.1667324004869268, 1.2595835827641961, 0.06587997523310443),
                                                  (0.17475892963137424, 1.3025144420626977, -0.0360815166822235),
                                                  (0.14290106585483067, 1.3542886454225695, -0.10979204452586305),
                                                  (-0.14562168650705645, 1.6010200287052339, -0.01830808656249229),
                                                  (-0.15605226759861715, 1.5409002288771294, 0.06625131171697192),
                                                  (-0.15692697413429135, 1.472602467114102, 0.11589728236753087),
                                                  (-0.1611171595311557, 1.390719781177317, 0.1346412117504242),
                                                  (-0.17867639198343707, 1.3113051279917358, 0.0835579936895649),
                                                  (-0.1790211679698359, 1.2988929019660467, -0.018987057887781808),
                                                  (-0.14283015200318144, 1.3462662176289693, -0.11644940939386697)]
                                                ,
                                   rotates = [(7.055976579276731, -85.53750609987287, -25.28291822061637),
                                               (104.725, 36.104, -259.825),
                                               (102.37955373368112, 36.86851315713348, -263.7682855104076),
                                               (69.57866053187405, -13.783259161522004, -79.55891018511898),
                                               (31.09498808271084, 22.713667499434465, -93.16871734732928),
                                               (-160.4423371925702, -191.13447626324273, 90.6875015390029),
                                               (-42.79088758849713, -61.93827329651057, -71.4659049948741),
                                               (100.77088001375095, -151.36927803253354, -225.77660905194142),
                                               (0.0, -106.41318153067618, 20.62490397784),
                                               (104.70223733183946, -38.46867443725896, -94.54151241017138),
                                               (109.50109681379878, -22.538129367076607, -89.87202383972189),
                                               (-53.76680398885172, -183.40542591779914, 88.69588244616119),
                                               (133.1176687381933, 64.36204623764101, -103.59140651458866),
                                               (305.3140658401604, 76.88591230195068, 64.6839921759408),
                                               (-78.5689769257198, 31.13565114891651, 54.40178442602435)],
    
                                   scales = [(0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01),
                                             (0.01, 0.01, 0.01)],
                       num_buffer = 1,
                       rig_parent = "C_rig_GRP", 
                       skel_parent = "C_skeleton_GRP",
                       sizes = [
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                .03,
                                ],
                       global_scale = global_hook,
                       debug = debug)
    misc.non_bind_jnt_invis()
    misc.sec_bind_jnt_vis()
    misc.select_bind_jnts()
    if weights_path:
        #---weights
        #---bind BIND jnts
        weights.skin_to_bind_jnts(["C_body_GEO", 
                                   'L_holster00plane_EX',
                                   'L_holster01plane_EX',
                                   'L_holster02plane_EX',
                                   'L_holster03plane_EX',
                                   'L_holster04plane_EX',
                                   'L_holster05plane_EX',
                                   'L_holster06plane_EX',
                                   'L_holster07plane_EX',
                                   'R_holster00plane_EX',
                                   'R_holster01plane_EX',
                                   'R_holster02plane_EX',
                                   'R_holster03plane_EX',
                                   'R_holster04plane_EX',
                                   'R_holster05plane_EX',
                                   'R_holster06plane_EX'
                                   ])
        #---bind SEC_BIND jnts
        weights.skin_to_bind_sec_jnts(["C_holster_GEO"])
        #import weights
        weights.import_skins(weights_path)
    #character fixes
    if debug == False:
        misc.cleanup_geo()
        misc.cleanup_skel()
######################################
#---Example
build_it(scene_path = scene_path, 
         weights_path = weights_path,
         debug = False)
#########################################