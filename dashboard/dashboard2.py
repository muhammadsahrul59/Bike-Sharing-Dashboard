import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# load dataset

df = pd.read_csv("https://raw.githubusercontent.com/muhammadsahrul59/Bike-Sharing-Dashboard/main/dashboard/all_dailysharing_df.csv")
df['dteday'] = pd.to_datetime(df['dteday'])


st.set_page_config(page_title="Bike-sharing Dashboard",
                   page_icon="🚲",
                   layout="wide")


# create helper functions

def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday": "yearmonth",
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['weekday'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekday_users_df = weekday_users_df.sort_values('weekday')
    
    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return hourly_users_df

# make filter components

min_date = df["dteday"].min()
max_date = df["dteday"].max()

# SIDEBAR 

with st.sidebar:
    # add bikeshare logo
    st.image("https://raw.github.com/muhammadsahrul59/Bike-Sharing-Dashboard/main/image/bikesharing_logo.png")

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Time Span", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.sidebar.header("Visit my Profile:")

st.sidebar.markdown("Muhammad Sahrul")

col1, col2, col3 = st.sidebar.columns(3)

with col1:
    st.markdown("[![LinkedIn](https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg)](https://www.linkedin.com/in/sahrul59/)")
with col2:
    st.markdown("[![Github](https://raw.github.com/muhammadsahrul59/Bike-Sharing-Dashboard/main/image/GitHub_Invertocat_Logo.png)](https://github.com/muhammadsahrul59/)")
with col3:
    st.markdown("[![Instagram](https://raw.github.com/muhammadsahrul59/Bike-Sharing-Dashboard/main/image/Instagram_logo_2022.png)](https://www.instagram.com/sahrullss/)")

# hubungkan filter dengan main_df

main_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]

# assign main_df ke helper functions yang telah dibuat sebelumnya

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)

# ----- MAINPAGE -----
st.title("🚲 Bike-Sharing Dashboard :sparkles:")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['cnt'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")

# CHART 
fig = px.line(monthly_users_df,
              x='yearmonth',
              y=['casual_rides', 'registered_rides', 'total_rides'],
              color_discrete_sequence=px.colors.qualitative.Pastel,
              markers=True,
              title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

fig1 = px.bar(seasonly_users_df,
              x='season',
              y=['count_rides'],
              color='type_of_rides',
              color_discrete_sequence=px.colors.qualitative.Pastel,
              title='Count of bikeshare rides by season').update_layout(xaxis_title='', yaxis_title='Total Rides')

fig2 = px.bar(weekday_users_df,
              x='weekday',
              y=['count_rides'],
              color='type_of_rides',
              barmode='group',
              color_discrete_sequence=px.colors.qualitative.Pastel,
              title='Count of bikeshare rides by weekday').update_layout(xaxis_title='', yaxis_title='Total Rides')


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

fig = px.line(hourly_users_df,
              x='hr',
              y=['casual_rides', 'registered_rides'],
              color_discrete_sequence=px.colors.qualitative.Pastel,
              markers=True,
              title='Count of bikeshare rides by hour of day').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)
# Histogram of daily total rides
fig3 = px.histogram(main_df,
                    x='cnt',
                    nbins=30,
                    title='Distribution of Daily Total Rides',
                    labels={'cnt': 'Total Rides', 'count': 'Number of Days'},
                    color_discrete_sequence=px.colors.qualitative.Pastel)

st.plotly_chart(fig3, use_container_width=True)
# Calculate total casual and registered rides
total_casual_rides = main_df['casual'].sum()
total_registered_rides = main_df['registered'].sum()

# Create data for pie chart
pie_data = pd.DataFrame({
    'Type of Rides': ['Casual', 'Registered'],
    'Total Rides': [total_casual_rides, total_registered_rides]
})

fig_pie = px.pie(pie_data,
                 values='Total Rides',
                 names='Type of Rides', 
                 title='Distribution of Rides (Casual vs Registered)',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig_pie, use_container_width=True)

st.caption('Copyright (c), created by Muhammad Sahrul')

# HIDE STREAMLIT STYLE
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)