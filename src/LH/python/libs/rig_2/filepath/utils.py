import sys, os
from rig_2 import filepath
import importlib
importlib.reload(filepath)
DELIMETER = filepath.DELIMETER

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
    file_name = asset_name.split(DELIMETER)[-1]
    if strip and ext in file_name:
        file_name = file_name.split(ext)[0]
    return file_name

def get_file_by_asset_name(asset_name, default_path=None, file="guides", ext=EXTENSION):
    # DOES NOT check whether the file exists
    default_path = check_default_path(default_path)
    asset_dir = DELIMETER + asset_name
    file_path = default_path + DELIMETER + BUILDER_DIR + asset_dir + DELIMETER + file + ext
    return file_path

def get_backup_dir_by_asset_name(asset_name, default_path=None):
    if not default_path:
        default_path = get_repo_default_path()
    asset_dir = DELIMETER + asset_name
    backup_path = default_path + DELIMETER + BUILDER_DIR + asset_dir + DELIMETER + "BAK"
    return backup_path

def get_asset_dir_by_asset_name(asset_name, default_path=None):
    if not default_path:
        default_path = get_repo_default_path()
    asset_dir = DELIMETER + asset_name
    path = default_path + DELIMETER + BUILDER_DIR + asset_dir
    return path
