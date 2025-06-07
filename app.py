import streamlit as st
import pandas as pd
from PIL import Image

# --- Page Config ---
st.set_page_config(page_title="RefilliqTrack", layout="centered")

# --- Load Logo ---
logo = Image.open("r2.png")  # Use your own logo filename here

# --- Top Header Layout ---
col_logo, col_title = st.columns([0.15, 0.85])
with col_logo:
    st.image(logo, width=60)
with col_title:
    st.markdown(
        """
        <div style="margin-top:-10px">
            <h1 style="color:#1E88E5; margin-bottom:0;">RefilliqTrack</h1>
            <h4 style="color:gray; margin-top:0;">Track. Refill. Stay Ahead.</h4>
            <p><b>Location:</b> Springfield Groceries, 45 High Street, London</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Sample Inventory Data ---
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

# --- Status Function ---
def get_status(row):
    if row["Remaining"] <= 0:
        return "Out of Stock"
    elif row["Remaining"] <= 5:
        return "Low Stock"
    else:
        return "Sufficient"
df["Status"] = df.apply(get_status, axis=1)

# --- KPI Section with Icons ---
total_products = len(df)
well_stocked = (df["Status"] == "Sufficient").sum()
low_stock = (df["Status"] == "Low Stock").sum()
out_of_stock = (df["Status"] == "Out of Stock").sum()

st.markdown("### 📊 Inventory Summary")
k1, k2, k3, k4 = st.columns(4)
k1.metric("🛒 Total Products", total_products)
k2.metric("✅ Well-Stocked", well_stocked)
k3.metric("⚠️ Low Stock", low_stock)
k4.metric("❌ Out of Stock", out_of_stock)

# --- Filter Dropdown ---
status_filter = st.selectbox("🔎 Filter by status:", ["All", "Sufficient", "Low Stock", "Out of Stock"])
if status_filter != "All":
    df_filtered = df[df["Status"] == status_filter]
else:
    df_filtered = df

# --- Add Emojis to Status ---
def status_emoji(status):
    if status == "Sufficient":
        return "🟢 Sufficient"
    elif status == "Low Stock":
        return "🟡 Low Stock"
    else:
        return "🔴 Out of Stock"
df_filtered["Status"] = df_filtered["Status"].apply(status_emoji)

# --- Table ---
st.markdown("### 📦 Product Inventory Table")
st.dataframe(df_filtered, use_container_width=True)
