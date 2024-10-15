# builtins
import importlib
# bdp
from rigbdp.ui import lockui_core
# reloads
importlib.reload(lockui_core)


def lockui():
    lockui_core.lockui()
