from maya import cmds
from . import base as component_base
import importlib
importlib.reload(component_base)
from rig_2.node import utils as node_utils
importlib.reload(node_utils)
from rig_2.attr import utils as attr_utils
importlib.reload(attr_utils)
from rig_2.manipulator import control as manip_control
importlib.reload(manip_control)
from rig_2.manipulator import elements as manip_elements
importlib.reload(manip_elements)
from rig_2.component import godnode
importlib.reload(godnode)

class Component(component_base.Subcomponent):
    def __init__(self,
                 **kw):
        super(Component, self).__init__(self, **kw)
        self.component_name= "Camera"
        self.container="asset_camera"

    def get_nodes(self):
        """ If controls don't exist yet, create them, otherwise just instantiate """
        self.godnode = godnode.Camera_Godnode(parent_component_class=self)
        self.godnode.create()
        self.camera = Camera(parent_component_class=self, container=self.container)
        self.camera.create()
        self.technocrane = Technocrane(parent_component_class=self, parent = self.godnode.outputs["body"], godnode_class=self.godnode, container=self.container)
        self.technocrane.create()
        
        cmds.parentConstraint(self.technocrane.offset_class.outputs["output"], self.camera.inputs["input_aim"])

        self.subcomponents = [self.camera, self.technocrane] + self.camera.subcomponents + self.technocrane.subcomponents


class Camera(component_base.Subcomponent):
    def __init__(self,
                 **kw):
        super(Camera, self).__init__(**kw)
        self.component_name="camera"

    def get_nodes(self):
        self.camera_node = "{0}_{1}_CAM".format(self.side, self.component_name)
        self.camera_shape_node = "{0}_{1}_SHP".format(self.side, self.component_name)
        node_utils.get_node_agnostic("transform", name = self.camera_node, parent = self.geo )
        node_utils.get_node_agnostic("camera", name = self.camera_shape_node, parent = self.geo )
        cmds.parent(self.camera_shape_node, self.camera_node, s=True, r=True)
        self.add_node_to_lock(self.camera_node)
        self.camera_buffer_class = node_utils.Buffer(maya_dag_node=self.camera_node,
                                                     side=self.side,
                                                     name=self.component_name,
                                                     suffix = "BUF",
                                                     num_buffer = 6
                                                     )
        self.camera_buffer_class.create()
        self.camera_buffers = self.camera_buffer_class.buffers

    def set_defaults(self):
        cmds.setAttr(self.camera_shape_node + ".locatorScale", 5)

    def connect_nodes(self):
        return

    def create_inputs(self):
        super(Camera, self).create_inputs()
        self.inputs["input_aim"] = self.camera_buffers[0]
        self.inputs["input_aim_traj"] = self.camera_buffers[1]
        self.inputs["input_aim_head"] = self.camera_buffers[2]
        self.inputs["input_aim_pan"] = self.camera_buffers[3]
        self.inputs["input_aim_tilt"] = self.camera_buffers[4]
        self.inputs["input_aim_offset"] = self.camera_buffers[5]


    def create_outputs(self):
        self.outputs["output_camera"] = self.camera_node
        self.outputs["output_camera_shape"] = self.camera_shape_node


class Technocrane(component_base.Subcomponent):
    def __init__(self,
                 **kw):
        super(Technocrane, self).__init__(**kw)
        self.component_name="technocrane"
        # vars
        self.master_ctrl_class = None
        self.body_ctrl_class = None
        self.traj_ctrl_class = None
        self.pan_ctrl_class = None
        self.tilt_ctrl_class = None
        self.roll_ctrl_class = None
        
        self.master_ctrl = None
        self.body_ctrl = None
        self.traj_ctrl = None
        self.pan_ctrl = None
        self.tilt_ctrl = None
        self.roll_ctrl = None

    def get_nodes(self):
        # Traj
        self.traj_class = Traj(parent_component_class=self, parent = self.parent, godnode_class=self.godnode_class, container=self.container)
        self.traj_class.create()
        self.traj_ctrl = self.traj_class.ctrl

        # Pan
        self.pan_class = Pan(parent_component_class=self, parent = self.traj_class.outputs["head_grp"], godnode_class=self.godnode_class, container=self.container)
        self.pan_class.create()
        self.pan_ctrl = self.pan_class.ctrl

        # Tilt
        self.tilt_class = Tilt(parent_component_class=self, parent = self.pan_class.outputs["ctrl"], godnode_class=self.godnode_class, container=self.container)
        self.tilt_class.create()
        self.tilt_ctrl = self.tilt_class.ctrl

        # Roll
        self.roll_class = Roll(parent_component_class=self, parent = self.tilt_class.outputs["ctrl"], godnode_class=self.godnode_class, container=self.container)
        self.roll_class.create()
        self.roll_ctrl = self.roll_class.ctrl

        # Offset
        self.offset_class = Offset(parent_component_class=self, parent = self.traj_class.outputs["ctrl"], godnode_class=self.godnode_class, container=self.container)
        self.offset_class.create()
        self.offset_ctrl = self.offset_class.ctrl

        self.subcomponents = [self.traj_class,
                              self.pan_class,
                              self.tilt_class,
                              self.roll_class,
                              self.offset_class,
                              ]

        # headGuide
        self.head_guide_sub = Head_Guide(parent_component_class=self, parent = self.traj_class.outputs["guide_root_parent"], godnode_class=self.godnode_class, container=self.container)
        self.head_guide_sub.create()

        # Technocrane Aim
        self.aim_class = Technocrane_Aim(parent_component_class=self, godnode_class=self.godnode_class,
                                       offset_class = self.offset_class,
                                       traj_class = self.traj_class,
                                       pan_class = self.pan_class,
                                       tilt_class = self.tilt_class,
                                       roll_class = self.roll_class,
                                       container=self.container,
                                       )
        self.aim_class.create()
        self.aim_ctrl = self.aim_class.ctrl

    def connect_nodes(self):
        self.basic_crane_ctrl_connections()
        self.head_guide_connections()


    def head_guide_connections(self):
        # This locator will be used as the target point for the z location of the head guide
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tz", self.tilt_class.inputs["target_z"], f=True)
        # This locator will be used as the target point for the y location of the head guide
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".ty", self.pan_class.inputs["target_y"], f=True)



        decompose_base = node_utils.decompose_matrix(name = "{0}_{1}HeadGuideBase".format(self.side, self.component_name),
                                                  matrix_attr = self.traj_class.outputs["target_world_matrix"])
        decompose_z = node_utils.decompose_matrix(name = "{0}_{1}HeadGuideZ".format(self.side, self.component_name),
                                                  matrix_attr = self.tilt_class.outputs["target_world_matrix"])
        decompose_y = node_utils.decompose_matrix(name = "{0}_{1}HeadGuideY".format(self.side, self.component_name),
                                                  matrix_attr = self.pan_class.outputs["target_world_matrix"])
        decompose_x = node_utils.decompose_matrix(name = "{0}_{1}HeadGuideX".format(self.side, self.component_name),
                                                  matrix_attr = self.offset_class.outputs["target_world_matrix"])

        cmds.connectAttr(decompose_base + ".outputTranslate", self.head_guide_sub.inputs["point0"], f=True)
        cmds.connectAttr(decompose_y + ".outputTranslate", self.head_guide_sub.inputs["point1"], f=True)
        cmds.connectAttr(decompose_z + ".outputTranslate", self.head_guide_sub.inputs["point2"], f=True)
        cmds.connectAttr(decompose_x + ".outputTranslate", self.head_guide_sub.inputs["point3"], f=True)


    def basic_crane_ctrl_connections(self):

        # This connects the points of the manipulators to the translation of the offset control
        # This may seem superficial, but it is an important visual indicator that makes manip selection simple

        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tz", self.tilt_class.inputs["topz_point1"] + ".zValue", f=True)
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tz", self.tilt_class.inputs["botz_point1"] + ".zValue", f=True)

        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tz", self.tilt_class.inputs["topx_point0"] + ".zValue", f=True)
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tx", self.tilt_class.inputs["topx_point1"] + ".xValue", f=True)
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tz", self.tilt_class.inputs["topx_point1"] + ".zValue", f=True)


        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tz", self.tilt_class.inputs["botx_point0"] + ".zValue", f=True)
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tx", self.tilt_class.inputs["botx_point1"] + ".xValue", f=True)
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tz", self.tilt_class.inputs["botx_point1"] + ".zValue", f=True)


        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".ty", self.pan_class.inputs["right_point1"] + ".yValue", f=True)
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".ty", self.pan_class.inputs["left_point1"] + ".yValue", f=True)

        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".ty", self.pan_class.inputs["axis_point0"] + ".yValue", f=True)
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".ty", self.pan_class.inputs["axis_point1"] + ".yValue", f=True)

        for idx in range(11):
            cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".ty", self.pan_class.ctrl_class.pan_top_shape + ".controlPoints[{0}]".format(idx) + ".yValue", f=True)

        # Have the pan, tilt, roll drive the offset, while the offset drives the roll and tilt, without a cycle
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".ty", self.tilt_class.inputs["aim_offset"] + ".ty", f=True)
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tx", self.roll_class.inputs["negate_ty"] + ".tx", f=True)
        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".tz", self.roll_class.inputs["negate_ty"] + ".tz", f=True)
        # at this point there will be some double transform, the next steps will undo this...

        # The roll is the lowest in the rotational hierarchy, so it is driven by the pan and tilt, which means we only need the roll to drive the offset
        # to multiply the two matrices together
        multMatrix = node_utils.get_node_agnostic("multMatrix", name = "{0}_{1}Mult_MTM".format(self.side, self.component_name))
        cmds.connectAttr(self.roll_class.outputs["ctrl"] + ".worldMatrix", multMatrix + ".matrixIn[0]", f=True)

        # We need to use the offset_grps world inverse matrix to nullify the master/body transform because otherwise the offset will double transform
        cmds.connectAttr(self.offset_class.inputs["offset_grp"] + ".worldInverseMatrix", multMatrix + ".matrixIn[1]")
        # This final sum cleanly allows the rotation to drive the translation and visa versa, without a cycle
        rollMatrix = node_utils.get_node_agnostic("decomposeMatrix", name = "{0}_{1}Roll_DCM".format(self.side, self.component_name))
        cmds.connectAttr(multMatrix + ".matrixSum", rollMatrix + ".inputMatrix")
        # connection back into the offset
        cmds.connectAttr(rollMatrix+ ".outputTranslate", self.offset_class.inputs["offset_world"] + ".translate")
        cmds.connectAttr(rollMatrix+ ".outputRotate", self.offset_class.inputs["offset_world"] + ".rotate")

        # the final negate to avoid the offset manip multi transforming
        negate_offset = node_utils.get_node_agnostic("multiplyDivide", name = "{0}_{1}NegateOffset_MTD".format(self.side, self.component_name))
        [cmds.setAttr(negate_offset + x, -1) for x in [".input2X", ".input2Y",".input2Z"]]

        cmds.connectAttr(self.offset_class.outputs["ctrl"] + ".translate", negate_offset + ".input1", f=True)
        cmds.connectAttr(negate_offset + ".output", self.offset_class.inputs["offset_negate"] + ".translate", f=True)

class Technocrane_Aim(component_base.Subcomponent):
    def __init__(self,
                 offset_class,
                 traj_class,
                 pan_class,
                 tilt_class,
                 roll_class,
                 offset_ctrl = None,
                 traj_ctrl = None,
                 **kw):
        super(Technocrane_Aim, self).__init__(**kw)

        # These are temp for ease, eventually we will want to give specific arguments for the specific ctrls
        self.offset_class=offset_class
        self.traj_class=traj_class
        self.pan_class=pan_class
        self.tilt_class=tilt_class
        self.roll_class=roll_class


        self.offset_ctrl=offset_ctrl
        self.traj_ctrl=traj_ctrl


        self.component_name="tCrn"

        # vars
        self.ctrl_class = None
        
        self.ctrl = None

    def get_nodes(self):
        # self.control_root = node_utils.get_node_agnostic("transform", name = "{0}_{1}ControlRoot_Grp".format(self.side, self.component_name), parent=self.control)
        # Master
        self.ctrl_class = manip_control.Ctrl(name="craneAim",
                                                    shape_dict=manip_elements.technocrane_aim,
                                                    num_buffer = 3,
                                                    parent = self.control,
                                                    color_side             = False,
                                                    outliner_color         = True,
                                                    gimbal                 = False,
                                                    num_secondary          = 0,
                                                    show_rot_order         = False,
                                                    lock_attrs             = ["rx", "ry", "rz", "sx", "sy", "sz"]
                                                    )
        self.ctrl_class.create()
        self.ctrl = self.ctrl_class.ctrl
        self.add_to_container_nodes(self.ctrl)

        # headGuide
        self.aim_guide_class = Aim_Guide(parent_component_class=self, parent = self.skeleton, godnode_class=self.godnode_class)
        self.aim_guide_class.create()
        # template and lock the guide
        self.add_node_to_lock(self.aim_guide_class.ctrl)

        self.aim_grp = node_utils.get_node_agnostic("transform",
                                                            name = "{0}_{1}_NULL".format(self.side, self.component_name),
                                                            parent=self.rig)

        # self.aim_driver = node_utils.get_locator(name = "{0}_{1}AimDrive_LOC".format(self.side, self.component_name),
        #                                            parent=self.aim_grp)


        # The idea is that these groups aim at each other without causing a cycle
        ######################### Aim To Head ############################################
        self.aim_to_head = node_utils.get_locator(
                                                         name = "{0}_{1}AimToHead_LOC".format(self.side, self.component_name),
                                                         parent=self.aim_grp)
        self.aim_to_head_x = node_utils.get_locator(
                                                           name = "{0}_{1}AimToHeadX_LOC".format(self.side, self.component_name),
                                                           parent=self.aim_to_head)
        self.aim_to_head_offset_x = node_utils.get_locator(
                                                              name = "{0}_{1}AimToHeadOffsetX_LOC".format(self.side, self.component_name),
                                                              parent=self.aim_to_head_x)


        ######################### Head To Aim ############################################
        self.head2aim_traj_align = node_utils.get_node_agnostic("transform",
                                                           name = "{0}_{1}HeadToAimTrajAlign_NULL".format(self.side, self.component_name),
                                                           parent=self.aim_grp)
        self.head2aim = node_utils.get_locator(
                                                         name = "{0}_{1}HeadToAim_LOC".format(self.side, self.component_name),
                                                         parent=self.head2aim_traj_align)
        self.head2aim_offset_x= node_utils.get_locator(
                                                         name = "{0}_{1}HeadToAimOffsetX_LOC".format(self.side, self.component_name),
                                                         parent=self.head2aim)
        self.head2aim_x_pan= node_utils.get_locator(
                                                      name = "{0}_{1}HeadToAimXPan_LOC".format(self.side, self.component_name),
                                                      parent=self.head2aim)
        self.head2aim_x_tilt = node_utils.get_locator(
                                                       name = "{0}_{1}HeadToAimXTilt_LOC".format(self.side, self.component_name),
                                                       parent=self.head2aim_x_pan)
        self.head2aim_x_traj = node_utils.get_locator(
                                                       name = "{0}_{1}HeadToAimXTraj_LOC".format(self.side, self.component_name),
                                                       parent=self.head2aim_x_tilt)


        self.aim_hierarchy = [self.aim_to_head,
                              self.aim_to_head_x,
                              self.aim_to_head_offset_x,
                              self.head2aim_traj_align,
                              self.head2aim,
                              self.head2aim_offset_x,
                              self.head2aim_x_pan,
                              self.head2aim_x_tilt,
                              self.head2aim_x_traj,
                              ]

        self.add_node_to_hide(self.aim_hierarchy)

        # ZXY is the rotateOrder
        for loc in self.aim_hierarchy:
            cmds.setAttr(loc + ".rotateOrder", 2)

    def create_inputs(self):
        super(Technocrane_Aim, self).create_inputs()
        self.inputs["ctrl_shape_vis"] = self.ctrl_class.ctrl_shape + ".v"

    def create_outputs(self):
        super(Technocrane_Aim, self).create_outputs()
        self.outputs["ctrl_matrix"] = self.ctrl + ".worldMatrix"
        self.outputs["aim_ctrl"] = self.ctrl

        target_decompose = node_utils.decompose_matrix(name="{0}_{1}Target".format(self.side, self.component_name),
                                                        matrix_attr = self.ctrl + ".worldMatrix",
                                                        rotate_order_transform = self.ctrl)
        offset_decompose = node_utils.decompose_matrix(name="{0}_{1}Source".format(self.side, self.component_name),
                                                        matrix_attr = self.head2aim_x_traj + ".worldMatrix",
                                                        rotate_order_transform = self.head2aim_x_traj)

        self.outputs["source_translate"] = offset_decompose + ".outputTranslate"
        self.outputs["target_translate"] = target_decompose + ".outputTranslate"
        self.outputs["source_rotate"] = offset_decompose + ".outputRotate"
        self.outputs["target_rotate"] = target_decompose + ".outputRotate"
        self.outputs["aim_attr"] = self.offset_class.aim_attr

    def connect_ctrl_vis(self):
        # make sure the controls go into template mode when AIM is turned on
        for attr in self.pan_class.inputs["template_attrs"]:
            cmds.connectAttr(self.outputs["aim_attr"], attr)
        for attr in self.tilt_class.inputs["template_attrs"]:
            cmds.connectAttr(self.outputs["aim_attr"], attr)

        cmds.connectAttr(self.outputs["aim_attr"], self.inputs["ctrl_shape_vis"])
        cmds.connectAttr(self.outputs["aim_attr"], self.aim_guide_class.inputs["shape_vis"])

    def connect_guide(self):
        cmds.connectAttr(self.outputs["source_translate"], self.aim_guide_class.inputs["point0"], f=True)
        cmds.connectAttr(self.outputs["target_translate"], self.aim_guide_class.inputs["point1"], f=True)

    def connect_nodes(self):
        self.connect_ctrl_vis()
        self.connect_guide()
        ######## Create the Aim Hierarchy #######
        # Root functionality
        matrix_to_mult = [self.traj_class.ctrl + ".worldMatrix", self.aim_grp + ".worldInverseMatrix"]
        mult_ctrl_aim = node_utils.mult_matrix(name="{0}_{1}ParInv".format(self.side, self.component_name), matrix_attrs = matrix_to_mult)
        decompose_parent = node_utils.decompose_matrix(name="{0}_{1}ParInv".format(self.side, self.component_name),
                                                        matrix_attr = mult_ctrl_aim + ".matrixSum",
                                                        rotate_order_transform = self.traj_class.ctrl)
        cmds.connectAttr(decompose_parent + ".outputTranslate", self.head2aim_traj_align + ".translate")
        cmds.connectAttr(decompose_parent + ".outputRotate", self.head2aim_traj_align + ".rotate")

        # Aim To Head
        decompose_ctrl = node_utils.decompose_matrix(name="{0}_{1}Ctrl".format(self.side, self.component_name),
                                                        matrix_attr = self.outputs["ctrl_matrix"],
                                                        rotate_order_transform = self.aim_to_head)

        cmds.connectAttr(decompose_ctrl + ".outputTranslate", self.aim_to_head + ".translate")

        cmds.aimConstraint(self.head2aim,
                           self.aim_to_head,
                           mo=True,
                           aimVector = (0, 0, -1),
                           upVector = (0, 1, 0),
                           worldUpType = "objectrotation",
                           worldUpVector = (0, 1, 0),
                           worldUpObject = self.godnode_class.outputs["body"])

        cmds.connectAttr(self.offset_class.ctrl + ".ty", self.head2aim + ".ty")

        cmds.aimConstraint(self.head2aim_offset_x,
                           self.aim_to_head_x,
                           mo=True,
                           aimVector = (0, 0, -1),
                           upVector = (0, 1, 0),
                           worldUpType = "objectrotation",
                           worldUpVector = (0, 1, 0),
                           worldUpObject = self.godnode_class.outputs["body"])
                    
        cmds.connectAttr(self.offset_class.ctrl + ".tx", self.head2aim_offset_x + ".tx")
        cmds.connectAttr(self.offset_class.ctrl + ".tx", self.aim_to_head_offset_x + ".tx")

        # Head To Aim
        cmds.aimConstraint(self.aim_to_head,
                           self.head2aim,
                           mo=True,
                           aimVector = (0, 0, -1),
                           upVector = (0, 1, 0),
                           worldUpType = "objectrotation",
                           worldUpVector = (0, 1, 0),
                           worldUpObject = self.godnode_class.outputs["body"])

        cmds.aimConstraint(self.aim_to_head_offset_x,
                           self.head2aim_x_pan,
                           mo=True,
                           aimVector = (0, 0, -1),
                           upVector = (0, 1, 0),
                           worldUpType = "objectrotation",
                           worldUpVector = (0, 1, 0),
                           worldUpObject = self.godnode_class.outputs["body"])

        cmds.connectAttr(self.offset_class.ctrl + ".tx", self.head2aim_x_traj + ".tx")

        cmds.connectAttr(self.offset_class.ctrl + ".tz", self.head2aim_x_traj + ".tz")

        ######## Connect the aim hierarchy to the controls #######

        ######## PAN AIM #########
        self.connect_aim(rotate_name="Pan",
                         decompose_axis = "Y",
                         parent_grp=self.traj_class.head_grp,
                         aim_driver=self.head2aim_x_pan,
                         aim_switch_attr=self.offset_class.aim_attr,
                         driver_neg_attr=self.pan_class.ctrl + ".ry",
                         driven_aim_attr=self.pan_class.inputs["aim_offset"] + ".ry",
                         driven_negate_attr=self.pan_class.inputs["aim_negate"] + ".ry",
                         
                         )

        ######## TILT AIM #########
        self.connect_aim(rotate_name="Tilt",
                         decompose_axis = "X",
                         parent_grp=self.pan_class.ctrl,
                         aim_driver=self.head2aim_x_tilt,
                         aim_switch_attr=self.offset_class.aim_attr,
                         driver_neg_attr=self.tilt_class.ctrl + ".rx",
                         driven_aim_attr=self.tilt_class.inputs["aim_offset"] + ".rx",
                         driven_negate_attr=self.tilt_class.inputs["aim_negate"] + ".rx",
                         
                         )

    def connect_aim(self,
                    rotate_name,
                    decompose_axis,
                    parent_grp,
                    aim_driver,
                    aim_switch_attr,
                    driven_aim_attr,
                    driver_neg_attr,
                    driven_negate_attr):

        """
        Cleanly separates the orientation of the aim hierarchys to drive single axis rotation.
        Sets up Aim attribute switching (switching from Aim to user specified Pan and Roll values)
        The driver matrix must be normalized using the parent's inverse
        this creates a clean non double transforming matrix that can then be used to drive the rotate
        The negates nullify the user define rotation value, so that when aim is on, any hand animated values will be removed
        """
        # Invert the axis rotation by the parent group for world scales, etc.
        matrix_to_mult_attrs = [aim_driver + ".worldMatrix", parent_grp + ".worldInverseMatrix"]
        head_rot_mult = node_utils.mult_matrix(name="{0}_{1}{2}Aim".format(self.side, self.component_name, rotate_name),
                                               matrix_attrs = matrix_to_mult_attrs)
        decompose_head = node_utils.decompose_matrix(name="{0}_{1}{2}Aim".format(self.side, self.component_name, rotate_name),
                                                matrix_attr = head_rot_mult + ".matrixSum",
                                                rotate_order_transform=aim_driver)

        head_mult_div = cmds.createNode("multiplyDivide", name="{0}_{1}{2}Aim_MTD".format(self.side, self.component_name, rotate_name))
        cmds.connectAttr(decompose_head + ".outputRotate{0}".format(decompose_axis), head_mult_div + ".input1X")
        cmds.connectAttr(self.offset_class.aim_attr, head_mult_div + ".input2X")
        cmds.connectAttr(head_mult_div + ".outputX", driven_aim_attr)


        # Invert the normalized val to nullify animation done out of "AIM" mode
        pan_mult_div_neg = cmds.createNode("multiplyDivide", name="{0}_{1}{2}Neg_MTD".format(self.side, self.component_name, rotate_name))
        cmds.connectAttr(driver_neg_attr, pan_mult_div_neg + ".input1X")
        cmds.setAttr(pan_mult_div_neg + ".input2X", -1)

        # Only do aim when attr is true using condition node
        pan_rot_cond_neg = node_utils.condition(name="{0}_{1}{2}Neg".format(self.side, self.component_name, rotate_name),
                                            first_term = aim_switch_attr,
                                            second_term = 1.0,
                                            operation = 0.0,
                                            color_if_true_attrs = [pan_mult_div_neg + ".outputX","",""],
                                            color_if_false_attrs = [0.0,"",""],
                                            )
        # Final connection to pan
        cmds.connectAttr(pan_rot_cond_neg + ".outColorR", driven_negate_attr)



class Crane_Ctrl_Subcomponent(component_base.Subcomponent):
    def __init__(self,
                 **kw):
        super(Crane_Ctrl_Subcomponent, self).__init__(**kw)
        self.component_name="base"
        self.ctrl_class = manip_control.Traj_Ctrl(parent=self.parent)

    def get_nodes(self):
        super(Crane_Ctrl_Subcomponent, self).get_nodes()
        self.ctrl_class.create()
        self.ctrl = self.ctrl_class.ctrl
        cmds.setAttr(self.ctrl + ".rotateOrder", 2)
        self.buffers = self.ctrl_class.buffers
        self.target_locator = node_utils.get_locator(name = "{0}_{1}TargetLocator_LOC".format(self.side, self.component_name),
                                                     parent = self.ctrl )
        self.add_node_to_hide(self.target_locator)
        self.add_node_to_cleanup(self.ctrl)
        self.add_to_container_nodes(self.ctrl)

    def create_inputs(self):
        super(Crane_Ctrl_Subcomponent, self).create_inputs()
        self.inputs["target_x"] = self.target_locator + ".tx"
        self.inputs["target_y"] = self.target_locator + ".ty"
        self.inputs["target_z"] = self.target_locator + ".tz"
        self.inputs["template_attr"] = self.ctrl + ".template"

        attrs = []
        for shape in self.ctrl_class.ctrl_shapes:
            attrs.append(shape + ".template")
        self.inputs["template_attrs"] = attrs


    def create_outputs(self):
        self.outputs["ctrl"] = self.ctrl
        self.outputs["output"] = self.ctrl
        self.outputs["target_world_matrix"] = self.target_locator + ".worldMatrix"


class Traj(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Traj, self).__init__(**kw)
        self.component_name="traj"
        self.ctrl_class = manip_control.Traj_Ctrl(parent=self.parent)

    def get_nodes(self):
        super(Traj, self).get_nodes()
        self.traj_guide_sub = Traj_Guide(parent_component_class=self, parent = self.parent)
        self.traj_guide_sub.create()
        self.head_grp = node_utils.get_node_agnostic("transform",
                                                     name = "{0}_head_GRP".format(self.side),
                                                     parent=self.ctrl)
        cmds.setAttr(self.head_grp + ".rotateOrder", 2)

        self.add_node_to_lock(self.traj_guide_sub.ctrl)

    def create_inputs(self):
        super(Traj, self).create_inputs()
        self.inputs["noise"] = self.buffers[0]
        self.inputs["noise_offset"] = self.buffers[1]
        self.inputs["noise_negate"] = self.buffers[2]
        self.inputs["head_grp"] = self.head_grp

    def create_outputs(self):
        super(Traj, self).create_outputs()
        self.outputs["noise"] = self.buffers[0]
        self.outputs["noise_offset"] = self.buffers[1]
        self.outputs["noise_negate"] = self.buffers[2]
        self.outputs["guide_root_parent"] = self.traj_guide_sub.outputs["root_parent"]
        self.outputs["head_grp"] = self.head_grp
        self.outputs["track"] = self.ctrl + ".track"
        self.outputs["pedestal"] = self.ctrl + ".pedestal"
        self.outputs["dolly"] = self.ctrl + ".dolly"


    def connect_nodes(self):
        # need to add together the matrix from the control and the noise
        add_ctrl_noise_matrix = node_utils.get_node_agnostic("addMatrix", name = "{0}_{1}TrajGuide_AMT".format(self.side, self.component_name))
        # adding the matrices
        cmds.connectAttr(self.outputs["noise_offset"] + ".matrix", add_ctrl_noise_matrix + ".matrixIn[0]", f=True)
        cmds.connectAttr(self.outputs["output"] + ".matrix", add_ctrl_noise_matrix + ".matrixIn[1]", f=True)


        # need to decompose the matrix to connect the translate to the points of the guide
        decompose_traj_guide = node_utils.get_node_agnostic("decomposeMatrix", name = "{0}_{1}TrajGuide_DCM".format(self.side, self.component_name))
        # connect the decompose
        cmds.connectAttr(add_ctrl_noise_matrix + ".matrixSum", decompose_traj_guide + ".inputMatrix", f=True)


        # Connect the points
        cmds.connectAttr(decompose_traj_guide + ".outputTranslateX", self.traj_guide_sub.inputs["point1_x"], f=True)
        cmds.connectAttr(decompose_traj_guide + ".outputTranslateX", self.traj_guide_sub.inputs["point2_x"], f=True)
        cmds.connectAttr(decompose_traj_guide + ".outputTranslateY", self.traj_guide_sub.inputs["point2_y"], f=True)
        cmds.connectAttr(decompose_traj_guide + ".outputTranslate", self.traj_guide_sub.inputs["point3"], f=True)

    def organize_container(self):
        self.add_to_container_attrs([self.outputs["track"], self.outputs["pedestal"], self.outputs["dolly"]])


class Offset(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Offset, self).__init__(**kw)
        self.component_name="offset"
        self.ctrl_class = manip_control.Offset_Ctrl(parent=self.parent)

    def get_attrs(self):
        super(Offset, self).get_attrs()
        
        self.aim_attr = attr_utils.get_attr(node=self.ctrl,
                                            attr="aim_rig",
                                            attrType="bool",
                                            defaultVal = True,
                                            k=True)
        self.add_to_container_attrs(self.aim_attr)

    def create_inputs(self):
        super(Offset, self).create_inputs()
        self.inputs["offset_grp"] = self.buffers[0]
        self.inputs["offset_world"] = self.buffers[1]
        self.inputs["offset_negate"] = self.buffers[2]
        self.inputs["aim_attr"] = self.aim_attr

    def create_outputs(self):
        super(Offset, self).create_outputs()
        self.outputs["aim_attr"] = self.aim_attr
        self.outputs["track_offset"] = self.ctrl + ".trackOffset"
        self.outputs["pedestal_offset"] = self.ctrl + ".pedestalOffset"
        self.outputs["dolly_offset"] = self.ctrl + ".dollyOffset"

    def organize_container(self):
        # cmds.aliasAttr("-----------OFFSETS", self.dummy_attr)
        self.dummy_attr = attr_utils.get_attr(node=self.ctrl_class.ctrl_shape,
                                            attr="OFFSETS",
                                            nice_name="-----------OFFSETS",
                                            enumName="-----------",
                                            attrType="enum",
                                            k=True)

        self.add_to_container_attrs([self.outputs["track_offset"], self.outputs["pedestal_offset"], self.outputs["dolly_offset"], self.dummy_attr])


class Pan(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Pan, self).__init__(**kw)
        self.component_name="pan"
        self.ctrl_class = manip_control.Pan_Ctrl(parent=self.parent)

    def create_inputs(self):
        super(Pan, self).create_inputs()
        self.inputs["aim"] = self.buffers[0]
        self.inputs["aim_offset"] = self.buffers[1]
        self.inputs["aim_negate"] = self.buffers[2]

        self.inputs["right_point1"] = self.ctrl_class.offset_right_shape + ".controlPoints[1]"
        self.inputs["left_point1"] = self.ctrl_class.offset_left_shape + ".controlPoints[1]"

        self.inputs["axis_point0"] = self.ctrl_class.offset_axis_shape + ".controlPoints[0]"
        self.inputs["axis_point1"] = self.ctrl_class.offset_axis_shape + ".controlPoints[1]"

    def create_outputs(self):
        super(Pan, self).create_outputs()
        self.outputs["pan"] = self.ctrl + ".pan"

    def organize_container(self):
        self.add_to_container_attrs(self.outputs["pan"])


        
class Tilt(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Tilt, self).__init__(**kw)
        self.component_name="tilt"
        self.ctrl_class = manip_control.Tilt_Ctrl(parent=self.parent)

    def create_inputs(self):
        super(Tilt, self).create_inputs()

        self.inputs["aim"] = self.buffers[0]

        self.inputs["aim_offset"] = self.buffers[1]
        self.inputs["aim_negate"] = self.buffers[2]

        self.inputs["topz_point1"] = self.ctrl_class.offset_topz_shape + ".controlPoints[1]"
        self.inputs["botz_point1"] = self.ctrl_class.offset_botz_shape + ".controlPoints[1]"

        self.inputs["topx_point0"] = self.ctrl_class.offset_topx_shape + ".controlPoints[0]"
        self.inputs["topx_point1"] = self.ctrl_class.offset_topx_shape + ".controlPoints[1]"

        self.inputs["botx_point0"] = self.ctrl_class.offset_botx_shape + ".controlPoints[0]"
        self.inputs["botx_point1"] = self.ctrl_class.offset_botx_shape + ".controlPoints[1]"

    def create_outputs(self):
        super(Tilt, self).create_outputs()
        self.outputs["tilt"] = self.ctrl + ".tilt"

    def organize_container(self):
        self.add_to_container_attrs(self.outputs["tilt"])



class Roll(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Roll, self).__init__(**kw)
        self.component_name="roll"
        self.ctrl_class = manip_control.Roll_Ctrl(parent=self.parent)

    def create_inputs(self):
        super(Roll, self).create_inputs()
        self.inputs["negate_ty"] = self.buffers[-1]

    def create_outputs(self):
        super(Roll, self).create_outputs()
        self.outputs["roll"] = self.ctrl + ".roll"

    def organize_container(self):
        self.add_to_container_attrs(self.outputs["roll"])


class Head_Guide(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Head_Guide, self).__init__(**kw)
        self.component_name="headGuide"
        self.parent =  self.skeleton
        self.ctrl_class = manip_control.Head_Guide_Ctrl(parent=self.parent)
    def get_nodes(self):
        super(Head_Guide, self).get_nodes()
        self.add_node_to_lock(self.ctrl)

    def create_inputs(self):
        super(Head_Guide, self).create_inputs()
        self.inputs["buffer"] = self.buffers[0]
        self.inputs["vis"] = self.ctrl + ".v"
        self.inputs["point0"] = self.ctrl_class.main_shape + ".controlPoints[0]"
        self.inputs["point1"] = self.ctrl_class.main_shape + ".controlPoints[1]"
        self.inputs["point2"] = self.ctrl_class.main_shape + ".controlPoints[2]"
        self.inputs["point2_x"] = self.ctrl_class.main_shape + ".controlPoints[2].xValue"
        self.inputs["point3"] = self.ctrl_class.main_shape + ".controlPoints[3]"
        
    def create_outputs(self):
        super(Head_Guide, self).create_outputs()
        self.outputs["parent_inverse_matrix"] = self.buffers[0] + ".parentInverseMatrix"

class Traj_Guide(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Traj_Guide, self).__init__(**kw)
        self.component_name="trajGuide"
        self.ctrl_class = manip_control.Traj_Guide_Ctrl(parent=self.parent)



    def create_inputs(self):
        super(Traj_Guide, self).create_inputs()
        self.inputs["buffer"] = self.buffers[0]
        self.inputs["vis"] = self.ctrl + ".v"
        self.inputs["translate"] = self.buffers[0] + ".translate"
        self.inputs["rotate"] = self.buffers[0] + ".rotate"
        self.inputs["root_parent"] = self.buffers[1]
        self.inputs["parentInverseMatrix"] = self.buffers[1] + ".parentInverseMatrix"
        self.inputs["worldInverseMatrix"] = self.buffers[1] + ".worldInverseMatrix"
        self.inputs["point1_x"] = self.ctrl_class.main_shape + ".controlPoints[1].xValue"
        self.inputs["point2_x"] = self.ctrl_class.main_shape + ".controlPoints[2].xValue"
        self.inputs["point2_y"] = self.ctrl_class.main_shape + ".controlPoints[2].yValue"
        self.inputs["point3"] = self.ctrl_class.main_shape + ".controlPoints[3]"

    def create_outputs(self):
        super(Traj_Guide, self).create_outputs()
        self.outputs["root_parent"] = self.buffers[1]
        self.outputs["parent_inverse_matrix"] = self.buffers[0] + ".parentInverseMatrix"


class Aim_Guide(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Aim_Guide, self).__init__(**kw)
        self.component_name="headGuide"
        self.parent =  self.skeleton
        self.ctrl_class = manip_control.Aim_Guide_Ctrl(parent=self.parent)
    def get_nodes(self):
        super(Aim_Guide, self).get_nodes()
        self.add_node_to_lock(self.ctrl)

    def create_inputs(self):
        super(Aim_Guide, self).create_inputs()
        self.inputs["buffer"] = self.buffers[0]
        self.inputs["vis"] = self.ctrl + ".v"
        self.inputs["shape_vis"] = self.ctrl_class.main_shape + ".v"
        self.inputs["point0"] = self.ctrl_class.main_shape + ".controlPoints[0]"
        self.inputs["point1"] = self.ctrl_class.main_shape + ".controlPoints[1]"
