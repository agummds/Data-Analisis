import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

# Dashboard title
st.title("Dashboard Penyewaan Sepeda :bike:")

# Sidebar
st.sidebar.header("Side Bar :sparkles:")
dataset_option = st.sidebar.radio("Pilih Dataset", ("Harian", "Jam"))

# Fitur Search Rentang Tanggal
if dataset_option == "Harian":
    st.subheader("Data Penyewaan Sepeda Harian")
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    start_date = st.sidebar.date_input("Mulai Tanggal", day_df["dteday"].min())
    end_date = st.sidebar.date_input("Akhir Tanggal", day_df["dteday"].max())
    filtered_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]
    st.dataframe(filtered_df)
else:
    st.subheader("Data Penyewaan Sepeda Per Jam")
    st.dataframe(hour_df)

# Statistik dasar
st.subheader("Statistik Data")
st.write(day_df.describe() if dataset_option == "Harian" else hour_df.describe())

# Visualisasi jumlah penyewaan berdasarkan waktu
st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=day_df["mnth"], y=day_df["cnt"], palette="Blues", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# Visualisasi jumlah penyewaan berdasarkan jam
st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(10, 5))
hourly_rentals = hour_df.groupby("hr")["cnt"].mean()
sns.lineplot(x=hourly_rentals.index, y=hourly_rentals.values, marker="o", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
st.pyplot(fig)


@st.cache_data
def load_data():
    day_df = pd.read_csv("../data/day.csv")  # Ganti dengan lokasi file dataset
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    day_df["week"] = day_df["dteday"].dt.isocalendar().week
    day_df["year"] = day_df["dteday"].dt.year
    return day_df

day_df = load_data()
last_date = day_df["dteday"].max()

# RFM Mingguan
weekly_rfm = day_df.groupby(["year", "week"]).agg(
    Recency=("dteday", lambda x: (last_date - x.max()).days),
    Frequency=("dteday", "count"),
    Monetary=("cnt", "sum")
).reset_index()

# RFM Musiman
season_rfm = day_df.groupby("season").agg(
    Recency=("dteday", lambda x: (last_date - x.max()).days),
    Frequency=("dteday", "count"),
    Monetary=("cnt", "sum")
).reset_index()

season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_rfm["season"] = season_rfm["season"].map(season_map)

# Sidebar untuk Filter
st.sidebar.header("Filter Data RFM")
year_filter = st.sidebar.selectbox("Pilih Tahun", sorted(day_df["year"].unique()), index=0)
weekly_rfm_filtered = weekly_rfm[weekly_rfm["year"] == year_filter]

st.title("📊 RFM Analysis Dashboard")

# 🚀 **1. Tabel RFM Mingguan**
st.subheader(f"📅 RFM Mingguan - Tahun {year_filter}")
st.dataframe(weekly_rfm_filtered)

# 🚀 **2. Grafik RFM Mingguan**
st.subheader("📈 Visualisasi RFM Mingguan")

fig, ax = plt.subplots(1, 3, figsize=(18, 5))

# Recency
sns.barplot(x=weekly_rfm_filtered["week"], y=weekly_rfm_filtered["Recency"], ax=ax[0], color="salmon")
ax[0].set_title("Recency Mingguan")

# Frequency
sns.lineplot(x=weekly_rfm_filtered["week"], y=weekly_rfm_filtered["Frequency"], ax=ax[1], marker="o", color="blue")
ax[1].set_title("Frequency Mingguan")

# Monetary
sns.barplot(x=weekly_rfm_filtered["week"], y=weekly_rfm_filtered["Monetary"], ax=ax[2], color="green")
ax[2].set_title("Monetary Mingguan")

st.pyplot(fig)

# 🚀 **3. Tabel RFM Musiman**
st.subheader("❄️🌞 RFM Musiman")
st.dataframe(season_rfm)

# 🚀 **4. Grafik RFM Musiman**
st.subheader("📊 Visualisasi RFM Musiman")

fig, ax = plt.subplots(1, 3, figsize=(15, 5))

sns.barplot(x=season_rfm["season"], y=season_rfm["Recency"], ax=ax[0], palette="Reds")
ax[0].set_title("Recency Musiman")

sns.barplot(x=season_rfm["season"], y=season_rfm["Frequency"], ax=ax[1], palette="Blues")
ax[1].set_title("Frequency Musiman")

sns.barplot(x=season_rfm["season"], y=season_rfm["Monetary"], ax=ax[2], palette="Greens")
ax[2].set_title("Monetary Musiman")

st.pyplot(fig)

# Copyright
st.markdown("---")
st.markdown("© 2025 Agum Medisa")
