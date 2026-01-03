# Import necessary libraries
from preswald import text, plotly, connect, get_df, slider
import pandas as pd
import plotly.express as px

# Set the title of the application
text("# NYC Airbnb Listings Map")

# Connect to the data source and get the DataFrame
connect()
df = get_df("AB_NYC_2019")

# Data cleaning and preprocessing
df = df.dropna(subset=['name', 'host_name', 'latitude', 'longitude', 'price'])
df = df.drop_duplicates()
df = df[df['price'] > 10]
df['room_type'] = df['room_type'].str.strip().str.title()
df['neighbourhood_group'] = df['neighbourhood_group'].str.strip().str.title()
df['is_active'] = df['reviews_per_month'].fillna(0) > 0

# Determine the price range for the sliders
min_price = int(df['price'].min())
max_price = int(df['price'].max())

# Create interactive sliders for price range selection
low = slider("Minimum Price", min_val=min_price, max_val=max_price, default=min_price)
high = slider("Maximum Price", min_val=min_price, max_val=max_price, default=max_price)

# Filter the DataFrame based on the selected price range
df_filtered = df[(df['price'] >= low) & (df['price'] <= high)]

# Create a scatter mapbox plot using Plotly Express
fig = px.scatter_mapbox(
    df_filtered,
    lat="latitude",
    lon="longitude",
    color="room_type",
    hover_name="name",
    hover_data=["price", "number_of_reviews", "neighbourhood_group"],
    zoom=10,
    height=600,
    title=f"Listings from ${low} to ${high}"
)

# Update the map layout and style
fig.update_layout(mapbox_style="carto-positron")

# Display the Plotly figure in the application
plotly(fig)

## update demo