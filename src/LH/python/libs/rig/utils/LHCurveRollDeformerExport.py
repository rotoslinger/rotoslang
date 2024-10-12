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
from rig.utils import exportUtils as xUtils
from maya import cmds
from rig.utils import LHCurveRollDeformerCmds
from .lhExport import lh_deformer_export, lh_deformer_import

class exportDeformer(lh_deformer_export):
    # ===============================================================================
    # CLASS:         export_curve_roll_deformer
    # DESCRIPTION:   exports the curve roll deformer to an external file
    # USAGE:         set args and run
    # RETURN:
    # REQUIRES:      maya.cmds
    # AUTHOR:        Levi Harrison
    # DATE:          Dec 2nd, 2014
    # Version        1.0.0
    # ===============================================================================
    ###############################################################################
    # ---Example:
    # export_curve_roll_deformer(name = "C_bLipRoll_CRD",
    #                       path = "/corp/home/lharrison/Desktop/testExport.crd")
    ###############################################################################

    def createInstanceVariables(self):

        """
        type  name:                        string
        param name:                        name of the deformer you want to
                                            export

        type  export_path:                 string
        param export_path:                 path to export to

        """

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

    def getInfo(self):
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

    def get_memberships(self):
            # get all deformed geometry and their memberships
            #get set

            self.set   = cmds.listConnections(self.name + ".message",
                                              d = True,
                                              p = True)[0].split(".")[0]
#             attr = cmds.getAttr(self.name + ".message")
            self.geo_membership = cmds.sets(self.set, q = True)

            self.geo_membership = cmds.deformer(self.name, q = True, g = True)


    def getGeoms(self):
            # get all driver geometry (for rebuilding)
        self.weight_geo = xUtils.meshData(name = self.weightGeo).mesh
        for i in range(len(self.weightBase)):
            shape = cmds.listRelatives(self.weightBase[i], shapes = True)[0]
            if (cmds.objectType(shape, isType='nurbsSurface')):
                self.base_geo.append(xUtils.nurbsSurfaceData(name = self.weightBase[i]).nurbs)
            if (cmds.objectType(shape, isType='mesh')):
                self.base_geo.append(xUtils.meshData(name = self.weightBase[i]).mesh)

        shape = cmds.listRelatives(self.inCurve, shapes = True)[0]
        self.in_curve = xUtils.nurbsCurveData(name = self.inCurve).nurbsCurve

        shape = cmds.listRelatives(self.outCurve, shapes = True)[0]
        self.out_curve = xUtils.nurbsCurveData(name = self.outCurve).nurbsCurve

#             need to write functionality for nurbs curves
    def getCurves(self):
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
        self.anim_curves = xUtils.get_anim_curve_info(anim_curve = all).curve_dict


    def pack(self):
        lh_deformer_export.pack(self)
        self.vector_dict["weight_geo"] = self.weight_geo
        self.vector_dict["anim_curves"] = self.anim_curves
        self.vector_dict["weights"] = self.weights
        self.vector_dict["geoms"] = self.geoms
        self.vector_dict["base_geo"] = self.base_geo
        self.vector_dict["in_curve"] = self.in_curve
        self.vector_dict["out_curve"] = self.out_curve
        self.vector_dict["geo_membership"] = self.geo_membership
        self.vector_dict["deformer_weights"] = self.deformer_weights
        self.vector_dict["weightGeo"] = self.weightGeo
        self.vector_dict["control"] = self.control
        self.vector_dict["lockAttrs"] = self.lockAttrs
        self.vector_dict["ihi"] = self.ihi
        self.vector_dict["side"] = self.side
        self.vector_dict["short_name"] = self.short_name
        self.vector_dict["rNames"] = self.rNames
        self.vector_dict["transferGeo"] = self.transferGeo

        # self.vector_dict = {
        #                    "weight_geo":           self.weight_geo,
        #                    "anim_curves":          self.anim_curves,
        #                    "weights":              self.weights,
        #                    "geoms":                self.geoms,
        #                    "base_geo":             self.base_geo,
        #                    "in_curve":             self.in_curve,
        #                    "out_curve":            self.out_curve,
        #                    "geo_membership":       self.geo_membership,
        #                    "deformer_weights":     self.deformer_weights,
        #                    "weightGeo":            self.weightGeo,
        #                    "control":              self.control,
        #                    "lockAttrs":            self.lockAttrs,
        #                    "ihi":                  self.ihi,
        #                    "side":                 self.side,
        #                    "short_name":           self.short_name,
        #                    "rNames":               self.rNames,
        #                    "transferGeo":          self.transferGeo,
        #                    "manipDict":            self.manipDict
        #
        # }


class importDeformer(lh_deformer_import):
    # ===============================================================================
    # CLASS:         import_curve_roll_deformer
    # DESCRIPTION:   rebuilds the curve roll deformer
    # USAGE:         set args and run
    # RETURN:
    # REQUIRES:      maya.cmds
    # AUTHOR:        Levi Harrison
    # DATE:          Dec 1st, 2014
    # Version        1.0.0
    # ===============================================================================
    ###############################################################################
    # ---Example:
    # export_curve_roll_deformer(name = "C_bLipRoll_CRD",
    #                       path = "/corp/home/lharrison/Desktop/testExport.crd")
    ###############################################################################
    ##############################################################################
    # ---Example:

    # import_curve_roll_deformer(path = "/corp/home/lharrison/Desktop/testExport.crd",
    #                             create_geo = True,
    #                             create_deformer = True,
    #                             set_weights = True,
    #                             set_curves = True)
    ##############################################################################

    def create_instance_variables(self):
        #---vars
        self.dict                    = {}
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
        # self.short_name              = ""
        self.rNames                  = {}
        self.in_curve                = ""
        self.out_curve               = ""


    def unpack(self):
        lh_deformer_import.unpack(self)
        self.weight_geo       = self.dict["weight_geo"]
        self.baseGeo          = self.dict["base_geo"]
        self.in_curve         = self.dict["in_curve"]
        self.out_curve        = self.dict["out_curve"]
        self.anim_curves      = self.dict["anim_curves"]
        self.weights          = self.dict["weights"]
        # if not self.geo_membership:
        #     self.geo_membership   = self.dict["geo_membership"]
        self.deformer_weights = self.dict["deformer_weights"]
        self.geoms            = self.dict["geoms"]
        self.control          = self.dict["control"]
        self.lockAttrs        = self.dict["lockAttrs"]
        self.ihi              = self.dict["ihi"]
        self.side             = self.dict["side"]
        if not self.short_name:
            self.short_name       = self.dict["short_name"]
        self.rNames           = self.dict["rNames"]
        self.transferGeo      = self.dict["transferGeo"]


    def createGeo(self):
        # check if geo already exists.  If so use it instead of creating new.
        if not self.create_geo:
            return
        #---create weight surface, parent if any
        if not cmds.objExists(self.weight_geo["name"]):
            self.weightGeo = xUtils.createMesh(self.weight_geo).fullPathName()
            self.weightGeo = cmds.listRelatives(self.weightGeo, parent = True)
            self.weightGeo = cmds.rename(self.weightGeo, self.weight_geo["name"])
        else:
            self.weightGeo = self.weight_geo["name"]

        #---create in_curve
        self.inCurve = xUtils.create_curve(self.in_curve).fullPathName()
        self.inCurve = cmds.listRelatives(self.inCurve, parent = True)
        self.inCurve = cmds.rename(self.inCurve, self.in_curve["name"])

        #---create out_curve
        self.outCurve = xUtils.create_curve(self.out_curve).fullPathName()
        self.outCurve = cmds.listRelatives(self.outCurve, parent = True)
        self.outCurve = cmds.rename(self.outCurve, self.out_curve["name"])


    def createDeformer(self):
        "creates deformer, turns envelope off"
        if not self.create_deformer:
            return
        self.deformer = LHCurveRollDeformerCmds.curveRollDeformerCmd(
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
        cmds.setAttr(self.deformer + ".envelope", 0)

    def createTransferDeformer(self):
        "creates deformer, turns envelope off"
        if not self.transferWeights:
            return
        self.transferDeformer = LHCurveRollDeformerCmds.curveRollDeformerCmd(
                                             weightGeo=self.weightGeo,
                                             geoms = self.transferGeo,
                                             weightBase = self.baseGeo,
                                             control = '',
                                             ihi = 1,
                                             side = self.side,
                                             name = self.short_name,
                                             inCurve = self.inCurve,
                                             outCurve = self.outCurve,
                                             rNames=self.rNames,
                                             animCurveSuffix="SRC",
                                             deformerSuffix="CRDSRC"
                                            ).returnDeformer
        cmds.setAttr(self.transferDeformer + ".envelope", 0)

    def getTransferData(self):
        self.transferSuffix = "CRD"

    def finalize(self):
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
        if self.transferDeformer:
            cmds.delete(self.transferDeformer)



