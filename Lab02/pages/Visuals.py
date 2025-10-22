# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="🎧 Music Listening Visuals",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")

csv_file = "../data.csv"
json_file = "../data.json"

# DATA LOADING
st.divider()
st.header("Load Data")

if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    csv_data = pd.read_csv(csv_file)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
    csv_data = pd.DataFrame(columns=["Genre", "Minutes"])

try:
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file, "r") as f:
            json_data = json.load(f)
            json_df = pd.DataFrame(json_data)
    else:
        st.warning("The 'data.json' file is empty or does not exist yet.")
        json_df = pd.DataFrame(columns=["Genre", "Minutes"])
except Exception as e:
    st.error(f"Error loading JSON: {e}")
    json_df = pd.DataFrame(columns=["Genre", "Minutes"])

st.success("Data loaded successfully!")

# Display your data for confirmation
st.subheader("CSV Data Preview")
st.dataframe(csv_data)

st.subheader("JSON Data Preview")
st.dataframe(json_df)

# GRAPH CREATION
st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Average Minutes per Genre")  # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("This static bar chart shows how much time you spend listening to each genre.")
st.bar_chart(csv_data, x="Genre", y="Minutes")  # STATIC GRAPH using CSV

# GRAPH 2: DYNAMIC GRAPH
st.subheader("Filter Genres")  # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("Use the dropdown below to select which genres to display.")  # NEW

# --- Session state for selected genres --- #NEW
if "selected_genres" not in st.session_state:
    st.session_state.selected_genres = json_df["Genre"].unique().tolist() if not json_df.empty else []

selected_genres = st.multiselect(
    "Select genres to view:",
    options=json_df["Genre"].unique() if not json_df.empty else [],
    default=st.session_state.selected_genres
)
st.session_state.selected_genres = selected_genres  # store selection in session state

filtered_json = json_df[json_df["Genre"].isin(selected_genres)]
if not filtered_json.empty:
    fig2 = px.bar(filtered_json, x="Genre", y="Minutes", color="Genre", title="Minutes Listened by Selected Genres")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No genres selected.")

# GRAPH 3: DYNAMIC GRAPH
st.subheader("Listening Comparisons")  # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("This dynamic line chart shows listening trends. Use the slider to adjust how much data is shown.")  # NEW

# --- Session state for slider --- #NEW
if "genre_limit" not in st.session_state:
    st.session_state.genre_limit = len(csv_data)

limit = st.slider(
    "Select how many genres to display:", 
    min_value=1, 
    max_value=max(1, len(csv_data)), 
    value=st.session_state.genre_limit  # NEW
)
st.session_state.genre_limit = limit  # store selection in session state

fig3 = px.line(
    csv_data.head(limit), 
    x="Genre", 
    y="Minutes", 
    markers=True, 
    title="Listening Trend by Genre"
)
st.plotly_chart(fig3, use_container_width=True)
