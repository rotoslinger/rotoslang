import sys, os

from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
from ui_2 import ui_utils
reload(ui_utils)
import elements
reload(elements)
from ui_2 import button_grid_base
reload(button_grid_base)


'''
@code
import sys
linux = '/scratch/levih/dev/rotoslang/src/LH/python/libs'
mac = "/Users/leviharrison/Documents/workspace/maya/scripts"
win = "C:\\Users\\harri\\Desktop\\dev\\rotoslang\\src\\LH\\python\\libs"
#---determine operating system
os = sys.platform
if "linux" in os:
    os = linux
if "darwin" in os:
    os = mac
if "win32" in os:
    os = win

if os not in sys.path:
    sys.path.append(os)

from ui_2 import guide
reload(guide)
guide_ui = guide.Guide_UI()
guide_ui.openUI()

@endcode
'''
class Guide_UI(button_grid_base.Base):

    def __init__(self,
                 **kw):
        super(Guide_UI, self).__init__(**kw)
        self.win_title = "Guide Utilities"
        self.setting_filename = "GuideUtilities"
        self.save_window_state = True


    def first_button_func(self):
        print "You have just pressed the first button"

    def second_button_func(self):
        print "You have just pressed the second button"

    def create_buttons(self):
        super(Guide_UI, self).create_buttons()
        # Buttons
        self.first_label, self.first_button = ui_utils.label_button(label_text="Documentation for first button",
                                                                    button_text="First Button",
                                                                    color=elements.purple,
                                                                    button_func=self.first_button_func
                                                                    )
        self.second_label, self.second_button = ui_utils.label_button(label_text="Documentation for second button",
                                                                    button_text="Second Button",
                                                                    color=elements.green,
                                                                    button_func=self.second_button_func
                                                                    )
        
        # Dummy Spacer, probably a better way to format this
        self.space = ui_utils.label("")

        self.widgets = [
                        self.first_label, 
                        self.first_button,
                        self.space,
                        self.second_label, 
                        self.second_button, 
                        self.space,
                        ]

