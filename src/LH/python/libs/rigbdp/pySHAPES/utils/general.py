#!/usr/bin/env python

"""System utility functions.
"""

import platform

from pySHAPES import var


def currentSystem():
    """Return the identifier string for the current platform.

    :return: The system string.
    :rtype: str
    """
    currentOS = platform.system()
    if currentOS == "Darwin":
        currentOS = var.MACOS
    return currentOS
