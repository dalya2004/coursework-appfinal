import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("inddata.csv")
#defining the travel columns used in the data 
travel_columns = [
    'Bus (type not known)', 'Car Share', 'Car/Van', 'Cycle',
    'Dedicated School Bus', 'Public Bus Service', 'Taxi', 'Train', 'Walk'
]

# Sidebar Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Sustainability Insights", "Low Sustainability Schools", "Average Transport Mode"]
)

if page == "Overview":
    st.header("School Travel Insights")
    st.subheader("Explore How Students Travel Across the UK")
    st.caption("Explore how students in Leeds travel to school!")

    #dropdown list for user to select school
    school_names = df['School Name'].dropna().unique()
    selected_school = st.selectbox("Select a School", sorted(school_names))
    filtered_df = df[df['School Name'] == selected_school]

    #displays the data
    st.subheader(f"Travel Data for {selected_school}")
    st.write(filtered_df)

    #Checking if the data is available for the selected school
if not filtered_df.empty:
    #Get the travel data for that school 
    travel_counts = filtered_df[travel_columns].iloc[0].dropna()
    total_students = int(travel_counts.sum())

    #Finds the top transport mode
    top_mode = travel_counts.idxmax()
    top_value = int(travel_counts.max())

    #shows key stats using metrics
    st.subheader("Key Stats")
    col1, col2 = st.columns(2)
    col1.metric("Total Students", f"{total_students}")
    col2.metric("Top Transport Mode", f"{top_mode}", f"{top_value} students")
