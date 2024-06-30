import sys, os
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds
from ui_2 import elements
import importlib
importlib.reload(elements)

from rig_2.tag import utils as tag_utils
importlib.reload(tag_utils)



OPERATING_SYSTEM = sys.platform

def test_func():
    print("Test func is working")

def get_outliner_icon(maya_object):
    if not maya_object:
        maya_object = cmds.ls(sl=True)[0]
    maya_object_type = cmds.objectType(maya_object)
    # If the object is a transform and has a shape, set the type to that of the shape
    if maya_object_type == "transform" and cmds.listRelatives(s=True):
        maya_object_type = cmds.objectType(cmds.listRelatives(s=True)[0])
    file_dir = ":/{0}.svg".format(maya_object_type)

    testfile = QtCore.QFile(file_dir)
    if not testfile.exists():
        file_dir = ":/default.svg"
    return QtGui.QIcon(file_dir)

def create_label(text="test", color="color: rgb(255, 102, 255);", center=True, text_size=None):

    label = QtWidgets.QLabel(text)
    label.setStyleSheet(color)
    if text_size:
        label.setFont(QtGui.QFont("Times", text_size)) 
    if center:
        label.setAlignment(QtCore.Qt.AlignCenter)
    return label

def create_heading(text="test", color="color: rgb(255, 102, 255);", size=14):
    label = create_label(text=text, color=color, center=True)
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setFont(QtGui.QFont("Times", size, QtGui.QFont.Bold)) 
    return label


def create_button(text="test",
                  color=elements.light_grey,
                  bg_color= elements.grey,
                  button_pressed_func=None,
                  tooltip="",
                  tooltip_color=elements.black):
    button = QtWidgets.QPushButton(text)
    if bg_color:
        bg_color = "background-" + bg_color
        color = "QPushButton {" + "{0}{1}".format(color, bg_color) + "}"
    button.setStyleSheet(color)
    if button_pressed_func:
        button.clicked.connect(button_pressed_func)
    if tooltip:
        button.setToolTip(tooltip)
        tooltip_color =  "QToolTip {0}".format(r"{" + tooltip_color + r"}")
        button.setStyleSheet(color + ";" + tooltip_color)
    return button

def label_button(label_text="Test label",
                 button_text="Test button",
                 color="color: rgb(255, 102, 255);",
                 button_func=test_func,
                 bg_color=elements.grey,
                 tooltip="",
                 ):
    label = create_label(text=label_text, color=color)
    button = create_button(text=button_text, color=color, bg_color=bg_color, tooltip=tooltip)
    button.clicked.connect(button_func)
    return label, button

def text_box(default_text="baseAsset", text_changed_func=None):
    text_field = QtWidgets.QLineEdit()
    text_field.setText(default_text)
    if text_changed_func:
        text_field.textChanged.connect(text_changed_func)
    return text_field

def label_text_box(label_name="Test: ", text_edit_default="", color=elements.blue, column_min_size=50, text_changed_func=None):
    grid_layout=QtWidgets.QGridLayout()
    layout = QtWidgets.QWidget()
    layout.setLayout(grid_layout)
    label = QtWidgets.QLabel(label_name)
    line_edit = text_box(text_edit_default, text_changed_func)
    grid_layout.addWidget(label, 0, 0)
    grid_layout.addWidget(line_edit, 0, 1)
    grid_layout.setColumnMinimumWidth(0, column_min_size)

    return layout, line_edit 

def collection_list(color=elements.blue, list_height=None, selection_changed_func=None):
    selection_list = QtWidgets.QListWidget()
    selection_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    selection_list.setAcceptDrops(True)
    selection_list.setDragDropMode(selection_list.InternalMove)
    if list_height:
        selection_list.setFixedHeight(list_height)
    if selection_changed_func:
        selection_list.selectionModel().selectionChanged.connect(selection_changed_func)
    return selection_list

def set_vis_selectability_by_tag(tag_name, vis, selectable):
    tag_utils.vis_all_with_tag(tag_name, vis=vis)
    tag_utils.make_selectable_all_with_tag(tag_name, selectable=selectable)

def tag_button_row(tag_name = "GUIDE", color=elements.blue):
    grid_layout=QtWidgets.QGridLayout()
    buttons = []
    layout = QtWidgets.QWidget()
    layout.setLayout(grid_layout)
    label = create_label(tag_name, color)
    vis_checkbox = QtWidgets.QCheckBox("Visibility")
    vis_checkbox.setChecked(True)
    selectable_checkbox = QtWidgets.QCheckBox("Selectable")
    selectable_checkbox.setChecked(True)
    func = lambda: set_vis_selectability_by_tag(label.text(), vis_checkbox.checkState(), selectable_checkbox.checkState())
    
    vis_checkbox.stateChanged.connect(func)
    selectable_checkbox.stateChanged.connect(func)
    grid_layout.addWidget(label, 0, 0)
    grid_layout.addWidget(vis_checkbox, 0, 1)
    grid_layout.addWidget(selectable_checkbox, 0, 2)
    return layout
    
def label_scroll_area(label_name="Test: ", color=elements.blue, list_height=200, selection_changed_func=None, parent=None):
    scroll_area  = QtWidgets.QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setFixedHeight(list_height)
    
    # self.scrollArea  = QtWidgets.QScrollArea(self)
    # self.scrollArea.setWidgetResizable(True)
    # self.scrollArea.setFixedHeight(200)


    scroll_contents = QtWidgets.QWidget()


    contents_grid_layout=QtWidgets.QGridLayout(scroll_contents)
    contents_grid_layout.setSpacing(10)

    # Layout
    scroll_area.setWidget(scroll_contents)
    tag_label = QtWidgets.QLabel(label_name)
    
    layout=QtWidgets.QGridLayout(scroll_contents)
    layout.setSpacing(10)
    
    
    layout.addWidget(tag_label, 0,0)
    layout.addWidget(scroll_area, 0,1)
    
    row_widget = QtWidgets.QWidget()
    row_widget.setLayout(layout)
    
    return row_widget, contents_grid_layout, scroll_area, scroll_contents

def label_list(label_name="Test: ", color=elements.blue, list_height=200, selection_changed_func=None):
    grid_layout=QtWidgets.QGridLayout()
    layout = QtWidgets.QWidget()
    layout.setLayout(grid_layout)
    label = QtWidgets.QLabel(label_name)
    selection_list = collection_list(color=color, list_height=list_height, selection_changed_func=selection_changed_func)
    # selection_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    # selection_list.setAcceptDrops(True)
    # selection_list.setDragDropMode(selection_list.InternalMove)

    grid_layout.addWidget(label, 0, 0)
    grid_layout.addWidget(selection_list, 0, 1)


    # if list_height:
    #     selection_list.setFixedHeight(list_height)
    # if selection_changed_func:
    #     selection_list.selectionModel().selectionChanged.connect(selection_changed_func)
        
    return layout, selection_list 


def get_QColor_from_style(style_color):
    "color: rgb(90, 90, 90);"
    style_color = style_color.split("(")[1].split(")")[0].split(",")
    # style_color = tuple(style_color)
    style_color = [int(x) for x in style_color]
    return QtGui.QColor(*style_color)



class DockContents(QtWidgets.QFrame):
    def __init__(self, name="TEST", parent=None, color=None, bg_color=None):
        super(DockContents, self).__init__(parent=parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Background)
        p = self.palette()
        tmp_bg_color = get_QColor_from_style(bg_color)
        tmp_fg_color = get_QColor_from_style(color)
        p.setColor(self.backgroundRole(), tmp_bg_color)
        p.setColor(self.foregroundRole(), tmp_fg_color)
        self.setPalette(p)
        # self.setStyleSheet(get_bg_color_from_color(bg_color) + ';' + get_fg_color_from_color(color))


def change_in_size():
    print("AAAAAAAAAAAA")
    
def get_bg_color_from_color(color):
    return color.replace("color", "background-color: ")

def get_fg_color_from_color(color):
    return color.replace("color", "foreground-color: ")

class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    def __init__(self, name="TEST", parent=None, widgets=None, color=None, bg_color=None, title_size=8, sp_color=elements.purple):
        super(MainWindow, self).__init__(parent=parent)
        
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Background)
        p = self.palette()
        tmp_bg_color = get_QColor_from_style(bg_color)
        tmp_fg_color = get_QColor_from_style(color)
        p.setColor(self.backgroundRole(), tmp_bg_color)
        p.setColor(self.foregroundRole(), tmp_fg_color)
        self.setPalette(p)
        
        
        self.win_name = name + "_Main"
        self.setObjectName(self.win_name)

        self.widgets = widgets
        # QtWidgets.QMainWindow.__init__(self)

        self.dock = QtWidgets.QDockWidget(name, self)
        self.dock.setFont(QtGui.QFont("Helvetica", title_size, QtGui.QFont.DemiBold))
        
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock)
        
        contents = DockContents(name=name, color=color, bg_color=bg_color)

        contents.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        contents.setLineWidth(2)
        
        layout = QtWidgets.QVBoxLayout(contents)
        layout.setContentsMargins(0, 0, 0, 0)



        for index, widget in enumerate(self.widgets):
            layout.addWidget(widget)

        self.dock.setWidget(contents)
        
    # def cleanup(self):
    #     try:
    #         globals()[self.win_name].close()
    #         globals()[self.win_name].deleteLater()
    #     except:
    #         pass
    #     del globals()[self.win_name]
        
    # def closeEvent(self, event):
    #     self.cleanup()

        
def create_collapsable_dock(text, widget_list, color=elements.blue, bg_color = elements.base_grey, parent=None, title_size=8):
    dock = MainWindow(name=text, parent=parent, widgets=widget_list, color=color, bg_color=bg_color, title_size=title_size)
        
        
        # self.setCentralWidget(self.dock)

        # self.widgets = widgets
        
        
        
        # self.dock = QtWidgets.QDockWidget(name, self)
        # self.scrollArea  = QtWidgets.QScrollArea()
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollAreaWidgetContents = QtWidgets.QWidget()

        # # Layout
        # self.gridLayout=QtWidgets.QGridLayout(self.scrollAreaWidgetContents)

        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # # self.layout.addWidget(self.scrollArea)

        # # Add
        # for index, widget in enumerate(self.widgets):
        #     self.gridLayout.addWidget(widget, index, 0)
            
        # # VBox
        # self.main_layout= QtWidgets.QVBoxLayout()
        # self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.main_layout.setSpacing(0)
        # self.main_layout.addWidget(self.scrollArea, 1) # stretch factor > 0
        # self.main_layout.addStretch(0) # 0 is full stretch
            
            
            
        # # add the main layout itself to the primitive ui dialog
        # self.setLayout(self.main_layout)

        # self.setCentralWidget(self.dock)
        
        # self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dock)
        




    #     print 'Test button was clicked'

# def create_collapsable_dock(text, widget_list, color=elements.blue, bg_color = elements.base_grey):
#     dock = QtWidgets.QDockWidget(text)
#     dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
#     dock.setAutoFillBackground(True)
#     dock.setStyleSheet(color)
#     dock.setFont(QtGui.QFont("Helvetica", 8, QtGui.QFont.DemiBold))

    
#     scrollArea  = QtWidgets.QScrollArea()
#     scrollArea.setWidgetResizable(True)

#     scrollAreaWidgetContents = DockContents()
#     scrollAreaWidgetContents.setSizeHint(400, 100)
#     scrollAreaWidgetContents.resize(4000,100)
#     # layout = QtWidgets.QVBoxLayout(dock)
#     # # layout.setContentsMargins(0, 0, 0, 0)
#     # # layout.setSpacing(1)
#     # layout.addStretch(0) # 0 is full stretch

#     # scrollAreaWidgetContents.setLayout(layout)

#     # Layout
#     gridLayout=QtWidgets.QGridLayout(scrollAreaWidgetContents)

#     scrollArea.setWidget(scrollAreaWidgetContents)
#     # scrollArea.setFixedSize(500,300)
#     for i in dir(scrollArea):
#         if "add" in i or "Add" in i:
#             print i
#     scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
#     scrollArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    
                                    
#     collapse_box = CollapsibleBox()
#     collapse_box.content_area.setBackgroundRole(QtGui.QPalette.Background)
#     p = collapse_box.content_area.palette()
#     bg_color = get_QColor_from_style(bg_color)
#     p.setColor(collapse_box.content_area.backgroundRole(), bg_color)
#     collapse_box.content_area.setPalette(p)


#     collapse_box.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
#     collapse_box.setLineWidth(2)
#     gridLayout.addWidget(collapse_box, 0, 0)
    
    
#     layout = QtWidgets.QVBoxLayout()
#     layout.setContentsMargins(0, 0, 0, 0)
#     layout.setSpacing(0)
#     layout.addStretch() # 0 is full stretch

#     for idx, widget in enumerate(widget_list):
#         layout.addWidget(widget,1)
#     dock.setWidget(scrollArea)
    
#     print scrollArea.sizeHint()

#     collapse_box.setContentLayout(layout)
#     # scrollArea.resize(1000, 300)
#     # scrollAreaWidgetContents.resize(4000,100)

#     return dock

# def create_collapsable_dock(text, widget_list, color=elements.blue, bg_color = elements.base_grey):
#     dock = QtWidgets.QDockWidget(text)
#     dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
#     dock.setAutoFillBackground(True)
#     dock.setStyleSheet(color)
#     dock.setFont(QtGui.QFont("Helvetica", 8, QtGui.QFont.DemiBold))
    
#     scrollArea  = QtWidgets.QScrollArea()
#     scrollArea.setWidgetResizable(True)

#     scrollAreaWidgetContents = QtWidgets.QWidget()

#     # Layout
#     gridLayout=QtWidgets.QGridLayout(scrollAreaWidgetContents)

#     scrollArea.setWidget(scrollAreaWidgetContents)

    
    
#     for idx, widget in enumerate(widget_list):
#         gridLayout.addWidget(widget,idx,0)
#     dock.setWidget(scrollArea)
    

#     return dock
# def create_collapsable_dock(text, widget_list, color=elements.blue, bg_color = elements.base_grey, parent=None):
#     dock = MainWindow(name=text, parent=parent, widgets=widget_list, color=color, bg_color=bg_color)
    # dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
    # dock.setAutoFillBackground(True)
    # dock.setStyleSheet(color)
    # dock.setFont(QtGui.QFont("Helvetica", 8, QtGui.QFont.DemiBold))
    
    # scrollArea  = QtWidgets.QScrollArea()
    # scrollArea.setWidgetResizable(True)

    # scrollAreaWidgetContents = QtWidgets.QWidget()

    # # Layout
    # gridLayout=QtWidgets.QGridLayout(scrollAreaWidgetContents)

    # scrollArea.setWidget(scrollAreaWidgetContents)

    
    
    # for idx, widget in enumerate(widget_list):
    #     gridLayout.addWidget(widget,idx,0)
    # dock.setWidget(scrollArea)
    

    return dock

        
class CollapsibleBox(QtWidgets.QFrame ):
    def __init__(self, title="", parent=None, collapsed=False):
        super(CollapsibleBox, self).__init__(parent)
        # self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.collapsed = collapsed
        self.toggle_button = QtWidgets.QToolButton(text=title, checkable=True, checked=not self.collapsed)
        
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        if self.collapsed:
            self.toggle_button.setArrowType(QtCore.Qt.ArrowType.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QtWidgets.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)
    
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self.content_area, b"maximumHeight"))

        if not self.collapsed:
            self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow )
            self.toggle_animation.setDirection(QtCore.QAbstractAnimation.Forward )
            content_animation  = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
            self.toggle_animation.start()
    # @QtCore.pyqtSlot()
    @QtCore.Slot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow if not checked else QtCore.Qt.ArrowType.RightArrow)
        self.toggle_animation.setDirection(QtCore.QAbstractAnimation.Forward if not checked else QtCore.QAbstractAnimation.Backward)
        self.toggle_animation.start()

    def setContentLayout(self, layout, duration=0):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(duration)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(duration)

        content_animation.setStartValue(0)
        # if self.collapsed:
        #     content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

    # contents = DockContents()
    # contents.setSizeHint(400, 100)
    
    # layout = QtWidgets.QVBoxLayout(collapse_box)
    # layout.setContentsMargins(0, 0, 0, 0)

    

    # for idx, widget in enumerate(widget_list):
    #     layout.addWidget(widget,1)
        
    # dock.setWidget(contents)
    

    # return dock














def button_row(names_funcs=[["testBox1", test_func], ["textBox2", test_func]], color=elements.blue, bg_color=elements.grey):
    grid_layout=QtWidgets.QGridLayout()
    buttons = []
    layout = QtWidgets.QWidget()
    layout.setLayout(grid_layout)
    for idx, checkbox in enumerate(names_funcs):
        button = create_button(text=checkbox[0], color=color, bg_color=bg_color)
        grid_layout.addWidget(button, 0, idx)
        button.clicked.connect(checkbox[1])
        buttons.append(button)
    return layout, buttons 

def radio_button_row(checkbox_names_defaults=[["testBox1", "tooltip1"], ["textBox2", "tooltip2"]], default_true_idx=0):
    grid_layout=QtWidgets.QGridLayout()
    buttons = []
    layout = QtWidgets.QWidget()
    layout.setLayout(grid_layout)
    for idx, checkbox in enumerate(checkbox_names_defaults):
        button = QtWidgets.QRadioButton(checkbox[0])
        grid_layout.addWidget(button, 0, idx)
        if idx == default_true_idx:
            button.setChecked(True)
        if len(checkbox) > 1 and checkbox[1]:
            button.setToolTip(checkbox[1])
        buttons.append(button)
    return layout, buttons 

def check_box_list(checkbox_names_defaults=[["testBox1", True], ["textBox2", False]], row=True, color=elements.blue):
    ### names defaults [(name1, True), (name2, False)]
    grid_layout=QtWidgets.QGridLayout()
    checkboxes = []
    layout = QtWidgets.QWidget()
    layout.setLayout(grid_layout)
    # layout.setGeometry(100,100,200,100)
    for idx, checkbox in enumerate(checkbox_names_defaults):
        row_or_column = [0, idx]
        if not row:
            row_or_column = [idx, 0]
        temp_checkbox = QtWidgets.QCheckBox(checkbox[0])
        temp_checkbox.setStyleSheet(color)
        temp_checkbox.setChecked(checkbox[1])
        grid_layout.addWidget(temp_checkbox, row_or_column[0], row_or_column[1])
        checkboxes.append(temp_checkbox)
    
    return layout, checkboxes 

def test(string_name):
    print(string_name)

class checkbox_list_with_limits(QtWidgets.QWidget):
    def __init__(self,
                 checkbox_names_defaults=[["testBox1", True, ""],
                 ["textBox2", False, "tooltip"]],
                 row=True,
                 limit_checkbox_default_index=0
                 ):
        self.limit_checkbox_default_index=limit_checkbox_default_index
        grid_layout=QtWidgets.QGridLayout()
        self.checkboxes = []
        self.layout = QtWidgets.QWidget()
        self.layout.setLayout(grid_layout)
        for idx, checkbox in enumerate(checkbox_names_defaults):
            row_or_column = [0, idx]
            if not row:
                row_or_column = [idx, 0]
            temp_checkbox = QtWidgets.QCheckBox(checkbox[0])
            temp_checkbox.setChecked(checkbox[1])
            if len(checkbox) > 2 and checkbox[2]:
                print("setting tooltip")
                temp_checkbox.setToolTip(checkbox[2])
            grid_layout.addWidget(temp_checkbox, row_or_column[0], row_or_column[1])
            self.checkboxes.append(temp_checkbox)
        self.limit()

    def limit(self):
        for idx in range(len(self.checkboxes)):
            self.checkboxes[idx].clicked.connect(lambda idx_arg=idx: self.check_box_list_limit(idx_arg))
        self.check_box_list_limit(self.limit_checkbox_default_index)

    def check_box_list_limit(self, idx):
        current_checkbox=self.checkboxes[idx]
        for checkbox in self.checkboxes:
            if current_checkbox == checkbox.text():
                continue
            if not checkbox.checkState():
                continue
            checkbox.setChecked(False)
            current_checkbox.setChecked(True)

def check_box_list_limit(current_checkbox, check_box_list):
    print(current_checkbox.text())
    for checkbox in check_box_list:
        if current_checkbox.text() == checkbox.text():
            # print "SAME!!!", checkbox.text(), current_checkbox.text()
            continue
        if not checkbox.checkState():
            continue
        checkbox.setChecked(False)
    # current_checkbox.setChecked(True)

def separator():
    separator_line = QtWidgets.QFrame()
    separator_line.setFrameShape(QtWidgets.QFrame.HLine)
    return separator_line

def file_dialog(default_filename):
    grid_layout=QtWidgets.QGridLayout()
    checkboxes = []
    layout = QtWidgets.QWidget()
    layout.setLayout(grid_layout)

    return layout


class Text_Box(QtWidgets.QWidget):
    def __init__(self,
                 parent = None,
                 default_text="baseAsset",
                 text_changed_func=None
                 ):
        self.default_text = default_text
        self.text_changed_func = text_changed_func
        super(Text_Box, self).__init__(parent)
        layout = QtWidgets.QGridLayout()

        self.contents = QtWidgets.QLineEdit()
        self.contents.setText(self.default_text)
        layout.addWidget(self.contents,0,0)
        self.setLayout(layout)
        self.contents.textChanged.connect(text_changed_func)


def get_outliner_icon(maya_object):
    if not maya_object:
        maya_object = cmds.ls(sl=True)[0]
    maya_object_type = cmds.objectType(maya_object)
    # If the object is a transform and has a shape, set the type to that of the shape
    if maya_object_type == "transform" and cmds.listRelatives(s=True):
        maya_object_type = cmds.objectType(cmds.listRelatives(s=True)[0])
    file_dir = ":/{0}.svg".format(maya_object_type)

    testfile = QtCore.QFile(file_dir)
    if not testfile.exists():
        file_dir = ":/default.svg"
    return QtGui.QIcon(file_dir)
