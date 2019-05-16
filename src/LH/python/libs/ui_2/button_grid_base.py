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

class Base(QtWidgets.QWidget):

    def __init__(self,
                 parent=None,
                 win_title = "Base Utilities",
                 win_name = None,
                 height = 300,
                 width = 300,
                 setting_filename = "baseSettings",
                 save_window_state = False):
        super(Base, self).__init__(parent)
        # args
        self.parent = parent
        self.win_title = win_title
        self.win_name = win_name
        self.height = height
        self.width = width
        self.setting_filename = setting_filename
        self.save_window_state = save_window_state
        # vars
        self.widgets = []


    def initialize_main_window(self):
        self.setWindowFlags(QtCore.Qt.Window)

        # If you would like to save preferences on close
        self.settings_path = os.path.join(os.getenv('HOME'), self.setting_filename + ".ini")

        self.setWindowTitle(self.win_title)
        self.setObjectName(self.win_name)

        # Not needed for simple buttons, but leaving in for reference
        self.setAcceptDrops(True) # Very important
        self.create_layout()

    def create_buttons(self):
        return

    def restore_window_state(self):
        print "OPENING", self.save_window_state
        if not self.save_window_state:
            return
        # If you would like to load preferences on on open
        if os.path.exists(self.settings_path):
            settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
            self.restoreGeometry(settings_obj.value("windowGeometry"))
            # self.restoreState(settings_obj.value("windowState", ""))

    def create_layout(self):
        self.create_buttons()
        self.resize(self.height, self.width)
        # Layout
        self.gridLayout=QtWidgets.QGridLayout()
        # VBox
        self.main_layout= QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(5)
        self.main_layout.addLayout(self.gridLayout, 0) # stretch factor > 0
        self.main_layout.addStretch(0) # 0 is full stretch
        # Add
        for index, widget in enumerate(self.widgets):
            self.gridLayout.addWidget(widget, index, 0)
        # add the main layout itself to the primitive ui dialog
        self.setLayout(self.main_layout)
        self.restore_window_state()

    def closeEvent(self, event):
        # Save window's geometry
        settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        settings_obj.setValue("windowGeometry", self.saveGeometry())
        # settings_obj.setValue("windowState", self.saveState())


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

    def create_buttons(self):
        super(Base_Test, self).create_buttons()

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

        self.widgets = [
                        self.first_label, 
                        self.first_button,
                        self.check_box_grid,
                        self.space,
                        self.second_label, 
                        self.second_button,
                        self.file_dialogue,
                        self.space,
                        ]

