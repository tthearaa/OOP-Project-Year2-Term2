# Data Analysis and Stock Management of ARV Inventory using Python with Data Visualization

## A functional inventory tracker that records sales, logs actions and analyses your data

---

## Features
- User authentication with login and registration
- Inventory management (add, remove, update quantity)
- Sales recording with transaction IDs
- Sales analysis (revenue, top items, payment breakdown, ratings)
- Data visualization with charts saved to the Charts/ folder
- Event and authentication logging

---

## Project Structure
```
Project/
├── Data/
│   ├── Fashion_Retail_Sales.csv
│   ├── inventory.csv
│   ├── users.csv
│   ├── auth_log.csv
│   ├── event_log.csv
│   └── analysis_summary.csv
├── Charts/
├── Finalized/
│   ├── Main.py
│   ├── Classes/
│   │   ├── ClothingItemClass.py
│   │   ├── Inventory.py
│   │   ├── SalesAnalysis.py
│   │   └── SalesVisualization.py
│   ├── Menu_Options/
│   │   ├── Authentication_Menu.py
│   │   ├── InventoryMenu.py
│   │   └── SalesAnalysisMenu.py
│   └── Utilites/
│       ├── Auth.py
│       ├── Display.py
│       ├── MenuCRUD.py
│       └── Util_Log.py
```

---

## Requirements
- Python 3.10+
- pandas
- matplotlib

Install dependencies:
```
pip install pandas matplotlib
```

---

## How to Run
1. Navigate to the `Finalized/` folder
2. Run the main file:
```
python Main.py
```
3. Login with the default credentials:
   - Username: `admin`
   - Password: `admin123`
4. Change your password after first login

---

## Data Visualization
To generate charts, run:
```
python Classes/SalesVisualization.py
```
Charts will be saved to the `Project/Charts/` folder.

---

## Author
Heang Sovanntheara