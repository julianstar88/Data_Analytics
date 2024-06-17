import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the combined DataFrame from the CSV file
df = pd.read_csv("../kaggle data/kaggle_data_complete.csv.gz", compression="gzip")

# Define a color palette to use consistently
palette = sns.color_palette("Set3", len(df['Origin'].unique()))
origin_colors = dict(zip(df['Origin'].unique(), palette))

# Create a bar plot showing the count of records per origin with black borders
plt.figure(figsize=(10, 6))

# Count the number of records per origin
record_counts_per_origin = df['Origin'].value_counts()

# Create the bar plot with consistent colors and black borders
record_counts_per_origin.plot(kind='bar', color=[origin_colors[origin] for origin in record_counts_per_origin.index], edgecolor='black')

plt.title('Count of Records per Origin')
plt.xlabel('Origin')
plt.ylabel('Count of Records')
plt.xticks(rotation=30)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.tight_layout()
plt.show()

# Create a box plot showing the distribution of ratings per origin with consistent colors and black borders, and include the mean
plt.figure(figsize=(10, 6))

# Create the box plot with mean points
sns.boxplot(x='Origin', y='Rating', data=df, palette=origin_colors, linewidth=1.5)

# Calculate the mean for each origin and plot it
means = df.groupby('Origin')['Rating'].mean().values
for i, mean in enumerate(means):
    plt.scatter(i, mean, color='black', zorder=5, marker='*', s=100)
    plt.text(i, mean + 0.1, f'{mean:.2f}', color='black', ha='center', va='bottom', fontsize=10)

plt.title('Box Plot of Ratings per Origin with Mean')
plt.xlabel('Origin')
plt.ylabel('Rating')
plt.xticks(rotation=30)
plt.yticks(range(int(df['Rating'].min()), int(df['Rating'].max()) + 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.tight_layout()
plt.show()
