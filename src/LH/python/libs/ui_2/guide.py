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
from ui_2 import file_dialog as file_dialog_ui
reload(file_dialog_ui)
from ui_2 import guide_core 
reload(guide_core)



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

    def export_func(self, dialog):
        print "exporting to {0}".format(dialoge.text())

    def import_func(self, dialog):
        print "importing to {0}".format(dialoge.text())

    def create_buttons(self):
        super(Guide_UI, self).create_buttons()
        # Buttons

        ######## GUIDE VIS ###############
        self.guide_vis_label = ui_utils.label("Guide Visibility.",
                                                                    color=elements.blue,
                                                                    )
        self.button_row_layout, self.buttons = ui_utils.button_row(
                                                                     [
                                                                      ["Vis Guides", guide_core.vis_all_guides],
                                                                      ["Hide Guides", lambda: guide_core.vis_all_guides(False)]
                                                                     ]
                                                                    )
        ######## SELECT GUIDE ###############
        self.select_guide_label, self.select_guide_button = ui_utils.label_button(label_text="Select All Guides.",
                                                                    button_text="Select Guides",
                                                                    color=elements.blue,
                                                                    button_func=guide_core.select_all_guides
                                                                    )

                                                                    
        ######## UPDATE GEOMETRY CONSTRAINT ###############
        self.geo_constraint_label, self.geo_constraint_button = ui_utils.label_button(label_text="Rebinds the geometry constraint for new guide positions.",
                                                                    button_text="Update Geometry Constraints",
                                                                    color=elements.blue,
                                                                    button_func=guide_core.update_geo_constraints
                                                                    )


        ############ ADD NO EXPORT ########################
        self.no_export_checkbox_grid, self.no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Control Shapes", True],
                                                                                                                   ["Guide Positions", True],                                                                                                                   
                                                                                                                   ["Guide Shapes", True],                                                                                                                   
                                                                                                                   ["Gimbal Shapes", True],
                                                                                                                   ])
        no_export_button_func_with_args = lambda: guide_core.tag_no_export(self.no_export_checkboxes)
        self.no_export_label, self.no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to tag NO_EXPORT",
                                                                    button_text="Tag NO_EXPORT",
                                                                    color=elements.green,
                                                                    button_func=no_export_button_func_with_args
                                                                    )

        ############ REMOVE NO EXPORT ########################
        self.remove_no_export_checkbox_grid, self.remove_no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Control Shapes", True],
                                                                                                                   ["Guide Positions", True],                                                                                                                   
                                                                                                                   ["Guide Shapes", True],                                                                                                                   
                                                                                                                   ["Gimbal Shapes", True],
                                                                                                                   ])
        remove_no_export_button_func_with_args = lambda checkboxes=self.remove_no_export_checkboxes: guide_core.remove_tag_no_export(checkboxes)
        self.remove_no_export_label, self.remove_no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to Remove NO_EXPORT",
                                                                    button_text="Remove NO_EXPORT tag",
                                                                    color=elements.red,
                                                                    button_func=remove_no_export_button_func_with_args
                                                                    )

        ######## Import Guides ###############
        self.import_dialog = file_dialog_ui.File_Dialog()
        import_func_with_args = lambda file_dialog=self.import_dialog: self.import_func(file_dialog)
        self.import_label, self.import_button = ui_utils.label_button(label_text="Export guides to the set file path.",
                                                                    button_text="Export",
                                                                    color=elements.purple,
                                                                    button_func=import_func_with_args
                                                                    )
        ######## Export Guides ###############
        self.export_dialog = file_dialog_ui.File_Dialog()
        export_func_with_args = lambda file_dialog=self.export_dialog: self.export_func(file_dialog)
        self.export_label, self.export_button = ui_utils.label_button(label_text="Import guides to the set file path.",
                                                                    button_text="Import",
                                                                    color=elements.purple,
                                                                    button_func=export_func_with_args
                                                                    )



        # Dummy Spacer, probably a better way to format this
        self.space = ui_utils.label("")

        self.widgets = [
                        self.guide_vis_label, 
                        self.button_row_layout,
                        self.space,
                        ui_utils.separator(),
                        self.space,

                        self.select_guide_label, 
                        self.select_guide_button,
                        self.space,
                        ui_utils.separator(),
                        self.space,


                        self.geo_constraint_label, 
                        self.geo_constraint_button,
                        self.space,
                        ui_utils.separator(),
                        self.space,

                        self.no_export_label, 
                        self.no_export_button,
                        self.no_export_checkbox_grid,
                        ui_utils.separator(),
                        self.space,

                        self.remove_no_export_label, 
                        self.remove_no_export_button,
                        self.remove_no_export_checkbox_grid,
                        ui_utils.separator(),
                        self.space,

                        self.import_label, 
                        self.import_button,
                        self.export_dialog,
                        ui_utils.separator(),
                        self.space,

                        self.export_label, 
                        self.export_button,
                        self.import_dialog,
                        ui_utils.separator(),
                        self.space,

                        ]

