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


# def unlock_unhide_bones(joint_radius=None):
#     cmds.setAttr("skel_grp.visibility", k=True, lock=0)
#     cmds.setAttr("rig_grp.visibility", k=True, lock=0)
#     cmds.setAttr("skel_grp.visibility",True, k=True, lock=0)
#     cmds.setAttr("rig_grp.visibility", True, k=True, lock=0)
#     for i in cmds.ls(type="joint"):
#         cmds.setAttr(i+".radius", k=True, lock=0)
#         if joint_radius:
#             cmds.setAttr(i+".radius", joint_radius)


### Joint Related Constants ###

# give a float value if you would like to set the joint size (depending on scale you may want to just set under display>Animation>Joint Size ...)
JOINT_RADIUS = None # <----- defaulting to whatever your display joints size is.  Human scale shouldn't change too much. Set using the display menu ( display>Animation>Joint Size ...)
# TODO if we end up needing a version of this for the Nowake rigs we might want to set a default for sea creatures, and another for humans.
# Needed to turn on visibility of the skinning joints.
UNLOCK_GROUPS = ["skel_grp", "rig_grp", "rigGeo_ndStep_grp", "rigGeo_200_grp", "spaces_grp", "modules_grp", "M_masterWalkOut_jnt", "M_freeze_env"]
# FYI --- the relevent joint groups are "rig_grp", "rigGeo_ndStep_grp", "rigGeo_200_grp", "M_masterWalkOut_jnt"
# other groups in the following list just need to be unlocked to allow visibility.

def unlock_unhide_bones(joint_radius=JOINT_RADIUS, unlock_groups = UNLOCK_GROUPS):
    for grp in unlock_groups:
        cmds.setAttr(grp + ".visibility", k=True, lock=0)
        cmds.setAttr(grp + ".visibility", True, k=True, lock=0)
    for i in cmds.ls(type="joint"):
        cmds.setAttr(i+".radius", k=True, lock=0)
        if joint_radius:
            cmds.setAttr(i+".radius", joint_radius)
# Usage #
# unlock_unhide_bones(joint_radius = JOINT_RADIUS, unlock_groups = UNLOCK_GROUPS)



# TODO obviously this will need to loop through all skinclusters on the given mesh because minimo is super cool (not cool).
'''
def list_skin_cluster_influences(mesh):
    # Find skin cluster attached to the mesh
    skin_clusters = cmds.ls(cmds.listHistory(mesh), type='skinCluster')
    
    if skin_clusters:
        skin_cluster = skin_clusters[0]
        # Get the influences (bones) for the skin cluster
        influences = cmds.skinCluster(skin_cluster, query=True, influence=True)
        return influences
    else:
        print("No skin cluster found on", mesh)
        return None
'''    
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

# Example usage
# mesh_name = 'pSphere1'  # Replace with your skinned geometry name
# influences = list_skin_cluster_influences("crrBrkExt_base_body_C_body_metal_sub")
# if influences:
#     print(influences)

def unlock():
    set_display_type(0)
      
def lock():
    set_display_type(2)


def unlock_all():
    unlock()
    unlock_unhide_bones()

    # disp_dict = dict()
    # # Searching all dag nodes for "overrideDisplayType" attribute
    # for dag_node in cmds.ls(dagObjects=True):
    #     attr_exists = cmds.attributeQuery( "overrideDisplayType",
    #                                         node=dag_node,
    #                                         exists=True)
    #     disp_attr = "{0}.{1}".format(dag_node, "overrideDisplayType")
    #     disp_attr_val = cmds.getAttr(disp_attr)
    #     if attr_exists:
    #         disp_attr = "{0}.{1}".format(dag_node, "overrideDisplayType")
    #         disp_attr_val = cmds.getAttr(disp_attr)
    #         if disp_attr_val > 0:
    #             disp_dict[disp_attr] = disp_attr_val


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

def find_jnts():
    for jnt in cmds.ls(type="joint"):
        print(jnt)

############## BDP Weight Export Utils ##################

def get_geom_skinclusters(geom):
    # Get the shape node if the input node is a transform
    shapes = cmds.listRelatives(geom, shapes=True, fullPath=True) or [geom]

    # This will hold all the found skin clusters
    skin_clusters = set() # <---- to avoid duplicates (shouldn't happen, but whatever)

    # Go through all the shapes
    for shape in shapes:
        # Get all incoming and outgoing connections of the shape
        connections = cmds.listConnections(shape, connections=True, plugs=True) or []

        # Look for any deformer-related connections (groupParts, tweak, skinCluster, etc.)
        for i in range(0, len(connections), 2):
            source_attr = connections[i]
            dest_attr = connections[i + 1]
            
            # Check for skinCluster in the deformer's connection chain
            if 'skinCluster' in cmds.nodeType(dest_attr.split('.')[0]):
                skin_clusters.add(dest_attr.split('.')[0])

            elif 'skinCluster' in cmds.nodeType(source_attr.split('.')[0]):
                skin_clusters.add(source_attr.split('.')[0])

    return list(skin_clusters)
### Usage
# skin_clusters = get_geom_skinclusters("jsh_base_body_geo")
# for skin in skin_clusters:
#     print(skin)
##########################################################################################


# TODO add a normalization feature to import? Needs testing.
def filter_skins(geom="", skin_filter=[""]):
    skins = get_geom_skinclusters(geom=geom)
    if skin_filter == ["all"]:
        skin_filter = skins
    filtered_skins = list()
    # Filter skins
    for skin in skins:
        filtered = [f for f in skin_filter if f in skin]
        if len(filtered) > 0:         
            filtered_skins.append(skin)
    return filtered_skins
# Usage #
# filter_skins(geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################

def export_skins(path="", geom="", skin_filter=[""]):
    # Filter skins
    filtered_skins = filter_skins(geom=geom, skin_filter=skin_filter)
    # Export filtered skins
    for skin in filtered_skins:
        cmds.deformerWeights(skin + ".xml",
                        export = True, 
                        deformer=skin,
                        path = path)
# Usage #
# weights_path = "C:/Users/harri/Documents/BDP/cha/jsh"
# export_skins(path=weights_path, geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################

def import_skins(path="", geom="", skin_filter=[""]):
    # Filter skins
    filtered_skins = filter_skins(geom=geom, skin_filter=skin_filter)
    # Export filtered skins
    for skin in filtered_skins:
        cmds.deformerWeights(skin + ".xml",
                            im = True,
                            method = "index",
                            deformer=skin,
                            path = path)
        
        # weight normalization for imported weights. Must be updated or points are disfigured at rest.
        # to make sure normalization has worked, translate the global movement controller 1000 units away, rotate global scale, and see if the points are drifting. 
        cmds.skinPercent(skin, geom, normalize = True)
        cmds.skinCluster(skin , e = True, forceNormalizeWeights = True)
        print("# Imported deformer weights from '" + path + skin + ".xml'.")

        # Exported deformer weights to 'C:/Users/harri/Documents/BDP/cha/jsh/jsh_base_body_geo_upperFace_skinCluster.xml'.

# Usage #
# weights_path = "C:/Users/harri/Documents/BDP/cha/jsh"
# import_skins(path=weights_path, geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################


# Full Usage #
weights_path = "C:/Users/harri/Documents/BDP/cha/jsh"
export_skins(path=weights_path, geom="jsh_base_body_geo", skin_filter=["upperFace"])
import_skins(path=weights_path, geom="jsh_base_body_geo", skin_filter=["upperFace"])









# def shape_from_xform(node):
#     # Check if the node is of type 'transform'
#     if cmds.objectType(node) == 'transform':
#         # List all shapes under the transform node
#         shapes = cmds.listRelatives(node, shapes=True, fullPath=True)
#         if shapes:
#             return shapes[0]  # Return the first shape found
#     if cmds.objectType(node) == 'transform':
#         # List all shapes under the transform node
#         shapes = cmds.listRelatives(node, shapes=True, fullPath=True)
#         if shapes:
#             return shapes[0]  # Return the first shape found

#     return None



















# def export_skins(path):
#     # get all skin clusters in the scene and export them to xml files
#     skins = cmds.ls(type = "skinCluster")
#     for i in skins:
#         cmds.deformerWeights(i + ".xml",
#                              export = True, 
#                              deformer=i,
#                              path = path)
# #############################################
# #---example
# # weights_path = "C:\Users\harri\Documents\BDP\cha\jsh"
# # export_skins(weights_path)
# #############################################
# def import_skins(path):
#     skins = cmds.ls(type = "skinCluster")
#     if skins:
#         for i in skins:
#             cmds.deformerWeights(i + ".xml",
#                              im = True,
#                              method = "index",
#                              deformer=i,
#                              path = path)

#             geom = cmds.skinCluster(i,q=True, g = True)
#             cmds.skinPercent(i,geom,normalize = True)
#             cmds.skinCluster(i , e = True, forceNormalizeWeights = True)


# TODO things to think about, should we filter node types?
# constants #
# possible future filter for skinCluster export node types
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












############################################################################################################################################################
# Supplemental Debugging for
import maya.cmds as cmds

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

# usage #
# skin_clusters = debug_skin_connection_chain("jsh_base_body_geo")
