# ----------------------------------------------------------------------
# Description:
#
# Helper module for working with instances of om2.MObject as well as
# processing transform and shape nodes.
# ----------------------------------------------------------------------

from maya.api import OpenMaya as om2
from maya import cmds


def asMObject(name):
    """Return the node as an MObject.

    :param name: The name of the node.
    :type name: str

    :return: The MObject of the node.
    :rtype: om2.MObject
    """
    sel = om2.MSelectionList()
    try:
        sel.add(name)
    except RuntimeError:
        msg = "The node with the name {} does not exist.".format(name)
        raise RuntimeError(msg)
    return sel.getDependNode(0)

# ----------------------------------------------------------------------
# Copyright 2021 brave rabbit, Ingo Clemens. All rights reserved.
#
# Use of this software is subject to the terms of the brave rabbit
# SHAPES license agreement provided at the time of installation, or
# which otherwise accompanies this software in electronic form.
# ----------------------------------------------------------------------
