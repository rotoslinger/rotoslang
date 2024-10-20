# builtins
import importlib

# third party
from maya import mel
from maya import cmds

# custom
from import_export import file
importlib.reload(file)

import maya.mel as mel
import os

def source_and_run_mel(filepath, proc_name, *proc_args):
    """
    Args:
        filepath (str): The full file path to the MEL script.
        proc_name (str): The name of the procedure to call from the MEL script.
        *proc_args: The arguments to pass to the MEL procedure (if any).
        
    Returns:
        The result of the MEL procedure (if any) or None.
    """
    # Normalize the file path for cross-platform compatibility
    filepath = os.path.normpath(filepath)
    
    # Check if the file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"MEL script not found: {filepath}")
    
    # Get the directory and script name (without extension)
    script_dir, script_file = os.path.split(filepath)
    script_name = os.path.splitext(script_file)[0]
    
    # Add the script directory to the MEL search path (if needed)
    mel.eval(f'addToRecentScriptTable("{script_dir}", "mel")')
    
    # Source the script
    mel.eval(f'source "{script_name}";')
    
    # Construct the MEL command to run the procedure with arguments
    mel_command = f'{proc_name}({" ".join(map(str, proc_args))});'
    
    # Run the procedure
    return mel.eval(mel_command)

# # Example usage
# try:
#     result = source_and_run_mel('/path/to/your/script/myMelScript.mel', 'SHAPES_getNamespace', 'myGeometry')
#     print(result)
# except FileNotFoundError as e:
#     print(e)


def import_correctives(filepath, proc_name, *proc_args):
    source_and_run_mel('/path/to/your/script/myMelScript.mel', 'SHAPES_getNamespace', 'myGeometry')