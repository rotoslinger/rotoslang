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
#CLASS:         create_global_ctl
#DESCRIPTION:   creates a global and local ctl for moving a standard rig
#USAGE:         set args and run
#RETURN:        groups
#REQUIRES:      maya.cmds, utils.misc
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class create_global_ctl():
    def __init__(self,
                 side = "C",
                 skel_parent = "C_skeleton_GRP",
                 rig_parent = "C_rig_GRP",
                 ctl_sizes = [1.0,1.0],
                 debug = False,
                 ):

        """
        type  side:                string
        param side:                usually C but L or R are also supported

        type  skel_parent:          string
        param skel_parent:          where to parent newly created joints,
                                     effectors, and generally things animators
                                     don't want to see.

        type  rig_parent:           string
        param rig_parent:           where to parent ctls and other things
                                     animators would like to see

        type  ctl_sizes:            float array
        param ctl_sizes:            sizes for the global & local controls

        type  debug:                bool
        param debug:                if debug is on, nothing will be locked and
                                     ihi will remain 1
        """

        #---arg vars
        self.side                   = side
        self.skel_parent            = skel_parent
        self.rig_parent             = rig_parent
        self.ctl_sizes              = ctl_sizes
        self.debug                  = debug

        #---vars
        self.ctls                   = []
        self.ctl_buffers            = []
        self.ctl_gimbals            = []
        self.global_scale_attr      = []

        self.__create()

    def __check(self):
        for i in [self.skel_parent, self.rig_parent]:
            if not cmds.objExists(i):
                raise Exception(i + " does not exist")
                quit()

    def __create_parents(self):
        """ create groups for skeleton and rig """
        self.skel_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_globalSkel_GRP",
                                          p = self.skel_parent)
        self.rig_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_globalRig_GRP",
                                          p = self.rig_parent)

    def __create_ctls(self):
        """ create ctls """
        names = ["global", "local"]
        for i in range(len(names)):
            if i == 0:
                parent = self.rig_parent
                lock_attrs = ["v"], 
            if i == 1:
                parent = self.ctl_gimbals[0]
                lock_attrs = ["sx", "sy", "sz", "v"], 
            return_ctl = control_base.create_ctl(side = self.side, 
                                                name = names[i], 
                                                parent = parent, 
                                                shape = "circle",
                                                num_buffer = 1,
                                                lock_attrs = lock_attrs[0], 
                                                gimbal = True,
                                                size = self.ctl_sizes[i],
                                                orient = [0,0,90])
            self.ctls.append(return_ctl.ctl)
            self.ctl_buffers.append(return_ctl.buffers)
            self.ctl_gimbals.append(return_ctl.gimbal_ctl)

    def __create_global_scale(self):
        """ create global scale attr, wire it up"""
        cmds.addAttr(self.ctls[0],
                     ln = "global_scale", 
                     at = "float", 
                     dv = 1,
                     min = 0,
                     k = True)
        self.global_scale_attr = self.ctls[0] + ".global_scale"
        cmds.connectAttr(self.global_scale_attr, self.ctls[0] + ".sx")
        cmds.connectAttr(self.global_scale_attr, self.ctls[0] + ".sy")
        cmds.connectAttr(self.global_scale_attr, self.ctls[0] + ".sz")
        misc.lock_attrs(node = self.ctls[0], attr = ["sx", "sy", "sz"])

    def __cleanup(self):
        if self.debug == False:
            misc.lock_all(hierarchy = self.rig_parent, filter = ["*_CTL"])
            misc.lock_all(hierarchy = self.skel_parent, filter = ["*_CTL"])

    def __create(self):
        self.__check()
        self.__create_parents()
        self.__create_ctls()
        self.__create_global_scale()
        self.__cleanup()