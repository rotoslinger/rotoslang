import sys
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import inspect
import io
import importlib

# Get Maya's main window
def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class ObjectInspectorUI(QtWidgets.QDialog):
    def __init__(self, obj=None, parent=get_maya_main_window()):
        super(ObjectInspectorUI, self).__init__(parent)
        
        self.setWindowTitle("Method Inspector")
        self.resize(600, 400)  # Set initial size

        # Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        new_obj = str(obj)
        new_obj = class_cleanup((new_obj))
        is_lib = False
        try:
            new_obj = eval(new_obj)
        except:
            is_lib = True
        obj = str(obj)
        obj = class_cleanup(obj=obj, is_lib=is_lib)

        # Text Field
        self.obj_text_field = QtWidgets.QLineEdit(self)
        self.obj_text_field.setPlaceholderText("Enter a python object")
        self.obj_text_field.textChanged.connect(self.update_method_list)
        main_layout.addWidget(self.obj_text_field)

        # Checkbox for Copy Selected Text
        self.copy_checkbox = QtWidgets.QCheckBox("Copy Selected Text ---> prefixes with '.' for easy object traversal", self)
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

        self.obj_text_field.setText(str(obj))

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
            # vars = [var for var in vars(obj)]
            self.methods_list_widget.addItems(["############# CALLABLES #############"])

            self.methods_list_widget.addItems(sorted(methods))
            self.methods_list_widget.addItems(["\n","############### VARS ###############",])

            self.methods_list_widget.addItems(vars(obj))
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
            obj_type = type(method)
            type_text = "############### Type ###############\n##################################\n{0}".format(obj_type)
            doc_text = "\n########## Documentation ###########\n##################################\n{0}".format(doc if doc else 'None')
            help_text = "\n############### Help ###############\n##################################\n{0}".format(help_text if help_text else 'None')
            self.help_text_field.setText("{0}\n\n{1}\n\n{2}".format(type_text, doc_text, help_text))

            # Copy selected text if checkbox is checked
            if self.copy_checkbox.isChecked():
                clipboard = QtWidgets.QApplication.clipboard()
                clipboard.setText(".{0}".format(method_name))
        except:
            self.help_text_field.setText("Error retrieving method help.")

    def get_help_text(self, obj):
        """Get the help text for the given object."""
        try:
            # Create a string buffer
            buffer = io.StringIO()

            # Save the original stdout and stderr
            original_stdout = sys.stdout
            original_stderr = sys.stderr

            try:
                # Redirect stdout and stderr to the buffer
                sys.stdout = buffer
                sys.stderr = buffer

                # Call help() on the object
                help(obj)
            except Exception as e:
                # Handle any exceptions that occur
                return "Error capturing help: {0}".format(str(e))
            finally:
                # Restore the original stdout and stderr
                sys.stdout = original_stdout
                sys.stderr = original_stderr

                # Get the string from the buffer
                help_text = buffer.getvalue()

                # Close the buffer
                buffer.close()

            return help_text
        except:
            return ""


def is_library(obj):
    try:
        # Get the module name where the object is defined
        module_name = obj.__class__.__module__
        
        # Extract the top-level package name (first part)
        library_name = module_name.split('.')[0]
        
        try:
            # Try to import the top-level package
            imported_lib = importlib.import_module(library_name)
            
            # Check if it contains submodules or specific properties
            if hasattr(imported_lib, '__path__'):
                return True, library_name
            else:
                return False, f"{library_name} is a module but not a library"
        except ImportError as e:
            # If it cannot be imported, return an error message
            return False, f"Could not import library: {library_name}, error: {str(e)}"
    
    except AttributeError as e:
        # Handle cases where obj.__class__.__module__ is not available or valid
        return False, f"Object does not have a valid module: {str(e)}"
    
    except Exception as e:
        # Catch-all for any other unexpected issues
        return False, f"Unexpected error: {str(e)}"

# Example usage
# obj = QtWidgets.QVBoxLayout()
# is_lib, library_name = is_library(obj)
def class_cleanup(obj, is_lib = False):
    # remember:
    # obj_string = str(QtWidgets)
    # returns <module 'PySide2.QtWidgets' from 'C:\\Program Files\\Autodesk\\Maya2024\\Python\\lib\\site-packages\\PySide2\\QtWidgets.cp310-win_amd64.pyd'>
    # when splitting make sure to do first index, then second index to get the class and not the library
    obj = str(obj)
    if "'" in obj:
        obj = obj.split("'")[1]
    if "'" in obj:
        obj = obj.split("'")[0]
    if is_lib and "." in obj:
        obj = obj.split(".")[1]
    return obj

# Create and show the UI
def ui_inspect(obj=None):
    global object_inspector_ui
    try:
        object_inspector_ui.close()  # Close existing window if it's open
    except:
        pass
    object_inspector_ui = ObjectInspectorUI(obj)
    object_inspector_ui.show()

# Call function to show the UI

