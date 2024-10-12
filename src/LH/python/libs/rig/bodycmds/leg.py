import sys
import importlib
linux = '/corp/projects/eng/lharrison/workspace/levi_harrison_test'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)


from maya import cmds
import maya.OpenMaya as OpenMaya
from utils import misc
from rig.control import base as control_base
importlib.reload(control_base)

importlib.reload(misc)
#===============================================================================
#CLASS:         leg
#DESCRIPTION:   Creates an leg rig
#USAGE:         set arguments for 3 joints (leg, knee, ankle)
#RETURN:        split_leg_jnts, split_knee_jnts,ik_fk_switch, ik_fk_attrs, 
#               ik_ctls, fk_ctls, ik_ctl_buffers, fk_ctl_buffers, 
#               ik_ctl_gimbals, fk_ctl_gimbals, ik_constraints, 
#               fk_constraints, ik_skel_grp, fk_skel_grp, bind_jnt_grp, 
#               blend_jnt_grp, ik_rig_grp, fk_rig_grp, bind_rig_grp, 
#               blend_rig_grp, bind_jnts, blend_jnts, ik_jnts, fk_jnts, move, 
#               ik_rp, leg_curve, knee_curve, leg_curve_clusters, 
#               knee_curve_clusters, leg_clusters_grp, knee_clusters_grp, 
#               leg_curve_locs, knee_curve_locs, leg_ikspline, knee_ikspline, 
#               leg_pole_vec_jnts, leg_pole_vec_ik, leg_pole_vec_ik_up, 
#               leg_pole_vec_z_up,
#REQUIRES       maya.cmds, maya.OpenMaya, utils.misc, sys.path
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class create_leg():
    def __init__(self,
                 side = "L",
                 name = "leg",
                 joints = ["l_leg_bind","l_knee_bind","l_ankle_bind"],
                 driver = "",
                 skel_parent = "C_skeleton_GRP",
                 rig_parent = "C_rig_GRP",
                 fk_ctl_size = [1.0,1.0,1.0],
                 ik_ctl_size = [1.0,1.0],
                 ik_ctl_scale = [1,1,1],
                 ik_ctl_offset = [0,0,0],
                 switch_offset = .1,
                 switch_ctl_size = [.1],
                 twist_axis = "x",
                 leg_splits = 2,
                 knee_splits = 4,
                 global_scale = "",
                 ik_space_names = ["world", "hip"],
                 ik_space_parents = [],
                 debug = False
                 ):

        """
        type  side:                string
        param side:                usually L or R, though C is also supported

        type  name:                string
        param name:                the name of the rig

        type  joints:              string array
        param joints:              a list of 3 joints (leg, knee, ankle)

        type  driver:              string
        param driver:              what the leg will be attached to
                                    usually the bind clavical joint, but 
                                    anything that exists will work

        type  skel_parent:          string
        param skel_parent:          where to parent newly created joints,
                                     effectors, and generally things animators
                                     don't want to see.

        type  rig_parent:           string
        param rig_parent:           where to parent ctls and other things
                                     animators would like to see

        type  fk_ctl_size:          float array
        param fk_ctl_size:          a size for leg, knee, and ankle controls
        
        type  twist_axis:           string
        param twist_axis:           the axis the joint will be oriented along
                                     right now only "x" and "y" are supported 

        type  leg_splits:           int
        param leg_splits:           amount of twist joints between the leg
                                     and knee (2 are recommended)

        type  knee_splits:         int
        param knee_splits:         amount of twist joints between the knee
                                     and ankle (4 are recommended)
                                     
        type  global_scale:         string
        param global_scale:         what the fingers will be attached to
                                     for scaling usually lowest point in
                                     hierarchy of global ctl


        type  ik_space_names:       string array
        param ik_space_names:       the names you would like to give your
                                     space switches (cleaner way of naming than
                                     using the space parents)

        type  ik_space_parents:     string array
        param ik_space_parents:     the things driving the ik control
                                     during space switching, I usually use
                                     bind joint names. Does not check for
                                     cycle errors so I need to be careful.

        type  debug:                bool
        param debug:                if debug is on, nothing will be locked or
                                     ihi set to 0
                                     
        """

        #---arg vars
        self.side                   = side
        self.name                   = name
        self.twist_axis             = twist_axis
        self.joints                 = joints
        self.driver                 = driver
        self.skel_parent            = skel_parent
        self.rig_parent             = rig_parent
        self.fk_ctl_size            = fk_ctl_size
        self.ik_ctl_size            = ik_ctl_size
        self.ik_ctl_offset          = ik_ctl_offset
        self.ik_ctl_scale           = ik_ctl_scale
        self.switch_ctl_size        = switch_ctl_size
        self.switch_offset          = switch_offset
        self.leg_splits             = leg_splits
        self.knee_splits            = knee_splits
        self.global_scale           = global_scale
        self.ik_space_names         = ik_space_names
        self.ik_space_parents       = ik_space_parents
        self.debug                  = debug

        #---vars
        self.split_leg_jnts         = []
        self.split_knee_jnts       = []
        self.ik_fk_switch           = ""
        self.ik_fk_attrs            = ""
        self.ik_ctls                = []
        self.fk_ctls                = []
        self.ik_ctl_buffers         = []
        self.fk_ctl_buffers         = []
        self.ik_ctl_gimbals         = []
        self.fk_ctl_gimbals         = []
        self.ik_constraints         = []
        self.fk_constraints         = []
        self.ik_skel_grp            = ""
        self.fk_skel_grp            = ""
        self.bind_jnt_grp           = ""
        self.blend_jnt_grp          = ""
        self.ik_rig_grp             = ""
        self.fk_rig_grp             = ""
        self.bind_rig_grp           = ""
        self.blend_rig_grp          = ""
        self.bind_jnts              = []
        self.blend_jnts             = []
        self.ik_jnts                = []
        self.fk_jnts                = []
        self.move                   = (1,0,0)
        self.ik_rp                  = []
        self.leg_curve              = ""
        self.knee_curve            = ""
        self.leg_curve_clusters     = []
        self.knee_curve_clusters   = []
        self.leg_clusters_grp       = []
        self.knee_clusters_grp     = []
        self.leg_curve_locs         = []
        self.knee_curve_locs       = []
        self.leg_ikspline           = []
        self.knee_ikspline         = []
        self.leg_pole_vec_jnts      = []
        self.leg_pole_vec_ik        = []
        self.leg_pole_vec_ik_up     = []
        self.leg_pole_vec_z_up      = []
        self.gimbal_buffers         = []

        self.__create()

    def __check(self):
        """ makes sure first three indexes in self.joints are joints """
        for i in self.joints:
            if cmds.nodeType(i) != "joint":
                raise Exception(i + " must be a joint")
                quit()
        if cmds.objExists(self.skel_parent) != 1:
            raise Exception(self.skel_parent + " does not exist")
            quit()
        if cmds.objExists(self.rig_parent) != 1:
            raise Exception(self.rig_parent + " does not exist")
            quit()

    def __create_parents(self):
        """ create groups for skeleton and rig """
        #---ikSkeleton
        self.skel_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_" + self.name +
                                          "Skel_GRP",
                                          p = self.skel_parent)

        self.rig_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_" + self.name +
                                          "Rig_GRP",
                                          p = self.rig_parent)
        #---create skeleton groups
        self.ik_skel_grp = cmds.createNode("transform",
                                          n = self.side + "_legIkSkel_GRP",
                                          p = self.skel_parent)
        self.fk_skel_grp = cmds.createNode("transform",
                                          n = self.side + "_legFkSkel_GRP",
                                          p = self.skel_parent)
        self.bind_jnt_grp = cmds.createNode("transform",
                                          n = self.side + "_legBindSkel_GRP",
                                          p = self.skel_parent)
        self.blend_jnt_grp = cmds.createNode("transform",
                                          n = self.side + "_legBlendSkel_GRP",
                                          p = self.skel_parent)
        #---create rig groups
        self.ik_rig_grp = cmds.createNode("transform",
                                          n = self.side + "_legIkRig_GRP",
                                          p = self.rig_parent)
        self.fk_rig_grp = cmds.createNode("transform",
                                          n = self.side + "_legFkRig_GRP",
                                          p = self.rig_parent)
        self.bind_rig_grp = cmds.createNode("transform",
                                          n = self.side + "_legBindRig_GRP",
                                          p = self.rig_parent)
        self.blend_rig_grp = cmds.createNode("transform",
                                          n = self.side + "_legBlendRig_GRP",
                                          p = self.rig_parent)

    def __create_bind_skel(self):
        """ create the bind skeleton, split leg and knee joints """
        jntNames = ["","Blend", "Ik", "Fk"]
        appendJnts = [ self.bind_jnts, 
                      self.blend_jnts, 
                      self.ik_jnts, 
                      self.fk_jnts]
        parents = [ self.bind_jnt_grp, 
                   self.blend_jnt_grp, 
                   self.ik_skel_grp, 
                   self.fk_skel_grp]
        #loop it so we don't have to do it 3 times
        for i in range(len(appendJnts)):
            appendJnts[i].append(cmds.createNode("joint",
                                                  name = self.side + 
                                                  "_leg" + jntNames[i]+"_JNT",
                                                  parent = parents[i]))
            if i == 0:
                knee_parent = self.bind_jnt_grp
            else:
                knee_parent = appendJnts[i][0]
            appendJnts[i].append(cmds.createNode("joint",
                                                  name = self.side + 
                                                  "_knee" + jntNames[i]+"_JNT",
                                                  parent = knee_parent))
            appendJnts[i].append(cmds.createNode("joint",
                                                  name = self.side + 
                                                  "_ankle" + jntNames[i]+"_JNT",
                                                  parent = appendJnts[i][1]))
            appendJnts[i].append(cmds.createNode("joint",
                                                  name = self.side + 
                                                  "_toe" + jntNames[i]+"_JNT",
                                                  parent = appendJnts[i][1]))
            #---Snap to self.joints
            for j in range(len(appendJnts[i])):
                if j < 3:
                    con = cmds.parentConstraint(self.joints[j],appendJnts[i][j])
                    cmds.delete(con)
                    cmds.makeIdentity(appendJnts[i][j],
                                      apply = True, t=0, r=1, s = 1, n=0, pn=1)
                if j == 3:
                    con = cmds.parentConstraint(self.joints[2],appendJnts[i][j])
                    cmds.delete(con)
                    cmds.makeIdentity(appendJnts[i][j],
                                      apply = True, t=0, r=1, s = 1, n=0, pn=1)
                #---add bind tag to let us know this is a bind joint
                if i == 0:
                    if j == 0 or j == 3:
                        cmds.addAttr(appendJnts[i][j], ln = "BIND",
                                         at = "bool",)
                        cmds.setAttr(appendJnts[i][j]+".BIND",
                                     l = True,
                                     k=False)
                        if j == 3:
                            cmds.parent(appendJnts[i][j],
                                        appendJnts[i][j-1])
            if i > 0:
                cmds.setAttr(appendJnts[i][0] + ".v",0)

    def __create_jnt_splits(self):
        """ create the leg splits"""
        self.move = (1,0,0)
        if self.twist_axis == "x":
            self.move = (1,0,0)
        if self.twist_axis == "y":
            self.move = (0,1,0)
        if self.twist_axis == "z":
            line1 = "Sorry, but aligning along z is not supported at this time"
            line2 = ", aligning to x instead"
            print(line1 + line2)
            self.move= (1,0,0)
        loop_leg_knee = ([self.joints[0],self.joints[1],self.leg_splits,
                    self.bind_jnts[0],self.split_leg_jnts,self.bind_jnts[1]],
                    [self.joints[1],self.joints[2],self.knee_splits,
                       self.bind_jnts[1],self.split_knee_jnts,
                       self.bind_jnts[2]])
        for i in range(2):
            if i == 0:
                name = "leg"
            if i == 1:
                name = "knee"
            #get distance between leg and knee
            fromPoint = cmds.xform(loop_leg_knee[i][0], 
                                   q =True, 
                                   ws=True, 
                                   t=True)
            toPoint = cmds.xform(loop_leg_knee[i][1], 
                                 q =True, 
                                 ws=True, 
                                 t=True)
            vector = OpenMaya.MVector(((fromPoint[0])-(toPoint[0])),
                                      ((fromPoint[1])-(toPoint[1])),
                                      ((fromPoint[2])-(toPoint[2])))
            dist = vector.length()
            if dist > 0:
                dist = dist/(loop_leg_knee[i][2] +1)
            move = (self.move[0] * dist,self.move[1] * dist,self.move[2] * dist)
            for j in range(loop_leg_knee[i][2]+1):
                #create joint in leg hier
                par = ""
                if j == 0:
                    par = loop_leg_knee[i][3]
                else:
                    par = loop_leg_knee[i][4][j-1]
                loop_leg_knee[i][4].append(cmds.createNode("joint", 
                                                           n = self.side
                                                           + "_" 
                                                           + name
                                                           +str(j+1)
                                                           +"_JNT",
                                                            parent = par))
                cmds.move(move[0], 
                          move[1],
                          move[2],
                          loop_leg_knee[i][4][j],
                          ls=True)
                cmds.addAttr(loop_leg_knee[i][4][j], ln = "BIND",
                             at = "bool",)
                cmds.setAttr(loop_leg_knee[i][4][j]+".BIND",
                             l = True,
                             k=False)
                cmds.parent(loop_leg_knee[i][5], 
                            loop_leg_knee[i][4][len(loop_leg_knee[i][4])-1])
        cmds.parent(self.bind_jnts[1], self.bind_jnt_grp)

    def __create_fk_ctls(self):
        """ create needed fk controls and attributes """
        for i in range(3):
            if i == 0:
                name = "legFK"
                lock = ["tx","ty","tz","sx","sy","sz"]
            if i == 1:
                name = "kneeFK"
                lock = ["tx","ty","tz","rx","rz","sx","sy","sz"]
            if i == 2:
                name = "ankleFK"
                lock = ["tx","ty","tz","sx","sy","sz"]

            return_ctl = control_base.create_ctl(side = self.side, 
                                                name = name, 
                                                parent = self.fk_rig_grp, 
                                                shape = "circle",
                                                num_buffer = 3,
                                                lock_attrs = lock, 
                                                gimbal = True,
                                                size = self.fk_ctl_size[i])
            self.fk_ctls.append(return_ctl.ctl)
            self.fk_ctl_buffers.append(return_ctl.buffers)
            self.fk_ctl_gimbals.append(return_ctl.gimbal_ctl)
            tmp_con = cmds.parentConstraint(self.joints[i], 
                                            self.fk_ctl_buffers[i][0])
            cmds.delete(tmp_con)
            if i > 0:
                cmds.parent(self.fk_ctl_buffers[i][0],self.fk_ctl_gimbals[i-1]) 

    def __create_ik_ctls(self):
        """ create needed ik controls and attributes """
        for i in range(2):
            if i == 0:
                name = "legIK"
                gimbal = True
                lock = ["sx","sy","sz"]
                shape = "cube"
                snap = self.joints[2]
                show_order = True
                offset = self.ik_ctl_offset
                scale = self.ik_ctl_scale
            if i == 1:
                name = "legPolVec"
                gimbal = False
                lock = ['rx','ry','rz',"sx","sy","sz"]
                shape = "sphere"
                snap = self.joints[1]
                show_order = False
                offset = [0,0,0]
                scale = [1,1,1]
            control_base.create_ctl
            return_ctl = control_base.create_ctl(side = self.side, 
                                                name = name, 
                                                parent = self.ik_rig_grp, 
                                                shape = shape,
                                                num_buffer = 3,
                                                lock_attrs = lock,
                                                show_rot_order =show_order, 
                                                gimbal = gimbal,
                                                offset = offset,
                                                size = self.ik_ctl_size[i],
                                                scale = scale)
            self.ik_ctls.append(return_ctl.ctl)
            self.ik_ctl_buffers.append(return_ctl.buffers)
            self.ik_ctl_gimbals.append(return_ctl.gimbal_ctl)
            orientJnt = ""
            if self.side == "L":
                if i == 0 and cmds.objExists("l_ikOrientationFoot_bind"):
                    orientJnt = "l_ikOrientationFoot_bind"
                    tmp_con = cmds.parentConstraint(orientJnt, 
                                                    self.ik_ctl_buffers[i][0])
                    cmds.delete(tmp_con)
                    for i in range(5):
                        parent_grp = ""
                        if i == 0:
                            parent_grp = return_ctl.ctl
                            num = 5
                        else:
                            parent_grp = (self.side 
                                          +"_ankleGimbalBuffer"
                                          + str(6-i)
                                          + "_GRP")
                            num = 5-i
                            
                        gimbal_group = cmds.createNode("transform",
                                          n = self.side 
                                          +"_ankleGimbalBuffer"
                                          + str(num)
                                          + "_GRP",
                                          p = parent_grp)
                        
                        self.gimbal_buffers.append(gimbal_group)
                    
                    
                    
                    
                    cmds.parent(return_ctl.gimbal_ctl,
                                self.gimbal_buffers[len(self.gimbal_buffers) -1 ])

                    tmp_con = cmds.parentConstraint(snap, 
                                                    self.gimbal_buffers[0])
                    cmds.delete(tmp_con)

#                 else:
#                     tmp_con = cmds.parentConstraint(snap, 
#                                                     self.ik_ctl_buffers[i][0])
#                     cmds.delete(tmp_con)
            if self.side == "R":
                if i == 0 and cmds.objExists("r_ikOrientationFoot_bind"):
                    orientJnt = "r_ikOrientationFoot_bind"
                    tmp_con = cmds.parentConstraint(orientJnt, 
                                                    self.ik_ctl_buffers[i][0])
                    cmds.delete(tmp_con)
                    for i in range(5):
                        parent_grp = ""
                        if i == 0:
                            parent_grp = return_ctl.ctl
                            num = 5
                        else:
                            parent_grp = (self.side 
                                          +"_ankleGimbalBuffer"
                                          + str(6-i)
                                          + "_GRP")
                            num = 5-i
                            
                        gimbal_group = cmds.createNode("transform",
                                          n = self.side 
                                          +"_ankleGimbalBuffer"
                                          + str(num)
                                          + "_GRP",
                                          p = parent_grp)
                        
                        self.gimbal_buffers.append(gimbal_group)
                    
                    
                    
                    
                    cmds.parent(return_ctl.gimbal_ctl,
                                self.gimbal_buffers[len(self.gimbal_buffers) -1 ])

                    tmp_con = cmds.parentConstraint(snap, 
                                                    self.gimbal_buffers[0])
                    cmds.delete(tmp_con)
#                 else:
#                     tmp_con = cmds.parentConstraint(snap, 
#                                                     self.ik_ctl_buffers[i][0])
#                     cmds.delete(tmp_con)



#             if i == 0:  
#                     tmp_con = cmds.parentConstraint(snap, 
#                                                     self.ik_ctl_buffers[i][0])
#                     cmds.delete(tmp_con)
                    
                    
            if i == 1:
                tmp_con = cmds.pointConstraint(snap, 
                                                self.ik_ctl_buffers[i][0])
                cmds.delete(tmp_con)
                #move buffer back
                tmp = cmds.createNode("transform", name = "TEMP")
                tcon = cmds.pointConstraint(self.ik_jnts[0], 
                                            tmp)
                cmds.delete(tcon)
                #move buffer back in leg plane
                tcon = cmds.pointConstraint(self.ik_jnts[1], 
                                            tmp)
                cmds.delete(tcon)
                fromPoint = cmds.xform(self.ik_jnts[0],
                                       q =True,
                                       ws=True,
                                       t=True)
                toPoint = cmds.xform(self.ik_jnts[2],
                                     q =True,
                                     ws=True,
                                     t=True)
                vector = OpenMaya.MVector(((fromPoint[0])-(toPoint[0])),
                                          ((fromPoint[1])-(toPoint[1])),
                                          ((fromPoint[2])-(toPoint[2])))
                move = vector.length()
                tmp2 = cmds.createNode("transform", name="TMP2", parent = tmp)
                cmds.move(0, 0, +move, tmp2, ls=True)
                tcon = cmds.pointConstraint(tmp2, 
                                            self.ik_ctl_buffers[i][0])
                cmds.delete(tmp, tmp2)

    def __create_switch_ctl(self):
        """ create ikfk switch"""
        if self.side == "L":
            scale = [-1,1,-1]
            orient = [0,-35,0]
        if self.side == "R":
            scale = [-1,1,1]
            orient = [0,35,0]
        self.ik_fk_switch = control_base.create_ctl(   side = self.side, 
                                    name = self.name + "IkFkSwitch", 
                                    parent = self.rig_parent, 
                                    shape = "ik/fk",
                                    show_rot_order = False,
                                    num_buffer = 1,
                                    lock_attrs = ["all"],
                                    orient = orient,
                                    offset = [0,0,0],
                                    scale = scale,
                                    size = self.switch_ctl_size)
        cmds.parentConstraint(self.bind_jnts[3], 
                              self.ik_fk_switch.buffers[0])
        #---offset
        off = 0
        if self.side == "L":
            off = self.switch_offset
        if self.side == "R":
            off = -self.switch_offset
        cmds.move(0,
                  off,
                  0,
                  self.ik_fk_switch.ctl + ".cv[0:]",
                  r = True,
                  os = True,
                  wd = True)

    def __create_ik_fk_switching(self):
        """connect ik and fk skels to bind skel"""
        cmds.addAttr(self.ik_fk_switch.ctl, ln = "ik_fk_switch", at = "float", 
                     dv = 0, min = 0, max = 1)
        switch_attr = self.ik_fk_switch.ctl + ".ik_fk_switch"
        cmds.setAttr(switch_attr, k = True, cb = False)
        p_constraints = []
        for i in range(4):
            p_constraints.append(cmds.parentConstraint(self.ik_jnts[i], 
                                                       self.fk_jnts[i],
                                                       self.blend_jnts[i])[0])
            cmds.connectAttr(switch_attr, p_constraints[i] + ".w1")
            if i <3:
                cmds.connectAttr(switch_attr,
                                 self.fk_ctls[i] + ".v",
                                 f = True)
                misc.lock_attrs(node = self.fk_ctls[i], 
                                attr = ["v"], 
                                l = True,
                                k = False,
                                cb = False)
            
            reverse = cmds.createNode("reverse", 
                                      name = self.side 
                                      + "_"
                                      + self.name + "SwitchFK"
                                      +str(i)
                                      + "_REV")
            cmds.connectAttr(switch_attr, reverse + ".inputX")
            cmds.connectAttr(reverse + ".outputX", p_constraints[i] + ".w0")
            if i < 2:
                cmds.connectAttr(reverse + ".outputX",
                                 self.ik_ctls[i] + ".v",
                                 f = True)
                misc.lock_attrs(node = self.ik_ctls[i], 
                                attr = ["v"], 
                                l = True,
                                k = False,
                                cb = False)
        cmds.parentConstraint(self.blend_jnts[2],
                              self.bind_jnts[2])
        cmds.parentConstraint(self.blend_jnts[3],
                              self.bind_jnts[3])
        cmds.parentConstraint(self.ik_jnts[3],
                              self.blend_jnts[3])

    def __rig_ik(self):
        self.ik_rp = cmds.ikHandle(sj = self.ik_jnts[0], 
                                   ee = self.ik_jnts[2], 
                                   sol = "ikRPsolver",
                                   name = self.side 
                                   + "_" + self.name 
                                   + "IkHandle_IKH")
        cmds.parentConstraint(self.ik_ctl_gimbals[0],
                              self.ik_rp[0])
        cmds.parent(self.ik_rp[0],
                    self.ik_ctl_gimbals[0])
        cmds.setAttr(self.ik_rp[0] + ".v", 0)
        cmds.poleVectorConstraint(self.ik_ctls[1],
                                  self.ik_rp[0],)
#         cmds.orientConstraint(self.ik_ctl_gimbals[0],
#                               self.ik_jnts[3])

    def __rig_fk(self):
        for i in range(len(self.fk_ctls)):
            if i <2:
                cmds.parentConstraint(self.fk_ctl_gimbals[i], self.fk_jnts[i])
            if i == 2:
                cmds.parentConstraint(self.fk_ctl_gimbals[i], self.fk_jnts[i+1])

    def __rig_leg_splits(self):
        leg_knee = ([self.ik_jnts,
                      self.leg_curve,
                      self.leg_curve_locs,
                      self.leg_curve_clusters,
                      self.joints,
                      self.leg_ikspline,
                      self.bind_jnts[0],
                      self.split_leg_jnts,
                      "_leg_CRV",
                      "_legFrom_GRP",
                      "_legFrom_LOC",
                      "_legFrom_CLS",
                      "_legTo_GRP",
                      "_legTo_LOC",
                      "_legTo_CLS",
                      "_legIKSpine_IKH",
                      self.leg_clusters_grp,
                      "_legIKSpine_EEF",
                      ],
                     [self.ik_jnts,
                      self.knee_curve,
                      self.knee_curve_locs,
                      self.knee_curve_clusters,
                      self.joints,
                      self.knee_ikspline,
                      self.bind_jnts[1],
                      self.split_knee_jnts,
                      "_knee_CRV",
                      "_kneeFrom_GRP",
                      "_kneeFrom_LOC",
                      "_kneeFrom_CLS",
                      "_kneeTo_GRP",
                      "_kneeTo_LOC",
                      "_kneeTo_CLS",
                      "_kneeIKSpine_IKH",
                      self.knee_clusters_grp,
                      "_kneeIKSpine_EEF",
                      ])
        for i in range(2):
            if i ==0:
                fromPoint = cmds.xform(leg_knee[i][0][0], 
                                       q =True, 
                                       ws=True, 
                                       t=True)
                toPoint = cmds.xform(leg_knee[i][0][1], 
                                     q =True, 
                                     ws=True, 
                                     t=True)
            if i ==1:
                fromPoint = cmds.xform(leg_knee[i][0][1], 
                                       q =True, 
                                       ws=True, 
                                       t=True)
                toPoint = cmds.xform(leg_knee[i][0][2], 
                                     q =True, 
                                     ws=True, 
                                     t=True)
            leg_knee[i][1] = cmds.curve(name = self.side + leg_knee[i][8], 
                                         d = 1, 
                                         p =  (fromPoint,toPoint))
            cmds.setAttr(leg_knee[i][1] + ".inheritsTransform", 0)
            cmds.parent(leg_knee[i][1], self.skel_parent)
            cmds.setAttr(leg_knee[i][1] + ".v",0)
            #from
            leg_knee[i][16].append(cmds.createNode("transform", 
                                      name = self.side + leg_knee[i][9],
                                      parent = self.skel_parent))
            leg_knee[i][2].append(cmds.spaceLocator(name = (self.side +
                                                             leg_knee[i][10])))
            cmds.parent(leg_knee[i][2][0][0], 
                        leg_knee[i][16][0])
            cmds.move(fromPoint[0], 
                      fromPoint[1], 
                      fromPoint[2],
                      leg_knee[i][16][0],
                      ws=True)
            leg_knee[i][3].append(cmds.cluster(leg_knee[i][1] + ".cv[0]",
                                                name = (self.side 
                                                        + leg_knee[i][11]),
                                                wn = (leg_knee[i][2][0][0],
                                                      leg_knee[i][2][0][0]),
                                                bindState=True))
            cmds.rename("clusterHandleShape", 
                        self.side + leg_knee[i][11] + "Shape")
            leg_knee[i][16].append(cmds.createNode("transform", 
                                      name = self.side + leg_knee[i][12],
                                      parent = self.skel_parent))
            leg_knee[i][2].append(cmds.spaceLocator(
                                   name = (self.side 
                                           + leg_knee[i][13])))
            cmds.parent(leg_knee[i][2][1][0], leg_knee[i][16][1])
            cmds.move(toPoint[0],
                      toPoint[1],
                      toPoint[2],
                      leg_knee[i][16][1],
                      ws=True)
            leg_knee[i][3].append(cmds.cluster(leg_knee[i][1] + ".cv[1]",
                                                name = (self.side 
                                                        + leg_knee[i][14]),
                                                wn = (leg_knee[i][2][1][0],
                                                      leg_knee[i][2][1][0]),
                                                bindState=True))
            cmds.rename("clusterHandleShape", 
                        self.side + leg_knee[i][14] + "Shape")
            leg_knee[i][5].append(cmds.ikHandle(sj = leg_knee[i][6], 
                                                 ee = (leg_knee[i][7]
                                                       [len(leg_knee[i][7])-1]),
                                                 sol = "ikSplineSolver", 
                                                 c = leg_knee[i][1], 
                                                 name = (self.side 
                                                         + leg_knee[i][15]),
                                                 ccv = False))
            leg_knee[i][5][0][1] = cmds.rename(leg_knee[i][5][0][1], 
                                                self.side + leg_knee[i][17])
            cmds.setAttr(leg_knee[i][5][0][0] + ".dTwistControlEnable", 1);
            cmds.setAttr(leg_knee[i][5][0][0] + ".dWorldUpType", 4)
            cmds.setAttr(leg_knee[i][5][0][0] + ".dWorldUpVectorY", 0)
            cmds.setAttr(leg_knee[i][5][0][0] + ".dWorldUpVectorEndY", 0)
            cmds.setAttr(leg_knee[i][5][0][0] + ".dWorldUpVectorZ", 1)
            cmds.setAttr(leg_knee[i][5][0][0] + ".dWorldUpVectorEndZ", 1)
            cmds.setAttr(leg_knee[i][5][0][0] + ".dWorldUpAxis", 3)
            cmds.connectAttr(leg_knee[i][3][0][1]+ ".worldMatrix[0]", 
                             leg_knee[i][5][0][0]
                             + ".dWorldUpMatrix",
                             f = True)
            cmds.connectAttr(leg_knee[i][3][1][1]+ ".worldMatrix[0]", 
                             leg_knee[i][5][0][0]
                             + ".dWorldUpMatrixEnd",
                             f = True)
        #leg to
        cmds.parent(self.leg_clusters_grp[1],
                    self.leg_ikspline[0][0],
                    self.blend_jnts[1])
        #knee from
        cmds.parent(self.knee_clusters_grp[0], 
                    self.blend_jnts[1])
        #knee to
        cmds.parent(self.knee_clusters_grp[1],
                    self.knee_ikspline[0][0],
                    self.blend_jnts[3])
        cmds.setAttr(self.leg_clusters_grp[0] + ".v",0)
        cmds.setAttr(self.knee_clusters_grp[0] + ".v",0)
        cmds.setAttr(self.leg_clusters_grp[1] + ".v",0)
        cmds.setAttr(self.knee_clusters_grp[1] + ".v",0)
        cmds.setAttr(self.leg_ikspline[0][0] + ".v",0)
        cmds.setAttr(self.knee_ikspline[0][0] + ".v",0)

    def __rig_leg_up_vec(self):
        """ rig the knee splits"""
        self.leg_pole_vec_jnts      = []
        self.leg_pole_vec_ik        = []
        self.leg_pole_vec_ik_up     = []
        self.leg_pole_vec_z_up      = []
        #create joints
        dist = misc.get_dist_between(self.bind_jnts[0], self.bind_jnts[1])
        dist_x_2 = dist.dist * 2
        self.leg_pole_vec_jnts.append(cmds.createNode("transform",
                                                      name = self.side + 
                                                      "_legTwistHelpA_GRP",
                                                      parent =
                                                      self.skel_parent))
        #create ik up vector
        self.leg_pole_vec_ik_up = cmds.createNode("transform",
                                                      name = self.side + 
                                                      "_legTwistIkUp_TFM",
                                                      parent =
                                                      self.leg_pole_vec_jnts[0])
        #create ik up vector
        self.leg_pole_vec_z_up = cmds.createNode("transform",
                                                      name = self.side + 
                                                      "_legTwistUp_TFM",
                                                      parent =
                                                      self.leg_pole_vec_jnts[0])
        cmds.move(0,
                  dist.point_from[1],
                  dist.point_from[2]-dist.dist,
                  self.leg_pole_vec_jnts[0],
                  ws =True)
        cmds.move(0,
                  dist.point_from[1]+ dist.dist,
                  dist.point_from[2]-dist.dist,
                  self.leg_pole_vec_ik_up,
                  ws =True)
        cmds.move(dist.point_from[0],
                  dist.point_from[1],
                  dist.point_from[2]-dist_x_2,
                  self.leg_pole_vec_z_up,
                  ws =True)
        self.leg_pole_vec_jnts.append(cmds.createNode("joint",
                                                      name = self.side + 
                                                      "_legTwistHelpA_JNT",
                                                      parent =
                                                      self.leg_pole_vec_jnts[0]))
        self.leg_pole_vec_jnts.append(cmds.createNode("joint",
                                                      name = self.side + 
                                                      "_legTwistHelpB_JNT",
                                                      parent = 
                                                      self.leg_pole_vec_jnts[1]))
        cmds.move(dist.point_from[0],
                  0,
                  0,
                  self.leg_pole_vec_jnts[2],
                  r =True)
        #create and constrain ik
        self.leg_pole_vec_ik = cmds.ikHandle(sj = self.leg_pole_vec_jnts[1], 
                                             ee = self.leg_pole_vec_jnts[2], 
                                             sol = "ikRPsolver",
                                             name = self.side 
                                             + "_legTwistHelpIK_IKH")
        cmds.parent(self.leg_pole_vec_ik[0],
                    self.leg_pole_vec_jnts[0])
        cmds.pointConstraint(self.blend_jnts[1],
                             self.leg_pole_vec_ik[0])
        cmds.poleVectorConstraint(self.leg_pole_vec_ik_up,
                                  self.leg_pole_vec_ik[0],)
        cmds.parent(self.leg_pole_vec_z_up,
                    self.leg_pole_vec_jnts[1])
        #create aim constraint
        cmds.aimConstraint(self.blend_jnts[1],
                           self.leg_curve_clusters[0],
                           aimVector = (1, 0, 0),
                           upVector = (0, 0, 1),
                           worldUpType = "objectrotation",
                           worldUpVector = (0, 0, 1),
                           worldUpObject = self.leg_pole_vec_z_up)
        cmds.setAttr(self.leg_pole_vec_jnts[0]+".v",0)

        #leg to no flip
        #---create ankle no flip jnts
        no_flip_parent = cmds.createNode("joint",
                                         name = self.side 
                                         + "_"
                                         + "legNoFlip0_JNT",
                                         parent = self.blend_jnts[0])
        no_flip_child = cmds.createNode("joint",
                                         name = self.side 
                                         + "_"
                                         + "legNoFlip1_JNT",
                                         parent = no_flip_parent)
        con = cmds.parentConstraint(self.blend_jnts[0], no_flip_parent)
        cmds.delete(con)
        con = cmds.parentConstraint(self.blend_jnts[1], no_flip_child)
        cmds.delete(con)
        cmds.makeIdentity(no_flip_parent,
                          apply = True,
                          t=0, 
                          r=1, 
                          s = 1, 
                          n=0, 
                          pn=1)

        cmds.makeIdentity(no_flip_child,
                          apply = True,
                          t=0, 
                          r=1, 
                          s = 1, 
                          n=0, 
                          pn=1)
        #---create ik single chain handle
        ik_handle = cmds.ikHandle(sj = no_flip_parent,
                                  ee = no_flip_child,
                                  sol = "ikSCsolver",
                                  name = self.side
                                  + "_"
                                  + "legNoFlip_IKH")
        cmds.parent(ik_handle[0], self.blend_jnts[1])
        if self.side == "R":
            cmds.parentConstraint(self.blend_jnts[1], ik_handle[0], mo = True)
            cmds.orientConstraint(no_flip_parent, 
                                  self.leg_curve_clusters[1],
                                  mo = True)
        else:
            cmds.parentConstraint(self.blend_jnts[1], ik_handle[0])
            cmds.orientConstraint(no_flip_parent, self.leg_curve_clusters[1])

    def __rig_knee_up_vec(self):
        """ to lessen flipping of the leg"""
        #---create ankle no flip jnts
        no_flip_parent = cmds.createNode("joint",
                                         name = self.side 
                                         + "_"
                                         + "ankleNoFlip0_JNT",
                                         parent = self.blend_jnts[1])
        no_flip_child = cmds.createNode("joint",
                                         name = self.side 
                                         + "_"
                                         + "ankleNoFlip1_JNT",
                                         parent = no_flip_parent)
        con = cmds.parentConstraint(self.blend_jnts[1], no_flip_parent)
        cmds.delete(con)
        con = cmds.parentConstraint(self.blend_jnts[2], no_flip_child)
        cmds.delete(con)
        cmds.makeIdentity(no_flip_parent,
                          apply = True,
                          t=0, 
                          r=1, 
                          s = 1, 
                          n=0, 
                          pn=1)

        cmds.makeIdentity(no_flip_child,
                          apply = True,
                          t=0, 
                          r=1, 
                          s = 1, 
                          n=0, 
                          pn=1)
        #---create ik single chain handle
        ik_handle = cmds.ikHandle(sj = no_flip_parent,
                                  ee = no_flip_child,
                                  sol = "ikSCsolver",
                                  name = self.side
                                  + "_"
                                  + "ankleNoFlip_IKH")
        cmds.parent(ik_handle[0], self.blend_jnts[3])
        if self.side == "R":
            cmds.parentConstraint(self.blend_jnts[3], ik_handle[0], mo = True)
            cmds.orientConstraint(no_flip_parent, 
                                  self.knee_curve_clusters[1],
                                  mo = True)
        else:
            cmds.parentConstraint(self.blend_jnts[3], ik_handle[0])
            cmds.orientConstraint(no_flip_parent, self.knee_curve_clusters[1])
    def __space_switching(self):
        if self.ik_space_parents:
            misc.create_space_switches(ctl = self.ik_ctls[0], 
                                       ctl_grp = self.ik_ctl_buffers[0]
                                       [len(self.ik_ctl_buffers[0])-1],
                                       space_names = self.ik_space_names,
                                       space_parents= self.ik_space_parents)
            #--poleVectorSpaceSwitching
            self.ik_space_names.append("foot")
            self.ik_space_parents.append(self.ik_ctls[0])
            
            misc.create_space_switches(ctl = self.ik_ctls[1], 
                                       ctl_grp = self.ik_ctl_buffers[1]
                                       [len(self.ik_ctl_buffers[1])-1],
                                       space_names = self.ik_space_names,
                                       space_parents= self.ik_space_parents)
    def __fk_world_align(self):
        #---legAlign
        misc.create_fk_align(ctl = self.fk_ctls[0], 
                             ctl_grp = self.fk_ctl_buffers[0]
                             [len(self.fk_ctl_buffers[0]) - 1],
                             default_align_parent = self.fk_ctl_buffers[0]
                             [len(self.fk_ctl_buffers[0]) - 2],
                             skel_group = self.fk_skel_grp)
        #---handAlign
        misc.create_fk_align(ctl = self.fk_ctls[2], 
                             ctl_grp = self.fk_ctl_buffers[2]
                             [len(self.fk_ctl_buffers[2]) - 1],
                             default_align_parent = self.fk_ctl_buffers[2]
                             [len(self.fk_ctl_buffers[2]) - 2],
                             skel_group = self.fk_skel_grp)

    def __drive_rig(self):
        if self.driver:
            cmds.parentConstraint(self.driver, self.fk_rig_grp, mo = True)
            cmds.parentConstraint(self.driver, self.ik_rig_grp, mo = True)
            cmds.parentConstraint(self.driver, self.skel_parent, mo = True)

        if self.global_scale:
            cmds.scaleConstraint(self.global_scale, self.rig_parent, mo = True)
            cmds.scaleConstraint(self.global_scale, self.skel_parent, mo = True)

    def __cleanup(self):
        if self.debug == False:
            misc.suffix_constraints()
#             misc.lock_all(hierarchy = self.skel_parent,
#                           filter = ["*_CTL", "*_JNT"])
#             misc.lock_all(hierarchy = self.rig_parent,
#                           filter = ["*_CTL", "*_JNT"])

    def __create(self):
        self.__check()
        self.__create_parents()
        self.__create_bind_skel()
        self.__create_jnt_splits()
        self.__create_ik_ctls()
        self.__create_fk_ctls()
        self.__create_switch_ctl()
        self.__create_ik_fk_switching()
        self.__rig_ik()
        self.__rig_fk()
        self.__rig_leg_splits()
        self.__rig_leg_up_vec()
        self.__rig_knee_up_vec()
        self.__space_switching()
        self.__fk_world_align()
        self.__drive_rig()
        self.__cleanup()
