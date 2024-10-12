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
#CLASS:         create_neck
#DESCRIPTION:   Creates neck rig
#USAGE:         set arguments for neck
#RETURN:        skel_joint, ctl, ctl_buffers, ctl_gimbal
#REQUIRES:      utils.misc, maya.cmds, sys
#AUTHOR:        Levi Harrison
#DATE:          Oct 21th, 2014
#Version        1.0.0
#===============================================================================

class create_neck():
    def __init__(self,
                 side = "C",
                 name = "neck",
                 joint = "neck_bind",
                 driver = "",
                 global_scale = "",
                 skel_parent = "C_skeleton_GRP",
                 rig_parent = "C_rig_GRP",
                 ctl_size = 1.0,
                 orient = [0,0,0],
                 offset = [0,0,0],
                 debug = False,
                 ):
        """
        type  side:                string
        param side:                usually C but L or R are also supported

        type  name:                string
        param name:                the names of your neck

        type  joint:               string array
        param joint:               the neck joint that the rig will drive

        type  driver:              string
        param driver:              what the neck will be attached to
                                    usually the chest joint but anything that
                                    exists will work

        type  global_scale:        string
        param global_scale:        what the neck will be attached to
                                    for scaling usually lowest point in
                                    hierarchy of global ctl


        type  skel_parent:          string
        param skel_parent:          where to parent newly created joints,
                                     effectors, and generally things animators
                                     don't want to see.

        type  rig_parent:           string
        param rig_parent:           where to parent ctls and other things
                                     animators would like to see

        type  ctl_size:             float
        param ctl_size:             a size for the neck control

        type  debug:                bool
        param debug:                if debug is on, nothing will be locked and
                                     ihi will remain 1
        """

        #---arg vars
        self.side                   = side
        self.name                   = name
        self.joint                  = joint
        self.driver                 = driver
        self.global_scale           = global_scale
        self.skel_parent            = skel_parent
        self.rig_parent             = rig_parent
        self.ctl_size               = ctl_size
        self.debug                  = debug
        self.orient                 = orient
        self.offset                 = offset

        #---vars
        self.skel_joint              = ""
        self.ctl                     = []
        self.ctl_buffers             = []
        self.ctl_gimbal              = []

        self.__create()

    def __check(self):
        """ makes sure first three indexes in self.joints are joints """
        if cmds.objExists(self.joint):
            if cmds.nodeType(self.joint) != "joint":
                raise Exception(self.joint + " must be a joint")
                quit()
        else:
            raise Exception(self.joint + " does not exist")
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
                                          "_neckSkel_GRP",
                                          p = self.skel_parent)
        
        self.rig_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_neckRig_GRP",
                                          p = self.rig_parent)

    def __create_bind_skel(self):
        """ create control and snap to neck """
        self.skel_joint = cmds.createNode("joint", 
                                          n = self.side + "_" 
                                          + self.name
                                          + "_JNT",
                                          parent = self.skel_parent)
        con = cmds.parentConstraint(self.joint,
                                    self.skel_joint)
        cmds.delete(con)
        cmds.makeIdentity(self.skel_joint,
                          apply = True, t=0, r=1, s = 1, n=0, pn=1)

        cmds.addAttr(self.skel_joint, ln = "BIND",
                         at = "bool",)
        cmds.setAttr(self.skel_joint+".BIND", l = True, k=False)

    def __create_ctl(self):
        """ create control and snap to neck """
        tmp_ctl = control_base.create_ctl(side = self.side, 
                                  name = self.name, 
                                  parent = self.rig_parent, 
                                  shape = "circle", 
                                  lock_attrs = ["sx","sy","sz","v"], 
                                  num_buffer = 3,
                                  gimbal = True,
                                  show_rot_order = True, 
                                  size = self.ctl_size, 
                                  orient = self.orient,
                                  offset = self.offset)
        self.ctl = tmp_ctl.ctl
        self.ctl_buffers = tmp_ctl.buffers
        self.ctl_gimbal = tmp_ctl.gimbal_ctl
        con = cmds.parentConstraint(self.skel_joint, self.ctl_buffers[0])
        cmds.delete(con)

    def __rig_neck(self):
        cmds.parentConstraint(self.ctl_gimbal, self.skel_joint)
        #---neck align
        misc.create_fk_align(ctl = self.ctl, 
                             ctl_grp = self.ctl_buffers
                             [len(self.ctl_buffers) - 1],
                             default_align_parent = self.ctl_buffers
                             [len(self.ctl_buffers) - 2],
                             skel_group = self.skel_parent)

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
            misc.lock_all(hierarchy = self.rig_parent, filter = ["*_CTL", "*_JNT"])
            misc.lock_all(hierarchy = self.skel_parent, filter = ["*_CTL", "*_JNT"])

    def __create(self):
        self.__check()
        self.__create_parents()
        self.__create_bind_skel()
        self.__create_ctl()
        self.__rig_neck()
        self.__drive_rig()
        self.__cleanup()