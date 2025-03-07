import streamlit as st
import pandas as pd
import os
import tempfile
from models import create_agent

# Streamlit App Configuration
st.set_page_config(page_title="AI-Powered CSV Explorer", layout="wide")

# Function to handle Excel files and convert to CSV
def convert_excel_to_csv(uploaded_file):
    try:
        excel_df = pd.read_excel(uploaded_file)
        if excel_df.empty:
            st.error(f"Error: The uploaded Excel file '{uploaded_file.name}' is empty.")
            return None
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        excel_df.to_csv(temp_file.name, index=False)
        return temp_file.name
    except Exception as e:
        st.error(f"Failed to convert Excel file: {e}")
        return None

# Function to handle encoding errors and check empty CSV files
def safe_read_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error(f"Error: The uploaded file '{uploaded_file.name}' is empty or has no columns.")
            return None
        return df
    except UnicodeDecodeError:
        return pd.read_csv(uploaded_file, encoding="ISO-8859-1")
    except pd.errors.EmptyDataError:
        st.error(f"Error: The uploaded file '{uploaded_file.name}' is empty or corrupted.")
        return None
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return None

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
        csv_files = {}
        for file in uploaded_files:
            if file.name.endswith(".xlsx"):
                csv_filename = convert_excel_to_csv(file)
                if csv_filename:
                    csv_files[file.name] = csv_filename
            else:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
                temp_file.write(file.getvalue())
                temp_file.close()
                csv_files[file.name] = temp_file.name
        
        if csv_files:
            st.session_state.files = csv_files
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("No valid files were uploaded. Please upload non-empty CSV or Excel files.")

# Dashboard Page
elif st.session_state.page == "dashboard":
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to:", ["📊 Visualization", "🌍 Geospatial Map", "📂 Multiple CSVs"], index=0)
    
    st.sidebar.header("📂 Uploaded CSV Files")
    dfs = {}
    for filename, file in st.session_state.files.items():
        df = safe_read_csv(file)
        if df is not None:
            dfs[filename] = df
            st.sidebar.write(f"✅ {filename}")
    
    selected_csv = st.sidebar.selectbox("Select a primary dataset for analysis", options=list(dfs.keys()) if dfs else [None])
    
    if selected_csv and selected_csv in dfs:
        df_main = dfs[selected_csv]
        
        # Ensure the file is not empty before passing to the agent
        if df_main.empty:
            st.error("The selected dataset is empty. Please upload a valid CSV file.")
        else:
            csv_path = st.session_state.files[selected_csv]  # Get temporary file path
            agent = create_agent(csv_path)  # Pass file path
            summary_text = agent.run("Summarize this dataset in one paragraph.")
            
            st.write(f"### 📄 {selected_csv} - Dataset Overview")
            st.write(summary_text)
            st.dataframe(df_main.head())
            
            #Navigation logic for different components
            if page == "📊 Visualization":
                st.switch_page("pages/visualization.py")
            elif page == "🌍 Geospatial Map":
                st.switch_page("pages/geospatial.py")
            elif page == "📂 Multiple CSVs":
                st.switch_page("pages/multiple_csvs.py")
    else:
        st.write("Upload a CSV to get started!")