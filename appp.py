import streamlit as st
import pandas as pd

# ----------------------------
# Simulated Weekly Data
# ----------------------------
data = {
    "Product": ["Biscuit", "Milk Bottle", "Sugar", "Tea Powder"],
    "Target": [30, 50, 40, 20],
    "Sold": [26, 49, 22, 20]
}
df = pd.DataFrame(data)
df["Remaining"] = df["Target"] - df["Sold"]

# Determine stock status
def get_status(row):
    if row["Remaining"] <= 0:
        return "Out of Stock"
    elif row["Remaining"] <= 5:
        return "Low Stock"
    else:
        return "Sufficient"

df["Status"] = df.apply(get_status, axis=1)

# ----------------------------
# Sidebar / Header
# ----------------------------
st.set_page_config(page_title="Shop Inventory Dashboard", layout="centered")

# Title and Shop Info
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("https://img.icons8.com/emoji/48/apple-emoji.png", width=40)
with col2:
    st.markdown("## **Shop Inventory Dashboard**\n123 Market St., Springfield")

# ----------------------------
# KPI Section
# ----------------------------
total_products = len(df)
well_stocked = (df["Status"] == "Sufficient").sum()
low_stock = (df["Status"] == "Low Stock").sum()
out_of_stock = (df["Status"] == "Out of Stock").sum()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Products Monitored", total_products)
kpi2.metric("Well-Stocked", well_stocked)
kpi3.metric("Low Stock", low_stock)
kpi4.metric("Out of Stock", out_of_stock)

# ----------------------------
# Filter Section
# ----------------------------
status_filter = st.selectbox(
    "Filter by status:",
    options=["All", "Sufficient", "Low Stock", "Out of Stock"],
    index=0
)

if status_filter != "All":
    df_filtered = df[df["Status"] == status_filter]
else:
    df_filtered = df

# ----------------------------
# Table Display with Emojis
# ----------------------------
def status_emoji(status):
    if status == "Sufficient":
        return "🟢 Sufficient"
    elif status == "Low Stock":
        return "🟡 Low Stock"
    else:
        return "🔴 Out of Stock"

df_filtered["Status"] = df_filtered["Status"].apply(status_emoji)
st.markdown("### 📦 Product Inventory Table")
st.dataframe(df_filtered, use_container_width=True)
