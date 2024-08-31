import os
from PySide6 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken6 import wrapInstance
from maya import cmds
class Node_Scratch_Panel(QtWidgets.QWidget):

    def __init__(self, parent=None, winTitle = "Node Scratch Panel", winName = None):
        super(Node_Scratch_Panel, self).__init__(parent)
        #main widget setting
        
        self.setWindowFlags(QtCore.Qt.Window)
        self.settings_path = os.path.join(os.getenv('HOME'), "scratchSettings.ini")

        self.setWindowTitle(winTitle)
        self.setObjectName(winName)
        self.setAcceptDrops(True)

        self.create_layout()
        self.create_connections()

    def create_layout(self):
        
        if os.path.exists(self.settings_path):
            settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
            self.restoreGeometry(settings_obj.value("windowGeometry"))
        for i in dir(self):
            if "save" in i or "restore" in i:
                print(i)

        # left list
        self.list_widget_l = LListWidget(self)
        self.list_widget_l.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_widget_l.setAcceptDrops(True)
        # Allow drag and drop reorder
        self.list_widget_l.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        # right list
        self.list_widget_r = QtWidgets.QListWidget(self)
        self.list_widget_r.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_widget_r.setAcceptDrops(True)
        self.list_widget_r.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)


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
        
        # to reduce button margins and the spacing
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addLayout(self.gridLayout, 1) # stretch factor > 0
        main_layout.addStretch(0) # 0 is full stretch
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

    def create_connections(self):

        # L List
        self.add_btn_l.clicked.connect(self.add_to_list_l)
        self.remove_btn_l.clicked.connect(self.remove_from_list_l)
        self.clear_btn_l.clicked.connect(lambda : self.list_widget_l.clear())
        self.list_widget_l.itemSelectionChanged.connect(self.clicked)
        self.list_widget_l.itemSelectionChanged.connect(self.clicked)
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
        first_level_selected =  cmds.ls(sl=True)
        # Filter objects that are already in the list
        items =  [str(list_widget.item(i).text()) for i in range(list_widget.count())]
        selected = [x for x in selected if x not in items]
        selected = [x for x in selected if x in first_level_selected]
        if not selected:
            return
        for sel in selected:
            print(cmds.objectType(sel))
            icon = get_outliner_icon(sel)
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

    def closeEvent(self, event):
        # Save window's geometry
        settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        settings_obj.setValue("windowGeometry", self.saveGeometry())


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
        mayaWin = wrapInstance(int(ptr), QtWidgets.QMainWindow)
        globals()[winName] = Node_Scratch_Panel(mayaWin, winTitle, winName)
        globals()[winName].show()
        return globals()[winName]


class LListWidget(QtWidgets.QListWidget):    
    def __init__(self, parent):
        super(LListWidget, self).__init__(parent)
        self.setAcceptDrops(True)

    def mimeTypes(self):
        mimetypes = super(LListWidget, self).mimeTypes()
        mimetypes.append('text/plain')
        return mimetypes

    def dropMimeData(self, index, data, action):
        if data.hasText():
            self.addItem(data.text())
            return True
        else:
            return super(LListWidget, self).dropMimeData(index, data, action)


def get_outliner_icon(maya_object):
    if not maya_object:
        maya_object = cmds.ls(sl=True)[0]
    maya_object_type = cmds.objectType(maya_object)
    maya_object_relatives = cmds.listRelatives(maya_object)
    # If the object is a transform and has a shape, set the type to that of the shape
    if maya_object_relatives != None and maya_object_type == "transform" and cmds.listRelatives(s=True) and len(cmds.listRelatives(maya_object)) == 1:
        maya_object_type = cmds.objectType(cmds.listRelatives(s=True)[0])
    file_dir = ":/{0}.svg".format(maya_object_type)
    testfile = QtCore.QFile(file_dir)
    if not testfile.exists():
        file_dir = ":/default.svg"
    return QtGui.QIcon(file_dir)

Node_Scratch_Panel.openUI()