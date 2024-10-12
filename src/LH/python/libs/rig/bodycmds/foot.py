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
if os not in sys.path:
    sys.path.append(os)

from maya import cmds
from utils import misc
from rig.control import base as control_base
importlib.reload(control_base)

importlib.reload(misc)

#===============================================================================
#CLASS:         create_foot
#DESCRIPTION:   Creates foot rig
#USAGE:         set arguments for foot
#RETURN:        skel_joint, ctl, ctl_buffers, ctl_gimbal
#REQUIRES:      utils.misc, maya.cmds, sys
#AUTHOR:        Levi Harrison
#DATE:          Oct 21th, 2014
#Version        1.0.0
#===============================================================================

class create_foot():
    def __init__(self,
                 side = "L",
                 name = "foot",
                 toe_joint = "l_toe_bind",
                 tip_joint = "l_toeTipFront_bind",
                 left_joint = "l_toeTipLeft_bind",
                 right_joint = "l_toeTipRight_bind",
                 heel_joint = "l_toeTipBack_bind",
                 toe_end_joint = "l_toe_bind_end",
                 ankle_joint = "l_ankle_bind",
                 ik_control = "",
                 ik_switch = "",
                 ik_root = "",
                 driver = "",
                 global_scale = "",
                 skel_parent = "C_skeleton_GRP",
                 rig_parent = "C_rig_GRP",
                 fk_ctl_size = 1.0,
                 orient = [0,0,0],
                 offset = [0,0,0],
                 foot_groups = [],
                 debug = False,
                 ):
        """
        type  side:                string
        param side:                usually C but L or R are also supported

        type  name:                string
        param name:                the names of your foot

        type  joint:               string array
        param joint:               the foot joint that the rig will drive

        type  driver:              string
        param driver:              what the foot will be attached to
                                    usually the chest joint but anything that
                                    exists will work

        type  global_scale:        string
        param global_scale:        what the foot will be attached to
                                    for scaling usually lowest point in
                                    hierarchy of global ctl


        type  skel_parent:          string
        param skel_parent:          where to parent newly created joints,
                                     effectors, and generally things animators
                                     don't want to see.

        type  rig_parent:           string
        param rig_parent:           where to parent ctls and other things
                                     animators would like to see

        type  fk_ctl_size:             float
        param fk_ctl_size:             a size for the foot control

        type  debug:                bool
        param debug:                if debug is on, nothing will be locked and
                                     ihi will remain 1
        """

        #---arg vars
        self.side                   = side
        self.name                   = name
        self.toe_joint              = toe_joint
        self.toe_end_joint          = toe_end_joint
        self.ankle_joint            = ankle_joint
        self.foot_helpers           = [ankle_joint,
                                       toe_joint,
                                       toe_end_joint]

        
        self.tip_joint              = tip_joint
        self.left_joint             = left_joint
        self.right_joint            = right_joint
        self.heel_joint             = heel_joint
        self.roll_joints            = [tip_joint,
                                       heel_joint,
                                       left_joint,
                                       right_joint,
                                       toe_joint]
        
        

        self.driver                 = driver
        self.global_scale           = global_scale
        self.skel_parent            = skel_parent
        self.rig_parent             = rig_parent
        self.fk_ctl_size            = fk_ctl_size
        self.debug                  = debug
        self.orient                 = orient
        self.offset                 = offset
        self.foot_groups            = foot_groups
        self.ik_control             = ik_control
        self.ik_switch              = ik_switch
        self.ik_root                = ik_root
        #---vars
        self.skel_joint              = ""
        self.ctl                     = []
        self.ctl_buffers             = []
        self.ctl_gimbal              = []
        self.roll_groups             = []
        self.__create()

    def __check(self):
        """ makes sure first three indexes in self.toe_joints are joints """
        if cmds.objExists(self.toe_joint):
            if cmds.nodeType(self.toe_joint) != "joint":
                raise Exception(self.toe_joint + " must be a joint")
                quit()
        else:
            raise Exception(self.toe_joint + " does not exist")
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
                                          "_footSkel_GRP",
                                          p = self.skel_parent)
        
        self.rig_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_footRig_GRP",
                                          p = self.rig_parent)

    def __create_bind_skel(self):
        """ create control and snap to foot """
        self.skel_joint = cmds.createNode("joint", 
                                          n = self.side + "_" 
                                          + self.name
                                          + "_JNT",
                                          parent = self.skel_parent)
        con = cmds.parentConstraint(self.toe_joint,
                                    self.skel_joint)
        cmds.delete(con)
        cmds.makeIdentity(self.skel_joint,
                          apply = True, t=0, r=1, s = 1, n=0, pn=1)

        cmds.addAttr(self.skel_joint, ln = "BIND",
                         at = "bool",)
        cmds.setAttr(self.skel_joint+".BIND", l = True, k=False)

    def __create_ctl(self):
        """ create control and snap to foot """
        tmp_ctl = control_base.create_ctl(side = self.side, 
                                  name = self.name, 
                                  parent = self.rig_parent, 
                                  shape = "circle", 
                                  lock_attrs = ["sx","sy","sz","v"], 
                                  num_buffer = 3,
                                  gimbal = True,
                                  show_rot_order = True, 
                                  size = self.fk_ctl_size, 
                                  orient = self.orient,
                                  offset = self.offset)
        self.ctl = tmp_ctl.ctl
        self.ctl_buffers = tmp_ctl.buffers
        self.ctl_gimbal = tmp_ctl.gimbal_ctl
        con = cmds.parentConstraint(self.skel_joint, self.ctl_buffers[0])
        cmds.delete(con)

    def __rig_foot(self):
        cmds.parentConstraint(self.ctl_gimbal, self.skel_joint)
        #---foot align
#         misc.create_fk_align(ctl = self.ctl, 
#                              ctl_grp = self.ctl_buffers
#                              [len(self.ctl_buffers) - 1],
#                              default_align_parent = self.ctl_buffers
#                              [len(self.ctl_buffers) - 2],
#                              skel_group = self.skel_parent)
        #---groupings
        for i in range(5):
            parent_grp = ""
            num = 0
            if i == 0:
                parent_grp = self.ik_control
                num = 5
            else:
                parent_grp = (self.side 
                              +"_footRollOffsets"
                              + str(6-i)
                              + "_JNT")
                num = 5-i
                
            gimbal_group = cmds.createNode("joint",
                              n = self.side 
                              +"_footRollOffsets"
                              + str(num)
                              + "_JNT",
                              p = parent_grp)
            tcon = cmds.parentConstraint(self.roll_joints[i],
                            gimbal_group)
            cmds.delete(tcon)
            cmds.makeIdentity(gimbal_group,
                              apply = True,
                              t=0, 
                              r=1, 
                              s = 1, 
                              n=0, 
                              pn=1)
            if i==4:
                cmds.parent(self.foot_groups[0],
                            gimbal_group)

            
            self.roll_groups.append(gimbal_group)
        #---Constraints
#         self.parent_con = cmds.orientConstraint(self.driver,
#                                                 self.roll_groups[3],
#                                                 self.ctl_buffers[1],
#                                                 mo= True)[0]
#         self.point_con = cmds.pointConstraint(self.driver,
#                                                 #self.roll_groups[3],
#                                                 self.ctl_buffers[1],
#                                                 mo= True)[0]
#         self.parent_con = cmds.parentConstraint(self.driver,
#                                                 self.helper_joints[1],
#                                                 self.ctl_buffers[1],
#                                                 mo= True)[0]


    def __create_ik_skel(self):
        """"""
        self.helper_joints = []
        self.helper_joints.append(self.ik_root)
        for i in range(len(self.foot_helpers)):
            if i > 0:
                name = self.foot_helpers[i].split("_JNT")[0]
                joint = (cmds.createNode("joint", 
                                                  n = name
                                                  + "_HELP",
                                                  parent = self.rig_parent))
                con = cmds.parentConstraint(self.foot_helpers[i],
                                            joint)
                cmds.delete(con)
                cmds.makeIdentity(joint,
                                  apply = True, t=0, r=1, s = 1, n=0, pn=1)
                self.helper_joints.append(joint)
            
        cmds.parent(self.helper_joints[2],self.helper_joints[1])
        cmds.parent(self.helper_joints[1],self.helper_joints[0])
#         
#         
        #cmds.pointConstraint(self.driver, self.helper_joints[0])
#         
#         
        ik_handle1 = cmds.ikHandle(sj = self.helper_joints[0],
                                  ee = self.helper_joints[1],
                                  sol = "ikSCsolver",
                                  name = self.side
                                  + "_"
                                  + "footHelper1_IKH")[0]
        cmds.setAttr(ik_handle1 + ".v", 0)
        tmp_parent_con = cmds.parentConstraint(self.roll_groups[4],
                                                ik_handle1,
                                                mo= True)[0]
        ik_handle2 = cmds.ikHandle(sj = self.helper_joints[1],
                                  ee = self.helper_joints[2],
                                  sol = "ikSCsolver",
                                  name = self.side
                                  + "_"
                                  + "footHelper2_IKH")[0]
        cmds.setAttr(ik_handle2 + ".v", 0)
        tmp_parent_con = cmds.parentConstraint(self.roll_groups[3],
                                                ik_handle2,
                                                mo= True)[0]
        self.parent_con = cmds.parentConstraint(self.driver,
                                                self.helper_joints[1],
                                                self.ctl_buffers[1],
                                                mo= True)[0]
        cmds.parent(ik_handle1,self.roll_groups[4])
        cmds.parent(ik_handle2,self.roll_groups[3])

    def __create_attrs(self):
        """"""
        cmds.addAttr(self.ik_control, ln = "roll", at = "float", 
             dv = 0, min = 0, max = 100)
        self.roll_attr = self.ik_control + ".roll"
        cmds.setAttr(self.roll_attr, k = True, cb = False)
        
        
        cmds.addAttr(self.ik_control, ln = "rockFB", at = "float", 
             dv = 0, min = -90, max = 90)
        self.rock_fb_attr = self.ik_control + ".rockFB"
        cmds.setAttr(self.rock_fb_attr, k = True, cb = False)
        
        cmds.addAttr(self.ik_control, ln = "rockLR", at = "float", 
             dv = 0, min = -90, max = 90)
        self.rock_lr_attr = self.ik_control + ".rockLR"

        cmds.setAttr(self.rock_lr_attr, k = True, cb = False)





    def __connect_attrs(self):
        """        self.roll_joints  = [
                                       tip_joint,
                                       heel_joint,
                                       left_joint,
                                       right_joint,
                                       toe_joint] 
"""
        #---Roll
        cmds.connectAttr(self.roll_attr, self.roll_groups[4] + ".ry")


        
        
        
        #---RockF
        condition = cmds.createNode("condition", 
                                  name = self.side 
                                  + "_"
                                  + self.name + "RockF"
                                  + "_CDN")
        cmds.setAttr(condition + ".operation", 4)
        cmds.setAttr(condition + ".colorIfFalseR", 0)

        cmds.connectAttr(self.rock_fb_attr, condition + ".firstTerm")
        reverse = cmds.createNode("reverse", 
                          name = self.side 
                          + "_"
                          + self.name + "RockFB"
                          + "_REV")
        cmds.connectAttr(self.rock_fb_attr, reverse + ".inputX")
        cmds.connectAttr(reverse + ".outputX", condition + ".colorIfTrueR")
        cmds.connectAttr(condition + ".outColorR", self.roll_groups[0] + ".ry")
        
        #---RockB
        condition = cmds.createNode("condition", 
                                  name = self.side 
                                  + "_"
                                  + self.name + "RockB"
                                  + "_CDN")
        cmds.setAttr(condition + ".operation", 2)
        cmds.setAttr(condition + ".colorIfFalseR", 0)

        cmds.connectAttr(self.rock_fb_attr, condition + ".firstTerm")
        cmds.connectAttr(self.rock_fb_attr, condition + ".colorIfTrueR")

        cmds.connectAttr(condition + ".outColorR", self.roll_groups[1] + ".ry")

        #---RockL
        condition = cmds.createNode("condition", 
                                  name = self.side 
                                  + "_"
                                  + self.name + "RockL"
                                  + "_CDN")
        cmds.setAttr(condition + ".operation", 4)
        cmds.setAttr(condition + ".colorIfFalseR", 0)
        cmds.connectAttr(self.rock_lr_attr, condition + ".firstTerm")
        reverse = cmds.createNode("reverse", 
                          name = self.side 
                          + "_"
                          + self.name + "RockFB"
                          + "_REV")
        cmds.connectAttr(self.rock_lr_attr, reverse + ".inputX")
        cmds.connectAttr(reverse + ".outputX", condition + ".colorIfTrueR")
        if self.side == "L":
            cmds.connectAttr(condition + ".outColorR", self.roll_groups[3] + ".ry")
        if self.side == "R":
            cmds.connectAttr(condition + ".outColorR", self.roll_groups[2] + ".ry")

        #---RockR
        condition = cmds.createNode("condition", 
                                  name = self.side 
                                  + "_"
                                  + self.name + "RockR"
                                  + "_CDN")
        cmds.setAttr(condition + ".operation", 2)
        cmds.setAttr(condition + ".colorIfFalseR", 0)
        cmds.connectAttr(self.rock_lr_attr, condition + ".firstTerm")
        cmds.connectAttr(self.rock_lr_attr, condition + ".colorIfTrueR")

        if self.side == "L":
            cmds.connectAttr(condition + ".outColorR", self.roll_groups[2] + ".ry")
        if self.side == "R":
            cmds.connectAttr(condition + ".outColorR", self.roll_groups[3] + ".ry")

        #---IKFKSwitching
        switch_reverse = cmds.createNode("reverse", 
                  name = self.side 
                  + "_"
                  + self.name + "FootSwitch"
                  + "_REV")
        #print self.ik_switch.ctl + ".v"
        
        cmds.setAttr( self.ctl + ".v", l = False, cb = False, k = False)

        cmds.connectAttr(self.ik_switch.ctl+".ik_fk_switch", 
                         str(self.ctl) + ".v")
        
        cmds.setAttr( self.ctl + ".v", l = True, cb = False, k = False)

        cmds.connectAttr(self.ik_switch.ctl+".ik_fk_switch", 
                         self.parent_con + ".w0")

        cmds.connectAttr(self.ik_switch.ctl+".ik_fk_switch", 
                         switch_reverse + ".inputX")
        cmds.connectAttr(switch_reverse+".outputX", 
                         self.parent_con + ".w1")

        
    def __drive_rig(self):
        if self.driver:
            cmds.parentConstraint(self.driver, self.rig_parent, mo = True)
            cmds.parentConstraint(self.driver, self.skel_parent, mo = True)
        if self.global_scale:
            cmds.scaleConstraint(self.global_scale, self.rig_parent, mo = True)
            cmds.scaleConstraint(self.global_scale, self.skel_parent, mo = True)

    def __cleanup(self):
        if self.debug == False:
            misc.suffix_constraints()
            misc.lock_all(hierarchy = self.rig_parent, filter = ["*_CTL", "*_JNT", "*_HELP"])
            misc.lock_all(hierarchy = self.skel_parent, filter = ["*_CTL", "*_JNT", "*_HELP"])

    def __create(self):
        self.__check()
        self.__create_parents()
        self.__create_bind_skel()
        self.__create_ctl()
        self.__rig_foot()
        self.__create_ik_skel()
        self.__create_attrs()
        self.__connect_attrs()
        self.__drive_rig()
        self.__cleanup()