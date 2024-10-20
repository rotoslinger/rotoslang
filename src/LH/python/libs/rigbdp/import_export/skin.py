# builtins
import importlib, os, sys, json

# third party
from maya import cmds
from maya import mel
# bdp
from rigbdp import decorator
from rigbdp.import_export import file as file_utils
from rigbdp.import_export import get_scene_dir
# from rigbdp import decorator

# reloads (DELETE_ME)
importlib.reload(decorator)
importlib.reload(file_utils)



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

def export_skinweight(path=None, geom="", skin_filter=[""], weight_data_path="weight_data", backup_dir="BAK"):
    # If a path is not given, just default to the path that the current scene is saved to
    if not path:
        path = get_scene_dir()

    # Filter skins
    filtered_skins = filter_skins(geom=geom, skin_filter=skin_filter)
    # Export filtered skins
    for skin in filtered_skins:
        filename= f"{skin}.json"

        filepath= os.path.join(path, weight_data_path)
        filepath = filepath.replace('\\', "/")

        # filepath= file_utils.join_and_norm(path, weight_data_path, filename) # func use os to join and normalize by operating system
        bakpath= file_utils.join_and_norm(path, weight_data_path, filename)
        file_utils.backup_file(full_path=bakpath)
        cmds.deformerWeights(f'{skin}.json', format = 'JSON', export = True,  deformer=skin, path = filepath)
####################################### Usage ########################################
# export_skins(geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################

def import_skin_weight(path=None, geom="", skin_filter=[""], weight_data_path="weight_data"):
    # If a path is not given, just default to the path that the current scene is saved to
    if not path:
        path = get_scene_dir()
    # Filter skins
    filtered_skins = filter_skins(geom=geom, skin_filter=skin_filter)
    # Export filtered skins
    for skin in filtered_skins:
        filepath= os.path.join(path, weight_data_path)
        filepath = filepath.replace('\\', "/")
        print(f'FILE PATH {filepath}')

        cmds.deformerWeights(skin + ".json", im = True, method = "index", deformer=skin, path = filepath)
        # weight normalization for imported weights. Must be updated or points are disfigured at rest.
        # to make sure normalization has worked, translate the global movement controller 1000 units away, rotate global scale, and see if the points are drifting. 
        cmds.skinPercent(skin, geom, normalize = True)
        cmds.skinCluster(skin , e = True, forceNormalizeWeights = True)
        # print("# Imported deformer weights from '" + path + skin + ".xml'.")
        print(f"# Imported deformer weights from '{filepath}/{skin}.json'.")
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

######################################################################################
######################################## End #########################################
######################################################################################











##########################################################################################
##################################### weight unlocking ###################################
##########################################################################################
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
    - file_path (str): The path to the JSON file_utils.
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

@decorator.restore_selection # --- annoying but we have to use this to preserve selection as cmds.file doesn't have an export arg that takes a list....
def export_obj(file_path, geometry):
        cmds.select(geometry)
        file_utils.backup_file(full_path=file_path)
        # arg v=0 will export with the obj version 0 which is widely supported by other software packages.  Probably not important, but whatever.
        # cmds.file(file_path, force=True, options='v=0', typ='OBJexport', exportSelected=True)
        cmds.file(file_path, force=True, options='groups=1;ptgroups=1;materials=0;smoothing=0;normals=1,mo=0,v=1', typ='OBJexport', pr=True,exportSelected=True)
        
def import_obj(file_path):
        cmds.file(file_path, i=True, typ='OBJ', ignoreVersion=True, ra=True, options='groups=1;ptgroups=1;materials=0;smoothing=0;normals=1,mo=0,v=1')  # You can specify additional options if needed
###########################################################################################################
##################################### not going to use this ###############################################
###########################################################################################################

@decorator.restore_selection
def export_animation_to_json(control_list=[], file_path=""):
    """Export animation keyframes from specified controls to a JSON file."""
    animation_data = {}
    if not file_path:
        file_path = get_scene_dir() + "rom.json"
    if not control_list:
        cmds.select('__EXPORT__CONTROLS')
        mel.eval('CBselectionChanged;')
        control_list = cmds.ls(sl=True)

    for control in control_list:
        if cmds.objExists(control):
            keyframes = cmds.keyframe(control, query=True, timeChange=True)
            if keyframes:
                animation_data[control] = {}
                for key in keyframes:
                    value = cmds.getAttr(control + '.translate')
                    animation_data[control][key] = {
                        'translateX': cmds.getAttr(control + '.translateX', time=key),
                        'translateY': cmds.getAttr(control + '.translateY', time=key),
                        'translateZ': cmds.getAttr(control + '.translateZ', time=key),
                        'rotateX': cmds.getAttr(control + '.rotateX', time=key),
                        'rotateY': cmds.getAttr(control + '.rotateY', time=key),
                        'rotateZ': cmds.getAttr(control + '.rotateZ', time=key)
                    }

    # Write the animation data to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(animation_data, json_file, indent=4)
    print(f'Animation data exported to {file_path}')

####################################################### Example usage ##########################################################
# controls = ['M_spineChestFkGimbal_ctrl', 'M_spineDrivenIk02_ctrl', 'L_handReverseRollFinger_ctrl', 'M_spineDriverLastTangent_ctrl', 'R_handPinky01_ctrl', 'M_neckHeadIk00_ctrl', 'R_footReverseRollHeel_ctrl', 'L_handThumb00Gimbal_ctrl', 'L_clavicle_ctrl', 'L_handThumb02_ctrl', 'R_ikArmHandleGimbal_ctrl', 'M_spineBellyIk_ctrl', 'L_handIndex00_ctrl', 'R_handIndex01Gimbal_ctrl', 'L_ikLegHandle_ctrl', 'L_fkArm01Gimbal_ctrl', 'R_handRing01Gimbal_ctrl', 'M_neckHeadFk00Gimbal_ctrl', 'M_neckHeadGimbal_ctrl', 'L_ikArmPV_ctrl', 'L_handReverseBankOutGimbal_ctrl', 'R_fkLeg01_ctrl', 'R_footReverseRollToe_ctrl', 'R_handThumb00Gimbal_ctrl', 'L_ikArmRoot_ctrl', 'L_handIndex02Gimbal_ctrl', 'R_armUpperBendy_ctrl', 'L_handMiddle01Gimbal_ctrl', 'L_fkArm00Gimbal_ctrl', 'L_armSettings_ctrl', 'R_ikLegHandle_ctrl', 'R_ikArmPV_ctrl', 'R_handThumb02_ctrl', 'L_handIndex01_ctrl', 'R_clavicle_ctrl', 'R_handPinky03Gimbal_ctrl', 'L_legSlide_ctrl', 'L_hand_ctrl', 'L_footReverseRollHeelGimbal_ctrl', 'M_all_ctrl', 'M_spineChestIkOffsetPivot_ctrl', 'M_spineBellyFkGimbal_ctrl', 'L_legUpperBendy_ctrl', 'M_spineDriven03Tangent01_ctrl', 'R_handReverseBankIn_ctrl', 'L_footToeGimbal_ctrl', 'R_handReverseBankOutGimbal_ctrl', 'M_spineBreathBelly_ctrl', 'L_footReverseBankIn_ctrl', 'M_spineDrivenIk03_ctrl', 'L_ikLegRoot_ctrl', 'R_handIndex01_ctrl', 'L_fkLeg02Gimbal_ctrl', 'R_handIndex03Gimbal_ctrl', 'L_footReverseBankOutGimbal_ctrl', 'R_handIndex02_ctrl', 'R_handPinky00_ctrl', 'L_foot_ctrl', 'L_handMiddle01_ctrl', 'M_spineLocalHip_ctrl', 'M_spineRoot_ctrl', 'M_neckHeadFk00_ctrl', 'M_spineDriven02Tangent00_ctrl', 'L_footReverseRollToeGimbal_ctrl', 'R_handThumb01Gimbal_ctrl', 'L_handReverseRollBallGimbal_ctrl', 'R_handThumb00_ctrl', 'L_handPinky03_ctrl', 'L_handRing03_ctrl', 'R_foot_ctrl', 'L_armUpperBendy_ctrl', 'R_legLowerBendy_ctrl', 'R_armSettings_ctrl', 'M_spineDriven04Tangent00_ctrl', 'L_footLollipop_ctrl', 'M_world_ctrl', 'R_footToeGimbal_ctrl', 'L_handLollipop_ctrl', 'L_handPinky03Gimbal_ctrl', 'L_handTipSmart_ctrl', 'R_footReverseBankInGimbal_ctrl', 'R_handRing01_ctrl', 'M_spineBellyFk_ctrl', 'R_armSlide_ctrl', 'L_handPinky00Gimbal_ctrl', 'M_spineRootGimbal_ctrl', 'M_spineDrivenIk01_ctrl', 'R_handMiddle01_ctrl', 'R_legUpperBendy_ctrl', 'L_handReverseRollHeelGimbal_ctrl', 'L_handRing03Gimbal_ctrl', 'L_handPinky00_ctrl', 'L_handMiddle02Gimbal_ctrl', 'R_handReverseRollBallGimbal_ctrl', 'L_footReverseRollToe_ctrl', 'L_legLowerBendy_ctrl', 'M_neckHeadIk01_ctrl', 'R_handMiddle00Gimbal_ctrl', 'R_fkLeg02Gimbal_ctrl', 'M_spineDriverFirstTangent_ctrl', 'R_fkArm02_ctrl', 'L_handRing00Gimbal_ctrl', 'L_handIndex01Gimbal_ctrl', 'R_handRing03_ctrl', 'L_footReverseRollBallGimbal_ctrl', 'R_handIndex00_ctrl', 'L_handMiddle02_ctrl', 'L_handMiddle03_ctrl', 'R_hand_ctrl', 'R_handRing02Gimbal_ctrl', 'R_fkArm01_ctrl', 'R_handReverseRollFingerGimbal_ctrl', 'R_handMiddle00_ctrl', 'L_handMiddle03Gimbal_ctrl', 'M_layoutSub_ctrl', 'L_handIndex03Gimbal_ctrl', 'M_spineChestIk_ctrl', 'R_fkArm02Gimbal_ctrl', 'L_armSlide_ctrl', 'R_fkArm00Gimbal_ctrl', 'R_fkLeg00Gimbal_ctrl', 'R_handReverseBankInGimbal_ctrl', 'M_layout_ctrl', 'R_footReverseBankIn_ctrl', 'L_handIndex00Gimbal_ctrl', 'L_ikArmHandle_ctrl', 'R_footReverseRollBall_ctrl', 'R_handThumb02Gimbal_ctrl', 'R_ikLegPV_ctrl', 'R_handReverseRollHeel_ctrl', 'L_handPinky01_ctrl', 'R_handRing02_ctrl', 'M_spineDriven02Tangent01_ctrl', 'L_handReverseBankOut_ctrl', 'R_handLollipop_ctrl', 'M_spineChestFk_ctrl', 'R_handThumb01_ctrl', 'R_fkLeg02_ctrl', 'L_handMiddle00_ctrl', 'L_handRing02_ctrl', 'M_spineUpperChestGimbal_ctrl', 'R_handPinky01Gimbal_ctrl', 'R_armLowerBendy_ctrl', 'M_spineUpperChest_ctrl', 'M_neckHeadSettings_ctrl', 'R_footToe_ctrl', 'L_fkLeg02_ctrl', 'L_ikLegPV_ctrl', 'M_spineDriven01Tangent01_ctrl', 'L_handReverseBankInGimbal_ctrl', 'L_handRing01_ctrl', 'R_handIndex03_ctrl', 'M_spineBreathChest_ctrl', 'R_handMiddle01Gimbal_ctrl', 'L_fkLeg00_ctrl', 'R_handMiddle02_ctrl', 'R_handPinky02_ctrl', 'M_spineDriven03Tangent00_ctrl', 'R_handPinky03_ctrl', 'R_footLollipop_ctrl', 'L_handRing00_ctrl', 'R_fkArm01Gimbal_ctrl', 'L_fkArm01_ctrl', 'R_handReverseRollFinger_ctrl', 'L_handThumb02Gimbal_ctrl', 'M_spineBellyIkGimbal_ctrl', 'L_fkArm00_ctrl', 'R_footReverseRollBallGimbal_ctrl', 'R_legSettings_ctrl', 'L_ikLegHandleGimbal_ctrl', 'R_fkArm00_ctrl', 'L_armLowerBendy_ctrl', 'R_ikArmHandle_ctrl', 'L_handReverseRollBall_ctrl', 'L_fkLeg00Gimbal_ctrl', 'L_handIndex02_ctrl', 'M_spineHipFkGimbal_ctrl', 'R_handMiddle03Gimbal_ctrl', 'R_handIndex00Gimbal_ctrl', 'L_footReverseRollBall_ctrl', 'L_fkArm02_ctrl', 'L_handPinky01Gimbal_ctrl', 'L_ikArmHandleGimbal_ctrl', 'M_spineRootOffsetPivot_ctrl', 'M_spineChestFkOffsetPivot_ctrl', 'R_handReverseRollBall_ctrl', 'R_footReverseBankOut_ctrl', 'L_handPinky02_ctrl', 'L_handThumb01Gimbal_ctrl', 'L_fkLeg01_ctrl', 'R_handIndex02Gimbal_ctrl', 'R_footReverseRollToeGimbal_ctrl', 'R_handRing00Gimbal_ctrl', 'M_spineLocalHipGimbal_ctrl', 'M_spineDriven00Tangent01_ctrl', 'L_fkArm02Gimbal_ctrl', 'R_fkLeg00_ctrl', 'L_handRing02Gimbal_ctrl', 'R_fkLeg01Gimbal_ctrl', 'L_legSettings_ctrl', 'L_handPinky02Gimbal_ctrl', 'R_legSlide_ctrl', 'R_handMiddle02Gimbal_ctrl', 'L_handThumb01_ctrl', 'L_footToe_ctrl', 'R_handRing00_ctrl', 'L_handMiddle00Gimbal_ctrl', 'R_handReverseBankOut_ctrl', 'L_footReverseBankOut_ctrl', 'R_footReverseBankOutGimbal_ctrl', 'R_handPinky02Gimbal_ctrl', 'R_ikLegRoot_ctrl', 'L_footReverseRollHeel_ctrl', 'R_handReverseRollHeelGimbal_ctrl', 'R_handRing03Gimbal_ctrl', 'M_spineHipIk_ctrl', 'L_footReverseBankInGimbal_ctrl', 'M_spineHipIkGimbal_ctrl', 'M_spineChestIkGimbal_ctrl', 'R_ikArmRoot_ctrl', 'L_handReverseRollHeel_ctrl', 'R_handMiddle03_ctrl', 'R_footReverseRollHeelGimbal_ctrl', 'M_spineHipFk_ctrl', 'M_spineDriven01Tangent00_ctrl', 'L_handReverseBankIn_ctrl', 'L_handThumb00_ctrl', 'L_handIndex03_ctrl', 'R_handTipSmart_ctrl', 'L_handRing01Gimbal_ctrl', 'M_neckHead_ctrl', 'L_handReverseRollFingerGimbal_ctrl', 'R_ikLegHandleGimbal_ctrl', 'L_fkLeg01Gimbal_ctrl', 'R_handPinky00Gimbal_ctrl']
# path=r'C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD\animtest\anim.json'
# export_animation_to_json(controls, r'C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD\animtest\anim.json')
####################################################### Example usage ##########################################################

def import_animation_from_json(file_path):
    """Import animation keyframes from a JSON file into specified controls."""
    with open(file_path, 'r') as json_file:
        animation_data = json.load(json_file)
    if not file_path:
        file_path = get_scene_dir()
    for control, keyframes in animation_data.items():
        if cmds.objExists(control):
            for time, attrs in keyframes.items():
                cmds.setKeyframe(control, time=time, attribute='translateX', value=attrs['translateX'])
                cmds.setKeyframe(control, time=time, attribute='translateY', value=attrs['translateY'])
                cmds.setKeyframe(control, time=time, attribute='translateZ', value=attrs['translateZ'])
                cmds.setKeyframe(control, time=time, attribute='rotateX', value=attrs['rotateX'])
                cmds.setKeyframe(control, time=time, attribute='rotateY', value=attrs['rotateY'])
                cmds.setKeyframe(control, time=time, attribute='rotateZ', value=attrs['rotateZ'])

    print(f'Animation data imported from {file_path}')

####################################################### Example usage ##########################################################
# Example usage
# import_animation_from_json(path)
####################################################### Example usage ##########################################################
