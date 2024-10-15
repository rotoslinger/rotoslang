import importlib
from rigbdp.shelf import add
from rigbdp.ui import lockui
importlib.reload(add)
importlib.reload(lockui)

def create():
    add.create_shelf_tab_with_button(lockui, 'BDP Rigging', debug=False)
