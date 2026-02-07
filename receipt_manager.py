import json
import os
from datetime import datetime

RECEIPT_FILE = "data/recipes.json"

def load_receipts():
    if not os.path.exists(RECEIPT_FILE):
        return {"receipts": []}
    with open(RECEIPT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_receipts(data):
    with open(RECEIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_receipt(customer, items, total,delivery_type,delivery_price,bal,):
    data = load_receipts()

    new_id = len(data["receipts"]) + 1

    data["receipts"].append({
        "id": new_id,
        "customer": customer,
        "items": items,
        "total": total,
        "payment_type": customer["payment_type"],
        "delivery_type":delivery_type,
        "delivery_price":delivery_price,
        "point":bal,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    save_receipts(data)
