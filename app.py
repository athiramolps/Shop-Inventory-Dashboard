import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# --------------------------
# PAGE CONFIG & STYLES
# --------------------------
st.set_page_config(page_title="RefilliqTrack", layout="centered")

# Light/Dark mode toggle
theme = st.toggle("🌗 Dark Mode", value=False)

if theme:
    bg_color = "#0e1117"
    text_color = "#fafafa"
    kpi_bg = "#1c1f26"
else:
    bg_color = "#ffffff"
    text_color = "#333333"
    kpi_bg = "#f1f3f6"

st.markdown(f"""
    <style>
        .main {{
            background-color: {bg_color};
            color: {text_color};
        }}
        h1, h4, p {{
            color: {text_color};
        }}
        .kpi-card {{
            background-color: {kpi_bg};
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .footer-note {{
            text-align: center;
            color: #777;
            font-size: 12px;
            margin-top: 2rem;
        }}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# HEADER: Logo + Title
# --------------------------
col1, col2 = st.columns([0.15, 0.85])
with col1:
    logo = Image.open("logo.png")  # Make sure this exists in your app folder
    st.image(logo, width=60)
with col2:
    st.markdown("""
        <h1 style='color:#1E88E5;'>RefilliqTrack</h1>
        <h4>Track. Refill. Stay Ahead.</h4>
        <p><b>Location:</b> Springfield Groceries, 45 High Street, London</p>
    """, unsafe_allow_html=True)

st.markdown("---")

# --------------------------
# DATASET
# --------------------------
data = {
    "Product": [
        "Parle-G Biscuits", "Amul Milk", "Tata Salt", "Red Label Tea",
        "Nestle Powder", "Maggi Noodles", "Sunfeast Marie", 
        "Fortune Oil", "Colgate Paste", "Bru Coffee"
    ],
    "Target": [30, 50, 40, 20, 25, 35, 30, 20, 25, 15],
    "Sold": [26, 49, 22, 20, 15, 34, 30, 17, 25, 15]
}
df = pd.DataFrame(data)
df["Remaining"] = df["Target"] - df["Sold"]

def get_status(row):
    if row["Remaining"] <= 0:
        return "🔴 Out of Stock"
    elif row["Remaining"] <= 5:
        return "🟡 Low Stock"
    else:
        return "🟢 Sufficient"

df["Status"] = df.apply(get_status, axis=1)

# --------------------------
# KPI SECTION
# --------------------------
total = len(df)
well = df["Status"].str.contains("Sufficient").sum()
low = df["Status"].str.contains("Low Stock").sum()
out = df["Status"].str.contains("Out of Stock").sum()

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"<div class='kpi-card'>🗂️<br><b>Total</b><br>{total}</div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='kpi-card'>🟢<br><b>Well-Stocked</b><br>{well}</div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='kpi-card'>🟡<br><b>Low Stock</b><br>{low}</div>", unsafe_allow_html=True)
with k4:
    st.markdown(f"<div class='kpi-card'>🔴<br><b>Out of Stock</b><br>{out}</div>", unsafe_allow_html=True)

st.markdown("---")

# --------------------------
# FILTER BY STATUS
# --------------------------
filter_option = st.selectbox("🔍 Filter products by stock level", ["All", "Sufficient", "Low Stock", "Out of Stock"])
emoji_map = {
    "Sufficient": "🟢 Sufficient",
    "Low Stock": "🟡 Low Stock",
    "Out of Stock": "🔴 Out of Stock"
}
df_filtered = df if filter_option == "All" else df[df["Status"] == emoji_map[filter_option]]

# --------------------------
# TABLE DISPLAY
# --------------------------
st.markdown("### 📦 Product Inventory Table")
st.dataframe(df_filtered, use_container_width=True)

# --------------------------
# PIE CHART
# --------------------------
st.markdown("### 📊 Stock Distribution")
stock_counts = [well, low, out]
labels = ["Sufficient", "Low Stock", "Out of Stock"]
colors = ["#4CAF50", "#FFC107", "#F44336"]

fig, ax = plt.subplots()
ax.pie(stock_counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax.axis("equal")
st.pyplot(fig)

# --------------------------
# EXPORT BUTTONS
# --------------------------
st.markdown("### ⬇️ Export Inventory")
col_csv, col_xlsx = st.columns(2)
with col_csv:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="inventory_data.csv", mime="text/csv")
with col_xlsx:
    import io
    from pandas import ExcelWriter
    output = io.BytesIO()
    with ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventory')
        writer.save()
    st.download_button("Download Excel", data=output.getvalue(), file_name="inventory_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# --------------------------
# FOOTER
# --------------------------
st.markdown("""
    <div class='footer-note'>
        NB: This project was developed under a real shop in Durham. Due to privacy concerns, the dataset and financials are not shown. All data here is for demonstration only.
    </div>
""", unsafe_allow_html=True)
