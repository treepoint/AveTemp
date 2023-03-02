# Form implementation generated from reading ui file './windows/main.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import support
import localization
import Entities

languages = Entities.Languages()
trans = localization.trans

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, locale):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(412, 346)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(412, 324))
        MainWindow.setMaximumSize(QtCore.QSize(600, 600))
        MainWindow.setWindowTitle("")
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet("QApplication:title {\n"
"    background: #eee;\n"
"}\n"
"\n"
"QWidget {\n"
"    background: #fff;\n"
"}")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(12)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.frame_2.setStyleSheet("background: #eee; border-right: 1px solid #d8d8d8; border-top: 1px solid #d8d8d8;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_12.setContentsMargins(4, 12, 6, 16)
        self.verticalLayout_12.setSpacing(8)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_12.addItem(spacerItem)
        self.buttonShowSettings = QtWidgets.QPushButton(self.frame_2)
        self.buttonShowSettings.setEnabled(True)
        self.buttonShowSettings.setMinimumSize(QtCore.QSize(20, 20))
        self.buttonShowSettings.setMaximumSize(QtCore.QSize(20, 20))
        self.buttonShowSettings.setStyleSheet("QPushButton {\n"
"    border:solid 0px;\n"
"    qproperty-icon: url(\" \"); /* empty image */\n"
"    qproperty-iconSize: 20px 20px; /* space for the background image */\n"
"    border-image : url("+ support.getResourcePath('./images/settings.svg')+ ");\n"
"    background-repeat: no-repeat;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-image : url("+ support.getResourcePath('./images/settings_hover.svg')+ ");\n"
"    background-repeat: no-repeat;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    border-image : url("+ support.getResourcePath('./images/settings_pressed.svg')+ ");\n"
"    background-repeat: no-repeat;\n"
"}")
        self.buttonShowSettings.setText("")
        self.buttonShowSettings.setDefault(False)
        self.buttonShowSettings.setFlat(False)
        self.buttonShowSettings.setObjectName("buttonShowSettings")
        self.verticalLayout_12.addWidget(self.buttonShowSettings)
        self.verticalLayout_6.addWidget(self.frame_2)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 6, 12, 12)
        self.verticalLayout_3.setSpacing(16)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(16)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setSpacing(8)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.cpuNameLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cpuNameLabel.setFont(font)
        self.cpuNameLabel.setStyleSheet("font-weight: bold; font-size:12px;")
        self.cpuNameLabel.setText("")
        self.cpuNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.cpuNameLabel.setObjectName("cpuNameLabel")
        self.verticalLayout_11.addWidget(self.cpuNameLabel)
        self.CPUinfoTable = QtWidgets.QTableWidget(self.centralwidget)
        self.CPUinfoTable.setMinimumSize(QtCore.QSize(0, 0))
        self.CPUinfoTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.CPUinfoTable.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.CPUinfoTable.setFont(font)
        self.CPUinfoTable.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.CPUinfoTable.setStyleSheet("QWidget {\n"
"    border: none;\n"
"    font-family: \"MS Shell Dlg 2\";\n"
"    font-size: 8pt;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #eee;\n"
"    border-style: none;\n"
"    border: 1px solid #d8d8d8;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QHeaderView::section::vertical {\n"
"   border: 1px solid #d8d8d8;\n"
"   font-weight: bold; \n"
"   color: #222; \n"
"   font-size:12px;\n"
"   border-top: none;\n"
"   text-align: right;\n"
"}\n"
"\n"
"\n"
"\n"
"QHeaderView::section::horizontal {\n"
"   border: 1px solid #d8d8d8;\n"
"   border-left: none;\n"
"   color: #222; \n"
"   font-size:12px;\n"
"}\n"
"\n"
"QHeaderView::section::horizontal::first {\n"
"   border-left: 1px solid #d8d8d8;\n"
"}\n"
"\n"
"QTableView\n"
"{\n"
"    border-top: 1px solid #d8d8d8;\n"
"}\n"
"")
        self.CPUinfoTable.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.CPUinfoTable.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.CPUinfoTable.setLineWidth(0)
        self.CPUinfoTable.setMidLineWidth(0)
        self.CPUinfoTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.CPUinfoTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.CPUinfoTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.CPUinfoTable.setAutoScroll(False)
        self.CPUinfoTable.setAlternatingRowColors(False)
        self.CPUinfoTable.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.CPUinfoTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerItem)
        self.CPUinfoTable.setShowGrid(True)
        self.CPUinfoTable.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.CPUinfoTable.setCornerButtonEnabled(True)
        self.CPUinfoTable.setRowCount(0)
        self.CPUinfoTable.setObjectName("CPUinfoTable")
        self.CPUinfoTable.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.CPUinfoTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.CPUinfoTable.setHorizontalHeaderItem(1, item)
        self.CPUinfoTable.horizontalHeader().setVisible(False)
        self.CPUinfoTable.horizontalHeader().setCascadingSectionResizes(True)
        self.CPUinfoTable.horizontalHeader().setDefaultSectionSize(58)
        self.CPUinfoTable.horizontalHeader().setMinimumSectionSize(42)
        self.CPUinfoTable.horizontalHeader().setStretchLastSection(True)
        self.CPUinfoTable.verticalHeader().setVisible(True)
        self.CPUinfoTable.verticalHeader().setCascadingSectionResizes(False)
        self.CPUinfoTable.verticalHeader().setDefaultSectionSize(24)
        self.CPUinfoTable.verticalHeader().setMinimumSectionSize(24)
        self.CPUinfoTable.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_11.addWidget(self.CPUinfoTable)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_11.addItem(spacerItem1)
        self.horizontalLayout_6.addLayout(self.verticalLayout_11)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(8)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("font-weight: bold; color: #222; font-size:12px;")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.tableAverage = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.tableAverage.setFont(font)
        self.tableAverage.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.tableAverage.setAutoFillBackground(False)
        self.tableAverage.setStyleSheet("QWidget {\n"
"    border: none;\n"
"    font-family: \"MS Shell Dlg 2\";\n"
"    font-size: 8pt;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #eee;\n"
"    border-style: none;\n"
"    border: 1px solid #d8d8d8;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QHeaderView::section::vertical {\n"
"   border: 1px solid #d8d8d8;\n"
"   font-weight: bold; \n"
"   color: #222; \n"
"   font-size:12px;\n"
"   border-top: none;\n"
"   text-align: right;\n"
"}\n"
"\n"
"QHeaderView::section::horizontal {\n"
"   border: 1px solid #d8d8d8;\n"
"   border-left: none;\n"
"   color: #222; \n"
"   font-size:12px;\n"
"}\n"
"\n"
"QHeaderView::section::horizontal::first {\n"
"   border-left: 1px solid #d8d8d8;\n"
"}\n"
"\n"
"QTableView\n"
"{\n"
"    border-top: 1px solid #d8d8d8;\n"
"}\n"
"")
        self.tableAverage.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.tableAverage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableAverage.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableAverage.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableAverage.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.tableAverage.setShowGrid(True)
        self.tableAverage.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.tableAverage.setWordWrap(True)
        self.tableAverage.setCornerButtonEnabled(True)
        self.tableAverage.setColumnCount(2)
        self.tableAverage.setObjectName("tableAverage")
        self.tableAverage.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableAverage.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAverage.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAverage.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAverage.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAverage.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAverage.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAverage.setHorizontalHeaderItem(1, item)
        self.tableAverage.horizontalHeader().setVisible(False)
        self.tableAverage.horizontalHeader().setDefaultSectionSize(58)
        self.tableAverage.horizontalHeader().setMinimumSectionSize(24)
        self.tableAverage.horizontalHeader().setStretchLastSection(True)
        self.tableAverage.verticalHeader().setDefaultSectionSize(24)
        self.tableAverage.verticalHeader().setMinimumSectionSize(24)
        self.tableAverage.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_5.addWidget(self.tableAverage)
        self.buttonResetAverageTemps = QtWidgets.QPushButton(self.centralwidget)
        self.buttonResetAverageTemps.setStyleSheet("QPushButton {\n"
"    border: 1px solid #d8d8d8;\n"
"    qproperty-icon: none;\n"
"    qproperty-iconSize: 18px;\n"
"    image : url("+ support.getResourcePath('./images/clear.svg')+ ");\n"
"    border-radius: 4px; \n"
"    background: #eeeeee; \n"
"    font-weight: normal; \n"
"    color: #222;\n"
"    padding: 4px; \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    image : url("+ support.getResourcePath('./images/clear_hover.svg')+ ");\n"
"    background: #d8d8d8; \n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    image : url("+ support.getResourcePath('./images/clear_pressed.svg')+ ");\n"
"    background: #c9c9c9; \n"
"}")
        self.buttonResetAverageTemps.setText("")
        self.buttonResetAverageTemps.setObjectName("buttonResetAverageTemps")
        self.verticalLayout_5.addWidget(self.buttonResetAverageTemps)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        spacerItem2 = QtWidgets.QSpacerItem(4, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.widgetCurrentValues = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetCurrentValues.sizePolicy().hasHeightForWidth())
        self.widgetCurrentValues.setSizePolicy(sizePolicy)
        self.widgetCurrentValues.setMinimumSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        self.widgetCurrentValues.setPalette(palette)
        font = QtGui.QFont()
        font.setKerning(True)
        self.widgetCurrentValues.setFont(font)
        self.widgetCurrentValues.setMouseTracking(False)
        self.widgetCurrentValues.setTabletTracking(False)
        self.widgetCurrentValues.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.widgetCurrentValues.setStyleSheet("")
        self.widgetCurrentValues.setObjectName("widgetCurrentValues")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widgetCurrentValues)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setSpacing(16)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(8)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setSpacing(4)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.widgetCurrentValues)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_9.setStyleSheet("font-weight: bold; color: #222; font-size:12px;")
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        self.line_4 = QtWidgets.QFrame(self.widgetCurrentValues)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_9.addWidget(self.line_4)
        self.verticalLayout_7.addLayout(self.verticalLayout_9)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(8)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widgetCurrentValues)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lineEditCpuMinTemp = QtWidgets.QLineEdit(self.widgetCurrentValues)
        self.lineEditCpuMinTemp.setEnabled(True)
        self.lineEditCpuMinTemp.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.lineEditCpuMinTemp.setFont(font)
        self.lineEditCpuMinTemp.setMouseTracking(False)
        self.lineEditCpuMinTemp.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.lineEditCpuMinTemp.setAcceptDrops(True)
        self.lineEditCpuMinTemp.setAutoFillBackground(False)
        self.lineEditCpuMinTemp.setStyleSheet("font-weight:normal; border:  1px solid #d8d8d8; width: 40px;")
        self.lineEditCpuMinTemp.setReadOnly(True)
        self.lineEditCpuMinTemp.setClearButtonEnabled(False)
        self.lineEditCpuMinTemp.setObjectName("lineEditCpuMinTemp")
        self.verticalLayout_2.addWidget(self.lineEditCpuMinTemp)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_8 = QtWidgets.QLabel(self.widgetCurrentValues)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_10.addWidget(self.label_8)
        self.lineEditCpuCurrentTemp = QtWidgets.QLineEdit(self.widgetCurrentValues)
        self.lineEditCpuCurrentTemp.setEnabled(True)
        self.lineEditCpuCurrentTemp.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEditCpuCurrentTemp.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.lineEditCpuCurrentTemp.setStyleSheet("font-weight:normal; border:  1px solid #d8d8d8; width: 40px;")
        self.lineEditCpuCurrentTemp.setReadOnly(True)
        self.lineEditCpuCurrentTemp.setObjectName("lineEditCpuCurrentTemp")
        self.verticalLayout_10.addWidget(self.lineEditCpuCurrentTemp)
        self.horizontalLayout_3.addLayout(self.verticalLayout_10)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.widgetCurrentValues)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.lineEditCpuMaxTemp = QtWidgets.QLineEdit(self.widgetCurrentValues)
        self.lineEditCpuMaxTemp.setEnabled(True)
        self.lineEditCpuMaxTemp.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEditCpuMaxTemp.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.lineEditCpuMaxTemp.setStyleSheet("font-weight:normal; border:  1px solid #d8d8d8; width: 40px;")
        self.lineEditCpuMaxTemp.setReadOnly(True)
        self.lineEditCpuMaxTemp.setObjectName("lineEditCpuMaxTemp")
        self.verticalLayout_4.addWidget(self.lineEditCpuMaxTemp)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.buttonResetGeneralTemps = QtWidgets.QPushButton(self.widgetCurrentValues)
        self.buttonResetGeneralTemps.setStyleSheet("QPushButton {\n"
"    border: 1px solid #d8d8d8;\n"
"    qproperty-icon: none;\n"
"    qproperty-iconSize: 18px;\n"
"    image : url("+ support.getResourcePath('./images/clear.svg')+ ");\n"
"    border-radius: 4px; \n"
"    background: #eeeeee; \n"
"    font-weight: normal; \n"
"    color: #222;\n"
"    padding: 4px; \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    image : url("+ support.getResourcePath('./images/clear_hover.svg')+ ");\n"
"    background: #d8d8d8; \n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    image : url("+ support.getResourcePath('./images/clear_pressed.svg')+ ");\n"
"    background: #c9c9c9; \n"
"}")
        self.buttonResetGeneralTemps.setObjectName("buttonResetGeneralTemps")
        self.verticalLayout_7.addWidget(self.buttonResetGeneralTemps)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSpacing(8)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setSpacing(4)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_10 = QtWidgets.QLabel(self.widgetCurrentValues)
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_10.setStyleSheet("font-weight: bold; color: #222; font-size:12px;")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_14.addWidget(self.label_10)
        self.line_7 = QtWidgets.QFrame(self.widgetCurrentValues)
        self.line_7.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_14.addWidget(self.line_7)
        self.verticalLayout_8.addLayout(self.verticalLayout_14)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_11 = QtWidgets.QLabel(self.widgetCurrentValues)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_13.addWidget(self.label_11)
        self.lineEditCpuMinTDP = QtWidgets.QLineEdit(self.widgetCurrentValues)
        self.lineEditCpuMinTDP.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.lineEditCpuMinTDP.setStyleSheet("font-weight:normal; border:  1px solid #d8d8d8; width: 40px;")
        self.lineEditCpuMinTDP.setReadOnly(True)
        self.lineEditCpuMinTDP.setObjectName("lineEditCpuMinTDP")
        self.verticalLayout_13.addWidget(self.lineEditCpuMinTDP)
        self.horizontalLayout_2.addLayout(self.verticalLayout_13)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_15 = QtWidgets.QLabel(self.widgetCurrentValues)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_17.addWidget(self.label_15)
        self.lineEditCpuCurrentTDP = QtWidgets.QLineEdit(self.widgetCurrentValues)
        self.lineEditCpuCurrentTDP.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.lineEditCpuCurrentTDP.setStyleSheet("font-weight:normal; border:  1px solid #d8d8d8; width: 40px;")
        self.lineEditCpuCurrentTDP.setReadOnly(True)
        self.lineEditCpuCurrentTDP.setObjectName("lineEditCpuCurrentTDP")
        self.verticalLayout_17.addWidget(self.lineEditCpuCurrentTDP)
        self.horizontalLayout_2.addLayout(self.verticalLayout_17)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_16 = QtWidgets.QLabel(self.widgetCurrentValues)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_16.addWidget(self.label_16)
        self.lineEditCpuMaxTDP = QtWidgets.QLineEdit(self.widgetCurrentValues)
        self.lineEditCpuMaxTDP.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.lineEditCpuMaxTDP.setStyleSheet("font-weight:normal; border:  1px solid #d8d8d8; width: 40px;")
        self.lineEditCpuMaxTDP.setReadOnly(True)
        self.lineEditCpuMaxTDP.setObjectName("lineEditCpuMaxTDP")
        self.verticalLayout_16.addWidget(self.lineEditCpuMaxTDP)
        self.horizontalLayout_2.addLayout(self.verticalLayout_16)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.buttonResetTDP = QtWidgets.QPushButton(self.widgetCurrentValues)
        self.buttonResetTDP.setStyleSheet("QPushButton {\n"
"    border: 1px solid #d8d8d8;\n"
"    qproperty-icon: none;\n"
"    qproperty-iconSize: 18px;\n"
"    image : url("+ support.getResourcePath('./images/clear.svg')+ ");\n"
"    border-radius: 4px; \n"
"    background: #eeeeee; \n"
"    font-weight: normal; \n"
"    color: #222;\n"
"    padding: 4px; \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    image : url("+ support.getResourcePath('./images/clear_hover.svg')+ ");\n"
"    background: #d8d8d8; \n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    image : url("+ support.getResourcePath('./images/clear_pressed.svg')+ ");\n"
"    background: #c9c9c9; \n"
"}")
        self.buttonResetTDP.setObjectName("buttonResetTDP")
        self.verticalLayout_8.addWidget(self.buttonResetTDP)
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.widgetCurrentValues)
        self.frameAlert = QtWidgets.QFrame(self.centralwidget)
        self.frameAlert.setEnabled(True)
        self.frameAlert.setMaximumSize(QtCore.QSize(16777215, 600))
        self.frameAlert.setVisible(False)
        self.frameAlert.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameAlert.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameAlert.setObjectName("frameAlert")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.frameAlert)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(4, 0, 4, 0)
        self.horizontalLayout_8.setSpacing(8)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.buttonAlertExpand = QtWidgets.QPushButton(self.frameAlert)
        self.buttonAlertExpand.setMaximumSize(QtCore.QSize(20, 20))
        self.buttonAlertExpand.setVisible(True)
        self.buttonAlertExpand.setStyleSheet("QPushButton {\n"
"    qproperty-icon: none;\n"
"    qproperty-iconSize: 18px;\n"
"    image : url("+ support.getResourcePath('./images/expand.svg')+ ");\n"
"    border-radius: 4px; \n"
"    background: #eeeeee; \n"
"    font-weight: normal; \n"
"    color: #222;\n"
"    padding: 4px; \n"
"    margin-bottom: 1px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    image : url("+ support.getResourcePath('./images/expand_hover.svg')+ ");\n"
"    background: #d8d8d8; \n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    image : url("+ support.getResourcePath('./images/expand_pressed.svg')+ ");\n"
"    background: #c9c9c9; \n"
"}")
        self.buttonAlertExpand.setText("")
        self.buttonAlertExpand.setFlat(True)
        self.buttonAlertExpand.setObjectName("buttonAlertExpand")
        self.horizontalLayout_8.addWidget(self.buttonAlertExpand)
        self.labelAlert = QtWidgets.QLabel(self.frameAlert)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAlert.sizePolicy().hasHeightForWidth())
        self.labelAlert.setSizePolicy(sizePolicy)
        self.labelAlert.setStyleSheet("padding:4px;")
        self.labelAlert.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelAlert.setOpenExternalLinks(True)
        self.labelAlert.setObjectName("labelAlert")
        self.horizontalLayout_8.addWidget(self.labelAlert)
        self.buttonAlertClose = QtWidgets.QPushButton(self.frameAlert)
        self.buttonAlertClose.setMinimumSize(QtCore.QSize(20, 20))
        self.buttonAlertClose.setMaximumSize(QtCore.QSize(20, 20))
        self.buttonAlertClose.setStyleSheet("QPushButton {\n"
"    qproperty-icon: none;\n"
"    qproperty-iconSize: 18px;\n"
"    image : url("+ support.getResourcePath('./images/close.svg')+ ");\n"
"    border-radius: 4px; \n"
"    background: none; \n"
"    font-weight: normal; \n"
"    color: #222;\n"
"    padding: 4px; \n"
"    margin-bottom: 1px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    image : url("+ support.getResourcePath('./images/close_hover.svg')+ ");\n"
"    background: none; \n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    image : url("+ support.getResourcePath('./images/close_pressed.svg')+ ");\n"
"    background: none; \n"
"}")
        self.buttonAlertClose.setText("")
        self.buttonAlertClose.setFlat(True)
        self.buttonAlertClose.setObjectName("buttonAlertClose")
        self.horizontalLayout_8.addWidget(self.buttonAlertClose)
        self.verticalLayout_15.addLayout(self.horizontalLayout_8)
        self.plainTextEditAlert = QtWidgets.QPlainTextEdit(self.frameAlert)
        self.plainTextEditAlert.setVisible(False)
        self.plainTextEditAlert.setStyleSheet("")
        self.plainTextEditAlert.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.plainTextEditAlert.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.plainTextEditAlert.setLineWidth(0)
        self.plainTextEditAlert.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.plainTextEditAlert.setReadOnly(True)
        self.plainTextEditAlert.setPlainText("")
        self.plainTextEditAlert.setBackgroundVisible(True)
        self.plainTextEditAlert.setObjectName("plainTextEditAlert")
        self.verticalLayout_15.addWidget(self.plainTextEditAlert)
        self.verticalLayout_3.addWidget(self.frameAlert)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.horizontalLayout_7.setStretch(1, 1)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionShowSettings = QtGui.QAction(MainWindow)
        self.actionShowSettings.setObjectName("actionShowSettings")
        self.actionResetAll = QtGui.QAction(MainWindow)
        self.actionResetAll.setObjectName("actionResetAll")
        self.retranslateUi(MainWindow, locale)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow, locale):
        self.CPUinfoTable.setSortingEnabled(False)
        item = self.CPUinfoTable.horizontalHeaderItem(0)
        item.setText(trans(locale, "frequency"))
        item = self.CPUinfoTable.horizontalHeaderItem(1)
        item.setText(trans(locale, "load"))
        self.label_3.setText(trans(locale, "averages"))
        item = self.tableAverage.verticalHeaderItem(0)
        item.setText("1 " + trans(locale, "minutes") + ".")
        item = self.tableAverage.verticalHeaderItem(1)
        item.setText("5 " + trans(locale, "minutes") + ".")
        item = self.tableAverage.verticalHeaderItem(2)
        item.setText("15 " + trans(locale, "minutes") + ".")
        item = self.tableAverage.verticalHeaderItem(3)
        item.setText("1 " + trans(locale, "hour"))
        item = self.tableAverage.verticalHeaderItem(4)
        item.setText(trans(locale, "24_hours"))
        item = self.tableAverage.horizontalHeaderItem(0)
        item.setText(trans(locale, "temp"))
        item = self.tableAverage.horizontalHeaderItem(1)
        item.setText(trans(locale, "TDP"))
        self.label_9.setText(trans(locale, "temp"))
        self.label.setText(trans(locale, "min") + ".")
        self.lineEditCpuMinTemp.setText("0")
        self.label_8.setText(trans(locale, "current_she"))
        self.lineEditCpuCurrentTemp.setText("0")
        self.label_2.setText(trans(locale, "max") + ".")
        self.lineEditCpuMaxTemp.setText("0")
        self.label_10.setText(trans(locale, "TDP"))
        self.label_11.setText(trans(locale, "min") + ".")
        self.lineEditCpuMinTDP.setText("0")
        self.label_15.setText(trans(locale, "current_he"))
        self.lineEditCpuCurrentTDP.setText("0")
        self.label_16.setText(trans(locale, "max") + ".")
        self.lineEditCpuMaxTDP.setText("0")

        #Получаем из конфига, чтобы проставить тот что был до переключения
        self.labelAlert.setOpenExternalLinks(True)
        self.actionShowSettings.setText(trans(locale, "settings"))
        self.actionResetAll.setText(trans(locale, "clear_all"))

        #Проставляем алерты
        self.labelAlert.setText(trans(locale, "alert_title"))
        self.plainTextEditAlert.setPlainText(trans(locale, "alert_description"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
