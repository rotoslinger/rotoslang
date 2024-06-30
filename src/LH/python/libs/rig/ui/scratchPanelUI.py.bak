import sys
from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance

'''
@code
from uiSSP.rigging.uiStackTest import uiStackTest
uiStackTest.UiStackTest.openUI()
@endcode
'''
class UiStackTest(QtWidgets.QWidget):

    def __init__(self, parent=None, winTitle = "UI Stack", winName = None):
        super(UiStackTest, self).__init__(parent)
        #main widget setting
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(winTitle)
        self.setObjectName(winName)


    winWidth = 150
    @classmethod
    def openUI(self, winTitle = "UI Stack", winName = None):
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
        globals()[winName] = UiStackTest(mayaWin, winTitle, winName)
        globals()[winName].show()
        return globals()[winName]




