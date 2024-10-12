import time, os, shutil, sys, re, json

from maya import cmds

######################################### Backup Utils ################################################
DELIMITER = os.path.sep  # Use the appropriate path delimiter for the OS
# Get the full path of the current scene
def get_scene_dir():
    current_scene = cmds.file(q=True, sn=True)
    # make sure the scene exists somewhere (you need to save to a directory to find out where the file is saved)
    if current_scene:
        # Extract the directory from the full scene path
        return os.path.dirname(current_scene)
    else:
        print("No saved scene is open. Save first, then try again")
        return None
#################################### Usage ####################################
# scene_dir = get_scene_dir()
# print("The current scene has been saved here: " + scene_dir)
###############################################################################
def generate_timestamp():
    t = time.localtime()
    # Creating a timestamp in a human-readable format: YYYY-MM-DD_HH-MM-SS
    return "{0}-{1}-{2}_{3}-{4}-{5}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

def generate_backup_filename(filepath, filename):
    filepath = os.path.normpath(f"{filepath}{DELIMITER}BAK")
    # Ensure the directory exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The directory '{filepath}' does not exist.")
    base_name, ext = os.path.splitext(filename)
    # Find existing versions
    existing_versions = []
    pattern = re.compile(rf"{re.escape(base_name)}_v(\d{{3}})_timestamp_.*{re.escape(ext)}")
    # Check files in the directory and extract version numbers
    for file in os.listdir(filepath):
        match = pattern.match(file)
        if match:
            existing_versions.append(int(match.group(1)))  # Append the extracted version number
    # Determine the next version number
    version = max(existing_versions, default=0) + 1  # Start from v001 if no versions exist
    timestamp = generate_timestamp()
    backup_filename = os.path.join(filepath, f"{base_name}_v{version:03d}_timestamp_{timestamp}{ext}")
    return backup_filename
################################### Usage ###################################
# filepath = r"C:\Users\harri\Documents\BDP\cha\jsh"
# filename = "jsh_base_body_geo_upperFace_skinCluster.xml"
# backup_filename = generate_backup_filename(filepath=filepath, filename=filename)
#############################################################################

def check_parent_directory(filepath, debug=False):
    # This only finds the path (BAK) just before the new file  and creates it if it doesn't exist
    # If other directories further up don't exist this will fail with an error
    # This fail is important because it is possible the entire file structure doesn't exist yet and
    # could indicate a previous error.
    filepath = os.path.normpath("{0}{1}{2}".format(filepath, DELIMITER, "BAK"))
    filepath= os.path.normpath(filepath)
    # Make sure the path exists
    if not os.path.exists(filepath):
        os.mkdir(filepath)
        if not debug: return
        print("New directory created @ {0}".format(filepath))
################################### Usage ###########################################
# scene_dir = get_scene_dir()
# filename = "jsh_base_body_geo_upperFace_skinCluster.xml"
# check_parent_directory(filepath=scene_dir, debug=True)
### --- If there is no folder called BAK in the directory, it will be created
### --- This will print out: New directory created @ C:\Users\harri\Documents\BDP\cha\jsh\BAK
#####################################################################################

def backup_file(filepath, filename):
    if not os.path.exists(filepath): return
    # 1. Check whether file exists yet.
    fullpath = "{0}/{1}".format(filepath, filename)
    norm_path= os.path.normpath(fullpath)
    # 2. If file doesn't exist return
    if not os.path.exists(norm_path):return
    # 3. File exists, run check_parent_directory(), to make sure the BAK dir exists
    check_parent_directory(filepath=filepath)
    # 4. Use generate_backup_filename() to rename with timestamp.
    backup_name = generate_backup_filename(filepath=filepath, filename=filename)
    shutil.copy(fullpath, backup_name)
############################# Full Backup Utils Usage ################################
# filepath = r"C:\Users\harri\Documents\BDP\cha\jsh"
# filename = "jsh_base_body_geo_upperFace_skinCluster.xml"
# backup_file(filepath=filepath, filename=filename)
######################################################################################


######################################################################################
############################# BDP Weight Export Utils ################################
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

# TODO add a normalization feature to import? Needs testing.
def filter_skins(geom="", skin_filter=None):
    skins = get_geom_skinclusters(geom=geom)
    if not skin_filter:
        return skins
    # if only a single string is given for the skin filter arg, add it to a list to avoid looping through individual chars 
    if type(skin_filter) != list: skin_filter = [skin_filter]
    filtered_skins = list()
    # Filter skins
    for skin in skins:
        filtered = [f for f in skin_filter if f in skin]
        if len(filtered) > 0:         
            filtered_skins.append(skin)
    return filtered_skins
####################################### Usage ########################################
# filter_skins(geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################

def export_skins(path=None, geom="", skin_filter=[""]):
    # If a path is not given, just default to the path that the current scene is saved to
    if not path:
        path = get_scene_dir()
    # Filter skins
    filtered_skins = filter_skins(geom=geom, skin_filter=skin_filter)
    # Export filtered skins
    for skin in filtered_skins:
        # Backup file
        norm_path= os.path.normpath(path)
        print(norm_path)
        backup_file(filepath=norm_path, filename=skin + ".xml")
        # Export weights
        cmds.deformerWeights(skin + ".xml", export = True,  deformer=skin, path = path)
####################################### Usage ########################################
# export_skins(geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################

def import_skins(path=None, geom="", skin_filter=[""]):
    # If a path is not given, just default to the path that the current scene is saved to
    if not path:
        path = get_scene_dir()
    # Filter skins
    filtered_skins = filter_skins(geom=geom, skin_filter=skin_filter)
    # Export filtered skins
    for skin in filtered_skins:
        cmds.deformerWeights(skin + ".xml", im = True, method = "index", deformer=skin, path = path)
        # weight normalization for imported weights. Must be updated or points are disfigured at rest.
        # to make sure normalization has worked, translate the global movement controller 1000 units away, rotate global scale, and see if the points are drifting. 
        cmds.skinPercent(skin, geom, normalize = True)
        cmds.skinCluster(skin , e = True, forceNormalizeWeights = True)
        # print("# Imported deformer weights from '" + path + skin + ".xml'.")
        print("# Imported deformer weights from '{0}{1}.xml'.".format(path,skin))
####################################### Usage ########################################
# import_skins(geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################

########################## Full Import/Export Weights Usage ###########################
# export_skins(path=None, geom="jsh_base_body_geo", skin_filter=["upperFace"])
# import_skins(path=None, geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################

# TODO Finish!!!! 
def list_skin_cluster_influences(geom, skin_filter=None):
    # Find skin cluster attached to the mesh
    all_skinclusters = list()
    skin_influence_map = dict()
    filtered_skins = filter_skins(geom=geom, skin_filter=skin_filter)
    # Export filtered skins
    for skin in filtered_skins:
        print(skin)
        # Get the influences (bones) for the skin cluster
        influences = cmds.skinCluster(skin, query=True, influence=True)
        skin_influence_map[skin] = influences

        all_skinclusters.append(influences)
    for key in skin_influence_map.keys():
        print(f'{key} : {skin_influence_map[key]}')
        for influence in skin_influence_map[key]:
            print(f'{key} : {influence}')

    return skin_influence_map
####################################### Usage ########################################
# list_skin_cluster_influences(geom="jsh_base_body_geo", skin_filter=None)
######################################################################################

def get_compound_attr_connect_map(node, compound_attr):
    """
    Lists all connections for a given compound attribute on a node and returns them in a dictionary.
    Args:
    - node (str): The name of the node (e.g., a skinCluster).
    - compound_attr (str): The name of the compound attribute (e.g., "matrix").
    Returns:
    - dict: A dictionary containing the connections.
    """
    # Dictionary to store the connections
    matrix_connections_dict = {}
    joint_connections_dict = {}
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
        if "matrix[39]" in indexed_attr:
            print("\n")
            print("\n")

            #print("index_attr " + indexed_attr)

        # List incoming connections
        connection = cmds.listConnections(indexed_attr, source=True, destination=False, plugs=True)[0]
        # if "R_arm05Localized_multMatrix" in connection:
        #     print("indexed attr connection " + connection)


        mult_matrix_input0 = connection.split(".")[0]
        mult_matrix_input0= f'{mult_matrix_input0}.matrixIn[0]'
        mult_matrix_input0_connection = cmds.listConnections(mult_matrix_input0, source=True, destination=False, plugs=True)[0]
        mult_matrix_input0_connection = f'{mult_matrix_input0_connection}[0]'
        if "R_arm05Localized_multMatrix" in connection:
            #print("joint out attr " + joint_out_attr)
            print("input0 connection is " + mult_matrix_input0_connection)

        if connection:
            # Store connections in the dictionary
            if "matrix[39]" in indexed_attr:
                print(f"the dict is : matrix_connections_dict[{connection}] = {indexed_attr}")

            matrix_connections_dict[connection] = indexed_attr
            joint_connections_dict[mult_matrix_input0_connection] = indexed_attr
        else:
            matrix_connections_dict[connection] = None
            joint_connections_dict[mult_matrix_input0_connection] = None


    export_dict = {f'{node}_MATRIX_MULT':matrix_connections_dict,
                   f'{node}_ENV':joint_connections_dict}
    return export_dict
####################################### Usage ########################################
# connections_data = get_compound_attr_connect_map(node='teshi_base_body_geo_bodyMechanics_skinCluster',
#                                                  compound_attr='matrix')
######################################################################################

def export_to_json(data, file_path=None, filename_prefix='',  suffix="MATRIX_CONNECTIONS"):
    """
    Exports a dictionary to a JSON file using the node name and a custom file path.
    Args:
    - data (dict): The dictionary to export.
    - node (str): The node name to use in the JSON file name.
    - file_path (str): The file path where the JSON file will be saved.
    - suffix (str): The suffix to append to the filename.
    """
    # Create the full file name using the node name and suffix
    if not file_path:
        file_path = get_scene_dir()
    file_name = f"{filename_prefix}_{suffix}.json"
    full_file_path = os.path.join(file_path, file_name)

    # Export the dictionary to a JSON file
    with open(full_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("\n")
    print(f"Exported to {full_file_path}")
    print("\n")

####################################### Usage ########################################
# connections_data = get_compound_attr_connect_map(node='teshi_base_body_geo_bodyMechanics_skinCluster',
#                                                  compound_attr='matrix')
# export_to_json(connections_data,
#                filename_prefix='teshi_base_body_geo_bodyMechanics_skinCluster',
#                file_path=r'C:\Users\harri\Documents\BDP\cha\teshi',
#                suffix='MATRIX_CONNECTIONS')
######################################################################################

class JsonAttributes:
    '''
    A simple class that creates attributes based on dictionary keys.

    1. Extracts the first dimension keys of the dictionary
    2. Dynamically creates variables with the names of the keys
    3. Sets new variables with the second dimension dict
    '''
    def __init__(self, json_dict):
        """
        Args:
        - json_dict (dict): a 2 dimensional dictionary that must be derived from the output of get_compound_attr_connect_map()
                            this dict has key entries that pertain to specific skin cluster attributes that must be connected.
                            For example: teshi_base_body_geo_bodyMechanics_skinCluster dictionary entry will return all of the connections from the skincluster to the multiMatrix nodes.
        Creates: 
        - self.variables, a dictionary of all the variables in the class
        """

        # Extract the first-level keys as attributes
        self.variables = dict()
        for key in json_dict:
            setattr(self, key, json_dict[key])
            self.variables[key] = json_dict[key]
####################################### Usage ########################################
# no usage, this class should be exclusively used with import_json_conn_map()
######################################################################################

def import_json_conn_map(file_path=None, filename_prefix='', suffix="MATRIX_CONNECTIONS"):
    """
    Imports a JSON file and returns its content as a dictionary.
    Args:
    - file_path (str): The path to the JSON file.
    Returns:
    - dict: The JSON content as a Python dictionary.
    """
    if not file_path:
        file_path = get_scene_dir()

    file_name = f"{filename_prefix}_{suffix}.json"
    full_file_path = os.path.join(file_path, file_name)
    print("\n")
    print(f"Imported from {full_file_path}")
    print("\n")

    with open(full_file_path, 'r') as json_file:
        return json.load(json_file)
        
####################################### Usage ########################################
# json_data = import_json_conn_map(file_path=r'C:\Users\harri\Documents\BDP\cha\teshi', filename_prefix='teshi_base_body_geo_bodyMechanics_skinCluster', suffix="MATRIX_CONNECTIONS")
# # Verbose output:
# json_attrs = JsonAttributes(json_data)
# for key in json_attrs.variables:
#     print(f'{key}:{json_attrs.variables[key]}')
######################################################################################

def connect_skins(connection_map, skincluster_name, dict_suffix):
    """
    Needs to save out a connection map to keep track of what all the connections originally were.
    CANNOT lose track of which connection goes to which index, this would permanently break the rig!
    If a mismatch does happen there would be a lot of trial and error to figure out which joint goes to which skincluster.matrix[index]

    Args:
    - connection_map (dict) - the
    "teshi_base_body_geo_bodyMechanics_skinCluster_MATRIX_MULT": {"M_neckHead00Localized_multMatrix.matrixSum": "matrix[0]"}
    """
    for key in connection_map:
        if f'{skincluster_name}{dict_suffix}' in key:
            connection_dict = connection_map[key]
            for key in connection_dict:
                cmds.connectAttr(key, connection_dict[key], force=True)
                # DELETE ME # Debugging
                # if "[39]" in connection_dict[key]:
                #     print("\n")
                #     print("KEY IS " + key)
                #     print("VALUE IS " + connection_dict[key])
                #     print("\n")
                #     print(f"The driver attr is {key} : The driven attr is {connection_dict[key]}")
                #     print(f"cmds.connectAttr({key}, {connection_dict[key]}, force=True)")

#Connects the joints to the skin so weights can be painted
def connect_skin_joints(connection_map, skincluster_name):
    connect_skins(connection_map, skincluster_name, dict_suffix="_ENV")

############################## connect_skin_joints Usage ####################################
# json_data = import_json_conn_map(file_path=r'C:\Users\harri\Documents\BDP\cha\teshi',filename_prefix='teshi_base_body_geo_bodyMechanics_skinCluster',suffix="MATRIX_CONNECTIONS")
# connect_skin_joints(connection_map=json_data,skincluster_name="teshi_base_body_geo_bodyMechanics_skinCluster")
#############################################################################################


#Connects the matrix mults to the skin so weights can be painted
def connect_matrix_mults(connection_map, skincluster_name):
    connect_skins(connection_map, skincluster_name, dict_suffix="_MATRIX_MULT")

####################################### connect_matrix_mults Usage ########################################
# json_data = import_json_conn_map(file_path=r'C:\Users\harri\Documents\BDP\cha\teshi',filename_prefix='teshi_base_body_geo_bodyMechanics_skinCluster',suffix="MATRIX_CONNECTIONS")
# connect_matrix_mults(connection_map=json_data,skincluster_name="teshi_base_body_geo_bodyMechanics_skinCluster")
###########################################################################################################


####################################### Full Connection Usage ########################################
# # export #
# connections_data = get_compound_attr_connect_map(node='teshi_base_body_geo_bodyMechanics_skinCluster', compound_attr='matrix')
# export_to_json(connections_data, filename_prefix='teshi_base_body_geo_bodyMechanics_skinCluster', file_path=r'C:\Users\harri\Documents\BDP\cha\teshi', suffix='MATRIX_CONNECTIONS')

# # import #
# json_data = import_json_conn_map(file_path=r'C:\Users\harri\Documents\BDP\cha\teshi',filename_prefix='teshi_base_body_geo_bodyMechanics_skinCluster',suffix="MATRIX_CONNECTIONS")

# # connect joints to skincluster #
# connect_skin_joints(connection_map=json_data, skincluster_name="teshi_base_body_geo_bodyMechanics_skinCluster")

# # connect matrixMultipliers to skincluster #
# connect_matrix_mults(connection_map=json_data, skincluster_name="teshi_base_body_geo_bodyMechanics_skinCluster")
###########################################################################################################
