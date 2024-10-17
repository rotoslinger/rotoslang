# ----------------------------------------------------------------------
# Description:
#
# Module for renaming the items in the target list.
# ----------------------------------------------------------------------

from maya.api import OpenMaya as om2
from maya import cmds, mel

from pySHAPES import var
from pySHAPES.ui import treeView


def searchReplace(search="", replace=""):
    """Search and replace a given string or comma separated list of
    items with the given replace string. If a list selection exists the
    renaming is performed only on the selected items.

    :param search: The search string or list of strings to search for.
    :type search: str or list(str)
    :param replace: The replace string.
    :type replace: str
    """
    items, hasSelection = getListItems(var.TARGET_TREE)

    # Clear the selection.
    targetTree = treeView.TreeView(var.TARGET_TREE)
    targetTree.clearSelection()

    # Check if the search is a string or list.
    if type(search) == str:
        searchList = [search]
    else:
        searchList = search

    renamed = []
    for name in items:
        newName = name
        # Check for each element in the given search list.
        for searchItem in searchList:
            # If the partial search string is found replace it.
            if searchItem in newName:
                newName = newName.replace(searchItem, replace)

        if newName != name:
            mel.eval('shapesAction_performRename("Corrective", "{}", "{}")'.format(name, newName))
            renamed.append(newName)
            updateOrderName(name, newName)

    # Refresh the target list.
    mel.eval("shapesList_listBlendShapeTargets(1)")

    # Reselect the chosen items in the list.
    if not hasSelection:
        renamed = []

    finalizeRename(var.TARGET_TREE, renamed)


def addPrefixSuffix(prefix="", suffix=""):
    """Add the given prefix and/or suffix to the selected list
    elements. If nothing is selected all items will receive a new name.

    :param prefix: The prefix string to add.
    :type prefix: str
    :param suffix: The suffix string to add.
    :type suffix: str
    """
    items, hasSelection = getListItems(var.TARGET_TREE)

    # Clear the selection.
    targetTree = treeView.TreeView(var.TARGET_TREE)
    targetTree.clearSelection()

    renamed = []
    for name in items:
        newName = "".join((prefix, name, suffix))

        if newName != name:
            mel.eval('shapesAction_performRename("Corrective", "{}", "{}")'.format(name, newName))
            renamed.append(newName)
            updateOrderName(name, newName)

    # Refresh the target list.
    mel.eval("shapesList_listBlendShapeTargets(1)")

    # Reselect the chosen items in the list.
    if not hasSelection:
        renamed = []

    finalizeRename(var.TARGET_TREE, renamed)


# ----------------------------------------------------------------------
# Common
# ----------------------------------------------------------------------

def getListItems(listName):
    """Return the selected items in the given treeView. If nothing is
    selected return all items from the list.

    :param listName: The name of the treeView control.
    :type listName: str

    :return: A tuple with the list of selected/all items and if the
             treeView has an active selection.
    :rtype: tuple(str, bool)
    """
    targetTree = treeView.TreeView(var.TARGET_TREE)

    # Get the selected channels from the target list.
    if targetTree.exists():
        items = targetTree.selection()

    # If nothing is selected get all shapes and attributes
    # from the setup.
    hasSelection = targetTree.hasSelection()
    if not hasSelection:
        items = mel.eval('shapesData_getAllAttrItems()')

    return items, hasSelection


def finalizeRename(listName, items):
    """After renaming select the renamed items if the renaming has been
    performed on a selection.
    Also update the target slider to affect the selected items.

    :param listName: The name of the treeView control.
    :type listName: str
    :param items: The list of items to re-select.
    :type items: list(str)
    """
    targetTree = treeView.TreeView(listName)

    if len(items):
        targetTree.select(items)
    else:
        # Clear the selection.
        targetTree.clearSelection()

    mel.eval("shapesMain_buildTargetSlider()")


def updateOrderName(oldName, newName):
    """Replace the previous name of a shape or helper attribute in the
    ordering attributes of the data node with the given new name.

    :param oldName: The old name of the list item.
    :type oldName: str
    :param newName: The new name of the list item.
    :type newName: str
    """
    dataNode = mel.eval("shapesData_getDataNode($gShapes_bsNode)")

    for listName in ["order", "parent", "expand"]:
        items = cmds.getAttr("{}.{}".format(dataNode, listName)).split(",")

        for i in range(len(items)):
            if items[i] == oldName:
                items[i] = newName

        cmds.setAttr("{}.{}".format(dataNode, listName),
                     ",".join(items),
                     type="string")


# ----------------------------------------------------------------------
# Copyright 2021 brave rabbit, Ingo Clemens. All rights reserved.
#
# Use of this software is subject to the terms of the brave rabbit
# SHAPES license agreement provided at the time of installation, or
# which otherwise accompanies this software in electronic form.
# ----------------------------------------------------------------------
