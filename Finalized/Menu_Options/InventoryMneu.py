from Utilites.MenuCRUD import menu_add_item,menu_low_stock,menu_remove_item,menu_save_load,menu_update_quantity,menu_view_inventory
from Utilites.Display import _section, _pause

def inventory_menu(inventory):
    options = {
        "1": ("View all items", menu_view_inventory),
        "2": ("Add item", menu_add_item),
        "3": ("Remove item", menu_remove_item),
        "4": ("Update quantity", menu_update_quantity),
        "5": ("Low-stock report", menu_low_stock),
        "6": ("Save / Load inventory", menu_save_load),
    }
    while True:
        _section("INVENTORY MENU")
        for k, (label, _) in options.items():
            print(f"  {k}. {label}") #this just print out the menu and add '.' after each number so it looks clean
        print("  0. Back")
        choice = input("\n  Choice: ").strip()
        if choice == "0":
            break
        #if the choice is in the option then run and pass the inventory into the fucntion
        elif choice in options: 
            options[choice][1](inventory) 
            _pause()
        else:
            print("  Invalid option.")