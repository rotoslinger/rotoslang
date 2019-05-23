import sys, os

from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
from ui_2 import ui_utils, file_dialog
from ui_2 import file_dialog as file_dialog_ui
reload(file_dialog)
reload(ui_utils)
import elements
reload(elements)
from ui_2 import button_grid_base_core as core
reload(core)

class Base(QtWidgets.QWidget):

    def __init__(self,
                 parent=None,
                 win_title = "Base Utilities",
                 win_name = None,
                 height = 300,
                 width = 300,
                 setting_filename = "baseSettings",
                 do_import_export_widgets = False,
                 do_asset_name_widgets = False,
                 auto_order_asset_import_export_widgets = False,
                 default_file_name = "default",
                 save_window_state = False,
                 import_export_checklist_options=[[]],
                 import_label_text="Import to the set file path.",
                 export_label_text="Export to the set file path.",
                 ):
        super(Base, self).__init__(parent)
        # args
        self.parent = parent
        self.win_title = win_title
        self.win_name = win_name
        self.height = height
        self.width = width
        self.setting_filename = setting_filename
        self.do_import_export_widgets = do_import_export_widgets
        self.do_asset_name_widgets = do_asset_name_widgets
        self.auto_order_asset_import_export_widgets = auto_order_asset_import_export_widgets
        self.default_file_name = default_file_name

        self.save_window_state = save_window_state
        self.import_export_checklist_options = import_export_checklist_options
        self.import_label_text = import_label_text
        self.export_label_text = export_label_text
        # Dummy Spacer
        self.space = ui_utils.label("")
        self.asset_name_widgets = []
        self.import_export_widgets = []
        self.main_widgets = []
        self.settings_path = os.path.join(os.getenv('HOME'), self.setting_filename + ".ini")
        # self.restore_window_state()
        self.view = QtWidgets.QTreeView(self)
        self.view.setMouseTracking(True)
        self.view.entered.connect(self.handleItemEntered)

    def get_settings_path(self):
        self.settings_path = os.path.join(os.getenv('HOME'), self.setting_filename + ".ini")

    def handleItemEntered(self, index):
        if index.isValid():
            QtGui.QToolTip.showText(
                QtGui.QCursor.pos(),
                index.data(),
                self.view.viewport(),
                self.view.visualRect(index)
                )

    def initialize_main_window(self):
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # If you would like to save preferences on close

        self.setWindowTitle(self.win_title)
        self.setObjectName(self.win_name)

        # Not needed for simple buttons, but leaving in for reference
        self.setAcceptDrops(True) # Very important
        self.create_layout()

    def create_layout(self):
        if self.do_asset_name_widgets:
            self.create_asset_name_widgets()
        self.create_widgets()
        if self.do_import_export_widgets:
            self.create_import_export_widgets()
        if self.auto_order_asset_import_export_widgets and self.do_asset_name_widgets and self.do_import_export_widgets:
            self.widgets = self.asset_name_widgets + self.main_widgets + self.import_export_widgets
        else:
            self.widgets = self.main_widgets

        self.resize(self.height, self.width)
        self.scrollArea  = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()

        # Layout
        self.gridLayout=QtWidgets.QGridLayout(self.scrollAreaWidgetContents)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # self.layout.addWidget(self.scrollArea)

        # VBox
        self.main_layout= QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.scrollArea, 1) # stretch factor > 0
        self.main_layout.addStretch(0) # 0 is full stretch
        # Add
        for index, widget in enumerate(self.widgets):
            self.gridLayout.addWidget(widget, index, 0)
        # add the main layout itself to the primitive ui dialog
        self.setLayout(self.main_layout)
        self.restore_window_state()

    def asset_name_text_changed(self):
        self.asset_name = self.asset_name_text_box.text()
        if not self.live_update_checkbox[0].isChecked():
            return

        self.import_dialog.asset_name = self.asset_name
        self.import_dialog.default_path=None
        self.import_dialog.get_default_path()

        self.export_dialog.asset_name = self.asset_name
        self.export_dialog.default_path=None
        self.export_dialog.get_default_path()


    def create_widgets(self):
        # This is where you create your self.main_widgets
        return

    def create_asset_name_widgets(self):
        self.asset_name_label = ui_utils.label("Set Your Asset Name",
                                                                    color=elements.blue,
                                                                    )
        self.asset_name_text_box = ui_utils.text_box(default_text=self.asset_name, text_changed_func=self.asset_name_text_changed)

        self.live_update_layout, self.live_update_checkbox = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Live Update Path", True],
                                                                                                                   ])
        self.asset_name_widgets = [
                        self.asset_name_label,
                        self.asset_name_text_box,
                        self.live_update_layout
                        ]

    def export_func(self):
        return

    def import_func(self):
        return

    def create_import_export_widgets(self):
                ######## Import Guides ###############
        self.import_checkboxes_grid, self.import_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=self.import_export_checklist_options)

        self.import_dialog = file_dialog_ui.File_Dialog(asset_name=self.asset_name,
                                                        default_filename = self.default_file_name,
                                                        default_path=self.default_import_path,
                                                        # contents_changed_func = self.contents_changed
                                                        )
        # import_func_with_args = lambda file_dialog=self.import_dialog, checkboxes = self.import_checkboxes: core.import_all(file_dialog, checkboxes)

        self.import_label, self.import_button = ui_utils.label_button(label_text=self.import_label_text,
                                                                    button_text="Import",
                                                                    color=elements.purple,
                                                                    button_func=self.import_func,
                                                                    )
        ######## Export Guides ###############
        self.backup_layout, self.backup_checkbox = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Save Backup", True],
                                                                                                                   ])
        self.export_checkboxes_grid, self.export_checkboxes = ui_utils.check_box_list(self.import_export_checklist_options)
                                                                                                                   
        self.export_dialog = file_dialog_ui.File_Dialog(asset_name=self.asset_name,
                                                        default_filename = self.default_file_name,
                                                        default_path=self.default_export_path)
        # Export Args
        # file_dialog=self.export_dialog                                                 
        # checkboxes=self.export_checkboxes
        # backup_checkbox=self.backup_checkbox
        # backup_filename = self.export_dialog.get_filename()
        # backup_path = self.export_dialog.default_backup_path
        # export_func_with_args = lambda: core.export_all(file_dialog, checkboxes, backup_checkbox, backup_filename, backup_path)
        self.export_label, self.export_button = ui_utils.label_button(label_text=self.export_label_text,
                                                                    button_text="Export",
                                                                    color=elements.purple,
                                                                    button_func=self.export_func
                                                                    )
                                                                    
        self.import_export_widgets = [
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
                                        self.backup_layout,
                                        ui_utils.separator(),
                                        self.space
                                   ]



    def restore_window_state(self):
        self.get_settings_path()
        if not os.path.exists(self.settings_path):
            return
        self.settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        if not self.save_window_state:
            return
        # If you would like to load preferences on on open
        self.restoreGeometry(self.settings_obj.value("windowGeometry"))
        if self.settings_obj.value("assetName"):
            self.asset_name = self.settings_obj.value("assetName")
        # If save import/export path....
        # if self.settings_obj.value("importPath"):
        #     self.default_import_path = self.settings_obj.value("importPath")
        # if self.settings_obj.value("exportPath"):
        #     self.default_export_path = self.settings_obj.value("exportPath")



    def closeEvent(self, event):
        self.get_settings_path()
        # Save window's geometry
        self.settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        self.settings_obj.setValue("windowGeometry", self.saveGeometry())
        if hasattr(self, "asset_name"):
            self.asset_name = self.asset_name_text_box.text()
            self.settings_obj.setValue("assetName", self.asset_name)
        # If save import/export path....
        # self.settings_obj.setValue("importPath", self.import_dialog.contents.text())
        # self.settings_obj.setValue("exportPath", self.export_dialog.contents.text())


    def openUI(self):
        self.initialize_main_window()
        if self.win_name == None or self.win_name == "":
            self.win_name = self.win_title.replace(" ", "")
        try:
            try:
                globals()[self.win_name].close()
                globals()[self.win_name].deleteLater()
            except:
                pass
            del globals()[self.win_name]
        except:
            pass
        ptr = OpenMayaUI.MQtUtil.mainWindow()
        mayaWin = wrapInstance(long(ptr), QtWidgets.QMainWindow)
        globals()[self.win_name] = self
        globals()[self.win_name].show()
        return globals()[self.win_name]



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

from ui_2 import button_grid_base
reload(button_grid_base)
basething = button_grid_base.Base_Test()
basething.openUI()

@endcode
'''
class Base_Test(Base):

    def __init__(self,
                 **kw):
        super(Base_Test, self).__init__(**kw)
        self.win_title = "Base Test Utilities"
        self.setting_filename = "baseTest"
        self.save_window_state = True


    def first_button_func(self, checkboxes):
        args = [checkbox.isChecked() for checkbox in checkboxes]
        print "You have just pressed the first button checkbox1 is {0}, checkbox 2 is {1}".format(args[0], args[1])

    def second_button_func(self, file_dialog):
        path = file_dialog.contents.text()
        print "You have just pressed the second button, the path is {0}".format(path)

    def create_widgets(self):
        super(Base_Test, self).create_widgets()

        ####### FIRST BUTTON ################
        ### first button has a label and accepts arguments using a QCheckbox by making use of the lamda function
        self.check_box_grid, self.checkboxes = ui_utils.check_box_list()
        first_button_func_with_args = lambda checkboxes=self.checkboxes: self.first_button_func(checkboxes)
        self.first_label, self.first_button = ui_utils.label_button(label_text="Documentation for first button",
                                                                    button_text="First Button",
                                                                    color=elements.purple,
                                                                    button_func=first_button_func_with_args
                                                                    )



        ####### SECOND BUTTON ################
        self.file_dialogue = file_dialog_ui.File_Dialog()
        second_button_func_with_args = lambda file_dialog=self.file_dialogue: self.second_button_func(file_dialog)
        self.second_label, self.second_button = ui_utils.label_button(label_text="Documentation for second button",
                                                                    button_text="Second Button",
                                                                    color=elements.green,
                                                                    button_func=second_button_func_with_args
                                                                    )
        


        # Dummy Spacer, probably a better way to format this
        self.space = ui_utils.label("")

        self.main_widgets = [
                        self.first_label, 
                        self.first_button,
                        self.check_box_grid,
                        self.space,
                        self.second_label, 
                        self.second_button,
                        self.file_dialogue,
                        self.space,
                        ]

