import streamlit as st
import pandas as pd

# Streamlit App Configuration
st.set_page_config(page_title="AI-Powered CSV Explorer", layout="wide")

# Landing Page
if "page" not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.page == "landing":
    st.title("📊 AI-Powered CSV Data Explorer")
    st.write("### Unlock the power of your data effortlessly!")
    st.write(
        "With this tool, you can upload your CSV files and explore them using AI-powered queries, visualizations, and geospatial mapping. "
        "Simply upload your dataset to get started!"
    )
    
    uploaded_files = st.file_uploader("📂 Upload CSV Files", type=["csv"], accept_multiple_files=True)
    
    if uploaded_files:
        st.session_state.files = uploaded_files
        st.session_state.page = "dashboard"
        st.experimental_rerun()

# Dashboard Page
elif st.session_state.page == "dashboard":
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to:", ["📊 Visualization", "🗺️ Geospatial Map", "📂 Multiple CSVs"], index=0)
    
    st.sidebar.header("📂 Uploaded CSV Files")
    dfs = {}
    for file in st.session_state.files:
        df = pd.read_csv(file)
        dfs[file.name] = df
        st.sidebar.write(f"✅ {file.name}")
    
    selected_csv = st.sidebar.selectbox("Select a primary dataset for analysis", options=list(dfs.keys()) if dfs else [None])
    
    if selected_csv and selected_csv in dfs:
        df_main = dfs[selected_csv]
        st.write(f"### 📄 {selected_csv} - Dataset Overview")
        st.write(f"**Rows:** {df_main.shape[0]} | **Columns:** {df_main.shape[1]}")
        st.dataframe(df_main.head())
        
        # Navigation logic for different components
        if page == "📊 Visualization":
            st.write("## 📊 Visualization Component (Coming Soon)")
        elif page == "🗺️ Geospatial Map":
            st.write("## 🗺️ Geospatial Map Component (Coming Soon)")
        elif page == "📂 Multiple CSVs":
            st.write("## 📂 Multiple CSV Management (Coming Soon)")
    else:
        st.write("Upload a CSV to get started!")