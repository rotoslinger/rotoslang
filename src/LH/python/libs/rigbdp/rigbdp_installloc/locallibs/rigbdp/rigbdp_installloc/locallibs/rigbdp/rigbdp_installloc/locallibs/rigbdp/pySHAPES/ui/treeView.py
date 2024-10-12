# ----------------------------------------------------------------------
# Description:
#
# Module containing the class for a treeView control.
# ----------------------------------------------------------------------

from maya import cmds


class TreeView(object):
    """Class for managing a treeView control.
    """
    def __init__(self, name):
        super(TreeView, self).__init__()
        self.tree = name

    def clearSelection(self):
        """Deselect all items of the control.
        """
        cmds.treeView(self.tree,
                      edit=True,
                      clearSelection=True)

    def exists(self):
        """Return True, if the control exists.
        """
        return cmds.treeView(self.tree, exists=True)

    def hasSelection(self):
        """Return True, if one or more items are selected.
        """
        return False if not len(self.selection()) else True

    def select(self, items):
        """Select the given items in the list.
        """
        for item in items:
            cmds.treeView(self.tree,
                          edit=True,
                          selectItem=(item, True))

    def selection(self):
        """Return the list of selected items. Returns an empty list if
        there is nothing selected.

        :return: The list of selected items.
        :rtype: list(str)
        """
        items = cmds.treeView(self.tree,
                              query=True,
                              selectItem=True)
        if items is None:
            items = []
        return items


# ----------------------------------------------------------------------
# Copyright 2021 brave rabbit, Ingo Clemens. All rights reserved.
#
# Use of this software is subject to the terms of the brave rabbit
# SHAPES license agreement provided at the time of installation, or
# which otherwise accompanies this software in electronic form.
# ----------------------------------------------------------------------
