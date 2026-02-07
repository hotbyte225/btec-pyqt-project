from PySide6.QtWidgets import QMainWindow, QMessageBox
from ui_admin_login import Ui_MainWindow
import json

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Admin tizimiga kirish")
        self.ui.loginButton.clicked.connect(self.login)

        self.ui.backButton.clicked.connect(self.back)

    def login(self):
        username = self.ui.usernameInput.text().strip()
        password = self.ui.passwordInput.text().strip()

        with open("data/users.json", "r", encoding="utf-8") as f:
            admin = json.load(f)["admin"]

        if username == admin["username"] and password == admin["password"]:
            self.open_main()
        else:
            QMessageBox.warning(self, "Error", "Foydalanuvchi nomi yoki parol noto'g'ri.")

    def open_main(self):
        from admin_menu import MainWindow
        self.main = MainWindow()
        self.main.show()
        self.close()

    def back(self):
        from mainwindow import MainWindow
        self.main = MainWindow()
        self.main.show()
        self.close()
