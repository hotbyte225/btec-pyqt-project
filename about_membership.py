from PySide6.QtWidgets import QMainWindow
from ui_about_membership import Ui_MainWindow   # .ui dan generatsiya qilingan

class AboutMembershipWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("A'zolik tariflari")
