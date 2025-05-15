import pandas as pd

# from
# https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.WP.list.v04r01.csv

# Load the data
cols = ["SID", "NAME", "SEASON", "ISO_TIME", "LAT", "LON", "TOKYO_WIND"]
df = pd.read_csv("ibtracs.WP.list.v04r01.csv", usecols=cols)
df.drop(df.index[0], inplace=True)  # Drop the first row (header row)

# Drop NAs and convert types
df = df.dropna(subset=["LAT", "LON", "ISO_TIME", "SEASON", "TOKYO_WIND"])
df["SEASON"] = df["SEASON"].astype(int)  # Convert SEASON to int

# Filter out typhoons with fewer than 10 points and < 1980
counts = df["SID"].value_counts()
valid_sids = counts[counts >= 10].index
df = df[df["SID"].isin(valid_sids)]
df = df[df["SEASON"] >= 1980]

# Save
df.to_csv("typhoons_wp_clean.csv", index=False)