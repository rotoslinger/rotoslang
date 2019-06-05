import sys, os

OPERATING_SYSTEM = sys.platform

BUILDER_DIR = "builders"
EXTENSION = ".py"

def get_repo_default_path():
    default_path = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.dirname(os.path.normpath(default_path))
    return os.path.dirname(os.path.normpath(default_path))


def get_delimeter():
    delimeter = "/"
    if OPERATING_SYSTEM == "win32" or OPERATING_SYSTEM == "win64":
        delimeter =  "\\"
    return delimeter

def get_delimeter_check_default_path(default_path):
    delimeter = get_delimeter()
    if not default_path:
        default_path = get_repo_default_path()
    return delimeter, default_path

def get_filename_from_path(asset_name, strip=False, ext=EXTENSION):
    delimeter = get_delimeter()
    file_name = asset_name.split(delimeter)[-1]
    if strip and ext in file_name:
        file_name = file_name.split(ext)[0]
    return file_name

def get_file_by_asset_name(asset_name, default_path=None, file="guides", ext=EXTENSION):
    # DOES NOT check whether the file exists
    delimeter, default_path = get_delimeter_check_default_path(default_path)
    asset_dir = delimeter + asset_name
    file_path = default_path + delimeter + BUILDER_DIR + asset_dir + delimeter + file + ext
    return file_path

def get_backup_dir_by_asset_name(asset_name, default_path=None):
    delimeter = get_delimeter()

    if not default_path:
        default_path = get_repo_default_path()
    asset_dir = delimeter + asset_name
    backup_path = default_path + delimeter + BUILDER_DIR + asset_dir + delimeter + "BAK"
    return backup_path

