from PySide2 import QtWidgets, QtCore
from uiCore import qtUtils
from . import helpBoxWidget


class CollapseBox(QtWidgets.QWidget):

    def __init__(self, indentSize = 0, helpTextMessage = None, includeHelp = True,
                 collapsable = True):
        super(CollapseBox, self).__init__()

        # edit this variable to manage whether or not to include
        # an helpbox associated to this widget (the question mark
        # in the collapse bar)
        self.includeHelp = includeHelp
        # this is the text to be shown in the helpbox associated
        # to this widget
        self.helpTextMessage = helpTextMessage
        # this will determine if the widget is collapsable or not
        # changing how the label on the header is formatted
        # and the click behavior on it
        self.collapsable = collapsable

        self.collapseChar = chr(11166)
        self.expandChar = chr(11167)

        # color management for the standard elements of the collapseBox
        self.textColor = {"base": (180, 180, 180),
                          "hover": (180, 180, 180),
                          "pressed": (250, 250, 250)}
        self.borderColor = {"base": (120, 120, 120),
                            "hover": (120, 120, 120),
                            "pressed": (30, 30, 30)}
        self.backgroundColor = {"base": (90, 90, 90),
                                "hover": (120, 120, 120),
                                "pressed": (60, 60, 60)}
        self.boxColor = {"text": (90, 90, 90),
                         "border": (90, 90, 90),
                         "back": (90, 90, 90)}


        self.collapseBoxName="collapseBox"

        self.headerStyleSheet = """QPushButton {{
                                    height: 20px;
                                    color: rgb({textR}, {textG}, {textB});
                                    border-style: inset;
                                    border-width: 0px;
                                    border-color: rgb({borderR}, {borderG}, {borderB});
                                    background-color: rgb({backR}, {backG}, {backB}); 
                                    text-align: left;
                                    font-weight: bold;
                                    padding-left: 5px;}}
                                    
                                    QPushButton:hover {{
                                    color: rgb({hTextR}, {hTextG}, {hTextB});
                                    border-style: flat;
                                    border-color: rgb({hBorderR}, {hBorderG}, {hBorderB});
                                    background-color: rgb({hBackR}, {hBackG}, {hBackB}); }}
                        
                                    QPushButton:pressed {{
                                    border-style: inset;
                                    color: rgb({pTextR}, {pTextG}, {pTextB});
                                    border-color: rgb({pBorderR}, {pBorderG}, {pBorderB});
                                    background-color: rgb({pBackR}, {pBackG}, {pBackB});}}"""

        self.boxStyleSheet = """QGroupBox {{
                                color: rgb({textR}, {textG}, {textB});
                                border-style: inset;
                                border-width: 0px;
                                border-radius: 0px;
                                border-color: rgb({borderR}, {borderG}, {borderB});
                                background-color: rgb({backR}, {backG}, {backB});
                                }}""" #

        #setting main layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignmentFlag().AlignTop)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(indentSize,0,0,0)
        self.setLayout(self.mainLayout)

        #create the header of the collapse box
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.header = QtWidgets.QPushButton()
        self.header.setText(self.collapseBoxName)
        self.header.released.connect(self.collapseGBox)

        self.helpButton = QtWidgets.QPushButton()
        self.helpButton.setText("? ")
        self.helpButton.released.connect(self.popUpHelpBox)
        self.helpButton.setHidden(True)
        self.helpButton.helpOut = False

        self.headerLayout.addWidget(self.header, 1)
        self.headerLayout.addWidget(self.helpButton, 0)

        self.createGbox()
        self.gBox.setHidden(True)
        if not self.collapsable:
            self.gBox.setHidden(False)
        self.vBox.setContentsMargins(2,2,2,2)
        self.vBox.setSpacing(2)

        self.mainLayout.addLayout(self.headerLayout)
        self.mainLayout.addWidget(self.gBox)

        self.updateColor()

    def collapseGBox(self):
        if self.collapsable:
            if self.gBox.isHidden():
                self.gBox.setHidden(False)
                if not self.helpButton.helpOut:
                    self.helpButton.setHidden(not self.includeHelp)
                label = self.sender().text().replace(self.collapseChar, self.expandChar)
                self.header.setText(label)
            else:
                self.gBox.setHidden(True)
                self.helpButton.setHidden(True)
                label = self.sender().text().replace(self.expandChar, self.collapseChar)
                self.header.setText(label)
        else:
            return

    def popUpHelpBox(self):

        if self.helpTextMessage == None:
            self.helpTextMessage = """
Empty Doc for
this Section
                """
        helpBox = helpBoxWidget.HelpBox(parent=self.parent(), textContent=self.helpTextMessage,
                                        fillColor=self.boxColor["back"],
                                        textColor=self.textColor["base"],
                                        collapseWidget=self)
        from . import uiStack # import within the procedure to avoid cross-import issues
        stackParent = uiStack.findParentUiStack(srcWidget = self)
        stackParentGlobalLayout = None
        if not stackParent:
            stackParentGlobalLayout = self.mainLayout
        else:
            stackParentGlobalLayout = stackParent.globalLayout
        stackParentGlobalLayout.addWidget(helpBox)
        self.helpButton.setHidden(True)
        self.helpButton.helpOut = True

    def updateColor(self):
        setSheetHead = self.headerStyleSheet.format
        setSheetBox = self.boxStyleSheet.format
        textB = self.textColor["base"]
        textH = self.textColor["hover"]
        textP = self.textColor["pressed"]
        borderB = self.borderColor["base"]
        borderH = self.borderColor["hover"]
        borderP = self.borderColor["pressed"]
        backB = self.backgroundColor["base"]
        backH = self.backgroundColor["hover"]
        backP = self.backgroundColor["pressed"]
        boxText = self.boxColor["text"]
        boxBorder = self.boxColor["border"]
        boxBack = self.boxColor["back"]
        for btn in (self.header, self.helpButton):
            btn.setStyleSheet(setSheetHead(textR=textB[0], textG=textB[1], textB=textB[2],
                                                   hTextR=textH[0], hTextG=textH[1], hTextB=textH[2],
                                                   pTextR=textP[0], pTextG=textP[1], pTextB=textP[2],
                                                   borderR=borderB[0], borderG=borderB[1], borderB=borderB[2],
                                                   hBorderR=borderH[0], hBorderG=borderH[1], hBorderB=borderH[2],
                                                   pBorderR=borderP[0], pBorderG=borderP[1], pBorderB=borderP[2],
                                                   backR=backB[0], backG=backB[1], backB=backB[2],
                                                   hBackR=backH[0], hBackG=backH[1], hBackB=backH[2],
                                                   pBackR=backP[0], pBackG=backP[1], pBackB=backP[2]))

        self.gBox.setStyleSheet(setSheetBox(textR=boxText[0], textG=boxText[1], textB=boxText[2],
                                            borderR=boxBorder[0], borderG=boxBorder[1], borderB=boxBorder[2],
                                            backR=boxBack[0], backG=boxBack[1], backB=boxBack[2]))

    def setColor(self, r,g,b):
        self.textColor = {"base": (220, 220, 220),
                          "hover": (220, 220, 220),
                          "pressed": (255, 255, 255)}
        self.borderColor = {"base": (r*1.2, g*1.2, b*1.2),
                            "hover": (r*1.4, g*1.4, b*1.4),
                            "pressed": (r*0.8, g*0.8, b*0.8)}
        self.backgroundColor = {"base": (r, g, b),
                                "hover": (r*1.2, g*1.2, b*1.2),
                                "pressed": (r*0.4, g*0.4, b*0.4)}
        self.boxColor = {"text": (220, 220, 220),
                         "border": (r*1.2, g*1.2, b*1.2),
                         "back": (r, g, b)}
        self.updateColor()

    def setColorExplicit(self, textColor=None, borderColor=None, backgroundColor=None, boxColor=None):

        if textColor != None:
            self.textColor = textColor.copy()
        if borderColor != None:
            self.borderColor = borderColor.copy()
        if backgroundColor != None:
            self.backgroundColor = backgroundColor.copy()
        if boxColor!=None:
            self.boxColor = boxColor.copy()

        self.updateColor()

    def setHeaderColor(self, r,g,b, hoverGain=1.3, pressed=None):
        if pressed == None:
            pressed = (200,200,200)
        rgb = qtUtils.clampRGB([r,g,b])
        rgbG = qtUtils.clampRGB([rgb[0]*hoverGain,rgb[1]*hoverGain,rgb[2]*hoverGain])
        presd = qtUtils.clampRGB([pressed[0],pressed[1],pressed[2]])
        headerClr = {"base": (rgb[0], rgb[1], rgb[2]),
                 "hover": (rgbG[0], rgbG[1], rgbG[2]),
                 "pressed": (presd[0], presd[1], presd[2])}
        self.setColorExplicit(backgroundColor = headerClr)

    def setBodyColor(self, r,g,b, borderGain=1.3, text=None):
        if text == None:
            text = (200,200,200)
        rgb = qtUtils.clampRGB([r,g,b])
        rgbG = qtUtils.clampRGB([rgb[0]*borderGain,rgb[1]*borderGain,rgb[2]*borderGain])
        txt = qtUtils.clampRGB([text[0],text[1],text[2]])
        boxClr = {"text": (txt[0], txt[1], txt[2]),
                 "border": (rgbG[0], rgbG[1], rgbG[2]),
                 "back": (rgb[0], rgb[1], rgb[2])}
        self.setColorExplicit(boxColor = boxClr)

    def setLabel(self, label):
        if self.collapsable:
            self.header.setText("{}   {}".format(self.collapseChar, label))
        else:
            self.header.setText("{}".format(label))

    def setCollapsable(self, collapsable=True):
        if not collapsable:
            self.gBox.setHidden(False)
            self.collapsable = False

    def createGbox(self):
        self.gBox = QtWidgets.QGroupBox()
        self.gBox.setObjectName(self.collapseBoxName)
        self.gBox.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gBox.setStyleSheet(self.boxStyleSheet)

        # Creating the vertical layout    
        self.vBox = QtWidgets.QVBoxLayout()
        self.vBox.setAlignment(QtCore.Qt.AlignmentFlag().AlignTop)

        self.gBox.setLayout(self.vBox)
        self.mainLayout.addWidget(self.gBox)