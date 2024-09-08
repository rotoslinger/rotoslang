import maya.cmds as cmds
import maya.api.OpenMaya as om2
import os
import json
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

import importlib
from ui_2.python_debugging import obj_inspect
importlib.reload(obj_inspect)


# Utility function to get Maya's main window
def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

# Function to get scene name and directory
def get_scene_info():
    scene_name = cmds.file(q=True, sceneName=True, shortName=True).split('.')[0]
    scene_dir = cmds.file(q=True, sceneName=True).rsplit('/', 1)[0]
    print(scene_dir)
    print(scene_name)
    return scene_name, scene_dir

# Function to select a directory
def select_directory(directory_field):
    multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII(*.ma);;Maya Binary(*.mb);;Json Files(*.json)"
# openDailog.Filter = "Json files (*.json)|*.json|Text files (*.txt)|*.txt";
    multipleFilters = "JSON Files (*.json);;Text Files (*.txt);;All Files (*.*)"

    selected_dir = cmds.fileDialog2(fm=0, ds=2, fileFilter=multipleFilters)[0]  # Directory selection mode
    directory_field.setText(selected_dir)

# Function to save lock settings
def save_lock_settings(settings, directory, scene_name):
    settings_path = os.path.join(directory, "{}_LOCK_SETTINGS.json".format(scene_name))
    # Versioning if file already exists
    if os.path.exists(settings_path):
        version = 1
        while os.path.exists(settings_path):
            version_str = "_v{:03d}".format(version)
            settings_path = os.path.join(directory, "{}_LOCK_SETTINGS{}.json".format(scene_name, version_str))
            version += 1
    
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)
    
    print("Lock settings saved to: {}".format(settings_path))

# Function to retrieve the lock settings file
def load_lock_settings(directory, scene_name):
    settings_path = os.path.join(directory, "{}_LOCK_SETTINGS.json".format(scene_name))
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            return json.load(f)

    return None

# Function to update user_settings based on scene
def gather_scene_settings():
    locked_nodes, templated_nodes, blackboxed_nodes = [], [], []
    
    # Get selection list and filter valid DAG paths
    # selection_list = om2.MGlobal.getSelectionListByName("*")
    # print(type(selection_list))
    # Get all objects in the scene
    all_objects = cmds.ls(dag=True, long=True)  # Get all DAG objects, including shapes

    # Loop through all objects
    for obj in all_objects:
        # Check if the object is locked
        if cmds.lockNode(obj, q=True, lock=True)[0]:
            locked_nodes.append(obj)
        
        # Check if the object is templated
        if cmds.attributeQuery('template', node=obj, exists=True):
            if cmds.getAttr(obj + ".template") == 1:
                templated_nodes.append(obj)
        
        # Check if the object is blackboxed
        if cmds.attributeQuery('blackBox', node=obj, exists=True):
            if cmds.getAttr(obj + ".blackBox") == 1:
                blackboxed_nodes.append(obj)
    
    return {
        'locked_nodes': locked_nodes if locked_nodes else ["none"],
        'templated_nodes': templated_nodes if templated_nodes else ["none"],
        'blackboxed_nodes': blackboxed_nodes if blackboxed_nodes else ["none"]
    }

# Function to unlock/untemplate/unblackbox nodes based on checkbox state
def unlock_nodes(lock_cb, template_cb, blackbox_cb, directory_field):
    scene_name, scene_dir = get_scene_info()
    directory = directory_field.text() or scene_dir
    settings = gather_scene_settings()
    print(settings)
    # Save current settings as a backup before unlocking
    save_lock_settings(settings, directory, scene_name)
    
    # Perform unlocking based on checkboxes
    if lock_cb.isChecked():
        for node in settings['locked_nodes']:
            if node != "none":
                cmds.lockNode(node, lock=False)
    
    if template_cb.isChecked():
        for node in settings['templated_nodes']:
            if node != "none":
                cmds.setAttr("{}.template".format(node), 0)
    
    if blackbox_cb.isChecked():
        for node in settings['blackboxed_nodes']:
            if node != "none":
                cmds.setAttr("{}.blackBox".format(node), 0)

# Function to lock/template/blackbox nodes based on checkbox state
def lock_nodes():
    settings = gather_scene_settings()
    for node in settings['locked_nodes']:
        if node != "none":
            cmds.lockNode(node, lock=True)
    print("Finished Locking")

    for node in settings['templated_nodes']:
        if node != "none":
            cmds.setAttr("{}.template".format(node), 1)
    print("Finished Templating")

    for node in settings['blackboxed_nodes']:
        if node != "none":
            cmds.setAttr("{}.blackBox".format(node), 1)
    print("Finished Blackboxing")

# UI
class LockUnlockToolUI(QtWidgets.QDialog):
    def __init__(self, parent=get_maya_main_window()):
        super(LockUnlockToolUI, self).__init__(parent)

        self.setWindowTitle("Lock/Unlock Tool")
        self.setMinimumWidth(300)  # Minimum width to ensure elements are not too cramped
        self.setMinimumHeight(250) # Minimum height to fit all elements

        self.scene_name, self.scene_dir = get_scene_info()

        # Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Small text to explain the checkboxes
        select_text = QtWidgets.QLabel("Select what to lock/unlock:")
        select_text.setStyleSheet("margin: 0px; padding: 5px;")
        main_layout.addWidget(select_text)

        # Checkboxes
        self.lock_cb = QtWidgets.QCheckBox("Locked Nodes")
        self.template_cb = QtWidgets.QCheckBox("Templated Nodes")
        self.blackbox_cb = QtWidgets.QCheckBox("Blackboxed Nodes")

        # Set checkboxes to true by default
        self.lock_cb.setChecked(True)
        self.template_cb.setChecked(True)
        self.blackbox_cb.setChecked(True)

        # Set tooltips
        self.lock_cb.setToolTip("Check to lock/unlock nodes that are locked.")
        self.template_cb.setToolTip("Check to template/untemplate nodes that are templated.")
        self.blackbox_cb.setToolTip("Check to blackbox/unblackbox nodes that are blackboxed.")
        
        main_layout.addWidget(self.lock_cb)
        main_layout.addWidget(self.template_cb)
        main_layout.addWidget(self.blackbox_cb)
        
        # Directory field and select button
        self.directory_field = QtWidgets.QLineEdit(self.scene_dir)
        self.directory_field.setToolTip("The directory where settings will be saved.")
        main_layout.addWidget(self.directory_field)

        select_button = QtWidgets.QPushButton("Select Directory")
        select_button.setToolTip("Click to choose a directory to save or load lock settings.")
        select_button.clicked.connect(lambda: select_directory(self.directory_field))
        main_layout.addWidget(select_button)
        
        # Unlock/Lock buttons
        unlock_button = QtWidgets.QPushButton("Unlock")
        unlock_button.setToolTip("Unlock the nodes based on the selected options.")
        unlock_button.clicked.connect(lambda: unlock_nodes(self.lock_cb, self.template_cb, self.blackbox_cb, self.directory_field))
        main_layout.addWidget(unlock_button)
        
        lock_button = QtWidgets.QPushButton("Lock")
        lock_button.setToolTip("Lock the nodes based on the selected options.")
        lock_button.clicked.connect(lambda: lock_nodes())
        main_layout.addWidget(lock_button)

        # Load existing lock settings from the scene directory
        existing_settings = load_lock_settings(self.scene_dir, self.scene_name)
        if existing_settings:
            # Update the UI based on previous settings (if they exist)
            self.lock_cb.setChecked("none" not in existing_settings['locked_nodes'])
            self.template_cb.setChecked("none" not in existing_settings['templated_nodes'])
            self.blackbox_cb.setChecked("none" not in existing_settings['blackboxed_nodes'])

# Function to create the UI window
def show_lock_unlock_tool_ui():
    global lock_unlock_tool_ui
    try:
        lock_unlock_tool_ui.close()  # Close existing window if it's open
    except:
        pass
    lock_unlock_tool_ui = LockUnlockToolUI()
    lock_unlock_tool_ui.show()

# Create and show the UI
show_lock_unlock_tool_ui()
