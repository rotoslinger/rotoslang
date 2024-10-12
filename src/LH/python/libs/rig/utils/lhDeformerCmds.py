import maya.cmds as cmds
#===============================================================================
#CLASS:         add_weights
#DESCRIPTION:   adds weights to specified LHDeformer
#USAGE:         set args and run
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          November 17th, 2014
#Version        1.0.0
#===============================================================================

class add_weights():
    def __init__(self,
                 deformer_type = "",
                 deformer = "",
                 names=[],
                 geoms = [],
                 uWeights = False,
                 vWeights = False,
                 nWeights = False,
                 tWeights = False,
                 rWeights = False,
                 rollWeights = False,
                 ):
        """
                                     
        type  deformer_type:        string
        param deformer_type:        supported types: "LHSlideDeformer",
                                     "LHVectorDeformer","LHCurveRollDeformer"
                                     
        type  names:                string array
        param names:                the names of the weights you will be adding
        
        type  geoms:                string array
        param geoms:                the names of the geometry that will be
                                     affected
        type  geoms:                string array
        param geoms:                the names of the geometry that will be
                                     affected
        """
        #----args
        self.deformer_type           = deformer_type
        self.deformer                = deformer
        self.names                   = names
        self.geoms                   = geoms
        self.uWeights                = uWeights
        self.vWeights                = vWeights
        self.nWeights                = nWeights
        self.tWeights                = tWeights
        self.rWeights                = rWeights
        self.rollWeights             = rollWeights

        #----vars
        self.valArray                = []
        self.valAttrs                = []

        self.animCurvesU             = []
        self.animCurvesV             = []
        self.weights                 = []
        self.geomShapes              = []
        self.pivotCurves             = []
        self.pivotCurveShapes        = []
        self.__create()
#     def __check(self):
#         """makes sure everything exists"""
    def __check(self):
        """make sure only one weight type option is set"""
        count = 0
        if self.uWeights>0:
            count += 1
        if self.vWeights>0:
            count += 1
        if self.nWeights>0:
            count += 1
        if self.tWeights>0:
            count += 1
        if self.rWeights>0:
            count += 1
        if self.rollWeights>0:
            count += 1
        if count != 1:
            raise Exception('''more than 1 weight type has been set, please only set 1 weight type to True''')
            quit()
    def __getShape(self):
        """gets shape"""
        try:
            try:
                for i in range(len(self.geoms)):
                    temp = cmds.listRelatives(self.geoms[i], shapes = True)[0]
                    self.geomShapes.append(temp)
            except:
                self.geomShapes = self.geoms
        except:
            raise Exception('''one or more argument either did not exist or did not have a shape''')
            quit()

    def __checkGeomArgs(self):
        """checks the args to make sure they are the right type"""
        for i in self.geomShapes:
            if ((cmds.objectType(i, isType='nurbsSurface') == True) or
                (cmds.objectType(i, isType='nurbsCurve') == True) or
                (cmds.objectType(i, isType='mesh') == True)) :
                continue
            else:
                raise Exception( i + ' is not supported geometry \n')
                quit()

    def __createAttrs(self):
        """add u and v attrs to control"""
        
        #----uValAttr
        for i in self.names:
            cmds.addAttr(self.deformer, longName= i,
                                at='float', keyable=True)
            self.valAttrs.append(self.deformer + '.' + i)
    def __createWeights(self):
        """add u and v weights to deformer"""

        #----UWeights
        for i in self.names:
            cmds.addAttr(self.deformer, 
                         longName = i + 'Weights',
                         numberOfChildren = 1, 
                         attributeType = 'compound',
                         multi = True, 
                         indexMatters=True)
            cmds.addAttr(self.deformer, 
                         longName = i + "Weight",
                         dataType = 'doubleArray',
                         parent = i + 'Weights')
            cmds.makePaintable('LHSlideDeformer', i + "Weight", attrType='doubleArray', shapeMode='deformer')
            self.weights.append(self.deformer + "." + i +'Weights')


    def __createAnimCurves(self):
        """add anim curves"""
        #----uAnimCurves
        for i in range(len(self.names)):
            self.animCurvesU.append(cmds.createNode("animCurveTU",
                                                    name = self.names[i]+"_ACV"))
            self.animCurvesV.append(cmds.createNode("animCurveTU",
                                                    name = self.names[i]+"Falloff_ACV"))

    def __createPivots(self):
        """createNurbsCurves that are used for pivots """
        if self.deformer_type == "LHVectorDeformer":
            for i in range(len(self.names)):
                    tmp = cmds.curve(name= self.names[i] + 'Pivot_CRV',
                                          d=1, p=[(0,0,0),(0,0,1)],
                                          k=[0,1])
                    self.pivotCurveShapes.append(cmds.listRelatives(tmp, shapes = True)[0])
                    self.pivotCurves.append(tmp)
    

    def __setAnimCurveShapes(self):
        """set anim curve shapes default is a straight line with a value of 1"""

        #----U
        for i in range(len(self.animCurvesU)):
            cmds.setKeyframe(self.animCurvesU[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, t = 0)
        for i in range(len(self.animCurvesV)):
            cmds.setKeyframe(self.animCurvesV[i], v = 1, breakdown = 0,
                             hierarchy="none", controlPoints = 0, 
                             shape = 0, t = 0)

    def __connect(self):
        """makes all connections into the slide deformer"""
        #----get attr names based on arguments
        if self.uWeights>0:
            prefix = "u"
        if self.vWeights>0:
            prefix = "v"
        if self.nWeights>0:
            prefix = "n"
        if self.tWeights>0:
            prefix = "t"
        if self.rWeights>0 or self.rollWeights>0:
            prefix = "r"
            
            
        #####################################
        ###########     pivots    ###########
        #####################################
        if self.deformer_type == "LHVectorDeformer":
            # find out what the next available value parent array is
            connects = cmds.listConnections(self.deformer + '.' + prefix+ 'PivotCurveArray', c = True)
            connects = [x.split("[")[1] for x in connects if "[" in x]
            connects = [x.split("]")[0] for x in connects if "]" in x]
            connects = [int(x) for x in connects]
            idx = max(connects)
            for i in range(len(self.valAttrs)):
                idx +=1
                cmds.connectAttr(self.pivotCurveShapes[i]+".worldSpace", 
                                 self.deformer + '.' + prefix+ 'PivotCurveArray['
                                 + str(idx) + '].'+ prefix+'PivotCurve', 
                                 force=True)


        #####################################
        ###########     value    ############
        #####################################
        # find out what the next available value parent array is
        connects = cmds.listConnections(self.deformer + '.' + prefix+ 'ValueParentArray', c = True)
        # if none then you can start at 0
        idx = 0
        if connects:
            connects = [x.split("[")[1] for x in connects if "[" in x]
            connects = [x.split("]")[0] for x in connects if "]" in x]
            connects = [int(x) for x in connects]        
            idx = max(connects)
        for i in range(len(self.valAttrs)):
            idx +=1
            cmds.connectAttr(self.valAttrs[i], 
                             self.deformer + '.' + prefix+ 'ValueParentArray['
                             + str(idx) + '].'+ prefix+'Value', 
                             force=True)
            
        #####################################
        ###########     weights    ##########
        #####################################
        # find out what the next available value parent array is

        connects = cmds.listConnections(self.deformer + '.' + prefix+ 'WeightsParentArray', c = True)
        idx = 0
        if connects:
            connects = [x.split("[")[1] for x in connects if "[" in x]
            connects = [x.split("]")[0] for x in connects if "]" in x]
            connects = [int(x) for x in connects]        
            idx = max(connects)
        #----u
        for i in range(len(self.weights)):
            idx +=1
            for j in range(len(self.geoms)):
                cmds.connectAttr(self.weights[i] + '[' + str(j) + ']',
                                 self.deformer+'.'+ prefix+ 'WeightsParentArray['+
                                 str(idx) +'].' + prefix+'WeightsParent[' + str(j) + ']',
                                 force=True)
                
        #####################################
        ########     uAnimCurves    #########
        #####################################
        # find out what the next available value parent array is
        connects = cmds.listConnections(self.deformer + '.' + prefix+ 'AnimCurveUArray', c = True)
        idx = 0
        if connects:
            connects = [x.split("[")[1] for x in connects if "[" in x]
            connects = [x.split("]")[0] for x in connects if "]" in x]
            connects = [int(x) for x in connects]        
            idx = max(connects)
        #----uu
        for i in range(len(self.animCurvesU)):
            idx +=1
            cmds.connectAttr(self.animCurvesU[i] + '.output', 
                             self.deformer + '.'+ prefix+'AnimCurveUArray[' + str(idx) + 
                             '].'+ prefix+'AnimCurveU', 
                             force=True)
            
        #####################################
        ########     vAnimCurves    #########
        #####################################
        # find out what the next available value parent array is
        connects = cmds.listConnections(self.deformer + '.' + prefix+ 'AnimCurveVArray', c = True)
        idx = 0
        if connects:
            connects = [x.split("[")[1] for x in connects if "[" in x]
            connects = [x.split("]")[0] for x in connects if "]" in x]
            connects = [int(x) for x in connects]        
            idx = max(connects)
        #----uv
        for i in range(len(self.animCurvesV)):
            idx +=1
            cmds.connectAttr(self.animCurvesV[i] + '.output',
                             self.deformer + '.'+ prefix+'AnimCurveVArray[' + str(idx) +
                             '].'+ prefix+'AnimCurveV', 
                             force=True)
            
            
    def __create(self):
        """ This method creates the curveDeformer setup """
        self.__check()
        self.__getShape()
        self.__checkGeomArgs()
        self.__createAttrs()
        self.__createPivots()
        self.__createWeights()
        self.__createAnimCurves()
        self.__setAnimCurveShapes()
        self.__connect()

# add_weights(deformer_type = "LHCurveRollDeformer",
#             deformer = "C_testFace_CRD",
#             names = ["thisV","thatV"],
#             geoms = ["c_geo_HI"],
#             uWeights = False,
#             vWeights = False,
#             nWeights = False,
#             tWeights = False,
#             rWeights = False,
#             rollWeights = True)



#===============================================================================
#CLASS:         bake_blendshape
#DESCRIPTION:   creates blendshape based on an attribute min and max
#USAGE:         give list of anim curves
#RETURN:        
#AUTHOR:        Levi Harrison
#DATE:          Dec. 08th, 2014
#Version        1.0.0
#===============================================================================

class bake_blendshape():
    def __init__(self,
                 geo = "",
                 name = "C_faceBake_BSP",
                 attr = "",
                 attr_min = -1.0,
                 attr_max = 1.0,
                 num_inbetweens = 2
                 ):
        """
        type  geo:                   string
        param geo:                   the side you are copying from
        
        type  name:                  string
        param name:                  name of the blendshape

        type  attr:                  string
        param attr:                  the attribute that will be converted into
                                      a blendshape 
                                      ex: "C_mouth_SLD.L_Side"

        type  attr_min:              float
        param attr_min:              the lowest the attribute will go

        type  attr_max:              float
        param attr_max:              the highest the attribute will go

        type  num_inbetweens:        int
        param num_inbetweens:        the number of inbetweens that will be
                                      generated.  Note: number of in-betweens
                                      refers to the amount of in-betweens in
                                      both the positive and negative values. If 
                                      5 in-betweens are specified, 5 will be
                                      used for the positive blendshape and 5 will
                                      be used for the negative blend shape.
        """
        #----args
        self.geo                       = geo
        self.name                      = name
        self.attr                      = attr
        self.attr_min                  = attr_min
        self.attr_max                  = attr_max
        self.num_inbetweens            = num_inbetweens
        #----vars
        self.new                       = 0
        self.min_attr_vals             = []
        self.max_attr_vals             = []
        self.min_extract_geo           = []
        self.max_extract_geo           = []
#         self.attrs                     = []
        self.__create()

    def __check(self):
        # if the blendshape already exists, add to that blendshape, else create
        if cmds.objExists(self.name):
            if cmds.nodeType(self.name) == "blendShape":
                pass
            else:
                print(self.node + "is not a blendShape, please specify a different name")
        else:
            self.new = 1
    def __split_values(self):
        "finds the values of the attrs for the in-betweens"
        max_segment_val = 0.0
        min_segment_val = 0.0
        if self.attr_min != 0 and self.num_inbetweens != 0:
            min_segment_val = self.attr_min / (self.num_inbetweens + 1)
        if self.attr_max != 0 and self.num_inbetweens != 0:
            max_segment_val = self.attr_max / (self.num_inbetweens + 1)
        min_val = min_segment_val
        max_val = max_segment_val
        for i in range(self.num_inbetweens+1):
            if i > 0:
                min_val += min_segment_val
                max_val += max_segment_val
            self.min_attr_vals.append(min_val)
            self.max_attr_vals.append(max_val)

        for i in range(self.num_inbetweens+1):
            #round to 3 decimal places
            self.min_attr_vals[i] = round(self.min_attr_vals[i],3)
            self.max_attr_vals[i] = round(self.max_attr_vals[i],3)
    def __extract_geo(self):
        "extracts geometry at attr values"
        # extract min vals
        for i in range(self.num_inbetweens+1):
            cmds.setAttr(self.attr, self.min_attr_vals[i])
            min_name = ""
            max_name = ""
            if i < self.num_inbetweens:
                min_name = self.attr.split(".")[1] + "neg_between" + str(i)
                max_name = self.attr.split(".")[1] + "pos_between" + str(i)
            if i == self.num_inbetweens:
                min_name = self.attr.split(".")[1] + "_neg"
                max_name = self.attr.split(".")[1]
            self.min_extract_geo.append(cmds.duplicate(self.geo,
                                                       n = min_name)[0])
            cmds.setAttr(self.attr, self.max_attr_vals[i])
            self.max_extract_geo.append(cmds.duplicate(self.geo,
                                                       n = max_name)[0])
            if i == self.num_inbetweens:
                cmds.setAttr(self.attr, 0)
                
    def __create_blendshapes(self):
        "creates blendshape, if already exists, just add"
        if self.new == 1:
            cmds.blendShape(self.geo, n = self.name )
        target_number = 0
        shapes = self.min_extract_geo + self.max_extract_geo
        tmp = cmds.blendShape(self.name, q = True, wc = True)
        cmds.setAttr(self.name + ".supportNegativeWeights", 1)
#         print tmp
        if tmp:
            target_number = tmp
        else:
            target_number = 0
        #add shape
        cmds.blendShape(self.name,
                        e = True,
                        t = (self.geo,
                             target_number,
                             self.max_extract_geo[len(self.max_extract_geo)-1],
                             self.max_attr_vals[len(self.max_attr_vals)-1])
                        )
#         cmds.blendShape(self.name, edit = True, w = [(target_number, 1.0)])
#         print target_number
#         idx_counter = target_number
        for i in range(self.num_inbetweens):
#             idx_counter += 1
#             print self.max_attr_vals[len(self.max_extract_geo)-1]
#             print self.min_attr_vals[i]
            cmds.blendShape(self.name,
                            e = True,
                            ib = True, 
                            t = (self.geo,
                                 target_number,
                                 self.min_extract_geo[i],
                                 self.min_attr_vals[i]))
 
#             idx_counter += 1
#             print self.max_attr_vals[i]
            if i < len(self.max_extract_geo):
                cmds.blendShape(self.name,
                                e = True,
                                ib = True,
                                t = (self.geo,
                                     target_number,
                                     self.max_extract_geo[i],
                                     self.max_attr_vals[i]))
#             
#         tmp = cmds.blendShape(self.name, q = True, t = True)
#         print tmp
    def __connect(self):
        new_attr = self.name + "." + self.attr.split(".")[1]
        cmds.connectAttr(self.attr, new_attr)


    def __cleanup(self):
        "delete geometry"
        cmds.delete(self.min_extract_geo, self.max_extract_geo)

    
    def __create(self):
        """put everything together"""
        self.__check()
        self.__split_values()
        self.__extract_geo()
        self.__create_blendshapes()
        self.__connect()
        self.__cleanup()
        
# bake_blendshape(geo = "C_body_HI",
#                 attr = "C_tLipRoll_CRD.C_upRoll",
#                 attr_min = -600.000,
#                 attr_max = 600.000,
#                 num_inbetweens = 8)
# 
# 
# bake_blendshape(geo = "C_body_HI",
#                 attr = "C_mouth_SLD.R_side",
#                 attr_min = -0.30,
#                 attr_max = 0.30,
#                 num_inbetweens = 3)
# 
# 
# bake_blendshape(geo = "C_body_HI",
#                 attr = "C_mouth_SLD.C_mouthLR",
#                 attr_min = -0.30,
#                 attr_max = 0.30,
#                 num_inbetweens = 3)


def refresh_paintable_attrs(deformer_name, deformer_type ):
    return
#     "if paintable attrs do not exist, remove them"
#     cmds.makePaintable(deformer_type, ca = True, attrType = "doubleArray", shapeMode='deformer')
#     # get all double array attributes
#     attrs = cmds.listAttr(deformer_name, ud = True, a = True)
#     if not attrs:
#         return
#     for i in attrs:
#         paint = i.split(".")[1]
# #         cmds.makePaintable()
#         cmds.makePaintable(deformer_type, paint, attrType='doubleArray', shapeMode='deformer')

def setFaceIdsOnLocator(locatorName):
    faces = cmds.ls(sl = True, fl=True)
    faces = [x.split("[")[1] for x in faces]
    faces = [x.split("]")[0] for x in faces]
    faces = [int(x) for x in faces]
    cmds.setAttr(locatorName + ".faceIds", faces, type = "doubleArray")
# setFaceIdsOnLocator("C_tLip_LOC")






