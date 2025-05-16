import streamlit as st
import pandas as pd
import plotly.express as px

# set page wider
st.set_page_config(layout = "wide")

# move title to sidebar
st.sidebar.title("Typhoon track viewer")

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
    df["Wind (m/s)"] = (df["TOKYO_WIND"] * 0.51444).round(1)  # Convert to m/s
    df["Category"] = df["Wind (m/s)"].apply(classify)
    return df

df = load_data()

# create a dataframe of typhoon tracks with max wind speed and category
tracks_df = (
    df.groupby(["SEASON","SID", "NAME"])["Wind (m/s)"]
    .max()
    .dropna()
    .reset_index()
    .rename(columns={"SEASON": "Year", 
                     "ISO_TIME": "Time",
                     "NAME": "Typhoon name",
                     "Wind (m/s)": "Max Wind (m/s)"})
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
            
| Label | Category             | Wind (m/s)   |
|:-----:|----------------------|--------------------|
| 🔴     | Severe Typhoon       | ≥ 51.0             |
| 🟡     | Moderate Typhoon     | 32.7 - 50.9        |
| 🟢     | Mild Typhoon         | 17.2 - 32.6        |
| 🔵     | Tropical Depression  | < 17.2             |
| ⚪     | Unknown              | —                  |
      
Data source: IBTrACS (Version 4r01): [doi:10.25921/82ty-9e16](https://doi.org/10.25921/82ty-9e16)
"""
)

col1, col2 = st.columns([1, 2])
col1.write(f"""### Search results            
There are **{len(selected_df)}** typhoons in **{year_start}-{year_end}** with the selected category.
Please select typhoon(s) to view on map:""")

with col1:
    # display the filtered dataframe (search results)
    selection_event = st.dataframe(
        selected_df,
        column_order=("Year", "Typhoon name", "Category","Max Wind (m/s)"),
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
        # container for track details    
        with st.expander("Selected track details", expanded=False):
            for sid in selected_sid:
                st.dataframe(
                    df_sel[df_sel["SID"] == sid]
                    .drop(columns=["SEASON", "SID", "TOKYO_WIND"]), 
                    hide_index=True, height=150)
    else:
        st.error("Please select at least one typhoon from the search results")
        # create an empty default dataframe to display empty map
        df_sel = pd.DataFrame(columns=df.columns)
        df_sel["LAT"] = [24]
        df_sel["LON"] = [121]
      

# Plotly map instead of PyDeck 
# build the scatter_map figure
with col2:
    fig = px.scatter_map(
        df_sel,
        lat="LAT",
        lon="LON",
        color="Category",
        color_discrete_map={
            "Severe Typhoon":     "red",
            "Moderate Typhoon":   "gold",
            "Mild Typhoon":       "green",
            "Tropical Depression":"blue",
            "Unknown":            "gray",
        },
        hover_name="NAME",
        hover_data={"Category": True, "ISO_TIME": True},
        height=800,
        zoom=4,                           # will be overridden below
        center=dict(
            lat=df_sel["LAT"].mean(),
            lon=df_sel["LON"].mean()
        )
    )

    fig.update_layout(
        map_style="carto-darkmatter" ,
        showlegend =False,
    )

    st.plotly_chart(fig, use_container_width=True)