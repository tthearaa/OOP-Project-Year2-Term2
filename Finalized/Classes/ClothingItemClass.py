from abc import ABC, abstractmethod
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
  def quantity(self):  
    return self._quantity

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

  def __eq__(self, other):
    if not isinstance(other, BaseItem):
      return NotImplemented
    return self._item_id == other._item_id

  def stock_value(self):
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
  PREMIUMEXTRA = 0.15
  def __init__(self, item_id, name, price, quantity, brand = "N/A"):
    super().__init__(item_id, name, price, quantity)
    self._brand = brand
  @property
  def brand(self): 
    return self._brand

  def category(self):
    return "Premium " + super().category()

  def summary(self):
    extra = self._price * self.PREMIUMEXTRA
    return (f"[PREMIUM] {self._brand} {self._name} — "
            f"${self._price:.2f} + ${extra:.2f} extra, "
            f"Qty: {self._quantity}")

  def final_price(self):
    return self._price * (1 + self.PREMIUMEXTRA)
  
if __name__ == "__main__":
  #Object Instaniation
  C1 =  ClothingItem("C01", "Shirt", 10, 10)
  #Getter Method Testing
  print(C1._item_id)
  print(C1._name)
  print(f"${C1._price}")
  print(C1._quantity, "items")
  #Test __str__
  print(C1)