from Utilites.Auth import login, register_user
from Utilites.Display import _banner
import maskpass
#This function perform the login and sign-up for the admin
def auth_menu():
    while True:
        _banner() #show the header and title
        print("  1. Login")
        print("  2. Register new admin")
        print("  0. Exit")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            username = input("  Username : ").strip()
            #mask the text with * so it won't exspose the actual password
            password = maskpass.askpass(prompt="  Password : ", mask="*") 
            session  = login(username, password) 
            # this will decide whether the password/username that user try to get into admin acc is correct or not
            #if its true (correct) return the value
            if session:
                return session
            
        elif choice == "2":
            #this will take new username and new password and input that it the resgister_user
            username = input("  New username : ").strip()
            # password = maskpass.askpass(prompt="  Password     : ",mask="*")
            password = input("  Password     : ").strip()
            register_user(username, password)

        elif choice == "0":
            return None
        else:
            print("  Invalid option.")