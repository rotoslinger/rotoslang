import sys
from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds

def get_outliner_icon(maya_object):
    if not maya_object:
        maya_object = cmds.ls(sl=True)[0]
    maya_object_type = cmds.objectType(maya_object)
    # If the object is a transform and has a shape, set the type to that of the shape
    if maya_object_type == "transform" and cmds.listRelatives(s=True):
        maya_object_type = cmds.objectType(cmds.listRelatives(s=True)[0])
    file_dir = ":/{0}.svg".format(maya_object_type)

    testfile = QtCore.QFile(file_dir)
    if not testfile.exists():
        file_dir = ":/default.svg"
    return QtGui.QIcon(file_dir)

def label(text="test", color="color: rgb(255, 102, 255);"):
    label = QtWidgets.QLabel(text)
    label.setStyleSheet(color)
    return label

def button(text="test", color="color: rgb(255, 102, 255);"):
    button = QtWidgets.QPushButton(text)
    button.setStyleSheet(color)
    return button

def test_func():
    print "Test func is working"

def label_button(label_text="Test label",
                 button_text="Test button",
                 color="color: rgb(255, 102, 255);",
                 button_func=test_func,

                 ):
    label = QtWidgets.QLabel(label_text)
    label.setStyleSheet(color)
    button = QtWidgets.QPushButton(button_text)
    button.setStyleSheet(color)
    button.clicked.connect(button_func)
    return label, button

