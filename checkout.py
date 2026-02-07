from PySide6.QtWidgets import QMainWindow, QMessageBox
from ui_checkout import Ui_MainWindow
from receipt import ReceiptWindow
import sys
import json
from datetime import datetime
from receipt_manager import add_receipt
import re
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QMessageBox,
)
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtGui import QColor



# A'zolik tariflari dictinoryda
MEMBERSHIPS = {
    "Bronze": {
        "point": 1,
        "discount": 0.00,
        "description": "Bronze – oddiy ballar va chegirmalar"
    },
    "Silver": {
        "point": 4,
        "discount": 0.05,   # 5%
        "description": "Silver – 5% chegirma"
    },
    "Gold": {
        "point": 6,
        "discount": 0.10,   # 10%
        "description": "Gold – 10% chegirma + yetkazib berish bepul"
    },
    "Business": {
        "point": 8,
        "discount": 0.15,   # 15%
        "description": "Business – 15% chegirma + maxsus servis + yetkazib berish bepul"
    }
}


def is_valid_phone(phone):
    return re.match(r"^\+998\d{9}$", phone)

class CheckoutWindow(QMainWindow):




    def __init__(self, cart_items, parent=None):
        super().__init__(parent)

        # Boshqa oynalardan ma'lumot yig'ish
        self.parent_window = parent

        # PySide6 UI dizayndan yani frontend qismidan backend qismi bilan ulash
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Ro'yxatdan o'tish")
        self.total_price = 0

        self.load_items(cart_items)



        self.ui.deliveryCombo.addItem("Olib ketish", {"type": "Olib ketish", "price": 0})
        self.ui.deliveryCombo.addItem("Shahar bo‘ylab", {"type": "Shahar bo‘ylab", "price": 200})
        self.ui.deliveryCombo.addItem("Viloyatga", {"type": "Viloyatga", "price": 500})

        self.ui.deliveryCombo.currentIndexChanged.connect(self.update_total)

        self.update_membership()
        self.calculate_total()

        # Tugmalarga Icon yani rasm joylash
        self.ui.confirmButton.setIcon(QIcon("assets/order_cart.png"))
        self.ui.confirmButton.setIconSize(QSize(50, 50))

        self.ui.cancelButton.setIcon(QIcon("assets/cancel.png"))
        self.ui.cancelButton.setIconSize(QSize(50, 50))
        self.ui.cancelButton.clicked.connect(self.cancel)

        # bronzeButton silverButton goldButton confirmButton signallar ya'ni foydalanuchi manashu tugmani bosganda funksiyalar ishlaydi
        self.ui.bronzeButton.toggled.connect(self.update_membership)
        self.ui.silverButton.toggled.connect(self.update_membership)
        self.ui.goldButton.toggled.connect(self.update_membership)

        self.ui.confirmButton.clicked.connect(self.checkout)

        self.ui.paymentCombo.addItems([
            "Naqd pul",
            "Bank karta",
            "Online to‘lov"
        ])


    # Bu funksiya savatchadan "cartWindow.py" olingan maxsulotlarni checkout listiga joylashtiradi
    def load_items(self, cart_items):
        table = self.ui.checkoutTable
        table.setRowCount(len(cart_items))

        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(
            ["Maxsulot", "Narx", "Miqdor", ""]
        )
        for row, item in enumerate(cart_items):
            table.setItem(row, 0, QTableWidgetItem(item["name"]))
            table.setItem(row, 1, QTableWidgetItem(f'{item["price"]} so`m'))
            table.setItem(row, 2, QTableWidgetItem(str(item["qty"])))
            table.setItem(
                row, 3,
                QTableWidgetItem(f'{item["price"] * item["qty"]} so`m')
            )
            self.total_price += item["price"]
    # Jami narx, soliq va chegirmani qo'shgan xolda umumiy narxni chiqaradi
    def update_total(self):
        table = self.ui.checkoutTable
        subtotal = 0

        for row in range(table.rowCount()):
            price = float(table.item(row, 1).text().replace("so`m", ""))
            qty = int(table.item(row, 2).text())
            subtotal += price * qty

        tax = subtotal * 0.08

        membership = self.get_selected_membership()

        discount_rate = MEMBERSHIPS[membership]["discount"]
        discount_amount = subtotal * discount_rate

        delivery_data = self.ui.deliveryCombo.currentData()
        delivery_type = delivery_data["type"]
        delivery_price = delivery_data["price"]
        if membership == "Gold" or membership == "Business":
            delivery_price = 0
        self.ui.deliveryPriceLabel.setText(f"{delivery_price:.2f} so`m")
        total = subtotal + tax + delivery_price - discount_amount

        self.ui.subtotalLabel.setText(f"{subtotal:.2f} so`m")
        self.ui.taxLabel.setText(f"{tax:.2f} so`m")
        self.ui.totalLabel.setText(f"{total:.2f} so`m")
    def calculate_total(self):
        self.update_total()

    def cancel(self):
        self.close()


    def get_selected_membership(self):

        # Bronza radio tugmani bosganda bronza medal rasm chiqishi
        if self.ui.bronzeButton.isChecked():
            self.ui.medal.setPixmap(QPixmap(f"images/bronze.png"))
            self.ui.medal.setScaledContents(True)
            self.ui.ballLabel.setText(f"+ {MEMBERSHIPS['Bronze']['point']} ball")
            return "Bronze"
        # Silver radio tugmani bosganda siler medal rasm chiqishi
        if self.ui.silverButton.isChecked():
            self.ui.medal.setPixmap(QPixmap(f"images/silver.png"))
            self.ui.medal.setScaledContents(True)
            self.ui.ballLabel.setText(f"+ {MEMBERSHIPS['Silver']['point']} ball")
            return "Silver"
        # Gold radio tugmani bosganda gold medal rasm chiqishi
        if self.ui.goldButton.isChecked():
            self.ui.medal.setPixmap(QPixmap(f"images/gold.png"))
            self.ui.medal.setScaledContents(True)
            self.ui.ballLabel.setText(f"+ {MEMBERSHIPS['Gold']['point']} ball")
            return "Gold"
        # Biznes radio tugmani bosganda platinium yani Biznes medal rasm chiqishi
        if self.ui.businessButton.isChecked():
            self.ui.medal.setPixmap(QPixmap(f"images/Business.png"))
            self.ui.medal.setScaledContents(True)
            self.ui.ballLabel.setText(f"+ {MEMBERSHIPS['Business']['point']} ball")
            return "Business"
        return "Bronze"
    def update_membership(self):
        membership = self.get_selected_membership()
        info = MEMBERSHIPS[membership]

        # Description chiqadi
        description = info["description"]
        self.ui.title.setText(description)


        # Total narxni qayta hisoblanadi
        self.calculate_total()

    # Foydalanuvchi Input labeldan kiritgan MALUMOTLARNI tekshiradi yani validation qismi
    def validate_checkout_inputs(self,cart_items):



            # Name validation
            name = self.ui.nameEdit.text().strip()
            if not name:
                QMessageBox.warning(self, "Error", "Iltimos Ismingizni to'liq kiriting")
                self.ui.nameEdit.setFocus()
                return False

            # Telefon raqam validation
            phone = self.ui.phoneEdit.text().strip()
            if not is_valid_phone(phone):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Telefon raqamda xatolik\nMasalan: +998901234567"
                )
                self.ui.phoneEdit.setFocus()
                return False

            # Address (agar delivery bo‘lsa)
            delivery = self.ui.deliveryCombo.currentText()
            address = self.ui.addressEdit.text().strip()

            if delivery == "Yetkazib berish" and not address:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Iltimos manzilni kiriting"
                )
                self.ui.addressEdit.setFocus()
                return False

            return True

    # Foydalanuvchi kiritgan malumotlari va xarid qilmoqchi bo'ldan narsalarni tasdiqlaydi va .json filega saqlaydi
    def checkout(self):
        # Cart itemlarni UI jadvaldan "cart_item" listga yig‘amiz SABABI KEYINGI OYNAGA O'TKANDA MA'LUMOTLARNI UZATISHDA VA
        #JSON FILEDA MALUMOTLARNI SAQLASHDA KERAK BO'LAI
        cart_items = []
        table = self.ui.checkoutTable

        for row in range(table.rowCount()):
            name = table.item(row, 0).text()
            price = float(table.item(row, 1).text().replace("so`m", ""))
            qty = int(table.item(row, 2).text())

            cart_items.append({
                "name": name,
                "price": price,
                "qty": qty
            })

        # Inputni tekshiramiz ya'ni validation qismi
        if not self.validate_checkout_inputs(cart_items):
            return

        # Total narxni labeldan olamiz
        total = float(self.ui.totalLabel.text().replace("so`m", ""))

        # Customer ma’lumotlari
        customer_data = {
            "name": self.ui.nameEdit.text().strip(),
            "phone": self.ui.phoneEdit.text().strip(),
            "address": self.ui.addressEdit.text().strip(),
            "membership": self.get_selected_membership()
        }

        # STOCKNI JSON’DA KAMAYTIRISH
        from mainwindow import load_products_data, save_products_data
        data = load_products_data()
        products = data["products"]

        for cart_item in cart_items:
            for p in products:
                if p["name"] == cart_item["name"]:
                    if p["stock"] < cart_item["qty"]:
                        QMessageBox.warning(
                            self,
                            "Stock error",
                            f'{p["name"]} ga yetarli zaxira mavjud emas '
                        )
                        return

                    p["stock"] -= cart_item["qty"]

        save_products_data(data)

        # Receiptni reciept.json ga saqlash
        payment_type = self.ui.paymentCombo.currentText()
        if not payment_type:
            QMessageBox.warning(self, "Error", "Iltimos to‘lov turini tanlang")
            return
        customer_data["payment_type"] = payment_type
        delivery_data = self.ui.deliveryCombo.currentData()
        delivery_type = delivery_data["type"]
        delivery_price = delivery_data["price"]
        membership = self.get_selected_membership()
        if membership == "Gold" or membership == "Business":
            delivery_price = 0
        if membership == "Bronze":
            bal = 1
        elif membership == "Silver":
            bal = 4
        elif membership == "Gold":
            bal = 6
        elif membership == "Business":
            bal = 8

        add_receipt(customer_data, cart_items, total, delivery_type,delivery_price, bal)
        # Receipt oynani ochish
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        payment_type = customer_data["payment_type"]
        self.receipt_window = ReceiptWindow(cart_items, customer_data, total,date, delivery_type,
        delivery_price,bal, payment_type)
        self.receipt_window.show()

        # Cart tozalash + MainWindow refresh
        if self.parent() and hasattr(self.parent(), "load_products"):
            self.parent().load_products()

        # Checkout oynani yopish
        self.close()



