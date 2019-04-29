import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
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

'''
-Optimization pass on all deformers
    -Avoid multiple MIndex, if multiple geo will be deformed, create different deformers
    -If B
    -Cache out an MIntArray of all the verts that are going to be posed
    -Ba
Need super simple version of the slide


'''