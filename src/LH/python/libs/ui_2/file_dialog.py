import sys, os
from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds

OPERATING_SYSTEM = sys.platform

class File_Dialog(QtWidgets.QWidget):
    def __init__(self,
                 parent = None,
                 default_path=None,
                 default_filename = "newBuilder.py"):
        self.default_path = default_path
        self.default_filename = default_filename
        super(File_Dialog, self).__init__(parent)
        layout = QtWidgets.QGridLayout()
            
        self.get_default_path()

        self.contents = QtWidgets.QLineEdit()
        self.contents.setText(self.default_path)
        layout.addWidget(self.contents,0,0)
        self.setLayout(layout)
            
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.getfiles)
        layout.addWidget(self.browse_button,0,1)

    def get_default_path(self):
        # gets default file from directory of this file
        # Default file
        if self.default_path:
            return
        seperator = "/{0}"
        if OPERATING_SYSTEM == "win32" or OPERATING_SYSTEM == "win64":
            seperator =  r"\{0}"

        self.default_path = os.path.dirname(os.path.abspath(__file__))
        self.default_path= os.path.dirname(os.path.normpath(self.default_path))
        self.default_path = self.default_path + seperator.format("builders") + seperator.format(self.default_filename) 

    def getfiles(self):
        diologue = QtWidgets.QFileDialog(directory =self.contents.text() )
        diologue.setFileMode(QtWidgets.QFileDialog.AnyFile)
            
        if diologue.exec_():
            filename = diologue.selectedFiles()
            if not filename:
                return
            filename = filename[0]
            self.contents.setText(filename)