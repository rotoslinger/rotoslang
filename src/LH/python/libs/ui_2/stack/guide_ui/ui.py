import sys, os
from PySide2 import QtWidgets, QtCore, QtGui

from maya import OpenMayaUI as OpenMayaUI
from ui_2 import ui_utils
import importlib
importlib.reload(ui_utils)
from ui_2 import elements
importlib.reload(elements)
from ui_2 import button_grid_base
importlib.reload(button_grid_base)
from ui_2 import file_dialog as file_dialog_ui
importlib.reload(file_dialog_ui)
from ui_2.stack.guide_ui import ui_core
importlib.reload(ui_core)



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
        self.do_import_export_widgets=True
        self.do_asset_name_widgets=True
        self.auto_order_asset_import_export_widgets=True
        self.import_export_checklist_options=[
                                              ["Control Shapes", True],
                                              ["Guide Positions", True],                                                                                                                   
                                              ["Guide Shapes", True],                                                                                                                   
                                              ["Gimbal Shapes", True],
                                             ]

        self.do_tag_window=True                                  
        self.tag_no_export_func = lambda: ui_core.tag_no_export(self.no_export_checkboxes)
        self.tag_remove_no_export_func = lambda: ui_core.remove_tag_no_export(self.remove_no_export_checkboxes)
        self.no_export_tag_options=[
                                    ["Control Shapes", True],
                                    ["Guide Positions", True],                                                                                                                   
                                    ["Guide Shapes", True],                                                                                                                   
                                    ["Gimbal Shapes", True],
                                             ]
        self.restore_window_state()
        # you need to fill the default asset with the last thing the UI had when you close the UI
        # self.asset_name_text_box = ui_utils.Text_Box(default_text=self.asset_name, text_changed_func=self.asset_name_text_changed)
        # self.initialize_main_window()

    def export_func(self):
        file_dialog=self.export_dialog                                                 
        checkboxes=self.export_checkboxes
        backup_checkbox=self.backup_checkbox
        # backup_filename = self.export_dialog.get_filename()
        # backup_path = self.export_dialog.default_backup_path
        # self.export_dialog.asset_name
        ui_core.export_all(file_dialog, checkboxes, backup_checkbox)

    def import_func(self):
        ui_core.import_all(self.import_dialog, self.import_checkboxes)

    def create_widgets(self):
        
        super(Guide_UI, self).create_widgets()
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
        self.mirror_plane_label = ui_utils.create_label("Mirror Behavior planes.",
                                                        color=elements.blue,
                                                        )
        self.mirror_plane_layout, self.mirror_plane_buttons = ui_utils.radio_button_row(checkbox_names_defaults=[
                                                                                                ["mirrorXY (Front Back)"],
                                                                                                ["mirrorYZ (Left Right)" ],
                                                                                                ["mirrorXZ (Up, Down)"],
                                                                                                ],default_true_idx=1)

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
        self.guide_vis_label = ui_utils.create_label("Guide Visibility.",
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
        # self.no_export_checkbox_grid, self.no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[
        #                                                                                                            ["Control Shapes", True],
        #                                                                                                            ["Guide Positions", True],                                                                                                                   
        #                                                                                                            ["Guide Shapes", True],                                                                                                                   
        #                                                                                                            ["Gimbal Shapes", True],
        #                                                                                                            ],color=elements.green)
        # no_export_button_func_with_args = lambda: ui_core.tag_no_export(self.no_export_checkboxes)
        # self.no_export_label, self.no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to tag NO_EXPORT",
        #                                                             button_text="Tag NO_EXPORT",
        #                                                             color=elements.green,
        #                                                             button_func=no_export_button_func_with_args
        #                                                             )

        # ############ REMOVE NO EXPORT ########################
        # self.remove_no_export_checkbox_grid, self.remove_no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[
        #                                                                                                            ["Control Shapes", True],
        #                                                                                                            ["Guide Positions", True],                                                                                                                   
        #                                                                                                            ["Guide Shapes", True],                                                                                                                   
        #                                                                                                            ["Gimbal Shapes", True],
        #                                                                                                            ],color=elements.light_red)
        # remove_no_export_button_func_with_args = lambda checkboxes=self.remove_no_export_checkboxes: ui_core.remove_tag_no_export(checkboxes)
        # self.remove_no_export_label, self.remove_no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to Remove NO_EXPORT",
        #                                                             button_text="Remove NO_EXPORT tag",
        #                                                             color=elements.red,
        #                                                             button_func=remove_no_export_button_func_with_args
        #                                                             )
        ############ DELETE ALL WEIGHT CURVES #####################################
        self.bake_guides, self.bake_guides_button = ui_utils.label_button(label_text="WARNING: Bakes all guides.\n" +
                                                                          "Only Use as finalization, BE CAREFUL EXPORTING AFTER THIS STEP.\n" +
                                                                          "Guides will no longer be live.",
                                                                    button_text="Bake All Guides",
                                                                    color=elements.red,
                                                                    button_func=ui_core.bake_all_guides,
                                                                    bg_color=elements.med_red
                                                                    )

        self.bake_guides_widgets = ui_utils.create_collapsable_dock("Finalize",
                                                                [
                                                                ui_utils.create_heading(text="Finalize", color=elements.red),
                                                                self.bake_guides, 
                                                                self.bake_guides_button,
                                                                ui_utils.separator(),
                                                                self.space
                                                                ],
                                                                elements.red,
                                                                elements.very_dark_red
                                                                )
        self.import_export_widgets.append(self.bake_guides_widgets)



        self.create_misc_utils()

        self.main_widgets = [
                        ui_utils.create_collapsable_dock("Guide/Shape Mirroring",
                                                        [
                                                            ui_utils.create_heading(text="Guide/Shape Mirroring", color=elements.blue),
                                                            self.mirror_transforms_label, 
                                                            self.mirror_transforms_button,
                                                            self.mirror_type_layout,
                                                            self.mirror_rot_type_layout,
                                                            self.mirror_plane_label,
                                                            self.mirror_plane_layout,
                                                            ui_utils.separator(),
                                                            self.space,
                                                            self.mirror_curves_label, 
                                                            self.mirror_curves_button,
                                                            ui_utils.separator(),
                                                            self.space,
                                                            self.copy_label, 
                                                            self.copy_button,
                                                            self.color_layout,
                                                            ui_utils.separator(),
                                                            self.space,
                                                        ]),
                        ui_utils.create_collapsable_dock("Misc Utils",
                                                        [
                                                        ui_utils.create_heading(text="Misc Utils", color=elements.blue),
                                                        self.guide_vis_label, 
                                                        self.button_row_layout,
                                                        ui_utils.separator(),
                                                        self.space,

                                                        self.select_guide_label, 
                                                        self.select_guide_button,
                                                        ui_utils.separator(),
                                                        self.space,

                                                        self.geo_constraint_label, 
                                                        self.geo_constraint_button,
                                                        ui_utils.separator(),
                                                        self.space,
                                                        
                                                        self.cache_label,
                                                        self.cache_curve_weights_widget,
                                                        self.cache_slide_widget,
                                                        ui_utils.separator(),
                                                        self.space,
                                                        
                                                        self.print_geo_label,
                                                        self.print_geo_button,
                                                        ui_utils.separator(),
                                                        self.space,

                                                        ]),


                        # ui_utils.create_heading(text="Tagging", color=elements.blue),
                        # self.no_export_label, 
                        # self.no_export_button,
                        # self.no_export_checkbox_grid,
                        # ui_utils.separator(),
                        # self.space,

                        # self.remove_no_export_label, 
                        # self.remove_no_export_button,
                        # self.remove_no_export_checkbox_grid,
                        # ui_utils.separator(),
                        # self.space,

                        ]

