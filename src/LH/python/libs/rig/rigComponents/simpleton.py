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
                #  curveData=None,
                #  parent=None,
                #  helperGeo=elements.componentNurbs,
                #  numBuffer=2,
                #  orient=[180, 90, 0],
                #  offset=[0, 0, 1],
                #  scale=[1, 1, 1],
                #  lock_attrs=["sx", "sy", "sz"],
                #  gimbal=True,
                #  size=.5)
                                #  size=.5)

                 **kw):
        super(Component, self).__init__(**kw)
        self.componentName = "simpletonCtrl"
        if not self.curveData:
            self.curveData = elements.blockIcon
        self.nullTransform=True

    def dummy(self):
        return

    def createHelperGeo(self):
        return