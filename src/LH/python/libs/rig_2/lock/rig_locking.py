import maya.cmds as cmds

def set_display_type(display_type = 1):
    top_level_nodes = cmds.ls( assemblies=True)
    for node in top_level_nodes:
        relatives = cmds.listRelatives(node)
        if len(relatives) > 1:
            model_hier = [x for x in relatives if "base_model_h" in x][0]
            
            cmds.setAttr("{0}.overrideDisplayType".format(model_hier), display_type)
            
def attribute_exists(obj, attr):
    return cmds.attributeQuery(attr, node=obj, exists=True)

#Leave the joint radius alone
#joint_radius = None
#uncomment if you want to set the size of the joint radius
#joint_radius = 10

def unlock_unhide_bones(joint_radius=None):
    cmds.setAttr("skel_grp.visibility", k=True, lock=0)
    cmds.setAttr("rig_grp.visibility", k=True, lock=0)
    cmds.setAttr("skel_grp.visibility",True, k=True, lock=0)
    cmds.setAttr("rig_grp.visibility", True, k=True, lock=0)
    for i in cmds.ls(type="joint"):
        cmds.setAttr(i+".radius", k=True, lock=0)
        if joint_radius:
            cmds.setAttr(i+".radius", joint_radius)
# Usage #
#joint_radius = None
#uncomment if you want to set the size of the joint radius
#joint_radius = 10                    
#unlock_unhide_bones(joint_radius = joint_radius)

def unlock():
    set_display_type(0)
      
def lock():
    set_display_type(2)


def unlock_all():
    disp_dict = dict()
    # Searching all dag nodes for "overrideDisplayType" attribute
    for dag_node in cmds.ls(dagObjects=True):
        attr_exists = cmds.attributeQuery( "overrideDisplayType",
                                            node=dag_node,
                                            exists=True)
        disp_attr = "{0}.{1}".format(dag_node, "overrideDisplayType")
        disp_attr_val = cmds.getAttr(disp_attr)
        if attr_exists:
            disp_attr = "{0}.{1}".format(dag_node, "overrideDisplayType")
            disp_attr_val = cmds.getAttr(disp_attr)
            if disp_attr_val > 0:
                disp_dict[disp_attr] = disp_attr_val


deformer_types = ["blendShape",
                  "cluster",
                  "curveWarp",
                  "deltaMush",
                  "tension",
                  "solidify",
                  "lattice",
                  "proximity",
                  "wrap",
                  "shrinkWrap",
                  "morph",
                  "wire",
                  "wrinkle",
                  "softMod",
                  "nonLinear"
                  ]


def check_attr(node_type="", node_attr="hiddenInOutliner",
               filter="",
               get_attr_val=True,
               select_nodes=True,
               value_filter = True,
               set_new_value = True,
               new_value = 0):
    # disp_dict = dict()
    # Searching all dag nodes for "overrideDisplayType" attribute
    node_type_exists = ""
    if node_type:
        pass
    for dag_node in cmds.ls(type=node_type):
        pass
    nodes = ls_optional_nodetype(node_type=node_type)
    final_nodes = list()
    for dag_node in nodes:
        attr_exists = cmds.attributeQuery( node_attr,
                                            node=dag_node,
                                            exists=True)
        disp_attr = "{0}.{1}".format(dag_node, node_attr)
        disp_attr_val = cmds.getAttr(disp_attr)
        if attr_exists:
            final_nodes.append(dag_node)
            disp_attr_val = cmds.getAttr(disp_attr)
            if filter and filter in dag_node:
                cmds.select(dag_node, add=True)
            if get_attr_val and value_filter:
                if disp_attr_val == value_filter:
                    print(disp_attr, str(disp_attr_val))
            if set_new_value:
                cmds.setAttr(disp_attr, new_value)

    if select_nodes:
        cmds.select(final_nodes)
    print(final_nodes)

            # print("{0}    {1}".format(disp_attr, disp_attr_val))
            # if disp_attr_val > 0:
            #     disp_dict[disp_attr] = disp_attr_val

def ls_optional_nodetype(node_type=""):
    if node_type:
        return cmds.ls(type=node_type)
    return cmds.ls(dagObjects=True)

def find_containers():
    disp_dict = dict()
    # Searching all dag nodes for "overrideDisplayType" attribute
    cmds.ls(containers=True)

    for container in cmds.ls(containers=True):
        print(container)

def find_jnts():
    for jnt in cmds.ls(type="joint"):
        print(jnt)

