# builtins
import importlib, os

# third party
import maya.cmds as cmds

# custom
from rigbdp import import_export
from rigbdp.import_export import file as file_utils

#reloads
importlib.reload(file_utils)

def file_at_relative_path(rel_path='../weight_data/*', file_type='.json', maya_style_delimiter=False):
    path_to_rel_path = import_export.get_scene_dir()
    files = file_utils.get_files_of_type(path_to_rel_path=path_to_rel_path, rel_path=rel_path, file_type=file_type)
    if maya_style_delimiter:
        files = [cmds.file(file, query=True, expandName=True) for file in files]
    return files

def files_in_path_filtered(path, file_type='mel'):
    # arg file_type can also be a list of filetypes, eg. ['ma', 'mb']
    full_file_path = []
    if file_type:
        full_file_path = file_utils.files_in_path_filtered(path, file_type)
        print('FULL FILE PATH : ',full_file_path)
    full_file_path = [os.path.normpath(p) for p in full_file_path]
    files = [cmds.file(file, query=True, expandName=True) for file in full_file_path]
    return files

def get_first_file(path, file_type='mel'):
    file = os.listdir(path)[0]
    file = cmds.file(file, query=True, expandName=True)
    return file
####################################### Usage ########################################
# Example 1: Non-recursive search (only files in the target directory)
# Assuming current Maya file is: /path/to/project/build/teshi_RIG_200_v007.ma
# This will find all .json files only in the ../weight_data/ directory (non-recursive)
# json_files_in_dir = file_at_relative_path('../weight_data/*', filetype='.json')
# print("Non-recursive matching JSON files:", json_files_in_dir)
# ------------------------------------------------------------------------------------
# Example 2: Recursive search (files in all nested directories)
# This will find all .json files in ../weight_data/ and all subdirectories
# json_files_recursive = file_at_relative_path('../weight_data/**/*', filetype='.json')
# print("Recursive matching JSON files:", json_files_recursive)
######################################################################################C:\Users\harri\Documents\BDP\cha\teshi\src\teshi_RIG_200_v008 .ma
