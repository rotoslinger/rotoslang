import sys, os, ast

from maya import cmds

from rig_2.mirror import utils as mirror_utils
reload(mirror_utils)

from rig_2.tag import utils as tag_utils
reload(tag_utils)

from rig.utils import misc
reload(misc)

from rig_2.weights import utils as weight_utils
reload(weight_utils)

from rig_2.backup import utils as backup_utils
reload(backup_utils)

from rig_2 import decorator
reload(decorator)
'''
@code
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
win = "C:\\Users\\harri\\Desktop\\dev\\rotoslang\\src\\LH\\python\\libs"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win32" in os:
    os = win

if os not in sys.path:
    sys.path.append(os)

from ui_2 import guide
reload(guide)
guide_ui = guide.Guide_UI()
guide_ui.openUI()

@endcode
'''
@decorator.undo_chunk
def tag_no_export(checkboxes):
    # guide=True, guide_shape=True, ctrl_shape=True, gimbal_shape=True
    weight_curves, falloff_weight_curves, hand_painted_weights = get_import_export_checkboxes(checkboxes)
    weight_utils.tag_all_no_export(do_weight_curve=weight_curves, do_falloff_weight_curve=falloff_weight_curves, do_hand_painted_weights=hand_painted_weights)

@decorator.undo_chunk
def remove_tag_no_export(checkboxes):
    weight_curves, falloff_weight_curves, hand_painted_weights = get_import_export_checkboxes(checkboxes)
    weight_utils.remove_tag_all_no_export(do_weight_curve=weight_curves, do_falloff_weight_curve=falloff_weight_curves, do_hand_painted_weights=hand_painted_weights)

def export_all(file_dialog, checkboxes, backup_checkbox, backup_filename, backup_path):
    weight_curves, falloff_weight_curves, hand_painted_weights = get_import_export_checkboxes(checkboxes)
    
    export_dict = weight_utils.export_all(file_dialog.contents.text(),
                                          weight_curves=weight_curves,
                                          falloff_weight_curves=falloff_weight_curves,
                                          hand_painted_weights=hand_painted_weights)
    
    full_backup_name = backup_utils.generate_backup_filename(backup_filename, backup_path)
    backup_utils.generate_backup_file(full_backup_name, export_dict)

@decorator.undo_ignore
def import_all(file_dialog, checkboxes):
    weight_curves, falloff_weight_curves, hand_painted_weights = get_import_export_checkboxes(checkboxes)
    weight_utils.import_all(file_dialog.contents.text(),
                            weight_curves=weight_curves,
                            falloff_weight_curves=falloff_weight_curves,
                            hand_painted_weights=hand_painted_weights)
    
def get_no_export_checkboxes(checkboxes):
    export_args = [checkbox.isChecked() for checkbox in checkboxes]
    weight_curves = export_args[0]
    falloff_weight_curves = export_args[1]
    return weight_curves, falloff_weight_curves

def get_import_export_checkboxes(checkboxes):
    export_args = [checkbox.isChecked() for checkbox in checkboxes]
    weight_curves = export_args[0]
    falloff_weight_curves = export_args[1]
    hand_painted_weights = export_args[2]
    return weight_curves, falloff_weight_curves, hand_painted_weights

def print_weight_curves_data():
    # To retrieve dictionaries stored as strings:
    # ast.literal_eval("{"DICTIONARY_KEY":["thingA", "thingB"]}")
    for sel in cmds.ls(sl=True):
        weights_string_dict = [ast.literal_eval(str(x)) for x in cmds.getAttr(sel + ".weight_curve_connection_dicts")]
        falloff_weights_string_dict = [ast.literal_eval(str(x)) for x in cmds.getAttr(sel + ".falloff_weight_curve_connection_dicts")]        
        print_control_weightcurve_connection("Weight Curves", weights_string_dict)
        print_control_weightcurve_connection("Falloff Weight Curves", falloff_weights_string_dict)

@decorator.undo_chunk
def weight_curves_to_point_weights():
    weight_utils.convert_selected_curve_to_hand_weights()

def print_control_weightcurve_connection(weight_curve_type, weightcurve_dict_list):
    for curve_dict in weightcurve_dict_list:
        print "================================ {0} {1} =====================================".format(curve_dict["control_node"], weight_curve_type)
        print "{0} --> {1} --> {2} --> {3}".format(
                                                                                             curve_dict["curve_name"],
                                                                                             curve_dict["curve_weights_node"],
                                                                                             curve_dict["node"],
                                                                                             curve_dict["output_idx"],
                                                                                                )
        if "hand_weights" in curve_dict.keys():
            print "Hand Painted Weights Overriding Curves: {0} --> {1}".format(
                                                                                curve_dict["hand_weights"],
                                                                                curve_dict["curve_name"],
                                                                                )
    print "================================================================================================="

def select_all_weight_curves(options_checkbox):
    export_args = [checkbox.isChecked() for checkbox in options_checkbox]
    do_weight_curves=export_args[0]
    do_falloff_curves=export_args[1]
    weight_curves=[]
    falloff_curves=[]
    if do_weight_curves:
        weight_curves = tag_utils.get_all_with_tag("WEIGHT_CURVE")
    if do_falloff_curves:
        falloff_curves = tag_utils.get_all_with_tag("FALLOFF_WEIGHT_CURVE")
    cmds.select( weight_curves, falloff_curves, r=True)

@decorator.undo_chunk
def remove_all_weight_curves():
    weight_utils.removeAllCurveWeightsNodes()

def mirror_weight_curve():
    print "mirror_weight_curve"
    
def copy_weight_curve():
    print "copy_weight_curve"

def flip_weight_curve():
    print "flip_weight_curve"

def mirror_weights():
    print "mirror_weights"

    
def copy_weights():
    print "copy_weights"

def flip_weights():
    print "flip_weights"

