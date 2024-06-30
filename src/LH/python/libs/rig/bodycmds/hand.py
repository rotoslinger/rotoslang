import sys
linux = '/corp/projects/eng/lharrison/workspace/levi_harrison_test'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "mac" in os:
    os = mac
if os not in sys.path:
    sys.path.append(os)

from maya import cmds
import maya.OpenMaya as OpenMaya


#===============================================================================
#CLASS:         hand_rig
#DESCRIPTION:   names and creates the hand rig
#USAGE:         select hand controls and run
#REQUIRES:      maya.cmds, maya.OpenMaya
#AUTHOR:        Levi Harrison
#DATE:          Nov 9th, 2016
#Version        1.0.0
#===============================================================================

class hand_rig():
    def __init__(self):

        #---vars
        self.ctl                      = ""
        self.root                     = ""
        self.side                     = ""
        self.forward_vector           = OpenMaya.MVector(0,0,0)
        self.num_digits               = 0
        self.names                    = []
        self.finger_knuckle_names     = ["Meta",
                                         "Base",
                                         "Mid",
                                         "Tip",
                                         "End"]
        self.thumb_knuckle_names      = ["Meta",
                                         "Base",
                                         "Tip",
                                         "End"]
        self.raw_digits               = []
        self.root_digits              = []
        self.has_meta                 = []
        self.metacarpals              = []
        self.thumb                    = []
        self.index                    = []
        self.middle                   = []
        self.ring                     = []
        self.pinky                    = []
        
        
        
        
        
        self.__create()

    def __check_selection(self):
        """finds the hand root joint does basic checks"""
        
        self.ctl = cmds.ls(selection = True,
                           type = "joint")
        if not self.ctl:
            raise Exception("please select the hand control and run hand" 
                            + " script again")
            quit()
            
        if len(self.ctl) > 1:
            raise Exception("you have selected multiple objects, please" 
                            + " select only the hand control and run script"
                            + " again")
            quit()
            
        self.ctl = self.ctl[0]
        
        #assumes that the controller is only connected to the root
        self.root = cmds.listConnections(self.ctl,
                                        type="joint",
                                        destination=True,
                                        source=False)
        if not self.root:
            raise Exception(self.ctl 
                            + " is not connected to a joint please check"
                            + " selection and run hand script again")
            quit()
            
        self.root = self.root[0]

    def __check_side(self):
        """determine whether the hand is left or right"""
        #---Check one: get world X location of hand control
        trans_tuple = cmds.xform(self.ctl,
                                 query = True,
                                 translation = True, 
                                 worldSpace = True)[0]
        
        if trans_tuple > 0:
            self.side = "Left"
            print("rigging left hand")
            
        if trans_tuple < 0:
            self.side = "Right"
            print("rigging right hand")
                        
        #---Check two: check naming convention & for non unique names
        simple_name = self.ctl.split("|")
        if len(simple_name) > 1:
            simple_name = simple_name[len(simple_name)-1]
            side_string = simple_name.split("_")
            print("Warning: your control is not using a unique name")
        else:
            side_string = self.ctl.split("_")
        
        if not side_string:
            raise Exception("your control has not been properly named "
                            + "please use the naming standard: Side_name_TYPE "
                            + "for example, Right_wrist_CTRL")
            quit()
        
        side_string = side_string[0]
        
        if side_string != "Left" and side_string != "Right":
            raise Exception("your control has not been properly named "
                            + "please use the naming standard: Side_name_TYPE"
                            + "for example, Right_wrist_CTRL")
            quit()
            
        if side_string != self.side:
            raise Exception("your control has been named for the "
                            + side_string
                            + " side but it is on the "
                            + self.side
                            + " side")
            
            quit()
        
    def __get_hand_forward_vector(self):
        """ use vector math to sort fingers """
        #get CTRL forward vector, assumes orientation will always be z forward
        trans = cmds.createNode("transform",
                                name = "forward_vector_node")
        tmp_con = cmds.parentConstraint(self.ctl, trans)
        cmds.delete(tmp_con)
        
        relative_trans = cmds.xform(trans,
                                    query = True,
                                    translation = True, 
                                    objectSpace = True)
        new_trans = relative_trans[0], relative_trans[1], relative_trans[2]+100, 
        cmds.xform(trans,
                   translation = new_trans, 
                   objectSpace = True,
                   )
        tmp_vector = cmds.xform(trans,
                                query = True,
                                translation = True, 
                                worldSpace = True)

        self.forward_vector = OpenMaya.MVector(tmp_vector[0],
                                               tmp_vector[1],
                                               tmp_vector[2])
        cmds.delete(trans)

    def __rig_fingers(self):
        """"""
        #determine how many fingers
        self.raw_digits = cmds.listRelatives(self.root,
                                              type = "joint",
                                              children = True,
                                              parent = False
                                              )
        self.num_digits = len(self.raw_digits)
        
        if self.num_digits == 5:
            self.names = ["thumb",
                          "indexFinger",
                          "middleFinger",
                          "ringFinger",
                          "pinkyFinger"]
            print("creating five digit rig")
            
        if self.num_digits == 4:
            self.names = ["thumb",
                          "indexFinger",
                          "middleFinger",
                          "pinkyFinger"]
            print("creating four digit rig")
            
        if self.num_digits == 3:
            self.names = ["thumb",
                          "indexFinger",
                          "pinkyFinger"]
            print("creating three digit rig")
            
        if self.num_digits == 2:
            self.names = ["thumb",
                          "indexFinger"]
            print("creating two digit rig")
        
        
        #---set divider for readability
        cmds.addAttr(self.ctl, ln = "___", at = "enum", en = "___:")
        attr_name = self.ctl + "." + "___"
        cmds.setAttr(attr_name, e = True, keyable = True, lock = True)

        
        #---get thumb
        self.thumb = self.__shortest_len(vector = self.forward_vector,
                                         joints = self.raw_digits)
        self.thumb, self.has_meta= self.__get_knuckles(digit = self.thumb,
                                                        has_meta = self.has_meta,
                                                        num_knuck_meta = 4)
        self.__name_fingers(digit = self.thumb,
                            name = "thumb",
                            thumb = True,
                            has_meta = self.has_meta[len(self.has_meta)-1]
                            )
        self.root_digits.append(self.thumb[0])
        self.__orient_bones_array(up_vector_ctl = self.ctl,
                                  joints = self.thumb,
                                  is_thumb = True,
                                  is_meta = self.has_meta[len(self.has_meta)-1]
                                  )       
        self.__add_attrs(name = "thumb",
                         ctl = self.ctl,
                         is_meta = self.has_meta[len(self.has_meta)-1],
                         thumb = True,
                         joints = self.thumb)


        #---set divider for readability
        cmds.addAttr(self.ctl, ln = "____", at = "enum", en = "____:")
        attr_name = self.ctl + "." + "____"
        cmds.setAttr(attr_name, e = True, keyable = True, lock = True)

         
         #---get index finger
        self.index = self.__shortest_len(vector = self.forward_vector,
                                         joints = self.raw_digits)
        self.index, self.has_meta = self.__get_knuckles(digit = self.index,
                                                       has_meta = self.has_meta,
                                                       num_knuck_meta = 5)
        self.__name_fingers(digit = self.index,
                            name = "index",
                            thumb = False,
                            has_meta = self.has_meta[len(self.has_meta)-1]
                            )
        self.root_digits.append(self.index[0])
        self.__orient_bones_array(up_vector_ctl = self.ctl,
                                  joints = self.index,
                                  is_thumb = False,
                                  is_meta = self.has_meta[len(self.has_meta)-1]
                                  )    
        
        self.__add_attrs(name = "index",
                         ctl = self.ctl,
                         is_meta = self.has_meta[len(self.has_meta)-1],
                         thumb = False,
                         joints = self.index)
        

        
        #---get middle finger
        if self.num_digits == 5 or self.num_digits == 4:
            #---set divider for readability
            cmds.addAttr(self.ctl, ln = "_____", at = "enum", en = "_____:")
            attr_name = self.ctl + "." + "_____"
            cmds.setAttr(attr_name, e = True, keyable = True, lock = True)
            
            
            self.middle = self.__shortest_len(vector = self.forward_vector,
                                              joints = self.raw_digits)
            self.middle, self.has_meta = self.__get_knuckles(digit = self.middle,
                                                             has_meta = self.has_meta,
                                                             num_knuck_meta = 5)
            self.__name_fingers(digit = self.middle,
                                name = "middle",
                                thumb = False,
                                has_meta = self.has_meta[len(self.has_meta)-1]
                                )
            self.root_digits.append(self.middle[0])
            self.__orient_bones_array(up_vector_ctl = self.ctl,
                                      joints = self.middle,
                                      is_thumb = False,
                                      is_meta = self.has_meta[len(self.has_meta)-1]
                                      )
            self.__add_attrs(name = "middle",
                             ctl = self.ctl,
                             is_meta = self.has_meta[len(self.has_meta)-1],
                             thumb = False,
                             joints = self.middle)
                 
        #---get ring finger
        if self.num_digits == 5:
            #---set divider for readability
            cmds.addAttr(self.ctl, ln = "______", at = "enum", en = "______:")
            attr_name = self.ctl + "." + "______"
            cmds.setAttr(attr_name, e = True, keyable = True, lock = True)

            self.ring = self.__shortest_len(vector = self.forward_vector,
                                            joints = self.raw_digits)
            self.ring, self.has_meta = self.__get_knuckles(digit = self.ring,
                                                           has_meta = self.has_meta,
                                                           num_knuck_meta = 5)
            self.__name_fingers(digit = self.ring,
                                name = "ring",
                                thumb = False,
                                has_meta = self.has_meta[len(self.has_meta)-1]
                                )
            self.root_digits.append(self.ring[0])
            self.__orient_bones_array(up_vector_ctl = self.ctl,
                                      joints = self.ring,
                                      is_thumb = False,
                                      is_meta = self.has_meta[len(self.has_meta)-1]
                                      )  
            
            self.__add_attrs(name = "ring",
                             ctl = self.ctl,
                             is_meta = self.has_meta[len(self.has_meta)-1],
                             thumb = False,
                             joints = self.ring)

        #---get pinky finger
        if self.num_digits == 5 or self.num_digits == 4 or self.num_digits == 3:
            #---set divider for readability
            cmds.addAttr(self.ctl, ln = "_______", at = "enum", en = "_______:")
            attr_name = self.ctl + "." + "_______"
            cmds.setAttr(attr_name, e = True, keyable = True, lock = True)

            self.pinky = self.__shortest_len(vector = self.forward_vector,
                                             joints = self.raw_digits)
            self.pinky, self.has_meta = self.__get_knuckles(digit = self.pinky,
                                                            has_meta = self.has_meta,
                                                            num_knuck_meta = 5)
            self.__name_fingers(digit = self.pinky,
                                name = "pinky",
                                thumb = False,
                                has_meta = self.has_meta[len(self.has_meta)-1]
                                )
            self.root_digits.append(self.pinky[0])
            self.__orient_bones_array(up_vector_ctl = self.ctl,
                                      joints = self.pinky,
                                      is_thumb = False,
                                      is_meta = self.has_meta[len(self.has_meta)-1]
                                      )       
            self.__add_attrs(name = "pinky",
                             ctl = self.ctl,
                             is_meta = self.has_meta[len(self.has_meta)-1],
                             thumb = False,
                             joints = self.pinky)
                    
                    
    def __add_attrs(self,
                    name = "",
                    ctl = "",
                    is_meta = False,
                    thumb = False,
                    joints = []):
        attrs = []
        if not thumb:
            attr_names = ["Base",
                          "Mid",
                          "Tip",
                          "Spread",
                          "Stretch",
                          "Twist"
                          ]
            trans_attrs = ["rz",
                           "rz",
                           "rz",
                           "ry",
                           "tx",
                           "rx"]
            indexes = [0,
                       1,
                       2,
                       0,
                       0,
                       0]
            stretch = [1,2,3]
        if is_meta and not thumb:
            attr_names = attr_names + ["Cup"]
            trans_attrs = trans_attrs + ["rx"]
            indexes = [1,
                       2,
                       3,
                       1,
                       1,
                       1,
                       0]
            stretch = [2,3,4]
        if thumb:
            attr_names = ["Base",
                          "Tip",
                          "Spread",
                          "Stretch",
                          "Twist"
                          ]
            trans_attrs = ["rz",
                           "rz",
                           "ry",
                           "tx",
                           "rx"]
            indexes = [0,
                       1,
                       0,
                       0,
                       0]
            stretch = [1,2]
        if is_meta and thumb:
            attr_names = attr_names + ["Cup"]
            trans_attrs = trans_attrs + ["rx"]
            indexes = [1,
                       2,
                       1,
                       1,
                       1,
                       0]
            stretch = [2,3]
            
        for i in range(len(attr_names)):
            cmds.addAttr(self.ctl, ln = name + attr_names[i], at = "float", 
                         dv = 0)
            attrs.append(self.ctl + "." + name + attr_names[i])
            cmds.setAttr(attrs[i], k = True, cb = False)

            #---cup
            if (attr_names[i] == "Cup"):
                if (name == "ring" or name == "pinky"):
                    mlt = cmds.createNode("multiplyDivide", name = (self.side
                                                             + "_"
                                                             + name
                                                             + attr_names[i]
                                                             + "Jnt"
                                                             + "_MLT"))
                    cmds.setAttr(mlt + ".input2X", -1)
                    
                    
                    cmds.connectAttr(attrs[i], mlt + ".input1X")
                    cmds.connectAttr(mlt + ".outputX", (joints[indexes[i]] 
                                                        + "." 
                                                        + trans_attrs[i]))
                if ((name != "ring" and name != "pinky")):
                    cmds.connectAttr(attrs[i], (joints[indexes[i]] 
                                                + "." 
                                                + trans_attrs[i]))
                    
            elif thumb and attr_names[i] == "Base":
                # needs to connect thumb base with spread
                if is_meta:
                    cmds.connectAttr(attrs[i], (joints[indexes[i]] 
                                                + "." 
                                                + trans_attrs[i]))
                else:
                    thumb_pma = cmds.createNode("plusMinusAverage", 
                                                name = (self.side
                                                        + "_"
                                                        + name
                                                        + attr_names[i]
                                                        + "Jnt"
                                                        + "_PMA"))
                    cmds.connectAttr (attrs[i], 
                                      thumb_pma + ".input3D[1].input3Dx")
                    cmds.connectAttr(thumb_pma + ".output3Dx", 
                                     joints[indexes[i]] 
                                     + "." 
                                     + trans_attrs[i])
                    
            #---spread
            elif (attr_names[i] == "Spread"):
                if (name == "thumb"):
                    mlt = cmds.createNode("multiplyDivide", name = (self.side
                                                             + "_"
                                                             + name
                                                             + attr_names[i]
                                                             + "Jnt"
                                                             + "_MLT"))
                    if self.side == "Right":
                        mult_val = 1
                    if self.side == "Left":
                        mult_val = -1
                        
                    cmds.setAttr(mlt + ".input2X", mult_val)
                    cmds.connectAttr(attrs[i], mlt + ".input1X")
                    if is_meta:
                        base_spread_joint = joints[0]
                        spread_attr = ".ry"
                        cmds.connectAttr(mlt + ".outputX", (base_spread_joint 
                                                            + spread_attr))
                    else:
                        base_spread_joint = joints[indexes[i]]
                        spread_attr = ".rz"
                        cmds.connectAttr (mlt + ".outputX", 
                                          thumb_pma + ".input3D[0].input3Dx")
                    
                elif (name == "index"):
                    cmds.connectAttr(attrs[i], (joints[indexes[i]] 
                                                + "." 
                                                + trans_attrs[i]))

                elif (name == "middle"):
                    mlt = cmds.createNode("multiplyDivide", name = (self.side
                                                             + "_"
                                                             + name
                                                             + attr_names[i]
                                                             + "Jnt"
                                                             + "_MLT"))
                    
                    if self.num_digits == 5:
                        mult_val = .45
                    if self.num_digits == 4:
                        mult_val = -.2
                    
                    cmds.setAttr(mlt + ".input2X", mult_val)
                    
                    
                    cmds.connectAttr(attrs[i], mlt + ".input1X")
                    cmds.connectAttr(mlt + ".outputX", (joints[indexes[i]] 
                                                        + "." 
                                                        + trans_attrs[i]))

                elif (name == "ring"):
                    mlt = cmds.createNode("multiplyDivide", name = (self.side
                                                             + "_"
                                                             + name
                                                             + attr_names[i]
                                                             + "Jnt"
                                                             + "_MLT"))
                    cmds.setAttr(mlt + ".input2X", -.45)
                    
                    
                    cmds.connectAttr(attrs[i], mlt + ".input1X")
                    cmds.connectAttr(mlt + ".outputX", (joints[indexes[i]] 
                                                        + "." 
                                                        + trans_attrs[i]))

                elif (name == "pinky"):
                    mlt = cmds.createNode("multiplyDivide", name = (self.side
                                                             + "_"
                                                             + name
                                                             + attr_names[i]
                                                             + "Jnt"
                                                             + "_MLT"))
                    cmds.setAttr(mlt + ".input2X", -1)
                    
                    
                    cmds.connectAttr(attrs[i], mlt + ".input1X")
                    cmds.connectAttr(mlt + ".outputX", (joints[indexes[i]] 
                                                        + "." 
                                                        + trans_attrs[i]))

            #---stretch
            elif (attr_names[i] == "Stretch"):
                for x in range(len(stretch)):
                    pma = cmds.createNode("plusMinusAverage", 
                                          name = (self.side
                                          + "_"
                                          + name
                                          + attr_names[i]
                                          + "Jnt"
                                          + str(x)
                                          + "_PMA"))
                    trans = cmds.getAttr(joints[stretch[x]] + ".translate")[0]
                    cmds.setAttr(pma + ".input3D[0].input3Dx",trans[0])
                    cmds.setAttr(pma + ".input3D[0].input3Dy",trans[1])
                    cmds.setAttr(pma + ".input3D[0].input3Dz",trans[2])
                    
                    if self.side == "Left":
                        cmds.connectAttr(attrs[i], pma + ".input3D[1].input3Dx")
                    if self.side == "Right":
                        mlt = cmds.createNode("multiplyDivide", name = (self.side
                                                                 + "_"
                                                                 + name
                                                                 + attr_names[i]
                                                                 + "Jnt"
                                                                 + str(x)
                                                                 + "_MLT"))
                        cmds.connectAttr(attrs[i], mlt + ".input1X")
                        cmds.setAttr(mlt + ".input2X", -1)
                        cmds.connectAttr(mlt + ".outputX", pma + ".input3D[1].input3Dx")
                    
                    cmds.connectAttr(pma + ".output3D",
                                     joints[stretch[x]] + ".translate")
            else:
                cmds.connectAttr(attrs[i], (joints[indexes[i]] 
                                            + "." 
                                            + trans_attrs[i]))
                    
                    
                    
                    
                    
                    
    def __orient_bones(self,
                       up_vector_ctl,
                       joint,
                       is_thumb = False,
                       is_meta = False):
        """ Orients a joint based on a nodes YAxis"""
        child_jnt = cmds.listRelatives(joint,
                                       children = True,
                                       parent = False,
                                       type = "joint")
        #---if a tip joint copy the parent orientation
        if child_jnt and is_meta:
                tmp_piv = cmds.createNode("transform")
                cmds.parent (child_jnt, tmp_piv)
                orient = cmds.xform(self.ctl,
                                    query = True,
                                    rotateAxis = True, 
                                    absolute = True)

                if self.side == "Left":
                    offset = [0,180,0]
                if self.side == "Right":
                    offset = [0,0,0]
                tmp_con = cmds.orientConstraint(self.ctl,
                                                joint,
                                                offset = offset
                                                )
                cmds.delete(tmp_con)
                cmds.makeIdentity(joint,
                                  apply = True,
                                  t=0,
                                  r=1,
                                  s = 1,
                                  n=0,
                                  pn=1)
                cmds.parent (child_jnt, joint)
                cmds.delete(tmp_piv)
        else:
            if not child_jnt:
                parent_jnt = cmds.listRelatives(joint,
                                                children = False,
                                                parent = True,
                                                type = "joint")[0]
                orient = cmds.xform(parent_jnt,
                                            query = True,
                                            rotateAxis = True, 
                                            absolute = True)
                cmds.joint(joint,
                           edit = True,
                           orientation = orient)
            else:
                tmp_piv = cmds.createNode("transform")
                tmp_trans = cmds.createNode("transform")
                tmp_con = cmds.pointConstraint(joint, tmp_trans)
                cmds.delete(tmp_con)
                tmp_con = cmds.orientConstraint(up_vector_ctl, tmp_trans)
                cmds.delete(tmp_con)
                relative_trans = cmds.xform(tmp_trans,
                                            query = True,
                                            translation = True, 
                                            objectSpace = True)
                new_trans = relative_trans[0], relative_trans[1]+10, relative_trans[2], 
                cmds.xform(tmp_trans,
                           translation = new_trans, 
                           objectSpace = True,
                           )
                cmds.parent(child_jnt, tmp_piv)
                if self.side == "Right":
                    aim_vector = [-1,0,0]
                    up_vector = [0,1,0]
                if self.side == "Left":
                    aim_vector = [1,0,0]
                    up_vector = [0,-1,0]
                if is_thumb and self.side == "Right":
                    up_vector = [0,0,-1]
                    
                if is_thumb and self.side == "Left":
                    up_vector = [0,0,1]

                tmp_con = cmds.aimConstraint(child_jnt,
                                             joint,
                                             aimVector = aim_vector,
                                             upVector = up_vector,
                                             worldUpType = "object",
                                             worldUpObject = tmp_trans)
                cmds.delete(tmp_con)
                cmds.parent(child_jnt, joint)
                cmds.makeIdentity(joint,
                                  apply = True,
                                  t=0,
                                  r=1,
                                  s = 1,
                                  n=0,
                                  pn=1)
                cmds.delete(tmp_trans,
                            tmp_piv)
            
    def __orient_bones_array(self,
                             up_vector_ctl,
                             joints = [],
                             is_thumb = False,
                             is_meta = False):
        for i in range(len(joints)):
            if is_meta == True and i == 0:
                is_meta = True
            else:
                is_meta = False
            self.__orient_bones(up_vector_ctl = self.ctl,
                                joint = joints[i],
                                is_thumb = is_thumb,
                                is_meta = is_meta)       

    def __name_fingers(self,
                       digit = [],
                       name = "",
                       thumb = False,
                       has_meta = False):
        """names fingers"""
        for x in range(len(digit)):
            if thumb:
                knuck_names = self.thumb_knuckle_names
            else:
                knuck_names = self.finger_knuckle_names
            if has_meta == True:
                idx_fix = 0
            else:
                idx_fix = 1
            tmp_name = (self.side
                        + "_"
                        + name
                        + knuck_names[x + idx_fix]
                        + "_JNT")
            digit[x] = cmds.rename(digit[x], tmp_name)
                
        
    def __shortest_len(self,
                       vector = OpenMaya.MVector(0,0,0),
                       joints = []):
        """find the bone that is the closest to the given point"""
        dist = 10000
        final_joint = ""
        for i in range(len(joints)):
            #make vector
            tmp_vector = cmds.xform(joints[i],
                                    query = True,
                                    translation = True, 
                                    worldSpace = True)
        
            tmp_vector = OpenMaya.MVector(tmp_vector[0],
                                          tmp_vector[1],
                                          tmp_vector[2])
            test_dist = vector - tmp_vector
            test_dist = test_dist.length()
            if test_dist < dist:
                dist = test_dist
                final_joint = joints[i]
        return final_joint

    def __get_knuckles(self,
                       digit = "",
                       has_meta = [],
                       num_knuck_meta = 5):
        """finds the knuckles and determines whether or not metacarpals exist"""
        
        rel = cmds.listRelatives(digit,
                                 type = "joint",
                                 children = True,
                                 allDescendents = True,
                                 parent = False
                                 )
        rel.reverse()
        self.raw_digits.remove(digit)
        digit = [digit] + rel
        if len(digit) == num_knuck_meta-1:
            has_meta.append(False)

        if len(digit) == num_knuck_meta:
            has_meta.append(True)
        return digit, has_meta
    
    def __create(self):
        self.__check_selection()
        self.__check_side()
        self.__get_hand_forward_vector()
        self.__rig_fingers()
hand_rig()
    
