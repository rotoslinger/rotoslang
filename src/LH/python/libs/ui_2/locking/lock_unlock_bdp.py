import sys
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import importlib
from ui_2.python_debugging import obj_inspect
importlib.reload(obj_inspect)

ui_inspect = obj_inspect.ui_inspect


# Utility function to get Maya's main window
def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class SimpleUI(QtWidgets.QDialog):
    def __init__(self, parent=get_maya_main_window()):
        super(SimpleUI, self).__init__(parent)
        
        self.setWindowTitle("Simple UI")
        self.setMinimumWidth(300)  # Set a minimum width for the window
        self.setMinimumHeight(100) # Set a minimum height for the window

        # Layout
        main_layout = QtWidgets.QVBoxLayout(self)

        # Checkboxes
        self.draw_override_cb = QtWidgets.QCheckBox("Drawing Overrides")
        self.locked_cb = QtWidgets.QCheckBox("Locked")
        self.templated_cb = QtWidgets.QCheckBox("Templated")
        self.black_boxed_cb = QtWidgets.QCheckBox("Black Boxed")
                # Set checkboxes to true by default
        self.draw_override_cb.setChecked(True)
        self.locked_cb.setChecked(True)
        self.templated_cb.setChecked(True)
        self.black_boxed_cb.setChecked(True)


        # Add checkboxes to layout
        main_layout.addWidget(self.draw_override_cb)
        main_layout.addWidget(self.locked_cb)
        main_layout.addWidget(self.templated_cb)
        main_layout.addWidget(self.black_boxed_cb)

        # Button layout
        button_layout = QtWidgets.QHBoxLayout()

        # Buttons
        self.button1 = QtWidgets.QPushButton("Lock")
        self.button2 = QtWidgets.QPushButton("Unlock")
        ui_inspect(QtWidgets.QPushButton)

        # Add buttons to button layout
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        
        # Add button layout to main layout
        main_layout.addLayout(button_layout)

        # Set layout
        self.setLayout(main_layout)

# Create and show the UI
def show_simple_ui():
    global simple_ui  # Declare as global before it's first used
    try:
        simple_ui.close()  # Close existing window if it's open
    except:
        pass
    simple_ui = SimpleUI()  # Instantiate the UI
    simple_ui.show()  # Show the UI

# Call function to show the UI
show_simple_ui()
