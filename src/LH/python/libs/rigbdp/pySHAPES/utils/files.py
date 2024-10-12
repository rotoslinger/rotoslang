# ----------------------------------------------------------------------
# Description:
#
# Module for file related tasks.
# ----------------------------------------------------------------------

import os
import subprocess

from pySHAPES import var
from pySHAPES.utils import general

import logging

logger = logging.getLogger(__name__)


def openFolderWithFile(filePath):
    """Open the given file or folder in the file system.

    :param filePath: The path to the file to show.
    :type filePath: str
    """
    filePath = os.path.realpath(filePath)

    if os.path.exists(filePath):
        currentOS = general.currentSystem()
        # Define the arguments for the subprocess based on the system.
        if currentOS == var.LINUX:
            args = ["xdg-open", os.path.dirname(filePath)]
        if currentOS == var.MACOS:
            args = ["open", "-R", filePath]
        else:  # currentOS == var.WINDOWS
            args = (r'explorer /select,"{}"'.format(filePath))

        try:
            subprocess.call(args)
            return
        except OSError:
            logger.warning("The file {} does yet exist".format(filePath))
    else:
        logger.warning("The file {} does yet exist".format(filePath))


# ----------------------------------------------------------------------
# Copyright 2021 brave rabbit, Ingo Clemens. All rights reserved.
#
# Use of this software is subject to the terms of the brave rabbit
# SHAPES license agreement provided at the time of installation, or
# which otherwise accompanies this software in electronic form.
# ----------------------------------------------------------------------
