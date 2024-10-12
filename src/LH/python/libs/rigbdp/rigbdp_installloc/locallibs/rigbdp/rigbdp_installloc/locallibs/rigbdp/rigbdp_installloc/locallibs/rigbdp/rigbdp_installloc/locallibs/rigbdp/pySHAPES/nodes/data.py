# ----------------------------------------------------------------------
# Description:
#
# Module for working with the data node.
# ----------------------------------------------------------------------

from maya.api import OpenMaya as om2
from maya import cmds

from pySHAPES.utils import attrTypes, nodes, plugs


def getShapeRangeAttrType(name, index):
    """Return the attribute type for the shape range.

    :param name: The name of the node.
    :type name: str
    :param index: The index of the element.
    :type index: int

    :return: The type of the MPlug attribute.
    :rtype: str or None
    """
    obj = nodes.asMObject(name)
    plug = plugs.findPlug(obj, "shape")
    rangePlug = plug.elementByLogicalIndex(index).child(1)
    return attrTypes.attributeType(rangePlug)


# ----------------------------------------------------------------------
# Copyright 2021 brave rabbit, Ingo Clemens. All rights reserved.
#
# Use of this software is subject to the terms of the brave rabbit
# SHAPES license agreement provided at the time of installation, or
# which otherwise accompanies this software in electronic form.
# ----------------------------------------------------------------------
