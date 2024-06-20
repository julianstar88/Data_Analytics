# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:06:29 2024

@author: Tung
"""

import os
import pandas as pd
import streamlit as st
import pathlib as pl

# Set the working directory to the script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))
listings_dir = pl.Path(r"../data/cities/finished")

# Get the list of available cities from the filenames
cities = []
for item in listings_dir.iterdir():
    if item.is_file() and (item.suffix in [".csv", ".gz"]) and ("_spacy" not in item.stem):
        city_name = item.stem.replace('listings_', '').replace('_finished', '').replace('.csv', '')
        cities.append(city_name)

# Streamlit dashboard
st.title("Top 10 Airbnb Hosts in Selected City")

# City selection
selected_city = st.selectbox("Select a city:", sorted(cities))

# Load the data for the selected city
selected_file_csv = listings_dir / f"listings_{selected_city}_finished.csv"
selected_file_gz = listings_dir / f"listings_{selected_city}_finished.csv.gz"

if selected_file_csv.exists():
    df_listings_finished = pd.read_csv(selected_file_csv)
elif selected_file_gz.exists():
    df_listings_finished = pd.read_csv(selected_file_gz, compression='gzip')
else:
    st.error(f"No data file found for {selected_city}")
    st.stop()

# Define a function to get the top hosts for a given neighbourhood
def get_top_hosts(df, neighbourhood, min_reviews, only_superhosts, top_n=10):
    # Filter the dataframe for the selected neighbourhood
    if neighbourhood != 'All':
        df = df[df['neighbourhood_cleansed'] == neighbourhood]
        
    # Filter the dataframe for minimum number of reviews
    df = df[df['number_of_reviews'] >= min_reviews]
    
    # Filter only Superhosts if the option is selected
    if only_superhosts:
        df = df[df['host_is_superhost'] == 't']
    
    # Aggregate data at the host level
    host_stats = df.groupby('host_id').agg({
        'review_scores_rating': 'mean',
        'number_of_reviews': 'sum',
        'host_is_superhost': 'first',
        'host_listings_count': 'first'
    }).reset_index()
    
    # Sort by average rating and number of reviews
    host_stats = host_stats.sort_values(by=['review_scores_rating', 'number_of_reviews'], ascending=False)
    
    # Add a ranking column
    host_stats['Ranking'] = range(1, len(host_stats) + 1)
    
    return host_stats.head(top_n), len(df)

# Get a list of unique neighbourhoods and sort them alphabetically
neighbourhoods = ['All'] + sorted(df_listings_finished['neighbourhood_cleansed'].unique().tolist())

# Neighbourhood selection
selected_neighbourhood = st.selectbox("Select a neighbourhood:", neighbourhoods)

# Minimum number of reviews selection
min_reviews = st.slider("How many reviews should the hosts have?", 0, 300, 10)

# Only superhosts selection
only_superhosts = st.checkbox("Only show superhosts", True)

# Get the top hosts based on selected filters
top_hosts, num_entries = get_top_hosts(df_listings_finished, selected_neighbourhood, min_reviews, only_superhosts)

# Sort top_hosts by 'review_scores_rating' and 'number_of_reviews' for the charts
top_hosts_sorted = top_hosts.sort_values(by=['review_scores_rating', 'number_of_reviews'], ascending=False)

# Display the title with the number of currently considered values
st.subheader(f"Top 10 Hosts in {selected_city.capitalize()} ({selected_neighbourhood}) - (currently considering {num_entries} listings)")

# Display the top hosts
st.dataframe(top_hosts)

# Sort top_hosts_sorted by 'Ranking' for the charts
top_hosts_sorted_by_ranking = top_hosts.sort_values(by='Ranking')

# Display charts
st.subheader(f"Average Rating of Top 10 Hosts in {selected_city.capitalize()} ({selected_neighbourhood})")
st.bar_chart(top_hosts_sorted_by_ranking[['host_id', 'review_scores_rating']].set_index('host_id'))

st.subheader(f"Number of Reviews of Top 10 Hosts in {selected_city.capitalize()} ({selected_neighbourhood})")
st.bar_chart(top_hosts_sorted_by_ranking[['host_id', 'number_of_reviews']].set_index('host_id'))
