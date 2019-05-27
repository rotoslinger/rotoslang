import sys, os
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds
from ui_2 import elements
reload(elements)
OPERATING_SYSTEM = sys.platform

def test_func():
    print "Test func is working"

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

def create_label(text="test", color="color: rgb(255, 102, 255);", center=False):
    label = QtWidgets.QLabel(text)
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setStyleSheet(color)
    if center:
        label.setAlignment(QtCore.Qt.AlignCenter)
    return label

def create_heading(text="test", color="color: rgb(255, 102, 255);"):
    label = create_label(text=text, color=color, center=True)
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold)) 
    return label


def create_button(text="test", color=elements.light_grey, bg_color= elements.grey):
    button = QtWidgets.QPushButton(text)
    if bg_color:
        bg_color = "background-" + bg_color
        color = "QPushButton {" + "{0}{1}".format(color, bg_color) + "}"
    button.setStyleSheet(color)
    return button

def label_button(label_text="Test label",
                 button_text="Test button",
                 color="color: rgb(255, 102, 255);",
                 button_func=test_func,
                 bg_color=elements.grey,
                 ):
    label = create_label(text=label_text, color=color)
    button = create_button(text=button_text, color=color, bg_color=bg_color)
    button.clicked.connect(button_func)
    return label, button

def text_box(default_text="baseAsset", text_changed_func=test_func):
    text_field = QtWidgets.QLineEdit()
    text_field.setText(default_text)
    text_field.textChanged.connect(text_changed_func)
    return text_field

def get_QColor_from_style(style_color):
    "color: rgb(90, 90, 90);"
    style_color = style_color.split("(")[1].split(")")[0].split(",")
    # style_color = tuple(style_color)
    style_color = [int(x) for x in style_color]
    return QtGui.QColor(*style_color)

def create_collapsable_dock(text, widget_list, color=elements.blue, bg_color = elements.base_grey):
    # if bg_color:
    #     bg_color = "background-" + bg_color
    #     color = "QDockWidget {" + "{0}{1}".format(color, bg_color) + "}"
    dock = QtWidgets.QDockWidget(text)
    dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
    dock.setAutoFillBackground(True)
    dock.setStyleSheet(color)
    # dock.setObjectName("myParentWidget");
    dock.setFont(QtGui.QFont("Helvetica", 8, QtGui.QFont.DemiBold))
    
    collapse_box = CollapsibleBox()
    collapse_box.content_area.setBackgroundRole(QtGui.QPalette.Background)

    p = collapse_box.content_area.palette()
    bg_color = get_QColor_from_style(bg_color)
    p.setColor(collapse_box.content_area.backgroundRole(), bg_color)
    collapse_box.content_area.setPalette(p)

    # collapse_box.content_area.setStyleSheet(elements.black)

    # collapse_box.setAutoFillBackground(True)
    # collapse_box.setStyleSheet(color)
    # collapse_box.setBackgroundRole(QtGui.QPalette.Window)
    # p = collapse_box.palette()
    # p.setColor(collapse_box.backgroundRole(), QtGui.QColor(0, 0, 0))
    # collapse_box.setPalette(p)

    collapse_box.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
    collapse_box.setLineWidth(2)
    layout = QtWidgets.QVBoxLayout()
    # dock.setStyleSheet(sheet)
    for idx, widget in enumerate(widget_list):
        # widget.setObjectName("myParentWidget" + str(idx))
        # sheet = "QWidget#{0}".format("myParentWidget" + str(idx)) + "{ background-color: #1d1d1d ; color: #f8f8f8}"
        # widget.setStyleSheet(sheet)
        layout.addWidget(widget)
    dock.setWidget(collapse_box)
    collapse_box.setContentLayout(layout)

    return dock

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
    print string_name

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
                print "setting tooltip"
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
    print current_checkbox.text()
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
        self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
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