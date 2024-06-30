from maya import cmds
from . import base as component_base
import importlib
importlib.reload(component_base)
from rig_2.node import utils as node_utils
importlib.reload(node_utils)
from rig_2.manipulator import control as manip_control
importlib.reload(manip_control)
from rig_2.manipulator import elements as manip_elements
importlib.reload(manip_elements)

class Camera_Godnode(component_base.Subcomponent):
    def __init__(self,
                 **kw):
        super(Camera_Godnode, self).__init__(**kw)
        self.name="godnode"

        # vars
        self.master_ctrl_class = None
        self.body_ctrl_class = None
        
        self.master_ctrl = None
        self.body_ctrl = None

    def get_nodes(self):
        # Master
        self.master_ctrl_class = manip_control.Ctrl(name="master",
                                                    shape_dict=manip_elements.camera_master,
                                                    num_buffer = 2,
                                                    parent = self.control,
                                                    color_side = False
                                                    )
        self.master_ctrl_class.create()
        self.master_ctrl = self.master_ctrl_class.ctrl

        # Body
        self.body_ctrl_class = manip_control.Ctrl(name="body",
                                                    shape_dict=manip_elements.camera_body,
                                                    num_buffer = 2,
                                                    parent = self.master_ctrl,
                                                    color_side = False
                                                    )
        self.body_ctrl_class.create()
        self.body_ctrl = self.body_ctrl_class.ctrl

    def create_inputs(self):
        self.inputs["master"] = self.master_ctrl_class.buffers[0]
        self.inputs["body"] = self.body_ctrl_class.buffers[0]
    
    def create_outputs(self):
        self.outputs["master"] = self.master_ctrl
        self.outputs["body"] = self.body_ctrl