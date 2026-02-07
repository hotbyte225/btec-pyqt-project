from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from PySide6.QtGui import QPixmap
from ui_receipt import Ui_MainWindow
from datetime import datetime
from PySide6.QtCore import Qt
class ReceiptWindow(QMainWindow):
    def __init__(self, cart_items,customer,total,date,delivery_type,delivery_price, bal,customer_data):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(460, 485)
        self.setWindowTitle("Maxsulot cheki")


        self.ui.totalLabel.setText(f"Total: $:.2f")


        self.load_items(cart_items)
        self.ui.nameLabel.setText(f"{customer['name']}")
        self.ui.phoneLabel.setText(f"{customer['phone']}")
        self.ui.addressLabel.setText(f"{customer['address']}")
        self.ui.membershipLabel.setPixmap(QPixmap(f"images/{customer['membership']}.png"))
        self.ui.membershipLabel.setScaledContents(True)
        self.ui.delivery_type.setText(str(delivery_type))
        self.ui.delivery_price.setText(f"{delivery_price} so`m")
        self.ui.dateLabel.setText(f"{date}")
        payment = customer["payment_type"]
        self.ui.paymentType.setText(f"{payment}")
        self.show_total(total)
        self.ui.bal.setText(f"{bal}")
    def load_items(self, items):
        table = self.ui.receiptTable
        table.setRowCount(len(items))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(
            ["Maxsulot", "Narx", "Miqdor"]
        )

        for row, item in enumerate(items):
            table.setItem(row, 0, QTableWidgetItem(item["name"]))
            table.setItem(row, 1, QTableWidgetItem(f"{item['price']} so`m"))
            table.setItem(row, 2, QTableWidgetItem(str(item["qty"])))
            table.setItem(
                row, 3,
                QTableWidgetItem(
                    f"${item['price'] * item['qty']:.2f}"
                )
            )
    #Chek oynasiga umumiy narxni ko'rsatish
    def show_total(self, total):

        self.ui.totalLabel.setText(f"Jami: {total} so'm")
