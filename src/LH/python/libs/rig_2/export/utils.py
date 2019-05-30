import json,os,sys,importlib

from rig_2.guide import utils as guide_utils
reload(guide_utils)
    
    
from rig_2.component import base as component_base
reload(component_base)

from rig_2.tag import utils as tag_utils

# this is important for the dynamic builds which will use relative module path names
import rig_2

def export_all(filename, ctrl_shape=True, guide=True, guide_shape=True, gimbal_shape=True, guide_components=True):
    export_dict = {}
    no_export_tag_dict = tag_utils.get_no_exports()
    export_dict["no_export_tag_dict"] = no_export_tag_dict
    if ctrl_shape:
        export_dict["control_shapes"] = guide_utils.get_control_shapes(no_export_tag_dict)
    if guide:
        export_dict["guide_positions"] = guide_utils.get_guide_positions(no_export_tag_dict)
    if guide_shape:
        export_dict["guide_shapes"] = guide_utils.get_guide_shapes(no_export_tag_dict)
    if gimbal_shape:
        export_dict["gimbal_shapes"] = guide_utils.get_gimbal_shapes(no_export_tag_dict)
    if guide_components:
        print component_base.get_all_component_args()
        export_dict["guide_components"] = component_base.get_all_component_args()
        
    # Make sure the path exists
    path= os.path.dirname(os.path.normpath(filename))
    if not os.path.exists(path):
        os.mkdir(path)

    file = open(filename, "wb")
    json.dump(export_dict, file, sort_keys = False, indent = 2)
    file.close()
    return export_dict


def import_all(filename, ctrl_shape=True, guide=True, guide_shape=True, gimbal_shape=True, guide_components=True):
    file = open(filename, "rb")
    import_dict = json.load(file)
    file.close()

    no_export_tag_dict = import_dict["no_export_tag_dict"]

    # Create your guide components first, so the guide control positions can be set after
    if guide_components and "guide_components" in import_dict.keys():
        create_class_from_dict(import_dict["guide_components"])


    # Set NO_EXPORT tags
    tag_utils.set_tags_from_dict(no_export_tag_dict)
    # Control Shapes
    if ctrl_shape:
        guide_utils.set_shapes_from_dict(import_dict["control_shapes"], no_export_tag_dict)
    # guidePositions
    if guide:
        guide_utils.set_guide_positions(import_dict["guide_positions"], no_export_tag_dict)
    # Guide Shapes
    if guide_shape:
        guide_utils.set_shapes_from_dict(import_dict["guide_shapes"], no_export_tag_dict)
    # Gimbal Shapes
    if gimbal_shape:
        guide_utils.set_shapes_from_dict(import_dict["gimbal_shapes"], no_export_tag_dict)
        
        
def create_class_from_dict(components_dict):
    # Dynamically gets the module (and reloads it) from a dictionary
    if not components_dict:
        return
    for component_name in components_dict.keys():
        component_dict = components_dict[component_name]
        # getattr(component_dict["class_name"], **component_dict)
        class_name = component_dict["class_name"].split(".")[-1]
        module_name = component_dict["class_name"].replace("."+ class_name, "")
        module = importlib.import_module(module_name)
        reload(module)
        component_class = eval(component_dict["class_name"])
        component = component_class(**component_dict)
        component.create()

