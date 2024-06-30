import inspect
from maya import cmds
from collections import OrderedDict
from rig.rigComponents import elements 
from rig_2.component import base
import importlib

importlib.reload(base) 

# The face is a master class that will control and wire up all of the face components.
class Face(base.Component):
    def __init__(self,
                 component_name="Face",
                 face_driver="head_output",
                 **kw
                 ):
        super(Face, self).__init__(component_name=component_name, input_driver=face_driver, **kw)
        self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()

    def wire_face_components(self):
        # Wires up the face_input to the input_driver
        cmds.parentConstraint(self.input_driver, self.input_anchor, mo=True)
        cmds.scaleConstraint(self.input_driver, self.input_anchor, mo=True)

    def create(self):
        super(Face, self).create()
        self.wire_face_components()
    
