import sys, os

from maya import cmds
from rig_2.mirror import utils as mirror_utils
reload(mirror_utils)
from rig_2.tag import utils as tag_utils
reload(tag_utils)

from rig.utils import misc
reload(misc)
from rig_2.guide import utils as guide_utils
reload(guide_utils)

from rig_2.manipulator import nurbscurve
'''
@code
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
win = "C:\\Users\\harri\\Desktop\\dev\\rotoslang\\src\\LH\\python\\libs"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win32" in os:
    os = win

if os not in sys.path:
    sys.path.append(os)

from ui_2 import guide
reload(guide)
guide_ui = guide.Guide_UI()
guide_ui.openUI()

@endcode
'''
