import sys

from rig.utils.exportUtils import set_anim_curve_data, lhDeformerWeightTransfer
from rig.rigComponents import slidingCtrl, elements, meshRivetCtrl
import importlib
importlib.reload(slidingCtrl)
importlib.reload(elements)
importlib.reload(meshRivetCtrl)
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
from maya import cmds, OpenMaya
import json
from rig.utils import LHSlideDeformerCmds, LHVectorDeformerCmds, LHCurveRollDeformerCmds, misc
importlib.reload(LHSlideDeformerCmds)
importlib.reload(LHVectorDeformerCmds)
importlib.reload(LHCurveRollDeformerCmds)


class lh_deformer_export(object):
    def __init__(self,
                 name = "",
                 path = "",
                 ):
        self.name = name
        self.path = path
        self.vector_dict = {}
        self.manipDict = {}
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
        self.weights = dict(list(zip(tmp_names, tmp_values)))
        # get deformer weights
        tmp_flat_weights = []
        tmp_flat_names = []
        try:
            for i in range(len(geoms)):
                tmp_def_names = self.name + ".weightList[" + str(i) + "].weights"
                indices = cmds.getAttr(tmp_def_names, mi=True)
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

    def getStickyObjectsCrappy(self, ctrl):
        buffer1 = cmds.listRelatives(ctrl, p=True)[0]
        buffer2 = cmds.listRelatives(buffer1, p=True)[0]
        locator = cmds.listRelatives(buffer2, p=True)[0]
        root = cmds.listRelatives(locator, p=True)[0]

        # Will Likely need to be replaced when we come up with a better way of constraining the up vector
        normalConstraint = cmds.listConnections(locator + ".rx")
        normalConstraintGeo = None
        if normalConstraint:
            # print normalConstraint[0], "THIS THING"
            normalConstraintGeo = cmds.listConnections(normalConstraint[0] + ".target[0].targetGeometry")
            if normalConstraintGeo:
                normalConstraintGeo = normalConstraintGeo[0]
            # print normalConstraintGeo
        geoConstraint = cmds.listConnections(buffer2 + ".geoConstraint")[0]
        mesh = cmds.listConnections(geoConstraint + ".inMesh", sh=True)[0]
        return buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo

    def getStickyControls(self):
        self.meshRivetManips = {}

        # attrs that might be connected
        # attrs = [".txOut", ".tyOut", ".tzOut", ".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz",
        #          ".speedTx",".speedTy", ".speedTz", ".rotateOrder", ".vis", ".gimbal_vis"]
        attrs = elements.MESH_RIVET_ATTRS
        stickControls = cmds.ls(et="nullTransform")
        for ctrl in stickControls:
            if ctrl not in list(self.meshRivetManips.keys()):
                self.meshRivetManips[ctrl] = {}
            buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo = self.getStickyObjectsCrappy(ctrl)

            name = key.split("_")
            self.manipDict[ctrl]["name"] = name[1]
            self.manipDict[ctrl]["side"] = name[0]
            self.manipDict[ctrl]["suffix"] = name[2]
            parent = False
            if cmds.listRelatives(name[0] + "_" + name[1] + "_CPT", parent=True):
                parent = cmds.listRelatives(name[0] + "_" + name[1] + "_CPT", parent=True)[0]
            self.manipDict[key]["parent"] = parent

            # self.manipDict[key]["uSpeedDefault"]= cmds.getAttr(key + ".uSpeed")
            # self.manipDict[key]["vSpeedDefault"]= cmds.getAttr(key + ".vSpeed")


            # print buffer1, buffer2, locator, geoConstraint
            if "geoConstraintGeo" not in list(self.meshRivetManips[ctrl].keys()):
                    self.meshRivetManips[ctrl]["geoConstraintGeo"] = xUtils.meshData(name=mesh).mesh
            if normalConstraintGeo and "surfaceConstraintGeo" not in list(self.meshRivetManips[ctrl].keys()):
                    self.meshRivetManips[ctrl]["surfaceConstraintGeo"] = xUtils.nurbsSurfaceData(name=normalConstraintGeo).nurbs
        # mesh = cmds.listConnections(geoConstraint + ".inMesh", sh=True)[0]
        #print stickControls

    def getDirectManips(self):
        #--- get the user defined attributes on the deformer, check connections, if connected to direct manip export
        # attributes = cmds.listAttr(self.name, ud=True, c=True, s=True, m=False, a=False)
        self.manipDict = {}

        attributes = cmds.listAttr(self.name, ud=True, c=True, s=True, m=False, a=False)
        for attr in attributes:
            if not cmds.objExists(self.name + "." + attr):
                continue
            connections = cmds.listConnections(self.name + "." + attr, p=True, t="transform", s=True)
            if not connections:
                continue
            for con in connections:
                if not ".outU" or ".outV" in con[0]:
                    continue
                key = con.split(".")[0]
                if key not in list(self.manipDict.keys()):
                    self.manipDict[key] = {}
                    name = key.split("_")
                    self.manipDict[key]["name"] = name[1]
                    self.manipDict[key]["side"] = name[0]
                    self.manipDict[key]["suffix"] = name[2]
                    parent = False
                    if cmds.listRelatives(name[0] + "_" + name[1] + "_CPT", parent=True):
                        parent = cmds.listRelatives(name[0] + "_" + name[1] + "_CPT", parent=True)[0]
                    self.manipDict[key]["parent"] = parent
                    if "helperGeo" not in list(self.manipDict[key].keys()):
                        pointOnSurface = cmds.listConnections(key, t="pointOnSurfaceInfo")
                        if pointOnSurface:
                            pointOnSurface = pointOnSurface[0]
                            surf = cmds.listConnections(pointOnSurface, p=True, t="nurbsSurface", s=True)[0]
                            surfaceShape = surf.split(".")[0]
                            self.manipDict[key]["helperGeo"] = cmds.listRelatives(surfaceShape, parent=True)[0]
                            self.manipDict[key]["helperGeoData"] = xUtils.nurbsSurfaceData(name=surfaceShape).nurbs
                    self.manipDict[key]["uSpeedDefault"]= cmds.getAttr(key + ".uSpeed")
                    self.manipDict[key]["vSpeedDefault"]= cmds.getAttr(key + ".vSpeed")
                    self.manipDict[key]["initUDefault"]= cmds.getAttr(key + ".initU")
                    self.manipDict[key]["initVDefault"]= cmds.getAttr(key + ".initV")
                    self.manipDict[key]["baseUDefault"]= cmds.getAttr(key + ".baseU")
                    self.manipDict[key]["baseVDefault"]= cmds.getAttr(key + ".baseV")
                    self.manipDict[key]["amountUDefault"]= cmds.getAttr(key + ".amountU")
                    self.manipDict[key]["amountVDefault"]= cmds.getAttr(key + ".amountV")
                if "outU" in con.split(".")[1]:
                    self.manipDict[key]["uOutConnectionAttr"] = self.name + "." + attr
                if "outV" in con.split(".")[1]:
                    self.manipDict[key]["vOutConnectionAttr"] = self.name + "." + attr
                ctrlShape = cmds.listRelatives(key, type = "nurbsCurve")[0]
                self.manipDict[key]["nurbsShape"] = xUtils.nurbsCurveData(name = ctrlShape, space=OpenMaya.MSpace.kObject).nurbsCurve


    def pack(self):
        self.vector_dict["manipDict"] = self.manipDict

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
        # self.getStickyControls()
        # self.getDirectManips()
        self.pack()
        self.export()


class lh_deformer_import(object):
    def __init__(self,
                 path = "",
                 short_name = "",
                 geo_membership = [],
                 create_geo = True,
                 create_deformer = True,
                 set_weights = True,
                 set_curves = True,
                 transferWeights = False
                 ):
        #---args
        self.path                    = path
        self.short_name              = short_name
        self.geo_membership          = geo_membership
        self.create_geo              = create_geo
        self.create_deformer         = create_deformer
        self.set_weights             = set_weights
        self.set_curves              = set_curves
        self.transferWeights         = transferWeights
        self.transferSuffix          = ""
        self.manipDict = {}

        self.create()

    def create_instance_variables(self):
        pass

    def getFileData(self):
        file = open(self.path, "rb")
        self.dict = json.load(file)
        file.close()

    def unpack(self):
        "imports the dictionary, separates all of the info for later use"
        if "manipDict" in list(self.dict.keys()):
            self.manipDict   = self.dict["manipDict"]
        print(self.geo_membership)
        if not self.geo_membership:
            self.geo_membership = self.dict["geo_membership"]

    def createGeo(self):
        return

    def createBase(self):
        """Creates base"""
        self.baseGeo = []
        print(self.geo_membership)
        for i in self.geo_membership:
            shapeParent = cmds.listRelatives(i, parent=True)
            if shapeParent:
                shapeParent = shapeParent[0]
            if not shapeParent:
                shapeParent = i
            if not cmds.objExists(shapeParent+"Base"):
                tmp = cmds.duplicate(shapeParent, name = shapeParent + "Base")[0]
                cmds.setAttr(tmp+".v",0)
                self.baseGeo.append(tmp)
            else:
                self.baseGeo.append(shapeParent+"Base")

    def createTransferGeo(self):
        if not self.transferWeights:
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
                print("Points do not match, weights can be transfered, not set")
                return

        if self.deformer_weights:
            for i in list(self.deformer_weights.keys()):
                cmds.setAttr(i, self.deformer_weights.get(i))
        #ToFixOldDeformers
        for i in list(self.weights.keys()):
            weights = self.weights.get(i)

            if not weights:
                continue
            try:
                cmds.setAttr(i, weights,typ='doubleArray')
            except:
                print("Weights for " + i + " unable to be set.  It is likely topology has changed.")

    def getTransferData(self):
        return

    def setTransferWeights(self):
        if not self.transferWeights:
            # right now if you don't set weights the deformer will crash maya, you need to set the weights to be all 1
            return
        #---Set Transfer weights
        for i in list(self.weights.keys()):
            weights = self.weights.get(i)
            if not weights:
                continue
            transferAttr = i.replace(self.transferSuffix, "{0}SRC".format(self.transferSuffix))

            try:
                cmds.setAttr(transferAttr, weights, typ='doubleArray')
            except:
                print("Weights for " + i + " unable to be set.")

    def transfer(self):
        if not self.transferWeights:
            return
        for i in range(len(self.transferGeo)):
            lhDeformerWeightTransfer(self.transferGeo[i], self.transferDeformer, self.geo_membership[i], self.deformer)

    def finalize(self):
        pass

    def createDirectManip(self):
        keys = ["name", "side", "suffix", "parent", "helperGeo", "helperGeoData", "uSpeedDefault",
                "vSpeedDefault", "initUDefault", "initVDefault", "baseUDefault", "baseVDefault",
                "amountUDefault", "amountVDefault", "uOutConnectionAttr", "vOutConnectionAttr", "nurbsShape"]

        for key in list(self.manipDict.keys()):
            ctrlDict = self.manipDict[key]
            for k in keys:
                setattr(self, k, ctrlDict[k])
            helperGeo = self.helperGeo
            if not cmds.objExists(helperGeo):
                name = self.helperGeo.split("_")
                helperGeo = xUtils.createNurbsSurface(self.helperGeoData, name=misc.formatName(name[0], name[1], name[2])).fullPathName()
                helperGeo = cmds.listRelatives(helperGeo, parent=True)[0]
                cmds.setAttr(helperGeo + ".v", 0)
            slidingCtrl.component( side=self.side,
                                   name=self.name,
                                   # suffix=self.suffix,
                                   parent=self.parent,
                                   helperGeo=helperGeo,
                                   uSpeedDefault=self.uSpeedDefault,
                                   vSpeedDefault=self.vSpeedDefault,
                                   initUDefault=self.initUDefault,
                                   initVDefault=self.initVDefault,
                                   baseUDefault=self.baseUDefault,
                                   baseVDefault=self.baseVDefault,
                                   amountUDefault=self.amountUDefault,
                                   amountVDefault=self.amountVDefault,
                                   uOutConnectionAttr=self.uOutConnectionAttr,
                                   vOutConnectionAttr=self.vOutConnectionAttr,
                                   curveData=self.nurbsShape)
            slidingCtrl.create()

            

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
        # self.createDirectManip()

# def weightTransfer(srcMesh, destMesh, srcDeformer, destDeformer, attributes):
class lh_component_export(object):
    def __init__(self,
                 type = "meshRivetCtrl",
                 path = "",
                 ):
        # self.name = name
        self.path = path
        # self.manipDict = {}
        self.create()

    def getStickyObjectsCrappy(self, ctrl):
        buffer1 = cmds.listRelatives(ctrl, p=True)[0]
        buffer2 = cmds.listRelatives(buffer1, p=True)[0]
        locator = cmds.listRelatives(buffer2, p=True)[0]
        root = cmds.listRelatives(locator, p=True)[0]

        # Will Likely need to be replaced when we come up with a better way of constraining the up vector
        normalConstraint = cmds.listConnections(locator + ".rx")
        normalConstraintGeo = None
        if normalConstraint:
            # print normalConstraint[0], "THIS THING"
            normalConstraintGeo = cmds.listConnections(normalConstraint[0] + ".target[0].targetGeometry")
            if normalConstraintGeo:
                normalConstraintGeo = normalConstraintGeo[0]
            # print normalConstraintGeo
        geoConstraint = cmds.listConnections(buffer2 + ".geoConstraint")[0]
        mesh = cmds.listConnections(geoConstraint + ".inMesh", sh=True)[0]
        return buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo

    def getManips(self):
        self.manipDict = {}

        # attrs that might be connected
        attributes = [".txOut", ".tyOut", ".tzOut", ".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz",
                 ".speedTx",".speedTy", ".speedTz", ".rotateOrder", ".vis", ".gimbal_vis"]
        stickControls = cmds.ls(et="nullTransform")
        self.manipDict["controls"] = {}
        for ctrl in stickControls:
            if ctrl not in list(self.manipDict.keys()):
                self.manipDict["controls"][ctrl] = {}
            ctrlShape = cmds.listRelatives(ctrl, type = "nurbsCurve")[0]
            self.manipDict["controls"][ctrl]["nurbsShape"] = xUtils.nurbsCurveData(name = ctrlShape, space=OpenMaya.MSpace.kObject).nurbsCurve
            buffer1, buffer2, locator, geoConstraint, root, mesh, normalConstraintGeo = self.getStickyObjectsCrappy(ctrl)
            self.manipDict["controls"][ctrl]["buffer1"] = buffer1
            self.manipDict["controls"][ctrl]["buffer2"] = buffer2
            self.manipDict["controls"][ctrl]["locator"] = locator
            self.manipDict["controls"][ctrl]["geoConstraint"] = geoConstraint
            self.manipDict["controls"][ctrl]["root"] = root

            name = ctrl.split("_")
            self.manipDict["controls"][ctrl]["name"] = name[1]
            self.manipDict["controls"][ctrl]["side"] = name[0]
            self.manipDict["controls"][ctrl]["suffix"] = name[2]
            parent = False
            if cmds.listRelatives(root, parent=True):
                parent = cmds.listRelatives(root, parent=True)[0]
                # print "PARENT!!!!!!", parent
            self.manipDict["controls"][ctrl]["parent"] = parent
            self.manipDict["controls"][ctrl]["attrVals"] = {}
            self.manipDict["controls"][ctrl]["attrConnections"] = {}
            for attr in attributes:
                # print ctrl + attr
                attrName = ctrl + attr
                if not cmds.objExists(attrName):
                    continue
                self.manipDict["controls"][ctrl]["attrVals"][attrName] = cmds.getAttr(attrName)
                con = None
                tmpConnection = cmds.listConnections(attrName, p=True, d=True, scn=True)
                if tmpConnection:
                    # convert to string if it exists
                    con = [str(x) for x in tmpConnection]
                self.manipDict["controls"][ctrl]["attrConnections"][attrName] = con

            self.manipDict["controls"][ctrl]["translate"] = cmds.xform(locator, q=True, t=True, ws=True)
            self.manipDict["controls"][ctrl]["rotate"] = cmds.xform(locator, q=True, ro=True, ws=True)
            self.manipDict["controls"][ctrl]["scale"] = cmds.xform(locator, q=True, s=True,ws=True)

            self.manipDict["controls"][ctrl]["translateOffset"] = cmds.xform(buffer2, q=True, t=True, ws=True)
            self.manipDict["controls"][ctrl]["rotateOffset"] = cmds.xform(buffer2, q=True, ro=True, ws=True)
            self.manipDict["controls"][ctrl]["scaleOffset"] = cmds.xform(buffer2, q=True, s=True,ws=True)

            self.manipDict["controls"][ctrl]["geoConstraintGeoName"] = mesh
            self.manipDict["controls"][ctrl]["normalConstraintGeoName"] = normalConstraintGeo

            if "geoConstraintGeo" not in list(self.manipDict.keys()):
                    self.manipDict["geoConstraintGeo"] = {}
            if mesh not in list(self.manipDict["geoConstraintGeo"].keys()):
                    self.manipDict["geoConstraintGeo"][mesh] = xUtils.meshData(name=mesh).mesh
            if normalConstraintGeo and "normalConstraintGeo" not in list(self.manipDict.keys()):
                    self.manipDict["normalConstraintGeo"] = {}
            if normalConstraintGeo and normalConstraintGeo not in list(self.manipDict["normalConstraintGeo"].keys()):
                    self.manipDict["normalConstraintGeo"][normalConstraintGeo] = xUtils.nurbsSurfaceData(name=normalConstraintGeo).nurbs

    def export(self):
        file = open(self.path, "wb")
        json.dump(self.manipDict, file, sort_keys=False, indent=2)
        file.close()

    def create(self):
        self.getManips()
        self.export()


class lh_component_import(object):
    def __init__(self,
                 path = "",
                 create_geo = True,
                 geo_name = None,
                 guides = False,
                 manipDict = None,
                 ):
        #---args
        self.path                    = path
        self.create_geo              = create_geo
        self.geo_name                = geo_name
        self.guides                  = guides
        self.manipDict               = manipDict

        self.create()

    def getFileData(self):
        if not self.manipDict:
            file = open(self.path, "rb")
            self.manipDict = json.load(file)
            file.close()

    # def unpack(self):
    #     "imports the dictionary, separates all of the info for later use"
    #     if "manipDict" in self.dict.keys():
    #         self.manipDict   = self.dict["manipDict"]

    
    def createComponents(self):
        """
        Attrs that will be unpacked as second layer keys:
        rotateOffset
        geoConstraintGeo
        rotate
        translateOffset
        suffix
        parent
        attrConnections
        surfaceConstraintGeo
        scale
        attrVals
        translate
        scaleOffset
        side
        name
        """
        # Find all of the mesh's, or create them if they don't exist yet

        for key in list(self.manipDict["geoConstraintGeo"].keys()):
            meshName = self.manipDict["geoConstraintGeo"][key]["name"]
            if not cmds.objExists(meshName):
                xUtils.createMesh(self.manipDict["geoConstraintGeo"][key],
                                  name=meshName,
                                  parent=self.manipDict["geoConstraintGeo"][key]["parent"])
        if "normalConstraintGeo" in list(self.manipDict.keys()):
            for key in list(self.manipDict["normalConstraintGeo"].keys()):
                nurbsName = self.manipDict["normalConstraintGeo"][key]["name"]
                if not cmds.objExists(nurbsName):
                    xUtils.createNurbsSurface(self.manipDict["normalConstraintGeo"][key],
                                            name=nurbsName,
                                            parent=self.manipDict["normalConstraintGeo"][key]["parent"])
        attributes = elements.MESH_RIVET_ATTRS
        for key in list(self.manipDict["controls"].keys()):
            ctrlDict = self.manipDict["controls"][key]
            if not cmds.objExists(key):
                if not self.geo_name:
                    self.geo_name = ctrlDict["geoConstraintGeoName"]
                # print "PAAARENT", ctrlDict["parent"]
                rivetComponent = meshRivetCtrl.Component(name=ctrlDict["name"],
                                                        parent=ctrlDict["parent"],
                                                        guide=True,
                                                        side=ctrlDict["side"],
                                                        normalConstraintPatch = ctrlDict["normalConstraintGeoName"],
                                                        mesh = self.geo_name,
                                                        selection=False,
                                                        translate=ctrlDict["translate"],
                                                        rotate=ctrlDict["rotate"],
                                                        scale=ctrlDict["scale"],
                                                        curveData=ctrlDict["nurbsShape"])
                rivetComponent.create()
            cmds.xform(ctrlDict["buffer2"], ws=True, t=ctrlDict["translateOffset"])
            cmds.xform(ctrlDict["buffer2"], ws=True, ro=ctrlDict["rotateOffset"])
            cmds.xform(ctrlDict["buffer2"], ws=True, s=ctrlDict["scaleOffset"])
            ctrl = key
            for attr in attributes:
                attrName = ctrl + attr
                if not cmds.objExists(attrName):
                    continue
                if cmds.getAttr(attrName, se=True):
                    cmds.setAttr(attrName, ctrlDict["attrVals"][attrName])
                if not ctrlDict["attrConnections"][attrName]:
                    continue
                for connectedAttr in ctrlDict["attrConnections"][attrName]:
                    connectedAttrName = str(connectedAttr)
                    # print connectedAttrName
                    if not cmds.objExists(connectedAttrName):
                        continue
                    # check if attr is locked, if not connect
                    if not cmds.getAttr(connectedAttrName, l=True):
                    # if cmds.attributeQuery(attr.split(".")[1], node = ctrl, connectable=True):
                        cmds.connectAttr(attrName, connectedAttrName, f=True)
    
    def cleanup(self):
        if not self.guides:
            meshRivetCtrl.rivetGuidesVis(False)


    def create(self):
        self.getFileData()
        self.createComponents()
        self.cleanup()


class joint(object):
    def __init__(self,
                 path = "",
                 jointRoot=""
                 ):
        #---args
        self.path                    = path
        self.jointRoot                = jointRoot


    def getJoints(self):
        # Find the hierarchy of joints
        allJoints = []
        allJoints = cmds.listRelatives(self.jointRoot, ad=True, typ="joint")
        allJoints.append(self.jointRoot)
        self.jointDict = {}
        for joint in allJoints:
            data = {}
            parent = cmds.listRelatives(joint, p=True)
            if parent:
                data["parent"] = parent[0]
                cmds.parent(joint, w=True)
            # if cmds.listRelatives(joint, parent=True):
            #     cmds.parent(joint, w=True)
            data["position"] = cmds.joint(joint, q=True, p=True, a=True)
            data["orientation"] = cmds.joint(joint, q=True, a=False, o=True)
            if joint == "l_wrist_bind":
                print(cmds.joint(joint, q=True, a=False, o=True))
            data["scaleOrientation"] = cmds.joint(joint, q=True, so=True)
            data["radius"] = cmds.joint(joint, q=True, rad=True)
            self.jointDict[joint] = data
        for joint in list(self.jointDict.keys()):
            if cmds.objExists(self.jointDict[joint]["parent"]):
                cmds.parent(joint, self.jointDict[joint]["parent"])
    def export(self):
        file = open(self.path, "wb")
        json.dump(self.jointDict, file, sort_keys=False, indent=2)
        file.close()

    def exportData(self):
        self.getJoints()
        self.export()
    
    def setJoints(self):
        for joint in list(self.jointDict.keys()):
            if not cmds.objExists(joint):
                cmds.joint(n=joint)
            if cmds.listRelatives(joint, parent=True):
                cmds.parent(joint, w=True)
            cmds.joint(joint, e=True, p=self.jointDict[joint]["position"], a=True)
            cmds.joint(joint, e=True, so=self.jointDict[joint]["scaleOrientation"])
            cmds.joint(joint, e=True, a=False, o=self.jointDict[joint]["orientation"])
            cmds.joint(joint, e=True, rad=self.jointDict[joint]["radius"][0])
        for joint in list(self.jointDict.keys()):
            if cmds.objExists(self.jointDict[joint]["parent"]):
                cmds.parent(joint, self.jointDict[joint]["parent"])

    def getFileData(self):
        file = open(self.path, "rb")
        self.jointDict = json.load(file)
        # print self.jointDict
        file.close()

    def importData(self):
        self.getFileData()
        self.setJoints()

class nurbsControl(object):
    def __init__(self,
                 path = "",
                 ctrlRoot=""
                 ):
        #---args
        self.path                    = path
        self.ctrlRoot                = ctrlRoot
        self.ctrlDict = {}

    def getCtrls(self):
        # Find the hierarchy of joints
        allCtrls = []
        allCtrls = cmds.listRelatives(self.ctrlRoot, ad=True, typ="nurbsCurve")
        self.ctrlDict = {}
        for ctrl in allCtrls:
            data = xUtils.nurbsCurveData(name = ctrl, space=OpenMaya.MSpace.kObject).nurbsCurve
            self.ctrlDict[ctrl] = data

    def export(self):
        file = open(self.path, "wb")
        json.dump(self.ctrlDict, file, sort_keys=False, indent=2)
        file.close()

    def exportData(self):
        self.getCtrls()
        self.export()
    

    def getFileData(self):
        file = open(self.path, "rb")
        self.ctrlDict = json.load(file)
        file.close()

    def setCtrls(self):
        curveDummy = cmds.circle()[0]
        curveShape = misc.getShape(curveDummy)
        for ctrl in list(self.ctrlDict.keys()):
            # if "L_armIK_CTLSHAPE" in ctrl:
            #     print ctrl
            if not cmds.objExists(ctrl):
                continue
            curve = xUtils.create_curve_2(self.ctrlDict[ctrl], "TEMP", "AHHHHH").name()
            if not cmds.listConnections(ctrl + ".create"):
                cmds.connectAttr(curve + ".worldSpace", ctrl + ".create")
            # cmds.dgdirty(a=1)
            cmds.connectAttr(ctrl + ".worldSpace", curveShape + ".create", f=True)
            cmds.refresh()

            # misc.pushCurveShape(sourceCurve=curve, targetCurve=ctrl, mirror=False, inheritColor=True)
            # print curve
            parent = cmds.listRelatives(curve, p=True)
            cmds.delete(parent)
        cmds.delete(curveDummy)


    def importData(self):
        self.getFileData()
        self.setCtrls()
# misc.pushCurveShape()

class constraintMap(object):
    def __init__(self,
                 path = "",
                 geoRoot=""
                 ):
        #---args
        self.path                    = path
        self.geoRoot                = geoRoot
        self.constraintDict = {}

    def getgeos(self):
        # Find the hierarchy of joints
        allConstraints = []
        allConstraints = cmds.listRelatives(self.geoRoot, ad=True, typ="parentConstraint")
        self.constraintDict = {}
        for con in allConstraints:
            target = None
            geo = None
            geo = cmds.listConnections(con+".constraintRotateY", d=True)
            if not geo:
                continue
            geo = geo[0]
            target = cmds.parentConstraint(con, q=True, targetList=True)
            if not target:
                continue
            target = target[0]
            
            self.constraintDict[geo] = target
        

    def export(self):
        file = open(self.path, "wb")
        json.dump(self.constraintDict, file, sort_keys=False, indent=2)
        file.close()

    def exportData(self):
        self.getgeos()
        self.export()
    

    def getFileData(self):
        file = open(self.path, "rb")
        self.constraintDict = json.load(file)
        file.close()

    def setConstraints(self):

        for driven in list(self.constraintDict.keys()):
            if not cmds.objExists(driven) or not cmds.objExists(self.constraintDict[driven]):
                continue
            cmds.parentConstraint(self.constraintDict[driven], driven, mo=True)
            cmds.scaleConstraint(self.constraintDict[driven], driven, mo=True)

    def importData(self):
        self.getFileData()
        self.setConstraints()

class selectionSet(object):
    def __init__(self,
                 path = "",
                 ):
        #---args
        self.path                    = path
        self.setDict = {}

    def getSel(self):
        # Find the hierarchy of joints
        self.setDict = {}
        self.setDict["controls"] = []
        for sel in cmds.ls(sl=True):
            self.setDict["controls"].append(sel)

    def export(self):
        file = open(self.path, "wb")
        json.dump(self.setDict, file, sort_keys=False, indent=2)
        file.close()

    def exportData(self):
        self.getSel()
        self.export()

    def getFileData(self):
        file = open(self.path, "rb")
        self.setDict = json.load(file)
        file.close()

    def setSel(self):
        selectionFiltered = []

        for sel in self.setDict["controls"]:
            if cmds.objExists(sel):
                selectionFiltered.append(sel)
        if not cmds.objExists("controlSelectionSet"):
            self.selectionSet = cmds.sets(selectionFiltered , n="controlSelectionSet")

    def importData(self):
        self.getFileData()
        self.setSel()