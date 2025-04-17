from preswald import text, plotly, connect, get_df, slider
import pandas as pd
import plotly.express as px

text("# NYC Airbnb Listings Map")

connect()
df = get_df("AB_NYC_2019")

df = df.dropna(subset=['name', 'host_name', 'latitude', 'longitude', 'price'])
df = df.drop_duplicates()
df = df[df['price'] > 10]
df['room_type'] = df['room_type'].str.strip().str.title()
df['neighbourhood_group'] = df['neighbourhood_group'].str.strip().str.title()
df['is_active'] = df['reviews_per_month'].fillna(0) > 0

min_price = int(df['price'].min())
max_price = int(df['price'].max())

low = slider("Minimum Price", min_val=min_price, max_val=max_price, default=min_price)
high = slider("Maximum Price", min_val=min_price, max_val=max_price, default=max_price)

df_filtered = df[(df['price'] >= low) & (df['price'] <= high)]

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

fig.update_layout(mapbox_style="carto-positron")
plotly(fig)