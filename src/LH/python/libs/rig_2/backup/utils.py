import time, os, fnmatch, shutil, json
from rig_2 import filepath
import importlib
importlib.reload(filepath)
from rig_2.filepath import utils as filepath_utils
importlib.reload(filepath_utils)

OPERATING_SYSTEM = filepath.OPERATING_SYSTEM
DELIMETER = filepath.DELIMETER

def generate_timestamp():
    t = time.localtime()
    return "{0}_{1}_{2}_{3}_{4}_{5}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

def generate_backup_filename(asset_path, file_name="guides", backup_directory_name="BAK", extension="py"):
    timestamp = generate_timestamp()
    # weights.timestamp.py
    filename = "{0}.{1}.{2}".format(file_name, timestamp, extension)
    # /path/baseAsset/BAK/ + filename
    return "{0}{1}{2}{3}{4}".format(asset_path, DELIMETER, backup_directory_name, DELIMETER, filename)

def check_parent_directory(path):
    # This only finds the path (BAK) just before the new file  and creates it if it doesn't exist
    # If other directories further up don't exist this will fail with an error
    # This fail is important because it is possible the entire file structure doesn't exist yet and
    # could indicate a previous error.
    norm_path= os.path.dirname(os.path.normpath(path))
    # Make sure the path exists
    if not os.path.exists(norm_path):
        os.mkdir(norm_path)


def generate_backup_file(path, dictionary):
    # This only finds the path just before the new file (BAK) and creates it if it doesn't exist
    # If other directories further up don't exist we want 
    check_parent_directory(path)

    file = open(path, "wb")
    json.dump(dictionary, file, sort_keys = False, indent = 2)
    file.close()
    return dictionary


def backup_file(asset_name, file_to_backup):
    if not os.path.exists(file_to_backup):
        return
    # filename will always be something like "guides" but it is important that the user can set it to anything for ease of use
    # User may want to make brow_guide or eye_guide
    # All guides will need to be merged into a file called "guides" but it is fine to do local work in other files...
    filename = filepath_utils.get_filename_from_path(file_to_backup)
    asset_path = filepath_utils.get_asset_dir_by_asset_name(asset_name)
    full_backup_file_name = generate_backup_filename(asset_path, filename)
    shutil.copy(file_to_backup, full_backup_file_name)

    
