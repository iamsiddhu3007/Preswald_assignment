from preswald import text, plotly, connect, get_df
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

df_filtered = df[df['price'] > 100]

fig = px.scatter_mapbox(
    df_filtered,
    lat="latitude",
    lon="longitude",
    color="neighbourhood_group",
    hover_name="name",
    hover_data=["price", "room_type"],
    zoom=10,
    height=600,
    title="NYC Airbnb Listings (Price > $100)"
)

fig.update_layout(mapbox_style="carto-positron")
plotly(fig)