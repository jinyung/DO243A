import streamlit as st
import pandas as pd
import pydeck as pdk
from pydeck.data_utils import compute_view

st.title("Typhoon track viewer")

# CWB classification
def classify(w):
    if pd.isna(w): 
        return "Unknown"
    if w < 17.2: 
        return "Tropical Depression"
    elif w <= 32.6:
        return "Mild Typhoon"
    elif w <= 50.9: 
        return "Moderate Typhoon"
    else: 
        return "Severe Typhoon"

# load data        
@st.cache_data
def load_data():
    df = pd.read_csv("typhoons_wp_clean.csv")
    df["TOKYO_WIND"] = pd.to_numeric(df["TOKYO_WIND"], errors="coerce")
    df["WIND_MS"] = (df["TOKYO_WIND"] * 0.51444).round(1)  # Convert to m/s
    df["CLASS"] = df["WIND_MS"].apply(classify)
    return df

df = load_data()

# create a dataframe of typhoon tracks with max wind speed and category
tracks_df = (
    df.groupby(["SEASON","SID", "NAME"])["WIND_MS"]
    .max()
    .dropna()
    .reset_index()
    .rename(columns={"SEASON": "Year", "WIND_MS": "Max Wind (m/s)"})
)
tracks_df["Category"] = tracks_df["Max Wind (m/s)"].apply(classify)

# select year
st.sidebar.write("### Choose range of years")
years = sorted(tracks_df["Year"].unique())
year_start, year_end = st.sidebar.select_slider(
    "Select Year", years,
    value=(2020, 2024),
    key="select_year"
)
years_mask = tracks_df["Year"].between(year_start, year_end)

# select category
cats = sorted(tracks_df["Category"].unique(), reverse=True)
st.sidebar.write("### Choose typhoon category")
chosen = []
for label in cats:
    if st.sidebar.checkbox(label, value=True):
        chosen.append(label)
cats = chosen
cats_mask = tracks_df["Category"].isin(cats)

selected_df = tracks_df[years_mask & cats_mask].sort_values(["Year", "Max Wind (m/s)"], ascending=False)

# Explanation
st.sidebar.markdown("""
### CWB Typhoon Classification
            
| Label | Category             | Wind Speed (m/s)   |
|:-----:|----------------------|--------------------|
| 🔴     | Severe Typhoon       | ≥ 51.0             |
| 🟡     | Moderate Typhoon     | 32.7 - 50.9        |
| 🟢     | Mild Typhoon         | 17.2 - 32.6        |
| 🔵     | Tropical Depression  | < 17.2             |
| ⚪     | Unknown              | —                  |
      
Data source: IBTrACS (Version 4r01): [doi:10.25921/82ty-9e16](https://doi.org/10.25921/82ty-9e16)
"""
)

map = st.container()

# display the filtered dataframe (search results)
st.write(f"""### Search results
There are {len(selected_df)} typhoons in {year_start}-{year_end} with the selected category.

Please select typhoon(s) to view on map:""")
selection_event = st.dataframe(
    selected_df,
    column_order=("Year", "NAME", "Category","Max Wind (m/s)"),
    hide_index = True,
    on_select="rerun",
    selection_mode="multi-row",
    use_container_width=True, 
    height=200
)

# select from the filtered dataframe
selected_rows = selection_event.get("selection", {}).get("rows") if selection_event else []
if selected_rows:
    selected_sid = selected_df.iloc[selected_rows, :]["SID"]
    df_sel = df[df["SID"].isin(selected_sid)]
else:
    st.error("Please select at least one typhoon from the search results")
    st.stop()

# preparing data for map
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
map.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, 
                        tooltip={"text": "{tooltip}"}))