import sys
import json
from cartWindow import CartWindow
from admin_login import LoginWindow
from receipt_history import ReceiptHistoryWindow
from contact import SupportContact
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QMessageBox
)
from ui_form import Ui_MainWindow
from about_membership import AboutMembershipWindow
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtGui import QColor

PRODUCTS_FILE = "data/fake_products_100.json"
# fake_products_100.json ni ochish o'qish
def load_products_data():
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# fake_products_100.json ni saqlash (ma'lumotkarni yangilash)
def save_products_data(data):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()

        # Frontend qismi bilan ulash
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Bosh menyu")
        #cart listi jadvaldan tanlangan maxsulotlarni saqlaydi
        self.cart = []

        # Jadvalga maxsulotlar ma'lumotlarni yuklaydi
        self.load_products()

        #Input Label signalni ulash
        self.ui.lineEdit.textChanged.connect(self.filter_products)

        # Savatchaga qo'shish tugmasini Icon joylash
        self.ui.addCartButton.setIcon(QIcon("assets/cart.png"))
        self.ui.addCartButton.setIconSize(QSize(50, 50))

        # Savatchaga qo'shish tugmasini "add_to_cart" signali(funksiyasi) bilan ulash
        self.ui.addCartButton.clicked.connect(self.add_to_cart)

        # Savatchani ko'rish tugmasini Icon joylash
        self.ui.viewCartButton.setIcon(QIcon("assets/view_cart.png"))
        self.ui.viewCartButton.setIconSize(QSize(50, 50))
        self.cart_window = None
        # Savatchani ko'rish tugmasini "open_cart" signali(funksiyasi) bilan ulash
        self.ui.viewCartButton.clicked.connect(self.open_cart)

        # Cheklar tarixi tugmasini "open_receipts" signali(funksiyasi) bilan ulash
        self.ui.recipesButton.clicked.connect(self.open_receipts)
        # Admin logingi kirish
        self.ui.adminButton.clicked.connect(self.open_admin_login)
        # Maxsulotlar kategoriyalar yordamida saralash va jadvalni yangilash
        self.load_categories()
         # Maxsulotlar kategoriyalar Combo Button ya'ni maxsulotlar kategoriyalarini saralash tugmasini "filter_by_category" signali bilan ulash
        self.ui.categoryComboButton.currentTextChanged.connect(self.filter_by_category)
        self.ui.aboutMembershipButton.clicked.connect(self.open_about_membership)


        self.ui.supportButton.clicked.connect(self.open_support)
    def open_admin_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
    def open_support(self):
        self.support_window = SupportContact()
        self.support_window.show()

    #Bu signal funksiyasi Receipt history tugmani bosganda Receipt history oynasi ochiladi
    def open_receipts(self):
        self.receipt_window = ReceiptHistoryWindow()
        self.receipt_window.show()

    #Bu signal funksiyasi Open cart tugmani bosganda Shopping cart oynasi ochiladi
    def open_cart(self):
        self.cart_window = CartWindow(self.cart, parent=self)
        self.cart_window.show()

    def open_about_membership(self):
        self.about_window = AboutMembershipWindow()
        self.about_window.show()

    def load_categories(self):
        # Kategoriya qarab set ga joylashtiradi
        categories = set()
        data = load_products_data()
        for p in data["products"]:
            categories.add(p["category"])
        # Dastur ishga tushganda odatiy All(xamma) katogoriyani ko'rsatadi
        self.ui.categoryComboButton.addItem("Xammasi")
        self.ui.categoryComboButton.addItems(sorted(categories))

    def filter_by_category(self, category):
        table = self.ui.productTable

        for row in range(table.rowCount()):
            category_item = table.item(row, 3)

            if category == "Xammasi":
                table.setRowHidden(row, False)
            elif category_item.text() == category:
                table.setRowHidden(row, False)
            else:
                table.setRowHidden(row, True)





    def load_products(self):
        data = load_products_data()
        products = data["products"]

        table = self.ui.productTable
        table.setRowCount(len(products))
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(
            ["Tanlash", "ID" ,"Maxsulot", "Toifa", "Narx", "Miqdor", "Holat"]
        )


        for row, p in enumerate(products):
            id_item = QTableWidgetItem(str(p["id"]))
            checkbox = QCheckBox()
            checkbox.setChecked(False)
            checkbox.setStyleSheet("margin-left:25px;")
            table.setCellWidget(row, 0, checkbox)

            table.setItem(row, 1, id_item)
            table.setItem(row, 2, QTableWidgetItem(p["name"]))
            table.setItem(row, 3, QTableWidgetItem(p["category"]))
            table.setItem(row, 4, QTableWidgetItem(f'{p["price"]} so`m'))
            table.setItem(row, 5, QTableWidgetItem(str(p["stock"])))

            status_item = QTableWidgetItem(p["status"])
            status_item.setForeground(QColor("green"))
            if p["status"].lower() == "mavjud emas":
                checkbox.setEnabled(False)
                status_item.setForeground(QColor("red"))

            table.setItem(row, 6, status_item)

        table.setColumnWidth(0, 80)
    # Input label da maxsulotlarni qidirish
    def filter_products(self, text):
        table = self.ui.productTable
        for row in range(table.rowCount()):
            item = table.item(row, 2)
            if text.lower() in item.text().lower():
                table.setRowHidden(row, False)
            else:
                table.setRowHidden(row, True)

    def add_to_cart(self):
        table = self.ui.productTable
        added_items = []
        added = 0
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                name = table.item(row, 2).text()
                price = table.item(row, 4).text()

                stock = int(table.item(row, 5).text())

                self.cart.append((name, price, stock))
                added_items.append(f"• {name} — {price}")
                added +=1

        if added == 0:
            QMessageBox.warning(self, "Ogohlantirish", "Maxsulot tanlanmagan!")
            return

        QMessageBox.information(
            self,
            "Maxsulotlar savatchaga qo'shildi",
            "Qo'shilgan maxsulotlar:\n\n" + "\n".join(added_items)
        )






if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
