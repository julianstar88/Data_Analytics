# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 15:10:12 2024

@author: Tung
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:23:13 2024

@author: Tung
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

#%% Analyse Listings

'''
Fragestellungen:
    1. df_listings_no_rev: 
        - Kommen die listings ohne Reviews auch in df_review vor? 
    2. df_listings_review:
        - Wie viele Reviews hat so ein Listing im Schnitt, was ist Maximum und Minimum?
'''

df_rev = df_listings[df_listings['name'].str.contains(r'\d+\.\d+', regex=True)]
df_no_rev = df_listings[~df_listings['name'].str.contains(r'\d+\.\d+', regex=True)]

plt_0 = 0

#%% Kommen die listings ohne Reviews auch in df_review vor? 

df_no_rev['id_in_reviews'] = df_no_rev['id'].isin(df_review['listing_id'])

# Zähle die Anzahl der True und False Werte
count_id_in_rev = df_no_rev['id_in_reviews'].value_counts()
if plt_0:
    # Diagramm erstellen
    count_id_in_rev.plot(kind='bar')
    plt.title(f'Analyse der Listings ohne Bewertung in "name" bei Gesamtanzahl von {len(df_no_rev)} Werten')
    plt.xlabel('Listings ohne Bewertung in Namen kommt in "reviews.csv" vor')
    plt.ylabel('Anzahl der IDs')
    plt.xticks(ticks=[0, 1], labels=['False', 'True'], rotation=0)
    plt.show()
    # Anzahl über jedem Balken anzeigen
    for i in range(len(count_id_in_rev)):
        plt.text(i, count_id_in_rev[i] + 0.1, str(count_id_in_rev[i]), ha='center', va='bottom')
    
#%% Wie viele Reviews hat so ein Listing im Schnitt, was ist Maximum und Minimum?

# Berechne, wie oft jede listing_id vorkommt
listing_id_counts = df_review['listing_id'].value_counts()

