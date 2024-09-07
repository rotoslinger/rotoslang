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

        # Checkbox for Copy Selected Text
        self.copy_checkbox = QtWidgets.QCheckBox("Copy Selected Text", self)
        self.copy_checkbox.setChecked(True)  # Default to checked
        main_layout.addWidget(self.copy_checkbox)

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
            doc = inspect.getdoc(method)
            help_text = self.get_help_text(method)



            '''
            help_text = "{0}<b><u>Documentation:</u></b> \n {1} \n \n <b><u>Help:</u></b> \n {2}".format(
                "", help_text, "None"
            ) if doc else "{0}<b><u>Documentation:</u></b> \n {1} \n \n <b><u>Help:</u></b> \n {2}".format(
            '''



            doc_text = f"<b>Documentation:</b><br>{doc if doc else 'None'}"
            help_text = f"<b>Help:</b><br>{help_text if help_text else 'None'}"
            self.help_text_field.setHtml(f"{doc_text}<br><br>{help_text}")

            # Copy selected text if checkbox is checked
            if self.copy_checkbox.isChecked():
                clipboard = QtWidgets.QApplication.clipboard()
                clipboard.setText("." + method_name)
        except:
            self.help_text_field.setHtml("Error retrieving method help.")

    def get_help_text(self, obj):
        """Get the help text for the given object."""
        try:
            # This is a placeholder; adjust based on your needs for extracting help.
            if obj:
                return str(obj)
            return ""
        except:
            return ""

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
