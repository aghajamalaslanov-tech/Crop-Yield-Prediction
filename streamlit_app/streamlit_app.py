import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os


# 1. Fayl yollarını avtomatik təyin etmək
# Bu hissə proqramın öz qovluğunu tapmasını təmin edir
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, 'crop_yield_prediction.csv')
model_path = os.path.join(current_dir, "model.pkl")

# 2. Səhifə konfiqurasiyası
st.set_page_config(page_title="Crop Yield Dashboard", page_icon="🌾", layout="wide")

# 3. Məlumatın yüklənməsi

@st.cache_data
def load_data():
    if os.path.exists(csv_path):
        data = pd.read_csv(csv_path)
        if 'Unnamed: 0' in data.columns:
            data = data.drop(columns=['Unnamed: 0'])
        return data
    return None

df = load_data()

# 4. Modelin yüklənməsi
@st.cache_resource
def load_model():
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    return None

model = load_model()

# --- SIDEBAR & NAV ---
st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to:", ["Project Overview", "Data Exploration", "Yield Prediction"])

if df is not None:
    st.sidebar.divider()
    st.sidebar.header("🌐 Global Filters")
    selected_countries = st.sidebar.multiselect(
        "🌍 Select Countries:", 
        options=sorted(df['Area'].unique().tolist()),
        default=df['Area'].unique()[:3]
    )
    min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
    year_range = st.sidebar.slider("🗓️ Select Year Range:", min_year, max_year, (min_year, max_year))
    
    filtered_df = df[(df['Area'].isin(selected_countries)) & 
                     (df['Year'] >= year_range[0]) & 
                     (df['Year'] <= year_range[1])]
else:
    st.sidebar.error(f"Dataset not found at: {csv_path}")

# --- MAIN CONTENT ---
# PAGE 1: PROJECT OVERVIEW
if page == "Project Overview":
    st.title("🌾 Crop Yield Prediction & Climate Analysis Dashboard")
    st.markdown("""
    ### 🎯 Project Mission
    This project bridges the gap between climate science and agriculture. By analyzing historical yield records alongside temperature and precipitation patterns, we identify key environmental drivers of food production.

    ### 🔑 Key Features:
    * **Data Collection**: Integration of historical yield records and weather API data.
    * **Exploratory Analysis**: Correlation studies between climate fluctuations and productivity.
    * **Machine Learning**: Predictive forecasting using a **Random Forest Regressor**.
    """)
    st.image("data_diagram.svg", caption="System Architecture")

elif page == "Data Exploration":
    if df is not None:
        st.title("📊 Data Exploration")
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            sns.lineplot(data=filtered_df, x='Year', y='hg/ha_yield', hue='Item', ax=ax)
            st.pyplot(fig)
        with col2:
            st.write(filtered_df.head(10))
    else:
        st.error("CSV file is missing!")

elif page == "Yield Prediction":
    if model is None:
        st.error(f"Model file missing! Looking for: {model_path}")
    else:
        st.title("🤖 Prediction Sandbox")
        with st.form("prediction_form"):
            c1, c2 = st.columns(2)
            with c1:
                in_country = st.selectbox("Country:", df['Area'].unique())
                in_item = st.selectbox("Crop:", df['Item'].unique())
                in_year = st.number_input("Year:", value=2026)
            with c2:
                in_temp = st.slider("Temperature (°C):", -10, 35, 20)
                in_rain = st.number_input("Rainfall (mm):", value=1000)
                in_pest = st.number_input("Pesticides (tonnes):", value=100)
            
            if st.form_submit_button("Predict"):
                input_df = pd.DataFrame(columns=model.feature_names_in_)
                input_df.loc[0] = 0
                input_df['Year'], input_df['pesticides_tonnes'] = in_year, in_pest
                input_df['avg_temp'], input_df['total_precip'] = in_temp, in_rain
                
                area_col, item_col = f"Area_{in_country}", f"Item_{in_item}"
                if area_col in input_df.columns: input_df[area_col] = 1
                if item_col in input_df.columns: input_df[item_col] = 1
                
                res = model.predict(input_df)[0]
                st.success(f"### Predicted Yield: {res:,.2f} hg/ha")