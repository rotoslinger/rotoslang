# builtins
import importlib

# bdp
from rigbdp.build import locking
from rigbdp.ui import dyn_button_ui

# reloads
importlib.reload(locking)
importlib.reload(dyn_button_ui)

def lockui():
    def unlock_all():
        # unlock the rig, allow selection, turn on ihi for every node in the scene
        locking.unlock_all(ihi_level=1, skin=False, walkout=False)

    def vis_sculpt_jnts():
        # # Vis walkout joints
        locking.vis_walkout_skin(skin=False, walkout=True)

    def vis_weight_jnts():
        # # Vis skin joints
        locking.vis_walkout_skin(skin=True, walkout=False)

    # Toggle display visibility
    def toggle_jnt_vis():
        locking.toggle_jnt_display_vis()

    # Toggle jnt xray
    def toggle_jnt_vis():
        locking.toggle_jnt_xray()

    ###################################################################################################

    # unlock the rig, allow selection, turn on ihi for every node in the scene

    button_dict = {
        "Unlock All": unlock_all,
        "Sculpt Jnts": vis_sculpt_jnts,
        "Weight Jnts": vis_weight_jnts,
        "Jnt On/Off": toggle_jnt_vis,
        "Xray On/Off": toggle_jnt_vis,
    }

    dyn_button_ui.create_dynamic_button_ui(button_dict,
                                           row_len=1, # --- how many horizontal buttons you want
                                           col_len=5, # --- how many vertical buttons you want
                                           row_title=["Unlock Rig",
                                                      "Sculpt Jnts Vis",
                                                      "Weight Jnts Vis",
                                                      "Toggle Jnt Vis",
                                                      "Toggle Jnt Xray",
                                                      ],
                                           col_title=[""],
                                           window_name="unlockui",
                                           window_title="BDP Minimo Unlocking UI")