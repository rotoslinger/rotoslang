# import sys
#
# from utils.exportUtils import set_anim_curves, lhDeformerWeightTransfer
#
# linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
# mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"
# #---determine operating system
# os = sys.platform
# if "linux" in os:
#     os = linux
# if "darwin" in os:
#     os = mac
# if os not in sys.path:
#     sys.path.append(os)
#
# from utils import exportUtils as xUtils
# from maya import cmds
# import json
# from utils import slideDeformerCmds, vectorDeformerCmds, LHCurveRollDeformerCmds
# reload(slideDeformerCmds)
# reload(vectorDeformerCmds)
# reload(LHCurveRollDeformerCmds)
#
#
# class export_slide_deformer():
#     # ===============================================================================
#     # CLASS:         export_slide_deformer
#     # DESCRIPTION:   gets all information about the slide deformer
#     # USAGE:         set args and run
#     # RETURN:
#     # REQUIRES:      maya.cmds
#     # AUTHOR:        Levi Harrison
#     # DATE:          Nov 10th, 2014
#     # Version        1.0.0
#     # ===============================================================================
#     ##############################################################################
#     # ---Example:
#     # export_slide_deformer(name = "C_mouth_SLD",
#     #                       path = "/corp/home/lharrison/Desktop/testExport.sld")
#     # print something["driver_surface"]["name"]
#
#     ##############################################################################
#
#     def __init__(self,
#                  name = "",
#                  path = "",
#                  ):
#
#         """
#         type  name:                        string
#         param name:                        name of the deformer you want to
#                                             export
#
#         type  export_path:                 string
#         param export_path:                 path to export to
#
#         """
#
#         #---args
#         self.name                           = name
#         self.path                           = path
#         #---vars
#         self.geo_membership                 = []
#         self.driver_surface                 = {}
#         self.weight_geo                     = {}
#         self.base_geo                       = []
#         self.transferGeo                   = []
#         self.anim_curves                    = {}
#         self.deformer_weights               = {}
#         self.weights                        = {}
#         self.vector_dict                     = {}
#         # naming information for rebuilding
#         self.driverSurface           = ""
#         self.geoms                   = []
#         self.weightGeo               = ""
#         self.weightBase              = []
#         self.transferGeo             = []
#         self.control                 = ""
#         self.lockAttrs               = []
#         self.ihi                     = None
#         self.side                    = ""
#         self.short_name              = ""
#         self.uNames                  = []
#         self.vNames                  = []
#         self.nNames                  = []
#         self.uUseAnimCurves          = []
#         self.vUseAnimCurves          = []
#         self.nUseAnimCurves          = []
#
#
#         self.__create()
#
#     def __check(self):
#         if not cmds.objExists(self.name):
#             raise Exception(self.name + " does not exist")
#             quit()
#     def __get_info(self):
#             # get all info from the deformer
#             # get all attribute names
#             # from attr names you will know curve and weight names
#         self.driverSurface = cmds.listConnections(self.name + ".surface",
#                                                   d = False)[0]
# #         self.geoms = cmds.deformer(self.name, q = True,g = True)
#         self.weightGeo = cmds.listConnections(self.name + ".weightPatch",
#                                               d = False)[0]
#
#         self.weightBase = cmds.listConnections(self.name + ".baseGeoArray",
#                                               d = False)
#         #---Will be a copy of the geometries where weights will be stored
#         self.transferGeo = cmds.deformer(self.name, q = True, g = True)
#
#         self.side = self.name.split("_")[0]
#         self.short_name = self.name.split("_")[1]
#         self.uNames = cmds.listConnections(self.name + ".uValueParentArray",
#                                            d = True,
#                                            p = True)
#         if self.uNames:
#             for i in range(len(self.uNames)):
#                 self.uNames[i] = self.uNames[i].split(".")[1]
#
#         self.vNames  = cmds.listConnections(self.name + ".vValueParentArray",
#                                                 d = True,
#                                                 p = True)
#
#         if self.vNames:
#             for i in range(len(self.vNames)):
#                 self.vNames[i] = self.vNames[i].split(".")[1]
#         self.nNames   = cmds.listConnections(self.name + ".nValueParentArray",
#                                              d = True,
#                                              p = True)
#         if self.nNames:
#             for i in range(len(self.nNames)):
#                 self.nNames[i] = self.nNames[i].split(".")[1]
#
#         self.uUseAnimCurves          = [1]
#         self.vUseAnimCurves          = [1]
#         self.nUseAnimCurves          = [1]
#
#     def __get_memberships(self):
#             # get all deformed geometry and their memberships
#             #get set
#             self.set   = cmds.listConnections(self.name + ".message",
#                                               d = True,
#                                               p = True)[0].split(".")[0]
# #             attr = cmds.getAttr(self.name + ".message")
#             self.geo_membership = cmds.sets(self.set, q = True)
#             self.geo_membership = cmds.deformer(self.name, q = True, g = True)
#
#     def __get_geoms(self):
#             # get all driver geometry (for rebuilding)
#         self.driver_surface = xUtils.return_nurbs_surface_info(name = self.driverSurface).nurbs
#         self.weight_geo = xUtils.return_mesh_info(name = self.weightGeo).mesh
#         if not self.weightBase:
#             self.weightBase = cmds.listConnections(self.name + ".baseGeoArray", d = False)
#         for i in range(len(self.weightBase)):
#             shape = cmds.listRelatives(self.weightBase[i], shapes = True)[0]
#             if (cmds.objectType(shape, isType='nurbsSurface')):
#                 self.base_geo.append(xUtils.return_nurbs_surface_info(name = self.weightBase[i]).nurbs)
#             if (cmds.objectType(shape, isType='mesh')):
#                 self.base_geo.append(xUtils.return_mesh_info(name = self.weightBase[i]).mesh)
#
#         #---Exporting the transfer geo means finding a non deformed copy of the mesh and storing it.
#         #---The base geo is the only geo that is garanteed to not be deformed.
#         self.transferGeo = []
#         tmpTransferGeo = []
#         for geo in cmds.listConnections(self.name + ".baseGeoArray", d = False):
#             tmpTransferGeo.append(cmds.duplicate(geo, n= geo.replace("Base","Transfer"))[0])
#         for i in range(len(tmpTransferGeo)):
#             shape = cmds.listRelatives(tmpTransferGeo[i], shapes = True)[0]
#             if (cmds.objectType(shape, isType='nurbsSurface')):
#                 transferGeo = xUtils.return_nurbs_surface_info(name = tmpTransferGeo[i]).nurbs
#                 self.transferGeo.append(transferGeo)
#
#             if (cmds.objectType(shape, isType='mesh')):
#                 transferGeo = xUtils.return_mesh_info(name = tmpTransferGeo[i]).mesh
#                 self.transferGeo.append(transferGeo)
#         cmds.delete(tmpTransferGeo)
#
#     def __get_curves(self):
#             # get all curve infos
#         self.connections = []
#         self.connections.append(cmds.listConnections(self.name + ".uuaca",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".uvaca",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".uva",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".uwpa",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".vuaca",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".vvaca",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".vva",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".vwpa",
#                                                      type = "animCurve",
#                                                      d = False))
#         flat_conn = []
#         for i in range(len(self.connections)):
#             if self.connections[i]:
#                 for j in range(len(self.connections[i])):
#                     if self.connections[i][j]:
#                         flat_conn.append(self.connections[i][j])
#         all = flat_conn
#         self.anim_curves = xUtils.get_anim_curve_info(anim_curve = all).curve_dict
#     def __get_weights(self):
#             # get all double array weights
#             tmp_weight_names = cmds.listAttr(self.name,
#                                              ud = True,
#                                              a = True)
#             tmp_values = []
#             tmp_names = []
#             geoms = cmds.deformer(self.name, q = True,g = True)
#             for i in range(len(tmp_weight_names)):
#                 for j in range(len(geoms)):
#                     split_weights = tmp_weight_names[i].split(".")
#                     tmp_names.append(self.name
#                                      + "."
#                                      + split_weights[0]
#                                      +"[" + str(j)
#                                      + "]."
#                                      + split_weights[1])
#                     tmp_values.append(cmds.getAttr(self.name
#                                                    + "."
#                                                    + split_weights[0]
#                                                    +"[" + str(j)
#                                                    + "]."
#                                                    + split_weights[1]))
#             self.weights = dict(zip(tmp_names,tmp_values))
#             # get deformer weights
#             tmp_def_weights = []
#             tmp_def_names   = []
#             tmp_flat_weights= []
#             tmp_flat_names= []
#             try:
#                 for i in range(len(geoms)):
#                     tmp_def_names = self.name + ".weightList[" + str(i) + "].weights"
#                     indices = cmds.getAttr(tmp_def_names, mi = True)
#     #                     tmp_def_weights = cmds.getAttr(tmp_def_names)
#     #                     print tmp_def_weights
#                     for j in range(len(indices)):
#                         tmp_flat_names.append(self.name
#                                               + ".weightList["
#                                               + str(i)
#                                               + "].weights["
#                                               + str(indices[j])
#                                               + "]")
#                         tmp_flat_weights.append(cmds.getAttr(tmp_flat_names[j]))
#     #                     print tmp_flat_weights[j]
#     #                         print cmds.getAttr(tmp_flat_names[j])
#     #                         print tmp_flat_weights[j], j, tmp_flat_names[j],tmp_def_weights[0][j]
#                 for i in range(len(tmp_flat_names)):
#                     self.deformer_weights[tmp_flat_names[i]] = tmp_flat_weights[i]
#             except:
#                 pass
# #             print self.deformer_weights
#     def __organize(self):
# #         print self.base_geo
#
#         self.vector_dict = {
#                            "driver_surface":       self.driver_surface,
#                            "weight_geo":           self.weight_geo,
#                            "anim_curves":          self.anim_curves,
#                            "weights":              self.weights,
#                            "driverSurface":        self.driverSurface,
#                            "geoms":                self.geoms,
#                            "base_geo":             self.base_geo,
#                            "transferGeo":         self.transferGeo,
#                            "geo_membership":       self.geo_membership,
#                            "deformer_weights":     self.deformer_weights,
#                            "weightGeo":            self.weightGeo,
#                            "control":              self.control,
#                            "lockAttrs":            self.lockAttrs,
#                            "ihi":                  self.ihi,
#                            "side":                 self.side,
#                            "short_name":           self.short_name,
#                            "uNames":               self.uNames,
#                            "vNames":               self.vNames,
#                            "nNames":               self.nNames,
#                            "uUseAnimCurves":       self.uUseAnimCurves,
#                            "vUseAnimCurves":       self.vUseAnimCurves,
#                            "nUseAnimCurves":       self.nUseAnimCurves,
#                            }
#     def __export(self):
#         file = open(self.path, "wb")
#         json.dump(self.vector_dict, file, sort_keys = False, indent = 2)
#         file.close()
#
#             # format info
#             # export info to a file
#     def __create(self):
#         self.__check()
#         self.__get_info()
#         self.__get_memberships()
#         self.__get_geoms()
#         self.__get_curves()
#         self.__get_weights()
#         self.__organize()
#         self.__export()
#
#
#
#
#
# class import_slide_deformer():
#     # ===============================================================================
#     # CLASS:         import_slide_deformer
#     # DESCRIPTION:   rebuilds the slide deformer
#     # USAGE:         set args and run
#     # RETURN:
#     # REQUIRES:      maya.cmds
#     # AUTHOR:        Levi Harrison
#     # DATE:          Nov 11th, 2014
#     # Version        1.0.0
#     # ===============================================================================
#     ##############################################################################
#     # ---Example:
#
#     # export_slide_deformer(name = "C_mouth_SLD",
#     #                       path = "/corp/home/lharrison/Desktop/testExport.sld")
#
#     # import_slide_deformer(path = "/corp/home/lharrison/Desktop/testExport.sld",
#     #                       create_geo = True,
#     #                       create_deformer = True,
#     #                       set_weights = True,
#     #                       set_curves = True)
#     #
#     # import_slide_deformer(path = "/corp/home/lharrison/Desktop/lips.sld",
#     #                       create_geo = False,
#     #                       create_deformer = False,
#     #                       set_weights = True,
#     #                       set_curves = True)
#     ##############################################################################
#
#     def __init__(self,
#                  path = "",
#                  create_geo = True,
#                  create_deformer = True,
#                  set_weights = True,
#                  set_curves = True,
#                  transfer = False
#                  ):
#
#         """
#         type  path:                 string
#         param path:                 path to import from
#         """
#
#         #---args
#         self.path                    = path
#         self.create_geo              = create_geo
#         self.create_deformer         = create_deformer
#         self.set_weights             = set_weights
#         self.set_curves              = set_curves
#         self.transfer                = transfer
#         #---vars
#         self.dict                    = {}
#         self.geo_membership          = []
#         self.driver_surface          = {}
#         self.weight_geo              = {}
#         self.anim_curves             = {}
#         self.weights                 = {}
#         self.deformer_weights        = {}
#         self.baseGeo                 = []
#         self.transferGeo             = []
#         self.driverSurface           = ""
#         self.geoms                   = []
#         self.control                 = ""
#         self.lockAttrs               = []
#         self.ihi                     = None
#         self.side                    = ""
#         self.short_name              = ""
#         self.uNames                  = []
#         self.vNames                  = []
#         self.nNames                  = []
#         self.uUseAnimCurves          = []
#         self.vUseAnimCurves          = []
#         self.nUseAnimCurves          = []
#
#         self.__create()
#
#     def __unpack(self):
#         "imports the dictionary, separates all of the info for later use"
#         file = open(self.path, "rb")
#         self.dict = json.load(file)
#         file.close()
#
#         self.driver_surface   = self.dict["driver_surface"]
#         self.weight_geo       = self.dict["weight_geo"]
#         self.baseGeo          = self.dict["base_geo"]
#         self.transferGeo      = self.dict["transferGeo"]
#         self.anim_curves      = self.dict["anim_curves"]
#         self.weights          = self.dict["weights"]
#         self.driverSurface    = self.dict["driverSurface"]
#         self.geo_membership   = self.dict["geo_membership"]
#         self.deformer_weights = self.dict["deformer_weights"]
#         self.geoms            = self.dict["geoms"]
#         self.control          = self.dict["control"]
#         self.lockAttrs        = self.dict["lockAttrs"]
#         self.ihi              = self.dict["ihi"]
#         self.side             = self.dict["side"]
#         self.short_name       = self.dict["short_name"]
#         self.uNames           = self.dict["uNames"]
#         self.vNames           = self.dict["vNames"]
#         self.nNames           = self.dict["nNames"]
#         self.uUseAnimCurves   = self.dict["uUseAnimCurves"]
#         self.vUseAnimCurves   = self.dict["vUseAnimCurves"]
#         self.nUseAnimCurves   = self.dict["nUseAnimCurves"]
#     def __create_geo(self):
#         if self.create_geo == True:
#             #---create driver surface, parent if any
#             self.driverSurface = xUtils.create_nurbs_surface(self.driver_surface).fullPathName()
#             self.driverSurface = cmds.listRelatives(self.driverSurface, parent = True)
#             self.driverSurface = cmds.rename(self.driverSurface, self.driver_surface["name"])
#             #---create weight surface, parent if any
#             if not cmds.objExists(self.weight_geo["name"]):
#                 self.weightGeo = xUtils.create_mesh(self.weight_geo).fullPathName()
#                 self.weightGeo = cmds.listRelatives(self.weightGeo, parent = True)
#                 self.weightGeo = cmds.rename(self.weightGeo, self.weight_geo["name"])
#             else:
#                 self.weightGeo = self.weight_geo["name"]
#             #---create base geo, parent if any
#             tmp_baseGeo = []
#             tmp = []
# #             for i in range(len(self.baseGeo)):
# #                 if not cmds.objExists(self.baseGeo[i]["name"]):
# #                     tmp = xUtils.create_mesh(self.baseGeo[i]).fullPathName()
# #                     tmp = cmds.listRelatives(tmp, parent = True)
# #                     tmp = cmds.rename(tmp, self.baseGeo[i]["name"])
# #                     cmds.setAttr(tmp+".v",0)
# #                     tmp_baseGeo.append(tmp)
# #                 else:
# #                     tmp_baseGeo.append(self.baseGeo[i]["name"])
# #             self.baseGeo = tmp_baseGeo
# #             #---Test to see whether or not the geo_membership and the base geo have the same number of points
# #             #---If geo_membership and base do not line up, copy the geo_membership, to create the base.
# #             if (len(self.geo_membership) != len(self.baseGeo)):
# #                 self.__createBase()
# #                 return
# #             for i in range(len(self.geo_membership)):
# #                 if not comparePolyCount(self.geo_membership[i], self.baseGeo[i]):
# #                     self.__createBase()
# #                     return
#             self.__createBase()
#
#             #---create transfer geo, parent if any
#             print self.baseGeo
#             tmp_transferGeo = []
#             tmp = []
#             for i in range(len(self.transferGeo)):
#                 if not cmds.objExists(self.transferGeo[i]["name"]):
#                     print "creating Transfer Geo"
#                     tmp = xUtils.create_mesh(self.transferGeo[i]).fullPathName()
#                     tmp = cmds.listRelatives(tmp, parent = True)
#                     tmp = cmds.rename(tmp, self.transferGeo[i]["name"])
#                     cmds.setAttr(tmp+".v",0)
#                     tmp_transferGeo.append(tmp)
#                 else:
#                     tmp_transferGeo.append(self.transferGeo[i]["name"])
#             self.transferGeo = tmp_transferGeo
#
#     def __createBase(self):
#         """Creates base"""
#         self.baseGeo = []
#         for i in self.geo_membership:
#             tmp = cmds.duplicate(i, name = i + "Base")[0]
#             cmds.setAttr(tmp+".v",0)
#             self.baseGeo.append(tmp)
#
#     def __create_deformer(self):
#         "creates deformer, turns envelope off"
#         #---If doesn't find geo_membership, attempts to apply to selected geo
#         if not self.geo_membership:
#             self.geo_membership = cmds.ls(sl=True)
#         if self.create_deformer == True:
#             self.deformer = slideDeformerCmds.slideDeformerCmd(
#                                                  driverSurface = self.driverSurface,
#                                                  weightGeo = self.weightGeo,
#                                                  geoms = self.geo_membership,
#                                                  weightBase = self.baseGeo,
#                                                  control = '',
#                                                  ihi = 1,
#                                                  side = self.side,
#                                                  name = self.short_name,
#                                                  #---Mouth
#                                                  uNames = self.uNames,
#                                                  vNames = self.vNames,
#                                                  nNames = self.nNames,
#                                                  ).returnDeformer
#             cmds.setAttr(self.deformer + ".envelope", 0)
#         self.transferDeformer = slideDeformerCmds.slideDeformerCmd(
#                                              driverSurface = self.driverSurface,
#                                              weightGeo = self.weightGeo,
#                                              geoms = self.transferGeo,
#                                              control = '',
#                                              ihi = 1,
#                                              side = self.side,
#                                              name = self.short_name,
#                                              #---Mouth
#                                              uNames = self.uNames,
#                                              vNames = self.vNames,
#                                              nNames = self.nNames,
#                                              animCurveSuffix = "SRC",
#                                              deformerSuffix = "SLDSRC"
#                                              ).returnDeformer
#         cmds.setAttr(self.transferDeformer + ".envelope", 0)
#
#     def __set_anim_curves(self):
#         if self.set_curves == True:
#             for i in range(len(self.anim_curves)):
#                 anim_curves = self.anim_curves[str(i)]["name"]
#                 frame_values = self.anim_curves[str(i)]["frame_values"]
#                 frame_times= self.anim_curves[str(i)]["frame_times"]
#                 in_x_tangents= self.anim_curves[str(i)]["in_x_tangents"]
#                 in_y_tangents= self.anim_curves[str(i)]["in_y_tangents"]
#                 out_x_tangents= self.anim_curves[str(i)]["out_x_tangents"]
#                 out_y_tangents= self.anim_curves[str(i)]["out_y_tangents"]
#                 in_tangents_type= self.anim_curves[str(i)]["in_tangents_type"]
#                 out_tangents_type= self.anim_curves[str(i)]["out_tangents_type"]
#                 set_anim_curves(anim_curves,
#                                 frame_values,
#                                 frame_times,
#                                 in_x_tangents,
#                                 in_y_tangents,
#                                 out_x_tangents,
#                                 out_y_tangents,
#                                 in_tangents_type,
#                                 out_tangents_type)
#
#     def __set_weights(self):
#         "sets deformer weight, then sets double array weights"
#         if self.set_weights == True:
#             #---Double Check that the geo in the scene is the same as the geo from the dictionary
#             #---If not, don't set weights, maya could crash
# #             for i in range(len(self.geo_membership)):
# #                 if not comparePolyCount(self.geo_membership[i], self.transferGeo[i]):
# #                     print "Points do not match, weights will be transfered, not set"
# #                     return
#
#             if self.deformer_weights:
#                 for i in self.deformer_weights.keys():
#                     cmds.setAttr(i, self.deformer_weights.get(i))
#             #ToFixOldDeformers
#             for i in self.weights.keys():
#                 weights = self.weights.get(i)
# #                 newName = i
# #                 if "LRU" in i:
# #                     newName = i.replace("LRU", "LR")
# #                 if "LRV" in i:
# #                     newName = i.replace("LRV", "LR")
# #                 if "UDU" in i:
# #                     newName = i.replace("UDU", "UD")
# #                 if "UDV" in i:
# #                     newName = i.replace("UDV", "UD")
# #                 if "SideU" in i:
# #                     newName = i.replace("SideU", "Side")
# #                 if "SideV" in i:
# #                     newName = i.replace("SideV", "Side")
# #                 cmds.setAttr(newName, weights,typ='doubleArray')
#                 if not weights:
#                     continue
#                 try:
#                     cmds.setAttr(i, weights,typ='doubleArray')
#                 except:
#                     print "Weights for " + i + " unable to be set.  It is likely topology has changed."
# #         #---Set Transfer weights
#         for i in self.weights.keys():
#             weights = self.weights.get(i)
#             if not weights:
#                 continue
#             transferAttr = i.replace("_SLD", "_SLDSRC")
#             try:
#                 cmds.setAttr(transferAttr, weights,typ='doubleArray')
#             except:
#                 print "Weights for " + i + " unable to be set."
#
#     def __transfer(self):
#         if self.transfer:
#             for i in range(len(self.transferGeo)):
#                 lhDeformerWeightTransfer(self.transferGeo[i], self.transferDeformer, self.geo_membership[i], self.deformer)
#
#     def __finalize(self):
#         if self.create_deformer:
#             cmds.setAttr(self.deformer + ".envelope", 1)
#             cmds.refresh(force = True)
#             cmds.setAttr(self.deformer + ".cacheWeights", 1)
#             cmds.setAttr(self.deformer + ".cacheParams", 1)
#             cmds.setAttr(self.deformer + ".cacheWeightMesh", 1)
#             cmds.setAttr(self.deformer + ".cacheWeightCurves", 1)
#             cmds.setAttr(self.deformer + ".cacheBase", 1)
#
#     def __create(self):
#         self.__unpack()
#         self.__create_geo()
#         self.__create_deformer()
#         self.__set_anim_curves()
#         self.__set_weights()
#         self.__transfer()
#         self.__finalize()
#
#
#
#
#
# class export_vector_deformer():
#     # ===============================================================================
#     # CLASS:         export_vector_deformer
#     # DESCRIPTION:   exports the vector deformer to an external file
#     # USAGE:         set args and run
#     # RETURN:
#     # REQUIRES:      maya.cmds
#     # AUTHOR:        Levi Harrison
#     # DATE:          Dec 1st, 2014
#     # Version        1.0.0
#     # ===============================================================================
#     ###############################################################################
#     # ---Example:
#     # export_vector_deformer(name = "C_testFace_VCD",
#     #                       path = "/corp/home/lharrison/Desktop/testExport.vec")
#     ###############################################################################
#     def __init__(self,
#                  name = "",
#                  path = "",
#                  ):
#
#         """
#         type  name:                        string
#         param name:                        name of the deformer you want to
#                                             export
#
#         type  export_path:                 string
#         param export_path:                 path to export to
#
#         """
#
#         #---args
#         self.name                           = name
#         self.path                           = path
#         #---vars
#         self.geo_membership                 = []
#         self.weight_geo                     = {}
#         self.base_geo                       = []
#         self.t_pivots                       = []
#         self.r_pivots                       = []
#         self.anim_curves                    = {}
#         self.deformer_weights               = {}
#         self.weights                        = {}
#         self.vector_dict                    = {}
#         # naming information for rebuilding
#         self.weightBase              = 0
#         self.geoms                   = []
#         self.weightGeo               = ""
#         self.weightBase              = []
#         self.tPivots                 = []
#         self.rPivots                 = []
#         self.control                 = ""
#         self.lockAttrs               = []
#         self.ihi                     = None
#         self.side                    = ""
#         self.short_name              = ""
#         self.tNames                  = []
#         self.rNames                  = []
#
#
#         self.__create()
#
#     def __check(self):
#         if not cmds.objExists(self.name):
#             raise Exception(self.name + " does not exist")
#             quit()
#     def __get_info(self):
#             # get all info from the deformer
#             # get all attribute names
#             # from attr names you will know curve and weight names
# #         self.geoms = cmds.deformer(self.name, q = True,g = True)
#
#         self.weightGeo = cmds.listConnections(self.name + ".weightPatch",
#                                               d = False)[0]
#
#         self.weightBase = cmds.listConnections(self.name + ".baseGeoArray",
#                                               d = False)
#
#         self.tPivots = cmds.listConnections(self.name + ".tPivotCurveArray",
#                                               d = False)
#
#         self.rPivots = cmds.listConnections(self.name + ".rPivotCurveArray",
#                                               d = False)
#
#         self.side = self.name.split("_")[0]
#         self.short_name = self.name.split("_")[1]
#         self.tNames = cmds.listConnections(self.name + ".tValueParentArray",
#                                            d = True,
#                                            p = True)
#         for i in range(len(self.tNames)):
#             self.tNames[i] = self.tNames[i].split(".")[1]
#         self.rNames  = cmds.listConnections(self.name + ".rValueParentArray",
#                                             d = True,
#                                             p = True)
#         for i in range(len(self.rNames)):
#             self.rNames[i] = self.rNames[i].split(".")[1]
#
#     def __get_memberships(self):
#             # get all deformed geometry and their memberships
#             #get set
#             self.set   = cmds.listConnections(self.name + ".message",
#                                               d = True,
#                                               p = True)[0].split(".")[0]
# #             attr = cmds.getAttr(self.name + ".message")
#             self.geo_membership = cmds.sets(self.set, q = True)
#             self.geo_membership = cmds.deformer(self.name, q = True, g = True)
#
#     def __get_geoms(self):
#             # get all driver geometry (for rebuilding)
#         self.weight_geo = xUtils.return_mesh_info(name = self.weightGeo).mesh
#         for i in range(len(self.weightBase)):
#             shape = cmds.listRelatives(self.weightBase[i], shapes = True)[0]
#             if (cmds.objectType(shape, isType='nurbsSurface')):
#                 self.base_geo.append(xUtils.return_nurbs_surface_info(name = self.weightBase[i]).nurbs)
#             if (cmds.objectType(shape, isType='mesh')):
#                 self.base_geo.append(xUtils.return_mesh_info(name = self.weightBase[i]).mesh)
#
#         for i in range(len(self.tPivots)):
#             shape = cmds.listRelatives(self.tPivots[i], shapes = True)[0]
#             self.t_pivots.append(xUtils.return_nurbs_curve_info(name = self.tPivots[i]).nurbsCurve)
#
#         for i in range(len(self.rPivots)):
#             shape = cmds.listRelatives(self.rPivots[i], shapes = True)[0]
#             self.r_pivots.append(xUtils.return_nurbs_curve_info(name = self.rPivots[i]).nurbsCurve)
# #             need to write functionality for nurbs curves
#     def __get_curves(self):
#             # get all curve infos
#         self.connections = []
#         self.connections.append(cmds.listConnections(self.name + ".tAnimCurveUArray",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".tAnimCurveVArray",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".rAnimCurveUArray",
#                                                      type = "animCurve",
#                                                      d = False))
#         self.connections.append(cmds.listConnections(self.name + ".rAnimCurveVArray",
#                                                      type = "animCurve",
#                                                      d = False))
#         flat_conn = []
#         for i in range(len(self.connections)):
#             if self.connections[i]:
#                 for j in range(len(self.connections[i])):
#                     if self.connections[i][j]:
#                         flat_conn.append(self.connections[i][j])
#         all = flat_conn
#         self.anim_curves = xUtils.get_anim_curve_info(anim_curve = all).curve_dict
#     def __get_weights(self):
#             # get all double array weights
#             tmp_weight_names = cmds.listAttr(self.name,
#                                              ud = True,
#                                              a = True)
#             tmp_values = []
#             tmp_names = []
#             geoms = cmds.deformer(self.name, q = True,g = True)
#             for i in range(len(tmp_weight_names)):
#                 for j in range(len(geoms)):
#                     split_weights = tmp_weight_names[i].split(".")
#                     tmp_names.append(self.name
#                                      + "."
#                                      + split_weights[0]
#                                      +"[" + str(j)
#                                      + "]."
#                                      + split_weights[1])
#                     tmp_values.append(cmds.getAttr(self.name
#                                                    + "."
#                                                    + split_weights[0]
#                                                    +"[" + str(j)
#                                                    + "]."
#                                                    + split_weights[1]))
#             self.weights = dict(zip(tmp_names,tmp_values))
#             # get deformer weights
#             tmp_def_weights = []
#             tmp_def_names   = []
#             tmp_flat_weights= []
#             tmp_flat_names= []
#             try:
#                 for i in range(len(geoms)):
#                     tmp_def_names = self.name + ".weightList[" + str(i) + "].weights"
#                     indices = cmds.getAttr(tmp_def_names, mi = True)
#                     for j in range(len(indices)):
#                         tmp_flat_names.append(self.name
#                                               + ".weightList["
#                                               + str(i)
#                                               + "].weights["
#                                               + str(indices[j])
#                                               + "]")
#                         tmp_flat_weights.append(cmds.getAttr(tmp_flat_names[j]))
#                 for i in range(len(tmp_flat_names)):
#                     self.deformer_weights[tmp_flat_names[i]] = tmp_flat_weights[i]
#             except:
#                 pass
#     def __organize(self):
#         self.vector_dict = {
#                            "weight_geo":           self.weight_geo,
#                            "anim_curves":          self.anim_curves,
#                            "weights":              self.weights,
#                            "geoms":                self.geoms,
#                            "base_geo":             self.base_geo,
#                            "t_pivots":             self.t_pivots,
#                            "r_pivots":             self.r_pivots,
#                            "geo_membership":       self.geo_membership,
#                            "deformer_weights":     self.deformer_weights,
#                            "weightGeo":            self.weightGeo,
#                            "control":              self.control,
#                            "lockAttrs":            self.lockAttrs,
#                            "ihi":                  self.ihi,
#                            "side":                 self.side,
#                            "short_name":           self.short_name,
#                            "tNames":               self.tNames,
#                            "rNames":               self.rNames,
#                            }
# #         print self.vector_dict
#     def __export(self):
#         file = open(self.path, "wb")
#         json.dump(self.vector_dict, file, sort_keys = True, indent = 2)
#         file.close()
#
#             # format info
#             # export info to a file
#     def __create(self):
#         self.__check()
#         self.__get_info()
#         self.__get_memberships()
#         self.__get_geoms()
#         self.__get_curves()
#         self.__get_weights()
#         self.__organize()
#         self.__export()
#
#
#
#
#
#
#
# class import_vector_deformer():
#     # ===============================================================================
#     # CLASS:         import_vector_deformer
#     # DESCRIPTION:   rebuilds the slide deformer
#     # USAGE:         set args and run
#     # RETURN:
#     # REQUIRES:      maya.cmds
#     # AUTHOR:        Levi Harrison
#     # DATE:          Dec 1st, 2014
#     # Version        1.0.0
#     # ===============================================================================
#     ##############################################################################
#     # ---Example:
#
#     # import_vector_deformer(path = "/corp/home/lharrison/Desktop/testExport.vec",
#     #                       create_geo = True,
#     #                       create_deformer = True,
#     #                       set_weights = True,
#     #                       set_curves = True)
#     ##############################################################################
#
#     def __init__(self,
#                  path = "",
#                  create_geo = True,
#                  create_deformer = True,
#                  set_weights = True,
#                  set_curves = True,
#                  ):
#
#         """
#         type  path:                 string
#         param path:                 path to import from
#         """
#
#         #---args
#         self.path                    = path
#         self.create_geo              = create_geo
#         self.create_deformer         = create_deformer
#         self.set_weights             = set_weights
#         self.set_curves              = set_curves
#         #---vars
#         self.dict                    = {}
#         self.geo_membership          = []
#         self.weight_geo              = {}
#         self.anim_curves             = {}
#         self.weights                 = {}
#         self.deformer_weights        = {}
#         self.baseGeo                 = []
#         self.geoms                   = []
#         self.control                 = ""
#         self.lockAttrs               = []
#         self.ihi                     = None
#         self.side                    = ""
#         self.short_name              = ""
#         self.tNames                  = {}
#         self.rNames                  = {}
#
#         self.__create()
#
#     def __unpack(self):
#         "imports the dictionary, separates all of the info for later use"
#         file = open(self.path, "rb")
#         self.dict = json.load(file)
#         file.close()
#
#         self.weight_geo       = self.dict["weight_geo"]
#         self.baseGeo          = self.dict["base_geo"]
#         self.t_pivots         = self.dict["t_pivots"]
#         self.r_pivots         = self.dict["r_pivots"]
#         self.anim_curves      = self.dict["anim_curves"]
#         self.weights          = self.dict["weights"]
#         self.geo_membership   = self.dict["geo_membership"]
#         self.deformer_weights = self.dict["deformer_weights"]
#         self.geoms            = self.dict["geoms"]
#         self.control          = self.dict["control"]
#         self.lockAttrs        = self.dict["lockAttrs"]
#         self.ihi              = self.dict["ihi"]
#         self.side             = self.dict["side"]
#         self.short_name       = self.dict["short_name"]
#         self.tNames           = self.dict["tNames"]
#         self.rNames           = self.dict["rNames"]
#     def __create_geo(self):
#         # check if geo already exists.  If so use it instead of creating new.
#         if self.create_geo == True:
#             #---create weight surface, parent if any
#             if not cmds.objExists(self.weight_geo["name"]):
#                 self.weightGeo = xUtils.create_mesh(self.weight_geo).fullPathName()
#                 self.weightGeo = cmds.listRelatives(self.weightGeo, parent = True)
#                 self.weightGeo = cmds.rename(self.weightGeo, self.weight_geo["name"])
#             else:
#                 self.weightGeo = self.weight_geo["name"]
#             #---create base geo, parent if any
#             tmp_baseGeo = []
#             tmp = []
#             for i in range(len(self.baseGeo)):
#                 if not cmds.objExists(self.baseGeo[i]["name"]):
#                     tmp = xUtils.create_mesh(self.baseGeo[i]).fullPathName()
#                     tmp = cmds.listRelatives(tmp, parent = True)
#                     tmp = cmds.rename(tmp, self.baseGeo[i]["name"])
#                     cmds.setAttr(tmp+".v",0)
#                     tmp_baseGeo.append(tmp)
#                 else:
#                     tmp_baseGeo.append(self.baseGeo[i]["name"])
#             self.baseGeo = tmp_baseGeo
#
#             #---create t_pivots
#             tmp_array = []
#             tmp = []
#             for i in range(len(self.t_pivots)):
#                 tmp = xUtils.create_curve(self.t_pivots[i]).fullPathName()
#                 tmp = cmds.listRelatives(tmp, parent = True)
#                 tmp = cmds.rename(tmp, self.t_pivots[i]["name"])
#                 cmds.setAttr(tmp+".v",0)
#                 tmp_array.append(tmp)
#             self.t_pivots = tmp_array
# #             print self.t_pivots
#             #---create r_pivots
#             tmp_array = []
#             tmp = []
#             for i in range(len(self.r_pivots)):
#                 tmp = xUtils.create_curve(self.r_pivots[i]).fullPathName()
#                 tmp = cmds.listRelatives(tmp, parent = True)
#                 tmp = cmds.rename(tmp, self.r_pivots[i]["name"])
#                 cmds.setAttr(tmp+".v",0)
#                 tmp_array.append(tmp)
#             self.r_pivots = tmp_array
#
#     def __create_deformer(self):
#         "creates deformer, turns envelope off"
#         if self.create_deformer == True:
#             self.deformer = vectorDeformerCmds.vectorDeformerCmd(
#                                                  weightGeo = self.weightGeo,
#                                                  geoms = self.geo_membership,
#                                                  weightBase = self.baseGeo,
#                                                  control = '',
#                                                  ihi = 1,
#                                                  side = self.side,
#                                                  name = self.short_name,
#                                                  tPivots = self.t_pivots,
#                                                  rPivots = self.r_pivots,
#                                                  #---Mouth
#                                                  tNames = self.tNames,
#                                                  rNames = self.rNames,
#                                                  ).returnDeformer
# #             cmds.setAttr(self.deformer + ".envelope", 0)
#
#     def __set_anim_curves(self):
#         if self.set_curves == True:
#             for i in range(len(self.anim_curves)):
#                 anim_curves = self.anim_curves[str(i)]["name"]
#                 frame_values = self.anim_curves[str(i)]["frame_values"]
#                 frame_times= self.anim_curves[str(i)]["frame_times"]
#                 in_x_tangents= self.anim_curves[str(i)]["in_x_tangents"]
#                 in_y_tangents= self.anim_curves[str(i)]["in_y_tangents"]
#                 out_x_tangents= self.anim_curves[str(i)]["out_x_tangents"]
#                 out_y_tangents= self.anim_curves[str(i)]["out_y_tangents"]
#                 in_tangents_type= self.anim_curves[str(i)]["in_tangents_type"]
#                 out_tangents_type= self.anim_curves[str(i)]["out_tangents_type"]
#                 set_anim_curves(anim_curves,
#                                 frame_values,
#                                 frame_times,
#                                 in_x_tangents,
#                                 in_y_tangents,
#                                 out_x_tangents,
#                                 out_y_tangents,
#                                 in_tangents_type,
#                                 out_tangents_type)
#
#     def __set_weights(self):
#         "sets deformer weight, then sets double array weights"
#         if self.set_weights == True:
#             if self.deformer_weights:
#                 for i in self.deformer_weights.keys():
#                     cmds.setAttr(i, self.deformer_weights.get(i))
#
#             for i in self.weights.keys():
#                 weights = self.weights.get(i)
#                 if not weights == None:
#                     try:
#                         cmds.setAttr(i, weights,typ='doubleArray')
#                     except:
#                         pass
#
#     def __finalize(self):
#         cmds.setAttr(self.deformer + ".envelope", 1)
#         cmds.refresh(force = True)
#         if self.create_deformer == True:
#             if self.baseGeo:
#                 cmds.setAttr(self.deformer + ".useBaseGeo", 1)
#             cmds.setAttr(self.deformer + ".cachePivots", 1)
#             cmds.setAttr(self.deformer + ".cacheWeights", 1)
#             cmds.setAttr(self.deformer + ".cacheWeightMesh", 1)
#             cmds.setAttr(self.deformer + ".cacheWeightCurves", 1)
#
#     def __create(self):
#         self.__unpack()
#         self.__create_geo()
#         self.__create_deformer()
#         self.__set_anim_curves()
#         self.__set_weights()
#         self.__finalize()
#
# # def weightTransfer(srcMesh, destMesh, srcDeformer, destDeformer, attributes):
