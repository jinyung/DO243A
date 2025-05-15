import streamlit as st
import pandas as pd
import pydeck as pdk
from pydeck.data_utils import compute_view

st.title("Typhoon track viewer")

# cache data loading
@st.cache_data
def load_data():
    df = pd.read_csv("typhoons_wp_clean.csv")
    return df

df = load_data()

# Select year
years = sorted(df["SEASON"].unique(), reverse=True)
year = st.selectbox("Select Year", years)
df_year = df[df["SEASON"] == year]

# Select typhoon(s)
typhoons = sorted(df_year["NAME"].unique())
selected = st.multiselect("Select Typhoon(s)", 
                          typhoons, default=typhoons[:1])

if not selected:
    st.error("Please select at least one typhoon.")
    st.stop()

df_sel = df_year[df_year["NAME"].isin(selected)].copy()

# Tooltip: typhoon name + timestamp
df_sel["tooltip"] = df_sel["NAME"] + "\n" + df_sel["ISO_TIME"]

# Scatterplot layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_sel,
    get_position="[LON, LAT]",
    get_fill_color=[0, 255, 0],
    radius_min_pixels=3,
    radius_max_pixels=3,
    pickable=True,
)

# Compute view based on data and show map
view = compute_view(df_sel[["LON", "LAT"]])
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, 
                         tooltip={"text": "{tooltip}"}))
