# builtins
import importlib, time, os, shutil, sys, re, json, glob, platform

from functools import wraps

# third party
from maya import cmds

# custom
import decorator

importlib.reload(decorator)

DELIMITER = os.path.sep  # more self explanatory for people not familiar with builtin path handling

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
    pattern = re.compile(rf"{re.escape(base_name)}__v(\d{{3}})__.*{re.escape(ext)}")
    # Check files in the directory and extract version numbers
    for file in os.listdir(filepath):
        match = pattern.match(file)
        if match:
            existing_versions.append(int(match.group(1)))  # Append the extracted version number
    # Determine the next version number
    version = max(existing_versions, default=0) + 1  # Start from v001 if no versions exist
    timestamp = generate_timestamp()
    backup_filename = os.path.join(filepath, f"{base_name}__v{version:03d}__{timestamp}{ext}")
    return backup_filename
################################### generate_backup_filename Usage ###################################
# filepath = r"C:\Users\harri\Documents\BDP\cha\jsh"
# filename = "jsh_base_body_geo_upperFace_skinCluster.xml"
# backup_filename = generate_backup_filename(filepath=filepath, filename=filename)
######################################################################################################

def generate_backup_dirname(path_to_backup_dir, dir_name):
    # Ensure the directory exists
    if not os.path.exists(path_to_backup_dir):
        raise FileNotFoundError(f"The directory '{path_to_backup_dir}' does not exist.")
    # Find existing versions
    existing_versions = []
    pattern = re.compile(rf"{re.escape(dir_name)}___v(\d{{3}})")
    # Check files in the directory and extract version numbers
    for file in os.listdir(path_to_backup_dir):
        match = pattern.match(file)
        if match:
            existing_versions.append(int(match.group(1)))  # Append the extracted version number
    # Determine the next version number
    version = max(existing_versions, default=0) + 1  # Start from v001 if no versions exist
    timestamp = generate_timestamp()
    backup_filename = os.path.join(path_to_backup_dir, f"{dir_name}___v{version:03d}___{timestamp}")
    return backup_filename
################################### generate_backup_filename Usage ###################################
# path_to_backup_dir = r"C:\Users\harri\Documents\BDP\cha\teshi\build_output\BAK"
# dir_name = "teshi_RIG_200_v009_build_output"
# backup_dirname = generate_backup_dirname(path_to_backup_dir=path_to_backup_dir, dir_name=dir_name)
# print(backup_dirname)
######################################################################################################


def dir_first_file(directory):
    try:
        # List all items in the directory
        items = os.listdir(directory)
        # Loop through the items to find the first file
        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                return item_path  # Return the full path of the first file
        return None  # If no files found
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory}'.")
################################### dir_first_file Usage ###########################################
# directory_path = r"C:\Users\harri\Documents\BDP\cha\teshi\src"
# first_file = dir_first_file(directory_path)
# if first_file:
#     print(f"First file found: {first_file}")
# else:
#     print("No files found in the directory.")
####################################################################################################


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


def files_in_path_filtered(path, file_type='mel'):
    # Normalize the path
    path = os.path.normpath(path)
    # Treat file_type as a list even if it's a single string
    file_types = [file_type] if isinstance(file_type, str) else file_type
    # Use a set comprehension to gather files
    files = {os.path.normpath(file.strip()) for _type in file_types 
             for file in glob.glob(f"{path}{DELIMITER}*.{_type.replace('.', '').strip()}")}
    # return as list so we have the option to choose a specific index ([0] for example)
    return list(files)
####################################### Usage ########################################
# path = r'C:\Users\harri\Documents\BDP\cha\teshi\data\corrective_data'
# files_in_path(path, file_type='mel')
######################################################################################


def all_files_in_path_except(path, except_files=['BAK']):
    # Normalize the path
    path = os.path.normpath(path)
    # Treat except_files as a list even if it's a single string
    except_files = [except_files] if isinstance(except_files, str) else except_files
    # Use a set comprehension to gather all files
    all_files = {os.path.normpath(file.strip()) for file in glob.glob(f"{path}{DELIMITER}*")}
    # Filter out files that match any of the except_files
    filtered_files = {file for file in all_files if not any(exc in os.path.basename(file) for exc in except_files)}
    # Return as a list
    return list(filtered_files)
####################################### Usage ########################################
# path = r'C:\Users\harri\Documents\BDP\cha\teshi\data\corrective_data'
# files_in_path(path, file_type='mel')
######################################################################################


def copy_all_in_dir_except(source_dir, destination_dir, except_paths=['BAK']):
    """Copy files (not directories) from source_dir to destination_dir."""
    if except_paths is None:
        except_paths = []
    dirs = all_files_in_path_except(source_dir)
    copied_files = []  # List to store copied files

    for dir in dirs:
        # tuple "(head, tail)" where "head" is the path "tail" is everything after the final slash
        # in this case I know neither will be empty, so I am getting index 1
        tail = os.path.split(dir)[1]
        local_data_dir = create_dir_verbose(os.path.join(destination_dir, tail))
        copy_files_except(source_dir=dir, destination_dir=local_data_dir, debug=False)
        if os.path.isfile(dir):
            pass
    return copied_files
############################# copy_all_in_dir_except Usage ################################
# source_directory = "path/to/source/directory"
# destination_directory = "path/to/destination/directory"
# except_list = ["skip_this", "ignore_this"]
# copy_all_in_dir_except(source_directory, destination_directory, except_list)
########################################################################################


def copy_files_except(source_dir, destination_dir, except_paths=['BAK']):
    if except_paths is None:
        except_paths = []
    # Normalize the paths
    source_dir = os.path.normpath(source_dir)
    destination_dir = os.path.normpath(destination_dir)
    # Check if source directory exists
    if not os.path.isdir(source_dir):
        print(f'The source directory "{source_dir}" does not exist or is not a directory.')
        return []
    # Create the destination directory that mirrors the source directory's name
    source_basename = os.path.basename(source_dir)
    new_dest_dir = os.path.join(destination_dir, source_basename)
    os.makedirs(new_dest_dir, exist_ok=True)
    copied_files = []  # List to store copied files
    # Iterate over the files and directories in the source directory
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        # Check if item matches any of the strings in except_paths
        if any(except_path in item for except_path in except_paths):
            print(f'Skipped: {item_path}')
            continue
        shutil.copy2(item_path, new_dest_dir)
        copied_files.append(os.path.join(new_dest_dir, os.path.basename(item_path)))
        print(f'Copied file: {item_path} to {new_dest_dir}')

    return copied_files
############################# copy_files_except Usage ################################
# source_directory = "path/to/source/directory"
# destination_directory = "path/to/destination/directory"
# except_list = ["skip_this", "ignore_this"]
# copy_files_except(source_directory, destination_directory, except_list)
########################################################################################


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


def backup_rig_build(build_output_path, backup_dir_name="BAK"):
    bak_dir = join_and_norm(build_output_path, backup_dir_name)
    # within the backup_output's BAK dir
    # ------ create a new build_output dir and add a backup filename to it
    # Generate path to build output
    output_dir_back_name = generate_backup_dirname(path_to_backup_dir=bak_dir, dir_name='build_output')
    output_dir_back_name= os.path.normpath(output_dir_back_name)
    versioned_output_dir = create_dir_verbose(output_dir_back_name)
    # ------ copy all files and directories in backup output, into this new backup build_output dir
    files_dirs = all_files_in_path_except(build_output_path, except_files=['BAK'])
    return_files = []
    for path in files_dirs:
        if os.path.isfile(path):
            shutil.copy(path, versioned_output_dir)
            return_files = return_files + [path]
        if os.path.isdir(path):
            tmp_files = copy_files_except(source_dir=path, destination_dir=versioned_output_dir, except_paths=['BAK'])
            return_files = return_files + tmp_files
    for return_file in return_files:
        print(f'>>Backing up file ---> {return_file}\n>>File has been saved here ---> {versioned_output_dir}')
    # returns the newly versioned output_dir, the files copied there
    return(versioned_output_dir, return_files)
############################# backup_rig_build Usage ################################
# path_to_backup = r"C:\Users\harri\Documents\BDP\cha\teshi\build_output\BAK"
# backup_files_in_directory(build_output_path=path_to_backup, backup_dir_name="BAK")
########################################################################################


def backup_files_in_dir(path, backup_dir_name='BAK', except_files=['BAK']):
    # Normalize the path
    path = os.path.normpath(path)
    # Get the backup directory path
    backup_dir = os.path.join(path, backup_dir_name)
    # Create the backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    # Get all files except the specified ones
    files_to_backup = all_files_in_path_except(path, except_files)
    # Backup each file
    for full_path in files_to_backup:
        if os.path.isfile(full_path):  # Ensure we are only copying files
            filename = os.path.basename(full_path)
            backup_name = os.path.join(backup_dir, filename)
            shutil.copy(full_path, backup_name)
            print(f'>>Backing up file ---> {filename}\n>>file has been saved here ---> {backup_name}')
        else:
            print(f'Skipping non-file item: {full_path}')
    return True
############################# backup_files_in_dir Usage ################################
# path_to_backup = "path/to/your/directory"
# excluded_files = ["temp"]  # Example of files to exclude
# backup_files_in_directory(path_to_backup, except_files=excluded_files)
########################################################################################


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


def create_dir_verbose(dir_path, debug=False):
    dir_path = os.path.normpath(dir_path)
    if os.path.isdir(dir_path):
        if debug:
            print(f'Directory "{dir_path}" already exists.')
    else:
        os.makedirs(dir_path)
        if debug:
            print(f"Created directory: {dir_path}")
    return dir_path
################################### create_dir_verbose Usage ########################################
# directory=r"C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD\test_directory_to_create"
# create_dir_verbose(dir_path=directory, debug=True)
##########################################################################################################


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
    if debug:print_directory_map(directory)
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
    Prints the directory structure of the given root folder recursively, starting with the root folder it
    
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


def get_files_of_type(path_to_rel_path, rel_path='../data/corrective_data', file_type='json'):
    """
    Having full_path & rel_path arg may seem redundant, but this function is meant 
    to be used from within an application, not necessarily within a file.

    For example, if we wanted to find a python module we could use module.__file__
    
    Within maya this method will be used to find relative paths from whatever file
    happens to be open at the time, as long as it has been save somewhere.
    
    For example, finding the multiple weights files for a file in maya:
    get_files_of_type(full_path=cmds.file(q=True, sn=True), rel_path='../weight_data/*')
    returns

    Args:
        path_to_rel_path (str): The full path where the relative path
                                will start its search
        rel_path (str): The relative path to search for files 
                        if /* is used, the search becomes recursive.
        filetype (str): The file extension to filter by (e.g., '.json').
    Returns:
        list: A list of file paths that match the criteria.
    """
    path_to_rel_path = os.path.normpath(path_to_rel_path)
    rel_path = os.path.normpath(rel_path)
    path = os.path.join(path_to_rel_path, rel_path)
    path = os.path.abspath(path)
    files = glob.glob(f'{path}{DELIMITER}*.{file_type}')
    os.path.normpath(path)
    return files
####################################### Usage ########################################
# path = r'C:\Users\harri\Documents\BDP\cha\teshi\src'
# rel_path = r'../data/corrective_data'
# correctives = get_files_of_type(path_to_rel_path=path, rel_path=rel_path, file_type = 'mel')
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
# Example usage:
# file_paths = [
#     "/path/to/project/weight_data/example1.json",
#     "/path/to/project/weight_data/example2.json"
# ]
# imported_dict = import_files_as_dict(file_paths)
# print("Imported Data:", imported_dict)
######################################################################################


###################################################################################################
########################################### Safe Delete ###########################################
###################################################################################################
'''
The following code has been written to safely delete files. It is meant to only delete temporary
after they have been backed up.  It should not be used to delete anything else.

Any function that deletes any data should have a debug arg that is set to True, which prints out
which directories and files will be delete. While this debug arg is True no files will be deleted.
only set this to False if you are 100% certain that the proper files are being removed.

I've tried to make this code as fool proof as possible. As much as I hate to admit it, sometimes
the biggest fool is me. Even a particularly bright person may make a mistake if they are sleep
deprived, distracted, or distraught.

For this reason I implore anyone who uses the following code to always check that the directories
and files they will be deleting are the correct ones.  Be especially careful renaming, refactoring,
or changing all occurrences of any code that use these functions.

The moment you decided to change something, first flip the Debug arg back to True before rolling out.

Stay safe.
'''
####################################### attrs and functions #################################
# Define common system directories to avoid based on the operating system
SYSTEM_DIRS = {
    'Windows': {'C:\\', 'C:\\Windows', 'C:\\Program Files'},
    'Linux': {'/', '/bin', '/etc', '/usr', '/var', '/lib'},
    'Darwin': {'/', '/System', '/Applications', '/usr', '/bin', '/etc'}
}

# Define common system file extensions to avoid
SYSTEM_FILE_EXTENSIONS = {'.exe', '.sys', '.dll', '.so', '.dylib', '.app', '.bat', '.sh'}

def is_system_file_or_directory(path):
    """Check if the given path is a system file or directory."""
    current_os = platform.system()
    for system_dir in SYSTEM_DIRS.get(current_os, []):
        if os.path.commonpath([path, system_dir]) == system_dir:
            return True
    _, ext = os.path.splitext(path)
    return ext in SYSTEM_FILE_EXTENSIONS

def safe_dir_delete_maya(target_dir, debug=True):
    # Check if running in Maya
    is_maya = False
    try:
        import maya.cmds as cmds
        is_maya = True
    except ImportError:
        pass
    # If not in Maya, exit the function
    if not is_maya:
        print("This function is only intended to run in Maya.")
        return
    # Normalize the target directory
    target_dir = os.path.normpath(target_dir)
    # Check if the target directory exists
    if not os.path.isdir(target_dir):
        print(f'The directory {target_dir} does not exist or is not a directory.')
        return
    # Iterate through the contents of the target directory
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if is_system_file_or_directory(item_path):
            print(f'Skipped system file or directory: {item_path}')
            continue
        try:
            if os.path.isfile(item_path):
                if debug:
                    print(f'Would delete file: {item_path}')
                else:
                    os.remove(item_path)
                    print(f'Deleted file: {item_path}')
            elif os.path.isdir(item_path):
                if not os.listdir(item_path):  # Check if directory is empty
                    if debug:
                        print(f'Would delete empty directory: {item_path}')
                    else:
                        os.rmdir(item_path)
                        print(f'Deleted empty directory: {item_path}')
                else:
                    print(f'Skipped non-empty directory: {item_path}')
        except Exception as e:
            print(f'Error processing {item_path}: {e}')

####################################### Usage ########################################
# directory_to_clean = "path/to/your/directory"
# safe_dir_delete_maya(directory_to_clean)
######################################################################################


def is_system_file(path):
    """Check if the given path is a system file."""
    _, ext = os.path.splitext(path)
    return ext in SYSTEM_FILE_EXTENSIONS

def safe_delete_file_maya(file_path, debug=True):
    # Check if running in Maya
    is_maya = False
    try:
        import maya.cmds as cmds
        is_maya = True
    except ImportError:
        pass
    # If not in Maya, exit the function
    if not is_maya:
        print("This function is only intended to run in Maya.")
        return
    # Normalize the file path
    file_path = os.path.normpath(file_path)
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f'The file {file_path} does not exist or is not a file.')
        return
    # Check if the file is a system file
    if is_system_file(file_path):
        print(f'Skipped system file: {file_path}')
        return
    try:
        if debug:
            print(f'Would delete file: {file_path}')
        else:
            os.remove(file_path)
            print(f'Deleted file: {file_path}')
    except Exception as e:
        print(f'Error deleting {file_path}: {e}')
####################################### Usage ########################################
# file_to_delete = "path/to/your/file.txt"
# safe_delete_file_maya(file_to_delete)
######################################################################################


def copy_files_with_newer_timestamps(source_dir, destination_dir):
    """
    Copy all files from source_dir to destination_dir.
    If destination_dir already exists, only copy files with newer timestamps.

    :param source_dir: The source directory to copy files from.
    :param destination_dir: The destination directory to copy files to.
    """
    # Normalize paths
    source_dir = os.path.normpath(source_dir)
    destination_dir = os.path.normpath(destination_dir)

    # Check if source directory exists
    if not os.path.isdir(source_dir):
        print(f'The source directory "{source_dir}" does not exist or is not a directory.')
        return

    # Create destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Iterate over the files in the source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        destination_path = os.path.join(destination_dir, item)

        # Check if the item is a file
        if os.path.isfile(source_path):
            # If the file does not exist in the destination or if the source file is newer
            if not os.path.exists(destination_path) or os.path.getmtime(source_path) > os.path.getmtime(destination_path):
                shutil.copy2(source_path, destination_path)  # Copy file with metadata
                print(f'Copied file: {source_path} to {destination_path}')
            else:
                print(f'Skipped (older or same timestamp): {source_path}')

        # If the item is a directory, recursively copy (optional)
        elif os.path.isdir(source_path):
            # If the directory does not exist in the destination, copy it
            if not os.path.exists(destination_path):
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                print(f'Copied directory: {source_path} to {destination_path}')
            else:
                print(f'Skipped directory (already exists): {source_path}')

####################################### Usage ########################################
# source_directory = 'path/to/source/directory'
# destination_directory = 'path/to/destination/directory'
# copy_files_with_newer_timestamps(source_directory, destination_directory)
######################################################################################


r"""
#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <src_dir> <dest_dir>"
    exit 1
fi

# Assign arguments to variables
SOURCE_DIR="$1"
DESTINATION_DIR="$2"

# Call the Python script to copy files
python3 -c "import sys; sys.path.append('${SOURCE_DIR}'); from file import copy_files_except; copy_files_except('${SOURCE_DIR}', '${DESTINATION_DIR}')"

# Usage examples
cat << EOF
Usage examples:
1. To copy files from /home/user/source to /home/user/destination:
   ./copy_files.sh /home/user/source /home/user/destination

2. To copy files from /path/to/source_dir to /path/to/destination_dir:
   ./copy_files.sh /path/to/source_dir /path/to/destination_dir
EOF
"""