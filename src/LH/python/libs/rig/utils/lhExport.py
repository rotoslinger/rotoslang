import sys

from utils.exportUtils import set_anim_curve_data, lhDeformerWeightTransfer

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

from utils import exportUtils as xUtils
from maya import cmds
import json
from utils import LHSlideDeformerCmds, LHVectorDeformerCmds, LHCurveRollDeformerCmds
reload(LHSlideDeformerCmds)
reload(LHVectorDeformerCmds)
reload(LHCurveRollDeformerCmds)


class lh_deformer_export(object):
    def __init__(self,
                 name = "",
                 path = "",
                 ):
        self.name = name
        self.path = path
        self.create()

    def check(self):
        if not cmds.objExists(self.name):
            raise Exception(self.name + " does not exist")

    def createInstanceVariables(self):
        return

    def getInfo(self):
        self.side = self.name.split("_")[0]
        self.short_name = self.name.split("_")[1]

    def get_memberships(self):
        self.geo_membership = cmds.deformer(self.name, q=True, g=True)

    def getGeoms(self):
        return

    def getTransferGeo(self):
        #---Exporting the transfer geo means finding a non deformed copy of the mesh and storing it.
        #---The base geo is the only geo that is garanteed to not be deformed.
        self.transferGeo = []
        tmpTransferGeo = []
        for geo in cmds.listConnections(self.name + ".baseGeoArray", d = False):
            tmpTransferGeo.append(cmds.duplicate(geo, n= geo.replace("Base","Transfer"))[0])
        for i in range(len(tmpTransferGeo)):
            shape = cmds.listRelatives(tmpTransferGeo[i], shapes = True)[0]
            if (cmds.objectType(shape, isType='nurbsSurface')):
                transferGeo = xUtils.nurbsSurfaceData(name = tmpTransferGeo[i]).nurbs
                self.transferGeo.append(transferGeo)

            if (cmds.objectType(shape, isType='mesh')):
                transferGeo = xUtils.meshData(name = tmpTransferGeo[i]).mesh
                self.transferGeo.append(transferGeo)
        cmds.delete(tmpTransferGeo)


    def getCurves(self):
        return


    def getWeights(self):
        # get all double array weights
        tmp_weight_names = cmds.listAttr(self.name,
                                         ud=True,
                                         a=True)
        tmp_values = []
        tmp_names = []
        geoms = cmds.deformer(self.name, q=True, g=True)
        for i in range(len(tmp_weight_names)):
            for j in range(len(geoms)):
                split_weights = tmp_weight_names[i].split(".")
                tmp_names.append(self.name
                                 + "."
                                 + split_weights[0]
                                 + "[" + str(j)
                                 + "]."
                                 + split_weights[1])
                tmp_values.append(cmds.getAttr(self.name
                                               + "."
                                               + split_weights[0]
                                               + "[" + str(j)
                                               + "]."
                                               + split_weights[1]))
        self.weights = dict(zip(tmp_names, tmp_values))
        # get deformer weights
        tmp_def_weights = []
        tmp_def_names = []
        tmp_flat_weights = []
        tmp_flat_names = []
        try:
            for i in range(len(geoms)):
                tmp_def_names = self.name + ".weightList[" + str(i) + "].weights"
                indices = cmds.getAttr(tmp_def_names, mi=True)
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


    def organize(self):
        return

    def export(self):
        file = open(self.path, "wb")
        json.dump(self.vector_dict, file, sort_keys=False, indent=2)
        file.close()

    def create(self):
        self.check()
        self.createInstanceVariables()
        self.getInfo()
        self.get_memberships()
        self.getGeoms()
        self.getTransferGeo()
        self.getCurves()
        self.getWeights()
        self.organize()
        self.export()


class lh_deformer_import(object):
    def __init__(self,
                 path = "",
                 create_geo = True,
                 create_deformer = True,
                 set_weights = True,
                 set_curves = True,
                 transferWeights = False
                 ):
        #---args
        self.path                    = path
        self.create_geo              = create_geo
        self.create_deformer         = create_deformer
        self.set_weights             = set_weights
        self.set_curves              = set_curves
        self.transferWeights         = transferWeights
        self.transferSuffix          = ""

        self.create()

    def create_instance_variables(self):
        pass

    def getFileData(self):
        file = open(self.path, "rb")
        self.dict = json.load(file)
        file.close()

    def unpack(self):
        "imports the dictionary, separates all of the info for later use"
        return

    def createGeo(self):
        return

    def createBase(self):
        """Creates base"""
        self.baseGeo = []
        for i in self.geo_membership:
            tmp = cmds.duplicate(i, name = i + "Base")[0]
            cmds.setAttr(tmp+".v",0)
            self.baseGeo.append(tmp)

    def createTransferGeo(self):
        if not self.transferWeights:
            return
        tmp_transferGeo = []
        tmp = []
        for i in range(len(self.transferGeo)):
            if not cmds.objExists(self.transferGeo[i]["name"]):
                print "creating Transfer Geo"
                tmp = xUtils.create_mesh(self.transferGeo[i]).fullPathName()
                tmp = cmds.listRelatives(tmp, parent = True)
                tmp = cmds.rename(tmp, self.transferGeo[i]["name"])
                cmds.setAttr(tmp+".v",0)
                tmp_transferGeo.append(tmp)
            else:
                tmp_transferGeo.append(self.transferGeo[i]["name"])
        self.transferGeo = tmp_transferGeo

    def createDeformer(self):
        "creates deformer, turns envelope off"
        return

    def createTransferDeformer(self):
        return

    def setAnimCurves(self):
        if not self.set_curves:
            return
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
            set_anim_curve_data(anim_curves,
                                frame_values,
                                frame_times,
                                in_x_tangents,
                                in_y_tangents,
                                out_x_tangents,
                                out_y_tangents,
                                in_tangents_type,
                                out_tangents_type)

    def setWeights(self):
        "sets deformer weight, then sets double array weights"
        if not self.set_weights:
            return
        #---Double Check that the geo in the scene is the same as the geo from the dictionary
        #---If not, don't set weights, maya could crash
        for i in range(len(self.geo_membership)):
            if not xUtils.comparePolyCount(self.geo_membership[i], self.transferGeo[i]):
                print "Points do not match, weights can be transfered, not set"
                return

        if self.deformer_weights:
            for i in self.deformer_weights.keys():
                cmds.setAttr(i, self.deformer_weights.get(i))
        #ToFixOldDeformers
        for i in self.weights.keys():
            weights = self.weights.get(i)

            if not weights:
                continue
            try:
                cmds.setAttr(i, weights,typ='doubleArray')
            except:
                print "Weights for " + i + " unable to be set.  It is likely topology has changed."

    def getTransferData(self):
        return

    def setTransferWeights(self):
        if not self.transferWeights:
            return
        #---Set Transfer weights
        for i in self.weights.keys():
            weights = self.weights.get(i)
            if not weights:
                continue
            transferAttr = i.replace(self.transferSuffix, "{0}SRC".format(self.transferSuffix))

            try:
                print transferAttr
                cmds.setAttr(transferAttr, weights, typ='doubleArray')
            except:
                print "Weights for " + i + " unable to be set."

    def transfer(self):
        if not self.transferWeights:
            return
        for i in range(len(self.transferGeo)):
            lhDeformerWeightTransfer(self.transferGeo[i], self.transferDeformer, self.geo_membership[i], self.deformer)

    def finalize(self):
        pass

    def create(self):
        self.create_instance_variables()
        self.getFileData()
        self.unpack()
        self.createGeo()
        self.createBase()
        self.createTransferGeo()
        self.createDeformer()
        self.createTransferDeformer()
        self.setAnimCurves()
        self.setWeights()
        self.getTransferData()
        self.setTransferWeights()
        self.transfer()
        self.finalize()

# def weightTransfer(srcMesh, destMesh, srcDeformer, destDeformer, attributes):
