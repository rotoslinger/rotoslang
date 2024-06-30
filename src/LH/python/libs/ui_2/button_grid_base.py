import sys, os

from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
from ui_2 import ui_utils, file_dialog
from ui_2 import file_dialog as file_dialog_ui
import importlib
importlib.reload(file_dialog)
importlib.reload(ui_utils)
from . import elements
importlib.reload(elements)
from ui_2 import button_grid_base_core as core
importlib.reload(core)
from ui_2 import filtered_list
importlib.reload(filtered_list)
from rig_2.weights import utils as weight_utils
importlib.reload(weight_utils)


def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QMainWindow)


class Base(QtWidgets.QWidget):

    def __init__(self,
                 parent=None,
                 win_title = "Base Utilities",
                 win_name = None,
                 height = 300,
                 width = 300,
                 setting_filename = "baseSettings",
                 do_import_export_widgets = False,
                 do_asset_name_widgets = False,
                 auto_order_asset_import_export_widgets = False,
                 default_file_name = "default",
                 save_window_state = False,
                 import_export_checklist_options=[[]],
                 import_label_text="Import to the set file path.",
                 export_label_text="Export to the set file path.",
                 do_tag_window=False,
                 tag_no_export_func=None,
                 tag_remove_no_export_func=None,
                 no_export_tag_options=None,
                 ):
        QtWidgets.QWidget.__init__(self, parent )
        # args
        self.parent = parent
        self.win_title = win_title
        self.win_name = win_name
        self.height = height
        self.width = width
        self.setting_filename = setting_filename
        self.do_import_export_widgets = do_import_export_widgets
        self.do_asset_name_widgets = do_asset_name_widgets
        self.auto_order_asset_import_export_widgets = auto_order_asset_import_export_widgets
        self.default_file_name = default_file_name

        self.save_window_state = save_window_state
        self.import_export_checklist_options = import_export_checklist_options
        self.import_label_text = import_label_text
        self.export_label_text = export_label_text

        self.do_tag_window = do_tag_window
        self.tag_no_export_func = tag_no_export_func
        self.tag_remove_no_export_func = tag_remove_no_export_func
        self.no_export_tag_options = no_export_tag_options


        # Dummy Spacer
        self.space = ui_utils.create_label("")
        self.asset_name_widgets = []
        self.import_export_widgets = []
        self.main_widgets = []
        self.settings_path = os.path.join(os.getenv('HOME'), self.setting_filename + ".ini")
        # self.restore_window_state()
        self.view = QtWidgets.QTreeView(self)
        self.view.setMouseTracking(True)
        self.view.entered.connect(self.handleItemEntered)

        self.no_export_checkboxes = None
        self.remove_no_export_checkboxes = None

    def get_settings_path(self):
        self.settings_path = os.path.join(os.getenv('HOME'), self.setting_filename + ".ini")

    def handleItemEntered(self, index):
        if index.isValid():
            QtGui.QToolTip.showText(
                QtGui.QCursor.pos(),
                index.data(),
                self.view.viewport(),
                self.view.visualRect(index)
                )

    def initialize_main_window(self):
        self.setWindowFlags(QtCore.Qt.Window)
        # self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)

        # If you would like to save preferences on close

        self.setWindowTitle(self.win_title)
        self.setObjectName(self.win_name)

        # Not needed for simple buttons, but leaving in for reference
        self.setAcceptDrops(True) # Very important
        self.create_layout()

    def create_layout(self):
        if self.do_tag_window:
            self.create_tag_window()
        if self.do_asset_name_widgets:
            self.create_asset_name_widgets()
        if self.do_import_export_widgets:
            self.create_import_export_widgets()
        self.create_widgets()
        if self.auto_order_asset_import_export_widgets and self.do_asset_name_widgets and self.do_import_export_widgets:
            self.widgets = self.asset_name_widgets + self.main_widgets + self.tag_window + self.import_export_widgets
        else:
            self.widgets = self.main_widgets

        self.resize(self.height, self.width)
        self.scrollArea  = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()

        # Layout
        self.gridLayout=QtWidgets.QGridLayout(self.scrollAreaWidgetContents)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # self.layout.addWidget(self.scrollArea)

        # VBox
        self.main_layout= QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.scrollArea, 1) # stretch factor > 0
        self.main_layout.addStretch(0) # 0 is full stretch
        # Add
        for index, widget in enumerate(self.widgets):
            self.gridLayout.addWidget(widget, index, 0)

        # add the main layout itself to the primitive ui dialog
        self.setLayout(self.main_layout)
        self.restore_window_state()
        self.scrollArea.scrollContentsBy(100, 100)
        
        

    def asset_name_text_changed(self):
        self.asset_name = self.asset_name_text_box.text()
        if not self.live_update_checkbox[0].isChecked():
            return

        self.import_dialog.asset_name = self.asset_name
        self.import_dialog.default_path=None
        self.import_dialog.get_default_path()

        self.export_dialog.asset_name = self.asset_name
        self.export_dialog.default_path=None
        self.export_dialog.get_default_path()


    def create_widgets(self):
        # This is where you create your self.main_widgets
        return

    def create_asset_name_widgets(self):
        
        self.asset_name_label = ui_utils.create_label("Set Your Asset Name",
                                                      color=elements.blue,
                                                      )
        self.asset_name_text_box = ui_utils.text_box(default_text=self.asset_name, text_changed_func=self.asset_name_text_changed)

        self.live_update_layout, self.live_update_checkbox = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Live Update Path", True],
                                                                                                                   ])
        self.component_filter = filtered_list.Filtered_List()
        self.asset_name_widgets = [
                                    ui_utils.create_collapsable_dock("Asset",
                                                                    [
                                                                    ui_utils.create_heading(text="Asset", color=elements.blue),
                                                                    self.asset_name_label,
                                                                    self.asset_name_text_box,
                                                                    self.live_update_layout,
                                                                    self.component_filter,
                                                                    
                                                                    ],parent=self)
                                  ]           

    def export_func(self):
        return

    def import_func(self):
        return

    def create_import_export_widgets(self):
                ######## Import Guides ###############
        self.import_checkboxes_grid, self.import_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=self.import_export_checklist_options)

        self.import_dialog = file_dialog_ui.File_Dialog(asset_name=self.asset_name,
                                                        default_filename = self.default_file_name,
                                                        default_path=self.default_import_path,
                                                        # contents_changed_func = self.contents_changed
                                                        )
        # import_func_with_args = lambda file_dialog=self.import_dialog, checkboxes = self.import_checkboxes: core.import_all(file_dialog, checkboxes)

        self.import_label, self.import_button = ui_utils.label_button(label_text=self.import_label_text,
                                                                    button_text="Import",
                                                                    color=elements.blue,
                                                                    button_func=self.import_func,
                                                                    bg_color=elements.dark_blue,
                                                                    )
        ######## Export Guides ###############
        self.backup_layout, self.backup_checkbox = ui_utils.check_box_list(checkbox_names_defaults=[
                                                                                                                   ["Save Backup", True],
                                                                                                                   ])
        self.export_checkboxes_grid, self.export_checkboxes = ui_utils.check_box_list(self.import_export_checklist_options)
                                                                                                                   
        self.export_dialog = file_dialog_ui.File_Dialog(asset_name=self.asset_name,
                                                        default_filename = self.default_file_name,
                                                        default_path=self.default_export_path)
        # Export Args
        self.export_label, self.export_button = ui_utils.label_button(label_text=self.export_label_text,
                                                                    button_text="Export",
                                                                    color=elements.purple,
                                                                    button_func=self.export_func,
                                                                    bg_color=elements.dark_purple,
                                                                    )
                                                                    
        self.import_export_widgets = [

                                        ui_utils.create_collapsable_dock("Save Data",
                                                                        [ui_utils.create_collapsable_dock("Export Data",
                                                                                                        [ui_utils.create_heading(text="Export Data", color=elements.purple),
                                                                                                        self.export_label, 
                                                                                                        self.export_button,
                                                                                                        self.export_dialog,
                                                                                                        self.export_checkboxes_grid,
                                                                                                        self.backup_layout,
                                                                                                        ui_utils.separator(),
                                                                                                        self.space],
                                                                                                        elements.purple,
                                                                                                        elements.very_dark_purple),
                                                                        ui_utils.create_collapsable_dock("Import Data",
                                                                                                        [ui_utils.create_heading(text="Import Data", color=elements.blue),
                                                                                                        self.import_label, 
                                                                                                        self.import_button,
                                                                                                        self.import_dialog,
                                                                                                        self.import_checkboxes_grid,
                                                                                                        ui_utils.separator(),
                                                                                                        self.space],
                                                                                                        elements.blue,
                                                                                                        elements.very_dark_blue)],
                                                                        # elements.green,
                                                                        # elements.dark_green,
                                                                        title_size=16),
                                        
                                        ]

    def create_tag_window(self):
        ############ ADD NO EXPORT ########################
        self.no_export_checkbox_grid, self.no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=self.no_export_tag_options, color=elements.green)
        no_export_button_func_with_args = self.tag_no_export_func
        self.no_export_label, self.no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to tag NO_EXPORT",
                                                                    button_text="Tag NO_EXPORT",
                                                                    color=elements.green,
                                                                    bg_color = elements.med_green,
                                                                    button_func=no_export_button_func_with_args
                                                                    )
        no_export_component_label = "Select Component Class and Run to tag NO EXPORT."
        tooltip= ("All nodes in Component must be properly tagged with create_component_tag() in rig_2.tag.utils \n" +
                  "The connect_to_class_node arg must be set to True when tagging nodes with this method.")

        self.no_export_component_label, self.no_export_component_button = ui_utils.label_button(label_text=no_export_component_label,
                                                                    button_text="Tag Component NO_EXPORT",
                                                                    color=elements.green,
                                                                    bg_color = elements.med_green,
                                                                    button_func=core.tag_component_no_export,
                                                                    tooltip=tooltip,
                                                                    )

        ############ REMOVE NO EXPORT ########################
        self.remove_no_export_checkbox_grid, self.remove_no_export_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=self.no_export_tag_options, color=elements.red)
        remove_no_export_button_func_with_args = self.tag_remove_no_export_func
        self.remove_no_export_label, self.remove_no_export_button = ui_utils.label_button(label_text="Select ctrl(s) and run to Remove NO_EXPORT",
                                                                    button_text="Remove NO_EXPORT tag",
                                                                    color=elements.red,
                                                                    bg_color=elements.med_red,
                                                                    button_func=remove_no_export_button_func_with_args
                                                                    )

        no_export_component_label = "Select Component Class and Run to tag NO EXPORT."
        tooltip= ("Be careful, this will remove ALL NO_EXPORT tags from every node in the component")

        self.remove_no_export_component_label, self.remove_no_export_component_button = ui_utils.label_button(label_text=no_export_component_label,
                                                                    button_text="Remove NO_EXPORT from component",
                                                                    color=elements.red,
                                                                    bg_color=elements.med_red,
                                                                    button_func=core.remove_tag_component_no_export,
                                                                    tooltip=tooltip,
                                                                    )


        self.tag_window = [ui_utils.create_collapsable_dock("Tagging",
                                            [
                                                # ui_utils.create_heading(text="Tagging", color=elements.green),
                                                ui_utils.separator(),
                                                self.space,
                                                
                                                ui_utils.create_collapsable_dock("Add No Export",
                                                        [  
                                                        ui_utils.create_heading(text="Add No Export", color=elements.green, size=12),
                                                        self.no_export_label, 
                                                        self.no_export_button,
                                                        self.no_export_checkbox_grid,
                                                        
                                                        ui_utils.separator(),
                                                        self.space,
                                                        self.no_export_component_label,
                                                        self.no_export_component_button,
                                                        ui_utils.separator(),
                                                        self.space
                                                        
                                                        ],
                                                        elements.green,
                                                        elements.dark_green),
                                                ui_utils.create_collapsable_dock("Remove No Export",
                                                        [  
                                                        ui_utils.create_heading(text="Remove No Export", color=elements.red, size=12),
                                                        self.remove_no_export_label, 
                                                        self.remove_no_export_button,
                                                        self.remove_no_export_checkbox_grid,
                                                        ui_utils.separator(),
                                                        self.space,
                                                        
                                                        ui_utils.separator(),
                                                        self.space,
                                                        self.remove_no_export_component_label,
                                                        self.remove_no_export_component_button,
                                                        ui_utils.separator(),
                                                        self.space

                                                        ],
                                                        elements.red,
                                                        elements.very_dark_red),
                                                
                                            ],
                                            # elements.red,
                                            # elements.very_dark_red,
                                            title_size=16,
                                            )]


    def restore_window_state(self):
        self.get_settings_path()
        if not os.path.exists(self.settings_path):
            return
        self.settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        if not self.save_window_state:
            return
        # If you would like to load preferences on on open
        self.restoreGeometry(self.settings_obj.value("windowGeometry"))
        if self.settings_obj.value("assetName"):
            self.asset_name = self.settings_obj.value("assetName")
        if  hasattr(self, "scrollArea"):
            self.scroll_val_y = self.settings_obj.value("scroll_val_y")
            self.scroll_val_x = self.settings_obj.value("scroll_val_x")
            
            # In order to set the scroll you have to connect a range changed....
            self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: self.scrollArea.verticalScrollBar().setSliderPosition(self.scroll_val_y) )
            self.scrollArea.horizontalScrollBar().rangeChanged.connect(lambda: self.scrollArea.horizontalScrollBar().setSliderPosition(self.scroll_val_x) )
       
        #If save import/export path....
        if self.settings_obj.value("importPath") and hasattr(self, "import_dialog"):
            self.import_dialog.contents.setText(self.settings_obj.value("importPath"))
        if self.settings_obj.value("exportPath") and hasattr(self, "export_dialog"):
            self.export_dialog.contents.setText(self.settings_obj.value("exportPath"))


            
    def create_misc_utils(self):
        self.cache_label = ui_utils.create_label("Uncache Nodes for guide placement.", color=elements.blue)
        
        self.cache_slide_widget, dummy = ui_utils.button_row(names_funcs=[["Uncache Slide Deformers", lambda:weight_utils.cache_all_slide_deformers(False)],
                                                                   ["Cache Slide Deformers", lambda:weight_utils.cache_all_slide_deformers(True)]],
                                                      color=elements.blue, bg_color=elements.grey)
        
        self.cache_curve_weights_widget, dummy = ui_utils.button_row(names_funcs=[["Uncache Curve Weights", lambda:weight_utils.cache_all_curve_weights(False)],
                                                                           ["Cache Curve Weights", lambda:weight_utils.cache_all_curve_weights(True)]],
                                                              color=elements.blue, bg_color=elements.grey)
                 
        self.print_geo_label, self.print_geo_button = ui_utils.label_button("Select single transform and press button to print Geometry Dictionary.  \n"
                                                                            + "NurbSurface, Polygon, and nurbsCurve are supported.",
                                                                             "Print Geometry Dictionary",
                                                                              button_func =core.print_geo_dict,
                                                                              color=elements.blue)



    def closeEvent(self, event):
        self.get_settings_path()
        # Save window's geometry
        self.settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        self.settings_obj.setValue("windowGeometry", self.saveGeometry())
        if hasattr(self, "asset_name"):
            self.asset_name = self.asset_name_text_box.text()
            self.settings_obj.setValue("assetName", self.asset_name)
        if hasattr(self, "scrollArea"):
            scroll_val_y = self.scrollArea.verticalScrollBar().value()
            self.settings_obj.setValue("scroll_val_y", scroll_val_y)
            scroll_val_x = self.scrollArea.horizontalScrollBar().value()
            self.settings_obj.setValue("scroll_val_x", scroll_val_x)
        self.mayaWin.removeEventFilter(self)

        #If save import/export path....
        self.settings_obj.setValue("importPath", self.import_dialog.contents.text())
        self.settings_obj.setValue("exportPath", self.export_dialog.contents.text())

    # def set_window_flag_on(self, bla=False):
    #     self.setWindowFlags(QtCore.Qt.Window)
    #     # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    #     return True

    # def set_window_flag_off(self, bla=False):
    #     self.setWindowFlags(QtCore.Qt.Window)
    #     self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)
    #     return True
    def openUI(self):
        self.initialize_main_window()

        if self.win_name == None or self.win_name == "":
            self.win_name = self.win_title.replace(" ", "")
        try:
            try:
                globals()[self.win_name].close()
                globals()[self.win_name].deleteLater()
            except:
                pass
            del globals()[self.win_name]
        except:
            pass
        ptr = OpenMayaUI.MQtUtil.mainWindow()
        self.mayaWin = wrapInstance(int(ptr), QtWidgets.QMainWindow)
        # self.setParent(self.mayaWin)
        # self.installEventFilter(self)
        # self.mayaWin.installEventFilter(self)
        globals()[self.win_name] = self
        globals()[self.win_name].show()
        
        return globals()[self.win_name]
    
    def eventFilter(self, object, event):
        #         if event.type() == QtCore.QEvent.WindowActivate:
        #     self.set_window_flag_on()
        # elif event.type()== QtCore.QEvent.WindowDeactivate:
        #     self.set_window_flag_off()
        if event.type() == QtCore.QEvent.WindowActivate and not self.windowState() == QtCore.Qt.WindowMinimized and not self.windowState() == QtCore.Qt.WindowActive :
            self.raise_()

            QtWidgets.QApplication.setActiveWindow(self)
            # self.mayaWin.blockSignals(True) 
            # QtWidgets.QApplication.setActiveWindow(self.mayaWin)
            # self.mayaWin.blockSignals(False) 
        elif event.type()== QtCore.QEvent.WindowDeactivate:
            self.raise_()
            pass



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

from ui_2 import button_grid_base
reload(button_grid_base)
basething = button_grid_base.Base_Test()
basething.openUI()

@endcode
'''
class Base_Test(Base):

    def __init__(self,
                 **kw):
        super(Base_Test, self).__init__(**kw)
        self.win_title = "Base Test Utilities"
        self.setting_filename = "baseTest"
        self.save_window_state = True


    def first_button_func(self, checkboxes):
        args = [checkbox.isChecked() for checkbox in checkboxes]
        print("You have just pressed the first button checkbox1 is {0}, checkbox 2 is {1}".format(args[0], args[1]))

    def second_button_func(self, file_dialog):
        path = file_dialog.contents.text()
        print("You have just pressed the second button, the path is {0}".format(path))

    def create_widgets(self):
        super(Base_Test, self).create_widgets()

        ####### FIRST BUTTON ################
        ### first button has a label and accepts arguments using a QCheckbox by making use of the lamda function
        self.check_box_grid, self.checkboxes = ui_utils.check_box_list()
        first_button_func_with_args = lambda checkboxes=self.checkboxes: self.first_button_func(checkboxes)
        self.first_label, self.first_button = ui_utils.label_button(label_text="Documentation for first button",
                                                                    button_text="First Button",
                                                                    color=elements.purple,
                                                                    button_func=first_button_func_with_args
                                                                    )



        ####### SECOND BUTTON ################
        self.file_dialogue = file_dialog_ui.File_Dialog()
        second_button_func_with_args = lambda file_dialog=self.file_dialogue: self.second_button_func(file_dialog)
        self.second_label, self.second_button = ui_utils.label_button(label_text="Documentation for second button",
                                                                    button_text="Second Button",
                                                                    color=elements.green,
                                                                    button_func=second_button_func_with_args
                                                                    )
        


        # Dummy Spacer, probably a better way to format this
        self.space = ui_utils.create_label("")

        self.main_widgets = [
                        self.first_label, 
                        self.first_button,
                        self.check_box_grid,
                        self.space,
                        self.second_label, 
                        self.second_button,
                        self.file_dialogue,
                        self.space,
                        ]

