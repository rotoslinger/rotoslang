from maya import cmds
from rig.utils import misc
from rig.utils import exportUtils


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
        self.customShape            = customShape

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

    def createCustomShape(self):
        if (self.customShape):
            self.ctl = cmds.createNode("transform", n=self.side + "_" + self.name + "_CTL", p=self.parent)
            curve = exportUtils.create_curve_2(self.customShape, self.side + "_" + self.name + "_CTL" + "Shape", self.ctl)

            # self.ctl = createGeoFromData(self.customShape, name = self.side + "_" + self.name + "_CTL").fullPathName()
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
        self.createCustomShape()
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
                 customShape = "",
                 lock_attrs=[],
                 num_buffer = 0,
                 gimbal = False,
                 num_secondary = 0,
                 show_rot_order = True,
                 size = 1,
                 orient = [0,0,0],
                 offset = [0,0,0],
                 scale = [1,1,1],
                 hide = False,
                 nullTransform = False
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

        if self.customShape:
            self.shape = ""



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
                            hide = self.hide).ctl
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
        self.gimbal_shape = misc.getShape(self.gimbal_ctl)
        if self.gimbal == True:
            misc.tag_gimbal(self.gimbal_shape)
        misc.tag_control(misc.getShape(self.ctl))
        # gimbal shape
        cmds.addAttr(self.ctl, ln = "gimbal", at = "message")
        cmds.connectAttr(self.gimbal_shape + ".message", self.ctl + ".gimbal")

    def __create(self):
        ""
        self.__check()
        self.__create_buffer()
        self.__create_ctl()
        self.__create_secondary()
        self.__create_gimbal()
        self.__make_gimbal_vis()
        self.add_tags()

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
