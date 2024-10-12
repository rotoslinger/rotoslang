import sys

import control.base
import importlib

linux = '/corp/projects/eng/lharrison/workspace/levi_harrison_test'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

from maya import cmds
from utils import misc
from rig.control import base as control_base
importlib.reload(control_base)

importlib.reload(misc)

#===============================================================================
#CLASS:         create_shoulder
#DESCRIPTION:   Creates shoulder rig
#USAGE:         set arguments for shouldr
#RETURN:        skel_joint, ctl, ctl_buffers, ctl_gimbal
#REQUIRES:      utils.misc, maya.cmds, sys
#AUTHOR:        Levi Harrison
#DATE:          Oct 21th, 2014
#Version        1.0.0
#===============================================================================

class create_torso():
    def __init__(self,
                 side = "C",
                 name = "torso",
                 root_joint = 'root_bind',
                 torso_joints = ["spinea_bind",
                                 "spineb_bind",
                                 "spinec_bind",
                                 "spined_bind"],
                 hip_joint = 'pelvis_bind',
                 driver = "",
                 global_scale = "",
                 skel_parent = "C_skeleton_GRP",
                 rig_parent = "C_rig_GRP",
                 switch_size = 1.0,
                 switch_orient = [0.0, 0.0, 0.0],
                 switch_offset = [0.0, 0.0, 0.0],
                 fwd_ctl_sizes   = [1.0, 
                                    1.0, 
                                    1.0, 
                                    1.0,
                                    1.0, 
                                    1.0],
                 rev_ctl_sizes   = [1.0, 
                                    1.0, 
                                    1.0, 
                                    1.0,
                                    1.0, 
                                    1.0],
                 ctl_orients = [[0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0]],
                 ctl_offsets = [[0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0],
                                [0,0,0]],
                 debug = False,
                 ):
        """
        type  side:                string
        param side:                usually C but L or R are also supported

        type  name:                string
        param name:                the name of your torso

        type  root_joint:          string
        param root_joint:          the root of the torso joint chain
                                    usually this would be the root of the whole
                                    skeleton if you give an empty string ''
                                    I will try to find the root automatically,
                                    but no guarantees

        type  torso_joints:        string array
        param torso_joints:        the torso joints that the rig will drive

        type  hip_joint:           string array
        param hip_joint:           the joint that the rig will drive the hips
                                    if an empty string '' no hip will be 
                                    created

        type  driver:              string
        param driver:              what the shoulder will be attached to
                                    usually the chest joint but anything that
                                    exists will work

        type  global_scale:        string
        param global_scale:        what the shoulder will be attached to
                                    for scaling usually lowest point in
                                    hierarchy of global ctl

        type  skel_parent:          string
        param skel_parent:          where to parent newly created joints,
                                     effectors, and generally things animators
                                     don't want to see.

        type  rig_parent:           string
        param rig_parent:           where to parent ctls and other things
                                     animators would like to see

        type  fwd_ctl_sizes:        float
        param fwd_ctl_sizes:        a size for the torso control

        type  rev_ctl_sizes:        float
        param rev_ctl_sizes:        a size for the torso control

        type  ctl_orients:          float
        param ctl_orients:          orientation for the controls
        
        type  ctl_offsets:          float
        param ctl_offsets:          translation offset for the controls

        type  switch_size:          float
        param switch_size:          switch size
        
        type  switch_orient:        float
        param switch_orient:        switch orientation
        
        type  switch_offset:        float
        param switch_offset:        switch translation offset


        type  debug:                bool
        param debug:                if debug is on, nothing will be locked and
                                     ihi will remain 1
        """

        #---arg vars
        self.side                   = side
        self.name                   = name
        self.root_joint             = root_joint
        self.torso_joints           = torso_joints
        self.hip_joint              = hip_joint
        self.driver                 = driver
        self.global_scale           = global_scale
        self.skel_parent            = skel_parent
        self.rig_parent             = rig_parent
        self.debug                  = debug
        self.fwd_ctl_sizes          = fwd_ctl_sizes
        self.rev_ctl_sizes          = rev_ctl_sizes
        self.ctl_orients            = ctl_orients
        self.ctl_offsets            = ctl_offsets
        self.switch_size            = switch_size
        self.switch_orient          = switch_orient
        self.switch_offset          = switch_offset

        #---vars
        self.fwd_joints              = []
        self.rev_joints              = []
        self.root_fwd_joint          = []
        self.torso_fwd_joints        = []
        self.root_rev_joint          = []
        self.torso_rev_joints        = []
        self.root_bind_joint         = []
        self.torso_bind_joints       = []
        self.bind_joints             = []
        self.fwd_ctls                = []
        self.fwd_ctl_buffers         = []
        self.fwd_ctl_gimbals         = []
        self.rev_ctls                = []
        self.rev_ctl_buffers         = []
        self.rev_ctl_gimbals         = []
        self.chest_anchor            = ""
        self.switch_ctl              = ""
        self.switch_attr             = ""
        self.switch_constraints      = []
        self.fwd_ik                  = []
        self.rev_ik                  = []
        self.fwd_root_two_ctl        = []
        self.rev_root_two_ctl        = []

        self.__create()

    def __check(self):
        """ makes sure things exist and are the right type """
        for i in self.torso_joints:
            if cmds.objExists(i):
                if cmds.nodeType(i) != "joint":
                    raise Exception(i + " must be a joint")
                    quit()
            else:
                raise Exception(i + " does not exist")
                quit()

        for i in [self.root_joint, self.hip_joint]:
            if cmds.objExists(i):
                if cmds.nodeType(i) != "joint":
                    raise Exception(self.joints + " must be a joint")
                    quit()
            else:
                raise Exception(i + " does not exist")
                quit()

        if cmds.objExists(self.skel_parent) != 1:
            raise Exception(self.skel_parent + " does not exist")
            quit()

        if cmds.objExists(self.rig_parent) != 1:
            raise Exception(self.rig_parent + " does not exist")
            quit()

    def __create_parents(self):
        """ create groups for skeleton and rig """
        self.skel_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_torsoSkel_GRP",
                                          p = self.skel_parent)

        self.rig_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_torsoRig_GRP",
                                          p = self.rig_parent)

    def __create_bind_skel(self):
        """ creates joints """
        tmp_root = cmds.createNode("joint",
                                   name = self.side
                                   + "_root_JNT", 
                                   parent = self.skel_parent)
        con = cmds.parentConstraint(self.root_joint, tmp_root)
        cmds.delete(con)
        tmp_hip = cmds.createNode("joint",
                                   name = self.side
                                   + "_hip_JNT", 
                                   parent = tmp_root)
        for i in [tmp_root,tmp_hip]:
            cmds.addAttr(i, 
                         ln = "BIND",
                         at = "bool",)
            cmds.setAttr(i+".BIND", 
                         l = True, 
                         k=False)
        
        con = cmds.parentConstraint(self.hip_joint, tmp_hip)
        cmds.delete(con)
        tmp_torso = []
        for i in range(len(self.torso_joints)+1):
            if i < len(self.torso_joints):
                if i == 0:
                    parent = tmp_root
                else:
                    parent = tmp_torso[i -1]
                tmp_torso.append(cmds.createNode("joint",
                                           name = (self.side 
                                                   + "_torso" 
                                                   + str(i) 
                                                   + "_JNT"),
                                           parent = parent))
                con = cmds.parentConstraint(self.torso_joints[i], tmp_torso[i])
                cmds.delete(con)
                if i < len(self.torso_joints):
                    cmds.addAttr(tmp_torso[i], ln = "BIND",
                                     at = "bool",)
                    cmds.setAttr(tmp_torso[i]+".BIND", l = True, k=False)
            else:
                self.chest_anchor = cmds.createNode("joint",
                                           name = (self.side 
                                                   + "_chest" 
                                                   + "_JNT"),
                                           parent = tmp_torso[i -1])
                con = cmds.parentConstraint(self.torso_joints[i-1],
                                            self.chest_anchor)
                cmds.delete(con)
                cmds.addAttr(self.chest_anchor, ln = "BIND",
                                 at = "bool",)
                cmds.setAttr(self.chest_anchor+".BIND", l = True, k=False)
        cmds.makeIdentity(tmp_root,
                          apply = True,
                          t=0, 
                          r=1, 
                          s = 1, 
                          n=0, 
                          pn=1)
        self.root_joint = tmp_root
        self.torso_joints = tmp_torso
        self.hip_joint = tmp_hip
        self.bind_joints = [self.root_joint] + self.torso_joints
        #---fwd joints
        self.root_fwd_joint = cmds.duplicate(self.root_joint, 
                                             name = self.side
                                             + "_fwdRoot_JNT",
                                             rc = True)[0]
        children = cmds.listRelatives(self.root_fwd_joint, 
                                      ad = True, 
                                      typ = "joint")
        cmds.delete(children[0])
        children.remove(children[0])
        for i in range(len(children)):
            new_name = children[i].split("_")
            new_name = (new_name[0] 
                        + "_" 
                        + "fwd"
                        + new_name[1][0:].capitalize()
                        +"_JNT")
            cmds.rename(children[i], new_name)
            self.torso_fwd_joints.append(new_name)
        self.fwd_joints = [self.root_fwd_joint] + self.torso_fwd_joints
        for i in self.fwd_joints:
            if cmds.objExists(i+".BIND"):
                cmds.setAttr(i+".BIND", l =False)
                cmds.deleteAttr(i+".BIND")
        #---rev joints
        self.root_rev_joint = cmds.duplicate(self.root_joint, 
                                             name = self.side
                                             + "_revRoot_JNT",
                                             rc = True)[0]
        children = cmds.listRelatives(self.root_rev_joint, 
                                      ad = True, 
                                      typ = "joint")
        cmds.delete(children[0])
        children.remove(children[0])
        for i in range(len(children)):
            new_name = children[i].split("_")
            new_name = (new_name[0] 
                        + "_" 
                        + "rev"
                        + new_name[1][0:].capitalize()
                        +"_JNT")
            cmds.rename(children[i], new_name)
            self.torso_rev_joints.append(new_name)
        self.torso_rev_joints.reverse()
        self.rev_joints = [self.root_rev_joint] + self.torso_rev_joints
        #flip rev joints
        self.rev_joints.reverse()
        cmds.reroot(self.rev_joints[0])
        #orientjoints
        cmds.joint(self.rev_joints[0],
                   e = True,
                    oj="xyz", 
                    secondaryAxisOrient = "yup", 
                    ch = True,
                    zso=True)
        self.rev_joints.reverse()
        for i in self.rev_joints:
            if cmds.objExists(i+".BIND"):
                cmds.setAttr(i+".BIND", l =False)
                cmds.deleteAttr(i+".BIND")
    def __create_ik(self):
        #fwd_ik
        cluster_parents = []
        for i in range(len(self.fwd_joints)):
            cluster_parents.append(self.skel_parent)
            i
        self.torso_fwd_joints.reverse()
        fwd_chest = self.torso_fwd_joints[len(self.torso_fwd_joints)-1]
        self.torso_fwd_joints.remove(self.torso_fwd_joints[len(self.torso_fwd_joints)-1])
        self.fwd_ik = control.base.create_spline_ik(side = self.side,
                                                    name = self.name + "fwd",
                                                    joints = self.torso_fwd_joints,
                                                    curve_parent = self.skel_parent,
                                                    inherit_transform = False,
                                                    cluster_parents = cluster_parents,
                                                    ik_handle_parent = self.skel_parent,
                                                    hide = True,
                                                    )
        self.torso_fwd_joints.append(fwd_chest)
        self.torso_fwd_joints.reverse()
        #rev_ik
        rev_chest = self.torso_rev_joints[len(self.torso_rev_joints)-1]
        self.torso_rev_joints.remove(self.torso_rev_joints[len(self.torso_rev_joints)-1])
        self.torso_rev_joints.reverse()
        self.rev_ik = control.base.create_spline_ik(side = self.side,
                                                    name = self.name + "Rev",
                                                    joints = self.torso_rev_joints,
                                                    curve_parent = self.skel_parent,
                                                    inherit_transform = False,
                                                    cluster_parents = cluster_parents,
                                                    ik_handle_parent = self.skel_parent,
                                                    hide = True,
                                                    )
        self.torso_rev_joints.append(rev_chest)
        self.torso_rev_joints.reverse()
        #---hide ik handles
        cmds.setAttr(self.fwd_ik.ik[0] + " .v", 0)
        cmds.setAttr(self.rev_ik.ik[0] + " .v", 0)
        #---hide curves
        cmds.setAttr(self.fwd_ik.curve + " .v", 0)
        cmds.setAttr(self.rev_ik.curve + " .v", 0)
        #---fix rev root
        con = cmds.pointConstraint(self.root_joint, self.root_rev_joint)
        cmds.delete(con)
    def __create_ctl(self):
        """ creates and positions controls for forward and reverse spines"""
        all_jnts = [self.root_joint] + self.torso_joints + [self.hip_joint]
        suffix = ["Fwd", "Rev"]
        shape = ["circle", "square"]
        loop_ctl = [self.fwd_ctls, self.rev_ctls]
        loop_buffer = [self.fwd_ctl_buffers, self.rev_ctl_buffers,]
        loop_gimbal =  [self.fwd_ctl_gimbals,self.rev_ctl_gimbals]
        ctl_sizes = [self.fwd_ctl_sizes,self.rev_ctl_sizes]
        for i in range(2):
            return_ctl = []
            for j in range(len(all_jnts)):
                num_secondary = 0,
                if i == 0 and j == 0:
                    num_secondary = 1,
                if i == 1 and j == len(all_jnts)-2:
                    num_secondary = 1,
                if i == 1 and j == len(all_jnts)-1:
                    continue
                else:
                    if i == 0 and j == len(all_jnts)-1:
                        suffix[i] = ""

                    name = all_jnts[j].split("_")[1] +suffix[i]
                    return_ctl.append(control_base.create_ctl(side = self.side, 
                                                      name = name, 
                                                      parent = self.rig_parent, 
                                                      shape = shape[i],
                                                      num_buffer = 3,
                                                      lock_attrs = ["sx",
                                                                    "sy",
                                                                    "sz",
                                                                    ],
                                                      show_rot_order = True, 
                                                      gimbal = True,
                                                      num_secondary = num_secondary[0],
                                                      size = ctl_sizes[i][j],
                                                      orient = (self.ctl_orients
                                                                [j]),
                                                      offset = (self.ctl_offsets
                                                                [j])))
                    con = cmds.parentConstraint(all_jnts[j], 
                                                return_ctl[j].buffers[0])
                    cmds.delete(con)
                    loop_ctl[i].append(return_ctl[j].ctl)
                    loop_buffer[i].append(return_ctl[j].buffers)
                    loop_gimbal[i].append(return_ctl[j].gimbal_ctl)
        #---create switch ctl
        self.switch_ctl = control_base.create_ctl(side = self.side, 
                                          name = (self.name 
                                                  + "Switch"), 
                                          parent = self.rig_parent, 
                                          shape = "switch",
                                          num_buffer = 1,
                                          lock_attrs = ["all"],
                                          show_rot_order = False, 
                                          gimbal = False,
                                          size = self.switch_size,
                                          orient = self.switch_orient,
                                          offset = self.switch_offset)
        con = cmds.pointConstraint(self.root_joint, 
                                    self.switch_ctl.buffers[0])
        cmds.delete(con)
        cmds.pointConstraint(self.root_joint, 
                            self.switch_ctl.buffers[0],
                            mo = True)
    def __parent_controls(self):
        #reverse rev controls
        self.rev_ctl_gimbals.reverse()
        self.rev_ctl_buffers.reverse()
#         ctls = [self.fwd_ctls,self.rev_ctls]
        ctls = [self.fwd_ctl_gimbals,self.rev_ctl_gimbals]
        buffers = [self.fwd_ctl_buffers, self.rev_ctl_buffers]
        for i in range(2):
            #---skip hip because there is only 1, it will be parent constrained
            # to the root ctl instead of parented
            for j in range(len(self.fwd_ctls)-1):
                if j == 0:
                    continue
                else:
                    #---parent buffers
                    cmds.parent(buffers[i][j][0],ctls[i][j-1])
        self.rev_ctl_gimbals.reverse()
        self.rev_ctl_buffers.reverse()

    def __create_switching(self):
        self.torso_fwd_joints.reverse()
        self.fwd_joints = [self.root_fwd_joint] + self.torso_fwd_joints
        cmds.addAttr(self.switch_ctl.ctl, ln = "forward_reverse", at = "short", 
                     dv = 0, min = 0, max = 1, k = True)
        self.switch_attr = self.switch_ctl.ctl + ".forward_reverse"
        #---create constraints
#         tmp_cons = []
        p_constraints = []
        for i in range(len(self.bind_joints)):
            p_constraints.append(cmds.parentConstraint(self.fwd_joints[i], 
                                                       self.rev_joints[i],
                                                       self.bind_joints[i],
                                                       mo = True)[0])
            cmds.connectAttr(self.switch_attr, p_constraints[i] + ".w1")
            if i <len(self.bind_joints):
                cmds.connectAttr(self.switch_attr,
                                 self.rev_ctls[i] + ".v",
                                 f = True)
                misc.lock_attrs(node = self.rev_ctls[i], 
                                attr = ["v"], 
                                l = True,
                                k = False,
                                cb = False)
            if i == 0:
                self.reverse = cmds.createNode("reverse", 
                                          name = self.side 
                                          + "_"
                                          + self.name + "SwitchRev"
                                          +str(i)
                                          + "_REV")
                #---chest blending here because of indexing issues
                tmp = cmds.parentConstraint(self.fwd_joints[len(self.fwd_joints)-1],
                                            self.rev_joints[len(self.rev_joints)-1],
                                            self.chest_anchor,
                                            mo = True)[0]
                cmds.connectAttr(self.switch_attr, tmp + ".w1")
                cmds.connectAttr(self.reverse + ".outputX", tmp +".w0")
                cmds.connectAttr(self.switch_attr, self.reverse + ".inputX")
            cmds.connectAttr(self.reverse + ".outputX", p_constraints[i] + ".w0")
            if i <len(self.bind_joints):
                cmds.connectAttr(self.reverse + ".outputX",
                                 self.fwd_ctls[i] + ".v",
                                 f = True)
                misc.lock_attrs(node = self.fwd_ctls[i], 
                                attr = ["v"], 
                                l = True,
                                k = False,
                                cb = False)

    def __create_rig(self):
        #---fwd
        gimbals = self.fwd_ctl_gimbals
        cons = []
        clusters =self.fwd_ik.cluster_ctl_buffers
        for i in range(len(self.fwd_ctls)-1):
            if i == 0:
                continue
            else:
                cons.append(cmds.parentConstraint(gimbals[i],
                                                  clusters[i-1],
                                                  mo = True))

        gimbals = self.rev_ctl_gimbals
        cons = []
        clusters =self.rev_ik.cluster_ctl_buffers
        clusters.reverse()
        for i in range(len(self.rev_ctl_gimbals)-1):
#             if i == 0:
#                 continue
            cons.append(cmds.parentConstraint(gimbals[i+1],
                                              clusters[i],
                                              mo = True))
        #---fwd chest
        chest_ctl = self.fwd_ctl_gimbals[len(self.fwd_ctl_gimbals)-2]
        cmds.orientConstraint(chest_ctl, 
                              self.torso_fwd_joints[len(self.torso_fwd_joints)-1],
                              mo = True)
        #---fwd root
        root_ctl = self.fwd_ctl_gimbals[0]
        cmds.parentConstraint(root_ctl, self.root_fwd_joint,
                              mo = True)
        
        #---rev chest
        chest_ctl = self.rev_ctl_gimbals[len(self.rev_ctl_gimbals)-1]
        cmds.parentConstraint(chest_ctl, 
                              self.torso_rev_joints[0],
                              mo = True)
        #---rev root
        root_ctl = self.rev_ctl_gimbals[0]
        cmds.orientConstraint(root_ctl, self.root_rev_joint,
                              mo=True)

        #---hip
        hip_ctl = self.fwd_ctl_gimbals[len(self.fwd_ctl_gimbals)-1]
        hip_buffer = self.fwd_ctl_buffers[len(self.fwd_ctls)-1][0]
        cmds.parentConstraint(hip_ctl, self.hip_joint)
        cmds.parentConstraint(self.root_joint, hip_buffer, mo = True)

    def __create_world_aligns(self):
        #---fwd align
#         quit()
        for i in range(len(self.fwd_ctls)-1):
            #---skip root
            if i == 0:
                continue
            else:
                misc.create_fk_align(ctl = self.fwd_ctls[i],
                                     ctl_grp = (self.fwd_ctl_buffers[i]
                                                [len(self.fwd_ctl_buffers[i])-1]), 
                                     default_align_parent = (self.fwd_ctl_buffers[i]
                                                             [len(self.fwd_ctl_buffers[i])-2]), 
                                     skel_group = self.skel_parent)
        for i in range(len(self.rev_ctls)):
            #---skip chest
            if i == len(self.rev_ctls)-1:
                continue
            else:
                misc.create_fk_align(ctl = self.rev_ctls[i],
                                     ctl_grp = (self.rev_ctl_buffers[i]
                                                [len(self.rev_ctl_buffers[i])-1]), 
                                     default_align_parent = (self.rev_ctl_buffers[i]
                                                             [len(self.rev_ctl_buffers[i])-2]), 
                                     skel_group = self.skel_parent)
        #---hip
        misc.create_fk_align(ctl = self.fwd_ctls[len(self.fwd_ctls)-1],
                             ctl_grp = (self.fwd_ctl_buffers[len(self.fwd_ctls)-1]
                                        [len(self.fwd_ctl_buffers[i])-1]), 
                             default_align_parent = (self.fwd_ctl_buffers[len(self.fwd_ctls)-1]
                                                     [len(self.fwd_ctl_buffers[i])-2]), 
                             skel_group = self.skel_parent)

    def __drive_rig(self):
        """ connect the rig to the specified driver/global scale if if exists"""
        if self.driver:
            cmds.parentConstraint(self.driver, self.rig_parent, mo = True)
            cmds.parentConstraint(self.driver, self.skel_parent, mo = True)

        if self.global_scale:
            cmds.scaleConstraint(self.global_scale, self.rig_parent, mo = True)
            cmds.scaleConstraint(self.global_scale, self.skel_parent, mo = True)
    def __cleanup(self):
        #---lock hip ctl translates
        misc.lock_attrs(node =self.fwd_ctls[len(self.fwd_ctls)-1],
                         attr = ["tx", "ty", "tz"],
                         l = True,
                         k = False,
                         cb = False)
        #---lock last 2 reverse translates
        misc.lock_attrs(node =self.rev_ctls[0],
                         attr = ["tx", "ty", "tz"],
                         l = True,
                         k = False,
                         cb = False)
        if self.debug == False:
            misc.suffix_constraints()
            misc.lock_all(hierarchy = self.rig_parent, 
                          filter = ["*_CTL", "*_JNT"])
            misc.lock_all(hierarchy = self.skel_parent, 
                          filter = ["*_CTL", "*_JNT"])

    def __create(self):
        self.__check()
        self.__create_parents()
        self.__create_bind_skel()
        self.__create_ctl()
        self.__create_ik()
        self.__parent_controls()
        self.__create_switching()
        self.__create_rig()
        self.__create_world_aligns()
        self.__drive_rig()
        self.__cleanup()