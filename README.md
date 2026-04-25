# PropVista

PropVista is a smart real estate analytics and recommendation web app built with Streamlit. It helps users estimate property prices, explore market trends, and discover similar apartments through machine learning and interactive visualizations.

## Live App

View the deployed app: https://ayush-yash-propvista.streamlit.app/

## Features

- **Price Predictor**: Estimate property prices using property type, sector, area, bedrooms, bathrooms, furnishing, luxury category, and more.
- **Market Analytics**: Explore price trends, BHK distribution, price-per-square-foot insights, furnishing impact, luxury score analysis, and property age trends.
- **Apartment Recommendations**: Search apartments by location and radius, then discover similar properties using recommendation logic.
- **Interactive Visualizations**: View maps, charts, heatmaps, box plots, pie charts, and distribution graphs.

## Tech Stack

Python, Streamlit, Pandas, NumPy, Scikit-learn, Plotly, Matplotlib, Seaborn, WordCloud

## Screenshots

Add your screenshots in an `assets/` folder and link them here:

```markdown
![Home Page](assets/home.png)
![Price Predictor](assets/price_predictor.png)
![Analytics Dashboard](assets/analytics.png)
![Recommendations](assets/recommendations.png)
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Project Structure

```text
PropVista/
├── Home.py
├── app_style.py
├── requirements.txt
├── pipeline.pkl
├── df.pkl
├── datasets/
└── pages/
    ├── Analysis.py
    ├── Price_Predictor.py
    └── Recommended Appartments.py
```

## How It Works

PropVista uses a trained machine learning pipeline to estimate property prices from user inputs. It also analyzes structured property data to generate visual insights and uses similarity-based recommendation logic to suggest related apartments.
