import os, shutil

import maya.cmds as cmds


def onMayaDroppedPythonFile(debug_path=False):
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



    print(copy_to_dir)
