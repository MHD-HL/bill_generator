from DBOps import DataBaseManager
from datetime import datetime
import simplePDF

db_path = "data/storage copy.db"
db = DataBaseManager(db_path)

class Bill:
    def __init__(self, customer_name: str, items: list[tuple], date: str = datetime.now().strftime("%Y-%m-%d")):
        self.customer_name = customer_name
        self.items = items
        self.date = date

    def get_prices(self):
        prices: dict = {}
        for item in self.items:
            name: str = item[0]
            if name.__contains__("Battery"):
                cap, ws = item[1], item[2]
                result = db.get_data("batteries", columns="price", condition=f"name='{name}' AND capacity={cap} AND working_system={ws}")
            elif name.__contains__("Inverter"):
                power = item[1]
                result = db.get_data("inverters", columns="price", condition=f"name='{name}' AND power={power}")
            else:
                wattage = item[1]
                result = db.get_data("solar_panels", columns="price", condition=f"name='{name}' AND wattage={wattage}")
            prices.update({item: result[0][0]})
        return prices

    def items_with_prices(self):
        description: str
        bill_items: list[tuple[str, int, float]] = []
        prices = self.get_prices()
        for item, price in prices.items():
            name: str = item[0]
            if name.__contains__("Battery"):
                cap, ws, qty = item[1], item[2], item[3]
                description = f"{name} {cap}Ah/{ws}V"
            elif name.__contains__("Inverter"):
                power, qty = item[1], item[2]
                description = f"{name} {power}W"
            else:
                wattage, qty = item[1], item[2]
                description = f"{name} {wattage}W"
            bill_items.append((description, qty, price))
        return bill_items

    def insert_bill(self):
        items = self.items_with_prices()
        db.insert_data("bills", [{"customer_name": self.customer_name, "date": self.date, "total_amount": sum([qty * price for _, qty, price in items])}])
    
    def generate_bill(self):
        self.insert_bill()
        bill_num = db.get_data("bills", "id", f"customer_name='{self.customer_name}' AND date='{self.date}'")
        items = self.items_with_prices()
        simplePDF.create_custom_bill(self.customer_name, items, bill_num[0][0], f"{self.customer_name} Bill.pdf")
