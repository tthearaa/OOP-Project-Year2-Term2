import getpass
from Finalized.Utilites.Auth import default_admin, login, register_user, change_password
from Utilites.Display import _banner

def auth_menu():
    while True:
        _banner()
        print("  1. Login")
        print("  2. Register new admin")
        print("  0. Exit")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            username = input("  Username : ").strip()
            password = getpass.getpass("  Password : ")
            session  = login(username, password)
            if session:
                return session

        elif choice == "2":
            username = input("  New username : ").strip()
            password = getpass.getpass("  Password     : ")
            register_user(username, password)

        elif choice == "0":
            return None
        else:
            print("  Invalid option.")