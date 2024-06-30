from maya import cmds, OpenMaya
import sys
import importlib
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"

#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)
from rig.rigComponents import lidTest
importlib.reload(lidTest)
from rig.rigComponents import browTest
importlib.reload(browTest)
from rig.rigComponents import lipTest
importlib.reload(lipTest)
from rig.rigComponents import mouthJawTest
importlib.reload(mouthJawTest)

def build():
    cmds.file( new=True, f=True )
    cmds.unloadPlugin("LHDeformerNodes")
    cmds.loadPlugin("C:/Users/harri/Desktop/dev/rotoslang/src/LH/cpp/plugins/mayaplugin/build/src/Debug/LHDeformerNodes")


    asset="C:/Users/harri/Desktop/dev/rotoslang/src/scenes/assets/oldMan/oldMan.ma"
    cmds.file( asset, i=True, f=True )
    lidTest.test(auto_load=False, old_man=True)
    browTest.test(auto_load=False, old_man=True)

