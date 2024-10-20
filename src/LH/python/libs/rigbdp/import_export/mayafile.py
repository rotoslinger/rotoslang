import os
import maya.cmds as cmds
import glob
import os
import maya.cmds as cmds
import glob

def file_at_relative_path(rel_path='../weight_data/*', filetype='.json'):
    """
    Get files at a relative path from the current Maya scene.
    Args:
        rel_path (str): The relative path to search for files, using 
                        '*' for files in the directory and '**/*' for 
                        recursive search.
        filetype (str): The file extension to filter by (e.g., '.json').
    Returns:
        list: A list of file paths that match the criteria.
    """
    # Get the current Maya file's absolute path
    current_file = cmds.file(q=True, sn=True)
    # Check if the current file is saved
    if not current_file:
        raise ValueError("Current scene has not been saved. Please save the scene before running this function.")
    # Get the directory of the current file
    current_dir = os.path.dirname(current_file)
    # Build the full path using the provided relative path
    target_pattern = os.path.normpath(os.path.join(current_dir, rel_path))
    # Use glob to find matching files
    matching_files = glob.glob(target_pattern, recursive='**' in rel_path)
    return matching_files
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
######################################################################################


import os
import json

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
file_paths = [
    "/path/to/project/weight_data/example1.json",
    "/path/to/project/weight_data/example2.json"
]
imported_dict = import_files_as_dict(file_paths)
print("Imported Data:", imported_dict)
######################################################################################
