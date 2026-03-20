from Classes.ClothingItemClass import ClothingItem, PremiumItem
from Utilites.Display import _banner, _section
#This function will add new item into inventory.csv
def menu_add_item(inventory):
    _section("ADD ITEM")
    item_id = input("  Item ID          : ").strip()
    name    = input("  Name             : ").strip()
    try:
        price = float(input("  Price ($)        : ").strip())
        quantity = int(input("  Quantity         : ").strip())
    except ValueError:
        print("  Invalid price or quantity.")
        return
    #check if the item is the premium type or normal type
    is_premium = input("  Premium item? (y/n): ").strip().lower() == "y"
    if is_premium:
        brand = input("  Brand            : ").strip()
        item  = PremiumItem(item_id, name, price, quantity, brand)
    else:
        item = ClothingItem(item_id, name, price, quantity)
    inventory.add_item(item)
#This function will remove item from the inventory by taking item's id
def menu_remove_item(inventory):
    _section("REMOVE ITEM")
    item_id = input("  Item ID to remove: ").strip()
    inventory.remove_item(item_id)
#this function will update the amount of the items that we have based on id
def menu_update_quantity(inventory):
    _section("UPDATE QUANTITY")
    item_id = input("  Item ID              : ").strip()
    try:
        amount = int(input("  Quantity change (+/-): ").strip())
    except ValueError:
        print("  Invalid number.")
        return
    inventory.update_quantity(item_id, amount)
#view all the items we added 
def menu_view_inventory(inventory):
    _section("ALL INVENTORY ITEMS")
    inventory.display_all() #if the inventory is empty then display notification (Inventory is Empty!)
    print(f"\n  Total items in inventory: {len(inventory)}")
#this will show the low stock report 
def menu_low_stock(inventory):
    _section("LOW STOCK REPORT")
    low = inventory.low_stock_report() #bring the low stock items in
    if not low: #see if there's no low stock report it return nothing
        print("  No items below the low-stock threshold.")
    else: #is there is, then show the amount of the item 
        print(f"  {len(low)} item(s) running low:\n")
        for item in low: # then dislay the item 
            print(f"    {item}")
#this will perform save to csv / load from csv
def menu_save_load(inventory):
    _section("SAVE / LOAD INVENTORY")
    print("  1. Save inventory to CSV")
    print("  2. Load inventory from CSV")
    choice = input("  Choice: ").strip()
    if choice == "1":
        inventory.save_to_csv()
    elif choice == "2":
        inventory.load_from_csv()
    else:
        print("  Invalid option.")

if __name__ == "__main__":
    pass