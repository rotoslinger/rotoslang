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

class simple_component():
    def __init__(self,
                 side = "C",
                 parent_hook = "",
                 skel_parent = "C_skeleton_GRP",
                 rig_parent = "C_rig_GRP",
                 ctrl_parent = "C_control_GRP",
                 ctrl_sizes = [1.0, 1.0, 1.0],
                 colors = None,  # [(1,1,0), (1,1,0), (1,1,0)]
                #  ty_offsets = [0,0,0] # just an offset in ty.
                 #create_bone = False,
                 ctrl_names = ["ControlA"], # ["ControlA", "ControlB", "ControlC"]
                 create_joints = True,
                 chained_pos_offset= (0,1,0), # by default this is going to increase in Y
                 root_pos_offset= (1,0,0), # this moves the root to an offset location
                 create_buffer_shape = True,
                 joint_parent = None, #if set to None automatically parent to root
                 ctrl_shape_orient = (0,0,0), #this is just the control wire orientation.
                 ctrl_rotation = (0, 0, 0), # this is the root of the chain rotation. All children will be oriented with an rx,ry,rz offset of 0, to inherit the root's rotation.
                 debug = False,
                 create_wire_deformer=True,
                 wire_deformer_root_name="ControlARoot", # if creating the wire deformer, the curve and curve base must be parented here in order to prevent flipping when the component is rotated.
                 # These are todo: These will align the control shape
                 # Then use aim constraints to orient the buffers
                 primary_axis = "X", # unless mirrored, then -X
                 secondary_axis = "Y", # up 
                 world_up_object = None,
                 floating_ctrls = False,
                 # Add functionality to inherit transforms
                 ):

        """
        @type  side:                        string
        @param side:                        usually C but L or R are also supported

        @type  skel_parent:                 string
        @param skel_parent:                 where to parent newly created joints,
                                            effectors, and generally things animators
                                            don't want to see.

        @type  rig_parent:                  string
        @param rig_parent:                  where to parent ctrls and other things
                                            animators would like to see

        @type  ctrl_sizes:                  float array
        @param ctrl_sizes:                  sizes for the global & local controls

        @type  debug:                       bool
        @param debug:                       if debug is on, nothing will be locked and
                                            ihi will remain 1

        @type  create_wire_deformer:        bool
        @param create_wire_deformer:        if True, a curve will be created with CVs 
                                            at every joint, then a wire deformer will 
                                            be created. This curve will be parented to
                                            a new control which is named after the arg
                                            wire_deformer_root_name.

        @type  wire_deformer_root_name:     string
        @param wire_deformer_root_name:     the name you would like to give the control
                                            where the the curve and curve base will be
                                            parented.
                                            
                                            If None split any numbers out of 
                                            the first control's name and append the word
                                            "Root". For example: ControlARoot.
                                            
                                            This control will be created in addition to
                                            the specified controls.  It will be parented
                                            under the parent_hook arg, then all of the 
                                            controls will be parented here instead of the
                                            parent_hook.
                                            





                                      if creating the wire deformer, the curve and curve base must be parented here in order to prevent flipping when the component is rotated.
        """

        #---arg vars
        self.side                   = side
        self.parent_hook            = parent_hook
        self.skel_parent            = skel_parent
        self.rig_parent             = rig_parent
        self.ctrl_parent            = ctrl_parent
        self.ctrl_sizes             = ctrl_sizes
        self.chained_pos_offset     = chained_pos_offset
        self.root_pos_offset        = root_pos_offset
        self.create_buffer_shape    = create_buffer_shape
        self.debug                  = debug
        # self.ty_offsets             = ty_offsets # This will be done by hand right now, no good procedural way to do this.
        self.colors                 = colors
        self.create_joints          = create_joints
        self.ctrl_names             = ctrl_names
        self.joint_parent           = joint_parent
        self.ctrl_shape_plane       = ctrl_shape_orient
        self.ctrl_rotation          = ctrl_rotation
        self.create_wire_deformer   = create_wire_deformer
        self.wire_deformer_root_name=wire_deformer_root_name
        # TODO: Add orientation options.
        # Right now I am using ctrl_rotation to orient the controls.
        # This is a temporary solution, and does not take into account mirroring.
        # In order to get mirrored rotations the control buffer will need to have its x axis scaled to -1 this has to be done by hand :(
        self.primary_axis           = primary_axis
        self.secondary_axis         = secondary_axis
        self.world_up_object        = world_up_object

        self.floating_ctrls         = floating_ctrls

        #---vars
        self.ctrls                  = []
        self.ctrl_buffers           = []
        self.ctrl_shapes     = []

        self.ctrl_gimbals           = []
        self.joints                 = []
        self.shape_size_attr        = []
        self.__create()

    def __create(self):
        self.__check()
        self.__create_ctrls()
        self.__create_wire_deformer()
        #self.__create_shape_size()
        self.__tag()
        self.__cleanup()


    def __check(self):
        for i in [self.skel_parent, self.rig_parent]:
            if not cmds.objExists(i):
                raise Exception(i + " does not exist")
                quit()
        # for index, arg in ["Keyword arg ctrl_names, value ", "Keyword arg ctrl_sizes "]:
        #     if type(arg) != list:
        #         raise Exception(arg + check_lists[index] + " should be a list, make sure you haven't missed any [] ")

    def __create_ctrls(self):
        """ create ctrls """
        self.ctrl_buffers = []
        chained_pos_off_count = self.chained_pos_offset
        
        # TODO need to check that we at least have 3 controls in ctrl names if making a wire deformer.

        if len(self.colors) > 0 < len(self.ctrl_names):
            # get the index at which the last color was specified - start the loop here
            # color every color the same as the last specified color
            # I am going to be lazy and expand the list as big as the names, even though that is too many, will fix if this ever becomes a speed issue (it won't)
            start_index = len(self.colors)
            for idx in range(len(self.ctrl_names)):
                self.colors.append(self.colors[start_index-1])
        # Yellow if none
        if not self.colors:
            self.colors = []
            for name in self.ctrl_names:
                self.colors.append((1,1,0))

        if len(self.ctrl_sizes) > 0 < len(self.ctrl_names):
            # get the index at which the last color was specified - start the loop here
            # color every color the same as the last specified color
            # I am going to be lazy and expand the list as big as the names, even though that is too many, will fix if this ever becomes a speed issue (it won't)
            start_index = len(self.ctrl_sizes)
            for idx in range(len(self.ctrl_names)):
                self.ctrl_sizes.append(self.ctrl_sizes[start_index-1])

        tmp_x, tmp_y, tmp_z = self.root_pos_offset

        rx,ry,rz = self.ctrl_rotation

        '''
        If you are creating a wire deformer, you will need a root control to move all of the child controls around.
        Whether the component is a chain, or a group of controls, you will need all of these controls to be parented to the root
        By default, the
        '''
        for index in range(len(self.ctrl_names)):
            if index == 0 & self.debug != 1:
                parent = self.parent_hook
                lock_attrs = ["v"],
            elif self.floating_ctrls: self.parent_hook
            else: parent = self.ctrls[index-1]  # ---Nested hierarchy
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
                                                offset = [0,0,0],
                                                orient = self.ctrl_shape_plane,
                                                create_joint = self.create_joints,
                                                create_buffer_shape = True
                                                )
            # Move offsets to make it easier to find
            if self.chained_pos_offset != (0,0,0):
                x = (chained_pos_off_count[0] * (index + 1)) + tmp_x
                y = (chained_pos_off_count[1] * (index + 1)) + tmp_y
                z = (chained_pos_off_count[2] * (index + 1)) + tmp_z
                cmds.move( x,y,z, return_ctrl.buffers_parent)
            elif self.root_pos_offset != (0,0,0):  # if no chained, make sure to still do the root! (if not nuetral)
                cmds.move( tmp_x, tmp_y,tmp_z, return_ctrl.buffers_parent)
            if index == 0:
                cmds.setAttr(return_ctrl.buffers_parent + ".rx", rx)
                cmds.setAttr(return_ctrl.buffers_parent + ".ry", ry)
                cmds.setAttr(return_ctrl.buffers_parent + ".rz", rz)
            else:
                cmds.setAttr(return_ctrl.buffers_parent + ".rx", 0)
                cmds.setAttr(return_ctrl.buffers_parent + ".ry", 0)
                cmds.setAttr(return_ctrl.buffers_parent + ".rz", 0)

                # cmds.rotate(rot_val[0],rot_val[1],rot_val[2], return_ctrl.buffers_parent)

            self.ctrl_shapes.append(return_ctrl.shape_node)
            self.ctrls.append(return_ctrl.ctl)
            self.ctrl_buffers.append(return_ctrl.buffers)
            self.joints.append(return_ctrl.joint)

            if index == 0:
                joint_parent = self.joint_parent
                if not joint_parent:
                    joint_parent = tag_utils.get_all_with_tag("ROOT_SKEL_JOINT", hint_list = cmds.ls(type="joint"))[0]
                cmds.parent(self.joints[index], joint_parent)
            if index > 0:
                cmds.parent(self.joints[index], self.joints[index-1])
    def __create_wire_deformer(self):
        # must have at least 3 controls
        self.wire_curve=""
        for ctrl in self.ctrls:
            print(ctrl)
        pass







    def __draw_curve(self):
        knots = []
        for i in range(len(self.joints)):
            self.points.append(tuple(cmds.xform(self.joints[i],
                                     q =True,
                                     ws=True,
                                     t=True)))
            knots.append(i)
        self.curve = cmds.curve(n = (self.side
                                     + "_"
                                     + self.name
                                     + "SplineIK_CRV"),
                                d = 1,
                                p = self.points,
                                k = knots)
        if self.inherit_transform == False:
            cmds.setAttr(self.curve + ".inheritsTransform",0)
        cmds.parent(self.curve,
                    self.curve_parent)

    def __create_clusters(self):
        tmp_cluster_ctls = []
        for i in range(len(self.joints)):

            self.clusters.append(cmds.cluster(self.curve
                                               + ".cv["
                                               + str(i)
                                               + "]",
                                              name = (self.side
                                                      + "_"
                                                      + self.name
                                                      + str(i)
                                                      + "_CLS"),
                                              wn = (tmp_cluster_ctls[i].ctl,
                                                    tmp_cluster_ctls[i].ctl,),
                                              bindState=True))
            cmds.rename("clusterHandleShape",
                        self.side + "_" + self.name + str(i) + "_CLS" + "Shape")



    def __create_shape_size(self):
        """ create global scale attr, wire it up"""
        # print("BUFFERS", str(self.ctrl_buffers))
        for buffer in self.ctrl_buffers:
            # print("THIS IS THE CURRENT BUFFER", buffer)

            buffer = buffer[0] # --- only do it to the first buffer
            cmds.addAttr(buffer,
                        ln = "ctrl_siz", 
                        at = "float", 
                        dv = 1,
                        min = 0,
                        k = True)
            shape_size_attr = buffer + ".ctrl_siz"

    def __tag(self):
        # this is for doing any component specific tagging.
        # Remember, controls, buffers, and joints automatically get tagged in base
        pass

    def __cleanup(self):
        if self.debug == False:
            misc.lock_all(hierarchy = self.rig_parent, filter = ["*_CTL"])
            misc.lock_all(hierarchy = self.skel_parent, filter = ["*_CTL"])







'''
For curve deform creation:
    def __draw_curve(self):
        knots = []
        for i in range(len(self.joints)):
            self.points.append(tuple(cmds.xform(self.joints[i],
                                     q =True,
                                     ws=True,
                                     t=True)))
            knots.append(i)
        self.curve = cmds.curve(n = (self.side
                                     + "_"
                                     + self.name
                                     + "SplineIK_CRV"),
                                d = 1,
                                p = self.points,
                                k = knots)
        if self.inherit_transform == False:
            cmds.setAttr(self.curve + ".inheritsTransform",0)
        cmds.parent(self.curve,
                    self.curve_parent)

    def __create_clusters(self):
        tmp_cluster_ctls = []
        for i in range(len(self.joints)):

            self.clusters.append(cmds.cluster(self.curve
                                               + ".cv["
                                               + str(i)
                                               + "]",
                                              name = (self.side
                                                      + "_"
                                                      + self.name
                                                      + str(i)
                                                      + "_CLS"),
                                              wn = (tmp_cluster_ctls[i].ctl,
                                                    tmp_cluster_ctls[i].ctl,),
                                              bindState=True))
            cmds.rename("clusterHandleShape",
                        self.side + "_" + self.name + str(i) + "_CLS" + "Shape")




'''