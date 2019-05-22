import sys, os

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

def tag_no_export(checkboxes):
    cmds.undoInfo(state=True, openChunk=True)
    # guide=True, guide_shape=True, ctrl_shape=True, gimbal_shape=True
    weight_curves, falloff_weight_curves = get_no_export_checkboxes(checkboxes)
    weight_utils.tag_all_no_export(weight_curve_checkbox=weight_curves, falloff_weight_curve_checkbox=falloff_weight_curves)

    cmds.undoInfo(state=True, closeChunk=True)

def remove_tag_no_export(checkboxes):
    cmds.undoInfo(state=True, openChunk=True)
    weight_curves, falloff_weight_curves = get_no_export_checkboxes(checkboxes)
    weight_utils.remove_tag_all_no_export(weight_curve_checkbox=weight_curves, falloff_weight_curve_checkbox=falloff_weight_curves)
    cmds.undoInfo(state=True, closeChunk=True)


def export_all(file_dialog, checkboxes, backup_checkbox, backup_filename, backup_path):
    cmds.undoInfo(state=True, openChunk=True)
    weight_curves, falloff_weight_curves, hand_painted_weights = get_import_export_checkboxes(checkboxes)
    
    export_dict = weight_utils.export_all(file_dialog.contents.text(),
                                          weight_curves=weight_curves,
                                          falloff_weight_curves=falloff_weight_curves,
                                          hand_painted_weights=hand_painted_weights)
    
    full_backup_name = backup_utils.generate_backup_filename(backup_filename, backup_path)
    backup_utils.generate_backup_file(full_backup_name, export_dict)

def import_all(file_dialog, checkboxes):
    cmds.undoInfo(stateWithoutFlush = False)
    weight_curves, falloff_weight_curves, hand_painted_weights = get_import_export_checkboxes(checkboxes)

    weight_utils.import_all(file_dialog.contents.text(),
                            weight_curves=weight_curves,
                            falloff_weight_curves=falloff_weight_curves,
                            hand_painted_weights=hand_painted_weights)
    
    cmds.undoInfo(stateWithoutFlush = True)

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

# def get_weight_curves_dict(do_weight_curves=True, do_falloff_weight_curves=True):
#     # get all animCurveWeightsNodes
#     weight_curves, falloff_weight_curves = get_all_weight_anim_curves()
#     # put all animCurves in a dict
#     weight_curve_dict = {}
#     falloff_weight_curve_dict = {}

#     if do_weight_curves:
#         for curve in weight_curves:
#             weight_curve_dict[curve] = animcurve_utils.getAnimCurve(curve)

#     if do_falloff_weight_curves:
#         for curve in falloff_weight_curves:
#             falloff_weight_curve_dict[curve] = animcurve_utils.getAnimCurve(curve)
    
#     return weight_curve_dict, falloff_weight_curve_dict


# def rebuildAnimCurveWeightsCurves(weight_curve_dict, falloff_weight_curve_dict, weight_curves=True, falloff_weight_curves=True):

#     if do_weight_curves and weight_curve_dict:
#         for curve in weight_curve_dict.keys:
#             animcurve_utils.getAnimCurve(weight_curve_dict[curve])

#     if do_falloff_weight_curves and falloff_weight_curve_dict:
#         for curve in falloff_weight_curve_dict.keys:
#             animcurve_utils.getAnimCurve(falloff_weight_curve_dict[curve])
