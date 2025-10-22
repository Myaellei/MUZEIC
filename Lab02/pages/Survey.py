# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("🎧 Music Listening Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# --- Session State for current session entries ---
if "submitted_entries" not in st.session_state:
    st.session_state["submitted_entries"] = []

csv_file = "../data.csv"

# DATA INPUT FORM
with st.form("survey_form"):
    genre = st.text_input("Enter a music genre:")
    minutes = st.number_input("Minutes listened:", min_value=0, step=1)
    submitted = st.form_submit_button("Submit Data")

    if submitted:
        if genre.strip() == "":
            st.error("Please enter a genre name.")
        else:
            # Append the data to the CSV file
            file_exists = os.path.exists(csv_file)
            with open(csv_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Genre", "Minutes"])
                writer.writerow([genre.strip(), minutes])

            # Add entry to session state
            st.session_state["submitted_entries"].append({"Genre": genre.strip(), "Minutes": minutes})

            st.success("Your data has been submitted!")
            st.write(f"You entered: **Genre:** {genre.strip()}, **Minutes:** {minutes}")

# Show session entries
if st.session_state["submitted_entries"]:
    st.subheader("Your current session entries:")
    st.dataframe(pd.DataFrame(st.session_state["submitted_entries"]))

# DATA DISPLAY
st.divider()
st.header("Current Data in CSV")

if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    csv_data = pd.read_csv(csv_file)
    st.dataframe(csv_data)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
    csv_data = pd.DataFrame(columns=["Genre", "Minutes"])
