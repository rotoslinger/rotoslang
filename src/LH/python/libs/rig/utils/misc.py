import sys

from rig_2.message import utils as message_utils
import importlib
importlib.reload(message_utils)
# from rig_2.tag.utils import tag_rivet_mesh, create_component_tag
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)



from maya import cmds
import maya.OpenMaya as OpenMaya
from fnmatch import fnmatch
from . import exportUtils
import maya.OpenMayaAnim as OpenMayaAnim


#===============================================================================
#CLASS:         lock_attrs
#DESCRIPTION:   locks listed attributes
#USAGE:         set args and run
#RETURN:
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class lock_attrs():
    def __init__(self,
                 node="",
                 attr=["tx","ty","tz","rx","ry","rz","sx","sy","sz"],
                 unhide = False,
                 l = True,
                 k = False,
                 cb = False):

        """
        type  node:                string
        param node:                name of the node that will have attrs 
                                    locked

        type  attr:                string
        param attr:                attribute names if "all" will use
                                    translates, rotates and scales

        type  l:                   bool
        param l:                   lock

        type  k:                   bool
        param k:                   keyable

        type  cb:                  bool
        param cb:                  channel box
        """

        #---args
        self.node                   = node
        self.attr                   = attr
        self.unhide                 = unhide
        self.l                      = l
        self.k                      = k
        self.cb                     = cb

        self.__do_it()

    def __do_it(self):
        if self.unhide == True:
            self.l = False
            self.k = True
            self.cb = True
        
        if self.attr == ["all"]:
            self.attr = ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]
        for i in range(len(self.attr)):
            cmds.setAttr(self.node + "."+ self.attr[i], 
                          lock = self.l, 
                          keyable = self.k, 
                          channelBox = self.cb)

#===============================================================================
#CLASS:         create_rig_hier
#DESCRIPTION:   creates a hierarchy for a standard rig
#USAGE:         give a character name
#RETURN:        groups
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class create_rig_hier():
    def __init__(self,
                 name = "character"):
        """
        type  name:                string
        param name:                character name
        """
        #---args
        self.name                   = name
        
        #---vars
        self.groups                      = []

        self.__create()

    def __create_nodes(self):
        "Create and name rig transforms"
        self.root_grp= cmds.createNode("transform", 
                                        name = "C_" + 
                                        self.name + 
                                        "_GRP")

        self.geo_grp = cmds.createNode("transform", 
                                        name   = "C_geo_GRP",
                                        parent = self.root_grp)

        self.skeleton_grp = cmds.createNode("transform", 
                                            name   = "C_skeleton_GRP",
                                            parent = self.root_grp)
        self.skel_bind = cmds.createNode("transform", 
                                             name   = "C_skelbind_GRP",
                                             parent = self.skeleton_grp)
        self.skel_helper = cmds.createNode("transform", 
                                                name   = "C_skelhelp_GRP",
                                                parent = self.skeleton_grp)

        self.rig_grp = cmds.createNode("transform",
                                       name   = "C_rig_GRP",
                                       parent = self.root_grp)
        
        self.rig_ctrl_grp = cmds.createNode("transform",
                                    name   = "C_rigctrl_GRP",
                                    parent = self.rig_grp)
        self.rig_sizectrl_grp = cmds.createNode("transform",
                                    name   = "C_ctrlsize_GRP",
                                    parent = self.rig_ctrl_grp)


        self.maintenence_grp = cmds.createNode("transform",
                                                name   = "C_maintenance_GRP",
                                                parent = self.root_grp)
        



        self.control_grp = cmds.createNode("transform", 
                                            name   = "C_control_GRP",
                                            parent = self.root_grp)

        self.groups = [self.root_grp, self.geo_grp, self.skeleton_grp, self.rig_grp, self.control_grp]
        tag_utils.tag_root_group(self.root_grp)
        tag_utils.tag_rig_group(self.rig_grp)
        tag_utils.tag_rig_ctrl_group(self.rig_ctrl_grp)
        tag_utils.tag_rig_ctrlsize_group(self.rig_sizectrl_grp)
        tag_utils.tag_ctrl_group(self.control_grp)
        tag_utils.tag_geo_group(self.geo_grp)
        tag_utils.tag_skeleton_group(self.skeleton_grp)
        tag_utils.tag_bindjnt_group(self.skel_bind)
        tag_utils.tag_helpjnt_group(self.skel_helper)
        tag_utils.tag_maintenance_group(self.maintenence_grp)

        # Any rig fitting or rig maintenance attributes will go here
        # This will make cleaning up the rig much easier.
        cmds.addAttr(self.maintenence_grp, ln = "fit_ctrl_vis", at = "bool")
        self.fit_ctrl_vis = self.maintenence_grp + ".fit_ctrl_vis"
        cmds.setAttr(self.fit_ctrl_vis, cb = True, e=True)
        cmds.addAttr(self.maintenence_grp, ln = "size_cluster_vis", at = "bool")
        self.size_cluster_vis = self.maintenence_grp + ".size_cluster_vis"
        cmds.setAttr(self.size_cluster_vis, cb = True, e=True)

        cmds.addAttr(self.maintenence_grp, ln = "ctrl_shape_vis", at = "bool", dv=True)
        self.ctrl_shape_vis = self.maintenence_grp + ".ctrl_shape_vis"
        cmds.setAttr(self.ctrl_shape_vis, cb = True, e=True)

        # addAttr -ln "vis_fit_ctrl"  -at bool  |C_Template_GRP|C_maintenance_GRP;
        # setAttr -e-channelBox true |C_Template_GRP|C_maintenance_GRP.vis_fit_ctrl;

    def finalize_maintenence(self):
        # meant to be used after the entire rig has finished building
        # creates all neccesary attributes.
        self.groups = [self.root_grp, self.geo_grp, self.skeleton_grp, self.rig_grp, self.control_grp, self.maintenence_grp]

        # wires up the maintenence group
        # turns on drawing overrides
        # Adds visibility switches for the rig groups
        # Adds override display types for each rig group

        # cmds.setAttr(self.groups[i]+".overrideEnabled",
        #         keyable = False, 
        #         channelBox = True,)

        pass

    def __lock_attrs(self):
        "Lock out attributes"
        for i in range(len(self.groups)):
            #---lock transform
            lock_attrs(node = self.groups[i])
            #---make vis non keyable
            cmds.setAttr(self.groups[i]+".v",
                         keyable = False, 
                         channelBox = True)
            cmds.setAttr(self.groups[i]+".overrideEnabled",
                         keyable = False, 
                         channelBox = True,)


            #---expose needed attrs
            cmds.setAttr(self.groups[i]+".overrideDisplayType",
                         2,
                         keyable = False, 
                         channelBox = True,)
            cmds.setAttr(self.groups[i]+".ihi", 0)

    def __create(self):
        "Put it all together"
        self.__create_nodes()
        self.__lock_attrs()







#===============================================================================
#CLASS:         snap_pivots
#DESCRIPTION:   snaps a source list of transforms to a target transform
#USAGE:         set args and run
#RETURN:        rot_piv_attr, trans_attr, final_piv
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class snap_pivots():
    def __init__(self,
                 target="",
                 source=[]):

        """
        type  target:                string
        param target:                name of the transform that will be 
                                      snapped to (driver)

        type  source:                string array
        param source:                names of the transforms that will be
                                      snapped (driven)
        """

        #---args
        self.target                   = target
        self.source                   = source

        #---vars
        self.tmp_piv                 = ""
        self.tmp_con                 = []
        self.rot_piv_attr            = []
        self.trans_attr              = []
        self.final_piv               = []
        
        self.__do_it()

    def __create_tmp_piv(self):
        """ create a temporary transform to get clean pivots from """
        self.tmp_piv = cmds.createNode("transform")

    def __snap_tmp(self):
        """ snaps tmp piv to the target using a parent constraint """
        self.tmp_con = cmds.parentConstraint(self.target, self.tmp_piv)
        cmds.delete(self.tmp_con)

    def __get_tmp_piv(self):
        """ gets info from tmp piv """
        self.rot_piv_attr = cmds.getAttr(self.tmp_piv + ".rotatePivot")[0]
        self.trans_attr = cmds.getAttr(self.tmp_piv + ".translate")[0]
#         print self.rot_piv_attr
        self.final_piv = ((self.rot_piv_attr[0] + self.trans_attr[0]), 
                          (self.rot_piv_attr[1] + self.trans_attr[1]),
                          (self.rot_piv_attr[2] + self.trans_attr[2]))

    def __snap_source_pivs(self):
        """ snaps all pivots """
        for i in self.source:
            cmds.move(self.final_piv[0], self.final_piv[1], self.final_piv[2],  
                      (i + ".scalePivot"),
                      (i + ".rotatePivot"),rpr = True)

    def __cleanup(self):
        """ deletes all tmp nodes associate with this class """
        cmds.delete(self.tmp_piv)

    def __do_it(self):
        """ put it all together """
        self.__create_tmp_piv()
        self.__snap_tmp()
        self.__get_tmp_piv()
        self.__snap_source_pivs()
        self.__cleanup()

##########################################################
#---example
# snap_pivots(target = "l_shoulder_bind", 
#             source = ["C_ctl_CTL", 
#                       "body_geo", 
#                       "holster_geo"])
##########################################################

#===============================================================================
#CLASS:         get_dist_between
#DESCRIPTION:   gets distance between 2 transforms
#USAGE:         set args and run
#RETURN:        point_from, point_to, dist
#REQUIRES:      maya.cmds, maya.OpenMaya
#AUTHOR:        Levi Harrison
#DATE:          Oct 21st, 2014
#Version        1.0.0
#===============================================================================

class get_dist_between():
    def __init__(self, 
                 from_trans = "", 
                 to_trans = ""):
        "gets the distance between 2 transforms"
        #get distance between arm and elbow
        self.point_from = cmds.xform(from_trans, q =True, ws=True, t=True)
        self.point_to = cmds.xform(to_trans, q =True, ws=True, t=True)
        vector = OpenMaya.MVector(((self.point_from[0])-(self.point_to[0])),
                                  ((self.point_from[1])-(self.point_to[1])),
                                  ((self.point_from[2])-(self.point_to[2])))
        self.dist = vector.length()

#===============================================================================
#CLASS:         create_space_switches
#DESCRIPTION:   creates space switching, usually used on ik controls
#USAGE:         set args and run
#RETURN:        space_conditions, space_constraints, space_attr
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 21st, 2014
#Version        1.0.0
#===============================================================================

class create_space_switches():
    def __init__(self, 
                 ctl = "", 
                 ctl_grp = "", 
                 space_names = "",
                 space_parents = "",
                 ):
        "gets the distance between 2 transforms"
        """
        type  ctl:                  string array
        param ctl:                  name of the ctl that will have the space
                                     switch attrs

        type  ctl_grp:              string array
        param ctl_grp:              name of the group above the ctl
        
        type  space_names:          string array
        param space_names:          the names you would like to give your
                                     space switches (cleaner way of naming than
                                     using the space parents)

        type  space_parents:        string array
        param space_parents:        the things driving the ik control
                                     during space switching, I usually use
                                     bind joint names. Does not check for
                                     cycle errors so I need to be careful.
        """
        #---args
        self.ctl                     = ctl
        self.ctl_grp                 = ctl_grp
        self.space_names             = space_names
        self.space_parents           = space_parents
        
        #---vars
        self.space_attr             = []
        self.space_enum_name         = ""
        self.space_conditions        = []
        self.space_constraints       = []
        
        self.__create()

    def __check_exists(self):
        """make sure ctl and space parents exist, fail otherwise"""
        if cmds.objExists(self.ctl):
            for i in self.space_parents:
                if cmds.objExists(i):
                    continue
                else:
                    raise Exception(i + " does not exist, space" 
                                    + "switching will not be added")
                    quit()
        else:
            raise Exception(self.ctl + " does not exist, space switching"
                            +" will not be added")
            quit()

    def __create_attr(self):
        #---format enum names
        if self.space_names:
            if len(self.space_names) > 1:
                for i in range(len(self.space_names)):
                    if not i == len(self.space_names)-1:
                        self.space_enum_name += self.space_names[i] + ":"
                    elif i == len(self.space_names)-1:
                        self.space_enum_name += self.space_names[i]
            else:
                self.space_enum_name = self.spaceAttrNames[0]
        #---create attrs        
        cmds.addAttr(self.ctl, ln = "spaces", 
                     enumName = self.space_enum_name, 
                     k = True, 
                     at = "enum",)
        self.space_attr = self.ctl+".spaces"

    def __create_conditions(self):
        #---Create conditions
        name = self.ctl.split("_")
        name = name[0] + "_" + name[1]

        for i in range(len(self.space_parents)):
            capitalize_name = self.space_names[i][0:].capitalize()
            tmp = cmds.createNode('condition', 
                                  name = name + 
                                  capitalize_name + 
                                  'Space_CDN')
            cmds.setAttr(tmp + ".secondTerm", i)
            cmds.setAttr(tmp + ".colorIfTrueR", 1)
            cmds.setAttr(tmp + ".colorIfFalseR", 0)
            self.space_conditions.append(tmp)

    def __create_constraints(self):
        for i in self.space_parents:
            self.space_constraints.append(cmds.parentConstraint(i, 
                                                                self.ctl_grp, 
                                                                mo = True)[0])

    def __make_connections(self):
        #---connect attrs
        for i in range(len(self.space_names)):
            
            cmds.connectAttr(self.space_attr, 
                             self.space_conditions[i]+ ".firstTerm")
            
            cmds.connectAttr(self.space_conditions[i]+ ".outColorR", 
                             self.space_constraints[i] + ".w" + str(i))

    def __create(self):
        """ """
        self.__check_exists()
        self.__create_attr()
        self.__create_conditions()
        self.__create_constraints()
        self.__make_connections()

##########################################################
#---example
# create_space_switches(ctl = "L_armIK_CTL", 
#                       ctl_grp = "L_armIKBuffer2_GRP",
#                       space_names = ["world",
#                                      "shoulder",
#                                      "neck",
#                                      "hip"],
#                       space_parents= ["C_character_GRP",
#                                       "l_clavicle_bind",
#                                       "neck_bind",
#                                       "pelvis_bind"])
###########################################################

#===============================================================================
#CLASS:         create_align
#DESCRIPTION:   creates an align, usually used on fk ctls
#USAGE:         set args and run
#RETURN:        align_attr, reverse_node, align_constraint, world_transform
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 21st, 2014
#Version        1.0.0
#===============================================================================

class create_fk_align():
    def __init__(self, 
                 ctl = "", 
                 ctl_grp = "",
                 default_align_parent = "", 
                 skel_group = "",
                 maintainOffset=False
                 ):
        """
        type  ctl:                  string array
        param ctl:                  name of the ctl that will have the space
                                     switch attrs

        type  ctl_grp:              string array
        param ctl_grp:              name of the group above the ctl

        type  default_align_parent: string array
        param default_align_parent: usually the name of the group above the 
                                     ctl_grp or anything you want to be the 
                                     to be aligned to by default


        type  skel_group:           string array
        param skel_group:           the group where you parent your skeleton
        """

        #---args
        self.ctl                     = ctl
        self.ctl_grp                 = ctl_grp
        self.default_align_parent    = default_align_parent
        self.skel_group              = skel_group
        self.maintainOffset          = maintainOffset

        #---vars
        self.align_attr              = []
        self.reverse_node            = []
        self.align_constraint        = []
        self.world_transform         = []
        self.name                    = ""
        self.__create()

    def __check_exists(self):
        """make sure ctl and space parents exist, fail otherwise"""
        for i in [self.ctl,
                  self.ctl_grp,
                  self.default_align_parent,]:
            if cmds.objExists(i):
                continue
            else:
                raise Exception(i + " does not exist, space" 
                                + "switching will not be added")
                quit()

    def __create_attr(self):
        cmds.addAttr(self.ctl, ln = "world_align", at = "float", 
                     dv = 0, min = 0, max = 1)
        self.align_attr = self.ctl + ".world_align"
        cmds.setAttr(self.align_attr, k = True, cb = False)

    def __create_reverse_nodes(self):
        self.name = self.ctl.split("_")
        self.name = self.name[0] + "_" + self.name[1]
        self.reverse_node = cmds.createNode("reverse", 
                                            name = self.name + "AlignCon_REV")

    def __create_world_align(self):
        "create a transform that shares alignment with the ctl but doesn't move"
        self.world_transform = cmds.createNode("transform", 
                                               name = self.name 
                                               + "WorldAlign_GRP", 
                                               parent = self.skel_group)
        tmp = cmds.parentConstraint(self.ctl, self.world_transform)
        cmds.delete(tmp)
        cmds.setAttr(self.world_transform + ".inheritsTransform",0)

    def __create_constraints(self):
        self.align_constraint = cmds.orientConstraint(self.default_align_parent,
                                                      self.world_transform,
                                                      self.ctl_grp,
                                                      mo=True)[0]
        # rotation = cmds.xform(self.default_align_parent,q=True, ws=True, ro=True)
        # if cmds.xform(self.world_transform,q=True, ws=True, ro=True) != cmds.xform(self.default_align_parent, q=True, ws=True, ro=True):
        #     cmds.xform(self.world_transform, ws=True, ro=rotation)


    def __make_connections(self):
        #---connect default
        cmds.connectAttr(self.align_attr, 
                         self.reverse_node + ".inputX")
        cmds.connectAttr(self.reverse_node+ ".outputX", 
                         self.align_constraint + ".w0")
        #---connect world
        cmds.connectAttr(self.align_attr, 
                         self.align_constraint + ".w1")

    def __create(self):

        self.__check_exists()
        self.__create_attr()
        self.__create_reverse_nodes()
        self.__create_world_align()
        self.__create_constraints()
        self.__make_connections()

##########################################################

#---example
# create_fk_align(ctl = "L_wristFK_CTL", 
#                 ctl_grp = "L_wristFKBuffer1_GRP",
#                 default_align_parent = "L_wristFKBuffer2_GRP",
#                 world_align_parent = "C_character_GRP",
#                 skel_group = 'L_armSkel_GRP')
##########################################################


#########################
#---stand alone functions
#########################

def suffix_constraints():
    "add proper suffix to all constraints in the scene"
    cons = ["orientConstraint",
            "parentConstraint",
            "pointConstraint",
            "aimConstraint",
            "scaleConstraint",
            "poleVectorConstraint"]
    ends = ["_ORC",
            "_PAC",
            "_POC",
            "_AIC",
            "_SCC",
            "_PVC"]
    for i in range(len(cons)):
        all_cons = cmds.ls(type = cons[i])
        for j in range(len(all_cons)):
            split = all_cons[j].split("_")
            new_name = split[0]+"_"+split[1]+ends[i]
            cmds.rename(all_cons[j], new_name)



def lock_all(hierarchy = "", filter = ["*_CTL"]):
    """ for a transform, get all decendants and connections and set ihi to 0
    remove all things that have filter arg in the name from list, then lock 
    everything in list"""

    hier = []
    tmp_all = []
    tmp_all.append(hierarchy)
    rel = cmds.listRelatives(hierarchy,
                             ad = True, s=False)
    if rel:
        rel.reverse()
        for i in rel:
            tmp_all.append(i)
        hier.append(tmp_all)
        hier = hier[0]
    #     hier = cmds.listRelatives(hierarchy, ad = True )
        all = []
    #     print all
        #---set all ihi to 0
        if hier:
            for i in hier:
                all.append(cmds.listConnections(i))
            flat = []
            for i in all:
                if i:
                    flat.append(i)
            all = []
            for i in flat:
                for j in i:
                    all.append(j)
        else:
            all = [hierarchy]
        all = list(set(all))
        for i in all:
            if cmds.objExists(i + ".ihi"):
                cmds.setAttr(i + ".ihi", 0)
    #---remove filter from hierarchy, then lock all keyable attrs     
    all = hier

    all_remove = set(filter)
    all = [x for x in all if not any(fnmatch(x, y) for y in all_remove)]
    #get attrs
    for i in all:
        attrs = cmds.listAttr(i, k =True)
        if attrs:
            for j in attrs:
                if i:
                    if "." in j:
                        j = j.split(".")[0]
                    cmds.setAttr(i+"."+j, l = True, k = False, cb = False)

def select_bind_jnts():
    "selects all joints with a BIND attribute"
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".BIND")]
        if bind_jnts:
            cmds.select(bind_jnts)

# select_bind_jnts()
def non_bind_jnt_invis():
    "sets draw type for non bind joints to 0"
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        non_bind_jnts = [x for x in test_jnts if not cmds.objExists(x + ".BIND")]
        if non_bind_jnts:
            for i in non_bind_jnts:
                cmds.setAttr(i+".drawStyle",2)
            cmds.select(non_bind_jnts)


def print_translate_rotate_scale():
    sel = cmds.ls(sl = True)
    print("TRANSLATE")
    if len(sel) > 1:
        for i in range(len(sel)):
            t = cmds.getAttr(sel[i] + ".t")
            if i == 0:
                print("[" + str(t[0]) + ",")
            if i > 0 and i < len(sel)-1:
                print(str(t[0]) + ",")
            if i == len(sel)-1:
                print(str(t[0]) + "]")
    else:
        t = cmds.getAttr(sel[0] + ".t")
        print("[" + str(t[0]) + "]")
    print("ROTATE")
    if len(sel) > 1:
        for i in range(len(sel)):
            t = cmds.getAttr(sel[i] + ".r")
            if i == 0:
                print("[" + str(t[0]) + ",")
            if i > 0 and i < len(sel)-1:
                print(str(t[0]) + ",")
            if i == len(sel)-1:
                print(str(t[0]) + "]")
    else:
        t = cmds.getAttr(sel[0] + ".r")
        print("[" + str(t[0]) + "]")
    print("SCALE")
    if len(sel) > 1:
        for i in range(len(sel)):
            t = cmds.getAttr(sel[i] + ".s")
            if i == 0:
                print("[" + str(t[0]) + ",")
            if i > 0 and i < len(sel)-1:
                print(str(t[0]) + ",")
            if i == len(sel)-1:
                print(str(t[0]) + "]")
    else:
        t = cmds.getAttr(sel[0] + ".s")
        print("[" + str(t[0]) + "]")



# print_translate_rotate_scale()
def select_secondary_bind_jnts():
    "selects all joints with a BIND attribute"
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".SEC_BIND")]
        if bind_jnts:
            cmds.select(bind_jnts)
# select_secondary_bind_jnts()

def select_all_bind_jnts():
    "selects all joints with a BIND attribute"
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".SEC_BIND") or cmds.objExists(x + ".BIND")]
        if bind_jnts:
            cmds.select(bind_jnts)


def sec_bind_jnt_vis():
    "sets draw type for non bind joints to 0"
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        non_bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".SEC_BIND")]
        if non_bind_jnts:
            for i in non_bind_jnts:
                cmds.setAttr(i+".drawStyle",0)
# sec_bind_jnt_vis()

def skin_jnt_vis():
    "sets draw type for non bind joints to 0"
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        non_bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".SKIN")]
        if non_bind_jnts:
            for i in non_bind_jnts:
                cmds.setAttr(i+".drawStyle",0)


def cleanup_geo():
    #get all correctly named geo and put it into the geo group
    if cmds.objExists("C_geo_GRP"):
        geos = cmds.ls("*_GEO")
        cmds.parent(geos, "C_geo_GRP")
    #get all correctly named geo and put it into the geo group
        cmds.setAttr("C_geo_GRP.overrideEnabled", 1)



def cleanup_skel():
    if cmds.objExists("C_skeleton_GRP"):
        #cmds.setAttr("C_skeleton_GRP.overrideEnabled", 1)
        cmds.setAttr("C_skeleton_GRP.v", 0)



# a function to print and format point positions for gl drawings in python
def printPointsPY(object=None):
    if not object: object = cmds.ls(sl=True)[0]
#     curve = cmds.listRelatives(object, type = "nurbsCurve", )
    curveNode = OpenMaya.MSelectionList()
    curveNode.add(object)
    pPath = OpenMaya.MDagPath()
    curveNode.getDagPath(0,pPath)
    fnCurve = OpenMaya.MFnNurbsCurve(pPath)
    
    points = OpenMaya.MPointArray()
    fnCurve.getCVs(points)
    for i in range(points.length()):
        if i == 0:
            print("[(" + str(points[i][0]) + ", " + str(points[i][1]) + ", " + str(points[i][2]) + "),")

        if i != 0 and i != points.length()-1:
            print("(" + str(points[i][0]) + ", " + str(points[i][1]) + ", " + str(points[i][2]) + "),")
        
        if i == points.length()-1:
            print("(" + str(points[i][0]) + ", " + str(points[i][1]) + ", " + str(points[i][2]) + ")]")


# a function to print and format point positions for gl drawings in cpp
def printPointsCPP(object=None):
    if not object: object = cmds.ls(sl=True)[0]
    curveNode = OpenMaya.MSelectionList()
    curveNode.add(object)
    pPath = OpenMaya.MDagPath()
    curveNode.getDagPath(0,pPath)
    fnCurve = OpenMaya.MFnNurbsCurve(pPath)
    
    points = OpenMaya.MPointArray()
    fnCurve.getCVs(points)
    for i in range(points.length()):
        if i == 0:
            print("{{" + str(points[i][0]) + "f, " + str(points[i][1]) + "f, " + str(points[i][2]) + "f},")
        if i != 0 and i != points.length()-1:
            print("{" + str(points[i][0]) + "f, " + str(points[i][1]) + "f, " + str(points[i][2]) + "f},")
        if i == points.length()-1:
            print("{" + str(points[i][0]) + "f, " + str(points[i][1]) + "f, " + str(points[i][2]) + "f}}")

def printIntArray():
    selectedPoints = cmds.ls(sl=True, fl=True)
    points = [str(s.split("[")[1].split("]")[0]) for s in selectedPoints]
    pointArray = ""
    for i , intName in enumerate(points):
        if i == 0:
            pointArray += "{" + intName + ", "
        if i != 0 and i != len(points)-1:
            pointArray += intName + ", "
        if i == len(points)-1:
            pointArray += intName + "}"
    print(pointArray)

# setFaceIdsOnLocator("C_bLip_LOC")

def rename_wild_card_attributes(deformer, string, rename_string):
    wild_string = "*" +string + "*"
    tmp_attrs = cmds.listAttr(deformer ,
                              st = wild_string,
                              ud = True)
#     print tmp_attrs
    for i in range(len(tmp_attrs)):
        old_str = deformer + "." + tmp_attrs[i]
        old = str(tmp_attrs[i])
        new = str(rename_string)
#         print old,new
        new_str = old.replace(string, rename_string)
        if cmds.objExists(old_str):
            print(old_str, new_str)
#         this = cmds.renameAttr(old_str, new_str)
#         print this
#         print deformer + "." + tmp_attrs[i]
#         print deformer + "." + tmp_attrs + 
#rename_wild_card_attributes("C_mouth_SLD","UWeights", "Weights")

def select_skin_jnts():
    "selects all joints with a BIND attribute"
    test_jnts = cmds.ls(type = "joint")
    if test_jnts:
        bind_jnts = [x for x in test_jnts if cmds.objExists(x + ".SKIN")]
        if bind_jnts:
            cmds.select(bind_jnts)

def create_bind_skel(children = [],
                     parents = [],
                     character_grp = "C_character_GRP",
                     rig_parent = "C_rig_GRP"):
    #---place to store it
    skel_parent = cmds.createNode("transform",
                              n = "C_bindSkeleton_GRP",
                              p = character_grp)
    select_bind_jnts()
    AllBones = cmds.ls(sl = True)
    roots = []
    
    for i in range(len(AllBones)):
        parent = cmds.listRelatives( AllBones[i],
                                     parent=True)
        if parent:
            #if cmds.objExists(parent[0] + ".BIND") == False:
            
            
            if cmds.attributeQuery('BIND', node = parent[0], ex = True) == False and cmds.attributeQuery('SEC_BIND', node = parent[0], ex = True) == False :
            #if cmds.objectType(parent[0]) != "joint":
                if AllBones[i] not in roots:
                    roots.append(AllBones[i])
                    #print AllBones[i]
    new_bones = []
    for i in range(len(roots)):
        if cmds.objExists(roots[i]):
            if cmds.objExists(roots[i] + "_FIX") == False:
            
                bone = cmds.duplicate(roots[i], n = roots[i] + "_FIX")[0]
                trash = cmds.listRelatives(bone, type = "parentConstraint", pa = True, ad = True)
                cmds.delete(trash)
                trash = cmds.listRelatives(bone, type = "pointConstraint", pa = True, ad = True)
                cmds.delete(trash)
                trash = cmds.listRelatives(bone, type = "scaleConstraint", pa = True, ad = True)
                cmds.delete(trash)
                trash = cmds.listRelatives(bone, type = "orientConstraint", pa = True, ad = True)
                cmds.delete(trash)
                trash = cmds.listRelatives(bone, type = "ikEffector", pa = True, ad = True)
                cmds.delete(trash)
    
                relatives_long = cmds.listRelatives(bone, type = "joint", pa = True, ad = True)
                relatives_short = cmds.listRelatives(bone, type = "joint", ad = True)
                if relatives_long:
                    for i in range(len(relatives_long)):
                        cmds.rename(relatives_long[i],  relatives_short[i] + "_FIX")
                if bone:
                    cmds.parent(bone,skel_parent)
    #---parenting
    for i in range(len(parents)):
        cmds.parent(children[i],parents[i])
    skel_relatives = cmds.listRelatives(skel_parent, type = "joint", ad = True)
    jnt_names = []
    for i in range(len(skel_relatives)):
        
        if cmds.attributeQuery('BIND', node = skel_relatives[i], ex = True) == True :

            cmds.setAttr( skel_relatives[i] + ".BIND", l = False, cb = False, k = False)
    
            cmds.deleteAttr(skel_relatives[i], at = "BIND")
        
        
        cmds.addAttr(skel_relatives[i], 
                     ln = "SKIN",
                     at = "bool",)
        cmds.setAttr(skel_relatives[i] + ".SKIN", 
                     l = True, 
                     k=False)
        name = skel_relatives[i].split("_JNT_FIX")[0]
        new_name = cmds.rename(skel_relatives[i], name + "_BIND")
        jnt_names.append(name)
        cmds.parentConstraint(name + "_JNT", new_name)
        cmds.scaleConstraint(name + "_JNT", new_name)

def set_global_jnt_radius(radius=1.0):
    for jnt in cmds.ls(type="joint"):
        cmds.setAttr(jnt + ".radius", radius)

def create_sec_bind_skel(children = [],
                     parents = [],
                     character_grp = "C_character_GRP",
                     rig_parent = "C_rig_GRP"):
    #---place to store it
    skel_parent = cmds.createNode("transform",
                              n = "C_bindSkeleton_GRP",
                              p = character_grp)
    select_secondary_bind_jnts()
    AllBones = cmds.ls(sl = True)
    roots = []
    
    for i in range(len(AllBones)):
        parent = cmds.listRelatives( AllBones[i],
                                     parent=True)
        if parent:
            #if cmds.objExists(parent[0] + ".BIND") == False:
            
            
            if cmds.attributeQuery('SEC_BIND', node = parent[0], ex = True) == False :
            #if cmds.objectType(parent[0]) != "joint":
                if AllBones[i] not in roots:
                    roots.append(AllBones[i])
                    #print AllBones[i]
    new_bones = []
    for i in range(len(roots)):
        if cmds.objExists(roots[i]):
            if cmds.objExists(roots[i] + "_FIX") == False:
            
                bone = cmds.duplicate(roots[i], n = roots[i] + "_FIX")[0]
                trash = cmds.listRelatives(bone, type = "parentConstraint", pa = True, ad = True)
                cmds.delete(trash)
                trash = cmds.listRelatives(bone, type = "pointConstraint", pa = True, ad = True)
                cmds.delete(trash)
                trash = cmds.listRelatives(bone, type = "scaleConstraint", pa = True, ad = True)
                cmds.delete(trash)
                trash = cmds.listRelatives(bone, type = "orientConstraint", pa = True, ad = True)
                cmds.delete(trash)
                trash = cmds.listRelatives(bone, type = "ikEffector", pa = True, ad = True)
                cmds.delete(trash)
    
                relatives_long = cmds.listRelatives(bone, type = "joint", pa = True, ad = True)
                relatives_short = cmds.listRelatives(bone, type = "joint", ad = True)
                if relatives_long:
                    for i in range(len(relatives_long)):
                        cmds.rename(relatives_long[i],  relatives_short[i] + "_FIX")
                if bone:
                    cmds.parent(bone,skel_parent)
    #---parenting
    for i in range(len(parents)):
        cmds.parent(children[i],parents[i])
    skel_relatives = cmds.listRelatives(skel_parent, type = "joint", ad = True)
    jnt_names = []
    for i in range(len(skel_relatives)):
        
        if cmds.attributeQuery('SEC_BIND', node = skel_relatives[i], ex = True) == True :

            cmds.setAttr( skel_relatives[i] + ".SEC_BIND", l = False, cb = False, k = False)
    
            cmds.deleteAttr(skel_relatives[i], at = "SEC_BIND")
        
        
        cmds.addAttr(skel_relatives[i], 
                     ln = "SEC_SKIN",
                     at = "bool",)
        cmds.setAttr(skel_relatives[i] + ".SEC_SKIN", 
                     l = True, 
                     k=False)
        name = skel_relatives[i].split("_JNT_FIX")[0]
        new_name = cmds.rename(skel_relatives[i], name + "_BIND")
        jnt_names.append(name)
        cmds.parentConstraint(name + "_JNT", new_name)
        cmds.scaleConstraint(name + "_JNT", new_name)

def getShape(mayaObject):
    # double check it isn't already a mesh, just in case a transform is passed in...
    objectType = cmds.objectType(mayaObject)
    if objectType == "mesh" or objectType == "nurbsCurve" or objectType == "nurbsSurface" or objectType == "lattice":
        return mayaObject
    relatives = cmds.listRelatives(mayaObject, shapes=True)
    if relatives:
        return relatives[0]
    return

def getShapeMultiple(mayaObject):
    # double check it isn't already a mesh, just in case a transform is passed in...
    objectType = cmds.objectType(mayaObject)
    if objectType == "mesh" or objectType == "nurbsCurve" or objectType == "nurbsSurface" or objectType == "lattice":
        return mayaObject
    relatives = cmds.listRelatives(mayaObject, shapes=True)
    if relatives:
        return relatives
    return

def getGeoData(mayaObject=None):
    """Returns a dictionary that can be used with exportUtils to create_mesh
    create_nurbs_surface, or create_nurbs_curve
    """
    if not mayaObject: mayaObject = cmds.ls(sl=True)[0]
    shape = getShape(mayaObject)
    if (cmds.objectType(shape, isType='nurbsSurface')):
        return exportUtils.nurbsSurfaceData(name=mayaObject).nurbs
    if (cmds.objectType(shape, isType='mesh')):
        return exportUtils.meshData(name=mayaObject).mesh
    if (cmds.objectType(shape, isType='nurbsCurve')):
        return exportUtils.nurbsCurveData(name=mayaObject).nurbsCurve

def createGeoFromData(geomDict=None, name=None, parent=None):
    """
    Creates geometry based on a dictionary created from exportUtils
    param geomDict: dictionary of geometry
    @return: 
    """
    if (geomDict["type"] == "nurbsSurface"):
        return exportUtils.createNurbsSurface(geomDict, name, parent)
    if (geomDict["type"] == "mesh"):
        return exportUtils.createMesh(geomDict, name, parent)
    if (geomDict["type"] == "nurbsCurve"):
        return exportUtils.create_curve(geomDict, name, parent)

def formatName(side, name, suffix):
    return "{0}_{1}_{2}".format(side, name, suffix)

def createLocator(name=None, parent=None, vis=True, shapeVis=True):
    transform = cmds.createNode("transform", name=name, parent=parent)
    shape = cmds.createNode("locator", name="{0}Shape".format(name), parent=transform)
    if not vis:
        cmds.setAttr(transform + ".v", 0)
    if not shapeVis:
        cmds.setAttr(shape + ".v", 0)
    return transform

def createAndConnectNode(type=None, name=None, srcOutput=None,
                         selfInput=None, selfOutput=None, dstInput=None):
    node = cmds.createNode(type, name=name)
    print(node)

    if srcOutput and selfInput:
        cmds.connectAttr(srcOutput, "{0}.{1}".format(node, selfInput))
    if selfOutput and dstInput:
        cmds.connectAttr("{0}.{1}".format(node, selfOutput), dstInput)
    return node



def pushCurveShape(sourceCurve=None, targetCurve=None, mirror=False, inheritColor=False):
    if not sourceCurve and not targetCurve:
        sourceCurve = cmds.ls(sl=True)[0]
        targetCurve = cmds.ls(sl=True)[1]
    if not cmds.objectType(sourceCurve, isType='nurbsCurve'):
        sourceCurve = cmds.listRelatives(sourceCurve, type = "nurbsCurve")[0]
    if not cmds.objectType(targetCurve, isType='nurbsCurve'):
        targetCurve = cmds.listRelatives(targetCurve, type = "nurbsCurve")[0]

    parentNode = OpenMaya.MSelectionList()
    parentNode.add(targetCurve)
    parentPath = OpenMaya.MDagPath()
    parentNode.getDagPath(0,parentPath)
    parentMObject = parentPath.transform()

    source = OpenMaya.MSelectionList()
    source.add(sourceCurve)
    sourcePath = OpenMaya.MDagPath()
    source.getDagPath(0,sourcePath)
    sourceMFnCurve = sourcePath.node()

    nurbsCurve_node = OpenMaya.MSelectionList()
    nurbsCurve_node.add(targetCurve)
    nurbsCurve_path = OpenMaya.MDagPath()
    nurbsCurve_node.getDagPath(0,nurbsCurve_path)
    fn_nurbsCurve = OpenMaya.MFnNurbsCurve(nurbsCurve_path)
    dummy = OpenMaya.MObject()

    curveColor = targetCurve

    if not inheritColor:
        curveColor = sourceCurve

    color = cmds.getAttr(curveColor + ".overrideColor")
    override = cmds.getAttr(curveColor + ".overrideRGBColors")

    colorR = cmds.getAttr(curveColor + ".overrideColorR")
    colorG = cmds.getAttr(curveColor + ".overrideColorG")
    colorB = cmds.getAttr(curveColor + ".overrideColorB")
    cmds.delete(targetCurve)
    newShape = fn_nurbsCurve.copy(sourceMFnCurve, parentMObject)
    path = nurbsCurve_path.getAPathTo(newShape)
    cmds.setAttr(path.fullPathName() + ".overrideRGBColors", override)
    cmds.setAttr(path.fullPathName() + ".overrideEnabled", True)
    cmds.setAttr(path.fullPathName() + ".overrideColor", color)
    cmds.setAttr(path.fullPathName() + ".overrideColorR", colorR)
    cmds.setAttr(path.fullPathName() + ".overrideColorG", colorG)
    cmds.setAttr(path.fullPathName() + ".overrideColorB", colorB)
    cmds.rename(path.fullPathName(), targetCurve)

    if mirror:
        numCV = fn_nurbsCurve.numCVs()
        points = path.fullPathName() + '.cv[0:{0}]'.format(numCV)
        cmds.scale(-1.0, points, r=True, scaleX=True, scaleY=False, scaleZ=False, )

'''
#button press
tool = maya.cmds.weightSlideContext()
maya.cmds.setToolTo( tool )
#button release
maya.cmds.deleteUI(tool)
maya.mel.eval("SelectToolOptionsMarkingMenu;MarkingMenuPopDown;")
'''

def getClosestUVOnMesh(pointX=None, pointY=None, pointZ=None, transform=None, mesh=None):
    debug=False
    if not pointX and not pointY and not pointZ and not transform and not mesh:
        # driver driven selection order
        mesh = cmds.ls(sl=True)[0]
        transform = cmds.ls(sl=True)[1]
        debug = True
    if transform:
        xform = cmds.xform(transform, q=True, a=True, ws=True, t=True)
        pointX = xform[0]
        pointY = xform[1]
        pointZ = xform[2]
    mesh = getShape(mesh)
    closestPointNode = cmds.createNode("closestPointOnMesh")
    cmds.connectAttr(mesh + ".outMesh", closestPointNode + ".inMesh")
    cmds.setAttr(closestPointNode+".inPositionX", pointX)
    cmds.setAttr(closestPointNode+".inPositionY", pointY)
    cmds.setAttr(closestPointNode+".inPositionZ", pointZ)
    u = cmds.getAttr(closestPointNode+".parameterU")
    v = cmds.getAttr(closestPointNode+".parameterV")
    cmds.delete(closestPointNode)
    # for debug
    if debug:
        print(u, v)
    return u, v

# def removeRotationFromPointOnPolyConstraint(pointOnPolyConstraint);

def closestPointOnPolyConstraint(name="test_PPC", closestPointNodeName="test_CPM", driverMesh=None, drivenTransform=None ):
    if not driverMesh and not drivenTransform:
        # driver driven selection order
        driverMesh = cmds.ls(sl=True)[0]
        drivenTransform = cmds.ls(sl=True)[1]
    driverMesh = getShape(driverMesh)
    u, v = getClosestUVOnMesh(transform=drivenTransform, mesh=driverMesh)
    # closestPointNode = cmds.createNode("closestPointOnMesh", n=closestPointNodeName)
    # cmds.connectAttr(driverMesh + ".outMesh", closestPointNode + ".inMesh")
    # cmds.connectAttr(closestPointNode + ".position", drivenTransform+".translate")

    constraint = cmds.pointOnPolyConstraint(driverMesh,
                                            drivenTransform,
                                            name = name)[0]
    cmds.setAttr(constraint + " .u0", u)
    cmds.setAttr(constraint + " .v0", v)
    return constraint

def getParent(mayaObject):
    return cmds.listRelatives( mayaObject, parent=True)[0]

def getOMMesh(mayaObject):
    meshNode = OpenMaya.MSelectionList()
    meshNode.add(mayaObject)
    pPath = OpenMaya.MDagPath()
    meshNode.getDagPath(0,pPath)
    return OpenMaya.MFnMesh(pPath)

def getOMAnimCurve(mayaObject):
    curveNode = OpenMaya.MSelectionList()
    curveNode.add(mayaObject)
    curvePlug = OpenMaya.MPlug()
    curveNode.getPlug(0, curvePlug)
    curveNode = curvePlug.node()
    return OpenMayaAnim.MFnAnimCurve(curveNode)

def getOMNurbsCurve(mayaObject):
    meshNode = OpenMaya.MSelectionList()
    meshNode.add(mayaObject)
    pPath = OpenMaya.MDagPath()
    meshNode.getDagPath(0,pPath)
    return OpenMaya.MFnNurbsCurve(pPath)

def getOMNurbsSurface(mayaObject):
    meshNode = OpenMaya.MSelectionList()
    meshNode.add(mayaObject)
    pPath = OpenMaya.MDagPath()
    meshNode.getDagPath(0,pPath)
    return OpenMaya.MFnNurbsSurface(pPath)

def getOMItergeo(mayaObject):
    meshNode = OpenMaya.MSelectionList()
    meshNode.add(mayaObject)
    pPath = OpenMaya.MDagPath()
    meshNode.getDagPath(0,pPath)
    return OpenMaya.MItGeometry(pPath)

def getDag(mayaObject):
    meshNode = OpenMaya.MSelectionList()
    meshNode.add(mayaObject)
    pPath = OpenMaya.MDagPath()
    meshNode.getDagPath(0,pPath)
    return pPath

def getMPointFromTransform(mayaObject):
    transformPoint = cmds.xform(mayaObject, 
                                q =True, 
                                ws=True, 
                                t=True)
    return OpenMaya.MPoint(transformPoint[0], transformPoint[1], transformPoint[2])


def getClosestPolygonToTransform(meshObject, transform):
    transformPoint = getMPointFromTransform(transform)
    fnMesh = getOMMesh(meshObject)
    closest_point = OpenMaya.MPoint()
    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    face_id = util.asIntPtr()
    fnMesh.getClosestPoint(transformPoint,
                            closest_point,
                            OpenMaya.MSpace.kWorld,
                            face_id)
    face_id = OpenMaya.MScriptUtil(face_id).asInt()
    point_ids = OpenMaya.MIntArray()
    fnMesh.getPolygonVertices(face_id, point_ids)
    pointA, pointB, pointC = get3PointsFromPolyID(fnMesh, point_ids)
    return point_ids, closest_point, pointA, pointB, pointC

def getClosestPointOnCurve(curve, position):
    point_to_check = OpenMaya.MPoint(position[0], position[1], position[2])
    fnCurve = getOMNurbsCurve(curve)
    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    util = OpenMaya.MScriptUtil()
    param = util.asDoublePtr()
    closest_point = fnCurve.closestPoint(point_to_check, param, OpenMaya.MSpace.kWorld)

    return [closest_point.x, closest_point.y, closest_point.z]


def get3PointsFromPolyID(fnMesh, intArray):
    pointA = OpenMaya.MPoint()
    pointB = OpenMaya.MPoint()
    pointC = OpenMaya.MPoint()
    pointD = OpenMaya.MPoint()
    fnMesh.getPoint(intArray[0], pointA, OpenMaya.MSpace.kWorld)
    fnMesh.getPoint(intArray[1], pointB, OpenMaya.MSpace.kWorld)
    fnMesh.getPoint(intArray[2], pointC, OpenMaya.MSpace.kWorld)
    # get average point if more than 3 points
    if intArray.length() >= 4:
        fnMesh.getPoint(intArray[3], pointD, OpenMaya.MSpace.kWorld)
        pointC = OpenMaya.MVector(pointC.x + pointD.x, pointC.y + pointD.y, pointC.z + pointD.z)/2.0;
    pointA = OpenMaya.MVector(pointA)
    pointB = OpenMaya.MVector(pointB)
    pointC = OpenMaya.MVector(pointC)
    return pointA, pointB, pointC

def getBarycentricCoords(closestPoint, pointA, pointB, pointC):
    vector0 = pointA - pointC
    vector1 = pointB - pointC
    vector2 = OpenMaya.MVector(closestPoint) - pointC
    dot00 = vector0 * vector0
    dot01 = vector0 * vector1
    dot11 = vector1 * vector1
    dot20 = vector2 * vector0
    dot21 = vector2 * vector1
    denominator = dot00 * dot11 - dot01 * dot01
    weightA = (dot11 * dot20 - dot01 * dot21) / denominator
    weightB = (dot00 * dot21 - dot01 * dot20) / denominator
    weightC = 1.0 - weightA - weightB
    return [weightA, weightB, weightC]

def getSetMaintainOffset(transform=None, offsetTransform=None, maintainOffsetT=True, maintainOffsetR=True, maintainOffsetS=True):
    """
    By giving a valid dictionary with translate and or rotate and or scale keys to the offsetTransform arg you will set offsets
    If you set offsetTransform to None, you will get offsets

    """
    if not transform:
        return

    if not offsetTransform:
        offsetTransform = {}
        if maintainOffsetT:
            offsetTransform["translate"] = cmds.xform(transform, q =True, ws=True, t=True)
        if maintainOffsetR:
            offsetTransform["rotate"] = cmds.xform(transform, q =True, ws=True, ro=True)
        if maintainOffsetS:
            offsetTransform["scale"] = cmds.xform(transform, q =True, ws=True, s=True)
        return offsetTransform

    if "translate" in offsetTransform:
        cmds.xform(transform, ws=True, t=offsetTransform["translate"])
    if "rotate" in offsetTransform:
        cmds.xform(transform, ws=True, ro=offsetTransform["rotate"])
    if "scale" in offsetTransform:
        cmds.xform(transform, ws=True, s=offsetTransform["scale"])

def geoConstraint(driverMesh=None, driven=None, parent=None, name=None, translate=True, rotate=True, scale=False,
                  offsetBuffer = None, maintainOffsetT=True, maintainOffsetR=True, maintainOffsetS=True, normalConstraintPatch=None,
                  up_vector_object="", up_vector=[0,1,0], up_vec_mult=100, aim_vector=[0,0,1]):
    """
    suffix GCS
    """
    if not driverMesh and not driven: 
        driverMesh = cmds.ls(sl=True)[0]
        driven = cmds.ls(sl=True)[1]
    driverMesh = getShape(driverMesh)
    if not name:
        name = "C_test_GCS"
    if offsetBuffer:
        offsetTransform = getSetMaintainOffset(offsetBuffer, None, maintainOffsetT, maintainOffsetR, maintainOffsetS)
    constraint = cmds.createNode("LHGeometryConstraint", n=name)
    int_array, closest_point, pointA, pointB, pointC = getClosestPolygonToTransform(driverMesh, driven)
    pointIdAttrs = ["a", "b", "c", "d"]
    # just in case we get back an ngon, set a hard range....
    idRange = 4
    if int_array.length() == 3:
        pointIdAttrs = ["a", "b", "c"]
        idRange = 3
    for idx in range(idRange):
        cmds.setAttr(constraint + "." + pointIdAttrs[idx] + "PointIdx", int_array[idx])
    weights = getBarycentricCoords(closest_point, pointA, pointB, pointC)
    for idx, attrSuffix in enumerate(["X", "Y", "Z"]):
        cmds.setAttr(constraint + ".baryWeights" + attrSuffix, weights[idx])
    
    cmds.connectAttr(driverMesh + ".worldMesh", constraint + ".inMesh" )
    decompose = cmds.createNode("decomposeMatrix", n = name + "_DCP")
    
    cmds.connectAttr(constraint + ".outputMatrix", decompose + ".inputMatrix")

    if translate:
        cmds.connectAttr(decompose + ".outputTranslate", driven + ".translate" )
    if rotate and not normalConstraintPatch:
        cmds.connectAttr(decompose + ".outputRotate", driven + ".rotate" )
    elif normalConstraintPatch:
        cmds.normalConstraint(normalConstraintPatch, driven, u=up_vector, wuo=up_vector_object, worldUpType="object", aimVector=aim_vector)
        reorient_normal_constraint_up_vector_object(up_vector_object, driven, up_vector, up_vec_mult=up_vec_mult)
        # cmds.normalConstraint(normalConstraintPatch, driven)

    if scale:
        cmds.connectAttr(decompose + ".outputScale", driven + ".scale" )
    if offsetBuffer:
        getSetMaintainOffset(offsetBuffer, offsetTransform)
        message_utils.create_message_attr_setup(constraint, "offsetBuffer", offsetBuffer, "geoConstraint")
    
    if up_vector_object:
        message_utils.create_message_attr_setup(constraint, "upVectorObject", up_vector_object, "geoConstraint")
        
    message_utils.create_message_attr_setup(constraint, "drivenObject", driven, "geoConstraint")

    return constraint

def reorient_normal_constraint_up_vector_object(up_vector_object, driven_object, up_vector=[0,1,0], up_vec_mult=100):
    # make sure the mult is high enough to never allow flipping.... 1000 seems to be more than enough
    # Assumes the normal isn't horizontal planar....
    # The normal should be at least slightly elevated in one axis...
    driven_location = cmds.xform(driven_object, q=True, ws=True, t=True)
    driven_location_up_adjusted = [driven_location[0] + up_vector[0], driven_location[1] + up_vector[1], driven_location[2] + up_vector[2]]
    cmds.xform(up_vector_object, ws=True, t=driven_location_up_adjusted )
    # rotation should now be relatively straight...
    driven_rotation = cmds.xform(driven_object, q=True, ws=True, ro=True)
    # put the up vector in the same planar space as the driven_object
    cmds.xform(up_vector_object, ws=True, t=driven_location, ro=driven_rotation)
    up_vector_object_trans= cmds.xform(up_vector_object, q=True, os=True, t=True)
    up_vector_object_trans_adjusted =  [up_vector_object_trans[0] + up_vector[0] * up_vec_mult,
                                        up_vector_object_trans[1] + up_vector[1] * up_vec_mult,
                                        up_vector_object_trans[2] + up_vector[2] * up_vec_mult]
    # translate in the up vector in the plane space
    cmds.xform(up_vector_object, os=True, t=up_vector_object_trans_adjusted)


def updateGeoConstraint(offsetBuffer=False,
                        geoConstraint=False,
                        maintainOffsetT=True,
                        maintainOffsetR=True,
                         maintainOffsetS=True,
                         up_vector=[0,1,0],
                         up_vec_mult=100
                         ):
    if geoConstraint and not offsetBuffer:
        offsetBuffer = message_utils.get_node_from_message_out(geoConstraint + ".offsetBuffer")
    if offsetBuffer and not geoConstraint:
        geoConstraint = message_utils.get_node_from_message_in(offsetBuffer + ".geoConstraint")
    if offsetBuffer:
        up_vector_object = message_utils.get_node_from_message_in(offsetBuffer + ".upVectorObject")

    if not offsetBuffer:
        return
    
    # offsetBuffer = cmds.ls(sl=True)[0]
        
    if not geoConstraint:
        geoConstraint = cmds.listConnections(cmds.ls(sl=True)[0] + ".geoConstraint")[0]

    offsetTransform = getSetMaintainOffset(offsetBuffer, None, maintainOffsetT, maintainOffsetR, maintainOffsetS)
    mesh = cmds.listConnections(geoConstraint + ".inMesh", sh=True)[0]
    int_array, closest_point, pointA, pointB, pointC = getClosestPolygonToTransform(mesh, offsetBuffer)
    pointIdAttrs = ["a", "b", "c", "d"]
    # just in case we get back an ngon, set a hard range....
    idRange = 4
    if int_array.length() == 3:
        pointIdAttrs = ["a", "b", "c"]
        idRange = 3
    for idx in range(idRange):
        cmds.setAttr(geoConstraint + "." + pointIdAttrs[idx] + "PointIdx", int_array[idx])
    weights = getBarycentricCoords(closest_point, pointA, pointB, pointC)
    for idx, attrSuffix in enumerate(["X", "Y", "Z"]):
        cmds.setAttr(geoConstraint + ".baryWeights" + attrSuffix, weights[idx])
    getSetMaintainOffset(offsetBuffer, offsetTransform)
    if up_vector_object:
        driven_object = message_utils.get_node_from_message_in(offsetBuffer + ".drivenObject")
        reorient_normal_constraint_up_vector_object(up_vector_object, driven_object, up_vector=[0,1,0], up_vec_mult=up_vec_mult)

def move(transform=None, translate=None, rotate=None, scale=None):
    if not transform:
        return
    if translate:
        cmds.xform(transform, ws=True, t=translate)
    if rotate:
        cmds.xform(transform, ws=True, ro=rotate)
    if scale:
        cmds.xform(transform, ws=True, s=scale)

def getSideColors(side):
    if side == "C":
        return (1,1,0)
    if side == "L":
        return (0,0,1)
    if side == "R":
        return (1,0,0)

def setFaceIdsOnLocator(locatorName, faces=None):
    if not faces:
        faces = cmds.ls(sl = True, fl=True)
    faces = [x.split("[")[1] for x in faces]
    faces = [x.split("]")[0] for x in faces]
    faces = [int(x) for x in faces]
    cmds.setAttr(locatorName + ".faceIds", faces, type = "doubleArray")

def createNakedLocator( name, side, geom, controlParent, parent, faces):
    locator = cmds.createNode("LHNakedLocator", p=parent, n=name)
    geom = getShape(geom)
    cmds.connectAttr(geom + ".worldMesh", locator + ".geom")
    cmds.connectAttr(controlParent + ".worldInverseMatrix", locator + ".nakedInverseMatrix")
    setFaceIdsOnLocator(locator, faces)
    colors = getSideColors(side)
    for idx, color in enumerate(["r", "g", "b"]):
        cmds.setAttr(locator + "." + color, colors[idx])
    return locator

def addNakedLocatorToControl(control=None, side= None, controlParent=None, geom=None, faces=None, locator=None, name=None):
    if not control:
        control = cmds.ls(sl=True)[0]
    if not faces:
        faces = cmds.ls(sl=True, fl=True)[1:]
    if not name:
        if "_CTL" in control:
            name = control.replace("_CTL", "Naked_SHP")
        else:
            name = "{0}nakedSHP".format(name)
    if not geom:
        geom = faces[0].split(".")[0]
    if not side:
        side = control.split("_")[0]
    if not controlParent:
        print(control)
        controlParent = cmds.listRelatives(control, parent=True)[0]
        print(controlParent)
    if not locator:
        createNakedLocator( name, side, geom, controlParent, control, faces)
        # locator = cmds.createNode("LHNakedLocator", p=control, n=name)

# def getBoundingBox(mesh):
#     # THIS CRASHES MAYA
#     fnMesh = getOMMesh(mesh)
#     meshDag = getDag(mesh)
#     allPoints = OpenMaya.MPointArray()
#     fnMesh.getPoints(allPoints)
#     bBox = OpenMaya.MBoundingBox()
#     for point in allPoints:
#         bBox.expand(point)
#     return bBox

def constrainMeshToClosestJoint(selections=None):
    """
    select only mesh transforms and joints
    """
    if not selections:
        selections = cmds.ls(sl=True)
    joints = cmds.ls(selections, type="joint")
    meshTransforms = cmds.ls(selections, type="transform")
    meshes = [getShape(x) for x in meshTransforms if getShape(x)]
    geomConstDict={}
    jointPosList = [getMPointFromTransform(x) for x in joints]
    for idx, mesh in enumerate(meshes):
        initDist = 1000
        foundID = -1
        mshCenter  =  cmds.getAttr(mesh + ".center" )[0]
        mshCenter = OpenMaya.MPoint(mshCenter[0],mshCenter[1],mshCenter[2])
        # mshCenter = getBoundingBox(mesh).center()
        for idx in range(0, len(joints)):
            dist = mshCenter.distanceTo(jointPosList[idx])
            if dist < initDist:
                initDist = dist
                foundID = idx
        # print foundID
        transform = cmds.listRelatives(mesh, p=True)[0]
        geomConstDict[transform] = joints[foundID]

    for driven, driver in list(geomConstDict.items()):
        cmds.parentConstraint(driver, driven, mo=True)
        cmds.scaleConstraint(driver, driven, mo=True)

def getSide(name):
    return name.split("_")[0]

def getName(name):
    return name.split("_")[1]

def getNameSide(stringCharacters):
    retSide = stringCharacters.split("_")[0]
    retName = stringCharacters.split("_")[1]
    return retSide, retName

def getGeomTypeAttr(mayaObject):
    retGeoType = ".worldMesh"
    objectType = cmds.objectType(mayaObject)
    if objectType == "nurbsCurve" or objectType == "nurbsSurface":
        retGeoType = ".worldSpace"
    if objectType == "lattice":
        retGeoType = ".worldLattice"
    return retGeoType

def printPointIndicies():
    indicies = cmds.ls(sl=True, fl=True)
    indicies = [int(x.split("[")[1].split("]")[0]) for x in indicies]
    return indicies


# def tag_guide_shape(node_to_tag):
#     create_tag(node_to_tag, "GUIDE_SHAPE")


def update_all_geo_constraints(maintainOffsetT=True, maintainOffsetR=True, maintainOffsetS=True):
    all_constraints = cmds.ls(typ="LHGeometryConstraint")
    for constraint in all_constraints:
        updateGeoConstraint(geoConstraint=constraint, maintainOffsetT=True, maintainOffsetR=True, maintainOffsetS=True)








