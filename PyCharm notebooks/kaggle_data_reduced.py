import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load the combined DataFrame from the CSV file
df = pd.read_csv("../kaggle data/kaggle_data_reduced.csv.gz", compression="gzip")

# Define a fixed order for the origins
fixed_order = ['andrewmvd', 'rifkiandriyanto', 'thedevastator']
df['Origin'] = pd.Categorical(df['Origin'], categories=fixed_order, ordered=True)

# Define a color palette to use consistently
palette = sns.color_palette("Set2", len(fixed_order))
origin_colors = dict(zip(fixed_order, palette))

''' bar plot with count of records per origin '''
# Create a bar plot showing the count of records per origin with black borders
plt.figure(figsize=(10, 6))

# Count the number of records per origin
record_counts_per_origin = df['Origin'].value_counts().reindex(fixed_order)

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

''' box plot with distribution of ratings per origin '''
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

''' stacked bar chart with distribution of ratings '''
# Prepare the data for the stacked bar chart
rating_counts = df.groupby(['Rating', 'Origin']).size().unstack().fillna(0).reindex(columns=fixed_order)

# Create the stacked bar chart
rating_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=[origin_colors[origin] for origin in rating_counts.columns], edgecolor='black')

plt.title('Stacked Bar Chart of Ratings by Origin')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Origin')

# Show plot
plt.tight_layout()
plt.show()

''' box plot with distribution of review length per rating '''
# Calculate the length of each review
df['Review_Length'] = df['Review'].apply(len)

# Create a box plot showing the distribution of review lengths per rating
plt.figure(figsize=(10, 6))

# Create the box plot
sns.boxplot(x='Rating', y='Review_Length', data=df, palette="Set3", linewidth=1.5)

plt.title('Box Plot of Review Lengths per Rating')
plt.xlabel('Rating')
plt.ylabel('Review Length')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.tight_layout()
plt.show()

''' scatter plot with correlation line '''
# Create the scatter plot with smaller grey points
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Rating', y='Review_Length', data=df, color='grey', s=50)

# Calculate the regression line
slope, intercept, r_value, p_value, std_err = linregress(df['Rating'], df['Review_Length'])
plt.plot(df['Rating'], intercept + slope * df['Rating'], 'r', label=f'R² = {r_value**2:.2f}, p = {p_value:.2e}')

plt.title('Scatter Plot of Review Length vs Rating with Correlation Line')
plt.xlabel('Rating')
plt.ylabel('Review Length')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.tight_layout()
plt.show()
