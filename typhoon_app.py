import streamlit as st
import pandas as pd

st.title(f"Typhoon track viewer")

# load data
df = pd.read_csv("typhoons_wp_clean.csv")

# Select year
years = sorted(df["SEASON"].unique(), reverse=True)
year = st.selectbox("Select Year", years)
df_year = df[df["SEASON"] == year]

# select typhoon
typhoons = sorted(df_year["NAME"].unique())
typhoon = [st.selectbox("Select typhoon", typhoons)]

# Filter for selected names
df_selected = df_year[df_year["NAME"].isin(typhoon)]

# Display
st.map(df_selected[["LAT", "LON"]])

