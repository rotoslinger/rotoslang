import sys
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import inspect

# Utility function to get Maya's main window
def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class MethodInspectorUI(QtWidgets.QDialog):
    def __init__(self, obj=None, parent=get_maya_main_window()):
        super(MethodInspectorUI, self).__init__(parent)
        
        self.setWindowTitle("Method Inspector")
        self.resize(600, 400)  # Set initial size

        # Layout
        main_layout = QtWidgets.QVBoxLayout(self)

        # Text Field
        self.obj_text_field = QtWidgets.QLineEdit(self)
        self.obj_text_field.setPlaceholderText("Enter Python object...")
        self.obj_text_field.textChanged.connect(self.update_method_list)
        main_layout.addWidget(self.obj_text_field)

        # Splitter for scroll areas
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Methods List Scroll Area
        self.methods_list_widget = QtWidgets.QListWidget(self)
        self.methods_list_widget.itemClicked.connect(self.display_method_help)
        self.splitter.addWidget(self.methods_list_widget)

        # Help Text Field
        self.help_text_field = QtWidgets.QTextEdit(self)
        self.help_text_field.setReadOnly(True)
        self.splitter.addWidget(self.help_text_field)

        # Add splitter to main layout
        main_layout.addWidget(self.splitter)

        # Set layout
        self.setLayout(main_layout)

        self.obj = obj
        if obj:
            self.update_method_list()

    def update_method_list(self):
        self.methods_list_widget.clear()
        self.help_text_field.clear()
        
        obj_text = self.obj_text_field.text()
        if not obj_text:
            return

        try:
            obj = eval(obj_text)
            if not hasattr(obj, '__class__'):
                return

            methods = [method for method in dir(obj) if callable(getattr(obj, method))]
            self.methods_list_widget.addItems(sorted(methods))
        except:
            pass

    def display_method_help(self, item):
        obj_text = self.obj_text_field.text()
        if not obj_text:
            return

        try:
            obj = eval(obj_text)
            method_name = item.text()
            method = getattr(obj, method_name, None)
            if method:
                doc = inspect.getdoc(method)
                self.help_text_field.setText(doc if doc else "No documentation available.")
            else:
                self.help_text_field.setText("Method not found.")
        except:
            self.help_text_field.setText("Error retrieving method help.")

# Create and show the UI
def show_method_inspector_ui(obj=None):
    global method_inspector_ui
    try:
        method_inspector_ui.close()  # Close existing window if it's open
    except:
        pass
    method_inspector_ui = MethodInspectorUI(obj)
    method_inspector_ui.show()

# Call function to show the UI
show_method_inspector_ui()
