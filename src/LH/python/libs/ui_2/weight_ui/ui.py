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
from ui_2.weight_ui import ui_core
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

        self.restore_window_state()
        
        # you need to fill the default asset with the last thing the UI had when you close the UI
        # self.asset_name_text_box = ui_utils.Text_Box(default_text=self.asset_name, text_changed_func=self.asset_name_text_changed)
        # self.initialize_main_window()


    def restore_window_state(self):
        super(Weight_UI, self).restore_window_state()
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
        # self.asset_name = self.asset_name_text_box.text()
        # self.settings_obj.setValue("assetName", self.asset_name)

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


    def create_widgets(self):
        super(Weight_UI, self).create_widgets()

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

