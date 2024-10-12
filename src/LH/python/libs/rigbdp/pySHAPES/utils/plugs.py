# ----------------------------------------------------------------------
# Description:
#
# Helper module for working with instances of om2.MObject as well as
# processing transform and shape nodes.
# ----------------------------------------------------------------------

from maya.api import OpenMaya as om2
from maya import cmds


def findPlug(obj, attr):
    """Return the given MObjects MPlug which belongs to the given
    attribute name. If the attribute is an alias the related MPlug is
    returned.

    This function is an improvement to the MFnDependencyNode.findPlug()
    because it can handle alias names and MFnDependencyNode.findAlias()
    doesn't return the index of an array attribute.

    :param obj: The MObject of the node the attribute belongs to.
    :type obj: om2.MObject
    :param attr: The name of the attribute to get the MPlug from.
    :type attr: str

    :return: The MPlug of the attribute.
    :rtype: om2.MPlug or None
    """
    mfn = om2.MFnDependencyNode(obj)
    # First check if the attribute is an alias.
    alias = mfn.findAlias(attr)
    if alias != om2.MObject.kNullObj:
        return plugFromAlias(obj, attr)
    else:
        try:
            return mfn.findPlug(attr, False)
        except:
            pass

# ----------------------------------------------------------------------
# Copyright 2021 brave rabbit, Ingo Clemens. All rights reserved.
#
# Use of this software is subject to the terms of the brave rabbit
# SHAPES license agreement provided at the time of installation, or
# which otherwise accompanies this software in electronic form.
# ----------------------------------------------------------------------
