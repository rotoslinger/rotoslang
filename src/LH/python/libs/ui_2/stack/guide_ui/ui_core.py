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

from rig_2.shape import nurbscurve

importlib.reload(nurbscurve)

from rig_2.backup import utils as backup_utils
from rig_2 import decorator
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
def vis_all_guides(vis=True):
    if vis:
        tag_utils.vis_all_guides()
    else:
        tag_utils.hide_all_guides()
        
@decorator.undo_chunk
def select_all_guides():
    tag_utils.select_all_guides()
    
@decorator.undo_chunk
def tag_no_export(checkboxes):
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    guide_utils.tag_all_no_export(ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)
    
@decorator.undo_chunk
def remove_tag_no_export(checkboxes):
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    guide_utils.remove_tag_all_no_export(ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)
    
@decorator.undo_chunk
def update_geo_constraints():
    misc.update_all_geo_constraints()

def export_all(file_dialog, checkboxes, backup_checkbox, ):
    backup_arg = backup_checkbox[0].isChecked()
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    # backup_filename = self.export_dialog.get_filename()
    # backup_path = self.export_dialog.default_backup_path

    export_dict = export_utils.export_all_guides(asset_name=file_dialog.asset_name,
                                                 filepath=file_dialog.contents.text(),
                                                 ctrl_shape=ctrl_shape,
                                                 guide=guide,
                                                 guide_shape=guide_shape,
                                                 gimbal_shape=gimbal_shape,
                                                 backup=backup_arg
                                                 )
    # full_backup_name = backup_utils.generate_backup_filename(backup_filename, backup_path)
    # backup_utils.generate_backup_file(full_backup_name, export_dict)

# Undo ignore stack for the next chunk because undoing will break the scene...
@decorator.undo_ignore
def import_all(file_dialog, checkboxes):
    ctrl_shape, guide, guide_shape, gimbal_shape = get_no_export_checkboxes(checkboxes)
    export_utils.import_all_guides(file_dialog.contents.text(), ctrl_shape=ctrl_shape, guide=guide, guide_shape=guide_shape, gimbal_shape=gimbal_shape)

def get_no_export_checkboxes(checkboxes):
    export_args = [checkbox.isChecked() for checkbox in checkboxes]
    ctrl_shape = export_args[0]
    guide = export_args[1]
    guide_shape = export_args[2]
    gimbal_shape = export_args[3]
    return ctrl_shape, guide, guide_shape, gimbal_shape

@decorator.undo_chunk
def mirror_selected_controls():
    guide_utils.mirror_selected_shape_transforms()
    
@decorator.undo_chunk
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

@decorator.undo_chunk
def copy_shape(checkbox):
    nurbscurve.copy_shape(checkbox[0].isChecked())
    
@decorator.undo_chunk
def bake_all_guides():
    guide_utils.bake_all_guides()