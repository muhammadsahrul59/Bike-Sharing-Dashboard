import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# load dataset

df = pd.read_csv("https://raw.githubusercontent.com/muhammadsahrul59/Bike-Sharing-Dashboard/main/dashboard/cleaned_bikeshare.csv")
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

def create_season_temperature_df(df):
    season_temperature_df = df.groupby(['season', 'temp']).agg({
        'cnt': 'sum'
    }).reset_index()
    return season_temperature_df

def create_weather_rides_df(df):
    weather_rides_df = df.groupby('weathersit').agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    weather_rides_df = pd.melt(weather_rides_df, id_vars=['weathersit'], 
                               value_vars=['casual', 'registered'], 
                               var_name='type_of_rides', 
                               value_name='count_rides')

    weather_rides_df['weathersit'] = weather_rides_df['weathersit'].replace({
        1: 'Clear',
        2: 'Mist',
        3: 'Light Rain/Snow',
        4: 'Heavy Rain/Snow'
    })
    return weather_rides_df

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

st.markdown("""
    <style>
        .sidebar .markdown-text-container span {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.header("Visit my Profile:")
st.sidebar.markdown("Muhammad Sahrul")

col1, col2, col3 = st.sidebar.columns(3)

with col1:
    st.markdown("[![LinkedIn](https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg)](https://www.linkedin.com/in/sahrul59/)")
with col2:
    st.markdown("[![Github](https://raw.github.com/muhammadsahrul59/Bike-Sharing-Dashboard/main/image/GitHub_Invertocat_Logo.png)](https://github.com/muhammadsahrul59/)")
with col3:
    st.markdown("[![Instagram](https://raw.github.com/muhammadsahrul59/Bike-Sharing-Dashboard/main/image/Instagram_logo_2022.png)](https://www.instagram.com/sahrullss/)")


st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #90C7AC;
    }
</style>
""", unsafe_allow_html=True)

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
season_temperature_df = create_season_temperature_df(main_df)
weather_rides_df = create_weather_rides_df(main_df)

# ----- MAINPAGE -----
st.markdown("<h1 style='text-align: center;'>🚲 Bike-Sharing Dashboard 💫</h1>", unsafe_allow_html=True)
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
              markers=True,
              title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

fig2 = px.bar(seasonly_users_df,
              x='season',
              y=['count_rides'],
              color='type_of_rides',
              title='Count of Bikeshare Rides by Season').update_layout(xaxis_title='', yaxis_title='Total Rides')

fig3 = px.bar(weekday_users_df,
              x='weekday',
              y=['count_rides'],
              color='type_of_rides',
              barmode='group',
              title='Count of Bikeshare Rides by Weekday').update_layout(xaxis_title='', yaxis_title='Total Rides')


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig2, use_container_width=True)
right_column.plotly_chart(fig3, use_container_width=True)

fig4 = px.line(hourly_users_df,
              x="hr",
              y=['casual_rides', 'registered_rides'],
              markers=True,
              title='Count of Bikeshare Rides by Hour').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig4, use_container_width=True)

# Plotting scatter plots for each season

fig5 = px.scatter(season_temperature_df, x='temp', y='cnt', color='season', 
                                    title='Clusters of Bikeshare Rides Count by Temperature in Different Seasons',
                                    labels={'cnt': 'Total Rides', 'temp': 'Temperature (Celsius)'},
                                    facet_col='season', facet_col_wrap=2, 
                                    color_discrete_map={'Winter': 'blue', 'Spring': 'green', 'Summer': 'orange', 'Fall': 'red'},
                                    hover_name='temp', hover_data={'temp': False})

fig5.update_traces(showlegend=True)

st.plotly_chart(fig5, use_container_width=True)

# Grouping by weather and aggregating total casual and registered rides

fig6 = px.bar(weather_rides_df, x='weathersit', y='count_rides', 
              color='type_of_rides', barmode='group', 
              title='Count of Bikeshare Rides by Weather Condition',
              labels={'count_rides': 'Total Rides', 'weathersit': 'Weather Condition'},
              color_discrete_map={'casual': 'orange', 'registered': 'blue'})

# Adding legend
fig6.update_layout(legend_title_text='Type of Rides')

# Displaying the plot
st.plotly_chart(fig6, use_container_width=True)


# Calculate total casual and registered rides
total_casual_rides = main_df['casual'].sum()
total_registered_rides = main_df['registered'].sum()

# Create data for pie chart
pie_data = pd.DataFrame({
    'Type of Rides': ['Casual', 'Registered'],
    'Total Rides': [total_casual_rides, total_registered_rides]
})

fig7 = px.pie(pie_data,
                 values='Total Rides',
                 names='Type of Rides', 
                 title='Distribution of Rides'
                 )

st.plotly_chart(fig7, use_container_width=True)

st.markdown("<p style='text-align: right; font-size: small;'>Copyright (c), created by Muhammad Sahrul</p>", unsafe_allow_html=True)

# HIDE STREAMLIT STYLE
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)