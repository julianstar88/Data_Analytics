import pandas as pd

columns = ["listing_id", "id", "date", "reviewer_id", "reviewer_name", "comments"]

''' Amsterdam '''
# url: https://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/2024-03-11/data/reviews.csv.gz
data_Amsterdam = pd.read_csv("airBnB/reviews_Amsterdam.csv.gz", compression="gzip")

df_Amsterdam = pd.DataFrame(data_Amsterdam)
df_Amsterdam = df_Amsterdam[columns]

# check data types
dtypes_Amsterdam = df_Amsterdam.dtypes

''' Antwerp '''
# url: https://data.insideairbnb.com/belgium/vlg/antwerp/2023-12-27/data/reviews.csv.gz
data_Antwerp = pd.read_csv("airBnB/reviews_Antwerp.csv.gz", compression="gzip")

df_Antwerp = pd.DataFrame(data_Antwerp)
df_Antwerp = df_Antwerp[columns]

# check data types
dtypes_Antwerp = df_Antwerp.dtypes
print("different data types (Amsterdam vs. Antwerp):",
      dtypes_Amsterdam[dtypes_Antwerp != dtypes_Amsterdam], "vs.",
      dtypes_Antwerp[dtypes_Antwerp != dtypes_Amsterdam])

''' Rotterdam '''
# url: https://data.insideairbnb.com/the-netherlands/south-holland/rotterdam/2023-12-23/data/reviews.csv.gz
data_Rotterdam = pd.read_csv("airBnB/reviews_Rotterdam.csv.gz", compression="gzip")

df_Rotterdam = pd.DataFrame(data_Rotterdam)
df_Rotterdam = df_Rotterdam[columns]

# check data types
dtypes_Rotterdam = df_Rotterdam.dtypes
print("different data types (Amsterdam vs. Rotterdam):",
      dtypes_Amsterdam[dtypes_Rotterdam != dtypes_Amsterdam], "vs.",
      dtypes_Rotterdam[dtypes_Rotterdam != dtypes_Amsterdam])

''' Los Angeles '''
# url: https://data.insideairbnb.com/united-states/ca/los-angeles/2024-03-11/data/reviews.csv.gz
data_LosAngeles = pd.read_csv("airBnB/reviews_LosAngeles.csv.gz", compression="gzip")

df_LosAngeles = pd.DataFrame(data_LosAngeles)
df_LosAngeles = df_LosAngeles[columns]

# check data types
dtypes_LosAngeles = df_LosAngeles.dtypes
print("different data types (Amsterdam vs. Los Angeles):",
      dtypes_Amsterdam[dtypes_LosAngeles != dtypes_Amsterdam], "vs.",
      dtypes_LosAngeles[dtypes_LosAngeles != dtypes_Amsterdam])

# save dataframes
df_Amsterdam.to_csv("../data/cities/reviews_Amsterdam.csv.gz", index=False, compression="gzip")
df_Antwerp.to_csv("../data/cities/reviews_Antwerp.csv.gz", index=False, compression="gzip")
df_Rotterdam.to_csv("../data/cities/reviews_Rotterdam.csv.gz", index=False, compression="gzip")
df_LosAngeles.to_csv("../data/cities/reviews_LosAngeles.csv.gz", index=False, compression="gzip")
