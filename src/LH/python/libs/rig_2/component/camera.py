from maya import cmds
import base as component_base
reload(component_base)
from rig_2.node import utils as node_utils
reload(node_utils)
from rig_2.manipulator import control as manip_control
reload(manip_control)
from rig_2.manipulator import elements as manip_elements
reload(manip_elements)
from rig_2.component import godnode
reload(godnode)

class Component(component_base.Builder):
    def __init__(self,
                 **kw):
        super(Component, self).__init__(**kw)
        self.name="Camera"

    def get_nodes(self):
        """ If controls don't exist yet, create them, otherwise just instantiate """
        self.godnode = godnode.Camera_Godnode(parent_component_class=self)
        self.godnode.create()
        self.camera = Camera(parent_component_class=self)
        self.camera.create()
        self.technocrane = Technocrane(parent_component_class=self, parent = self.godnode.outputs["body"], godnode_class=self.godnode)
        self.technocrane.create()
        

        self.subcomponents = [self.camera, self.technocrane] + self.camera.subcomponents + self.technocrane.subcomponents


class Camera(component_base.Subcomponent):
    def __init__(self,
                 **kw):
        super(Camera, self).__init__(**kw)
        self.name="camera"

    def get_nodes(self):
        self.camera_node = "{0}_{1}_CAM".format(self.side, self.name)
        self.camera_shape_node = "{0}_{1}_SHP".format(self.side, self.name)
        node_utils.get_node_agnostic("transform", name = self.camera_node, parent = self.geo )
        node_utils.get_node_agnostic("camera", name = self.camera_shape_node, parent = self.geo )
        cmds.parent(self.camera_shape_node, self.camera_node, s=True, r=True)
        self.add_node_to_lock(self.camera_node)
        self.camera_buffer_class = node_utils.Buffer(maya_dag_node=self.camera_node,
                                                     side=self.side,
                                                     name=self.name,
                                                     suffix = "BUF",
                                                     num_buffer = 6
                                                     )
        self.camera_buffer_class.create()
        self.camera_buffers = self.camera_buffer_class.buffers

    def connect_nodes(self):
        return

    def create_inputs(self):
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
        self.name="technocrane"
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
        self.traj_sub = Traj(parent_component_class=self, parent = self.parent, godnode_class=self.godnode_class)
        self.traj_sub.create()
        self.traj_ctrl = self.traj_sub.ctrl

        # Pan
        self.pan_sub = Pan(parent_component_class=self, parent = self.traj_sub.outputs["head_grp"], godnode_class=self.godnode_class)
        self.pan_sub.create()
        self.pan_ctrl = self.pan_sub.ctrl

        # Tilt
        self.tilt_sub = Tilt(parent_component_class=self, parent = self.pan_sub.outputs["pan"], godnode_class=self.godnode_class)
        self.tilt_sub.create()
        self.tilt_ctrl = self.tilt_sub.ctrl

        # Roll
        self.roll_sub = Roll(parent_component_class=self, parent = self.tilt_sub.outputs["tilt"], godnode_class=self.godnode_class)
        self.roll_sub.create()
        self.roll_ctrl = self.roll_sub.ctrl

        # Offset
        self.offset_sub = Offset(parent_component_class=self, parent = self.traj_sub.outputs["traj"], godnode_class=self.godnode_class)
        self.offset_sub.create()
        self.offset_ctrl = self.offset_sub.ctrl

        self.subcomponents = [self.traj_sub,
                              self.pan_sub,
                              self.tilt_sub,
                              self.roll_sub,
                              self.offset_sub,
                              ]

        # headGuide
        self.head_guide_sub = Head_Guide(parent_component_class=self, parent = self.traj_sub.outputs["guide_root_parent"], godnode_class=self.godnode_class)
        self.head_guide_sub.create()

        # Technocrane Aim
        self.aim_sub = Technocrane_Aim(parent_component_class=self, godnode_class=self.godnode_class,
                                       offset_class = self.offset_sub,
                                       traj_class = self.traj_sub,
                                       pan_class = self.tilt_sub,
                                       tilt_class = self.roll_sub,
                                       roll_class = self.offset_sub,
                                       
                                       )
        self.aim_sub.create()
        self.aim_ctrl = self.aim_sub.ctrl

    def connect_nodes(self):
        self.basic_crane_ctrl_connections()
        self.head_guide_connections()


    def head_guide_connections(self):
        # This locator will be used as the target point for the z location of the head guide
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tz", self.tilt_sub.inputs["target_z"], f=True)
        # This locator will be used as the target point for the y location of the head guide
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".ty", self.pan_sub.inputs["targetY"], f=True)



        decompose_base = node_utils.decompose_matrix(name = "{0}_{1}HeadGuideBase".format(self.side, self.name),
                                                  matrix_attr = self.traj_sub.outputs["target_world_matrix"])
        decompose_z = node_utils.decompose_matrix(name = "{0}_{1}HeadGuideZ".format(self.side, self.name),
                                                  matrix_attr = self.tilt_sub.outputs["target_world_matrix"])
        decompose_y = node_utils.decompose_matrix(name = "{0}_{1}HeadGuideY".format(self.side, self.name),
                                                  matrix_attr = self.pan_sub.outputs["target_world_matrix"])
        decompose_x = node_utils.decompose_matrix(name = "{0}_{1}HeadGuideX".format(self.side, self.name),
                                                  matrix_attr = self.offset_sub.outputs["target_world_matrix"])

        cmds.connectAttr(decompose_base + ".outputTranslate", self.head_guide_sub.inputs["point0"], f=True)
        cmds.connectAttr(decompose_y + ".outputTranslate", self.head_guide_sub.inputs["point1"], f=True)
        cmds.connectAttr(decompose_z + ".outputTranslate", self.head_guide_sub.inputs["point2"], f=True)
        cmds.connectAttr(decompose_x + ".outputTranslate", self.head_guide_sub.inputs["point3"], f=True)


    def basic_crane_ctrl_connections(self):

        # This connects the points of the manipulators to the translation of the offset control
        # This may seem superficial, but it is an important visual indicator that makes manip selection simple

        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tz", self.tilt_sub.inputs["topz_point1"] + ".zValue", f=True)
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tz", self.tilt_sub.inputs["botz_point1"] + ".zValue", f=True)

        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tz", self.tilt_sub.inputs["topx_point0"] + ".zValue", f=True)
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tx", self.tilt_sub.inputs["topx_point1"] + ".xValue", f=True)
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tz", self.tilt_sub.inputs["topx_point1"] + ".zValue", f=True)


        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tz", self.tilt_sub.inputs["botx_point0"] + ".zValue", f=True)
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tx", self.tilt_sub.inputs["botx_point1"] + ".xValue", f=True)
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tz", self.tilt_sub.inputs["botx_point1"] + ".zValue", f=True)


        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".ty", self.pan_sub.inputs["right_point1"] + ".yValue", f=True)
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".ty", self.pan_sub.inputs["left_point1"] + ".yValue", f=True)

        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".ty", self.pan_sub.inputs["axis_point0"] + ".yValue", f=True)
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".ty", self.pan_sub.inputs["axis_point1"] + ".yValue", f=True)

        for idx in range(11):
            cmds.connectAttr(self.offset_sub.outputs["offset"] + ".ty", self.pan_sub.ctrl_class.pan_top_shape + ".controlPoints[{0}]".format(idx) + ".yValue", f=True)

        # Have the pan, tilt, roll drive the offset, while the offset drives the roll and tilt, without a cycle
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".ty", self.tilt_sub.inputs["aim"] + ".ty", f=True)
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tx", self.roll_sub.inputs["negate_ty"] + ".tx", f=True)
        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".tz", self.roll_sub.inputs["negate_ty"] + ".tz", f=True)
        # at this point there will be some double transform, the next steps will undo this...

        # The roll is the lowest in the rotational hierarchy, so it is driven by the pan and tilt, which means we only need the roll to drive the offset
        # to multiply the two matrices together
        multMatrix = node_utils.get_node_agnostic("multMatrix", name = "{0}_{1}Mult_MTM".format(self.side, self.name))
        cmds.connectAttr(self.roll_sub.outputs["roll"] + ".worldMatrix", multMatrix + ".matrixIn[0]", f=True)

        # We need to use the offset_grps world inverse matrix to nullify the master/body transform because otherwise the offset will double transform
        cmds.connectAttr(self.offset_sub.inputs["offset_grp"] + ".worldInverseMatrix", multMatrix + ".matrixIn[1]")
        # This final sum cleanly allows the rotation to drive the translation and visa versa, without a cycle
        rollMatrix = node_utils.get_node_agnostic("decomposeMatrix", name = "{0}_{1}Roll_DCM".format(self.side, self.name))
        cmds.connectAttr(multMatrix + ".matrixSum", rollMatrix + ".inputMatrix")
        # connection back into the offset
        cmds.connectAttr(rollMatrix+ ".outputTranslate", self.offset_sub.inputs["offset_world"] + ".translate")
        cmds.connectAttr(rollMatrix+ ".outputRotate", self.offset_sub.inputs["offset_world"] + ".rotate")

        # the final negate to avoid the offset manip multi transforming
        negate_offset = node_utils.get_node_agnostic("multiplyDivide", name = "{0}_{1}NegateOffset_MTD".format(self.side, self.name))
        [cmds.setAttr(negate_offset + x, -1) for x in [".input2X", ".input2Y",".input2Z"]]

        cmds.connectAttr(self.offset_sub.outputs["offset"] + ".translate", negate_offset + ".input1", f=True)
        cmds.connectAttr(negate_offset + ".output", self.offset_sub.inputs["offset_negate"] + ".translate", f=True)

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


        self.name="tCrn"

        # vars
        self.ctrl_class = None
        
        self.ctrl = None

    def get_nodes(self):
        # self.control_root = node_utils.get_node_agnostic("transform", name = "{0}_{1}ControlRoot_Grp".format(self.side, self.name), parent=self.control)
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

        self.aim_grp = node_utils.get_node_agnostic("transform",
                                                            name = "{0}_{1}_NULL".format(self.side, self.name),
                                                            parent=self.rig)

        # self.aim_driver = node_utils.get_locator(name = "{0}_{1}AimDrive_LOC".format(self.side, self.name),
        #                                            parent=self.aim_grp)


        # The idea is that these groups aim at each other without causing a cycle
        ######################### Aim To Head ############################################
        self.aim_to_head = node_utils.get_locator(
                                                         name = "{0}_{1}AimToHead_LOC".format(self.side, self.name),
                                                         parent=self.aim_grp)
        self.aim_to_head_x = node_utils.get_locator(
                                                           name = "{0}_{1}AimToHeadX_LOC".format(self.side, self.name),
                                                           parent=self.aim_to_head)
        self.aim_to_head_offset_x = node_utils.get_locator(
                                                              name = "{0}_{1}AimToHeadOffsetX_LOC".format(self.side, self.name),
                                                              parent=self.aim_to_head_x)


        ######################### Head To Aim ############################################
        # self.head_to_aim_grp = node_utils.get_node_agnostic("transform",
        #                                                      name = "{0}_{1}HeadToAim_NULL".format(self.side, self.name),
        #                                                      parent=self.aim_grp)
        self.head2aim_traj_align = node_utils.get_node_agnostic("transform",
                                                           name = "{0}_{1}HeadToAimTrajAlign_NULL".format(self.side, self.name),
                                                           parent=self.aim_grp)
        self.head2aim = node_utils.get_locator(
                                                         name = "{0}_{1}HeadToAim_LOC".format(self.side, self.name),
                                                         parent=self.head2aim_traj_align)
        self.head2aim_offset_x= node_utils.get_locator(
                                                         name = "{0}_{1}HeadToAimOffsetX_LOC".format(self.side, self.name),
                                                         parent=self.head2aim)
        self.head2aim_x_pan= node_utils.get_locator(
                                                      name = "{0}_{1}HeadToAimXPan_LOC".format(self.side, self.name),
                                                      parent=self.head2aim_offset_x)
        self.head2aim_x_tilt = node_utils.get_locator(
                                                       name = "{0}_{1}HeadToAimXTilt_LOC".format(self.side, self.name),
                                                       parent=self.head2aim_x_pan)
        self.head2aim_x_traj = node_utils.get_locator(
                                                       name = "{0}_{1}HeadToAimXTraj_LOC".format(self.side, self.name),
                                                       parent=self.head2aim_x_tilt)

    def set_defaults(self):
        cmds.setAttr(self.ctrl + ".tz", 30)


    def create_inputs(self):
        super(Technocrane_Aim, self).create_inputs()
        # self.inputs["aim_driver"] = self.aim_driver

    def create_outputs(self):
        super(Technocrane_Aim, self).create_outputs()
        self.outputs["ctrl_matrix"] = self.ctrl + ".worldMatrix"

    def connect_nodes(self):

        # Root functionality
        matrix_to_mult = [self.aim_grp + ".worldInverseMatrix", self.traj_class.ctrl + ".worldMatrix"]
        mult_ctrl_aim = node_utils.mult_matrix(name="{0}_{1}ParInv".format(self.side, self.name), matrix_attrs = matrix_to_mult)
        decompose_parent = node_utils.decompose_matrix(name="{0}_{1}ParInv".format(self.side, self.name),
                                                        matrix_attr = mult_ctrl_aim + ".matrixSum")
        cmds.connectAttr(decompose_parent + ".outputTranslate", self.head2aim_traj_align + ".translate")
        cmds.connectAttr(decompose_parent + ".outputRotate", self.head2aim_traj_align + ".rotate")

        # Aim To Head
        decompose_ctrl = node_utils.decompose_matrix(name="{0}_{1}Ctrl".format(self.side, self.name),
                                                        matrix_attr = self.outputs["ctrl_matrix"])

        cmds.connectAttr(decompose_ctrl + ".outputTranslate", self.aim_to_head + ".translate")

        cmds.aimConstraint(self.head2aim,
                           self.aim_to_head,
                           aimVector = (0, 0, -1),
                           upVector = (0, 1, 0),
                           worldUpType = "objectrotation",
                           worldUpVector = (0, 1, 0),
                           worldUpObject = self.godnode_class.outputs["body"])

        cmds.connectAttr(self.offset_class.ctrl + ".ty", self.head2aim + ".ty")

        cmds.aimConstraint(self.head2aim_offset_x,
                           self.aim_to_head_x,
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
                           aimVector = (0, 0, -1),
                           upVector = (0, 1, 0),
                           worldUpType = "objectrotation",
                           worldUpVector = (0, 1, 0),
                           worldUpObject = self.godnode_class.outputs["body"])

        cmds.aimConstraint(self.aim_to_head_offset_x,
                           self.head2aim_x_pan,
                           aimVector = (0, 0, -1),
                           upVector = (0, 1, 0),
                           worldUpType = "objectrotation",
                           worldUpVector = (0, 1, 0),
                           worldUpObject = self.godnode_class.outputs["body"])

        cmds.connectAttr(self.offset_class.ctrl + ".tx", self.head2aim_x_traj + ".tx")

        cmds.connectAttr(self.offset_class.ctrl + ".ty", self.head2aim_x_traj + ".ty")


    # def set_defaults(self):
    #     super(Technocrane_Aim, self).set_defaults()
    #     shape = misc_utils.get_shape(self.ctrl)
    #     cmds.setAttr(shape[0], "vis")
    #     self.main_shape = shape[-1]

    # def create_inputs(self):
    #     super(Offset, self).create_inputs()
    #     self.inputs["aim_to_head"] = self.buffers[0]
    #     self.inputs["offset_world"] = self.buffers[1]
    #     self.inputs["offset_negate"] = self.buffers[2]






class Crane_Ctrl_Subcomponent(component_base.Subcomponent):
    def __init__(self,
                 **kw):
        super(Crane_Ctrl_Subcomponent, self).__init__(**kw)
        self.name="base"
        self.ctrl_class = manip_control.Traj_Ctrl(parent=self.parent)

    def get_nodes(self):
        super(Crane_Ctrl_Subcomponent, self).get_nodes()
        self.ctrl_class.create()
        self.ctrl = self.ctrl_class.ctrl
        self.buffers = self.ctrl_class.buffers
        self.target_locator = node_utils.get_locator(name = "{0}_{1}TargetLocator_LOC".format(self.side, self.name),
                                                     parent = self.ctrl )
        self.add_node_to_hide(self.target_locator)

    def create_inputs(self):
        super(Crane_Ctrl_Subcomponent, self).create_inputs()
        self.inputs["targetX"] = self.target_locator + ".tx"
        self.inputs["targetY"] = self.target_locator + ".ty"
        self.inputs["target_z"] = self.target_locator + ".tz"

    def create_outputs(self):
        self.outputs[self.name] = self.ctrl
        self.outputs["output"] = self.ctrl
        self.outputs["target_world_matrix"] = self.target_locator + ".worldMatrix"


class Traj(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Traj, self).__init__(**kw)
        self.name="traj"
        self.ctrl_class = manip_control.Traj_Ctrl(parent=self.parent)

    def get_nodes(self):
        super(Traj, self).get_nodes()
        self.traj_guide_sub = Traj_Guide(parent_component_class=self, parent = self.parent)
        self.traj_guide_sub.create()
        self.head_grp = node_utils.get_node_agnostic("transform",
                                                     name = "{0}_head_GRP".format(self.side),
                                                     parent=self.ctrl)

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

    def connect_nodes(self):
        # need to add together the matrix from the control and the noise
        add_ctrl_noise_matrix = node_utils.get_node_agnostic("addMatrix", name = "{0}_{1}TrajGuide_AMT".format(self.side, self.name))
        # adding the matrices
        cmds.connectAttr(self.outputs["noise_offset"] + ".matrix", add_ctrl_noise_matrix + ".matrixIn[0]", f=True)
        cmds.connectAttr(self.outputs["output"] + ".matrix", add_ctrl_noise_matrix + ".matrixIn[1]", f=True)


        # need to decompose the matrix to connect the translate to the points of the guide
        decompose_traj_guide = node_utils.get_node_agnostic("decomposeMatrix", name = "{0}_{1}TrajGuide_DCM".format(self.side, self.name))
        # connect the decompose
        cmds.connectAttr(add_ctrl_noise_matrix + ".matrixSum", decompose_traj_guide + ".inputMatrix", f=True)


        # Connect the points
        cmds.connectAttr(decompose_traj_guide + ".outputTranslateX", self.traj_guide_sub.inputs["point1_x"], f=True)
        cmds.connectAttr(decompose_traj_guide + ".outputTranslateX", self.traj_guide_sub.inputs["point2_x"], f=True)
        cmds.connectAttr(decompose_traj_guide + ".outputTranslateY", self.traj_guide_sub.inputs["point2_y"], f=True)
        cmds.connectAttr(decompose_traj_guide + ".outputTranslate", self.traj_guide_sub.inputs["point3"], f=True)

class Pan(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Pan, self).__init__(**kw)
        self.name="pan"
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

        
class Tilt(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Tilt, self).__init__(**kw)
        self.name="tilt"
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


class Roll(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Roll, self).__init__(**kw)
        self.name="roll"
        self.ctrl_class = manip_control.Roll_Ctrl(parent=self.parent)

    def create_inputs(self):
        super(Roll, self).create_inputs()
        self.inputs["negate_ty"] = self.buffers[-1]


class Offset(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Offset, self).__init__(**kw)
        self.name="offset"
        self.ctrl_class = manip_control.Offset_Ctrl(parent=self.parent)

    def create_inputs(self):
        super(Offset, self).create_inputs()
        self.inputs["offset_grp"] = self.buffers[0]
        self.inputs["offset_world"] = self.buffers[1]
        self.inputs["offset_negate"] = self.buffers[2]
        

class Head_Guide(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Head_Guide, self).__init__(**kw)
        self.name="headGuide"
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

    def connect_nodes(self):
        super(Head_Guide, self).connect_nodes()
        decompose_inverse = node_utils.decompose_matrix(name="{0}_{1}ParentInverse".format(self.side, self.name),
                                                        matrix_attr = self.outputs["parent_inverse_matrix"])
        cmds.connectAttr(decompose_inverse + ".outputTranslate", self.ctrl + ".translate", f=True)
        cmds.connectAttr(decompose_inverse + ".outputRotate", self.ctrl + ".rotate", f=True)
        cmds.connectAttr(decompose_inverse + ".outputScale", self.ctrl + ".scale", f=True)

class Traj_Guide(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Traj_Guide, self).__init__(**kw)
        self.name="trajGuide"
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
        

class Offset(Crane_Ctrl_Subcomponent):
    def __init__(self,
                 **kw):
        super(Offset, self).__init__(**kw)
        self.name="offset"
        self.ctrl_class = manip_control.Offset_Ctrl(parent=self.parent)

    def create_inputs(self):
        super(Offset, self).create_inputs()
        self.inputs["offset_grp"] = self.buffers[0]
        self.inputs["offset_world"] = self.buffers[1]
        self.inputs["offset_negate"] = self.buffers[2]

