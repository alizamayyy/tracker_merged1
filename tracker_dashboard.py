import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64
import requests

st.set_page_config(layout="wide")

# Load your dataset
file_path = "https://raw.githubusercontent.com/alizamayyy/tracker_merged/main/tracker_merged.csv"

response = requests.get(file_path)
df = pd.read_csv(io.StringIO(response.text))

margins_css = """
    <style>
        .main > div {
            margin-top: -80px;
            text-align: center;
            margin-left: 2px;
        }
    </style>
"""

st.markdown(margins_css, unsafe_allow_html=True)

# Streamlit app title
st.markdown("<h1 style='text-align: center; margin-bottom: 20px'>What Happened in the Span of Two Weeks?</h1>", unsafe_allow_html=True)


sleep_data = df[df['Activity'] == 'sleep']
# Calculate total sleep hours
total_sleep_hours = sleep_data['Duration in Hrs'].sum()
average_sleep_hours = total_sleep_hours / len(sleep_data)

# Filter the DataFrame for "review" activity
study_data = df[df['Activity'].str.contains('review', case=False, na=False)]

# Calculate the total study hours for "review"
total_study_hours = study_data['Duration in Hrs'].sum()

# Calculate the average study hours for "review"
average_study_hours = total_study_hours / len(study_data)

# Filter the DataFrame for "me-time (tiktok and social media)" activity
me_time_data = df[df['Activity'].str.contains('me-time', case=False, na=False)]

# Calculate the total "me-time" hours
total_me_time_hours = me_time_data['Duration in Hrs'].sum()

# Calculate the average "me-time" hours
average_me_time_hours = total_me_time_hours / len(me_time_data)

travel_to_school_data = df[df['Activity'].str.contains('travel to school', case=False, na=False)]
total_travel_to_school_hours = travel_to_school_data['Duration in Hrs'].sum()
average_travel_to_school_hours = total_travel_to_school_hours / len(travel_to_school_data)

# Calculate the total "Travel to Home" hours
travel_to_home_data = df[df['Activity'].str.contains('go home', case=False, na=False)]
total_travel_to_home_hours = travel_to_home_data['Duration in Hrs'].sum()

# Calculate the average "Travel to Home" hours
average_travel_to_home_hours = total_travel_to_home_hours / len(travel_to_home_data)

# Calculate the total "Travel to Home" hours
travel_to_home_data = df[df['Activity'].str.contains('go home', case=False, na=False)]
total_travel_to_home_hours = travel_to_home_data['Duration in Hrs'].sum()

# Filter the data for "Travel to School" and "Go Home" activities
travel_data = df[df['Activity'].str.contains('travel to school', case=False, na=False) | df['Activity'].str.contains('go home', case=False, na=False)]

# Create a word cloud with a fully transparent background
wordcloud = WordCloud(width=600, height=500, background_color='white').generate(' '.join(df['Activity']))

# Convert the WordCloud image to Base64
buffer = io.BytesIO()
plt.figure(figsize=(6, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig(buffer, format='png')
plt.tight_layout(pad=0)
wordcloud_base64 = base64.b64encode(buffer.getvalue()).decode()

c1, c2, c3 = st.columns(3)

# Nested columns in c1
with c1:
    c1_col1, c1_col2 = st.columns([1, 1])

    # Add box shadow with the color fbb1bd and remove the border
    c1_col1.markdown(f"""
        <div style="height: 150px; padding: 20px; border-radius: 20px; background-color: #fbb1bd; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);">
            <div style="text-align: center; margin-top: 20px">
                <h3 style="line-height: 0.3;">Average Sleep:</h3>
                <h4 style="line-height: 0.3;">{average_sleep_hours:.2f} hours</h4>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1_col2.markdown(f"""
        <div style="height: 150px; padding: 20px; border-radius: 20px; background-color: #ff99ac; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);">
            <div style="text-align: center; margin-top: 20px">
                <h3 style="line-height: 0.3;">Average Study:</h3>
                <h4 style="line-height: 0.3;">{average_study_hours:.2f} hours</h4>
            </div>
        </div>
    """, unsafe_allow_html=True)


# Add the Location Check pie chart in a new row
with c1:
    st.markdown("<h3 style='text-align: center; margin-top: 20px'>Location Check</h3>", unsafe_allow_html=True)
    location_counts = df['Location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Count']
    
    # Define a custom color palette
    custom_colors = ['#EC0B43', '#fbb1bd', '#58355E', '#D6FFB7', '#ff5c8a', '#FFF689']
    
#     EC0B43
# 58355E
# 7AE7C7
# D6FFB7
# FFF689
    
    location_fig = px.pie(
        location_counts,
        names='Location',
        values='Count',
        title='',
        color_discrete_sequence=custom_colors  # Set the custom color palette
    )
    location_fig.update_layout(
        title_text='Where We Spend Portions of Our Time',
        title_x=0.28,
        title_y=0.99,
        height=400,  # Set the height of the chart (in pixels)
        width=300,  # Set the width of the chart (in pixels)
    )
    st.plotly_chart(location_fig, use_container_width=True)
    

# Nested columns in c2
c2_col1, c2_col2 = c2.columns([1, 1])

# Add box shadow with the color fbb1bd and remove the border
c2_col1.markdown(f"""
    <div style="height: 150px; padding: 20px; border-radius: 20px; background-color: #ff7096; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);">
        <div style="text-align: center; margin-top: 1px">
            <h3 style="line-height: 1;">Average Travel to School:</h3>
            <h4 style="line-height: 0;">{average_travel_to_school_hours:.2f} hours</h4>
        </div>
    </div>
""", unsafe_allow_html=True)

c2_col2.markdown(f"""
    <div style="height: 150px; padding: 20px; border-radius: 20px; background-color: #ff5c8a; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);">
        <div style="text-align: center; margin-top: 1px">
            <h3 style="line-height: 1;">Average Travel to Home:</h3>
            <h4 style="line-height: 0;">{average_travel_to_home_hours:.2f} hours</h4>
        </div>
    </div>
""", unsafe_allow_html=True)

# Add the Feelings in a Pie chart in a new row
with c2:
    st.markdown("<h3 style='text-align: center; margin-top: 20px; margin-bottom: -10px'>Time of Sleep per Day</h3>", unsafe_allow_html=True)
    # Display the first "Sleep Check" chart
    df['Date'] = pd.to_datetime(df['Date'])
    # Display the "Sleep Time per Day" chart for Aliza, John, and Xianna
    sleep_data_individuals = df[df['Activity'] == 'sleep']

    # Combine all sleep charts into one with different colors and a legend
    sleep_fig_combined = px.line(
        sleep_data_individuals,
        x='Date',
        y='Time',
        color='Name',
        title='What time did we sleep per day?',
        line_shape='linear',  # Set the line shape to 'linear' for solid lines
        labels={'Time': 'Sleep Time'},
        color_discrete_sequence=['#ff477e', 'blue', 'red']  # Add your desired colors for the second and third person
    )

    # Customize the layout
    sleep_fig_combined.update_layout(
        title_x=0.30,
        title_y=0.99,# Center the title
        height=400,  # Set the height of the chart (in pixels)
        width=800,   # Set the width of the chart (in pixels)
        legend=dict(orientation='h', y=1.2, x=0.55),  # Move the legend below (horizontal orientation)
        xaxis=dict(
            tickmode='linear',
            tickvals=pd.date_range(start='2023-10-09', end='2023-10-23', freq='D').tolist(),
            tickformat="%Y-%m-%d"
        )
    )

    # Display the combined sleep chart
    st.plotly_chart(sleep_fig_combined, use_container_width=True)
    
        # Specific dates from 10/09/2023 to 10/23/2023
    specific_dates = pd.date_range(start='2023-10-09', end='2023-10-23')

    # Filter the data for the "Go Home" and "Travel" activities
    go_home_data = df[df['Activity'].str.contains('go home', case=False, na=False)]
    travel_data = df[df['Activity'].str.contains('travel', case=False, na=False)]

    # Extract the common dates from both datasets
    common_dates = set(go_home_data['Date']).intersection(set(travel_data['Date']))

        # Display the "Hours of Commute per School Day" grouped bar chart with names
    commute_data = df[df['Activity'].str.contains('go home|travel', case=False, na=False)]

    # Specific dates from 10/09/2023 to 10/23/2023
    specific_dates = pd.date_range(start='2023-10-09', end='2023-10-23')

    # Filter the data for commute activities
    commute_data = commute_data[commute_data['Date'].isin(common_dates) | commute_data['Date'].isin(specific_dates)]

    
    # Create two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='text-align: center; margin-top: 20px'>Hours of Sleep per Day</h3>", unsafe_allow_html=True)
    sleep_bar_fig_grouped = px.bar(
        sleep_data,
        x='Date',
        y='Duration in Hrs',
        color='Name',
        title='Hours many hours did we spend sleeping per day?',
        labels={'Duration in Hrs': 'Hours'},
        color_discrete_sequence=['#ff477e', 'blue', 'red']
    )
    sleep_bar_fig_grouped.update_layout(
        xaxis_title='Date',
        yaxis_title='Hours',
        title_x=0.1,  # Set the title position
        title_y=0.89,
        height=500,  # Set the height of the chart (in pixels)
        width=800,   # Set the width of the chart (in pixels)
        barmode='group',  # Set the bar mode to "group"
        xaxis=dict(
            categoryorder='category ascending',  # Display all dates
        ),
        legend=dict(
            orientation='h',  # Horizontal orientation
            y=1.2, x=0.7  # Adjust the y position to move the legend slightly below
        )
    )
    st.plotly_chart(sleep_bar_fig_grouped, use_container_width=False)

# Display the "Hours of Commute per School Day" grouped bar chart in the second column
with col2:
    st.markdown("<h3 style='text-align: center; margin-top: 20px'>Hours of Commute per School Day</h3>", unsafe_allow_html=True)
    fig_commute = px.bar(
        commute_data,
        x='Date',
        y='Duration in Hrs',
        color='Name',
        title='Hours many hours did we spend commuting per day?',
        labels={'Duration in Hrs': 'Hours'},
        color_discrete_sequence=['#ff477e', 'blue', 'red']
    )
    fig_commute.update_layout(
        xaxis=dict(
            categoryorder='category ascending',
            tickvals=specific_dates,
            ticktext=[date.strftime('%m/%d/%Y') for date in specific_dates]
        ),
        xaxis_title='Date',
        yaxis_title='Hours',
        height=500,  # Set the height of the chart (in pixels)
        width=750, 
        title_x=0.1,
        title_y=0.89,# Set the title to the middle
        barmode='group',  # Set the bar mode to "group" for grouped bars
        legend=dict(
            orientation='h',  # Horizontal orientation
            y=1.2, x=0.7  # Adjust the y position to move the legend slightly below
        )
    )
    st.plotly_chart(fig_commute, use_container_width=True)


# Add box shadow with the color fbb1bd and remove the border
c3.markdown(f"""
    <div style="width: 630px; height: 560px; padding: 20px; border-radius: 20px; background-color: white; box-shadow: 5px 5px 10px #EC0B43;">
        <div style="text-align: center; margin-top: 15px">
            <h2 style="line-height: 1; color: #EC0B43; margin-bottom: -50px">Our Activities Word Cloud</h2>
            <img src="data:image/png;base64,{wordcloud_base64}" alt="activity word cloud" />
        </div>
    </div>
""", unsafe_allow_html=True)

c3_col1, c3_col2 = st.columns([1, 1])

c3_col1.markdown("<h2 style='text-align: center; margin-top: 55px; margin-bottom: -10px; margin-left: 300px'>Student-Life Balance</h2>", unsafe_allow_html=True)

# Filter the DataFrame for "me-time (tiktok and social media)" activity for the specific names
me_time_data_individual = df[df['Name'].isin(['Aliza', 'John', 'Xianna']) & df['Activity'].str.contains('me-time', case=False, na=False)]

# Filter the DataFrame for "review" activity
study_data = df[df['Activity'].str.contains('review|class', case=False, na=False)]

# Calculate the total study hours for "review"
total_study_hours = study_data['Duration in Hrs'].sum()

# Filter the DataFrame for "review" activity for the specific names
study_data_individual = df[df['Name'].isin(['Aliza', 'John', 'Xianna']) & df['Activity'].str.contains('review|class', case=False, na=False)]

# Filter the DataFrame for "me-time (tiktok and social media)" activity
me_time_data = df[df['Activity'].str.contains('me-time', case=False, na=False)]

# Calculate the total "me-time" hours
total_me_time_hours = me_time_data['Duration in Hrs'].sum()

# Values for the pie chart
values = [total_study_hours, total_me_time_hours]

# Create a pie chart with custom colors and move the legend below
fig = go.Figure(data=[go.Pie(labels=['Student Life', 'Me-time'], values=values, marker=dict(colors=['#EC0B43', '#fbb1bd']))])

# Calculate the percentages
percentages = [f'{val / sum(values) * 100:.2f}%' for val in values]

# Set the height and width of the pie charts
chart_height = 400
chart_width = 600

# Create three columns
col1, col2, col3 = st.columns(3)

# Column 1: Me-time Distribution
with col1:
    st.markdown("<h3 style='text-align: center; margin-top: 55px; margin-bottom: -10px; margin-left: 15px'>Me-time Distribution</h3>", unsafe_allow_html=True)
    fig_me_time_comparison = px.pie(
        me_time_data_individual,
        names='Name',
        title='Me-time of Each Student',
        color='Name',
        color_discrete_map={'Aliza': '#ff85a1', 'John': 'blue', 'Xianna': 'red'},  # Different colors for each name
    )
    fig_me_time_comparison.update_layout(
         title_y=0.99,
        title_x=0.36,   # Center the title
        height=chart_height,  # Set the height of the chart (in pixels)
        width=chart_width,  # Set the width of the chart (in pixels)
        legend=dict(orientation='h', y=-0.2, x=0.3),  # Move the legend below (horizontal orientation)
    )
    fig_me_time_comparison.update_traces(textinfo='percent+label', textfont_size=14)
    st.plotly_chart(fig_me_time_comparison, use_container_width=True)

# Column 2: Student Life Distribution
with col2:
    st.markdown("<h3 style='text-align: center; margin-top: 55px; margin-bottom: -10px'>Student Life Distribution</h3>", unsafe_allow_html=True)
    fig_student_life_comparison = px.pie(
        study_data_individual,
        names='Name',
        title='Student Life of Each Student',
        color='Name',
        color_discrete_map={'Aliza': '#ff85a1', 'John': 'blue', 'Xianna': 'red'},  # Different colors for each name
    )
    fig_student_life_comparison.update_layout(
        title_y=0.99,
        title_x=0.31,  # Center the title
        height=chart_height,  # Set the height of the chart (in pixels)
        width=chart_width,  # Set the width of the chart (in pixels)
        legend=dict(orientation='h', y=-0.2, x=0.3),  # Move the legend below (horizontal orientation)
    )
    fig_student_life_comparison.update_traces(textinfo='percent+label', textfont_size=14)
    st.plotly_chart(fig_student_life_comparison, use_container_width=True)

# Column 3: Feelings Distribution
with col3:
    st.markdown("<h3 style='text-align: center; margin-top: 55px'>Feelings Distribution</h3>", unsafe_allow_html=True)
    feelings_counts = df['Feelings'].value_counts().reset_index()
    feelings_counts.columns = ['Feelings', 'Count']
    top_6_feelings = feelings_counts.head(6)
    feelings_fig = px.pie(
        top_6_feelings,
        names='Feelings',
        values='Count',
        title='How We Felt From Time to Time',
        color_discrete_sequence=custom_colors  # Set the custom color palette
    )
    feelings_fig.update_layout(
        title_y=0.99,
        title_x=0.3,  # Center the title
        height=600,  # Set the height of the chart (in pixels)
        width=600,  # Set the width of the chart (in pixels)
        legend=dict(orientation='h', x=0.1),  # Center the legend below (horizontal orientation)
    )
    feelings_fig.update_traces(textinfo='percent', textfont_size=14)
    st.plotly_chart(feelings_fig, use_container_width=True)

# # Below Columns 1 and 2: Hours Being Me
# with col1:
#     st.markdown("<h3 style='text-align: center; margin-top: 55px'>Hours Being Me and a Student</h3>", unsafe_allow_html=True)
#     fig_hours_being_me = go.Figure(data=[go.Pie(labels=['Student Life', 'Me-time'], values=values, marker=dict(colors=['#EC0B43', '#fbb1bd']))])
#     fig_hours_being_me.update_layout(
#         title='Hours Being Me and a Student',
#         title_x=0.5,  # Center the title
#         height=600,  # Set the height of the chart (in pixels)
#         width=600,  # Set the width of the chart (in pixels)
#         legend=dict(orientation='h', x=0.5, y=-0.2),  # Move the legend below (horizontal orientation)
#     )
#     fig_hours_being_me.update_traces(textinfo='percent', textfont_size=14)
#     st.plotly_chart(fig_hours_being_me, use_container_width=True, style={'margin-left': '150px'})
    
# Create two columns for the layout
col1, col2 = st.columns([1, 1])

# Below Columns 1: Div
with col1:
    st.markdown("<h3 style='text-align: center; margin-top: -150px; margin-left: 300px'>Time Being Ourselves and Students</h3>", unsafe_allow_html=True)

    # Create the pie chart
    fig_hours_being_me = go.Figure(data=[go.Pie(labels=['Student Life', 'Me-time'], values=values, marker=dict(colors=['#EC0B43', '#fbb1bd']))])

    # Adjust the size and margin of the chart
    fig_hours_being_me.update_layout(
        height=350,  # Set the height of the chart (in pixels)
        width=350,   # Set the width of the chart (in pixels)
        margin=dict(t=0, l=400),
    )

    # Plot the chart inside the iframe
    st.plotly_chart(fig_hours_being_me, use_container_width=True, key="plotly_chart")




# Below Columns 2: Chart
with col2:
    # Encapsulate the div with custom styling
    st.markdown("""
        <div style="margin-left: -1000px;">
        </div>
    """, unsafe_allow_html=True)






# Define your custom color palette
custom_colors = ["#fbb1bd", "#ff99ac", "#ff7096", "#ff5c8a", "#ff477e"]



# fbb1bd
# ff99ac
# ff85a1
# ff7096
# ff5c8a
# ff477e



st.markdown("---")

