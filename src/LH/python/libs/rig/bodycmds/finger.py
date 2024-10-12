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
from utils import misc
from rig.control import base as control_base
importlib.reload(control_base)

importlib.reload(misc)

#===============================================================================
#CLASS:         finger
#DESCRIPTION:   Creates finger rig
#USAGE:         set arguments for finger roots
#RETURN:        skel_parents, rig_parents, finger_joints, source_finger_joints, 
#               ctls, ctl_buffers, ctl_gimbals, knuckle_jnts, metacarpal_jnts,
#REQUIRES:      utils.misc, maya.cmds, sys
#AUTHOR:        Levi Harrison
#DATE:          Oct 21st, 2014
#Version        1.0.0
#===============================================================================

class create_finger():
    def __init__(self,
                 side = "L",
                 names = ["thumb",
                          "index",
                          "middle",
                          "ring",
                          "pinky"],
                 joint_roots = ["l_thumba_bind",
                                "l_indexa_bind",
                                "l_middlea_bind",
                                "l_ringa_bind",
                                "l_pinkya_bind"],
                 ignore_end_joints = True,
                 driver = "",
                 global_scale = "",
                 skel_parent = "C_skeleton_GRP",
                 rig_parent = "C_rig_GRP",
                 ctl_size = [[1.0,1.0,1.0],
                             [1.0,1.0,1.0],
                             [1.0,1.0,1.0],
                             [1.0,1.0,1.0],
                             [1.0,1.0,1.0, 1.0]],
                 debug = False,
                 infinite_digits = False,
                 worldAlign = False
                 ):

        """
        type  side:                 string
        param side:                 usually L or R, though C is also supported

        type  names:                string
        param names:                the names of your fingers

        type  joint_roots:          string array
        param joint_roots:          the top root of the finger you want to 
                                     create usually a joint chain of 5 which
                                     includes metacarpal_jnts.  If more than 
                                     five extra metacarpal_jnts will be created
                                     If fewer than five only the 3 finger digits
                                     will be created

        type  ignore_end_joints:    bool
        param ignore_end_joints:    if True will ignore the last digit in the
                                     joint chain, if False, all digits will be
                                     rigged.

        type  driver:               string
        param driver:               what the fingers will be attached to
                                     usually the hand or wrist joint, but 
                                     anything that exists will work

        type  global_scale:         string
        param global_scale:         what the fingers will be attached to
                                     for scaling usually lowest point in
                                     hierarchy of global ctl


        type  skel_parent:          string
        param skel_parent:          where to parent newly created joints,
                                     effectors, and generally things animators
                                     don't want to see.

        type  rig_parent:           string
        param rig_parent:           where to parent ctls and other things
                                     animators would like to see

        type  ctl_size:             2-d float array
        param ctl_size:             a size for controls

        type  debug:                bool
        param debug:                if debug is on, nothing will be locked and
                                     ihi will remain 1
        """

        #---args
        self.side                    = side
        self.names                   = names
        self.joint_roots             = joint_roots
        self.ignore_end_joints       = ignore_end_joints
        self.driver                  = driver
        self.global_scale            = global_scale
        self.skel_parent             = skel_parent
        self.rig_parent              = rig_parent
        self.ctl_size                = ctl_size
        self.debug                   = debug
        self.infinite_digits         = infinite_digits
        self.worldAlign              = worldAlign

        #---vars
        self.skel_parents            = []
        self.rig_parents             = []
        self.finger_joints           = []
        self.source_finger_joints    = []
        self.ctls                    = []
        self.ctl_buffers             = []
        self.ctl_gimbals             = []
        self.knuckle_jnts            = []
        self.metacarpal_jnts         = []

        self.__create()

    def __check(self):
        for i in self.joint_roots:
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
        #create fingers groups
        self.skel_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_fingerSkel_GRP",
                                          p = self.skel_parent)

        self.rig_parent = cmds.createNode("transform",
                                          n = self.side + 
                                          "_fingerRig_GRP",
                                          p = self.rig_parent)

        for i in range(len(self.names)):
            #---create skeleton groups
            self.skel_parents.append(cmds.createNode("transform",
                                     n = self.side+ "_"
                                     +self.names[i]
                                     + "Skel_GRP",
                                     p = self.skel_parent))

            #---create rig groups
            self.rig_parents.append(cmds.createNode("transform",
                                     n = self.side+ "_"
                                     +self.names[i]
                                     + "Rig_GRP",
                                     p = self.rig_parent))

    def __create_bind_skel(self):
        for i in range(len(self.names)):
            #---get children
            tmp_jnts = []
            tmp_jnts.append(self.joint_roots[i])
            rel = cmds.listRelatives(self.joint_roots[i]
                                     , ad = True,
                                     type = "joint")
            rel.reverse()
            for j in rel:
                tmp_jnts.append(j)
            self.source_finger_joints.append(tmp_jnts)

            #---any more knuckle_jnts than 3 become meta carpals 
            if self.ignore_end_joints == 1:
                num_knucks = 3
            else:
                num_knucks = 4

            tmp_knuckle_jnts            = []
            tmp_metacarpal_jnts         = []
            tmp_finger = []
            if self.infinite_digits:
                num_knucks = 10

            for j in range(len(self.source_finger_joints[i])):
                rev_counter = len(self.source_finger_joints[i])-1 - j
                if rev_counter <= num_knucks:
                    name = self.names[i]
                    count = str(rev_counter)
                    knuckle_finger = tmp_knuckle_jnts

                if rev_counter > num_knucks:
                    name = self.names[i] + "Metacarpal"
                    count = str(rev_counter-num_knucks-1)
                    knuckle_finger = tmp_metacarpal_jnts
                    
                if self.infinite_digits:
                    count=str(j)
                if j == 0:
                    parent = self.skel_parents[i]
                    tmp_finger.append(cmds.createNode("joint",
                                                      name = self.side + 
                                                      "_" + name
                                                      + count + "_JNT",
                                                      parent = parent))

                if j > 0:
                    tmp_finger.append(cmds.createNode("joint",
                                                      name = self.side + 
                                                      "_" + name
                                                      + count + "_JNT",
                                                      parent = tmp_finger[j-1]))

                knuckle_finger.append(tmp_finger[j])

                con = cmds.parentConstraint(self.source_finger_joints[i][j],
                                            tmp_finger[j])
                cmds.delete(con)
                cmds.makeIdentity(tmp_finger[j],
                                  apply = True, t=0, r=1, s = 1, n=0, pn=1)

                cmds.addAttr(tmp_finger[j], ln = "BIND",
                                 at = "bool",)
                cmds.setAttr(tmp_finger[j]+".BIND", l = True, k=False)

            self.knuckle_jnts.append(tmp_knuckle_jnts)
            self.metacarpal_jnts.append(tmp_metacarpal_jnts)
            self.finger_joints.append(tmp_finger)

    def __rig_fingers(self):
        """ create controls and snap to fingers """
        for i in range(len(self.finger_joints)):
            tmp_ctls=[]
            tmp_buffers=[]
            tmp_gimbals=[]
            skip = 0

            if self.ignore_end_joints == 1:
                skip = -1
                num_knucks = 3
            else:
                num_knucks = 4
            for j in range(len(self.finger_joints[i])+skip):
                if self.infinite_digits:
                    num_knucks = 10
                rev_counter = len(self.finger_joints[i])+skip - j
                if rev_counter <= num_knucks:
                    name = self.names[i]
                    count = str(rev_counter-1)
                if rev_counter > num_knucks:
                    name = self.names[i] + "Metacarpal"
                    count = str(rev_counter-num_knucks-1)

                    
                size = 1.0
                orient = [0,0,0]
                scale = [1,1,1]
                if not self.infinite_digits:
                    size = self.ctl_size[i][j]

                if self.infinite_digits:
                    orient = [0,0,90]
                    scale = [1,1,5]
                    count=str(j)
                num_buffer = 1
                if self.worldAlign:
                    num_buffer = 3
                return_ctl = control_base.create_ctl(side = self.side, 
                                             name = name + count, 
                                             parent = self.rig_parents[i], 
                                             shape = "circle",
                                             num_buffer = num_buffer,
                                             lock_attrs = ["sx","sy","sz","v"], 
                                             gimbal = True,
                                             size = size,
                                             orient = orient,
                                             scale = scale
                                             )


                tmp_ctls.append(return_ctl.ctl)
                tmp_buffers.append(return_ctl.buffers)
                tmp_gimbals.append(return_ctl.gimbal_ctl)
                #---constrain it
                misc.lock_attrs(node = return_ctl.buffers[0], 
                                attr = ["all"], 
                                l = False)
                tmp_con = cmds.parentConstraint(self.finger_joints[i][j], 
                                                return_ctl.buffers[0])
                cmds.delete(tmp_con)
                # as long as it isn't the first in the chain, parent under
                # the gimbal of the last iteration's ctl
                if j > 0:
                    cmds.parent(tmp_buffers[j][0],tmp_gimbals[j-1])
                #---rig it
                cmds.parentConstraint(tmp_gimbals[j],
                                      self.finger_joints[i][j])

                if self.worldAlign:
                    align = misc.create_fk_align(ctl = return_ctl.ctl, 
                                        ctl_grp = return_ctl.buffers[1],
                                        default_align_parent = return_ctl.buffers[0],
                                        skel_group = self.skel_parent,
                                        maintainOffset=True)

            self.ctls.append(tmp_ctls)
            self.ctl_buffers.append(tmp_buffers)
            self.ctl_gimbals.append(tmp_gimbals)

    def __drive_rig(self):
        if self.driver:
            cmds.parentConstraint(self.driver, 
                                  self.rig_parent, 
                                  mo = True)
            cmds.parentConstraint(self.driver, 
                                  self.skel_parent, 
                                  mo = True)
        if self.global_scale:
            cmds.scaleConstraint(self.global_scale, 
                                 self.rig_parent, mo = True)
            cmds.scaleConstraint(self.global_scale, 
                                 self.skel_parent, mo = True)

    def __cleanup(self):
        if self.debug == False:
            misc.suffix_constraints()
            misc.lock_all(hierarchy = self.rig_parent, 
                          filter = ["*_CTL", "*_JNT"])
            misc.lock_all(hierarchy = self.skel_parent, 
                          filter = ["*_CTL", "*_JNT"])

    def __create(self):
        self.__check()
        self.__create_parents()
        self.__create_bind_skel()
        self.__rig_fingers()
        self.__drive_rig()
        self.__cleanup()