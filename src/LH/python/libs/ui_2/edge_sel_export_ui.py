import sys
import json
import os
from PySide2.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QFileDialog, QLabel, QScrollArea, QGridLayout, QToolTip
)
from PySide2.QtCore import Qt
import shiboken2
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

def maya_main_window():
    # Get Maya's main window pointer to attach our UI to it
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QDialog)  # Use QDialog

class ExportToolUI(QDialog):  # Use QDialog instead of QWidget
    def __init__(self, parent=None):
        super(ExportToolUI, self).__init__(parent)
        self.setWindowTitle("Export Tool")
        self.setGeometry(300, 300, 600, 400)
        self.setLayout(QVBoxLayout())  # Directly setting the layout
        
        self.create_widgets()
        self.setup_tooltips()
        self.load_default_path()

    def create_widgets(self):
        # Main layout
        main_layout = self.layout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QDialog())  # Use QDialog here as well
        scroll_area.widget().setLayout(QVBoxLayout())
        
        # Export to JSON button
        self.export_json_btn = QPushButton("Export to JSON")
        self.export_json_btn.clicked.connect(self.export_to_json)
        scroll_area.widget().layout().addWidget(self.export_json_btn)
        
        # Export mirrored button
        self.export_mirrored_btn = QPushButton("Export Mirrored")
        self.export_mirrored_btn.clicked.connect(self.export_mirrored)
        scroll_area.widget().layout().addWidget(self.export_mirrored_btn)
        
        # Path input and button
        path_layout = QHBoxLayout()
        self.path_line_edit = QLineEdit()
        self.path_line_edit.setPlaceholderText("Type or paste a path here...")
        self.export_location_btn = QPushButton("Export Location")
        self.export_location_btn.clicked.connect(self.select_export_location)
        path_layout.addWidget(QLabel("Path:"))
        path_layout.addWidget(self.path_line_edit)
        path_layout.addWidget(self.export_location_btn)
        scroll_area.widget().layout().addLayout(path_layout)
        
        # Name input
        self.name_line_edit = QLineEdit("l_part_name")
        scroll_area.widget().layout().addWidget(QLabel("Name:"))
        scroll_area.widget().layout().addWidget(self.name_line_edit)
        
        # Edge selection rows
        self.edge_selection_layout = QGridLayout()
        self.edge_selection_widgets = []
        self.add_edge_selection_row()
        scroll_area.widget().layout().addLayout(self.edge_selection_layout)
        
        main_layout.addWidget(scroll_area)
    
    def setup_tooltips(self):
        # Set tooltips without QToolTip.setDelay() as it's not available in PySide2
        self.export_json_btn.setToolTip(
            "Creates a dictionary of edges, formats it properly, and exports it to a dictionary."
        )
        self.export_mirrored_btn.setToolTip("Export mirrored edges as a dictionary.")
        self.path_line_edit.setToolTip(
            "Type or paste a path here, or use the ‘Export Location’ button to select a directory."
        )
        self.export_location_btn.setToolTip("Select a directory.")
    
    def load_default_path(self):
        # Load the default path from saved settings
        default_path = self.get_saved_path()
        if default_path:
            self.path_line_edit.setText(default_path)
    
    def get_saved_path(self):
        # Here you would get the saved path from Maya preferences or a settings file
        return cmds.optionVar(q="exportTool_defaultPath") if cmds.optionVar(exists="exportTool_defaultPath") else ""
    
    def save_default_path(self, path):
        # Here you would save the path to Maya preferences or a settings file
        cmds.optionVar(sv=("exportTool_defaultPath", path))
    
    def select_export_location(self):
        path = QFileDialog.getExistingDirectory(self, "Select Export Directory", self.path_line_edit.text())
        if path:
            self.path_line_edit.setText(path)
            self.save_default_path(path)
    
    def add_edge_selection_row(self):
        row_count = len(self.edge_selection_widgets)
        edge_label = QLabel("Edge Selection:")
        edge_input = QLineEdit()
        update_btn = QPushButton("Update Selection")
        new_row_btn = QPushButton("New Row")
        update_btn.clicked.connect(lambda: self.update_edge_selection(edge_input))
        new_row_btn.clicked.connect(self.add_edge_selection_row)
        
        self.edge_selection_widgets.append((edge_input, update_btn, new_row_btn))
        
        self.edge_selection_layout.addWidget(edge_label, row_count, 0)
        self.edge_selection_layout.addWidget(edge_input, row_count, 1)
        self.edge_selection_layout.addWidget(update_btn, row_count, 2)
        self.edge_selection_layout.addWidget(new_row_btn, row_count, 3)
    
    def update_edge_selection(self, edge_input):
        selection = cmds.ls(selection=True, flatten=True)
        edge_list = []
        
        for obj in selection:
            if cmds.objectType(obj) == 'mesh':
                edges = cmds.polyListComponentConversion(obj, toEdge=True)
                edge_list.extend(edges)
        
        if edge_list:
            edge_input.setText(str(edge_list))
            if edge_input.text():
                self.add_edge_selection_row()
        else:
            cmds.warning("Selection is not edges or there are no edges selected.")
    
    def export_to_json(self):
        path = self.path_line_edit.text()
        name = self.name_line_edit.text()
        if not path.endswith(".json"):
            path = os.path.join(path, f"{name}.json")
        self.export_json(path)
    
    def export_json(self, file_path, data=None):
        if data is None:
            data = self.collect_edge_data()

        # Check if file exists and handle backups
        if os.path.exists(file_path):
            if not os.access(file_path, os.W_OK):
                file_name, file_ext = os.path.splitext(file_path)
                backup_dir = os.path.join(os.path.dirname(file_path), "backup_dictionaries")
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                backup_files = [f for f in os.listdir(backup_dir) if f.startswith(os.path.basename(file_name))]
                new_backup_name = f"{file_name}__BAK__v{str(len(backup_files)+1).zfill(3)}{file_ext}"
                os.rename(file_path, os.path.join(backup_dir, new_backup_name))
        
        # Save new JSON file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def collect_edge_data(self):
        # Collect data from edge selections
        data = {}
        for edge_input, _, _ in self.edge_selection_widgets:
            if edge_input.text():
                data[edge_input.text()] = edge_input.text()
        return data
    
    def export_mirrored(self):
        # Collect edge data
        edge_data = self.collect_edge_data()
        
        # Mirror edge data logic
        mirrored_data = self.mirror_edge_data(edge_data)
        
        # Save mirrored data
        path = self.path_line_edit.text()
        name = self.name_line_edit.text()
        if not path.endswith(".json"):
            path = os.path.join(path, f"mirrored_{name}.json")
        self.export_json(path, mirrored_data)
    
    def mirror_edge_data(self, edge_data):
        # Dummy function for mirroring edge data
        mirrored_data = {}
        for key, value in edge_data.items():
            mirrored_data[f"mirrored_{key}"] = value
        return mirrored_data

def run():
    # Use the Maya main window as parent
    parent = maya_main_window()
    
    # Create and show the tool UI
    window = ExportToolUI(parent=parent)
    window.show()

if __name__ == "__main__":
    run()