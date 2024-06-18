# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 15:10:12 2024

@author: Tung
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:23:13 2024

@author: Tung

Gilt der Voranalyse der Airbnb-Daten
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


#%%

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#%% Einlesen

# data_path = r"C:\Users\Tung\OneDrive\Data_Analyst_Alfa\Woche 4\reviews.csv"
path_review = "../data/cities/reviews_Antwerp.csv"
path_listings = "../data/cities/listings_Antwerp.csv"

# df_full = pd.read_csv(data_path)
df_review = pd.read_csv(path_review)
df_listings = pd.read_csv(path_listings)

#%% Vorverarbeitung
lst_col_remove = ['listing_url',
'scrape_id',
'last_scraped',
'source',
'picture_url',
'host_url',
'host_name',
'host_since',
'host_location',
'host_thumbnail_url',
'host_picture_url',
'host_neighbourhood',
'host_verifications',
'host_has_profile_pic',
'host_identity_verified',
'neighbourhood',
'neighbourhood_cleansed',
'neighbourhood_group_cleansed',
'latitude',
'longitude',
'minimum_minimum_nights',
'maximum_minimum_nights',
'minimum_maximum_nights',
'minimum_nights_avg_ntm',
'maximum_nights_avg_ntm',
'calendar_updated',
'has_availability',
'availability_30',
'availability_60',
'availability_90',
'availability_365',
'calendar_last_scraped',
'license']

# Entfernen der Spalten
df_listings = df_listings.drop(columns=lst_col_remove)

#%% Analyse Listings

'''
Fragestellungen:
    1. df_listings_no_rev: 
        - Kommen die listings ohne Reviews auch in df_review vor? 
    2. df_listings_review:
        - Wie viele Reviews hat so ein Listing im Schnitt, was ist Maximum und Minimum?
'''

df_rev = df_listings[df_listings['name'].str.contains(r'\d+\.\d+', regex=True)].copy()
df_no_rev = df_listings[~df_listings['name'].str.contains(r'\d+\.\d+', regex=True)].copy()

plt_0 = 1
check_num_rev = 0

#%% Kommen die listings ohne Reviews auch in df_review vor? 

df_no_rev['id_in_reviews'] = df_no_rev['id'].isin(df_review['listing_id'])
df_rev['id_in_reviews'] = df_rev['id'].isin(df_review['listing_id'])


#%% Entferne Einträge ohne Reviews
df_no_rev_filtered = df_no_rev[df_no_rev['id_in_reviews']]
df_rev_filtered = df_rev[df_rev['id_in_reviews']]

# Kombiniere die gefilterten DataFrames
df_filtered = pd.concat([df_no_rev_filtered, df_rev_filtered], ignore_index=True)

# Entferne Zeilen aus df_listings basierend auf den gefilterten DataFrames
df_listings = df_listings[df_listings['id'].isin(df_filtered['id'])] 

if check_num_rev:
    #Prüfen, ob es noch Unterkünfte ohne Reviews gibt
    # Überprüfen, ob in der Spalte 'number_of_reviews' Werte gleich 0 vorhanden sind
    number_of_reviews_zero = df_listings['number_of_reviews'] == 0
    
    # Anzahl der Einträge mit 'number_of_reviews' gleich 0 anzeigen
    number_of_reviews_zero_count = number_of_reviews_zero.sum()
    print(f"Anzahl der Einträge mit 'number_of_reviews' gleich 0: {number_of_reviews_zero_count}")
    
    # Optional: Anzeigen der Einträge, bei denen 'number_of_reviews' gleich 0 ist
    listings_with_zero_reviews = df_listings[number_of_reviews_zero]
    print(listings_with_zero_reviews)


#%% Plot
# Zähle die Anzahl der True und False Werte
count_id_in_rev_0 = df_no_rev['id_in_reviews'].value_counts().reindex([True, False], fill_value=0)
count_id_in_rev_1 = df_rev['id_in_reviews'].value_counts().reindex([True, False], fill_value=0)
if plt_0:
    # Diagramm erstellen
    count_id_in_rev_0.plot(kind='bar')
    plt.title(f'Analyse der Listings OHNE Bewertung in "name" bei Gesamtanzahl von {len(df_no_rev)} Werten')
    plt.xlabel('Listings OHNE Bewertung in Namen kommt in "reviews.csv" vor')
    plt.ylabel('Anzahl der IDs')
    plt.xticks(ticks=[0, 1], labels=['True', 'False'], rotation=0)
    plt.show()
    # Anzahl über jedem Balken anzeigen
    for i in range(len(count_id_in_rev_0)):
        plt.text(i, count_id_in_rev_0.iloc[i] + 0.1, str(count_id_in_rev_0.iloc[i]), ha='center', va='bottom')

    
    plt.figure()
    count_id_in_rev_1.plot(kind='bar')
    plt.title(f'Analyse der Listings MIT Bewertung in "name" bei Gesamtanzahl von {len(df_rev)} Werten')
    plt.xlabel('Listings MIT Bewertung in Namen kommt in "reviews.csv" vor')
    plt.ylabel('Anzahl der IDs')
    plt.xticks(ticks=[0, 1], labels=['True', 'False'], rotation=0)
    plt.show()
    # Anzahl über jedem Balken anzeigen
    for i in range(len(count_id_in_rev_1)):
        plt.text(i, count_id_in_rev_1.iloc[i] + 0.1, str(count_id_in_rev_1.iloc[i]), ha='center', va='bottom')

        
    #%% Confusion Matrix erstellen und anzeigen

    # Tatsächliche Werte (0: Keine Bewertung im Namen, 1: Bewertung im Namen)
    y_true = pd.concat([pd.Series([0] * len(df_no_rev)), pd.Series([1] * len(df_rev))], ignore_index=True)
    
    # Vorhergesagte Werte (0: Nicht in reviews.csv, 1: In reviews.csv)
    y_pred = pd.concat([df_no_rev['id_in_reviews'].astype(int), df_rev['id_in_reviews'].astype(int)], ignore_index=True)
    
    # Confusion Matrix berechnen
    cm = confusion_matrix(y_true, y_pred)
    
    # Confusion Matrix anzeigen
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No Review', 'Review'])
    fig, ax = plt.subplots()
    disp.plot(cmap=plt.cm.Blues, ax=ax)
    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
    plt.title(f"Einordnung der Listings nach Review-Vorkommen - Gesamtzahl: {len(df_listings)}")
    plt.show()
        
        
#%% Wie viele Reviews hat so ein Listing im Schnitt, was ist Maximum und Minimum?

# Berechne, wie oft jede listing_id vorkommt
listing_id_counts = df_review['listing_id'].value_counts()

