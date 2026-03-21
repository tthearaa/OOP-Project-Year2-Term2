import getpass
from Classes.Inventory import Inventory
from Utilites.Auth import default_admin, register_user, change_password
from Utilites.Display import _banner, _pause
from Menu_Options.Authentication_Menu import auth_menu
from Menu_Options.InventoryMneu import inventory_menu
from Menu_Options.SalesAnalysisMenu import sales_menu
import maskpass
def main():
    
    default_admin()

    inventory = Inventory()
    inventory.load_from_csv()

    session = auth_menu()
    if session is None:
        print("  Goodbye!")
        return

    while True:
        #show header 👗  ARV Studios INVENTORY & SALES SYSTEM  👗
        _banner()
        #get admin username from login(username, password) inside session
        print(f"  Logged in as: {session['username']}  [admin]")
        print()
        print("  1. Inventory management")
        print("  2. Sales & analysis")
        print("  3. Register new admin")
        print("  4. Change my password")
        print("  0. Logout / Exit")

        choice = input("\n  Choice: ").strip()

        if   choice == "1": inventory_menu(inventory)
        elif choice == "2": sales_menu(inventory)
        elif choice == "3":
            username = input("  New username : ").strip()
            password = maskpass.askpass(prompt="  Password     : ", mask="*")
            #update new admin's username and password into users.csv
            register_user(username, password)
            _pause()
        elif choice == "4":
            old = maskpass.askpass(prompt="  Current password : ", mask="*")
            new = maskpass.askpass(prompt="  New password     : ", mask="*")
            change_password(session["username"], old, new)
            _pause()
        elif choice == "0":
            inventory.save_to_csv()
            print(f"\n  Goodbye, {session['username']}!")
            break
        else:
            print("  Invalid option.")

if __name__ == "__main__":
    main()
