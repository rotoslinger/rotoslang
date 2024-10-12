import copy
from maya import cmds

from rig_2.message import utils as message_utils
import importlib
importlib.reload(message_utils)

from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)
from rig_2.manipulator import elements
importlib.reload(elements)
from rig_2.shape import nurbscurve
importlib.reload(nurbscurve)


# from rig_2.manipulator import misc
# reload(misc)
from rig_2.node import utils as node_utils
importlib.reload(node_utils)
from rig_2.misc import utils as misc_utils
importlib.reload(misc_utils)


from rig.utils import misc
importlib.reload(misc)

#===============================================================================
#CLASS:         Shape
#DESCRIPTION:   draws controls
#USAGE:         set args and run
#RETURN:        ctl
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class Shape(object):
    def __init__(self,
                 side="L",
                 name="testControl",
                 parent="",
                 shape_dict = elements.circle,
                 lock_attrs=["v"],
                 show_rot_order= True,
                 size = 1,
                 orient = [0,0,0],
                 offset = [0,0,0],
                 scale = [1,1,1],
                 hide = False,
                 color_side=True,
                 outliner_color=False
                 ):

        """
        type  side:                string
        param side:                side the control is on C,L,R
        
        type  name:                string
        param name:                name of the ctl
        
        type  parent:              string
        param parent:              the transform this will be parented under

        type  shape_dict:          dictionary
        param shape_dict:          a dictionary that can be used to rebuild a nurbs
                                    curve shape check the "shape" module for reference

        type  lock_attrs:          string array
        param lock_attrs:          the attribute names you want locked,
                                    unkeyable, and hidden

        type  show_rot_order:      bool
        param show_rot_order:          if true, rotation order is exposed as a 
                                    non keyable attribute

        type  size:                float
        param size:                average size of all points in ctl in units

        type  orient:              float array
        param orient:              x,y,z values you want to rotate the points
                                    by.  These values will not be reflected in
                                    the transform of the control
        
        type  offset:              float array
        param offset:              x,y,z values you want to translate the 
                                    points by.  These values will not be 
                                    reflected in the transform of the control
                                    
        type  scale:               float array
        param scale:               x,y,z values you want to scale the 
                                    points by.  These values will not be 
                                    reflected in the transform of the control
        type  hide:                bool
        param hide:                if true control visibility will be set to 0
        """

        #---args
        self.side                   = side
        self.name                   = name
        self.parent                 = parent
        self.shape_dict             = shape_dict
        self.lock_attrs             = lock_attrs
        self.show_rot_order         = show_rot_order
        self.size                   = size
        self.orient                 = orient
        self.offset                 = offset
        self.scale                  = scale
        self.hide                   = hide
        self.color_side             = color_side
        self.outliner_color         = outliner_color

        #---vars
        self.ctrl                    = ""
        if self.shape_dict:
            self.shape = ""

    def initialize(self):
        # placeholder until we have naming utils
        if self.side:
            self.full_name = self.side + "_" + self.name
        else:
            self.full_name = self.name
        self.ctrl_name = self.full_name + "_CTL"
        self.ctrl_shape_name = self.full_name + "_CTLShape"

    def create_shape(self):
        self.ctrl, self.ctrl_shapes = nurbscurve.create_curve(curve_dict = self.shape_dict,
                                                              name = self.full_name,
                                                              parent = self.parent,
                                                              color = True,
                                                              outliner_color=self.outliner_color)

    def set_shape_transformations(self):
        shapes = misc_utils.get_shape(self.ctrl)
        for shape in self.ctrl_shapes:
            shape_cvs = shape + ".cv[0:]"
            cmds.scale(self.size, self.size, self.size, 
                    shape_cvs,
                    r = True,ocp=True)
            cmds.move(self.offset[0],
                    self.offset[1],
                    self.offset[2],
                    shape_cvs, 
                    r = True,
                    os=True)
            cmds.scale(self.scale[0],
                    self.scale[1],
                    self.scale[2],
                    shape_cvs, 
                    r = True,ocp=True)
            cmds.rotate(self.orient[0],
                        self.orient[1],
                        self.orient[2],
                        shape_cvs, 
                        r = True,ocp=True)

    def color_it(self):
        if not self.color_side:
            return
        for shape in self.ctrl_shapes:
            cmds.setAttr(shape + ".overrideEnabled", True)
            self.ctrl_color = shape + ".overrideColor"
            cmds.setAttr(shape + ".overrideRGBColors", 1)
            if self.side == "C":
                cmds.setAttr(self.ctrl_color + "R", 1)
                cmds.setAttr(self.ctrl_color + "G", 1)
                cmds.setAttr(self.ctrl_color + "B", 0)
            if self.side == "L":
                cmds.setAttr(self.ctrl_color + "R", 0)
                cmds.setAttr(self.ctrl_color + "G", 0)
                cmds.setAttr(self.ctrl_color + "B", 1)
            if self.side == "R":
                cmds.setAttr(self.ctrl_color + "R", 1)
                cmds.setAttr(self.ctrl_color + "G", 0)
                cmds.setAttr(self.ctrl_color + "B", 0)

    def cleanup(self):
        cmds.delete(self.ctrl, ch = True)
        if self.show_rot_order == True:
            cmds.setAttr(self.ctrl + ".ro", cb = True)

        if self.hide == True:
            cmds.setAttr(self.ctrl + ".v", 0)

        if self.lock_attrs:
            misc_utils.lock_attrs(mayaObject=self.ctrl,
                            attrs=self.lock_attrs,
                            lock = True, 
                            keyable = False, 
                            channelBox = False)

    def create(self):
        ""
        self.initialize()
        self.create_shape()
        self.set_shape_transformations()
        self.color_it()
        self.cleanup()

#===============================================================================
#CLASS:         create_ctl
#DESCRIPTION:   create controls, groups, and gimbal if you need them
#USAGE:         set args and run
#RETURN:        ctl, gimbal_ctrl, buffers, gimbal_vis_attr, buffer_parent
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class Ctrl(object):
    def __init__(self,
                 side="C",
                 name="controlTest",
                 parent="",
                 shape_dict = elements.circle,
                 lock_attrs=["v"],
                 num_buffer = 3,
                 gimbal = True,
                 num_secondary = 0,
                 show_rot_order = True,
                 size = 1,
                 orient = [0,0,0],
                 offset = [0,0,0],
                 scale = [1,1,1],
                 hide = False,
                 null_transform = False,
                 color_side=True,
                 outliner_color=False,
                 ctrl_alias_attr_remap={},
                 guide=False
                 ):

        """
        type  side:                string
        param side:                the side the control is on C,L,R
        
        type  name:                string
        param name:                name of the ctl
        
        type  parent:              string
        param parent:              the transform this will be parented under

        type  shape_dict:          dictionary
        param shape_dict:          a dictionary that can be used to rebuild a nurbs
                                    curve shape check the "shape" module for reference

        type  lock_attrs:          string array
        param lock_attrs:          the attribute names you want locked,
                                    unkeyable, and hidden

        type  num_buffer:          int
        param num_buffer:          number of transforms to group ctl under

        type  gimbal:              bool
        param gimbal:              whether or not you want a gimbal control
                                    not recommended for controls with less than
                                    all 3 rotation attributes
                                    
        type  num_secondary:       bool
        param num_secondary:       creates extra controls which will be
                                    parented under the main ctl
                                    
        type  show_rot_order:      string array
        param show_rot_order:      the attribute names you want locked,
                                    unkeyable, and hidden

        type  size:                float
        param size:                average size of all points in ctl in units

        type  orient:              float array
        param orient:              x,y,z values you want to rotate the points
                                    by.  These values will not be reflected in
                                    the transform of the control

        type  offset:              float array
        param offset:              x,y,z values you want to translate the 
                                    points by.  These values will not be 
                                    reflected in the transform of the control

        type  scale:               float array
        param scale:               x,y,z values you want to scale the 
                                    points by.  These values will not be 
                                    reflected in the transform of the control

        type  hide:                bool
        param hide:                if True control will be hidden
        """

        #---args
        self.side                   = side
        self.name                   = name
        self.parent                 = parent
        # self.shape                  = shape
        self.shape_dict             = shape_dict
        self.lock_attrs             = lock_attrs
        self.num_buffer             = num_buffer
        self.gimbal                 = gimbal
        self.num_secondary          = num_secondary
        self.show_rot_order         = show_rot_order
        self.size                   = size
        self.orient                 = orient
        self.offset                 = offset
        self.scale                  = scale
        self.hide                   = hide
        self.null_transform          = null_transform
        self.color_side             = color_side
        self.outliner_color         = outliner_color
        self.ctrl_alias_attr_remap  = ctrl_alias_attr_remap
        self.guide                  = guide

        #---vars
        self.ctrl                    = ""
        self.gimbal_ctrl             = ""
        self.buffers                = []
        self.gimbal_vis_attr        = ""
        self.buffer_parent          = ""
        self.gimbal_parent          = ""
        self.buffers = []
        self.buffers_ascending = []
        self.buffers_parent = []

    def initialize(self):
        # placeholder until we have naming utils
        if self.side:
            self.full_name = self.side + "_" + self.name
        else:
            self.full_name = self.name

    def create_buffer(self):
        "creates extra transforms to parent the ctls under ascending "
        self.buffers = []
        self.buffers_ascending = []
        self.buffers_parent = []
        self.lastParent = copy.deepcopy(self.parent)
        for idx in reversed(list(range(self.num_buffer))):
            bufferName = "{0}{1:02}_BUF".format(self.full_name, idx)
            # self.lastParent = cmds.createNode("transform", 
            #                               name = bufferName,
            #                               parent = self.lastParent)

            self.lastParent = node_utils.get_node_agnostic(name = bufferName, nodeType="transform", parent=self.lastParent)


            self.buffers.append(self.lastParent)
        self.buffers_ascending = copy.deepcopy(self.buffers)
        self.buffers_ascending.reverse()
        self.buffers_parent =  self.buffers[0]

    def create_ctl(self):
        self.ctrl_shape = Shape(side = self.side,
                            name = self.name,
                            parent = self.lastParent, 
                            shape_dict = self.shape_dict,
                            lock_attrs = self.lock_attrs, 
                            size = self.size,
                            show_rot_order = self.show_rot_order,
                            orient = self.orient,
                            offset = self.offset,
                            scale = self.scale,
                            hide = self.hide,
                            color_side = self.color_side,
                            outliner_color = self.outliner_color)
        self.ctrl_shape.create()     
        self.ctrl = self.ctrl_shape.ctrl
        self.ctrl_shapes = misc_utils.get_shape(self.ctrl)
        self.ctrl_shape = self.ctrl_shapes[0]

        if self.null_transform:
            name = self.ctrl
            parent = misc_utils.get_parent(self.ctrl)
            self.ctrl = cmds.rename(self.ctrl, self.ctrl + "OLD")
            nullTrans = cmds.createNode("nullTransform", n=name, p=parent)
            shape = misc_utils.get_shape(self.ctrl)
            cmds.parent(shape, nullTrans, s=True, r=True)
            cmds.delete(self.ctrl)
            self.ctrl = nullTrans
            misc_utils.lock_attrs(mayaObject=self.ctrl,
                            attrs=self.lock_attrs,
                            lock = True, 
                            keyable = False, 
                            channelBox = False)

    def attr_alias_remap(self):
        """ aliases need to be added before custom attributes are added to the control... """
        if not self.ctrl_alias_attr_remap:
            return
        for attr_alias_name, attr_original_name in self.ctrl_alias_attr_remap.items():
            if not (cmds.objExists(self.ctrl + "." + attr_alias_name)):
                cmds.aliasAttr(attr_alias_name, self.ctrl + attr_original_name)

    def create_secondary(self):
        "creates ctl"
        sec_parent = []
        size = self.size
        self.secondary_ctrls = []
        for i in range(self.num_secondary):
            if i == 0:
                parent = self.ctrl
            else:
                parent = self.secondary_ctrls[i-1]
            size = size / 1.1
            tmp_sec = Shape(side = self.side,
                                name = self.name + str(i),
                                parent = parent, 
                                shape_dict = self.shape_dict,
                                lock_attrs = self.lock_attrs,
                                size = size,
                                show_rot_order = self.show_rot_order,
                                orient = self.orient,
                                offset = self.offset,
                                scale = self.scale,
                                hide = self.hide)
            tmp_sec.create()
            self.secondary_ctrls.append(tmp_sec.ctrl)

            if i == self.num_secondary-1:
                self.gimbal_parent = self.secondary_ctrls[i]

    def create_gimbal(self):
        ""
        if self.num_secondary > 0:
            parent = self.gimbal_parent
        else:
            parent = self.ctrl
        if self.gimbal == True:
            gimbal_class = Shape(side = self.side,
                                       name = self.name + "Gimbal",
                                       parent = parent,
                                       shape_dict = elements.sphere_small,
                                       lock_attrs = ["tx","ty","tz",
                                                     "sx","sy","sz"], 
                                       size = self.size * 5,
                                       show_rot_order = True)
            gimbal_class.create()
            self.gimbal_ctrl = gimbal_class.ctrl
            gimbal_shape = cmds.listRelatives(self.gimbal_ctrl, shapes = True)[0]
            cmds.setAttr(gimbal_shape + ".overrideColor", 19)

    def make_gimbal_vis(self):
        if self.gimbal:
            self.gimbal_vis_attr = self.ctrl+".gimbal_vis"
            if cmds.objExists(self.gimbal_vis_attr):
                return
            cmds.addAttr(self.ctrl, ln = "gimbal_vis", at = "short", dv = 0,
                        min = 0, max = 1)
            cmds.setAttr( self.gimbal_vis_attr, cb = True, k = False)
            gimbalShape = cmds.listRelatives(self.gimbal_ctrl, shapes = True)[0]
            cmds.connectAttr(self.gimbal_vis_attr, gimbalShape + ".v", f=True)
            cmds.setAttr( gimbalShape + ".v", l = True, cb = False, k = False)

    def add_tags(self):
        if self.gimbal:
            self.gimbal_shape = misc.getShape(self.gimbal_ctrl)
            tag_utils.tag_gimbal(self.gimbal_ctrl)
            message_utils.create_message_attr_setup(self.ctrl, "gimbal", self.gimbal_ctrl, "ctrl")

        # misc.tag_control_shape(misc.getShape(self.ctrl))
        if not self.guide:
            tag_utils.tag_control(self.ctrl)
        else:
            tag_utils.tag_guide(self.ctrl)
        # # gimbal shape
        # cmds.addAttr(self.ctrl, ln = "gimbal", at = "message")
        # cmds.connectAttr(self.gimbal_shape + ".message", self.ctrl + ".gimbal")

    def post_create(self):
        return

    def create(self):
        ""
        self.initialize()
        self.create_buffer()
        self.create_ctl()
        self.attr_alias_remap()
        self.create_secondary()
        self.create_gimbal()
        self.make_gimbal_vis()
        self.add_tags()
        self.post_create()


class Traj_Ctrl(Ctrl):
    def __init__(self,
                 **kw):
        super(Traj_Ctrl, self).__init__(**kw)
        self.name = "traj"
        self.shape_dict = elements.camera_traj
        self.color_side             = False
        self.outliner_color         = True
        self.gimbal                 = False
        self.num_secondary          = 0
        self.show_rot_order         = False
        self.lock_attrs             = ["rx", "ry", "rz", "sx", "sy", "sz"]
        self.ctrl_alias_attr_remap  = {
                                       "track": ".tx",
                                       "pedestal": ".ty",
                                       "dolly": ".tz"
                                      }

    def post_create(self):
        shape = misc_utils.get_shape(self.ctrl)
        self.main_shape = shape[0]
        self.dolly_rear_left_shape = shape[1]
        self.dolly_front_left_shape = shape[2]
        self.dolly_front_right_shape = shape[3]
        self.dolly_rear_right_shape = shape[4]

class Pan_Ctrl(Ctrl):
    def __init__(self,
                 **kw):
        super(Pan_Ctrl, self).__init__(**kw)
        self.name = "pan"
        self.shape_dict = elements.camera_pan
        self.color_side             = False
        self.outliner_color         = True
        self.gimbal                 = False
        self.num_secondary          = 0
        self.show_rot_order         = False
        self.lock_attrs             = ["tx", "ty", "tz", "rx", "rz", "sx", "sy", "sz"]
        self.ctrl_alias_attr_remap  = {
                                       "pan": ".ry",
                                      }

    def post_create(self):
        shape = misc_utils.get_shape(self.ctrl)
        self.main_shape = shape[0]
        self.offset_right_shape = shape[1]
        self.offset_left_shape = shape[2]
        self.pan_top_shape = shape[3]
        self.offset_axis_shape = shape[4]


class Tilt_Ctrl(Ctrl):
    def __init__(self,
                 **kw):
        super(Tilt_Ctrl, self).__init__(**kw)
        self.name = "tilt"

        self.shape_dict = elements.camera_tilt
        self.color_side             = False
        self.outliner_color         = True
        self.gimbal                 = False
        self.num_secondary          = 0
        self.show_rot_order         = False
        self.lock_attrs             = ["tx", "ty", "tz", "ry", "rz", "sx", "sy", "sz"]
        self.ctrl_alias_attr_remap  = {
                                       "tilt": ".rx",
                                      }

    def post_create(self):
        shape = misc_utils.get_shape(self.ctrl)
        self.main_shape = shape[0]
        self.offset_topz_shape = shape[1]
        self.offset_botz_shape = shape[2]
        self.offset_topx_shape = shape[3]
        self.offset_botx_shape = shape[4]


class Roll_Ctrl(Ctrl):
    def __init__(self,
                 **kw):
        super(Roll_Ctrl, self).__init__(**kw)
        self.name = "roll"
        self.shape_dict = elements.camera_roll
        self.color_side             = False
        self.outliner_color         = True
        self.gimbal                 = False
        self.num_secondary          = 0
        self.show_rot_order         = False
        self.lock_attrs             = ["tx", "ty", "tz", "rx", "ry", "sx", "sy", "sz"]
        self.ctrl_alias_attr_remap  = {
                                       "roll": ".rz",
                                      }

    def post_create(self):
        shape = misc_utils.get_shape(self.ctrl)
        self.main_shape = shape[0]
        self.roll_marker_shape = shape[1]

class Offset_Ctrl(Ctrl):
    def __init__(self,
                 **kw):
        super(Offset_Ctrl, self).__init__(**kw)
        self.name = "offset"
        self.shape_dict = elements.camera_offset
        self.color_side             = False
        self.outliner_color         = True
        self.gimbal                 = False
        self.num_secondary          = 0
        self.show_rot_order         = False
        self.lock_attrs             = ["rx", "ry", "rz", "sx", "sy", "sz"]
        self.null_transform          = False
        self.ctrl_alias_attr_remap  = {
                                       "trackOffset": ".tx",
                                       "pedestalOffset": ".ty",
                                       "dollyOffset": ".tz"
                                      }

class Camera_Guide_Ctrl_Base(Ctrl):
    def __init__(self,
                 **kw):
        """
        These guides will not be used to fit the rig, they are helpers for visualizing different parts of the camera
        Also, they will not be selectable
        """
        super(Camera_Guide_Ctrl_Base, self).__init__(**kw)
        self.name = "base"
        self.color_side             = False
        self.outliner_color         = True
        self.gimbal                 = False
        self.num_secondary          = 0
        self.show_rot_order         = False
        self.lock_attrs             = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
        self.num_buffer             = 1

    def post_create(self):
        shape = misc_utils.get_shape(self.ctrl)
        self.main_shape = shape[0]

class Head_Guide_Ctrl(Camera_Guide_Ctrl_Base):
    def __init__(self,
                 **kw):
        super(Head_Guide_Ctrl, self).__init__(**kw)
        self.name = "headGuide"
        self.shape_dict = elements.camera_head_guide

class Traj_Guide_Ctrl(Camera_Guide_Ctrl_Base):
    def __init__(self,
                 **kw):
        super(Traj_Guide_Ctrl, self).__init__(**kw)
        self.name = "trajGuide"
        self.shape_dict = elements.camera_traj_guide
        self.num_buffer             = 2

class Aim_Guide_Ctrl(Camera_Guide_Ctrl_Base):
    def __init__(self,
                 **kw):
        super(Aim_Guide_Ctrl, self).__init__(**kw)
        self.name = "aimGuide"
        self.shape_dict = elements.camera_aim_line
