import copy
from maya import cmds
from rig_2.misc import utils as misc_utils

def get_node_agnostic(nodeType, name, parent=None):
    if cmds.objExists(name):
        return name
    return cmds.createNode(nodeType, n=name, p=parent)

def get_node_agnostic_multiple(names=[], nodeType=None,  parent=None):
    retNodes = []
    for name in names:
        retNodes.append(get_node_agnostic(name=name, nodeType=nodeType, parent=parent))
    return retNodes

def get_locator(name, parent=None, return_transform=True, return_shape=False):
    shape_name = name + "Shape"
    transform = get_node_agnostic("transform", name=name, parent=parent)
    shape = get_node_agnostic("locator", name=shape_name, parent=transform)
    if return_transform and return_shape:
        return transform, shape
    if return_transform:
        return transform
    if return_shape:
        return shape

def decompose_matrix(name, matrix_attr, suffix = "_DCM", rotate_order_transform = ""):
    ret_decompose_matrix = get_node_agnostic("decomposeMatrix", name = name + suffix)
    cmds.connectAttr(matrix_attr, ret_decompose_matrix + ".inputMatrix")
    if rotate_order_transform:
        cmds.connectAttr(rotate_order_transform + ".rotateOrder", ret_decompose_matrix + ".inputRotateOrder")
    return ret_decompose_matrix

def mult_matrix(name, matrix_attrs, suffix = "_MTM"):
    ret_mult_matrix = get_node_agnostic("multMatrix", name = name + suffix)
    for idx, attr in enumerate(matrix_attrs):
        cmds.connectAttr(attr, ret_mult_matrix + ".matrixIn[{0}]".format(idx))
    return ret_mult_matrix

def condition(name,
              first_term = 0.0,
              second_term = 0.0,
              operation = 0.0,
              color_if_true_attrs = ["","",""],
              color_if_false_attrs = ["","",""],
              suffix = "_CON"):

    ret_cond_matrix = get_node_agnostic("condition", name = name + suffix)
    
    # If it is a value set it
    if  type(first_term) == float or type(first_term) == int:
        cmds.setAttr(ret_cond_matrix + ".firstTerm", first_term)
    if  type(second_term) == float or type(second_term) == int:
        cmds.setAttr(ret_cond_matrix + ".secondTerm", second_term)

    # If it is an attribute connect it
    if  type(first_term) == unicode:
        cmds.connectAttr(first_term, ret_cond_matrix + ".firstTerm")
    if  type(second_term) == unicode:
        cmds.connectAttr(second_term, ret_cond_matrix + ".secondTerm")

    for idx, color in enumerate(["R", "G", "B"]):
        # If it is a value set it
        if type(color_if_true_attrs[idx]) == float:
            cmds.setAttr(ret_cond_matrix + ".colorIfTrue{0}".format(color), color_if_true_attrs[idx])
        if type(color_if_false_attrs[idx]) == float:
            cmds.setAttr(ret_cond_matrix + ".colorIfFalse{0}".format(color), color_if_false_attrs[idx])

        # If it is an attribute connect it
        if color_if_true_attrs[idx] and type(color_if_true_attrs[idx]) == unicode:
            cmds.connectAttr(color_if_true_attrs[idx], ret_cond_matrix + ".colorIfTrue{0}".format(color))
        if color_if_false_attrs[idx] and type(color_if_false_attrs[idx]) == unicode:
            cmds.connectAttr(color_if_false_attrs[idx], ret_cond_matrix + ".colorIfFalse{0}".format(color))
            

    return ret_cond_matrix


class Buffer(object):
    def __init__(self,
                 maya_dag_node="",
                 side="C",
                 name="buffer",
                 suffix = "BUF",
                 num_buffer = 3
                 ):

        # args
        self.maya_dag_node = maya_dag_node
        self.side = side
        self.name = name
        self.suffix = suffix
        self.num_buffer = num_buffer

        # vars
        self.parent = None
        self.buffers = []
        self.buffers_ascending = []
        self.buffers_parent = []
        self.buffers_curr_parent = ""

        # a direct reference to the buffers, but a more verbose description of how they are ordered for readability
        self.buffers_descending = self.buffers
    

    def create(self):
            "creates extra transforms to parent the ctls under ascending "
            self.parent = misc_utils.get_parent(self.maya_dag_node)
            self.buffers = []
            self.buffers_ascending = []
            self.buffers_parent = []
            self.buffers_curr_parent = copy.deepcopy(self.parent)
            for idx in reversed(range(self.num_buffer)):
                bufferName = "{0}_{1}{2:02}_{3}".format(self.side, self.name, idx, self.suffix)
                self.buffers_curr_parent = get_node_agnostic(name = bufferName, nodeType="transform", parent=self.buffers_curr_parent)
                self.buffers.append(self.buffers_curr_parent)

            self.buffers_ascending = copy.deepcopy(self.buffers)
            self.buffers_ascending.reverse()
            self.buffers_parent =  self.buffers_ascending[0]
            if not misc_utils.get_parent(self.maya_dag_node) == self.buffers_parent:
                cmds.parent(self.maya_dag_node, self.buffers_parent)

    def initialize(self):
        """
        create() is safe enough not to recreate the same nodes, it will still set them to their correct vars if they already exist
        initialize() just gets the nodes from the scene using create()
        initialize() is more human readable, and can be what you use to get the nodes from the scene
        """
        self.create()

def get_parent(mayaObject):
    parent = cmds.listRelatives( mayaObject, parent=True)
    if parent:
        return parent[0]