# from PySide import QtCore
# from PySide import QtGui
from PySide2 import QtWidgets, QtCore, QtGui

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import cmds
from ui_2.stack.guide_ui import ui as guide
import importlib
importlib.reload(guide)
from ui_2.stack.weight_ui import ui as weight
importlib.reload(weight)



class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    def __init__(self,
                 parent=None,
                #  win_title = "Base Utilities",
                 win_name = "Rig Tools",
                 
                 
                 
                 ):
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowTitle(win_name)
        self.setObjectName(win_name)

        # # Main widget
        # main_widget = QtWidgets.QWidget()
        # main_layout = QtWidgets.QVBoxLayout()
        # main_layout.setAlignment(QtCore.Qt.AlignTop)
        # # # Create UI widgets
        # # self.test_btn = QtWidgets.QPushButton('Test')

        # # # Attach widgets to the main layout
        # # main_layout.addWidget(self.test_btn)

        # # # Set main layout
        # main_widget.setLayout(main_layout)
        # self.setCentralWidget(main_widget)

        # # Connect buttons signals
        # self.test_btn.clicked.connect(self.on_test_btn_click)
        
        guide_widget = QtWidgets.QDockWidget("Guide Dock", self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, guide_widget)
        weight_widget = QtWidgets.QDockWidget("Weight Dock", self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, weight_widget)
        self.tabifyDockWidget(guide_widget, weight_widget)

        self.guide_ui = guide.Guide_UI()
        guide_widget.setWidget(self.guide_ui)
        self.guide_ui.openUI()



        self.weight_ui = weight.Weight_UI()
        weight_widget.setWidget(self.weight_ui)
        self.weight_ui.openUI()


    # def closeEvent(self, event):
    #     self.guide_ui.closeEvent()
    #     self.weight_ui.closeEvent()



def main():
    win_name = "Rig Tools"
    control_name = "{0}WorkspaceControl".format(win_name)
    deleteControl(control_name)
    try:
        try:
            globals()[win_name].close()
            globals()[win_name].deleteLater()
        except:
            pass
        del globals()[win_name]
    except:
        pass
    
    
    w = MainWindow(win_name=win_name)
    
    
    w.show(dockable=True, floating=False, area="left", allowedArea="left")
    cmds.workspaceControl(control_name, e=True , ttc=["AttributeEditor", 0], wp="preferred", mw=420, dockToMainWindow=["left", True], floating=False)
    # w.raise_()


def deleteControl(control_name):
    if cmds.workspaceControl(control_name, q=True, exists=True):
        cmds.workspaceControl(control_name, e=True, close=True)
        cmds.deleteUI(control_name, control=True)
