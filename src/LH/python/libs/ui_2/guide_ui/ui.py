import sys, os
from PySide2 import QtWidgets, QtCore, QtGui

from maya import OpenMayaUI as OpenMayaUI
from ui_2 import ui_utils
reload(ui_utils)
from ui_2 import elements
reload(elements)
from ui_2 import button_grid_base
reload(button_grid_base)
from ui_2 import file_dialog as file_dialog_ui
reload(file_dialog_ui)
from ui_2.guide_ui import ui_core
reload(ui_core)



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
class Guide_UI(button_grid_base.Base):

    def __init__(self,
                 **kw):
        super(Guide_UI, self).__init__(**kw)
        self.win_title = "Guide Utilities"
        self.setting_filename = "GuideUtilities"
        self.save_window_state = True
        self.asset_name = "baseAsset"
        self.default_file_name = "guides.py"
        self.default_import_path = None
        self.default_export_path = None

        self.restore_window_state()
        
        # you need to fill the default asset with the last thing the UI had when you close the UI
        # self.asset_name_text_box = ui_utils.Text_Box(default_text=self.asset_name, text_changed_func=self.asset_name_text_changed)
        # self.initialize_main_window()


    def restore_window_state(self):
        super(Guide_UI, self).restore_window_state()
        if self.settings_obj.value("assetName"):
            self.asset_name = self.settings_obj.value("assetName")

        # if self.settings_obj.value("importPath"):
        #     self.default_import_path = self.settings_obj.value("importPath")
        # if self.settings_obj.value("exportPath"):
        #     self.default_export_path = self.settings_obj.value("exportPath")

    def closeEvent(self, event):
        # Save window's geometry
        self.settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        self.settings_obj.setValue("windowGeometry", self.saveGeometry())
        self.asset_name = self.asset_name_text_box.text()
        self.settings_obj.setValue("assetName", self.asset_name)

        # self.settings_obj.setValue("importPath", self.import_dialog.contents.text())
        # self.settings_obj.setValue("exportPath", self.export_dialog.contents.text())

    def asset_name_text_changed(self):
        self.asset_name = self.asset_name_text_box.text()
        if not self.live_update_checkbox[0].isChecked():
            return

        self.import_dialog.asset_name = self.asset_name
        self.import_dialog.get_default_path()
        self.import_dialog.default_path=None

        self.export_dialog.asset_name = self.asset_name
        self.export_dialog.get_default_path()
        self.export_dialog.default_path=None


    def create_buttons(self):
        super(Guide_UI, self).create_buttons()
        # Buttons
        self.asset_name_label = ui_utils.label("Set Your Asset Name",
                                                                    color=elements.blue,
                                                                    )
        self.asset_name_text_box = ui_utils.text_box(default_text=self.asset_name, text_changed_func=self.asset_name_text_changed)

        self.live_update_layout, self.live_update_checkbox = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Live Update Path", True],
                                                                                                                   ])
        ######## MIRROR CURVES ###################
        self.mirror_curves_label, self.mirror_curves_button = ui_utils.label_button(label_text="Select a Curve on the right or left side and run to mirror the shape(s).",
                                                                    button_text="Mirror Curves",
                                                                    color=elements.blue,
                                                                    button_func=ui_core.mirror_selected_controls,
                                                                    )

        ######## MIRROR TRANSFORMS ###################
        self.mirror_type_layout, self.mirror_type_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Translation", True],
                                                                                                                   ["Rotation", True],
                                                                                                                   # Don't currently support scale                                                                                                                
                                                                                                                #    ["Scale", True],                                                                                                                   
                                                                                                                   ])
        self.mirror_plane_label = ui_utils.label("Mirror Behavior planes.",
                                              color=elements.blue,
                                                                    )
        self.mirror_plane_layout, self.mirror_plane_buttons = ui_utils.radio_button_row(checkbox_names_defaults=[
                                                                                                ["mirrorXY (Front Back)"],
                                                                                                ["mirrorYZ (Left Right)" ],
                                                                                                ["mirrorXZ (Up, Down)"],
                                                                                                ],default_true_idx=1)

        # self.mirror_rot_class = ui_utils.checkbox_list_with_limits(checkbox_names_defaults=[
        #                                                                                         ["Auto All", True, "Mirrors each selection based on preset mirror conditions. \n Rivets will be mirrored in the standard way. \n Matrix deformer rotation locators will have behavior mirrored."],
        #                                                                                         ["Standard", False, "Standard mirror without behavior"],
        #                                                                                         ["Behavior", False, "Mirrors behaviors to get mirrored rotation on every axis"],
        #                                                                                         ])
        self.mirror_rot_type_layout, self.mirror_rot_type_buttons = ui_utils.radio_button_row(checkbox_names_defaults=[
                                                                                                ["Auto All", "Mirrors each selection based on preset mirror conditions. \n Rivets will be mirrored in the standard way. \n Matrix deformer rotation locators will have behavior mirrored."],
                                                                                                ["Standard", "Standard mirror without behavior"],
                                                                                                ["Behavior", "Mirrors behaviors to get mirrored rotation on every axis"],
                                                                                                ])
                                                                                                
        self.mirror_transforms_label, self.mirror_transforms_button = ui_utils.label_button(label_text="Select a transform on the right or left side and run to mirror.",
                                                                    button_text="Mirror Transforms",
                                                                    color=elements.blue,
                                                                    button_func=lambda: ui_core.mirror_selected_transforms(self.mirror_type_checkboxes,
                                                                                                                           self.mirror_rot_type_buttons,
                                                                                                                           self.mirror_plane_buttons),
                                                                    )

        ######## PUSH SHAPES ###################
        self.color_layout, self.color_checkbox = ui_utils.check_box_list(checkbox_names_defaults=[["Copy Color?", False] ])
        self.copy_label, self.copy_button = ui_utils.label_button(label_text="Select the Source curve then Target curve(s) and run to copy the curve shape.",
                                                                    button_text="Copy Curves",
                                                                    color=elements.blue,
                                                                    button_func=lambda:ui_core.copy_shape(self.color_checkbox),
                                                                    )

        ######## GUIDE VIS ###############
        self.guide_vis_label = ui_utils.label("Guide Visibility.",
                                              color=elements.blue,
                                                                    )
        self.button_row_layout, self.buttons = ui_utils.button_row(
                                                                     [
                                                                      ["Vis Guides", ui_core.vis_all_guides],
                                                                      ["Hide Guides", lambda: ui_core.vis_all_guides(False)]
                                                                     ]
                                                                    )
        ######## SELECT GUIDE ###############
        self.select_guide_label, self.select_guide_button = ui_utils.label_button(label_text="Select All Guides.",
                                                                    button_text="Select Guides",
                                                                    color=elements.blue,
                                                                    button_func=ui_core.select_all_guides,
                                                                    )

                                                                    
        ######## UPDATE GEOMETRY CONSTRAINT ###############
        self.geo_constraint_label, self.geo_constraint_button = ui_utils.label_button(label_text="Rebinds the geometry constraint for new guide positions.",
                                                                    button_text="Update Geometry Constraints",
                                                                    color=elements.blue,
                                                                    button_func=ui_core.update_geo_constraints
                                                                    )


        ############ ADD NO EXPORT ########################
        self.no_export_checkbox_grid, self.no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Control Shapes", True],
                                                                                                                   ["Guide Positions", True],                                                                                                                   
                                                                                                                   ["Guide Shapes", True],                                                                                                                   
                                                                                                                   ["Gimbal Shapes", True],
                                                                                                                   ])
        no_export_button_func_with_args = lambda: ui_core.tag_no_export(self.no_export_checkboxes)
        self.no_export_label, self.no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to tag NO_EXPORT",
                                                                    button_text="Tag NO_EXPORT",
                                                                    color=elements.green,
                                                                    button_func=no_export_button_func_with_args
                                                                    )

        ############ REMOVE NO EXPORT ########################
        self.remove_no_export_checkbox_grid, self.remove_no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Control Shapes", True],
                                                                                                                   ["Guide Positions", True],                                                                                                                   
                                                                                                                   ["Guide Shapes", True],                                                                                                                   
                                                                                                                   ["Gimbal Shapes", True],
                                                                                                                   ])
        remove_no_export_button_func_with_args = lambda checkboxes=self.remove_no_export_checkboxes: ui_core.remove_tag_no_export(checkboxes)
        self.remove_no_export_label, self.remove_no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to Remove NO_EXPORT",
                                                                    button_text="Remove NO_EXPORT tag",
                                                                    color=elements.red,
                                                                    button_func=remove_no_export_button_func_with_args
                                                                    )

        ######## Import Guides ###############
        self.import_checkboxes_grid, self.import_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Control Shapes", True],
                                                                                                                   ["Guide Positions", True],                                                                                                                   
                                                                                                                   ["Guide Shapes", True],                                                                                                                   
                                                                                                                   ["Gimbal Shapes", True],
                                                                                                                   ])

        self.import_dialog = file_dialog_ui.File_Dialog(asset_name=self.asset_name,
                                                        default_filename = self.default_file_name,
                                                        default_path=self.default_import_path,
                                                        # contents_changed_func = self.contents_changed
                                                        )
        import_func_with_args = lambda file_dialog=self.import_dialog, checkboxes = self.import_checkboxes: ui_core.import_all(file_dialog, checkboxes)
        self.import_label, self.import_button = ui_utils.label_button(label_text="Import guides to the set file path.",
                                                                    button_text="Import",
                                                                    color=elements.purple,
                                                                    button_func=import_func_with_args,
                                                                    )
        ######## Export Guides ###############
        self.export_checkboxes_grid, self.export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Control Shapes", True],
                                                                                                                   ["Guide Positions", True],                                                                                                                   
                                                                                                                   ["Guide Shapes", True],                                                                                                                   
                                                                                                                   ["Gimbal Shapes", True],
                                                                                                                   ],
                                                                                                                   )
        self.export_dialog = file_dialog_ui.File_Dialog(asset_name=self.asset_name,
                                                        default_filename = self.default_file_name,
                                                        default_path=self.default_export_path)
        export_func_with_args = lambda file_dialog=self.export_dialog, checkboxes=self.export_checkboxes: ui_core.export_all(file_dialog, checkboxes)
        self.export_label, self.export_button = ui_utils.label_button(label_text="Export guides to the set file path.",
                                                                    button_text="Export",
                                                                    color=elements.purple,
                                                                    button_func=export_func_with_args
                                                                    )

        # Dummy Spacer, probably a better way to format this
        self.space = ui_utils.label("")

        self.widgets = [
                        self.asset_name_label, 
                        self.asset_name_text_box,
                        self.live_update_layout,
                        # self.space,
                        ui_utils.separator(),
                        self.space,

                        self.mirror_transforms_label, 
                        self.mirror_transforms_button,
                        self.mirror_type_layout,
                        self.mirror_rot_type_layout,
                        self.mirror_plane_label,
                        self.mirror_plane_layout,
                        # self.space,
                        ui_utils.separator(),
                        self.space,

                        self.mirror_curves_label, 
                        self.mirror_curves_button,
                        # self.space,
                        ui_utils.separator(),
                        self.space,


                        self.copy_label, 
                        self.copy_button,
                        self.color_layout,
                        # self.space,
                        ui_utils.separator(),
                        self.space,


                        self.guide_vis_label, 
                        self.button_row_layout,
                        # self.space,
                        ui_utils.separator(),
                        self.space,

                        self.select_guide_label, 
                        self.select_guide_button,
                        # self.space,
                        ui_utils.separator(),
                        self.space,


                        self.geo_constraint_label, 
                        self.geo_constraint_button,
                        # self.space,
                        ui_utils.separator(),
                        self.space,

                        self.no_export_label, 
                        self.no_export_button,
                        self.no_export_checkbox_grid,
                        ui_utils.separator(),
                        self.space,

                        self.remove_no_export_label, 
                        self.remove_no_export_button,
                        self.remove_no_export_checkbox_grid,
                        ui_utils.separator(),
                        self.space,

                        self.import_label, 
                        self.import_button,
                        self.import_dialog,
                        self.import_checkboxes_grid,
                        ui_utils.separator(),
                        self.space,

                        self.export_label, 
                        self.export_button,
                        self.export_dialog,
                        self.export_checkboxes_grid,
                        ui_utils.separator(),
                        self.space,

                        ]

