import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.stats import linregress


# Caching the data loading function
@st.cache_data
def load_data():
    city_files = {
        'Amsterdam, Netherlands': "listings_Amsterdam_finished.csv",
        'Antwerp, Belgium': "listings_Antwerp_finished.csv",
        'Los Angeles, USA': "listings_LosAngeles_finished.csv",
        'Rotterdam, Netherlands': "listings_Rotterdam_finished.csv"
    }

    city_data = {}

    for city, file_path in city_files.items():
        df = pd.read_csv(file_path)
        df = df.drop(columns="neighbourhood").rename(
            columns={'neighbourhood_cleansed': 'neighbourhood',
                     'room_type': 'room type',
                     'review_scores_rating': 'rating (original)',
                     'rf_predict_avg': 'rating (rf-prediction)',
                     'xgb_predict_avg': 'rating (xgb-prediction)'})

        city_data[city] = df

    return city_data


# Load data
city_data = load_data()

# Create lists for selection boxes
cities = list(city_data.keys())
columns = ['neighbourhood', 'room type', 'accommodates', 'rating (original)', 'rating (rf-prediction)',
           'rating (xgb-prediction)']

# Streamlit title
st.title('AirBnB Price Dependencies')

# Streamlit sidebar for selections
selected_city = st.sidebar.selectbox('Select the city', cities)
selected_column = st.sidebar.selectbox('Select the factor to analyze', columns)

# Select the appropriate dataframe based on city selection
df = city_data[selected_city]

# Slider for price range
price_min, price_max = int(df['price_$'].min()), int(df['price_$'].max())
default_price_max = min(price_max, 1000)
selected_price_range = st.sidebar.slider('Select the price range', price_min, price_max, (price_min, default_price_max), step=50)
df = df[(df['price_$'] >= selected_price_range[0]) & (df['price_$'] <= selected_price_range[1])]

# Slider for top N neighbourhoods
if selected_column == 'neighbourhood':
    max_neighbourhoods = len(df['neighbourhood'].value_counts())
    top_n = st.sidebar.slider('Select N neighbourhoods (most counts)', 1, max_neighbourhoods, 10)
    top_neighbourhoods = df['neighbourhood'].value_counts().nlargest(top_n).index
    df = df[df['neighbourhood'].isin(top_neighbourhoods)]

# Slider for ratings
if selected_column in ['rating (original)', 'rating (rf-prediction)', 'rating (xgb-prediction)']:
    rating_range = st.sidebar.slider('Select the rating range', 1, 5, (1, 5), step=1)
    # Filter dataframe based on rating range
    df = df[(df[selected_column] >= rating_range[0]) & (df[selected_column] <= rating_range[1])]

# Remove rows with NaN values in the relevant columns
df = df.dropna(
    subset=['price_$', 'neighbourhood', 'room type', 'accommodates',
            'rating (original)', 'rating (rf-prediction)', 'rating (xgb-prediction)'])

# Plotting
fig, ax = plt.subplots(figsize=(8, 6))  # Set the figure size

if selected_column in ['neighbourhood', 'room type']:
    # Sort the categories alphabetically
    sorted_categories = sorted(df[selected_column].unique())
    # Boxplot
    sns.boxplot(x=selected_column, y='price_$', data=df, ax=ax, palette="Set2", order=sorted_categories)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
else:
    x = df[selected_column]
    y = df['price_$']
    # Scatter plot
    sns.scatterplot(x=x, y=y, ax=ax, color='grey', s=20)
    # Regression line
    reg = LinearRegression().fit(x.values.reshape(-1, 1), y)
    y_pred = reg.predict(x.values.reshape(-1, 1))
    r2 = r2_score(y, y_pred)
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    ax.plot(x, y_pred, color='red')
    # R² and p-value
    ax.text(0.05, 0.95, f'R²: {r2:.2f}\np-value: {p_value:.2e}', transform=ax.transAxes,
            fontsize=10, verticalalignment='top', color='red',
            bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='white'))

# Set axis labels
ax.set_xlabel(selected_column, fontsize=12, fontweight='bold')
ax.set_ylabel('price ($)', fontsize=12, fontweight='bold')

# Add subtitle with city name
plt.title(f'Price vs. {selected_column} in {selected_city}', fontsize=14)

st.pyplot(fig)
