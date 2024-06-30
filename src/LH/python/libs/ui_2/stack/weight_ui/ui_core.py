import sys, os, ast

from maya import cmds

from rig_2.mirror import utils as mirror_utils
import importlib
importlib.reload(mirror_utils)

from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)

from rig.utils import misc
importlib.reload(misc)

from rig_2.weights import utils as weight_utils
importlib.reload(weight_utils)

from rig_2.backup import utils as backup_utils
importlib.reload(backup_utils)

from rig_2.animcurve import utils as animcurve_utils
importlib.reload(animcurve_utils)

from rig_2 import decorator
importlib.reload(decorator)

from rig.utils import misc
importlib.reload(misc)

from rig_2.export import utils as export_utils
importlib.reload(export_utils)

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
    
    export_utils.export_all_weights(file_dialog.asset_name,
                                    file_dialog.contents.text(),
                                    weight_curves=weight_curves,
                                    falloff_weight_curves=falloff_weight_curves,
                                    hand_painted_weights=hand_painted_weights)


@decorator.undo_ignore
def import_all(file_dialog, checkboxes):
    weight_curves, falloff_weight_curves, hand_painted_weights = get_import_export_checkboxes(checkboxes)
    export_utils.import_all_weights(file_dialog.contents.text(),
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
        if cmds.objExists(sel + ".weight_curve_connection_dicts"): 
            weights_string_dict = [ast.literal_eval(str(x)) for x in cmds.getAttr(sel + ".weight_curve_connection_dicts")]
            falloff_weights_string_dict = [ast.literal_eval(str(x)) for x in cmds.getAttr(sel + ".falloff_weight_curve_connection_dicts")]        
            print_control_weightcurve_connection("Weight Curves", weights_string_dict)
            print_control_weightcurve_connection("Falloff Weight Curves", falloff_weights_string_dict)
            return
        if cmds.objectType(sel) == "animCurveTU":
            print(animcurve_utils.getAnimCurve(sel))
        

@decorator.undo_chunk
def weight_curves_to_point_weights():
    weight_utils.convert_selected_curve_to_hand_weights()

def print_control_weightcurve_connection(weight_curve_type, weightcurve_dict_list):
    for curve_dict in weightcurve_dict_list:
        print("================================ {0} {1} =====================================".format(curve_dict["control_parent"], weight_curve_type))
        print("{0} --> {1} --> {2} --> {3}".format(
                                                                                             curve_dict["curve_name"],
                                                                                             curve_dict["curve_weights_node"],
                                                                                             curve_dict["node"],
                                                                                             curve_dict["output_idx"],
                                                                                                ))
        if "hand_weights" in list(curve_dict.keys()):
            print("Hand Painted Weights Overriding Curves: {0} --> {1}".format(
                                                                                curve_dict["hand_weights"],
                                                                                curve_dict["curve_name"],
                                                                                ))
            print("Weighted GEO: --> {0}".format(curve_dict["geo_shape"]))
    print("=================================================================================================")

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
    # print "mirror_weight_curve"
    for sel in cmds.ls(sl=True):
        mirror_utils.smart_mirror_anim_curve(sel)
    
def copy_weight_curve():
    # print "copy_weight_curve"
    animcurve_utils.copyAnimCurve()

def flip_weight_curve():
    for sel in cmds.ls(sl=True):
        side = mirror_utils.get_mirror_side_name(sel)
        animcurve_utils.copy_flip_anim_curves(side=side,
                                              source = sel,
                                              target = sel,
                                              flip=True)

def mirror_weights(mirror_side_checkboxes, side_symmetric_checkbox):
    mirror_side_checkboxes = [checkbox.isChecked() for checkbox in mirror_side_checkboxes]
    mirror_side="L"
    if mirror_side_checkboxes[0] == False:
        mirror_side = "R"
    symmetric_sides = side_symmetric_checkbox[0].isChecked()
    mirror_from_ctrls(center_mirror_side=mirror_side, symmetric_sides=symmetric_sides)
    mirror_from_geo(center_mirror_side=mirror_side)
    # sorted_ctrls = tag_utils.control_from_selected()
    # for ctrl in sorted_ctrls:
    #     geo, hand_weights = tag_utils.get_geo_weights_from_connection_dict(ctrl)
    #     if not geo:
    #         continue
    #     for weight_attr in hand_weights:
    #         mirror_utils.smart_mirror_hand_weights(geo=geo, weight_attr=weight_attr, center_mirror_side=mirror_side, symmetric_sides=symmetric_sides)

def mirror_from_geo(center_mirror_side="L"):
    for sel in cmds.ls(sl=True):
        shape = misc.getShape(sel)
        if not cmds.objectType(shape) == "mesh":
            continue
        mirror_utils.mirror_all_geo_weights(shape, side_to_mirror=center_mirror_side)


def mirror_from_ctrls(center_mirror_side="L", symmetric_sides=False):
    sorted_ctrls = tag_utils.control_from_selected()
    for ctrl in sorted_ctrls:
        geo, hand_weights = tag_utils.get_geo_weights_from_connection_dict(ctrl)
        if not geo:
            continue
        for weight_attr in hand_weights:
            mirror_utils.smart_mirror_hand_weights(geo=geo, weight_attr=weight_attr, center_mirror_side=center_mirror_side, symmetric_sides=symmetric_sides)

def copy_weights():
    sorted_ctrls = tag_utils.control_from_selected()
    weights = []
    for ctrl in sorted_ctrls:
        geo, hand_weights = tag_utils.get_geo_weights_from_connection_dict(ctrl)
        weights.append(hand_weights)

    source_attrs = weights[0]
    for weight_attr in weights[1:]:
        for idx, attr in enumerate(source_attrs):
            if idx > len(weight_attr)-1:
                continue
            source_weights = cmds.getAttr(attr)
            cmds.setAttr(weight_attr[idx], source_weights, type="doubleArray")

def flip_weights(side="L"):
    retrieve_side = True, False
    if side == "R":
        retrieve_side = False, True

    sorted_ctrls = tag_utils.control_from_selected()
    for ctrl in sorted_ctrls:
        geo, hand_weights = tag_utils.get_geo_weights_from_connection_dict(ctrl)
        symmetry_dict = mirror_utils.get_symmetry_dict(geo)
        for weight_attr in hand_weights:
            weights = cmds.getAttr(weight_attr)
            weights2 = cmds.getAttr(weight_attr)
            for key in list(symmetry_dict.keys()):
                weights[symmetry_dict[key]] = weights2[key]
            cmds.setAttr(weight_attr, weights, type="doubleArray")
def establish_symmetry():
    for sel in cmds.ls(sl=True):
        mirror_utils.get_symmetry_dict(sel, retrieve_if_exists=False)

