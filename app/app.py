# app.py
import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="6th of October Restaurant Landscape", layout="wide")
st.title("🍽️ 6th of October City — Restaurant Landscape")

@st.cache_data
def load_data():
    conn = sqlite3.connect('data/analytics/restaurants.db')
    df = pd.read_sql("SELECT * FROM restaurants", conn)
    conn.close()
    return df

df = load_data()
st.write(f"Loaded {len(df)} food-serving businesses.")

col1, col2, col3 = st.columns(3)
col1.metric("Total restaurants", len(df))
col1.metric("Rated", int(df['is_rated'].sum()))
col2.metric("Avg. rating", round(df.loc[df['is_rated']==1, 'total_score'].mean(), 2))
col3.metric("Total reviews", int(df['reviews_count'].sum()))

st.sidebar.header("Filters")
categories = st.sidebar.multiselect(
    "Category", options=sorted(df['category_name'].unique()),
    default=sorted(df['category_name'].unique())
)
min_reviews = st.sidebar.slider("Minimum reviews", 0, int(df['reviews_count'].max()), 0)

filtered = df[df['category_name'].isin(categories) & (df['reviews_count'] >= min_reviews)]

st.subheader("Rating distribution")
rating_display = df['total_score'].apply(lambda x: 'Unrated' if pd.isna(x) else str(round(x, 1)))
counts = rating_display.value_counts()

# sort numeric labels ascending, then push 'Unrated' to the end
numeric_labels = sorted([l for l in counts.index if l != 'Unrated'], key=float)
ordered_labels = numeric_labels + (['Unrated'] if 'Unrated' in counts.index else [])

st.bar_chart(counts.reindex(ordered_labels))


st.subheader("Restaurants by category")
st.bar_chart(filtered['category_name'].value_counts())

st.subheader("Map")
st.map(
    filtered.dropna(subset=['latitude', 'longitude'])
    .rename(columns={'latitude': 'lat', 'longitude': 'lon'})[['lat', 'lon']]
)

st.subheader("Top reviewed")
st.dataframe(
    filtered.sort_values('reviews_count', ascending=False)
    [['title', 'category_name', 'total_score', 'reviews_count']]
    .fillna({'total_score': 'Unrated'})
    .head(10)
)

st.caption(
    f"Data quality note: {int((df['is_rated'] == 0).sum())} of {len(df)} businesses have no reviews yet "
    f"('Unrated'), and {int((df['neighborhood']=='Not provided').sum())} have no neighborhood listed on Google Maps."
)