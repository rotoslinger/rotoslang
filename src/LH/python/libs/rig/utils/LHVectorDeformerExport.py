import json
from maya import cmds
from rig.utils import exportUtils as xUtils, LHVectorDeformerCmds
from rig.utils.exportUtils import set_anim_curve_data
from .lhExport import lh_deformer_export, lh_deformer_import


class exportDeformer(lh_deformer_export):
    # ===============================================================================
    # CLASS:         export_vector_deformer
    # DESCRIPTION:   exports the vector deformer to an external file
    # USAGE:         set args and run
    # RETURN:
    # REQUIRES:      maya.cmds
    # AUTHOR:        Levi Harrison
    # DATE:          Dec 1st, 2014
    # Version        1.0.0
    # ===============================================================================
    ###############################################################################
    # ---Example:
    # export_vector_deformer(name = "C_testFace_VCD",
    #                       path = "/corp/home/lharrison/Desktop/testExport.vec")
    ###############################################################################
    def createInstanceVariables(self):
        #---vars
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


    def getInfo(self):
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

    def getGeoms(self):
            # get all driver geometry (for rebuilding)
        self.weight_geo = xUtils.meshData(name = self.weightGeo).mesh
        for i in range(len(self.weightBase)):
            shape = cmds.listRelatives(self.weightBase[i], shapes = True)[0]
            if (cmds.objectType(shape, isType='nurbsSurface')):
                self.base_geo.append(xUtils.nurbsSurfaceData(name = self.weightBase[i]).nurbs)
            if (cmds.objectType(shape, isType='mesh')):
                self.base_geo.append(xUtils.meshData(name = self.weightBase[i]).mesh)

        for i in range(len(self.tPivots)):
            shape = cmds.listRelatives(self.tPivots[i], shapes = True)[0]
            self.t_pivots.append(xUtils.nurbsCurveData(name = self.tPivots[i]).nurbsCurve)

        for i in range(len(self.rPivots)):
            shape = cmds.listRelatives(self.rPivots[i], shapes = True)[0]
            self.r_pivots.append(xUtils.nurbsCurveData(name = self.rPivots[i]).nurbsCurve)
#             need to write functionality for nurbs curves
    def getCurves(self):
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
        self.anim_curves = xUtils.get_anim_curve_info(anim_curve = all).curve_dict


    def pack(self):
        lh_deformer_export.pack(self)
        self.vector_dict["weight_geo"] = self.weight_geo
        self.vector_dict["anim_curves"] = self.anim_curves
        self.vector_dict["weights"] = self.weights
        self.vector_dict["geoms"] = self.geoms
        self.vector_dict["base_geo"] = self.base_geo
        self.vector_dict["t_pivots"] = self.t_pivots
        self.vector_dict["r_pivots"] = self.r_pivots
        self.vector_dict["geo_membership"] = self.geo_membership
        self.vector_dict["deformer_weights"] = self.deformer_weights
        self.vector_dict["weightGeo"] = self.weightGeo
        self.vector_dict["control"] = self.control
        self.vector_dict["lockAttrs"] = self.lockAttrs
        self.vector_dict["ihi"] = self.ihi
        self.vector_dict["side"] = self.side
        self.vector_dict["short_name"] = self.short_name
        self.vector_dict["tNames"] = self.tNames
        self.vector_dict["rNames"] = self.rNames
        self.vector_dict["transferGeo"] = self.transferGeo
        # self.vector_dict["manipDict"] = self.manipDict
        # self.vector_dict["manipDict"] = self.manipDict
        # self.vector_dict["manipDict"] = self.manipDict
        # self.vector_dict["manipDict"] = self.manipDict
        # self.vector_dict["manipDict"] = self.manipDict

        # self.vector_dict = {
        #                    "weight_geo":           self.weight_geo,
        #                    "anim_curves":          self.anim_curves,
        #                    "weights":              self.weights,
        #                    "geoms":                self.geoms,
        #                    "base_geo":             self.base_geo,
        #                    "t_pivots":             self.t_pivots,
        #                    "r_pivots":             self.r_pivots,
        #                    "geo_membership":       self.geo_membership,
        #                    "deformer_weights":     self.deformer_weights,
        #                    "weightGeo":            self.weightGeo,
        #                    "control":              self.control,
        #                    "lockAttrs":            self.lockAttrs,
        #                    "ihi":                  self.ihi,
        #                    "side":                 self.side,
        #                    "short_name":           self.short_name,
        #                    "tNames":               self.tNames,
        #                    "rNames":               self.rNames,
        #                    "transferGeo":          self.transferGeo,
        #                    "manipDict":            self.manipDict
        #
        # }


class importDeformer(lh_deformer_import):
    # ===============================================================================
    # CLASS:         import_vector_deformer
    # DESCRIPTION:   rebuilds the slide deformer
    # USAGE:         set args and run
    # RETURN:
    # REQUIRES:      maya.cmds
    # AUTHOR:        Levi Harrison
    # DATE:          Dec 1st, 2014
    # Version        1.0.0
    # ===============================================================================
    ##############################################################################
    # ---Example:

    # import_vector_deformer(path = "/corp/home/lharrison/Desktop/testExport.vec",
    #                       create_geo = True,
    #                       create_deformer = True,
    #                       set_weights = True,
    #                       set_curves = True)
    ##############################################################################

    def create_instance_variables(self):
        #---vars
        self.dict                    = {}
        # self.geo_membership          = []
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
        self.tNames                  = {}
        self.rNames                  = {}

    def unpack(self):
        lh_deformer_import.unpack(self)
        self.weight_geo       = self.dict["weight_geo"]
        self.baseGeo          = self.dict["base_geo"]
        self.t_pivots         = self.dict["t_pivots"]
        self.r_pivots         = self.dict["r_pivots"]
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
        self.tNames           = self.dict["tNames"]
        self.rNames           = self.dict["rNames"]
        self.transferGeo      = self.dict["transferGeo"]

    def createGeo(self):
        # check if geo already exists.  If so use it instead of creating new.
        if self.create_geo == True:
            #---create weight surface, parent if any
            if not cmds.objExists(self.weight_geo["name"]):
                self.weightGeo = xUtils.createMesh(self.weight_geo).fullPathName()
                self.weightGeo = cmds.listRelatives(self.weightGeo, parent=True)
                self.weightGeo = cmds.rename(self.weightGeo, self.weight_geo["name"])
            else:
                self.weightGeo = self.weight_geo["name"]

            #---create t_pivots
            tmp_array = []
            tmp = []
            for i in range(len(self.t_pivots)):
                tmp = xUtils.create_curve(self.t_pivots[i]).fullPathName()
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
                tmp = xUtils.create_curve(self.r_pivots[i]).fullPathName()
                tmp = cmds.listRelatives(tmp, parent = True)
                tmp = cmds.rename(tmp, self.r_pivots[i]["name"])
                cmds.setAttr(tmp+".v",0)
                tmp_array.append(tmp)
            self.r_pivots = tmp_array

    def createDeformer(self):
        "creates deformer, turns envelope off"
        if not self.create_deformer:
            return
        self.deformer = LHVectorDeformerCmds.vectorDeformerCmd(
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
        cmds.setAttr(self.deformer + ".envelope", 0)

    def createTransferDeformer(self):
        "creates deformer, turns envelope off"
        if not self.transferWeights:
            return
        self.transferDeformer = LHVectorDeformerCmds.vectorDeformerCmd(
                                             weightGeo = self.weightGeo,
                                             geoms = self.transferGeo,
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
                                             animCurveSuffix="SRC",
                                             deformerSuffix="VCDSRC"
                                             ).returnDeformer
        cmds.setAttr(self.transferDeformer + ".envelope", 0)


    def getTransferData(self):
        self.transferSuffix = "VCD"


    def finalize(self):
        cmds.setAttr(self.deformer + ".envelope", 1)
        cmds.refresh(force = True)
        if self.create_deformer == True:
            if self.baseGeo:
                cmds.setAttr(self.deformer + ".useBaseGeo", 1)
            cmds.setAttr(self.deformer + ".cachePivots", 1)
            cmds.setAttr(self.deformer + ".cacheWeights", 1)
            cmds.setAttr(self.deformer + ".cacheWeightMesh", 1)
            cmds.setAttr(self.deformer + ".cacheWeightCurves", 1)
        if self.transferDeformer:
            cmds.delete(self.transferDeformer)

