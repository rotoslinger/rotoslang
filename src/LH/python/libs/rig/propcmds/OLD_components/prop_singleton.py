from maya import cmds
from rig.rigComponents import base
import importlib
importlib.reload(base)
from rig.utils.misc import formatName
from rig.control import base as control_base
importlib.reload(control_base)
from rig.utils import misc
from rig.utils import exportUtils
from rig_2.manipulator import elements as manipulator_elements
from rig_2.shape import nurbscurve
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)


# A simple control with translate, rotate, and scale.  Can have custom attributes but really shouldn't do to much more than the basics.

class Component(base.Component):
    def __init__(self,
                ###### inherited args #####
                #  side="C",
                #  name="component",
                #  suffix="CPT",
                #  curveData=None,
                #  helperGeo=elements.componentNurbs,
                #  orient=[180, 90, 0],
                #  offset=[0, 0, 1],
                #  scale=[1, 1, 1],
                #  lock_attrs=["sx", "sy", "sz"],
                #  size=.5)
                curveData=manipulator_elements.sphere_small,
                numBuffer=1,
                gimbal=False,
                parent=None,   # this will be set by the builder
                createJoint = True,
                null_transform=False,
                ctrl_names = ["ControlA"],
                ctrls_with_bones = [False, False, True],
                ctl_sizes = [10.0, 10.0, 10.0],
                 colors = [ 
                            (1.0, 1.0, 0.0),
                            (0.1, 0.75, 0.7),
                            (0.5, 0.5, 0.0)
                          ],

                debug = True,

                 **kw):
        super(Component, self).__init__(**kw)
        self.componentName = "PropSingleton"
        self.name = "PropSingleton"
        self.createJoint = True
        # if not self.curveData:
        #     self.curveData = manipulator_elements.sphere_small
        self.nullTransform=null_transform
        self.ctrls_with_bones       = ctrls_with_bones
        self.ctrl_names             = ctrl_names
        self.debug                  = debug
        self.ctl_sizes              = ctl_sizes
        self.colors                 = colors
        self.parent                 = parent

    def dummy(self):
        return

    def createCtrl(self):
        """ create ctls """
        self.ctls = []
        self.ctl_buffers = []
        lock_attrs = ["v"]
        for i in range(len(self.ctrl_names)):
            if i == 0:
                parent = self.parent
                if self.debug != 1:
                    lock_attrs = ["v"],
            else: parent = self.ctls[i-1]
            if i == 1:
                lock_attrs = ["sx", "sy", "sz", "v"], 
            return_ctl = control_base.create_ctl(side = self.side, 
                                                name = self.ctrl_names[i], 
                                                parent = self.cmptMasterParent, 
                                                shape = "circle",
                                                num_buffer = 1,
                                                lock_attrs = lock_attrs[0], 
                                                gimbal = False,
                                                size = self.ctl_sizes[i],
                                                color = self.colors[i],
                                                orient = [0,0,90],
                                                create_joint = self.ctrls_with_bones[i],
                                                )
            self.ctls.append(return_ctl.ctl)
            self.ctl_buffers.append(return_ctl.buffers)
            # self.ctl_gimbals.append(return_ctl.gimbal_ctl)
            if return_ctl.gimbal_ctl:
                tag_utils.tag_gimbal(return_ctl.gimbal_ctl)
            tag_utils.tag_control(return_ctl.ctl)
            component_to_tag=""

            if i == 0 & len(return_ctl.buffers) > 0:
                component_to_tag = return_ctl.buffers[0]
            elif i == 0:
                component_to_tag = return_ctl.ctl
            tag_utils.create_component_tag(component_to_tag, self.component_name)
        for buffer in self.ctl_buffers:
            flattened_buffers = [tag_utils.tag_buffer(b) for b in buffer]
            # print (flattened_buffers)
        self.ctrl = self.ctls
        self.locator = self.ctl_buffers[0][0]
        print(self.locator)
            # tag_utils.tag_buffer(buffer)
    def createJoints(self):
        if not self.createJoint:
            return
        self.joints = []
        self.bone_parent_constraints = []
        self.bone_scale_constraints = []

        if not type(self.ctrl) == list:
            self.joint=cmds.joint(self.ctrl, p=self.translate, orientation=self.rotate, scale=self.scale, name = "{0}_{1}_JNT".format(self.side, self.name))
            cmds.setAttr(self.joint + ".visibility", 0)
            cmds.addAttr(self.joint, ln = "BIND",
                                at = "bool")
            cmds.setAttr(self.joint+".BIND", True,
                            l = True,
                            k=False, )
            self.joints.append(self.joint)

            tmp_parent_constraint = cmds.parentConstraint(ctrl, temp_jnt)
            tmp_scale_constraint = cmds.scaleConstraint(ctrl, temp_jnt)

            self.bone_parent_constraints = [{temp_jnt:tmp_parent_constraint}]
            self.bone_scale_constraints = [{temp_jnt:tmp_scale_constraint}]
            print("CREATING CONTROL!!!!")
        elif type(self.ctrl) == list:
            

            for ctrl in self.ctrl:
                temp_jnt = cmds.joint(ctrl, name = "{0}_{1}_JNT".format(self.side, ctrl))

                cmds.setAttr(temp_jnt + ".visibility", 0)
                cmds.addAttr(temp_jnt, ln = "BIND",
                                    at = "bool",)
                cmds.setAttr(temp_jnt+".BIND", True,
                                l = True,
                                k=False, )
                tmp_parent_constraint = cmds.parentConstraint(ctrl, temp_jnt)
                tmp_scale_constraint = cmds.scaleConstraint(ctrl, temp_jnt)
                self.bone_parent_constraints.append({temp_jnt:tmp_parent_constraint})
                self.bone_scale_constraints.append({temp_jnt:tmp_scale_constraint})
                self.joints.append(temp_jnt)
                print("CREATING multiple CONTROL!!!!")



    def createHelperGeo(self):
        return