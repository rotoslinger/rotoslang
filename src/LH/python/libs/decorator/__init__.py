# builtins
from functools import wraps

# third party
import maya.cmds as cmds
from maya import mel


# for use within maya
def sel_restore(func):
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

def undo_chunk(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(state=True, openChunk=True)
        result = func(*args, **kwargs)
        cmds.undoInfo(state=True, closeChunk=True)
        return result
    return wrapper

def undo_ignore(func):
    # Ignores undo just for the decorated method
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(stateWithoutFlush = False)
        result = func(*args, **kwargs)
        cmds.undoInfo(stateWithoutFlush = True)
        return result
    return wrapper

def suppress_warnings(func):
    # Ignores undo just for the decorated method
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.scriptEditorInfo(suppressWarnings=True)
        result = func(*args, **kwargs)
        cmds.scriptEditorInfo(suppressWarnings=False)
        return result
    return wrapper

def print_bookends(func):
    """
    Decorator to print bookend lines before and after the output of the function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('\n###################################################################')
        func(*args, **kwargs)
        print('###################################################################\n')
    return wrapper

# creating a new poseInterpolator always selects it, so you will want to restore sel afterward
@sel_restore
def suppress_pose_editor(func):
    """
    A decorator to save the current selection, run a function, and restore the selection afterward.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # will create the poseInterpolator without warning
        # -1 - the dialog should pop up;
        #  0 - the dialog should not pop up, and not create neutral pose when driver are controlled
        #  1 - the dialog should not pop up, and create neutral pose when driver are controlled

        # find out what the global value is
        # set the nuetral to not be created, and suppress the dialogue (we will set later)
        mel.eval('$gCreateNeutralPoseWhenControlled=0;')

        try:
            # Run the decorated function
            return func(*args, **kwargs)
        finally:
            # this is the maya default, so I am going to 
            mel.eval(f'$gCreateNeutralPoseWhenControlled={-1};')
    return wrapper


