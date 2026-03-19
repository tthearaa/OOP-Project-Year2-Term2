import os
from datetime import datetime
import pandas as pd
from Utilites.Util_Log import log_sale, SALES_LOG_FILE
#Constants
DATASET_PATH   = "Data/Fashion_Retail_Sales.csv"


def process_sale(inventory, item_id, qty, payment_method: str = "Cash", rating: float | None = None):
    item = inventory.get_item(item_id)
    if item is None:
        print(f"  Sale failed: item '{item_id}' not found in inventory.")
        return False
    if item.quantity < qty:
        print(f"  Sale failed: only {item.quantity} units of '{item.name}' in stock "
              f"(requested {qty}).")
        return False
    revenue     = item.price * qty
    date_str    = datetime.now().strftime("%Y-%m-%d")
    txn_id      = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    inventory.update_quantity(item_id, -qty)
    log_sale(txn_id, item.name, revenue, date_str,
             payment_method, rating, qty)
    print(f"  Sale recorded: {qty}x '{item.name}' for ${revenue:,.2f}  [{txn_id}]")
    if item.quantity == 0:
        print(f"  ⚠  '{item.name}' is now OUT OF STOCK.")
    return True

# ── SalesAnalysis class ────────────────────────────────────────────────────────

class SalesAnalysis:
 
    COL_CUSTOMER   = "Customer Reference ID"
    COL_ITEM       = "Item Purchased"
    COL_AMOUNT     = "Purchase Amount (USD)"
    COL_DATE       = "Date Purchase"
    COL_PAYMENT    = "Payment Method"
    COL_RATING     = "Review Rating"

    def __init__(self, filepath: str = DATASET_PATH):
        self._filepath = filepath
        self._df: pd.DataFrame = pd.DataFrame()
        self._loaded = False

    # ── loading ────────────────────────────────────────────────────────────────

    def load(self) -> bool:
        """Load and clean the CSV. Returns True on success."""
        if not os.path.isfile(self._filepath):
            print(f"  Dataset not found: {self._filepath}")
            return False
        try:
            df = pd.read_csv(self._filepath)

            # Normalise column names (strip extra spaces)
            df.columns = df.columns.str.strip()

            # Parse date column if present
            if self.COL_DATE in df.columns:
                df[self.COL_DATE] = pd.to_datetime(df[self.COL_DATE], errors="coerce")

            # Coerce numeric columns
            if self.COL_AMOUNT in df.columns:
                df[self.COL_AMOUNT] = pd.to_numeric(df[self.COL_AMOUNT], errors="coerce")
            if self.COL_RATING in df.columns:
                df[self.COL_RATING] = pd.to_numeric(df[self.COL_RATING], errors="coerce")

            df.dropna(subset=[self.COL_AMOUNT], inplace=True)
            self._df     = df
            self._loaded = True
            print(f"  Dataset loaded: {len(df):,} transactions from {self._filepath}")
            return True
        except Exception as e:
            print(f"  Failed to load dataset: {e}")
            return False

    def _check_loaded(self) -> bool:
        if not self._loaded:
            print("  No data loaded. Call .load() first.")
        return self._loaded

    # ── overall summary ────────────────────────────────────────────────────────

    def summary(self):
        """Print high-level statistics."""
        if not self._check_loaded():
            return
        df = self._df
        total_rev  = df[self.COL_AMOUNT].sum()
        avg_rev    = df[self.COL_AMOUNT].mean()
        num_txn    = len(df)
        date_range = ""
        if self.COL_DATE in df.columns:
            mn = df[self.COL_DATE].min()
            mx = df[self.COL_DATE].max()
            date_range = f"  Date range   : {mn.date()} → {mx.date()}\n"

        print("\n" + "═" * 48)
        print("  SALES SUMMARY")
        print("═" * 48)
        print(f"  Transactions : {num_txn:,}")
        print(f"  Total revenue: ${total_rev:,.2f}")
        print(f"  Avg per sale : ${avg_rev:,.2f}")
        if date_range:
            print(date_range, end="")
        if self.COL_RATING in df.columns:
            avg_r = df[self.COL_RATING].mean()
            print(f"  Avg rating   : {avg_r:.2f} ⭐")
        print("═" * 48 + "\n")

    # ── top sellers ───────────────────────────────────────────────────────────

    def top_items_by_revenue(self, n: int = 10):
        """Show the n best-selling items by total revenue."""
        if not self._check_loaded():
            return
        if self.COL_ITEM not in self._df.columns:
            print("  Item column not found in dataset.")
            return
        grouped = (
            self._df.groupby(self.COL_ITEM)[self.COL_AMOUNT]
            .agg(total_revenue="sum", transactions="count")
            .sort_values("total_revenue", ascending=False)
            .head(n)
        )
        print(f"\n  TOP {n} ITEMS BY REVENUE")
        print("  " + "-" * 44)
        for rank, (item, row) in enumerate(grouped.iterrows(), 1):
            print(f"  {rank:2}. {item:<25} ${row['total_revenue']:>10,.2f}"
                  f"   ({row['transactions']} txns)")
        print()

    def top_items_by_frequency(self, n: int = 10):
        """Show the n most frequently purchased items."""
        if not self._check_loaded():
            return
        if self.COL_ITEM not in self._df.columns:
            print("  Item column not found in dataset.")
            return
        counts = (
            self._df[self.COL_ITEM].value_counts().head(n)
        )
        print(f"\n  TOP {n} ITEMS BY PURCHASE COUNT")
        print("  " + "-" * 36)
        for rank, (item, cnt) in enumerate(counts.items(), 1):
            print(f"  {rank:2}. {item:<25} {cnt:>6} purchases")
        print()

    def payment_breakdown(self):
        """Revenue and count split by payment method."""
        if not self._check_loaded():
            return
        if self.COL_PAYMENT not in self._df.columns:
            print("  Payment column not found.")
            return
        grouped = (
            self._df.groupby(self.COL_PAYMENT)[self.COL_AMOUNT]
            .agg(total="sum", count="count")
            .sort_values("total", ascending=False)
        )
        total_all = grouped["total"].sum()
        print("\n  PAYMENT METHOD BREAKDOWN")
        print("  " + "-" * 52)
        for method, row in grouped.iterrows():
            pct = (row["total"] / total_all) * 100
            print(f"  {method:<20} ${row['total']:>10,.2f}  "
                  f"{row['count']:>5} txns  ({pct:.1f}%)")
        print()

    # ── rating analysis ────────────────────────────────────────────────────────

    def rating_analysis(self):
        """Distribution and per-item average rating."""
        if not self._check_loaded():
            return
        if self.COL_RATING not in self._df.columns:
            print("  Rating column not found.")
            return
        df = self._df.dropna(subset=[self.COL_RATING])
        print("\n  RATING DISTRIBUTION")
        print("  " + "-" * 36)
        dist = df[self.COL_RATING].value_counts().sort_index(ascending=False)
        for star, cnt in dist.items():
            bar = "█" * int(cnt / max(dist) * 20)
            print(f"  {star:.1f}⭐  {bar:<20}  {cnt:,}")

        if self.COL_ITEM in df.columns:
            print("\n  AVERAGE RATING PER ITEM (top 10)")
            print("  " + "-" * 40)
            top = (
                df.groupby(self.COL_ITEM)[self.COL_RATING]
                .mean()
                .sort_values(ascending=False)
                .head(10)
            )
            for item, avg in top.items():
                print(f"  {item:<25}  {avg:.2f} ⭐")
        print()

    # ── monthly trend ─────────────────────────────────────────────────────────

    def monthly_revenue(self):
        """Print monthly revenue totals."""
        if not self._check_loaded():
            return
        if self.COL_DATE not in self._df.columns:
            print("  Date column not found.")
            return
        df = self._df.dropna(subset=[self.COL_DATE]).copy()
        df["month"] = df[self.COL_DATE].dt.to_period("M")
        monthly = (
            df.groupby("month")[self.COL_AMOUNT]
            .sum()
            .sort_index()
        )
        max_val = monthly.max()
        print("\n  MONTHLY REVENUE TREND")
        print("  " + "-" * 44)
        for period, rev in monthly.items():
            bar = "█" * int((rev / max_val) * 30)
            print(f"  {str(period):<10}  {bar:<30}  ${rev:,.2f}")
        print()

    # ── sales log analysis ────────────────────────────────────────────────────

    def load_sales_log(self) -> bool:
        """Switch to live sales_log.csv instead of the dataset."""
        return self.load.__func__(
            SalesAnalysis(SALES_LOG_FILE), # create temp obj to reuse load logic
        ) if False else self._load_log()

    def _load_log(self):
        try:
            df = pd.read_csv(SALES_LOG_FILE)
            df.columns = df.columns.str.strip()
            df["amount"]  = pd.to_numeric(df["amount"],  errors="coerce")
            df["qty_sold"]= pd.to_numeric(df["qty_sold"],errors="coerce")
            df["date"]    = pd.to_datetime(df["date"],   errors="coerce")
            df.dropna(subset=["amount"], inplace=True)

            # Map to standard column names for shared methods
            df = df.rename(columns={
                "item_name":      self.COL_ITEM,
                "amount":         self.COL_AMOUNT,
                "date":           self.COL_DATE,
                "payment_method": self.COL_PAYMENT,
                "rating":         self.COL_RATING,
            })
            self._df     = df
            self._loaded = True
            print(f"  Sales log loaded: {len(df):,} recorded sales.")
            return True
        except Exception as e:
            print(f"  Failed to load sales log: {e}")
            return False

    def export_summary_csv(self, out_path: str = "Data/analysis_summary.csv"):
        if not self._check_loaded():
            return
        if self.COL_ITEM not in self._df.columns:
            print("  Item column not found.")
            return
        grouped = (
            self._df.groupby(self.COL_ITEM)[self.COL_AMOUNT]
            .agg(total_revenue="sum", transactions="count")
            .sort_values("total_revenue", ascending=False)
            .reset_index()
        )
        grouped.to_csv(out_path, index=False)
        print(f"  Summary exported to {out_path}")
