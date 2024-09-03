import maya.api.OpenMaya as om
from maya import cmds
import maya.mel as mel

def weight_info():
    # get points
    # get MfnMesh

    sel = om.MGlobal.getActiveSelectionList()
    # first object in selection (index 0); if several objects are selected, you can pass another index, or loop over selection
    dagPath, component = sel.getComponent(0)
    mesh = om.MFnMesh(dagPath)
    for i in dir(mesh):
        print(type(component))
        print(i)


    # iterate over selected vertices ONLY, by passing component as second argument
    itGeometry = om.MItGeometry(dagPath, component)
    index = 0
    while not itGeometry.isDone():
        print(f"Object: {dagPath} <==> Vertex ID: {itGeometry.index()}")

        # if index == 0:
        #     point = (dagPath)
        #     print(itGeometry)


        index += index
        itGeometry.next()
weight_info()