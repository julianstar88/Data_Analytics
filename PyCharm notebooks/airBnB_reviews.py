import pandas as pd
from langdetect import detect, LangDetectException

# function for language detection
def detect_language(text):
    try:
        if isinstance(text, str) and text.strip():
            return detect(text)
        else:
            return "unknown"
    except LangDetectException:
        return "error"

''' Amsterdam '''
# url: https://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/2024-03-11/data/reviews.csv.gz
data_Amsterdam = pd.read_csv("airBnB/reviews_Amsterdam.csv.gz", compression="gzip")
df_Amsterdam = pd.DataFrame(data_Amsterdam)

# check data types
dtypes_Amsterdam = df_Amsterdam.dtypes

# check language
df_Amsterdam["language"] = df_Amsterdam["comments"].map(detect_language)
df_Amsterdam_en = df_Amsterdam.loc[df_Amsterdam["language"] == "en"].drop(columns="language")
print("percentage of english comments (Amsterdam):", round(len(df_Amsterdam_en) / len(df_Amsterdam) * 100, 2))

''' Antwerp '''
# url: https://data.insideairbnb.com/belgium/vlg/antwerp/2023-12-27/data/reviews.csv.gz
data_Antwerp = pd.read_csv("airBnB/reviews_Antwerp.csv.gz", compression="gzip")
df_Antwerp = pd.DataFrame(data_Antwerp)

# check data types
dtypes_Antwerp = df_Antwerp.dtypes
print("different data types (Amsterdam vs. Antwerp):",
      dtypes_Amsterdam[dtypes_Antwerp != dtypes_Amsterdam], "vs.",
      dtypes_Antwerp[dtypes_Antwerp != dtypes_Amsterdam])

# check language
df_Antwerp["language"] = df_Antwerp["comments"].map(detect_language)
df_Antwerp_en = df_Antwerp.loc[df_Antwerp["language"] == "en"].drop(columns="language")
print("percentage of english comments (Antwerp):", round(len(df_Antwerp_en) / len(df_Antwerp) * 100, 2))

''' Rotterdam '''
# url: https://data.insideairbnb.com/the-netherlands/south-holland/rotterdam/2023-12-23/data/reviews.csv.gz
data_Rotterdam = pd.read_csv("airBnB/reviews_Rotterdam.csv.gz", compression="gzip")
df_Rotterdam = pd.DataFrame(data_Rotterdam)

# check data types
dtypes_Rotterdam = df_Rotterdam.dtypes
print("different data types (Amsterdam vs. Rotterdam):",
      dtypes_Amsterdam[dtypes_Rotterdam != dtypes_Amsterdam], "vs.",
      dtypes_Rotterdam[dtypes_Rotterdam != dtypes_Amsterdam])

# check language
df_Rotterdam["language"] = df_Rotterdam["comments"].map(detect_language)
df_Rotterdam_en = df_Rotterdam.loc[df_Rotterdam["language"] == "en"].drop(columns="language")
print("percentage of english comments (Rotterdam):", round(len(df_Rotterdam_en) / len(df_Rotterdam) * 100, 2))

''' Los Angeles '''
# url: https://data.insideairbnb.com/united-states/ca/los-angeles/2024-03-11/data/reviews.csv.gz
data_LosAngeles = pd.read_csv("airBnB/reviews_LosAngeles.csv.gz", compression="gzip")
df_LosAngeles = pd.DataFrame(data_LosAngeles)

# check data types
dtypes_LosAngeles = df_LosAngeles.dtypes
print("different data types (Amsterdam vs. Los Angeles):",
      dtypes_Amsterdam[dtypes_LosAngeles != dtypes_Amsterdam], "vs.",
      dtypes_LosAngeles[dtypes_LosAngeles != dtypes_Amsterdam])

# check language
df_LosAngeles["language"] = df_LosAngeles["comments"].map(detect_language)
df_LosAngeles_en = df_LosAngeles.loc[df_LosAngeles["language"] == "en"].drop(columns="language")
print("percentage of english comments (Los Angeles):", round(len(df_LosAngeles_en) / len(df_LosAngeles) * 100, 2))

# save dataframes
df_Amsterdam.to_csv("../data/cities/reviews_Amsterdam.csv.gz", index=False, compression="gzip")
df_Antwerp.to_csv("../data/cities/reviews_Antwerp.csv.gz", index=False, compression="gzip")
df_Rotterdam.to_csv("../data/cities/reviews_Rotterdam.csv.gz", index=False, compression="gzip")
df_LosAngeles.to_csv("../data/cities/reviews_LosAngeles.csv.gz", index=False, compression="gzip")
