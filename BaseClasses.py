class ClothingItem:
    def __init__(self):
        print("You are adding a New item, Please Input its details")
        self.itemName = input("Input your Item Name: ")
        self.itemSize = input("Input the Item Size: ")
        self.itemColor = input("Input the Item Color: ")
        self.itemFabric = input("Input the Item Fabric: ")
        self.itemQuantity = int(input("Input the Quantity: "))
        self.price = float(input("Input the Price: $"))  
        print("✅ Item added successfully!")
    
    def display_info(self):
        print("\n Item's Info: ")
        print(f"Name: {self.itemName}")
        print(f"Size: {self.itemSize}")
        print(f"Color: {self.itemColor}")
        print(f"Fabric: {self.itemFabric}")
        print(f"Quantity: {self.itemQuantity}")
        print(f"Price: ${self.price}")
        print(f"Total Value: ${self.price * self.itemQuantity}")
    
    def ChangeCharacteristics(self):
        while True:
            print("\n🔧 CHANGE CHARACTERISTICS:")
            print("1. Item Name")
            print("2. Item Size")
            print("3. Item Color")
            print("4. Item Fabric")
            print("5. Item Quantity")
            print("6. Item Price")
            print("0. Exit")
            
            choice = input("\nChoose what characteristic to change (0-6): ")
            
            if choice == "1":
                new_value = input(f"Current Name '{self.itemName}'. Enter new name: ")
                self.itemName = new_value
                print("✅ Name updated!")
                
            elif choice == "2":
                new_value = input(f"Current Size '{self.itemSize}'. Enter new size: ")
                self.itemSize = new_value
                print("✅ Size updated!")
                
            elif choice == "3":
                new_value = input(f"Current Color '{self.itemColor}'. Enter new color: ")
                self.itemColor = new_value
                print("✅ Color updated!")
                
            elif choice == "4":
                new_value = input(f"Current Fabric '{self.itemFabric}'. Enter new fabric: ")
                self.itemFabric = new_value
                print("✅ Fabric updated!")
                
            elif choice == "5":
                new_value = int(input(f"Current Quantity '{self.itemQuantity}'. Enter new quantity: "))
                self.itemQuantity = new_value
                print("✅ Quantity updated!")
                
            elif choice == "6":
                new_value = float(input(f"Current Price '${self.price}'. Enter new price: $"))
                self.price = new_value
                print("✅ Price updated!")
                
            elif choice == "0":
                print("Exiting change menu...")
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def update_quantity(self, amount):
        self.itemQuantity += amount
        if amount > 0:
            print(f"✅ Added {amount} items. New quantity: {self.itemQuantity}")
        else:
            print(f"✅ Removed {abs(amount)} items. New quantity: {self.itemQuantity}")
