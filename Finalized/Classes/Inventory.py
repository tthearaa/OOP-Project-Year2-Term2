import csv
from Classes.ClothingItemClass import PremiumItem, ClothingItem
from Utilites.Util_Log import log_event

#Constants
DATASET_PATH = "Data/Fashion_Retail_Sales.csv"
INVENTORY_FILE = "Data/inventory.csv"
LOG_FILE = "Data/event_log.csv"
LOW_STOCK_THRESHOLD = 5
#In this we will perform CRUD operation for items in the inventory 
class Inventory:
  def __init__(self):
    self._items = {}
    self._low_stock_ids = set()

  def __len__(self):
    return len(self._items) #get the amount of the items that we have in stock 
  
  def __contains__(self, item_id):
    return item_id in self._items 
    
  def __iter__(self):
    return iter(self._items.values())

  def __add__(self, other):
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
        print(f"Adding Error! {e}")
#This function will remove item by chekcing with id if the id doesn't exist then it will print error
  def remove_item(self, item_id):
    try:
      item = self._items.pop(item_id) #this will remove one row from inventory
      self._low_stock_ids.discard(item_id)
      log_event("REMOVE", f"Removed {item.name} (ID={item_id})")
    except KeyError:
      print(f"Remove Error! Item ID {item_id} not found.")

#This function will update the quantity of the item in the inventory 
  def update_quantity(self, item_id, addon):
   try:
    item = self._items[item_id] 
    new_qty = item.quantity + addon
    if new_qty < 0: #check if the new amount is wrong (can't be negative)
      print("Quantity needs to be positive!")
      return
    item.quantity = new_qty #update the new amount
    self._check_low_stock(item) #check if the stock is low 
    log_event("UPDATE_QTY",f"{item.name} qty changed to {new_qty}") #after update done
   except KeyError:
    print(f"Update error! Item ID {item_id} not found.") #enter the wrong/non-exist id
   except ValueError as e:
    print(f"Update Error! {e}") #show the error

  def get_item(self, item_id):
    try:
      return self._items[item_id]
    except KeyError:
      print(f"Item was not found")
      return
#this will check if the stock is low by comparing with LOW_STOCK_THRESHOLD = 5
  def _check_low_stock(self, item):
    if item.quantity <= LOW_STOCK_THRESHOLD: #if it's less then add to low stock report
      self._low_stock_ids.add(item.item_id)
    else:
      self._low_stock_ids.discard(item.item_id) #if no then remove it from low stock report
#this will return the items that are currently low in stock
  def low_stock_report(self):
    return [self._items[i] for i in self._low_stock_ids if i in self._items]
#save file to csv 
  def save_to_csv(self, filepath = INVENTORY_FILE):
    try:
      with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["item_id","name","price","quantity","type","brand"])
        for item in self:
          t = "premium" if isinstance(item, PremiumItem) else "standard"
          brand = item.brand if isinstance(item, PremiumItem) else "" 
          writer.writerow([item.item_id, item.name, item.price, item.quantity, t, brand])
        log_event("SAVE", f"Inventory saved to {filepath}")
        print(f"Inventory saved to {filepath}")
    except IOError:
      print(f"There was an error")
#load data from csv 
  def load_from_csv(self, filepath = INVENTORY_FILE):
    try:
      with open(filepath, newline="") as f:
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
      print(f"Success! Inventory loaded from {filepath}.")
    except FileNotFoundError:
      print(f"{filepath} Not found!")
#check if the inventory is empty or not then display
  def display_all(self):
    if not self._items:
      print("Inventory is Empty!")
      return
    for item in self:
      print(" ", item)

class SalesTransaction:
  def __init__(self, transaction_id, item_name, amount, date ,payment_method , rating: float | None = None):
    self._transaction_id = transaction_id
    self._item_name = item_name
    self._amount = amount
    self._date = date
    self._payment_method = payment_method
    self._rating = rating

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
  print(f"Shirt category: {shirt.category()}")
  print(f"Jeans category: {jeans.category()}")
  print(f"Jacket category: {jacket.category()}")
  print(f"Hat category: {hat.category()}")
  print(f"Premium shirt category: {premium_shirt.category()}")

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
  print("\nDisplay All Items")
  inventory.display_all()
  inventory2.display_all()

  # Test magic method
  print("\n--- Testing Magic Methods ---")
  print(f"Length of inventory: {len(inventory)}")  # __len__
  print(f"Is 'C001' in inventory? {'C001' in inventory}")  # __contains__
  print(f"Is 'A001' in inventory? {'A001' in inventory}")  # __contains__
  print("\nIterating through inventory:")
  for item in inventory:  # __iter__
    print(f"  - {item.item_id}: {item.name}")

  item = inventory.get_item("C001")
  print(f"Got item: {item}")
  item = inventory.get_item("INVALID")
  print(f"Got invalid item: {item}")

  