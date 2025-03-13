import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data (kamu bisa ganti ini dengan file data kamu)
@st.cache_data
def load_data():
    data = pd.read_csv("main_data.csv")
    return data

data = load_data()

# Sidebar untuk filter
st.sidebar.header("Filter Data")
workingday_filter = st.sidebar.selectbox("Pilih Hari Kerja atau Akhir Pekan:", ["Semua", "Hari Kerja", "Akhir Pekan"])
weather_filter = st.sidebar.selectbox("Pilih Kondisi Cuaca:", ["Semua", "Cerah", "Mendung", "Hujan Ringan"])

# Filter data
filtered_data = data.copy()
if workingday_filter != "Semua":
    workingday_mapping = {"Hari Kerja": 1, "Akhir Pekan": 0}
    filtered_data = filtered_data[filtered_data['workingday'] == workingday_mapping[workingday_filter]]
if weather_filter != "Semua":
    weather_mapping = {"Cerah": 1, "Mendung": 2, "Hujan Ringan": 3}
    filtered_data = filtered_data[filtered_data['weathersit'] == weather_mapping[weather_filter]]

# Visualisasi pola penggunaan sepeda
st.header("Pola Penggunaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 6))
avg_usage = filtered_data.groupby('workingday')[['casual', 'registered']].mean().reset_index()
avg_usage['workingday'] = avg_usage['workingday'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})

avg_usage.set_index('workingday').plot(kind='bar', ax=ax, color=['#3498db', '#2ecc71'])
plt.title('Rata-Rata Jumlah Pengguna Sepeda')
plt.xlabel('')
plt.ylabel('Jumlah Pengguna')
plt.xticks(rotation=0)
st.pyplot(fig)

# Visualisasi pengaruh cuaca
st.header("Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda")
fig2, ax2 = plt.subplots(figsize=(10, 6))
weather_avg = filtered_data.groupby('weathersit')[['casual', 'registered']].mean().reset_index()
weather_avg['weathersit'] = weather_avg['weathersit'].map({1: 'Cerah', 2: 'Mendung', 3: 'Hujan Ringan'})

weather_avg.set_index('weathersit').plot(kind='bar', ax=ax2, color=['#3498db', '#2ecc71'])
plt.title('Rata-Rata Peminjaman Berdasarkan Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Pengguna')
plt.xticks(rotation=0)
st.pyplot(fig2)

# Insight section
st.header("Insight & Kesimpulan")
st.markdown("""
- **Pengguna casual lebih aktif di akhir pekan**, sedangkan **registered lebih aktif saat hari kerja**.
- **Cuaca cerah meningkatkan peminjaman**, terutama untuk pengguna casual.
- **Hujan ringan mengurangi peminjaman drastis untuk casual**, walaupun registered lebih stabil.

➡️ **Rekomendasi Strategi:**
1. **Promo & event saat akhir pekan** untuk menarik pengguna casual.
2. **Fasilitas pendukung komuter saat weekday** untuk loyalitas registered.
3. **Jas hujan gratis atau notifikasi cuaca** untuk mempertahankan peminjaman saat cuaca buruk.

✨ Dengan strategi ini, bisnis bisa **lebih fleksibel & tahan cuaca**! 🚴‍♀️
""")
