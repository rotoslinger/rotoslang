# builtins
import importlib, time, os, shutil, sys, re, json

# third party
from maya import cmds

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
    if not os.path.exists(full_path): return
    path, filename = os.path.split(full_path)
    check_parent_directory(filepath=path)
    backup_name = generate_backup_filename(filepath=path, filename=filename, backup_dir_name=backup_dir_name)
    shutil.copy(full_path, backup_name)
############################# backup_file Usage ################################
# filepath = r"C:\Users\harri\Documents\BDP\cha\jsh\jsh_base_body_geo_upperFace_skinCluster.xml"
# backup_dir = "jsh_base_body_geo_upperFace_skinCluster.xml"
# backup_file(filepath=filepath, filename=filename)
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

def create_folder_structure(directory, dirs=None, debug=False):
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
        dir_vars[bak_dir_key] = tmp_bak_path

        try:
            create_dir_verbose(tmp_dir_path, debug=debug)
            create_dir_verbose(tmp_bak_path)
        except Exception as e:
            print(f'Failed to create directory {tmp_dir_path}: {e}')
    return dir_vars
# ################################### create_folder_structure Usage ########################################
# directory=r"C:\Users\harri\Documents\BDP\cha\teshi_TESTBUILD"
# dir_vars = create_folder_structure(directory=directory, debug=True)
# ##########################################################################################################

def join_and_norm(*paths):
    # a builtin helper function to keep code brief 
    # Simple way to join and clean up path name.  Important because we could be working multi platform.
    return os.path.normpath(os.path.join(*paths))
# no usage, this is a builtin helper function, it should not be used by itself
# ################################### join_and_norm Usage ########################################
# dir=r"drive/mangled\path//"
# file=r"test.txt"
# full_path = join_and_norm(dir, file)
# print(full_path) # --- returns: drive/mangled/path/test.txt
# ################################################################################################
