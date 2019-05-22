import time, os, fnmatch, shutil, json
from rig_2 import backup
reload(backup)
OPERATING_SYSTEM = backup.OPERATING_SYSTEM
DELIMETER = backup.DELIMETER

def generate_timestamp():
    t = time.localtime()
    return "{0}_{1}_{2}_{3}_{4}_{5}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

def generate_backup_filename(original_name, path_without_name, backup_directory_name="BAK", extension="py"):
    timestamp = generate_timestamp()
    # weights.timestamp.py
    filename = "{0}.{1}.{2}".format(original_name, timestamp, extension)
    # /path/baseAsset/BAK/ + filename
    return "{0}{1}{2}{3}{4}".format(path_without_name, DELIMETER, backup_directory_name, DELIMETER, filename)

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


