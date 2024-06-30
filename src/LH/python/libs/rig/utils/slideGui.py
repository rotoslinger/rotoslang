import sys
import importlib
linux = '/scratch/levih/dev/rotoslang/lhrig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

from maya import cmds
import json
from . import faceWeights, lhDeformerExport, lhDeformerCmds, exportUtils
from . import weightingUtils
from . import slideUICmds
from rigComponents import slidingCtrl
from rigComponents import meshRivetCtrl
from rig.utils import misc
importlib.reload(misc)
importlib.reload(exportUtils)
importlib.reload(slidingCtrl)
importlib.reload(meshRivetCtrl)
importlib.reload(slideUICmds)
importlib.reload(weightingUtils)
importlib.reload(faceWeights)
importlib.reload(lhDeformerExport)
importlib.reload(lhDeformerCmds)

import maya.mel as mel

class slideDeformerGui(object):
    def __init__(self):
        #vars
        self.win                   = "SlideDeformerWindow"
        self.layout                = None
        self.column_layout         = None
        self.deformer_list         = None
        self.symmetry_dict         = None
        self.connections           = []
        self.geo_selection         = []
        self.source_selection      = []
        self.target_selection      = []
        self.geo_string            = []
        
        self.slide_weight_select_src  = []
        self.slide_weight_select_trg  = []
        self.slide_anim_curve_select_src = []
        self.slide_anim_curve_select_trg = []
        
        self.vec_weight_select_src  = []
        self.vec_weight_select_trg  = []
        self.vec_anim_curve_select_src = []
        self.vec_anim_curve_select_trg = []
        
        self.roll_weight_select_src  = []
        self.roll_weight_select_trg  = []
        self.roll_anim_curve_select_src = []
        self.roll_anim_curve_select_trg = []
        self.bake_list = None
        self.bake_layout = None
        self.bake_row = ""
        self.bake_this = ""
        self.bake_dict = {}
        self.raw_bake_dict = []
        self.undo_cache = {}
        self.undo_counter = 0
        # This initializes the weight value dragger.
        # Sets to (q) tool to avoid entering the context immediately.
        # You will want to set add cmds.setToolTo("weightValueDragger") in your hotkeys to be able to use this feature
        self.weightDragger = weightingUtils.weightValueDragger()
        self.weightDragger.clickAndMoveCommand()
        cmds.setToolTo("selectSuperContext")

    def __selectDeformerAction(self, *args):
        type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)
        if deformer:
            reloadType = cmds.checkBox(self.multiTransferOptionCheckBox, q=True, v=True)
            deformer_type = cmds.nodeType(deformer[0])
            lhDeformerCmds.refresh_paintable_attrs(deformer, deformer_type)
            self.geo_string = cmds.textFieldGrp(self.geo_filter, q = 1, text = 1)
            #---get geometry based on filter
            if self.geo_string == "":
            # if filter is empty, load all geo, otherwise, filter
                if len(deformer)>1:
                    self.geo1 = cmds.deformer(deformer[0],
                                             q = True,
                                             g = True)
                    self.geo2 = cmds.deformer(deformer[1],
                                             q = True,
                                             g = True)
                    self.geo = self.geo1+self.geo2
                    self.geo = list(set(self.geo))
                else:
                    if cmds.objectType(deformer[0]) == "LHWeightNode":
                        self.geo = cmds.listConnections(deformer[0] + ".weightedMesh")
                        if self.geo:
                            self.geo = self.geo[0]
                    else:
                        self.geo = cmds.deformer(deformer,
                                                q = True,
                                                g = True)
                #---clear it
                cmds.textScrollList(self.geo_list,
                                    e = 1, 
                                    ra = 1)
                #---fill it
                cmds.textScrollList(self.geo_list,
                                    e = 1, 
                                    append = self.geo)
                try:
                    cmds.textScrollList(self.geo_list,
                                        e = 1,
                                        selectItem = self.geo_selection)
                except:
                    pass
            else:
                #---clear it
                cmds.textScrollList(self.geo_list,
                    e = 1, 
                    ra = 1)
                deformer = cmds.textScrollList(self.deformer_list, 
                                               q = 1, 
                                               selectItem = 1)
                self.geo = cmds.deformer(deformer,
                                 q = True,
                                 g = True)
                
                self.geo_string = self.__filter(filter_string = self.geo_string,
                                                    list = self.geo)
                #---fill it
                cmds.textScrollList(self.geo_list,
                                    e = 1, 
                                    append = self.geo_string)
                try:
                    cmds.textScrollList(self.geo_list,
                                        e = 1,
                                        selectItem = self.geo_selection)
                except:
                    pass
            self.reloadWeightInfoSource()
            self.reloadWeightInfoTarget()

    def selectSourceWeightAction(self, *args):
        ""
        type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        self.__select_weights_src()
        self.__select_weights_trg()
        if type == 1:

            weights_source = cmds.textScrollList(self.weights_source_list, 
                                           q = 1, 
                                           selectItem = 1)
            deformer = cmds.textScrollList(self.deformer_list, 
                                           q = 1, 
                                           selectItem = 1)
            geo = None
            if cmds.objectType(deformer[0]) == "LHWeightNode":
                geo = cmds.listConnections(deformer[0] + ".weightedMesh")
                # if geo:
                #     geo= geo[0]
            else:
                geo = cmds.deformer(deformer,
                                        q = True,
                                        g = True)

            # geo = cmds.deformer(deformer, q=True, geometry=True)
            if geo:
                geo= geo[0]
            idx = len(weights_source)-1
            print(deformer)
            if cmds.objectType(deformer[0]) == "LHMatrixDeformer":
                geoTransform = cmds.listRelatives(geo, p=True)[0]
                self.current_weights= geo + "." + weights_source[idx]
                cmds.makePaintable("mesh", self.current_weights)
                mel.eval('artSetToolAndSelectAttr( "artAttrCtx", "mesh.' +self.current_weights+ '" );')
                self.weightDragger.weightAttr = self.current_weights
                return
            
            if cmds.objectType(deformer[0]) == "LHWeightNode":
                geoTransform = cmds.listRelatives(geo, p=True)[0]
                shape = misc.getShape(geo)
                self.current_weights= shape + "." + weights_source[idx]
                print(self.current_weights)
                print(self.current_weights)
                print(self.current_weights)
                print(self.current_weights)
                print(self.current_weights)
                cmds.makePaintable("mesh", self.current_weights)
                mel.eval('artSetToolAndSelectAttr( "artAttrCtx", "mesh.' + self.current_weights+ '" );')
                self.weightDragger.weightAttr = self.current_weights
                return




            try:
                self.current_weights= "LHSlideDeformer." + deformer[0] + "." + weights_source[idx]
            except:
                pass
            try:
                self.current_weights= "LHVectorDeformer." + deformer[0] + "." + weights_source[idx]
            except:
                pass
            try:
                self.current_weights= "LHCurveRollDeformer." + deformer[0] + "." + weights_source[idx]
            except:
                pass
            # try:
            #     self.current_weights= "LHWeightDeformer." + deformer[0] + "." + weights_source[idx]
            # except:
            #     pass
            # Check if any of the geo from the deformer is selected before switching the paint channels

            # shapes = [cmds.listRelatives(i, shapes=True)[0] for i in cmds.ls(sl=True) if cmds.ls(sl=True) and cmds.listRelatives(i, shapes=True)]
            # if any(elem in geo for elem in shapes):
            #--- if you have weightable geo selected this will work
            try:
                mel.eval('artSetToolAndSelectAttr( "artAttrCtx", "' +self.current_weights+ '" );')
            except:
                pass
            cmds.optionVar( sv=('weightName', self.current_weights) )
            self.weightDragger.weightAttr = self.current_weights
            weightingUtils.turnOffVertexColor()
        if type == 2:
            weights_source = cmds.textScrollList(self.weights_source_list, 
                                           q = 1, 
                                           selectItem = 1)
            cmds.select(weights_source)

    def __filter(self, filter_string = "", list = []):
        ""
        new = [i for i in list if filter_string in i]
        return new

    def __reload_geo(self, filter_string = "", list = []):
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)
        self.geo_string = cmds.textFieldGrp(self.geo_filter, q = 1, text = 1)
        #---get geometry based on filter
        if self.geo_string == "":
        # if filter is empty, load all geo, otherwise, filter
            self.geo = cmds.deformer(deformer,
                                     q = True,
                                     g = True)
    #                                  gi = True)
            #---clear it
            cmds.textScrollList(self.geo_list,
                                e = 1, 
                                ra = 1)
            #---fill it
            cmds.textScrollList(self.geo_list,
                                e = 1, 
                                append = self.geo)
        else:
            #---clear it
            cmds.textScrollList(self.geo_list,
                e = 1, 
                ra = 1)
            deformer = cmds.textScrollList(self.deformer_list, 
                                           q = 1, 
                                           selectItem = 1)
            self.geo = cmds.deformer(deformer,
                             q = True,
                             g = True)
            
            self.geo_string = self.__filter(filter_string = self.geo_string,
                                                list = self.geo)
            #---fill it
            cmds.textScrollList(self.geo_list,
                                e = 1, 
                                append = self.geo_string)

    def reloadWeightInfoSource(self, *args):
        self.reloadWeights(weightsTextScrollList =self.weights_source_list , filterTextGroup=self.source_filter)

    def reloadWeightInfoTarget(self, *args):
        self.reloadWeights(source=False, weightsTextScrollList = self.weights_target_list , filterTextGroup=self.target_filter)


    def reloadWeights(self, source=True, weightsTextScrollList=None,
                      filterTextGroup=None):
        flipSourceTarget = cmds.checkBox(self.flipSourceTarget, q=True, v=True)
        reloadType = cmds.checkBox(self.multiTransferOptionCheckBox, q=True, v=True)
        index = 0
        if reloadType and not source:
            index = 1
        weightType = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)
        if len(deformer) == 1:
            index = 0

        if flipSourceTarget and reloadType and index == 0 and len(deformer) > 1:
            index = 1
        elif flipSourceTarget and reloadType and index == 1:
            index = 0

        weightType = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)

        deformerType = cmds.objectType(deformer[index])
        if deformerType == "cluster":
            # filter source
            self.source_string = cmds.textFieldGrp(filterTextGroup, q = 1, text = 1)
            if self.source_string == "":
                self.names = [deformer[index] + ".Weights"]
                self.source_string = self.__filter(filter_string = self.source_string,
                                                    list = self.names)
                #---clear weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    append = self.source_string,
                                    sc =self.selectSourceWeightAction)
            return

        if deformerType == "LHWeightNode":
            # filter source
            self.source_string = cmds.textFieldGrp(filterTextGroup, q = 1, text = 1)
            if self.source_string == "":
                elemLength = cmds.getAttr(deformer[index] + ".inputs", s=True)
                self.names = []
                for elem in range(elemLength):
                    attrName = deformer[index] + ".inputs[{0}].inputWeights".format(elem)
                    con = cmds.listConnections(attrName, d=False, s=True, p =True)
                    if not con:
                        continue
                    con = con[0]
                    if cmds.objectType(con) != 'mesh':
                        print(cmds.objectType(con))
                        continue
                    attrNameCon = cmds.listConnections(attrName, p=True)
                    if not attrNameCon:
                        continue
                    attrNameCon = attrNameCon[0]
                    self.names.append(attrNameCon.split(".")[1])


                # self.names = [deformer[index] + ".matrixWeight"]   
                self.source_string = self.__filter(filter_string = self.source_string,
                                                    list = self.names)
                #---clear weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    append = self.source_string,
                                    sc =self.selectSourceWeightAction)
            return
        if deformerType == "LHMatrixDeformer":
            # filter source
            self.source_string = cmds.textFieldGrp(filterTextGroup, q = 1, text = 1)
            if self.source_string == "":
                elemLength = cmds.getAttr(deformer[index] + ".inputs", s=True)
                self.names = []
                for elem in range(elemLength):
                    attrName = deformer[index] + ".inputs[{0}].matrixWeight".format(elem)
                    con = cmds.listConnections(attrName)
                    if not con:
                        continue
                    con = con[0]
                    if cmds.objectType(con) != 'transform':
                        continue
                    attrNameCon = cmds.listConnections(attrName, p=True)
                    if not attrNameCon:
                        continue
                    attrNameCon = attrNameCon[0]
                    self.names.append(attrNameCon.split(".")[1])


                # self.names = [deformer[index] + ".matrixWeight"]   
                self.source_string = self.__filter(filter_string = self.source_string,
                                                    list = self.names)
                #---clear weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    append = self.source_string,
                                    sc =self.selectSourceWeightAction)
            return
                                       
        if weightType == 1:
            #---get weights
            attrDeformer = deformer

            if reloadType:
               attrDeformer = deformer[index]

            self.attrs = cmds.listAttr(attrDeformer, 
                                    ud = True, 
                                    a = True)
            self.names = []
            for i in range(len(self.attrs)):
                tmp_name = self.attrs[i].split(".")
                self.names.append(tmp_name[1])
            self.weight_dict = dict(list(zip(self.names,self.attrs)))
                 
            # filter source
            self.source_string = cmds.textFieldGrp(filterTextGroup, q = 1, text = 1)
            if self.source_string == "":
                #---clear weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    append = self.names,
                                    sc =self.selectSourceWeightAction)
            else:
                self.source_string = self.__filter(filter_string = self.source_string,
                                                    list = self.names)
                #---clear weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    append = self.source_string,
                                    sc =self.selectSourceWeightAction)
        if weightType == 2:
            # get curves
            animCurveAttrs = [".uAnimCurveUArray", ".uAnimCurveVArray", ".vAnimCurveUArray", ".vAnimCurveVArray",
                                ".nAnimCurveUArray", ".nAnimCurveVArray", ".tAnimCurveUArray", ".tAnimCurveVArray",
                                ".rAnimCurveVArray", ".uAnimCurveArray", ".vAnimCurveArray"]
            self.connections = []


            srcIndex = 0
            targetIndex = 1
            if flipSourceTarget and reloadType:
                srcIndex = 1
                targetIndex = 0

            if reloadType and source:
                self.getCurveAttrs(animCurveAttrs, deformer[srcIndex])
            elif not reloadType:
                self.getCurveAttrs(animCurveAttrs, deformer[srcIndex])

            if reloadType and not source and len(deformer)>1:
                self.getCurveAttrs(animCurveAttrs, deformer[targetIndex])
            elif not reloadType and len(deformer)>1:
                self.getCurveAttrs(animCurveAttrs, deformer[targetIndex])

            flat_conn = []
            for i in range(len(self.connections)):
                if self.connections[i]:
                    for j in range(len(self.connections[i])):
                        if self.connections[i][j]:
                            flat_conn.append(self.connections[i][j])
            self.connections = flat_conn
            #---filter connections
            # filter source
            self.source_string = cmds.textFieldGrp(filterTextGroup, q = 1, text = 1)
            if self.source_string == "":
                #---clear weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    append = self.connections,
                                    sc =self.selectSourceWeightAction)
            else:
                self.source_string = self.__filter(filter_string = self.source_string,
                                                    list = self.connections)
                #---clear weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(weightsTextScrollList,
                                    e = 1, 
                                    append = self.source_string,
                                    sc =self.selectSourceWeightAction)

    def getCurveAttrs(self, curveAttrs, deformer):
        for curveAttr in curveAttrs:
            if not cmds.objExists(deformer + curveAttr):
                continue
            self.connections.append(cmds.listConnections(deformer + curveAttr,
                                            type = "animCurve",
                                            d = False))

    def __findWeights(self, *args):
        cmds.textScrollList(self.deformer_list,
                            e = 1,
                            ra = 1)
        self.slideDeformers = cmds.ls(type = "LHSlideDeformer")
        self.vecDeformers = cmds.ls(type = "LHVectorDeformer")
        self.curveRollDeformers = cmds.ls(type = "LHCurveRollDeformer")
        # self.weightDeformers = cmds.ls(type = "LHWeightDeformer")
        self.clusterDeformers = cmds.ls(type = "cluster")
        self.weightNodes = cmds.ls(type = "LHWeightNode")
        self.matrixDeformers = cmds.ls(type = "LHMatrixDeformer")
        self.deformers = self.slideDeformers + self.vecDeformers + self.curveRollDeformers  + self.clusterDeformers + self.weightNodes + self.matrixDeformers
#         self.deformers.append(cmds.ls(type = "LHVectorDeformer"))

        cmds.textScrollList(self.deformer_list,
                            e = 1,
                            ra = 1)
        cmds.textScrollList(self.deformer_list,
                            e = 1,
                            append = self.deformers,
                            sc = self.__selectDeformerAction)

    def __findWeights2(self, *args):
        cmds.textScrollList(self.deformer_list2,
                            e = 1,
                            ra = 1)
        self.slideDeformers = cmds.ls(type = "LHSlideDeformer")
        self.vecDeformers = cmds.ls(type = "LHVectorDeformer")
        self.curveRollDeformers = cmds.ls(type = "LHCurveRollDeformer")
        # self.weightDeformers = cmds.ls(type = "LHWeightDeformer")
        self.deformers = self.slideDeformers + self.vecDeformers + self.curveRollDeformers
#         self.deformers.append(cmds.ls(type = "LHVectorDeformer"))

        cmds.textScrollList(self.deformer_list2,
                            e = 1,
                            ra = 1)
        cmds.textScrollList(self.deformer_list2,
                            e = 1,
                            append = self.deformers,
                            sc = self.__selectDeformerAttrAction)

    def __findWeights3(self, *args):
        cmds.textScrollList(self.deformer_list3,
                            e = 1,
                            ra = 1)
        self.slideDeformers = cmds.ls(type = "LHSlideDeformer")
        self.vecDeformers = cmds.ls(type = "LHVectorDeformer")
        self.curveRollDeformers = cmds.ls(type = "LHCurveRollDeformer")
        # self.weightDeformers = cmds.ls(type = "LHWeightDeformer")
        self.deformers = self.slideDeformers + self.vecDeformers + self.curveRollDeformers
#         self.deformers.append(cmds.ls(type = "LHVectorDeformer"))

        cmds.textScrollList(self.deformer_list3,
                            e = 1,
                            ra = 1)
        cmds.textScrollList(self.deformer_list3,
                            e = 1,
                            append = self.deformers,
                            sc = self.__selectDeformerAttrRemoveAction)
        
    def __findWeights4(self, *args):
        cmds.textScrollList(self.deformer_list4,
                            e = 1,
                            ra = 1)
        self.slideDeformers = cmds.ls(type = "LHSlideDeformer")
        self.vecDeformers = cmds.ls(type = "LHVectorDeformer")
        self.curveRollDeformers = cmds.ls(type = "LHCurveRollDeformer")
        # self.weightDeformers = cmds.ls(type = "LHWeightDeformer")
        self.deformers = self.slideDeformers + self.vecDeformers + self.curveRollDeformers
#         self.deformers.append(cmds.ls(type = "LHVectorDeformer"))

        cmds.textScrollList(self.deformer_list4,
                            e = 1,
                            ra = 1)
        cmds.textScrollList(self.deformer_list4,
                            e = 1,
                            append = self.deformers,
                            sc = self.__selectDeformerBakeAction)

    def findWeightsSlide(self, *args):
        cmds.textScrollList(self.deformer_list_slide,
                            e = 1,
                            ra = 1)
        self.slideDeformers = cmds.ls(type = "LHSlideDeformer")
        self.vecDeformers = cmds.ls(type = "LHVectorDeformer")
        self.curveRollDeformers = cmds.ls(type = "LHCurveRollDeformer")
        # self.weightDeformers = cmds.ls(type = "LHWeightDeformer")
        self.deformers = self.slideDeformers + self.vecDeformers + self.curveRollDeformers
    #         self.deformers.append(cmds.ls(type = "LHVectorDeformer"))

        cmds.textScrollList(self.deformer_list_slide,
                            e = 1,
                            ra = 1)
        cmds.textScrollList(self.deformer_list_slide,
                            e = 1,
                            append = self.deformers,
                            sc = self.selectAttrsForSlide)


    def selectAttrsForSlide(self, *args):
        self.attr_channels = []
        self.attr_names = []
        deformer = cmds.textScrollList(self.deformer_list_slide, 
                                        q = 1, 
                                        selectItem = 1)
        if deformer:
            deformer_type = cmds.nodeType(deformer[0])
            self.attr_names = cmds.listAttr(deformer, 
                                        ud = True, 
                                        s = True)
            # filter source
            self.attr_string = cmds.textFieldGrp(self.attr_filter_slide, q = 1, text = 1)
            if self.attr_string == "":
                #---clear weights from
                cmds.textScrollList(self.attr_list_slide,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.attr_list_slide,
                                    e = 1, 
                                    append = self.attr_names)
            else:
                self.attr_string = self.__filter(filter_string = self.attr_string,
                                                    list = self.attr_names)
                #---clear weights from
                cmds.textScrollList(self.attr_list_slide,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.attr_list_slide,
                                    e = 1, 
                                    append = self.attr_string)
    def getSlideData(self):
        # Only one Deformer should be selected
        deformer = cmds.textScrollList(self.deformer_list_slide, 
                                        q = 1, 
                                        selectItem = 1)[0]
        attrs = cmds.textScrollList(self.attr_list_slide, 
                                        q = 1, 
                                        selectItem = 1)
        name = cmds.textFieldGrp(self.slideNameField, q = 1, text = 1)
        slideSurf = cmds.textFieldGrp(self.slideSurfName, q = 1, text = 1)
        geoName = cmds.textFieldGrp(self.constraintGeoName, q = 1, text = 1)
        return deformer, attrs, name, slideSurf, geoName

    # for i in range(len(attrs)):
    #     # find corresponding weights, anim curves, and pivots based on attr connection
    #     coor_attrs = faceWeights.get_cooresponding_attrs(node = deformer[0], attr=attrs[i])
    #     cmds.deleteAttr(deformer[0] +"."+ attrs[i])


    def addSlideCtrl(self, *args):
        deformer, unsortedAttrs, name, slideSurf, geoName = self.getSlideData()

        print(unsortedAttrs, "UNSORTED ATTRS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        if len(unsortedAttrs) != 2:
            return
        # force the attribute order... selection order is not understood by the textScrollList
        # make sure you have u then V
        print(unsortedAttrs[0], "UNSORTED ATTRS")
        attrs = ["", ""]
        if "uValue" in cmds.listConnections(deformer + "." + unsortedAttrs[0], d=True,p=True)[0]:
            attrs[0] = unsortedAttrs[0]
        elif "vValue" in cmds.listConnections(deformer + "." + unsortedAttrs[0], d=True,p=True)[0]:
            attrs[1] = unsortedAttrs[0]
        if "uValue" in cmds.listConnections(deformer + "." + unsortedAttrs[1], d=True,p=True)[0]:
            attrs[0] = unsortedAttrs[1]
        elif "vValue" in cmds.listConnections(deformer + "." + unsortedAttrs[1], d=True,p=True)[0]:
            attrs[1] = unsortedAttrs[1]
        
        if not attrs[0] and not attrs[1]:
            attrs[0] = unsortedAttrs[0]
            attrs[1] = unsortedAttrs[1]
        # print attrs, "ATTRS"

        # print attrs
        # return
        side = "C"
        # if name is entered in the UI users must use this format L_Mouth (side_name)
        if name:
            if "_" in name:
                side = name.split("_")[0]
                name = name.split("_")[1]
        else:
            if "L_" in attrs[0]:
                side = "L"
            if "R_" in attrs[0]:
                side = "R"
            if "_" in attrs[0]:
                name = attrs[0].split("_")[1]
            if "LR" in name:
                name = name.split("LR")[0]
        componentType = cmds.radioButtonGrp(self.add_component_type, q = 1, sl = 1)
        if componentType == 1:
            slidingCtrl.Component(name=name, side=side, helperGeo = slideSurf, uOutConnectionAttr =deformer + "." + attrs[0], vOutConnectionAttr =deformer + "." + attrs[1])
            slidingCtrl.create()
        elif componentType == 2:
            # print deformer + "." + attrs[0], deformer + "." + attrs[1]
            meshRivetCtrl.Component(name=name, guide=True, side=side, normalConstraintPatch = slideSurf,
                                    txConnectionAttr = deformer + "." + attrs[0], tyConnectionAttr = deformer + "." + attrs[1], mesh = geoName, selection=True)
            meshRivetCtrl.create()



# class component(base.component):
#     def __init__(self,
#                  speedTxDefault=.1,
#                  speedTyDefault=.1,
#                  speedTzDefault=.1,
#                  curveData=None,
#                  mesh = None,
#                  translate = None,
#                  rotate = None,
#                  scale = None,
#                  guide = False,
                 
#                  txConnectionAttr=None,
#                  tyConnectionAttr=None,
#                  tzConnectionAttr=None,

#                  rxConnectionAttr=None,
#                  ryConnectionAttr=None,
#                  rzConnectionAttr=None,

#                  sxConnectionAttr=None,
#                  syConnectionAttr=None,
#                  szConnectionAttr=None,

#                  normalConstraintPatch=None,



    def normalizeSlideCtrl(self, *args):
        componentType = cmds.radioButtonGrp(self.add_component_type, q = 1, sl = 1)
        if componentType == 1:
            slidingCtrl.normalizeSlidingCtrls()
        if componentType == 2:
            misc.updateGeoConstraint()

    def mirrorSlideCtrl(self, *args):
        slidingCtrl.mirrorSlidingCtrls()

    def toggleEnvelope(self, *args):
        deformer = cmds.textScrollList(self.deformer_list_slide, 
                                        q = 1, 
                                        selectItem = 1)[0]
        envVal = cmds.getAttr(deformer + ".envelope")
        if envVal == 0:
            cmds.setAttr(deformer + ".envelope", 1)
        if envVal == 1:
            cmds.setAttr(deformer + ".envelope", 0)



    def __mirror_weights(self, *args):
        type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        side = cmds.radioButtonGrp(self.mirror_side, q = 1, sl = 1)
        if side == 1:
            side = "L"
        if side == 2:
            side = "R"
        if type == 1:
            deformer = cmds.textScrollList(self.deformer_list, 
                                           q = 1, 
                                           selectItem = 1)
            geo = cmds.textScrollList(self.geo_list, 
                                           q = 1, 
                                           selectItem = 1)
            tmp_weights_source = cmds.textScrollList(self.weights_source_list, 
                                           q = 1, 
                                           selectItem = 1)
            weights_source = []
    
            if cmds.objectType(deformer) == "LHMatrixDeformer":
                weightAttr = geo[0] + "." + tmp_weights_source[0]
                faceWeights.mirror_double_array_attrs(source = tmp_weights_source,
                                                      geo = geo[0],
                                                      side = side,
                                                        )
                return

            for i in tmp_weights_source:
                weights_source.append(self.weight_dict.get(i))
    
            if deformer:
                try:
                    cmds.setAttr(deformer[0]+".envelope", 0)
                except:
                    pass
                if geo:
                    if weights_source:
                        for i in range(len(geo)):
                            geo_tmp = cmds.deformer(deformer, q = True, g = True)
                            index_tmp = cmds.deformer(deformer, q = True, gi = True)
                            geo_dict = dict(list(zip(geo_tmp,index_tmp)))
                            for j in range(len(weights_source)):
                                index = geo_dict.get(geo[i])
                                weights_split = weights_source[j].split(".")
                                faceWeights.mirror_double_array_attrs(source = deformer[0] 
                                                                      +"."
                                                                      + weights_split[0]
                                                                      +"["
                                                                      +str(index)
                                                                      +"]."
                                                                      +weights_split[1],
                                                                      geo = geo[i],
                                                                      side = side,
                                                                      )
                try:
                    cmds.setAttr(deformer[0]+".envelope", 1)
                except:
                    pass
        if type == 2:
            weights_source = cmds.textScrollList(self.weights_source_list, 
                                           q = 1, 
                                           selectItem = 1)
            center_frame = cmds.textFieldGrp(self.axis_frame, q = 1, text = 1)
            center_frame = int(center_frame)
            for i in weights_source:
                faceWeights.mirror_anim_curves(anim_curve = i, 
                                               side = side, 
                                               center_frame = center_frame, 
                                               flip = False)

    def getWeightAttributes(self, deformerName):
        sourceAttrs = cmds.listAttr(deformerName, 
                        ud = True, 
                        a = True,
                        m=True)

        sourceWeightNames = []
        for i in range(len(sourceAttrs)):
            tmp_name = sourceAttrs[i].split(".")
            sourceWeightNames.append(tmp_name[1])
        return dict(list(zip(sourceWeightNames,sourceAttrs)))


    def __copy_weights(self, *args):
        reloadType = cmds.checkBox(self.multiTransferOptionCheckBox, q=True, v=True)
        weightType = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        if reloadType and weightType == 1:
            flipSourceTarget = cmds.checkBox(self.flipSourceTarget, q=True, v=True)

            deformer = cmds.textScrollList(self.deformer_list, 
                                            q = 1, 
                                            selectItem = 1)
            sourceIdx = 0
            targetIdx = 1
            if flipSourceTarget:
                sourceIdx = 1
                targetIdx = 0

            srcMesh = cmds.deformer(deformer[sourceIdx], q = True, g = True)[0]
            destMesh = cmds.deformer(deformer[targetIdx], q = True, g = True)[0]

            sourceWeights = self.getWeightAttributes(deformer[sourceIdx])
            destWeights = self.getWeightAttributes(deformer[targetIdx])

            tmp_source = cmds.textScrollList(self.weights_source_list, 
                                q = 1, 
                                selectItem = 1)[0]
            source = sourceWeights.get(tmp_source)

            tmp_target = cmds.textScrollList(self.weights_target_list, 
                                           q = 1, 
                                           selectItem = 1)
            target = []
            for i in tmp_target:
                target.append(destWeights.get(i))

            exportUtils.lhDeformerWeightTransfer(srcMesh, deformer[sourceIdx], destMesh, deformer[targetIdx], srcAttributes=[source], destAttrs=target)

            


        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)
        geo = cmds.textScrollList(self.geo_list, 
                                       q = 1, 
                                       selectItem = 1)
        if weightType == 1:
            tmp_source = cmds.textScrollList(self.weights_source_list, 
                                           q = 1, 
                                           selectItem = 1)[0]
            source = self.weight_dict.get(tmp_source)

            tmp_target = cmds.textScrollList(self.weights_target_list, 
                                           q = 1, 
                                           selectItem = 1)
            target = []

            for i in tmp_target:
                target.append(self.weight_dict.get(i))

            flip = cmds.checkBoxGrp(self.copy_options, 
                                        q = 1, 
                                         v1 = True)
            invert = cmds.checkBoxGrp(self.copy_options, 
                                        q = 1, 
                                         v2 = True)
            if deformer:
                if geo:
                    if source:
                        if target:
                            for i in range(len(geo)):
                                geo_tmp = cmds.deformer(deformer[0], q = True, g = True)
                                index_tmp = cmds.deformer(deformer[0], q = True, gi = True)
                                geo_dict = dict(list(zip(geo_tmp,index_tmp)))
                                index = geo_dict.get(geo[i])
                                weights_split = source.split(".")
                                tmp_target = []
                                src_deformer = deformer[0]
                                trg_deformer = deformer[0]

                                # sourceAttr = src_deformer + "." + weights_split[0] + "[" + str(index) + "]." + weights_split[1]
                                # sourceWeights = cmds.getAttr(sourceAttr)


                                if len(deformer)>1:
                                    trg_deformer = deformer[1]
                                for j in range(len(target)):
                                    targets_split = target[j].split(".")
                                    tmp_target.append(trg_deformer 
                                                      +"."
                                                      + targets_split[0]
                                                      +"["
                                                      +str(index)
                                                      +"]."
                                                      +targets_split[1],
                                                      )

                                    # sourceAttr = src_deformer + "." + weights_split[0] + "[" + str(index) + "]." + weights_split[1]
                                    sourceAttr = tmp_target[j]
                                    sourceWeights = cmds.getAttr(sourceAttr)


                                faceWeights.copy_double_array_weights(source = src_deformer
                                                                      +"."
                                                                      + weights_split[0]
                                                                      +"["
                                                                      +str(index)
                                                                      +"]."
                                                                      +weights_split[1],
                                                                      target = tmp_target,
                                                                      invert = invert,
                                                                      flip = flip,
                                                                      symmetry_dict = self.symmetry_dict
                                                                      )
        if weightType == 2:
            flip = cmds.checkBoxGrp(self.copy_options, 
                                        q = 1, 
                                         v1 = True)
            weights_source = cmds.textScrollList(self.weights_source_list, 
                                           q = 1, 
                                           selectItem = 1)[0]
            side = cmds.radioButtonGrp(self.mirror_side, q = 1, sl = 1)
            weights_target = cmds.textScrollList(self.weights_target_list, 
                                                 q = 1, 
                                                 selectItem = 1)
            center_frame = cmds.textFieldGrp(self.axis_frame, q = 1, text = 1)
            center_frame = int(center_frame)
            for i in weights_target:
                faceWeights.copy_flip_anim_curves(source = weights_source,
                                                  target = i,
                                                  side = side,
                                                  center_frame = center_frame, 
                                                  flip = flip)

    def __establish_symmetry(self, *args):
        geo = cmds.textScrollList(self.geo_list, 
                                       q = 1, 
                                       selectItem = 1)[0]
        if geo:
            self.symmetry_dict = faceWeights.create_symmetric_partners( geo = geo).symmetry_dict

    def __import_file_browser(self, *args):

        self.import_path = str(cmds.fileDialog2(fm = 1,
                                                ff = "LHDeformer Files (*.sld *.vec *.crd)")[0])
        cmds.textFieldGrp(self.import_file, e = True, text=self.import_path)

    def __export_file_browser(self, *args):
        self.export_path = str(cmds.fileDialog2(fm = 0,
                                                ff = "LHDeformer Files (*.sld *.vec *.crd)")[0])
        cmds.textFieldGrp(self.export_file, e = True, text=self.export_path)

    def __import(self, *args):
        
        arg_1 = cmds.checkBox( self.import_args_1, q = True, v = True)
        arg_2 = cmds.checkBox( self.import_args_2, q = True, v = True)
        arg_3 = cmds.checkBox( self.import_args_3, q = True, v = True)
        arg_4 = cmds.checkBox( self.import_args_4, q = True, v = True)
        
        self.import_args_1 = cmds.checkBox( label='Create Geo', v =True)
        self.import_args_2 = cmds.checkBox( label='Create Deformer', v =True)
        self.import_args_3 = cmds.checkBox( label='Set Anim Curves', v =True)
        self.import_args_4 = cmds.checkBox( label='Set Weights', v =True)

        if self.import_path:
            lhDeformerExport.import_slide_deformer(path = self.import_path,
                                                      create_geo = arg_1,
                                                      create_deformer = arg_2,
                                                      set_curves = arg_3,
                                                      set_weights = arg_4)

    def __export(self, *args):
        if self.export_path:
            deformer = cmds.textScrollList(self.deformer_list, 
                                           q = 1, 
                                           selectItem = 1)[0]
            lhDeformerExport.export_slide_deformer(name = deformer,path = self.export_path)

    def __add_weights(self, *args):
        ""
        # get deformer
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)[0]
        # get deformer type
        deformer_type = cmds.nodeType(deformer)
        geo = cmds.textScrollList(self.geo_list, 
                               q = 1, 
                               selectItem = 1)
        if deformer:
            if geo:
                if deformer_type:
                    if deformer_type == "LHSlideDeformer":
                            ""
                            arg1 = False
                            arg2 = False
                            arg3 = False
                            
                            args = cmds.radioButtonGrp(self.slide_deformer_options, q = 1, sl = 1)
                            if args == 1:
                                arg1 = True
                            if args == 2:
                                arg2 = True
                            if args == 3:
                                arg3 = True
                            names = cmds.textFieldGrp(self.weight_name, q = 1, text = 1)
                            if "," in names:
                                names = names.split(",")
                                names = [str(x.replace(" ", "")) if " " in x else str(x) for x in names]
                            else:
                                names = [str(names)]
                            lhDeformerCmds.add_weights(deformer_type = deformer_type,
                                                       deformer = deformer,
                                                       names = names,
                                                       geoms = geo,
                                                       uWeights = arg1,
                                                       vWeights = arg2,
                                                       nWeights = arg3)
                            
                    elif deformer_type == "LHVectorDeformer":
                        arg1 = False
                        arg2 = False
                        
                        args = cmds.radioButtonGrp(self.vector_deformer_options, q = 1, sl = 1)
                        if args == 1:
                            arg1 = True
                        if args == 2:
                            arg2 = True
                        names = cmds.textFieldGrp(self.weight_name, q = 1, text = 1)
                        if "," in names:
                            names = names.split(",")
                            names = [str(x.replace(" ", "")) if " " in x else str(x) for x in names]
                        else:
                            names = [str(names)]
                        lhDeformerCmds.add_weights(deformer_type = deformer_type,
                                                   deformer = deformer,
                                                   names = names,
                                                   geoms = geo,
                                                   tWeights = arg1,
                                                   rWeights = arg2)
                    elif deformer_type == "LHCurveRollDeformer":
                        names = cmds.textFieldGrp(self.weight_name, q = 1, text = 1)
                        if "," in names:
                            names = names.split(",")
                            names = [str(x.replace(" ", "")) if " " in x else str(x) for x in names]
                        else:
                            names = [str(names)]
                        lhDeformerCmds.add_weights(deformer_type = deformer_type,
                                                   deformer = deformer,
                                                   names = names,
                                                   geoms = geo,
                                                   rollWeights = True)

    def __add_geo(self, *args):
        ""

    def __select_geo(self, *args):
        self.geo_selection = cmds.textScrollList(self.geo_list,
                                                 q = True, 
                                                 selectItem = True)

    def __select_weights_src(self, *args):
        self.type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        if self.type == 1:
            self.slide_weight_select_src = cmds.textScrollList(self.weights_source_list,
                                                         q = True, 
                                                         selectItem = True)
#                                                          sc =self.selectSourceWeightAction)
        if self.type == 2:
            self.slide_anim_curve_select_src = cmds.textScrollList(self.weights_source_list,
                                                             q = True, 
                                                             selectItem = True)

    def __select_weights_trg(self, *args):
        
        self.type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        if self.type == 1:
            self.slide_weight_select_trg = cmds.textScrollList(self.weights_target_list,
                                                         q = True, 
                                                         selectItem = True)
#                                                          sc =self.selectSourceWeightAction)
        if self.type == 2:
            self.slide_anim_curve_select_trg = cmds.textScrollList(self.weights_target_list,
                                                             q = True, 
                                                             selectItem = True)

    def __set_weights(self, *args):
        value = cmds.textFieldGrp(self.value, q = 1, text = 1)
        operation = cmds.radioButtonGrp(self.operation, q = True,sl = True)
        value = float(value)
        if cmds.optionVar(exists='weightName') == 1:
            weightAttr = cmds.optionVar(q='weightName')
            weightAttrSplit = weightAttr.split(".")
            #---get deformer
            deformer = weightAttr.split(".")[1]
            geo = cmds.deformer(deformer, q = True, g = True)
            geoTransform = [cmds.listRelatives(i,parent = True)[0] for i in geo]
            #---make sure selected are points, and are in the deformer
            selected = cmds.ls(sl = True, fl = True)
            vtx = [i for i in selected if ".vtx[" in i]
            cv = [i for i in selected if ".cv[" in i]
            points = vtx + cv
            finalPoints = []
            
            weightAttrs = []
            allWeightValues = []
            for i in range(len(geoTransform)):
                weightAttrs.append(weightAttrSplit[1]+"."+weightAttrSplit[2] + "s["+str(i)+"]." + weightAttrSplit[2])
                allWeightValues.append(cmds.getAttr(weightAttrs[i]))
            
            final_points_indexes = []
            initial_values = []
            for i in range(len(geoTransform)):
                tmp_final_idx = []
                tmp_value = []
                for j in range(len(points)):
                    if geoTransform[i] in points[j]:
                        finalPoints.append(points[j])
                        idx = points[j].split("[")[1]
                        idx = int(idx.split("]")[0])
                        tmp_final_idx.append(idx)
                        tmp_value.append(allWeightValues[i][idx])
                final_points_indexes.append(tmp_final_idx)
                initial_values.append(tmp_value)
            for i in range(len(geoTransform)):
                for j in range(len(final_points_indexes[i])):
                    if operation == 1:
                        allWeightValues[i][final_points_indexes[i][j]] = value
                    if operation == 2:
                        allWeightValues[i][final_points_indexes[i][j]] = initial_values[i][j]+value
                    if operation == 3:
                        allWeightValues[i][final_points_indexes[i][j]] = initial_values[i][j]*value
                    if operation == 4:
                        if initial_values[i][j] != 0:
                            if value != 0:
                                allWeightValues[i][final_points_indexes[i][j]] = initial_values[i][j]/value
            for i in range(len(allWeightValues)):
                cmds.setAttr(weightAttrs[i],allWeightValues[i], typ='doubleArray')
            self.setVertexColorsToWeightVals()

    def __copy_point_weights(self, *args):
        if cmds.optionVar(exists='weightName') == 1:
            weightAttr = cmds.optionVar(q='weightName')
            weightAttrSplit = weightAttr.split(".")
            #---get deformer
            deformer = weightAttr.split(".")[1]
            geo = cmds.deformer(deformer, q = True, g = True)
            geoTransform = [cmds.listRelatives(i,parent = True)[0] for i in geo]
            #---make sure selected are points, and are in the deformer
            selected = cmds.ls(sl = True, fl = True)
            vtx = [i for i in selected if ".vtx[" in i]
            cv = [i for i in selected if ".cv[" in i]
            points = vtx + cv
            finalPoints = []
            
            weightAttrs = []
            allWeightValues = []
            for i in range(len(geoTransform)):
                weightAttrs.append(weightAttrSplit[1]+"."+weightAttrSplit[2] + "s["+str(i)+"]." + weightAttrSplit[2])
                allWeightValues.append(cmds.getAttr(weightAttrs[i]))
            
            final_points_indexes = []
            initial_values = []
            for i in range(len(geoTransform)):
                tmp_final_idx = []
                tmp_value = []
                for j in range(len(points)):
                    if geoTransform[i] in points[j]:
                        finalPoints.append(points[j])
                        idx = points[j].split("[")[1]
                        idx = int(idx.split("]")[0])
                        tmp_final_idx.append(idx)
                        tmp_value.append(allWeightValues[i][idx])
                final_points_indexes.append(tmp_final_idx)
                initial_values.append(tmp_value)
            final_weight = []
            for i in range(len(initial_values)):
                for j in range(len(initial_values[i])):
                    final_weight.append(initial_values[i][j])
            if len(final_weight) != 0:
                self.copied_weight = sum(final_weight)/len(final_weight)

    def __paste_point_weights(self, *args):
        
        if self.copied_weight:
            value = self.copied_weight
            if cmds.optionVar(exists='weightName') == 1:
                weightAttr = cmds.optionVar(q='weightName')
                weightAttrSplit = weightAttr.split(".")
                #---get deformer
                deformer = weightAttr.split(".")[1]
                geo = cmds.deformer(deformer, q = True, g = True)
                geoTransform = [cmds.listRelatives(i,parent = True)[0] for i in geo]
                #---make sure selected are points, and are in the deformer
                selected = cmds.ls(sl = True, fl = True)
                vtx = [i for i in selected if ".vtx[" in i]
                cv = [i for i in selected if ".cv[" in i]
                points = vtx + cv
                finalPoints = []
                
                weightAttrs = []
                allWeightValues = []
                for i in range(len(geoTransform)):
                    weightAttrs.append(weightAttrSplit[1]+"."+weightAttrSplit[2] + "s["+str(i)+"]." + weightAttrSplit[2])
                    allWeightValues.append(cmds.getAttr(weightAttrs[i]))
                
                final_points_indexes = []
                initial_values = []
                for i in range(len(geoTransform)):
                    tmp_final_idx = []
                    tmp_value = []
                    for j in range(len(points)):
                        if geoTransform[i] in points[j]:
                            finalPoints.append(points[j])
                            idx = points[j].split("[")[1]
                            idx = int(idx.split("]")[0])
                            tmp_final_idx.append(idx)
                            tmp_value.append(allWeightValues[i][idx])
                    final_points_indexes.append(tmp_final_idx)
                    initial_values.append(tmp_value)
            for i in range(len(geoTransform)):
                for j in range(len(final_points_indexes[i])):
                    allWeightValues[i][final_points_indexes[i][j]] = value
            for i in range(len(allWeightValues)):
                cmds.setAttr(weightAttrs[i],allWeightValues[i], typ='doubleArray')

    def __selectDeformerAttrAction(self, *args):
        self.attr_channels = []
        self.attr_names = []
        deformer = cmds.textScrollList(self.deformer_list2, 
                                       q = 1, 
                                       selectItem = 1)
        if deformer:
            deformer_type = cmds.nodeType(deformer[0])
            self.attr_names = cmds.listAttr(deformer, 
                                       ud = True, 
                                       s = True)
            # filter source
            self.attr_string = cmds.textFieldGrp(self.attr_filter, q = 1, text = 1)
            if self.attr_string == "":
                #---clear weights from
                cmds.textScrollList(self.attr_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.attr_list,
                                    e = 1, 
                                    append = self.attr_names)
            else:
                self.attr_string = self.__filter(filter_string = self.attr_string,
                                                    list = self.attr_names)
                #---clear weights from
                cmds.textScrollList(self.attr_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.attr_list,
                                    e = 1, 
                                    append = self.attr_string)

    def __selectDeformerAttrRemoveAction(self, *args):
        self.attr_channels = []
        self.attr_names = []
        deformer = cmds.textScrollList(self.deformer_list3, 
                                       q = 1, 
                                       selectItem = 1)
        if deformer:
            deformer_type = cmds.nodeType(deformer[0])
            self.attr_names = cmds.listAttr(deformer, 
                                       ud = True, 
                                       s = True)
            # filter source
            self.attr_string = cmds.textFieldGrp(self.attr_filter2, q = 1, text = 1)
            if self.attr_string == "":
                #---clear weights from
                cmds.textScrollList(self.attr_list2,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.attr_list2,
                                    e = 1, 
                                    append = self.attr_names)
            else:
                self.attr_string = self.__filter(filter_string = self.attr_string,
                                                    list = self.attr_names)
                #---clear weights from
                cmds.textScrollList(self.attr_list2,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.attr_list2,
                                    e = 1, 
                                    append = self.attr_string)

    def __rename_attrs(self, *args):
        # get selected deformer
        deformer = cmds.textScrollList(self.deformer_list2, 
                                       q = 1, 
                                       selectItem = 1)
        # get search for
        search_string = cmds.textFieldGrp(self.search_for, q = 1, text = 1)
        # get replace with
        replace_string = cmds.textFieldGrp(self.replace_with, q = 1, text = 1)
        if replace_string:
            # get selection type 
            type = cmds.radioButtonGrp(self.selection_type, q = 1, sl = 1)
            # if selected deformer
            attrs = []
            if type == 1:
                bloated_attrs = []
                # all attrs for selected deformer
                for i in range(len(deformer)):
                    tmp_attrs = cmds.listAttr(deformer[i], 
                                              ud = True, 
                                              s = True)
                    bloated_attrs.append(tmp_attrs)
                for i in range(len(bloated_attrs)):
                    for j in range(len(bloated_attrs[i])):
                        attrs.append(bloated_attrs[i][j])
    
            if type == 2:
                # get selected attrs
                attrs = cmds.textScrollList(self.attr_list, 
                                               q = 1, 
                                               selectItem = 1)
    
            deformer_types = []
            full_attrs = []
            for i in range(len(deformer)):
                for j in range(len(attrs)):
                    if cmds.objExists(deformer[i] + "." + attrs[j]):
                        full_attrs.append(deformer[i] + "." + attrs[j])
                        deformer_types.append(cmds.nodeType(deformer[i]))
            # get attr connections
            
            attr_connections = []
            for i in range(len(full_attrs)):
                tmp_connections = cmds.listConnections(full_attrs[i], s = False, p = True)
                if not tmp_connections == None:
                    attr_connections.append(tmp_connections[0])
                else:
                    attr_connections.append("dummy")
            attr_type = []
            for i in range(len(full_attrs)):
                if attr_connections[i] != "dummy":
                    tmp = attr_connections[i].split(".")
                    attr_type.append(tmp[1][0])
                else:
                    attr_type.append("dummy")
            weight_attrs = []
            u_anim_curves = []
            v_anim_curves = []
            pivots = []
            for i in range(len(full_attrs)):
                if not full_attrs[i] == "dummy":
                    tmp = full_attrs[i].split(".")
                    # find corresponding weights, anim curves, and pivots based on attr connection
                    coor_attrs = faceWeights.get_cooresponding_attrs(node = tmp[0], attr=tmp[1])
                    # get_cooresponding_attrs(node = "C_mouth_SLD", attr="L_TLipPinchLR")
#                     weight_attrs.append(coor_attrs.weight_attr)
#                     u_anim_curves.append(coor_attrs.u_anim_curve)
#                     v_anim_curves.append(coor_attrs.v_anim_curve)
#                     pivots.append(coor_attrs.pivot)
                    search_final = ""
                    if not search_string:
                        search_final = tmp[1]
                    else:
                        search_final = search_string
                    if coor_attrs.end == 0:
                        if search_string in full_attrs[i]:
                            new_attr = tmp[1].replace(search_final, replace_string)
                            new_weight = new_attr + "Weight"
                            new_u_anim = new_attr + "_ACV"
                            new_v_anim = new_attr + "Falloff_ACV"
                            new_pivot = ""
                            if deformer_types[i] == "LHVectorDeformer":
                                new_pivot = new_attr + "Pivot_CRV"

                            check = 1

                            if cmds.attributeQuery(new_attr, node = tmp[0], ex = True):
                                print("attribute " + new_attr + " already exists please try a different name")
                                check = 0
                            if cmds.attributeQuery(new_weight, node = tmp[0], ex = True):
                                print("attribute " + new_weight + " already exists please try a different name")
                                check = 0
                            if cmds.objExists(new_u_anim):
                                print(new_u_anim + " already exists please try a different name")
                                check = 0
                            if cmds.objExists(new_v_anim):
                                print(new_v_anim + " already exists please try a different name")
                                check = 0
                            if cmds.objExists(new_pivot):
                                print(new_pivot + " already exists please try a different name")
                                check = 0

                            if check == 1:
                                
                                cmds.renameAttr( full_attrs[i], new_attr )
                                faceWeights.rename_weight_attrs(node = tmp[0], old = coor_attrs.weight_attr, new = new_weight)
                                cmds.rename( coor_attrs.u_anim_curve, new_u_anim )
                                cmds.rename( coor_attrs.v_anim_curve, new_v_anim )
                                if deformer_types[i] == "LHVectorDeformer":
                                    cmds.rename( coor_attrs.pivot, new_pivot )
                                self.__selectDeformerAttrAction()

    def __delete_attrs(self, *args):
        ""
        deformer = cmds.textScrollList(self.deformer_list3, 
                                       q = 1, 
                                       selectItem = 1)
        attrs = cmds.textScrollList(self.attr_list2, 
                                       q = 1, 
                                       selectItem = 1)
        for i in range(len(attrs)):
            # find corresponding weights, anim curves, and pivots based on attr connection
            coor_attrs = faceWeights.get_cooresponding_attrs(node = deformer[0], attr=attrs[i])
            cmds.deleteAttr(deformer[0] +"."+ attrs[i])
            if coor_attrs.end == 0:
                parent = cmds.attributeQuery(coor_attrs.weight_attr, node = deformer[0], lp = True)
                cmds.deleteAttr(deformer[0] +"."+ parent[0])
                cmds.delete(coor_attrs.u_anim_curve)
                cmds.delete(coor_attrs.v_anim_curve)
                if coor_attrs.pivot:
                    cmds.delete(coor_attrs.pivot)
                    
        self.__selectDeformerAttrRemoveAction()
#             print coor_attrs.u_anim_curve, coor_attrs.v_anim_curve, coor_attrs.weight_attr, coor_attrs.pivot, 
            # get_cooresponding_attrs(node = "C_mouth_SLD", attr="L_TLipPinchLR")

    def __selectDeformerBakeAction(self, *args):
        if cmds.objectTypeUI(self.bake_row, isType = "rowColumnLayout"):
            cmds.deleteUI(self.bake_row)

        deformer = cmds.textScrollList(self.deformer_list4, 
                                       q = 1, 
                                       selectItem = 1)
        if deformer:
            deformer_type = cmds.nodeType(deformer[0])
#             print deformer_type
            self.attr_names = cmds.listAttr(deformer, 
                                       ud = True, 
                                       s = True)
            # filter source
            self.attr_string = cmds.textFieldGrp(self.attr_filter3, q = 1, text = 1)
            if self.attr_string == "":
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
                    min = -1.0
                    tween = 2
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [55,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts))
                    self.raw_bake_dict.append(tmp)
                    # if dictionary key for attr name exists set the value(if key in dict)

                
            else:
                self.attr_string = self.__filter(filter_string = self.attr_string,
                                                    list = self.attr_names)
                self.attr_names = self.attr_string
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
                    min = -1.0
                    tween = 2
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [55,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts
                                          ))

                    self.raw_bake_dict.append(tmp)                
            self.__get_bake_dicts()
    def __set_all_max_bake(self, *args):
        if cmds.objectTypeUI(self.bake_row, isType = "rowColumnLayout"):
            cmds.deleteUI(self.bake_row)
        max = cmds.floatFieldGrp(self.set_all_max, 
                                       q = 1, 
                                       value1 = True)
        print("maxBake")
        deformer = cmds.textScrollList(self.deformer_list4, 
                                       q = 1, 
                                       selectItem = 1)
        if deformer:
            deformer_type = cmds.nodeType(deformer[0])
#             print deformer_type
            self.attr_names = cmds.listAttr(deformer, 
                                       ud = True, 
                                       s = True)
            # filter source
            self.attr_string = cmds.textFieldGrp(self.attr_filter3, q = 1, text = 1)
            if self.attr_string == "":
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
#                     max = 1.0
                    min = -1.0
                    tween = 2
#                     if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
#                         max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [80,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts))
                    self.raw_bake_dict.append(tmp)
                    # if dictionary key for attr name exists set the value(if key in dict)
                self.__get_bake_dicts()
                self.__selectDeformerBakeAction()
            else:
                self.attr_string = self.__filter(filter_string = self.attr_string,
                                                    list = self.attr_names)
                self.attr_names = self.attr_string
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
#                     max = 1.0
                    min = -1.0
                    tween = 2
#                     if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
#                         max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [80,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts
                                          ))

                    self.raw_bake_dict.append(tmp)   

    def __set_all_min_bake(self, *args):
        if cmds.objectTypeUI(self.bake_row, isType = "rowColumnLayout"):
            cmds.deleteUI(self.bake_row)
#         print "minBake"
        min = cmds.floatFieldGrp(self.set_all_min, 
                                       q = 1, 
                                       value1 = True)
        deformer = cmds.textScrollList(self.deformer_list4, 
                                       q = 1, 
                                       selectItem = 1)
        if deformer:
            deformer_type = cmds.nodeType(deformer[0])
#             print deformer_type
            self.attr_names = cmds.listAttr(deformer, 
                                       ud = True, 
                                       s = True)
            # filter source
            self.attr_string = cmds.textFieldGrp(self.attr_filter3, q = 1, text = 1)
            if self.attr_string == "":
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
#                     min = -1.0
                    tween = 2
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
#                     if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
#                         min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [80,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts))
                    self.raw_bake_dict.append(tmp)
                    # if dictionary key for attr name exists set the value(if key in dict)
#                 self.__get_bake_dicts()
                self.__get_bake_dicts()
                self.__selectDeformerBakeAction()
            else:
                self.attr_string = self.__filter(filter_string = self.attr_string,
                                                    list = self.attr_names)
                self.attr_names = self.attr_string
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
#                     min = -1.0
                    tween = 2
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
#                     if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
#                         min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [80,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts
                                          ))

                    self.raw_bake_dict.append(tmp)   
                self.__get_bake_dicts()
                self.__selectDeformerBakeAction()

    def __set_all_tween_bake(self, *args):
        if cmds.objectTypeUI(self.bake_row, isType = "rowColumnLayout"):
            cmds.deleteUI(self.bake_row)
#         print "tweenBake"
        tween = cmds.intFieldGrp(self.set_all_tween, 
                                       q = 1, 
                                       value1 = True)
        
        deformer = cmds.textScrollList(self.deformer_list4,  
                                       q = 1, 
                                       selectItem = 1)
        if deformer:
            deformer_type = cmds.nodeType(deformer[0])
#             print deformer_type
            self.attr_names = cmds.listAttr(deformer, 
                                       ud = True, 
                                       s = True)
            # filter source
            self.attr_string = cmds.textFieldGrp(self.attr_filter3, q = 1, text = 1)
            if self.attr_string == "":
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
                    min = -1.0
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [80,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts))
                    self.raw_bake_dict.append(tmp)
                    # if dictionary key for attr name exists set the value(if key in dict)
#                 self.__get_bake_dicts()
                self.__get_bake_dicts()
                self.__selectDeformerBakeAction()
            else:
                self.attr_string = self.__filter(filter_string = self.attr_string,
                                                    list = self.attr_names)
                self.attr_names = self.attr_string
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
                    min = -1.0
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,80],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [80,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts
                                          ))

                    self.raw_bake_dict.append(tmp)   
                self.__get_bake_dicts()
                self.__selectDeformerBakeAction()

    def __undo_bake_dict(self, *args):
        if self.undo_counter > 1:
            self.undo_counter += -1
            self.bake_dict = self.undo_cache.get(self.undo_counter)
        else:
            print("Nothing left to undo")
#         print "UNDO"
        if cmds.objectTypeUI(self.bake_row, isType = "rowColumnLayout"):
            cmds.deleteUI(self.bake_row)

        deformer = cmds.textScrollList(self.deformer_list4, 
                                       q = 1, 
                                       selectItem = 1)
        if deformer:
            deformer_type = cmds.nodeType(deformer[0])
#             print deformer_type
            self.attr_names = cmds.listAttr(deformer, 
                                       ud = True, 
                                       s = True)
            # filter source
            self.attr_string = cmds.textFieldGrp(self.attr_filter3, q = 1, text = 1)
            if self.attr_string == "":
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
                    min = -1.0
                    tween = 2
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [55,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts))
                    self.raw_bake_dict.append(tmp)
                    # if dictionary key for attr name exists set the value(if key in dict)
#                 self.__get_bake_dicts()
                
            else:
                self.attr_string = self.__filter(filter_string = self.attr_string,
                                                    list = self.attr_names)
                self.attr_names = self.attr_string
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
                    min = -1.0
                    tween = 2
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [55,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts
                                          ))

                    self.raw_bake_dict.append(tmp)                
#                 self.__get_bake_dicts()

    def __redo_bake_dict(self, *args):
        if self.undo_counter < 20:
            self.undo_counter += 1
            self.bake_dict = self.undo_cache.get(self.undo_counter)
        else:
            print("Nothing to redo")
            
        if cmds.objectTypeUI(self.bake_row, isType = "rowColumnLayout"):
            cmds.deleteUI(self.bake_row)

        deformer = cmds.textScrollList(self.deformer_list4, 
                                       q = 1, 
                                       selectItem = 1)
        if deformer:
            deformer_type = cmds.nodeType(deformer[0])
#             print deformer_type
            self.attr_names = cmds.listAttr(deformer, 
                                       ud = True, 
                                       s = True)
            # filter source
            self.attr_string = cmds.textFieldGrp(self.attr_filter3, q = 1, text = 1)
            if self.attr_string == "":
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
                    min = -1.0
                    tween = 2
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [55,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts))
                    self.raw_bake_dict.append(tmp)
                    # if dictionary key for attr name exists set the value(if key in dict)
#                 self.__get_bake_dicts()
                
            else:
                self.attr_string = self.__filter(filter_string = self.attr_string,
                                                    list = self.attr_names)
                self.attr_names = self.attr_string
                cmds.setParent(self.bake_layout)
                self.bake_row = cmds.rowColumnLayout( numberOfColumns=4 )
                self.raw_bake_dict = []
                for i in range(len(self.attr_names)):
                    tmp = []
                    tmp.append(deformer[0])
                    tmp.append(self.attr_names[i])
                    cmds.text(self.attr_names[i], w = 120, al = "left")
                    max = 1.0
                    min = -1.0
                    tween = 2
                    if deformer[0] + "." + self.attr_names[i] + ".max" in self.bake_dict:
                        max = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".max")
                    if deformer[0] + "." + self.attr_names[i] + ".min" in self.bake_dict:
                        min = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".min")
                    if deformer[0] + "." + self.attr_names[i] + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(deformer[0] + "." + self.attr_names[i] + ".tween")
                    tmp.append(cmds.floatFieldGrp( label='Min:',
                                        numberOfFields=1,
                                         value1= min,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.floatFieldGrp( label='Max:',
                                        numberOfFields=1,
                                        value1= max,
                                           cw2 = [30,70],
                                           cal = [(1,"center"),(2,"center")],
                                           cc = self.__get_bake_dicts))
                    tmp.append(cmds.intFieldGrp( label='Betweens:',
                                          numberOfFields=1,
                                          value1= tween,
                                          cw2 = [55,30],
                                          cal = [(1,"center"),(2,"center")],
                                          cc = self.__get_bake_dicts
                                          ))

                    self.raw_bake_dict.append(tmp)                    
#                 self.__get_bake_dicts()

    def __get_bake_dicts(self,*args):
        if self.undo_counter == 30:
            self.undo_counter = 0
        else:   
            self.undo_counter += 1
#         print self.undo_counter
        # get deformers
        lh_deformers = []
        lh_deformers.append(cmds.ls(type = "LHSlideDeformer"))
        lh_deformers.append(cmds.ls(type = "LHVectorDeformer"))
        lh_deformers.append(cmds.ls(type = "LHCurveRollDeformer"))
        flat = []
        if lh_deformers:
            for i in range(len(lh_deformers)):
                if lh_deformers[i]:
                    for j in range(len(lh_deformers[i])):
                        if lh_deformers[i][j]:
                            flat.append(lh_deformers[i][j])
        lh_deformers = flat
        
        # get attributes
        lh_attrs = []
        min_val = []
        max_val = []
        tween_val = []
        for i in range(len(lh_deformers)):
            tmp = cmds.listAttr(lh_deformers[i], 
                                ud = True, 
                                s = True)
            for j in tmp:
                if j:
                    if lh_deformers[i] + "." + j + ".max" in self.bake_dict:
                        max = self.bake_dict.get(lh_deformers[i] + "." + j + ".max")
                        self.bake_dict[lh_deformers[i] + "." + j + ".max"] = max
                    else:
                        self.bake_dict[lh_deformers[i] + "." + j + ".max"] = 1
                        
                    if lh_deformers[i] + "." + j + ".min" in self.bake_dict:
                        min = self.bake_dict.get(lh_deformers[i] + "." + j + ".min")
                        self.bake_dict[lh_deformers[i] + "." + j + ".min"] = min

                    else:
                        self.bake_dict[lh_deformers[i] + "." + j + ".min"] = -1
                        
                    if lh_deformers[i] + "." + j + ".tween" in self.bake_dict:
                        tween = self.bake_dict.get(lh_deformers[i] + "." + j + ".tween")
                        self.bake_dict[lh_deformers[i] + "." + j + ".tween"] = tween

                    else:
                        self.bake_dict[lh_deformers[i] + "." + j + ".tween"] = 2
                    
        for i in range(len(self.raw_bake_dict)):
            key_min = self.raw_bake_dict[i][0] + "." +self.raw_bake_dict[i][1] + ".min"
            key_max = self.raw_bake_dict[i][0] + "." +self.raw_bake_dict[i][1] + ".max"
            key_tween = self.raw_bake_dict[i][0] + "." +self.raw_bake_dict[i][1] + ".tween"
            min = cmds.floatFieldGrp(self.raw_bake_dict[i][2], q = True, value1 = True)
            max = cmds.floatFieldGrp(self.raw_bake_dict[i][3], q = True, value1 = True)
            tween = cmds.intFieldGrp(self.raw_bake_dict[i][4], q = True, value1 = True)

            self.bake_dict[key_max] = max
            self.bake_dict[key_min] = min
            self.bake_dict[key_tween] = tween
        self.undo_cache[self.undo_counter] = self.bake_dict

    def __import_bake_file_browser(self, *args):

        self.bake_import_path = str(cmds.fileDialog2(fm = 1,
                                                ff = "LHAttrBake Files (*.lhb)")[0])
        cmds.textFieldGrp(self.import_bake_file, e = True, text=self.bake_import_path)

    def __export_bake_file_browser(self, *args):
#         print " establish symmetry"
        self.bake_export_path = str(cmds.fileDialog2(fm = 0,
                                                ff = "LHAttrBake Files (*.lhb)")[0])
        cmds.textFieldGrp(self.export_bake_file, e = True, text=self.bake_export_path)

    def __export_bake_dicts(self,*args):
        # write the bake dictionaries to a file
        if self.bake_export_path:
            file = open(self.bake_export_path, "wb")
            json.dump(self.bake_dict, file, sort_keys = True, indent = 2)
            file.close()

    def __import_bake_dicts(self,*args):
        # import the bake dictionaries from a file
        if self.bake_import_path:
            file = open(self.bake_import_path, "rb")
            self.bake_dict = json.load(file)
            file.close()
            self.__selectDeformerBakeAction()

    def __bake(self,*args):
        # import the bake dictionaries from a file
        # unpack bake dict
        attrs = []
        attr_mins = []
        attr_maxs = []
        num_inbetweens = []
#         print self.bake_dict
        # get attrs first
#         count = 0
        for i in self.bake_dict:
            split = i.split(".")
            attrs.append(split[0] + "." + split[1])
        # get rid of duplicats
        attrs = list(set(attrs))
        for i in range(len(attrs)):
            attr_mins.append(self.bake_dict.get(attrs[i] + ".min"))
            attr_maxs.append(self.bake_dict.get(attrs[i] + ".max"))
            num_inbetweens.append(self.bake_dict.get(attrs[i] + ".tween"))
            print(attr_mins[i], attr_maxs[i],num_inbetweens[i])
#             print attrs[count]
#             count += 1

        # get geometry for each deformer, then do blendshape for that geometry
        count = 0
        for i in range(len(attrs)):
#             if "SLD" in attrs[i]:
#                 name = ""
#                 if "Lip" in attrs[i]:
#                     name = "Lip"
#                 else:
#                     name = "Mouth"
            lhDeformerCmds.bake_blendshape(geo = "C_body_HI",
#                                            name = name,
                                           attr = attrs[i],
                                           attr_min = attr_mins[i],
                                           attr_max = attr_maxs[i],
                                           num_inbetweens = num_inbetweens[i])
            print(count)
            count += 1


    def setVertexColorsToWeightVals(self):
        if cmds.checkBoxGrp(self.weightDraggerSettings, q=True, v1=True):
            allWeightValues = weightingUtils.getAllWeightValues(self.current_weights)[0]
            weightingUtils.setVertexColorsToWeightValue(allWeightValues, True)


    def callWeightAverageWithArgs(self, *args):
        averageVal = cmds.textFieldGrp(self.averageValue, q=1, text=1)
        print(averageVal)
        weightingUtils.weightAverageAll(self.current_weights, int(averageVal))
        self.setVertexColorsToWeightVals()

    def callWeightAverageSelectionBorder(self, *args):
        weightingUtils.weightAverageSelectionBorder(self.current_weights)
        self.setVertexColorsToWeightVals()

    def queryFlattenVals(self):
        flattenX = cmds.checkBoxGrp(self.averageWeightsBounds, q=True, v1=True)
        flattenY = cmds.checkBoxGrp(self.averageWeightsBounds, q=True, v2=True)
        flattenZ = cmds.checkBoxGrp(self.averageWeightsBounds, q=True, v3=True)
        return flattenX, flattenY, flattenZ

    def callAverageBetween2Points(self, *args):
        # flattenX, flattenY, flattenz = self.queryFlattenVals()
        weightingUtils.averageBetweenPoints(self.current_weights,
                                                    # flattenX,
                                                    # flattenY,
                                                    # flattenz
                                                    )
        self.setVertexColorsToWeightVals()

    def callGradientBetween2Points(self, *args):
        calcDefVal = cmds.checkBox(self.checkBoxDeform, query=True, v=True)
        # flattenX, flattenY, flattenz = self.queryFlattenVals()
        weightingUtils.gradientBetweenPoints(self.current_weights,
                                                     # flattenX,
                                                     # flattenY,
                                                     # flattenz,
                                                     calcDefVal)
        self.setVertexColorsToWeightVals()

    def updateVertexColorToggle(self, *args):
        self.weightDragger.vertexColorWeightVis = cmds.checkBoxGrp(self.weightDraggerSettings, q=True, v1=True)
        self.weightDragger.toggleVisOnDrag = cmds.checkBoxGrp(self.weightDraggerSettings, q=True, v2=True)


    def turnOnVertexWeightColors(self, *args):
        weightingUtils.turnOnVertexColor(self.current_weights)

    def __createUiElements(self):
        if cmds.window(self.win, ex = 1):
            cmds.deleteUI(self.win)

        self.win = cmds.window("SlideDeformerWindow")
        cmds.scrollLayout( 'scrollLayout' )
        self.layout_main = cmds.columnLayout(adjustableColumn=True)

        ###########################################################
        #---Deformer Info Frame
        ###########################################################

        cmds.setParent(self.layout_main)
        self.frame1 = cmds.frameLayout(label = "Get Deformer Info",
                                       collapsable = True,
                                       collapse = False)
        self.layout = cmds.rowColumnLayout(nc = 2)
        #---row 1
        self.get_deformers = cmds.button(label = "Get LH Deformers", 
                                                c = self.__findWeights,
                                                h = 30)
        cmds.text("Geo")
        
        
#         self.layout = cmds.rowColumnLayout(nc = 1)
        self.weight_type = cmds.radioButtonGrp(label = "Weight Type:", 
                                   labelArray2=['Painted', 'Anim Curve'], 
                                   numberOfRadioButtons = 2,
                                   sl = 1,
                                   cw3 = [80,70,30],
                                   cal = [(1,"left"),(2,"left"),(3,"left")],
                                   onc = self.__selectDeformerAction
                                   )
        self.geo_filter = cmds.textFieldGrp( label='Geo Filter', text='',
                                       cw2 = [60,180],
                                       cal = [(1,"left"),(2,"left")],
                                       tcc = self.__reload_geo)

#         self.layout = cmds.rowColumnLayout(nc = 4)
        ###########################################################
        #---Weight Info Frame
        ###########################################################
        

        self.deformer_list = cmds.textScrollList( numberOfRows = 8,
                                                  allowMultiSelection = 1,
                                                  h = 200)
        self.geo_list = cmds.textScrollList( numberOfRows = 8,
                                             allowMultiSelection = 1,
                                             h = 200,
                                             sc = self.__select_geo)
        cmds.setParent(self.layout_main)
        self.frame2 = cmds.frameLayout(label = "Get Weights Info",
                                       collapsable = True,
                                       collapse = False)
        self.layout = cmds.rowColumnLayout(nc = 2)
        cmds.text("Weights Source")
        cmds.text("Weights Target")
        self.source_filter = cmds.textFieldGrp( label='Source Filter', text='',
                                       cw2 = [70,180],
                                       cal = [(1,"left"),(2,"left")],
                                       tcc = self.reloadWeightInfoSource)
        self.target_filter = cmds.textFieldGrp( label='Target Filter', text='',
                                       cw2 = [70,180],
                                       cal = [(1,"left"),(2,"left")],
                                       tcc = self.reloadWeightInfoTarget)
        self.weights_source_list = cmds.textScrollList( numberOfRows = 8,
                                                      allowMultiSelection = 1,
                                                      h = 200,
                                                      sc = self.__select_weights_src
                                                      )
        self.weights_target_list = cmds.textScrollList( numberOfRows = 8,
                                                    allowMultiSelection = 1,
                                                    h = 200,
                                                    sc = self.__select_weights_trg
                                                    )
#         self.layout = cmds.rowColumnLayout(nc = 1,)
        cmds.text("")
        cmds.text(" ")
        cmds.text("  ")
        # self.layoutForMultiTransfer = cmds.rowColumnLayout(nc = 4)
        cmds.setParent(self.layout_main)
        self.flipSourceTarget = cmds.checkBox( label='Flip Source and target',
                                                  w=80, al="right", value=False, cc=self.__selectDeformerAction )

        self.multiTransferOptionCheckBox = cmds.checkBox( label='Load Different Deformers in Source and Target',
                                                  w=80, al="right", value=False)
        
        ###########################################################
        #---Weight Calculator Frame
        ###########################################################
        cmds.setParent(self.layout_main)
        # cmds.textFieldGrp(label='Weight Dragger Settings', text='0.0',
        #                   cw2=[70, 180],
        #                   cal=[(1, "left"), (2, "left")])

        self.weightDraggerSettings = cmds.checkBoxGrp(numberOfCheckBoxes=3,
                                                      label='Weight Dragger Settings',
                                                      labelArray3=['Vertex Weight Vis',
                                                                   'Toggle Vis on Drag',
                                                                   'Vertex Weight Switch'],
                                                      cw5=[80,80,80,80, 80],
                                                      cal=[(1, "right"), (1, "left"), (3, "left")],
                                                      valueArray3=[False, False, False],
                                                      cc=self.updateVertexColorToggle,
                                                      onCommand3=self.turnOnVertexWeightColors,
                                                      offCommand3=weightingUtils.turnOffVertexColor
                                                      )

        cmds.setParent(self.layout_main)
        self.frame4 = cmds.frameLayout(label = "Weight Calculator",
                                       collapsable = True,
                                       collapse = True)
        
        cmds.setParent(self.frame4)
        
        #---buttons
        self.layout = cmds.rowColumnLayout(nc = 2)
        self.value = cmds.textFieldGrp( label='Value', text='0.0',
                                       cw2 = [70,180],
                                       cal = [(1,"left"),(2,"left")])
#                                        tcc = self.__reload_source)
        self.set_pw = cmds.button(label = "Set Weight",
                                        c = self.__set_weights,
                                         w = 100)
        cmds.setParent(self.frame4)
        self.layout = cmds.rowColumnLayout(nc = 2)
        self.operation = cmds.radioButtonGrp(label = "Operation", 
                                           labelArray4=['Set',
                                                        'Sum',
                                                        'Multiply',
                                                        'Divide'], 
                                           numberOfRadioButtons = 4,
                                            sl = 1,
                                           cw5 = [80,80,80,80,80],
                                           cal = [(1,"left"),(2,"left"),(3,"left")]
                                           )
        cmds.setParent(self.frame4)
        self.copy_pw = cmds.button(label = "Copy",
                                        c = self.__copy_point_weights,
                                         w = 100)
        cmds.text("Select one or more point")
        #---copy
        self.paste_pw = cmds.button(label = "Paste",
                                        c = self.__paste_point_weights,
                                       w = 200)

        cmds.text("Select one or more point")
        self.layout = cmds.rowColumnLayout(nc = 2)
        if not hasattr(self, "current_weights"):
            self.current_weights = ""
        self.averageValue = cmds.textFieldGrp(label='Average Factor', text='4',
                                       cw2=[90, 180],
                                       cal=[(1, "left"), (2, "left")])
        self.weightAverageButton = cmds.button(label="AverageWeights",
                                               c=self.callWeightAverageWithArgs,
                                               w=100)
        self.layout = cmds.rowColumnLayout(nc = 2)

        cmds.setParent(self.frame4)
        self.weightAverageButton = cmds.button(label="Average Weights Selection Border",
                                               c=self.callWeightAverageSelectionBorder,
                                               w=200)
        cmds.text("Average weights for the border of an island of verts")




        cmds.setParent(self.frame4)
        cmds.text("#####################################################################################")
        cmds.text("  Bounds Weighting Commands  ")
        cmds.text("#####################################################################################")

        # self.averageWeightsBounds = cmds.checkBoxGrp(numberOfCheckBoxes=3,
        #                                              label='Bounds Axis',
        #                                              labelArray3=['FlattenX',
        #                                                           'FlattenY',
        #                                                           'FlattenZ'],
        #                                              cw5 = [80,80,80,80, 80],
        #                                              cal = [(1,"left"),(2,"left"),(3,"left")],
        #                                              valueArray3=[False, True, False]
        #
        #                                              )
        # cmds.text("Use these check boxes to flatten the bounds search in an axis")
        # cmds.text("If you want bounds to have a more horizontal average, flatten Y if vertical, flatten X")

        self.averageBetweenMinMaxPoint = cmds.button(label="Average Between Two Points",
                                               c=self.callAverageBetween2Points,
                                               w=200)
        cmds.text("Finds the min and max point in selected points and sets the average weight of those two points")

        self.gradientBetweenMinMaxPoint = cmds.button(label="Gradient Between Two Points",
                                               c=self.callGradientBetween2Points,
                                               # cw2=[90, 180],
                                               # cal=[(1, "left"), (2, "left")],
                                               w=100)
        self.checkBoxDeform = cmds.checkBox(label="Calculate Gradient Deformed", w=200)

        cmds.text("Finds the min and max point in selected points and sets a weight gradient those two points")


        cmds.text("#####################################################################################")
        cmds.text("  End Bounds  ")
        cmds.text("#####################################################################################")



        # self.operation = cmds.radioButtonGrp(label = "Flatten Axis",
        #                                    labelArray3=['FlattenX',
        #                                                 'FlattenX',
        #                                                 'FlattenX'],
        #                                    numberOfRadioButtons = 3,
        #                                     sl = 1,
        #                                    cw5 = [80,80,80,80],
        #                                    cal = [(1,"left"),(2,"left"),(3,"left")]
        #                                    )




        ###########################################################
        #---Weight Groups Frame
        ###########################################################
        
        cmds.setParent(self.layout_main)
        self.frame3 = cmds.frameLayout(label = "Copy Weight Groups",
                                       collapsable = True,
                                       collapse = True)
        cmds.setParent(self.frame3)
        #---buttons
        self.mirror_button = cmds.button(label = "Mirror",
                                         c = self.__mirror_weights,
                                         w = 100)
        self.mirror_side = cmds.radioButtonGrp(label = "Side", 
                                           labelArray2=['L', 'R'], 
                                           numberOfRadioButtons = 2,
                                           sl = 1,
                                           cw3 = [40,40,30],
                                           cal = [(1,"left"),(2,"left"),(3,"left")]
                                           )
        self.axis_frame = cmds.textFieldGrp( label='Axis Frame', text='0',
                                       cw2 = [60,40],
                                       cal = [(1,"left"),(2,"left")])
        cmds.text("Select geo and one or more from the Weights Source")
        #---copy
        self.copy_button = cmds.button(label = "Copy",
                                       c = self.__copy_weights,
                                       w = 200)
        self.copy_options = cmds.checkBoxGrp(numberOfCheckBoxes=2, 
                                            label='Options', 
                                            labelArray2=['Flip', 'Invert Values'],
                                           cw3 = [50,50,30],
                                           cal = [(1,"left"),(2,"left"),(3,"left")]
                                            )
        cmds.text("Select a Weights Source and multiple from" +
                  " Weights Target")
        self.symmetry_button = cmds.button(label = "Establish Symmetry",
                                 c = self.__establish_symmetry,
                                 w = 200)
        cmds.text("Select geo: Needed to flip weights")
        
        
        
        ###########################################################
        #---Add attrs frame
        ###########################################################
        
        cmds.setParent(self.layout_main)
        self.frame2 = cmds.frameLayout(label = "Add Deformer Attributes",
                                       collapsable = True,
                                       collapse = True)
        cmds.setParent(self.frame2)
        #---buttons
        self.weight_name = cmds.textFieldGrp( label='Weight Name:', text='',
                                       cw2 = [80,430],
                                       cal = [(1,"left"),(2,"left")])
#         cmds.text('''Type a string or list of strings to add: "example" or ["example1", "example2"]''')
        self.slide_deformer_options = cmds.radioButtonGrp(numberOfRadioButtons=3, 
                                            label='Slide Weight Type:', 
                                            labelArray3=['uWeight', 'vWeight', "nWeight"],
                                           cw4 = [130,100,100,100],
                                           cal = [(1,"left"),(2,"left"),(3,"left"),(4,"left")]
                                            )
        
        self.vector_deformer_options = cmds.radioButtonGrp(numberOfRadioButtons=2, 
                                            label='Vector Weight Type:', 
                                            labelArray2=['tWeight', 'rWeight'],
                                           cw3 = [130,100,100],
                                           cal = [(1,"left"),(2,"left"),(3,"left")]
                                            )

        
        self.add_weights = cmds.button(label = "Add Weights",
                                         c = self.__add_weights,
                                         w = 100)
#         cmds.text('''Select deformer and geometry you want to add weight to, then press "Add Weights" button''')

        #---buttons
        self.geo_name = cmds.textFieldGrp( label='Geo Name:', text='',
                                       cw2 = [80,430],
                                       cal = [(1,"left"),(2,"left")])
        self.add_geo = cmds.button(label = "Add Geometry",
                                         c = self.__add_geo,
                                         w = 100)


        ###########################################################
        #---Rename Deformer Attr Frame
        ###########################################################

        cmds.setParent(self.layout_main)
        self.frame7 = cmds.frameLayout(label = "Rename Deformer Attrs",
                                       collapsable = True,
                                       collapse = True)
        self.layout54 = cmds.rowColumnLayout(nc = 2)
        #---row 1
        self.get_deformers2 = cmds.button(label = "Get LH Deformers", 
                                                c = self.__findWeights2,
                                                h = 30)
        cmds.text("Attrs")

        cmds.text("Deformers")
        
        
#         self.layout = cmds.rowColumnLayout(nc = 1)
        self.attr_filter = cmds.textFieldGrp( label='Attr Filter', text='',
                                       cw2 = [60,180],
                                       cal = [(1,"left"),(2,"left")],
                                        tcc = self.__selectDeformerAttrAction
                                       )
        
        self.deformer_list2 = cmds.textScrollList( numberOfRows = 8,
                                                  allowMultiSelection = False,
                                                  h = 200)
        self.attr_list = cmds.textScrollList( numberOfRows = 8,
                                             allowMultiSelection = True,
                                             h = 200,
#                                              sc = self.__select_geo
                                             )
        cmds.setParent(self.frame7)
        self.layout3 = cmds.rowColumnLayout(nc = 1)
        cmds.text("Rename Attributes")
        self.search_for = cmds.textFieldGrp( label='Search For:', text='',
                                       cw2 = [80,430],
                                       cal = [(1,"left"),(2,"left")],
#                                         tcc = self.__selectDeformerAttrAction
                                       )
        self.replace_with = cmds.textFieldGrp( label='Replace With:', text='',
                                       cw2 = [80,430],
                                       cal = [(1,"left"),(2,"left")],
#                                         tcc = self.__selectDeformerAttrAction
                                       )
        self.selection_type = cmds.radioButtonGrp(label = "", 
                                           labelArray2=['Selected Deformer', 'Selected Attribute'], 
                                           numberOfRadioButtons = 2,
                                           sl = 2,
                                           cw3 = [80,120,120],
                                           cal = [(1,"left"),(2,"left"),(3,"left")]
                                           )
        
        cmds.text("WARNING: Undo not supported, save before renaming")
        self.rename_button = cmds.button(label = "Rename", 
                                                c = self.__rename_attrs,
                                                h = 30)
        
        


        cmds.setParent(self.layout_main)

        
        
        ###########################################################
        #---Edit Deformer Frame
        ###########################################################

        cmds.setParent(self.layout_main)
        self.frame88 = cmds.frameLayout(label = "Edit Deformer Attrs",
                                       collapsable = True,
                                       collapse = True)
        self.layout32 = cmds.rowColumnLayout(nc = 2)
        #---row 1
        self.get_deformers3 = cmds.button(label = "Get LH Deformers", 
                                                c = self.__findWeights3,
                                                h = 30)
        cmds.text("Attrs")

        cmds.text("Deformers")
        
        
#         self.layout = cmds.rowColumnLayout(nc = 1)
        self.attr_filter2 = cmds.textFieldGrp( label='Attr Filter', text='',
                                       cw2 = [60,180],
                                       cal = [(1,"left"),(2,"left")],
                                        tcc = self.__selectDeformerAttrRemoveAction
                                       )
        
        self.deformer_list3 = cmds.textScrollList( numberOfRows = 8,
                                                  allowMultiSelection = False,
                                                  h = 200)
        self.attr_list2 = cmds.textScrollList( numberOfRows = 8,
                                             allowMultiSelection = True,
                                             h = 200,
#                                              sc = self.__select_geo
                                             )
        cmds.setParent(self.frame88)
        self.layout45 = cmds.rowColumnLayout(nc = 1)

        self.remove_button = cmds.button(label = "Remove Selected Attributes", 
                                                c = self.__delete_attrs,
                                                h = 30, w = 520)
        cmds.text(" ")

        cmds.setParent(self.layout_main)

        
        ###########################################################
        #---add Slide Controls Frame
        ###########################################################

        cmds.setParent(self.layout_main)
        
        # self.addComponentType = cmds.checkBox( label='Flip Source and target',
        #                                     w=80, al="right", value=False, cc=self.__selectDeformerAction )

        self.addSlideCtrlFrame = cmds.frameLayout(label = "Add Slide Ctrls",
                                       collapsable = True,
                                       collapse = True)
        self.slideCtrlLayout = cmds.rowColumnLayout(nc = 2)
        #---row 1
        self.get_deformers_slide = cmds.button(label = "Get LH Deformers", 
                                                c = self.findWeightsSlide,
                                                h = 30)
        cmds.text("Attrs")

        cmds.text("Deformers")
        
        
#         self.layout = cmds.rowColumnLayout(nc = 1)
        self.attr_filter_slide = cmds.textFieldGrp( label='Attr Filter', text='',
                                       cw2 = [60,180],
                                       cal = [(1,"left"),(2,"left")],
                                        tcc = self.selectAttrsForSlide
                                       )
        

        self.deformer_list_slide = cmds.textScrollList( numberOfRows = 8,
                                                  allowMultiSelection = False,
                                                  h = 200)
        self.attr_list_slide = cmds.textScrollList( numberOfRows = 8,
                                             allowMultiSelection = True,
                                             h = 200,
#                                              sc = self.__select_geo
                                             )
        cmds.setParent(self.addSlideCtrlFrame)
        self.layoutSlide = cmds.rowColumnLayout(nc = 1)
        self.add_component_type = cmds.radioButtonGrp(label = "Type:", 
                            labelArray2=['Slide Ctrl', 'Stick Ctrl'], 
                            numberOfRadioButtons = 2,
                            sl = 2,
                            cw3 = [80,70,30],
                            cal = [(1,"left"),(2,"left"),(3,"left")],
                            onc = self.addComponentTypeAction
                            )


        self.slideSurfaceInstruction = cmds.text("Enter the surface that will be used to slide on")
        self.slideSurfName = cmds.textFieldGrp( label='Surf Name', text='C_mouthSurface_EX',
                                cw2 = [100,180],
                                cal = [(1,"left"),(2,"left")],
                                )



        cmds.text("Enter side and name ex: L_mouth ")
        cmds.text("If not entered will try to automatically name")
        self.slideNameField = cmds.textFieldGrp( label='Ctrl Name', text='',
                                cw2 = [100,180],
                                cal = [(1,"left"),(2,"left")],
                                )
        self.constraintGeoInstruction = cmds.text("For Stick Controls")
        self.constraintGeoInstruction = cmds.text("Enter the geo that will be used to constrain the control")
        self.constraintGeoName = cmds.textFieldGrp( label='Geo Name', text='C_body_HI',
                                cw2 = [100,180],
                                cal = [(1,"left"),(2,"left")],
                                )


        cmds.text("Select LR attr first, then UD attr (U Parameter followed by V Parameter)")
        self.addSelectedButton = cmds.button(label = "Add Ctrl", 
                                                c = self.addSlideCtrl,
                                                h = 30, w = 520)

        cmds.text("Toggle Envelope for placing controls")
        self.toggleEnvelopeButton = cmds.button(label = "Toggle Envelope", 
                                        c = self.toggleEnvelope,
                                        h = 30, w = 520)
        cmds.text("Set Control to neutral position")
        self.normalizeSlideButton = cmds.button(label = "Update Nuetral Pose", 
                                        c = self.normalizeSlideCtrl,
                                        h = 30, w = 520)
        cmds.text("Select Slide Ctrl on L or R side and run to mirror")
        self.mirrorWeights = cmds.checkBox( label='Mirror Weights',
                                                  w=80, al="right", value=False )
        self.mirrorSlideButton = cmds.button(label = "Mirror Slide Control", 
                                        c = self.mirrorSlideCtrl,
                                        h = 30, w = 520)

        cmds.text(" ")

        cmds.setParent(self.layout_main)

#         ###########################################################
#         #---Bake Deformer Frame
#         ###########################################################

#         cmds.setParent(self.layout_main)
#         self.bake_frame = cmds.frameLayout(label = "Bake Deformer",
#                                        collapsable = True,
#                                        collapse = True)
# #         self.layout33 = cmds.rowColumnLayout(nc = 1)
#         #---row 1
#         self.get_deformers4 = cmds.button(label = "Get LH Deformers", 
#                                                 c = self.__findWeights4,
#                                                 h = 30)
#         self.deformer_list4 = cmds.textScrollList( numberOfRows = 8,
#                                                   allowMultiSelection = False,
#                                                   h = 100)
#         self.attr_filter3 = cmds.textFieldGrp( label='Attr Filter', text='',
#                                        cw2 = [60,180],
#                                        cal = [(1,"left"),(2,"left")],
#                                         tcc = self.__selectDeformerBakeAction
#                                        )
#         cmds.text("WARNING: set all values will set values for all currently visible attributes UNDO IS NOT SUPPORTED")
#         self.bake_row3 = cmds.rowColumnLayout( numberOfColumns=6)
#         cmds.text(" Set All Values", w = 120, al = "left")

        
#         self.set_all_min = cmds.floatFieldGrp( label='  Min: ',
#                                                numberOfFields=1,
#                                                value1= 1,
#                                                cw2 = [30,70],
#                                                cal = [(1,"center"),(2,"center")],
#                                                cc = self.__set_all_min_bake
#                                                )
        
#         self.set_all_max = cmds.floatFieldGrp( label='  Max: ',
#                                                numberOfFields=1,
#                                                value1= 1,
#                                                cw2 = [30,70],
#                                                cal = [(1,"center"),(2,"center")],
#                                                cc = self.__set_all_max_bake
#                                                )

#         self.set_all_tween = cmds.intFieldGrp( label='  Betweens: ',
#                                                   numberOfFields=1,
#                                                   value1= 2,
#                                                   cw2 = [55,30],
#                                                   cal = [(1,"center"),(2,"center")],
#                                                   cc = self.__set_all_tween_bake
# #                                                   vcc = self.__set_all_tween_bake
#                                                   )
# #         self.undo_btn = cmds.button(label = "Set All",
# # #                                         c = self.__export_bake_dicts,
# #                                         w = 80)
# #         self.bake_row = cmds.rowColumnLayout( numberOfColumns=6)
# #         self.bake_row2 = cmds.rowColumnLayout( numberOfColumns=6, cat = [1,"left",10000], co = [1,"right",1000])
# #         cmds.setParent(self.bake_frame)
# #         self.bake_row2 = cmds.rowColumnLayout( numberOfColumns=2, co = [(1,"left",429)])
# # 
# #         cmds.text("            ")
# #         cmds.text("           ")
# #         cmds.text("          ")
# #         cmds.text("        ")

# #         self.undo_btn = cmds.button(label = "Undo",
# #                                         c = self.__undo_bake_dict,
# #                                         w = 40)
# #         self.redo_btn = cmds.button(label = "Redo",
# #                                         c = self.__redo_bake_dict,
# #                                         w = 40)
#         cmds.setParent(self.bake_frame)
        
#         self.bake_layout = cmds.scrollLayout(horizontalScrollBarThickness=16,
#                                              verticalScrollBarThickness=16,
#                                              h = 200)
#         self.bake_row4 = cmds.rowColumnLayout( numberOfColumns=3 )

        
        
        
#         cmds.setParent(self.bake_frame)
#         self.export_bake_frame = cmds.frameLayout(label = "Export Bake",
#                                        collapsable = True,
#                                        collapse = False)
        
        
# #         self.layout = cmds.rowColumnLayout(nc = 2)

#         self.export_bake_row = cmds.rowColumnLayout(nc = 2)
#         self.export_bake_file = cmds.textFieldGrp( label='File', text='',
#                                        cw2 = [40,360],
#                                        cal = [(1,"left"),(2,"left")])
# #                                        tcc = self.__reload_source)
#         self.export_bake_btn = cmds.button(label = "Browse",
#                                         c = self.__export_bake_file_browser,
#                                          w = 100)
#         self.export_bake_row = cmds.rowColumnLayout(nc = 1)
#         cmds.setParent(self.export_bake_frame)
        
#         self.export_bake_btn = cmds.button(label = "Export Bake Values",
#                                         c = self.__export_bake_dicts,
#                                        w = 200)




#         cmds.setParent(self.bake_frame)
        
#         self.import_bake_frame = cmds.frameLayout(label = "Import Bake",
#                                        collapsable = True,
#                                        collapse = False)
#         self.export_bake_row = cmds.rowColumnLayout(nc = 2)
#         self.import_bake_file = cmds.textFieldGrp( label='File', text='',
#                                                    cw2 = [40,360],
#                                                    cal = [(1,"left"),(2,"left")])
#         self.import_bake_button = cmds.button(label = "Browse",
#                                               c = self.__import_bake_file_browser,
#                                               w = 100)
#         self.export_bake_row = cmds.rowColumnLayout(nc = 1)
#         cmds.setParent(self.import_bake_frame)
        
#         self.import_bake_btn = cmds.button(label = "Import Bake Values",
#                                         c = self.__import_bake_dicts,
#                                        w = 200)
#         self.bake_btn = cmds.button(label = "Bake all deformers",
#                                 c = self.__bake,
#                                w = 200)

        
# #         self.bake_layout = cmds.rowColumnLayout(nc = 1)
# #         self.bake_list = cmds.scrollLayout(horizontalScrollBarThickness=16,
# #                                  verticalScrollBarThickness=16, h = 200,
# #                                  width = 520)
# #         cmds.rowColumnLayout( numberOfColumns=3 )
        
# #         for i in range(200):
# #             cmds.text()
# #             cmds.intField()
# #             cmds.intSlider()        
# #         self.attr_channels = []
# #         self.attr_names = []
#         cmds.setParent(self.layout_main)
        
        ###########################################################
        #---Import Deformers
        ###########################################################
     
        cmds.setParent(self.layout_main)
        self.frame5 = cmds.frameLayout(label = "Import Deformer",
                                       collapsable = True,
                                       collapse = True)
        self.layout = cmds.rowColumnLayout(nc = 2)
        self.import_file = cmds.textFieldGrp( label='File', text='',
                                       cw2 = [40,360],
                                       cal = [(1,"left"),(2,"left")])
#                                        tcc = self.__reload_source)
        self.import_btn = cmds.button(label = "Browse",
                                        c = self.__import_file_browser,
                                         w = 100)
        cmds.setParent(self.frame5)

        self.import_args_1 = cmds.checkBox( label='Create Geo', v =True)
        self.import_args_2 = cmds.checkBox( label='Create Deformer', v =True)
        self.import_args_3 = cmds.checkBox( label='Set Anim Curves', v =True)
        self.import_args_4 = cmds.checkBox( label='Set Weights', v =True)


        #---buttons
        self.import_btn = cmds.button(label = "Import",
                                        c = self.__import,
                                         w = 100)
        
        
        ###########################################################
        #---Export Deformers
        ###########################################################
     
        cmds.setParent(self.layout_main)
        self.frame6 = cmds.frameLayout(label = "Export Deformer",
                                       collapsable = True,
                                       collapse = True)

        self.layout = cmds.rowColumnLayout(nc = 2)
        self.export_file = cmds.textFieldGrp( label='File', text='',
                                       cw2 = [40,360],
                                       cal = [(1,"left"),(2,"left")])
#                                        tcc = self.__reload_source)
        self.export_btn = cmds.button(label = "Browse",
                                        c = self.__export_file_browser,
                                         w = 100)
        cmds.setParent(self.frame6)
        self.export_btn = cmds.button(label = "Export",
                                        c = self.__export,
                                       w = 200)
#         cmds.text("Select one or more point")
    def addComponentTypeAction(self, *args):
        componentType = cmds.radioButtonGrp(self.add_component_type, q = 1, sl = 1)
        print(componentType)
        if componentType == 1:
            cmds.text(self.slideSurfaceInstruction, e=True, label = "Enter the surface that will be used to slide on")
        if componentType == 2:
            cmds.text(self.slideSurfaceInstruction, e=True, label = "Enter the surface that will be used to aim at")

    def show(self):
        self.__createUiElements()
        cmds.showWindow(self.win)



