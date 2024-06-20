import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px
import streamlit as st
import pathlib as pl
import spacy
from icecream import ic

plt.style.use('ggplot')
ic.configureOutput(includeContext=True)
pio.renderers.default='browser'

### Functions
def load_data(path: pl.Path | str, compression: None | str = None) -> pd.DataFrame:
    path = pl.Path(path)
    if compression is not None:
        return pd.read_csv(path, compression=compression)
    else:
        return pd.read_csv(path)

### setup

# TODO: los Angeles
listings_dir = pl.Path(r"data\cities\finished")
listings_files = list()
for item in listings_dir.iterdir():
    if (item.is_file()) and (item.suffix == ".csv") and ("_spacy" not in item.stem):
        listings_files.append(item.stem)
    

### Streamlit
string = """
    # What are the most popular listings?
"""
st.markdown(string)

## sidebar for filteroptions
city_filter_selectbox = st.sidebar.selectbox(
    "Select a city",
    listings_files
)

listings_path = listings_dir / f"{city_filter_selectbox}.csv"
listings = load_data(listings_path, compression=None)
listings = listings.dropna(subset="neighbourhood_cleansed", how="any")

nh_filter_selectbox = st.sidebar.selectbox(
    "Select a neighbourhood",
    (None, *listings["neighbourhood_cleansed"].unique())
)

ranking_cut_off = st.sidebar.select_slider(
    "Select the n-th most pupular listings",
    options= np.arange(1, 11)
)


col1, col2, col3 = st.columns(3)

string = """
    ### Selected city
"""
col1.markdown(string)
col1.write(city_filter_selectbox)

string = """
    ### Selected neighbourhood
"""
col2.markdown(string)
col2.write(nh_filter_selectbox)

string = """
    ### n-th most popular
"""
col3.markdown(string)
col3.write(ranking_cut_off)


## overview of listings
string = """
    ### Overview
"""
st.markdown(string)
map_df = listings[["id", "latitude", "longitude", "room_type", "price_$", "review_scores_rating", "neighbourhood_cleansed"]]
if nh_filter_selectbox is not None:
    map_df = map_df[map_df["neighbourhood_cleansed"] == nh_filter_selectbox]

st.map(data=map_df, use_container_width=True, size=1, zoom=10)

## ranking
ranking_df = map_df.sort_values(by="review_scores_rating")
st.write(listings)
# ranking_df = listings[[]]


# fig = px.density_mapbox(
#         data_frame=map_df,
#         lat="latitude",
#         lon="longitude",
#         z="price_$",
#         radius=10,
#         center=dict(lat=map_df["latitude"].mean(), lon=map_df["longitude"].mean()),
#         zoom=10,
#         mapbox_style="open-street-map",
#         color_continuous_scale="inferno"
#     )
# st.plotly_chart(fig, use_container_width=True)