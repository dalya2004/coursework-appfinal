import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("inddata.csv")
#defining the travel columns used in the data 
travel_columns = [
    'Bus (type not known)', 'Car Share', 'Car/Van', 'Cycle',
    'Dedicated School Bus', 'Public Bus Service', 'Taxi', 'Train', 'Walk'
]
#this does the caculations for my eco friendly scores 
df['Eco-Friendly %'] = (df[['Walk', 'Cycle']].sum(axis=1) / df[travel_columns].sum(axis=1)) * 100
df['Eco-Friendly %'] = df['Eco-Friendly %'].fillna(0)

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
        # Get the travel data for that school 
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

        # Get the travel counts once
        existing_columns = [col for col in travel_columns if col in filtered_df.columns]
        if existing_columns:
            travel_counts = filtered_df[existing_columns].iloc[0].dropna().sort_values(ascending=False)

            #radio button for user option into which chart to select
            chart_type = st.radio("Select chart type:", ['Bar Chart', 'Pie Chart'])

            if chart_type == "Bar Chart":
                st.subheader("Student Travel - Bar Chart")
                st.bar_chart(travel_counts)

            elif chart_type == "Pie Chart":
                st.subheader("Student Travel - Pie Chart")
                total = travel_counts.sum()
                percentages = (travel_counts / total) * 100
                main_slices = travel_counts[percentages > 2]
                other = travel_counts[percentages <= 2].sum()
                if other > 0:
                    main_slices["Other"] = other

                if len(main_slices) < 2:
                    st.warning("Not enough data to display a pie chart. Try another school.")
                else:
                    fig, ax = plt.subplots()
                    ax.pie(
                        main_slices,
                        labels=main_slices.index,
                        autopct='%1.1f%%',
                        startangle=90,
                        #adgusted so user can read this without them overlapping
                        textprops={'fontsize': 8},
                        labeldistance=1.2,
                        pctdistance=0.9,
                        wedgeprops={'width': 0.95}
                    )
                    ax.axis('equal')
                    st.pyplot(fig)
        else:
            st.warning("No transport data available to display.")
#2nd page begings
elif page == "Sustainability Insights":
    #header for 2nd page
    st.header("Sustainability Insights Across Leeds")

    #most sustainable school
    most_sustainable_school = df.loc[df['Eco-Friendly %'].idxmax()]
    school_name = most_sustainable_school['School Name']
    eco_percent = most_sustainable_school['Eco-Friendly %']

    st.subheader("Most Sustainable School")
    st.success(f"**{school_name}** leads the way with **{eco_percent:.1f}%** of students walking or cycling to school.")

    #top 3 eco friendly schools
    top_3_eco = df[['School Name', 'Eco-Friendly %']].sort_values(by='Eco-Friendly %', ascending=False).head(3)
    top_3_eco = top_3_eco.reset_index(drop=True)
    #making it starts from 1 instead of 0 (problem found during testing)
    top_3_eco.index += 1 
    #naming the column rank
    top_3_eco.index.name = 'Rank'
    
    
    st.subheader("Top 3 Eco-Friendly Schools")
    st.dataframe(top_3_eco)
    #bar chart for ecofriendly schools
    bar_chart_data = top_3_eco.copy().set_index('School Name')
    st.bar_chart(bar_chart_data['Eco-Friendly %'])

    #slider for user to be able to filter the schools with certain eco friendly %
    st.subheader("Filter Schools by Eco-Friendly % Range")

    min_percent, max_percent = st.slider(
    "Please select Eco-Friendly % Range",
    0, 100, (0, 100)
)
    #filtering the data frame based on the slider 
    filtered_schools = df[(df['Eco-Friendly %'] >= min_percent) & (df['Eco-Friendly %'] <= max_percent)]

    st.write(f"Showing schools with Eco-Friendly % between {min_percent}% and {max_percent}%:")

    if not filtered_schools.empty:
        st.dataframe(filtered_schools[['School Name', 'Eco-Friendly %']].sort_values(by='Eco-Friendly %', ascending=False).reset_index(drop=True))
    else:
        st.info("No schools found in this range.")


    #sustainable vs non sustainable schools 
    sustainable = df[df['Eco-Friendly %'] > 50]
    non_sustainable = df[df['Eco-Friendly %'] <= 50]

    st.subheader("Sustainable vs Non-Sustainable Schools")
    col1, col2 = st.columns(2)
    col1.metric("Sustainable Schools", len(sustainable))
    col2.metric("Non-Sustainable Schools", len(non_sustainable))

    avg_eco = df['Eco-Friendly %'].mean()
    st.info(f"**Average eco-friendly travel rate across all Leeds schools:** {avg_eco:.1f}%")

#third page: Low Sustainability Schools
elif page == "Low Sustainability Schools":
    st.header("Low Sustainability Schools")

    low_threshold = 30 #my threshhold for low sustainability
    low_sustain = df[df['Eco-Friendly %'] < low_threshold].copy()

    if not low_sustain.empty:
        st.warning(f"These schools have less than {low_threshold}% of students walking or cycling to school.")

        #gives user the option to view all or just the bottom 5
        view_option = st.radio("Display Options", ["All Low-Sustainability Schools", "Bottom 5 Only"], horizontal=True)

        if view_option == "Bottom 5 Only":
            low_sustain = low_sustain.sort_values(by='Eco-Friendly %').head(5)

        #displays table
        st.subheader("Low Sustainability Schools List")
        st.dataframe(low_sustain[['School Name', 'Eco-Friendly %']].reset_index(drop=True))

        #bar chart for visualisation
        st.subheader("Lowest Eco-Friendly Rates")
        st.bar_chart(low_sustain.set_index('School Name')['Eco-Friendly %'])
    else:
        st.success("No schools fall below the threshhold, (adgust threshold)")

#4th page: Average Transport Mode
elif page == "Average Transport Mode":
    st.header("Average Transport Mode Across All Schools")
    #description of page
    st.caption("This page explores the average student travel modes across all Leeds schools.")

    #my average calculation 
    avg_transport = df[travel_columns].mean().sort_values(ascending=False)

    st.subheader("Average Student Travel Mode Distribution")
    #bar chart based on the avergage calc 
    st.bar_chart(avg_transport)

    if st.checkbox("Show as Pie Chart"):
        #grouping small slices into 'other"
        total = avg_transport.sum()
        percentages = (avg_transport / total) * 100
        #Keeping only slices >3%
        main_slices = avg_transport[percentages > 3] 
        other = avg_transport[percentages <= 3].sum()
        if other > 0:
            main_slices["Other"] = other

        fig, ax = plt.subplots(figsize=(9, 9))
        ax.pie(
            main_slices,
            labels=main_slices.index,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10},
            labeldistance=1.2,
            wedgeprops={'width': 0.95}
        )
        ax.axis('equal')
        st.pyplot(fig)

    most_popular = avg_transport.idxmax()
    least_popular = avg_transport.idxmin()

    st.subheader("Most and Least Popular Transport Modes")
    st.success(f"The most popular mode of transport is **{most_popular}**.")
    st.warning(f"The least popular mode of transport is **{least_popular}**.")

