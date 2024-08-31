
import sys, os, inspect, importlib
from functools import partial

from PySide6 import QtWidgets, QtCore, QtGui

from . import collapseBoxWidget
from uiCore import qtUtils


class UiStack(QtWidgets.QWidget):
    '''
    @code
    from uiCore.uiStack import uiStack
    uiStack.UiStack.openUI()
    @endcode
    '''

    def __init__(self, winTitle="UI Stack", parent=None):
        if parent==None:
            parent=qtUtils.getMayaWindow()
        super(UiStack, self).__init__(parent)

        self.winName = winTitle.replace(" ", "")

        self.winTitle = winTitle
        self.dragging_threshould = 15.0
        self.isDragging = False
        self.mousePosStart = None
        self.mouseMovePos = None

        self.setWindowFlags(QtCore.Qt.SplashScreen)

        self.globalLayout = QtWidgets.QHBoxLayout(self)
        self.globalLayout.setContentsMargins(0, 0, 0, 0)
        self.globalLayout.setSpacing(0)
        self.globalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.globalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.headerLayout = self.initHeader()
        self.mainLayout.addLayout(self.headerLayout)
        self.setColor()

        self.globalLayout.addLayout(self.mainLayout, QtCore.Qt.AlignTop)

    def initHeader(self):
        headerLayout = QtWidgets.QHBoxLayout()
        headerLayout.setContentsMargins(0, 0, 0, 10)
        headerLayout.setSpacing(0)

        # labelTab serves only to balance the spacing in the header bar, and have the title
        # in the center
        labelTab = QtWidgets.QLabel("")
        labelTab.setMinimumWidth(12)
        headerLayout.addWidget(labelTab, 0, QtCore.Qt.AlignLeft)

        titleFont = QtGui.QFont('Arial', 10)
        titleFont.setBold(True)
        labelTitle = QtWidgets.QLabel("{}".format(self.winTitle))
        labelTitle.setFont(titleFont)
        headerLayout.addWidget(labelTitle, 1,
                               QtCore.Qt.AlignCenter)  # "1" makes it stretchy: you can actually
                                                       # "compete" with other controls in the same
                                                       # layout rising this number to manage the
                                                       # weight

        self.btnX = QtWidgets.QPushButton("")
        self.btnX.released.connect(self.killThis)
        self.btnX.setMaximumWidth(12)
        self.btnX.setMaximumHeight(12)

        initColor = qtUtils.getQtColor("white")
        _r = initColor.red()
        _g = initColor.green()
        _b = initColor.blue()
        self.btnX.setStyleSheet("background-color: rgb({}, {}, {});".format(_r, _g, _b))
        headerLayout.addWidget(self.btnX, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        return headerLayout

    def setColor(self, fillColor = None, textColor = None, btnXColor = None):
        # setting default color where not specified
        if fillColor == None:
            fillColor = (100, 100, 100)
        if textColor == None:
            textColor = (250, 250, 250)
        # by default the btnX Color is going to be a lighter shade of the fillColor
        if btnXColor == None:
            baseColor = qtUtils.getQtColor(fillColor)
            _r = max(0, min( baseColor.red()+70, 255))
            _g = max(0, min(baseColor.green() + 70, 255))
            _b = max(0, min(baseColor.blue() + 70, 255))
            btnXColor = qtUtils.getQtColor((_r, _g, _b))

        # setting the palette for the window colors
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, qtUtils.getQtColor(fillColor))
        pal.setColor(QtGui.QPalette.WindowText, qtUtils.getQtColor(textColor))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        # setting the background color for the btnX
        initColor = qtUtils.getQtColor(btnXColor)
        _r = initColor.red()
        _g = initColor.green()
        _b = initColor.blue()
        self.btnX.setStyleSheet("background-color: rgb({}, {}, {});".format(_r, _g, _b))

    def addWidgetsToStack(self, parentWidget = None, indentStep = 10, indent = 0):
        # passing the parentWidget explicitly, should happen only when you are looking for subSections:
        # the default value 'None', will point to 'self', and this should always bee the UiStack instance, rather
        # then a CollapsibleBox
        if parentWidget == None:
            parentWidget = self

        # If the parentWidget is a UI stack, we are looking at parenting the new widgets within its 'mainLayout'.
        # if the parentWidget is a CollapseBox instead, the subSection must go under the 'vBox' layout
        parentLayut = None
        if isinstance(parentWidget, UiStack):
            parentLayut = parentWidget.mainLayout
        else:
            parentLayut = parentWidget.vBox

        # Informations needed to build the full path to the new modules to import. Within this modules, we will go
        # looking for classes inheriting the CollapseBox class. Any of those that is found is going to be added
        # to the parentLayout
        thisModule = parentWidget.__module__
        parentModuleName = ".".join(thisModule.split(".")[:-1])
        # Folders is a recursive dictionary of the folder structure rooted in the parentModule folder
        folders = qtUtils.getSubFoldersFromClass(parentWidget)
        for k,v in list(folders.items()):
            pyFiles = qtUtils.listPyFiles(k)
            newWidget = None
            for f in pyFiles:
                # Building the full path to the module found in the folder structure of the parent module.
                # With that, we will be able to import and inspect to find CollapseBox classes
                newModuleName = "{}.{}.{}".format(parentModuleName,
                                              os.path.basename(k),
                                              os.path.splitext(f)[0])
                newModule = importlib.import_module(newModuleName)
                # reloading module to ensure that's up to date
                importlib.reload(newModule)
                # retrive a list of classes of type CollapseBox
                newWdgtLst = qtUtils.listSubClassesOf(newModule, collapseBoxWidget.CollapseBox)
                # if no CollapseBoxs are found, continue to the next py file
                if not newWdgtLst:
                    continue
                # we only handle ONE CollapseBox per module
                NewWdgt = newWdgtLst[0]
                newWidget = NewWdgt(indent)
                # Adding the new widget to the parentLayout
                parentLayut.addWidget(newWidget)

            # 'v' is the value of the present dictionary key, which contains the subFolder of the widget module
            # just added to the layout. Where this is not empty, we might find some subSection to parent to the
            # new CollapseBox: so increment the indent of the section, and go look for some
            if v:
                self.addWidgetsToStack(newWidget, indentStep, indentStep)

            if not pyFiles:
                print(k)

        # for aDirName in qtUtils.listSubdir(baseDir):
        #     srcDir = os.path.join(baseDir, aDirName)
        #     for aModuleName in [o[:-3] for o in listPyFiles(srcDir)]:
        #         modulePath = "{}.{}.{}".format(parentModuleName, aDirName, aModuleName)
        #         print "importing: {}".format(modulePath)
        #         thisModule = importlib.import_module(modulePath)
        #         reload(thisModule)
        #         classesInModule = listSubClassesOf(thisModule, ParentClass)
        #         for o in classesInModule:
        #             print o

    def killThis(self):
        try:
            del globals()[self.winName]
        except:
            pass
        self.close()
        self.deleteLater()

    def mousePressEvent(self, thisEvent):
        if thisEvent.button() == QtCore.Qt.LeftButton:
            self.isDragging = True
            self.mousePosStart = thisEvent.globalPos()
            self.mouseMovePos = thisEvent.globalPos() - self.pos()
        super(UiStack, self).mousePressEvent(thisEvent)

    def mouseMoveEvent(self, thisEvent):
        if thisEvent.button() == QtCore.Qt.NoButton and self.isDragging == True:
            globalPos = thisEvent.globalPos()
            moved = globalPos - self.mousePosStart
            if moved.manhattanLength() > self.dragging_threshould:
                diff = globalPos - self.mouseMovePos
                self.move(diff)
        super(UiStack, self).mouseMoveEvent(thisEvent)

    def mouseReleaseEvent(self, thisEvent):
        if thisEvent.button() == QtCore.Qt.LeftButton:
            self.isDragging = False
        super(UiStack, self).mouseReleaseEvent(thisEvent)

    def openUI(self):
        try:
            try:
                globals()[self.winName].close()
                globals()[self.winName].deleteLater()
            except:
                pass
            del globals()[self.winName]
        except:
            pass

        globals()[self.winName] = self

        globals()[self.winName].show()
        return globals()[self.winName]


def findParentUiStack(srcWidget = None):
    return qtUtils.findParentWidgetByType(srcWidget, UiStack)