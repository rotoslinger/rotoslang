import os
import time
import maya.cmds as cmds

################################# Pre Build Functions ################################
######################################################################################

def create_folder_structure(dir_path, dirs=["model_data", "pivot_data", "weight_data", "corrective_data", "build"]):
    """
    Creates specific directories within the provided parent directory.
    Args:
        dir_path (str): The path to the parent directory where the new directories will be created.
    Postscript:
        Users can add custom scripts that run after directory creation.
    """
    # Create each directory within the parent directory

    for dir_name in dirs:
        tmp_dir_path = os.path.join(dir_path, dir_name)
        tmp_bak_path = os.path.join(tmp_dir_path, "BAK")
        try:
            # os.makedirs(dir_path, exist_ok=True)  # Creates the directory and ignores error if it already exists
            print(f"Created directory: {tmp_dir_path}")
            print(f"Created directory: {tmp_bak_path}")
        except Exception as e:
            print(f"Failed to create directory {tmp_dir_path}: {e}")
################################### Usage ###################################
# parent_dir_path = r"C:\Users\harri\Documents\BDP\dummy_test_dir"
# create_folder_structure(parent_dir_path)
#############################################################################

#-------------------------------------------------------------------------------------

######################################################################################
################################# Build Functions ####################################
######################################################################################


def new_scene(char_name, working_dir, save_file=True):
    """
    Creates a new scene, names the file, saves it, and versions it safely.

    Args:
        char_name (str): The non-versioned character name used as the file name prefix.
        working_dir (str): The directory where the Minimo rig is stored.
        save_file (bool): Whether to save the file on creation. Defaults to True.

    Postscript:
        Users can add custom code here that needs to run prior to every other step in the build process.
    """
    # Create a new Maya scene
    cmds.file(new=True, force=True)
    
    # Create the 'builds' directory if it doesn't exist
    builds_dir = os.path.join(working_dir, 'builds')
    if not os.path.exists(builds_dir):
        os.makedirs(builds_dir)
    
    # Generate timestamp and file name
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_name = f"{char_name}_build_{timestamp}.ma"  # Save as mayaAscii
    file_path = os.path.join(builds_dir, file_name)
    
    # Save the file if the save_file flag is True
    if save_file:
        cmds.file(rename=file_path)
        cmds.file(save=True, type='mayaAscii')    
    return file_path


def import_rig(filepath):
    """
    Imports the Minimo rig and flattens namespaces.

    Args:
        filepath (str): The full filepath of the Minimo rig, including the file name. Can be local or global.

    Postscript:
        Users can add custom scripts such as preparing for placing pivots, adding connections, or breaking connections.
    """
    # Import the rig
    cmds.file(filepath, i=True, namespace=":", preserveReferences=True)
    
    # Flatten namespaces (remove them)
    cmds.namespace(set=':')
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
    for ns in namespaces:
        if ns not in ['UI', 'shared']:
            cmds.namespace(force=True, moveNamespace=(ns, ':'))
            cmds.namespace(removeNamespace=ns)


def import_pivots(pivot_data):
    """
    Imports pivots from a given data source (e.g., JSON dictionary).

    Args:
        pivot_data (dict): A dictionary or JSON file containing pivot information.

    Postscript:
        Users can add custom scripts that run after pivot import.
    """
    if not isinstance(pivot_data, dict):
        cmds.warning("pivot_data must be a dictionary.")
        return

    for obj, pivot in pivot_data.items():
        if cmds.objExists(obj):
            cmds.xform(obj, piv=pivot, ws=True)


def import_model(filepath):
    """
    Imports a model and plugs it into the rig as a blendshape.

    Args:
        filepath (str): The full filepath to the model.

    Returns:
        list: A list of blendshape nodes created.

    Postscript:
        Users can add custom scripts that happen after model import.
    """
    # Import the model
    imported_nodes = cmds.file(filepath, i=True, returnNewNodes=True)
    
    # Find the geometry and create a blendshape (user to modify based on naming convention)
    blendshape_nodes = []
    rig_geo = "rigGeometry"  # Placeholder: update to your rig geometry name
    
    for node in imported_nodes:
        if cmds.nodeType(node) == 'mesh':
            blendshape_node = cmds.blendShape(node, rig_geo, origin="local")[0]
            blendshape_nodes.append(blendshape_node)
        
    return blendshape_nodes


def import_weight(filepath):
    """
    Reconnects joints to their skin clusters, imports saved weights, and reconnects joints to the Minimo rig.

    Args:
        filepath (str): The file path to the saved skin weights.

    Postscript:
        Users can add custom scripts that run after weights import.
    """
    if os.path.isfile(filepath):
        # Example of importing weights (user to customize based on format)
        cmds.deformerWeights(filepath, im=True)
    else:
        cmds.warning("The provided weight file path does not exist.")


def import_correctives(filepath):
    """
    Imports corrective shapes for the rig.

    Args:
        filepath (str): The file path to the corrective shapes.

    Postscript:
        Users can add custom scripts that run after corrective shapes import.
    """
    if os.path.isfile(filepath):
        # Example of importing corrective shapes (user to customize)
        cmds.file(filepath, i=True, returnNewNodes=True)
    else:
        cmds.warning("The provided corrective shapes file path does not exist.")

#-------------------------------------------------------------------------------------

######################################## Build #########################################

###################################### data ######################################
# These 
char_name = "MinimoCharacter"
working_dir = "path/to/your/working/directory"
rig_filepath = "path/to/your/minimo_rig.ma"
pivot_data = {
    "pivot1": (0, 0, 0),
    "pivot2": (1, 1, 1),
}
model_filepath = "path/to/your/model.obj"
weight_filepath = "path/to/your/skin_weights.xml"
corrective_filepath = "path/to/your/correctives.ma"
##################################################################################

"""
#------------------------------------ Build Prep --------------------------------------
create_folder_structure(working_dir, dirs=["model_data", "pivot_data", "weight_data", "corrective_data", "build"])
#--------------------------------------------------------------------------------------



#------------------------------------ New Scene ---------------------------------------
# Step 1: Create a new scene
new_scene(char_name, working_dir)

# Step 1.5: post-scripts
'''postscripts running'''
#--------------------------------------------------------------------------------------

#------------------------------------ Import Rig --------------------------------------
# Step 2: Import the Minimo rig
import_rig(rig_filepath)
# Step 2.5:
'''postscripts running'''
#--------------------------------------------------------------------------------------

#---------------------------------- Import Pivots -------------------------------------
# Step 3: Import pivots
import_pivots(pivot_data)
# Step 3.5:
'''postscripts running'''
#--------------------------------------------------------------------------------------

#----------------------------------- Import Model -------------------------------------
# Step 4: Import the model as a blendshape
import_model(model_filepath)
# Step 4.5:
'''postscripts running'''
#--------------------------------------------------------------------------------------

#----------------------------------- Import Weight ------------------------------------
# Step 5: Import weights
import_weight(weight_filepath)
# Step 5.5:
'''postscripts running'''
#--------------------------------------------------------------------------------------

#-------------------------------- Import Correctives ----------------------------------
# Step 6: Import corrective shapes
import_correctives(corrective_filepath)
# Step 6.5: 
'''postscripts running'''
#--------------------------------------------------------------------------------------

print("All operations completed successfully.")
"""