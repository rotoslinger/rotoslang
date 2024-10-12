import os, importlib
import maya.cmds as cmds
from rigbdp.build import file as file_utils
importlib.reload(file_utils)

class RigBuilder:
    def __init__(self, local_build_dir, src_rig_file, debug=False):
        self.local_build_dir = local_build_dir
        self.src_rig_file = src_rig_file
        self.data_dirs = ["connection_data", "pivot_data", "model_data", "weight_data", "corrective_data", "build"]
        self.debug = debug


    def new_scene(self, save_file=True):
        """
        Creates a new scene, names the file, saves it, and versions it safely.

        Args:
            save_file (bool): Whether to save the file on creation. Defaults to True.
        """
        self.__initialize_directories() # --- makes sure the directories exist, create instance variables of each. 
        tmp_file_name = os.path.basename(self.src_rig_file) # --- extract filename from path
        self.file_name = file_utils.asset_version_increment(tmp_file_name) # --- add to the version v004 -> v005
        file_path = os.path.join(self.build_dir, self.file_name)

        # --- If the file already exists back it up
        file_utils.backup_file(full_path=file_path)
        
        # Create a new Maya scene
        cmds.file(new=True, force=True)

        # Save the file if the save_file flag is True
        if save_file:
            cmds.file(rename=file_path)
            cmds.file(save=True, type='mayaAscii')    
        return file_path

    def import_rig(self):
        """
        Imports the Minimo rig and flattens namespaces.
        """
        # Import the rig
        cmds.file(self.src_rig_file, i=True, namespace=":", preserveReferences=True)
        # Flatten namespaces (remove them)
        cmds.namespace(set=':')
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
        for ns in namespaces:
            if ns not in ['UI', 'shared']:
                cmds.namespace(force=True, moveNamespace=(ns, ':'))
                cmds.namespace(removeNamespace=ns)

    def import_pivots(self, pivot_data):
        """
        Imports pivots from a given data source (e.g., JSON dictionary).
        Args:
            pivot_data (dict): A dictionary or JSON file containing pivot information.
        Postscript:
            Users can add custom scripts that run after pivot import.
        """
        # this is a placeholder for a method that imports pivot data from the pivot_data directory
        # pivots will be set by moving the objects with xform (or whatever)
        
        # dictionary will be something along the lines of:
        pivot_data = {"root|L_fkArm02_offset" : ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz' ]}


    def import_model(self, filepath):
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
        # Specifing for clarity: the i flag stands for import, there is no nice name for the flag because of python
        # mo=0 refers to merge object.  We do not want maya to merge all of the data in the obj so we will set it to 'false'
        imported_nodes = cmds.file(filepath, i=True, type='OBJ', returnNewNodes=True, options="mo=0")

        # Find the geometry and create a blendshape (user to modify based on naming convention)
        blendshape_nodes = []
        rig_geo = "rigGeometry"  # Placeholder: update to your rig geometry name

        for node in imported_nodes:
            if cmds.nodeType(node) == 'mesh':
                blendshape_node = cmds.blendShape(node, rig_geo, origin="local")[0]
                blendshape_nodes.append(blendshape_node)

        return blendshape_nodes

    def import_weight(self, filepath):
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

    def import_correctives(self, filepath):
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

    def __initialize_directories(self):
        # For debugging, this method can be called from outside the class by using builder._RigBuilder__initialize_directories()

        # Call the standalone function and get the dynamically created directory variables
        dir_vars = file_utils.create_folder_structure(self.local_build_dir, dirs=self.data_dirs, debug=self.debug)

        # The next section dynamically creates the instance vars below.
        # I am adding here to give them more visibility
        self.connection_data_dir=""
        self.connection_data_bak_dir=""
        self.pivot_data_dir=""
        self.pivot_data_bak_dir=""
        self.model_data_dir=""
        self.model_data_bak_dir=""
        self.weight_data_dir=""
        self.weight_data_bak_dir=""
        self.corrective_data_dir=""
        self.corrective_data_bak_dir=""
        self.build_dir=""
        self.build_bak_dir=""

        # Dynamically set the returned directory variables as instance variables
        for var_name, path in dir_vars.items():
            setattr(self, var_name, path)  # Set as instance variable

        # Now all the directory variables like self.connection_data_dir, self.pivot_data_dir etc. are initialized
        if self.debug:
            print("\n")
            print('### initialized variables ###')
            for var_name in dir_vars.keys():
                print(f'self.{var_name}')




# # Create an instance of the RigBuilder
# builder = RigBuilder(local_build_dir=r"C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD",
#                      src_rig_file = r"C:\Users\harri\Documents\BDP\cha\teshi\teshi_RIG_200_v005.ma",
#                      )

# # Create folder structure
# builder._RigBuilder__initialize_directories()

# # Create a new scene
# builder.new_scene(save_file=True)

# # Import rig, pivots, model, weights, and correctives as needed
# builder.import_rig(filepath="path_to_rig")

# builder.import_pivots(pivot_data={...})
# builder.import_model(filepath="path_to_model")
# builder.import_weight(filepath="path_to_weight_file")
# builder.import_correctives(filepath="path_to_corrective_shapes")
