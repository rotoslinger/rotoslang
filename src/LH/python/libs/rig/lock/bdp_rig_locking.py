import maya.cmds as cmds

############################################################################################################################################################
##################################################################### Rig Unlocking ########################################################################
############################################################################################################################################################

### Constants ###

# give a float value if you would like to set the joint size (depending on scale you may want to just set under display>Animation>Joint Size ...)
JOINT_RADIUS = None # <----- defaulting to whatever your display joints size is.  Human scale shouldn't change too much. Set using the display menu ( display>Animation>Joint Size ...)
# TODO if we end up needing a version of this for the Nowake rigs we might want to set a default for sea creatures, and another for humans.
# Needed to turn on visibility of the skinning joints.
UNLOCK_GROUPS = ["skel_grp", "rig_grp", "rigGeo_ndStep_grp", "rigGeo_200_grp", "spaces_grp", "modules_grp", "M_freeze_env", "M_masterWalkOut_jnt"]
# FYI --- the relevant joint groups are "rig_grp", "rigGeo_ndStep_grp", "rigGeo_200_grp", "M_masterWalkOut_jnt"
# other groups in the following list just need to be unlocked to allow visibility.
SKIN_JNTS = "skel_grp"
WALKOUT_JNTS = "M_masterWalkOut_jnt"
DEFORMER_TYPES = ["blendShape",
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
NODE_TYPES = [
    "mesh",
    "nurbsCurve",
    "nurbsSurface",
    "nurbsTrimmedSurface",
    "subdiv",
    "bezierCurve",
    "bezierSurface",
    "lattice"
]

def unlock_unhide_grps(joint_radius=JOINT_RADIUS, unlock_groups = UNLOCK_GROUPS):
    for grp in unlock_groups:
        cmds.setAttr(grp + ".visibility", k=True, lock=0)
        cmds.setAttr(grp + ".visibility", True, k=True, lock=0)
    for i in cmds.ls(type="joint"):
        cmds.setAttr(i+".radius", k=False, lock=0)
        if joint_radius:
            cmds.setAttr(i+".radius", joint_radius)
# Usage #
# unlock_unhide_bones(joint_radius = JOINT_RADIUS, unlock_groups = UNLOCK_GROUPS)

def vis_walkout_skin(skin=True, walkout=True):
    for child in cmds.listRelatives(SKIN_JNTS, shapes=False, typ="transform"):
        cmds.setAttr(child + ".visibility", skin, k=False, lock=0)
    cmds.setAttr(WALKOUT_JNTS + ".visibility", walkout, k=False, lock=0)
####################################### Usage ########################################
# # walkout only
# vis_walkout_skin(skin=False, walkout=True)
# # skin only
# vis_walkout_skin(skin=True, walkout=False)
######################################################################################

def set_display_type(display_type = 1):
    top_level_nodes = cmds.ls( assemblies=True)
    for node in top_level_nodes:
        relatives = cmds.listRelatives(node)
        if len(relatives) > 1:
            model_hier = [x for x in relatives if "base_model_h" in x][0]
            
            cmds.setAttr("{0}.overrideDisplayType".format(model_hier), display_type)
            
def attribute_exists(obj, attr):
    return cmds.attributeQuery(attr, node=obj, exists=True)

def list_skin_cluster_influences(mesh, debug = True):
    # Find skin cluster attached to the mesh
    skin_clusters = cmds.ls(cmds.listHistory(mesh), type='skinCluster')
    
    if skin_clusters:
        for skin_cluster in skin_clusters:
            # skin_cluster = skin_clusters[0]
            # Get the influences (bones) for the skin cluster
            influences = cmds.skinCluster(skin_cluster, query=True, influence=True)
            if debug:
                print(influences)
            return influences
    else:
        print("No skin cluster found on", mesh)
        return None

####################################### Usage ########################################
# mesh_name = 'pSphere1'  # Replace with your skinned geometry name
# influences = list_skin_cluster_influences("crrBrkExt_base_body_C_body_metal_sub")
# if influences:
#     print(influences)
######################################################################################



def setIsHistoricallyInteresting(value=1):
    '''
    Set isHistoricallyInteresting attribute for all nodes in scene.
    The historicallyInteresting attribute is 0 on nodes which are only interesting to programmers.
    1 for the TDs, 2 for the users.
    param value        Set ihi to 0: off, 1:on, 2:also on
    setIsHistoricallyInteresting(value=0)  # hide history from channelbox
    setIsHistoricallyInteresting(value=2)  # show history (a bit more than Maya's default)
    '''
    allNodes = cmds.ls()
    failed = []
    for node in allNodes:
        plug = '{}.ihi'.format(node)
        if cmds.objExists(plug):
            try:
                cmds.setAttr(plug, value)
            except:
                failed.append(node)
    if failed:
        print("Skipped the following nodes {}".format(failed))
####################################### Usage ########################################
#setIsHistoricallyInteresting(value=1)
######################################################################################

def find_all_children_and_set_visibility(node, filter, object_type):
    # List to store all child nodes and their parents
    child_list = []
    parent_list = []  # List to store parents for visibility updates
    visibility_changed = []  # List to store names of objects with visibility changed
    # Recursive function to find all children
    def get_children(current_node):
        # Get immediate children of the current node
        children = cmds.listRelatives(current_node, children=True, fullPath=True)
        if not children:
            return False  # Base case: no more children, exit early
        found_env_child = False  # Flag to check if any child has the check_string
        for child in children:
            child_list.append(child)  # Add current child to the list
            # Check if the child has the check string in its name
            if filter in child:
                # Check the object type
                child_type = cmds.nodeType(child)
                print(f"Found child: {child} of type: {child_type}")  # Debug information
                if child_type == object_type:
                    found_env_child = True  # Mark that we found a child with the check_string
                    visibility_changed.append(child)  # Store child name for visibility change
                    # Check the visibility of the child
                    visibility = cmds.getAttr(child + ".visibility")
                    if not visibility:  # If visibility is off
                        cmds.setAttr(child + ".visibility", 1)  # Set visibility to on
                        print(f"Turning on visibility for: {child}")  # Debug information
            # Store the current child as a parent for future visibility setting
            parent_list.append(current_node)
            # Check if the current child has its own children
            if cmds.listRelatives(child, children=True):
                if get_children(child):  # Recursive call to find this child's children
                    found_env_child = True  # If any child has the check_string, mark it
        return found_env_child  # Return if any child has the check_string
    if get_children(node):  # Start the recursion with the initial node
        # If we found a child with the check string, set visibility for all parents
        for parent in parent_list:
            # Check and set visibility for the current parent
            visibility = cmds.getAttr(parent + ".visibility")
            if not visibility:  # If visibility is off
                cmds.setAttr(parent + ".visibility", 1)  # Set visibility to on
                visibility_changed.append(parent)  # Store parent name for visibility change
                print(f"Turning on visibility for parent: {parent}")  # Debug information
    return child_list, visibility_changed
####################################### Verbose Usage ########################################
# # Get the currently selected object
# selected_objects = cmds.ls(selection=True, long=True)
# # User input for the string to check and the object type to filter
# user_check_string = "env"  # Change this string as needed or get user input
# user_object_type = "joint"  # Set the object type to "joint"
# if selected_objects:
#     selected_object = selected_objects[0]  # Take the first selected object
#     all_children, changed_visibilities = find_all_children_and_set_visibility(selected_object, user_check_string, user_object_type)
#     # Final debug printing
#     if changed_visibilities:
#         print("\nThe following objects had their visibility turned on:")
#         for name in changed_visibilities:
#             print(f"{name} of type {cmds.nodeType(name)}")  # Print the name and type
#     else:
#         print("No objects had their visibility turned on.")
# else:
#     print("Please select a group.")
######################################################################################

# Toggle joint vis in viewport display.
# #This is not setting the visibility attributes, it is only happening on the viewport level.
def toggle_jnt_display_vis():
    viewPanels = cmds.getPanel( type='modelPanel')
    for view in viewPanels:
        joint_curr_vis = cmds.modelEditor(view, q=True, joints=True)
        joint_curr_vis = cmds.modelEditor(view, e=True, joints=not joint_curr_vis)
####################################### Usage ########################################
# toggle_jnt_display_vis()
######################################################################################

def unlock_unselectable():
    set_display_type(0)
      
def lock_unselectable():
    set_display_type(2)


def unlock_all(ihi_level=1, skin=True, walkout=True):
    unlock_unselectable()
    unlock_unhide_grps()
    vis_walkout_skin(skin=skin, walkout=walkout)
    setIsHistoricallyInteresting(value=ihi_level)


############################################################################################################################################################
############################################################ Full Unlocking Usage ##########################################################################
# # Unlock, unhide, unreference, and vis important groups and joints.

# # If you need to paint weights, you want to see the joints used for skinning
# unlock_all(ihi_level=1, skin=True, walkout=False)

# # If you are debugging rig functionality, you would only want to see the walkout joints
# unlock_all(ihi_level=1, skin=False, walkout=True)
############################################################################################################################################################
############################################################################################################################################################



############################################################################################################################################################
##################################################################### Rig Unlocking End ####################################################################
############################################################################################################################################################



#-----------------------------------------------------------------------------------------------------------------------------------------------------------



############################################################################################################################################################
####################################################################### Debugging ##########################################################################
############################################################################################################################################################

# TODO:
# add print statements to function
# add check if transform selected, find shapes, test on them
# shrink usage to one line.
def find_influencing_deformers_recursive(node, visited=None):
    if visited is None:
        visited = set()
    # If node has already been visited, skip it
    if node in visited:
        return []
    # Mark node as visited
    visited.add(node)
    deformers = []
    # List all input connections to the node (both shape and deformers)
    connections = cmds.listConnections(node, source=True, destination=False) or []
    for conn in connections:
        # Check if the connected node is a recognized deformer type
        if cmds.nodeType(conn) in ['skinCluster', 'blendShape', 'lattice', 'cluster', 'nonLinear', 'ffd', 'wire', 'sculpt']:
            deformers.append(conn)
        # Recursively traverse the connections to find deeper deformers
        deformers.extend(find_influencing_deformers_recursive(conn, visited))
    return deformers
####################################### Verbose Usage ########################################
# # Select the mesh first
# selected_mesh = cmds.ls(selection=True, dag=True, type="transform")
# if selected_mesh:
#     # Get the shape node of the selected mesh
#     shapes = cmds.listRelatives(selected_mesh[0], shapes=True, noIntermediate=True)
#     if shapes:
#         deformers = find_influencing_deformers_recursive(shapes[0])
#         if deformers:
#             deformers = list(set(deformers))  # Remove duplicates
#             print("Deformers influencing {}: {}".format(selected_mesh[0], deformers))
#         else:
#             print("No deformers found influencing the mesh.")
#     else:
#         print("No shape node found for the selected mesh.")
# else:
#     print("Please select a mesh.")
######################################################################################

# Deformer debugging.
def get_all_defomers(deformer_types=DEFORMER_TYPES):
    for deform_typ in deformer_types:
        deformers = cmds.ls(type = deform_typ)
        if deformers:
            print(deform_typ, len(deformers))

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

def print_jnt_names():
    for jnt in cmds.ls(type="joint"):
        print(jnt)


def debug_get_connection_chain(node):
    """Recursively retrieve the connection chain to the specified node."""
    chain = []
    current_node = node

    while True:
        # Get incoming connections for the current node
        incoming = cmds.listConnections(current_node, source=True, destination=False)
        if not incoming:
            break  # No more connections to follow

        # Assume the first incoming connection for simplicity
        current_node = incoming[0]
        chain.append(current_node)
    return chain

def debug_skin_connection_chain(node):
    # Get the shape node if the input node is a transform
    shapes = cmds.listRelatives(node, shapes=True, fullPath=True) or [node]

    # This will hold all the found skin clusters
    skin_clusters = set()

    # Go through all the shapes
    for shape in shapes:
        # Get all incoming and outgoing connections of the shape
        connections = cmds.listConnections(shape, connections=True, plugs=True) or []

        # Look for any deformer-related connections (groupParts, tweak, skinCluster, etc.)
        for i in range(0, len(connections), 2):
            source_attr = connections[i]
            dest_attr = connections[i + 1]
            source_node = source_attr.split('.')[0]
            dest_node = dest_attr.split('.')[0]

            # Check if the destination attribute is a skinCluster
            if 'skinCluster' in cmds.nodeType(dest_node):
                skin_clusters.add(dest_node)
                chain = debug_get_connection_chain(shape)  # Get the connection chain
                chain_str = '->'.join(reversed(chain + [shape, dest_node]))  # Build the chain string
                print(f"Connection chain for {dest_node}: {chain_str}")

            # Check if the source attribute is a skinCluster
            elif 'skinCluster' in cmds.nodeType(source_node):
                skin_clusters.add(source_node)
                chain = debug_get_connection_chain(dest_node)  # Get the connection chain
                chain_str = '->'.join(reversed(chain + [dest_node, source_node]))  # Build the chain string
                print(f"Connection chain for {source_node}: {chain_str}")
    return list(skin_clusters)
####################################### Usage ########################################
# skin_clusters = debug_skin_connection_chain("jsh_base_body_geo")
######################################################################################



def list_compound_attribute_connections(node, compound_attr):
    """
    Lists all connections for a given compound attribute on a node.
    Args:
    - node (str): The name of the node (e.g., a skinCluster).
    - compound_attr (str): The name of the compound attribute (e.g., "matrix").
    """
    # Get the full path of the compound attribute (node + compound attribute)
    full_attr = f"{node}.{compound_attr}"
    # Check if the attribute exists and is compound
    if not cmds.attributeQuery(compound_attr, node=node, exists=True):
        raise ValueError(f"The attribute {compound_attr} does not exist on node {node}.")
    if not cmds.attributeQuery(compound_attr, node=node, multi=True):
        raise ValueError(f"The attribute {compound_attr} is not a compound array.")
    # Get all indices for the compound array
    indices = cmds.getAttr(full_attr, multiIndices=True)
    # Loop through all indices and find incoming connections
    for index in indices:
        # Build the indexed attribute (e.g., skinCluster.matrix[0])
        indexed_attr = f"{full_attr}[{index}]"
        # List incoming connections
        connections = cmds.listConnections(indexed_attr, source=True, destination=False, plugs=True)
        if connections:
            for conn in connections:
                # conn will be something like "nodeName.attributeName"
                print(f"Connection to {indexed_attr}: {conn}")
        else:
            print(f"No incoming connections to {indexed_attr}")
####################################### Usage ########################################
# list_compound_attribute_connections('teshi_base_body_geo_bodyMechanics_skinCluster', 'matrix')
######################################################################################


def list_compound_attribute_connections(node, compound_attr):
    """
    Lists all connections for a given compound attribute on a node.
    Args:
    - node (str): The name of the node (e.g., a skinCluster).
    - compound_attr (str): The name of the compound attribute (e.g., "matrix").
    """
    # Get the full path of the compound attribute (node + compound attribute)
    full_attr = f"{node}.{compound_attr}"
    # Check if the attribute exists and is compound
    if not cmds.attributeQuery(compound_attr, node=node, exists=True):
        raise ValueError(f"The attribute {compound_attr} does not exist on node {node}.")
    if not cmds.attributeQuery(compound_attr, node=node, multi=True):
        raise ValueError(f"The attribute {compound_attr} is not a compound array.")
    # Get all indices for the compound array
    indices = cmds.getAttr(full_attr, multiIndices=True)
    # Loop through all indices and find incoming connections
    for index in indices:
        # Build the indexed attribute (e.g., skinCluster.matrix[0])
        indexed_attr = f"{full_attr}[{index}]"
        # List incoming connections
        connections = cmds.listConnections(indexed_attr, source=True, destination=False, plugs=True)
        if connections:
            for conn in connections:
                # conn will be something like "nodeName.attributeName"
                print(f"Connection to {indexed_attr}: {conn}")
        else:
            print(f"No incoming connections to {indexed_attr}")
####################################### Usage ########################################
# list_compound_attribute_connections('teshi_base_body_geo_bodyMechanics_skinCluster', 'matrix')
######################################################################################


def unlock_skinweights(node, compound_attr):
    """
    Lists all connections for a given compound attribute on a node.
    Args:
    - node (str): The name of the node (e.g., a skinCluster).
    - compound_attr (str): The name of the compound attribute (e.g., "matrix").
    """
    # Get the full path of the compound attribute (node + compound attribute)
    full_attr = f"{node}.{compound_attr}"
    # Get all indices for the compound array
    indices = cmds.getAttr(full_attr, multiIndices=True)
    # Loop through all indices and find incoming connections
    for index in indices:
        # Build the indexed attribute (e.g., skinCluster.matrix[0])
        indexed_attr = f"{full_attr}[{index}]"
        # List incoming connections
        connections = cmds.listConnections(indexed_attr, source=True, destination=False, plugs=True)
        if connections:
            for conn in connections:
                # conn will be something like "nodeName.attributeName"
                print(f"Connection to {indexed_attr}: {conn}")
        else:
            print(f"No incoming connections to {indexed_attr}")
####################################### Usage ########################################
# list_compound_attribute_connections('teshi_base_body_geo_bodyMechanics_skinCluster', 'matrix')
######################################################################################

############################################################################################################################################################
##################################################################### Debugging End ########################################################################
############################################################################################################################################################
