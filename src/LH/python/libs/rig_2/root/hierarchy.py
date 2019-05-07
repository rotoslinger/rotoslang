from maya import cmds
from rig_2.node import utils as node_utils
from rig_2.misc import utils as misc_utils

reload(misc_utils)
reload(node_utils)

class base(object):
    def __init__(self,
                 asset_name = "asset",
                 ):
        """
        @type  asset_name:                string
        @param asset_name:                asset name
        """
        #---args
        self.asset_name                   = asset_name
        
        #---vars
        # side and suffix could be args, but for now they will be constant until we figure out what to do with them
        self.side                        = "C"
        self.suffix                      = "GRP"
        self.groups                      = []

    def initialize(self):
        """ Placeholder for naming node_utils """
        self.root = "{0}_{1}_{2}".format(self.side, self.asset_name, self.suffix)
        self.geo = "{0}_{1}_{2}".format(self.side, "Geo", self.suffix)
        self.skeleton = "{0}_{1}_{2}".format(self.side, "Skeleton", self.suffix)
        self.rig = "{0}_{1}_{2}".format(self.side, "Rig", self.suffix)
        self.control = "{0}_{1}_{2}".format(self.side, "Control", self.suffix)
        self.component = "{0}_{1}_{2}".format(self.side, "Component", self.suffix)

    def create_nodes(self):
        """ Create and name rig transforms """
        node_utils.get_node_agnostic(name = self.root, nodeType="transform", parent=None)
        # self.groups = [self.root] + node_utils.get_node_agnostic_multiple(names=[self.geo,
        #                                                                  self.skeleton,
        #                                                                  self.rig,
        #                                                                  self.control,
        #                                                                  self.component],
        #                                                           nodeType="transform", 
        #                                                           parent=self.root)
        init_hierarchy(side=self.side, name="", suffix=self.suffix, hierarchy_class=None, parent=self.root)
        self.groups = [self.root, self.geo, self.skeleton, self.rig, self.component]


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

def init_hierarchy(side,
                   name,
                   suffix,
                   hierarchy_class=None,
                   parent=None,
                   create_geo_grp=False,
                   create_skelton_grp=False,
                   create_rig_grp=False,
                   create_control_grp=False,
                   create_subcomponent_grp=False,
                   ):
    """
    
    """
    geo = "{0}_{1}Geo_{2}".format(side, name, suffix)
    skeleton = "{0}_{1}Skeleton_{2}".format(side, name, suffix)
    rig = "{0}_{1}Rig_{2}".format(side, name, suffix)
    control = "{0}_{1}Control_{2}".format(side, name, suffix)
    component = "{0}_{1}Component_{2}".format(side, name, suffix)

    # Where to parent the new nodes.  If this is the root there will be no parent class
    class_geo = parent
    class_skeleton = parent
    class_rig = parent
    class_control = parent
    class_component = parent

    if hierarchy_class:
        class_geo = hierarchy_class.geo
        class_skeleton = hierarchy_class.skeleton
        class_rig = hierarchy_class.rig
        class_control = hierarchy_class.control
        component = hierarchy_class.component

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

    # only create the component transform if you are creating the root
    if not hierarchy_class:
        node_utils.get_node_agnostic(name = component, nodeType="transform", parent=class_component)

    return geo, skeleton, rig, control, component
