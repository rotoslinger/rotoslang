import json
import time

from rig.utils import exportUtils as xUtils, LHSlideDeformerCmds
import importlib
importlib.reload(xUtils)
from rig.utils.exportUtils import set_anim_curve_data, lhDeformerWeightTransfer
from maya import cmds
from .lhExport import lh_deformer_export, lh_deformer_import


class exportDeformer(lh_deformer_export):
    # ===============================================================================
    # CLASS:         export_slide_deformer
    # DESCRIPTION:   gets all information about the slide deformer
    # USAGE:         set args and run
    # RETURN:
    # REQUIRES:      maya.cmds
    # AUTHOR:        Levi Harrison
    # DATE:          Nov 10th, 2014
    # Version        1.0.0
    # ===============================================================================
    ##############################################################################
    # ---Example:
    # export_slide_deformer(name = "C_mouth_SLD",
    #                       path = "/corp/home/lharrison/Desktop/testExport.sld")
    # print something["driver_surface"]["name"]

    ##############################################################################

    def createInstanceVariables(self):
        # ---vars
        self.geo_membership = []
        self.driver_surface = {}
        self.weight_geo = {}
        self.base_geo = []
        self.transferGeo = []
        self.anim_curves = {}
        self.deformer_weights = {}
        self.weights = {}
        self.vector_dict = {}
        # naming information for rebuilding
        self.driverSurface = ""
        self.geoms = []
        self.weightGeo = ""
        self.weightBase = []
        self.transferGeo = []
        self.control = ""
        self.lockAttrs = []
        self.ihi = None
        self.side = ""
        self.short_name = ""
        self.uNames = []
        self.vNames = []
        self.nNames = []
        self.uUseAnimCurves = []
        self.vUseAnimCurves = []
        self.nUseAnimCurves = []

    def getInfo(self):
        # get all info from the deformer
        # get all attribute names
        # from attr names you will know curve and weight names
        self.driverSurface = cmds.listConnections(self.name + ".surface",
                                                  d=False)[0]
        #         self.geoms = cmds.deformer(self.name, q = True,g = True)
        self.weightGeo = cmds.listConnections(self.name + ".weightPatch",
                                              d=False)[0]

        self.weightBase = cmds.listConnections(self.name + ".baseGeoArray",
                                               d=False)
        # ---Will be a copy of the geometries where weights will be stored
        self.transferGeo = cmds.deformer(self.name, q=True, g=True)

        self.side = self.name.split("_")[0]
        self.short_name = self.name.split("_")[1]
        self.uNames = cmds.listConnections(self.name + ".uValueParentArray",
                                           d=True,
                                           p=True)
        if self.uNames:
            for i in range(len(self.uNames)):
                self.uNames[i] = self.uNames[i].split(".")[1]

        self.vNames = cmds.listConnections(self.name + ".vValueParentArray",
                                           d=True,
                                           p=True)

        if self.vNames:
            for i in range(len(self.vNames)):
                self.vNames[i] = self.vNames[i].split(".")[1]
        self.nNames = cmds.listConnections(self.name + ".nValueParentArray",
                                           d=True,
                                           p=True)
        if self.nNames:
            for i in range(len(self.nNames)):
                self.nNames[i] = self.nNames[i].split(".")[1]

        self.uUseAnimCurves = [1]
        self.vUseAnimCurves = [1]
        self.nUseAnimCurves = [1]

    def getGeoms(self):
        # get all driver geometry (for rebuilding)
        self.driver_surface = xUtils.nurbsSurfaceData(name=self.driverSurface).nurbs
        self.weight_geo = xUtils.meshData(name=self.weightGeo).mesh
        if not self.weightBase:
            self.weightBase = cmds.listConnections(self.name + ".baseGeoArray", d=False)
        for i in range(len(self.weightBase)):
            shape = cmds.listRelatives(self.weightBase[i], shapes=True)[0]
            if (cmds.objectType(shape, isType='nurbsSurface')):
                self.base_geo.append(xUtils.nurbsSurfaceData(name=self.weightBase[i]).nurbs)
            if (cmds.objectType(shape, isType='mesh')):
                self.base_geo.append(xUtils.meshData(name=self.weightBase[i]).mesh)

    def getCurves(self):
        # get all curve infos
        self.connections = []
        self.connections.append(cmds.listConnections(self.name + ".uuaca",
                                                     type="animCurve",
                                                     d=False))
        self.connections.append(cmds.listConnections(self.name + ".uvaca",
                                                     type="animCurve",
                                                     d=False))
        self.connections.append(cmds.listConnections(self.name + ".uva",
                                                     type="animCurve",
                                                     d=False))
        self.connections.append(cmds.listConnections(self.name + ".uwpa",
                                                     type="animCurve",
                                                     d=False))
        self.connections.append(cmds.listConnections(self.name + ".vuaca",
                                                     type="animCurve",
                                                     d=False))
        self.connections.append(cmds.listConnections(self.name + ".vvaca",
                                                     type="animCurve",
                                                     d=False))
        self.connections.append(cmds.listConnections(self.name + ".vva",
                                                     type="animCurve",
                                                     d=False))
        self.connections.append(cmds.listConnections(self.name + ".vwpa",
                                                     type="animCurve",
                                                     d=False))
        flat_conn = []
        for i in range(len(self.connections)):
            if self.connections[i]:
                for j in range(len(self.connections[i])):
                    if self.connections[i][j]:
                        flat_conn.append(self.connections[i][j])
        all = flat_conn
        self.anim_curves = xUtils.get_anim_curve_info(anim_curve=all).curve_dict


    def pack(self):
        lh_deformer_export.pack(self)
        self.vector_dict["driver_surface"] = self.driver_surface
        self.vector_dict["weight_geo"] = self.weight_geo
        self.vector_dict["anim_curves"] = self.anim_curves
        self.vector_dict["weights"] = self.weights
        self.vector_dict["geoms"] = self.geoms
        self.vector_dict["base_geo"] = self.base_geo
        self.vector_dict["transferGeo"] = self.transferGeo
        self.vector_dict["geo_membership"] = self.geo_membership
        self.vector_dict["deformer_weights"] = self.deformer_weights
        self.vector_dict["weightGeo"] = self.weightGeo
        self.vector_dict["control"] = self.control
        self.vector_dict["lockAttrs"] = self.lockAttrs
        self.vector_dict["ihi"] = self.ihi
        self.vector_dict["side"] = self.side
        self.vector_dict["short_name"] = self.short_name
        self.vector_dict["uNames"] = self.uNames
        self.vector_dict["vNames"] = self.vNames
        self.vector_dict["nNames"] = self.nNames
        self.vector_dict["uUseAnimCurves"] = self.uUseAnimCurves
        self.vector_dict["vUseAnimCurves"] = self.vUseAnimCurves
        self.vector_dict["nUseAnimCurves"] = self.nUseAnimCurves

        # "weight_geo": self.weight_geo,
        #     "anim_curves": self.anim_curves,
        #     "weights": self.weights,
        #     "driverSurface": self.driverSurface,
        #     "geoms": self.geoms,
        #     "base_geo": self.base_geo,
        #     "transferGeo": self.transferGeo,
        #     "geo_membership": self.geo_membership,
        #     "deformer_weights": self.deformer_weights,
        #     "weightGeo": self.weightGeo,
        #     "control": self.control,
        #     "lockAttrs": self.lockAttrs,
        #     "ihi": self.ihi,
        #     "side": self.side,
        #     "short_name": self.short_name,
        #     "uNames": self.uNames,
        #     "vNames": self.vNames,
        #     "nNames": self.nNames,
        #     "uUseAnimCurves": self.uUseAnimCurves,
        #     "vUseAnimCurves": self.vUseAnimCurves,
        #     "nUseAnimCurves": self.nUseAnimCurves,
        # }




class importDeformer(lh_deformer_import):
    # ===============================================================================
    # CLASS:         import_slide_deformer
    # DESCRIPTION:   rebuilds the slide deformer
    # USAGE:         set args and run
    # RETURN:
    # REQUIRES:      maya.cmds
    # AUTHOR:        Levi Harrison
    # DATE:          Nov 11th, 2014
    # Version        1.0.0
    # ===============================================================================
    ##############################################################################
    # ---Example:

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

    def create_instance_variables(self):
        #---vars
        self.dict                    = {}
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
        # self.short_name              = ""
        self.uNames                  = []
        self.vNames                  = []
        self.nNames                  = []
        self.uUseAnimCurves          = []
        self.vUseAnimCurves          = []
        self.nUseAnimCurves          = []

    def unpack(self):
        lh_deformer_import.unpack(self)
        self.driver_surface   = self.dict["driver_surface"]
        self.weight_geo       = self.dict["weight_geo"]
        self.baseGeo          = self.dict["base_geo"]
        self.transferGeo      = self.dict["transferGeo"]
        self.anim_curves      = self.dict["anim_curves"]
        self.weights          = self.dict["weights"]
        # self.driverSurface    = self.dict["driverSurface"]
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
        self.uNames           = self.dict["uNames"]
        self.vNames           = self.dict["vNames"]
        self.nNames           = self.dict["nNames"]
        self.uUseAnimCurves   = self.dict["uUseAnimCurves"]
        self.vUseAnimCurves   = self.dict["vUseAnimCurves"]
        self.nUseAnimCurves   = self.dict["nUseAnimCurves"]


    def createGeo(self):
        if not self.create_geo:
            return
        #---create driver surface, parent if any
        self.driverSurface = xUtils.createNurbsSurface(self.driver_surface).fullPathName()
        self.driverSurface = cmds.listRelatives(self.driverSurface, parent = True)
        self.driverSurface = cmds.rename(self.driverSurface, self.driver_surface["name"])
        cmds.setAttr(self.driverSurface + ".v", 0)
        #---create weight surface, parent if any
        if not cmds.objExists(self.weight_geo["name"]):
            self.weightGeo = xUtils.createMesh(self.weight_geo).fullPathName()
            self.weightGeo = cmds.listRelatives(self.weightGeo, parent = True)
            self.weightGeo = cmds.rename(self.weightGeo, self.weight_geo["name"])
        else:
            self.weightGeo = self.weight_geo["name"]
        cmds.setAttr(self.weightGeo + ".v", 0)


    def createTransferGeo(self):
        if not self.transfer:
            return
        tmp_transferGeo = []
        tmp = []
        for i in range(len(self.transferGeo)):
            if not cmds.objExists(self.transferGeo[i]["name"]):
                tmp = xUtils.createMesh(self.transferGeo[i]).fullPathName()
                tmp = cmds.listRelatives(tmp, parent = True)
                tmp = cmds.rename(tmp, self.transferGeo[i]["name"])
                cmds.setAttr(tmp+".v",0)
                tmp_transferGeo.append(tmp)
            else:
                tmp_transferGeo.append(self.transferGeo[i]["name"])
        self.transferGeo = tmp_transferGeo

    def createDeformer(self):
        "creates deformer, turns envelope off"
        if not self.create_deformer:
            return
        self.deformer = LHSlideDeformerCmds.slideDeformerCmd(
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
        # cmds.setAttr(self.deformer + ".cacheWeights", 0)
        # cmds.setAttr(self.deformer + ".cacheParams", 0)
        # cmds.setAttr(self.deformer + ".cacheWeightMesh", 0)
        # cmds.setAttr(self.deformer + ".cacheWeightCurves", 0)
        # cmds.setAttr(self.deformer + ".cacheBase", 0)
        # cmds.refresh(force=True)

        # print("initializing points")
        # cmds.refresh()
        # time.sleep(1.0)

    def createTransferDeformer(self):
        if not self.transferWeights:
            return
        self.transferDeformer = LHSlideDeformerCmds.slideDeformerCmd(
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
        # cmds.setAttr(self.transferDeformer + ".cacheWeights", 0)
        # cmds.setAttr(self.transferDeformer + ".cacheParams", 0)
        # cmds.setAttr(self.transferDeformer + ".cacheWeightMesh", 0)
        # cmds.setAttr(self.transferDeformer + ".cacheWeightCurves", 0)
        # cmds.setAttr(self.transferDeformer + ".cacheBase", 0)
        # cmds.refresh(force=True)
        # print("initializing points")
        # cmds.refresh()
        # time.sleep(1.0)

    def getTransferData(self):
        self.transferSuffix = "SLD"

    # def transfer(self):
    #     if not self.transferWeights:
    #         return
    #     for i in range(len(self.transferGeo)):
    #         lhDeformerWeightTransfer(self.transferGeo[i], self.transferDeformer, self.geo_membership[i], self.deformer)

    def finalize(self):
        if not self.create_deformer:
            return
        cmds.setAttr(self.deformer + ".envelope", 1)
        cmds.refresh(force=True)
        cmds.setAttr(self.deformer + ".cacheWeights", 1)
        cmds.setAttr(self.deformer + ".cacheParams", 1)
        cmds.setAttr(self.deformer + ".cacheWeightMesh", 1)
        cmds.setAttr(self.deformer + ".cacheWeightCurves", 1)
        cmds.setAttr(self.deformer + ".cacheBase", 1)
        if self.transferDeformer:
            cmds.delete(self.transferDeformer)
