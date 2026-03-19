from Utilites.Display import _section, _pause
from Finalized.Classes.SalesAnalysis import SalesAnalysis, process_sale

def menu_record_sale(inventory):
    _section("RECORD SALE")
    item_id = input("  Item ID          : ").strip()
    try:
        qty = int(input("  Quantity sold    : ").strip())
    except ValueError:
        print("  Invalid quantity.")
        return
    print("  Payment methods: Cash / Credit Card / Debit Card / PayPal")
    payment    = input("  Payment method   : ").strip() or "Cash"
    rating_str = input("  Customer rating (1-5, or blank): ").strip()
    rating     = float(rating_str) if rating_str else None
    process_sale(inventory, item_id, qty, payment, rating)

def menu_analysis():
    analysis = SalesAnalysis()
    print("\n  Load which data?")
    print("  1. Main retail dataset (Fashion_Retail_Sales.csv)")
    print("  2. Live sales log      (sales_log.csv)")
    src = input("  Choice: ").strip()

    loaded = analysis._load_log() if src == "2" else analysis.load()
    if not loaded:
        return

    while True:
        _section("SALES ANALYSIS")
        print("  1. Summary statistics")
        print("  2. Top items by revenue")
        print("  3. Top items by frequency")
        print("  4. Payment method breakdown")
        print("  5. Rating analysis")
        print("  6. Monthly revenue trend")
        print("  7. Export summary to CSV")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()

        if   choice == "1": analysis.summary()
        elif choice == "2":
            n = input("  How many top items? [10]: ").strip()
            analysis.top_items_by_revenue(int(n) if n.isdigit() else 10)
        elif choice == "3":
            n = input("  How many top items? [10]: ").strip()
            analysis.top_items_by_frequency(int(n) if n.isdigit() else 10)
        elif choice == "4": analysis.payment_breakdown()
        elif choice == "5": analysis.rating_analysis()
        elif choice == "6": analysis.monthly_revenue()
        elif choice == "7": analysis.export_summary_csv()
        elif choice == "0": break
        else: print("  Invalid option.")
        if choice != "0":
            _pause()

def sales_menu(inventory):
    while True:
        _section("SALES MENU")
        print("  1. Record a sale")
        print("  2. View sales analysis")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()
        if   choice == "0": break
        elif choice == "1": menu_record_sale(inventory); _pause()
        elif choice == "2": menu_analysis();             _pause()
        else: print("  Invalid option.")