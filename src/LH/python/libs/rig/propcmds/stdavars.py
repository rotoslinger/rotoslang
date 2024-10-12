import sys
import importlib
from maya import cmds
from rig.utils import misc
from rig.control import base as control_base
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)
importlib.reload(control_base)
importlib.reload(misc)

#===============================================================================
#CLASS:         create_stdavar_ctrl
#DESCRIPTION:   creates a global and local ctrl for moving a standard rig
#USAGE:         set args and run
#RETURN:        groups
#REQUIRES:      maya.cmds, utils.misc
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================


class create_stdavar_ctrl():
    def __init__(self,
                 side = "C",
                 skel_parent = "C_skeleton_GRP",
                 rig_parent = "C_rig_GRP",
                 ctrl_parent = "C_control_GRP",
                 ctrl_sizes = [1.0, 1.0, 1.0],
                 colors = [ 
                            (1.0, 1.0, 0.0),
                            (0.1, 0.75, 0.7),
                            (0.5, 0.5, 0.0)
                          ],
                 ty_offsets = [0,0,0],
                 #create_bone = False,
                 ctrl_names = ["World", "Layout", "Root"],
                 ctrls_with_bones = [False, False, True],
                 create_buffer_shape = True,
                 debug = False,
                 model_hier = "", # this is the model_hier that will be parented to C_geo_Group
                 ):

        """
        type  side:                string
        param side:                usually C but L or R are also supported

        type  skel_parent:          string
        param skel_parent:          where to parent newly created joints,
                                     effectors, and generally things animators
                                     don't want to see.

        type  rig_parent:           string
        param rig_parent:           where to parent ctrls and other things
                                     animators would like to see

        type  ctrl_sizes:            float array
        param ctrl_sizes:            sizes for the global & local controls

        type  debug:                bool
        param debug:                if debug is on, nothing will be locked and
                                     ihi will remain 1
        """

        #---arg vars
        self.side                   = side
        self.skel_parent            = skel_parent
        self.rig_parent             = rig_parent
        self.ctrl_parent            = ctrl_parent
        self.ctrl_sizes             = ctrl_sizes
        self.create_buffer_shape    = create_buffer_shape
        self.debug                  = debug
        self.ty_offsets             = ty_offsets
        self.colors                 = colors
        #self.create_bone           = create_bone
        self.ctrls_with_bones       = ctrls_with_bones
        self.ctrl_names             = ctrl_names
        self.world_ctrl = ""
        self.layout_ctrl = ""
        self.root_ctrl = ""
        #---vars
        self.ctrls                  = []
        self.ctrl_buffers           = []
        self.ctrl_gimbals           = []
        self.mdlsiz_attr            = []
        self.__create()

    def __check(self):
        for i in [self.skel_parent, self.rig_parent]:
            if not cmds.objExists(i):
                raise Exception(i + " does not exist")
                quit()

    def __create_parents(self):
        """ create groups for skeleton and rig """
        pass

    def __create_ctrls(self):
        """ create ctrls """
        self.root_joint = ""
        create_buffer_shape = [False, False, True]
        for index in range(len(self.ctrl_names)):
            if index == 0 & self.debug != 1:
                parent = self.ctrl_parent

                # parent = self.rig_parent
                lock_attrs = ["v"],
            else: parent = self.ctrls[index-1]
            if index == 1:
                lock_attrs = ["sx", "sy", "sz", "v"],
            return_ctrl = control_base.create_ctl(side = self.side, 
                                                name = self.ctrl_names[index], 
                                                parent = parent, 
                                                shape = "circle",
                                                num_buffer = 1,
                                                lock_attrs = lock_attrs[0], 
                                                gimbal = False,
                                                size = self.ctrl_sizes[index],
                                                color = self.colors[index],
                                                offset = [0,self.ty_offsets[index],0],
                                                orient = [0,0,90],
                                                create_buffer_shape=create_buffer_shape[index],
                                                create_joint = self.ctrls_with_bones[index],
                                                )
            self.ctrls.append(return_ctrl.ctl)
            self.ctrl_buffers.append(return_ctrl.buffers)
            if return_ctrl.joint:
                self.root_joint = return_ctrl.joint
                tag_utils.tag_rootskel_joint(self.root_joint)
                bind_jnt_grp = tag_utils.get_all_with_tag("BIND_JOINT_GRP", hint_list=None)[0]
                cmds.parent(self.root_joint, bind_jnt_grp)

            
            # self.ctrl_gimbals.append(return_ctl.gimbal_ctl)
        self.world_ctrl = self.ctrls[0]
        self.layout_ctrl = self.ctrls[1]
        self.root_ctrl = self.ctrls[2]


    def __create_mdlsiz(self):
        """ create global scale attr, wire it up"""
        cmds.addAttr(self.ctrls[0],
                     ln = "mdlsiz", 
                     at = "float", 
                     dv = 1,
                     min = 0,
                     k = True)
        self.mdlsiz_attr = self.ctrls[0] + ".mdlsiz"
        cmds.connectAttr(self.mdlsiz_attr, self.ctrls[0] + ".sx")
        cmds.connectAttr(self.mdlsiz_attr, self.ctrls[0] + ".sy")
        cmds.connectAttr(self.mdlsiz_attr, self.ctrls[0] + ".sz")
        misc.lock_attrs(node = self.ctrls[0], attr = ["sx", "sy", "sz"])


    def __cleanup(self):
        if self.debug == False:
            misc.lock_all(hierarchy = self.rig_parent, filter = ["*_CTL"])
            misc.lock_all(hierarchy = self.skel_parent, filter = ["*_CTL"])

    def __create(self):
        self.__check()
        self.__create_parents()
        self.__create_ctrls()
        self.__create_mdlsiz()
        self.__cleanup()