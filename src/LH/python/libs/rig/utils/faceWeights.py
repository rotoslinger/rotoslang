# import math, sys
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.OpenMayaAnim as OpenMayaAnim


#===============================================================================
#CLASS:         create_symmetric_partners
#DESCRIPTION:   creates a dictionary that gives the symmetric point id for every
#               point id because this can be slow for large meshes this module
#               is meant as a method for caching out this information so it
#               only has to be done one time per maya session
#USAGE:         give polygon geo
#RETURN:        symmetry_dict
#AUTHOR:        Levi Harrison
#DATE:          Nov. 7th, 2014
#Version        1.0.0
#===============================================================================

class create_symmetric_partners():
    def __init__(self,
                 geo = '',
                 ):
        """
        
        type  geo:               string
        param geo:               geometry you want to build symmetric
                                  partners from.  Best results the closer a
                                  mesh is to symmetric.  Right now only polygons
                                  are supported
        """
        #----args
        self.geo              = geo
        #----vars
        self.symmetry_dict      = None

        self.__create()

    def __create(self):
        """get source double array attributes set values on targets"""
        regular_idx = []
        flipped_idx = []
        if self.geo:
            # create mfnmesh
            meshNode = OpenMaya.MSelectionList()
            meshNode.add(self.geo)
            pPath = OpenMaya.MDagPath()
            meshNode.getDagPath(0,pPath)
            fnMesh = OpenMaya.MFnMesh(pPath)
            
            points = OpenMaya.MPointArray()
            fnMesh.getPoints(points)
            dummy_point = OpenMaya.MPoint()
            for i in range(points.length()):
                opposite_point = OpenMaya.MPoint(points[i].x*-1,
                                                 points[i].y,
                                                 points[i].z)
                util = OpenMaya.MScriptUtil()
                util.createFromInt(0)
                face_id = util.asIntPtr()
                fnMesh.getClosestPoint(opposite_point,
                                       dummy_point,
                                       OpenMaya.MSpace.kObject,
                                       face_id)
                face_id = OpenMaya.MScriptUtil(face_id).asInt()
                point_ids = OpenMaya.MIntArray()
                fnMesh.getPolygonVertices(face_id,point_ids)
                closest_lengths = []
                for j in point_ids:
                    fnMesh.getPoint(j,dummy_point)
                    vector_to = OpenMaya.MVector(dummy_point.x,
                                                 dummy_point.y,
                                                 dummy_point.z)
                    vector_from = OpenMaya.MVector(opposite_point.x,
                                                   opposite_point.y,
                                                   opposite_point.z)
                    vector_from = vector_from - vector_to
                    closest_lengths.append(vector_from.length())
                #make dictionary
                id_dict = dict(list(zip(closest_lengths,point_ids)))
                smallest_id = min(closest_lengths)
#                 regular_idx.append(self.geo + ".vtx["+ str(i)+"]")
#                 flipped_idx.append(self.geo + ".vtx["+ str(id_dict.get(smallest_id))+"]")
                regular_idx.append(i)
                flipped_idx.append(id_dict.get(smallest_id))
            self.symmetry_dict = dict(list(zip(regular_idx,flipped_idx)))
# sym_points = create_symmetric_partners(geo = "pSphere1").symmetry_dict
# 
# sel = sym_points.get("pSphere1.vtx[296]")
# cmds.select(sel)

#===============================================================================
#CLASS:         copy_double_array_weights
#DESCRIPTION:   copies double array attrs used for weighting from attr to attr(s)
#USAGE:         give source and target.  Target can be list.
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          Oct. 10th, 2014
#Version        1.0.0
#===============================================================================

class copy_double_array_weights():
    def __init__(self,
                 source = '',
                 target = [],
                 invert = False,
                 flip = False,
                 symmetry_dict = None
                 ):
        """
        type  source:            string (full attr name deformer.doubleArray)
        param source:            attr you will copy from

        type  target:            list of strings
        param target:            attr(s) you will copy to

        type  invert:            bool
        param invert:            whether or not you want to invert the weight
                                  values before you paste them

        type  invert:            bool
        param invert:            whether or not you want to invert the weight
                                  values before you paste them

        type  flip:              bool
        param flip:              if true weighting will be flipped from one
                                  side of the mesh to the other. The closer
                                  symmetry is the better this will work

        type  symmetry_dict:     dictionary
        param symmetry_dict:     required if you want to flip, can be retrieved
                                  using the create_symmetric_partners module
                                  the opposite id for each id in the double
                                  array
        """
        #----args
        self.source           = source
        self.target           = target
        self.invert           = invert
        self.flip             = flip
        self.symmetry_dict  = symmetry_dict
        #----vars
        self.weights          = []
        self.flip_weights          = []
        self.__create()

    def __get(self):
        """get source double array attributes set values on targets"""
        self.weights = cmds.getAttr(self.source)

    def __invert(self):
        """get source double array attributes set values on targets"""
        if self.invert == True:
            for i in range(len(self.weights)):
                self.weights[i] = self.weights[i] * -1
        if self.flip == True:
            self.flip_weights = list(self.weights)
    def __flip(self):
        """get source double array attributes set values on targets"""
#         tmp_weights = []
        if self.flip == True:
            if self.symmetry_dict:
                for i in range(len(self.flip_weights)):
#                     print self.weights[i], self.flip_weights[i]
                    try:
                        self.flip_weights[i] = self.weights[self.symmetry_dict.get(i)]
                    except:
                        pass
                self.weights =  self.flip_weights
                
    def __set(self):
        """get source double array attributes set values on targets"""
        for i in range(len(self.target)):
            cmds.setAttr(self.target[i], self.weights, typ='doubleArray')

    def __create(self):
        """put everything together"""
        self.__get()
        self.__invert()
        self.__flip()
        self.__set()

# copy_double_array_weights(source = 'C_testFace_SLD.mouthUDVWeights[0].mouthUDVWeight', 
#                           target = ['C_testFace_SLD.lMouthUDVWeights[0].lMouthUDVWeight'],
#                           geo = "C_body_HI",
#                           flip = True)

# #ULid
# copyDoubleArrayAttrs(source = 'L_lids_SLD.L_ULidUD_ACVVWeights[0].L_ULidUD_ACVVWeight', 
#                      target = ['L_lids_SLD.L_ULidLR_ACVUWeights[0].L_ULidLR_ACVUWeight',
#                                'L_lids_SLD.L_ULidInnLR_ACVUWeights[0].L_ULidInnLR_ACVUWeight',
#                                'L_lids_SLD.L_ULidMidLR_ACVUWeights[0].L_ULidMidLR_ACVUWeight',
#                                'L_lids_SLD.L_ULidOutLR_ACVUWeights[0].L_ULidOutLR_ACVUWeight',
#                                'L_lids_SLD.L_ULidInnUD_ACVVWeights[0].L_ULidInnUD_ACVVWeight',
#                                'L_lids_SLD.L_ULidMidUD_ACVVWeights[0].L_ULidMidUD_ACVVWeight',
#                                'L_lids_SLD.L_ULidOutUD_ACVVWeights[0].L_ULidOutUD_ACVVWeight',
#                                ])
# #BLid
# copyDoubleArrayAttrs(source = 'L_lids_SLD.L_BLidUD_ACVVWeights[0].L_BLidUD_ACVVWeight', 
#                      target = ['L_lids_SLD.L_BLidLR_ACVUWeights[0].L_BLidLR_ACVUWeight',
#                                'L_lids_SLD.L_BLidInnLR_ACVUWeights[0].L_BLidInnLR_ACVUWeight',
#                                'L_lids_SLD.L_BLidMidLR_ACVUWeights[0].L_BLidMidLR_ACVUWeight',
#                                'L_lids_SLD.L_BLidOutLR_ACVUWeights[0].L_BLidOutLR_ACVUWeight',
#                                'L_lids_SLD.L_BLidInnUD_ACVVWeights[0].L_BLidInnUD_ACVVWeight',
#                                'L_lids_SLD.L_BLidMidUD_ACVVWeights[0].L_BLidMidUD_ACVVWeight',
#                                'L_lids_SLD.L_BLidOutUD_ACVVWeights[0].L_BLidOutUD_ACVVWeight',
#                                ])

#===============================================================================
#CLASS:         mirrorDoubleArrayWeights
#DESCRIPTION:   mirrors double array weighting using a cluster
#USAGE:         give weight attr(s) and geo.
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          Oct. 12th, 2014
#Version        1.0.0
#===============================================================================

class mirror_double_array_attrs():
    def __init__(self,
                 source = '',
                 geo = '',
                 side = "L"
                 ):
        """
        type  source:            string
        param source:            attr you will mirror
                                  geometry should be close to symmetric
                                     
        type  geo:               string
        param geo:               geo on which to mirror
                                  geometry should be close to symmetric

        type  side:              string
        param side:              "L" or "R" if "L" mirrors +x to -x and opposite
                                  if "R"
        """
        #----args
        self.source               = source
        self.geo                  = geo
        self.side                 = side
        #----vars
        self.weights              = []
        self.cluster              = ''
        self.cluster_weight_attr    = []
        self.mirrored_weights      = []
        self.__create()

    def __get_weights(self):
        """gets weight values"""
        self.weights = cmds.getAttr(self.source)
        
    def __create_cluster(self):
        """creates a cluster to use for mirroring"""
        self.cluster = cmds.cluster(self.geo, name = "temporaryCluster")

    def __set_cluster_weights(self):
        """sets non mirrored weights on cluster"""
        cmds.percent( self.cluster[0], self.geo, v = 0)
        self.cluster_weight_attr = self.cluster[0] + '.weightList[0].weights'
        for i in range(len(self.weights)):
            cmds.setAttr(self.cluster_weight_attr+"["+str(i)+"]", 
                         self.weights[i],)

    def __mirror_cluster_weights(self):
        """mirrors cluster weights"""
        if self.side == "L":
            cmds.copyDeformerWeights( ss=self.geo, ds=self.geo, sd=self.cluster[0], 
                                      mirrorMode='YZ')
        if self.side == "R":
            cmds.copyDeformerWeights( ss=self.geo, ds=self.geo, sd=self.cluster[0], 
                                      mirrorMode='YZ', mi = True)
    def __get_cluster_weights(self):
        """gets newly mirrored cluster weight values"""
        self.mirrored_weights = cmds.getAttr(self.cluster_weight_attr)[0]

    def __set_mirrored_weights(self):
        """sets weight values"""
        cmds.setAttr(self.source, self.mirrored_weights, typ='doubleArray')

    def __cleanup(self):
        """delete cluster"""
        cmds.delete(self.cluster)
        
    def __create(self):
        """put everything together"""
        self.__get_weights()
        self.__create_cluster()
        self.__set_cluster_weights()
        self.__mirror_cluster_weights()
        self.__get_cluster_weights()
        self.__set_mirrored_weights()
        self.__cleanup()
        
# mirror_double_array_attrs(source = 'cluster1.weightList[0].weights', 
#                        geo = 'pSphere1')
# mirror_double_array_attrs(source = 'C_testFace_SLD.mouthUDVWeights[0].mouthUDVWeight', 
#                        geo = 'C_body_HI')
# mirror_double_array_attrs(source = 'C_testFace_SLD.mouthLRUWeights[0].mouthLRUWeight', 
#                        geo = 'C_body_HI')

# copy_double_array_weights(source = 'C_testFace_SLD.lSideUWeights[0].lSideUWeight', 
#                      target = ['C_testFace_SLD.lMouthUDVWeights[0].lMouthUDVWeight'])

#===============================================================================
#CLASS:         mirror_anim_curves
#DESCRIPTION:   mirrors anim curves
#USAGE:         give list of anim curves
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          Oct. 14th, 2014
#Version        1.0.0
#===============================================================================

class mirror_anim_curves():
    def __init__(self,
                 anim_curve = '',
                 side = "L",
                 center_frame = 0,
                 flip = False,
                 ):
        """
        type  anim_curve:            list
        param anim_curve:            anim curves     

        type  side:                  string
        param side:                  if "L" mirrors from timeline right to left
                                      if "R" mirrors from timeline left to right
                                      this happens under the assumption that you
                                      are looking at a character's face from the
                                      front while modifying anim curves.  In
                                      this case "L" is referring to the left side
                                      of the face, not the left side of the
                                      timeline, or the screen

        type  center_frame:          int
        param center_frame:          the mirror axis, can be thought of as
                                      the scale pivot

        type  flip:                  bool
        param flip:                  if False mirrors from left to right
        """
        #----args
        self.anim_curve                   = anim_curve
        self.side                         = side
        self.center_frame                 = center_frame
        self.flip                         = flip
        #----vars
        self.num_keys                     = 0
        # all
        self.api_anim_curve               = ""
        self.all_frame_values             = []
        self.all_frame_times              = []
        self.all_in_x_tangents            = []
        self.all_in_y_tangents            = []
        self.all_out_x_tangents           = []
        self.all_out_y_tangents           = []
        self.all_in_tangents_type         = []
        self.all_out_tangents_type        = []
        self.remove_keys                  = []
        # side
        self.side_frame_values            = []
        self.side_frame_times             = []
        self.side_in_x_tangents           = []
        self.side_in_y_tangents           = []
        self.side_out_x_tangents          = []
        self.side_out_y_tangents          = []
        self.side_in_tangents_type         = []
        self.side_out_tangents_type        = []
        self.center_key                   = []

        self.__create()

    def __get_anim_curve_info(self):
        type = cmds.nodeType(self.anim_curve)
        if "animCurve" in type:
            #--- get all keys and times of all_frame_values and num all_frame_values and frame range
            anim_curve_node = OpenMaya.MSelectionList()
            anim_curve_node.add(self.anim_curve)
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

            if self.num_keys > 1:
                for i in range(self.num_keys):
                    tmp_x = 0
                    tmp_y = 0
                    tmp_times = self.api_anim_curve.time(i)
                    self.all_frame_times.append(tmp_times.value())
                    self.all_frame_values.append(self.api_anim_curve.value(i))
                    #get tangent types
                    self.all_in_tangents_type.append(self.api_anim_curve.inTangentType(i))
                    self.all_out_tangents_type.append(self.api_anim_curve.outTangentType(i))
                    # get in tangents
                    self.api_anim_curve.getTangent(i,x,y,True)
                    self.all_in_x_tangents.append(OpenMaya.MScriptUtil.getFloat(x))
                    self.all_in_y_tangents.append(OpenMaya.MScriptUtil.getFloat(y))
                    # get out tangents
                    self.api_anim_curve.getTangent(i,x,y,False)
                    self.all_out_x_tangents.append(OpenMaya.MScriptUtil.getFloat(x))
                    self.all_out_y_tangents.append(OpenMaya.MScriptUtil.getFloat(y))
            else:
                raise Exception( self.api_anim_curve + ''' doesn't have enough keys to mirror ''')
                quit()        
        else:
            raise Exception( self.api_anim_curve + ''' is not an anim_curve ''')
            quit()
    def __get_keys_from_side(self):
        """isolate all keyframe information from the side you are interested in"""
        if self.side == "L":
            #---get all info from time greater than center frame
            for i in range(len(self.all_frame_times)):
                if self.all_frame_times[i] > self.center_frame:
                    self.side_frame_values.append(self.all_frame_values[i])
                    self.side_frame_times.append(self.all_frame_times[i])
                    self.side_in_x_tangents.append(self.all_in_x_tangents[i])
                    self.side_in_y_tangents.append(self.all_in_y_tangents[i])
                    self.side_out_x_tangents.append(self.all_out_x_tangents[i])
                    self.side_out_y_tangents.append(self.all_out_y_tangents[i])
                    self.side_in_tangents_type.append(self.all_in_tangents_type[i])
                    self.side_out_tangents_type.append(self.all_out_tangents_type[i])
        elif self.side == "R":
            #---get all info from time greater than center frame
            for i in range(len(self.all_frame_times)):
                if self.all_frame_times[i] < self.center_frame:
                    self.side_frame_values.append(self.all_frame_values[i])
                    self.side_frame_times.append(self.all_frame_times[i])
                    self.side_in_x_tangents.append(self.all_in_x_tangents[i])
                    self.side_in_y_tangents.append(self.all_in_y_tangents[i])
                    self.side_out_x_tangents.append(self.all_out_x_tangents[i])
                    self.side_out_y_tangents.append(self.all_out_y_tangents[i])
                    self.side_in_tangents_type.append(self.all_in_tangents_type[i])
                    self.side_out_tangents_type.append(self.all_out_tangents_type[i])

    def __flatten_opposite(self):
        """zeros out all keys on the opposite side"""
        if self.side == "L":
            #---get all info from time greater than center frame
            for i in range(len(self.all_frame_times)):
                if self.all_frame_times[i] < self.center_frame:
                    # set value 0
                    self.api_anim_curve.setValue(i,0)
                    # set in tangent 0
                    self.api_anim_curve.setTangent(i,0,0,True)
                    # set out tangent 0
                    self.api_anim_curve.setTangent(i,0,0,False)
                    self.remove_keys.append(i)
        elif self.side == "R":
            #---get all info from time greater than center frame
            for i in range(len(self.all_frame_times)):
                if self.all_frame_times[i] > self.center_frame:
                    # set value 0
                    self.api_anim_curve.setValue(i,0)
                    # set in tangent 0
                    self.api_anim_curve.setTangent(i,0,0,True)
                    # set out tangent 0
                    self.api_anim_curve.setTangent(i,0,0,False)
                    self.remove_keys.append(i)
        for i in range(len(self.remove_keys)):
            if not i == len(self.remove_keys):
                if i == 0:
                    index = self.remove_keys[i]
                self.api_anim_curve.remove(index)
#         print self.remove_keys
        
    def __flip_keys(self):
        """inverse scale keys"""
        cmds.scaleKey(self.anim_curve, 
                      scaleSpecifiedKeys = True,
                      timeScale = -1,
                      timePivot = self.center_frame,
                      floatScale = -1, 
                      floatPivot = self.center_frame,
                      valueScale = 1,
                      valuePivot = 0)

    def __set_keys(self):
        """sets original keys"""
        #get index
        if self.flip == False:
            for i in range(len(self.side_frame_times)):
                time = OpenMaya.MTime(self.side_frame_times[i])
                index = self.api_anim_curve.addKey(time,
                                                   self.side_frame_values[i],
                                                   self.side_in_tangents_type[i],
                                                   self.side_out_tangents_type[i])
                # set in tangent 
                self.api_anim_curve.setTangent(index,
                                               self.side_in_x_tangents[i],
                                               self.side_in_y_tangents[i],
                                               True,
                                               None,
                                               False)
                # set out tangent 0
                self.api_anim_curve.setTangent(index,
                                               self.side_out_x_tangents[i],
                                               self.side_out_y_tangents[i],
                                               True,
                                               None,
                                               False)

    def __create(self):
        """put everything together"""
        self.__get_anim_curve_info()
        self.__get_keys_from_side()
        self.__flatten_opposite()
        self.__flip_keys()
        self.__set_keys()
##############################################
#Example:
# mirror_anim_curves(anim_curve = 'L_innUDVU_ACV')
###############################################

#===============================================================================
#CLASS:         mirror_anim_curves
#DESCRIPTION:   copies from one anim curve to another and flips to the opposite
#               side
#USAGE:         give list of anim curves
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          Oct. 14th, 2014
#Version        1.0.0
#===============================================================================

class copy_flip_anim_curves():
    def __init__(self,
                 side = "L",
                 source = "",
                 target = "",
                 center_frame = 0,
                 flip = False
                 ):
        """
        type  side:                  string
        param side:                  the side you are copying from
        
        type  source:                string
        param source:                the curve to copy from

        type  target:           string
        param target:           the curve to copy to

        type  center_frame:          int
        param center_frame:          the mirror axis, can be thought of as
                                      the scale pivot

        type  flip:                  bool
        param flip:                  if false only a regular copy is done
        """
        #----args
        self.side                         = side
        self.source                       = source
        self.target                  = target
        self.center_frame                 = center_frame
        self.flip                         = flip
        
        self.__create()

    def __check(self):
        # makes sure source and target are anim curves
        for i in [self.source, self.target]:
            type = cmds.nodeType(i)
            if "animCurve" in type:
                continue
            else:
                raise Exception( i + ''' is not an anim_curve ''')
                quit()

    def __copy_anim_curve(self):
        """use the option replace completely"""
        cmds.copyKey(self.source, o = "curve")
        cmds.pasteKey(self.target, o = "replaceCompletely")

    def __flip_dest(self):
        """use the option replace completely"""
        if self.flip == True:
            mirror_anim_curves(anim_curve = self.target, 
                               side = self.side,
                               center_frame = self.center_frame,
                               flip = True)

    def __create(self):
        """put everything together"""
        self.__check()
        self.__copy_anim_curve()
        self.__flip_dest()
        
#===============================================================================
#CLASS:         rename_weight_attrs
#DESCRIPTION:   renames a compound attribute that is used for weighting
#USAGE:         give old attribute name and new attribute name
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          Oct. 14th, 2014
#Version        1.0.0
# because renameAttrs doesn't work for compound attributes right now
# should only be used for lh deformer weight compounds
# assumes the child double array attributes have no direct connections
#===============================================================================

class rename_weight_attrs():
    def __init__(self,
                 node = "",
                 old = "",
                 new = "",
                 ):
        """
        type  node:                 string
        param node:                 name of the node that has the attribute
        
        type  old:                  string
        param old:                  old attribute name: Weights
        
        type  new:                  string
        param new:                  new attribute name: newWeights
        """
        #----args
        self.node                    = node
        self.old                     = old
        self.new                     = new
        #----variables
        self.parent                        = []
        self.numParents                    = []
        self.numChildren                   = []
        self.newParentName                 = []
        self.final_parent_attr             = ""
        self.final_child_attr              = ""
        self.__create()

    def __check(self):
        # make sure the old attribute exists, and that the new one does not
#         print cmds.attributeQuery(self.old, node = self.node, ex= True)
        
        if cmds.attributeQuery(self.old, node = self.node, ex= True):
            if not cmds.attributeQuery(self.new, node = self.node, ex= True):
                pass
            else:
                raise Exception(self.old + " already exists")
                quit()
        else:
            raise Exception(self.new + " does not exist")
            quit()

    def __get_attr_info(self):
        self.parent = cmds.attributeQuery(self.old, node = self.node, lp =True )
        self.final_parent_attr = self.node + "." +self.parent[0]
        self.numParents = cmds.getAttr(self.final_parent_attr, size =True )
        for i in range(self.numParents):
            self.numChildren.append(cmds.getAttr(self.node
                                            + "." +self.parent[0]
                                            + "["
                                            +str(i)
                                            + "]"
                                            +"."
                                            +self.old,
                                            size =True ))
        self.newParentName = self.parent[0].replace(self.parent[0], self.new + "s")
#         print self.new, self.newParentName

    def __create_new_attr(self):
        """create the new attribute"""
        cmds.addAttr(self.node,
                     longName = self.newParentName,
                     numberOfChildren = 1, 
                     attributeType = 'compound',
                     multi = True, 
                     indexMatters=True)
        cmds.addAttr(self.node, 
                     longName = self.new,
                     dataType = 'doubleArray',
                     parent = self.newParentName)


    def __copy_weights(self):
        """copies the weights from the old attribute to the new attribute"""
#         print self.old
#         print self.final_parent_attr
        for i in range(self.numParents):
            cmds.connectAttr(self.final_parent_attr 
                             + "[" 
                             + str(i)
                             + "]." + self.old,
                             self.node 
                             + "." 
                             + self.newParentName 
                             + "[" 
                             + str(i) 
                             + "]." + self.new)
            cmds.disconnectAttr(self.final_parent_attr 
                             + "[" 
                             + str(i)
                             + "]." + self.old,
                             self.node 
                             + "." 
                             + self.newParentName 
                             + "[" 
                             + str(i) 
                             + "]." + self.new)
    def __switch_connections(self):
        """get the outgoing connections from the old attribute"""
        self.parent_connections = []
        self.child_connections = []
        for i in range(self.numParents):
            connects = cmds.listConnections(self.final_parent_attr 
                                            + "[" 
                                            + str(i) 
                                            + "]", 
                                            d = True,
                                            p = True)
            if connects:
                for j in connects:
                    if j:
                        cmds.connectAttr(self.node 
                                         + "." 
                                         + self.newParentName 
                                         + "[" 
                                         + str(i) 
                                         + "]", 
                                         j,
                                         f = True)

    def __delete_old(self):
        """delete the old attribute"""
        cmds.deleteAttr(self.final_parent_attr)

    def __create(self):
        """put everything together"""
        self.__check()
        self.__get_attr_info()
        self.__create_new_attr()
        self.__copy_weights()
        self.__switch_connections()
        self.__delete_old()
        
###############################################################################
# Example
# rename_weight_attrs(node = "C_mouth_SLD", old = "mouthLRWeight", new = "C_mouthLRWeight") 
#################################################################################




#===============================================================================
#CLASS:         get_cooresponding_attrs
#DESCRIPTION:   specifically for lhDeformers.  Given a deformer name, and attribute
#               finds the cooresponding weight attr, animation curves, and pivot
#               (pivots, if the deformer is an LHVectorDeformer type)
#USAGE:         give list of anim curves
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          Oct. 14th, 2014
#Version        1.0.0
#===============================================================================

class get_cooresponding_attrs():
    def __init__(self,
                 node = "",
                 attr = "",
                 ):
        """
        type  node:                string
        param node:                the side you are copying from
        
        type  attr:                string
        param attr:                the curve to copy from
        """
        #----args
        self.node                         = node
        self.attr                         = attr
        #----vars
        self.full_attr                    = self.node  + "." + self.attr
        self.prefix                       = ""
        self.type                         = ""
        self.connections                   = []
        self.weight_attr                  = []
        self.u_anim_curve                 = []
        self.v_anim_curve                 = []
        self.pivot                        = []
        self.end                          = 0
        self.__create()

    def __check(self):
        """make sure node type is one of the supported LHDeformers"""
        if cmds.objExists(self.node):
            self.type = cmds.nodeType(self.node)
        else:
            print(self.node + " does not exist")
            self.end = 1

        if not cmds.objExists(self.full_attr):
            print(self.full_attr + " does not exist")
            self.end = 1
        if not (self.type == "LHSlideDeformer" or self.type == "LHVectorDeformer" or self.type == "LHCurveRollDeformer"):
            print(self.node + " is not a supported node")
            self.end = 1

    def __get_connection(self):
        """gets the connection of the attribute to determine what it relates to"""
        self.connections = cmds.listConnections(self.full_attr, d=True, p=True, t = self.type)
#         print self.connections
        if not self.connections:
            print(self.full_attr + " is not connected, unable to find cooresponding attributes")
            self.end = 1
            
    def __compose_attrs(self):
        """gets the connection of the attribute to determine what it relates to"""
            
        self.tmp_attr = self.connections[0].split(".")
        self.prefix = self.tmp_attr[1][0]
        self.tmp_attr = self.tmp_attr[0]+ "." + self.tmp_attr[1]
        
        
        self.weight_attr = self.tmp_attr.replace("ValueParentArray", "WeightsParentArray")
        self.weight_attr =  self.weight_attr + "." + self.prefix + "WeightsParent[0]"

        self.u_anim_curve = self.tmp_attr.replace("ValueParentArray", "AnimCurveUArray")
        self.u_anim_curve =  self.u_anim_curve + "." + self.prefix + "AnimCurveU"
        
        self.v_anim_curve = self.tmp_attr.replace("ValueParentArray", "AnimCurveVArray")
        self.v_anim_curve =  self.v_anim_curve + "." + self.prefix + "AnimCurveV"
        if self.type == "LHVectorDeformer":
            self.pivot = self.tmp_attr.replace("ValueParentArray", "PivotCurveArray")
            self.pivot =  self.pivot + "." + self.prefix + "PivotCurve"
        
        if (cmds.objExists(self.weight_attr) and cmds.objExists(self.u_anim_curve) and cmds.objExists(self.v_anim_curve)):
            pass
        else:
            print("One or more cooresponding attributes don't have a connection, check connections and try again")
            self.end = 1
        if self.type == "LHVectorDeformer":
            if cmds.objExists(self.pivot) :
                pass
            else:
                print("One or more cooresponding attributes don't have a connection, check connections and try again")
                self.end = 1
#         self.weights_attr = self.weights_attr + .
    def __get_final(self):
        """get the connections of the related attributes"""
        self.weight_attr = cmds.listConnections(self.weight_attr, s=True, p=True, t = self.type)[0]
        self.weight_attr = self.weight_attr.split(".")[1]
        self.weight_attr = self.weight_attr.split("[")[0]
        self.weight_attr = self.weight_attr.replace("Weights", "Weight")
        
        self.u_anim_curve = cmds.listConnections(self.u_anim_curve, s=True, p=True, t = "animCurve")[0]
        self.u_anim_curve = self.u_anim_curve.split(".")[0]
        
        self.v_anim_curve = cmds.listConnections(self.v_anim_curve, s=True, p=True, t = "animCurve")[0]
        self.v_anim_curve = self.v_anim_curve.split(".")[0]
        
        if self.type == "LHVectorDeformer":
            self.pivot = cmds.listConnections(self.pivot, s=True, p=True, t = "nurbsCurve")[0]
            self.pivot = self.pivot.split(".")[0]
            self.pivot = cmds.listRelatives(self.pivot, parent = True)[0]
        else:
            self.pivot = ""

#         #Debug
#         if (cmds.attributeQuery(self.weight_attr, node = self.node, ex = True) and cmds.objExists(self.u_anim_curve) and cmds.objExists(self.v_anim_curve)):
#             print self.weight_attr, self.u_anim_curve, self.v_anim_curve, self.pivot
        
    def __create(self):
        """put everything together"""
        self.__check()
        if self.end == 0:
            self.__get_connection()
            if self.end == 0:
                self.__compose_attrs()
                if self.end == 0:
                    self.__get_final()
###############################################################################
#Example:
# get_cooresponding_attrs(node = "C_mouth_SLD", attr="L_TLipPinchLR")
###############################################################################


def refresh_paintable_attrs(slide_deformer):
    "if paintable attrs do not exist, remove them"
    cmds.makePaintable('LHSlideDeformer', ca = True, attrType = "doubleArray", shapeMode='deformer')
    # get all double array attributes
    attrs = cmds.listAttr(slide_deformer, ud = True, a = True)
    for i in attrs:
        paint = i.split(".")[1]
        cmds.makePaintable('LHSlideDeformer', paint, attrType='doubleArray', shapeMode='deformer')
    cmds.makePaintable('LHSlideDeformer', "weights", attrType='multiFloat', shapeMode='deformer')
