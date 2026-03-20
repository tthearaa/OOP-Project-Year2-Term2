import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

#Paths 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "Data")
CHARTS_DIR = os.path.join(BASE_DIR, "Charts")
SALES_FILE   = os.path.join(DATA_DIR, "Fashion_Retail_Sales.csv")
SUMMARY_FILE = os.path.join(DATA_DIR, "analysis_summary.csv")
#Using pandas to read files
sales   = pd.read_csv(SALES_FILE)
summary = pd.read_csv(SUMMARY_FILE)

#normalization
sales.columns = sales.columns.str.strip()

# Parse dates
sales["Date Purchase"] = pd.to_datetime(sales["Date Purchase"], dayfirst=True, errors="coerce")
sales["Month"] = sales["Date Purchase"].dt.to_period("M")
print("Loaded Data")
 
def save(name):
    path = os.path.join(CHARTS_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved → {path}")


#Chart 1: Top 10 items
top10 = summary.nlargest(10, "total_revenue")

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(top10["Item Purchased"], top10["total_revenue"], color="#4a90d9", edgecolor="white")

ax.set_title("Top 10 Items by Total Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Revenue (USD)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.invert_yaxis()                   # highest on top
ax.bar_label(bars, fmt="$%.0f", padding=4, fontsize=8)
ax.spines[["top", "right"]].set_visible(False)

save("chart1_top10_revenue.png")


#Chart 2: transcation difference
payment_counts = sales["Payment Method"].value_counts()

fig, ax = plt.subplots(figsize=(6, 6))
wedge_props = dict(width=0.55, edgecolor="white")
ax.pie(
  payment_counts,
  labels=payment_counts.index,
  autopct="%1.1f%%",
  startangle=90,
  wedgeprops=wedge_props,
  colors=["#4a90d9", "#50c878"],
)
ax.set_title("Payment Method Distribution", fontsize=14, fontweight="bold")

save("chart2_payment_methods.png")


#Chart 3: Monthly revenue trend
monthly = (
  sales.dropna(subset=["Month"])
    .groupby("Month")["Purchase Amount (USD)"]
    .sum()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(monthly.index.astype(str), monthly.values, marker="o", color="#4a90d9", linewidth=2, markersize=5)
ax.fill_between(monthly.index.astype(str), monthly.values, alpha=0.15, color="#4a90d9")

ax.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.tick_params(axis="x", rotation=45)
ax.spines[["top", "right"]].set_visible(False)

save("chart3_monthly_trend.png")


#Chart 4: Customer rating
ratings = sales["Review Rating"].dropna()

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(ratings, bins=20, color="#50c878", edgecolor="white", linewidth=0.6)

ax.set_title("Customer Rating Distribution", fontsize=14, fontweight="bold")
ax.set_xlabel("Rating (1 - 5)")
ax.set_ylabel("Number of Reviews")
ax.spines[["top", "right"]].set_visible(False)

avg = ratings.mean()
ax.axvline(avg, color="#e74c3c", linestyle="--", linewidth=1.5, label=f"Average: {avg:.2f}")
ax.legend()

save("chart4_rating_distribution.png")

print("All charts are saved.")