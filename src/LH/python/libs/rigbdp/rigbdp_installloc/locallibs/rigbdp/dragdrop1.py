import os, importlib

import maya.cmds as cmds

importlib.reload(__file__)

def onMayaDroppedPythonFile(path):
    lib_copy_dir = os.path.dirname(os.path.realpath(__file__))  # Directory of the script

    maya_script_dir = cmds.internalVar(userScriptDir=True)

    root_dir_name = os.path.basename(lib_copy_dir)  # Use the current directory's name

    print(maya_script_dir)

