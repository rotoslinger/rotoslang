from maya import cmds, OpenMaya, OpenMayaAnim


class meshData():
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
                     "type"            : "mesh"
                     }

    def __create(self):
        self.__check()
        self.__get_num_verts()
        self.__get_num_polygons()
        self.__get_vert_array()
        self.__get_counts_connects()
        self.__get_UVs()
        self.__write_dict()


def createMesh(mesh_dict, name=None, parent=None):
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
    parentNameNewGeo(mesh_dict, name, new_mesh, parent)
    return new_mesh


def parentNameNewGeo(meshDict, name, newGeo, parent):
    if parent:
        child = cmds.listRelatives(newGeo.fullPathName(), parent=True)[0]
        if cmds.objExists(parent):
            cmds.parent(child, parent)
    if not parent:
        if meshDict.get("parent"):
            child = cmds.listRelatives(newGeo.fullPathName(), parent=True)[0]
            parent = meshDict.get("parent")
            if cmds.objExists(parent):
                cmds.parent(child, parent)
    if name:
        shapeParent = cmds.listRelatives(newGeo.fullPathName(), parent=True)[0]
        cmds.rename(shapeParent, name)
        cmds.rename(newGeo.fullPathName(), "{0}Shape".format(name))


class nurbsSurfaceData():
    # ===============================================================================
    # CLASS:         return_nurbs_surface_info
    # DESCRIPTION:   returns information that can be used to rebuild a nurbsSurface
    # USAGE:         set args and run
    # RETURN:        nurbs
    # REQUIRES:      maya.cmds, maya.OpenMaya
    # AUTHOR:        Levi Harrison
    # DATE:          Nov 10th, 2014
    # Version        1.0.0
    # ===============================================================================

    # ==============================================================================
    #########################################################
    # ---Example
    # nurbs_dict = return_nurbs_surface_info(name = "C_lipsSlidePatch_EX").nurbs
    # create_nurbs_surface(nurbs_dict)
    #########################################################
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
                     "parent"             : self.parent,
                     "type"               : "nurbsSurface"

                      }

    def __get_nurbs(self):
        self.__check()
        self.__get_cvs()
        self.__get_knot_sequences()
        self.__get_degrees()
        self.__get_forms()
        self.__write_dict()


def createNurbsSurface(nurbs_dict, name=None, parent=None):
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
    parentNameNewGeo(nurbs_dict, name, new_nurbs, parent)
    return new_nurbs


class nurbsCurveData():
    # ===============================================================================
    # CLASS:         return_nurbs_curve_info
    # DESCRIPTION:   returns information that can be used to rebuild a nurbsSurface
    # USAGE:         set args and run
    # RETURN:        nurbs
    # REQUIRES:      maya.cmds, maya.OpenMaya
    # AUTHOR:        Levi Harrison
    # DATE:          Dec 1st, 2014
    # Version        1.0.0
    # ===============================================================================

    # ==============================================================================

    #########################################################
    # ---Example
    # curve_dict = return_nurbs_curve_info(name = "curve1").nurbsCurve
    # create_curve(curve_dict)
    #########################################################

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
                           "parent"            : self.parent,
                           "type"              : "nurbsCurve"
                           }

    def __get_nurbsCurve(self):
        self.__check()
        self.__get_cvs()
        self.__get_knot_sequences()
        self.__get_degrees()
        self.__get_forms()
        self.__write_dict()


def create_curve(curve_dict, name=None, parent=None):
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
    parentNameNewGeo(curve_dict, name, new_nurbsCurve, parent)
    return new_nurbsCurve


class get_anim_curve_info():
    # ===============================================================================
    # CLASS:         get_anim_curve_info
    # DESCRIPTION:   puts anim curve info info from a list of anim curves into a dict
    # USAGE:         give list of anim curves
    # RETURN:        anim_curves
    # REQUIRES:      maya.cmds, maya.OpenMayaAnim
    # AUTHOR:        Levi Harrison
    # DATE:          Nov. 11th, 2014
    # Version        1.0.0
    # ===============================================================================
    ##############################################
    # Example:
    # dict = get_anim_curve_info(anim_curve = ["C_TLipLR_ACV"]).curve_dict
    # print dict
    ###############################################

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


def set_anim_curve_data(anim_curves,
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


def comparePolyCount(srcMesh, baseMesh):

    srcCount = cmds.polyEvaluate(srcMesh, v=True)
    baseCount = cmds.polyEvaluate(baseMesh, v=True)
    if srcCount == baseCount:
        return True
    return


# def lhDeformerWeightTransfer(srcMesh, srcDeformer, destMesh, destDeformer):
#     # Get Attributes From Source
#     attrs = cmds.listAttr(srcDeformer, ud = True, a = True, m=True)
#     srcAttributes = ["{0}.{1}".format(srcDeformer, x) for x in attrs]
#
#     jointOff = cmds.joint(n="JntOFF_TEMP", p=(0,0,0))
#     jointOn = cmds.joint(n="JntON_TEMP", p=(0,0,0))
#     tmpMesh = cmds.duplicate(srcMesh, name = srcMesh + "TempWeightTransfer")[0]
#
#     srcSkin = cmds.skinCluster(jointOn, jointOff, tmpMesh, n = "TempSKIN", tsb=True)[0]
#     srcVertCount = cmds.polyEvaluate(srcMesh, v=1) - 1
#     dstVertCount = cmds.polyEvaluate(destMesh, v=1) - 1
#
#     dstSkin = cmds.skinCluster(jointOn, jointOff, destMesh, n = "TempSKINDEST", tsb=True)[0]
#
#     for srcAttr in srcAttributes:
#         weight = cmds.getAttr(srcAttr)
#         #---If weight hasn't been set, skip it
#         if not weight:
#             continue
#         #---If weight isn't large enough, fill additional indexes with empty weight values
#         if len(weight) < srcVertCount:
#             difference = srcVertCount - len(weight)
#             for i in range(srcVertCount):
#                 if i > difference:
#                     continue
#                 weight.append(0.0)
#
#         empty = [1.0 for x in range(len(weight))]
#         cmds.setAttr('{0}.weightList[0:{1}].weights[1]'.format(srcSkin, srcVertCount), *empty, size=len(empty))
#         cmds.setAttr('{0}.weightList[0:{1}].weights[0]'.format(srcSkin, srcVertCount), *weight, size=len(empty))
#         # Only Use Skin Percent to normalize! It is crappy slow to set points....
#         cmds.skinPercent( srcSkin, '{0}.vtx[0:{1}]'.format(srcMesh + "TempWeightTransfer", srcVertCount), normalize=True)
#
#         cmds.copySkinWeights( ss=srcSkin, ds=dstSkin, noMirror=True, ia="oneToOne")
#
#         destAttr = srcAttr.replace(srcDeformer, destDeformer)
#         #---Get weights from dest skin cluster
#         destWeight = cmds.getAttr("{0}.weightList[0:{1}].weights[0]".format(dstSkin, dstVertCount))
#         cmds.setAttr(destAttr, destWeight, typ='doubleArray')
#
#     cmds.delete(srcSkin, dstSkin, jointOff, jointOn, tmpMesh)



def lhDeformerWeightTransfer(srcMesh, srcDeformer, destMesh, destDeformer):
    # Get Attributes From Source
    attrs = cmds.listAttr(srcDeformer, ud = True, a = True, m=True)
    srcAttributes = ["{0}.{1}".format(srcDeformer, x) for x in attrs]

    jointOff = cmds.joint(n="JntOFF_TEMP", p=(0,0,0))
    jointOn = cmds.joint(n="JntON_TEMP", p=(0,0,0))
    tmpMesh = cmds.duplicate(srcMesh, name = srcMesh + "TempWeightTransfer")[0]

    srcSkin = cmds.skinCluster(jointOn, jointOff, tmpMesh, n = "TempSKIN", tsb=True)[0]
    cmds.setAttr(srcSkin + ".envelope", 0)
    srcVertCount = cmds.polyEvaluate(srcMesh, v=1) - 1
    dstVertCount = cmds.polyEvaluate(destMesh, v=1) - 1

    dstSkin = cmds.skinCluster(jointOn, jointOff, destMesh, n = "TempSKINDEST", tsb=True)[0]
    cmds.setAttr(dstSkin + ".envelope", 0)
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
        empty = [1.0 for x in range(srcVertCount)]



        cmds.setAttr('{0}.weightList[0:{1}].weights[0]'.format(srcSkin, srcVertCount), *weight, size=srcVertCount)
        attr = cmds.getAttr('{0}.weightList[0:{1}].weights[0]'.format(srcSkin, srcVertCount))
        print attr
        normAttrs = []
        for i in attr:
            if i < 1:
                normAttrs.append(1.0-i)
                continue
            if i == 1:
                normAttrs.append(0.0)
                continue
            if i == 0.0:
                normAttrs.append(1.0)
                continue
        try:
            cmds.setAttr('{0}.weightList[0:{1}].weights[1]'.format(srcSkin, srcVertCount), *normAttrs, size=srcVertCount)
        except:
            print "weights could not be properly transfered for " + srcAttr
        # Only Use Skin Percent to normalize! It is crappy slow to set points....
        #cmds.skinPercent( srcSkin, '{0}.vtx[0:{1}]'.format(srcMesh + "TempWeightTransfer", srcVertCount), normalize=False, prw=.01)
        cmds.skinPercent( srcSkin, '{0}.vtx[0:{1}]'.format(srcMesh + "TempWeightTransfer", srcVertCount), normalize=True)



        cmds.copySkinWeights( ss=srcSkin, ds=dstSkin, noMirror=True, ia="oneToOne")

        # print cmds.getAttr('{0}.weightList[0:{1}].weights[0]'.format(dstSkin, srcVertCount))
        # cmds.delete(srcSkin, dstSkin, jointOff, jointOn, tmpMesh)
        # return


        destAttr = srcAttr.replace(srcDeformer, destDeformer)
        #---Get weights from dest skin cluster
        destWeight = cmds.getAttr("{0}.weightList[0:{1}].weights[0]".format(dstSkin, dstVertCount))
        cmds.setAttr(destAttr, destWeight, typ='doubleArray')

    cmds.delete(srcSkin, dstSkin, jointOff, jointOn, tmpMesh)
#
# def getNodeNetwork(mayaObjList=None):
#     if not mayaObjList: selection = cmds.ls(sl=True)
#     for sel in selection:
#         attrConnectDict = getConnectedAttrs(sel)
#         if not attrConnectDict:
#             continue
#         print attrConnectDict
#
#
#
# def getConnectedAttrs(mayaObject):
#     attrs = cmds.listAttr(mayaObject, ud=True, c=True)
#     if not attrs:
#         return
#     attrConnectDict = {}
#     attrConnectDict[mayaObject] = {}
#
#     testDict = {
#         "NodeName":
#             {
#                 "srcAttrName": {
#                     "srcNodeType": "nurbs",
#                     "srcAttrType": "float",
#                     "srcAttrUserDefined": True,
#                     "srcAttr": "NodeName.UVal",
#
#                     "dstAttrName": "SLDNode",
#                     "dstType": "PMANode",
#                     "dstAttrType": "float",
#                     "dstAttrUserDefined": False,
#                     "dstAttr": "PMANode.OutputX"
#                 }
#             }
#
#     }
#
#     for a in attrs:
#         fullAttrName = "{0}.{1}".format(mayaObject, a)
#         connectionsNodes = cmds.listConnections(fullAttrName, c=True)
#         connectionsAttributes = cmds.listConnections(fullAttrName, c=True, p=True)
#         if not connectionsNodes:
#             continue
#         srcNodeType = cmds.nodeType(connectionsNodes[0])
#         dstNodeType = cmds.nodeType(connectionsNodes[1])
#
#         print "TYPE", srcNodeType
#         # src data
#         attrConnectDict[mayaObject][fullAttrName]["srcNodeType"] = srcNodeType
#         # attrConnectDict[mayaObject][fullAttrName]["srcAttrType"] = "TEMP"
#         # attrConnectDict[mayaObject][fullAttrName]["srcAttrUserDefined"] = "TEMP"
#         attrConnectDict[mayaObject][fullAttrName]["srcAttr"] = connectionsAttributes[0]
#         # dst data
#         attrConnectDict[mayaObject][fullAttrName]["dstAttrName"] = connectionsNodes[1]
#         attrConnectDict[mayaObject][fullAttrName]["dstNodeType"] = dstNodeType
#         attrConnectDict[mayaObject][fullAttrName]["dstAttrType"] = "TEMP"
#         # attrConnectDict[mayaObject][fullAttrName]["dstAttrUserDefined"] = "TEMP"
#         attrConnectDict[mayaObject][fullAttrName]["dstAttr"] = connectionsAttributes[1]
#
#
#         print attrConnectDict
#
#         return
#         #attrConnectDict[connections[0]] = (connections[1]
#
#
# def getAllAttrData():
#     {"attrName":
#
# def getAllNodeAttrValues():
#     pass
#
#


