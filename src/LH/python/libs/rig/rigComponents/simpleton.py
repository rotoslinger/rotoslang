from maya import cmds
from rigComponents import base
reload(base)
from rig.utils.misc import formatName, create_ctl
from rig.utils import misc
from rig.utils import exportUtils
from rig.utils import faceWeights
import elements

# A simple control with translate, rotate, and scale.  Can have custom attributes but really shouldn't do to much more than the basics.

class Component(base.Component):
    def __init__(self,
                # inherited args
                #  side="C",
                #  name="component",
                #  suffix="CPT",
                #  parent=None,
                 **kw):
        super(Component, self).__init__(**kw)
        self.componentName = "simpletonCtrl"

    def dummy(self):
        return
