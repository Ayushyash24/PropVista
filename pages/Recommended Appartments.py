import streamlit as st
import pickle
import pandas as pd
import numpy as np

from app_style import apply_app_style, page_hero


st.set_page_config(page_title="PropVista Recommendations", page_icon="🏠", layout="wide")
apply_app_style()

page_hero(
    "🏠 Apartment Recommendations",
    "Find nearby apartments by location and radius, then compare similar properties from the recommendation model.",
)

location_df = pd.read_pickle('datasets/location_distance.pkl')

cosine_sim1 = pd.read_pickle('datasets/cosine_sim1.pkl')
cosine_sim2 = pd.read_pickle('datasets/cosine_sim2.pkl')
cosine_sim3 = pd.read_pickle('datasets/cosine_sim3.pkl')

def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df


# Test the recommender function using a property name
recommend_properties_with_scores('DLF The Camellias')


st.header('Search By Location And Radius')

selected_location = st.selectbox('Location',sorted(location_df.columns.to_list()))

radius = st.number_input('Radius in Kms')

if st.button('Search'):
    result_ser = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()

    for key, value in result_ser.items():
        st.text(str(key) + " " + str(round(value/1000)) + ' kms')

st.header('Recommend Apartments')
selected_apartment = st.selectbox('Select an apartment',sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_apartment)

    st.dataframe(recommendation_df)
