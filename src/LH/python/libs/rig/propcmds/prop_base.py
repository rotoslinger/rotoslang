import sys
import importlib
import re
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
                 create_wire_deformer=False,
                 wire_deformer_root_name=None, # if creating the wire deformer, the curve and curve base must be parented here in order to prevent flipping when the component is rotated.
                 wire_ctrl_scale_factor = 1.5,
                 wire_ctrl_color = (1,1,0),
                 wire_deformer_geom = "",
                 # These are todo: These will align the control shape
                 # Then use aim constraints to orient the buffers
                 primary_axis = "X", # unless mirrored, then -X
                 secondary_axis = "Y", # up 
                 world_up_object = None,
                 floating_ctrls = False,
                 # Add functionality to inherit transforms
                 ):

        """
        type  side:                        string
        param side:                        usually C but L or R are also supported

        type  skel_parent:                 string
        param skel_parent:                 where to parent newly created joints,
                                            effectors, and generally things animators
                                            don't want to see.

        type  rig_parent:                  string
        param rig_parent:                  where to parent ctrls and other things
                                            animators would like to see

        type  ctrl_sizes:                  float array
        param ctrl_sizes:                  sizes for the global & local controls

        type  debug:                       bool
        param debug:                       if debug is on, nothing will be locked and
                                            ihi will remain 1

        type  create_wire_deformer:        bool
        param create_wire_deformer:        if True, a curve will be created with CVs 
                                            at every joint, then a wire deformer will 
                                            be created. This curve will be parented to
                                            a new control which is named after the arg
                                            wire_deformer_root_name.

        type  wire_deformer_root_name:     string
        param wire_deformer_root_name:     the name you would like to give the control
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
        self.wire_deformer_geom     = wire_deformer_geom
        # TODO: Add orientation options.
        # Right now I am using ctrl_rotation to orient the controls.
        # This is a temporary solution, and does not take into account mirroring.
        # In order to get mirrored rotations the control buffer will need to have its x axis scaled to -1 this has to be done by hand :(
        self.primary_axis           = primary_axis
        self.secondary_axis         = secondary_axis
        self.world_up_object        = world_up_object

        self.floating_ctrls         = floating_ctrls
        self.wire_ctrl_scale_factor = wire_ctrl_scale_factor
        self.wire_ctrl_color        = wire_ctrl_color

        #---vars
        self.ctrls                  = []
        self.ctrl_buffers           = []
        self.ctrl_shapes            = []

        self.ctrl_gimbals           = []
        self.joints                 = []
        self.shape_size_attr        = []
        self.curve_parent           = ""

        self.__create()

    def __create(self):
        self.__check()
        self.__create_ctrls()
        if self.create_wire_deformer:
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
        # self.ctrl_buffers = []
        chained_pos_off_count = self.chained_pos_offset
        
        # TODO need to check that we at least have 3 controls in ctrl names if making a wire deformer.

        '''
        If you are creating a wire deformer, you will need a root control to move all of the child controls around.
        Whether the component is a chain, or a group of controls, you will need all of these controls to be parented to the root
        By default, the
        '''
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

        if not self.wire_ctrl_scale_factor: self.wire_ctrl_scale_factor = 1.5,
        if not self.wire_ctrl_color: self.wire_ctrl_color = (1,1,0),

        self.wire_ctrl_scale_factor = 1.5
        self.wire_ctrl_color = (1,1,0)
        if self.create_wire_deformer:
            if self.wire_deformer_root_name == None:
                # using  re.sub to remove all digits for example: re.sub(r'\d+', '', string)
                # the '\d' is a shorthand character class for digits
                # the '+' in '\d+' --- the + is an iterator or quantifier in (re) regular expressions, and it modifies how many times the preceding pattern (in this case, \d) can occur.
                # A single + is a lazy aka greedy quantifier. It requires less work and is 'safer' in that you can backtrack(find a partial match).
                # Backtracking can be fatal or cause performance problems if it happens too much. In this simple case however, there won't be an issue.
                first_control_name = self.ctrl_names[0]
                # wire_root_tmp = re.sub(r'\d+', '', first_control_name)
                self.wire_deformer_root_name = first_control_name + 'WireCtrlRoot'
            self.ctrl_sizes.insert(0, self.ctrl_sizes[0] * self.wire_ctrl_scale_factor)
            self.colors.insert(0, self.wire_ctrl_color)
            self.ctrl_names.insert(0, self.wire_deformer_root_name)


        if len(self.ctrl_sizes) > 0 < len(self.ctrl_names):
            # get the index at which the last color was specified - start the loop here
            # color every color the same as the last specified color
            # I am going to be lazy and expand the list as big as the names, even though that is too many, will fix if this ever becomes a speed issue (it won't)
            start_index = len(self.ctrl_sizes)
            for idx in range(len(self.ctrl_names)):
                self.ctrl_sizes.append(self.ctrl_sizes[start_index-1])

        tmp_x, tmp_y, tmp_z = self.root_pos_offset

        rx,ry,rz = self.ctrl_rotation
        


        for index in range(len(self.ctrl_names)):
            # print(self.ctrl_names[index] + " This is index " + str(index))
            if index == 0:
                parent = self.parent_hook
                lock_attrs = ["v"],
                # print("INDEX IS "+  str(index)+" INDEX == 0")

            elif self.floating_ctrls:
                if not self.create_wire_deformer:
                    pass # --- just leave the parent
                else:
                    parent = self.ctrls[0] # --- needs to float inside the root ctrl which is at ctrls index 0
                    # print("IS FLOATING AND CREATING WIRE DEFORMER")
            else:
                parent = self.ctrls[index-1]  # ---Nested hierarchy
                print("IS WORKING and not floating!!!")

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
            if self.root_pos_offset != (0,0,0) and index==0:  # if no chained, make sure to still do the root! (if not nuetral)
                cmds.move( tmp_x, tmp_y,tmp_z, return_ctrl.buffers_parent, worldSpace=True)
                print("MOVING OFFSET ")
            if index == 0:
                cmds.setAttr(return_ctrl.buffers_parent + ".rx", rx)
                cmds.setAttr(return_ctrl.buffers_parent + ".ry", ry)
                cmds.setAttr(return_ctrl.buffers_parent + ".rz", rz)
            else:
                cmds.setAttr(return_ctrl.buffers_parent + ".rx", 0)
                cmds.setAttr(return_ctrl.buffers_parent + ".ry", 0)
                cmds.setAttr(return_ctrl.buffers_parent + ".rz", 0)
            if self.floating_ctrls and not self.create_wire_deformer:
                cmds.setAttr(return_ctrl.buffers_parent + ".rx", rx)
                cmds.setAttr(return_ctrl.buffers_parent + ".ry", ry)
                cmds.setAttr(return_ctrl.buffers_parent + ".rz", rz)
                
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
            if index == 0 and self.create_wire_deformer:
                self.curve_parent = self.ctrls[0]
                
    def __create_wire_deformer(self):
        # must have at least 3 controls
        self.wire_curve=""
        self.clusters = []
        self.__draw_curve()
        self.__create_clusters()
        # create wire deformer....
        self.wire_deformer = ""
        # self.wire_base = cmds.duplicate(self.wire_curve)[0]
        # cmds.setAttr(self.wire_base + ".inheritsTransform",1)
        # cmds.rename(self.wire_base, self.wire_base + "BASE")
        # self.wire_base =  self.wire_base + "BASE"
        # print("WIRE BASE " + str(self.wire_base))


        # if self.wire_deformer_geom:
        #     self.wire_deformer=cmds.wire(self.wire_deformer_geom, self.wire_curve)

    def __draw_curve(self):
        knots = []
        self.points = []
        self.final_point_count =len(self.joints)-1
        for idx in range(self.final_point_count):
            # i =
            i=idx+1
            self.points.append(tuple(cmds.xform(self.joints[i],
                                     q =True,
                                     ws=True,
                                     t=True)))
            knots.append(idx)
        degree = 2
        knot_list = get_knot_list(self.final_point_count, degree=degree)
        print(knot_list)
        self.wire_curve = cmds.curve(n = (self.side
                                     + "_"
                                     + self.wire_deformer_root_name
                                     + "SplineIK_CRV"),
                                degree = degree,
                                p = self.points,
                                k = knot_list)
        print("CURVE NAME " + str(self.wire_curve))
        cmds.setAttr(self.wire_curve + ".inheritsTransform",0)
        cmds.parent(self.wire_curve,
                    self.curve_parent)
        # self.wire_base = cmds.duplicate(self.wire_curve)[0]
        # cmds.setAttr(self.wire_base + ".inheritsTransform",1)
        # cmds.rename(self.wire_base, self.wire_base + "BASE")
        # self.wire_base =  self.wire_base + "BASE"
        # print("WIRE BASE " + str(self.wire_base))




    def __create_clusters(self):
        tmp_cluster_ctls = []
        for idx in range(self.final_point_count):
            i = idx+1
            self.clusters.append(cmds.cluster(self.wire_curve
                                            + ".cv["
                                            + str(idx)
                                            + "]",
                                            name = (self.side
                                                    + "_"
                                                    + self.wire_deformer_root_name
                                                    + str(idx)
                                                    + "_CLS"),
                                            wn = (self.ctrls[i],
                                                    self.ctrls[i]),
                                            bindState=True))
            cmds.rename("clusterHandleShape",
                        self.side + "_" + self.wire_deformer_root_name + str(idx) + "_CLS" + "Shape")



    def __create_shape_size(self):
        ''' this is now in base, done in the draw_ctls class'''
        """ create global scale attr, wire it up"""
        for buffer in self.ctrl_buffers:
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




def get_knot_list(num_points, degree=3):
    """
    degree(d)
    The degree of the new curve. Default is 3. Note that you need (degree+1) curve points to create a visible curve span. eg. you must place 4 points for a degree 3 curve.
    knot(k)	
    A knot value in a knot vector. One flag per knot value. There must be (numberOfPoints + degree - 1) knots and the knot vector must be non-decreasing.

    """

    num_knots = num_points + degree -1
    num_betweens = num_knots - degree * 2

    start_num = 0
    end_num = num_betweens+2
    start_indices = []
    middle_indices = []
    end_indices = []
    for indice in range(degree):
        start_indices.append(start_num)
    for indice in range(num_betweens):
        middle_indices.append(indice + (degree-1))
    for indice in range(degree):
        end_indices.append(end_num)
    knot_list = start_indices + middle_indices + end_indices
    print("num_knots ", str(num_knots))
    print("num_betweens ", str(num_betweens))
    print("Final", str(knot_list))
    print("Middle", str(middle_indices))
    # (number of CVs + degree - 1) knots and that the knot

    return knot_list



