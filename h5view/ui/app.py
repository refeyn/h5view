# pylint: disable=all
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QPlainTextEdit,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTabWidget, QTableView, QToolBar, QTreeView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionShow_Image = QAction(MainWindow)
        self.actionShow_Image.setObjectName(u"actionShow_Image")
        self.actionShow_Image.setCheckable(True)
        self.actionAutoscale_Image = QAction(MainWindow)
        self.actionAutoscale_Image.setObjectName(u"actionAutoscale_Image")
        self.actionAutoscale_Image.setCheckable(True)
        self.actionAutoscale_Image.setChecked(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.treeView = QTreeView(self.splitter)
        self.treeView.setObjectName(u"treeView")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.treeView)
        self.treeView.header().setVisible(False)
        self.rightPanels = QWidget(self.splitter)
        self.rightPanels.setObjectName(u"rightPanels")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.rightPanels.sizePolicy().hasHeightForWidth())
        self.rightPanels.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.rightPanels)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pathLabel = QLabel(self.rightPanels)
        self.pathLabel.setObjectName(u"pathLabel")

        self.gridLayout.addWidget(self.pathLabel, 0, 0, 1, 1)

        self.typeLabel = QLabel(self.rightPanels)
        self.typeLabel.setObjectName(u"typeLabel")
        self.typeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.typeLabel, 0, 1, 1, 1)

        self.tabWidget = QTabWidget(self.rightPanels)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy2)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_4 = QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.spinContainer = QWidget(self.tab)
        self.spinContainer.setObjectName(u"spinContainer")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.spinContainer.sizePolicy().hasHeightForWidth())
        self.spinContainer.setSizePolicy(sizePolicy3)
        self.horizontalLayout = QHBoxLayout(self.spinContainer)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(5, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addWidget(self.spinContainer)

        self.viewWidgetContainer = QWidget(self.tab)
        self.viewWidgetContainer.setObjectName(u"viewWidgetContainer")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.viewWidgetContainer.sizePolicy().hasHeightForWidth())
        self.viewWidgetContainer.setSizePolicy(sizePolicy4)
        self.verticalLayout = QVBoxLayout(self.viewWidgetContainer)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.valueTextView = QPlainTextEdit(self.viewWidgetContainer)
        self.valueTextView.setObjectName(u"valueTextView")
        self.valueTextView.setReadOnly(True)

        self.verticalLayout.addWidget(self.valueTextView)

        self.valueTableView = QTableView(self.viewWidgetContainer)
        self.valueTableView.setObjectName(u"valueTableView")
        self.valueTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.valueTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.valueTableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.valueTableView.horizontalHeader().setVisible(False)
        self.valueTableView.horizontalHeader().setStretchLastSection(True)
        self.valueTableView.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.valueTableView)


        self.verticalLayout_4.addWidget(self.viewWidgetContainer)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.attrTableView = QTableView(self.tab_2)
        self.attrTableView.setObjectName(u"attrTableView")
        self.attrTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.attrTableView.setTextElideMode(Qt.ElideNone)
        self.attrTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.attrTableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.attrTableView.horizontalHeader().setVisible(False)
        self.attrTableView.horizontalHeader().setStretchLastSection(True)
        self.attrTableView.verticalHeader().setVisible(False)

        self.verticalLayout_3.addWidget(self.attrTableView)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_5 = QVBoxLayout(self.tab_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.metadataTableView = QTableView(self.tab_3)
        self.metadataTableView.setObjectName(u"metadataTableView")
        self.metadataTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.metadataTableView.setTextElideMode(Qt.ElideNone)
        self.metadataTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.metadataTableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.metadataTableView.horizontalHeader().setVisible(False)
        self.metadataTableView.horizontalHeader().setStretchLastSection(True)
        self.metadataTableView.verticalHeader().setVisible(False)

        self.verticalLayout_5.addWidget(self.metadataTableView)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 2)

        self.splitter.addWidget(self.rightPanels)

        self.verticalLayout_2.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionShow_Image)
        self.toolBar.addAction(self.actionAutoscale_Image)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"H5View", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionShow_Image.setText(QCoreApplication.translate("MainWindow", u"Show 2D as Image", None))
        self.actionAutoscale_Image.setText(QCoreApplication.translate("MainWindow", u"Autoscale Image", None))
        self.pathLabel.setText(QCoreApplication.translate("MainWindow", u"/x/y/z", None))
        self.typeLabel.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Value", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Attributes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Metadata", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

