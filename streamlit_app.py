import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="AI/ML Salaries", layout="wide")

hide_deploy = """
<style>
[data-testid="stToolbarActions"] {display:none !important;}
</style>
"""
st.markdown(hide_deploy, unsafe_allow_html=True)

st.title("🤖 AI/ML Salaries Explorer")

st.write("Dataset from Kaggle: AI/ML Salaries")

dataset_path = Path.home() / ".cache/kagglehub/datasets/cedricaubin/ai-ml-salaries/versions/7"

try:
    csv_files = list(dataset_path.glob("*.csv"))
    if csv_files:
        df = pd.read_csv(csv_files[0])

        st.subheader("Dataset Overview")
        st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("First few rows")
            st.dataframe(df.head())

        with col2:
            st.subheader("Data Info")
            st.write(df.dtypes)

        st.subheader("Summary Statistics")
        st.dataframe(df.describe())

        st.subheader("Missing Values")
        st.bar_chart(df.isnull().sum())
    else:
        st.error("No CSV files found in dataset directory")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
