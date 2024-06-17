import pandas as pd

''' first dataset '''
# url: https://www.kaggle.com/datasets/thedevastator/tripadvisor-hotel-reviews
data_thedevastator = pd.read_csv("kaggle/b.csv", encoding="ISO-8859-1")
df_thedevastator = pd.DataFrame(data_thedevastator)[["Review", "Rating"]]
df_thedevastator["Origin"] = "thedevastator"

''' second dataset '''
# url: https://www.kaggle.com/datasets/arnabchaki/tripadvisor-reviews-2023?resource=download
data_arnabchaki = pd.read_csv("kaggle/New_Delhi_reviews.csv")
df_arnabchaki = pd.DataFrame(data_arnabchaki)
df_arnabchaki.columns = ["Rating", "Review"]
df_arnabchaki["Origin"] = "arnabchaki"

''' third dataset '''
# url: https://www.kaggle.com/datasets/rifkiandriyanto/tripadvisor-1000-dataset-examples
data_rifkiandriyanto = pd.read_csv("kaggle/trip-advisor-copy.csv")
df_rifkiandriyanto = pd.DataFrame(data_rifkiandriyanto)
df_rifkiandriyanto["Origin"] = "rifkiandriyanto"

''' fourth dataset '''
# url: https://www.kaggle.com/datasets/andrewmvd/trip-advisor-hotel-reviews
data_andrewmvd = pd.read_csv("kaggle/tripadvisor_hotel_reviews.csv")
df_andrewmvd = pd.DataFrame(data_andrewmvd)
df_andrewmvd["Origin"] = "andrewmvd"

''' combine datasets '''
combined_df_complete = pd.concat([df_thedevastator, df_arnabchaki, df_rifkiandriyanto, df_andrewmvd], ignore_index=True)
combined_df_complete.to_csv("kaggle_data_complete.csv.gz", index=False, compression="gzip")

combined_df_reduced = pd.concat([df_thedevastator, df_rifkiandriyanto, df_andrewmvd], ignore_index=True)
combined_df_reduced.to_csv("kaggle_data_reduced.csv.gz", index=False, compression="gzip")
