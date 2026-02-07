# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.titleLabel)

        self.cartTable = QTableWidget(self.centralwidget)
        if (self.cartTable.columnCount() < 4):
            self.cartTable.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.cartTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.cartTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.cartTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.cartTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.cartTable.setObjectName(u"cartTable")
        self.cartTable.setColumnCount(4)

        self.verticalLayout.addWidget(self.cartTable)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setObjectName(u"bottomLayout")
        self.removeBtn = QPushButton(self.centralwidget)
        self.removeBtn.setObjectName(u"removeBtn")

        self.bottomLayout.addWidget(self.removeBtn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bottomLayout.addItem(self.horizontalSpacer)

        self.totalLabel = QLabel(self.centralwidget)
        self.totalLabel.setObjectName(u"totalLabel")

        self.bottomLayout.addWidget(self.totalLabel)

        self.checkoutBtn = QPushButton(self.centralwidget)
        self.checkoutBtn.setObjectName(u"checkoutBtn")

        self.bottomLayout.addWidget(self.checkoutBtn)


        self.verticalLayout.addLayout(self.bottomLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLabel.setStyleSheet(QCoreApplication.translate("MainWindow", u"font-size:20px;font-weight:bold;", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"\U0001f6d2 Shopping Cart", None))
        ___qtablewidgetitem = self.cartTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem1 = self.cartTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Product", None));
        ___qtablewidgetitem2 = self.cartTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Price", None));
        ___qtablewidgetitem3 = self.cartTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Quantity", None));
        self.removeBtn.setText(QCoreApplication.translate("MainWindow", u"Remove Selected", None))
        self.totalLabel.setStyleSheet(QCoreApplication.translate("MainWindow", u"font-size:16px;font-weight:bold;", None))
        self.totalLabel.setText(QCoreApplication.translate("MainWindow", u"Total: $0", None))
        self.checkoutBtn.setText(QCoreApplication.translate("MainWindow", u"Checkout", None))
    # retranslateUi

