import json
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton
from ui_recipt_history import Ui_MainWindow   # .ui dan generatsiya qilingan
from receipt import ReceiptWindow
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
class ReceiptHistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Cheklar tarixi")
        self.load_receipts()

    def load_receipts(self):
        with open("data/recipes.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        receipts = data.get("receipts", [])
        table = self.ui.receiptTable

        table.setRowCount(len(receipts))
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels([
            "ID", "Mijoz", "Telefon raqam", "Maxsulot","Yetkazib berish turi","Yetkazib berish narxi" , "Jami", "Sana","",
        ])

        for row, r in enumerate(receipts):
            table.setItem(row, 0, QTableWidgetItem(str(r["id"])))
            table.setItem(row, 1, QTableWidgetItem(r["customer"]["name"]))
            table.setItem(row, 2, QTableWidgetItem(r["customer"]["phone"]))
            table.setItem(row, 3, QTableWidgetItem(str(len(r["items"]))))
            table.setItem(row, 4, QTableWidgetItem(r["delivery_type"]))
            table.setItem(row, 5, QTableWidgetItem(str(r["delivery_price"])))
            table.setItem(row, 6, QTableWidgetItem(f'{r["total"]} so`m'))
            table.setItem(row, 7, QTableWidgetItem(r["date"]))
            btn = QPushButton()
            btn.setIcon(QIcon("assets/view.png"))
            btn.setIconSize(QSize(20, 20))
            btn.setStyleSheet("border:none;")
            btn.clicked.connect(lambda _, rec=r: self.open_receipt(rec))

            table.setCellWidget(row, 8, btn)
    def open_receipt(self, receipt_data):
        cart_items = receipt_data["items"]
        customer = receipt_data["customer"]
        total = receipt_data["total"]
        date = receipt_data["date"]
        delivery_type =  receipt_data["delivery_type"]
        delivery_price = receipt_data["delivery_price"]
        bal = receipt_data["point"]
        payment_type = receipt_data["payment_type"]
        self.view_window = ReceiptWindow(cart_items, customer, total,date,delivery_type,delivery_price,bal,payment_type)
        self.view_window.show()
