import sys
import json
from cartWindow import CartWindow
from add_product import AddProductWindow
from receipt_history import ReceiptHistoryWindow
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QMessageBox
)
from ui_admin_menu import Ui_MainWindow
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
        self.setWindowTitle("Admin menyu")
        #cart listi jadvaldan tanlangan maxsulotlarni saqlaydi
        self.cart = []

        # Jadvalga maxsulotlar ma'lumotlarni yuklaydi
        self.load_products()

        #Input Label signalni ulash
        self.ui.lineEdit.textChanged.connect(self.filter_products)

        # Savatchaga qo'shish tugmasini Icon joylash
        self.ui.addProductButton.setIcon(QIcon("assets/add_product.png"))
        self.ui.addProductButton.setIconSize(QSize(50, 50))


        self.ui.addProductButton.clicked.connect(self.open_add_product)

        # Savatchani ko'rish tugmasini Icon joylash
        self.ui.deleteButton.setIcon(QIcon("assets/del_product.png"))
        self.ui.deleteButton.setIconSize(QSize(50, 50))
        self.cart_window = None
        # Savatchani ko'rish tugmasini "open_cart" signali(funksiyasi) bilan ulash
        self.ui.deleteButton.clicked.connect(self.delete_selected_products)

        # Cheklar tarixi tugmasini "open_receipts" signali(funksiyasi) bilan ulash
        self.ui.recipesButton.clicked.connect(self.open_receipts)
        # Admin logingi kirish
        self.ui.buyerButton.clicked.connect(self.open_buyer_menu)
        # Maxsulotlar kategoriyalar yordamida saralash va jadvalni yangilash
        self.load_categories()
         # Maxsulotlar kategoriyalar Combo Button ya'ni maxsulotlar kategoriyalarini saralash tugmasini "filter_by_category" signali bilan ulash
        self.ui.categoryComboButton.currentTextChanged.connect(self.filter_by_category)




    def open_buyer_menu(self):
        from mainwindow import MainWindow
        self.buyer_window = MainWindow()
        self.buyer_window.show()
        self.close()

    #Bu signal funksiyasi Receipt history tugmani bosganda Receipt history oynasi ochiladi
    def open_receipts(self):
        self.receipt_window = ReceiptHistoryWindow()
        self.receipt_window.show()

    #Bu signal funksiyasi Open cart tugmani bosganda Shopping cart oynasi ochiladi
    def open_cart(self):
        self.cart_window = CartWindow(self.cart, parent=self)
        self.cart_window.show()

    def open_add_product(self):
        self.add_product_window = AddProductWindow(parent=self)
        self.add_product_window.show()

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

    def delete_selected_products(self):
        table = self.ui.productTable
        rows_to_delete = []

        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                rows_to_delete.append(row)

        if not rows_to_delete:
            QMessageBox.warning(self, "Warning", "Maxsulot tanlanmagan!")
            return


        from mainwindow import load_products_data, save_products_data
        data = load_products_data()
        products = data["products"]

        # 3️⃣ Pastdan yuqoriga o‘chiramiz (maxsulotni nomiga qarab)
        for row in reversed(rows_to_delete):
            product_name = table.item(row, 2).text()

            # JSON’dan o‘chirish
            products[:] = [p for p in products if p["name"] != product_name]

            # UI table’dan o‘chirish
            table.removeRow(row)

        save_products_data(data)

        QMessageBox.information(
            self,
            "Success",
            f"{len(rows_to_delete)} product(s) deleted"
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
