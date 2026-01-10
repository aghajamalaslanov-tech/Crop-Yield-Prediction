import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. YOL TƏYİNİ (Sənin köhnə xətalı yollarını bu əvəz edir)
# Bu hissə həm GitHub-da, həm Codespace-də avtomatik işləyir
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "prediction.csv")
model_path = os.path.join(current_dir, "model.pkl")

# SVG şəkli bir pillə yuxarıdadır (root folder)
parent_dir = os.path.dirname(current_dir)
diagram_path = os.path.join(parent_dir, "data_diagram.svg")

# 2. SƏHİFƏ AYARLARI
st.set_page_config(page_title="Crop Yield Dashboard", page_icon="🌾", layout="wide")

# 3. DATA YÜKLƏMƏ FUNKSİYASI
@st.cache_data
def load_data():
    if os.path.exists(csv_path):
        data = pd.read_csv(csv_path)
        if 'Unnamed: 0' in data.columns:
            data = data.drop(columns=['Unnamed: 0'])
        return data
    return None

df = load_data()

# 4. MODEL YÜKLƏMƏ FUNKSİYASI
@st.cache_resource
def load_model():
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    return None

model = load_model()

# --- ƏGƏR DATA TAPILMAZSA STOP ---
if df is None:
    st.error(f"❌ Dataset tapılmadı! Axtarılan yer: {csv_path}")
    st.info("Zəhmət olmasa CSV faylının 'streamlit_app' qovluğunda olduğunu yoxlayın.")
    st.stop()

# --- SIDEBAR & NAVİGASİYA (Sənin kodların) ---
st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to:", ["Project Overview", "Data Exploration", "Yield Prediction"])

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

# --- ANA SƏHİFƏLƏR ---
if page == "Project Overview":
    st.title("🌾 Crop Yield Prediction Dashboard")
    st.markdown("### 🎯 Project Mission...")
    
    # Şəkli dinamik yolla yükləyirik
    if os.path.exists(diagram_path):
        st.image(diagram_path, caption="System Architecture")
    else:
        st.warning("Diagram faylı tapılmadı.")

elif page == "Data Exploration":
    st.title("📊 Data Exploration")
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        sns.lineplot(data=filtered_df, x='Year', y='hg/ha_yield', hue='Item', ax=ax)
        st.pyplot(fig)
    with col2:
        st.write(filtered_df.head(10))

elif page == "Yield Prediction":
    if model is None:
        st.error("Model faylı (model.pkl) tapılmadı!")
    else:
        st.title("🤖 Prediction Sandbox")
        with st.form("prediction_form"):
            # Sənin form kodların bura gəlir...
            # (Country, Crop, Year, Temp, Rain, Pesticides)
            # ...
            if st.form_submit_button("Predict"):
                st.success("Analiz tamamlandı!")