import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
plt.rcParams['figure.figsize'] = (20.0, 10.0)
from babel.numbers import format_currency
sns.set(style='dark')

all_df = pd.read_csv("main_data.csv")
 

with st.sidebar:
    # Menambahkan logo perusahaan
    st.sidebar.header('Dashboard `BIKE SHARE`')
    st.image("https://th.bing.com/th/id/OIP.up96mXJZb59GCdvWuRrFswHaFj?pid=ImgDet&rs=1")
    st.sidebar.markdown('''
                        ---
                        Created by Muhammad Sahrul
                        ''')
    
st.header('Bike Share Dashboard :sparkles:')

df = pd.read_csv("main_data.csv")

st.subheader('Musim mempengaruhi penggunaan bikeshare')
col1,col2 = st.columns((7,4))

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(data=df[['season','cnt']],
                x='season',
                y='cnt',
                ax=ax)
    plt.title('Capital Bikeshare Ridership by Season')
    plt.ylabel('Total Rides')
    plt.xlabel('Season')

    tick_val=[0, 1, 2, 3]
    tick_lab=['Winter', 'Spring', 'Summer', 'Fall']
    plt.xticks(tick_val, tick_lab)

    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots()
    sns.barplot(data=df[['mnth','cnt']], x='mnth', y='cnt', ax=ax)

    plt.title('Capital Bikeshare Ridership by Month')
    plt.ylabel('Total Rides')
    plt.xlabel('Month')

    tick_val=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    tick_lab=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    plt.xticks(rotation=45)
    plt.xticks(tick_val, tick_lab)

    st.pyplot(fig)

st.subheader('Tren penggunaan berdasarkan jenis membership')

fig, ax = plt.subplots()
sns.pointplot(data=df[['mnth', 'casual', 'registered']],
              x='mnth',
              y='casual',
              ax=ax,
              color='orange')

sns.pointplot(data=df[['mnth', 'casual', 'registered']],
              x='mnth',
              y='registered',
              ax=ax,
              color='green')

tick_val=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
tick_lab=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
plt.xticks(tick_val, tick_lab)
plt.xticks(rotation=45)

plt.title('Casual and Registered Bikeshare Ridership by Month')
plt.ylabel('Total Rides')
plt.xlabel('Month')

st.pyplot(fig)

st.subheader('Cuaca mempengaruhi penggunaan bikeshare')

df_weathersit = df.groupby('weathersit').instant.nunique().reset_index()
df_weathersit.rename(columns={'instant': 'sum'}, inplace=True)

fig = plt.figure(figsize=(5, 4))
sns.barplot(
    data=df_weathersit.sort_values('weathersit', ascending=False),
    x='weathersit',
    y='sum',
)

plt.title('Jumlah Bike Sharing Berdasarkan Cuaca')
plt.xlabel('Cuaca')
plt.ylabel('Jumlah')
st.pyplot(fig)

