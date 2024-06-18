import pandas as pd

columns = [
    "id", "name", "description", "neighborhood_overview", "host_id", "host_name", "host_since", "host_location",
    "host_about", "host_response_time", "host_response_rate", "host_acceptance_rate", "host_is_superhost",
    "host_listings_count", "host_total_listings_count", "host_verifications", "host_identity_verified", "neighbourhood",
    "neighbourhood_cleansed", "latitude", "longitude", "property_type", "room_type", "accommodates", "bathrooms",
    "bathrooms_text", "bedrooms", "beds", "amenities", "price", "minimum_nights", "maximum_nights",
    "minimum_minimum_nights", "maximum_minimum_nights", "minimum_maximum_nights", "maximum_maximum_nights",
    "minimum_nights_avg_ntm", "maximum_nights_avg_ntm", "has_availability", "availability_30", "availability_60",
    "availability_90", "availability_365", "number_of_reviews", "number_of_reviews_ltm", "number_of_reviews_l30d",
    "first_review", "last_review", "review_scores_rating", "review_scores_accuracy", "review_scores_cleanliness",
    "review_scores_checkin", "review_scores_communication", "review_scores_location", "review_scores_value",
    "instant_bookable", "calculated_host_listings_count", "calculated_host_listings_count_entire_homes",
    "calculated_host_listings_count_shared_rooms", "reviews_per_month"]

''' Amsterdam '''
# url: https://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/2024-03-11/data/listings.csv.gz
data_Amsterdam = pd.read_csv("airBnB/listings_Amsterdam.csv.gz", compression="gzip")

df_Amsterdam = pd.DataFrame(data_Amsterdam)
df_Amsterdam = df_Amsterdam[columns]

# extract currency from column price
df_Amsterdam["price"] = df_Amsterdam["price"].replace("[\$,]", "", regex=True).astype(float)
df_Amsterdam.rename(columns={"id": "listing_id",
                             "price": "price_$"}, inplace=True)

# check data types
dtypes_Amsterdam = df_Amsterdam.dtypes

''' Antwerp '''
# url: https://data.insideairbnb.com/belgium/vlg/antwerp/2023-12-27/data/listings.csv.gz
data_Antwerp = pd.read_csv("airBnB/listings_Antwerp.csv.gz", compression="gzip")

df_Antwerp = pd.DataFrame(data_Antwerp)
df_Antwerp = df_Antwerp[columns]

# extract currency from column price
df_Antwerp["price"] = df_Antwerp["price"].replace("[\$,]", "", regex=True).astype(float)
df_Antwerp.rename(columns={"id": "listing_id",
                           "price": "price_$"}, inplace=True)

# check data types
dtypes_Antwerp = df_Antwerp.dtypes
print("different data types (Amsterdam vs. Antwerp):",
      dtypes_Amsterdam[dtypes_Antwerp != dtypes_Amsterdam], "vs.",
      dtypes_Antwerp[dtypes_Antwerp != dtypes_Amsterdam])
df_Antwerp["description"] = df_Antwerp["description"].astype(object)

''' Rotterdam '''
# url: https://data.insideairbnb.com/the-netherlands/south-holland/rotterdam/2023-12-23/data/listings.csv.gz
data_Rotterdam = pd.read_csv("airBnB/listings_Antwerp.csv.gz", compression="gzip")

df_Rotterdam = pd.DataFrame(data_Rotterdam)
df_Rotterdam = df_Rotterdam[columns]

# extract currency from column price
df_Rotterdam["price"] = df_Rotterdam["price"].replace("[\$,]", "", regex=True).astype(float)
df_Rotterdam.rename(columns={"id": "listing_id",
                             "price": "price_$"}, inplace=True)

# check data types
dtypes_Rotterdam = df_Rotterdam.dtypes
print("different data types (Amsterdam vs. Rotterdam):",
      dtypes_Amsterdam[dtypes_Rotterdam != dtypes_Amsterdam], "vs.",
      dtypes_Rotterdam[dtypes_Rotterdam != dtypes_Amsterdam])
df_Rotterdam["description"] = df_Rotterdam["description"].astype(object)

''' Los Angeles '''
# url: https://data.insideairbnb.com/united-states/ca/los-angeles/2024-03-11/data/listings.csv.gz
data_LosAngeles = pd.read_csv("airBnB/listings_LosAngeles.csv.gz", compression="gzip")

df_LosAngeles = pd.DataFrame(data_LosAngeles)
df_LosAngeles = df_LosAngeles[columns]

# extract currency from column price
df_LosAngeles["price"] = df_LosAngeles["price"].replace("[\$,]", "", regex=True).astype(float)
df_LosAngeles.rename(columns={"id": "listing_id",
                              "price": "price_$"}, inplace=True)

# check data types
dtypes_LosAngeles = df_LosAngeles.dtypes
print("different data types (Amsterdam vs. Los Angeles):",
      dtypes_Amsterdam[dtypes_LosAngeles != dtypes_Amsterdam], "vs."
,      dtypes_LosAngeles[dtypes_LosAngeles != dtypes_Amsterdam])
df_Amsterdam["host_listings_count"] = df_Amsterdam["host_listings_count"].astype(float)
df_Antwerp["host_listings_count"] = df_Antwerp["host_listings_count"].astype(float)
df_Rotterdam["host_listings_count"] = df_Rotterdam["host_listings_count"].astype(float)

# save dataframes
df_Amsterdam.to_csv("../data/cities/listings_Amsterdam.csv.gz", index=False, compression="gzip")
df_Antwerp.to_csv("../data/cities/listings_Antwerp.csv.gz", index=False, compression="gzip")
df_Rotterdam.to_csv("../data/cities/listings_Rotterdam.csv.gz", index=False, compression="gzip")
df_LosAngeles.to_csv("../data/cities/listings_LosAngeles.csv.gz", index=False, compression="gzip")
