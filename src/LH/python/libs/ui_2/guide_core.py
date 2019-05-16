import sys, os

from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
from ui_2 import ui_utils
reload(ui_utils)
import elements
reload(elements)
from ui_2 import button_grid_base
reload(button_grid_base)

from rig.utils import misc
reload(misc)
from rig_2.guide import utils as guide_utils
reload(guide_utils)

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
        misc.vis_all_guides()
    else:
        misc.hide_all_guides()

def select_all_guides():
    misc.select_all_guides()

def tag_no_export(checkboxes):
    # guide=True, guide_shape=True, ctrl_shape=True, gimbal_shape=True
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    guide_utils.tag_all_no_export(ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)

def remove_tag_no_export(checkboxes):
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    guide_utils.remove_tag_all_no_export(ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)

def update_geo_constraints():
    misc.update_all_geo_constraints()

def export_all(file_path):
    pass
    
def import_all(file_path):
    pass

def get_no_export_checkboxes(checkboxes):
    export_args = [checkbox.isChecked() for checkbox in checkboxes]
    ctrl_shape = export_args[0]
    guide = export_args[1]
    guide_shape = export_args[2]
    gimbal_shape = export_args[3]
    return ctrl_shape, guide, guide_shape, gimbal_shape
