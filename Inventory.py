import os
import csv
from abc import ABC, abstractmethod
from datetime import datetime

#Constants
DATASET_PATH   = "Data/Fashion_Retail_Sales.csv"
INVENTORY_FILE = "Data/inventory.csv"
LOG_FILE       = "Data/event_log.csv"
LOW_STOCK_THRESHOLD = 5


def log_event(action , detail):
    try:
      file_exists = os.path.isfile(LOG_FILE)
      with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
          writer.writerow(["timestamp", "action", "detail"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),action, detail])
    except IOError as e:
        print(f"[LOG ERROR] Could not write to log: {e}")

class BaseItem(ABC):
  def __init__(self, item_id, name, price, quantity):
    self._item_id  = item_id
    self._name     = name
    self._price    = price
    self._quantity = quantity

  @property
  def item_id(self):   
    return self._item_id
  
  @property
  def name(self):      
      return self._name
  
  @property
  def price(self):     
      return self._price
  
  @price.setter
  def price(self, v):
    if v < 0:
      raise ValueError("Price cannot be negative.")
    self._price = v

  @property
  def quantity(self):  return self._quantity

  @quantity.setter
  def quantity(self, v):
    if v < 0:
      raise ValueError("Quantity cannot be negative.")
    self._quantity = v

  @abstractmethod
  def category(self):
      pass

  @abstractmethod
  def summary(self):
      pass

  def __str__(self):
    return (f"[{self._item_id}] {self._name} | "
            f"${self._price:.2f} | Qty: {self._quantity} | "
            f"Category: {self.category()}")

  def __repr__(self):
    return (f"{self.__class__.__name__}("
            f"id={self._item_id!r}, name={self._name!r}, "
            f"price={self._price}, qty={self._quantity})")

  def __eq__(self, other):
    if not isinstance(other, BaseItem):
      return NotImplemented
    return self._item_id == other._item_id

  def stock_value(self) -> float:
    return self._price * self._quantity


class ClothingItem(BaseItem):

  CLOTHING_CATEGORIES = {
    "tops"    : {"T-shirt","Tunic","Tank Top","Blouse","Camisole","Flannel Shirt","Polo Shirt","Hoodie","Sweater","Cardigan"},
    "bottoms" : {"Jeans","Trousers","Leggings","Shorts","Skirt","Pants","Overalls"},
    "dresses" : {"Dress","Romper","Jumpsuit","Onesie","Kimono","Pajamas"},
    "outerwear": {"Jacket","Coat","Trench Coat","Raincoat","Blazer","Vest","Poncho"},
    "footwear": {"Boots","Loafers","Slippers","Flip-Flops","Sneakers","Sandals"},
    "accessories": {"Handbag","Wallet","Belt","Scarf","Gloves","Bowtie","Tie","Hat","Sun Hat","Sunglasses","Umbrella","Backpack","Socks"},
    "swimwear": {"Swimsuit"},
    }

  def category(self):
    for cat, items in self.CLOTHING_CATEGORIES.items():
      if self._name in items:
        return cat.title()
    return "Other"

  def summary(self):
    return (f"{self._name} ({self.category()}) — "
            f"${self._price:.2f} x {self._quantity} units "
            f"= ${self.stock_value():,.2f} total value")

class PremiumItem(ClothingItem):
  SURCHARGE_RATE = 0.15
  def __init__(self, item_id, name, price, quantity, brand = "N/A"):
    super().__init__(item_id, name, price, quantity)
    self._brand = brand
  @property
  def brand(self): 
    return self._brand

  def category(self):
    return "Premium " + super().category()

  def summary(self):
    surcharge = self._price * self.SURCHARGE_RATE
    return (f"[PREMIUM] {self._brand} {self._name} — "
            f"${self._price:.2f} + ${surcharge:.2f} surcharge, "
            f"Qty: {self._quantity}")

  def final_price(self):
    return self._price * (1 + self.SURCHARGE_RATE)

class Inventory:
  def __init__(self):
    self._items: dict[str, BaseItem] = {}
    self._low_stock_ids: set = set()

  def __len__(self):
    return len(self._items)
  
  def __contains__(self, item_id):
    return item_id in self._items
    
  def __iter__(self):
    return iter(self._items.values())

  def __add__(self, other: "Inventory"):
    merged = Inventory()
    for item in self:
      merged.add_item(item)
    for item in other:
      if item.item_id not in merged:
        merged.add_item(item)
    return merged
  def add_item(self, item):
    try:
      if item.item_id in self._items:
        raise ValueError(f"Item ID '{item.item_id}' already exists.")
      self._items[item.item_id] = item
      self._check_low_stock(item)
      log_event("ADD", f"Added {item.name} (ID={item.item_id})")
    except ValueError as e:
        print(f"[ADD ERROR] {e}")

  def remove_item(self, item_id):
    try:
      item = self._items.pop(item_id)
      self._low_stock_ids.discard(item_id)
      log_event("REMOVE", f"Removed {item.name} (ID={item_id})")
    except KeyError:
      print(f"[REMOVE ERROR] Item ID '{item_id}' not found.")

  def update_quantity(self, item_id, addon):
   try:
    item = self._items[item_id]
    new_qty = item.quantity + addon
    if new_qty < 0:
      print("Quantity needs to be positive!")
      return
    item.quantity = new_qty
    self._check_low_stock(item)
    log_event("UPDATE_QTY",f"{item.name} qty changed by {addon:+d} → {new_qty}")
   except KeyError:
    print(f"[UPDATE ERROR] Item ID '{item_id}' not found.")
   except ValueError as e:
    print(f"[UPDATE ERROR] {e}")

  def get_item(self, item_id):
        try:
            return self._items[item_id]
        except KeyError:
            print(f"Item was not found")
            return None

  def _check_low_stock(self, item: BaseItem):
        if item.quantity <= LOW_STOCK_THRESHOLD:
            self._low_stock_ids.add(item.item_id)
        else:
            self._low_stock_ids.discard(item.item_id)

  def low_stock_report(self) -> list[BaseItem]:
        return [self._items[i] for i in self._low_stock_ids
                if i in self._items]

  def save_to_csv(self, filepath = INVENTORY_FILE):
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["item_id","name","price","quantity","type","brand"])
                for item in self:
                    t = "premium" if isinstance(item, PremiumItem) else "standard"
                    brand = item.brand if isinstance(item, PremiumItem) else ""
                    writer.writerow([item.item_id, item.name, item.price,
                                     item.quantity, t, brand])
            log_event("SAVE", f"Inventory saved to {filepath}")
            print(f"Inventory is saved to {filepath}")
        except IOError:
            print(f"There was an error")

  def load_from_csv(self, filepath: str = INVENTORY_FILE):
    try:
      with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
          try:
            iid  = row["item_id"]
            name = row["name"]
            price = float(row["price"])
            qty   = int(row["quantity"])
            if row["type"] == "premium":
              item = PremiumItem(iid, name, price, qty, brand=row.get("brand",""))
            else:
              item = ClothingItem(iid, name, price, qty)
              self.add_item(item)
          except (ValueError, KeyError) as e:
                print(f"No value detected. Skipping row {e}")
      log_event("LOAD", f"Inventory loaded from {filepath}")
      print(f"[LOAD] Inventory loaded from '{filepath}'.")
    except FileNotFoundError:
      print(f"{filepath} Not found!")

  def display_all(self):
    if not self._items:
      print("Inventory is Empty!")
      return
    for item in self:
      print(" ", item)

class SalesTransaction:
  def __init__(self, transaction_id, item_name, amount, date ,payment_method , rating: float | None = None):
    self._transaction_id  = transaction_id
    self._item_name       = item_name
    self._amount          = amount
    self._date            = date
    self._payment_method  = payment_method
    self._rating          = rating

  @property
  def transaction_id(self): 
    return self._transaction_id
  @property
  def item_name(self):    
    return self._item_name
  @property
  def amount(self):         
    return self._amount
  @property
  def date(self):           
    return self._date
  @property
  def payment_method(self):
    return self._payment_method
  @property
  def rating(self):         
    return self._rating
  def __str__(self):
    stars = f"{self._rating:.1f}⭐" if self._rating else "N/A"
    return (f"TXN {self._transaction_id} | {self._item_name} | "
            f"${self._amount:,.2f} | {self._date} | "
            f"{self._payment_method} | Rating: {stars}")
  
if __name__ == "__main__":
  #Object initialization
  shirt = ClothingItem("C001", "T-shirt", 19.99, 50)
  jeans = ClothingItem("C002", "Jeans", 49.99, 30)
  jacket = ClothingItem("C003", "Jacket", 89.99, 15)
  hat = ClothingItem("C004", "Baseball Cap", 14.99, 20)
  premium_shirt = PremiumItem("P001", "T-shirt", 89.99, 10, "Gucci")
  premium_jeans = PremiumItem("P002", "Jeans", 199.99, 5, "Armani")

  #Check the category function
  print(f"Shirt category: {shirt.category()}")  # Should be "Tops"
  print(f"Jeans category: {jeans.category()}")  # Should be "Bottoms"
  print(f"Jacket category: {jacket.category()}")  # Should be "Outerwear"
  print(f"Hat category: {hat.category()}")  # Should be "Other" (not in dictionary)
  print(f"Premium shirt category: {premium_shirt.category()}")  # Should be "Premium Tops"

  #Check summary
  print(f"\nShirt summary: {shirt.summary()}")
  print(f"Premium jeans summary: {premium_jeans.summary()}")
  print(f"Premium shirt final price: ${premium_shirt.final_price():.2f}") #Math subcharge testing

  #Inventory test
  inventory = Inventory()
  inventory2 = Inventory()  # For merge test later

  # Add items to first inventory
  inventory.add_item(shirt)
  inventory.add_item(jeans)
  inventory.add_item(jacket)
  inventory.add_item(premium_shirt)
  inventory.add_item(premium_jeans)
  inventory2.add_item(hat)
  inventory2.add_item(ClothingItem("C005", "Sneakers", 79.99, 25))

  #Check items
  print(f"\nInventory 1 size: {len(inventory)} items")
  print(f"Inventory 2 size: {len(inventory2)} items")

  #Display test
  print("\n👕 TEST 4: Display All Items")
  inventory.display_all()
  inventory2.display_all()