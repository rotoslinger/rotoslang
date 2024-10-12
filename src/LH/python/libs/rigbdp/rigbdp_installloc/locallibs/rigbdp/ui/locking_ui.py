# builtins
import importlib

# bdp
from rigbdp.build import locking


from rigbdp.ui import dyn_button_ui

# reloads
importlib.reload(locking)
importlib.reload(dyn_button_ui)












# # Toggle display visibility
# locking.toggle_jnt_display_vis()

# # Vis skin joints
# locking.vis_walkout_skin(skin=True, walkout=False)

# # Vis walkout joints
# locking.vis_walkout_skin(skin=False, walkout=True)

# unlock the rig, allow selection, turn on ihi for every node in the scene
locking.unlock_all(ihi_level=1, skin=False, walkout=False)
###################################################################################################

# unlock the rig, allow selection, turn on ihi for every node in the scene
