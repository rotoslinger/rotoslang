import ka_rigTools
import importlib
importlib.reload(ka_rigTools)

import ka_rigTools.ka_hotkeys as ka_hotkeys
importlib.reload(ka_hotkeys)

ka_hotkeys.activateHotkey(['v', 'tilda'])

import ka_rigTools.ka_hotkeys as ka_hotkeys
importlib.reload(ka_hotkeys)   
ka_hotkeys.activateHotkey(['x', 'tilda', 'f_ctrl', 'z_alt', 'c_ctrl', 'v_ctrl', 'V_ctrl', 't'])
