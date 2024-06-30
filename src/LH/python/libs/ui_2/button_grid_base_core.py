from maya import cmds

from rig_2.export import utils as export_utils
import importlib
importlib.reload(export_utils)
from rig_2.mirror import utils as mirror_utils
importlib.reload(mirror_utils)
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)

from rig.utils import misc
importlib.reload(misc)
from rig_2.guide import utils as guide_utils
importlib.reload(guide_utils)

from rig_2.backup import utils as backup_utils
importlib.reload(backup_utils)

from rig_2.shape import mesh
importlib.reload(mesh)
from rig_2.shape import nurbscurve
importlib.reload(nurbscurve)
from rig_2.shape import nurbsurface
importlib.reload(nurbsurface)


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


# def export_all(file_dialog, checkboxes, backup_checkbox, backup_filename, backup_path):
#     backup_arg = backup_checkbox[0].isChecked()
#     ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
#     export_dict = export_utils.export_all(file_dialog.contents.text(), ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)
#     full_backup_name = backup_utils.generate_backup_filename(backup_filename, backup_path)
#     backup_utils.generate_backup_file(full_backup_name, export_dict)

# def import_all(file_dialog, checkboxes):
#     # cmds.undoInfo(state=False)
#     cmds.undoInfo(stateWithoutFlush = False)
#     ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
#     export_utils.import_all(file_dialog.contents.text(), ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)
#     cmds.undoInfo(stateWithoutFlush = True)
#     # cmds.flushUndo()

def get_no_export_checkboxes(checkboxes):
    export_args = [checkbox.isChecked() for checkbox in checkboxes]
    ctrl_shape = export_args[0]
    guide = export_args[1]
    guide_shape = export_args[2]
    gimbal_shape = export_args[3]
    return ctrl_shape, guide, guide_shape, gimbal_shape

def print_geo_dict():
    sel = cmds.ls(sl=True)[0]

    geo_type = cmds.objectType(misc.getShape(sel))
    
    if geo_type == "nurbsCurve":
        print("Type is nurbsCurve")
        print(nurbscurve.get_curve_shape_dict())
    if geo_type == "mesh":
        print("Type is mesh")
        print(mesh.meshData(sel).mesh)
    if geo_type == "nurbsSurface":
        print("Type is nurbsSurface")
        print(nurbsurface.nurbsSurfaceData(sel).nurbs)

def tag_component_no_export():
    guide_utils.tag_no_export_component_membership(add_tag=True)
    
def remove_tag_component_no_export():
    guide_utils.tag_no_export_component_membership(add_tag=False)
