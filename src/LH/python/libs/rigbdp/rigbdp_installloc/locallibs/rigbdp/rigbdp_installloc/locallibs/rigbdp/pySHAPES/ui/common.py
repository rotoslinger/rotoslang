# ----------------------------------------------------------------------
# Description:
#
# Module for common ui control elements and tasks.
# ----------------------------------------------------------------------

from maya import cmds


def createWindow(name, title, width, height, fixed=True):
    """Create a new window with the given name. If the window already
    exists, close it.

    :param name: The name of the window.
    :type name: str
    :param title: The title of the window.
    :type title: str
    :param width: The width of the window.
    :type width: str
    :param height: The height of the window.
    :type height: str
    :param fixed: True, if the pre-defined size should be kept.
    :type fixed: bool
    """
    if cmds.window(name, exists=True):
        cmds.deleteUI(name)

    if fixed and cmds.windowPref(name, exists=True):
        cmds.windowPref(name,
                        edit=True,
                        width=width,
                        height=height)
    cmds.window(name,
                title=title,
                width=width,
                height=height)


def closeWindow(name, *args):
    """Close the window with the given name.

    :param name: The name of the window.
    :type name: str
    """
    cmds.deleteUI(name)


# ----------------------------------------------------------------------
# Copyright 2021 brave rabbit, Ingo Clemens. All rights reserved.
#
# Use of this software is subject to the terms of the brave rabbit
# SHAPES license agreement provided at the time of installation, or
# which otherwise accompanies this software in electronic form.
# ----------------------------------------------------------------------
