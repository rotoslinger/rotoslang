import os, importlib
from maya import cmds, mel
from rigbdp.import_export import file as file_utils
from rigbdp.import_export import mayafile
importlib.reload(file_utils)
importlib.reload(mayafile)

class RigBuilder:
    def __init__(self, local_build_dir, src_rig_file=None, debug=False, backup=True):
        if not src_rig_file:
            pass
        self.local_build_dir = local_build_dir
        self.src_rig_file = src_rig_file
        self.data_dirs = ["connection_data", "pivot_data", "model_data", "weight_data", "corrective_data", "build"]
        self.debug = debug
        self.backup = backup
        # listing here for readability
        # dynamically created and set by self.__initialize_directories
        self.build_output_bak_dir=''
        self.build_output_dir=''
        self.connection_data_bak_dir=''
        self.connection_data_dir=''
        self.corrective_data_bak_dir=''
        self.corrective_data_dir=''
        self.data_dir=''
        self.model_data_bak_dir=''
        self.model_data_dir=''
        self.pivot_data_bak_dir=''
        self.pivot_data_dir=''
        self.rom_data_bak_dir=''
        self.rom_data_dir=''
        self.src_dir=''
        self.weight_data_bak_dir=''
        self.weight_data_dir=''
        self.__initialize_directories() # --- makes sure the directories exist, create instance variables of each.


    def new_scene(self, save_file=True):
        """
        Creates a new scene, names the file, saves it, and versions it safely.

        Args:
            save_file (bool): Whether to save the file on creation. Defaults to True.
        """
        if not self.src_rig_file:
            self.src_rig_file = mayafile.files_in_path_filtered(self.src_dir, ['.ma', '.mb'])[0]
            # print('SOURCE DATA DIRECTORY : ', self.src_dir)
        tmp_file_name = os.path.basename(self.src_rig_file) # --- extract filename from path
        self.file_name = file_utils.asset_version_increment(tmp_file_name) # --- add to the version v004 -> v005
        self.src_file_path = os.path.join(self.build_output_dir, self.file_name)
        if self.debug:
            print('The source rig is located at : ', self.src_rig_file)
            print('The rig file has been created at  : ', self.src_file_path)

        # If the file already exists and self.backup is True, back it up
        if self.backup:
            output_dir_back, backed_up_files = file_utils.backup_rig_build(self.build_output_dir, backup_dir_name="BAK")

            #file_utils.backup_files_in_dir(path=self.build_output_dir)

        # # Delete the build data dir (you've already backed it up, and all of the source data still exists)
        # get all files in path except BAK
        delete_paths = file_utils.all_files_in_path_except(self.build_output_dir, except_files=['BAK'])
        print('DELETE PATHS : ', delete_paths)
        for path in delete_paths:
            print('PATH : ', path)
            # delete files
            if os.path.isfile(path): file_utils.safe_delete_file_maya(path, debug=False)
            # delete build_data directory
            if os.path.isdir(path) and 'build_data' in path: file_utils.safe_dir_delete_maya(path, debug=False)

        # Copy data_dirs
        self.data_dirs = file_utils.all_files_in_path_except(self.data_dir)
        for data_dir in self.data_dirs:
            head, tail = os.path.split(data_dir)
            print("DIR TO BE COPIED FROM : ", tail) 
            local_data_dir = file_utils.create_dir_verbose(os.path.join(self.build_output_dir, tail))
            print("LOCAL DATA DIR CREATED : ", local_data_dir) 

            file_utils.copy_files_except(source_dir=data_dir, destination_dir=local_data_dir)

        # Create a new Maya scene
        cmds.file(new=True, force=True)
        # Save the file if the save_file flag is True
        if save_file:
            cmds.file(rename=self.src_file_path)
            cmds.file(save=True, type='mayaAscii')
        return self.src_file_path

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


    def import_model(self, file_path):
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
        imported_nodes = cmds.file(file_path, i=True, type='OBJ', returnNewNodes=True, options="mo=0")

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

    def import_correctives(self, filepaths=None):
        """
        Imports corrective shapes for the rig.

        Args:
            filepath (str): The file path to the corrective shapes.
        Postscript:
            Users can add custom scripts that run after corrective shapes import.
        """
        if not filepaths:
            filepaths = mayafile.files_in_path_filtered(self.corrective_data_dir, 'mel')
            print(filepaths)
        for file in filepaths:
            print(f'source "{file}";')

            if os.path.isfile(file):
                mel.eval(f'source "{file}";')
            else:
                cmds.warning("The provided corrective shapes file path does not exist.")

    def __initialize_directories(self):
        # For debugging, this method can be called from outside the class by using builder._RigBuilder__initialize_directories()

        # Call the standalone function and get the dynamically created directory variables
        self.dir_vars = file_utils.create_asset(self.local_build_dir, debug=self.debug)
        # Sort in alphabetical order (thank you python 3.7!)
        self.dir_vars = {key: self.dir_vars[key] for key in sorted(self.dir_vars)}

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
        self.rom_data_dir=""
        self.rom_data_bak_dir=""
        self.src_data_dir=""
        self.build_output_dir=""
        self.build_output_bak_dir=""

        # Dynamically set the returned directory variables as instance variables
        for var_name, path in self.dir_vars.items():
            setattr(self, var_name, path)  # Set as instance variable

        # Important to do even when not debugging as these instance variables are being created dynamically
        print("\n")
        print('########## instantiated attrs ##########')
        for var_name in self.dir_vars.keys():
            print(f"self.{var_name}=''")
        print('########################################')

        # Now all the directory variables like self.connection_data_dir, self.pivot_data_dir etc. are initialized
        if self.debug:
            self.print_dir_vars()


    def print_dir_vars(self):
        print("\n")
        print('############################################# attr vals ###########################################')
        for var_name in self.dir_vars.keys():
            print(f'self.{var_name} : {self.dir_vars[var_name]}' )
        print('###################################################################################################')
        print("\n")



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

# # builder.import_pivots(pivot_data={...})
# # builder.import_model(filepath="path_to_model")
# # builder.import_weight(filepath="path_to_weight_file")
# builder.import_correctives(filepath="path_to_corrective_shapes")
############################################################################################################################################################
# import importlib
# from rigbdp.build import rigbuild
# from rigbdp.import_export import file as file_utils
# importlib.reload(rigbuild)
# importlib.reload(file_utils)

# local_build_dir=r"C:\Users\harri\Documents\BDP\cha\build_test_dir"

# builder = rigbuild.RigBuilder(local_build_dir=r"C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD",
#                                 src_rig_file = r"C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD\teshi_RIG_200_v006.ma",debug=True)
# # Create folder structure
# builder._RigBuilder__initialize_directories()

# builder.new_scene()
# builder.import_rig()

############################################################################################################################################################
