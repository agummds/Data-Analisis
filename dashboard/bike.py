import streamlit as st
import pandas as pd

# Load dataset
day_df = pd.read_csv("https://github.com/agummds/Data-Analisis/blob/master/data/day.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

time_df = pd.read_csv("https://github.com/agummds/Data-Analisis/blob/master/data/hour.csv")
time_df['dteday'] = pd.to_datetime(time_df['dteday'])

# Streamlit UI
st.title("🚲 Bike Sharing Dashboard")
st.sidebar.header("Filter Data")

# Date Range Filter
date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal", 
    [day_df['dteday'].min(), day_df['dteday'].max()],
    min_value=day_df['dteday'].min(), 
    max_value=day_df['dteday'].max()
)

# Season Filter
seasons = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
day_df['season_label'] = day_df['season'].map(seasons)
selected_season = st.sidebar.multiselect("Pilih Musim", options=seasons.values(), default=list(seasons.values()))

# Hour Filter
selected_hour = st.sidebar.slider("Pilih Jam", min_value=0, max_value=23, value=(0, 23))

# Weekly Filter
day_df['week'] = day_df['dteday'].dt.isocalendar().week
selected_week = st.sidebar.multiselect("Pilih Minggu", options=sorted(day_df['week'].unique()), default=sorted(day_df['week'].unique()))

# Filter dataset
filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(date_range[0])) &
                      (day_df['dteday'] <= pd.to_datetime(date_range[1])) &
                      (day_df['season_label'].isin(selected_season)) &
                      (day_df['week'].isin(selected_week))]

time_filtered_df = time_df[(time_df['dteday'] >= pd.to_datetime(date_range[0])) &
                            (time_df['dteday'] <= pd.to_datetime(date_range[1])) &
                            (time_df['hr'] >= selected_hour[0]) &
                            (time_df['hr'] <= selected_hour[1])]

# Visualisasi Penyewaan Sepeda per Hari (Bar Chart)
st.subheader("Jumlah Penyewaan Sepeda per Hari")
fig = px.bar(filtered_df, x='dteday', y='cnt', title='Jumlah Penyewaan Sepeda per Hari')
st.plotly_chart(fig)

# Visualisasi Penyewaan Sepeda per Musim (Pie Chart)
st.subheader("Distribusi Penyewaan Sepeda per Musim")
fig_pie = px.pie(filtered_df, names='season_label', values='cnt', title='Distribusi Penyewaan Sepeda per Musim')
st.plotly_chart(fig_pie)

# Visualisasi Suhu vs Penyewaan
st.subheader("Pengaruh Suhu terhadap Penyewaan")
fig2 = px.scatter(filtered_df, x='temp', y='cnt', title='Suhu vs Penyewaan', trendline='ols')
st.plotly_chart(fig2)

# Copyright
st.markdown("---")
st.markdown("© 2025 Agum Medisa")
