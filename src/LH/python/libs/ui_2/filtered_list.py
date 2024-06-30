import sys, os, re
from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
from ui_2 import ui_utils
import importlib
importlib.reload(ui_utils)
from ui_2 import elements
importlib.reload(elements)
from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)
from rig_2.tag import constants as tag_constants
importlib.reload(tag_utils)
from rig_2 import decorator
importlib.reload(decorator)

class Filtered_List(QtWidgets.QWidget):
    def __init__(self,
                 parent = None,
                 do_search_filter = True,
                 do_tag_filter = True,
                 do_component_selector = True,
                 do_component_tag_buttons = True,
                 data_list = [],
                 tag_filter = "COMPONENT_MEMBERSHIP",
                 label= "Filtered List",
                 color = elements.blue,
                 ):
        super(Filtered_List, self).__init__(parent)
        #--args
        self.do_component_selector = do_component_selector
        self.do_search_filter = do_search_filter
        self.data_list = data_list
        self.do_tag_filter = do_tag_filter
        self.do_component_tag_buttons = do_component_tag_buttons
        self.tag_filter = tag_filter
        self.label = label
        self.color = color
        self.tag_filter_line_edit = None
        self.search_line_edit = None
        self.tag_filter_text = ""
        self.search_text = ""
        self.tag_label_widgets = []
        self.tag_vis_widgets = []
        self.tag_select_widgets = []
        #---vars
        # The tag_filter is the actual string of the tag that will be searched for.
        # This can be set as a constant if you don't want an updating dynamic list
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.layout.addStretch(0) # 0 is full stretch

        self.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.vis_tag_dict = {}
        self.tag_visibility_status = {"tag":{}}
        self.select_tag_dict = {}
        self.tag_selectability_status = {"tag":{}}
        self.vis_all_dict = {}
        self.select_all_dict = {}
        
        # QGridLayout.columnCount() isn't working for some reason..... 
        self.num_columns = 0
        self.get_components()
        self.nodes_from_selected_components = []
        self.tag_checklist_contents = None
        
        self.get_all_tags()
        
        if self.label:
            self.label_widget = ui_utils.create_label(self.label, text_size=13, color=self.color)
            self.add_widget_to_layout(self.label_widget)

        if self.do_component_selector:
            self.component_select_layout, self.component_list = ui_utils.label_list("Component",list_height=100, color=self.color,selection_changed_func=self.filter_data)
            self.refresh_button = ui_utils.create_button("Get Components", color=self.color, button_pressed_func=self.populate_component_list)
            self.add_widget_to_layout(self.component_select_layout)
            self.add_widget_to_layout(self.refresh_button)
            self.populate_component_list()

        if self.do_tag_filter:
            self.tag_filter_layout, self.tag_filter_line_edit = ui_utils.label_text_box("Filter Tag", color=self.color, text_changed_func=self.trigger_multi_filter)
            self.add_widget_to_layout(self.tag_filter_layout)
    
        if self.do_search_filter:
            self.search_layout, self.search_line_edit = ui_utils.label_text_box("Search", color=self.color, text_changed_func=self.filter_data)
            self.add_widget_to_layout(self.search_layout)

        if self.do_component_tag_buttons:            
            tag_row_widget, self.tag_contents_grid_layout, self.scrollArea,self.tag_checklist_contents = ui_utils.label_scroll_area(label_name="Tag Vis Selector",
                                                                                                     color=elements.blue,
                                                                                                     list_height=200,
                                                                                                     selection_changed_func=None)
            self.tag_contents_grid_layout.setAlignment(QtCore.Qt.AlignTop)
            
            self.vis_checkbox = QtWidgets.QCheckBox("Vis All")
            self.vis_checkbox.setFont(QtGui.QFont("Helvetica", 12))
            self.vis_checkbox.setChecked(True)
            self.selectable_checkbox = QtWidgets.QCheckBox("All Selectable")
            self.selectable_checkbox.setFont(QtGui.QFont("Helvetica", 12))
            self.selectable_checkbox.setChecked(True)
                        
            self.vis_checkbox.clicked.connect(self.vis_all)
            self.selectable_checkbox.clicked.connect(self.selectable_all)
                        
            self.tag_contents_grid_layout.addWidget(self.vis_checkbox, 0, 1, QtCore.Qt.AlignTop)
            self.tag_contents_grid_layout.addWidget(self.selectable_checkbox, 0, 2, QtCore.Qt.AlignTop)
            self.add_widget_to_layout(tag_row_widget)
            
            self.tag_selection_option_label = ui_utils.create_label("Choose what visibility effects for geometry.  \n" + 
                                                                  "By default visibility only effects shape, which avoids hierarchy visibility changing. \n" +
                                                                  "If transforms have been hidden for certain shapes, such as base geometry, shape vis toggling will need to be done on the transform level."
                                                                  , color=self.color)
            
            self.tag_selection_option_widget, self.tag_selection_option_checkboxes = ui_utils.check_box_list(checkbox_names_defaults=[["Vis effects shape", True],
                                                                                                    ["Vis effects transform", False]], row=True, color=self.color)
            
            self.add_widget_to_layout(self.tag_selection_option_label)
            self.add_widget_to_layout(self.tag_selection_option_widget)
            


        
        self.add_widget_to_layout(ui_utils.create_label("Nodes Associated With Component", color = self.color))
        self.list_widget = ui_utils.collection_list(color=self.color, list_height=200, selection_changed_func=self.list_widget_selection_changed)
        self.add_widget_to_layout(self.list_widget)
        
        self.setLayout(self.layout)
        self.filter_data()

        # This is the tag to search for if you would like to populate based on tag
        self.tag_name = None

        self.create_layout()
        
    def get_all_tags(self):
        self.all_tags = []
        components = tag_utils.get_all_component_names()
        for component in components:
            self.all_tags += tag_utils.get_all_tags_in_component(component)
        # remove duplicate entries
        self.all_tags = list(dict.fromkeys(self.all_tags))

            

    
    def trigger_multi_filter(self):
        self.get_tag_checklists_from_selected()
        self.filter_data()
        

    def vis_all(self):
        if not self.tag_vis_widgets:
            return
        checked = self.vis_checkbox.isChecked()
        for component in self.component_list.selectedItems():
            component = str(component.text())
            self.vis_all_dict[component] = checked
            for idx, checkbox in enumerate(self.tag_vis_widgets):
                checkbox.setChecked(checked)
                tag=self.tag_label_widgets[idx].text()
                vis_selection = [checkbox.isChecked() for checkbox in self.tag_selection_option_checkboxes]
                tag_utils.vis_all_with_tag(self.tag_label_widgets[idx].text(), checked, component, vis_shape=vis_selection[0], vis_transform=vis_selection[1])
                if not component in list(self.tag_visibility_status.keys()):
                    self.tag_visibility_status[component] = {}
                self.tag_visibility_status[component][tag] = checked

    def selectable_all(self):
        if not self.tag_select_widgets:
            return
        checked = self.selectable_checkbox.isChecked()
        for component in self.component_list.selectedItems():
            component = str(component.text())
            self.select_all_dict[component] = checked
            for idx, checkbox in enumerate(self.tag_select_widgets):
                checkbox.setChecked(checked)
                tag=self.tag_label_widgets[idx].text()
                tag_utils.make_selectable_all_with_tag(tag, checked, component)
                if not component in list(self.tag_selectability_status.keys()):
                    self.tag_selectability_status[component] = {}
                self.tag_selectability_status[component][tag] = checked
        
        
        
    def add_widget_to_layout(self, widget):
        self.layout.addWidget(widget, self.num_columns, 0)
        self.num_columns += 1


    def list_widget_selection_changed(self):

        cmds.select([item.text() for item in self.list_widget.selectedItems()])


    def populate_component_list(self):
        self.get_all_tags()
        self.update_tag_all_checklists()

        self.get_components()
        if not self.components:
            return

        self.component_list.clear()
        for item in self.components:
            if item:
                self.component_list.addItem(item)

    def add_data(self):
        return

    def get_components(self):
        self.components = tag_utils.get_all_component_tag_vals()

    def get_nodes_from_selected_components(self):
        self.get_tag_checklists_from_selected()
        nodes = []
        for component_name in [item.text() for item in self.component_list.selectedItems()]:
            nodes += tag_utils.get_nodes_by_component_name(component_name)
        return nodes
    
    @decorator.undo_chunk
    def set_vis_selectability_by_tag(self, idx):
        for component in self.component_list.selectedItems():
            component = str(component.text())
            tag = self.tag_label_widgets[idx].text()
            vis_selection = [checkbox.isChecked() for checkbox in self.tag_selection_option_checkboxes]
            tag_utils.vis_all_with_tag(tag, vis=self.tag_vis_widgets[idx].isChecked(), component=component, vis_shape=vis_selection[0], vis_transform=vis_selection[1])
            if not component in list(self.tag_visibility_status.keys()):
                self.tag_visibility_status[component] = {}
            self.tag_visibility_status[component][tag] =  self.tag_vis_widgets[idx].isChecked()

        for component in self.component_list.selectedItems():
            component = str(component.text())
            tag = self.tag_label_widgets[idx].text()
            tag_utils.make_selectable_all_with_tag(tag, selectable=self.tag_select_widgets[idx].isChecked(), component=component)
            if not component in list(self.tag_selectability_status.keys()):
                self.tag_selectability_status[component] = {}
            self.tag_selectability_status[component][tag] = self.tag_select_widgets[idx].isChecked()

    def get_filter_list(self):
        
        if self.tag_filter_line_edit:
            self.tag_filter_text = self.tag_filter_line_edit.text()

        filter_text = self.tag_filter_text
        if " " in filter_text:
            filter_text.replace(" ", "")
        
        if "," in filter_text:
            filter_text = filter_text.split(",")
        
        if type(filter_text) != list:
            filter_text = [filter_text]
        tmp_list = []
        for tag in filter_text:
            tag=str(tag)
            if not tag:
                continue
            if tag == " " or tag == str(" "):
                continue
            if " " in tag:
                tag.replace(" ", "")
            tmp_list.append(tag)
        return tmp_list

    def get_tag_checklists_from_selected(self):
        self.update_tag_all_checklists()
        if self.tag_label_widgets:
            [x.deleteLater() for x in self.tag_label_widgets]
        if self.tag_vis_widgets:
            [x.deleteLater() for x in self.tag_vis_widgets]
        if self.tag_select_widgets:
            [x.deleteLater() for x in self.tag_select_widgets]
        tags = []
        self.tag_label_widgets = []
        self.tag_vis_widgets = []
        self.tag_select_widgets = []
        # self.tag_dict = {}
        filter_list = self.get_filter_list()
        for component in [str(item.text()) for item in self.component_list.selectedItems()]:
            # self.tag_filter_text
            tags = tag_utils.get_all_tags_in_component(component)
            tags = sorted(list(dict.fromkeys(tags)))
            
            for i in tag_constants.TAG_VIS_SEL_PANEL_IGNORE:
                if i in tags:
                    tags.remove(i)
                    
            if self.tag_filter_line_edit.text():
                final_text = re.compile(self.tag_filter_line_edit.text())
                final_list = list(filter(final_text.search, tags))
                if final_list:
                    tags = final_list

            for idx, tag in enumerate(tags):
                if not tag:
                    continue

                label = ui_utils.create_label(tag, self.color, center=False)

                vis_checkbox = QtWidgets.QCheckBox("Visibility")
                if component in list(self.tag_visibility_status.keys()) and tag in list(self.tag_visibility_status[component].keys()):
                    vis_checkbox.setChecked(self.tag_visibility_status[component][tag])
                else:
                    vis_checkbox.setChecked(True)
                selectable_checkbox = QtWidgets.QCheckBox("Selectable")
                if component in list(self.tag_selectability_status.keys()) and tag in list(self.tag_selectability_status[component].keys()):
                    selectable_checkbox.setChecked(self.tag_selectability_status[component][tag])
                else:
                    selectable_checkbox.setChecked(True)
                
                self.tag_label_widgets.append(label)           
                self.tag_vis_widgets.append(vis_checkbox)      
                self.tag_select_widgets.append(selectable_checkbox)             
                
                func = lambda idx_arg=idx:  self.set_vis_selectability_by_tag(idx_arg)
                self.tag_vis_widgets[idx].clicked.connect(func)
                func2 = lambda idx_arg_1=idx:  self.set_vis_selectability_by_tag(idx_arg_1)
                self.tag_select_widgets[idx].clicked.connect(func2)
                
                # Add one to idx, always reserve space for the vis all and select all widgets...
                self.tag_contents_grid_layout.addWidget(self.tag_label_widgets[idx], idx + 1, 0)
                self.tag_contents_grid_layout.addWidget(self.tag_vis_widgets[idx], idx + 1, 1)
                self.tag_contents_grid_layout.addWidget(self.tag_select_widgets[idx], idx + 1, 2)
                
    def update_tag_all_checklists(self):
        for component in [str(item.text()) for item in self.component_list.selectedItems()]:
            if component in list(self.vis_all_dict.keys()):
                self.vis_checkbox.setChecked(self.vis_all_dict[component])
            else:
                self.vis_all_dict[component] = True
                self.vis_checkbox.setChecked(True)
            if component in list(self.select_all_dict.keys()):
                self.selectable_checkbox.setChecked(self.select_all_dict[component])
            else:
                self.select_all_dict[component] = True
                self.selectable_checkbox.setChecked(True)

    def filter_data(self):
        self.update_tag_all_checklists()

        self.final_list = []
        self.tag_filter_tag_list = []
        self.nodes_from_selected_components = self.get_nodes_from_selected_components()
        if not self.tag_filter_line_edit and not self.search_layout and not self.tag_filter and not self.nodes_from_selected_components:
            return

        if self.tag_filter_line_edit:
            self.tag_filter_text = self.tag_filter_line_edit.text()

        if self.search_line_edit:
            self.search_text = self.search_line_edit.text()

        if not self.tag_filter and not self.tag_filter_text:
            self.final_list = self.nodes_from_selected_components
            self.populate_list()
            return
        
        self.final_list = tag_utils.get_all_with_tag(self.tag_filter)

        # If you are using component selection to narrow down the results, make sure to only include nodes that are in the selected component
        if self.nodes_from_selected_components:
            self.final_list = [x for x in self.final_list if x in self.nodes_from_selected_components]

        if not self.search_text and not self.tag_filter_text:
            self.populate_list()
            return
        
        # Search name using regular expression module
        final_text = re.compile(self.search_text)
        self.final_list = list(filter(final_text.search, self.final_list))
        
        # Search using TAGS with regular expression
        filtered_tags = []  
        if self.tag_filter_line_edit.text():
            final_text = re.compile(self.tag_filter_line_edit.text())
            final_list = list(filter(final_text.search, self.all_tags))
            if final_list:
                filtered_tags = final_list
            tmp_list = []
            for tag in filtered_tags:
                tag=str(tag)
                if not tag:
                    continue
                if tag == " " or tag == str(" "):
                    continue
                if " " in tag:
                    tag.replace(" ", "")
                tmp_list += [x for x in self.final_list if cmds.objExists(x + "." + tag)]

            self.final_list = tmp_list

        ###################
        self.populate_list()



    def sort_list(self, by_type=True, alphabetic=True):
        type_dict = {}
        self.final_list =[str(x) for x in self.final_list]
        if alphabetic:
            self.final_list.sort(key=str.lower)
        if not by_type:
            return
        for node in self.final_list:
            if cmds.objectType(node) not in type_dict:
                type_dict[cmds.objectType(node)] = []
            type_dict[cmds.objectType(node)].append(node)
        self.final_list = []
        for key, value in sorted(type_dict.items()):
            self.final_list += value



    def populate_list(self):
        self.update_tag_all_checklists()
        if not self.final_list:
            return

        self.list_widget.clear()

        # Get rid of duplicates...
        self.final_list = list(dict.fromkeys(self.final_list))
        self.sort_list()

        for item in self.final_list:
            icon = ui_utils.get_outliner_icon(item)
            item = QtWidgets.QListWidgetItem(icon, item)
            self.list_widget.addItem(item)



    def create_layout(self):
        return
