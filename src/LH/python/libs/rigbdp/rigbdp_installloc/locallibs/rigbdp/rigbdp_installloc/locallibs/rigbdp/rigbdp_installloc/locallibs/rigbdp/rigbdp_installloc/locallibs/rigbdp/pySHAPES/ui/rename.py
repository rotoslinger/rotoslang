# ----------------------------------------------------------------------
# Description:
#
# Module for the ui elements related to target list renaming.
# ----------------------------------------------------------------------

from maya.api import OpenMaya as om2
from maya import cmds, mel

from functools import partial

from pySHAPES.commands.targetList import rename
from pySHAPES.ui import common

REPLACE_WINDOW = "shapesUI_searchReplaceWindow"
SEARCH_FIELD = "shapesUI_searchField"
REPLACE_FIELD = "shapesUI_replaceField"
REPLACE_SIZE = (250, 80)

PREFIX_WINDOW = "shapesUI_prefixSuffixWindow"
PREFIX_FIELD = "shapesUI_prefixField"
SUFFIX_FIELD = "shapesUI_suffixField"
PREFIX_SIZE = (250, 80)


# ----------------------------------------------------------------------
# Search and replace
# ----------------------------------------------------------------------
def searchReplaceUI():
    """Build the window for the search and replace.
    """
    common.createWindow(REPLACE_WINDOW,
                        "Search and Replace",
                        REPLACE_SIZE[0],
                        REPLACE_SIZE[1])

    form = cmds.formLayout()
    searchLabel = cmds.text(label="Search")
    replaceLabel = cmds.text(label="Replace")
    cmds.textField(SEARCH_FIELD,
                   placeholderText="Use + for combinations")
    cmds.textField(REPLACE_FIELD)
    applyButton = cmds.button(label="Apply",
                              command=partial(applySearchReplace))
    closeButton = cmds.button(label="Close",
                              command=partial(common.closeWindow, REPLACE_WINDOW))
    cmds.formLayout(form,
                    edit=True,
                    attachForm=[(searchLabel, "left", 7),
                                (searchLabel, "top", 5),
                                (replaceLabel, "top", 5),
                                (SEARCH_FIELD, "left", 5),
                                (REPLACE_FIELD, "right", 5),
                                (applyButton, "left", 5),
                                (applyButton, "bottom", 5),
                                (closeButton, "right", 5),
                                (closeButton, "bottom", 5)],
                    attachControl=[(SEARCH_FIELD, "top", 3, searchLabel),
                                   (REPLACE_FIELD, "top", 3, replaceLabel)],
                    attachPosition=[(replaceLabel, "left", 3, 70),
                                    (SEARCH_FIELD, "right", 2, 70),
                                    (REPLACE_FIELD, "left", 2, 70),
                                    (applyButton, "right", 2, 50),
                                    (closeButton, "left", 2, 50)])

    cmds.showWindow(REPLACE_WINDOW)


def applySearchReplace(*args):
    """Collect the search and replace strings and perform the renaming.
    """
    search = cmds.textField(SEARCH_FIELD,
                            query=True,
                            text=True).split("+")
    replace = cmds.textField(REPLACE_FIELD,
                             query=True,
                             text=True)
    rename.searchReplace(search, replace)


# ----------------------------------------------------------------------
# Prefix/suffix
# ----------------------------------------------------------------------
def prefixSuffixUI():
    """Build the window for adding a prefix and/or suffix.
    """
    common.createWindow(PREFIX_WINDOW,
                        "Add Prefix/Suffix",
                        PREFIX_SIZE[0],
                        PREFIX_SIZE[1])

    form = cmds.formLayout()
    prefixLabel = cmds.text(label="Prefix")
    suffixLabel = cmds.text(label="Suffix")
    cmds.textField(PREFIX_FIELD)
    cmds.textField(SUFFIX_FIELD)
    applyButton = cmds.button(label="Apply",
                              command=partial(applyPrefixSuffix))
    closeButton = cmds.button(label="Close",
                              command=partial(common.closeWindow, PREFIX_WINDOW))
    cmds.formLayout(form,
                    edit=True,
                    attachForm=[(prefixLabel, "left", 7),
                                (prefixLabel, "top", 5),
                                (suffixLabel, "top", 5),
                                (PREFIX_FIELD, "left", 5),
                                (SUFFIX_FIELD, "right", 5),
                                (applyButton, "left", 5),
                                (applyButton, "bottom", 5),
                                (closeButton, "right", 5),
                                (closeButton, "bottom", 5)],
                    attachControl=[(PREFIX_FIELD, "top", 3, prefixLabel),
                                   (SUFFIX_FIELD, "top", 3, suffixLabel)],
                    attachPosition=[(suffixLabel, "left", 3, 50),
                                    (PREFIX_FIELD, "right", 2, 50),
                                    (SUFFIX_FIELD, "left", 2, 50),
                                    (applyButton, "right", 2, 50),
                                    (closeButton, "left", 2, 50)])

    cmds.showWindow(PREFIX_WINDOW)


def applyPrefixSuffix(*args):
    """Collect the prefix and suffix strings and perform the renaming.
    """
    prefix = cmds.textField(PREFIX_FIELD,
                            query=True,
                            text=True)
    suffix = cmds.textField(SUFFIX_FIELD,
                            query=True,
                            text=True)
    rename.addPrefixSuffix(prefix, suffix)


# ----------------------------------------------------------------------
# Copyright 2021 brave rabbit, Ingo Clemens. All rights reserved.
#
# Use of this software is subject to the terms of the brave rabbit
# SHAPES license agreement provided at the time of installation, or
# which otherwise accompanies this software in electronic form.
# ----------------------------------------------------------------------
