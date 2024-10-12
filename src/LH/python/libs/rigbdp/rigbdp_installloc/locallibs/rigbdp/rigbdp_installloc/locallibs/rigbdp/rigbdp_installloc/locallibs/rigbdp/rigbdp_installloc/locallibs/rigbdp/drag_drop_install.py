# builtins
import os, sys, shutil

# third party
import maya.cmds as cmds

# bdp
from rigbdp.ui import dyn_button_ui

def install_python_library(modules=None, debug_path=False):
    # Get the absolute path of the directory containing this script
    install_script_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.abspath(os.path.join(install_script_dir, os.pardir))  # Get the parent directory

    # Determine the destination directory
    if debug_path:
        maya_script_dir = debug_path
    else:
        if sys.platform.startswith('win'):
            maya_script_dir = os.path.join(os.getenv('USERPROFILE'), 'Documents', 'maya', 'scripts')
        elif sys.platform == 'darwin':
            maya_script_dir = os.path.join(os.getenv('HOME'), 'Library', 'Preferences', 'Autodesk', 'maya', 'scripts')
        else:
            maya_script_dir = os.path.join(os.getenv('HOME'), 'maya', 'scripts')
    
    # Create the destination directory if it doesn't exist
    if not os.path.exists(maya_script_dir):
        os.makedirs(maya_script_dir)
    
    # Copy the root directory to the destination directory
    root_dir_name = os.path.basename(root_dir)
    lib_dst = os.path.join(maya_script_dir, root_dir_name)
    
    if os.path.exists(lib_dst):
        shutil.rmtree(lib_dst)  # Remove existing library to ensure a clean install
    
    shutil.copytree(root_dir, lib_dst)
    print(f"Library installed successfully to: {lib_dst}")

    # Create shelf buttons if modules are provided
    if modules:
        create_shelf_buttons(modules)

def create_shelf_buttons(modules):
    # Get the current shelf tab name
    shelf_tab = 'Shelf'
    
    # Ensure the shelf exists
    if not cmds.shelfLayout(shelf_tab, exists=True):
        cmds.shelfLayout(shelf_tab, p='MayaWindow')

    for module in modules:
        button_name = f"{module}_button"
        button_command = f"import {module}\n{module}.run()"  # Replace 'run()' with the actual function you want to call
        
        # Check if the button already exists to avoid duplicates
        if not cmds.shelfButton(button_name, exists=True):
            cmds.shelfButton(
                button_name,
                label=module,
                command=button_command,
                annotation=f"Run {module}",
                image='pythonFamily.png',  # You can change the image to any valid Maya image
                parent=shelf_tab
            )
            print(f"Shelf button created for module: {module}")
        else:
            print(f"Shelf button for {module} already exists.")

# Example usage with modules and debug path
# install_python_library(modules=[dyn_button_ui], debug_path=r'C:\Users\harri\Documents\Github\rotoslang\src\LH\python\rigbdprigbdp_installloc')
install_python_library(modules=[], debug_path=r'C:\Users\harri\Documents\Github\rotoslang\src\LH\python\libs\rigbdp\rigbdp_installloc')
