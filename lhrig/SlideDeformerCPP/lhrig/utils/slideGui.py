import sys
linux = '/corp/projects/eng/lharrison/workspace/levi_harrison_test/lhrig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts/lhrig"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "mac" in os:
    os = mac
sys.path.append(os)

from maya import cmds
from utils import faceWeights, slideDeformerExport
reload(faceWeights)
reload(slideDeformerExport)

import maya.mel as mel

class slideDeformerGui(object):
    def __init__(self):
        #vars
        self.win              = "SlideDeformerWindow"
        self.layout           = None
        self.column_layout    = None
        self.deformer_list    = None
        self.symmetry_dict    = None
        self.connections      = []
        self.geo_selection    = []
        self.source_selection = []
        self.target_selection = []

    def __selectDeformerAction(self, *args):
        type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)
        faceWeights.refresh_paintable_attrs(deformer)
        self.geo_string = cmds.textFieldGrp(self.geo_filter, q = 1, text = 1)
        #---get geometry based on filter
        if self.geo_string == "":
        # if filter is empty, load all geo, otherwise, filter
            self.geo = cmds.deformer(deformer,
                                     q = True,
                                     g = True)
    #                                  gi = True)
    #         print self.geo
    #         self.geo_index
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
        
        if type == 1:
            #---get weights
            self.attrs = cmds.listAttr(deformer, 
                                       ud = True, 
                                       a = True)
            self.names = []
            for i in range(len(self.attrs)):
                tmp_name = self.attrs[i].split(".")
                self.names.append(tmp_name[1])
            self.weight_dict = dict(zip(self.names,self.attrs))
                 
            # filter source
            self.source_string = cmds.textFieldGrp(self.source_filter, q = 1, text = 1)
            if self.source_string == "":
                #---clear weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    append = self.names,
                                    sc =self.__select_weight_action)
            else:
                self.source_string = self.__filter(filter_string = self.source_string,
                                                    list = self.names)
                #---clear weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    append = self.source_string,
                                    sc =self.__select_weight_action)
            #---Filter Target
            self.target_string = cmds.textFieldGrp(self.target_filter, q = 1, text = 1)
            if self.target_string == "":
                #---clear weights to
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights to
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, append = self.names)
            else:
                self.target_string = self.__filter(filter_string = self.target_string,
                                                    list = self.names)
                #---clear weights from
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    append = self.target_string)
        if type == 2:
            # get curves
            self.connections = []
            self.connections.append(cmds.listConnections(deformer[0] + ".uuaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".uvaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".uva",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".uwpa",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vuaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vvaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vva",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vwpa",
                                                         type = "animCurve",
                                                         d = False))
            flat_conn = []
            for i in range(len(self.connections)):
                if self.connections[i]:
                    for j in range(len(self.connections[i])):
                        if self.connections[i][j]:
                            flat_conn.append(self.connections[i][j])
            self.connections = flat_conn
#             print self.connections
            #---filter connections
            # filter source
            self.source_string = cmds.textFieldGrp(self.source_filter, q = 1, text = 1)
            if self.source_string == "":
                #---clear weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    append = self.connections,
                                    sc =self.__select_weight_action)
            else:
                self.source_string = self.__filter(filter_string = self.source_string,
                                                    list = self.connections)
                #---clear weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    append = self.source_string,
                                    sc =self.__select_weight_action)
            #---Filter Target
            self.target_string = cmds.textFieldGrp(self.target_filter, q = 1, text = 1)
            if self.target_string == "":
                #---clear weights to
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights to
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, append = self.connections)
            else:
                self.target_string = self.__filter(filter_string = self.target_string,
                                                    list = self.connections)
                #---clear weights from
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    append = self.target_string)

            
            
    def __select_weight_action(self, *args):
        ""
        type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        if type == 1:
            weights_source = cmds.textScrollList(self.weights_source_list, 
                                           q = 1, 
                                           selectItem = 1)
            deformer = cmds.textScrollList(self.deformer_list, 
                                           q = 1, 
                                           selectItem = 1)
            idx = len(weights_source)-1
#     
#             weights_source = self.weight_dict.get(weights_source[idx])
            try:
                self.current_weights= "LHSlideDeformer." + deformer[0] + "." + weights_source[idx]
            except:
                pass
            try:
                self.current_weights= "LHVectorDeformer." + deformer[0] + "." + weights_source[idx]
            except:
                pass
            #--- if you have weightable geo selected this will work
            try:
                mel.eval('artSetToolAndSelectAttr( "artAttrCtx", "' +self.current_weights+ '" );')
            except:
                pass
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
        
    def __reload_source(self, filter_string = "", list = []):
        type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)
        if type == 1:
            #---get weights
            self.attrs = cmds.listAttr(deformer, 
                                       ud = True, 
                                       a = True)
            self.names = []
            for i in range(len(self.attrs)):
                tmp_name = self.attrs[i].split(".")
                self.names.append(tmp_name[1])
            self.weight_dict = dict(zip(self.names,self.attrs))
                 
            # filter source
            self.source_string = cmds.textFieldGrp(self.source_filter, q = 1, text = 1)
            if self.source_string == "":
                #---clear weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    append = self.names,
                                    sc =self.__select_weight_action)
            else:
                self.source_string = self.__filter(filter_string = self.source_string,
                                                    list = self.names)
                #---clear weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    append = self.source_string,
                                    sc =self.__select_weight_action)
        if type == 2:
            # get curves
            self.connections = []
            self.connections.append(cmds.listConnections(deformer[0] + ".uuaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".uvaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".uva",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".uwpa",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vuaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vvaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vva",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vwpa",
                                                         type = "animCurve",
                                                         d = False))
            flat_conn = []
            for i in range(len(self.connections)):
                if self.connections[i]:
                    for j in range(len(self.connections[i])):
                        if self.connections[i][j]:
                            flat_conn.append(self.connections[i][j])
            self.connections = flat_conn
#             print self.connections
            #---filter connections
            # filter source
            self.source_string = cmds.textFieldGrp(self.source_filter, q = 1, text = 1)
            if self.source_string == "":
                #---clear weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    append = self.connections,
                                    sc =self.__select_weight_action)
            else:
                self.source_string = self.__filter(filter_string = self.source_string,
                                                    list = self.connections)
                #---clear weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_source_list,
                                    e = 1, 
                                    append = self.source_string,
                                    sc =self.__select_weight_action)

    def __reload_target(self, filter_string = "", list = []):
        type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)
        type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)
        if type == 1:
            #---get weights
            self.attrs = cmds.listAttr(deformer, 
                                       ud = True, 
                                       a = True)
            self.names = []
            for i in range(len(self.attrs)):
                tmp_name = self.attrs[i].split(".")
                self.names.append(tmp_name[1])
            self.weight_dict = dict(zip(self.names,self.attrs))
                 
            #---Filter Target
            self.target_string = cmds.textFieldGrp(self.target_filter, q = 1, text = 1)
            if self.target_string == "":
                #---clear weights to
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights to
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, append = self.names)
            else:
                self.target_string = self.__filter(filter_string = self.target_string,
                                                    list = self.names)
                #---clear weights from
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    append = self.target_string)
        if type == 2:
            # get curves
            self.connections = []
            self.connections.append(cmds.listConnections(deformer[0] + ".uuaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".uvaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".uva",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".uwpa",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vuaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vvaca",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vva",
                                                         type = "animCurve",
                                                         d = False))
            self.connections.append(cmds.listConnections(deformer[0] + ".vwpa",
                                                         type = "animCurve",
                                                         d = False))
            flat_conn = []
            for i in range(len(self.connections)):
                if self.connections[i]:
                    for j in range(len(self.connections[i])):
                        if self.connections[i][j]:
                            flat_conn.append(self.connections[i][j])
            self.connections = flat_conn
#             print self.connections
            #---filter connections
            #---Filter Target
            self.target_string = cmds.textFieldGrp(self.target_filter, q = 1, text = 1)
            if self.target_string == "":
                #---clear weights to
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights to
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, append = self.connections)
            else:
                self.target_string = self.__filter(filter_string = self.target_string,
                                                    list = self.connections)
                #---clear weights from
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    ra = 1)
                #---fill weights from
                cmds.textScrollList(self.weights_target_list,
                                    e = 1, 
                                    append = self.target_string)
    def __findWeights(self, *args):
        print "FIND WEIGHTS"
        cmds.textScrollList(self.deformer_list,
                            e = 1,
                            ra = 1)
        self.slideDeformers = cmds.ls(type = "LHSlideDeformer")
        self.vecDeformers = cmds.ls(type = "LHVectorDeformer")
        self.deformers = self.slideDeformers + self.vecDeformers
#         self.deformers.append(cmds.ls(type = "LHVectorDeformer"))

        cmds.textScrollList(self.deformer_list,
                            e = 1,
                            ra = 1)
        cmds.textScrollList(self.deformer_list,
                            e = 1,
                            append = self.deformers,
                            sc = self.__selectDeformerAction)
#     
    def __mirror_weights(self, *args):
        print "mirror WEIGHTS"
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
                            geo_dict = dict(zip(geo_tmp,index_tmp))
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

    def __copy_weights(self, *args):
        type = cmds.radioButtonGrp(self.weight_type, q = 1, sl = 1)
        deformer = cmds.textScrollList(self.deformer_list, 
                                       q = 1, 
                                       selectItem = 1)
        geo = cmds.textScrollList(self.geo_list, 
                                       q = 1, 
                                       selectItem = 1)
        if type == 1:
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
                                geo_tmp = cmds.deformer(deformer, q = True, g = True)
                                index_tmp = cmds.deformer(deformer, q = True, gi = True)
                                geo_dict = dict(zip(geo_tmp,index_tmp))
                                index = geo_dict.get(geo[i])
                                weights_split = source.split(".")
                                tmp_target = []
                                for j in range(len(target)):
                                    targets_split = target[j].split(".")
                                    tmp_target.append(deformer[0] 
                                                      +"."
                                                      + targets_split[0]
                                                      +"["
                                                      +str(index)
                                                      +"]."
                                                      +targets_split[1],
                                                      )
                                faceWeights.copy_double_array_weights(source = deformer[0] 
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
        if type == 2:
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
#         print " establish symmetry"
        geo = cmds.textScrollList(self.geo_list, 
                                       q = 1, 
                                       selectItem = 1)[0]
        if geo:
            self.symmetry_dict = faceWeights.create_symmetric_partners( geo = geo).symmetry_dict

    def __import_file_browser(self, *args):

        self.import_path = str(cmds.fileDialog2(fm = 1, ff = "*.sld")[0])
        cmds.textFieldGrp(self.import_file, e = True, text=self.import_path)

    def __export_file_browser(self, *args):
#         print " establish symmetry"
        self.export_path = str(cmds.fileDialog2(fm = 0, ff = "*.sld")[0])
        print self.export_path
        cmds.textFieldGrp(self.export_file, e = True, text=self.export_path)

    def __import(self, *args):
        if self.import_path:
            slideDeformerExport.import_slide_deformer(path = self.import_path)

    def __export(self, *args):
        if self.export_path:
            deformer = cmds.textScrollList(self.deformer_list, 
                                           q = 1, 
                                           selectItem = 1)[0]
            slideDeformerExport.export_slide_deformer(name = deformer,path = self.export_path)

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
        self.get_deformers = cmds.button(label = "Get Slide Deformers", 
                                                c = self.__findWeights,
                                                h = 30)
        cmds.text("Geo")
        
        
#         self.layout = cmds.rowColumnLayout(nc = 1)
        self.weight_type = cmds.radioButtonGrp(label = "Weight Type:", 
                                   labelArray2=['Painted', 'Anim Curve'], 
                                   numberOfRadioButtons = 2,
                                   sl = 1,
                                   cw3 = [80,70,30],
                                   cal = [(1,"left"),(2,"left"),(3,"left")]
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
                                                  h = 200)
        self.geo_list = cmds.textScrollList( numberOfRows = 8,
                                             allowMultiSelection = 1,
                                             h = 200)
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
                                       tcc = self.__reload_source)
        self.target_filter = cmds.textFieldGrp( label='Target Filter', text='',
                                       cw2 = [70,180],
                                       cal = [(1,"left"),(2,"left")],
                                       tcc = self.__reload_target)
        self.weights_source_list = cmds.textScrollList( numberOfRows = 8,
                                                      allowMultiSelection = 1,
                                                      h = 200
                                                      )
        self.weights_target_list = cmds.textScrollList( numberOfRows = 8,
                                                    allowMultiSelection = 1,
                                                    h = 200)
#         self.layout = cmds.rowColumnLayout(nc = 1,)
        cmds.text("")
        cmds.text(" ")
        cmds.text("  ")
        ###########################################################
        #---Weight Groups Frame
        ###########################################################
        
        cmds.setParent(self.layout_main)
        self.frame2 = cmds.frameLayout(label = "Copy Weight Groups",
                                       collapsable = True,
                                       collapse = True)
        cmds.setParent(self.frame2)
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
        #---Copy point Weights Frame
        ###########################################################
     
        cmds.setParent(self.layout_main)
        self.frame3 = cmds.frameLayout(label = "Weight Calculator",
                                       collapsable = True,
                                       collapse = True)
        
        cmds.setParent(self.frame3)
        
        #---buttons
        self.value = cmds.textFieldGrp( label='Value', text='0.0',
                                       cw2 = [70,180],
                                       cal = [(1,"left"),(2,"left")])
#                                        tcc = self.__reload_source)
        self.operation = cmds.radioButtonGrp(label = "Operation", 
                                           labelArray4=['Add',
                                                        'Subtract',
                                                        'Multiply',
                                                        'Divide'], 
                                           numberOfRadioButtons = 4,
                                           sl = 1,
                                           cw5 = [80,80,80,80,80],
                                           cal = [(1,"left"),(2,"left"),(3,"left")]
                                           )
        self.copy_pw = cmds.button(label = "Copy",
#                                          c = self.__mirror_weights,
                                         w = 100)
        cmds.text("Select one or more point")
        #---copy
        self.paste_pw = cmds.button(label = "Paste",
#                                        c = self.__copy_weights,
                                       w = 200)
        cmds.text("Select one or more point")

        ###########################################################
        #---Import Deformers
        ###########################################################
     
        cmds.setParent(self.layout_main)
        self.frame4 = cmds.frameLayout(label = "Import Deformer",
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
        cmds.setParent(self.frame4)
        
        
        #---buttons
        self.import_btn = cmds.button(label = "Import",
                                        c = self.__import,
                                         w = 100)
        
        
        ###########################################################
        #---Export Deformers
        ###########################################################
     
        cmds.setParent(self.layout_main)
        self.frame5 = cmds.frameLayout(label = "Export Deformer",
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
        cmds.setParent(self.frame5)
        self.export_btn = cmds.button(label = "Export",
                                        c = self.__export,
                                       w = 200)
#         cmds.text("Select one or more point")
           
        
    def show(self):
        self.__createUiElements()
        cmds.showWindow(self.win)

window = slideDeformerGui()
window.show()