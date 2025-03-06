import streamlit as st
import pandas as pd
import os
from models import create_agent

# Streamlit App Configuration
st.set_page_config(page_title="AI-Powered CSV Explorer", layout="wide")

# Function to handle Excel files and convert to CSV
def convert_excel_to_csv(uploaded_file):
    excel_df = pd.read_excel(uploaded_file)
    csv_filename = uploaded_file.name.replace(".xlsx", ".csv")
    excel_df.to_csv(csv_filename, index=False)
    return csv_filename

# Function to handle encoding errors
def safe_read_csv(file):
    try:
        return pd.read_csv(file)
    except UnicodeDecodeError:
        return pd.read_csv(file, encoding="ISO-8859-1")

# Landing Page
if "page" not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.page == "landing":
    st.title("📊 AI-Powered CSV Data Explorer")
    st.write("### Unlock the power of your data effortlessly!")
    st.write(
        "With this tool, you can upload your CSV or Excel files and explore them using AI-powered queries, visualizations, and geospatial mapping. "
        "Simply upload your dataset to get started!"
    )
    
    uploaded_files = st.file_uploader("📂 Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)
    
    if uploaded_files:
        csv_files = []
        for file in uploaded_files:
            if file.name.endswith(".xlsx"):
                csv_filename = convert_excel_to_csv(file)
                csv_files.append(csv_filename)
            else:
                csv_files.append(file)
        
        st.session_state.files = csv_files
        st.session_state.page = "dashboard"
        st.rerun()

# Dashboard Page
elif st.session_state.page == "dashboard":
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to:", ["📊 Visualization", "🗺️ Geospatial Map", "📂 Multiple CSVs"], index=0)
    
    st.sidebar.header("📂 Uploaded CSV Files")
    dfs = {}
    for file in st.session_state.files:
        df = safe_read_csv(file)
        dfs[file if isinstance(file, str) else file.name] = df
        st.sidebar.write(f"✅ {file if isinstance(file, str) else file.name}")
    
    selected_csv = st.sidebar.selectbox("Select a primary dataset for analysis", options=list(dfs.keys()) if dfs else [None])
    
    if selected_csv and selected_csv in dfs:
        df_main = dfs[selected_csv]
        agent = create_agent(selected_csv)
        summary_text = agent.run("Summarize this dataset in one paragraph.")
        
        st.write(f"### 📄 {selected_csv} - Dataset Overview")
        st.write(summary_text)
        st.dataframe(df_main.head())
        
        # Navigation logic for different components
        if page == "📊 Visualization":
            st.switch_page("visualization.py")
        elif page == "🗺️ Geospatial Map":
            st.switch_page("geospatial.py")
        elif page == "📂 Multiple CSVs":
            st.switch_page("multiple_csvs.py")
    else:
        st.write("Upload a CSV to get started!")
