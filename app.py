import streamlit as st
import pandas as pd
from PIL import Image

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="RefilliqTrack Dashboard", layout="centered")

# ----------------------------
# Header with Logo and Title
# ----------------------------
# Load logo
logo = Image.open("logo.png")

# Display logo and title in same row
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 10px;">
        <img src="logo.png" width="50">
        <div>
            <h1 style="margin: 0; color:#1E88E5;">RefilliqTrack</h1>
            <h4 style="margin: 0; color:gray;">Track. Refill. Stay Ahead.</h4>
            <p style="margin: 0;"><b>Location:</b> Springfield Groceries, 45 High Street, London</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Simulated Weekly Data (10 Products)
# ----------------------------
data = {
    "Product": [
        "Parle-G Biscuits", "Amul Full Cream Milk", "Tata Salt", "Red Label Tea",
        "Nestle Everyday Milk Powder", "Maggi Noodles", "Sunfeast Marie Light",
        "Fortune Soya Oil", "Colgate Toothpaste", "Bru Instant Coffee"
    ],
    "Target": [30, 50, 40, 20, 25, 35, 30, 20, 25, 15],
    "Sold": [26, 49, 22, 20, 15, 34, 30, 17, 25, 15]
}
df = pd.DataFrame(data)
df["Remaining"] = df["Target"] - df["Sold"]

def get_status(row):
    if row["Remaining"] <= 0:
        return "Out of Stock"
    elif row["Remaining"] <= 5:
        return "Low Stock"
    else:
        return "Sufficient"
df["Status"] = df.apply(get_status, axis=1)

# ----------------------------
# KPI Section with Icons
# ----------------------------
total_products = len(df)
well_stocked = (df["Status"] == "Sufficient").sum()
low_stock = (df["Status"] == "Low Stock").sum()
out_of_stock = (df["Status"] == "Out of Stock").sum()

st.markdown("### 📊 Weekly Stock Summary")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("📦 Total", total_products)
kpi2.metric("✅ Sufficient", well_stocked)
kpi3.metric("⚠️ Low Stock", low_stock)
kpi4.metric("❌ Out of Stock", out_of_stock)

# ----------------------------
# Filter Section
# ----------------------------
status_filter = st.selectbox(
    "🔍 Filter by Stock Status:",
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
