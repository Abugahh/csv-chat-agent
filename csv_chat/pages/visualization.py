import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from models import create_agent

# Set Streamlit Page Configuration
st.set_page_config(page_title="📊 Data Visualization", layout="wide")

# Load the selected dataset from session state
if "files" not in st.session_state or "selected_csv" not in st.session_state:
    st.error("No dataset selected. Please upload a CSV file from the main dashboard.")
    st.stop()

csv_path = st.session_state.files[st.session_state.selected_csv]

# Read the CSV file
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(csv_path)

# Display dataset preview
st.title("📊 Data Visualization Dashboard")
st.write("### Dataset Preview")
st.dataframe(df.head())

# Sidebar for visualization options
st.sidebar.header("Select Visualization Type")
plot_type = st.sidebar.selectbox("Choose a plot type:", [
    "Histogram",
    "Scatter Plot",
    "Box Plot",
    "Correlation Heatmap"
])

# Select columns for plotting
num_cols = df.select_dtypes(include=['number']).columns.tolist()
if plot_type != "Correlation Heatmap":
    x_col = st.sidebar.selectbox("Select X-axis:", num_cols)
    y_col = st.sidebar.selectbox("Select Y-axis:", num_cols) if plot_type != "Histogram" else None

# Generate Visualization
st.write("### 📈 Generated Visualization")
fig, ax = plt.subplots(figsize=(10, 5))

if plot_type == "Histogram":
    sns.histplot(df[x_col], kde=True, ax=ax)
    ax.set_title(f"Histogram of {x_col}")

elif plot_type == "Scatter Plot":
    sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax)
    ax.set_title(f"Scatter Plot: {x_col} vs {y_col}")

elif plot_type == "Box Plot":
    sns.boxplot(x=df[x_col], ax=ax)
    ax.set_title(f"Box Plot of {x_col}")

elif plot_type == "Correlation Heatmap":
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")

st.pyplot(fig)

# Chat Section for AI-Generated Visualizations
st.write("### 💬 AI-Powered Visualization Assistant")
if "agent" not in st.session_state:
    st.session_state.agent = create_agent(csv_path)

user_query = st.text_input("Ask the AI to generate a visualization (e.g., 'Show a bar chart of sales'):")
if st.button("Generate AI Visualization") and user_query:
    response = st.session_state.agent.run(f"Generate a visualization based on this query: {user_query}")
    st.write("#### AI Response:")
    st.write(response)
