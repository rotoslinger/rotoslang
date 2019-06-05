import inspect
from collections import OrderedDict
from rig.rigComponents import lip 
from rig.rigComponents import elements 
from rig_2.component import base
from rig.rigComponents import mouthJaw

reload(base) 
reload(lip)


class Mouth(base.Subcomponent):
    def __init__(self,
                 class_name=None, # Will be set by "self.get_relative_path". This really only becomes important when you are doing a dynamic build from within maya 
                 component_name="mouth",
                 mout_guide_class=None, 
                 **kw
                 ):
        super(Mouth, self).__init__(self, class_name=class_name, component_name=component_name, **kw)
        # by creating a local var "class_name" here we are insuring a relative path of this class is formed and set in the maya args
        class_name = self.get_relative_path()
        # Creating a clean dictionary to avoid inheriting arguments from base.Subcomponent
        self.ordered_args = OrderedDict()
        # Getting args as the current locals at this point in parsing of the file
        self.frame = inspect.currentframe()
        self.get_args()
    
    def unpack_args_from_guide_class(self):
        return
    
    def create_mouth_jaw(self):
        MouthJawClass = mouthJaw.MouthJaw(
                    nameMouth="mouth",
                    nameJaw="jaw",
                    deformMesh="jawMouth",
                    baseGeoToDeform="jawMouthBase",
                    
                    slidePatch="C_mouthGuide_SLDE",
                    slidePatchBase="C_mouthGuide_SLDEBASE",
                    projectionMesh="C_mouthJawPkg_PRJ",
                    characterName = "character",
                    controlParent="C_control_GRP",
                    rigParent="C_rig_GRP",
                    ctrlAutoPositionThreshold=.09)
        MouthJawClass.create()
    
    def create(self):
        super(Mouth, self).create()
        self.unpack_args_from_guide_class()
        self.create_mouth_jaw()


