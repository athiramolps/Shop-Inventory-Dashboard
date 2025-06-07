import streamlit as st
import pandas as pd

# Set page layout
st.set_page_config(page_title="RefilliqTrack", layout="wide")

# --- Title Section ---
st.markdown("""
    <div style="margin-top:-10px;">
        <h1 style="color:#1976D2; margin-bottom:0;">RefilliqTrack</h1>
        <h4 style="margin-top:0; color:gray;">Track. Refill. Stay Ahead.</h4>
        <p><b>Location:</b> Springfield Groceries, 45 High Street, London</p>
    </div>
""", unsafe_allow_html=True)

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

# Determine status
def get_status(row):
    if row["Remaining"] <= 0:
        return "Out of Stock"
    elif row["Remaining"] <= 5:
        return "Low Stock"
    else:
        return "Sufficient"
df["Status"] = df.apply(get_status, axis=1)

# --- KPI Cards ---
total = len(df)
sufficient = len(df[df['Status'] == 'Sufficient'])
low = len(df[df['Status'] == 'Low Stock'])
out = len(df[df['Status'] == 'Out of Stock'])

st.markdown("### 🧮 Inventory Overview")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"### 🛒<br><sub>Total Products</sub><br><h2>{total}</h2>", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"### ✅<br><sub>Well-Stocked</sub><br><h2>{sufficient}</h2>", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"### ⚠️<br><sub>Low Stock</sub><br><h2>{low}</h2>", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"### ❌<br><sub>Out of Stock</sub><br><h2>{out}</h2>", unsafe_allow_html=True)

# --- Filter ---
status_option = st.selectbox("🔍 Filter by status:", ["All", "Sufficient", "Low Stock", "Out of Stock"])
filtered_df = df if status_option == "All" else df[df["Status"] == status_option]

# Add emoji to status
def emoji_label(status):
    return {
        "Sufficient": "🟢 Sufficient",
        "Low Stock": "🟡 Low Stock",
        "Out of Stock": "🔴 Out of Stock"
    }.get(status, status)

filtered_df["Status"] = filtered_df["Status"].apply(emoji_label)

# --- Display Table ---
st.markdown("### 📦 Product Inventory Table")
st.dataframe(filtered_df, use_container_width=True)
