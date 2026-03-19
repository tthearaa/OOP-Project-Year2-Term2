import os
import csv
import datetime

#----------------------------------------------------------------------#

LOG_FILE = "Data/event_log.csv"

def log_event(action , detail):
    try:
      file_exists = os.path.isfile(LOG_FILE)
      with open(LOG_FILE, "a") as f:
        writer = csv.writer(f)
        if not file_exists:
          writer.writerow(["timestamp", "action", "detail"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),action, detail])
    except IOError as e:
        print(f"Error has occured!")

#-------------------------------------------------------------------------#

SALES_LOG_FILE = "Data/sales_log.csv"

def log_sale(transaction_id, item_name, amount, date, payment_method, rating, qty_sold):
    os.makedirs("Data", exist_ok=True)
    if not os.path.isfile(SALES_LOG_FILE):
        with open(SALES_LOG_FILE, "w", newline="") as f:
            csv.writer(f).writerow(
                ["transaction_id", "item_name", "amount", "date", "payment_method", "rating", "qty_sold"]
            )
    with open(SALES_LOG_FILE, "a", newline="") as f:
        csv.writer(f).writerow(
            [transaction_id, item_name, f"{amount:.2f}", date, payment_method, rating if rating else "", qty_sold]
        )