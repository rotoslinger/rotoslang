import inspect
from collections import OrderedDict
from maya import cmds
from rig_2.root import hierarchy as rig_hierarchy
from rig_2.node import utils as node_utils
from rig_2.misc import utils as misc_utils
from rig_2.attr import utils as attr_utils
from rig_2.tag import utils as tag_utils
from rig_2.attr import constants as attr_constants
from rig.utils import misc
import importlib


importlib.reload(rig_hierarchy)
importlib.reload(node_utils)
importlib.reload(misc_utils)
importlib.reload(attr_utils)
importlib.reload(tag_utils)
importlib.reload(attr_constants)
importlib.reload(misc)



class Component(object):
    def __init__(self,
                 parent_component_class=None,
                 geo_hier_name="C_geo_GRP",
                #  class_name=None,
                 component_name="subcomponent",
                 godnode_class=None,
                 container="",
                 side="C",
                 suffix = "SUBCPT",
                 debug = False,
                 parent = "",
                 create_geo_grp=False,
                 create_skelton_grp=False,
                 create_rig_grp=False,
                 create_control_grp=False,
                 arg_dict=None,
                 hide_on_build=False,
                 is_guide_class=False,
                 input_driver="",
                 output_driven="",
                 control_driver="",
                 # Should change this default, but it is good for the short term ;)
                 input_anchor_name="face_input"
                 ):
        # Arg Snapshot
        # class_name = self.get_relative_path()
        self.ordered_args = OrderedDict()
        # self.component_hier_inputs = OrderedDict()
        self.frame = inspect.currentframe()
        self.get_args()
        # Args
        self.parent_component_class = parent_component_class
        self.geo_hier_name = geo_hier_name
        self.component_name = component_name
        self.godnode_class = godnode_class
        self.side = side
        self.suffix = suffix
        self.debug = debug
        self.parent = parent
        self.create_geo_grp = create_geo_grp
        self.create_skelton_grp = create_skelton_grp
        self.create_rig_grp = create_rig_grp
        self.create_control_grp = create_control_grp
        self.arg_dict = arg_dict
        self.hide_on_build = hide_on_build
        self.is_guide_class = is_guide_class
        self.input_driver = input_driver
        self.output_driven = output_driven
        self.control_driver = control_driver
        self.input_anchor_name = input_anchor_name
        
        self.container = container

        # vars
        self.geo = None
        self.skeleton = None
        self.rig = None
        self.control_parent = None
        self.nodes_to_lock = []
        self.nodes_to_hide = []
        self.nodes_to_cleanup = []
        self.inputs = {}
        self.outputs = {}
        self.input_names = []
        self.output_names = []
        self.subcomponents = []
        self.container_attrs = []
        self.container_nodes = []
        self.subcomponent_group=None
        self.component_membership_nodes=[]
        self.controls = []
        self.guides = []
        # if parent is a dictionary get the value of the first key
        if type(self.parent) == dict:
            self.parent = self.parent[list(self.parent.keys())[0]]

        # these need to happen when the class is initialized
        if self.arg_dict:
            self.get_arg_attrs_from_dict()
        self.initialize()
        self.get_container()
        # These are the nodes that will be constrained to the input anchor
        self.input_anchor_nodes =[]

    def get_relative_path(self):
        module = self.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return self.__class__.__name__  # Avoid reporting __builtin__
        else:
            return module + '.' + self.__class__.__name__


    def get_args(self):
        args, dummy, dummy, arg_dict = inspect.getargvalues(self.frame)
        # make sure self is always ordered first
        self.ordered_args["self"] = arg_dict["self"]
        for key in args:
            if key == "self":
                continue
            self.ordered_args[key] = arg_dict[key]

    def initialize(self):
        """ Check for a root, create if none """
        self.class_node = "{0}_CLASS".format(self.component_name)
        # This is for readability, can be removed maybe...
        self.class_node_name = self.class_node
        
        hierarchy_class = self.parent_component_class
        
        
        self.hierarchy_class = rig_hierarchy.base()
        self.hierarchy_class.initialize()

        if not cmds.objExists(self.hierarchy_class.root):
            self.hierarchy_class.create()
            if cmds.objExists(self.geo_hier_name):
                cmds.parent(self.geo_hier_name, self.hierarchy_class.geo)
        self.input_anchor = node_utils.get_node_agnostic("transform", name=self.input_anchor_name, parent=self.hierarchy_class.input)
        hierarchy_class = self.hierarchy_class
        self.create_class_node(parent=self.hierarchy_class.component)
        self.subcomponent_group = self.class_node
            
        # Tag
        # if self.group_under_subcomponent:
            
        #Create component Hierarchy within the parent class hierarchy. 
        self.geo, self.skeleton, self.rig, self.control_parent, self.input, self.output, self.component = rig_hierarchy.init_hierarchy(
                                                                                                             name=self.component_name,
                                                                                                             suffix=self.suffix,
                                                                                                             subcomponent_group=self.subcomponent_group,
                                                                                                             hierarchy_class=hierarchy_class)
        
        self.geo_input = self.geo
        self.skeleton_input = self.skeleton
        self.rig_input = self.rig
        self.control_parent_input = self.control_parent
        self.component_input = self.component
        
        # if self.do_component_hier_inputs:
        #     self.component_hier_inputs["geo_input"] = ""
        #     self.component_hier_inputs["skeleton_input"] = ""
        #     self.component_hier_inputs["rig_input"] = ""
        #     self.component_hier_inputs["control_parent_input"] = ""
        #     self.component_hier_inputs["component_input"] = ""
        #     self.create_arg_attrs_agnostic(self.component_hier_inputs)

    def create_class_node(self, parent=None):
        node_utils.get_node_agnostic("transform", name = self.class_node, parent=parent)
        # clean up your CLASS node
        misc.lock_attrs(node=self.class_node)
        cmds.setAttr(self.class_node + ".v", channelBox=False, k=False)
        # This is the only node that will never connect to the component_class, and that is because it is the component class
        tag_utils.create_component_tag(self.class_node, self.component_name, connect_to_class_node=False)
        tag_utils.tag_arg_node(self.class_node)
        self.nodes_message_attrr = attr_utils.get_attr(self.class_node, "membership_nodes", attrType="message")
        if self.is_guide_class:
            tag_utils.tag_guide_class(self.class_node)

    def get_arg_attrs_from_dict(self):
        for key, val in list(self.arg_dict.items()):
            setattr(self, key, val)

    def create_arg_attrs(self):
        self.arg_attrs = []
        for key, val in list(self.ordered_args.items()):
            if type(val) == str:
                val=str(val)
            attr_type = type(val)
            self.arg_attrs.append(attr_utils.get_attr_from_arg(node=self.class_node, attr_name=key, attr_type=attr_type, attr_default=val))

    def create_arg_attrs_agnostic(self, agnostic_arg_dict):
        self.arg_attrs = []
        for key, val in list(agnostic_arg_dict.items()):
            if type(val) == str:
                val=str(val)
            attr_type = type(val)
            self.arg_attrs.append(attr_utils.get_attr_from_arg(node=self.class_node, attr_name=key, attr_type=attr_type, attr_default=val))


    def get_container(self):
        if not self.container:
            return
        if not cmds.objExists(self.container):
            self.container = cmds.container(n=self.container)

    def get_ctrls(self):
        """ If controls don't exist yet, create them, otherwise just instantiate """
        return

    def get_nodes(self):
        return

    def get_attrs(self):
        return

    def set_defaults(self):
        return

    def create_inputs(self):
        return
    
    def create_outputs(self):
        return

    def get_subcomponent_inputs(self):
        for subcomponent in self.subcomponents:
            for key, val in subcomponent.inputs.items():
                self.inputs[key] = val

    def get_subcomponent_outputs(self):
        # self.outputs = []
        for subcomponent in self.subcomponents:
            for key, val in subcomponent.outputs.items():
                self.outputs[key] = val

    def finalize_input_output(self):
        self.input_names = [x for x in list(self.inputs.keys())]
        self.output_names = [x for x in list(self.outputs.keys())]

    def set_up_message_network(self):
        return
        for input, input_node in self.inputs.items():
            attr_name = input
            full_attr_name = self.class_node + "." + attr_name
            cmds.addAttr(self.class_node, ln = attr_name, at = "message")
            cmds.connectAttr(input_node + ".message", full_attr_name)

    def connect_nodes(self):
        # THIS IS A VERY TEMP TEST, the final input output connection should be much more customizable.
        # I reccommend doing all constraints and connections very specifically, and avoid generalized connections like this
        # Also would like to avoid massive super complicated dictionaries of connections and connection types excetera
        # but I recognize that might be needed for simplifying certain things... I would just like to avoid complications early......
        if self.input_driver:
            cmds.parentConstraint(self.input_driver, self.input, mo=True)
            cmds.scaleConstraint(self.input_driver, self.input, mo=True)
        if self.output_driven:
            cmds.parentConstraint(self.output, self.output_driven, mo=True)
            cmds.scaleConstraint(self.output, self.output_driven, mo=True)
        if self.control_driver:
            cmds.parentConstraint(self.control_driver, self.control_parent, mo=True)
            cmds.scaleConstraint(self.control_driver, self.control_parent, mo=True)
        for node in self.input_anchor_nodes:
            cmds.parentConstraint(self.input_anchor, node, mo=True)
            cmds.scaleConstraint(self.input_anchor, node, mo=True)
            
            
    def organize_container(self):
        return


    ############ Cleanup type finalize things start here #############
    def hide_nodes(self):
        if not self.nodes_to_hide or self.debug:
            return
        for node in self.nodes_to_hide:
            cmds.setAttr(node + ".v", 0)

    def lock_nodes(self):
        if not self.nodes_to_lock or self.debug:
            return
        lock_nodes(self.nodes_to_lock)

    def cleanup_nodes(self):
        if not self.nodes_to_cleanup or self.debug:
            return
        cleanup_nodes(self.nodes_to_cleanup)

    def add_container_attrs(self):
        if not self.container_attrs or not self.container:
            return
        add_attrs_to_container(self.container, self.container_attrs)

    def add_container_nodes(self):
        if not self.container_nodes or not self.container:
            return
        add_nodes_to_container(self.container, self.container_nodes)

    def post_create(self):
        if self.hide_on_build:
            cmds.setAttr(self.class_node + ".v", 0)

    def create_component_tag(self):
        [tag_utils.create_component_tag(node, component_name=self.component_name) for node in self.component_membership_nodes]

    def create(self):
        self.create_arg_attrs()
        self.get_ctrls()
        self.get_nodes()
        self.get_attrs()
        self.set_defaults()
        self.create_inputs()
        self.create_outputs()
        self.get_subcomponent_inputs()
        self.get_subcomponent_outputs()
        self.finalize_input_output()
        self.set_up_message_network()
        self.connect_nodes()
        self.organize_container()
        self.hide_nodes()
        self.lock_nodes()
        self.cleanup_nodes()
        self.add_container_attrs()
        self.add_container_nodes()
        self.post_create()
        self.create_component_tag()

    # misc methods

    def safe_append(self, node_to_add, list_to_append):
        if type(node_to_add) != list:
            node_to_add = [node_to_add]

        for node in node_to_add:
            if node in list_to_append:
                continue
            list_to_append.append(node)

    def add_node_to_hide(self, node_to_add):
        self.safe_append(node_to_add=node_to_add,
                         list_to_append=self.nodes_to_hide)

            
    def add_node_to_lock(self, node_to_add):
        self.safe_append(node_to_add=node_to_add,
                         list_to_append=self.nodes_to_lock)

    def add_node_to_cleanup(self, node_to_add):
        self.safe_append(node_to_add=node_to_add,
                         list_to_append=self.nodes_to_cleanup)

    def add_to_container_attrs(self, attr_to_add):
        self.safe_append(node_to_add=attr_to_add,
                         list_to_append=self.container_attrs)

    def add_to_container_nodes(self, node_to_add):
        self.safe_append(node_to_add=node_to_add,
                         list_to_append=self.container_nodes)

    def get_controls_guides_etc(self):
        self.controls=tag_utils.get_all_in_component_with_tag("CONTROL", self.component_name)
        self.guides=tag_utils.get_all_in_component_with_tag("GUIDE", self.component_name)


def get_all_component_args():
    all_arg_dicts = {}
    names = tag_utils.get_all_component_names()
    for name in names:
        component_dict = get_component_args_from_scene(component_name=name)
        if not component_dict:
            continue
        all_arg_dicts[name] =component_dict
    return all_arg_dicts

def get_component_args_from_scene(component_name):
    node = tag_utils.get_arg_node_by_component_name(component_name)
    if not node:
        return
    attrs = cmds.listAttr(node, userDefined=True)
    # Remove tags and message attrs
    attrs = [x for x in attrs if not x.isupper() and not cmds.addAttr(node + "." + x, q=True, attributeType=True) == "message"]
    arg_dict = {}
    for attr in attrs:
        full_attr_name = node + "." + attr
        attr_type = cmds.addAttr(node + "." + attr, q=True, attributeType=True)
        val = cmds.getAttr(full_attr_name)
        if type(val) == str:
            val = str(val)
        arg_dict[str(attr)] = val
    return arg_dict

class Container(object):
    def __init__(self,
                 component_class,
                 side="C",
                 name="container",
                 suffix = "CTNR",
                 ):
        self.component_class = component_class
        self.side = side
        self.name = name
        self.suffix = suffix
        pass


def lock_nodes(nodes_to_lock):
    # Right now is adding cleaned up attributes to the channel box for easy debug....
    for node in nodes_to_lock:
        cmds.setAttr(node + ".overrideDisplayType",
                        2,
                        keyable = False, 
                        channelBox = True,
                        )
        cmds.setAttr(node + ".template",
                        1,
                        keyable = False, 
                        channelBox = True,
                        )
        cmds.setAttr(node + ".ihi", 0)

def cleanup_nodes(nodes_to_cleanup):
    for node in nodes_to_cleanup:
        cmds.setAttr(node + ".ihi", 1)

def add_nodes_to_container(container, nodes):
    for node in nodes:
        node_list = cmds.container(container, q=True, nodeList=True)
        if not node_list or node_list and node not in node_list:
            cmds.container(container, e=True, addNode=node)

def add_attrs_to_container(container, attrs):
    for attr in attrs:
        # make sure the node is in the container
        node = attr.split(".")[0]
        attr_name = attr.split(".")[1]
        node_list = cmds.container(container, q=True, nodeList=True)
        if not node_list or node_list and node not in node_list:
            cmds.container(container, e=True, addNode=node)
        
        # TODO need to add a check here to make sure the publish name is unique....

        cmds.container(container, e=True, publishName=attr_name)
        cmds.container(container, e=True, bindAttr=[attr, attr_name])
        

