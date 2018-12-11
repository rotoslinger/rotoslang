import sys
linux = '/corp/projects/eng/lharrison/workspace/levi_harrison_test/lhrig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "mac" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)






# import maya.cmds as cmds
from maya import cmds, OpenMaya, mel, OpenMayaAnim
import json
import os
from utils import slideDeformerCmds
reload(slideDeformerCmds)
# random
# math

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
        self.__create()

    def __check(self):
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
    return new_mesh

###################################################
#---Example
# mesh_dict = return_mesh_info(name = "C_lipsWeightPatch_EX").mesh
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
        self.formU                          = None #---MFnNurbsSurface::Form
        self.formV                          = None #---MFnNurbsSurface::Form
        self.parent                         = ""#---MObject
        self.__get_nurbs()

    def __check(self):
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
        self.formU = self.fn_nurbs.formInU()
        self.formV = self.fn_nurbs.formInV()

    def __write_dict(self):
        self.nurbs = {"name"              : self.name,
                     "controlVertices"    : self.controlVertices ,
                     "uKnotSequences"     : self.uKnotSequences ,
                     "vKnotSequences"     : self.vKnotSequences ,
                     "degreeInU"          : self.degreeInU ,
                     "degreeInV"          : self.degreeInV,
                     "formU"              : self.formU,
                     "formV"              : self.formV,
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
                     nurbs_dict.get("formU"),
                     nurbs_dict.get("formV"),
                     False)
    return new_nurbs
#########################################################
#---Example
# nurbs_dict = return_nurbs_surface_info(name = "C_lipsSlidePatch_EX").nurbs
# create_nurbs_surface(nurbs_dict)
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
                                      True,
                                      None,
                                      False)
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
        self.anim_curves                    = {}
        self.deformer_weights               = {}
        self.weights                        = {}
        self.slide_dict                     = {}
        # naming information for rebuilding
        self.driverSurface           = ""
        self.geoms                   = []
        self.weightGeo               = ""
        self.control                 = ""
        self.lockAttrs               = []
        self.ihi                     = None
        self.side                    = ""
        self.short_name              = ""
        self.uNames                  = []
        self.vNames                  = []
        self.rNames                  = []
        self.nNames                  = []
        self.uUseAnimCurves          = []
        self.vUseAnimCurves          = []
        self.nUseAnimCurves          = []
        self.rUseAnimCurves          = []
        

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
#         self.control                 = ""
# 
#         self.lockAttrs               = []
#         self.ihi                     = None

        self.side = self.name.split("_")[0]
        self.short_name = self.name.split("_")[1]
        self.uNames = cmds.listConnections(self.name + ".uValueParentArray",
                                           d = True,
                                           p = True)
        for i in range(len(self.uNames)):
            self.uNames[i] = self.uNames[i].split(".")[1]
        self.vNames  = cmds.listConnections(self.name + ".vValueParentArray",
                                            d = True,
                                            p = True)
        for i in range(len(self.vNames)):
            self.vNames[i] = self.vNames[i].split(".")[1]
        self.rNames  = cmds.listConnections(self.name + ".rValueParentArray",
                                            d = True,
                                            p = True)
        for i in range(len(self.rNames)):
            self.rNames[i] = self.rNames[i].split(".")[1]
        self.nNames   = cmds.listConnections(self.name + ".nValueParentArray",
                                             d = True,
                                             p = True)
        for i in range(len(self.nNames)):
            self.nNames[i] = self.nNames[i].split(".")[1]

        self.uUseAnimCurves          = [1]
        self.vUseAnimCurves          = [1]
        self.nUseAnimCurves          = [1]
        self.rUseAnimCurves          = [1]

    def __get_memberships(self):
            # get all deformed geometry and their memberships
            #get set
            self.set   = cmds.listConnections(self.name + ".message",
                                              d = True,
                                              p = True)[0].split(".")[0]
#             attr = cmds.getAttr(self.name + ".message")
            self.geo_membership = cmds.sets(self.set, q = True)

    def __get_driver_geom(self):
            # get all driver geometry (for rebuilding)
        self.driver_surface = return_nurbs_surface_info(name = self.driverSurface).nurbs
        self.weight_geo = return_mesh_info(name = self.weightGeo).mesh

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
#         print self.anim_curves
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
                    tmp_def_weights = cmds.getAttr(tmp_def_names)
                    for j in range(len(tmp_def_weights[0])):
                        tmp_flat_names.append(self.name
                                              + ".weightList["
                                              + str(i)
                                              + "].weights["
                                              + str(j)
                                              + "]")
                        tmp_flat_weights.append(tmp_def_weights[0][j])
                for i in range(len(tmp_flat_names)):
                    self.deformer_weights[tmp_flat_names[i]] = tmp_flat_weights[i]
            except:
                pass

    def __organize(self):
        self.slide_dict = {
                           "driver_surface":       self.driver_surface,
                           "weight_geo":           self.weight_geo,
                           "anim_curves":          self.anim_curves,
                           "weights":              self.weights,
                           "driverSurface":        self.driverSurface,
                           "geoms":                self.geoms,
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
                           "rNames":               self.rNames,
                           "nNames":               self.nNames,
                           "uUseAnimCurves":       self.uUseAnimCurves,
                           "vUseAnimCurves":       self.vUseAnimCurves,
                           "nUseAnimCurves":       self.nUseAnimCurves,
                           "rUseAnimCurves":       self.rUseAnimCurves,
                           }
#         print self.slide_dict
    def __export(self):
        file = open(self.path, "wb")
        json.dump(self.slide_dict, file, sort_keys = True, indent = 2)
        file.close()
        
            # format info
            # export info to a file
    def __create(self):
        self.__check()
        self.__get_info()
        self.__get_memberships()
        self.__get_driver_geom()
        self.__get_curves()
        self.__get_weights()
        self.__organize()
        self.__export()

##############################################################################
#---Example:
# export_slide_deformer(name = "C_testFace_SLD",
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
        self.driver_surface          = {}
        self.weight_geo              = {}
        self.anim_curves             = {}
        self.weights                 = {}
        self.deformer_weights        = {}
        self.driverSurface           = ""
        self.geoms                   = []
        self.control                 = ""
        self.lockAttrs               = []
        self.ihi                     = None
        self.side                    = ""
        self.short_name              = ""
        self.uNames                  = []
        self.vNames                  = []
        self.rNames                  = []
        self.nNames                  = []
        self.uUseAnimCurves          = []
        self.vUseAnimCurves          = []
        self.nUseAnimCurves          = []
        self.rUseAnimCurves          = []

        self.__create()

    def __unpack(self):
        "imports the dictionary, separates all of the info for later use"
        file = open(self.path, "rb")
        self.dict = json.load(file)
        file.close()
        
        self.driver_surface   = self.dict["driver_surface"]
        self.weight_geo       = self.dict["weight_geo"]
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
        self.rNames           = self.dict["rNames"]
        self.nNames           = self.dict["nNames"]
        self.uUseAnimCurves   = self.dict["uUseAnimCurves"]
        self.vUseAnimCurves   = self.dict["vUseAnimCurves"]
        self.nUseAnimCurves   = self.dict["nUseAnimCurves"]
        self.rUseAnimCurves   = self.dict["rUseAnimCurves"]
    def __create_geo(self):
        if self.create_geo == True:
            #---create driver surface, parent if any
            self.driverSurface = create_nurbs_surface(self.driver_surface).fullPathName()
            self.driverSurface = cmds.listRelatives(self.driverSurface, parent = True)
            self.driverSurface = cmds.rename(self.driverSurface, self.driver_surface["name"])
            #---create weight patch, parent if any
            self.weightGeo = create_mesh(self.weight_geo).fullPathName()
            self.weightGeo = cmds.listRelatives(self.weightGeo, parent = True)
            self.weightGeo = cmds.rename(self.weightGeo, self.weight_geo["name"])

    def __create_deformer(self):
        "creates deformer, turns envelope off"
        if self.create_deformer == True:
            self.deformer = slideDeformerCmds.slideDeformerCmd(
                                                 driverSurface = self.driverSurface,
                                                 weightGeo = self.weightGeo,
                                                 geoms = self.geo_membership,
                                                 control = '',
                                                 ihi = 1,
                                                 side = self.side,
                                                 name = self.short_name,
                                                 #---Mouth
                                                 uNames = self.uNames,
                                                 vNames = self.vNames,
                                                 rNames = self.rNames,
                                                 nNames = self.nNames,
                                                 ).returnDeformer
            cmds.setAttr(self.deformer + ".envelope", 0)

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
                    try:
                        cmds.setAttr(i, self.deformer_weights.get(i))
                    except:
                        pass
                print self.deformer_weights
            
            for i in self.weights.keys():
                weights = self.weights.get(i)
                if not weights == None:
                    try:
                        cmds.setAttr(i, weights,typ='doubleArray')
                    except:
                        pass

    def __finalize(self):
        if self.create_deformer == True:
            cmds.setAttr(self.deformer + ".envelope", 1)
            cmds.setAttr(self.deformer + ".cachePivots", 1)
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
        self.__finalize()

##############################################################################
#---Example:
# import_slide_deformer(path = "/corp/home/lharrison/Desktop/SlideDeformerCPP/brow.sld", 
#                       create_geo = False,
#                       create_deformer = False,
#                       set_weights = True,
#                       set_curves = False)
# 
# import_slide_deformer(path = "/corp/home/lharrison/Desktop/lips.sld", 
#                       create_geo = False,
#                       create_deformer = False,
#                       set_weights = True,
#                       set_curves = True)
##############################################################################
