import sys, os

from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
from rig_2.mirror import utils as mirror_utils
reload(mirror_utils)
from rig_2.tag import utils as tag_utils
reload(tag_utils)
from ui_2 import ui_utils
reload(ui_utils)
from ui_2 import elements
reload(elements)
from ui_2 import button_grid_base
reload(button_grid_base)

from rig.utils import misc
reload(misc)
from rig_2.guide import utils as guide_utils
reload(guide_utils)

from rig_2.manipulator import nurbscurve
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
def vis_all_guides(vis=True):
    if vis:
        tag_utils.vis_all_guides()
    else:
        tag_utils.hide_all_guides()

def select_all_guides():
    tag_utils.select_all_guides()

def tag_no_export(checkboxes):
    # guide=True, guide_shape=True, ctrl_shape=True, gimbal_shape=True
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    guide_utils.tag_all_no_export(ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)

def remove_tag_no_export(checkboxes):
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    guide_utils.remove_tag_all_no_export(ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)

def update_geo_constraints():
    misc.update_all_geo_constraints()

def export_all(file_dialog, checkboxes):
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    export_dict = guide_utils.export_all(file_dialog.contents.text(), ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)
    # print export_dict
def import_all(file_dialog, checkboxes):
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    guide_utils.import_all(file_dialog.contents.text(), ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)

def get_no_export_checkboxes(checkboxes):
    export_args = [checkbox.isChecked() for checkbox in checkboxes]
    ctrl_shape = export_args[0]
    guide = export_args[1]
    guide_shape = export_args[2]
    gimbal_shape = export_args[3]
    return ctrl_shape, guide, guide_shape, gimbal_shape

def mirror_selected_controls():
    guide_utils.mirror_selected_shape_transforms()

def mirror_selected_transforms(mirror_axes_checkboxes, mirror_type_checkboxes, mirror_plane_checkboxes):
    # selected = cmds.ls(sl=True)
    mirror_axes_checkboxes = [checkbox.isChecked() for checkbox in mirror_axes_checkboxes]
    mirror_type_checkboxes = [checkbox.isChecked() for checkbox in mirror_type_checkboxes]
    mirror_plane_checkboxes = [checkbox.isChecked() for checkbox in mirror_plane_checkboxes]

    translation = mirror_axes_checkboxes[0]
    rotate = mirror_axes_checkboxes[1]
    # Don't currently support scaling...
    scale = False
    
    auto_all = mirror_type_checkboxes[0]
    standard = mirror_type_checkboxes[1]
    behavior = mirror_type_checkboxes[2]

    mirrorXY = mirror_plane_checkboxes[0]
    mirrorYZ = mirror_plane_checkboxes[1]
    mirrorXZ = mirror_plane_checkboxes[2]




    mirror_utils.mirror_selected_transforms(translation=translation,
                                            rotate=rotate,
                                            scale=scale,
                                            auto_all=auto_all,
                                            standard=standard,
                                            behavior=behavior,
                                            mirrorXY=mirrorXY,
                                            mirrorYZ=mirrorYZ,
                                            mirrorXZ=mirrorXZ,
                                            )
    # cmds.select(selected)


def copy_shape(checkbox):
    nurbscurve.copy_shape(checkbox[0].isChecked())
