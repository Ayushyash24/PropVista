import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os

from app_style import apply_app_style, page_hero

st.set_page_config(page_title="Real Estate Price Predictor", page_icon="🏠", layout="wide")

apply_app_style()

page_hero(
    "🏠 Price Predictor",
    "Estimate property prices from location, area, rooms, furnishing, luxury category, and floor profile.",
)

# ============================================================================
# LOAD PIPELINE AND REFERENCE DATA
# ============================================================================

# Get the directory of the parent folder (where pipeline.pkl and df.pkl are stored)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
PIPELINE_PATH = os.path.join(PARENT_DIR, 'pipeline.pkl')
DATA_PATH = os.path.join(PARENT_DIR, 'df.pkl')

@st.cache_resource
def load_pipeline():
    """Load the pre-trained pipeline"""
    try:
        # Use joblib instead of pickle
        pipeline = joblib.load(PIPELINE_PATH)
        return pipeline
    except FileNotFoundError:
        st.error(f"❌ Error: pipeline.pkl not found at {PIPELINE_PATH}!")
        st.info(f"Make sure pipeline.pkl exists at: {PIPELINE_PATH}")
        return None
    except Exception as e:
        st.error(f"❌ Error loading pipeline: {e}")
        return None

@st.cache_resource
def load_reference_data():
    """Load the reference dataframe for unique values"""
    try:
        import pickle
        with open(DATA_PATH, 'rb') as file:
            df = pickle.load(file)
        return df
    except Exception as e:
        st.error(f"Error loading reference data: {e}")
        return None

# Load data
pipeline = load_pipeline()
df_reference = load_reference_data()

if pipeline is None or df_reference is None:
    st.stop()

# ============================================================================
# SIDEBAR: USER INPUTS
# ============================================================================

st.sidebar.header("🏢 Property Details")
st.sidebar.markdown("Enter the property information below")

# Property Type
property_type = st.sidebar.selectbox(
    'Property Type',
    options=['flat', 'house'],
    help="Select the type of property"
)

# Sector
sector = st.sidebar.selectbox(
    'Sector',
    options=sorted(df_reference['sector'].unique().tolist()),
    help="Select the sector"
)

# Bedrooms
bedrooms = float(st.sidebar.selectbox(
    'Number of Bedrooms',
    options=sorted(df_reference['bedRoom'].unique().tolist()),
    help="Select number of bedrooms"
))

# Bathrooms
bathroom = float(st.sidebar.selectbox(
    'Number of Bathrooms',
    options=sorted(df_reference['bathroom'].unique().tolist()),
    help="Select number of bathrooms"
))

# Balcony
balcony = st.sidebar.selectbox(
    'Balconies',
    options=sorted(df_reference['balcony'].unique().tolist()),
    help="Select number of balconies"
)

# Property Age
property_age = st.sidebar.selectbox(
    'Property Age',
    options=sorted(df_reference['agePossession'].unique().tolist()),
    help="Select property age/possession status"
)

# Built Up Area
built_up_area = float(st.sidebar.number_input(
    'Built Up Area (sq ft)',
    min_value=500.0,
    max_value=10000.0,
    value=2000.0,
    step=100.0,
    help="Enter the built-up area in square feet"
))

# Servant Room
servant_room = float(st.sidebar.selectbox(
    'Servant Room',
    options=[0.0, 1.0],
    help="Does property have a servant room?"
))

# Store Room
store_room = float(st.sidebar.selectbox(
    'Store Room',
    options=[0.0, 1.0],
    help="Does property have a store room?"
))

# Furnishing Type
furnishing_type = st.sidebar.selectbox(
    'Furnishing Type',
    options=sorted(df_reference['furnishing_type'].unique().tolist()),
    help="Select the furnishing type"
)

# Luxury Category
luxury_category = st.sidebar.selectbox(
    'Luxury Category',
    options=sorted(df_reference['luxury_category'].unique().tolist()),
    help="Select the luxury category"
)

# Floor Category
floor_category = st.sidebar.selectbox(
    'Floor Category',
    options=sorted(df_reference['floor_category'].unique().tolist()),
    help="Select the floor category"
)

# ============================================================================
# PREDICTION
# ============================================================================

if st.sidebar.button('🔮 Predict Price', use_container_width=True):
    
    # Create DataFrame with input values
    input_data = pd.DataFrame({
        'property_type': [property_type],
        'sector': [sector],
        'bedRoom': [bedrooms],
        'bathroom': [bathroom],
        'balcony': [balcony],
        'agePossession': [property_age],
        'built_up_area': [built_up_area],
        'servant room': [servant_room],
        'store room': [store_room],
        'furnishing_type': [furnishing_type],
        'luxury_category': [luxury_category],
        'floor_category': [floor_category]
    })
    
    try:
        # IMPORTANT: The pipeline includes preprocessing (scaling, encoding)
        # So we pass raw input values directly - the pipeline handles transformation
        prediction_log = pipeline.predict(input_data)[0]
        
        # Convert from log scale back to original price (in crores)
        # The target was log-transformed, so we use expm1 to reverse it
        predicted_price = np.expm1(prediction_log)
        
        # Calculate confidence interval (±22% based on your original code)
        lower_bound = predicted_price * (1 - 0.22)
        upper_bound = predicted_price * (1 + 0.22)
        
        # ============================================================================
        # DISPLAY RESULTS
        # ============================================================================
        
        st.success("✅ Prediction Complete!")
        
        # Main prediction display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🏷️ Predicted Price",
                value=f"₹ {predicted_price:.2f} Cr",
            )
        
        with col2:
            st.metric(
                label="📊 Price Range",
                value=f"₹ {lower_bound:.2f} - {upper_bound:.2f} Cr",
            )
        
        with col3:
            st.metric(
                label="📐 Price per Sq Ft",
                value=f"₹ {(predicted_price * 10000000) / built_up_area:,.0f}",
            )
        
        # Detailed summary
        st.subheader("📋 Input Summary")
        
        summary_data = {
            'Property Type': property_type,
            'Sector': sector,
            'Bedrooms': int(bedrooms),
            'Bathrooms': int(bathroom),
            'Balconies': balcony,
            'Built-up Area': f"{int(built_up_area)} sq ft",
            'Property Age': property_age,
            'Servant Room': '✓' if servant_room == 1.0 else '✗',
            'Store Room': '✓' if store_room == 1.0 else '✗',
            'Furnishing': furnishing_type,
            'Luxury Category': luxury_category,
            'Floor Category': floor_category
        }
        
        summary_df = pd.DataFrame(list(summary_data.items()), columns=['Feature', 'Value'])
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        # Show input dataframe (for debugging)
        with st.expander("🔍 Debug: Raw Input Data"):
            st.dataframe(input_data, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Prediction Error: {str(e)}")
        st.info("Make sure all inputs are valid and match the training data format")

# ============================================================================
# INFO SECTION
# ============================================================================

with st.expander("ℹ️ About This Model"):
    st.markdown("""
    **Model Details:**
    - Type: Scikit-learn Pipeline with preprocessing
    - Algorithm: Gradient Boosting / XGBoost
    - Training Data: Real estate market
    - Target: Property price (log-transformed)
    
    **How it works:**
    1. Your inputs are encoded (categorical) and scaled (numerical)
    2. The trained model predicts log-transformed price
    3. The price is converted back to crores (₹ Cr)
    4. A confidence interval (±22%) is calculated
    
    **Features Used:**
    - Property type, sector, bedrooms, bathrooms, balconies
    - Built-up area, possession age, furnishings
    - Servant room, store room, luxury category, floor
    
    **Limitations:**
    - Predictions based on historical market data
    - Market conditions fluctuate
    - Use as reference, not financial advice
    """)

with st.expander("⚠️ Troubleshooting"):
    st.markdown("""
    **Different predictions in Colab vs Streamlit?**
    - Ensure the same pipeline.pkl is used
    - Check that input data is in the same format
    - Verify preprocessing is applied correctly
    
    **Price seems too high/low?**
    - Check the sector and built-up area
    - Verify property type selection
    - Compare with actual market data
    
    **Missing pipeline.pkl?**
    - Download from Colab using: `joblib.dump(pipeline, 'pipeline.pkl')`
    - Place in the same directory as this script
    """)

st.divider()
st.caption("🏠 Real Estate Price Predictor | Market Analysis")
