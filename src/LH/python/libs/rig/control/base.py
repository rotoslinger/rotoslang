from maya import cmds

from rig_2.tag import utils as tag_utils
from rig.utils import misc
from rig.utils import exportUtils
import importlib
importlib.reload(tag_utils)
importlib.reload(misc)
importlib.reload(exportUtils)


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
                 customShape=None,
                 color = None,
                 hide = False,
                 suffix = "_CTL"
                 ):

        """
        type  side:                string
        param side:                side the control is on C,L,R

        type  name:                string
        param name:                name of the ctl

        type  parent:              string
        param parent:              the transform this will be parented under

        type  shape:               string
        param shape:               shape name, currently supported:
                                    circle
                                    sphere
                                    switch
                                    cube
                                    square
                                    shoulder
                                    ik\\fk

        type  lock_attrs:          string array
        param lock_attrs:          the attribute names you want locked,
                                    unkeyable, and hidden

        type  show_rot_order:      bool
        param show_rot_order:          if true, rotation order is exposed as a
                                    non keyable attribute

        type  size:                float
        param size:                average size of all points in ctl in units

        type  orient:              float array
        param orient:              x,y,z values you want to rotate the points
                                    by.  These values will not be reflected in
                                    the transform of the control

        type  offset:              float array
        param offset:              x,y,z values you want to translate the
                                    points by.  These values will not be
                                    reflected in the transform of the control

        type  scale:               float array
        param scale:               x,y,z values you want to scale the
                                    points by.  These values will not be
                                    reflected in the transform of the control
        type  hide:                bool
        param hide:                if true control visibility will be set to 0
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
        self.customShape            = customShape
        self.color                  = color
        self.suffix                 = suffix

        #---vars
        self.ctl                    = ""
        if self.customShape:
            self.shape = ""

        self.__create()

    def __check(self):
        "checks to make sure shape is supported"
        if not(self.shape != "circle" or
               self.shape != "sphere" or
               self.shape != "switch" or
               self.shape != "cube" or
               self.shape != "square" or
               self.shape != "ik/fk" or
               self.shape != "" or
               self.shape != "shoulder"):
            raise Exception(self.shape + " is not supported yet")
            quit()

    def __circle(self):
        if (self.shape == "circle"):
            self.ctl = cmds.circle(n = self.side + "_" + self.name +  self.suffix,
                                   nr=(1, 0, 0), c=(0, 0, 0), r = self.size)[0]
            cmds.parent(self.ctl, self.parent)

    def __sphere(self):
        if (self.shape == "sphere"):
            self.ctl = cmds.curve(n = self.side + "_" + self.name +  self.suffix,
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
            self.ctl = cmds.curve(n = self.side + "_" + self.name +  self.suffix,
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
            self.ctl = cmds.curve(n = self.side + "_" + self.name +  self.suffix,
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
            self.ctl = cmds.curve(n = self.side + "_" + self.name +  self.suffix,
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
            self.ctl = cmds.curve(n = self.side + "_" + self.name + self.suffix,
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
            self.ctl = cmds.curve(n = self.side + "_" + self.name + self.suffix,
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

    def createCustomShape(self):
        if (self.customShape):
            self.ctl = cmds.createNode("transform", n=self.side + "_" + self.name + self.suffix, p=self.parent)
            curve = exportUtils.create_curve_2(self.customShape, self.side + "_" + self.name + self.suffix + "Shape", self.ctl)

            # self.ctl = createGeoFromData(self.customShape, name = self.side + "_" + self.name + self.suffix).fullPathName()
            # print  "CURVE SHAPE,", self.ctl
            # self.ctl = cmds.listRelatives(self.ctl, p=True)[0]
            # cmds.parent(self.ctl, self.parent)
            cmds.scale(self.size, self.size, self.size,
                       self.ctl + ".cv[0:]",
                       r = True,p = (0, 0, 0))

    def __lock_it(self):
        if self.hide == True:
            cmds.setAttr(self.ctl + ".v", 0)
        if self.lock_attrs == ["all"]:
            self.lock_attrs = ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]
        for i in range(len(self.lock_attrs)):
            cmds.setAttr(self.ctl + "." + self.lock_attrs[i],
                          lock = True,
                          keyable = False,
                          channelBox = False)

    def __color_it(self, color_rgb = (0.0,0.0,0.0)):
        # color_rgb can be a numerical rgb value like so:
        # color_rgb = (1.0,1.0,0.0)
        # if none, base it on side naming
        ctl_shape = cmds.listRelatives(self.ctl, shapes = True)[0]
        cmds.setAttr(ctl_shape + ".overrideEnabled", True)
        color = ctl_shape + ".overrideColor"
        cmds.setAttr(ctl_shape + ".overrideRGBColors", 1)
        if color_rgb:
            cmds.setAttr(color + "R", color_rgb[0])
            cmds.setAttr(color + "G", color_rgb[1])
            cmds.setAttr(color + "B", color_rgb[2])
            return 
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
        self.createCustomShape()
        self.__lock_it()
        self.__color_it(color_rgb = self.color)
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
                 customShape = "",
                 lock_attrs=[],
                 num_buffer = 0,
                 add_fit_ctrl = False, # if true each buffer gets a nurbscurve shape added and the tag CONTROLFIT and clusters to controls for scaling.
                 gimbal = False,
                 num_secondary = 0,
                 show_rot_order = True,
                 size = 1,
                 orient = [0,0,0],
                 offset = [0,0,0],
                 scale = [1,1,1],
                 hide = False,
                 color = None,
                 nullTransform = False,
                 create_joint = False,
                 create_buffer_shape = False
                 ):

        """
        type  side:                string
        param side:                the side the control is on C,L,R

        type  name:                string
        param name:                name of the ctl

        type  parent:              string
        param parent:              the transform this will be parented under

        type  shape:               string
        param shape:               shape name, currently supported:
                                    circle
                                    sphere
                                    switch
                                    cube
                                    shoulder

        type  lock_attrs:          string array
        param lock_attrs:          the attribute names you want locked,
                                    unkeyable, and hidden

        type  num_buffer:          int
        param num_buffer:          number of transforms to group ctl under

        type  gimbal:              bool
        param gimbal:              whether or not you want a gimbal control
                                    not recommended for controls with less than
                                    all 3 rotation attributes

        type  num_secondary:       bool
        param num_secondary:       creates extra controls which will be
                                    parented under the main ctl

        type  show_rot_order:      string array
        param show_rot_order:      the attribute names you want locked,
                                    unkeyable, and hidden

        type  size:                float
        param size:                average size of all points in ctl in units

        type  orient:              float array
        param orient:              x,y,z values you want to rotate the points
                                    by.  These values will not be reflected in
                                    the transform of the control

        type  offset:              float array
        param offset:              x,y,z values you want to translate the
                                    points by.  These values will not be
                                    reflected in the transform of the control

        type  scale:               float array
        param scale:               x,y,z values you want to scale the
                                    points by.  These values will not be
                                    reflected in the transform of the control

        type  hide:                bool
        param hide:                if True control will be hidden

        type  create_bone:                bool
        param create_bone:                if True create a create_bone
        """

        #---args
        self.side                   = side
        self.name                   = name
        self.parent                 = parent
        self.shape                  = shape
        self.customShape            = customShape
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
        self.nullTransform          = nullTransform
        self.create_joint            = create_joint
        self.color                  = color
        if self.customShape:
            self.shape              = ""
        self.shape_node             = ""
        self.create_buffer_shape    = create_buffer_shape


        #---vars
        self.ctl                    = ""
        self.gimbal_ctl             = ""
        self.buffers                = []
        self.gimbal_vis_attr        = ""
        self.buffer_parent          = ""
        self.gimbal_parent          = ""

        self.__create()

    def __create(self):
        ""
        self.__check()
        if self.create_buffer_shape:
            self.__create_buffer_as_shape()
        else:
            self.__create_buffer()
        self.__create_ctl()
        self.__create_secondary()
        self.__create_gimbal()
        self.__make_gimbal_vis()
        self.add_tags()

    def __check(self):
        "checks to make sure shape is supported"
        if not(self.shape != "circle" or
               self.shape != "sphere" or
               self.shape != "switch" or
               self.shape != "cube" or
               self.shape != "ik/fk" or
               self.shape != "" or
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


    def __create_buffer_as_shape(self):
        "creates extra transforms to parent the ctls under"
        self.buffer_shapes = []
        self.shape_size_attr = ""
        for i in range(self.num_buffer):
            format_num = self.num_buffer-i
            temp_buffer = draw_ctl(
                                    name =  self.side
                                            + "_"
                                            + self.name
                                            + "Buffer"
                                            + str(format_num)
                                            + "_GRP",
                                    parent = self.parent,
                                    shape = self.shape,
                                    size =self.size,
                                    show_rot_order = False,
                                    orient = self.orient,
                                    color = (1,1,1),
                                    hide = False)
            self.parent = temp_buffer.ctl
            buffer_shape = misc.getShape(self.parent)
            self.buffer_shapes.append(buffer_shape)
            self.buffers.append(self.parent)
            # Add attr for buffer_shape_vis, connect to shape.
            # 
            self.maintenence_grp = tag_utils.get_all_with_tag("MAINTENANCE_GRP")[0]
            self.fit_ctrl_vis = self.maintenence_grp + ".fit_ctrl_vis"
            cmds.connectAttr(self.fit_ctrl_vis, buffer_shape + ".visibility")
            cmds.setAttr(buffer_shape + ".alwaysDrawOnTop", 1)
            if i == self.num_buffer-1:
                cmds.addAttr(temp_buffer.ctl,
                ln = "ctrl_siz", 
                at = "float", 
                dv = 1,
                min = 0,
                k = True)
                self.shape_size_attr = temp_buffer.ctl + ".ctrl_siz"
        self.buffers_parent =  self.buffers[0]

    def __create_ctl(self):
        "creates ctl"
        self.ctl = draw_ctl(side = self.side,
                            name = self.name,
                            parent = self.parent,
                            shape = self.shape,
                            customShape = self.customShape,
                            lock_attrs = self.lock_attrs,
                            size = self.size,
                            show_rot_order = self.show_rot_order,
                            orient = self.orient,
                            offset = self.offset,
                            scale = self.scale,
                            color = self.color,
                            hide = self.hide).ctl
        self.shape_node = misc.getShape(self.ctl)

        if self.nullTransform:
            name = self.ctl
            parent = misc.getParent(self.ctl)
            self.ctl = cmds.rename(self.ctl, self.ctl + "OLD")
            nullTrans = cmds.createNode("nullTransform", n=name, p=parent)
            shape = misc.getShape(self.ctl)
            cmds.parent(shape, nullTrans, s=True, r=True)
            cmds.delete(self.ctl)
            self.ctl = nullTrans
            if self.lock_attrs == ["all"]:
                self.lock_attrs = ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]
            for i in range(len(self.lock_attrs)):
                cmds.setAttr(self.ctl + "." + self.lock_attrs[i],
                            lock = True,
                            keyable = False,
                            channelBox = False)
        self.joint = ''
        self.parent_constraint = ''
        self.scale_constraint = ''
        if self.create_joint:
            self.joint = cmds.joint( self.ctl, name=self.side + self.name + "_jnt")
            self.parent_constraint = cmds.parentConstraint(self.ctl , self.joint)
            self.scale_constraint = cmds.scaleConstraint(self.ctl, self.joint)
        if self.create_buffer_shape:
            # create cluster in rig control connect buffer siz attr to scale
            # self.ctl
            cluster_parent = tag_utils.get_all_with_tag("RIG_CONTROL_SIZE_GRP")
            self.shape_siz_clust, self.shape_siz_clust_handle = cmds.cluster(self.shape_node, name=self.shape_node + "Cluster") # the cluster handle is at index 1, this is what to scale
            cmds.parent(self.shape_siz_clust_handle, cluster_parent)
            cmds.connectAttr(self.shape_size_attr, self.shape_siz_clust_handle + ".scaleX")
            cmds.connectAttr(self.shape_size_attr, self.shape_siz_clust_handle + ".scaleY")
            cmds.connectAttr(self.shape_size_attr, self.shape_siz_clust_handle + ".scaleZ")
            self.cluster_vis_attr = self.maintenence_grp + ".size_cluster_vis"
            cmds.connectAttr(self.cluster_vis_attr, self.shape_siz_clust_handle + ".visibility")
        self.maintenence_grp = tag_utils.get_all_with_tag("MAINTENANCE_GRP")[0]
        self.ctrl_shape_vis_attr = self.maintenence_grp + ".ctrl_shape_vis"
        cmds.connectAttr(self.ctrl_shape_vis_attr, self.shape_node + ".visibility")

            

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

    def add_tags(self):
        # for i in range(50):
        #     print("CREATING TAGS")
        if self.gimbal == True:
            self.gimbal_shape = misc.getShape(self.gimbal_ctl) 
            tag_utils.tag_gimbal(self.gimbal_shape)
            # gimbal shape
            cmds.addAttr(self.ctl, ln = "gimbal", at = "message")
            cmds.connectAttr(self.gimbal_shape + ".message", self.ctl + ".gimbal")
        if self.create_joint:
            tag_utils.tag_bind_joint(self.joint)


        tag_utils.tag_control(self.ctl)
        tag_utils.tag_control_shape(misc.getShape(self.ctl))

        for buffer in self.buffers:
            tag_utils.tag_buffer(buffer)
        if self.create_buffer_shape:
            for buffer_shape in self.buffer_shapes:
                tag_utils.tag_buffer_shape(buffer_shape)


    ##########################################################
    # ---example
    # create_ctl(side = "C",
    #            name = "ctl",
    #            parent = 'character_grp',
    #            shape = "switch",
    #            num_buffer = 5,
    #            lock_attrs = ["tx","ty","tz","v"],
    #            gimbal = True,
    #            size = 1)
    ##########################################################

def create_circle_in_xform(transform_name):
    # Create a NURBS circle shape
    curve_shape = cmds.circle(name=transform_name + "Shape", constructionHistory=False, normal=(0, 1, 0), radius=1.0)[0]
    # Parent the circle shape to the existing transform (without affecting transforms)
    cmds.parent(curve_shape, transform_name, shape=True, relative=True)
    # Delete the temporary transform node created with the circle
    cmds.delete(transform_name + "Shape")

class create_spline_ik():
    # ===============================================================================
    # CLASS:         create_spline_ik
    # DESCRIPTION:   creates spline ik along with clusters w/ locator handles
    # USAGE:         set args and run
    # RETURN:        align_attr, reverse_node, align_constraint, world_transform
    # REQUIRES:      maya.cmds
    # AUTHOR:        Levi Harrison
    # DATE:          Oct 21st, 2014
    # Version        1.0.0
    # ===============================================================================
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
        type  side:                string
        param side:                C or L or R

        type  name:                string
        param name:                the name of your torso

        type  joints:              string array
        param joints:              the joints that will be in the ik,
                                    please list in hierarchical order

        type  curve_parent:        string
        param curve_parent:        where you would like to parent the curve
                                    if blank curve will not be parented

        type  inherit_transform:   bool
        param inherit_transform:   whether or not you want the curve to
                                    inherit the transform of the group it is
                                    under. To avoid double movement I would
                                    recommend setting this to false

        type  cluster_parents:     string array
        param cluster_parents:     where to parent your locator cluster
                                    handles.  This list should be as long
                                    as your joints, if left blank, clusters
                                    will not be parented

        type  ik_handle_parent:    string array
        param ik_handle_parent:    where to parent your ik handle if blank
                                    ik handle will not be parented

        type  hide:                bool
        param hide:                if true hides the controls that are created

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

            tmp_cluster_ctls.append(create_ctl(side = self.side,
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
                                              
                                              weightedNode = (tmp_cluster_ctls[i].ctl,
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


class create_rivet_rig():
    # ===============================================================================
    # CLASS:         create_rivet_rig
    # DESCRIPTION:   creates a simple single ctl rig constrained to a poly plane
    # USAGE:         set args and run
    # RETURN:        constraint, ctl, ctl, buffers, gimbal, poly_plane
    # REQUIRES:      maya.cmds
    # AUTHOR:        Levi Harrison
    # DATE:          Oct 27th, 2014
    # Version        1.0.0
    # ===============================================================================
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
        type  side:                 string
        param side:                 C or L or R

        type  name:                 string
        param name:                 the name of your rivet

        type  translate:            3 tuple
        param translate:            translation of the poly plane (Tx, Ty, Tz
                                     attributes)

        type  rotate:               3 tuple
        param rotate:               rotation of the poly plane (Rx, Ry, Rz
                                     attributes)

        type  scale:            3 tuple
        param scale:            scale of the poly plane (Sx, Sy, Sz
                                     attributes)

        type  uv:                   2 doubles
        param uv:                   this will tell the point on poly constraint
                                     what u and v parameters you want to
                                     constrain to

        type  num_buffer:        unsigned int
        param num_buffer:        the amount of buffers you will have above
                                     your ctl one is mandatory (even if you give
                                     0) but above that is your choice.

        type  rig_parent:            string array
        param rig_parent:            the group where you parent your skeleton

        type  skel_parent:           string array
        param skel_parent:           the group where you parent your skeleton

        type  shape:               string
        param shape:               ctl arg: shape name, currently supported:
                                    circle
                                    sphere
                                    switch
                                    cube
                                    shoulder

        type  lock_attrs:          string array
        param lock_attrs:          ctl arg: the attribute names you want
                                    locked, unkeyable, and hidden

        type  gimbal:              bool
        param gimbal:              ctl arg: whether or not you want a gimbal
                                    control not recommended for controls with
                                    less than all 3 rotation attributes

        type  show_rot_order:      string array
        param show_rot_order:      ctl arg: the attribute names you want
                                    locked, unkeyable, and hidden

        type  size:                float
        param size:                ctl arg: average size of all points in ctl
                                    in units

        type  orient:              float array
        param orient:              ctl arg: x,y,z values you want to rotate the
                                    points by.  These values will not be
                                    reflected in the transform of the control

        type  offset:              float array
        param offset:              ctl arg: x,y,z values you want to translate
                                    the points by.  These values will not be
                                    reflected in the transform of the control

        type  ctl_scale:           float array
        param ctl_scale:           ctl arg: x,y,z values you want to scale the
                                    points by.  These values will not be
                                    reflected in the transform of the control

        type  hide:                bool
        param hide:                ctl arg: if True control will be hidden

        type  global_scale:        string
        param global_scale:        what the rig will be attached to
                                    for scaling usually lowest point in
                                    hierarchy of global ctl
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
            misc.lock_all(hierarchy = self.rig_parent, filter = ["*"+ self.suffix, "*_JNT"])
            misc.lock_all(hierarchy = self.skel_parent, filter = ["*" + self.suffix, "*_JNT","*_EX"])

    def __create(self):
        self.__create_parents()
        self.__create_poly_plane()
        self.__create_skel()
        self.__create_ctl()
        self.__constrain()
        self.__move()
        self.__global_scale()
        self.__cleanup()