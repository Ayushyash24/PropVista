import streamlit as st

from app_style import apply_app_style, feature_card, page_hero


st.set_page_config(page_title="PropVista", page_icon="🏠", layout="wide")
apply_app_style()

page_hero(
    "🏠 PropVista",
    "A smarter way to explore Gurgaon real estate with price prediction, market analytics, and apartment recommendations.",
    "Smart Real Estate Insights",
)

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric("Market Focus", "Gurgaon")

with metric_col2:
    st.metric("Core Tools", "3")

with metric_col3:
    st.metric("Decision Support", "Price + Match")

st.divider()

st.markdown("## Explore The Platform")

col1, col2, col3 = st.columns(3)

with col1:
    feature_card(
        "🏡 Price Predictor",
        "Estimate property prices using sector, property type, BHK, bathrooms, area, furnishing, and luxury category.",
    )

with col2:
    feature_card(
        "📊 Market Analytics",
        "Compare sector pricing, BHK demand, luxury impact, furnishing premium, and Gurgaon price trends visually.",
    )

with col3:
    feature_card(
        "🔎 Apartment Finder",
        "Search apartments by location and radius, then discover similar properties from the recommendation engine.",
    )

st.divider()

st.markdown("## Recommended Flow")

flow_col1, flow_col2, flow_col3 = st.columns(3)

with flow_col1:
    feature_card(
        "1. Study The Market",
        "Start with Analytics to understand sector prices, popular BHK types, and premium locations.",
    )

with flow_col2:
    feature_card(
        "2. Predict A Price",
        "Use Price Predictor when you have a specific property profile and want an estimated value.",
    )

with flow_col3:
    feature_card(
        "3. Find Similar Homes",
        "Use Recommendations to compare nearby or similar apartments before shortlisting options.",
    )

st.info("🏠 Use the sidebar to open Price Predictor, Analytics, or Recommended Appartments.")
