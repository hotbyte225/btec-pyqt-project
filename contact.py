from PySide6.QtWidgets import QMainWindow
from ui_contact import Ui_MainWindow   # .ui dan generatsiya qilingan

class SupportContact(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Qo'llab-quvvatlash")
