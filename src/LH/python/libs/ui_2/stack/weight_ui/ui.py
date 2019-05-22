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
from ui_2.stack.weight_ui import ui_core
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
weight_ui = guide.Weight_UI()
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
        self.no_export_tag_options=[
                                    ["Weight Curves", True],
                                    ["Falloff Weight Curves", True],                                                                                                                   
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

        ############ ADD NO EXPORT ########################
        self.no_export_checkbox_grid, self.no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=self.no_export_tag_options)
        no_export_button_func_with_args = lambda: ui_core.tag_no_export(self.no_export_checkboxes)
        self.no_export_label, self.no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to tag NO_EXPORT",
                                                                    button_text="Tag NO_EXPORT",
                                                                    color=elements.green,
                                                                    button_func=no_export_button_func_with_args
                                                                    )

        ############ REMOVE NO EXPORT ########################
        self.remove_no_export_checkbox_grid, self.remove_no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=self.no_export_tag_options)
        remove_no_export_button_func_with_args = lambda checkboxes=self.remove_no_export_checkboxes: ui_core.remove_tag_no_export(checkboxes)
        self.remove_no_export_label, self.remove_no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to Remove NO_EXPORT",
                                                                    button_text="Remove NO_EXPORT tag",
                                                                    color=elements.red,
                                                                    button_func=remove_no_export_button_func_with_args
                                                                    )


        self.main_widgets = [

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

                        ]

