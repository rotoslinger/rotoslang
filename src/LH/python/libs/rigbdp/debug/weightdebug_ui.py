import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class SkinInfoUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(SkinInfoUI, self).__init__(parent)

        self.setWindowTitle("BDP Debug Utils - Skin Info")
        self.setMinimumWidth(300)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_ui()
        self.create_connections()

    def create_ui(self):
        # Filter Geometry Type
        self.geom_type_label = QtWidgets.QLabel("Filter Geometry Type:")
        self.geom_type_combo = QtWidgets.QComboBox()
        self.geom_type_combo.addItem("None", None)
        self.geom_type_combo.addItem("Mesh", "mesh")
        self.geom_type_combo.addItem("Nurbs Curve", "nurbsCurve")
        self.geom_type_combo.addItem("Nurbs Surface", "nurbsSurface")
        self.geom_type_combo.addItem("Lattice", "lattice")

        # Print Shapes
        self.print_shapes_checkbox = QtWidgets.QCheckBox("Print Shapes")

        # Filter Geometry Name
        self.geom_name_label = QtWidgets.QLabel("Filter Geometry Name:")
        self.geom_name_line_edit = QtWidgets.QLineEdit()

        # Skin Cluster List
        self.skin_clusters_label = QtWidgets.QLabel("Skin Clusters:")
        self.skin_clusters_list = QtWidgets.QListWidget()
        self.skin_clusters_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)  # Enable multi-selection

        # Buttons
        self.populate_button = QtWidgets.QPushButton("Populate Skin Clusters")
        self.select_skincluster_button = QtWidgets.QPushButton("Select Skin Cluster in Scene")
        self.run_button = QtWidgets.QPushButton("Run")
        self.close_button = QtWidgets.QPushButton("Close")

        # Layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.geom_type_label, self.geom_type_combo)
        form_layout.addRow(self.print_shapes_checkbox)
        form_layout.addRow(self.geom_name_label, self.geom_name_line_edit)
        form_layout.addRow(self.populate_button)
        form_layout.addRow(self.skin_clusters_label, self.skin_clusters_list)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.select_skincluster_button)
        button_layout.addWidget(self.close_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.populate_button.clicked.connect(self.populate_skin_clusters)
        self.select_skincluster_button.clicked.connect(self.select_skin_cluster)
        self.run_button.clicked.connect(self.run_skin_infos)
        self.close_button.clicked.connect(self.close)

    def populate_skin_clusters(self):
        """ Populate skin clusters based on the filter geometry name, ensuring no duplicates. """
        self.skin_clusters_list.clear()
        filter_geom_name = self.geom_name_line_edit.text()
    
        if filter_geom_name:
            added_skin_clusters = set()  # Keep track of added skin clusters to avoid duplicates
            for skin in cmds.ls(type="skinCluster"):
                geos = cmds.skinCluster(skin, q=True, g=True)
                for geo in geos:
                    if filter_geom_name in geo and skin not in added_skin_clusters:
                        self.skin_clusters_list.addItem(skin)
                        added_skin_clusters.add(skin)

    def select_skin_cluster(self):
        """ Select the skin cluster(s) in the Maya scene based on the user's selection in the UI. """
        selected_skin_clusters = [item.text() for item in self.skin_clusters_list.selectedItems()]
        if selected_skin_clusters:
            cmds.select(selected_skin_clusters)

    def run_skin_infos(self):
        filter_geom_type = self.geom_type_combo.currentData()
        print_shapes = self.print_shapes_checkbox.isChecked()
        filter_geom_name = self.geom_name_line_edit.text() or None

        # Call the skin_infos function with user input
        skin_infos(filter_geom_type=filter_geom_type, print_shapes=print_shapes, filter_geom_name=filter_geom_name)

def print_skin_infos(geo, skin, print_shapes):
    if not print_shapes:
        geo = cmds.listRelatives(geo, parent=True)[0]
    print("{0} -------------- bound to skinCluster ------------ {1}.".format(geo, skin))

def skin_infos(filter_geom_type=None, print_shapes=False, filter_geom_name=None):
    print("##############################################################################################################")
    print("############################################## START #########################################################")
    print("##############################################################################################################")
    for skin in cmds.ls(type="skinCluster"):
        geom = cmds.skinCluster(skin, q=True, g=True)
        for geo in geom:
            if filter_geom_type is not None and filter_geom_type == cmds.objectType(geo):
                if filter_geom_name is None:
                    print_skin_infos(geo, skin, print_shapes)
                    continue
                if filter_geom_name is not None and filter_geom_name in geo:
                    print_skin_infos(geo, skin, print_shapes)
                    continue
            if filter_geom_type is None:
                if filter_geom_name is None:
                    print_skin_infos(geo, skin, print_shapes)
                    continue
                if filter_geom_name is not None and filter_geom_name in geo:
                    print_skin_infos(geo, skin, print_shapes)
                    continue
    print("##############################################################################################################")
    print("##############################################  END  #########################################################")
    print("##############################################################################################################")

if __name__ == "__main__":
    try:
        SkinInfoUI.close()  # Close previous instance if it exists
        SkinInfoUI.deleteLater()
    except:
        pass

    skin_info_ui = SkinInfoUI()
    skin_info_ui.show()
