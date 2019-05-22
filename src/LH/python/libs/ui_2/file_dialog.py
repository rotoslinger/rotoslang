import sys, os
from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds

OPERATING_SYSTEM = sys.platform

class File_Dialog(QtWidgets.QWidget):
    def __init__(self,
                 parent = None,
                 asset_name="baseAsset",
                 default_path=None,
                 default_backup_path=None,
                 default_filename = "baseGuides.py",
                #  contents_changed_func=None
                 
                 ):
        self.asset_name = asset_name
        self.default_path = default_path
        self.default_backup_path = default_backup_path
        self.default_filename = default_filename
        self.root_path = ""
        self.filename=""

        super(File_Dialog, self).__init__(parent)
        layout = QtWidgets.QGridLayout()
            
        # self.get_default_path()

        self.contents = QtWidgets.QLineEdit()
        self.get_default_path()
        # self.contents.setText(self.default_path)
        # if contents_changed_func:
        #     self.contents.textChanged.connect(self.test_func)
        layout.addWidget(self.contents,0,0)
        self.setLayout(layout)
            
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.getfiles)
        layout.addWidget(self.browse_button,0,1)

    # def test_func(self):
    #     print self.contents.text()

    def get_filename(self):
        self.get_delimeter()
        stripped_filename = self.contents.text().split(self.delimeter)[-1]
        if ".py" in stripped_filename:
            stripped_filename = stripped_filename.split(".py")[0]
        return stripped_filename

    def get_default_path(self):
        # gets default file from directory of this file
        # Default file
        if self.default_path:
            return

        self.get_delimeter()

        self.default_path = os.path.dirname(os.path.abspath(__file__))
        self.default_path= os.path.dirname(os.path.normpath(self.default_path))
        self.asset = ""
        if self.asset_name:
            self.asset = self.delimeter + self.asset_name
        self.root_path = self.default_path + self.delimeter + "builders" + self.asset
        self.default_path = self.root_path + self.delimeter + self.default_filename
        self.default_backup_path = self.root_path
        self.contents.setText(self.default_path)
        self.get_filename()

    def getfiles(self):
        diologue = QtWidgets.QFileDialog(directory =self.contents.text() )
        diologue.setFileMode(QtWidgets.QFileDialog.AnyFile)
            
        if diologue.exec_():
            filepath = diologue.selectedFiles()
            if not filepath:
                return
            filepath = filepath[0]
            self.contents.setText(filepath)
    
    def get_delimeter(self):
        self.delimeter = "/"
        if OPERATING_SYSTEM == "win32" or OPERATING_SYSTEM == "win64":
            self.delimeter =  "\\"
