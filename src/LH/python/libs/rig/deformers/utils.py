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
    os = mac

if os not in sys.path:
    sys.path.append(os)

from maya import cmds
import maya.OpenMaya as OpenMaya
from rig.utils import misc
reload(misc)
from rig.utils import exportUtils
reload(exportUtils)

def calimari(skinCluster, mesh, bias, hide=True):
    vertCount = cmds.polyEvaluate(mesh, v=1) - 1
    jnts = cmds.skinCluster(skinCluster, q=True, inf=True)
    tmpMeshTransform = cmds.duplicate(mesh, name="TEMPORARY")[0]
    tmpMesh = cmds.listRelatives(tmpMeshTransform, shapes=True)
    tmpSkinCluster = cmds.skinCluster(jnts, tmpMeshTransform, mi=1)[0]
    cmds.copySkinWeights(ss=skinCluster, ds=tmpSkinCluster, noMirror=True, ia="oneToOne")
    # skincluster always locks transforms, unlock them
    misc.lock_attrs(tmpMeshTransform, unhide=True)
    
    for idx, jnt in enumerate(jnts):
        attr = '{0}.weightList[0:{1}].weights[{2}]'.format(tmpSkinCluster, vertCount, idx)
        newMeshName = "{0}Calimari_GEO".format(jnt)
        newMesh, newMeshTransform = facesFromWeightmap(attr, newMeshName, tmpMeshTransform, bias)
        cmds.parentConstraint(jnt, newMeshTransform, mo=True)

    cmds.delete(tmpMesh, tmpMeshTransform, tmpSkinCluster)
    if hide:
        cmds.setAttr(mesh + ".v", 0)

def facesFromWeightmap(weightAttribute="cluster1.weightList[0].weights", newGeoName=None, geo=None, bias=.2):
    weightlist = cmds.getAttr(weightAttribute)
    filterArray=[]
    fnMesh = misc.getOMMesh(geo)
    meshDag = misc.getDag(geo)
    allPoints = OpenMaya.MPointArray()
    fnMesh.getPoints(allPoints)
    vertices_to_delete = {}
    vertices_to_delete["points"] = OpenMaya.MPointArray()
    vertices_to_delete['indices'] = OpenMaya.MIntArray()
    for idx in range(len(weightlist)):
        if weightlist[idx] > bias:
            filterArray.append(idx)

    mesh_iter = OpenMaya.MItMeshPolygon(meshDag)
    poly_to_delete = []
    while mesh_iter.isDone() == False :
        proceed = 1
        temp_vert_ids = OpenMaya.MIntArray()
        mesh_iter.getVertices(temp_vert_ids)
        # If the vert isn't in our filter, skip the face
        for i in range(temp_vert_ids.length()):
            if temp_vert_ids[i] not in filterArray:
                proceed = 0
        if proceed:
            poly_to_delete.append(mesh_iter.index())
        mesh_iter.next()

    allPolys = OpenMaya.MIntArray()
    poly_to_delete = [x for x in range(mesh_iter.count()) if x not in poly_to_delete]
    faces = []
    newMeshTransform = cmds.duplicate(geo, name=newGeoName)[0]
    newMesh = cmds.listRelatives(newMeshTransform, shapes=True)
    for i in range(len(poly_to_delete)):
        faces.append("{0}.f[{1}]".format(newMeshTransform, poly_to_delete[i]))
    if faces:
        cmds.delete(faces)
    return newMesh, newMeshTransform