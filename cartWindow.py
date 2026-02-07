from PySide6.QtWidgets import QMainWindow
from ui_shopping_cart import Ui_MainWindow

from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from PySide6.QtWidgets import (
    QMainWindow, QTableWidgetItem, QPushButton, QSpinBox, QWidget, QHBoxLayout, QLabel,QMessageBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt

class CartWindow(QMainWindow):
    def __init__(self, cart_items, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Savatcha")

        self.load_cart(cart_items)

        self.total_price = 0
        self.calculate_total()
        self.ui.checkoutButton.setIcon(QIcon("assets/order_cart.png"))
        self.ui.checkoutButton.setIconSize(QSize(50, 50))
        self.ui.checkoutButton.clicked.connect(self.checkout)
        self.ui.checkoutButton.clicked.connect(self.open_checkout)





    def load_cart(self, cart_items):
        table = self.ui.cartTable
        table.setRowCount(len(cart_items))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Maxsulot", "Narx", "Miqdor", ""])

        for row, (name, price, stock) in enumerate(cart_items):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(price))

            qty_widget = self.create_qty_widget(stock)
            table.setCellWidget(row, 2, qty_widget)

            btn = QPushButton()
            btn.setIcon(QIcon("assets/trash.png"))
            btn.setIconSize(QSize(18, 18))
            btn.setStyleSheet("border:none;")
            btn.clicked.connect(self.remove_clicked)
            table.setCellWidget(row, 3, btn)

        self.calculate_total()


    def calculate_total(self):
        table = self.ui.cartTable
        total = 0

        for row in range(table.rowCount()):
            price_item = table.item(row, 1)
            qty_widget = table.cellWidget(row, 2)

            if price_item and qty_widget:
                price = float(price_item.text().replace("so`m", ""))
                label = qty_widget.findChild(QLabel)
                qty = int(label.text())
                total += price * qty

        self.ui.totalLabel.setText(f"Umumiy: {total:.2f} So'm")


    def remove_clicked(self):
        button = self.sender()
        table = self.ui.cartTable

        for row in range(table.rowCount()):
            if table.cellWidget(row, 3) == button:
                product_name = table.item(row, 0).text()


                if self.parent_window:
                    for item in self.parent_window.cart:
                        if item[0] == product_name:
                            self.parent_window.cart.remove(item)
                            break


                table.removeRow(row)
                break

        self.calculate_total()


    def create_qty_widget(self, stock):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        btn_minus = QPushButton("−")
        btn_plus = QPushButton("+")
        label = QLabel("1")

        btn_minus.setFixedSize(28, 28)
        btn_plus.setFixedSize(28, 28)
        label.setFixedWidth(24)
        label.setAlignment(Qt.AlignCenter)

        btn_minus.clicked.connect(lambda: self.change_qty(label, -1, stock))
        btn_plus.clicked.connect(lambda: self.change_qty(label, +1, stock))

        layout.addWidget(btn_minus)
        layout.addWidget(label)
        layout.addWidget(btn_plus)

        return container

    def change_qty(self, label, delta, stock):
        qty = int(label.text())
        new_qty = qty + delta

        if new_qty < 1:
            return

        if new_qty > stock:
            QMessageBox.warning(
                self,
                "Out of stock",
                f"Only {stock} items available!"
            )
            return

        label.setText(str(new_qty))
        self.calculate_total()
    def checkout(self):
        from mainwindow import load_products_data, save_products_data

        data = load_products_data()
        products = data["products"]

        cart_items = self.get_cart_items_from_table()

        for cart_item in cart_items:
            found = False

            for p in products:
                if p["name"] == cart_item["name"]:
                    found = True
                    stock = int(p["stock"])
                    qty = int(cart_item["qty"])

                    # 🔴 STOCK TEKSHIRUV
                    if qty > stock:
                        QMessageBox.warning(
                            self,
                            "Stock error",
                            f'{p["name"]} ga yetarli zaxira mavjud emas\n'
                            f'Mavjud: {p["stock"]}'
                        )
                        return




                    if p["stock"] == 0:
                        p["status"] = "Zaxira mavjud emas"

                    break  # 🔥 MUHIM: product topildi → chiqamiz

            if not found:
                QMessageBox.warning(
                    self,
                    "Error",
                    f'Maxsulot topilmadi: {cart_item["name"]}'
                )
                return
            if not cart_items:
                QMessageBox.warning(
                    self,
                    "Empty cart",
                    "Sotib olmoqchi bo'lgan maxsulotingiz mavjud emas!"
                )
                return



        QMessageBox.information(
            self,
            "Success",
            "Buyurtma muvaffaqiyatli bajarildi!"
        )


        if self.parent_window and hasattr(self.parent_window, "load_products"):
            self.parent_window.load_products()

        self.close()
        from checkout import CheckoutWindow
        checkout = CheckoutWindow(
                cart_items=self.get_cart_items_from_table(),
                parent=self.parent_window
            )
        checkout.show()
    def get_cart_items_from_table(self):
        items = []
        table = self.ui.cartTable

        for row in range(table.rowCount()):
            name = table.item(row, 0).text()
            price = float(table.item(row, 1).text().replace("so`m", ""))

            qty_widget = table.cellWidget(row, 2)
            label = qty_widget.findChild(QLabel)
            qty = int(label.text())

            items.append({
                "name": name,
                "price": price,
                "qty": qty
            })

        return items

    def open_checkout(self):
        cart_items = self.get_cart_items_from_table()

        if not cart_items:
            QMessageBox.warning(
                self,
                "Savatcha bo'sh",
                "No items to checkout!"
            )
            return



