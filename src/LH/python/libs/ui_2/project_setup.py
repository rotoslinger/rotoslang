import sys, os

from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
import utils as ui_utils
import importlib
importlib.reload(ui_utils)
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
from rig.ui import scratch_panel
reload(scratch_panel)
scratch_panel.Setup_UI.openUI()

@endcode
'''
class Setup_UI(QtWidgets.QWidget):

    def __init__(self, parent=None, winTitle = "Project Setup", winName = None):
        super(Setup_UI, self).__init__(parent)
        #main widget setting
        
        self.setWindowFlags(QtCore.Qt.Window)
        self.settings_path = os.path.join(os.getenv('HOME'), "scratchSettings.ini")

        self.setWindowTitle(winTitle)
        self.setObjectName(winName)
        self.setAcceptDrops(True) # Very important

        self.create_layout()
        self.create_connections()

    def create_layout(self):
        
        if os.path.exists(self.settings_path):
            settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
            self.restoreGeometry(settings_obj.value("windowGeometry"))
            # self.restoreState(settings_obj.value("windowState", ""))
        for i in dir(self):
            if "save" in i or "restore" in i:
                print(i)

        #add button
        self.add_py_path = QtWidgets.QPushButton("Add to python path")

        self.gridLayout=QtWidgets.QGridLayout()

        #--create the layout vbox#$#$#$
        main_layout= QtWidgets.QVBoxLayout()
        
        ################ to reduce button margins and the spacing
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addLayout(self.gridLayout, 1) # stretch factor > 0
        main_layout.addStretch(0) # 0 is full stretch
        
        # 
        self.gridLayout.addWidget(self.add_py_path, 0, 0)

        #add the main layout itself to the primitive ui dialog
        self.setLayout(main_layout)


    def create_connections(self):

        # L List
        # We could do this with lamda like below.  Not using because it is hard to read...
        # self.add_btn_l.clicked.connect(lambda widget_arg=self.list_widget_l: self.add_to_list(widget_arg))
        self.add_py_path.clicked.connect(self.add_py_path_action)

    def add_py_path_action(self):
        path = os.path.dirname(os.path.abspath(__file__))
        print(os.path.dirname(os.path.normpath(path)))

        #print os.path.dirname(sys.modules['__main__'].__file__)



    winWidth = 800
    @classmethod
    def openUI(self, winTitle = "Project Setup", winName = None):
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

