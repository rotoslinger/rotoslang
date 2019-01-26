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
Notes on anim curve weights

- Need seperate animCurveWeights node.
    - has in weights that it can use to multiply against the curve, will skip 0 weights
    - cache closest point on weight patch for area mapping - this never has to be live
    - must have U and V weight per for area weighting (U = width, V = length) L x W = area
    - super optimize weight curve evaluations and mapping of weight curves to patch to avoid costly algorithm
    - see if it is possible to only update current plug index, cache out all other values until plug is upated
- Need weight curve distribution one with bias, and one that linearly splits everything
    - bias can be used to provide different areas of influence, while the linear split just does everything
- Maybe we don't do a bias, that would be hard to control....
- Try a linear split first that normalizes the weighting


- After getting good weight output you can write a script that gets the final output and autoPlaces controls


- Will need to write a curve weight node that outputs a single weight map, and maybe one that does multiple for joints


'''