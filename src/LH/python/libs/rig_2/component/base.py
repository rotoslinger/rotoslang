import inspect
from collections import OrderedDict
from maya import cmds
from rig_2.root import hierarchy as rig_hierarchy
reload(rig_hierarchy)
from rig_2.node import utils as node_utils
reload(node_utils)
from rig_2.misc import utils as misc_utils
reload(misc_utils)
from rig_2.attr import utils as attr_utils
reload(attr_utils)
from rig_2.tag import utils as tag_utils
reload(tag_utils)
from rig_2.attr import constants as attr_constants
reload(attr_constants)
from rig.utils import misc
reload(misc)



class Subcomponent(object):
    def __init__(self,
                 parent_component_class,
                 class_name=None,
                 component_name="base",
                 godnode_class=None,
                 container="",
                 side="C",
                 name="subcomponent",
                 suffix = "SUBCPT",
                 debug = False,
                 parent = "",
                 create_geo_grp=False,
                 create_skelton_grp=False,
                 create_rig_grp=False,
                 create_control_grp=False,
                 create_subcomponent_grp=False,
                 arg_dict=None,
                 # This will make the component the base which means you won't need a parent class
                 # a hierarchy will be created for you (or found if it already exists)
                 is_root=False,
                 ):
        # Arg Snapshot
        class_name = self.get_relative_path()
        self.ordered_args = OrderedDict()
        self.frame = inspect.currentframe()
        self.get_args()
        # Args
        self.parent_component_class = parent_component_class
        self.component_name = component_name
        self.godnode_class = godnode_class
        self.side = side
        self.name = name
        self.suffix = suffix
        self.debug = debug
        self.parent = parent
        self.create_geo_grp = create_geo_grp
        self.create_skelton_grp = create_skelton_grp
        self.create_rig_grp = create_rig_grp
        self.create_control_grp = create_control_grp
        self.create_subcomponent_grp = create_subcomponent_grp
        self.arg_dict = arg_dict
        
        self.container = container
        self.is_root = is_root

        # vars
        self.geo = None
        self.skeleton = None
        self.rig = None
        self.control = None
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

        # if parent is a dictionary get the value of the first key
        if type(self.parent) == dict:
            self.parent = self.parent[self.parent.keys()[0]]

        # these need to happen when the class is initialized
        if self.arg_dict:
            self.get_arg_attrs_from_dict()
        self.initialize()
        self.get_container()

    def get_relative_path(self):
        module = self.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return self.__class__.__name__  # Avoid reporting __builtin__
        else:
            return module + '.' + self.__class__.__name__


    def get_args(self):
        args, dummy, dummy, arg_dict = inspect.getargvalues(self.frame)
        for key in args:
            self.ordered_args[key] = arg_dict[key]


    def initialize(self):
        """ Check for a root, create if none """
        hierarchy_class = self.parent_component_class
        if self.is_root:
            self.hierarchy_class = rig_hierarchy.base()
            self.hierarchy_class.initialize()

            if not cmds.objExists(self.hierarchy_class.root):
                self.hierarchy_class.create()
                
            hierarchy_class = self.hierarchy_class
            
            
        self.aggr = "{0}_{1}Aggr_{2}".format(self.side, self.name, self.suffix)

        # This is for readability, can be removed maybe...
        self.aggr_name = self.aggr
        # Tag
        
        #Create component Hierarchy within the parent class hierarchy. 
        self.geo, self.skeleton, self.rig, self.control, self.component = rig_hierarchy.init_hierarchy(side=self.side,
                                                                                                    name=self.name,
                                                                                                    suffix=self.suffix,
                                                                                                    hierarchy_class=hierarchy_class)
        if not self.is_root:
            # If not base, set the asset structure to be that of the parent class
            self.geo = self.parent_component_class.geo 
            self.skeleton = self.parent_component_class.skeleton 
            self.rig = self.parent_component_class.rig 
            self.control = self.parent_component_class.control 
            self.component = self.parent_component_class.component 
            
        self.rig_geo = "C_{0}_GRP".format(self.component_name)
        node_utils.get_node_agnostic("transform", name = self.rig_geo, parent=self.geo)

        node_utils.get_node_agnostic("transform", name = self.aggr, parent=self.component)
        misc.lock_attrs(node=self.aggr, attr=["all"])
        tag_utils.create_component_tag(self.aggr, self.component_name)
        tag_utils.tag_arg_node(self.aggr)

    def get_arg_attrs_from_dict(self):
        for key, val in self.arg_dict.items():
            setattr(self, key, val)

    def create_arg_attrs(self):
        self.arg_attrs = []
        for key, val in self.ordered_args.items():
            # print key,val, type(val)
            if type(val) == unicode:
                val=str(val)
            if type(val) not in attr_constants.SUPPORTED_TYPES:
                continue
            attr_type = type(val)
            self.arg_attrs.append(attr_utils.get_attr_from_arg(node=self.aggr, attr_name=key, attr_type=attr_type, attr_default=val))

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
            for key, val in subcomponent.inputs.iteritems():
                self.inputs[key] = val

    def get_subcomponent_outputs(self):
        # self.outputs = []
        for subcomponent in self.subcomponents:
            for key, val in subcomponent.outputs.iteritems():
                self.outputs[key] = val

    def finalize_input_output(self):
        self.input_names = [x for x in self.inputs.keys()]
        self.output_names = [x for x in self.outputs.keys()]

    def set_up_message_network(self):
        return
        for input, input_node in self.inputs.iteritems():
            attr_name = input
            full_attr_name = self.aggr + "." + attr_name
            cmds.addAttr(self.aggr, ln = attr_name, at = "message")
            cmds.connectAttr(input_node + ".message", full_attr_name)

    def connect_nodes(self):
        return

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
        return

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

def get_all_component_args():
    all_arg_dicts = {}
    names = tag_utils.get_all_component_names()
    for name in names:
        component_dict = get_component_args_from_scene(component_name=name)
        if not component_dict:
            continue
        all_arg_dicts[name] =component_dict
    return all_arg_dicts
    # print all_arg_dicts

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
        if type(val) == unicode:
            val = str(val)
        arg_dict[str(attr)] = val
    return arg_dict
    
class Builder(Subcomponent):
    def __init__(self,
                 parent_component_class=None,
                 class_name=None,
                 **kw):
        super(Builder, self).__init__(self, class_name=class_name, **kw)
        class_name = self.get_relative_path()
        self.ordered_args = OrderedDict()
        self.frame = inspect.currentframe()
        self.get_args()
        
    def initialize(self):
        
        """ Check for a root, create if none """
        self.hierarchy_class = rig_hierarchy.base()
        self.hierarchy_class.initialize()

        if not cmds.objExists(self.hierarchy_class.root):
            self.hierarchy_class.create()

        self.aggr = "{0}_{1}Aggr_{2}".format(self.side, self.name, self.suffix)

        """
        Create component Hierarchy within the asset hierarchy. 
        These transforms should mirror the asset hierarchy's layout and should be populated based on global scaling needs.
        """

        self.geo, self.skeleton, self.rig, self.control, self.component = rig_hierarchy.init_hierarchy(side=self.side,
                                                                                              name=self.name,
                                                                                              suffix=self.suffix,
                                                                                              hierarchy_class=self.hierarchy_class)
        node_utils.get_node_agnostic("transform", name = self.aggr, parent=self.component)

        tag_utils.create_component_tag(self.component, self.component_name)
        tag_utils.tag_arg_node(self.component)
        
        misc.lock_attrs(node=self.aggr, attr=["all"])



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
        

