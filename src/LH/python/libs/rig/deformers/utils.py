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
from rig.utils import exportUtils
reload(exportUtils)


def facesFromWeightmap(weightAttribute="cluster1.weightList[0].weights", geo=None, attrType="multi"):
    weightlist = cmds.getAttr(weightAttribute)[0]
    filterArray=[]
    for idx in range(len(weightlist)):
        if weightlist[idx] > 0.0:
            filterArray.append(idx)

    meshDict = exportUtils.meshDataFiltered(name = geo, filterArray = filterArray).mesh
    print meshDict
    # print filterArray
    # fnMesh = misc.getOMMesh(geo)


    # vertexArray = []
    # points = OpenMaya.MPointArray()
    # fnMesh.getPoints(points, OpenMaya.MSpace.kWorld)
    # for i in range(len(filterArray)):
    #     vertexArray.append((points[i].x, points[i].y, points[i].z))
    
    # polyCounts = []
    # polygonConnects = []
    # polyIdxList = []
    # mesh_iter = OpenMaya.MItMeshPolygon(fnMesh)
    # while mesh_iter.isDone() == False :
    #     temp_vert_ids = OpenMaya.MIntArray()
    #     mesh_iter.getVertices(temp_vert_ids)
    #     # If the vert isn't in our filter, skip the face
    #     for i in range(temp_vert_ids.length())
    #         if temp_vert_ids[i] not in filterArray:
    #             mesh_iter.next()
    #     polyCounts.append(mesh_iter.polygonVertexCount())
    #     polyIdxList.append(mesh_iter.idx())
    #     for i in range(temp_vert_ids.length()):
    #         polygonConnects.append(temp_vert_ids[i])
    #     mesh_iter.next()

        

    #     tmp_U_float_array = OpenMaya.MFloatArray()
    #     tmp_V_float_array = OpenMaya.MFloatArray()
    #     self.fnMesh.getUVs(tmp_U_float_array,tmp_V_float_array)
    #     self.uArray = [i for i in tmp_U_float_array]
    #     self.vArray = [i for i in tmp_V_float_array]
    #     uv_counts = OpenMaya.MIntArray()
    #     uv_ids = OpenMaya.MIntArray()
    #     self.fnMesh.getAssignedUVs(uv_counts,uv_ids)
    #     self.uv_count = [i for i in uv_counts]
    #     self.uv_id = [i for i in uv_ids]



    

