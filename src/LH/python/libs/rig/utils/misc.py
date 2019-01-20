import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs/rig'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
win = "C:\\Users\\harri\\Desktop\\dev\\rotoslang\\src\\LH\\python\\libs"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win32" in os:
    os = mac

if os not in sys.path:
    sys.path.append(os)

from maya import cmds
import maya.OpenMaya as OpenMaya
from fnmatch import fnmatch
import exportUtils


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
        @type  node:                string
        @param node:                name of the node that will have attrs 
                                    locked

        @type  attr:                string
        @param attr:                attribute names if "all" will use
                                    translates, rotates and scales

        @type  l:                   bool
        @param l:                   lock

        @type  k:                   bool
        @param k:                   keyable

        @type  cb:                  bool
        @param cb:                  channel box
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
                 char_name = "character"):
        """
        @type  char_name:                string
        @param char_name:                character name
        """
        #---args
        self.char_name                   = char_name
        
        #---vars
        self.groups                      = []

        self.__create()

    def __create_nodes(self):
        "Create and name rig transforms"
        self.groups.append(cmds.createNode("transform", 
                                           name = "C_" + 
                                           self.char_name + 
                                           "_GRP"))

        self.groups.append(cmds.createNode("transform", 
                                           name = "C_geo_GRP",
                                           parent = self.groups[0]))

        self.groups.append(cmds.createNode("transform", 
                                           name = "C_skeleton_GRP",
                                           parent = self.groups[0]))

        self.groups.append(cmds.createNode("transform", 
                                           name = "C_rig_GRP",
                                           parent = self.groups[0]))

    def __lock_attrs(self):
        "Lock out attributes"
        for i in range(len(self.groups)):
            #---lock transform
            lock_attrs(node = self.groups[i])
            #---make vis non keyable
            cmds.setAttr(self.groups[i]+".v",
                         keyable = False, 
                         channelBox = True)
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
#CLASS:         draw_ctl
#DESCRIPTION:   draws controls
#USAGE:         set args and run
#RETURN:        ctl
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class draw_ctl():
    def __init__(self,
                 side="L",
                 name="",
                 parent="",
                 shape = "circle",
                 lock_attrs=["v"],
                 show_rot_order= True,
                 size = 1,
                 orient = [0,0,0],
                 offset = [0,0,0],
                 scale = [1,1,1],
                 hide = False
                 ):

        """
        @type  side:                string
        @param side:                side the control is on C,L,R
        
        @type  name:                string
        @param name:                name of the ctl
        
        @type  parent:              string
        @param parent:              the transform this will be parented under

        @type  shape:               string
        @param shape:               shape name, currently supported:
                                    circle
                                    sphere
                                    switch
                                    cube
                                    square
                                    shoulder
                                    ik\\fk

        @type  lock_attrs:          string array
        @param lock_attrs:          the attribute names you want locked,
                                    unkeyable, and hidden

        @type  show_rot_order:      bool
        @param show_rot_order:          if true, rotation order is exposed as a 
                                    non keyable attribute

        @type  size:                float
        @param size:                average size of all points in ctl in units

        @type  orient:              float array
        @param orient:              x,y,z values you want to rotate the points
                                    by.  These values will not be reflected in
                                    the transform of the control
        
        @type  offset:              float array
        @param offset:              x,y,z values you want to translate the 
                                    points by.  These values will not be 
                                    reflected in the transform of the control
                                    
        @type  scale:               float array
        @param scale:               x,y,z values you want to scale the 
                                    points by.  These values will not be 
                                    reflected in the transform of the control
        @type  hide:                bool
        @param hide:                if true control visibility will be set to 0
        """

        #---args
        self.side                   = side
        self.name                   = name
        self.parent                 = parent
        self.shape                  = shape
        self.lock_attrs             = lock_attrs
        self.show_rot_order         = show_rot_order
        self.size                   = size
        self.orient                 = orient
        self.offset                 = offset
        self.scale                  = scale
        self.hide                   = hide

        #---vars
        self.ctl                    = ""

        self.__create()

    def __check(self):
        "checks to make sure shape is supported"
        if not(self.shape != "circle" or 
               self.shape != "sphere" or 
               self.shape != "switch" or 
               self.shape != "cube" or 
               self.shape != "square" or 
               self.shape != "ik/fk" or 
               self.shape != "shoulder"):
            raise Exception(self.shape + " is not supported yet")
            quit()

    def __circle(self):
        if (self.shape == "circle"):
            self.ctl = cmds.circle(n = self.side + "_" + self.name + "_CTL", 
                                   nr=(1, 0, 0), c=(0, 0, 0), r = self.size)[0]
            cmds.parent(self.ctl, self.parent)

    def __sphere(self):
        if (self.shape == "sphere"):
            self.ctl = cmds.curve(n = self.side + "_" + self.name + "_CTL",
                                  d = 1, 
                                  p=[(0, 0, 1),
                                     (0, 0.5, 0.866025 ),
                                     ( 0, 0.866025, 0.5 ),
                                     ( 0, 1, 0 ), ( 0, 0.866025, -0.5 ),
                                     ( 0, 0.5, -0.866025 ),( 0, 0, -1 ),
                                     ( 0, -0.5 ,-0.866025 ),( 0, -0.866025, -0.5 ),
                                     ( 0, -1, 0 ),( 0, -0.866025, 0.5 ),
                                     ( 0, -0.5, 0.866025 ),( 0, 0, 1 ),
                                     ( 0.707107, 0, 0.707107 ),( 1, 0, 0 ),
                                     ( 0.707107, 0, -0.707107 ),( 0, 0, -1 ),
                                     ( -0.707107, 0, -0.707107, ),( -1, 0, 0 ),
                                     ( -0.866025, 0.5, 0 ),( -0.5, 0.866025, 0 ),
                                     ( 0, 1, 0 ),( 0.5, 0.866025, 0 ),
                                     ( 0.866025, 0.5, 0 ),( 1, 0, 0 ),
                                     ( 0.866025, -0.5, 0 ),( 0.5, -0.866025, 0 ),
                                     ( 0, -1, 0 ),( -0.5, -0.866025, 0 ),
                                     ( -0.866025, -0.5, 0 ),( -1, 0, 0 ),
                                     ( -0.707107, 0, 0.707107 ),( 0, 0, 1)],
                                  k = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                                       11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                       20, 21, 22, 23, 24, 25, 26, 27, 28, 
                                       29, 30, 31, 32])
            cmds.parent(self.ctl, self.parent)
            cmds.scale(self.size, self.size, self.size, 
                       self.ctl + ".cv[0:]", 
                       r = True,p = (0, 0, 0))

    def __switch(self):
        if (self.shape == "switch"):
            self.ctl = cmds.curve(n = self.side + "_" + self.name + "_CTL", 
                                  d = 1, 
                                  p=[(7.06316e-009, 0, -1),
                                     (0.104714, 0, -0.990425),
                                     (0.314142, 0, -0.971274),
                                     (0.597534, 0, -0.821244),
                                     (0.822435, 0, -0.597853),
                                     (0.96683, 0, -0.314057),
                                     (1.016585, 0, -2.28604e-005),
                                     (0.96683, 0, 0.314148),
                                     (0.822435, 0, 0.597532),
                                     (0.597534, 0, 0.822435),
                                     (0.314142, 0, 0.96683),
                                     (1.22886e-008, 0, 1.016585),
                                     (-0.314142, 0, 0.96683),
                                     (-0.597534, 0, 0.822435),
                                     (-0.822435, 0, 0.597532),
                                     (-0.96683, 0, 0.314148),
                                     (-1.016585, 0, -2.29279e-005),
                                     (-0.96683, 0, -0.314057),
                                     (-0.822435, 0, -0.597853),
                                     (-0.597534, 0, -0.821244),
                                     (-0.314142, 0, -0.971274),
                                     (-0.104714, 0, -0.990425),
                                     (7.06316e-009, 0, -1)],
                                  k = [ 0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20 ,21 ,22])
            oddPoints = [self.ctl + ".ep[1]", self.ctl + ".ep[3]", 
                         self.ctl + ".ep[5]", self.ctl + ".ep[7]", 
                         self.ctl + ".ep[9]", self.ctl + ".ep[11]",
                         self.ctl + ".ep[13]", self.ctl + ".ep[15]",
                         self.ctl + ".ep[17]", self.ctl + ".ep[19]",
                         self.ctl + ".ep[0]", self.ctl + ".ep[22]",
                         self.ctl + ".ep[21]"]
            for i in oddPoints:
                cmds.scale(0.732056, 0.732056, 0.732056, 
                           i, 
                           r = True,p = (0, 0, 0))
            cmds.delete(self.ctl + ".ep[1]",self.ctl + ".ep[21]")
            cmds.parent(self.ctl, self.parent)
            cmds.scale(self.size, self.size, self.size, 
                       self.ctl + ".cv[0:]", 
                       r = True,p = (0, 0, 0))

    def __cube(self):
        if (self.shape == "cube"):
            self.ctl = cmds.curve(n = self.side + "_" + self.name + "_CTL",
                                  d = 1, 
                                  p=[(0.5, 0.5, 0.5), (0.5, 0.5, -0.5), 
                                     (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5),
                                    (0.5, -0.5, -0.5), (0.5, 0.5, -0.5),
                                     (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), 
                                     (0.5, 0.5, 0.5), (0.5, -0.5, 0.5), 
                                     (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), 
                                     (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), 
                                     (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5)],
                                  k = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
            cmds.parent(self.ctl, self.parent)
            cmds.scale(self.size, self.size, self.size, 
                       self.ctl + ".cv[0:]", 
                       r = True,p = (0, 0, 0))

    def __square(self):
        if (self.shape == "square"):
            self.ctl = cmds.curve(n = self.side + "_" + self.name + "_CTL",
                                  d = 1, 
                                  p=[(-1, 0, 1), (1, 0, 1), 
                                     (1, 0, -1), (-1, 0, -1),
                                     (-1, 0, 1)],
                                  k = [0,1,2,3,4])
            cmds.parent(self.ctl, self.parent)
            cmds.scale(self.size, self.size, self.size, 
                       self.ctl + ".cv[0:]", 
                       r = True,p = (0, 0, 0))
            cmds.rotate(0,
                        0,
                        90,
                        self.ctl + ".cv[0:]", 
                        r = True,p = (0, 0, 0))

    def __shoulder(self):
        if (self.shape == "shoulder"):
            self.ctl = cmds.curve(n = self.side + "_" + self.name + "_CTL",
                                  d = 3, 
                                  p=[(-7.590953, 0, 12.696369), 
                                     (0.42242, 0, 10.152781), 
                                     (0.42242, 0, 10.152781), 
                                     (0.42242, 0, 10.152781), 
                                     (5.556196, 4.560603, 6.99268), 
                                     (7.404822, 6.310447, 3.216172), 
                                     (8.041815, 6.721348, 0.00012392), 
                                     (7.404822, 6.310447, -3.215924), 
                                     (5.556196, 4.560603, -6.992433), 
                                     (0.42242, 0, -10.151544), 
                                     (0.42242, 0, -10.151544), 
                                     (0.42242, 0, -10.151544), 
                                     (-7.590953, 0, -12.697621), 
                                     (-7.590953, 0, -12.697621), 
                                     (-7.590953, 0, -12.697621), 
                                     (-1.663151, 5.946572, -8.744516), 
                                     (0.44383, 8.206007, -4.021817), 
                                     (0.969434, 8.743409, 0), 
                                     (0.44383, 8.206007, 4.021817), 
                                     (-1.663151, 5.946572, 8.744516),
                                     (-7.590953, 0, 12.696369)],
                                  k = [0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,
                                       14,15,16,17,18,18,18])
            cmds.scale(0.04, 0.04, 0.04, 
                       self.ctl + ".cv[0:]", 
                       r = True,p = (0, 0, 0))
            cmds.parent(self.ctl, self.parent)
            cmds.scale(self.size, 
                       self.size, 
                       self.size, 
                       self.ctl + ".cv[0:]", 
                       r = True,p = (0, 0, 0))
    def __ik_fk(self):
        """"""
        if (self.shape == "ik/fk"):
            self.ctl = cmds.curve(n = self.side + "_" + self.name + "_CTL",
                                  d = 1, 
                                  p=[(1.54953666109, -1.60264861549e-16, 0.471768770752),
                                    (1.17923504277, -4.70697878823e-17, -0.0380165208327),
                                    (1.53137259859, 3.15088187204e-17, -0.391903104248),
                                    (1.29816947359, 3.15088187204e-17, -0.391903104248),
                                    (0.964771036094, -4.74644675234e-17, -0.0362390417482),
                                    (0.964771036094, 3.15088187204e-17, -0.391903104248),
                                    (0.787231973594, 3.15088187204e-17, -0.391903104248),
                                    (0.787231973594, -1.60264861549e-16, 0.471768770752),
                                    (0.964771036094, -1.60264861549e-16, 0.471768770752),
                                    (0.964771036094, -9.61234610246e-17, 0.182901583252),
                                    (1.05090384859, -7.64777176591e-17, 0.0944250207518),
                                    (1.31750541109, -1.60264861549e-16, 0.471768770752),
                                    (1.54953666109, -1.60264861549e-16, 0.471768770752),
                                    (0.230591348594, -1.60264861549e-16, 0.471768770752),
                                    (0.230591348594, -7.98604284373e-17, 0.109659395752),
                                    (0.609692911094, -7.98604284373e-17, 0.109659395752),
                                    (0.609692911094, -4.65537376985e-17, -0.0403406042482),
                                    (0.230591348594, -4.65537376985e-17, -0.0403406042482),
                                    (0.230591348594, -2.44839332182e-18, -0.238973416748),
                                    (0.663599161094, -2.44839332182e-18, -0.238973416748),
                                    (0.663599161094, 3.1248610199e-17, -0.390731229248),
                                    (0.0512944735937, 3.1248610199e-17, -0.390731229248),
                                    (0.0512944735937, -1.60264861549e-16, 0.471768770752),
                                    (0.230591348594, -1.60264861549e-16, 0.471768770752),
                                    (-0.273846226506, -1.60447796687e-16, 0.472592637371),
                                    (0.0988796189713, 5.89503152776e-17, -0.515488617917),
                                    (-0.0620969617443, 5.88796105146e-17, -0.515170191973),
                                    (-0.444494027695, -1.6997261774e-16, 0.515488617917),
                                    (-0.290027527924, -1.6997261774e-16, 0.515488617917),
                                    (-0.273846226506, -1.60447796687e-16, 0.472592637371),
                                    (-0.290508231216, -1.6997261774e-16, 0.515488617917),
                                    (-0.444494027695, -1.6997261774e-16, 0.515488617917),
                                    (-0.436841348594, -1.60264861549e-16, 0.471768770752),
                                    (-0.808911661094, -4.74644675234e-17, -0.0362390417482),
                                    (-0.455005411094, 3.15088187204e-17, -0.391903104248),
                                    (-0.688208536094, 3.15088187204e-17, -0.391903104248),
                                    (-1.02160697359, -4.74644675234e-17, -0.0362390417482),
                                    (-1.02160697359, 3.15088187204e-17, -0.391903104248),
                                    (-1.19914603609, 3.15088187204e-17, -0.391903104248),
                                    (-1.19914603609, -1.60264861549e-16, 0.471768770752),
                                    (-1.02160697359, -1.60264861549e-16, 0.471768770752),
                                    (-1.02160697359, -9.61234610246e-17, 0.182901583252),
                                    (-0.935474161094, -7.64777176591e-17, 0.0944250207518),
                                    (-0.668872598594, -1.60264861549e-16, 0.471768770752),
                                    (-0.436841348594, -1.60264861549e-16, 0.471768770752),
                                    (-1.37023978609, -1.60264861549e-16, 0.471768770752),
                                    (-1.37023978609, 3.15088187204e-17, -0.391903104248),
                                    (-1.54953666109, 3.15088187204e-17, -0.391903104248),
                                    (-1.54953666109, -1.60264861549e-16, 0.471768770752),
                                    (-1.3847677758, -1.60264861549e-16, 0.471768770752)],
                                    k = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
                                       16,17,18,19,20,21,22,23,24,25,26,27,28,
                                       29,30,31,32,33,34,35,36,37,38,39,40,
                                       41,42,43,44,45,46,47,48,49])
             
            #50
 
            cmds.parent(self.ctl, self.parent)
            cmds.scale(self.size, 
                       self.size, 
                       self.size, 
                       self.ctl + ".cv[0:]", 
                       r = True,p = (0, 0, 0))

    def __lock_it(self):
        if self.hide == True:
            cmds.setAttr(self.ctl + ".v", 0)
        if self.lock_attrs == ["all"]:
            self.lock_attrs = ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]
        for i in range(len(self.lock_attrs)):
            cmds.setAttr(self.ctl + "."+ self.lock_attrs[i], 
                          lock = True, 
                          keyable = False, 
                          channelBox = False)

    def __color_it(self):
        ctl_shape = cmds.listRelatives(self.ctl, shapes = True)[0]
        cmds.setAttr(ctl_shape + ".overrideEnabled", True)
        color = ctl_shape + ".overrideColor"
        cmds.setAttr(ctl_shape + ".overrideRGBColors", 1)
        if self.side == "C":
            cmds.setAttr(color + "R", 1)
            cmds.setAttr(color + "G", 1)
            cmds.setAttr(color + "B", 0)
        if self.side == "L":
            cmds.setAttr(color + "R", 0)
            cmds.setAttr(color + "G", 0)
            cmds.setAttr(color + "B", 1)
        if self.side == "R":
            cmds.setAttr(color + "R", 1)
            cmds.setAttr(color + "G", 0)
            cmds.setAttr(color + "B", 0)
    def __cleanup(self):
        cmds.delete(self.ctl, ch = True)
        if self.show_rot_order == True:
            cmds.setAttr(self.ctl + ".ro", cb = True)
        #orient
        cmds.rotate(self.orient[0],
                    self.orient[1],
                    self.orient[2],
                    self.ctl + ".cv[0:]", 
                    r = True,p = (0, 0, 0))
        cmds.move(self.offset[0],
                  self.offset[1],
                  self.offset[2],
                  self.ctl + ".cv[0:]", 
                  r = True)
        cmds.scale(self.scale[0],
                   self.scale[1],
                   self.scale[2],
                   self.ctl + ".cv[0:]", 
                   r = True,p = (0, 0, 0))

    def __create(self):
        ""
        self.__check()
        self.__circle()
        self.__sphere()
        self.__switch()
        self.__cube()
        self.__square()
        self.__shoulder()
        self.__ik_fk()
        self.__lock_it()
        self.__color_it()
        self.__cleanup()

##########################################################
#---example
# draw_ctl(name = "BLA", 
#          parent = 'character_grp', 
#          shape = "ik/fk", 
#          lock_attrs = ["tx","ty","tz"], 
#          size = 1)
##########################################################



#===============================================================================
#CLASS:         create_ctl
#DESCRIPTION:   create controls, groups, and gimbal if you need them
#USAGE:         set args and run
#RETURN:        ctl, gimbal_ctl, buffers, gimbal_vis_attr, buffer_parent
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 14th, 2014
#Version        1.0.0
#===============================================================================

class create_ctl():
    def __init__(self,
                 side="",
                 name="",
                 parent="",
                 shape = "",
                 lock_attrs=[],
                 num_buffer = 0,
                 gimbal = False,
                 num_secondary = 0,
                 show_rot_order = True,
                 size = 1,
                 orient = [0,0,0],
                 offset = [0,0,0],
                 scale = [1,1,1],
                 hide = False
                 ):

        """
        @type  side:                string
        @param side:                the side the control is on C,L,R
        
        @type  name:                string
        @param name:                name of the ctl
        
        @type  parent:              string
        @param parent:              the transform this will be parented under

        @type  shape:               string
        @param shape:               shape name, currently supported:
                                    circle
                                    sphere
                                    switch
                                    cube
                                    shoulder

        @type  lock_attrs:          string array
        @param lock_attrs:          the attribute names you want locked,
                                    unkeyable, and hidden

        @type  num_buffer:          int
        @param num_buffer:          number of transforms to group ctl under

        @type  gimbal:              bool
        @param gimbal:              whether or not you want a gimbal control
                                    not recommended for controls with less than
                                    all 3 rotation attributes
                                    
        @type  num_secondary:       bool
        @param num_secondary:       creates extra controls which will be
                                    parented under the main ctl
                                    
        @type  show_rot_order:      string array
        @param show_rot_order:      the attribute names you want locked,
                                    unkeyable, and hidden

        @type  size:                float
        @param size:                average size of all points in ctl in units

        @type  orient:              float array
        @param orient:              x,y,z values you want to rotate the points
                                    by.  These values will not be reflected in
                                    the transform of the control

        @type  offset:              float array
        @param offset:              x,y,z values you want to translate the 
                                    points by.  These values will not be 
                                    reflected in the transform of the control

        @type  scale:               float array
        @param scale:               x,y,z values you want to scale the 
                                    points by.  These values will not be 
                                    reflected in the transform of the control

        @type  hide:                bool
        @param hide:                if True control will be hidden
        """

        #---args
        self.side                   = side
        self.name                   = name
        self.parent                 = parent
        self.shape                  = shape
        self.lock_attrs             = lock_attrs
        self.num_buffer             = num_buffer
        self.gimbal                 = gimbal
        self.num_secondary          = num_secondary
        self.show_rot_order         = show_rot_order
        self.size                   = size
        self.orient                 = orient
        self.offset                 = offset
        self.scale                  = scale
        self.hide                   = hide
        #---vars
        self.ctl                    = ""
        self.gimbal_ctl             = ""
        self.buffers                = []
        self.gimbal_vis_attr        = ""
        self.buffer_parent          = ""
        self.gimbal_parent          = ""
        
        self.__create()

    def __check(self):
        "checks to make sure shape is supported"
        if not(self.shape != "circle" or 
               self.shape != "sphere" or 
               self.shape != "switch" or 
               self.shape != "cube" or 
               self.shape != "ik/fk" or 
               self.shape != "shoulder"):
            raise Exception(self.shape + " is not supported yet")
            quit()

    def __create_buffer(self):
        "creates extra transforms to parent the ctls under"
        for i in range(self.num_buffer):
            format_num = self.num_buffer-i
            self.parent = cmds.createNode("transform", 
                                          name = self.side
                                          + "_"
                                          + self.name
                                          + "Buffer"
                                          + str(format_num)
                                          + "_GRP",
                                          parent = self.parent)
            self.buffers.append(self.parent)
        self.buffers_parent =  self.buffers[0]

    def __create_ctl(self):
        "creates ctl"
        self.ctl = draw_ctl(side = self.side,
                            name = self.name,
                            parent = self.parent, 
                            shape = self.shape, 
                            lock_attrs = self.lock_attrs, 
                            size = self.size,
                            show_rot_order = self.show_rot_order,
                            orient = self.orient,
                            offset = self.offset,
                            scale = self.scale,
                            hide = self.hide).ctl

    def __create_secondary(self):
        "creates ctl"
        sec_parent = []
        size = self.size
        for i in range(self.num_secondary):
            if i == 0:
                parent = self.ctl
            else:
                parent = sec_parent[i-1]
            size = size / 1.1
            sec_parent.append(  draw_ctl(side = self.side,
                                name = self.name + str(i),
                                parent = parent, 
                                shape = self.shape, 
                                lock_attrs = self.lock_attrs,
                                size = size,
                                show_rot_order = self.show_rot_order,
                                orient = self.orient,
                                offset = self.offset,
                                scale = self.scale,
                                hide = self.hide).ctl)
            if i == self.num_secondary-1:
                self.gimbal_parent = sec_parent[i]

    def __create_gimbal(self):
        ""
        if self.num_secondary > 0:
            parent = self.gimbal_parent
        else:
            parent = self.ctl
        if self.gimbal == True:
            self.gimbal_ctl = draw_ctl(side = self.side,
                                       name = self.name + "Gimbal",
                                       parent = parent, 
                                       shape = "sphere", 
                                       lock_attrs = ["tx","ty","tz",
                                                     "sx","sy","sz"], 
                                       size = self.size * .9,
                                       show_rot_order = True).ctl
            gimbal_shape = cmds.listRelatives(self.gimbal_ctl, shapes = True)[0]
            cmds.setAttr(gimbal_shape + ".overrideColor", 19)

    def __make_gimbal_vis(self):
        ""
        if self.gimbal == True:
            cmds.addAttr(self.ctl, ln = "gimbal_vis", at = "short", dv = 0,
                         min = 0, max = 1)
            self.gimbal_vis_attr = self.ctl+".gimbal_vis"
            cmds.setAttr( self.gimbal_vis_attr, cb = True, k = False)
            gimbalShape = cmds.listRelatives(self.gimbal_ctl, shapes = True)[0]
            cmds.connectAttr(self.gimbal_vis_attr, gimbalShape + ".v")
            cmds.setAttr( gimbalShape + ".v", l = True, cb = False, k = False)

    def __create(self):
        ""
        self.__check()
        self.__create_buffer()
        self.__create_ctl()
        self.__create_secondary()
        self.__create_gimbal()
        self.__make_gimbal_vis()

##########################################################
#---example
# create_ctl(side = "C", 
#            name = "ctl", 
#            parent = 'character_grp', 
#            shape = "switch",
#            num_buffer = 5,
#            lock_attrs = ["tx","ty","tz","v"], 
#            gimbal = True,
#            size = 1)
##########################################################

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
        @type  target:                string
        @param target:                name of the transform that will be 
                                      snapped to (driver)

        @type  source:                string array
        @param source:                names of the transforms that will be
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
        @type  ctl:                  string array
        @param ctl:                  name of the ctl that will have the space
                                     switch attrs

        @type  ctl_grp:              string array
        @param ctl_grp:              name of the group above the ctl
        
        @type  space_names:          string array
        @param space_names:          the names you would like to give your
                                     space switches (cleaner way of naming than
                                     using the space parents)

        @type  space_parents:        string array
        @param space_parents:        the things driving the ik control
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
                 skel_group = ""
                 ):
        """
        @type  ctl:                  string array
        @param ctl:                  name of the ctl that will have the space
                                     switch attrs

        @type  ctl_grp:              string array
        @param ctl_grp:              name of the group above the ctl

        @type  default_align_parent: string array
        @param default_align_parent: usually the name of the group above the 
                                     ctl_grp or anything you want to be the 
                                     to be aligned to by default


        @type  skel_group:           string array
        @param skel_group:           the group where you parent your skeleton
        """

        #---args
        self.ctl                     = ctl
        self.ctl_grp                 = ctl_grp
        self.default_align_parent    = default_align_parent
        self.skel_group              = skel_group

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
                                                      self.ctl_grp)[0]

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



#===============================================================================
#CLASS:         create_spline_ik
#DESCRIPTION:   creates spline ik along with clusters w/ locator handles
#USAGE:         set args and run
#RETURN:        align_attr, reverse_node, align_constraint, world_transform
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 21st, 2014
#Version        1.0.0
#===============================================================================

class create_spline_ik():
    def __init__(self,
                 side = "C",
                 name = "torso",
                 joints = [],
                 curve_parent = "",
                 inherit_transform = False,
                 cluster_parents = [],
                 ik_handle_parent = "",
                 hide = True, 
                 ):
        """
        @type  side:                string
        @param side:                C or L or R

        @type  name:                string
        @param name:                the name of your torso

        @type  joints:              string array
        @param joints:              the joints that will be in the ik,
                                    please list in hierarchical order

        @type  curve_parent:        string
        @param curve_parent:        where you would like to parent the curve
                                    if blank curve will not be parented

        @type  inherit_transform:   bool
        @param inherit_transform:   whether or not you want the curve to 
                                    inherit the transform of the group it is
                                    under. To avoid double movement I would
                                    recommend setting this to false

        @type  cluster_parents:     string array
        @param cluster_parents:     where to parent your locator cluster
                                    handles.  This list should be as long
                                    as your joints, if left blank, clusters
                                    will not be parented

        @type  ik_handle_parent:    string array
        @param ik_handle_parent:    where to parent your ik handle if blank
                                    ik handle will not be parented

        @type  hide:                bool
        @param hide:                if true hides the controls that are created
        """
        #---args
        self.side                   = side
        self.name                   = name
        self.joints                 = joints
        self.curve_parent           = curve_parent
        self.inherit_transform      = inherit_transform
        self.cluster_parents        = cluster_parents
        self.ik_handle_parent       = ik_handle_parent
        self.hide                   = hide
        #---vars
        self.ik                     = []
        self.curve                  = ""
        self.clusters               = []
        self.cluster_ctls           = []
        self.cluster_ctl_buffers    = []
        self.points                 = []

        self.__create()

    def __check_exists(self):
        for i in self.joints:
            if cmds.objExists(i):
                if cmds.nodeType(i) != "joint":
                    raise Exception(i + " must be a joint")
                    quit()
            else:
                raise Exception(i + " does not exist")
                quit()

        if self.cluster_parents:
            for i in  self.cluster_parents:
                if not cmds.objExists(i):
                    raise Exception(i + " does not exist")

        if self.curve_parent:
                if not cmds.objExists(self.curve_parent):
                    raise Exception(self.curve_parent + " does not exist")

        if self.ik_handle_parent:
                if not cmds.objExists(self.ik_handle_parent):
                    raise Exception(self.ik_handle_parent + " does not exist")

    def __draw_curve(self):
        knots = []
        for i in range(len(self.joints)):
            self.points.append(tuple(cmds.xform(self.joints[i],
                                     q =True,
                                     ws=True,
                                     t=True)))
            knots.append(i)
        self.curve = cmds.curve(n = (self.side
                                     + "_"
                                     + self.name
                                     + "SplineIK_CRV"),
                                d = 1, 
                                p = self.points,
                                k = knots)
        if self.inherit_transform == False:
            cmds.setAttr(self.curve + ".inheritsTransform",0)
        cmds.parent(self.curve,
                    self.curve_parent)
        
    def __create_clusters(self):
        tmp_cluster_ctls = []
        for i in range(len(self.joints)):

            tmp_cluster_ctls.append(create_ctl( side = self.side, 
                                            name = self.name + "Cluster"+str(i), 
                                            parent = self.cluster_parents[i],
                                            shape = "cube",
                                            lock_attrs = ["all"], 
                                            num_buffer = 1, 
                                            gimbal = False,
                                            show_rot_order = False, 
                                            size = .01,
                                            hide = self.hide))
            self.cluster_ctls.append(tmp_cluster_ctls[i].ctl)
            self.cluster_ctl_buffers.append(tmp_cluster_ctls[i].buffers)
            
            con = cmds.pointConstraint(self.joints[i],
                                        self.cluster_ctl_buffers[i][0])
            cmds.delete(con)

            self.clusters.append(cmds.cluster(self.curve 
                                               + ".cv["
                                               + str(i) 
                                               + "]",
                                              name = (self.side 
                                                      + "_" 
                                                      + self.name
                                                      + str(i)
                                                      + "_CLS"),
                                              wn = (tmp_cluster_ctls[i].ctl,
                                                    tmp_cluster_ctls[i].ctl,),
                                              bindState=True))
            cmds.rename("clusterHandleShape", 
                        self.side + "_" + self.name + str(i) + "_CLS" + "Shape")

    def __create_ik(self):
        self.ik = cmds.ikHandle(sj = self.joints[0], 
                                ee = self.joints[len(self.joints)-1],
                                sol = "ikSplineSolver", 
                                curve = self.curve, 
                                name = (self.side 
                                        + "_" 
                                        + self.name
                                        + "Ik_IKH"),
                                ccv = False,
                                pcv = False)
        cmds.parent(self.ik[0],self.ik_handle_parent)

    def __setup_advanced_twist(self):
        cmds.setAttr(self.ik[0] + ".dTwistControlEnable", 1);
        cmds.setAttr(self.ik[0] + ".dWorldUpType", 4)
        cmds.setAttr(self.ik[0] + ".dWorldUpVectorY", 0)
        cmds.setAttr(self.ik[0] + ".dWorldUpVectorEndY", 0)
        cmds.setAttr(self.ik[0] + ".dWorldUpVectorZ", 1)
        cmds.setAttr(self.ik[0] + ".dWorldUpVectorEndZ", 1)
        cmds.setAttr(self.ik[0] + ".dWorldUpAxis", 3)
        cmds.connectAttr(self.cluster_ctls[0]+ ".worldMatrix[0]", 
                         self.ik[0]+ ".dWorldUpMatrix",
                         f = True)
        cmds.connectAttr(self.cluster_ctls[len(self.cluster_ctls)-1]+ 
                         ".worldMatrix[0]", 
                         self.ik[0] + ".dWorldUpMatrixEnd",
                         f = True)

    def __create(self):

        self.__check_exists()
        self.__draw_curve()
        self.__create_clusters()
        self.__create_ik()
        self.__setup_advanced_twist()

##########################################################
# #---example
# create_spline_ik( 
#                  side = "C",
#                  name = "torso",
#                  joints = ['spinea_bind', 
#                            'spineb_bind',
#                            'spinec_bind',
#                            'spined_bind',
#                             ],
#                  curve_parent = "character_grp",
#                  inherit_transform = False,
#                  cluster_parents = ["character_grp",
#                                     "character_grp",
#                                     "character_grp",
#                                     "character_grp",
#                                     ],
#                  ik_handle_parent = "character_grp", 
#                  )
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
                             ad = True)
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

#===============================================================================
#CLASS:         create_rivet_rig
#DESCRIPTION:   creates a simple single ctl rig constrained to a poly plane
#USAGE:         set args and run
#RETURN:        constraint, ctl, ctl, buffers, gimbal, poly_plane
#REQUIRES:      maya.cmds
#AUTHOR:        Levi Harrison
#DATE:          Oct 27th, 2014
#Version        1.0.0
#===============================================================================

class create_rivet_rig():
    def __init__(self, 
                 side = "C",
                 name = "rivet001",
                 translate = (0,0,0),
                 rotate = (0,0,0),
                 scale = (1,1,1),
                 uv = (0.5,0.5),
                 num_buffer = 2,
                 rig_parent = "C_rig_GRP", 
                 skel_parent = "C_skeleton_GRP",
                 shape = "sphere",
                 lock_attrs=["v"],
                 gimbal = False,
                 show_rot_order= True,
                 size = 1,
                 orient = [0,0,0],
                 offset = [0,0,0],
                 ctl_scale = [1,1,1],
                 hide = False,
                 global_scale = "",
                 debug = False
                 ):
        """
        @type  side:                 string
        @param side:                 C or L or R

        @type  name:                 string
        @param name:                 the name of your rivet

        @type  translate:            3 tuple
        @param translate:            translation of the poly plane (Tx, Ty, Tz 
                                     attributes)

        @type  rotate:               3 tuple
        @param rotate:               rotation of the poly plane (Rx, Ry, Rz 
                                     attributes)

        @type  scale:            3 tuple
        @param scale:            scale of the poly plane (Sx, Sy, Sz 
                                     attributes)

        @type  uv:                   2 doubles
        @param uv:                   this will tell the point on poly constraint
                                     what u and v parameters you want to 
                                     constrain to

        @type  num_buffer:        unsigned int
        @param num_buffer:        the amount of buffers you will have above
                                     your ctl one is mandatory (even if you give
                                     0) but above that is your choice. 

        @type  rig_parent:            string array
        @param rig_parent:            the group where you parent your skeleton
        
        @type  skel_parent:           string array
        @param skel_parent:           the group where you parent your skeleton

        @type  shape:               string
        @param shape:               ctl arg: shape name, currently supported:
                                    circle
                                    sphere
                                    switch
                                    cube
                                    shoulder

        @type  lock_attrs:          string array
        @param lock_attrs:          ctl arg: the attribute names you want 
                                    locked, unkeyable, and hidden

        @type  gimbal:              bool
        @param gimbal:              ctl arg: whether or not you want a gimbal 
                                    control not recommended for controls with 
                                    less than all 3 rotation attributes

        @type  show_rot_order:      string array
        @param show_rot_order:      ctl arg: the attribute names you want 
                                    locked, unkeyable, and hidden

        @type  size:                float
        @param size:                ctl arg: average size of all points in ctl 
                                    in units

        @type  orient:              float array
        @param orient:              ctl arg: x,y,z values you want to rotate the
                                    points by.  These values will not be 
                                    reflected in the transform of the control

        @type  offset:              float array
        @param offset:              ctl arg: x,y,z values you want to translate
                                    the points by.  These values will not be 
                                    reflected in the transform of the control

        @type  ctl_scale:           float array
        @param ctl_scale:           ctl arg: x,y,z values you want to scale the 
                                    points by.  These values will not be 
                                    reflected in the transform of the control

        @type  hide:                bool
        @param hide:                ctl arg: if True control will be hidden

        @type  global_scale:        string
        @param global_scale:        what the rig will be attached to
                                    for scaling usually lowest point in
                                    hierarchy of global ctl
        """

        #---args
        self.side                    = side
        self.name                    = name
        self.translate               = translate
        self.rotate                  = rotate
        self.scale                   = scale
        self.uv                      = uv
        self.num_buffer              = num_buffer
        self.rig_parent              = rig_parent
        self.skel_parent             = skel_parent
        self.shape                   = shape
        self.gimbal                  = gimbal
        self.lock_attrs              = lock_attrs
        self.show_rot_order          = show_rot_order
        self.size                    = size
        self.orient                  = orient
        self.offset                  = offset
        self.ctl_scale               = ctl_scale
        self.global_scale            = global_scale
        self.hide                    = hide
        self.debug                   = debug
        #---vars
        self.constraint              = []
        self.ctl                     = ""
        self.jnt                     = ""
        self.buffers                 = []
        self.gimbal                  = ""
        self.poly_plane              = ""

        self.__create()

    def __create_parents(self):
        """ create groups for skeleton and rig """
        self.skel_parent = cmds.createNode("transform",
                                          n = self.side +"_" + 
                                          self.name + "Skel_GRP",
                                          p = self.skel_parent)

        self.rig_parent = cmds.createNode("transform",
                                          n = self.side
                                          +"_"
                                          + self.name 
                                          + "Rig_GRP",
                                          p = self.rig_parent)

    def __create_poly_plane(self):
        self.poly_plane = cmds.polyPlane(name = (self.side
                                                 +"_"
                                                 + self.name
                                                 + "plane_EX"),
                                         ch = False,
                                         cuv = 2,
                                         sx = 1,
                                         sy = 1,
                                         ax = [0,1,0],
                                         w = 1,
                                         h = 1,
                                         )
        cmds.parent(self.poly_plane,self.skel_parent)
        cmds.setAttr(self.poly_plane[0] + ".inheritsTransform",0)

    def __create_skel(self):
        self.jnt = cmds.createNode("joint",
                                   name = (self.side
                                           +"_"
                                           + self.name
                                           + "_JNT"),
                                   parent = self.skel_parent)
        cmds.addAttr(self.jnt, 
                     ln = "SEC_BIND",
                     at = "bool",)
        cmds.setAttr(self.jnt+".SEC_BIND", 
                     l = True, 
                     k=False)

    def __create_ctl(self):
        if self.num_buffer <1:
            self.num_buffer =1
        self.ctl = create_ctl(side = self.side, 
                              name = self.name, 
                              parent = self.rig_parent, 
                              shape = self.shape, 
                              lock_attrs = self.lock_attrs, 
                              num_buffer = self.num_buffer, 
                              gimbal = self.gimbal, 
                              show_rot_order = self.show_rot_order, 
                              size = self.size, 
                              orient = self.orient, 
                              offset = self.offset, 
                              scale = self.ctl_scale, 
                              hide = self.hide)
        if  self.ctl.gimbal_ctl:
            self.gimbal = self.ctl.gimbal_ctl
        else:
            self.gimbal = self.ctl.ctl
        self.buffers = self.ctl.buffers
        self.ctl = self.ctl.ctl

    def __constrain(self):
        self.constraint = cmds.pointOnPolyConstraint(self.poly_plane,
                                                     self.buffers[0],
                                                     name = self.side+
                                                     self.name+"_PPC")
        cmds.setAttr(self.constraint[0] + " .u0",self.uv[0])
        cmds.setAttr(self.constraint[0] + " .v0",self.uv[1])
        cmds.parentConstraint(self.gimbal, 
                              self.jnt, 
                              name = self.side
                              +self.name+"_PAC")
        cmds.parentConstraint(self.gimbal, 
                              self.jnt, 
                              name = self.side
                              +self.name+"_PAC")

    def __move(self):
        cmds.move(self.translate[0],
                  self.translate[1],
                  self.translate[2],
                  self.poly_plane,
                  r=True)
        cmds.rotate(self.rotate[0],
                    self.rotate[1],
                    self.rotate[2],
                    self.poly_plane,
                    r=True)
        cmds.scale(self.scale[0],
                   self.scale[1],
                   self.scale[2],
                   self.poly_plane,
                   r=True)

    def __global_scale(self):
        if self.global_scale:
            cmds.scaleConstraint(self.global_scale, self.rig_parent, mo = True)
            cmds.scaleConstraint(self.global_scale, self.skel_parent, mo = True)

    def __cleanup(self):
        if self.debug == False:
            suffix_constraints()
            lock_all(hierarchy = self.rig_parent, filter = ["*_CTL", "*_JNT"])
            lock_all(hierarchy = self.skel_parent, filter = ["*_CTL", "*_JNT","*_EX"])

    def __create(self):
        self.__create_parents()
        self.__create_poly_plane()
        self.__create_skel()
        self.__create_ctl()
        self.__constrain()
        self.__move()
        self.__global_scale()
        self.__cleanup()

##########################################################
#---example
# create_rivet_rig(side = "C",
#                  name = "holster01",
#                  translate = (0.14,1.506,0.097),
#                  rotate = (104.725,36.104,-259.825),
#                  scale = (0.099,0.01,0.025),
#                  uv = (0.5,0.5),
#                  num_buffer = 1,
#                  rig_parent = "C_rig_GRP", 
#                  skel_parent = "C_skeleton_GRP",
#                  shape = "sphere",
#                  lock_attrs=["v"],
#                  show_rot_order= True,
#                  size = .03,
#                  orient = [0,0,0],
#                  offset = [0,0,0],
#                  ctl_scale = [1,1,1],
#                  gimbal = True,
#                  hide = False,
#                  global_scale = global_hook,
#                  debug = True)
#########################################################

def print_translate_rotate_scale():
    sel = cmds.ls(sl = True)
    print "TRANSLATE"
    if len(sel) > 1:
        for i in range(len(sel)):
            t = cmds.getAttr(sel[i] + ".t")
            if i == 0:
                print "[" + str(t[0]) + ","
            if i > 0 and i < len(sel)-1:
                print str(t[0]) + ","
            if i == len(sel)-1:
                print str(t[0]) + "]"
    else:
        t = cmds.getAttr(sel[0] + ".t")
        print "[" + str(t[0]) + "]"
    print "ROTATE"
    if len(sel) > 1:
        for i in range(len(sel)):
            t = cmds.getAttr(sel[i] + ".r")
            if i == 0:
                print "[" + str(t[0]) + ","
            if i > 0 and i < len(sel)-1:
                print str(t[0]) + ","
            if i == len(sel)-1:
                print str(t[0]) + "]"
    else:
        t = cmds.getAttr(sel[0] + ".r")
        print "[" + str(t[0]) + "]"
    print "SCALE"
    if len(sel) > 1:
        for i in range(len(sel)):
            t = cmds.getAttr(sel[i] + ".s")
            if i == 0:
                print "[" + str(t[0]) + ","
            if i > 0 and i < len(sel)-1:
                print str(t[0]) + ","
            if i == len(sel)-1:
                print str(t[0]) + "]"
    else:
        t = cmds.getAttr(sel[0] + ".s")
        print "[" + str(t[0]) + "]"



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
        cmds.setAttr("C_skeleton_GRP.overrideEnabled", 1)
        cmds.setAttr("C_skeleton_GRP.v", 0)



# a function to print and format point positions for gl drawings in python
def printPointsPY(object):
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
            print "[(" + str(points[i][0]) + ", " + str(points[i][1]) + ", " + str(points[i][2]) + "),"

        if i != 0 and i != points.length()-1:
            print "(" + str(points[i][0]) + ", " + str(points[i][1]) + ", " + str(points[i][2]) + "),"
        
        if i == points.length()-1:
            print "(" + str(points[i][0]) + ", " + str(points[i][1]) + ", " + str(points[i][2]) + ")]"


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
            print "{{" + str(points[i][0]) + "f, " + str(points[i][1]) + "f, " + str(points[i][2]) + "f},"
        if i != 0 and i != points.length()-1:
            print "{" + str(points[i][0]) + "f, " + str(points[i][1]) + "f, " + str(points[i][2]) + "f},"
        if i == points.length()-1:
            print "{" + str(points[i][0]) + "f, " + str(points[i][1]) + "f, " + str(points[i][2]) + "f}}"

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
    print pointArray

def setFaceIdsOnLocator(locatorName):
    faces = cmds.ls(sl = True, fl=True)
    faces = [x.split("[")[1] for x in faces]
    faces = [x.split("]")[0] for x in faces]
    faces = [int(x) for x in faces]
    cmds.setAttr(locatorName + ".faceIds", faces, type = "doubleArray")
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
            print old_str, new_str
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
    return cmds.listRelatives(mayaObject, shapes=True)[0]

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
    @param geomDict: dictionary of geometry
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
    print node

    if srcOutput and selfInput:
        cmds.connectAttr(srcOutput, "{0}.{1}".format(node, selfInput))
    if selfOutput and dstInput:
        cmds.connectAttr("{0}.{1}".format(node, selfOutput), dstInput)
    return node



'''
#button press
tool = maya.cmds.weightSlideContext()
maya.cmds.setToolTo( tool )
#button release
maya.cmds.deleteUI(tool)
maya.mel.eval("SelectToolOptionsMarkingMenu;MarkingMenuPopDown;")
'''
    