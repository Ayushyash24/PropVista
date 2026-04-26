import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

from app_style import app_footer, apply_app_style, page_hero


st.set_page_config(page_title="PropVista Analytics", page_icon="🏠", layout="wide")
apply_app_style()

page_hero(
    "🏠 Market Analytics",
    "Explore real estate patterns across sectors, BHK demand, luxury scores, furnishing impact, and pricing trends.",
)

# ── Load Data ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

new_df = pd.read_csv(os.path.join(DATASETS_DIR, 'data_viz1.csv'))
feature_text = pickle.load(open(os.path.join(DATASETS_DIR, 'feature_text.pkl'), 'rb'))

# ── Fix Data Types ──────────────────────────────────────────
cols = [
    'price',
    'built_up_area',
    'price_per_sqft',
    'latitude',
    'longitude',
    'bedRoom',
    'bathroom',
    'floorNum',
    'luxury_score',
    'furnishing_type',
]
for col in cols:
    new_df[col] = pd.to_numeric(new_df[col], errors='coerce')

new_df['property_type'] = new_df['property_type'].astype(str).str.lower().str.strip()
new_df['sector'] = new_df['sector'].astype(str).str.lower().str.strip()

# Remove invalid rows
new_df = new_df.dropna(subset=['price', 'built_up_area', 'bedRoom', 'property_type'])
new_df = new_df[(new_df['price'] > 0) & (new_df['built_up_area'] > 0)]
new_df['bedRoom'] = new_df['bedRoom'].astype(int)
new_df['furnishing_label'] = new_df['furnishing_type'].map({
    0: 'Unfurnished',
    1: 'Semi Furnished',
    2: 'Furnished',
})

st.header('Market Snapshot')

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric('Listings', f"{len(new_df):,}")

with metric_col2:
    st.metric('Median Price', f"₹ {new_df['price'].median():.2f} Cr")

with metric_col3:
    st.metric('Median Price / Sqft', f"₹ {new_df['price_per_sqft'].median():,.0f}")

with metric_col4:
    st.metric('Median Area', f"{new_df['built_up_area'].median():,.0f} sqft")

# ── Geomap ─────────────────────────────────────────────────
st.header('Sector Price per Sqft Geomap')

group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area',
                                     'latitude', 'longitude']].mean(numeric_only=True)

fig_map = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size='built_up_area',
    zoom=10,
    mapbox_style="open-street-map",
    hover_name=group_df.index
)

st.plotly_chart(fig_map, use_container_width=True)

# ── Wordcloud ──────────────────────────────────────────────
st.header('Features Wordcloud')

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color='white'
).generate(feature_text)

fig_wc, ax_wc = plt.subplots(figsize=(8, 8))
ax_wc.imshow(wordcloud)
ax_wc.axis("off")
st.pyplot(fig_wc)

# ── Area vs Price (FINAL FIX 🔥) ───────────────────────────
st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat', 'house'])

scatter_df = new_df[new_df['property_type'] == property_type].copy()

# Clean again
scatter_df = scatter_df.dropna(subset=['built_up_area', 'price'])
scatter_df = scatter_df[
    (scatter_df['built_up_area'] > 0) &
    (scatter_df['price'] > 0)
]

st.write("Filtered rows:", len(scatter_df))
st.write("Area range:", scatter_df['built_up_area'].min(), "-", scatter_df['built_up_area'].max())
st.write("Price range:", scatter_df['price'].min(), "-", scatter_df['price'].max())

if len(scatter_df) > 0:

    fig1 = px.scatter(
        scatter_df,
        x="built_up_area",
        y="price",
        color=scatter_df['bedRoom'].astype(str)
    )

    # 🔥 MAIN FIX (markers visible)
    fig1.update_traces(
        mode='markers',
        marker=dict(
            size=8,
            opacity=0.8,
            line=dict(width=1)
        )
    )

    fig1.update_layout(
        template='plotly_white'
    )

    st.plotly_chart(fig1, use_container_width=True)

else:
    st.error("No valid data 🚨")

# ── BHK Pie Chart ──────────────────────────────────────────
st.header('BHK Pie Chart')

sector_options = ['overall'] + sorted(new_df['sector'].dropna().unique().tolist())
selected_sector = st.selectbox('Select Sector', sector_options)

pie_data = new_df if selected_sector == 'overall' else new_df[new_df['sector'] == selected_sector]

fig2 = px.pie(
    pie_data,
    names=pie_data['bedRoom'].astype(str),
    title=f'BHK Distribution — {selected_sector}',
)

st.plotly_chart(fig2, use_container_width=True)

# ── BHK Box Plot ───────────────────────────────────────────
st.header('BHK Price Comparison')

box_df = new_df[new_df['bedRoom'] <= 4]

fig3 = px.box(
    box_df,
    x='bedRoom',
    y='price',
    color=box_df['bedRoom'].astype(str)
)

st.plotly_chart(fig3, use_container_width=True)

# ── KDE Plot ───────────────────────────────────────────────
st.header('Price Distribution')

fig4, ax4 = plt.subplots()

sns.kdeplot(new_df[new_df['property_type'] == 'house']['price'], label='House', fill=True)
sns.kdeplot(new_df[new_df['property_type'] == 'flat']['price'], label='Flat', fill=True)

ax4.legend()
st.pyplot(fig4)

st.header('Sector Value Analysis')

sector_stats = (
    new_df.dropna(subset=['sector', 'price_per_sqft', 'price'])
    .groupby('sector')
    .agg(
        listings=('price', 'count'),
        median_price=('price', 'median'),
        median_price_per_sqft=('price_per_sqft', 'median'),
        median_area=('built_up_area', 'median'),
    )
    .reset_index()
)

min_listings = st.slider(
    'Minimum listings per sector',
    min_value=5,
    max_value=50,
    value=15,
    step=5,
)

sector_stats = sector_stats[sector_stats['listings'] >= min_listings]

if len(sector_stats) > 0:
    affordable_sectors = sector_stats.nsmallest(10, 'median_price_per_sqft')
    premium_sectors = sector_stats.nlargest(10, 'median_price_per_sqft')

    value_col1, value_col2 = st.columns(2)

    with value_col1:
        fig_value = px.bar(
            affordable_sectors.sort_values('median_price_per_sqft'),
            x='median_price_per_sqft',
            y='sector',
            orientation='h',
            color='median_price',
            hover_data=['listings', 'median_area'],
            title='Most Affordable Sectors by Median Price / Sqft',
            labels={
                'median_price_per_sqft': 'Median price / sqft',
                'sector': 'Sector',
                'median_price': 'Median price',
            },
        )
        st.plotly_chart(fig_value, use_container_width=True)

    with value_col2:
        fig_premium = px.bar(
            premium_sectors.sort_values('median_price_per_sqft'),
            x='median_price_per_sqft',
            y='sector',
            orientation='h',
            color='median_price',
            hover_data=['listings', 'median_area'],
            title='Premium Sectors by Median Price / Sqft',
            labels={
                'median_price_per_sqft': 'Median price / sqft',
                'sector': 'Sector',
                'median_price': 'Median price',
            },
        )
        st.plotly_chart(fig_premium, use_container_width=True)
else:
    st.warning('No sectors available for the selected minimum listing count.')

st.header('Luxury Score vs Price')

luxury_df = new_df.dropna(subset=['luxury_score', 'price', 'price_per_sqft']).copy()

if len(luxury_df) > 0:
    luxury_df['luxury_bucket'] = pd.cut(
        luxury_df['luxury_score'],
        bins=[-1, 50, 100, 150, luxury_df['luxury_score'].max()],
        labels=['Basic', 'Comfort', 'Premium', 'Luxury'],
        include_lowest=True,
    )

    fig_luxury = px.box(
        luxury_df,
        x='luxury_bucket',
        y='price',
        color='property_type',
        points='outliers',
        title='How Luxury Score Impacts Property Price',
        labels={
            'luxury_bucket': 'Luxury bucket',
            'price': 'Price in Cr',
            'property_type': 'Property type',
        },
    )
    st.plotly_chart(fig_luxury, use_container_width=True)

st.header('Furnishing Price Impact')

furnishing_df = new_df.dropna(subset=['furnishing_label', 'price_per_sqft', 'price']).copy()

if len(furnishing_df) > 0:
    furnishing_stats = (
        furnishing_df.groupby(['property_type', 'furnishing_label'])
        .agg(
            listings=('price', 'count'),
            median_price=('price', 'median'),
            median_price_per_sqft=('price_per_sqft', 'median'),
        )
        .reset_index()
    )

    fig_furnishing = px.bar(
        furnishing_stats,
        x='furnishing_label',
        y='median_price_per_sqft',
        color='property_type',
        barmode='group',
        hover_data=['listings', 'median_price'],
        title='Median Price / Sqft by Furnishing Type',
        labels={
            'furnishing_label': 'Furnishing type',
            'median_price_per_sqft': 'Median price / sqft',
            'property_type': 'Property type',
        },
    )
    st.plotly_chart(fig_furnishing, use_container_width=True)

st.header('BHK Demand Heatmap')

top_sector_names = (
    new_df['sector']
    .value_counts()
    .head(15)
    .index
    .tolist()
)

heatmap_df = new_df[
    (new_df['sector'].isin(top_sector_names)) &
    (new_df['bedRoom'].between(1, 5))
].copy()

if len(heatmap_df) > 0:
    heatmap_table = heatmap_df.pivot_table(
        index='sector',
        columns='bedRoom',
        values='price_per_sqft',
        aggfunc='median',
    )

    fig_heatmap = px.imshow(
        heatmap_table,
        aspect='auto',
        color_continuous_scale='Viridis',
        title='Median Price / Sqft by Sector and BHK',
        labels={
            'x': 'BHK',
            'y': 'Sector',
            'color': 'Median price / sqft',
        },
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.header('Property Age Price Trend')

age_df = new_df.dropna(subset=['agePossession', 'price_per_sqft', 'price']).copy()

if len(age_df) > 0:
    age_stats = (
        age_df.groupby(['agePossession', 'property_type'])
        .agg(
            listings=('price', 'count'),
            median_price=('price', 'median'),
            median_price_per_sqft=('price_per_sqft', 'median'),
        )
        .reset_index()
    )

    fig_age = px.bar(
        age_stats,
        x='agePossession',
        y='median_price_per_sqft',
        color='property_type',
        barmode='group',
        hover_data=['listings', 'median_price'],
        title='New vs Old Property Pricing',
        labels={
            'agePossession': 'Property age',
            'median_price_per_sqft': 'Median price / sqft',
            'property_type': 'Property type',
        },
    )
    st.plotly_chart(fig_age, use_container_width=True)

app_footer()
