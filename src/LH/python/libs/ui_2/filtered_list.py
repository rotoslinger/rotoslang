import sys, os, re
from PySide2 import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
from maya import cmds
from ui_2 import ui_utils
reload(ui_utils)
from ui_2 import elements
reload(elements)
from rig_2.tag import utils as tag_utils
reload(tag_utils)

class Filtered_List(QtWidgets.QWidget):
    def __init__(self,
                 parent = None,
                 do_search_filter = True,
                 do_tag_filter = True,
                 do_component_selector = True,
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
        self.tag_filter = tag_filter
        self.label = label
        self.color = color
        self.tag_filter_line_edit = None
        self.search_line_edit = None
        self.tag_filter_text = ""
        self.search_text = ""
        #---vars
        # The tag_filter is the actual string of the tag that will be searched for.
        # This can be set as a constant if you don't want an updating dynamic list
        self.layout = QtWidgets.QGridLayout()
        # QGridLayout.columnCount() isn't working for some reason..... 
        self.num_columns = 0
        self.components = self.get_components()
        self.nodes_from_selected_components = []

        if self.label:
            self.label_widget = ui_utils.create_label(self.label, text_size=13, color=self.color)
            self.layout.addWidget(self.label_widget, self.num_columns, 0)
            self.num_columns += 1

        if self.do_component_selector:
            self.component_select_layout, self.component_list = ui_utils.label_list("Component", color=self.color, selection_changed_func=self.filter_data)
            self.layout.addWidget(self.component_select_layout, self.num_columns, 0)
            self.num_columns += 1
            self.populate_component_list()

        if self.do_tag_filter:
            self.tag_filter_layout, self.tag_filter_line_edit = ui_utils.label_text_box("Filter Tag", color=self.color, text_changed_func=self.filter_data)
            self.layout.addWidget(self.tag_filter_layout, self.num_columns, 0)
            self.num_columns += 1
    
        if self.do_search_filter:
            self.search_layout, self.search_line_edit = ui_utils.label_text_box("Search", color=self.color, text_changed_func=self.filter_data)
            self.layout.addWidget(self.search_layout, self.num_columns, 0)
            self.num_columns += 1



        self.list_widget = ui_utils.collection_list(color=self.color, selection_changed_func=self.list_widget_selection_changed)


        # self.list_widget = ui_utils.collection_list(color=self.color, selection_changed_func=self.list_widget_selection_changed)
        self.layout.addWidget(self.list_widget, self.num_columns, 0)
        self.num_columns += 1

        self.setLayout(self.layout)
        self.filter_data()


        # This is the tag to search for if you would like to populate based on tag
        self.tag_name = None

        self.create_layout()

    def list_widget_selection_changed(self):

        cmds.select([item.text() for item in self.list_widget.selectedItems()])


    def populate_component_list(self):
        if not self.components:
            return

        self.component_list.clear()
        for item in self.components:
            if item:
                self.component_list.addItem(item)

    def add_data(self):
        return

    def get_components(self):
        return tag_utils.get_all_component_tag_vals()

    def get_nodes_from_selected_components(self):
        nodes = []
        for component_name in [item.text() for item in self.component_list.selectedItems()]:
            print component_name
            nodes += tag_utils.get_nodes_by_component_name(component_name)
        return nodes

    def filter_data(self):
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

        if self.tag_filter_text:
            self.tag_filter_tag_list = tag_utils.get_all_with_tag(self.tag_filter_text)
            self.final_list = [x for x in self.final_list if x in self.tag_filter_tag_list]
            
        # If you are using component selection to narrow down the results, make sure to only include nodes that are in the selected component
        if self.nodes_from_selected_components:
            self.final_list = [x for x in self.final_list if x in self.nodes_from_selected_components]

        if not self.search_text:
            self.populate_list()
            return

        # Search using regular expression module
        final_text = re.compile(self.search_text)
        self.final_list = list(filter(final_text.search, self.final_list))
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
