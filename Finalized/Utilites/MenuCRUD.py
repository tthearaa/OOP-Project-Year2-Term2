from Classes.ClothingItemClass import ClothingItem, PremiumItem
from Utilites.Display import _banner, _section

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
    is_premium = input("  Premium item? (y/n): ").strip().lower() == "y"
    if is_premium:
        brand = input("  Brand            : ").strip()
        item  = PremiumItem(item_id, name, price, quantity, brand)
    else:
        item = ClothingItem(item_id, name, price, quantity)
    inventory.add_item(item)

def menu_remove_item(inventory):
    _section("REMOVE ITEM")
    item_id = input("  Item ID to remove: ").strip()
    inventory.remove_item(item_id)

def menu_update_quantity(inventory):
    _section("UPDATE QUANTITY")
    item_id = input("  Item ID              : ").strip()
    try:
        amount = int(input("  Quantity change (+/-): ").strip())
    except ValueError:
        print("  Invalid number.")
        return
    inventory.update_quantity(item_id, amount)

def menu_view_inventory(inventory):
    _section("ALL INVENTORY ITEMS")
    inventory.display_all()
    print(f"\n  Total items in inventory: {len(inventory)}")

def menu_low_stock(inventory):
    _section("LOW STOCK REPORT")
    low = inventory.low_stock_report()
    if not low:
        print("  No items below the low-stock threshold.")
    else:
        print(f"  {len(low)} item(s) running low:\n")
        for item in low:
            print(f"    {item}")

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
