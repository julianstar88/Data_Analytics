# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:06:29 2024

@author: Tung
"""

import os
import pandas as pd
import streamlit as st

# Set the working directory to the script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))
path_listings_finished = "../data/cities/finished/listings_Antwerp_finished.csv"

# Load the data
df_listings_finished = pd.read_csv(path_listings_finished)

# Define a function to get the top hosts for a given neighbourhood
def get_top_hosts(df, neighbourhood, min_reviews, only_superhosts, top_n=10):
    # Filter the dataframe for the selected neighbourhood
    if neighbourhood != 'All':
        df = df[df['neighbourhood'] == neighbourhood]
        
    # Filter the dataframe for minimum number of reviews
    df = df[df['number_of_reviews'] >= min_reviews]
    
    # Aggregate data at the host level
    host_stats = df.groupby('host_id').agg({
        'review_scores_rating': 'mean',
        'number_of_reviews': 'sum',
        'host_is_superhost': 'first',
        'host_listings_count': 'first'
    }).reset_index()
    
    # Filter only Superhosts if the option is selected
    if only_superhosts:
        host_stats = host_stats[host_stats['host_is_superhost'] == 't']
    
    # Sort by average rating and number of reviews
    host_stats = host_stats.sort_values(by=['review_scores_rating', 'number_of_reviews'], ascending=False)
    
    return host_stats.head(top_n), len(df)

# Get a list of unique neighbourhoods
neighbourhoods = ['All'] + df_listings_finished['neighbourhood'].unique().tolist()

# Streamlit dashboard
st.title("Top 10 Airbnb Hosts in Antwerp")

# Neighbourhood selection
selected_neighbourhood = st.selectbox("Select a neighbourhood:", neighbourhoods)

# Minimum number of reviews selection
min_reviews = st.slider("How many reviews should the hosts have?", 0, 300, 10)

# Only superhosts selection
only_superhosts = st.checkbox("Only show superhosts", True)

# Get the top hosts based on selected filters
top_hosts, num_entries = get_top_hosts(df_listings_finished, selected_neighbourhood, min_reviews, only_superhosts)

# Display the title with the number of currently considered values
st.subheader(f"Top 10 Hosts (currently considering {num_entries} listings)")

# Display the top hosts
st.dataframe(top_hosts)

# Display charts
st.subheader("Average Rating of Top 10 Hosts")
st.bar_chart(top_hosts[['host_id', 'review_scores_rating']].set_index('host_id'))

st.subheader("Number of Reviews of Top 10 Hosts")
st.bar_chart(top_hosts[['host_id', 'number_of_reviews']].set_index('host_id'))