from importlib import reload

from maya import cmds
from maya import mel

import decorator

@decorator.undo_chunk
def sel_all_rename(old_name='jsh', new_name='teshi'):
    # Transfers are a lot easier when all names of a character are replaced before export
    # It is less work:
    # you do this once before export, you avoid having to do it in 2 maya ascii, and 1 mel file. 
    everything = cmds.ls(shapes=False)
    renamed_nodes = set()  # To track renamed nodes and avoid reprocessing
    
    for node in everything:
        if old_name in node and node not in renamed_nodes:
            updated_name = node.replace(old_name, new_name)
            cmds.rename(node, updated_name, ignoreShape=True)
            renamed_nodes.add(updated_name)  # Add the new name to the set

@decorator.undo_chunk
def duplicate_and_rename():
    """
    meant for replacing all meshes in a SHAPES export with the nuetral of another char
    """
    
    # Get the current selection
    selection = cmds.ls(selection=True)
    
    if len(selection) < 2:
        cmds.error("Please select the base mesh first, followed by one or more target meshes.")
        return
    
    # The first selected object is the base mesh, the rest are the target meshes
    base_mesh = selection[0]

    # Make sure the base mesh is parented to world, this may not be the case if it is imported
    cmds.parent(base_mesh, w=True)

    target_meshes = selection[1:]
    
    for target in target_meshes:
        # Duplicate the base mesh
        duplicate = cmds.duplicate(base_mesh)[0]
        
        # Delete the target mesh
        cmds.delete(target)
        
        # Rename the duplicate to the name of the target mesh
        cmds.rename(duplicate, target)
        
# # To run, select the base mesh first, then the target meshes, and run:
# duplicate_and_rename()