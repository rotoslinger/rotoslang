from maya import cmds, OpenMaya, OpenMayaAnim


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
        type  name:                        string
        param name:                        name of the deformer you want to
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
        self.get_nurbs()

    def check(self):
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

    def get_cvs(self):
        points = OpenMaya.MPointArray()
        self.fn_nurbs.getCVs(points, OpenMaya.MSpace.kWorld)
        for i in range(points.length()):
            self.controlVertices.append((points[i].x,
                                         points[i].y,
                                         points[i].z))

    def get_knot_sequences(self):
        u_knots = OpenMaya.MDoubleArray()
        v_knots = OpenMaya.MDoubleArray()
        self.fn_nurbs.getKnotsInU(u_knots)
        self.fn_nurbs.getKnotsInV(v_knots)
        self.uKnotSequences = [i for i in u_knots]
        self.vKnotSequences = [i for i in v_knots]

    def get_degrees(self):
        self.degreeInU = self.fn_nurbs.degreeU()
        self.degreeInV = self.fn_nurbs.degreeV()

    def get_forms(self):
        self.form = self.fn_nurbs.formInU()
        self.formV = self.fn_nurbs.formInV()

    def write_dict(self):
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

    def get_nurbs(self):
        self.check()
        self.get_cvs()
        self.get_knot_sequences()
        self.get_degrees()
        self.get_forms()
        self.write_dict()


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