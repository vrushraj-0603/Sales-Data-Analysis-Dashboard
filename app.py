import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# Page Configuration
# ==========================
st.set_page_config(page_title="Sales Data Analysis Dashboard", layout="wide")

st.title("📊 Sales Data Analysis Dashboard")

uploaded_file = st.file_uploader(
    "Upload Sample - Superstore.csv",
    type=["csv"]
)

if uploaded_file is not None:

    # Load Dataset
    df = pd.read_csv(uploaded_file, encoding="Windows-1252")

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Required Columns
    required_columns = [
        "Order ID",
        "Order Date",
        "Ship Date",
        "Category",
        "Region",
        "Sales",
        "Profit",
        "Quantity",
        "Segment",
        "Product Name"
    ]

    # Check Missing Columns
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error("Required columns are missing.")
        st.write("Columns found in file:")
        st.write(df.columns.tolist())
        st.stop()

    # ==========================
    # Data Cleaning
    # ==========================
    df = df.drop_duplicates()

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    # Remove invalid dates
    df = df.dropna(subset=["Order Date"])

    # ==========================
    # Dataset Preview
    # ==========================
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ==========================
    # KPI Cards
    # ==========================
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    total_quantity = df["Quantity"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Sales", f"${total_sales:,.2f}")
    c2.metric("Total Profit", f"${total_profit:,.2f}")
    c3.metric("Total Orders", total_orders)
    c4.metric("Total Quantity", int(total_quantity))

    # ==========================
    # Sales by Category
    # ==========================
    st.subheader("Sales by Category")

    category_sales = df.groupby("Category")["Sales"].sum()

    fig, ax = plt.subplots(figsize=(7,4))
    category_sales.plot(kind="bar", ax=ax)
    ax.set_ylabel("Sales")
    st.pyplot(fig)

    # ==========================
    # Profit by Region
    # ==========================
    st.subheader("Profit by Region")

    region_profit = df.groupby("Region")["Profit"].sum()

    fig, ax = plt.subplots(figsize=(7,4))
    region_profit.plot(kind="bar", ax=ax)
    ax.set_ylabel("Profit")
    st.pyplot(fig)

    # ==========================
    # Monthly Sales Trend
    # ==========================
    st.subheader("Monthly Sales Trend")

    monthly = df.copy()
    monthly["Month"] = monthly["Order Date"].dt.to_period("M")

    monthly_sales = monthly.groupby("Month")["Sales"].sum()

    fig, ax = plt.subplots(figsize=(10,4))
    monthly_sales.plot(kind="line", marker="o", ax=ax)
    ax.set_ylabel("Sales")
    st.pyplot(fig)

    # ==========================
    # Sales by Segment
    # ==========================
    st.subheader("Sales by Segment")

    segment_sales = df.groupby("Segment")["Sales"].sum()

    fig, ax = plt.subplots(figsize=(5,5))
    segment_sales.plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

    # ==========================
    # Top Products
    # ==========================
    st.subheader("Top 10 Products")

    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.dataframe(top_products.reset_index())

    # ==========================
    # Download Cleaned CSV
    # ==========================
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Cleaned CSV",
        csv,
        "cleaned_superstore.csv",
        "text/csv"
    )

else:
    st.info("Please upload 'Sample - Superstore.csv'.")