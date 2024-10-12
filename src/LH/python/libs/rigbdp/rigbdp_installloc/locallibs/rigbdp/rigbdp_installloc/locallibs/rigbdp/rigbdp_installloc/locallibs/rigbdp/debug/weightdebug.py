import importlib, os, re

from maya import cmds


############################# File Path Utils ###############################

##############  Why we need to use \ delimiter for filepaths on Windows ###############
# Leave it to windows to choose \ as the path delimiter, simply because DOS used / for command flags instead of the bash standard of -
# In bash or shell even C, the flag option is usually a -(hyphen) -h for concise help or --help for more verbose help.
# In a shell, for example, you can use rm -rf * to delete the whole internet, or maybe just your hard drive.  It can be tempting, but don't do it (test on your friend's computer first).
# It goes without saying this f***s using special characters in strings and formatting. 
# python, C, C++ and etc, use the backslash (\) as an escape character in strings.
# This allows you to include special characters, such as newlines (\n), tabs (\t), or even literal backslashes (\\), within string literals.
# That means we need to use sub to do a wildcard search and replace because maya uses Unix style / for paths
def de_windows_os_path(filepath):
    path =  os.path.normpath(filepath)
    if '\\' in path: return re.sub(r'\\', '/', path)
    return path
#################################### Usage ####################################
# don't forget to double them backspaces, because \\ resolves to \ and doesn't break python. Or C++, or C, etc. Did I mention I hate this?
# mayaified_directory = de_windows_os_path(filepath = "C:\\foobar\\skoobar\\skeebop\\skeedoobar\\" ) # on windows returns --- C:/foobar/skoobar/skeebop/skeedoobar
# print("This is the normalized directory " + mayaified_directory)
###############################################################################

######################################################################################

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
####################################### Usage ########################################
# skin_clusters = get_geom_skinclusters("jsh_base_body_geo")
# for skin in skin_clusters:
#     print(skin)
##########################################################################################



######################################################################################
################################# BDP Debug Utils ####################################
######################################################################################

def print_skin_infos(geo, skin, print_shapes):
            if not print_shapes:
                geo = cmds.listRelatives(geo, parent=True)[0]
            print("{0} -------------- bound to skinCluster ------------ {1}.". format(geo, skin))
####################################### Usage ########################################
# This function is only used by skin_infos and shouldn't be used on its own.
# See the usage for function skin_infos.
######################################################################################

def skin_infos(filter_geom_type = None, print_shapes=False, filter_geom_name="beep"):
    print("##############################################################################################################")
    print("############################################## START #########################################################")
    print("##############################################################################################################")
    for skin in cmds.ls(type="skinCluster"):
        geom = cmds.skinCluster(skin,q=True, g = True)
        for geo in geom:
            if filter_geom_type != None and filter_geom_type == cmds.objectType(geo):
                # print("this is the geo " + cmds.listRelatives(geo, parent=True)[0])
                # print("this is the filter name " + filter_geom_name)
                if filter_geom_name == None:
                    print_skin_infos(geo, skin, print_shapes)
                    continue
                if filter_geom_name != None and filter_geom_name in geo:
                    print_skin_infos(geo, skin, print_shapes)
                    continue
            if filter_geom_type == None:
                if filter_geom_name == None:
                    print_skin_infos(geo, skin, print_shapes)
                    continue
                if filter_geom_name != None and filter_geom_name in geo:
                    print_skin_infos(geo, skin, print_shapes)
                    continue
    print("##############################################################################################################")
    print("##############################################  END  #########################################################")
    print("##############################################################################################################")
####################################### Usage ########################################
# ################# --- How to specify info about a particular mesh
# skin_infos(filter_geom_type = "mesh", print_shapes=False, filter_geom_name="jsh_base_body_geo")
# ################# --- Less specific about a particular mesh (keep in mind the filter_geom_name is a wildcard, or search)
# ################# --- This might return things with "jsh_base_body_geo" in them such as "jsh_base_body_geo_headSquashAndStretch_ltclattice"
# skin_infos(filter_geom_type = None, print_shapes=False, filter_geom_name="jsh_base_body_geo")
# ################# --- Not specific, will return every geometry that has a skincluster in the whole scene
# ################# --- This includes nurbsCurves, nurbsSurfaces, lattices, meshes, (possibly others, but these are what I have seen so far).
# skin_infos(filter_geom_type = None, print_shapes=False, filter_geom_name=None)
# ################# --- Examples of all geometry types
# skin_infos(filter_geom_type = "mesh", print_shapes=False)
# skin_infos(filter_geom_type = "nurbsCurve", print_shapes=False)
# skin_infos(filter_geom_type = "nurbsSurface", print_shapes=False)
# skin_infos(filter_geom_type = "lattice", print_shapes=False)
# ######################################################################################

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

# TODO Finish!!!! 
def list_skin_cluster_influences(geom):
    # Find skin cluster attached to the mesh
    skinclusters =get_geom_skinclusters(geom=geom)
    all_skinclusters = list()
    skin_influence_map = dict()
    for skincluster in skinclusters:
        # Get the influences (bones) for the skin cluster
        influences = cmds.skinCluster(skincluster, query=True, influence=True)
        all_skinclusters.append(influences)
        skin_influence_map

####################################### Usage ########################################
# mesh_name = 'pSphere1'  # Replace with your skinned geometry name
# influences = list_skin_cluster_influences("crrBrkExt_base_body_C_body_metal_sub")
# if influences:
#     print(influences)
# If you need to rebuild your skincluster
# 1. Print the influences list
# 2. Copy output to a text file (save it, and remember where you have saved it)
# 3. Delete the skin cluster.
######################################################################################

# TODO loop through all NODE_TYPES in the scene get deformer
# Print per geometry deformer info, including number, type, and if a skinCluster the number of influences.
# At the end give a summary, there are this many skinclusters, lattice deformers, curve deformers, etc.
# 1. Find all deformers on geoms, specified in the type filter.
# 2. Print the geometry name, then the number of each deformer on the geom, then what the name of the deformer is
# 3. Summary. This scene has this many skinclusters, lattice deformers, curve deformers, etc.
def scene_deform_info():
    pass
