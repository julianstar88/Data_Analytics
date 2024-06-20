# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 10:04:28 2024

@author: Tung

What are the ten most popular provider of a listing within a city
"""

import os
import pandas as pd
import streamlit as st


os.chdir(os.path.dirname(os.path.abspath(__file__)))
path_listings_finished = "../data/cities/finished/listings_Antwerp_finished.csv"



df_listings_finished = pd.read_csv(path_listings_finished)


# Definiere eine Funktion zur Ermittlung der besten Hosts
def get_top_hosts(df, top_n=10):
    # Aggregiere Daten auf Host-Ebene
    host_stats = df.groupby('host_id').agg({
        'review_scores_rating': 'mean',
        'number_of_reviews': 'sum',
        'host_is_superhost': 'first',
        'host_listings_count': 'first'
    }).reset_index()
    
    # Filtere nur Superhosts
    superhosts = host_stats[host_stats['host_is_superhost'] == 't']
    
    # Sortiere nach Durchschnittsbewertung und Anzahl der Bewertungen
    superhosts = superhosts.sort_values(by=['review_scores_rating', 'number_of_reviews'], ascending=False)
    
    return superhosts.head(top_n)

# Beste Hosts ermitteln
top_hosts = get_top_hosts(df_listings_finished)

# Streamlit-Dashboard
st.title("Top 10 Airbnb Hosts in Antwerp")

st.subheader("Host Details")
st.dataframe(top_hosts)

st.subheader("Average Rating of Top 10 Hosts")
st.bar_chart(top_hosts[['host_id', 'review_scores_rating']].set_index('host_id'))

st.subheader("Number of Reviews of Top 10 Hosts")
st.bar_chart(top_hosts[['host_id', 'number_of_reviews']].set_index('host_id'))