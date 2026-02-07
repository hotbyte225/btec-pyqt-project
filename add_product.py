from PySide6.QtWidgets import QMainWindow, QMessageBox
from ui_add_product import Ui_MainWindow
from mainwindow import load_products_data, save_products_data


class AddProductWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Add Product")

        self.ui.categoryCombo.addItems([
            "Oshxona texnikasi",
            "Tozalash uskunalari",
            "Isitish va sovitish qurilmalari",
            "Shaxsiy parvarish qurilmalari",
            "Aqlli uy texnikasi"
        ])

        self.ui.saveButton.clicked.connect(self.save_product)


    def save_product(self):
        name = self.ui.nameEdit.text().strip()
        category = self.ui.categoryCombo.currentText()
        price_text = self.ui.priceEdit.text().strip()
        stock_text = self.ui.stockEdit.text().strip()

        # 🔴 VALIDATION
        if not name:
            QMessageBox.warning(self, "Xato", "Mahsulot nomini kiriting")
            return

        if not price_text.isdigit():
            QMessageBox.warning(self, "Xato", "Narx faqat raqam bo‘lishi kerak")
            return

        if not stock_text.isdigit():
            QMessageBox.warning(self, "Xato", "Miqdor faqat raqam bo‘lishi kerak")
            return

        price = int(price_text)
        stock = int(stock_text)

        data = load_products_data()
        products = data["products"]

        new_id = max([p["id"] for p in products], default=0) + 1

        status = "Mavjud" if stock > 0 else "Mavjud emas"

        products.append({
            "id": new_id,
            "name": name,
            "category": category,
            "price": price,
            "stock": stock,
            "status": status
        })

        save_products_data(data)

        QMessageBox.information(self, "OK", "Mahsulot qo‘shildi")

        # 🔄 Parent table refresh
        if self.parent():
            self.parent().load_products()

        self.close()
