from maya import cmds
from rig_2.node import utils as node_utils
from rig_2.misc import utils as misc_utils
import importlib

importlib.reload(misc_utils)
importlib.reload(node_utils)

class base(object):
    """
    Creates root groups for an asset.  Most things will go under subcomponents, but there are root groups for general things.
    The Model will go under geo and if there are any master skeletons, rigs, or controls there are groups for these, but mostly
    everything will end up under the Components group
    """
    
    def __init__(self,
                 asset_name = "asset",
                 ):
        """
        type  asset_name:                string
        param asset_name:                asset name
        """
        #---args
        self.asset_name                   = asset_name
        
        #---vars
        self.suffix                      = "GRP"
        self.groups                      = []

    def initialize(self):
        """ Placeholder for naming node_utils """
        self.root = "{0}_{1}".format(self.asset_name, self.suffix)
        self.geo = "{0}_{1}".format("Geo", self.suffix)
        self.skeleton = "{0}_{1}".format("Skeleton", self.suffix)
        self.rig = "{0}_{1}".format("Rig", self.suffix)
        self.control = "{0}_{1}".format("Control", self.suffix)
        self.input = "{0}_{1}".format( "Input", self.suffix)
        self.output = "{0}_{1}".format( "Output", self.suffix)
        self.component = "{0}_{1}".format( "Components", self.suffix)

    def create_nodes(self):
        """ Create and name rig transforms """
        node_utils.get_node_agnostic(name = self.root, nodeType="transform", parent=None)
        init_hierarchy(name="", suffix=self.suffix, hierarchy_class=None, parent=self.root)
        self.groups = [self.root, self.geo, self.skeleton, self.rig, self.input, self.output, self.component]


    def finalize(self):
        """ Cleanup """
        for i in range(len(self.groups)):
            #---lock transform
            misc_utils.lock_attrs(mayaObject = self.groups[i])
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

    def create(self):
        self.initialize()
        self.create_nodes()
        self.finalize()

def init_hierarchy(
                   name,
                   suffix,
                   hierarchy_class=None,
                   parent=None,
                   create_geo_grp=False,
                   create_skelton_grp=False,
                   create_rig_grp=False,
                   create_control_grp=False,
                   create_subcomponent_grp=False,
                   create_guide_grp=False,
                   create_input=False,
                   create_output=False,
                   subcomponent_group=None,
                   ):
    """
    Having a subcomponent group is going to trigger an automatic creation of all subcomponent grps
    """
    geo = "{0}Geo_{1}".format( name, suffix)
    skeleton = "{0}Skeleton_{1}".format( name, suffix)
    rig = "{0}Rig_{1}".format( name, suffix)
    control = "{0}Control_{1}".format( name, suffix)
    component = "{0}Components_{1}".format( name, suffix)
    input = "{0}Input_{1}".format( name, suffix)
    output = "{0}Output_{1}".format( name, suffix)

    # Where to parent the new nodes.  If this is the root there will be no parent class
    class_geo = parent
    class_skeleton = parent
    class_rig = parent
    class_control = parent
    class_component = parent
    class_input = parent
    class_output = parent
    
    if hierarchy_class:
        class_geo = hierarchy_class.geo
        class_skeleton = hierarchy_class.skeleton
        class_rig = hierarchy_class.rig
        class_control = hierarchy_class.control
        class_input = hierarchy_class.input
        class_output = hierarchy_class.output
        component = hierarchy_class.component

    if subcomponent_group:
        geo = "{0}_GEO".format( name)
        skeleton = "{0}_SKELETON".format( name)
        rig = "{0}_RIG".format(name)
        control = "{0}_CONTROL".format(name)
        input = "{0}_INPUT".format(name)
        output = "{0}_OUTPUT".format(name)

        create_geo_grp=True,
        create_skelton_grp=True,
        create_rig_grp=True,
        create_control_grp=True,
        create_input=True,
        create_output=True,
        
        class_geo = subcomponent_group
        class_skeleton = subcomponent_group
        class_rig = subcomponent_group
        class_control = subcomponent_group
        class_input = subcomponent_group
        class_output = subcomponent_group

    if create_geo_grp or not hierarchy_class:
        node_utils.get_node_agnostic(name = geo, nodeType="transform", parent=class_geo)
    else:
        geo = class_geo

    if create_skelton_grp or not hierarchy_class:
        node_utils.get_node_agnostic(name = skeleton, nodeType="transform", parent=class_skeleton)
    else:
        skeleton = class_skeleton

    if create_rig_grp or not hierarchy_class:
        node_utils.get_node_agnostic(name = rig, nodeType="transform", parent=class_rig)
    else:
        rig = class_rig

    if create_control_grp or not hierarchy_class:
        node_utils.get_node_agnostic(name = control, nodeType="transform", parent=class_control)
    else:
        control = class_control
        
    if create_input or not hierarchy_class:
        node_utils.get_node_agnostic(name = input, nodeType="transform", parent=class_input)
    else:
        input = class_input
        
    if create_output or not hierarchy_class:
        node_utils.get_node_agnostic(name = output, nodeType="transform", parent=class_output)
    else:
        output = class_output
        

    # only create the component transform if you are creating the root
    if not hierarchy_class:
        node_utils.get_node_agnostic(name = component, nodeType="transform", parent=class_component)

    return geo, skeleton, rig, control, input, output, component
