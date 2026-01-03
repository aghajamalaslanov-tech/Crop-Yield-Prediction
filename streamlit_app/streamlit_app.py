import streamlit as st
import pandas as pd

st.title("Crop Yield Explorer")

# load dataset (adjust path if needed)
df = pd.read_csv("data_preparation/crop_yield_prediction_with_weather.csv")

st.header("Data preview")
st.dataframe(df.head())

col = st.sidebar.selectbox("Select numeric column to plot", df.select_dtypes("number").columns)
st.header(f"{col} over rows")
st.line_chart(df[col])