import streamlit as st
import pandas as pd
from cleaner import clean_data
from io import BytesIO

st.set_page_config(page_title="Smart CSV Cleaner", layout="centered")

st.title("🧼 Smart CSV/Excel Cleaner")
st.markdown("Upload your messy file and get a clean version in seconds!")

uploaded_file = st.file_uploader("📤 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("🔍 Original Data")
        st.dataframe(df.head())

        # Missing value strategy
        fill_option = st.checkbox("Fill missing values instead of removing?", value=True)

        if fill_option:
            fill_value = st.selectbox("Value to fill missing data with:", ["N/A", "0", "Unknown", ""])
        else:
            fill_value = None  # Will be ignored in cleaner.py

        # Clean the data
        cleaned_df, summary = clean_data(df, fill_missing=fill_option, fill_value=fill_value)

        st.subheader("✅ Cleaned Data Preview")
        st.dataframe(cleaned_df.head())

        # Show cleaning summary
        st.markdown(f"""
        ### 🧾 Cleaning Summary:
        - Original rows: `{summary['original_rows']}`
        - Original columns: `{summary['original_cols']}`
        - Rows removed: `{summary['rows_removed']}`
        - Columns removed: `{summary['cols_removed']}`
        """)

        # Convert to CSV and prepare for download
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv_data = convert_df(cleaned_df)

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Oops! Something went wrong: {e}")
