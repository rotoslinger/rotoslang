import sys, os

from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
from ui_2 import ui_utils
import importlib
importlib.reload(ui_utils)
from . import elements
importlib.reload(elements)
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
from ui_2 import weight_utilities
reload(weight_utilities)
weight_utilities.Weight_Utility_UI.openUI()

@endcode
'''
class Weight_Utility_UI(QtWidgets.QWidget):

    def __init__(self, parent=None, winTitle = "Weight Utilities", winName = None):
        super(Weight_Utility_UI, self).__init__(parent)
        #main widget setting
        
        self.setWindowFlags(QtCore.Qt.Window)
        self.settings_path = os.path.join(os.getenv('HOME'), "scratchSettings.ini")

        self.setWindowTitle(winTitle)
        self.setObjectName(winName)
        self.setAcceptDrops(True) # Very important

        self.create_layout()
        self.create_connections()


    def create_layout(self):
        
        # if os.path.exists(self.settings_path):
        #     settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        #     self.restoreGeometry(settings_obj.value("windowGeometry"))
            # self.restoreState(settings_obj.value("windowState", ""))
        self.resize(300, 300)

        # Buttons

        self.hand_weights_label = ui_utils.create_label("Select Weight Stack and Press", elements.purple)
        self.hand_weights_button = ui_utils.create_button("Print All Handweights", elements.purple)

        self.guide_positions_label = ui_utils.create_label("Run to get all guides in scene", elements.green)
        self.guide_positions_button = ui_utils.create_button("Print All Guide Positions", elements.green)


        self.space = ui_utils.create_label("", green)

        self.widgets = [
                   self.hand_weights_label, 
                   self.hand_weights_button,
                   self.space,
                   self.guide_positions_label, 
                   self.guide_positions_button, 
                   self.space,
                  
                  ]

        ####### Layout
        self.gridLayout=QtWidgets.QGridLayout()

        #--vbox
        main_layout= QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(5)
        main_layout.addLayout(self.gridLayout, 0) # stretch factor > 0
        main_layout.addStretch(0) # 0 is full stretch
        
        # Add
        for index, widget in enumerate(self.widgets):
            self.gridLayout.addWidget(widget, index, 0)

        #add the main layout itself to the primitive ui dialog
        self.setLayout(main_layout)


    def create_connections(self):

        # L List
        # We could do this with lamda like below.  Not using because it is hard to read...
        # self.add_btn_l.clicked.connect(lambda widget_arg=self.list_widget_l: self.add_to_list(widget_arg))
        self.hand_weights_button.clicked.connect(self.add_py_path_action)

    def add_py_path_action(self):
        path = os.path.dirname(os.path.abspath(__file__))
        print(os.path.dirname(os.path.normpath(path)))

        #print os.path.dirname(sys.modules['__main__'].__file__)



    winWidth = 800
    @classmethod
    def openUI(self, winTitle = "Weight Utilities", winName = None):
        if winName == None or winName == "":
            winName = winTitle.replace(" ", "")
        try:
            try:
                globals()[winName].close()
                globals()[winName].deleteLater()
            except:
                pass
            del globals()[winName]
        except:
            pass
        ptr = OpenMayaUI.MQtUtil.mainWindow()
        mayaWin = wrapInstance(int(ptr), QtWidgets.QMainWindow)
        globals()[winName] = self(mayaWin, winTitle, winName)
        globals()[winName].show()
        return globals()[winName]

