import json,os,sys,importlib, ast

from rig_2.guide import utils as guide_utils
reload(guide_utils)

from rig_2.filepath import utils as filepath_utils
reload(filepath_utils)

from rig_2.backup import utils as backup_utils
reload(backup_utils)
    
    
from rig_2.component import base as component_base
reload(component_base)

from rig_2.tag import utils as tag_utils
reload(tag_utils)

from rig_2.attr import constants as attr_constants
reload(attr_constants)

# this is important for the dynamic builds which will use relative module path names
import rig_2
reload(rig_2)
from rig_2 import decorator


def export_all(asset_name,
               filepath,
               ctrl_shape=True,
               guide=True,
               guide_shape=True,
               gimbal_shape=True,
               guide_components=True,
               guide_geo=True,
               backup=True,
               append=True):
    
    if backup:
        backup_utils.backup_file(asset_name, filepath)

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
        export_dict["guide_components"] = component_base.get_all_component_args()

    if guide_geo:
        export_dict["guide_geo"] = guide_utils.get_guide_geo(no_export_tag_dict)

    # Make sure the path exists
    path= os.path.dirname(os.path.normpath(filepath))
    if not os.path.exists(path):
        os.mkdir(path)

    if append and os.path.exists(filepath):
        file = open(filepath, "rb")
        original_dict = json.load(file)
        # Add new entries to the original file.
        # But also overwrite the original key values with new entries
        for key in export_dict.keys():
            for inner_key in export_dict[key]:
                original_dict[key][inner_key] = export_dict[key][inner_key]
        export_dict = original_dict
    
    file = open(filepath, "wb")
    
    json.dump(original_dict, file, sort_keys = False, indent = 2)
    file.close()
    return export_dict


def import_all(filename, ctrl_shape=True, guide=True, guide_shape=True, gimbal_shape=True, build_components=False, guide_geo=True):
    file = open(filename, "rb")
    import_dict = json.load(file)
    file.close()

    no_export_tag_dict = import_dict["no_export_tag_dict"]

    # Create your guide components first, so the guide control positions can be set after
    if build_components and "guide_components" in import_dict.keys():
        create_class_from_dict(import_dict["guide_components"])


    # Set NO_EXPORT tags This will also update the tag dict with component level overrides
    #(if the component is tagged NO_EXPORT, all of its nodes will recieve the tag)
    no_export_tag_dict = tag_utils.set_tags_from_dict(no_export_tag_dict)
    # Control Shapes
    if ctrl_shape:
        guide_utils.set_shapes_from_dict(import_dict["control_shapes"], no_export_tag_dict, check_if_exists=True)
    # guidePositions
    if guide:
        guide_utils.set_guide_positions(import_dict["guide_positions"], no_export_tag_dict)
    # Guide Shapes
    if guide_shape:
        guide_utils.set_shapes_from_dict(import_dict["guide_shapes"], no_export_tag_dict, check_if_exists=True)
    # Gimbal Shapes
    if gimbal_shape:
        guide_utils.set_shapes_from_dict(import_dict["gimbal_shapes"], no_export_tag_dict, check_if_exists=True)

    if "guide_geo" in  import_dict.keys() and guide_geo:
        guide_utils.set_guide_geo_dict(import_dict["guide_geo"], no_export_tag_dict)
        
def literal_eval(string_attribute):
    try:
        return ast.literal_eval(string_attribute)
    except:
        # If the string does not evaluate to strings, numbers, tuples, lists, dicts, booleans, or None it will fail silently
        # Not going to warn because this will happen often, return of false will be enough indication of failure
        return
    
def convert_value_to_literals(dictionary_value):
    if not type(dictionary_value) == unicode and not type(dictionary_value) == str:
        return dictionary_value
    test_val = str(dictionary_value)
    litteral_val = literal_eval(test_val)
    if not litteral_val:
        return dictionary_value
    for attr_instance in attr_constants.ARG_SUPPORTED_TYPES:
        if not isinstance(litteral_val, attr_instance):
            continue
        return litteral_val
        
        
@decorator.undo_chunk
def create_class_from_dict(components_dict):
    # Dynamically gets the module (and reloads it) from a dictionary
    if not components_dict:
        return
    for component_name in components_dict.keys():
        component_dict = components_dict[component_name]
        for key in component_dict.keys():
            component_dict[key] = convert_value_to_literals(component_dict[key])
            
            # print type(component_dict[key]), "type of the entry"
            # if type(component_dict[key]) == unicode or type(component_dict[key]) == str:
            #     test_val = str(component_dict[key])
            #     print "THIS IS THE TESTING VALUE", test_val
            #     print key, component_dict[key]
            #     litteral_val = literal_eval(test_val)
            #     if not litteral_val:
            #         continue
            #     for attr_instance in attr_constants.SUPPORTED_TYPES:
            #         if not isinstance(litteral_val, attr_instance):
            #             continue
            #         print "THJS IS WORKING", litteral_val, type(litteral_val)
                    
            #         component_dict[key] = litteral_val
                        
                    
                    
                    
        # getattr(component_dict["class_name"], **component_dict)
        class_name = component_dict["class_name"].split(".")[-1]
        module_name = component_dict["class_name"].replace("."+ class_name, "")
        module = importlib.import_module(module_name)
        reload(module)
        component_class = eval(component_dict["class_name"])
        component = component_class(**component_dict)
        component.create()

