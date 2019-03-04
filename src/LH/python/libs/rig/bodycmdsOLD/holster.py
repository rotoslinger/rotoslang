import sys
linux = '/corp/projects/eng/lharrison/workspace/levi_harrison_test'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "mac" in os:
    os = mac
sys.path.append(os)

from maya import cmds
from utils import misc

reload(misc)

#===============================================================================
#CLASS:         create_holster_rig
#DESCRIPTION:   creates the holster rig
#USAGE:         set args and run
#RETURN:        align_attr, reverse_node, align_constraint, world_transform
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 27th, 2014
#Version        1.0.0
#===============================================================================

class create_holster_rig():
    def __init__(self, 
                 sides = ["C"],
                 names = [],
                 translates = [(0,0,0)],
                 rotates = [(0,0,0)],
                 scales = [(.1,.1,.1)],
                 num_buffer = 2,
                 rig_parent = "C_rig_GRP", 
                 skel_parent = "C_skeleton_GRP",
                 lock_attrs=["v"],
                 sizes = [1],
                 global_scale = "",
                 debug = False
                 ):
        """
        @type  sides:                string
        @param sides:                C or L or R

        @type  names:                string
        @param names:                the name of your rivet

        @type  translates:           3 tuple
        @param translates:           translation of the poly plane (Tx, Ty, Tz 
                                     attributes)

        @type  rotates:              3 tuple
        @param rotates:              rotation of the poly plane (Rx, Ry, Rz 
                                     attributes)

        @type  scales:               3 tuple
        @param scales:               scale of the poly plane (Sx, Sy, Sz 
                                     attributes)

        @type  uvs:                  2 doubles
        @param uvs:                  this will tell the point on poly constraint
                                     what u and v parameters you want to 
                                     constrain to

        @type  num_buffers:          unsigned int
        @param num_buffers:          the amount of buffers you will have above
                                     your ctl one is mandatory (even if you give
                                     0) but above that is your choice. 

        @type  rig_parent:           string array
        @param rig_parent:           the group where you parent your skeleton
        
        @type  skel_parent:          string array
        @param skel_parent:          the group where you parent your skeleton

        @type  lock_attrs:           string array
        @param lock_attrs:           ctl arg: the attribute names you want 
                                     locked, unkeyable, and hidden

        @type  size:                 float
        @param size:                 ctl arg: average size of all points in ctl 
                                     in units

        @type  global_scale:         string
        @param global_scale:         what the rig will be attached to
                                     for scaling usually lowest point in
                                     hierarchy of global ctl
        """

        #---args
        self.sides                    = sides
        self.names                    = names
        self.translates               = translates
        self.rotates                  = rotates
        self.scales                   = scales
        self.num_buffer               = num_buffer
        self.rig_parent               = rig_parent
        self.skel_parent              = skel_parent
        self.lock_attrs               = lock_attrs
        self.sizes                    = sizes
        self.global_scale             = global_scale
        self.debug                    = debug

        #---vars
        self.ctls                    = []

        self.__create()

    def __create_parents(self):
        """ create groups for skeleton and rig """
        self.skel_parent = cmds.createNode("transform",
                                          n = "C_holsterSkel_GRP",
                                          p = self.skel_parent)

        self.rig_parent = cmds.createNode("transform",
                                          n = "C_holsterRig_GRP",
                                          p = self.rig_parent)

    def __create_rigs(self):
        for i in range(len(self.names)):
            self.ctls.append(misc.create_rivet_rig(side = self.sides[i],
                                                   name = self.names[i],
                                                   translate = self.translates[i],
                                                   rotate = self.rotates[i],
                                                   scale = self.scales[i],
                                                   uv = (0.5,0.5),
                                                   num_buffer = self.num_buffer,
                                                   rig_parent = self.rig_parent, 
                                                   skel_parent = self.skel_parent,
                                                   shape = "sphere",
                                                   lock_attrs=["sx","sy","sz"],
                                                   size = self.sizes[i],
                                                   orient = [0,0,0],
                                                   offset = [0,0,0],
                                                   gimbal = True,
                                                   hide = False,
                                                   global_scale = "",
                                                   debug = self.debug))

    def __global_scale(self):
        if self.global_scale:
            cmds.scaleConstraint(self.global_scale, self.rig_parent, mo = True)
            cmds.scaleConstraint(self.global_scale, self.skel_parent, mo = True)

    def __cleanup(self):
        if self.debug == False:
            misc.lock_all(hierarchy = self.rig_parent, filter = ["*_CTL", "*_JNT"])
            misc.lock_all(hierarchy = self.skel_parent, filter = ["*_CTL", "*_JNT","*_EX"])

    def __create(self):
        self.__create_parents()
        self.__create_rigs()
        self.__global_scale()
        self.__cleanup()