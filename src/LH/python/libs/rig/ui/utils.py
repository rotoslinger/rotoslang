import sys
from PySide6 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken6 import wrapInstance
from maya import cmds

def get_outliner_icon(maya_object):
    if not maya_object:
        print("NOT OBJECT!!!!")
        maya_object = cmds.ls(sl=True)[0]
    maya_object_type = cmds.objectType(maya_object)
    # If the object is a transform and has a shape, set the type to that of the shape
    if maya_object_type == "transform" and cmds.listRelatives(s=True):
        maya_object_type = cmds.objectType(cmds.listRelatives(s=True)[0])
    print(maya_object_type)
    file_dir = ":/{0}.svg".format(maya_object_type)

    testfile = QtCore.QFile(file_dir)
    if not testfile.exists():
        file_dir = ":/default.svg"
    return QtGui.QIcon(file_dir)


