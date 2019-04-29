import sys
from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
import utils as ui_utils
reload(ui_utils)
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
scratch_panel.Scratch_Panel.openUI()

@endcode
'''
class Scratch_Panel(QtWidgets.QWidget):

    def __init__(self, parent=None, winTitle = "Scratch Panel", winName = None):
        super(Scratch_Panel, self).__init__(parent)
        #main widget setting
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(winTitle)
        self.setObjectName(winName)
        self.setAcceptDrops(True) # Very important

        self.create_layout()
        self.create_connections()

    def create_layout(self):
        # left list
        self.list_widget_l = QtWidgets.QListWidget(self)
        self.list_widget_l.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_widget_l.setAcceptDrops(True)
        # Allow drag and drop reorder
        self.list_widget_l.setDragDropMode(self.list_widget_l.InternalMove)
        # self.list_widget_l.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        # right list
        self.list_widget_r = QtWidgets.QListWidget(self)
        self.list_widget_r.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_widget_r.setAcceptDrops(True)
        self.list_widget_r.setDragDropMode(self.list_widget_r.InternalMove)


        #add button
        self.add_btn_l = QtWidgets.QPushButton("Add To List")
        self.remove_btn_l = QtWidgets.QPushButton("Remove From List")
        self.clear_btn_l = QtWidgets.QPushButton("Clear List")


        self.add_btn_r = QtWidgets.QPushButton("Add To List")
        self.remove_btn_r = QtWidgets.QPushButton("Remove From List")
        self.clear_btn_r = QtWidgets.QPushButton("Clear List")

        self.gridLayout=QtWidgets.QGridLayout()

        #--create the layout vbox#$#$#$
        main_layout= QtWidgets.QVBoxLayout()
        
        ################ to reduce button margins and the spacing
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addLayout(self.gridLayout, 1) # stretch factor > 0
        main_layout.addStretch(0) # 0 is full stretch
        
        # 
        self.gridLayout.addWidget(self.list_widget_l, 0, 0)
        self.gridLayout.addWidget(self.add_btn_l, 1, 0)
        self.gridLayout.addWidget(self.remove_btn_l, 2, 0)
        self.gridLayout.addWidget(self.clear_btn_l, 3, 0)
                
        self.gridLayout.addWidget(self.list_widget_r, 0, 1)
        self.gridLayout.addWidget(self.add_btn_r, 1, 1)
        self.gridLayout.addWidget(self.remove_btn_r, 2, 1)
        self.gridLayout.addWidget(self.clear_btn_r, 3, 1)

        #add the main layout itself to the primitive ui dialog
        self.setLayout(main_layout)

    def dropEvent(self, event):
        """
        The event called when the user drops its elements
        Only if dragEnterEvent accept the event
        """
        print "AAAAAAAAAAAAAAAA"

    def create_connections(self):

        # L List
        # We could do this with lamda like below.  Not using because it is hard to read...
        # self.add_btn_l.clicked.connect(lambda widget_arg=self.list_widget_l: self.add_to_list(widget_arg))
        self.add_btn_l.clicked.connect(self.add_to_list_l)
        self.remove_btn_l.clicked.connect(self.remove_from_list_l)
        self.clear_btn_l.clicked.connect(lambda : self.list_widget_l.clear())
        self.list_widget_l.itemSelectionChanged.connect(self.clicked)
        self.list_widget_l.itemSelectionChanged.connect(self.clicked)
        # def test():
        #     print "aaaaa"
        # self.list_widget_l.dropEvent(test)
        # R List
        self.add_btn_r.clicked.connect(self.add_to_list_r)
        self.remove_btn_r.clicked.connect(self.remove_from_list_r)
        self.clear_btn_r.clicked.connect(lambda : self.list_widget_r.clear())
        self.list_widget_r.itemSelectionChanged.connect(self.clicked)

    

    def remove_from_list_l(self):
        self.remove_from_list(self.list_widget_l)

    def remove_from_list_r(self):
        self.remove_from_list(self.list_widget_r)

    def remove_from_list(self, list_widget):
        selected = cmds.ls(sl=True)
        # Filter objects that are already in the list
        if not selected:
            return
        for sel in selected:
            # Have to map the rows every time because the list is re indexed every time an item is removed
            items =  {str(list_widget.item(i).text()):i for i in range(list_widget.count())}
            list_widget.takeItem(items.get(sel))


    def add_to_list_l(self):
        self.add_to_list(self.list_widget_l)

    def add_to_list_r(self):
        self.add_to_list(self.list_widget_r)

    def add_to_list(self, list_widget):
        selected = cmds.ls(sl=True)
        # Filter objects that are already in the list
        items =  [str(list_widget.item(i).text()) for i in range(list_widget.count())]
        selected = [x for x in selected if x not in items]
        if not selected:
            return
        for sel in selected:
            icon = ui_utils.get_outliner_icon(sel)
            item = QtWidgets.QListWidgetItem(icon, sel)
            list_widget.addItem( item)


    def clicked(self):
        items_l = self.list_widget_l.selectedItems()
        items_r = self.list_widget_r.selectedItems()
        items = items_l + items_r
        x = []
        for i in range(len(items)):
            x.append(str(items[i].text()))
        cmds.select(x)



    winWidth = 800
    @classmethod
    def openUI(self, winTitle = "Scratch Panel", winName = None):
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
        mayaWin = wrapInstance(long(ptr), QtWidgets.QMainWindow)
        globals()[winName] = Scratch_Panel(mayaWin, winTitle, winName)
        globals()[winName].show()
        return globals()[winName]




