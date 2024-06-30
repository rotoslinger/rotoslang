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
from ui_2.stack.weight_ui import ui_core
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

from ui_2 import weight
reload(weight)
weight_ui = weight.Weight_UI()
weight_ui.openUI()

@endcode
'''
class Weight_UI(button_grid_base.Base):

    def __init__(self,
                 **kw):
        super(Weight_UI, self).__init__(**kw)
        self.win_title = "Weight Utilities"
        self.setting_filename = "WeightUtilities"
        self.save_window_state = True
        self.asset_name = "baseAsset"
        self.default_file_name = "weights.py"
        self.default_import_path = None
        self.default_export_path = None
        self.do_import_export_widgets=True
        self.do_asset_name_widgets=True
        self.auto_order_asset_import_export_widgets=True
        self.import_export_checklist_options=[
                                              ["Weight Curves", True],
                                              ["Falloff Weight Curves", True],                                                                                                                   
                                              ["Hand Painted Weights", True],                                                                                                                   
                                             ]
        self.do_tag_window=True                                  
        self.tag_no_export_func = lambda: ui_core.tag_no_export(self.no_export_checkboxes)
        self.tag_remove_no_export_func = lambda: ui_core.remove_tag_no_export(self.remove_no_export_checkboxes)
        self.no_export_tag_options=[
                                              ["Weight Curves", True],
                                              ["Falloff Weight Curves", True],                                                                                                                   
                                              ["Hand Painted Weights", False],                                                                                                                   
                                             ]

        self.restore_window_state()
        
        # you need to fill the default asset with the last thing the UI had when you close the UI
        # self.asset_name_text_box = ui_utils.Text_Box(default_text=self.asset_name, text_changed_func=self.asset_name_text_changed)
        # self.initialize_main_window()

    def export_func(self):
        file_dialog=self.export_dialog                                                 
        checkboxes=self.export_checkboxes
        backup_checkbox=self.backup_checkbox
        backup_filename = self.export_dialog.get_filename()
        backup_path = self.export_dialog.default_backup_path
        ui_core.export_all(file_dialog, checkboxes, backup_checkbox, backup_filename, backup_path)

    def import_func(self):
        ui_core.import_all(self.import_dialog, self.import_checkboxes)

    

    def create_widgets(self):
        super(Weight_UI, self).create_widgets()

        self.weight_curves_label = ui_utils.create_label("Weight Curve utilities.  Select control before running.",
                                                         color=elements.blue,
                                                         )
        ##################### HAND WEIGHTS ########################################

        self.establish_symmetry_label, self.establish_symmetry_button = ui_utils.label_button(label_text="Establishes symmetry on all selected mesh transforms.\n"
                                                                                                        + "This can be used to reset symmetry if geometry changes",
                                                                    button_text="Establish Symmetry",
                                                                    color=elements.blue,
                                                                    button_func=ui_core.establish_symmetry,
                                                                    )


        self.mirror_weights_label= ui_utils.create_label(text="Select Control(s) to run. Select multiple controls to copy in the driver, driven(s) order.\n"
                                                              + "Select Geometry(s) to run all weights will be mirrored, determine which side to mirror from, L-> R or R-> L with the radio buttons.\n"
                                                              + "If you select a Center control, determine which side to mirror from, L-> R or R-> L with the radio buttons.\n"
                                                              + "If you select a Left control and press 'Mirror Weight(s)' weights will be copied and flipped to the opposite control's weights.\n"
                                                              + "If you check on the 'Symmetric Mirror Side?' L and R side weights will not be copied and flipped, they will be mirrored symmetrically.\n"
                                                              + "If you are using 'Symmetric Mirror Side?' the L->R radio buttons can be used to determine which side will be mirrored from.",
                                                         color=elements.blue)

        self.mirror_side_layout, self.mirror_side_buttons = ui_utils.radio_button_row(checkbox_names_defaults=[
                                                                                                ["L -> R" ],
                                                                                                ["R -> L"],
                                                                                                ],default_true_idx=0)

        self.side_symmetric_layout, self.side_symmetric_checkbox = ui_utils.check_box_list(checkbox_names_defaults=[["Symmetric Mirror Side?", False] ])


        self.mirror_weights_layout, self.mirror_weights_buttons = ui_utils.button_row(names_funcs=[
                                                                      ["Mirror Weight(s)", lambda: ui_core.mirror_weights(self.mirror_side_buttons, self.side_symmetric_checkbox)],
                                                                      ["Copy Weight(s)", ui_core.copy_weights], 
                                                                      ["Flip Weight(s)", ui_core.flip_weights], 
                                                                      ])

        ##################### WEIGHT CURVES ########################################
        self.weight_curve_button_layout, self.weight_curve_button = ui_utils.button_row(
                                                                     [
                                                                      ["Print Weight Curve Data", ui_core.print_weight_curves_data],
                                                                      ["Convert Weight Curve to point weights", ui_core.weight_curves_to_point_weights]
                                                                     ]
                                                                    )

        
        self.mirror_curves_label= ui_utils.create_label(text="Select Weight Curves to run. Select multiple curves to copy in the driver, driven(s) order.\n"
                                                             +"If you are mirroring a center curve it will always be mirrored from the screen right side.",
                                                        color=elements.blue)



        self.mirror_curves_layout, self.mirror_curves_buttons = ui_utils.button_row(names_funcs=[
                                                                      ["Mirror Weight Curve(s)", ui_core.mirror_weight_curve],
                                                                      ["Copy Weight Curve(s)", ui_core.copy_weight_curve], 
                                                                      ["Flip Weight Curve(s)", ui_core.flip_weight_curve], 
                                                                      ])






        ############ MISC #########################################
        self.select_weight_curves_options, self.select_weight_curves_checkbox = ui_utils.check_box_list(checkbox_names_defaults=[["Weight Curves", True],["Falloff Weight Curves",True]])
        select_func = lambda:ui_core.select_all_weight_curves(self.select_weight_curves_checkbox)
        self.select_curves_label, self.select_curves_button = ui_utils.label_button(label_text="Selects all anim curves being used for weighting.",
                                                                    button_text="Select Weight Curves",
                                                                    color=elements.blue,
                                                                    button_func=select_func
                                                                    )


        ############ DELETE ALL WEIGHT CURVES #####################################
        self.delete_curves_lebel, self.delete_curves_button = ui_utils.label_button(label_text="WARNING: Deletes all weight curves.  Only Use as finalization, NEVER EXPORT AFTER THIS STEP",
                                                                    button_text="Delete Weight Curves",
                                                                    color=elements.red,
                                                                    button_func=ui_core.remove_all_weight_curves,
                                                                    bg_color=elements.med_red
                                                                    )

        self.delete_widgets = ui_utils.create_collapsable_dock("Finalize",
                                                                [
                                                                ui_utils.create_heading(text="Finalize", color=elements.red),
                                                                self.delete_curves_lebel, 
                                                                self.delete_curves_button,
                                                                ui_utils.separator(),
                                                                self.space
                                                                ],
                                                                elements.red,
                                                                elements.very_dark_red
                                                                )
        self.import_export_widgets.append(self.delete_widgets)


        self.main_widgets = [
                                ui_utils.create_collapsable_dock("Weight Utils",
                                                                [
                                                                    ui_utils.create_heading(text="Weight Utils", color=elements.blue),
                                                                    ui_utils.separator(),
                                                                    self.establish_symmetry_label,
                                                                    self.establish_symmetry_button,
                                                                    self.mirror_weights_label, 
                                                                    self.mirror_weights_layout,
                                                                    self.mirror_side_layout,
                                                                    self.side_symmetric_layout,
                                                                    ui_utils.separator(),
                                                                    self.space,
                                                                ]),
                                ui_utils.create_collapsable_dock("Weight Curve Utils",
                                                                [
                                                                    ui_utils.create_heading(text="Weight Curve Utils", color=elements.blue),
                                                                    self.weight_curves_label, 
                                                                    self.weight_curve_button_layout,
                                                                    self.mirror_curves_label, 
                                                                    self.mirror_curves_layout,
                                                                    ui_utils.separator(),
                                                                    self.space,
                                                                ]),

                                ui_utils.create_collapsable_dock("Misc Utils",
                                                                [
                                                                    ui_utils.create_heading(text="Misc Utils", color=elements.blue),
                                                                    self.select_curves_label,
                                                                    self.select_curves_button,
                                                                    self.select_weight_curves_options, 
                                                                    ui_utils.separator(),
                                                                    self.space,
                                                                ]),

                        ]

