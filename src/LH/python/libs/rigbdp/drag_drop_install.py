#builtins
import os, shutil, importlib

#thirdparty
import maya.cmds as cmds

#bdp
# from rigbdp.shelf import add
# from rigbdp.shelf import bdpshelf

# #reloads
# importlib.reload(add)

# -------------------------------------------------------------------------------
# - Important to note --- importlib.reload() is broken for drag drop:
#
#   When working on a function that uses onMayaDroppedPythonFile
#   you have no means of reloading. If you update the function you will need to 
#   restart maya to test the drag-drop function again.
#   I would recommend opening a maya session and using reload for refreshing.
#   This will not fix the drag drop issue, but you can call the function directly.
#
#   Once testing is finished, restart maya, then drag drop to be sure things work.
# -------------------------------------------------------------------------------

def onMayaDroppedPythonFile(debug=False):
    # Find the path of the currently running script
    module_path = os.path.dirname(os.path.realpath(__file__))

    # Find Maya's user directory and the Maya.env file location
    maya_user_dir = cmds.internalVar(userAppDir=True)
    maya_version = cmds.about(version=True)
    env_dir = os.path.join(maya_user_dir, maya_version)
    env_file = os.path.join(env_dir, "Maya.env")

    # Ensure the file path is properly formatted for the current OS
    env_file = os.path.normpath(env_file)
    module_path = os.path.normpath(module_path)

    if debug:
        print(f"Debug Mode: ON")
        print(f"Drag Drop Install path to copy: {module_path}")
        print(f"Maya.env location: {env_file}")

    # Check if the Maya.env file exists
    if not os.path.exists(env_file):
        if debug:
            print("Maya.env does not exist yet.")
        return

    # Read the current contents of Maya.env
    with open(env_file, 'r') as f:
        env_content = f.readlines()

    # Find the current PYTHONPATH in the Maya.env file
    pythonpath_line = next((line for line in env_content if line.startswith("PYTHONPATH=")), None)

    # Get current paths, or initialize an empty list if PYTHONPATH is not found
    if pythonpath_line:
        current_paths = pythonpath_line.strip().split('=')[1].split(';')

        # Remove any empty strings caused by trailing semicolons
        current_paths = [p for p in current_paths if p]

    else:
        current_paths = []

    if debug:
        print(f"Current PYTHONPATH: {pythonpath_line}")
        print(f"Current paths list: {current_paths}")

    # Check if the module_path is already in PYTHONPATH
    if module_path not in current_paths:
        current_paths.append(module_path)

    # Prepare the new PYTHONPATH entry
    new_pythonpath = "PYTHONPATH=" + ';'.join(os.path.normpath(p) for p in current_paths)

    if debug:
        print(f"PYTHONPATH after modification: {new_pythonpath}")
        print(f"New Maya.env would look like:\n{new_pythonpath}")
    
    # If not in debug mode, write the changes to Maya.env
    if not debug:
        with open(env_file, 'w') as f:
            # Write back all non-PYTHONPATH lines first
            for line in env_content:
                if not line.startswith("PYTHONPATH="):
                    f.write(line)
            # Write the updated PYTHONPATH at the end
            f.write(new_pythonpath + "\n")
        print(f"PYTHONPATH updated in Maya.env successfully.")
    # bdpshelf.create()
    # add.create(lockui, 'BDP Rigging', debug=False)

################################### Usage ############################################
'''
This functions in this module should not be run from the command line.
Instead, in a file browser drag it to a maya viewport and drop it for installation.
'''
######################################################################################



#########################################################################################################
# This function is not currently used.
# - It still needs some work, but would be best used to do a permanent install
#   if code will not be changing
# 
def copy_library_dragdrop(debug_path=False):
    # get the library you are going to copy for the install
    # make sure
    copy_src_dir = os.path.dirname(os.path.realpath(__file__))  # Directory of the script

    # likely unneeded, but maya has a tendency of mangling paths
    # because this will be run in maya and things may change, might as well be overly careful
    copy_src_dir = os.path.normpath(copy_src_dir) 

    copy_to_dir = cmds.internalVar(userScriptDir=True)
    if debug_path:
        debug_path=os.path.normpath(debug_path)
        copy_to_dir = debug_path

    # if it doesn't exist create the libs dir
    libs_path = os.path.join(copy_to_dir, "locallibs")
    if not os.path.exists(libs_path):
        os.makedirs(libs_path)
    libs_path = os.path.normpath(libs_path) #---shouldn't need to do this again for libs or init...

    # Create the __init__.py file if it doesn't exist
    init_file_path = os.path.join(libs_path, '__init__.py')
    if not os.path.exists(init_file_path):
        with open(init_file_path, 'w') as init_file:
            init_file.write('"Generated from a drag drop install"')
    copy_to_dir = libs_path

    # Copy the directory where the install script is located to the destination directory
    root_dir_name = os.path.basename(copy_src_dir)  # Use the current directory's name
    copy_to_dir = os.path.join(copy_to_dir, root_dir_name)

    if os.path.exists(copy_to_dir):
        print("removing dir tree")
        # shutil.rmtree(lib_dst)  # Remove existing library to ensure a clean install

    shutil.copytree(copy_src_dir, copy_to_dir)

