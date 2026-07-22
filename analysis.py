import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# 1. Load Dataset
# =====================================
df = pd.read_csv("Sample - Superstore.csv", encoding="Windows-1252")

print("=" * 50)
print("FIRST 5 ROWS")
print("=" * 50)
print(df.head())

print("\nDATASET INFORMATION")
print(df.info())

print("\nDATASET SHAPE:", df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

# =====================================
# 2. Data Cleaning
# =====================================

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE ROWS:", df.duplicated().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# Convert date columns
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

print("\nDATA TYPES")
print(df.dtypes)

# =====================================
# 3. Key Business Metrics
# =====================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
total_orders = df["Order ID"].nunique()

print("\n" + "=" * 50)
print("KEY METRICS")
print("=" * 50)

print(f"Total Sales     : {total_sales:.2f}")
print(f"Total Profit    : {total_profit:.2f}")
print(f"Total Quantity  : {total_quantity}")
print(f"Total Orders    : {total_orders}")

# =====================================
# 4. Category Analysis
# =====================================

category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

print("\nSALES BY CATEGORY")
print(category_sales)

# =====================================
# 5. Region Analysis
# =====================================

region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)

print("\nPROFIT BY REGION")
print(region_profit)

# =====================================
# 6. Top Products
# =====================================

top_products = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\nTOP 10 PRODUCTS")
print(top_products)

# =====================================
# 7. Segment Analysis
# =====================================

segment_sales = df.groupby("Segment")["Sales"].sum()

print("\nSALES BY SEGMENT")
print(segment_sales)

# =====================================
# 8. Monthly & Yearly Trend
# =====================================

df["Month"] = df["Order Date"].dt.to_period("M")
monthly_sales = df.groupby("Month")["Sales"].sum()

df["Year"] = df["Order Date"].dt.year
yearly_sales = df.groupby("Year")["Sales"].sum()

# =====================================
# 9. Business Insights
# =====================================

print("\n" + "=" * 50)
print("BUSINESS INSIGHTS")
print("=" * 50)

print("Highest Sales Category :", category_sales.idxmax())
print("Highest Profit Region  :", region_profit.idxmax())
print("Top Selling Product    :", top_products.idxmax())
print("Best Customer Segment  :", segment_sales.idxmax())

# =====================================
# 10. Visualizations
# =====================================

# Sales by Category
plt.figure(figsize=(8,5))
category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Profit by Region
plt.figure(figsize=(8,5))
region_profit.plot(kind="bar")
plt.title("Profit by Region")
plt.xlabel("Region")
plt.ylabel("Profit")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Monthly Sales Trend
plt.figure(figsize=(10,5))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.tight_layout()
plt.show()

# Yearly Sales Trend
plt.figure(figsize=(7,5))
yearly_sales.plot(kind="line", marker="o")
plt.title("Yearly Sales Trend")
plt.xlabel("Year")
plt.ylabel("Sales")
plt.grid(True)
plt.tight_layout()
plt.show()

# Sales by Segment
plt.figure(figsize=(6,6))
segment_sales.plot(kind="pie", autopct="%1.1f%%")
plt.title("Sales by Segment")
plt.ylabel("")
plt.tight_layout()
plt.show()

# =====================================
# 11. Export Clean Dataset
# =====================================

df = df.drop(columns=["Month", "Year"])

df.to_csv(
    "cleaned_superstore.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\ncleaned_superstore.csv created successfully!")
print("\nPROJECT COMPLETED SUCCESSFULLY!")