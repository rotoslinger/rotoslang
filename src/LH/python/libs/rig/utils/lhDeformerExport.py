import sys
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

# import maya.cmds as cmds
from maya import cmds, OpenMaya, mel, OpenMayaAnim
import json
import os
from utils import slideDeformerCmds, vectorDeformerCmds, curveRollDeformerCmds
reload(slideDeformerCmds)
reload(vectorDeformerCmds)
reload(curveRollDeformerCmds)


#===============================================================================
#CLASS:         return_mesh_info
#DESCRIPTION:   returns information that can be used to rebuild a mesh
#USAGE:         set args and run
#RETURN:
#REQUIRES:      maya.cmds, maya.OpenMaya
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class return_mesh_info():
    def __init__(self,
                 name = "",
                 ):

        """
        @type  name:                        string
        @param name:                        name of the deformer you want to
                                            export

        @type  import_path:                 bool
        @param import_path:                 path to import from
        """

        #---args
        self.name                           = name
        #---vars
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

    def __check(self):
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

    def __get_num_verts(self):
        self.numVertices = self.fn_mesh.numVertices()

    def __get_num_polygons(self):
        self.numPolygons = self.fn_mesh.numPolygons()

    def __get_vert_array(self):
        points = OpenMaya.MPointArray()
        self.fn_mesh.getPoints(points, OpenMaya.MSpace.kWorld)
        for i in range(points.length()):
            self.vertexArray.append((points[i].x,
                                     points[i].y,
                                     points[i].z))

    def __get_counts_connects(self):
        mesh_iter = OpenMaya.MItMeshPolygon(self.mesh_path)
        while mesh_iter.isDone() == False :
            temp_vert_ids = OpenMaya.MIntArray()
            self.polygonCounts.append(mesh_iter.polygonVertexCount())
            mesh_iter.getVertices(temp_vert_ids)
            for i in range(temp_vert_ids.length()):
                self.polygonConnects.append(temp_vert_ids[i])
            mesh_iter.next()

    def __get_UVs(self):
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

    def __write_dict(self):
        self.mesh = {"name"            : self.name,
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
                     }

    def __create(self):
        self.__check()
        self.__get_num_verts()
        self.__get_num_polygons()
        self.__get_vert_array()
        self.__get_counts_connects()
        self.__get_UVs()
        self.__write_dict()



#=============================================================================
def create_mesh(mesh_dict):
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
                                         vArray)

    new_mesh.assignUVs(uv_counts,uv_id)
    if mesh_dict.get("parent"):
        child = cmds.listRelatives(new_mesh.fullPathName(), parent = True)[0]
        parent = mesh_dict.get("parent")
        if cmds.objExists(parent):
            cmds.parent(child, parent)

    return new_mesh

###################################################
#---Example
# mesh_dict = return_mesh_info(name = "C_mouthWeightPatch_EX").mesh
# create_mesh(mesh_dict)
###################################################



#===============================================================================
#CLASS:         return_nurbs_surface_info
#DESCRIPTION:   returns information that can be used to rebuild a nurbsSurface
#USAGE:         set args and run
#RETURN:        nurbs
#REQUIRES:      maya.cmds, maya.OpenMaya
#AUTHOR:        Levi Harrison
#DATE:          Nov 10th, 2014
#Version        1.0.0
#===============================================================================

class return_nurbs_surface_info():
    def __init__(self,
                 name = "",
                 ):

        """
        @type  name:                        string
        @param name:                        name of the deformer you want to
                                            export
        """

        #---args
        self.name                           = name
        #---vars
        self.nurbs                          = {}
        self.fn_nurbs                       = ""
        self.controlVertices                = [] #---MPointArray
        self.uKnotSequences                 = [] #---MDoubleArray
        self.vKnotSequences                 = [] #---MDoubleArray
        self.degreeInU                      = 0 #---unsigned Int
        self.degreeInV                      = 0 #---unsigned Int
        self.form                          = None #---MFnNurbsSurface::Form
        self.formV                          = None #---MFnNurbsSurface::Form
        self.parent                         = ""#---MObject
        self.__get_nurbs()

    def __check(self):
        tmp = cmds.listRelatives(self.name, parent = True)
        if tmp:
            self.parent = tmp[0]
        nurbs_node = OpenMaya.MSelectionList()
        nurbs_node.add(self.name)
        self.nurbs_path = OpenMaya.MDagPath()
        nurbs_node.getDagPath(0,self.nurbs_path)
        try:
            self.fn_nurbs = OpenMaya.MFnNurbsSurface(self.nurbs_path)
        except:
            raise Exception(self.name + " is not a recognizable nurbsSurface")
            quit()

    def __get_cvs(self):
        points = OpenMaya.MPointArray()
        self.fn_nurbs.getCVs(points, OpenMaya.MSpace.kWorld)
        for i in range(points.length()):
            self.controlVertices.append((points[i].x,
                                         points[i].y,
                                         points[i].z))

    def __get_knot_sequences(self):
        u_knots = OpenMaya.MDoubleArray()
        v_knots = OpenMaya.MDoubleArray()
        self.fn_nurbs.getKnotsInU(u_knots)
        self.fn_nurbs.getKnotsInV(v_knots)
        self.uKnotSequences = [i for i in u_knots]
        self.vKnotSequences = [i for i in v_knots]

    def __get_degrees(self):
        self.degreeInU = self.fn_nurbs.degreeU()
        self.degreeInV = self.fn_nurbs.degreeV()

    def __get_forms(self):
        self.form = self.fn_nurbs.formInU()
        self.formV = self.fn_nurbs.formInV()

    def __write_dict(self):
        self.nurbs = {"name"              : self.name,
                     "controlVertices"    : self.controlVertices ,
                     "uKnotSequences"     : self.uKnotSequences ,
                     "vKnotSequences"     : self.vKnotSequences ,
                     "degreeInU"          : self.degreeInU ,
                     "degreeInV"          : self.degreeInV,
                     "form"               : self.form,
                     "formV"              : self.formV,
                     "parent"             : self.parent
                     }

    def __get_nurbs(self):
        self.__check()
        self.__get_cvs()
        self.__get_knot_sequences()
        self.__get_degrees()
        self.__get_forms()
        self.__write_dict()
#==============================================================================
def create_nurbs_surface(nurbs_dict):
    #put everything back into m arrays
    #verts
    controlVertices = OpenMaya.MPointArray()
    [controlVertices.append(OpenMaya.MPoint(i[0],i[1],i[2]))for i in nurbs_dict.get("controlVertices")]
    #counts
    uKnots = OpenMaya.MDoubleArray()
    [uKnots.append(i) for i in nurbs_dict.get("uKnotSequences")]
    #connects
    vKnots = OpenMaya.MDoubleArray()
    [vKnots.append(i) for i in nurbs_dict.get("vKnotSequences")]
    new_nurbs = OpenMaya.MFnNurbsSurface()
    new_nurbs.create(controlVertices,
                     uKnots,
                     vKnots,
                     nurbs_dict.get("degreeInU"),
                     nurbs_dict.get("degreeInV"),
                     nurbs_dict.get("form"),
                     nurbs_dict.get("formV"),
                     
                     False)
    if nurbs_dict.get("parent"):
        child = cmds.listRelatives(new_nurbs.fullPathName(), parent = True)[0]
        parent = nurbs_dict.get("parent")
        if cmds.objExists(parent):
            cmds.parent(child, parent)
    return new_nurbs
#########################################################
#---Example
# nurbs_dict = return_nurbs_surface_info(name = "C_lipsSlidePatch_EX").nurbs
# create_nurbs_surface(nurbs_dict)
#########################################################




#===============================================================================
#CLASS:         return_nurbs_curve_info
#DESCRIPTION:   returns information that can be used to rebuild a nurbsSurface
#USAGE:         set args and run
#RETURN:        nurbs
#REQUIRES:      maya.cmds, maya.OpenMaya
#AUTHOR:        Levi Harrison
#DATE:          Dec 1st, 2014
#Version        1.0.0
#===============================================================================

class return_nurbs_curve_info():
    def __init__(self,
                 name = "",
                 ):

        """
        @type  name:                        string
        @param name:                        name of the curve you want to
                                            export
        """

        #---args
        self.name                           = name
        #---vars
        self.nurbsCurve                     = {}
        self.fn_nurbsCurve                  = ""
        self.controlVertices                = [] #---MPointArray
        self.knots                          = [] #---MDoubleArray
        self.degree                         = 0 #---unsigned Int
        self.form                           = None #---MFnNurbsSurface::Form
        self.parent                         = ""#---MObject
        self.__get_nurbsCurve()

    def __check(self):
        tmp = cmds.listRelatives(self.name, parent = True)
        if tmp:
            self.parent = tmp[0]
#         print self.parent
        nurbsCurve_node = OpenMaya.MSelectionList()
        nurbsCurve_node.add(self.name)
        self.nurbsCurve_path = OpenMaya.MDagPath()
        nurbsCurve_node.getDagPath(0,self.nurbsCurve_path)
#         self.fn_nurbsCurve = OpenMaya.MFnNurbsCurve(self.nurbsCurve_path)
        try:
            self.fn_nurbsCurve = OpenMaya.MFnNurbsCurve(self.nurbsCurve_path)
        except:
            raise Exception(self.name + " is not a recognizable nurbsCurve")
            quit()

    def __get_cvs(self):
        points = OpenMaya.MPointArray()
        self.fn_nurbsCurve.getCVs(points, OpenMaya.MSpace.kWorld)
        for i in range(points.length()):
            self.controlVertices.append((points[i].x,
                                         points[i].y,
                                         points[i].z))

    def __get_knot_sequences(self):
        knots = OpenMaya.MDoubleArray()
        self.fn_nurbsCurve.getKnots(knots)
        self.knots = [i for i in knots]

    def __get_degrees(self):
        self.degree = self.fn_nurbsCurve.degree()

    def __get_forms(self):
        self.form = self.fn_nurbsCurve.form()

    def __write_dict(self):
        self.nurbsCurve = {"name"              : self.name,
                           "controlVertices"   : self.controlVertices ,
                           "knots"             : self.knots ,
                           "degree"            : self.degree ,
                           "form"              : self.form,
                           "parent"            : self.parent
                           }

    def __get_nurbsCurve(self):
        self.__check()
        self.__get_cvs()
        self.__get_knot_sequences()
        self.__get_degrees()
        self.__get_forms()
        self.__write_dict()
#==============================================================================
def create_curve(curve_dict):
    #put everything back into m arrays
    #verts
    controlVertices = OpenMaya.MPointArray()
    [controlVertices.append(OpenMaya.MPoint(i[0],i[1],i[2]))for i in curve_dict.get("controlVertices")]
    #counts
    uKnots = OpenMaya.MDoubleArray()
    [uKnots.append(i) for i in curve_dict.get("knots")]
    #connects
    new_nurbsCurve = OpenMaya.MFnNurbsCurve()
    new_nurbsCurve.create(controlVertices,
                          uKnots,
                          curve_dict.get("degree"),
                          curve_dict.get("form"),
                          False,
                          False,
                          )
    if curve_dict.get("parent"):
        child = cmds.listRelatives(new_nurbsCurve.fullPathName(), parent = True)[0]
        parent = curve_dict.get("parent")
        if cmds.objExists(parent):
            cmds.parent(child, parent)
    
    return new_nurbsCurve

#########################################################
#---Example
# curve_dict = return_nurbs_curve_info(name = "curve1").nurbsCurve
# create_curve(curve_dict)
#########################################################







#===============================================================================
#CLASS:         get_anim_curve_info
#DESCRIPTION:   puts anim curve info info from a list of anim curves into a dict
#USAGE:         give list of anim curves
#RETURN:        anim_curves
#REQUIRES:      maya.cmds, maya.OpenMayaAnim
#AUTHOR:        Levi Harrison
#DATE:          Nov. 11th, 2014
#Version        1.0.0
#===============================================================================

class get_anim_curve_info():
    def __init__(self,
                 anim_curve = [],
                 ):
        """
        @type  anim_curve:            list
        @param anim_curve:            anim curves     

        """
        #----args
        self.anim_curve                   = anim_curve
        #----vars
        self.num_keys                     = 0
        # all
        self.api_anim_curve               = ""

        self.frame_values             = []
        self.frame_times              = []
        self.in_x_tangents            = []
        self.in_y_tangents            = []
        self.out_x_tangents           = []
        self.out_y_tangents           = []
        self.in_tangents_type         = []
        self.out_tangents_type        = []
        self.curve_dict                   = {}

        self.__create()

    def __get_anim_curve_info(self):
        for i in range(len(self.anim_curve)):
            #tmps
            tmp_frame_values             = []
            tmp_frame_times              = []
            tmp_in_x_tangents            = []
            tmp_in_y_tangents            = []
            tmp_out_x_tangents           = []
            tmp_out_y_tangents           = []
            tmp_in_tangents_type         = []
            tmp_out_tangents_type        = []
            type = cmds.nodeType(self.anim_curve[i])
            if "animCurve" in type:
                #--- get all keys and times of tmp_frame_values 
                # and num tmp_frame_values and frame range
                anim_curve_node = OpenMaya.MSelectionList()
                anim_curve_node.add(self.anim_curve[i])
                c_plug = OpenMaya.MPlug()
                anim_curve_node.getPlug(0,c_plug)
                oAnimCurve = OpenMaya.MObject()
                oAnimCurve = c_plug.node()
                self.api_anim_curve = OpenMayaAnim.MFnAnimCurve(oAnimCurve)
                self.num_keys = self.api_anim_curve.numKeys()
                #---get all info for anim curve
                fn_x = OpenMaya.MScriptUtil()
                fn_x.createFromDouble(0.0)
                x = fn_x.asFloatPtr()
                fn_y = OpenMaya.MScriptUtil()
                fn_y.createFromDouble(0.0)
                y = fn_y.asFloatPtr()
                if self.num_keys > 0:
                    for i in range(self.num_keys):
                        tmp_times = self.api_anim_curve.time(i)
                        tmp_frame_times.append(tmp_times.value())
                        tmp_frame_values.append(self.api_anim_curve.value(i))
                        #get tangent types
                        tmp_in_tangents_type.append(self.api_anim_curve.inTangentType(i))
                        tmp_out_tangents_type.append(self.api_anim_curve.outTangentType(i))
                        # get in tangents
                        self.api_anim_curve.getTangent(i,x,y,True)
                        tmp_in_x_tangents.append(OpenMaya.MScriptUtil.getFloat(x))
                        tmp_in_y_tangents.append(OpenMaya.MScriptUtil.getFloat(y))
                        # get out tangents
                        self.api_anim_curve.getTangent(i,x,y,False)
                        tmp_out_x_tangents.append(OpenMaya.MScriptUtil.getFloat(x))
                        tmp_out_y_tangents.append(OpenMaya.MScriptUtil.getFloat(y))
                else:
                    raise Exception( self.api_anim_curve + " doesn't have any" +
                                      "keys please add keys and try again")
                    quit()
        
                self.frame_values.append(tmp_frame_values)
                self.frame_times.append(tmp_frame_times)
                self.in_x_tangents.append(tmp_in_x_tangents)
                self.in_y_tangents.append(tmp_in_y_tangents)
                self.out_x_tangents.append(tmp_out_x_tangents)
                self.out_y_tangents.append(tmp_out_y_tangents)
                self.in_tangents_type.append(tmp_in_tangents_type)
                self.out_tangents_type.append(tmp_out_tangents_type)
            else:
                raise Exception( self.api_anim_curve + " is not an anim_curve")
                quit()

    def __create_dict(self):
        """put everything together"""
        for i in range(len(self.anim_curve)):
            self.curve_dict[i] = {"name":             self.anim_curve[i],
                                  "frame_values":     self.frame_values[i],
                                  "frame_times":      self.frame_times[i],
                                  "in_x_tangents":    self.in_x_tangents[i],
                                  "in_y_tangents":    self.in_y_tangents[i],
                                  "out_x_tangents":   self.out_x_tangents[i],
                                  "out_y_tangents":   self.out_y_tangents[i],
                                  "in_tangents_type": self.in_tangents_type[i],
                                  "out_tangents_type":self.out_tangents_type[i]}

    def __create(self):
        """put everything together"""
        self.__get_anim_curve_info()
        self.__create_dict()
#===============================================================================
def set_anim_curves(anim_curves,
                      frame_values,
                      frame_times,
                      in_x_tangents,
                      in_y_tangents,
                      out_x_tangents,
                      out_y_tangents,
                      in_tangents_type,
                      out_tangents_type):
    # get mfnAnimCurve
    try:
        anim_curve_node = OpenMaya.MSelectionList()
        anim_curve_node.add(anim_curves)
        c_plug = OpenMaya.MPlug()
        anim_curve_node.getPlug(0,c_plug)
    #     oAnimCurve = OpenMaya.MObject()
        oAnimCurve = c_plug.node()
        api_anim_curve = OpenMayaAnim.MFnAnimCurve(oAnimCurve)
        num_keys = api_anim_curve.numKeys()
        # delete any existing keys
        if num_keys>0:
            for i in range(num_keys):
                api_anim_curve.remove(i)
        # set keys based on args
        for i in range(len(frame_times)):
            time = OpenMaya.MTime(frame_times[i])
            index = api_anim_curve.addKey(time,
                                          frame_values[i],
                                          in_tangents_type[i],
                                          out_tangents_type[i])
            
            
            
            
    #                 print index
            # set in tangent 
    #                 print i
            api_anim_curve.setTangent(index,
                                      in_x_tangents[i],
                                      in_y_tangents[i],
                                      True,
                                      None,
                                      False)
            # set out tangent 0
            api_anim_curve.setTangent(index,
                                      out_x_tangents[i],
                                      out_y_tangents[i],
                                      False,
                                      None,
                                      False)
            api_anim_curve.setInTangentType(index,
                                      in_tangents_type[i])
            # set out tangent 0
            api_anim_curve.setOutTangentType(index,
                                      out_tangents_type[i])
    except:
        pass





##############################################
#Example:
# dict = get_anim_curve_info(anim_curve = ["C_TLipLR_ACV"]).curve_dict
# print dict
###############################################
#===============================================================================
#CLASS:         get_slide_deformer
#DESCRIPTION:   gets all information about the slide deformer
#USAGE:         set args and run
#RETURN:
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Nov 10th, 2014
#Version        1.0.0
#===============================================================================

class export_slide_deformer():
    def __init__(self,
                 name = "",
                 path = "",
                 ):

        """
        @type  name:                        string
        @param name:                        name of the deformer you want to
                                            export

        @type  export_path:                 string
        @param export_path:                 path to export to

        """

        #---args
        self.name                           = name
        self.path                           = path
        #---vars
        self.geo_membership                 = []
        self.driver_surface                 = {}
        self.weight_geo                     = {}
        self.base_geo                       = []
        self.transferGeo                   = []
        self.anim_curves                    = {}
        self.deformer_weights               = {}
        self.weights                        = {}
        self.vector_dict                     = {}
        # naming information for rebuilding
        self.driverSurface           = ""
        self.geoms                   = []
        self.weightGeo               = ""
        self.weightBase              = []
        self.transferGeo             = []
        self.control                 = ""
        self.lockAttrs               = []
        self.ihi                     = None
        self.side                    = ""
        self.short_name              = ""
        self.uNames                  = []
        self.vNames                  = []
        self.nNames                  = []
        self.uUseAnimCurves          = []
        self.vUseAnimCurves          = []
        self.nUseAnimCurves          = []
        

        self.__create()

    def __check(self):
        if not cmds.objExists(self.name):
            raise Exception(self.name + " does not exist")
            quit()
    def __get_info(self):
            # get all info from the deformer
            # get all attribute names
            # from attr names you will know curve and weight names
        self.driverSurface = cmds.listConnections(self.name + ".surface",
                                                  d = False)[0]
#         self.geoms = cmds.deformer(self.name, q = True,g = True)
        self.weightGeo = cmds.listConnections(self.name + ".weightPatch",
                                              d = False)[0]

        self.weightBase = cmds.listConnections(self.name + ".baseGeoArray",
                                              d = False)
        #---Will be a copy of the geometries where weights will be stored
        self.transferGeo = cmds.deformer(self.name, q = True, g = True)

        self.side = self.name.split("_")[0]
        self.short_name = self.name.split("_")[1]
        self.uNames = cmds.listConnections(self.name + ".uValueParentArray",
                                           d = True,
                                           p = True)
        if self.uNames:
            for i in range(len(self.uNames)):
                self.uNames[i] = self.uNames[i].split(".")[1]

        self.vNames  = cmds.listConnections(self.name + ".vValueParentArray",
                                                d = True,
                                                p = True)

        if self.vNames:
            for i in range(len(self.vNames)):
                self.vNames[i] = self.vNames[i].split(".")[1]
        self.nNames   = cmds.listConnections(self.name + ".nValueParentArray",
                                             d = True,
                                             p = True)
        if self.nNames:
            for i in range(len(self.nNames)):
                self.nNames[i] = self.nNames[i].split(".")[1]

        self.uUseAnimCurves          = [1]
        self.vUseAnimCurves          = [1]
        self.nUseAnimCurves          = [1]

    def __get_memberships(self):
            # get all deformed geometry and their memberships
            #get set
            self.set   = cmds.listConnections(self.name + ".message",
                                              d = True,
                                              p = True)[0].split(".")[0]
#             attr = cmds.getAttr(self.name + ".message")
            self.geo_membership = cmds.sets(self.set, q = True)
            self.geo_membership = cmds.deformer(self.name, q = True, g = True)

    def __get_geoms(self):
            # get all driver geometry (for rebuilding)
        self.driver_surface = return_nurbs_surface_info(name = self.driverSurface).nurbs
        self.weight_geo = return_mesh_info(name = self.weightGeo).mesh
        if not self.weightBase:
            self.weightBase = cmds.listConnections(self.name + ".baseGeoArray", d = False)
        for i in range(len(self.weightBase)):
            shape = cmds.listRelatives(self.weightBase[i], shapes = True)[0]
            if (cmds.objectType(shape, isType='nurbsSurface')):
                self.base_geo.append(return_nurbs_surface_info(name = self.weightBase[i]).nurbs)
            if (cmds.objectType(shape, isType='mesh')):
                self.base_geo.append(return_mesh_info(name = self.weightBase[i]).mesh)
                
        
        #---Exporting the transfer geo means finding a non deformed copy of the mesh and storing it.
        #---The base geo is the only geo that is garanteed to not be deformed.
        self.transferGeo = []
        tmpTransferGeo = []
        for geo in cmds.listConnections(self.name + ".baseGeoArray", d = False):
            tmpTransferGeo.append(cmds.duplicate(geo, n= geo.replace("Base","Transfer"))[0])
        for i in range(len(tmpTransferGeo)):
            shape = cmds.listRelatives(tmpTransferGeo[i], shapes = True)[0]
            if (cmds.objectType(shape, isType='nurbsSurface')):
                transferGeo = return_nurbs_surface_info(name = tmpTransferGeo[i]).nurbs
                self.transferGeo.append(transferGeo)
                
            if (cmds.objectType(shape, isType='mesh')):
                transferGeo = return_mesh_info(name = tmpTransferGeo[i]).mesh
                self.transferGeo.append(transferGeo)
        cmds.delete(tmpTransferGeo)

    def __get_curves(self):
            # get all curve infos
        self.connections = []
        self.connections.append(cmds.listConnections(self.name + ".uuaca",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".uvaca",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".uva",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".uwpa",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".vuaca",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".vvaca",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".vva",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".vwpa",
                                                     type = "animCurve",
                                                     d = False))
        flat_conn = []
        for i in range(len(self.connections)):
            if self.connections[i]:
                for j in range(len(self.connections[i])):
                    if self.connections[i][j]:
                        flat_conn.append(self.connections[i][j])
        all = flat_conn
        self.anim_curves = get_anim_curve_info(anim_curve = all).curve_dict
    def __get_weights(self):
            # get all double array weights
            tmp_weight_names = cmds.listAttr(self.name, 
                                             ud = True, 
                                             a = True)
            tmp_values = []
            tmp_names = []
            geoms = cmds.deformer(self.name, q = True,g = True)
            for i in range(len(tmp_weight_names)):
                for j in range(len(geoms)):
                    split_weights = tmp_weight_names[i].split(".")
                    tmp_names.append(self.name
                                     + "."
                                     + split_weights[0]
                                     +"[" + str(j)
                                     + "]."
                                     + split_weights[1])
                    tmp_values.append(cmds.getAttr(self.name
                                                   + "."
                                                   + split_weights[0]
                                                   +"[" + str(j)
                                                   + "]."
                                                   + split_weights[1]))
            self.weights = dict(zip(tmp_names,tmp_values))
            # get deformer weights
            tmp_def_weights = []
            tmp_def_names   = []
            tmp_flat_weights= []
            tmp_flat_names= []
            try:
                for i in range(len(geoms)):
                    tmp_def_names = self.name + ".weightList[" + str(i) + "].weights"
                    indices = cmds.getAttr(tmp_def_names, mi = True)
    #                     tmp_def_weights = cmds.getAttr(tmp_def_names)
    #                     print tmp_def_weights
                    for j in range(len(indices)):
                        tmp_flat_names.append(self.name
                                              + ".weightList["
                                              + str(i)
                                              + "].weights["
                                              + str(indices[j])
                                              + "]")
                        tmp_flat_weights.append(cmds.getAttr(tmp_flat_names[j]))
    #                     print tmp_flat_weights[j]
    #                         print cmds.getAttr(tmp_flat_names[j])
    #                         print tmp_flat_weights[j], j, tmp_flat_names[j],tmp_def_weights[0][j]
                for i in range(len(tmp_flat_names)):
                    self.deformer_weights[tmp_flat_names[i]] = tmp_flat_weights[i]
            except:
                pass
#             print self.deformer_weights
    def __organize(self):
#         print self.base_geo

        self.vector_dict = {
                           "driver_surface":       self.driver_surface,
                           "weight_geo":           self.weight_geo,
                           "anim_curves":          self.anim_curves,
                           "weights":              self.weights,
                           "driverSurface":        self.driverSurface,
                           "geoms":                self.geoms,
                           "base_geo":             self.base_geo,
                           "transferGeo":         self.transferGeo,
                           "geo_membership":       self.geo_membership,
                           "deformer_weights":     self.deformer_weights,
                           "weightGeo":            self.weightGeo,
                           "control":              self.control,
                           "lockAttrs":            self.lockAttrs,
                           "ihi":                  self.ihi,
                           "side":                 self.side,
                           "short_name":           self.short_name,
                           "uNames":               self.uNames,
                           "vNames":               self.vNames,
                           "nNames":               self.nNames,
                           "uUseAnimCurves":       self.uUseAnimCurves,
                           "vUseAnimCurves":       self.vUseAnimCurves,
                           "nUseAnimCurves":       self.nUseAnimCurves,
                           }
    def __export(self):
        file = open(self.path, "wb")
        json.dump(self.vector_dict, file, sort_keys = False, indent = 2)
        file.close()
        
            # format info
            # export info to a file
    def __create(self):
        self.__check()
        self.__get_info()
        self.__get_memberships()
        self.__get_geoms()
        self.__get_curves()
        self.__get_weights()
        self.__organize()
        self.__export()

##############################################################################
#---Example:
# export_slide_deformer(name = "C_mouth_SLD",
#                       path = "/corp/home/lharrison/Desktop/testExport.sld")
# print something["driver_surface"]["name"]

##############################################################################



#===============================================================================
#CLASS:         import_slide_deformer
#DESCRIPTION:   rebuilds the slide deformer
#USAGE:         set args and run
#RETURN:        
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Nov 11th, 2014
#Version        1.0.0
#===============================================================================

class import_slide_deformer():
    def __init__(self,
                 path = "",
                 create_geo = True,
                 create_deformer = True,
                 set_weights = True,
                 set_curves = True,
                 transfer = False
                 ):

        """
        @type  path:                 string
        @param path:                 path to import from
        """

        #---args
        self.path                    = path
        self.create_geo              = create_geo
        self.create_deformer         = create_deformer
        self.set_weights             = set_weights
        self.set_curves              = set_curves
        self.transfer                = transfer
        #---vars
        self.dict                    = {}
        self.geo_membership          = []
        self.driver_surface          = {}
        self.weight_geo              = {}
        self.anim_curves             = {}
        self.weights                 = {}
        self.deformer_weights        = {}
        self.baseGeo                 = []
        self.transferGeo             = []
        self.driverSurface           = ""
        self.geoms                   = []
        self.control                 = ""
        self.lockAttrs               = []
        self.ihi                     = None
        self.side                    = ""
        self.short_name              = ""
        self.uNames                  = []
        self.vNames                  = []
        self.nNames                  = []
        self.uUseAnimCurves          = []
        self.vUseAnimCurves          = []
        self.nUseAnimCurves          = []

        self.__create()

    def __unpack(self):
        "imports the dictionary, separates all of the info for later use"
        file = open(self.path, "rb")
        self.dict = json.load(file)
        file.close()
        
        self.driver_surface   = self.dict["driver_surface"]
        self.weight_geo       = self.dict["weight_geo"]
        self.baseGeo          = self.dict["base_geo"]
        self.transferGeo      = self.dict["transferGeo"]
        self.anim_curves      = self.dict["anim_curves"]
        self.weights          = self.dict["weights"]
        self.driverSurface    = self.dict["driverSurface"]
        self.geo_membership   = self.dict["geo_membership"]
        self.deformer_weights = self.dict["deformer_weights"]
        self.geoms            = self.dict["geoms"]
        self.control          = self.dict["control"]
        self.lockAttrs        = self.dict["lockAttrs"]
        self.ihi              = self.dict["ihi"]
        self.side             = self.dict["side"]
        self.short_name       = self.dict["short_name"]
        self.uNames           = self.dict["uNames"]
        self.vNames           = self.dict["vNames"]
        self.nNames           = self.dict["nNames"]
        self.uUseAnimCurves   = self.dict["uUseAnimCurves"]
        self.vUseAnimCurves   = self.dict["vUseAnimCurves"]
        self.nUseAnimCurves   = self.dict["nUseAnimCurves"]
    def __create_geo(self):
        if self.create_geo == True:
            #---create driver surface, parent if any
            self.driverSurface = create_nurbs_surface(self.driver_surface).fullPathName()
            self.driverSurface = cmds.listRelatives(self.driverSurface, parent = True)
            self.driverSurface = cmds.rename(self.driverSurface, self.driver_surface["name"])
            #---create weight surface, parent if any
            if not cmds.objExists(self.weight_geo["name"]):
                self.weightGeo = create_mesh(self.weight_geo).fullPathName()
                self.weightGeo = cmds.listRelatives(self.weightGeo, parent = True)
                self.weightGeo = cmds.rename(self.weightGeo, self.weight_geo["name"])
            else:
                self.weightGeo = self.weight_geo["name"]
            #---create base geo, parent if any
            tmp_baseGeo = []
            tmp = []
#             for i in range(len(self.baseGeo)):
#                 if not cmds.objExists(self.baseGeo[i]["name"]):
#                     tmp = create_mesh(self.baseGeo[i]).fullPathName()
#                     tmp = cmds.listRelatives(tmp, parent = True)
#                     tmp = cmds.rename(tmp, self.baseGeo[i]["name"])
#                     cmds.setAttr(tmp+".v",0)
#                     tmp_baseGeo.append(tmp)
#                 else:
#                     tmp_baseGeo.append(self.baseGeo[i]["name"])
#             self.baseGeo = tmp_baseGeo
#             #---Test to see whether or not the geo_membership and the base geo have the same number of points
#             #---If geo_membership and base do not line up, copy the geo_membership, to create the base.
#             if (len(self.geo_membership) != len(self.baseGeo)):
#                 self.__createBase()
#                 return
#             for i in range(len(self.geo_membership)):
#                 if not comparePolyCount(self.geo_membership[i], self.baseGeo[i]):
#                     self.__createBase()
#                     return
            self.__createBase()

            #---create transfer geo, parent if any
            print self.baseGeo        
            tmp_transferGeo = []
            tmp = []
            for i in range(len(self.transferGeo)):
                if not cmds.objExists(self.transferGeo[i]["name"]):
                    print "creating Transfer Geo"
                    tmp = create_mesh(self.transferGeo[i]).fullPathName()
                    tmp = cmds.listRelatives(tmp, parent = True)
                    tmp = cmds.rename(tmp, self.transferGeo[i]["name"])
                    cmds.setAttr(tmp+".v",0)
                    tmp_transferGeo.append(tmp)
                else:
                    tmp_transferGeo.append(self.transferGeo[i]["name"])
            self.transferGeo = tmp_transferGeo

    def __createBase(self):
        """Creates base"""
        self.baseGeo = []
        for i in self.geo_membership:
            tmp = cmds.duplicate(i, name = i + "Base")[0]
            cmds.setAttr(tmp+".v",0)
            self.baseGeo.append(tmp)

    def __create_deformer(self):
        "creates deformer, turns envelope off"
        #---If doesn't find geo_membership, attempts to apply to selected geo
        if not self.geo_membership:
            self.geo_membership = cmds.ls(sl=True)
        if self.create_deformer == True:
            self.deformer = slideDeformerCmds.slideDeformerCmd(
                                                 driverSurface = self.driverSurface,
                                                 weightGeo = self.weightGeo,
                                                 geoms = self.geo_membership,
                                                 weightBase = self.baseGeo,
                                                 control = '',
                                                 ihi = 1,
                                                 side = self.side,
                                                 name = self.short_name,
                                                 #---Mouth
                                                 uNames = self.uNames,
                                                 vNames = self.vNames,
                                                 nNames = self.nNames,
                                                 ).returnDeformer
            cmds.setAttr(self.deformer + ".envelope", 0)
        self.transferDeformer = slideDeformerCmds.slideDeformerCmd(
                                             driverSurface = self.driverSurface,
                                             weightGeo = self.weightGeo,
                                             geoms = self.transferGeo,
                                             control = '',
                                             ihi = 1,
                                             side = self.side,
                                             name = self.short_name,
                                             #---Mouth
                                             uNames = self.uNames,
                                             vNames = self.vNames,
                                             nNames = self.nNames,
                                             animCurveSuffix = "SRC",
                                             deformerSuffix = "SLDSRC"
                                             ).returnDeformer
        cmds.setAttr(self.transferDeformer + ".envelope", 0)

    def __set_anim_curves(self):
        if self.set_curves == True:
            for i in range(len(self.anim_curves)):
                anim_curves = self.anim_curves[str(i)]["name"]
                frame_values = self.anim_curves[str(i)]["frame_values"]
                frame_times= self.anim_curves[str(i)]["frame_times"]
                in_x_tangents= self.anim_curves[str(i)]["in_x_tangents"]
                in_y_tangents= self.anim_curves[str(i)]["in_y_tangents"]
                out_x_tangents= self.anim_curves[str(i)]["out_x_tangents"]
                out_y_tangents= self.anim_curves[str(i)]["out_y_tangents"]
                in_tangents_type= self.anim_curves[str(i)]["in_tangents_type"]
                out_tangents_type= self.anim_curves[str(i)]["out_tangents_type"]
                set_anim_curves(anim_curves,
                                frame_values,
                                frame_times,
                                in_x_tangents,
                                in_y_tangents,
                                out_x_tangents,
                                out_y_tangents,
                                in_tangents_type,
                                out_tangents_type)

    def __set_weights(self):
        "sets deformer weight, then sets double array weights"
        if self.set_weights == True:
            #---Double Check that the geo in the scene is the same as the geo from the dictionary
            #---If not, don't set weights, maya could crash
#             for i in range(len(self.geo_membership)):
#                 if not comparePolyCount(self.geo_membership[i], self.transferGeo[i]):
#                     print "Points do not match, weights will be transfered, not set"
#                     return

            if self.deformer_weights:
                for i in self.deformer_weights.keys():
                    cmds.setAttr(i, self.deformer_weights.get(i))
            #ToFixOldDeformers
            for i in self.weights.keys():
                weights = self.weights.get(i)
#                 newName = i
#                 if "LRU" in i:
#                     newName = i.replace("LRU", "LR")
#                 if "LRV" in i:
#                     newName = i.replace("LRV", "LR")
#                 if "UDU" in i:
#                     newName = i.replace("UDU", "UD")
#                 if "UDV" in i:
#                     newName = i.replace("UDV", "UD")
#                 if "SideU" in i:
#                     newName = i.replace("SideU", "Side")
#                 if "SideV" in i:
#                     newName = i.replace("SideV", "Side")
#                 cmds.setAttr(newName, weights,typ='doubleArray')
                if not weights:
                    continue
                try:
                    cmds.setAttr(i, weights,typ='doubleArray')
                except:
                    print "Weights for " + i + " unable to be set.  It is likely topology has changed."
#         #---Set Transfer weights
        for i in self.weights.keys():
            weights = self.weights.get(i)
            if not weights:
                continue
            transferAttr = i.replace("_SLD", "_SLDSRC")
            try:
                cmds.setAttr(transferAttr, weights,typ='doubleArray')
            except:
                print "Weights for " + i + " unable to be set."
    
    def __transfer(self):
        if self.transfer:
            for i in range(len(self.transferGeo)):
                lhDeformerWeightTransfer(self.transferGeo[i], self.transferDeformer, self.geo_membership[i], self.deformer)

    def __finalize(self):
        if self.create_deformer:
            cmds.setAttr(self.deformer + ".envelope", 1)
            cmds.refresh(force = True)
            cmds.setAttr(self.deformer + ".cacheWeights", 1)
            cmds.setAttr(self.deformer + ".cacheParams", 1)
            cmds.setAttr(self.deformer + ".cacheWeightMesh", 1)
            cmds.setAttr(self.deformer + ".cacheWeightCurves", 1)
            cmds.setAttr(self.deformer + ".cacheBase", 1)

    def __create(self):
        self.__unpack()
        self.__create_geo()
        self.__create_deformer()
        self.__set_anim_curves()
        self.__set_weights()
        self.__transfer()
        self.__finalize()

##############################################################################
#---Example:

# export_slide_deformer(name = "C_mouth_SLD",
#                       path = "/corp/home/lharrison/Desktop/testExport.sld")

# import_slide_deformer(path = "/corp/home/lharrison/Desktop/testExport.sld", 
#                       create_geo = True,
#                       create_deformer = True,
#                       set_weights = True,
#                       set_curves = True)
# 
# import_slide_deformer(path = "/corp/home/lharrison/Desktop/lips.sld", 
#                       create_geo = False,
#                       create_deformer = False,
#                       set_weights = True,
#                       set_curves = True)
##############################################################################



#===============================================================================
#CLASS:         export_vector_deformer
#DESCRIPTION:   exports the vector deformer to an external file
#USAGE:         set args and run
#RETURN:
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Dec 1st, 2014
#Version        1.0.0
#===============================================================================

class export_vector_deformer():
    def __init__(self,
                 name = "",
                 path = "",
                 ):

        """
        @type  name:                        string
        @param name:                        name of the deformer you want to
                                            export

        @type  export_path:                 string
        @param export_path:                 path to export to

        """

        #---args
        self.name                           = name
        self.path                           = path
        #---vars
        self.geo_membership                 = []
        self.weight_geo                     = {}
        self.base_geo                       = []
        self.t_pivots                       = []
        self.r_pivots                       = []
        self.anim_curves                    = {}
        self.deformer_weights               = {}
        self.weights                        = {}
        self.vector_dict                    = {}
        # naming information for rebuilding
        self.weightBase              = 0
        self.geoms                   = []
        self.weightGeo               = ""
        self.weightBase              = []
        self.tPivots                 = []
        self.rPivots                 = []
        self.control                 = ""
        self.lockAttrs               = []
        self.ihi                     = None
        self.side                    = ""
        self.short_name              = ""
        self.tNames                  = []
        self.rNames                  = []
        

        self.__create()

    def __check(self):
        if not cmds.objExists(self.name):
            raise Exception(self.name + " does not exist")
            quit()
    def __get_info(self):
            # get all info from the deformer
            # get all attribute names
            # from attr names you will know curve and weight names
#         self.geoms = cmds.deformer(self.name, q = True,g = True)

        self.weightGeo = cmds.listConnections(self.name + ".weightPatch",
                                              d = False)[0]

        self.weightBase = cmds.listConnections(self.name + ".baseGeoArray",
                                              d = False)

        self.tPivots = cmds.listConnections(self.name + ".tPivotCurveArray",
                                              d = False)
        
        self.rPivots = cmds.listConnections(self.name + ".rPivotCurveArray",
                                              d = False)

        self.side = self.name.split("_")[0]
        self.short_name = self.name.split("_")[1]
        self.tNames = cmds.listConnections(self.name + ".tValueParentArray",
                                           d = True,
                                           p = True)
        for i in range(len(self.tNames)):
            self.tNames[i] = self.tNames[i].split(".")[1]
        self.rNames  = cmds.listConnections(self.name + ".rValueParentArray",
                                            d = True,
                                            p = True)
        for i in range(len(self.rNames)):
            self.rNames[i] = self.rNames[i].split(".")[1]

    def __get_memberships(self):
            # get all deformed geometry and their memberships
            #get set
            self.set   = cmds.listConnections(self.name + ".message",
                                              d = True,
                                              p = True)[0].split(".")[0]
#             attr = cmds.getAttr(self.name + ".message")
            self.geo_membership = cmds.sets(self.set, q = True)
            self.geo_membership = cmds.deformer(self.name, q = True, g = True)

    def __get_geoms(self):
            # get all driver geometry (for rebuilding)
        self.weight_geo = return_mesh_info(name = self.weightGeo).mesh
        for i in range(len(self.weightBase)):
            shape = cmds.listRelatives(self.weightBase[i], shapes = True)[0]
            if (cmds.objectType(shape, isType='nurbsSurface')):
                self.base_geo.append(return_nurbs_surface_info(name = self.weightBase[i]).nurbs)
            if (cmds.objectType(shape, isType='mesh')):
                self.base_geo.append(return_mesh_info(name = self.weightBase[i]).mesh)
 
        for i in range(len(self.tPivots)):
            shape = cmds.listRelatives(self.tPivots[i], shapes = True)[0]
            self.t_pivots.append(return_nurbs_curve_info(name = self.tPivots[i]).nurbsCurve)
  
        for i in range(len(self.rPivots)):
            shape = cmds.listRelatives(self.rPivots[i], shapes = True)[0]
            self.r_pivots.append(return_nurbs_curve_info(name = self.rPivots[i]).nurbsCurve)
#             need to write functionality for nurbs curves
    def __get_curves(self):
            # get all curve infos
        self.connections = []
        self.connections.append(cmds.listConnections(self.name + ".tAnimCurveUArray",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".tAnimCurveVArray",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".rAnimCurveUArray",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".rAnimCurveVArray",
                                                     type = "animCurve",
                                                     d = False))
        flat_conn = []
        for i in range(len(self.connections)):
            if self.connections[i]:
                for j in range(len(self.connections[i])):
                    if self.connections[i][j]:
                        flat_conn.append(self.connections[i][j])
        all = flat_conn
        self.anim_curves = get_anim_curve_info(anim_curve = all).curve_dict
    def __get_weights(self):
            # get all double array weights
            tmp_weight_names = cmds.listAttr(self.name, 
                                             ud = True, 
                                             a = True)
            tmp_values = []
            tmp_names = []
            geoms = cmds.deformer(self.name, q = True,g = True)
            for i in range(len(tmp_weight_names)):
                for j in range(len(geoms)):
                    split_weights = tmp_weight_names[i].split(".")
                    tmp_names.append(self.name
                                     + "."
                                     + split_weights[0]
                                     +"[" + str(j)
                                     + "]."
                                     + split_weights[1])
                    tmp_values.append(cmds.getAttr(self.name
                                                   + "."
                                                   + split_weights[0]
                                                   +"[" + str(j)
                                                   + "]."
                                                   + split_weights[1]))
            self.weights = dict(zip(tmp_names,tmp_values))
            # get deformer weights
            tmp_def_weights = []
            tmp_def_names   = []
            tmp_flat_weights= []
            tmp_flat_names= []
            try:
                for i in range(len(geoms)):
                    tmp_def_names = self.name + ".weightList[" + str(i) + "].weights"
                    indices = cmds.getAttr(tmp_def_names, mi = True)
                    for j in range(len(indices)):
                        tmp_flat_names.append(self.name
                                              + ".weightList["
                                              + str(i)
                                              + "].weights["
                                              + str(indices[j])
                                              + "]")
                        tmp_flat_weights.append(cmds.getAttr(tmp_flat_names[j]))
                for i in range(len(tmp_flat_names)):
                    self.deformer_weights[tmp_flat_names[i]] = tmp_flat_weights[i]
            except:
                pass
    def __organize(self):
        self.vector_dict = {
                           "weight_geo":           self.weight_geo,
                           "anim_curves":          self.anim_curves,
                           "weights":              self.weights,
                           "geoms":                self.geoms,
                           "base_geo":             self.base_geo,
                           "t_pivots":             self.t_pivots,
                           "r_pivots":             self.r_pivots,
                           "geo_membership":       self.geo_membership,
                           "deformer_weights":     self.deformer_weights,
                           "weightGeo":            self.weightGeo,
                           "control":              self.control,
                           "lockAttrs":            self.lockAttrs,
                           "ihi":                  self.ihi,
                           "side":                 self.side,
                           "short_name":           self.short_name,
                           "tNames":               self.tNames,
                           "rNames":               self.rNames,
                           }
#         print self.vector_dict
    def __export(self):
        file = open(self.path, "wb")
        json.dump(self.vector_dict, file, sort_keys = True, indent = 2)
        file.close()
        
            # format info
            # export info to a file
    def __create(self):
        self.__check()
        self.__get_info()
        self.__get_memberships()
        self.__get_geoms()
        self.__get_curves()
        self.__get_weights()
        self.__organize()
        self.__export()

###############################################################################
#---Example:
# export_vector_deformer(name = "C_testFace_VCD",
#                       path = "/corp/home/lharrison/Desktop/testExport.vec")
###############################################################################





#===============================================================================
#CLASS:         import_vector_deformer
#DESCRIPTION:   rebuilds the slide deformer
#USAGE:         set args and run
#RETURN:        
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Dec 1st, 2014
#Version        1.0.0
#===============================================================================

class import_vector_deformer():
    def __init__(self,
                 path = "",
                 create_geo = True,
                 create_deformer = True,
                 set_weights = True,
                 set_curves = True,
                 ):

        """
        @type  path:                 string
        @param path:                 path to import from
        """

        #---args
        self.path                    = path
        self.create_geo              = create_geo
        self.create_deformer         = create_deformer
        self.set_weights             = set_weights
        self.set_curves              = set_curves
        #---vars
        self.dict                    = {}
        self.geo_membership          = []
        self.weight_geo              = {}
        self.anim_curves             = {}
        self.weights                 = {}
        self.deformer_weights        = {}
        self.baseGeo                 = []
        self.geoms                   = []
        self.control                 = ""
        self.lockAttrs               = []
        self.ihi                     = None
        self.side                    = ""
        self.short_name              = ""
        self.tNames                  = {}
        self.rNames                  = {}

        self.__create()

    def __unpack(self):
        "imports the dictionary, separates all of the info for later use"
        file = open(self.path, "rb")
        self.dict = json.load(file)
        file.close()
        
        self.weight_geo       = self.dict["weight_geo"]
        self.baseGeo          = self.dict["base_geo"]
        self.t_pivots         = self.dict["t_pivots"]
        self.r_pivots         = self.dict["r_pivots"]
        self.anim_curves      = self.dict["anim_curves"]
        self.weights          = self.dict["weights"]
        self.geo_membership   = self.dict["geo_membership"]
        self.deformer_weights = self.dict["deformer_weights"]
        self.geoms            = self.dict["geoms"]
        self.control          = self.dict["control"]
        self.lockAttrs        = self.dict["lockAttrs"]
        self.ihi              = self.dict["ihi"]
        self.side             = self.dict["side"]
        self.short_name       = self.dict["short_name"]
        self.tNames           = self.dict["tNames"]
        self.rNames           = self.dict["rNames"]
    def __create_geo(self):
        # check if geo already exists.  If so use it instead of creating new.
        if self.create_geo == True:
            #---create weight surface, parent if any
            if not cmds.objExists(self.weight_geo["name"]):
                self.weightGeo = create_mesh(self.weight_geo).fullPathName()
                self.weightGeo = cmds.listRelatives(self.weightGeo, parent = True)
                self.weightGeo = cmds.rename(self.weightGeo, self.weight_geo["name"])
            else:
                self.weightGeo = self.weight_geo["name"]
            #---create base geo, parent if any
            tmp_baseGeo = []
            tmp = []
            for i in range(len(self.baseGeo)):
                if not cmds.objExists(self.baseGeo[i]["name"]):
                    tmp = create_mesh(self.baseGeo[i]).fullPathName()
                    tmp = cmds.listRelatives(tmp, parent = True)
                    tmp = cmds.rename(tmp, self.baseGeo[i]["name"])
                    cmds.setAttr(tmp+".v",0)
                    tmp_baseGeo.append(tmp)
                else:
                    tmp_baseGeo.append(self.baseGeo[i]["name"])
            self.baseGeo = tmp_baseGeo
            
            #---create t_pivots
            tmp_array = []
            tmp = []
            for i in range(len(self.t_pivots)):
                tmp = create_curve(self.t_pivots[i]).fullPathName()
                tmp = cmds.listRelatives(tmp, parent = True)
                tmp = cmds.rename(tmp, self.t_pivots[i]["name"])
                cmds.setAttr(tmp+".v",0)
                tmp_array.append(tmp)
            self.t_pivots = tmp_array
#             print self.t_pivots
            #---create r_pivots
            tmp_array = []
            tmp = []
            for i in range(len(self.r_pivots)):
                tmp = create_curve(self.r_pivots[i]).fullPathName()
                tmp = cmds.listRelatives(tmp, parent = True)
                tmp = cmds.rename(tmp, self.r_pivots[i]["name"])
                cmds.setAttr(tmp+".v",0)
                tmp_array.append(tmp)
            self.r_pivots = tmp_array
            
    def __create_deformer(self):
        "creates deformer, turns envelope off"
        if self.create_deformer == True:
            self.deformer = vectorDeformerCmds.vectorDeformerCmd(
                                                 weightGeo = self.weightGeo,
                                                 geoms = self.geo_membership,
                                                 weightBase = self.baseGeo,
                                                 control = '',
                                                 ihi = 1,
                                                 side = self.side,
                                                 name = self.short_name,
                                                 tPivots = self.t_pivots,
                                                 rPivots = self.r_pivots,
                                                 #---Mouth
                                                 tNames = self.tNames,
                                                 rNames = self.rNames,
                                                 ).returnDeformer
#             cmds.setAttr(self.deformer + ".envelope", 0)

    def __set_anim_curves(self):
        if self.set_curves == True:
            for i in range(len(self.anim_curves)):
                anim_curves = self.anim_curves[str(i)]["name"]
                frame_values = self.anim_curves[str(i)]["frame_values"]
                frame_times= self.anim_curves[str(i)]["frame_times"]
                in_x_tangents= self.anim_curves[str(i)]["in_x_tangents"]
                in_y_tangents= self.anim_curves[str(i)]["in_y_tangents"]
                out_x_tangents= self.anim_curves[str(i)]["out_x_tangents"]
                out_y_tangents= self.anim_curves[str(i)]["out_y_tangents"]
                in_tangents_type= self.anim_curves[str(i)]["in_tangents_type"]
                out_tangents_type= self.anim_curves[str(i)]["out_tangents_type"]
                set_anim_curves(anim_curves,
                                frame_values,
                                frame_times,
                                in_x_tangents,
                                in_y_tangents,
                                out_x_tangents,
                                out_y_tangents,
                                in_tangents_type,
                                out_tangents_type)

    def __set_weights(self):
        "sets deformer weight, then sets double array weights"
        if self.set_weights == True:
            if self.deformer_weights:
                for i in self.deformer_weights.keys():
                    cmds.setAttr(i, self.deformer_weights.get(i))

            for i in self.weights.keys():
                weights = self.weights.get(i)
                if not weights == None:
                    try:
                        cmds.setAttr(i, weights,typ='doubleArray')
                    except:
                        pass

    def __finalize(self):
        cmds.setAttr(self.deformer + ".envelope", 1)
        cmds.refresh(force = True)
        if self.create_deformer == True:
            if self.baseGeo:
                cmds.setAttr(self.deformer + ".useBaseGeo", 1)
            cmds.setAttr(self.deformer + ".cachePivots", 1)
            cmds.setAttr(self.deformer + ".cacheWeights", 1)
            cmds.setAttr(self.deformer + ".cacheWeightMesh", 1)
            cmds.setAttr(self.deformer + ".cacheWeightCurves", 1)

    def __create(self):
        self.__unpack()
        self.__create_geo()
        self.__create_deformer()
        self.__set_anim_curves()
        self.__set_weights()
        self.__finalize()

##############################################################################
#---Example:

# import_vector_deformer(path = "/corp/home/lharrison/Desktop/testExport.vec", 
#                       create_geo = True,
#                       create_deformer = True,
#                       set_weights = True,
#                       set_curves = True)
##############################################################################




#===============================================================================
#CLASS:         export_curve_roll_deformer
#DESCRIPTION:   exports the curve roll deformer to an external file
#USAGE:         set args and run
#RETURN:
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Dec 2nd, 2014
#Version        1.0.0
#===============================================================================

class export_curve_roll_deformer():
    def __init__(self,
                 name = "",
                 path = "",
                 ):

        """
        @type  name:                        string
        @param name:                        name of the deformer you want to
                                            export

        @type  export_path:                 string
        @param export_path:                 path to export to

        """

        #---args
        self.name                           = name
        self.path                           = path
        #---vars
        self.geo_membership                 = []
        self.weight_geo                     = {}
        self.base_geo                       = []
        self.in_curve                       = {}
        self.out_curve                      = {}
#         self.t_pivots                       = []
#         self.r_pivots                       = []
        self.anim_curves                    = {}
        self.deformer_weights               = {}
        self.weights                        = {}
        self.vector_dict                    = {}
        # naming information for rebuilding
        self.weightBase              = 0
        self.geoms                   = []
        self.weightGeo               = ""
        self.weightBase              = []
#         self.tPivots                 = []
#         self.rPivots                 = []
        self.inCurve                 = []
        self.outCurve                = []
        self.control                 = ""
        self.lockAttrs               = []
        self.ihi                     = None
        self.side                    = ""
        self.short_name              = ""
        self.tNames                  = []
        self.rNames                  = []

        self.__create()

    def __check(self):
        if not cmds.objExists(self.name):
            raise Exception(self.name + " does not exist")
            quit()
    def __get_info(self):
            # get all info from the deformer
            # get all attribute names
            # from attr names you will know curve and weight names
#         self.geoms = cmds.deformer(self.name, q = True,g = True)

        self.weightGeo = cmds.listConnections(self.name + ".weightPatch",
                                              d = False)[0]

        self.weightBase = cmds.listConnections(self.name + ".baseGeoArray",
                                              d = False)

        self.inCurve = cmds.listConnections(self.name + ".inCurve",
                                              d = False)[0]
        
        self.outCurve = cmds.listConnections(self.name + ".outCurve",
                                              d = False)[0]

        self.side = self.name.split("_")[0]
        self.short_name = self.name.split("_")[1]
        self.tNames = cmds.listConnections(self.name + ".rValueParentArray",
                                           d = True,
                                           p = True)
        for i in range(len(self.tNames)):
            self.tNames[i] = self.tNames[i].split(".")[1]
        self.rNames  = cmds.listConnections(self.name + ".rValueParentArray",
                                            d = True,
                                            p = True)
        for i in range(len(self.rNames)):
            self.rNames[i] = self.rNames[i].split(".")[1]

    def __get_memberships(self):
            # get all deformed geometry and their memberships
            #get set
            
            self.set   = cmds.listConnections(self.name + ".message",
                                              d = True,
                                              p = True)[0].split(".")[0]
#             attr = cmds.getAttr(self.name + ".message")
            self.geo_membership = cmds.sets(self.set, q = True)

            self.geo_membership = cmds.deformer(self.name, q = True, g = True)


    def __get_geoms(self):
            # get all driver geometry (for rebuilding)
        self.weight_geo = return_mesh_info(name = self.weightGeo).mesh
        for i in range(len(self.weightBase)):
            shape = cmds.listRelatives(self.weightBase[i], shapes = True)[0]
            if (cmds.objectType(shape, isType='nurbsSurface')):
                self.base_geo.append(return_nurbs_surface_info(name = self.weightBase[i]).nurbs)
            if (cmds.objectType(shape, isType='mesh')):
                self.base_geo.append(return_mesh_info(name = self.weightBase[i]).mesh)
 
        shape = cmds.listRelatives(self.inCurve, shapes = True)[0]
        self.in_curve = return_nurbs_curve_info(name = self.inCurve).nurbsCurve

        shape = cmds.listRelatives(self.outCurve, shapes = True)[0]
        self.out_curve = return_nurbs_curve_info(name = self.outCurve).nurbsCurve

#             need to write functionality for nurbs curves
    def __get_curves(self):
            # get all curve infos
        self.connections = []
        self.connections.append(cmds.listConnections(self.name + ".rAnimCurveUArray",
                                                     type = "animCurve",
                                                     d = False))
        self.connections.append(cmds.listConnections(self.name + ".rAnimCurveVArray",
                                                     type = "animCurve",
                                                     d = False))
        flat_conn = []
        for i in range(len(self.connections)):
            if self.connections[i]:
                for j in range(len(self.connections[i])):
                    if self.connections[i][j]:
                        flat_conn.append(self.connections[i][j])
        all = flat_conn
        self.anim_curves = get_anim_curve_info(anim_curve = all).curve_dict
    def __get_weights(self):
            # get all double array weights
            tmp_weight_names = cmds.listAttr(self.name, 
                                             ud = True, 
                                             a = True)
            tmp_values = []
            tmp_names = []
            geoms = cmds.deformer(self.name, q = True,g = True)
            for i in range(len(tmp_weight_names)):
                for j in range(len(geoms)):
                    split_weights = tmp_weight_names[i].split(".")
                    tmp_names.append(self.name
                                     + "."
                                     + split_weights[0]
                                     +"[" + str(j)
                                     + "]."
                                     + split_weights[1])
                    tmp_values.append(cmds.getAttr(self.name
                                                   + "."
                                                   + split_weights[0]
                                                   +"[" + str(j)
                                                   + "]."
                                                   + split_weights[1]))
            self.weights = dict(zip(tmp_names,tmp_values))
            # get deformer weights
            tmp_def_weights = []
            tmp_def_names   = []
            tmp_flat_weights= []
            tmp_flat_names= []
            try:
                for i in range(len(geoms)):
                    tmp_def_names = self.name + ".weightList[" + str(i) + "].weights"
                    indices = cmds.getAttr(tmp_def_names, mi = True)
                    for j in range(len(indices)):
                        tmp_flat_names.append(self.name
                                              + ".weightList["
                                              + str(i)
                                              + "].weights["
                                              + str(indices[j])
                                              + "]")
                        tmp_flat_weights.append(cmds.getAttr(tmp_flat_names[j]))
                for i in range(len(tmp_flat_names)):
                    self.deformer_weights[tmp_flat_names[i]] = tmp_flat_weights[i]
#             print self.deformer_weights
            except:
                pass
#             print self.deformer_weights
    def __organize(self):
        self.vector_dict = {
                           "weight_geo":           self.weight_geo,
                           "anim_curves":          self.anim_curves,
                           "weights":              self.weights,
                           "geoms":                self.geoms,
                           "base_geo":             self.base_geo,
                           "in_curve":             self.in_curve,
                           "out_curve":             self.out_curve,
#                            "t_pivots":             self.t_pivots,
#                            "r_pivots":             self.r_pivots,
                           "geo_membership":       self.geo_membership,
                           "deformer_weights":     self.deformer_weights,
                           "weightGeo":            self.weightGeo,
                           "control":              self.control,
                           "lockAttrs":            self.lockAttrs,
                           "ihi":                  self.ihi,
                           "side":                 self.side,
                           "short_name":           self.short_name,
                           "rNames":               self.rNames,
                           }
#         print self.vector_dict
    def __export(self):
        file = open(self.path, "wb")
        json.dump(self.vector_dict, file, sort_keys = True, indent = 2)
        file.close()
        
            # format info
            # export info to a file
    def __create(self):
        self.__check()
        self.__get_info()
        self.__get_memberships()
        self.__get_geoms()
        self.__get_curves()
        self.__get_weights()
        self.__organize()
        self.__export()

###############################################################################
#---Example:
# export_curve_roll_deformer(name = "C_bLipRoll_CRD",
#                       path = "/corp/home/lharrison/Desktop/testExport.crd")
###############################################################################



#===============================================================================
#CLASS:         import_vector_deformer
#DESCRIPTION:   rebuilds the slide deformer
#USAGE:         set args and run
#RETURN:        
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Dec 1st, 2014
#Version        1.0.0
#===============================================================================

class import_curve_roll_deformer():
    def __init__(self,
                 path = "",
                 create_geo = True,
                 create_deformer = True,
                 set_weights = True,
                 set_curves = True,
                 ):

        """
        @type  path:                 string
        @param path:                 path to import from
        """

        #---args
        self.path                    = path
        self.create_geo              = create_geo
        self.create_deformer         = create_deformer
        self.set_weights             = set_weights
        self.set_curves              = set_curves
        #---vars
        self.dict                    = {}
        self.geo_membership          = []
        self.weight_geo              = {}
        self.anim_curves             = {}
        self.weights                 = {}
        self.deformer_weights        = {}
        self.baseGeo                 = []
        self.geoms                   = []
        self.control                 = ""
        self.lockAttrs               = []
        self.ihi                     = None
        self.side                    = ""
        self.short_name              = ""
        self.rNames                  = {}
        self.in_curve                = ""
        self.out_curve               = ""
        self.__create()

    def __unpack(self):
        "imports the dictionary, separates all of the info for later use"
        file = open(self.path, "rb")
        self.dict = json.load(file)
        file.close()
        
        self.weight_geo       = self.dict["weight_geo"]
        self.baseGeo          = self.dict["base_geo"]
        self.in_curve         = self.dict["in_curve"]
        self.out_curve        = self.dict["out_curve"]
        self.anim_curves      = self.dict["anim_curves"]
        self.weights          = self.dict["weights"]
        self.geo_membership   = self.dict["geo_membership"]
        self.deformer_weights = self.dict["deformer_weights"]
        self.geoms            = self.dict["geoms"]
        self.control          = self.dict["control"]
        self.lockAttrs        = self.dict["lockAttrs"]
        self.ihi              = self.dict["ihi"]
        self.side             = self.dict["side"]
        self.short_name       = self.dict["short_name"]
        self.rNames           = self.dict["rNames"]
    def __create_geo(self):
        # check if geo already exists.  If so use it instead of creating new.
        if self.create_geo == True:
            #---create weight surface, parent if any
            if not cmds.objExists(self.weight_geo["name"]):
                self.weightGeo = create_mesh(self.weight_geo).fullPathName()
                self.weightGeo = cmds.listRelatives(self.weightGeo, parent = True)
                self.weightGeo = cmds.rename(self.weightGeo, self.weight_geo["name"])
            else:
                self.weightGeo = self.weight_geo["name"]
            #---create base geo, parent if any
            tmp_baseGeo = []
            tmp = []
            for i in range(len(self.baseGeo)):
                if not cmds.objExists(self.baseGeo[i]["name"]):
                    tmp = create_mesh(self.baseGeo[i]).fullPathName()
                    tmp = cmds.listRelatives(tmp, parent = True)
                    tmp = cmds.rename(tmp, self.baseGeo[i]["name"])
                    cmds.setAttr(tmp+".v",0)
                    tmp_baseGeo.append(tmp)
                else:
                    tmp_baseGeo.append(self.baseGeo[i]["name"])
            self.baseGeo = tmp_baseGeo
            
        #---create in_curve
        self.inCurve = create_curve(self.in_curve).fullPathName()
        self.inCurve = cmds.listRelatives(self.inCurve, parent = True)
        self.inCurve = cmds.rename(self.inCurve, self.in_curve["name"])
            
        #---create out_curve
        self.outCurve = create_curve(self.out_curve).fullPathName()
        self.outCurve = cmds.listRelatives(self.outCurve, parent = True)
        self.outCurve = cmds.rename(self.outCurve, self.out_curve["name"])
    def __create_deformer(self):
        "creates deformer, turns envelope off"
        if self.create_deformer == True:
            self.deformer = curveRollDeformerCmds.curveRollDeformerCmd(
                                                 weightGeo = self.weightGeo,
                                                 geoms = self.geo_membership,
                                                 weightBase = self.baseGeo,
                                                 control = '',
                                                 ihi = 1,
                                                 side = self.side,
                                                 name = self.short_name,
                                                 inCurve = self.inCurve,
                                                 outCurve = self.outCurve,
                                                 #---Mouth
                                                 rNames = self.rNames,
                                                 ).returnDeformer
#             cmds.setAttr(self.deformer + ".envelope", 0)

    def __set_anim_curves(self):
        if self.set_curves == True:
            for i in range(len(self.anim_curves)):
                anim_curves = self.anim_curves[str(i)]["name"]
                frame_values = self.anim_curves[str(i)]["frame_values"]
                frame_times= self.anim_curves[str(i)]["frame_times"]
                in_x_tangents= self.anim_curves[str(i)]["in_x_tangents"]
                in_y_tangents= self.anim_curves[str(i)]["in_y_tangents"]
                out_x_tangents= self.anim_curves[str(i)]["out_x_tangents"]
                out_y_tangents= self.anim_curves[str(i)]["out_y_tangents"]
                in_tangents_type= self.anim_curves[str(i)]["in_tangents_type"]
                out_tangents_type= self.anim_curves[str(i)]["out_tangents_type"]
                set_anim_curves(anim_curves,
                                frame_values,
                                frame_times,
                                in_x_tangents,
                                in_y_tangents,
                                out_x_tangents,
                                out_y_tangents,
                                in_tangents_type,
                                out_tangents_type)

    def __set_weights(self):
        "sets deformer weight, then sets double array weights"
        if self.set_weights == True:
            if self.deformer_weights:
                for i in self.deformer_weights.keys():
                    cmds.setAttr(i, self.deformer_weights.get(i))

            for i in self.weights.keys():
                weights = self.weights.get(i)
                if not weights == None:
                    try:
                        cmds.setAttr(i, weights,typ='doubleArray')
                    except:
                        pass

    def __finalize(self):
        cmds.setAttr(self.deformer + ".envelope", 1)
        cmds.refresh(force = True)
        if self.create_deformer == True:
            if self.baseGeo:
                cmds.setAttr(self.deformer + ".useBaseGeo", 1)
            cmds.setAttr(self.deformer + ".cacheParams", 1)
            cmds.setAttr(self.deformer + ".cacheTangents", 1)
            cmds.setAttr(self.deformer + ".cacheWeights", 1)
            cmds.setAttr(self.deformer + ".cacheWeightMesh", 1)
            cmds.setAttr(self.deformer + ".cacheWeightCurves", 1)

    def __create(self):
        self.__unpack()
        self.__create_geo()
        self.__create_deformer()
        self.__set_anim_curves()
        self.__set_weights()
        self.__finalize()



###############################################################################
#---Example:
# export_curve_roll_deformer(name = "C_bLipRoll_CRD",
#                       path = "/corp/home/lharrison/Desktop/testExport.crd")
###############################################################################



##############################################################################
#---Example:

# import_curve_roll_deformer(path = "/corp/home/lharrison/Desktop/testExport.crd", 
#                             create_geo = True,
#                             create_deformer = True,
#                             set_weights = True,
#                             set_curves = True)
##############################################################################


def comparePolyCount(srcMesh, baseMesh):
    
    srcCount = cmds.polyEvaluate(srcMesh, v=True)
    baseCount = cmds.polyEvaluate(baseMesh, v=True)
    if srcCount == baseCount:
        return True
    return

# def weightTransfer(srcMesh, destMesh, srcDeformer, destDeformer, attributes):
def lhDeformerWeightTransfer(srcMesh, srcDeformer, destMesh, destDeformer):
    # Get Attributes From Source
    attrs = cmds.listAttr(srcDeformer, ud = True, a = True, m=True)
    srcAttributes = ["{0}.{1}".format(srcDeformer, x) for x in attrs]
    
    jointOff = cmds.joint(n="JntOFF_TEMP", p=(0,0,0))
    jointOn = cmds.joint(n="JntON_TEMP", p=(0,0,0))
    tmpMesh = cmds.duplicate(srcMesh, name = srcMesh + "TempWeightTransfer")[0]

    srcSkin = cmds.skinCluster(jointOn, jointOff, tmpMesh, n = "TempSKIN", tsb=True)[0]
    srcVertCount = cmds.polyEvaluate(srcMesh, v=1) - 1
    dstVertCount = cmds.polyEvaluate(destMesh, v=1) - 1

    dstSkin = cmds.skinCluster(jointOn, jointOff, destMesh, n = "TempSKINDEST", tsb=True)[0]
    
    for srcAttr in srcAttributes:
        weight = cmds.getAttr(srcAttr)
        #---If weight hasn't been set, skip it
        if not weight:
            continue
        #---If weight isn't large enough, fill additional indexes with empty weight values
        if len(weight) < srcVertCount:
            difference = srcVertCount - len(weight)
            for i in range(srcVertCount):
                if i > difference:
                    continue
                weight.append(0.0)

        empty = [1.0 for x in range(len(weight))]
        cmds.setAttr('{0}.weightList[0:{1}].weights[1]'.format(srcSkin, srcVertCount), *empty, size=len(empty))
        cmds.setAttr('{0}.weightList[0:{1}].weights[0]'.format(srcSkin, srcVertCount), *weight, size=len(empty))
        # Only Use Skin Percent to normalize! It is crappy slow to set points....
        cmds.skinPercent( srcSkin, '{0}.vtx[0:{1}]'.format(srcMesh + "TempWeightTransfer", srcVertCount), normalize=True)

        cmds.copySkinWeights( ss=srcSkin, ds=dstSkin, noMirror=True, ia="oneToOne")

        destAttr = srcAttr.replace(srcDeformer, destDeformer)
        #---Get weights from dest skin cluster
        destWeight = cmds.getAttr("{0}.weightList[0:{1}].weights[0]".format(dstSkin, dstVertCount))
        cmds.setAttr(destAttr, destWeight, typ='doubleArray')
    
    cmds.delete(srcSkin, dstSkin, jointOff, jointOn, tmpMesh)
