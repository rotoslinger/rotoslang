# builtins
import importlib, time, os, shutil, sys, re, json
from functools import wraps

# third party
from maya import cmds
import decorator
importlib.reload(decorator)
DELIMITER = os.path.sep  # Use the appropriate path delimiter for the OS

# Get the full path of the current scene
#################################### Usage ####################################
'''
----This module is for native python pathing and file related functions----
    Any functions that rely on the maya library functions go in mayafile.
    Usage examples sometimes rely on maya cmds
'''
###############################################################################


def join_and_norm(*paths):
    # a builtin helper function to keep code brief 
    # Simple way to join and clean up path name.  Important because we could be working multi platform.
    paths = os.path.join(*paths)
    return os.path.normpath(paths)
# no usage, this is a builtin helper function, it should not be used by itself
# ################################### join_and_norm Usage ########################################
# dir=r"drive/mangled\path//"
# file=r"test.txt"
# full_path = join_and_norm(dir, file)
# print(full_path) # --- returns: drive/mangled/path/test.txt
# ################################################################################################


def generate_timestamp():
    t = time.localtime()
    # Creating a timestamp in a human-readable format: YYYY-MM-DD_HH-MM-SS
    return "{0}-{1}-{2}_{3}-{4}-{5}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

def generate_backup_filename(filepath, filename, backup_dir_name='BAK'):
    filepath = os.path.normpath(f"{filepath}{DELIMITER}{backup_dir_name}")
    # Ensure the directory exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The directory '{filepath}' does not exist.")
    base_name, ext = os.path.splitext(filename)
    # Find existing versions
    existing_versions = []
    pattern = re.compile(rf"{re.escape(base_name)}___v(\d{{3}})___.*{re.escape(ext)}")
    # Check files in the directory and extract version numbers
    for file in os.listdir(filepath):
        match = pattern.match(file)
        if match:
            existing_versions.append(int(match.group(1)))  # Append the extracted version number
    # Determine the next version number
    version = max(existing_versions, default=0) + 1  # Start from v001 if no versions exist
    timestamp = generate_timestamp()
    backup_filename = os.path.join(filepath, f"{base_name}___v{version:03d}___{timestamp}{ext}")
    return backup_filename
################################### generate_backup_filename Usage ###################################
# filepath = r"C:\Users\harri\Documents\BDP\cha\jsh"
# filename = "jsh_base_body_geo_upperFace_skinCluster.xml"
# backup_filename = generate_backup_filename(filepath=filepath, filename=filename)
######################################################################################################


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
    return filepath
################################### check_parent_directory Usage ###########################################
# from rigbdp.save.export import get_scene_dir
# scene_dir = get_scene_dir()
# filename = "jsh_base_body_geo_upperFace_skinCluster.xml"
# check_parent_directory(filepath=scene_dir, debug=True)
### --- If there is no folder called BAK in the directory, it will be created
### --- This will print out: New directory created @ C:\Users\harri\Documents\BDP\cha\jsh\BAK
############################################################################################################


def OLD_backup_file(filepath, filename):
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
############################# backup_file Usage ################################
# filepath = r"C:\Users\harri\Documents\BDP\cha\jsh"
# filename = "jsh_base_body_geo_upperFace_skinCluster.xml"
# backup_file(filepath=filepath, filename=filename)
######################################################################################


def backup_file(full_path, backup_dir_name="BAK"):
    if not os.path.exists(full_path):
        print(f'Backup file could not be created, {full_path}, does not exist.')
        return
    path, filename = os.path.split(full_path)

    check_parent_directory(filepath=path)
    backup_name = generate_backup_filename(filepath=path, filename=filename, backup_dir_name=backup_dir_name)
    shutil.copy(full_path, backup_name)
    print(f'>>Backing up file ---> {filename}\n>>File has been saved here ---> {backup_name}')
############################# backup_file Usage ################################
# filepath = r"C:\Users\harri\Documents\BDP\cha\jsh\jsh_base_body_geo_upperFace_skinCluster.xml"
# backup_dir = "jsh_base_body_geo_upperFace_skinCluster.xml"
# backup_file(filepath=filepath, filename=filename)
######################################################################################


def import_files_as_dict(file_paths):
    """
    Import the contents of given file paths as dictionaries with filenames as keys.
    Args:
        file_paths (list): List of file paths to import.
    Returns:
        dict: A dictionary where keys are the filenames (without extensions or paths),
              and values are the contents of the files.
    """
    imported_data = {}
    for file_path in file_paths:
        # Strip path and extension from filename
        filename = os.path.splitext(os.path.basename(file_path))[0]
        # Open and read the file
        with open(file_path, 'r') as file:
            try:
                # Assuming files are in JSON format
                imported_data[filename] = json.load(file)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {file_path}")
    return imported_data
####################################### Usage ########################################
# # Example usage:
# file_paths = [
#     "/path/to/project/weight_data/example1.json",
#     "/path/to/project/weight_data/example2.json"
# ]
# imported_dict = import_files_as_dict(file_paths)
# print("Imported Data:", imported_dict)
######################################################################################


def asset_version_increment(filename):
    '''Increments the version number in the given filename by 1.'''
    # Regular expression to match 'v' followed by a 3-digit version number
    version_pattern = r'(v)(\d{3})'
    # Search for the version pattern in the filename
    match = re.search(version_pattern, filename)
    if match:
        # Extract the current version number
        current_version = int(match.group(2))
        # Increment the version number by 1
        new_version = current_version + 1
        # Replace the old version with the new version, keeping the 'v' and formatting to 3 digits
        new_filename = re.sub(version_pattern, f'v{new_version:03}', filename)
        return new_filename
    else:
        raise NameError('Filename does not contain a valid version number in the format "vXXX". Returning None')
############################# Full Backup Utils Usage ################################
# filename = 'jeremy_RIG_200_v007.ma'
# new_filename = asset_version_increment(filename)
# print(new_filename)  # Output: 'jeremy_RIG_200_v008.ma'
######################################################################################


def create_dir_verbose(directory_path, debug=False):
    directory_path = os.path.normpath(directory_path)
    if os.path.isdir(directory_path):
        if debug:
            print(f'Directory "{directory_path}" already exists.')
    else:
        os.makedirs(directory_path)
        if debug:
            print(f"Created directory: {directory_path}")
# ################################### create_dir_verbose Usage ########################################
# directory=r"C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD\test_directory_to_create"
# create_dir_verbose(directory_path=directory, debug=True)
# ##########################################################################################################

def create_dir_structure(directory, debug=False, add_backup_dir=False, dirs=None, ):
    if dirs is None:
        dirs = ['connection_data', 'pivot_data', 'model_data', 'weight_data', 'corrective_data', 'build']
    dir_vars = {}
    for dir_name in dirs:
        # Generate directory and backup directory names dynamically
        dir_key = f'{dir_name}_dir'
        bak_dir_key = f'{dir_name}_bak_dir'
        tmp_dir_path = os.path.join(directory, dir_name)
        tmp_bak_path = os.path.join(tmp_dir_path, 'BAK')
        # Set in the dictionary
        dir_vars[dir_key] = tmp_dir_path
        if add_backup_dir:
            dir_vars[bak_dir_key] = tmp_bak_path
        try:
            create_dir_verbose(tmp_dir_path, debug=debug)
            if add_backup_dir:
                create_dir_verbose(tmp_bak_path)
        except Exception as e:
            print(f'Failed to create directory {tmp_dir_path}: {e}')
    return dir_vars
# ################################### create_folder_structure Usage ########################################
# directory=r"C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD"
# dir_vars = create_folder_structure(directory=directory, debug=True)
# ##########################################################################################################


def create_asset(directory, debug=True):
    # ############################# dir map #############################
    # ├── charname
    # │   └──── charname_working.ma <--- this is your working file (It can be named anything. You can have as many as you want)
    # │   ├──── data <--- this is where all of the different data types go
    # │   │     ├──── connection_data    <--- how skinclusters are supposed to connected to their joints
    # │   │     │     └────────────── BAK
    # │   │     ├──── corrective_data    <--- where correctives should be exported
    # │   │     │     └────────────── BAK
    # │   │     ├──── model_data         <--- (not implemented yet)
    # │   │     │     └────────────── BAK
    # │   │     ├──── pivot_data         <--- (not implemented yet)
    # │   │     │     └────────────── BAK
    # │   │     ├──── rom_data           <--- if you have a custom range of motion you can export it here
    # │   │     │     └────────────── BAK
    # │   │     └──── weight_data        <--- where you export weights
    # │   │           └────────────── BAK
    # │   ├──── build_output <--- this is where builds go
    # │   │     ├──── connection_data    <--- When you build, your current data files are output here
    # │   │     ├──── corrective_data    
    # │   │     ├──── model_data         
    # │   │     ├──── pivot_data         
    # │   │     ├──── rom_data           
    # │   │     ├──── weight_data
    # │   │     └────────────── BAK 
    # │   └──── src
    # │         └──── charname_RIG_200_v001.ma <--- this is where you put the latest version of the rig from Minimo
    # ###################################################################
    output_dict = {}
    tmp_dict = create_dir_structure(directory, debug, dirs=['build_output'], add_backup_dir=True)
    output_dict.update(tmp_dict)
    tmp_dict = create_dir_structure(directory, debug, dirs=['data', 'src'])
    output_dict.update(tmp_dict)
    data_dir = join_and_norm(directory, 'data')
    tmp_dict = create_dir_structure(data_dir, debug, dirs=['connection_data', 'pivot_data','model_data',
                                                           'weight_data', 'corrective_data', "rom_data"],
                                                           add_backup_dir=True)
    output_dict.update(tmp_dict)
    return output_dict
# ############################# create_asset Usage #############################
# directory=r"C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD"
# dir_vars = create_folder_structure(directory=directory, debug=True)
# ##############################################################################


def bookend_output(func):
    """
    Decorator to print bookend lines before and after the output of the function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('\n# ############################# dir map #############################')
        func(*args, **kwargs)
        print('# ###################################################################\n')
    return wrapper
# ############################# bookend_output Usage #############################
# None, see usage for print_directory_map below.
# ################################################################################


@bookend_output
def print_directory_map(root_folder, indent=""):
    # Outputs something like this:
    # #########################################
    # ├── subdir1/
    # │   ├── file1.txt
    # │   └── file2.txt
    # └── subdir2/
    #     └── file3.txt
    # #########################################
    recursive_print_directory_map(root_folder, indent)
# ############################### print_directory_map Usage ######################################
# print_directory_map(r'C:\Users\harri\Documents\BDP\cha\SHAPES_transfer')
# ################################################################################################


def recursive_print_directory_map(root_folder, indent="", num_padding=4, back_num_padding=14):
    """
    Prints the directory structure of the given root folder recursively, starting with the root folder itself.
    
    Args:
        root_folder (str): The path of the folder to print.
        indent (str): The current indentation level for printing.
    
    Outputs something like this:
    
    # ├── subdir1/
    # │   ├── file1.txt
    # │   └── file2.txt
    # └── subdir2/
    #     └── file3.txt
    """
    if not os.path.exists(root_folder):
        print(f"Error: The directory '{root_folder}' does not exist.")
        return

    line = '─' * num_padding
    back_line = '─' * back_num_padding
    space = ' ' * num_padding

    # Print the root folder as the first subdirectory
    print(f"# ├── {os.path.basename(root_folder)}")

    def _print_subdirs(folder, indent):
        # List all files and folders in the current directory
        try:
            items = os.listdir(folder)
        except PermissionError:
            print(f"Error: Permission denied for '{folder}'")
            return

        files = []
        dirs = []

        # Separate files and directories
        for item in items:
            item_path = os.path.join(folder, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append(item)

        # Sort files and directories alphabetically
        files.sort()
        dirs.sort()

        # Print files first
        for index, item in enumerate(files):
            item_path = os.path.join(folder, item)
            is_last = index == len(files) - 1  # Check if it's the last file
            connector = f"└{line} " if is_last else f"├{line} "
            print(f"# {indent}{connector}{item}")

        # Print directories next
        total_dirs = len(dirs)
        for index, item in enumerate(dirs):
            item_path = os.path.join(folder, item)
            is_last = index == total_dirs - 1  # Check if it's the last directory
            connector = f"└{line} " if is_last else f"├{line} "

            # Check for 'BAK' in the directory name
            if 'BAK' in item:
                connector = f"└{back_line} " if is_last else f"├{back_line} "

            print(f"# {indent}{connector}{item}")  # Added trailing slash for directories

            # Recursive call for children
            new_indent = indent + (f" {space} " if is_last else f"│{space} ")
            _print_subdirs(item_path, new_indent)

    # Start the recursive print for subdirectories
    _print_subdirs(root_folder, indent + "│   ")

####################################### Usage ########################################
# Example usage:
# recursive_print_directory_map(r'C:\Users\harri\Documents\BDP\cha\SHAPES_transfer')
######################################################################################

####################################### Usage ########################################
# Example usage:
# recursive_print_directory_map(r'C:\Users\harri\Documents\BDP\cha\SHAPES_transfer')
######################################################################################
