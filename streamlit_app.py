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

