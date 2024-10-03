import time, os, shutil, sys, re
from maya import cmds


############################# File Path Utils ###############################

##############  Why we need to use \ for filepaths on Windows ###############
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
############# Usage ###############
# don't forget to double them backspaces, because \\ resolves to \ and doesn't break python. Or C++, or C, etc. Did I mention I hate this?
# mayaified_directory = de_windows_os_path(filepath = "C:\\foobar\\skoobar\\skeebop\\skeedoobar\\" ) # on windows returns --- C:/foobar/skoobar/skeebop/skeedoobar
# print("This is the normalized directory " + mayaified_directory)
###################################

# Make the Maya filepath Windows compatible
def format_filepath(filepath):
    # honestly, this is just for windows to make sure / becomes \
    # much cleaner than re.sub(r'/', '\\', path) as this gets rid of redundant chars, ./..\, or whatever other nonsense you might end up with
    return os.path.normpath(filepath)
############# Usage ###############
# normalized_directory = format_filepath(filepath = "C:/foobar/skoobar/skeebop/skeedoobar/" ) # on windows returns --- C:\foobar\skoobar\skeebop\skeedoobar
# print("This is the normalized directory " + normalized_directory)
###################################
#############################################################################


######################################### Backup Utils ################################################
OPERATING_SYSTEM = sys.platform

# Have to get the path delimiter because microsoft is cool. Thanks a lot microsoft, we (don't) love you.
def get_delimiter():
    delimiter = "/"
    if OPERATING_SYSTEM == "win32" or OPERATING_SYSTEM == "win64":
        delimiter =  "\\"
    return delimiter
############# Usage ###############
# delimiter = get_delimiter()
# print("Your operating system is {0} so your path delimiter is {1} congratulations.".format(OPERATING_SYSTEM, delimiter))
####################################

DELIMITER = get_delimiter()

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
############# Usage ###############
# scene_dir = get_scene_dir()
# print("The current scene has been saved here: " + scene_dir)
###################################

def generate_timestamp():
    t = time.localtime()
    # doing a nonstandard date time format, for the sake of readability, mankind, and all that is holy.
    # YYYY-MM-DD_HH-MM-SS (instead of standard YYYYMMDD-HHMMSS, f*** the rules, they aren't super readable)
    return "{0}-{1}-{2}_{3}-{4}-{5}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
############# Usage ###############
# timestamp = generate_timestamp()
# print(timestamp)
####################################

def generate_backup_filename(filepath, file_name="weights", backup_directory_name="BAK", extension="xml"):
    timestamp = generate_timestamp()
    # weights.timestamp.xml
    filename = "{0}_{1}.{2}".format(file_name, timestamp, extension)
    clean_path = format_filepath("{0}{1}{2}{3}{4}".format(filepath, DELIMITER, backup_directory_name, DELIMITER, filename))
    # /path/baseAsset/BAK/ + filename
    return clean_path
############# Usage ###############
# backup_filename = generate_backup_filename(filepath=get_scene_dir(), file_name="weights")
# print(backup_filename)
# On windows returns C:\Users\harri\Documents\BDP\cha\jsh\BAK\weights_2024-10-2_22-24-32.xml 
# On UNIX returns: C:/Users/harri/Documents/BDP/cha/jsh/BAK/weights_2024-10-2_22-24-32.xml
####################################

def check_parent_directory(filepath, debug=False):
    # This only finds the path (BAK) just before the new file  and creates it if it doesn't exist
    # If other directories further up don't exist this will fail with an error
    # This fail is important because it is possible the entire file structure doesn't exist yet and
    # could indicate a previous error.
    norm_path= os.path.dirname(os.path.normpath(filepath))
    # Make sure the path exists
    if not os.path.exists(norm_path):
        os.mkdir(norm_path)
        if not debug: return
        print("New directory created @ {0}".format(norm_path))
############# Usage ###############
scene_dir = get_scene_dir()
backup_filename = generate_backup_filename(filepath=scene_dir)
parent_dir = check_parent_directory(filepath=backup_filename, debug=True)
print(parent_dir)
####################################

# TODO Fix all of this crap, 
# TODO needs to do the check_parent_directory to create the backup folder if it doesn't exist yet.  Otherwise the maya rig directory is going to get crowded.
def backup_file(skincluster_name, file_to_backup, filename, filepath):
    if not os.path.exists(file_to_backup):
        return
    full_backup_file_name = generate_backup_filename(filepath, filename)

    shutil.copy(file_to_backup, full_backup_file_name)

'''
BUILDER_DIR = "builders"
EXTENSION = ".py"

def get_repo_default_path():
    default_path = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.dirname(os.path.normpath(default_path))
    return os.path.dirname(os.path.normpath(default_path))

def check_default_path(default_path):
    if not default_path:
        default_path = get_repo_default_path()
    return default_path

def get_filename_from_path(asset_name, strip=False, ext=EXTENSION):
    file_name = asset_name.split(DELIMITER)[-1]
    if strip and ext in file_name:
        file_name = file_name.split(ext)[0]
    return file_name

def get_file_by_asset_name(asset_name, default_path=None, file="guides", ext=EXTENSION):
    # DOES NOT check whether the file exists
    default_path = check_default_path(default_path)
    asset_dir = DELIMITER + asset_name
    file_path = default_path + DELIMITER + BUILDER_DIR + asset_dir + DELIMITER + file + ext
    return file_path

def get_backup_dir_by_asset_name(asset_name, default_path=None):
    if not default_path:
        default_path = get_repo_default_path()
    asset_dir = DELIMITER + asset_name
    backup_path = default_path + DELIMITER + BUILDER_DIR + asset_dir + DELIMITER + "BAK"
    return backup_path

def get_asset_dir_by_asset_name(asset_name, default_path=None):
    if not default_path:
        default_path = get_repo_default_path()
    asset_dir = DELIMITER + asset_name
    path = default_path + DELIMITER + BUILDER_DIR + asset_dir
    return path

def generate_backup_file(path, dictionary):
    # This only finds the path just before the new file (BAK) and creates it if it doesn't exist
    # If other directories further up don't exist we want 
    check_parent_directory(path)

    file = open(path, "wb")
    json.dump(dictionary, file, sort_keys = False, indent = 2)
    file.close()
    return dictionary

'''
    












#########################################################
############## BDP Weight Export Utils ##################
#########################################################

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

# Usage #
# weights_path = "C:/Users/harri/Documents/BDP/cha/jsh"
# import_skins(path=weights_path, geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################

 
######################################################################################
# Full Usage #
# weights_path = "C:/Users/harri/Documents/BDP/cha/jsh"
# export_skins(path=weights_path, geom="jsh_base_body_geo", skin_filter=["upperFace"])
# import_skins(path=weights_path, geom="jsh_base_body_geo", skin_filter=["upperFace"])
######################################################################################

