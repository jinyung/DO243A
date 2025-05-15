import streamlit as st
import pandas as pd
import pydeck as pdk
from pydeck.data_utils import compute_view

st.title("Typhoon track viewer")

@st.cache_data
def load_data():
    df = pd.read_csv("typhoons_wp_clean.csv")
    df["TOKYO_WIND"] = pd.to_numeric(df["TOKYO_WIND"], errors="coerce")
    return df

df = load_data()

# Select year 
years = sorted(df["SEASON"].unique(), reverse=True)
year = st.selectbox("Select Year", years)
df_year = df[df["SEASON"] == year]

# Select typhoon(s)
typhoons = sorted(df_year["NAME"].unique())

def expand_select_all():
    if "Select all" in st.session_state.typhoon:
        st.session_state.typhoon = typhoons

selected = st.multiselect(
    "Select Typhoon(s)", 
    ["Select all"] + typhoons, 
    default=typhoons[:1],
    key="typhoon",
    on_change=expand_select_all
)

if not selected:
    st.error("Please select at least one typhoon.")
    st.stop()

df_sel = df_year[df_year["NAME"].isin(selected)].copy()

# CWB classification
def classify(w):
    if pd.isna(w): 
        return "Unknown"
    w = w * 0.51444  # Convert to m/s
    if w < 17.2: 
        return "Tropical Depression"
    elif w <= 32.6:
        return "Mild Typhoon"
    elif w <= 50.9: 
        return "Moderate Typhoon"
    else: 
        return "Severe Typhoon"

df_sel["CLASS"] = df_sel["TOKYO_WIND"].apply(classify)

# Color by class
color_map = {
    "Severe Typhoon": [255, 0, 0],         # 🔴 red
    "Moderate Typhoon": [255, 215, 0],     # 🟡 yellow
    "Mild Typhoon": [0, 200, 100],         # 🟢 green
    "Tropical Depression": [0, 120, 255],  # 🔵 blue
    "Unknown": [150, 150, 150],            # ⚪ grey
}

df_sel["color"] = df_sel["CLASS"].map(color_map)

# Tooltip
df_sel["tooltip"] = (
    df_sel["NAME"] + " (" + df_sel["CLASS"] + ")" + "\n" + df_sel["ISO_TIME"]
)

# Scatterplot layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_sel,
    get_position="[LON, LAT]",
    get_fill_color="color",
    radius_min_pixels=4,
    radius_max_pixels=4,
    pickable=True,
)

# Compute view based on data and show map
view = compute_view(df_sel[["LON", "LAT"]])  
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, 
                         tooltip={"text": "{tooltip}"}))

# Explanation
st.markdown("### 🌀 CWB Typhoon Classification")
st.markdown("""
| Label | Category             | Wind Speed (m/s)   |
|:-----:|----------------------|--------------------|
| 🔴     | Severe Typhoon       | ≥ 51.0             |
| 🟡     | Moderate Typhoon     | 32.7 - 50.9        |
| 🟢     | Mild Typhoon         | 17.2 - 32.6        |
| 🔵     | Tropical Depression  | < 17.2             |
| ⚪     | Unknown              | —                  |
""")
