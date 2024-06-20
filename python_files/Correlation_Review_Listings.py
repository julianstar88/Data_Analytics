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

# Extrahiere die Städtenamen aus den Dateipfaden
def extract_city_name(file_path):
    # Basisname der Datei ohne Erweiterung
    base_name = os.path.basename(file_path)
    
    # Entferne die Dateierweiterung und teile den Namen nach Unterstrichen auf
    parts = base_name.split('_')
    
    # Durchsuche die Teile von rechts nach links, um den ersten Buchstabenstring vor der Dateierweiterung zu finden
    for part in reversed(parts):
        city_name = os.path.splitext(part)[0]  # Entferne die Dateierweiterung, falls vorhanden
        if city_name.isalpha():  # Prüfe, ob der Teil ein Wort (keine Zahl) ist
            return city_name
    
    raise ValueError(f"Städtenamen konnten nicht aus dem Dateipfad extrahiert werden: {file_path}")
    

plt_0 = 1
check_num_rev = 0
bool_save = 0
bool_edit = 0
#%% Voreinstellungen
os.chdir(os.path.dirname(os.path.abspath(__file__)))

p0 = r"C:\Users\Tung\OneDrive\Data_Analyst_Alfa\Data_Analytics\data\cities\reviews_Amsterdam_1.csv"
p1 = r"C:\Users\Tung\OneDrive\Data_Analyst_Alfa\Data_Analytics\data\cities\reviews_Amsterdam_2.csv"
# p2 = r"C:\Users\Tung\OneDrive\Data_Analyst_Alfa\Data_Analytics\data\cities\reviews_LosAngeles_en_5.csv"
# p3 = r"C:\Users\Tung\OneDrive\Data_Analyst_Alfa\Data_Analytics\data\cities\reviews_LosAngeles_en_4.csv"
# p4 = r"C:\Users\Tung\OneDrive\Data_Analyst_Alfa\Data_Analytics\data\cities\reviews_LosAngeles_en_3.csv"
# p5 = r"C:\Users\Tung\OneDrive\Data_Analyst_Alfa\Data_Analytics\data\cities\reviews_LosAngeles_en_2.csv"
# p6 = r"C:\Users\Tung\OneDrive\Data_Analyst_Alfa\Data_Analytics\data\cities\reviews_LosAngeles_en_1.csv"

# path_review = "../data/cities/reviews_Antwerp.csv"

path_listings = "../data/cities/listings_Amsterdam.csv"


city_name_0 = extract_city_name(p0)
city_name_1 = extract_city_name(path_listings)

# Vergleiche die Städtenamen
if city_name_0 != city_name_1:
    raise ValueError(f"Die Städtenamen am Ende der CSV-Dateien stimmen nicht überein: {city_name_0}, {city_name_1}")

# Speicherpfad und Dateinamen definieren
save_path = "../data/cities/processed"
filename = os.path.splitext(os.path.basename(path_listings))[0]
new_filename = f"{filename}_processed.csv"
full_save_path = os.path.join(save_path, new_filename)

# Verzeichnis erstellen, falls es nicht existiert
if not os.path.exists(save_path):
    os.makedirs(save_path)

#%% Einlesen

# Liste der Pfade
file_paths = [p0, p1]
# Liste für die einzelnen DataFrames
dfs = []
# Einlesen und Zusammenfügen der CSV-Dateien
for path in file_paths:
    df = pd.read_csv(path)
    dfs.append(df)
# Zusammenführen aller DataFrames zu einem einzigen DataFrame
df_review = pd.concat(dfs, ignore_index=True)


# df_review = pd.read_csv(path_review)
df_listings = pd.read_csv(path_listings)

#%% Vorverarbeitung
lst_col_remove = [
'host_about',
'description',
'listing_url',
'scrape_id',
'last_scraped',
'source',
'picture_url',
'host_url',
'host_since',
'host_location',
'host_thumbnail_url',
'host_picture_url',
'host_neighbourhood',
'host_verifications',
'host_has_profile_pic',
'host_identity_verified',
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
df_listings = df_listings.drop(columns=lst_col_remove, errors='ignore')

# Überprüfe, ob "price_$" bereits existiert
if "price_$" not in df_listings.columns:
    # Ersetze "$" und "," und konvertiere nach float
    df_listings["price"] = df_listings["price"].replace("[\$,]", "", regex=True).astype(float)
    # Benenne die Spalte um
    df_listings.rename(columns={"price": "price_$"}, inplace=True)

#%% Überprüfen, ob 'id' oder 'listing_id' vorhanden ist und entsprechend verwenden
if 'id' in df_listings.columns:
    id_column = 'id'
elif 'listing_id' in df_listings.columns:
    id_column = 'listing_id'
else:
    raise KeyError("Weder 'id' noch 'listing_id' Spalte ist in df_listings vorhanden")
#%% Analyse Listings

'''
Fragestellungen:
    1. df_listings_no_rev: 
        - Kommen die listings ohne Reviews auch in df_review vor? 
    2. df_listings_review:
        - Wie viele Reviews hat so ein Listing im Schnitt, was ist Maximum und Minimum?
'''

df_rev = df_listings[df_listings['review_scores_rating'].notna()].copy()
df_no_rev = df_listings[df_listings['review_scores_rating'].isna()].copy()


#%% Kommen die listings ohne Reviews auch in df_review vor? 

df_no_rev.loc[:, 'id_in_reviews'] = df_no_rev[id_column].isin(df_review['listing_id'])
df_rev.loc[:, 'id_in_reviews'] = df_rev[id_column].isin(df_review['listing_id'])

#%% Entferne Einträge ohne Reviews
df_no_rev_filtered = df_no_rev[df_no_rev['id_in_reviews']]
df_rev_filtered = df_rev[df_rev['id_in_reviews']]

# Kombiniere die gefilterten DataFrames
df_filtered = pd.concat([df_no_rev_filtered, df_rev_filtered], ignore_index=True)

# Entferne Zeilen aus df_listings basierend auf den gefilterten DataFrames
df_listings = df_listings[df_listings[id_column].isin(df_filtered[id_column])] 

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
    plt.title(f'Analyse der Listings, bei der anscheinend KEINE Reviews gegeben sind bei Gesamtanzahl von {len(df_no_rev)} Werten für {city_name_0}')
    plt.xlabel('Unterkunft kommt trotzdem in "reviews.csv" vor')
    plt.ylabel('Anzahl der IDs')
    plt.xticks(ticks=[0, 1], labels=['True', 'False'], rotation=0)
    plt.show()
    # Anzahl über jedem Balken anzeigen
    for i in range(len(count_id_in_rev_0)):
        plt.text(i, count_id_in_rev_0.iloc[i] + 0.1, str(count_id_in_rev_0.iloc[i]), ha='center', va='bottom')

    
    plt.figure()
    count_id_in_rev_1.plot(kind='bar')
    plt.title(f'Analyse der Listings, bei der anscheinend KEINE Reviews gegeben sind bei Gesamtanzahl von {len(df_rev)} Werten für {city_name_0}')
    plt.xlabel('Unterkunft kommt in "reviews.csv" vor')
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

#%% Speichern der neuen CSV
if bool_save:
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    df_listings.to_csv(full_save_path, index=False)
    print(f"Datei wurde gespeichert als {full_save_path}")

