import maya.cmds as cmds
from functools import wraps

def restore_selection(func):
    """
    A decorator to save the current selection, run a function, and restore the selection afterward.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the current selection
        original_selection = cmds.ls(selection=True)

        try:
            # Run the decorated function
            return func(*args, **kwargs)
        finally:
            # Restore the original selection
            if original_selection:
                cmds.select(original_selection)
            else:
                cmds.select(clear=True)  # Clear selection if original was empty
    return wrapper