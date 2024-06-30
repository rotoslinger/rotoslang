# WINDOWS BUILD TERMINAL COMMANDS:
# YOU HAVE TO SET TO BUILD ON Win64 OR YOU WILL GET ERRORS
# 1 Windows inside build dir run:       cmake ..
# 2 THEN WINDOWS:                       cmake -G "Visual Studio 15 2017 Win64" -DMAYA_VERSION=2018 .. 
# 3 THEN Windows inside build dir run:  cmake --build . --config Debug





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
TODO before release

CURRENT TASKS
- Write guides
    -Add guide to rivet, should always be created regardless of being visible
    -Add guide to matrix deformer

    -All guide controls should have a locked attribute called "GUIDE"
    
- Write method that gets all guide positions prints into dictionary
- Write method that gets all anim curve weight nodes, puts into a dictionary
- write method that gets all weight stacks and finds all hand weights and puts them into a dictionary

FIRST PASS
- Apply the current rig to a face
- Finish prototypes for the face
    - eye control, use joints for aim, but deformer for pupil/iris scale
        - eye pupil iris patch scale (possible new deformer)
        - eye squash and stretch needs lattice component and utils
    - eye mass squash and stretch
    - jaw squash and stretch
    - slide rotation deformer component and utils (figure out UV length width normalization)
    - nose
    - ear
- Make modeling fixes as you go
- Standardize a file system for the face
- Document the steps needed for setting up the face
- Make sure the rig works with a skeleton
- Make sure rig can be scaled and rotated
- CLEANUP CLASSES AND DOCUMENT THEM

SECOND PASS
- Fix annoying issues from step one
- Convert all code to rig_2 and the components there
- Make set up and auto placement of controls easier by using curves to place controls, similar to the lips
- Have all base geometry be auto created to reduce arguments and setup time
- Create a procedural geo base for setup, includes all geometry and fitting controls as well as the ability to save out this geometry to a separate file
- Figure out a container system with utilities
- CLEANUP CLASSES AND DOCUMENT THEM

THIRD PASS
- Guide System
- Ability to turn on guides visibility with a switch
- Also turn off control visibility
- Ability to place geometry needed for sliding the face live, (scripts for isolation and visualization of different components)
- CLEANUP CLASSES AND DOCUMENT THEM

FOURTH PASS
- Ability to pickle each class into a string and save the state as text in the rig
- Ability to save entire rig out to a file that can be built again
- Ability to extract code needed to add to a builder class
- CLEANUP CLASSES AND DOCUMENT THEM

FIFTH PASS
- UIs
- UIs for weighting: copying anim curves copying weight stacks, and between weight stacks
- UIs for adding weight groups and controls
- UIs for Guides and mirroring guides and mirroring poses (same core)
- UIs for creating the rig
- UI for saving rig to file, import and export
- UI that will create a builder script so the rig can be built or debugged, or simply a file that just rebuilds the whole thing
- CLEANUP CLASSES AND DOCUMENT THEM

OPTIMIZATION
- try to put rivet into a single node that loops through all rivets on the whole mesh to optimize.
- simplify the geometry the rivets are attaching to, create individual patches then wrap them to the final geo

'''