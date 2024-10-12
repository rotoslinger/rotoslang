from maya import cmds, OpenMaya, OpenMayaAnim
from rig.utils import misc
import importlib
importlib.reload(misc)

class meshData(object):
    # ===============================================================================
    # CLASS:         return_mesh_info
    # DESCRIPTION:   returns information that can be used to rebuild a mesh
    # USAGE:         set args and run
    # RETURN:
    # REQUIRES:      maya.cmds, maya.OpenMaya
    # AUTHOR:        Levi Harrison
    # DATE:          Oct 14th, 2014
    # Version        1.0.0
    # ===============================================================================
    # =============================================================================

    ###################################################
    # ---Example
    # mesh_dict = return_mesh_info(name = "C_mouthWeightPatch_EX").mesh
    # create_mesh(mesh_dict)
    ###################################################

    def __init__(self,
                 name = "",
                 ):

        """
        type  name:                        string
        param name:                        name of the geo you want to get data from
        """

        #---args
        self.name                           = name
        #---vars
        self.transform_name = self.name
        self.shape_name = misc.getShape(self.name)
        
        self.mesh                           = {}
        self.fn_mesh                        = ""
        self.numVertices                    = 0
        self.numPolygons                    = 0
        self.vertexArray                    = []
        self.polygonCounts                  = []
        self.polygonConnects                = []
        self.uArray                         = []
        self.vArray                         = []
        self.uv_count                       = []
        self.uv_id                          = []
        self.parent                         = ""
        self.__create()

    def check(self):
        tmp = cmds.listRelatives(self.name, parent = True)
        if tmp:
            self.parent = tmp[0]
        mesh_node = OpenMaya.MSelectionList()
        mesh_node.add(self.name)
        self.mesh_path = OpenMaya.MDagPath()
        mesh_node.getDagPath(0,self.mesh_path)
        try:
            self.fn_mesh = OpenMaya.MFnMesh(self.mesh_path)
        except:
            raise Exception(self.name + " is not a recognizable mesh")
            quit()

    def getNumVerts(self):
        self.numVertices = self.fn_mesh.numVertices()

    def get_num_polygons(self):
        self.numPolygons = self.fn_mesh.numPolygons()

    def get_vert_array(self):
        points = OpenMaya.MPointArray()
        self.fn_mesh.getPoints(points, OpenMaya.MSpace.kWorld)
        for i in range(points.length()):
            self.vertexArray.append((points[i].x,
                                     points[i].y,
                                     points[i].z))

    def get_counts_connects(self):
        mesh_iter = OpenMaya.MItMeshPolygon(self.mesh_path)
        while mesh_iter.isDone() == False :
            temp_vert_ids = OpenMaya.MIntArray()
            self.polygonCounts.append(mesh_iter.polygonVertexCount())
            mesh_iter.getVertices(temp_vert_ids)
            for i in range(temp_vert_ids.length()):
                self.polygonConnects.append(temp_vert_ids[i])
            next(mesh_iter)

    def get_UVs(self):
        tmp_U_float_array = OpenMaya.MFloatArray()
        tmp_V_float_array = OpenMaya.MFloatArray()
        self.fn_mesh.getUVs(tmp_U_float_array,tmp_V_float_array)
        self.uArray = [i for i in tmp_U_float_array]
        self.vArray = [i for i in tmp_V_float_array]
        uv_counts = OpenMaya.MIntArray()
        uv_ids = OpenMaya.MIntArray()
        self.fn_mesh.getAssignedUVs(uv_counts,uv_ids)
        self.uv_count = [i for i in uv_counts]
        self.uv_id = [i for i in uv_ids]

    def write_dict(self):
        self.mesh = {"name"            : self.name,
                     "transform_name" : self.transform_name,
                     "shape_name" : self.shape_name,
                     "numVertices"     : self.numVertices ,
                     "numPolygons"     : self.numPolygons ,
                     "vertexArray"     : self.vertexArray ,
                     "polygonCounts"   : self.polygonCounts ,
                     "polygonConnects" : self.polygonConnects,
                     "uArray"          : self.uArray,
                     "vArray"          : self.vArray,
                     "uvCount"         : self.uv_count,
                     "uvId"            : self.uv_id,
                     "parent"          : self.parent,
                     "type"            : "mesh"
                     }

    def __create(self):
        self.check()
        self.getNumVerts()
        self.get_num_polygons()
        self.get_vert_array()
        self.get_counts_connects()
        self.get_UVs()
        self.write_dict()

def safe_create_mesh(mesh_dict, name=None, parent=None):
    if not name:
        name= mesh_dict.get("transform_name")
    if not cmds.objExists(name):
        return create_mesh(mesh_dict=mesh_dict, name=name, parent=parent)
    return name

def create_mesh(mesh_dict, name=None, parent=None):
    if not name:
        name= mesh_dict.get("transform_name")
    newTransform = cmds.createNode("transform", name=name, parent=parent )
    transformNode = OpenMaya.MSelectionList()
    transformNode.add(newTransform)
    transformPath = OpenMaya.MDagPath()
    transformNode.getDagPath(0,transformPath)
    transformMObject = transformPath.transform()

    #put everything back into m arrays
    #verts
    vertexArray = OpenMaya.MPointArray()
    [vertexArray.append(OpenMaya.MPoint(i[0],i[1],i[2])) for i in mesh_dict.get("vertexArray")]
    #counts
    counts = OpenMaya.MIntArray()
    [counts.append(i) for i in mesh_dict.get("polygonCounts")]
    #connects
    connects = OpenMaya.MIntArray()
    [connects.append(i) for i in mesh_dict.get("polygonConnects")]
    #uarray
    uArray = OpenMaya.MFloatArray()
    [uArray.append(i) for i in mesh_dict.get("uArray")]
    #uarray
    vArray = OpenMaya.MFloatArray()
    [vArray.append(i) for i in mesh_dict.get("vArray")]

    #uv_counts
    uv_counts = OpenMaya.MIntArray()
    [uv_counts.append(i) for i in mesh_dict.get("polygonCounts")]
    #uv_id
    uv_id = OpenMaya.MIntArray()
    [uv_id.append(i) for i in mesh_dict.get("polygonConnects")]

    new_mesh = OpenMaya.MFnMesh()
    new_mesh.create(mesh_dict.get("numVertices"),
                    mesh_dict.get("numPolygons"),
                                         vertexArray,
                                         counts,
                                         connects,
                                         uArray,
                                         vArray,
                                         transformMObject)
    cmds.rename(new_mesh.fullPathName(), mesh_dict.get("shape_name"))
    new_mesh.assignUVs(uv_counts,uv_id)
    if not cmds.objExists("lambert1"):
        lambert = cmds.shadingNode('lambert', asShader=True, name="lambert1")
    shading_engine = get_shading_engine("lambert1")
    cmds.sets(newTransform, e=True, forceElement=shading_engine)
    return newTransform

def get_shading_engine(shader):
    engine = cmds.listConnections(shader, d=True, et=True, t='shadingEngine')
    if not engine: 
        return
    return engine[0]

