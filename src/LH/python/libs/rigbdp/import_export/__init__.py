import os

from maya import cmds


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