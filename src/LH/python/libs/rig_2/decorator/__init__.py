from maya import cmds
from functools import wraps

def undo_chunk(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(state=True, openChunk=True)
        result = func(*args, **kwargs)
        cmds.undoInfo(state=True, closeChunk=True)
        return result
    return wrapper

def undo_ignore(func):
    # Ifnores undo just for the decorated method
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(stateWithoutFlush = False)
        result = func(*args, **kwargs)
        cmds.undoInfo(stateWithoutFlush = True)
        return result
    return wrapper

def suppress_warnings(func):
    # Ifnores undo just for the decorated method
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.scriptEditorInfo(suppressWarnings=True)
        result = func(*args, **kwargs)
        cmds.scriptEditorInfo(suppressWarnings=False)
        return result
    return wrapper
