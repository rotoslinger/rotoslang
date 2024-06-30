import sys
from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
from . import utils as ui_utils
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
from rig.ui import weightstack
weightstack.WeightStackWidget.openUI()@endcode
'''
class WeightStackWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, winTitle = "Weight Stack", winName = None):
        super(WeightStackWidget, self).__init__(parent)
        #main widget setting
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(winTitle)
        self.setObjectName(winName)
        self.create_layout()
        self.create_connections()

    def create_layout(self):
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        #add button
        self.add_btn = QtWidgets.QPushButton("Add To List")
        self.gridLayout=QtWidgets.QGridLayout()

        #--create the layout vbox#$#$#$
        main_layout= QtWidgets.QVBoxLayout()
        
        ################ to reduce button margins and the spacing
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addLayout(self.gridLayout, 1) # stretch factor > 0
        main_layout.addStretch(0) # 0 is full stretch
            
        self.gridLayout.addWidget(self.listWidget, 0, 1)
        self.gridLayout.addWidget(self.add_btn, 1, 1)
                
        #add the main layout itself to the primitive ui dialog
        self.setLayout(main_layout)

    def create_connections(self):
        self.add_btn.clicked.connect(self.add_to_list)   # 
        #self.listWidget.itemClicked.connect(self.clicked)
        self.listWidget.itemSelectionChanged.connect(self.clicked)

    def add_to_list(self):
        selected = cmds.ls(sl=True)
        # Filter objects that are already in the list
        items =  [str(self.listWidget.item(i).text()) for i in range(self.listWidget.count())]
        selected = [x for x in selected if x not in items]
        if not selected:
            return
        for sel in selected:
            icon = ui_utils.get_outliner_icon(sel)
            item = QtWidgets.QListWidgetItem(icon, sel)

            self.listWidget.addItem( item)

    def clicked(self):
        items = self.listWidget.selectedItems()
        x = []
        for i in range(len(items)):
            x.append(str(self.listWidget.selectedItems()[i].text()))
        cmds.select(x)



    winWidth = 800
    @classmethod
    def openUI(self, winTitle = "Weight Stack", winName = None):
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
        globals()[winName] = WeightStackWidget(mayaWin, winTitle, winName)
        globals()[winName].show()
        return globals()[winName]




