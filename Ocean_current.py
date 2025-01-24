import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load data
@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)

# Load the data
data_file = 'sadcp_grid15moa.csv.gz'
data = load_csv(data_file)

# Map time periods to seasons
key_season = {
    0: "Climatology",
    13: "Winter (Dec-Feb)",
    14: "Spring (Mar-May)",
    15: "Summer (Jun-Aug)",
    16: "Autumn (Sep-Nov)",
    17: "Northeast monsoon months (Oct-Apr)",
    18: "Southwest monsoon months (May-Sep)"
}

# Sidebar for filters
st.sidebar.header("View Options")
depth_options = sorted(data["depth(m)"].unique())
time_period_options = sorted(data["time_period"].unique())

# Map time periods to their corresponding season names
season_options = [key_season[tp] for tp in time_period_options]
selected_depth = st.sidebar.selectbox("Select Depth (m):", depth_options)
selected_season = st.sidebar.selectbox("Select Season:", season_options)

# Get the corresponding time period for the selected season
selected_time = [tp for tp, season in key_season.items() if season == selected_season][0]

# Filter data
filtered_data = data[
    (data["depth(m)"] == selected_depth) & 
    (data["time_period"] == selected_time)
]

# Extract data for plotting
lon = filtered_data["longitude(deg.)"].values
lat = filtered_data["latitude(deg.)"].values
u = filtered_data["u_avg(m/s)"].values
v = filtered_data["v_avg(m/s)"].values

# Define fixed map region
map_extent = [117, 125, 18, 27]  # [lon_min, lon_max, lat_min, lat_max]

# Create map with PlateCarree projection
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(7, 7))

# Set extent to the fixed region
ax.set_extent(map_extent, crs=ccrs.PlateCarree())

# Add map features
ax.add_feature(cfeature.OCEAN, facecolor="lightblue")
ax.add_feature(cfeature.COASTLINE, edgecolor="black")

# Plot vector field
quiver = ax.quiver(lon, lat, u, v, transform=ccrs.PlateCarree(), scale=20, 
    color='black')

# Add longitude and latitude labels
ax.set_xticks([i for i in range(map_extent[0], map_extent[1] + 1, 2)], crs=ccrs.PlateCarree())
ax.set_yticks([i for i in range(map_extent[2], map_extent[3] + 1, 2)], crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}°E"))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}°N"))
ax.tick_params(labelsize=14)

# Add a legend for vector magnitudes
ax.quiverkey(quiver, X=0.1, Y=0.9, U=1, label='1 m/s', labelpos='E')

# Add title
ax.set_title(f"Daily drifting trajectory at {selected_depth} m depth\n{selected_season}", 
    fontsize=18)

# Show plot in app
st.pyplot(fig)

st.write("Data from [Ocean Data Bank, National Science and Technology Council](https://www.odb.ntu.edu.tw/adcp/display/traj/), which can be downloaded from [here](https://www.odb.ntu.edu.tw/adcp/adcp15moa/)")
