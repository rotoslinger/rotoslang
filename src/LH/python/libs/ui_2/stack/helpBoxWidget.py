from PySide2 import QtCore, QtWidgets, QtGui
from uiCore import qtUtils


class HelpBox(QtWidgets.QWidget):
    """VBox Layout widget with kill button and some color management"""

    def __init__(self, parent=None, textContent = None, fillColor = None, textColor = "white", btnXFillColor = None,
                 btnXTextColor = None, btnXCharacter = "", collapseWidget = None):
        """
        :param parent: parent widget
        :param textContent: string to be displayed in the text box
        :param fillColor: base fill color for the box. Default = [120, 60, 60]
        :param textColor: text color for the box content. Default = "white"
        :param btnXFillColor: fill color for the X button. Default is brighter than fillColor
        :param btnXTextColor: text color for the X button. Default is brighter than textColor
        :param btnXCharacter: character to use for the X button. Default ""
        :param collapseWidget: the collapseWidget of the helpbox. When you show hide the helpbox
                               you want to properly manage the visibility of the helpBox button
                               in this widget, and you need to be able to reach the button and
                               check if the section is collapsed or not
        """
        super(HelpBox, self).__init__(parent)

        if textContent == None:
            textContent = """Type text on multilines here.
You can override the addContent() procedure
if you want to customize the display
message."""
        self.textContent = textContent                # string to be displayed in the text box
        self.fillColor = fillColor                    # base fill color for the box
        self.textColor = textColor                    # text color for the box content
        self.btnXFillColor = btnXFillColor            # fill color for the X button
        self.btnXTextColor = btnXTextColor            # text color for the X button
        self.btnXCharacter = btnXCharacter            # character to use for the X button
        self.collapseWidget = collapseWidget          # Collapsible group box of the helpBox
        self.drawIt()

    def drawIt(self):
        """Update the helpBox widget display
        
        If you want to change the aspect of the helpbox after having initialized it, change the value of the 
        instance variables you find in the __init__, and run drawIt() again
        """
        pal = QtGui.QPalette()
        if self.fillColor == None:
            self.fillColor = [120, 60, 60]
        pal.setColor(QtGui.QPalette.Background, qtUtils.getQtColor(self.fillColor))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        self.btnX = QtWidgets.QPushButton(self.btnXCharacter)  # QtWidgets.QFrame()
        self.btnX.setMaximumWidth(12)
        self.btnX.setMaximumHeight(12)
        self.btnX.released.connect(self.killThis)
        self.setBtnXColor()
        self.mainLayout.addWidget(self.btnX, 0, QtCore.Qt.AlignRight)

        self.addContent()

    def addContent(self):
        helpBox = QtWidgets.QFrame()
        helpBox.setMinimumWidth(200)
        helpBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addWidget(helpBox)

        self.contentLayout = QtWidgets.QVBoxLayout(helpBox)
        self.contentLayout.setContentsMargins(10, 5, 10, 5)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setAlignment(QtCore.Qt.AlignTop)
        self.contentLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        for thisLine in self.textContent.split("\n"):
            if thisLine == "":
                continue
            thisLabel = QtWidgets.QLabel(thisLine)
            textClr = qtUtils.getQtColor(self.textColor)
            thisStyle = "color:rgb({},{},{});".format(textClr.red(), textClr.green(), textClr.blue())
            thisLabel.setStyleSheet(thisStyle)
            self.contentLayout.addWidget(thisLabel)

        self.mainLayout.addLayout(self.mainLayout, QtCore.Qt.AlignTop)

    def setBtnXColor(self):
        if self.btnXFillColor == None:
            fillColor = qtUtils.getQtColor(self.fillColor)
            red = max(min(fillColor.red() + 30, 255), 0)
            green = max(min(fillColor.green() + 30, 255), 0)
            blue = max(min(fillColor.blue() + 30, 255), 0)
            self.btnXFillColor = QtGui.QColor(red, green, blue)

        if self.btnXTextColor == None:
            textColor = qtUtils.getQtColor(self.textColor)
            red = max(min(textColor.red() + 30, 255), 0)
            green = max(min(textColor.green() + 30, 255), 0)
            blue = max(min(textColor.blue() + 30, 255), 0)
            self.btnXTextColor = QtGui.QColor(red, green, blue)

        btnXcolor = qtUtils.getQtColor(self.btnXFillColor)
        btnXTextColor = qtUtils.getQtColor(self.btnXTextColor)
        btnStyle = """background-color:rgb({},{},{}); color:rgb({},{},{});"""
        self.btnX.setStyleSheet(btnStyle.format(btnXcolor.red(), btnXcolor.green(), btnXcolor.blue(),
                                                btnXTextColor.red(), btnXTextColor.green(), btnXTextColor.blue()))

    def killThis(self):
        if self.collapseWidget:
            if not self.collapseWidget.gBox.isHidden():
                self.collapseWidget.helpButton.setHidden(False)
        self.collapseWidget.helpButton.helpOut = False
        self.close()
        self.deleteLater()


